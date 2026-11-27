//! Read-only measurement of disk space macOS rebuilds after a restart.
//!
//! Memory swap and the hibernation sleep image are allocated while the Mac
//! runs and are recreated at boot. They are often reported as "System Data"
//! and look like unexplained loss, but they are neither leftover clutter nor
//! safe to delete while macOS owns them. This module measures them, records a
//! per-boot sample so the app can show what the last restart returned, and
//! never offers a cleanup action for either one.

use crate::{model::now, system};
use serde::{Deserialize, Serialize};
use serde_json::{json, Value};
use std::{
    collections::HashSet,
    fs,
    os::unix::fs::MetadataExt,
    path::{Path, PathBuf},
};

const VM_VOLUME: &str = "/System/Volumes/VM";
const LEGACY_VM: &str = "/private/var/vm";
const SAMPLE_KEY: &str = "restart-space:v1";
const MAX_SAMPLE_AGE: u64 = 30 * 24 * 60 * 60;

#[derive(Clone, Serialize, Deserialize)]
struct Sample {
    booted_at: u64,
    available_bytes: u64,
    reclaim_bytes: u64,
    observed_at: u64,
}

#[derive(Default, Serialize, Deserialize)]
struct History {
    #[serde(default)]
    current: Option<Sample>,
    #[serde(default)]
    previous: Option<Sample>,
}

pub fn inspect() -> Value {
    match system::user_home() {
        Ok(home) => inspect_at(&home),
        Err(_) => inspect_at(Path::new("/")),
    }
}

pub fn inspect_at(home: &Path) -> Value {
    let mut warnings = Vec::new();
    let booted_at = boot_time();
    let (total, available) = system::disk_space().unwrap_or((0, 0));
    let (swap_total, swap_used, swap_free) = swap_usage(&mut warnings);
    let (swap_file_bytes, swap_files) = swap_files(&mut warnings);
    let sleep_image_bytes = sleep_image();
    let snapshot_count = local_snapshots(&mut warnings);
    let hibernate_mode = hibernate_mode();
    let pressure = memory_pressure();

    // Only these two are recreated by macOS at boot. Local snapshots can also
    // be released, but their size is not reliably attributable here, so they
    // are reported as a count rather than folded into the total.
    let reclaim = swap_file_bytes.saturating_add(sleep_image_bytes);

    let previous = {
        let stored = crate::runtime_store::cache_get(home, SAMPLE_KEY)
            .ok()
            .flatten()
            .and_then(|value| serde_json::from_value::<History>(value).ok())
            .unwrap_or_default();
        match stored.current.as_ref() {
            Some(current) if booted_at > 0 && current.booted_at == booted_at => stored.previous,
            Some(current) if booted_at > 0 && current.booted_at < booted_at => Some(current.clone()),
            Some(_) => None,
            None => stored.previous,
        }
    };
    let last_restart = last_restart(previous.as_ref(), booted_at, available);

    if booted_at > 0 {
        let sample = Sample {
            booted_at,
            available_bytes: available,
            reclaim_bytes: reclaim,
            observed_at: now(),
        };
        let history = History {
            current: Some(sample),
            previous,
        };
        // A failed cache write must not hide the measurement itself.
        if let Ok(value) = serde_json::to_value(&history) {
            let _ = crate::runtime_store::cache_put(home, SAMPLE_KEY, &value, None);
        }
    }

    let items = vec![
        json!({
            "id": "swap",
            "name": "Memory swap",
            "bytes": swap_file_bytes,
            "files": swap_files,
            "description": "Paging space macOS wrote to disk while RAM was under pressure. It is rebuilt at boot, not left behind by cleanup."
        }),
        json!({
            "id": "sleep-image",
            "name": "Sleep image",
            "bytes": sleep_image_bytes,
            "files": if sleep_image_bytes > 0 { 1 } else { 0 },
            "description": "Hibernation copy of memory. macOS rewrites it after a restart, and its size follows installed RAM and hibernation mode."
        }),
        json!({
            "id": "snapshots",
            "name": "Local snapshots",
            "bytes": Value::Null,
            "files": snapshot_count,
            "description": "Time Machine may release these under disk pressure or after a restart. Their size is not reliably attributable, so it is not counted here."
        }),
    ];

    json!({
        "timestamp": now(),
        "totalBytes": total,
        "availableBytes": available,
        "bootedAt": if booted_at > 0 { json!(booted_at) } else { Value::Null },
        "uptimeSeconds": if booted_at > 0 && booted_at <= now() { json!(now() - booted_at) } else { Value::Null },
        "swap": {
            "totalBytes": swap_total,
            "usedBytes": swap_used,
            "freeBytes": swap_free
        },
        "swapFiles": swap_files,
        "swapFileBytes": swap_file_bytes,
        "sleepImageBytes": sleep_image_bytes,
        "hibernateMode": hibernate_mode,
        "localSnapshotCount": snapshot_count,
        "memoryPressure": {
            "level": pressure,
            "label": pressure_label(pressure)
        },
        "restartReclaimBytes": reclaim,
        "estimatedAvailableAfterRestartBytes": available.saturating_add(reclaim),
        "items": items,
        "lastRestart": last_restart,
        "warnings": warnings,
        "note": "Swap and the sleep image are disk that macOS reuses while the Mac runs. They are not clutter, and Breathing Room does not delete them. A restart is the supported way to release them; how much returns depends on memory pressure and what else changes before the next boot."
    })
}

