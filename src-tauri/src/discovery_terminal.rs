//! Free-form discovery commands, constrained by the OS, not a command allowlist.
use crate::cleanup_session as session;
use serde_json::{json, Value};
use std::{fs, io::Read, os::unix::process::CommandExt, path::Path, process::{Command, Stdio}, sync::{Arc, Mutex}, thread, time::{Duration, Instant}};

fn quoted(path: &Path) -> String { serde_json::to_string(&path.to_string_lossy()).unwrap() }
fn profile(scope: Option<&Path>) -> String {
    let mut rules = String::from("(version 1)(deny default)(allow process-exec process-fork)(allow sysctl-read)(allow signal (target self))(allow file-write-data (literal \"/dev/null\"))");
    if let Some(scope) = scope {
        rules.push_str(&format!("(allow file-read* (subpath {}))", quoted(scope)));
        for root in ["/System", "/usr", "/bin", "/sbin", "/opt/homebrew", "/Library/Apple"] {
            rules.push_str(&format!("(allow file-read* (subpath \"{root}\"))"));
        }
        for path in scope.ancestors() { rules.push_str(&format!("(allow file-read-metadata (literal {}))", quoted(path))); }
        rules.push_str("(allow file-read* (literal \"/dev/null\") (literal \"/dev/urandom\") (literal \"/dev/random\"))");
    } else { rules.push_str("(allow file-read*)"); }
    // Metadata stays visible; conventional secret/session contents do not.
    rules.push_str(r#"(deny file-read-data (regex #"(^|/)([.]ssh|[.]aws|[.]gnupg|Keychains|[.]kube|[.]azure|[.]docker|[.]config|[.]local/share/opencode|app[.]breathingroom[.]mac)(/|$)"))
      (deny file-read-data (regex #"(^|/)([.]env[^/]*|[.]npmrc|[.]netrc|auth[.]json|credentials[^/]*|Cookies|Login Data|Web Data)(/|$)"))"#);
    rules
}
fn drain(mut pipe: impl Read, target: Arc<Mutex<Vec<u8>>>, limit: usize) {
    let mut buffer = [0u8; 8192];
    while let Ok(count) = pipe.read(&mut buffer) {
        if count == 0 { break; }
        if let Ok(mut output) = target.lock() { let keep = count.min(limit.saturating_sub(output.len())); output.extend_from_slice(&buffer[..keep]); }
        // Keep draining after the cap, so verbose commands cannot block on pipes.
    }
}
fn run(home: &Path, scope: Option<&Path>, command: &str, cwd: &Path, seconds: u64, cancelled: impl Fn() -> bool) -> Result<Value, String> {
    if command.trim().is_empty() || command.len() > 16000 || command.contains('\0') { return Err("Provide a discovery command of at most 16000 bytes".into()); }
    if !cfg!(target_os = "macos") || !Path::new("/usr/bin/sandbox-exec").is_file() { return Err("OS read-only sandbox unavailable; terminal discovery is disabled (no unsandboxed fallback)".into()); }
    let mut child = Command::new("/usr/bin/sandbox-exec")
        .args(["-p", &profile(scope), "/bin/zsh", "-f", "-c", command])
        .env_clear().env("PATH", session::runtime_path(home)).env("HOME", home)
        .env("ZDOTDIR", "/var/empty")
        .env("LANG", "en_US.UTF-8").env("LC_ALL", "C").env("PYTHONDONTWRITEBYTECODE", "1")
        .current_dir(cwd).stdin(Stdio::null()).stdout(Stdio::piped()).stderr(Stdio::piped()).process_group(0)
        .spawn().map_err(|_| "Could not start OS-sandboxed discovery terminal")?;
    let output = Arc::new(Mutex::new(Vec::new())); let errors = Arc::new(Mutex::new(Vec::new()));
    let stdout = child.stdout.take().unwrap(); let stderr = child.stderr.take().unwrap();
    let out = output.clone(); let err = errors.clone();
    let (finished,completion)=std::sync::mpsc::channel();let error_finished=finished.clone();
    thread::spawn(move || {drain(stdout, out, 24000);let _=finished.send(());});
    thread::spawn(move || {drain(stderr, err, 8000);let _=error_finished.send(());});
    let deadline = Instant::now() + Duration::from_secs(seconds.clamp(1, 120));
    let mut interrupted = false;
    let status = loop {
        match child.try_wait() {
            Ok(Some(status)) => break Some(status),
            Ok(None) if Instant::now() < deadline && !cancelled() => thread::sleep(Duration::from_millis(50)),
            _ => { interrupted = true; break None; }
        }
    };
    // Stop the fresh process group, never an existing user process. An unusual
    // detached helper must not hang the app by retaining an inherited pipe.
    unsafe { libc::kill(-(child.id() as i32), libc::SIGKILL); }
    let _ = child.wait();
    for _ in 0..2{if completion.recv_timeout(Duration::from_millis(500)).is_err(){interrupted=true;break;}}
    let out = output.lock().map_err(|_| "Terminal output unavailable")?;
    let err = errors.lock().map_err(|_| "Terminal errors unavailable")?;
    Ok(json!({"output":String::from_utf8_lossy(&out),"stderr":String::from_utf8_lossy(&err),"exitCode":status.and_then(|s|s.code()),"interrupted":interrupted,"truncated":out.len()>=24000||err.len()>=8000,"readOnly":true,"cleanupEligible":false,"note":"Untrusted evidence, not cleanup authority. Retain findings with inspect_location/register_candidate; never sum overlapping locations."}))
}
pub(crate) fn inspect(home: &Path, id: &str, args: &Value) -> Result<Value, String> {
    let saved = session::tool_run(home, id)?;
    let scope = if saved.scope.is_empty() { None } else { Some(session::inspection_path(home, id, &saved.scope)?) };
    let cwd = if let Some(raw) = args["cwd"].as_str() {
        let path = fs::canonicalize(raw).map_err(|_| "Working directory unavailable")?;
        if scope.as_ref().is_some_and(|root| !path.starts_with(root)) { return Err("Outside this inspection's requested scope".into()); } path
    } else { scope.clone().unwrap_or_else(|| home.into()) };
    run(home, scope.as_deref(), args["command"].as_str().ok_or("Command required")?, &cwd, args["seconds"].as_u64().unwrap_or(45), || session::inspection_cancelled(home))
}
#[cfg(all(test, target_os = "macos"))]
mod tests {
    use super::*;
    #[test]
    fn terminal_allows_pipelines_but_blocks_writes_network_and_secret_contents() {
        let home = fs::canonicalize(std::env::temp_dir()).unwrap().join(format!("br-terminal-{}-{}", std::process::id(), crate::model::now()));
        fs::create_dir_all(home.join(".ssh")).unwrap(); fs::write(home.join("data"), "fixture").unwrap(); fs::write(home.join(".ssh/key"), "fixture-secret").unwrap();
        let result = run(&home, None, "du -sk . | sort -n; printf forbidden > new-file; cat .ssh/key; /usr/bin/curl --connect-timeout 1 http://127.0.0.1:9", &home, 5, || false).unwrap();
        assert!(result["output"].as_str().unwrap().contains('.')); assert!(!result["output"].as_str().unwrap().contains("fixture-secret"));
        assert!(!home.join("new-file").exists()); assert!(result["stderr"].as_str().unwrap().contains("not permitted"));
        let scoped = run(&home, Some(&home), "cat /etc/hosts; stat -f %z data; echo changed >> data", &home, 5, || false).unwrap();
        assert!(!scoped["output"].as_str().unwrap().contains("localhost")); assert_eq!(fs::read_to_string(home.join("data")).unwrap(), "fixture");
        fs::remove_dir_all(home).unwrap();
    }
    #[test]
    fn terminal_timeout_retains_partial_output() {
        let home = fs::canonicalize(std::env::temp_dir()).unwrap(); let start = Instant::now();
        let result = run(&home, None, "print partial; sleep 30", &home, 1, || false).unwrap();
        assert_eq!(result["interrupted"], true); assert!(result["output"].as_str().unwrap().contains("partial")); assert!(start.elapsed().as_secs() < 5);
    }
}
