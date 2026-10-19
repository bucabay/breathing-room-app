//! Read-only temporal storage evidence, not growth attribution or cleanup authority.
use crate::{cleanup_session as session, discovery_inventory};
use serde_json::{json, Value};
use std::{collections::{BTreeMap, HashSet}, fs, os::unix::fs::MetadataExt, path::{Path, PathBuf}, time::{Duration, Instant, SystemTime, UNIX_EPOCH}};

pub(crate) fn temporary_root() -> Option<PathBuf> {
    // Resolve the current user's OS-provided temp directory, never all of /var.
    let path = fs::canonicalize(std::env::temp_dir()).ok()?;
    let meta = fs::symlink_metadata(&path).ok()?;
    (meta.is_dir() && meta.uid() == unsafe { libc::getuid() }).then_some(path)
}

pub(crate) fn metadata(home:&Path,raw:&str,args:&Value)->Result<Value,String>{
    let path=match session::read_path(home,raw){Ok(path)=>path,Err(error)=>{
        let path=PathBuf::from(raw);
        if !temporary_root().is_some_and(|root|path.starts_with(root))||fs::canonicalize(&path).ok().as_ref()!=Some(&path)||discovery_inventory::excluded(home,&path){return Err(error);}path
    }};
    scan(home,&path,args,||false)
}

pub(crate) fn inspect(home: &Path, run_id: &str, args: &Value) -> Result<Value, String> {
    let raw = args["path"].as_str().ok_or("Location required")?;
    let path = match session::inspection_path(home, run_id, raw) {
        Ok(path) => path,
        Err(error) => {
            let run = session::tool_run(home, run_id)?;
            let path = PathBuf::from(raw);
            if !run.scope.is_empty() || !temporary_root().is_some_and(|root| path.starts_with(root))
                || path.components().any(|c| matches!(c, std::path::Component::ParentDir))
                || fs::canonicalize(&path).ok().as_ref() != Some(&path)
                || discovery_inventory::excluded(home, &path) {
                return Err(error);
            }
            path
        }
    };
    scan(home, &path, args, || session::inspection_cancelled(home))
}

#[derive(Default)]
struct Totals { allocated: u64, logical: u64, created: u64, modified: u64, files: u64 }

fn timestamp(time: std::io::Result<SystemTime>) -> Option<u64> {
    time.ok()?.duration_since(UNIX_EPOCH).ok().map(|d| d.as_secs())
}

