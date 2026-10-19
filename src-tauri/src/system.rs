use std::{
    io::Read,
    os::unix::process::CommandExt,
    process::{Command, Stdio},
    thread,
    time::{Duration, Instant},
};

pub fn user_home() -> Result<std::path::PathBuf, String> {
    // dirs::home_dir may resolve to the container home in a sandboxed app.
    // The passwd record identifies the actual user's home; it grants no access.
    unsafe {
        let mut record: libc::passwd = std::mem::zeroed();
        let mut result = std::ptr::null_mut();
        let mut buffer = vec![0_u8; 16_384];
        let status = libc::getpwuid_r(
            libc::getuid(),
            &mut record,
            buffer.as_mut_ptr() as *mut i8,
            buffer.len(),
            &mut result,
        );
        if status != 0 || result.is_null() || record.pw_dir.is_null() {
            return Err("User home unavailable".into());
        }
        Ok(std::path::PathBuf::from(
            std::ffi::CStr::from_ptr(record.pw_dir)
                .to_string_lossy()
                .into_owned(),
        ))
    }
}

pub fn output(program: &str, args: &[&str], seconds: u64) -> Result<String, String> {
    let mut child = Command::new(program)
        .args(args)
        .env("PATH", format!("/opt/homebrew/bin:/usr/local/bin:{}", std::env::var("PATH").unwrap_or_else(|_| "/usr/bin:/bin:/usr/sbin:/sbin".into())))
        .process_group(0)
        .stdin(Stdio::null())
        .stdout(Stdio::piped())
        .stderr(Stdio::null())
        .spawn()
        .map_err(|e| format!("Cannot run {program}: {e}"))?;
    let mut stdout = child.stdout.take().ok_or("Cannot read command output")?;
    let reader = thread::spawn(move || {
        let mut bytes = Vec::new();
        let _ = stdout.read_to_end(&mut bytes);
        bytes
    });
    let deadline = Instant::now() + Duration::from_secs(seconds);
    loop {
        match child.try_wait() {
            Ok(Some(status)) => {
                let bytes = reader.join().unwrap_or_default();
                return if status.success() {
                    Ok(String::from_utf8_lossy(&bytes).into_owned())
                } else {
                    Err(format!("{program} could not complete (permissions, unavailable tool, or busy resource)."))
                };
            }
            Ok(None) if Instant::now() < deadline => thread::sleep(Duration::from_millis(30)),
            _ => {
                // This negative PID is only the fresh command group created above,
                // never a group inferred from the user's running-app display.
                unsafe {
                    libc::kill(-(child.id() as i32), libc::SIGKILL);
                }
                let _ = child.kill();
                let _ = child.wait();
                return Err(format!("{program} exceeded its time limit."));
            }
        }
    }
}
pub fn disk_space() -> Result<(u64, u64), String> {
    let text = output("/bin/df", &["-k", "/"], 5)?;
    let fields: Vec<_> = text
        .lines()
        .last()
        .ok_or("Disk information unavailable")?
        .split_whitespace()
        .collect();
    if fields.len() < 4 {
        return Err("Disk information incomplete".into());
    }
    let total = fields[1]
        .parse::<u64>()
        .map_err(|_| "Disk total unavailable")?
        * 1024;
    let available = fields[3]
        .parse::<u64>()
        .map_err(|_| "Available space unavailable")?
        * 1024;
    Ok((total, available))
}
#[cfg(feature = "gui")]
pub fn local_day_hour() -> (String, u32) {
    let seconds = crate::model::now() as libc::time_t;
    let mut local: libc::tm = unsafe { std::mem::zeroed() };
    unsafe {
        libc::localtime_r(&seconds, &mut local);
    }
    (
        format!(
            "{}-{}-{}",
            local.tm_year + 1900,
            local.tm_mon + 1,
            local.tm_mday
        ),
        local.tm_hour as u32,
    )
}
#[cfg(feature = "gui")]
pub fn on_low_battery() -> bool {
    crate::native::low_battery()
}
#[cfg(feature = "gui")]
pub fn busy() -> bool {
    let cores = std::thread::available_parallelism()
        .map(|n| n.get())
        .unwrap_or(1) as f64;
    if let Ok(processes) = crate::processes::sample() {
        return processes.iter().map(|p| p.cpu).sum::<f64>() / cores > 20.0;
    }
    // Sandboxed builds may not execute ps. System load provides a conservative
    // public-API fallback rather than pretending zero process activity.
    let mut average = 0.0_f64;
    unsafe {
        if libc::getloadavg(&mut average, 1) != 1 {
            return true;
        }
    }
    average / cores > 0.75
}
