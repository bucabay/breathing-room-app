pub mod model;
pub mod cleanup_session;
mod cleanup_discovery;
mod discovery_inventory;
mod review_storage;
mod recent_space;
mod discovery_rules;
pub mod disk_map_cache;
pub mod runtime_store;
pub mod remote_agent;
mod cleanup_tools;
mod discovery_terminal;
mod system_tools;
pub mod anomalies;
#[cfg(feature = "gui")]
pub mod assistant;
#[cfg(feature = "gui")]
pub mod monitor;
#[cfg(feature = "gui")]
mod fswatch;
#[cfg(feature = "gui")]
mod native;
#[cfg(feature = "gui")]
mod activity_panel;
pub mod processes;
#[cfg(feature = "gui")]
mod state;
pub mod storage;
mod system;
pub mod daily_care;
mod update_gate;
#[cfg(feature = "gui")]
mod updates;

#[cfg(feature = "gui")]
pub(crate) mod gui {
    use super::*;
    use std::{
        sync::{atomic::Ordering, Arc},
        time::Duration,
    };
    use tauri::{Emitter, Manager, State};
    type Shared = Arc<state::Engine>;
    pub(crate) struct MonitorService { pub(crate) monitor: Option<Arc<monitor::Monitor>>, error: String }
    #[tauri::command]
    fn live_status(service: State<'_, MonitorService>) -> serde_json::Value {
        service.monitor.as_ref().map(|m|{m.refresh_disk();m.live()}).unwrap_or_else(||serde_json::json!({"ready":false,"databaseError":service.error}))
    }
    #[tauri::command]
    async fn activity_log(filter: String, search: String, before: i64, service: State<'_, MonitorService>) -> Result<serde_json::Value,String> {
        if !["all","files","processes"].contains(&filter.as_str()) || search.len()>500 || before<0 { return Err("Invalid activity query".into()); }
        let monitor=service.monitor.as_ref().ok_or("Activity database unavailable")?.clone();
        tauri::async_runtime::spawn_blocking(move||monitor.history(&filter,&search,before)).await.map_err(|e|e.to_string())?
    }
    #[tauri::command]
    fn configure_monitor(config: monitor::Config, service: State<'_, MonitorService>) -> Result<(),String> {
        service.monitor.as_ref().ok_or("Monitor unavailable")?.configure(config)
    }

    fn scopes(engine: &Shared) -> Vec<native::Scope> {
        let bookmarks = engine
            .data
            .lock()
            .map(|data| data.bookmarks.clone())
            .unwrap_or_default();
        bookmarks
            .values()
            .filter_map(|b| native::scope(b).ok())
            .collect()
    }