fn scan(home: &Path, root: &Path, args: &Value, cancelled: impl Fn() -> bool) -> Result<Value, String> {
    let observed = timestamp(Ok(SystemTime::now())).ok_or("System clock unavailable")?;
    let hours = args["hours"].as_u64().unwrap_or(6).clamp(1, 168);
    let cutoff = observed.saturating_sub(hours * 3600);
    let seconds = args["seconds"].as_u64().unwrap_or(5).clamp(1, 10);
    let max_entries = args["maxEntries"].as_u64().unwrap_or(50000).clamp(1, 100000);
    let limit = args["limit"].as_u64().unwrap_or(30).clamp(1, 100) as usize;
    let min_bytes = args["minBytes"].as_u64().unwrap_or(1024 * 1024);
    let group_depth = args["groupDepth"].as_u64().unwrap_or(1).clamp(1, 4) as usize;
    let metadata = fs::symlink_metadata(root).map_err(|_| "Cannot inspect this location")?;
    if !metadata.is_dir() || metadata.file_type().is_symlink() { return Err("Use an exact directory, without symlinks".into()); }
    let device = metadata.dev();
    let deadline = Instant::now() + Duration::from_secs(seconds);
    let mut pending = vec![root.to_path_buf()];
    let mut identities = HashSet::new();
    let mut groups = BTreeMap::<PathBuf, Totals>::new();
    let mut windows = vec![1, 3, 6, 12, 24, hours]; windows.sort(); windows.dedup();
    let mut window_bytes = BTreeMap::<u64, u64>::new();
    let mut largest = Vec::<Value>::new();
    let mut latest = Vec::<Value>::new();
    let (mut visited, mut files, mut inaccessible, mut excluded, mut unknown_created, mut duplicates) = (0u64, 0u64, 0u64, 0u64, 0u64, 0u64);
    let (mut allocated, mut logical, mut created_bytes, mut modified_bytes) = (0u64, 0u64, 0u64, 0u64);
    let mut stopped = false;
    'walk: while let Some(directory) = pending.pop() {
        if visited >= max_entries || Instant::now() >= deadline || cancelled() { stopped = true; break; }
        if discovery_inventory::excluded(home, &directory) { excluded += 1; continue; }
        if fs::canonicalize(&directory).ok().as_ref() != Some(&directory) { excluded += 1; continue; }
        let entries = match fs::read_dir(&directory) { Ok(entries) => entries, Err(_) => { inaccessible += 1; continue; } };
        for entry in entries {
            if visited >= max_entries || Instant::now() >= deadline || cancelled() { stopped = true; break 'walk; }
            visited += 1;
            let entry = match entry { Ok(entry) => entry, Err(_) => { inaccessible += 1; continue; } };
            let path = entry.path();
            if discovery_inventory::excluded(home, &path) { excluded += 1; continue; }
            let meta = match fs::symlink_metadata(&path) { Ok(meta) => meta, Err(_) => { inaccessible += 1; continue; } };
            if meta.file_type().is_symlink() || meta.dev() != device || meta.uid() != unsafe { libc::getuid() } { excluded += 1; continue; }
            if meta.is_dir() { pending.push(path); continue; }
            if !meta.is_file() { excluded += 1; continue; }
            if !identities.insert((meta.dev(), meta.ino())) { duplicates += 1; continue; }
            files += 1;
            let bytes = meta.blocks().saturating_mul(512);
            let birth = timestamp(meta.created());
            let modified = timestamp(meta.modified());
            if birth.is_none() { unknown_created += 1; }
            let recent_birth = birth.is_some_and(|t| t >= cutoff && t <= observed);
            let recent_modified = modified.is_some_and(|t| t >= cutoff && t <= observed);
            allocated = allocated.saturating_add(bytes); logical = logical.saturating_add(meta.len());
            if recent_birth { created_bytes = created_bytes.saturating_add(bytes); }
            if recent_modified { modified_bytes = modified_bytes.saturating_add(bytes); }
            for window in &windows {
                if birth.is_some_and(|t| t >= observed.saturating_sub(window * 3600) && t <= observed) {
                    let total = window_bytes.entry(*window).or_default(); *total = total.saturating_add(bytes);
                }
            }
            // Partition files into disjoint descendant buckets, never nested totals.
            let relative = path.strip_prefix(root).unwrap();
            let components = relative.components().collect::<Vec<_>>();
            let group = if components.len() == 1 { root.to_path_buf() } else { root.join(components.iter().take(group_depth.min(components.len()-1)).collect::<PathBuf>()) };
            let total = groups.entry(group).or_default();
            total.allocated = total.allocated.saturating_add(bytes); total.logical = total.logical.saturating_add(meta.len()); total.files += 1;
            if recent_birth { total.created = total.created.saturating_add(bytes); }
            if recent_modified { total.modified = total.modified.saturating_add(bytes); }
            if bytes >= min_bytes && (recent_birth || recent_modified) {
                let row = json!({"path":path,"allocatedBytes":bytes,"logicalBytes":meta.len(),"createdAt":birth,"modifiedAt":modified,"recentlyCreated":recent_birth,"recentlyModified":recent_modified,"reviewOnly":true});
                largest.push(row.clone()); largest.sort_by(|a,b|b["allocatedBytes"].as_u64().cmp(&a["allocatedBytes"].as_u64())); largest.truncate(limit);
                if recent_birth { latest.push(row); latest.sort_by(|a,b|b["createdAt"].as_u64().cmp(&a["createdAt"].as_u64()).then_with(||b["allocatedBytes"].as_u64().cmp(&a["allocatedBytes"].as_u64()))); latest.truncate(limit); }
            }
        }
    }
    let mut grouped = groups.into_iter().map(|(path,t)|json!({"path":path,"allocatedBytes":t.allocated,"logicalBytes":t.logical,"recentlyCreatedBytes":t.created,"recentlyModifiedBytes":t.modified,"files":t.files,"reviewOnly":true})).collect::<Vec<_>>();
    grouped.sort_by(|a,b|b["recentlyCreatedBytes"].as_u64().cmp(&a["recentlyCreatedBytes"].as_u64()).then_with(||b["recentlyModifiedBytes"].as_u64().cmp(&a["recentlyModifiedBytes"].as_u64())));
    let total_groups = grouped.len(); grouped.truncate(limit);
    Ok(json!({"path":root,"observedAt":observed,"since":cutoff,"hours":hours,"allocatedBytes":allocated,"logicalBytes":logical,"recentlyCreatedBytes":created_bytes,"recentlyModifiedBytes":modified_bytes,"windows":windows.into_iter().map(|h|json!({"hours":h,"recentlyCreatedBytes":window_bytes.get(&h).copied().unwrap_or(0)})).collect::<Vec<_>>(),"groups":grouped,"groupsOmitted":total_groups.saturating_sub(limit),"largestRecentFiles":largest,"latestCreatedFiles":latest,"coverage":{"partial":stopped||inaccessible>0||excluded>0,"budgetReachedOrCancelled":stopped,"entriesInspected":visited,"filesInspected":files,"inaccessible":inaccessible,"excluded":excluded,"unknownCreationTimes":unknown_created,"hardLinksDeduplicated":duplicates},"reviewOnly":true,"note":"Current allocated size of recently created/modified files, NOT measured growth or guaranteed reclaimable space. Modified bytes include old file contents. Creation times can reflect copies/downloads, not the originating process. Window totals overlap; groups partition scanned files (root bucket is direct files only). Hard links count once; APFS clones may share extents. Partial results are lower bounds. No contents opened, cloud files downloaded, process attribution claimed, or cleanup authorized. Drill into a group with another bounded call."}))
}

