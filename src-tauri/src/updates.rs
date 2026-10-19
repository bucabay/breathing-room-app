//! Only native code chooses the feed/key and retains the exact checked release.
use serde::{Deserialize, Serialize};
use std::{sync::{atomic::{AtomicBool, Ordering}, Mutex}, time::Duration};
use tauri::{AppHandle, Emitter, State};
use tauri_plugin_updater::{Update, UpdaterExt};

#[derive(Deserialize)]
#[serde(rename_all = "camelCase")]
struct Config { endpoint: Option<String>, public_key: Option<String> }
impl Config {
    fn validated(self) -> Result<Option<(reqwest::Url, String)>, String> {
        match (self.endpoint.filter(|v| !v.trim().is_empty()), self.public_key.filter(|v| !v.trim().is_empty())) {
            (None, None) => Ok(None),
            (Some(endpoint), Some(key)) => { let url = secure_url(&endpoint)?; Ok(Some((url, key))) },
            _ => Err("App updates need both a release feed and a signing public key.".into()),
        }
    }
}
fn secure_url(value: &str) -> Result<reqwest::Url, String> {
    let url = reqwest::Url::parse(value).map_err(|_| "Invalid update URL")?;
    if url.scheme() != "https" || url.host_str().is_none() || !url.username().is_empty() || url.password().is_some() || url.fragment().is_some() {
        return Err("App updates require an HTTPS URL without embedded credentials.".into());
    }
    Ok(url)
}

#[derive(Default)]
pub(crate) struct UpdateState {
    busy: AtomicBool,
    pending: Mutex<Option<Update>>,
    installed: AtomicBool,
}
struct Busy<'a>(&'a AtomicBool);
impl Drop for Busy<'_> { fn drop(&mut self) { self.0.store(false, Ordering::Release); } }
impl UpdateState {
    fn begin(&self) -> Result<Busy<'_>, String> {
        self.busy.compare_exchange(false, true, Ordering::AcqRel, Ordering::Acquire).map_err(|_| "An update operation is already running.")?;
        Ok(Busy(&self.busy))
    }
}
#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
pub(crate) struct CheckResult { configured: bool, current_version: String, version: Option<String>, notes: Option<String>, installed: bool }

#[tauri::command]
pub(crate) async fn check_app_update(app: AppHandle, state: State<'_, UpdateState>) -> Result<CheckResult, String> {
    let _busy = state.begin()?;
    let current_version = app.package_info().version.to_string();
    if state.installed.load(Ordering::Acquire) {
        return Ok(CheckResult { configured: true, current_version, version: None, notes: None, installed: true });
    }
    let config: Config = serde_json::from_str(include_str!("../update-config.json")).map_err(|_| "Invalid app update configuration")?;
    let configured = config.validated()?;
    if configured.is_none() || crate::native::sandboxed() {
        return Ok(CheckResult { configured: false, current_version, version: None, notes: None, installed: false });
    }
    let (url, key) = configured.unwrap();
    let update = app.updater_builder().pubkey(key).endpoints(vec![url]).map_err(|e| e.to_string())?
        .configure_client(|client| client.https_only(true))
        .timeout(Duration::from_secs(30)).build().map_err(|e| e.to_string())?.check().await.map_err(|e| e.to_string())?;
    if let Some(update) = &update { secure_url(update.download_url.as_str())?; }
    let result = CheckResult { configured: true, current_version, version: update.as_ref().map(|u| u.version.clone()), notes: update.as_ref().and_then(|u| u.body.clone()), installed: false };
    *state.pending.lock().map_err(|_| "Update state unavailable")? = update;
    Ok(result)
}

#[tauri::command]
pub(crate) async fn install_app_update(app: AppHandle, state: State<'_, UpdateState>, version: String) -> Result<(), String> {
    let _busy = state.begin()?;
    if state.installed.load(Ordering::Acquire) { return Err("The update is installed. Restart when ready.".into()); }
    let mut update = state.pending.lock().map_err(|_| "Update state unavailable")?.clone().ok_or("Check for an update first.")?;
    if update.version != version { return Err("The available update changed. Check again before installing.".into()); }
    secure_url(update.download_url.as_str())?;
    crate::runtime_store::require_no_active_agent(&crate::system::user_home()?)?;
    update.timeout = Some(Duration::from_secs(300));
    let mut downloaded = 0u64;
    let bytes = update.download(|chunk, total| {
        downloaded = downloaded.saturating_add(chunk as u64);
        let _ = app.emit_to("main", "app-update-progress", serde_json::json!({"downloaded":downloaded,"total":total}));
    }, || {}).await.map_err(|e| e.to_string())?;
    // Download is read-only; block new maintenance starts only during replacement.
    tauri::async_runtime::spawn_blocking(move || {
        let _gate = crate::update_gate::exclusive()?;
        crate::runtime_store::require_no_active_agent(&crate::system::user_home()?)?;
        update.install(&bytes).map_err(|e| e.to_string())
    }).await.map_err(|e| e.to_string())??;
    state.installed.store(true, Ordering::Release);
    *state.pending.lock().map_err(|_| "Update state unavailable")? = None;
    Ok(())
}

#[tauri::command]
pub(crate) fn restart_after_update(app: AppHandle, state: State<'_, UpdateState>) -> Result<(), String> {
    let _busy = state.begin()?;
    if !state.installed.load(Ordering::Acquire) { return Err("No installed update is waiting for a restart.".into()); }
    let _gate = crate::update_gate::exclusive()?;
    crate::runtime_store::require_no_active_agent(&crate::system::user_home()?)?;
    app.restart();
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test] fn unconfigured_updates_are_disabled_not_reported_up_to_date() {
        assert!(Config { endpoint: None, public_key: None }.validated().unwrap().is_none());
        assert!(Config { endpoint: Some("https://updates.example.test/latest.json".into()), public_key: None }.validated().is_err());
    }
    #[test] fn feed_and_artifacts_require_https_without_credentials() {
        for value in ["http://example.test/update", "file:///tmp/update", "https://token@example.test/update", "https://example.test/update#fragment"] { assert!(secure_url(value).is_err()); }
        assert!(secure_url("https://updates.example.test/latest.json").is_ok());
    }
    #[test] fn update_operations_are_serialized_and_failures_release_the_lock() {
        let state = UpdateState::default(); let busy = state.begin().unwrap();
        assert!(state.begin().is_err()); drop(busy); assert!(state.begin().is_ok());
    }
}
