//! Persist the latest measured disk map; reading it never starts a scan.
use serde_json::{json, Value};
use std::{fs, os::unix::fs::MetadataExt, path::{Path, PathBuf}};
#[cfg(test)]use std::os::unix::fs::PermissionsExt;

const VERSION: u64 = 1;
const MAX_BYTES: u64 = 32 * 1024 * 1024;

fn path(home: &Path) -> PathBuf {
    home.join("Library/Application Support/app.breathingroom.mac/disk-map.json")
}
fn valid_report(report: &Value) -> bool {
    report["totalBytes"].as_u64().is_some_and(|n| n > 0)
        && report["availableBytes"].is_u64() && report["scannedBytes"].is_u64()
        && report["scannedAt"].as_u64().is_some_and(|n| n > 0)
        && ["groups", "directories", "largeFiles", "roots", "candidates", "warnings"].iter().all(|field| report[*field].is_array())
        && report["partial"].is_boolean()
}
pub fn load() -> Result<Option<Value>, String> { load_at(&crate::system::user_home()?) }
pub fn save(report: &Value) -> Result<(), String> { save_at(&crate::system::user_home()?, report) }

fn load_at(home: &Path) -> Result<Option<Value>, String> {
    if let Some(report)=crate::runtime_store::cache_get(home,"disk-map:v1")?{if valid_report(&report){return Ok(Some(report));}}
    let file = path(home);
    let metadata = match fs::symlink_metadata(&file) {
        Ok(value) => value,
        Err(error) if error.kind() == std::io::ErrorKind::NotFound => return Ok(None),
        Err(error) => return Err(error.to_string()),
    };
    if !metadata.is_file() || metadata.file_type().is_symlink() || metadata.len() > MAX_BYTES || metadata.uid() != unsafe { libc::getuid() } { return Ok(None); }
    let bytes = fs::read(file).map_err(|error| error.to_string())?;
    let Ok(value) = serde_json::from_slice::<Value>(&bytes) else { return Ok(None); };
    if value["version"].as_u64() != Some(VERSION) || value["home"].as_str() != home.to_str() || !valid_report(&value["report"]) { return Ok(None); }
    let report=value["report"].clone();crate::runtime_store::cache_put(home,"disk-map:v1",&report,None)?;
    Ok(Some(report))
}
fn save_at(home: &Path, report: &Value) -> Result<(), String> {
    if !valid_report(report) { return Err("Disk map was incomplete; the previous saved map was retained".into()); }
    let bytes = serde_json::to_vec(&json!({"version":VERSION,"home":home,"report":report})).map_err(|error| error.to_string())?;
    if bytes.len() as u64 > MAX_BYTES { return Err("Disk map exceeds the cache size limit".into()); }
    crate::runtime_store::cache_put(home,"disk-map:v1",report,None)
}

#[cfg(test)] mod tests {
    use super::*;
    fn fixture() -> PathBuf {
        fs::canonicalize(std::env::temp_dir()).unwrap().join(format!("breathing-map-cache-{}",std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).unwrap().as_nanos()))
    }
    fn report(stamp: u64) -> Value { json!({"totalBytes":1000,"availableBytes":100,"scannedBytes":800,"scannedAt":stamp,"partial":true,"groups":[],"directories":[{"path":"/fixture","bytes":800}],"largeFiles":[],"roots":["/System/Volumes/Data"],"candidates":[],"warnings":["Partial fixture"]}) }
    #[test] fn cache_survives_reloads_and_failed_refreshes() {
        let home=fixture(); assert_eq!(load_at(&home).unwrap(),None);
        save_at(&home,&report(100)).unwrap();assert_eq!(load_at(&home).unwrap(),Some(report(100)));
        assert!(save_at(&home,&json!({"error":"Scan failed"})).is_err());assert_eq!(load_at(&home).unwrap(),Some(report(100)));
        save_at(&home,&report(200)).unwrap();assert_eq!(load_at(&home).unwrap(),Some(report(200)));
        assert_eq!(fs::metadata(crate::runtime_store::path(&home)).unwrap().permissions().mode() & 0o777,0o600);
        fs::remove_dir_all(home).unwrap();
    }
    #[test] fn corrupt_foreign_and_obsolete_caches_are_misses() {
        let home=fixture();fs::create_dir_all(path(&home).parent().unwrap()).unwrap();
        for bytes in [b"invalid".to_vec(),serde_json::to_vec(&json!({"version":99,"home":home,"report":report(100)})).unwrap(),serde_json::to_vec(&json!({"version":1,"home":"/another-user","report":report(100)})).unwrap()] { fs::write(path(&home),bytes).unwrap();assert_eq!(load_at(&home).unwrap(),None); }
        fs::remove_dir_all(home).unwrap();
    }
    #[test] fn linked_cache_files_are_not_read() {
        let home=fixture();fs::create_dir_all(path(&home).parent().unwrap()).unwrap();let original=home.join("original.json");fs::write(&original,serde_json::to_vec(&json!({"version":1,"home":home,"report":report(100)})).unwrap()).unwrap();
        std::os::unix::fs::symlink(original,path(&home)).unwrap();assert_eq!(load_at(&home).unwrap(),None);fs::remove_dir_all(home).unwrap();
    }
    #[test] fn legacy_mapping_is_migrated_without_rescanning(){let home=fixture();fs::create_dir_all(path(&home).parent().unwrap()).unwrap();fs::write(path(&home),serde_json::to_vec(&json!({"version":1,"home":home,"report":report(100)})).unwrap()).unwrap();assert_eq!(load_at(&home).unwrap(),Some(report(100)));fs::remove_file(path(&home)).unwrap();assert_eq!(load_at(&home).unwrap(),Some(report(100)));fs::remove_dir_all(home).unwrap();}
}