#[cfg(test)]
mod tests {
    use super::*;
    fn fixture() -> PathBuf {
        let root = fs::canonicalize(std::env::temp_dir()).unwrap().join(format!("br-recent-{}-{}", std::process::id(), SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_nanos()));
        fs::create_dir_all(root.join("build/debug")).unwrap(); root
    }
    #[test]
    fn groups_recent_files_without_counting_hardlinks_twice() {
        let root = fixture(); fs::write(root.join("build/debug/artifact"), vec![0u8;8192]).unwrap();
        fs::hard_link(root.join("build/debug/artifact"),root.join("build/debug/copy")).unwrap();
        fs::write(root.join(".env.secret"), b"not scanned").unwrap();
        std::os::unix::fs::symlink("/",root.join("escape")).unwrap();
        let result = scan(&root,&root,&json!({"minBytes":0}),||false).unwrap();
        assert_eq!(result["logicalBytes"],8192); assert_eq!(result["coverage"]["hardLinksDeduplicated"],1);
        assert_eq!(result["coverage"]["excluded"],2); assert_eq!(result["groups"].as_array().unwrap().len(),1);
        assert_eq!(result["recentlyCreatedBytes"],result["allocatedBytes"]);
        assert_eq!(result["latestCreatedFiles"].as_array().unwrap().len(),1);
        assert_eq!(result["reviewOnly"],true); fs::remove_dir_all(root).unwrap();
    }
    #[test]
    fn budgets_and_cancellation_are_explicit() {
        let root = fixture();
        for i in 0..5 { fs::write(root.join(format!("file-{i}")),b"fixture").unwrap(); }
        let result = scan(&root,&root,&json!({"maxEntries":1}),||false).unwrap();
        assert_eq!(result["coverage"]["entriesInspected"],1); assert_eq!(result["coverage"]["partial"],true);
        let result = scan(&root,&root,&json!({}),||true).unwrap();
        assert_eq!(result["coverage"]["entriesInspected"],0); assert_eq!(result["coverage"]["partial"],true);
        fs::remove_dir_all(root).unwrap();
    }
}
