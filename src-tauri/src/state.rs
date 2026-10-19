use crate::model::{now, Event, Settings};
use serde::{Deserialize, Serialize};
use std::{
    fs,
    sync::{atomic::AtomicBool, Mutex},
};

#[derive(Default, Serialize, Deserialize, Clone)]
#[serde(rename_all = "camelCase")]
pub struct Persisted {
    pub settings: Settings,
    pub history: Vec<Event>,
    pub last_daily_day: String,
    #[serde(default)]
    pub bookmarks: std::collections::BTreeMap<String, String>,
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn running_operation_is_named_and_cleared_on_guard_drop() {
        let engine = Engine::new();
        let guard = engine.begin("Mapping your whole disk", "Read-only scan", "space").unwrap();
        let activity = engine.activity.lock().unwrap().clone().unwrap();
        assert_eq!(activity.title, "Mapping your whole disk");
        assert_eq!(activity.page, "space");
        assert!(activity.started_at > 0);
        let conflict = engine.begin("Cleanup", "Selected cleanup", "assistant");
        assert!(conflict.err().unwrap().contains("Mapping your whole disk is running"));
        drop(guard);
        assert!(engine.activity.lock().unwrap().is_none());
        assert!(engine.begin("Cleanup", "Selected cleanup", "assistant").is_ok());
    }
    #[test]
    fn failure_unwinds_activity_without_leaving_stale_busy_state() {
        let engine = Engine::new();
        fn fail(engine: &Engine) -> Result<(), String> {
            let _guard = engine.begin("JEV AI assessment", "Metadata", "assistant")?;
            Err("Fixture failure".into())
        }
        assert!(fail(&engine).is_err());
        assert!(engine.activity.lock().unwrap().is_none());
        assert!(engine.operation.try_lock().is_ok());
    }
    #[test]
    fn disk_mapping_is_visible_but_does_not_gate_the_independent_agent() {
        let engine=Engine::new();
        let guard=engine.begin_disk_map("Refreshing disk map","Background metadata scan").unwrap();
        let activity=engine.activity.lock().unwrap().clone().unwrap();
        assert!(!activity.blocks_agent);
        assert_eq!(serde_json::to_value(&activity).unwrap()["blocksAgent"],false);
        assert!(engine.begin_disk_map("Mapping your whole disk","Duplicate").is_err());
        drop(guard);assert!(engine.activity.lock().unwrap().is_none());
        let _guard=engine.begin("Cleaning cache","Approved mutation","assistant").unwrap();
        assert!(engine.activity.lock().unwrap().as_ref().unwrap().blocks_agent);
    }
}
pub struct Engine {
    pub data: Mutex<Persisted>,
    pub operation: Mutex<()>,
    pub cancel: AtomicBool,
    pub last_scan_files: Mutex<Vec<crate::model::LargeFile>>,
    pub activity: Mutex<Option<Activity>>,
}
#[derive(Clone, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct Activity {
    pub title: String,
    pub detail: String,
    pub page: String,
    pub started_at: u64,
    pub cancellable: bool,
    pub blocks_agent: bool,
}
pub struct OperationGuard<'a> {
    engine: &'a Engine,
    _lock: std::sync::MutexGuard<'a, ()>,
    _update_gate: std::sync::RwLockReadGuard<'static, ()>,
}
impl Drop for OperationGuard<'_> {
    fn drop(&mut self) {
        if let Ok(mut activity) = self.engine.activity.lock() { *activity = None; }
    }
}
fn path() -> Result<std::path::PathBuf, String> {
    Ok(dirs::data_local_dir()
        .ok_or("Application data folder unavailable")?
        .join("app.breathingroom.mac")
        .join("state.json"))
}
impl Engine {
    pub fn new() -> Self {
        let data = path()
            .ok()
            .and_then(|p| fs::read(p).ok())
            .and_then(|b| serde_json::from_slice(&b).ok())
            .unwrap_or_default();
        Self {
            data: Mutex::new(data),
            operation: Mutex::new(()),
            cancel: AtomicBool::new(false),
            last_scan_files: Mutex::new(vec![]),
            activity: Mutex::new(None),
        }
    }
    pub fn begin(&self, title: &str, detail: &str, page: &str) -> Result<OperationGuard<'_>, String> {
        self.begin_with_agent_policy(title,detail,page,true)
    }
    pub fn begin_disk_map(&self, title: &str, detail: &str) -> Result<OperationGuard<'_>, String> {
        // The remote/native agent has its own run lifecycle, cancellation and
        // validated action IDs. A read-only disk map must not gate that runner.
        self.begin_with_agent_policy(title,detail,"space",false)
    }
    fn begin_with_agent_policy(&self, title: &str, detail: &str, page: &str, blocks_agent: bool) -> Result<OperationGuard<'_>, String> {
        let update_gate = crate::update_gate::operation()?;
        let lock = self.operation.try_lock().map_err(|_| {
            let title = self.activity.lock().ok().and_then(|a| a.as_ref().map(|a| a.title.clone())).unwrap_or("Maintenance".into());
            format!("{title} is running. Wait for it to finish before starting another operation.")
        })?;
        *self.activity.lock().map_err(|_| "Activity state unavailable")? = Some(Activity {
            title: title.into(), detail: detail.into(), page: page.into(), started_at: now(), cancellable: title == "Finding cleanup with JEV AI", blocks_agent,
        });
        Ok(OperationGuard { engine: self, _lock: lock, _update_gate: update_gate })
    }
    pub fn save(&self) -> Result<(), String> {
        let data = self.data.lock().map_err(|_| "State unavailable")?;
        let path = path()?;
        fs::create_dir_all(path.parent().unwrap()).map_err(|e| e.to_string())?;
        let temporary = path.with_extension("tmp");
        fs::write(
            &temporary,
            serde_json::to_vec_pretty(&*data).map_err(|e| e.to_string())?,
        )
        .map_err(|e| e.to_string())?;
        fs::rename(temporary, path).map_err(|e| e.to_string())
    }
    pub fn record(&self, title: &str, detail: &str, recovered_bytes: u64, kind: &str) {
        if let Ok(mut data) = self.data.lock() {
            let id = format!(
                "{}-{}",
                now(),
                std::time::SystemTime::now()
                    .duration_since(std::time::UNIX_EPOCH)
                    .unwrap_or_default()
                    .as_nanos()
            );
            data.history.insert(
                0,
                Event {
                    id,
                    timestamp: now(),
                    title: title.into(),
                    detail: detail.into(),
                    recovered_bytes,
                    kind: kind.into(),
                },
            );
            data.history.truncate(100);
        }
        let _ = self.save();
    }
}