    #[tauri::command]
    async fn scan_storage(engine: State<'_, Shared>) -> Result<model::StorageReport, String> {
        let engine = engine.inner().clone();
        tauri::async_runtime::spawn_blocking(move || {
            let _guard = engine.begin("Checking storage", "Reading accessible folders and file sizes", "space")?;
            engine.cancel.store(false, Ordering::Relaxed);
            let _scopes = scopes(&engine);
            let settings = engine
                .data
                .lock()
                .map_err(|_| "Settings unavailable")?
                .settings
                .clone();
            let report = storage::scan(&settings, &engine.cancel)?;
            *engine
                .last_scan_files
                .lock()
                .map_err(|_| "Scan state unavailable")? = report.large_files.clone();
            Ok(report)
        })
        .await
        .map_err(|e| e.to_string())?
    }
    #[tauri::command]
    fn cancel_scan(engine: State<'_, Shared>) {
        engine.cancel.store(true, Ordering::Relaxed);
    }
    #[tauri::command]
    fn get_capabilities() -> serde_json::Value {
        capabilities()
    }
    #[tauri::command]
    fn get_activity(engine: State<'_, Shared>) -> Result<Option<state::Activity>, String> {
        Ok(engine.activity.lock().map_err(|_| "Activity unavailable")?.clone())
    }
    #[tauri::command]
    async fn cached_volume() -> Result<Option<serde_json::Value>, String> {
        tauri::async_runtime::spawn_blocking(disk_map_cache::load).await.map_err(|error|error.to_string())?
    }
    #[tauri::command]
    async fn scan_volume(app: tauri::AppHandle, engine: State<'_, Shared>) -> Result<serde_json::Value, String> {
        let engine = engine.inner().clone();
        tauri::async_runtime::spawn_blocking(move || {
            let cached = disk_map_cache::load().ok().flatten().is_some();
            let _guard = engine.begin_disk_map(if cached { "Refreshing disk map" } else { "Mapping your whole disk" }, if cached { "Updating saved storage results in the background" } else { "df, du and APFS accounting · may take up to three minutes" })?;
            let _scopes = scopes(&engine);
            assistant::space(&app)
        }).await.map_err(|e| e.to_string())?
    }
    #[tauri::command]
    async fn browse_storage(app: tauri::AppHandle, path: String) -> Result<serde_json::Value, String> {
        tauri::async_runtime::spawn_blocking(move || assistant::browse(&app, path)).await.map_err(|e| e.to_string())?
    }
    #[tauri::command]
    async fn agent_cleanup_connection() -> Result<serde_json::Value,String> {
        tauri::async_runtime::spawn_blocking(cleanup_session::connection).await.map_err(|e|e.to_string())
    }
    #[tauri::command]
    fn open_trash()->Result<(),String>{native::open_trash()}
    #[tauri::command]
    async fn assistant_message(message:String,history:serde_json::Value,automatic:Option<bool>,limits:Option<cleanup_discovery::Policy>,engine:State<'_,Shared>,service:State<'_,MonitorService>)->Result<serde_json::Value,String>{
        let settings=engine.data.lock().map_err(|_|"Settings unavailable")?.settings.clone();
        let options=cleanup_discovery::Options{profiles:settings.profiles,roots:settings.scan_paths,policy:limits.unwrap_or_default(),daily_care:false};
        let monitor=service.monitor.clone();
        tauri::async_runtime::spawn_blocking(move||{
            let home=system::user_home()?;let request=message.clone();
            remote_agent::message(message,history,move|name,args|match name{
                "start_disk_discovery"=>{let id=cleanup_session::inspect_configured(request.clone(),args["scope"].as_str().unwrap_or("").into(),automatic.unwrap_or(false),options.clone())?;Ok(serde_json::json!({"runId":id,"status":"inspecting","note":"Parallel discovery started. No cleanup was approved. Findings will appear in the native review UI."}))},
                "inspect_activity"=>{
                    let monitor=monitor.as_ref().ok_or("Activity monitor unavailable")?;
                    let filter=args["filter"].as_str().unwrap_or("all");if !["all","files","processes"].contains(&filter){return Err("Unknown activity filter".into());}
                    let live=monitor.live();let mut history=monitor.history(filter,"",0)?;
                    if let Some(rows)=history["events"].as_array_mut(){rows.truncate(20);}
                    if let Some(rows)=history["diskHistory"].as_array_mut(){let skip=rows.len().saturating_sub(60);rows.drain(..skip);}
                    Ok(serde_json::json!({"timestamp":model::now(),"monitoring":live["config"],"sampleTimestamp":live["timestamp"],"watching":live["watching"],"watchError":live["watchError"],"droppedEvents":live["dropped"],"history":history,"note":"Existing observations only; monitoring was not enabled or changed. Path-inferred ownership is not proven writer attribution. History may have gaps and includes records before monitoring was paused."}))
                },
                _=>system_tools::inspect(&home,name,args)
            })
        }).await.map_err(|e|e.to_string())?
    }
    #[tauri::command]
    async fn agent_cleanup_inspect(request:String,scope:String,model:String,automatic:Option<bool>,limits:Option<cleanup_discovery::Policy>,daily:Option<bool>,engine:State<'_,Shared>)->Result<String,String>{let _=model;let daily=daily.unwrap_or(false);let shared=engine.inner().clone();let settings=engine.data.lock().map_err(|_|"Settings unavailable")?.settings.clone();let options=cleanup_discovery::Options{profiles:settings.profiles,roots:settings.scan_paths,policy:limits.unwrap_or_default(),daily_care:daily};tauri::async_runtime::spawn_blocking(move||{let id=cleanup_session::inspect_configured(request,scope,automatic.unwrap_or(false),options)?;if daily{shared.data.lock().map_err(|_|"Settings unavailable")?.last_daily_day=system::local_day_hour().0;shared.save()?;}Ok(id)}).await.map_err(|e|e.to_string())?}
    #[tauri::command]
    async fn daily_approvals()->Result<Vec<daily_care::Approval>,String>{tauri::async_runtime::spawn_blocking(daily_care::approvals).await.map_err(|e|e.to_string())?}
    #[tauri::command]
    async fn revoke_daily_approval(key:String)->Result<(),String>{tauri::async_runtime::spawn_blocking(move||daily_care::revoke(key)).await.map_err(|e|e.to_string())?}
    #[tauri::command]
    async fn daily_notifications()->Result<Vec<daily_care::Notification>,String>{tauri::async_runtime::spawn_blocking(daily_care::notifications).await.map_err(|e|e.to_string())?}
    #[tauri::command]
    async fn mark_daily_notification_seen(id:String)->Result<(),String>{tauri::async_runtime::spawn_blocking(move||daily_care::mark_seen(id)).await.map_err(|e|e.to_string())?}
    #[tauri::command]
    async fn agent_cleanup_inventory(id:String,offset:Option<usize>,category:Option<String>)->Result<serde_json::Value,String>{tauri::async_runtime::spawn_blocking(move||cleanup_session::inventory_page(id,offset.unwrap_or(0),category)).await.map_err(|e|e.to_string())?}
    #[tauri::command]
    fn agent_cleanup_state(id:String)->Result<cleanup_session::Run,String>{cleanup_session::state(id)}
    #[tauri::command]
    async fn agent_cleanup_approve(id:String,ids:Vec<String>)->Result<(),String>{tauri::async_runtime::spawn_blocking(move||cleanup_session::approve(id,ids)).await.map_err(|e|e.to_string())?}
    #[tauri::command]
    fn agent_cleanup_cancel(id:String)->Result<(),String>{cleanup_session::cancel(id)}
    #[tauri::command]
    fn agent_cleanup_latest()->Result<Option<cleanup_session::Run>,String>{cleanup_session::latest()}
    #[tauri::command]
    async fn agent_cleanup_resume(id:String)->Result<(),String>{tauri::async_runtime::spawn_blocking(move||cleanup_session::resume(id)).await.map_err(|e|e.to_string())?}
    #[tauri::command]
    async fn agent_auth_start(provider:String)->Result<serde_json::Value,String>{tauri::async_runtime::spawn_blocking(move||remote_agent::auth_start(provider)).await.map_err(|e|e.to_string())?}
    #[tauri::command]
    async fn agent_auth_poll(id:String)->Result<serde_json::Value,String>{tauri::async_runtime::spawn_blocking(move||remote_agent::auth_poll(id)).await.map_err(|e|e.to_string())?}
    #[tauri::command]
    async fn agent_auth_logout()->Result<(),String>{tauri::async_runtime::spawn_blocking(remote_agent::logout).await.map_err(|e|e.to_string())?}
    #[tauri::command]
    fn agent_api_configure(url:String)->Result<(),String>{remote_agent::configure(url)}
    #[tauri::command]
    async fn open_ai_care_checkout(url:String)->Result<(),String>{
        let config:serde_json::Value=serde_json::from_str(include_str!("../../src/billing-config.json")).map_err(|_|"Invalid billing configuration")?;
        let plan=if config["stripeSubscriptionUrl"].as_str()==Some(url.as_str()){"monthly"}else if config["stripeAnnualUrl"].as_str()==Some(url.as_str()){"annual"}else{return Err("Choose a configured AI Care plan".into());};
        // The UI's public link identifies the plan, not the destination. Native
        // authenticates with our backend so payment is tied to this app account.
        tauri::async_runtime::spawn_blocking(move||{let checkout=remote_agent::billing_checkout(plan)?;let status=std::process::Command::new("/usr/bin/open").arg(checkout).status().map_err(|_|"Could not open checkout in your browser")?;if status.success(){Ok(())}else{Err("Could not open checkout in your browser".to_string())}}).await.map_err(|e|e.to_string())?
    }
    #[tauri::command]
    async fn ai_care_billing_status()->Result<serde_json::Value,String>{tauri::async_runtime::spawn_blocking(remote_agent::billing_status).await.map_err(|e|e.to_string())?}
    #[tauri::command]
    async fn open_ai_care_portal()->Result<(),String>{
        tauri::async_runtime::spawn_blocking(||{let url=remote_agent::billing_portal()?;let status=std::process::Command::new("/usr/bin/open").arg(url).status().map_err(|_|"Could not open subscription management")?;if status.success(){Ok(())}else{Err("Could not open subscription management".to_string())}}).await.map_err(|e|e.to_string())?
    }
    #[tauri::command]
    async fn cleanup_discover(app: tauri::AppHandle, prompt: String, scope: String, profiles: Vec<String>, jev: bool, engine: State<'_, Shared>) -> Result<serde_json::Value, String> {
        if prompt.len() > 2000 || scope.len() > 1000 || profiles.iter().any(|p| !["everyday", "developer", "builder", "creator"].contains(&p.as_str())) {
            return Err("Invalid assistant request".into());
        }
        let engine = engine.inner().clone();
        tauri::async_runtime::spawn_blocking(move || {
            let _guard = engine.begin("Finding cleanup locations", "Measuring locations and available cleanup adapters", "assistant")?;
            assistant::prepare_discovery()?;
            let _scopes = scopes(&engine);
            let roots = engine.data.lock().map_err(|_| "Settings unavailable")?.settings.scan_paths.clone();
            assistant::call(&app, &["discover".into(), "--managed".into(), "--roots".into(), serde_json::to_string(&roots).unwrap(), "--profiles".into(), serde_json::to_string(&profiles).unwrap(), "--prompt".into(), prompt, "--scope".into(), scope].into_iter().chain(if jev { vec!["--jev".into()] } else { vec![] }).collect::<Vec<_>>(), 240)
        }).await.map_err(|e| e.to_string())?
    }
    #[tauri::command]
    fn cleanup_progress()->Result<serde_json::Value,String>{assistant::discovery_state("discovery-progress.json")}
    #[tauri::command]
    fn cleanup_findings()->Result<serde_json::Value,String>{
        let mut value=assistant::discovery_state("plugin-findings.json")?;
        if value.is_object(){
            value["cached"]=serde_json::json!(true);
            if let Some(items)=value["candidates"].as_array_mut(){for item in items{item["executable"]=serde_json::json!(false);if item["actions"].is_object(){item["actions"]["delete"]=serde_json::json!(false);}}}
        }
        Ok(value)
    }
    #[tauri::command]
    fn cleanup_stop(engine: State<'_, Shared>)->Result<(),String>{
        let activity=engine.activity.lock().map_err(|_|"Activity state unavailable")?;
        if activity.as_ref().is_some_and(|a|a.cancellable){assistant::stop_discovery()}else{Err("No cancellable discovery is running".into())}
    }
    #[tauri::command]
    async fn cleanup_assess(app: tauri::AppHandle, plan_id: String, prompt: String, engine: State<'_, Shared>) -> Result<serde_json::Value, String> {
        let engine = engine.inner().clone();
        tauri::async_runtime::spawn_blocking(move || {
            let _guard = engine.begin("Typed AI assessment", "Jev first, Clef fallback for reproducibility and impact", "assistant")?;
            assistant::call(&app, &["assess".into(), "--plan".into(), plan_id, "--prompt".into(), prompt], 150)
        }).await.map_err(|e| e.to_string())?
    }
    #[tauri::command]
    async fn cleanup_execute(app: tauri::AppHandle, plan_id: String, ids: Vec<String>, agent_mode: Option<String>, agent_model: Option<String>, engine: State<'_, Shared>) -> Result<serde_json::Value, String> {
        if ids.is_empty() || ids.len() > 1000 { return Err("Select exact locations from a current cleanup plan".into()); }
        let engine = engine.inner().clone();
        tauri::async_runtime::spawn_blocking(move || {
            let _guard = engine.begin("Cleaning selected locations", "Running the explicitly selected cleanup adapters", "assistant")?;
            let _scopes = scopes(&engine);
            let result = assistant::call(&app, &["execute".into(), "--plan".into(), plan_id, "--ids".into(), serde_json::to_string(&ids).unwrap(), "--agent-mode".into(), agent_mode.unwrap_or_else(|| "platform".into()), "--agent-model".into(), agent_model.unwrap_or_else(|| "platform/auto".into()), "--confirm".into()], 600)?;
            engine.record("Selected cleanup plan executed", result["message"].as_str().unwrap_or("See per-location results"), result["recoveredBytes"].as_u64().unwrap_or(0), "cleanup");
            Ok(result)
        }).await.map_err(|e| e.to_string())?
    }
    #[tauri::command]
    fn cleanup_last_result() -> Result<serde_json::Value, String> { assistant::discovery_state("cleanup-last-result.json") }
    #[tauri::command]
    fn cleanup_execution_progress() -> Result<serde_json::Value, String> { assistant::discovery_state("cleanup-execution-progress.json") }
    #[tauri::command]
    async fn cleanup_agent_status(app: tauri::AppHandle) -> Result<serde_json::Value, String> {
        tauri::async_runtime::spawn_blocking(move || assistant::call(&app, &["agent-status".into()], 90)).await.map_err(|e| e.to_string())?
    }
    #[tauri::command]
    async fn cleanup_catalog(app: tauri::AppHandle) -> Result<serde_json::Value, String> {
        tauri::async_runtime::spawn_blocking(move || assistant::call(&app, &["catalog".into()], 15)).await.map_err(|e| e.to_string())?
    }
    #[tauri::command]
    async fn cleanup_approve(app: tauri::AppHandle, plan_id: String, id: String, engine: State<'_, Shared>) -> Result<serde_json::Value, String> {
        let engine = engine.inner().clone();
        tauri::async_runtime::spawn_blocking(move || {
            let _guard = engine.begin("Checking manual cleanup approval", "Validating the exact location and current file identities", "assistant")?;
            let _scopes = scopes(&engine);
            assistant::call(&app, &["approve".into(), "--plan".into(), plan_id, "--id".into(), id], 45)
        }).await.map_err(|e| e.to_string())?
    }
    #[tauri::command]
    async fn cleanup_update_catalog(app: tauri::AppHandle, url: String, engine: State<'_, Shared>) -> Result<serde_json::Value, String> {
        let engine = engine.inner().clone();
        tauri::async_runtime::spawn_blocking(move || {
            let _guard = engine.begin("Updating cleanup heuristics", "Downloading and validating the catalog", "assistant")?;
            assistant::call(&app, &["update-catalog".into(), "--url".into(), url], 30)
        }).await.map_err(|e| e.to_string())?
    }
    #[tauri::command]
    async fn trash_file(
        file: model::LargeFile,
        engine: State<'_, Shared>,
    ) -> Result<String, String> {
        let engine = engine.inner().clone();
        tauri::async_runtime::spawn_blocking(move || {
            let _guard = engine.begin("Moving selected file to Trash", "Rechecking identity before moving the selected file", "space")?;
            let _scopes = scopes(&engine);
            if !engine.last_scan_files.lock().map_err(|_| "Scan state unavailable")?.iter().any(|known| known.path == file.path && known.identity == file.identity && known.removable) {
                return Err("This file is not an eligible item from the current scan. Scan again.".into());
            }
            let home = system::user_home()?;
            let path = std::path::Path::new(&file.path);
            let metadata = std::fs::symlink_metadata(path).map_err(|_| "File unavailable")?;
            use std::os::unix::fs::MetadataExt;
            if !metadata.is_file() || metadata.file_type().is_symlink() || metadata.uid() != unsafe { libc::getuid() } ||
                storage::file_identity(&metadata) != file.identity || !storage::personal_file(&home, path) || native::in_package(path, &home) ||
                path.canonicalize().map_err(|_| "File unavailable")? != path {
                return Err("File changed, is app-managed, or is outside the selected personal-file scope.".into());
            }
            native::trash(&file.path)?;
            engine.record("File moved to Trash", &file.path, 0, "trash");
            Ok("Moved to Trash. Space is not reclaimed until you review and empty Trash in Finder.".into())
        }).await.map_err(|e| e.to_string())?
    }
    #[tauri::command]
    async fn choose_folder(
        app: tauri::AppHandle,
        engine: State<'_, Shared>,
    ) -> Result<Option<String>, String> {
        let (send, receive) = std::sync::mpsc::sync_channel(1);
        app.run_on_main_thread(move || {
            let _ = send.send(native::pick_folder());
        })
        .map_err(|e| e.to_string())?;
        let picked = tauri::async_runtime::spawn_blocking(move || {
            receive
                .recv()
                .map_err(|_| "Folder picker closed unexpectedly")?
        })
        .await
        .map_err(|e| e.to_string())??;
        if let Some((path, bookmark)) = picked {
            let home = system::user_home()?;
            storage::valid_root(&home, std::path::Path::new(&path))?;
            engine
                .data
                .lock()
                .map_err(|_| "Settings unavailable")?
                .bookmarks
                .insert(path.clone(), bookmark);
            engine.save()?;
            Ok(Some(path))
        } else {
            Ok(None)
        }
    }
    #[tauri::command]
    async fn list_apps(service:State<'_,MonitorService>) -> Result<serde_json::Value, String> {
        let monitor=service.monitor.clone();
        tauri::async_runtime::spawn_blocking(move||match monitor{Some(m)=>m.apps(),None=>processes::groups().map(|groups|serde_json::json!(groups))})
            .await
            .map_err(|e| e.to_string())?
    }
    #[tauri::command]
    async fn app_icon(id: String) -> Result<String, String> {
        tauri::async_runtime::spawn_blocking(move || {
            let group = processes::groups()?
                .into_iter()
                .find(|g| g.id == id)
                .ok_or("App is no longer running")?;
            native::icon(
                &group
                    .bundle_path
                    .ok_or("No app icon for a background tool")?,
            )
        })
        .await
        .map_err(|e| e.to_string())?
    }
    #[tauri::command]
    async fn quit_app(id: String, engine: State<'_, Shared>) -> Result<String, String> {
        let engine = engine.inner().clone();
        tauri::async_runtime::spawn_blocking(move || {
            let group = processes::groups()?
                .into_iter()
                .find(|g| g.id == id)
                .ok_or("App is no longer running")?;
            if !group.can_quit {
                return Err("This application cannot be quit through this build.".into());
            }
            let bundle = group
                .bundle_path
                .as_ref()
                .ok_or("This is a background tool; select an individual process instead.")?;
            let main = group
                .processes
                .iter()
                .find(|p| {
                    p.executable
                        .starts_with(&format!("{bundle}/Contents/MacOS/"))
                })
                .ok_or("The main application process is unavailable or protected")?;
            let current = processes::groups()?
                .into_iter()
                .flat_map(|g| g.processes)
                .find(|p| processes::same_identity(main, p))
                .ok_or("Application changed. Refresh first.")?;
            native::quit(current.pid)?;
            engine.record("Application quit requested", &group.name, 0, "process");
            Ok(format!(
                "{} was asked to quit. It may prompt to save your work.",
                group.name
            ))
        })
        .await
        .map_err(|e| e.to_string())?
    }
    #[tauri::command]
    fn get_state(engine: State<'_, Shared>) -> Result<serde_json::Value, String> {
        let data = engine.data.lock().map_err(|_| "State unavailable")?;
        // Folder capability bookmarks remain in the native process, not the UI.
        Ok(
            serde_json::json!({ "settings": data.settings, "history": data.history, "lastDailyDay": data.last_daily_day }),
        )
    }
    #[tauri::command]
    fn save_settings(settings: model::Settings, engine: State<'_, Shared>) -> Result<(), String> {
        if settings.hour > 23
            || settings.window_hours == 0
            || settings.window_hours > 12
            || settings.minimum_free_gb > 1000
        {
            return Err("Invalid daily care settings".into());
        }
        if settings.profiles.is_empty()
            || settings
                .profiles
                .iter()
                .any(|p| !["everyday", "developer", "builder", "creator"].contains(&p.as_str()))
        {
            return Err("Choose at least one supported profile".into());
        }
        if settings
            .cleanup_rules
            .iter()
            .any(|p| !["npm", "uv", "pip"].contains(&p.as_str()))
        {
            return Err("Unsupported automatic cleanup rule".into());
        }
        let _scopes = scopes(engine.inner());
        let home = system::user_home()?;
        for path in &settings.scan_paths {
            storage::valid_root(&home, std::path::Path::new(path))?;
        }
        engine
            .data
            .lock()
            .map_err(|_| "State unavailable")?
            .settings = settings;
        engine.save()
    }
    #[tauri::command]
    async fn clean_cache(id: String, engine: State<'_, Shared>) -> Result<String, String> {
        let engine = engine.inner().clone();
        tauri::async_runtime::spawn_blocking(move || {
            let _guard = engine.begin("Cleaning cache", "Running the supported tool cleanup command", "assistant")?;
            let (_, before) = system::disk_space()?;
            let _scopes = scopes(&engine);
            let result = storage::cleanup(&id)?;
            let (_, after) = system::disk_space()?;
            let recovered = after.saturating_sub(before);
            engine.record("Cache cleanup completed", &format!("{id}: measured available-space change; other disk activity may affect the result."), recovered, "cleanup");
            Ok(format!("Cleanup completed. Available space increased by {:.2} GB. {}", recovered as f64 / 1e9, result))
        }).await.map_err(|e| e.to_string())?
    }
    #[tauri::command]
    async fn end_process(
        process: model::Process,
        force: bool,
        engine: State<'_, Shared>,
    ) -> Result<String, String> {
        let engine = engine.inner().clone();
        tauri::async_runtime::spawn_blocking(move || {
            processes::terminate(&process, force)?;
            engine.record(
                "Process signal sent",
                &format!(
                    "{} (PID {}), {}",
                    process.name,
                    process.pid,
                    if force {
                        "force termination"
                    } else {
                        "termination requested"
                    }
                ),
                0,
                "process",
            );
            Ok("Termination requested. Refresh to check whether the process exited.".into())
        })
        .await
        .map_err(|e| e.to_string())?
    }
    #[tauri::command]
    async fn end_group(
        id: String,
        members: Vec<model::Process>,
        force: bool,
        engine: State<'_, Shared>,
    ) -> Result<String, String> {
        let engine = engine.inner().clone();
        tauri::async_runtime::spawn_blocking(move || {
            let group = processes::groups()?.into_iter().find(|g| g.id == id).ok_or("App group changed. Refresh first.")?;
            if members.is_empty() || members.iter().any(|p| !group.processes.iter().any(|c| processes::same_identity(p, c))) {
                return Err("Group members changed. Refresh before ending this group.".into());
            }
            let mut succeeded = 0; let mut failed = 0;
            for process in members.iter().rev() {
                if processes::terminate(process, force).is_ok() { succeeded += 1; } else { failed += 1; }
            }
            let detail = format!("{}: signaled {succeeded} processes; {failed} protected, exited, changed, or unavailable.", group.name);
            engine.record("App group signal sent", &detail, 0, "process"); Ok(detail)
        }).await.map_err(|e| e.to_string())?
    }
    #[tauri::command]
    async fn reveal_path(path: String, engine: State<'_, Shared>) -> Result<(), String> {
        let engine = engine.inner().clone();
        tauri::async_runtime::spawn_blocking(move || {
            let _scopes = scopes(&engine);
            let home = system::user_home()?;
            let validated = std::path::Path::new(&path)
                .canonicalize()
                .map_err(|_| "Path unavailable")?;
            if !validated.starts_with(home) && !["/Applications","/Volumes","/Library/Caches","/Library/Developer","/opt/homebrew","/usr/local"].iter().any(|root|validated.starts_with(root)) {
                return Err("Choose a path within supported storage inspection locations".into());
            }
            native::reveal(validated.to_str().ok_or("Invalid path")?);
            Ok(())
        })
        .await
        .map_err(|e| e.to_string())?
    }
    pub fn run() {
        let engine = Arc::new(state::Engine::new());
        let scheduler = engine.clone();
        std::thread::spawn(move || {let mut retry_after=std::time::Instant::now();loop {
            std::thread::sleep(Duration::from_secs(60));
            let (day, hour) = system::local_day_hour();
            let Ok(data) = scheduler.data.lock() else {
                continue;
            };
            let elapsed = (hour + 24 - data.settings.hour) % 24;
            let due = data.settings.enabled
                && elapsed < data.settings.window_hours
                && data.last_daily_day != day;
            drop(data);
            if due&&!native::sandboxed()&&std::time::Instant::now()>=retry_after&&!system::on_low_battery()&&!system::busy() {
                let settings=scheduler.data.lock().map(|data|data.settings.clone()).unwrap_or_default();
                let options=cleanup_discovery::Options{profiles:settings.profiles,roots:settings.scan_paths,daily_care:true,..Default::default()};
                match cleanup_session::inspect_configured("Free up disk space. Clean reproducible caches and generated files; keep my personal files.".into(),String::new(),false,options){
                    Ok(_)=>{if let Ok(mut data)=scheduler.data.lock(){data.last_daily_day=day;}let _=scheduler.save();},
                    Err(error)=>{retry_after=std::time::Instant::now()+Duration::from_secs(900);scheduler.record("Daily care deferred",&error,0,"daily");}
                }
            }
        }});
        tauri::Builder::default()
            .plugin(tauri_plugin_notification::init())
            .plugin(tauri_plugin_updater::Builder::new().build())
            .manage(updates::UpdateState::default())
            .manage(engine)
            .setup(|app| {
                let service=match monitor::Monitor::start() {
                    Ok(monitor)=>{let handle=app.handle().clone();monitor.set_publisher(Arc::new(move|snapshot|{let _=handle.emit("metrics-updated",snapshot);}));MonitorService{monitor:Some(monitor),error:String::new()}},
                    Err(error)=>MonitorService{monitor:None,error},
                };
                app.manage(service);
                {use tauri_plugin_notification::NotificationExt;
                    let handle=app.handle().clone();let shared=handle.state::<Shared>().inner().clone();
                    daily_care::set_publisher(Arc::new(move|notification,notify_system|{
                        shared.record(&notification.title,&notification.body,notification.recovered_bytes,"daily");
                        let _=handle.emit("daily-care-updated",&notification);
                        if notify_system{let _=handle.notification().builder().title(&notification.title).body(&notification.body).extra("runId",&notification.run_id).show();}
                    }));
                    let handle=app.handle().clone();
                    app.notification().on_action(move|action|{
                        if action.action_id()!="tap"{return;}
                        let id=action.notification().and_then(|n|n.extra().get("runId")).and_then(|v|v.as_str()).map(str::to_owned);
                        let handle=handle.clone();std::thread::spawn(move||{
                            let id=id.filter(|id|daily_care::notifications().is_ok_and(|items|items.iter().any(|n|&n.run_id==id))).unwrap_or_default();
                            if let Some(window)=handle.get_webview_window("main"){let _=window.show();let _=window.set_focus();}
                            let _=handle.emit("daily-care-review",id);
                        });
                    }).map_err(|error|error.to_string())?;
                }
                let show = tauri::menu::MenuItem::with_id(
                    app,
                    "show",
                    "Open Breathing Room",
                    true,
                    None::<&str>,
                )?;
                let quit = tauri::menu::MenuItem::with_id(
                    app,
                    "quit",
                    "Quit Breathing Room",
                    true,
                    None::<&str>,
                )?;
                let menu = tauri::menu::Menu::with_items(app, &[&show, &quit])?;
                let mut tray = tauri::tray::TrayIconBuilder::with_id("care")
                    .tooltip("Breathing Room — daily care")
                    .menu(&menu)
                    .show_menu_on_left_click(false)
                    .on_tray_icon_event(|tray,event| {
                        if matches!(event,tauri::tray::TrayIconEvent::Click{button:tauri::tray::MouseButton::Left,button_state:tauri::tray::MouseButtonState::Up,..}) {
                            let app=tray.app_handle();
                            activity_panel::toggle(app);
                        }
                    })
                    .on_menu_event(|app, event| match event.id.as_ref() {
                        "show" => {
                            if let Some(window) = app.get_webview_window("main") {
                                let _ = window.show();
                                let _ = window.set_focus();
                            }
                        }
                        "quit" => app.exit(0),
                        _ => {}
                    });
                if let Some(icon) = app.default_window_icon() {
                    tray = tray.icon(icon.clone());
                }
                tray.build(app)?;
                activity_panel::setup(app)?;
                Ok(())
            })
            .on_window_event(|window, event| {
                if window.label()=="activity-panel" {
                    if let tauri::WindowEvent::CloseRequested{api,..}=event {api.prevent_close();activity_panel::dismiss(window.app_handle());}
                    if matches!(event,tauri::WindowEvent::Focused(true)) {window.state::<activity_panel::PanelState>().focused.store(true,Ordering::Relaxed);}
                    if matches!(event,tauri::WindowEvent::Focused(false)) && window.state::<activity_panel::PanelState>().focused.swap(false,Ordering::Relaxed) && !window.state::<activity_panel::PanelState>().pinned.load(Ordering::Relaxed) {activity_panel::dismiss(window.app_handle());}
                    return;
                }
                if let tauri::WindowEvent::CloseRequested { api, .. } = event {
                    let engine = window.state::<Shared>();
                    let keep_running = engine
                        .data
                        .lock()
                        .map(|d| d.settings.keep_in_menu_bar)
                        .unwrap_or(false);
                    if keep_running {
                        api.prevent_close();
                        let _ = window.hide();
                    } else {
                        // The hidden activity panel is another window; explicitly quit
                        // when background operation has been disabled.
                        window.app_handle().exit(0);
                    }
                }
            })
            .invoke_handler(tauri::generate_handler![
                updates::check_app_update, updates::install_app_update, updates::restart_after_update,
                activity_panel::dismiss_activity_panel,
                activity_panel::pin_activity_panel,
                activity_panel::activity_panel_state,
                activity_panel::open_activity_main,
                scan_storage,
                scan_volume,
                cached_volume,
                browse_storage,
                cancel_scan,
                choose_folder,
                list_apps,
                app_icon,
                quit_app,
                get_state,
                save_settings,
                clean_cache,
                end_process,
                end_group,
                reveal_path,
                daily_approvals, revoke_daily_approval, daily_notifications, mark_daily_notification_seen,
                get_capabilities,
                get_activity,
                live_status,
                activity_log,
                configure_monitor,
                trash_file,
                cleanup_discover, cleanup_assess, cleanup_execute, cleanup_catalog, cleanup_update_catalog, cleanup_approve, cleanup_agent_status, cleanup_last_result, cleanup_execution_progress,
                open_trash, assistant_message, agent_cleanup_connection, agent_cleanup_inspect, agent_cleanup_inventory, agent_cleanup_state, agent_cleanup_approve, agent_cleanup_cancel,
                agent_cleanup_latest, agent_cleanup_resume, agent_auth_start, agent_auth_poll, agent_auth_logout, agent_api_configure, open_ai_care_checkout, ai_care_billing_status, open_ai_care_portal,
                cleanup_progress, cleanup_findings, cleanup_stop
            ])
            .build(tauri::generate_context!())
            .expect("Cannot start Breathing Room")
            .run(|app,event| {
                #[cfg(target_os="macos")]
                if matches!(event,tauri::RunEvent::Reopen{..}) {
                    if let Some(window)=app.get_webview_window("main") {
                        let _=window.show();let _=window.unminimize();let _=window.set_focus();
                    }
                }
            });
    }
}
#[cfg(feature = "gui")]
pub use gui::run;

#[cfg(feature = "gui")]
pub fn capabilities() -> serde_json::Value {
    serde_json::json!({ "sandboxed": native::sandboxed(), "cacheCommands": !native::sandboxed(), "cloudAi": false })
}
