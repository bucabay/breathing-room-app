use crate::{
    model::{AppGroup, Process},
    system,
};
use std::collections::{BTreeMap, HashMap};

pub fn protected_executable(executable: &str) -> bool {
    let ordinary_apple_app = executable.starts_with("/System/Applications/")
        || executable.starts_with("/System/Cryptexes/App/System/Applications/");
    (executable.starts_with("/System/") && !ordinary_apple_app)
        || executable.starts_with("/usr/libexec/")
        || executable.starts_with("/usr/sbin/")
        || executable.contains("breathing-room")
        || executable.contains("Breathing Room.app")
        || executable == "/sbin/launchd"
}

pub fn parse_line(line: &str, own_uid: u32) -> Option<Process> {
    let parts: Vec<_> = line.split_whitespace().collect();
    if parts.len() < 11 {
        return None;
    }
    let executable = parts[10..].join(" ");
    let name = executable
        .rsplit('/')
        .next()
        .unwrap_or(&executable)
        .to_string();
    let pid = parts[0].parse().ok()?;
    let uid = parts[2].parse().ok()?;
    Some(Process {
        pid,
        parent_pid: parts[1].parse().ok()?,
        uid,
        cpu: parts[3].parse().ok()?,
        memory_bytes: parts[4].parse::<u64>().ok()? * 1024,
        started: parts[5..10].join(" "),
        executable: executable.clone(),
        name,
        app: String::new(),
        protected: uid != own_uid
            || pid <= 1
            || pid == std::process::id() as i32
            || protected_executable(&executable),
    })
}
fn bundle(executable: &str) -> Option<(String, String)> {
    let end = executable.find(".app/")? + 4;
    let path = executable[..end].to_string();
    let name = path
        .rsplit('/')
        .next()?
        .trim_end_matches(".app")
        .to_string();
    Some((name, path))
}
pub fn sample() -> Result<Vec<Process>, String> {
    let text = system::output(
        "/bin/ps",
        &["-axo", "pid=,ppid=,uid=,%cpu=,rss=,lstart=,comm="],
        5,
    )?;
    let own_uid = unsafe { libc::getuid() };
    Ok(text
        .lines()
        .filter_map(|l| parse_line(l, own_uid))
        .collect())
}
pub fn groups() -> Result<Vec<AppGroup>, String> {
    let processes = match sample() {
        Ok(processes) => processes,
        Err(error) => {
            #[cfg(feature = "gui")]
            {
                return crate::native::running_apps()
                    .map_err(|fallback| format!("{error}; {fallback}"));
            }
            #[cfg(not(feature = "gui"))]
            {
                return Err(error);
            }
        }
    };
    Ok(group_samples(processes))
}
pub fn group_samples(processes: Vec<Process>) -> Vec<AppGroup> {
    let index: HashMap<_, _> = processes.iter().map(|p| (p.pid, p)).collect();
    let mut groups: BTreeMap<String, AppGroup> = BTreeMap::new();
    for mut process in processes.clone() {
        let mut current = &process;
        let mut owner = None;
        for _ in 0..24 {
            if let Some(found) = bundle(&current.executable) {
                owner = Some(found);
                break;
            }
            let Some(parent) = index.get(&current.parent_pid) else {
                break;
            };
            if parent.pid <= 1 || parent.pid == current.pid {
                break;
            }
            current = parent;
        }
        let (name, bundle_path, id) = match owner {
            Some((name, path)) => (name, Some(path.clone()), path),
            None if process.protected => {
                ("macOS & protected services".into(), None, "system".into())
            }
            None => (
                process.name.clone(),
                None,
                format!("background:{}", process.pid),
            ),
        };
        process.app = name.clone();
        let group = groups.entry(id.clone()).or_insert(AppGroup {
            id,
            name,
            bundle_path,
            cpu: 0.0,
            memory_bytes: 0,
            processes: vec![],
            metrics_available: true,
            can_quit: false,
            coverage: "Observed app processes".into(),
        });
        if !process.protected
            && group.bundle_path.as_ref().is_some_and(|p| {
                process
                    .executable
                    .starts_with(&format!("{p}/Contents/MacOS/"))
            })
        {
            group.can_quit = true;
        }
        group.cpu += process.cpu;
        group.memory_bytes += process.memory_bytes;
        group.processes.push(process);
    }
    let mut result: Vec<_> = groups.into_values().collect();
    result.sort_by(|a, b| b.memory_bytes.cmp(&a.memory_bytes));
    for g in &mut result {
        g.processes
            .sort_by(|a, b| b.memory_bytes.cmp(&a.memory_bytes));
    }
    result
}
pub fn same_identity(expected: &Process, current: &Process) -> bool {
    expected.pid == current.pid
        && expected.uid == current.uid
        && expected.started == current.started
        && expected.executable == current.executable
}
pub fn terminate(expected: &Process, force: bool) -> Result<(), String> {
    let current = sample()?
        .into_iter()
        .find(|p| p.pid == expected.pid)
        .ok_or("Process already exited")?;
    if !same_identity(expected, &current) {
        return Err("Process changed since it was selected. Refresh the app list.".into());
    }
    if current.protected {
        return Err("This process is protected or belongs to another user.".into());
    }
    let signal = if force { libc::SIGKILL } else { libc::SIGTERM };
    if unsafe { libc::kill(current.pid, signal) } != 0 {
        return Err(std::io::Error::last_os_error().to_string());
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn ordinary_apple_apps_are_distinct_from_critical_services() {
        assert!(!protected_executable(
            "/System/Applications/Photos.app/Contents/MacOS/Photos"
        ));
        assert!(protected_executable(
            "/System/Library/PrivateFrameworks/SkyLight.framework/Resources/WindowServer"
        ));
        assert!(protected_executable(
            "/Applications/Breathing Room.app/Contents/MacOS/breathing-room"
        ));
    }
    #[test]
    fn spaces_in_app_path_survive_parsing() {
        let p = parse_line("123 1 501 12.5 1024 Fri Oct 2 09:00:00 2026 /Applications/Google Chrome.app/Contents/MacOS/Google Chrome", 501).unwrap();
        assert_eq!(p.memory_bytes, 1048576);
        assert_eq!(bundle(&p.executable).unwrap().0, "Google Chrome");
        assert_eq!(p.started, "Fri Oct 2 09:00:00 2026");
    }
    #[test]
    fn sampled_helpers_are_combined_with_their_parent_app() {
        let parent=parse_line("123 1 501 85 1024 Fri Oct 2 09:00:00 2026 /Applications/Editor.app/Contents/MacOS/Editor",501).unwrap();
        let helper=parse_line("124 123 501 40 1024 Fri Oct 2 09:00:00 2026 /usr/local/bin/node",501).unwrap();
        let groups=group_samples(vec![parent,helper]);
        assert_eq!(groups.len(),1);assert_eq!(groups[0].cpu,125.0);
        assert_eq!(groups[0].bundle_path.as_deref(),Some("/Applications/Editor.app"));
        assert_eq!(groups[0].processes.len(),2);
    }
    #[test]
    fn reused_pid_cannot_be_terminated() {
        let p = parse_line(
            "123 1 501 0 1 Fri Oct 2 09:00:00 2026 /usr/local/bin/node",
            501,
        )
        .unwrap();
        let mut replacement = p.clone();
        replacement.started = "later".into();
        assert!(!same_identity(&p, &replacement));
    }
    #[test]
    fn termination_only_targets_a_verified_test_child() {
        let mut child = std::process::Command::new("/bin/sleep")
            .arg("15")
            .spawn()
            .unwrap();
        std::thread::sleep(std::time::Duration::from_millis(100));
        let process = sample()
            .unwrap()
            .into_iter()
            .find(|p| p.pid == child.id() as i32)
            .unwrap();
        let mut changed = process.clone();
        changed.started = "not the same process".into();
        assert!(terminate(&changed, false).is_err());
        assert!(child.try_wait().unwrap().is_none());
        terminate(&process, false).unwrap();
        assert!(!child.wait().unwrap().success());
    }
}
