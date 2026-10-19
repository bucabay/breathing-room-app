//! Development scripting bridge. Credentials stay in the child/native process.
use crate::system;
use std::path::PathBuf;
use tauri::Manager;
pub fn cache_path(name: &str) -> Result<PathBuf,String> {
    if !["discovery-progress.json","discovery.cancel","plugin-findings.json","cleanup-last-result.json","cleanup-execution-progress.json"].contains(&name) { return Err("Unknown discovery state".into()); }
    Ok(system::user_home()?.join("Library/Application Support/app.breathingroom.mac").join(name))
}
pub fn prepare_discovery() -> Result<(),String> {
    let path=cache_path("discovery.cancel")?;
    if path.exists(){std::fs::remove_file(path).map_err(|e|e.to_string())?;}
    let progress=cache_path("discovery-progress.json")?;
    std::fs::create_dir_all(progress.parent().unwrap()).map_err(|e|e.to_string())?;
    std::fs::write(progress,serde_json::to_vec(&serde_json::json!({"running":true,"phase":"starting","total":100,"completed":0,"active":[],"plugins":[],"candidates":[]})).unwrap()).map_err(|e|e.to_string())
}
pub fn discovery_state(name:&str)->Result<serde_json::Value,String>{
    let path=cache_path(name)?;
    if !path.exists(){return Ok(serde_json::Value::Null);}
    let metadata=std::fs::symlink_metadata(&path).map_err(|e|e.to_string())?;
    if metadata.file_type().is_symlink()||metadata.len()>4*1024*1024{return Err("Invalid discovery cache".into());}
    serde_json::from_slice(&std::fs::read(path).map_err(|e|e.to_string())?).map_err(|_|"Discovery state unavailable".into())
}
pub fn stop_discovery()->Result<(),String>{
    std::fs::write(cache_path("discovery.cancel")?,b"stop").map_err(|e|e.to_string())
}

pub fn call(app: &tauri::AppHandle, args: &[String], seconds: u64) -> Result<serde_json::Value, String> {
    let script: PathBuf = app.path().resource_dir().map_err(|_| "Cleanup resources unavailable")?.join("cleanup/cleanup.py");
    run_script(script, args, seconds)
}
pub fn space(app: &tauri::AppHandle) -> Result<serde_json::Value, String> {
    let script = app.path().resource_dir().map_err(|_| "Inventory resources unavailable")?.join("cleanup/space.py");
    map_disk(script)
}
fn map_disk(script: PathBuf) -> Result<serde_json::Value, String> {
    let mut report = run_script(script, &[], 230)?;
    if let Err(error) = crate::disk_map_cache::save(&report) {
        if let Some(warnings) = report["warnings"].as_array_mut() { warnings.push(serde_json::json!(format!("Could not save disk map: {error}"))); }
    }
    Ok(report)
}
pub fn packaged_space() -> Result<serde_json::Value, String> {
    let binary = std::env::current_exe().map_err(|_| "Application path unavailable")?;
    map_disk(binary.parent().ok_or("Application path unavailable")?.join("../Resources/cleanup/space.py"))
}
pub fn browse(app: &tauri::AppHandle, path: String) -> Result<serde_json::Value, String> {
    let script = app.path().resource_dir().map_err(|_| "Inventory resources unavailable")?.join("cleanup/space.py");
    run_script(script, &["browse".into(), path], 15)
}

pub fn packaged_cli(args: &[String]) -> Result<serde_json::Value, String> {
    let binary = std::env::current_exe().map_err(|_| "Application path unavailable")?;
    let script = binary.parent().ok_or("Application path unavailable")?.join("../Resources/cleanup/cleanup.py");
    run_script(script, args, 180)
}

fn run_script(script: PathBuf, args: &[String], seconds: u64) -> Result<serde_json::Value, String> {
    if crate::native::sandboxed() {
        return Err("External cleanup scripts are disabled in the sandbox build. Use the development app for this workflow.".into());
    }
    let python = ["/opt/homebrew/bin/python3", "/usr/local/bin/python3", "/usr/bin/python3"]
        .iter().find(|p| std::path::Path::new(p).is_file()).ok_or("Python 3.10+ is required for development cleanup scripts")?;
    if !script.is_file() { return Err("Bundled cleanup scripts unavailable. Rebuild the desktop app.".into()); }
    let mut owned = vec!["-B".to_string(), script.to_string_lossy().into_owned()];
    owned.extend_from_slice(args);
    // Finder launches have a minimal PATH; local subscription runtimes live here.
    let home = system::user_home()?;
    let path = format!("{}/.opencode/bin:{}/.local/bin:{}/.cargo/bin:{}/.bun/bin:/opt/homebrew/bin:/usr/local/bin:{}", home.display(), home.display(), home.display(), home.display(), std::env::var("PATH").unwrap_or_default());
    let refs: Vec<&str> = owned.iter().map(String::as_str).collect();
    let assignment = format!("PATH={path}");
    let command_args: Vec<&str> = [assignment.as_str(), *python].into_iter().chain(refs.iter().copied()).collect();
    let text = system::output("/usr/bin/env", &command_args, seconds)?;
    let value: serde_json::Value = serde_json::from_str(&text).map_err(|_| "Cleanup script returned an invalid response")?;
    if let Some(error) = value.get("error").and_then(|e| e.as_str()) { return Err(error.to_string()); }
    Ok(value)
}