fn last_restart(previous: Option<&Sample>, booted_at: u64, available: u64) -> Value {
    let Some(previous) = previous else {
        return Value::Null;
    };
    if previous.booted_at == 0
        || booted_at == 0
        || previous.booted_at >= booted_at
        || previous.observed_at < previous.booted_at
        || booted_at.saturating_sub(previous.observed_at) > MAX_SAMPLE_AGE
    {
        return Value::Null;
    }
    json!({
        "previousBootAt": previous.booted_at,
        "availableBeforeBytes": previous.available_bytes,
        "availableAfterBytes": available,
        "freedBytes": available as i64 - previous.available_bytes as i64,
        "volatileBeforeBytes": previous.reclaim_bytes,
        "observedBeforeAt": previous.observed_at
    })
}

fn boot_time() -> u64 {
    system::output("/usr/sbin/sysctl", &["-n", "kern.boottime"], 5)
        .ok()
        .and_then(|text| text.split("sec = ").nth(1).map(str::to_owned))
        .and_then(|text| {
            text.chars()
                .take_while(|c| c.is_ascii_digit())
                .collect::<String>()
                .parse()
                .ok()
        })
        .unwrap_or(0)
}

fn megabytes(text: &str, label: &str) -> Option<u64> {
    let rest = text.split(label).nth(1)?;
    let value = rest.trim_start().trim_start_matches('=').trim_start();
    let end = value
        .find(|c: char| !(c.is_ascii_digit() || c == '.'))
        .unwrap_or(value.len());
    let number: f64 = value[..end].parse().ok()?;
    Some((number * 1_048_576.0).round() as u64)
}

fn swap_usage(warnings: &mut Vec<String>) -> (Option<u64>, Option<u64>, Option<u64>) {
    match system::output("/usr/sbin/sysctl", &["vm.swapusage"], 5) {
        Ok(text) => (
            megabytes(&text, "total = "),
            megabytes(&text, "used = "),
            megabytes(&text, "free = "),
        ),
        Err(_) => {
            warnings.push("Swap usage could not be read from sysctl; swap file sizes are still measured.".into());
            (None, None, None)
        }
    }
}

fn allocated(metadata: &fs::Metadata) -> u64 {
    let blocks = metadata.blocks().saturating_mul(512);
    if blocks > 0 {
        blocks
    } else {
        metadata.len()
    }
}

fn swap_files(warnings: &mut Vec<String>) -> (u64, u64) {
    let mut seen = HashSet::new();
    let mut bytes = 0_u64;
    let mut files = 0_u64;
    let mut found_directory = false;
    for directory in [VM_VOLUME, LEGACY_VM] {
        let Ok(entries) = fs::read_dir(directory) else {
            continue;
        };
        found_directory = true;
        for entry in entries.flatten() {
            let path = entry.path();
            if !path
                .file_name()
                .and_then(|name| name.to_str())
                .is_some_and(|name| name.starts_with("swapfile"))
            {
                continue;
            }
            let Ok(metadata) = fs::symlink_metadata(&path) else {
                continue;
            };
            if !metadata.is_file() || metadata.file_type().is_symlink() {
                continue;
            }
            if !seen.insert((metadata.dev(), metadata.ino())) {
                continue;
            }
            bytes = bytes.saturating_add(allocated(&metadata));
            files += 1;
        }
    }
    if !found_directory {
        warnings.push("The swap directory could not be listed; swap file sizes are unavailable.".into());
    }
    (bytes, files)
}

