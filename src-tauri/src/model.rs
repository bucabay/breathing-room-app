use serde::{Deserialize, Serialize};

#[derive(Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct Settings {
    pub profiles: Vec<String>,
    pub enabled: bool,
    pub hour: u32,
    pub window_hours: u32,
    pub minimum_free_gb: u32,
    pub automatic_cleanup: bool,
    pub cleanup_rules: Vec<String>,
    pub scan_paths: Vec<String>,
    #[serde(default = "keep_running_default")]
    pub keep_in_menu_bar: bool,
}
fn keep_running_default() -> bool { true }
impl Default for Settings {
    fn default() -> Self {
        Self {
            profiles: vec!["everyday".into()],
            enabled: false,
            hour: 9,
            window_hours: 3,
            minimum_free_gb: 20,
            automatic_cleanup: false,
            cleanup_rules: vec![],
            scan_paths: vec![],
            keep_in_menu_bar: true,
        }
    }
}
#[derive(Clone, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct StorageGroup {
    pub id: String,
    pub name: String,
    pub category: String,
    pub owner: String,
    pub project: String,
    pub bytes: u64,
    pub files: u64,
}
#[derive(Clone, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct Candidate {
    pub id: String,
    pub name: String,
    pub path: String,
    pub bytes: u64,
    pub description: String,
    pub method: String,
    pub executable: bool,
}
#[derive(Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct LargeFile {
    pub path: String,
    pub bytes: u64,
    pub identity: String,
    pub removable: bool,
}
#[derive(Clone, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct StorageReport {
    pub total_bytes: u64,
    pub available_bytes: u64,
    pub scanned_bytes: u64,
    pub file_count: u64,
    pub partial: bool,
    pub skipped: u64,
    pub scanned_at: u64,
    pub roots: Vec<String>,
    pub groups: Vec<StorageGroup>,
    pub candidates: Vec<Candidate>,
    pub warnings: Vec<String>,
    pub large_files: Vec<LargeFile>,
}
#[derive(Clone, Serialize, Deserialize, Debug)]
#[serde(rename_all = "camelCase")]
pub struct Process {
    pub pid: i32,
    pub parent_pid: i32,
    pub uid: u32,
    pub cpu: f64,
    pub memory_bytes: u64,
    pub started: String,
    pub executable: String,
    pub name: String,
    pub app: String,
    pub protected: bool,
}
#[derive(Clone, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct AppGroup {
    pub id: String,
    pub name: String,
    pub bundle_path: Option<String>,
    pub cpu: f64,
    pub memory_bytes: u64,
    pub processes: Vec<Process>,
    pub metrics_available: bool,
    pub can_quit: bool,
    pub coverage: String,
}
#[derive(Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct Event {
    pub id: String,
    pub timestamp: u64,
    pub title: String,
    pub detail: String,
    pub recovered_bytes: u64,
    pub kind: String,
}
pub fn now() -> u64 {
    std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .unwrap_or_default()
        .as_secs()
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn background_operation_defaults_on_but_respects_an_explicit_opt_out() {
        assert!(Settings::default().keep_in_menu_bar);
        let mut value=serde_json::to_value(Settings::default()).unwrap();
        value.as_object_mut().unwrap().remove("keepInMenuBar");
        assert!(serde_json::from_value::<Settings>(value.clone()).unwrap().keep_in_menu_bar);
        value["keepInMenuBar"]=serde_json::json!(false);
        assert!(!serde_json::from_value::<Settings>(value).unwrap().keep_in_menu_bar);
    }
}