fn sleep_image() -> u64 {
    let mut seen = HashSet::new();
    for directory in [LEGACY_VM, VM_VOLUME] {
        let path: PathBuf = Path::new(directory).join("sleepimage");
        let Ok(metadata) = fs::symlink_metadata(&path) else {
            continue;
        };
        if !metadata.is_file() || metadata.file_type().is_symlink() {
            continue;
        }
        if seen.insert((metadata.dev(), metadata.ino())) {
            return allocated(&metadata);
        }
    }
    0
}

fn local_snapshots(warnings: &mut Vec<String>) -> u64 {
    match system::output("/usr/bin/tmutil", &["listlocalsnapshots", "/"], 8) {
        Ok(text) => text
            .lines()
            .filter(|line| line.contains("com.apple.TimeMachine"))
            .count() as u64,
        Err(_) => {
            warnings.push("Local snapshots could not be listed; the count may be incomplete.".into());
            0
        }
    }
}

fn hibernate_mode() -> Option<u32> {
    let text = system::output("/usr/bin/pmset", &["-g"], 5).ok()?;
    text.lines().find_map(|line| {
        line.trim()
            .strip_prefix("hibernatemode")?
            .trim()
            .parse()
            .ok()
    })
}

fn memory_pressure() -> Option<u32> {
    system::output(
        "/usr/sbin/sysctl",
        &["-n", "kern.memorystatus_vm_pressure_level"],
        5,
    )
    .ok()?
    .trim()
    .parse()
    .ok()
}

fn pressure_label(level: Option<u32>) -> &'static str {
    match level {
        Some(1) => "normal",
        Some(2) => "warning",
        Some(4) => "critical",
        _ => "unknown",
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn swap_usage_parses_the_sysctl_labels() {
        let text = "total = 4864.00M  used = 4245.44M  free = 618.56M  (encrypted)";
        assert_eq!(megabytes(text, "total = "), Some(5_100_273_664));
        assert_eq!(megabytes(text, "used = "), Some(4_451_666_493));
        assert_eq!(megabytes(text, "free = "), Some(648_607_171));
        assert_eq!(megabytes("unavailable", "total = "), None);
    }

    #[test]
    fn last_restart_reports_the_available_space_delta() {
        let previous = Sample {
            booted_at: 1_000,
            available_bytes: 2_000,
            reclaim_bytes: 3_000,
            observed_at: 1_500,
        };
        let value = last_restart(Some(&previous), 9_000, 8_000);
        assert_eq!(value["freedBytes"], 6_000);
        assert_eq!(value["availableBeforeBytes"], 2_000);
        assert_eq!(value["volatileBeforeBytes"], 3_000);
    }

    #[test]
    fn a_same_boot_or_foreign_sample_is_not_a_restart() {
        let same_boot = Sample {
            booted_at: 9_000,
            available_bytes: 2_000,
            reclaim_bytes: 3_000,
            observed_at: 9_500,
        };
        assert_eq!(last_restart(Some(&same_boot), 9_000, 8_000), Value::Null);
        let stale = Sample {
            booted_at: 1_000,
            available_bytes: 2_000,
            reclaim_bytes: 3_000,
            observed_at: 1_500,
        };
        assert_eq!(
            last_restart(Some(&stale), 1_500 + MAX_SAMPLE_AGE + 1, 8_000),
            Value::Null
        );
        assert_eq!(last_restart(None, 9_000, 8_000), Value::Null);
    }

    #[test]
    fn measurement_totals_only_what_macos_rebuilds() {
        let home = std::env::temp_dir().join(format!(
            "breathing-restart-{}",
            std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH)
                .unwrap()
                .as_nanos()
        ));
        let value = inspect_at(&home);
        assert_eq!(
            value["restartReclaimBytes"].as_u64(),
            Some(
                value["swapFileBytes"].as_u64().unwrap()
                    + value["sleepImageBytes"].as_u64().unwrap()
            )
        );
        assert!(value["items"]
            .as_array()
            .unwrap()
            .iter()
            .any(|item| item["id"] == "swap"));
        assert!(value["note"].as_str().unwrap().contains("not clutter"));
        let _ = fs::remove_dir_all(home);
    }
}
