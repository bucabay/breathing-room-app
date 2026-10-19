//! Discovery-only personal/app storage. Never produces an executable action.
use crate::{cleanup_session as session, discovery_inventory};
use serde::{Deserialize, Serialize};
use serde_json::{json, Value};
use std::{collections::{HashSet, VecDeque}, fs, os::unix::fs::MetadataExt, path::{Path, PathBuf}, time::{Duration, Instant}};

// Search locations, formats and storage semantics, never a vendor-name allowlist.
const STORAGE_ROOTS: &[&str] = &["Library/Application Support", "Movies", "Music", "Pictures", "Documents", "Downloads", "Desktop", "Library/Containers"];
const PROJECT_BUNDLES: &[&str] = &["cap", "screenstudio", "screenflow", "cmproj", "logicx", "band", "fcpbundle", "imovielibrary", "scriv", "vmwarevm", "pvm", "utm"];
const PROJECT_FILES: &[&str] = &["blend", "psd", "psb", "ai", "aep", "prproj", "drp", "rpp", "als", "flp", "c4d", "sketch", "tscproj", "mlt", "vdi", "vmdk", "qcow2"];
const COLLECTIONS: &[&str] = &["recordings", "captures", "projects", "sessions", "libraries", "exports", "renders", "media", "virtual machines", "models"];
const MEDIA: &[&str] = &["mp4", "mov", "m4v", "webm", "mkv", "avi", "mp3", "wav", "m4a", "aiff", "flac", "jpg", "jpeg", "png", "heic", "raw"];
const MIN_LARGE_FILE: u64 = 32 * 1024 * 1024;

fn extension(path: &Path) -> String { path.extension().unwrap_or_default().to_string_lossy().to_ascii_lowercase() }
fn app_data(home: &Path, path: &Path) -> bool {
    path.starts_with(home.join("Library/Application Support")) || path.starts_with(home.join("Library/Containers"))
}
fn collection(path: &Path) -> bool { COLLECTIONS.contains(&path.file_name().unwrap_or_default().to_string_lossy().to_ascii_lowercase().as_str()) }
fn traversal_excluded(home: &Path, path: &Path) -> bool {
    if discovery_inventory::excluded(home, path) { return true; }
    let name=path.file_name().unwrap_or_default().to_string_lossy().to_ascii_lowercase();
    ["node_modules", ".git", ".venv", "vendor", "target", ".next", "extensions", "sync data", "backup", "backups"].contains(&name.as_str()) || name.ends_with(".app") ||
        (app_data(home,path)&&["cache", "caches", "code cache", "gpucache", "cacheddata", "media cache", "media cache files"].contains(&name.as_str()))
}

#[derive(Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct Risk {
    pub severity: String,
    pub recoverability: String,
    pub warning: String,
}

#[derive(Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct Location {
    pub path: String, pub title: String, pub bytes: u64, pub logical_bytes: u64,
    #[serde(default)] pub aliases: Vec<String>,
    pub modified_at: u64, pub file_count: usize, pub partial: bool,
    #[serde(flatten)] pub risk: Risk,
    pub review_only: bool, pub cleanup_eligible: bool, pub requires_selection: bool,
}

pub fn managed_project(home: &Path, path: &Path) -> bool {
    path.ancestors().any(|parent| PROJECT_BUNDLES.contains(&extension(parent).as_str())) ||
        (app_data(home,path) && path.ancestors().take_while(|p| *p != home).any(|parent| ["recordings", "captures"].contains(&parent.file_name().unwrap_or_default().to_string_lossy().to_ascii_lowercase().as_str())))
}

pub fn protected_storage(home: &Path, path: &Path) -> bool {
    managed_project(home,path) || (app_data(home,path) && path.ancestors().take_while(|p|*p!=home).any(collection))
}

pub fn risk(home: &Path, path: &Path) -> Option<Risk> {
    // Owning-project semantics take precedence over misleading Cache/dist names.
    let managed = managed_project(home, path);
    let relative = path.strip_prefix(home).unwrap_or(path).to_string_lossy();
    let app_data = relative.starts_with("Library/Application Support/") || relative.starts_with("Library/Containers/");
    let cache = relative.starts_with("Library/Caches/") || relative.starts_with(".cache/") || (app_data && path.components().any(|part| ["cache", "caches", "code cache", "gpucache", "cacheddata", "media cache", "media cache files"].contains(&part.as_os_str().to_string_lossy().to_ascii_lowercase().as_str())));
    if !protected_storage(home,path) && cache { return None; }
    let original = managed || MEDIA.contains(&extension(path).as_str()) || PROJECT_FILES.contains(&extension(path).as_str());
    if original {
        return Some(Risk { severity: "critical".into(), recoverability: "not-rebuildable".into(), warning: "Original media, editable project or virtual-machine data. Breathing Room cannot recreate this after deletion; recovery requires a separate usable backup. Exports may omit source assets, edit history or machine state. Select deliberately and use the owning app to review removal.".into() });
    }
    Some(Risk { severity: "warning".into(), recoverability: "unknown".into(), warning: "Rebuildability and backup status are unverified. This may contain unique files, settings or app state. It is not approved cleanup; select it for manual/owning-app review before considering removal.".into() })
}

pub fn known_locations(home: &Path, scope: Option<&Path>) -> Vec<PathBuf> {
    let roots=scope.map(|path|vec![path.to_path_buf()]).unwrap_or_else(||STORAGE_ROOTS.iter().map(|relative|home.join(relative)).chain(std::iter::once(home.to_path_buf())).collect());
    roots.into_iter().filter(|path| {
        scope.is_none_or(|s| path.starts_with(s)) && !discovery_inventory::excluded(home, path) &&
        session::read_path(home, &path.to_string_lossy()).is_ok() && fs::symlink_metadata(path).is_ok_and(|m| !m.file_type().is_symlink() && m.uid() == unsafe { libc::getuid() })
    }).collect()
}

pub fn leads(home: &Path, scope: Option<&Path>) -> Vec<Value> {
    known_locations(home, scope).into_iter().map(|path| json!({"path":path,"storageKind":if app_data(home,&path){"application-storage-root"}else{"user-storage-root"},"reviewOnly":true,"cleanupEligible":false,"note":"Enumerate actual applications and large files here; app names are not an allowlist. Source projects/media need explicit owning-app review; other data has unknown rebuildability."})).collect()
}

pub fn retain(locations: &mut Vec<Location>, mut item: Location) {
    if locations.iter().any(|old|old.path==item.path&&!old.partial&&item.partial){return;}
    if let Ok(meta)=fs::symlink_metadata(&item.path){if meta.is_file(){if let Some(old)=locations.iter_mut().find(|old|old.path!=item.path&&fs::symlink_metadata(&old.path).is_ok_and(|other|other.is_file()&&other.dev()==meta.dev()&&other.ino()==meta.ino())){
        if item.risk.severity=="critical"&&old.risk.severity!="critical"{item.aliases.extend(old.aliases.clone());item.aliases.push(old.path.clone());*old=item;}else if !old.aliases.contains(&item.path){old.aliases.push(item.path);}return;
    }}}
    // Prefer specific project/file rows over a later broad app/home measurement.
    if locations.iter().any(|old| old.path != item.path && Path::new(&old.path).starts_with(&item.path)) { return; }
    locations.retain(|old| !Path::new(&item.path).starts_with(&old.path));
    if locations.len() < 500 { locations.push(item); locations.sort_by(|a,b| b.bytes.cmp(&a.bytes).then_with(|| a.path.cmp(&b.path))); }
}

pub fn measure(home: &Path, raw: &Path, deadline: Instant, remaining: &mut usize) -> Result<Location, String> {
    let path = session::read_path(home, &raw.to_string_lossy())?;
    if discovery_inventory::excluded(home, &path) { return Err("Protected storage is excluded".into()); }
    let risk = risk(home, &path).ok_or("Cache storage belongs in supported cleanup discovery")?;
    let root = fs::symlink_metadata(&path).map_err(|e| e.to_string())?;
    if root.uid() != unsafe { libc::getuid() } { return Err("Not owned by the current user".into()); }
    let mut result = Location { path: path.to_string_lossy().into_owned(), aliases:vec![], title: path.file_name().unwrap_or_default().to_string_lossy().into_owned(), bytes: 0, logical_bytes: 0, modified_at: root.mtime().max(0) as u64, file_count: 0, partial: false, risk, review_only: true, cleanup_eligible: false, requires_selection: true };
    let mut stack = vec![path]; let mut seen = HashSet::new();
    while let Some(path) = stack.pop() {
        if *remaining == 0 || Instant::now() >= deadline || session::inspection_cancelled(home) { result.partial = true; break; }
        *remaining -= 1;
        let Ok(meta) = fs::symlink_metadata(&path) else { result.partial = true; continue; };
        if meta.file_type().is_symlink() || meta.dev() != root.dev() || meta.uid() != root.uid() || discovery_inventory::excluded(home, &path) || !fs::canonicalize(&path).is_ok_and(|p| p == path) { result.partial = true; continue; }
        if meta.is_file() {
            if seen.insert((meta.dev(), meta.ino())) { result.bytes = result.bytes.saturating_add(meta.blocks().saturating_mul(512)); result.logical_bytes = result.logical_bytes.saturating_add(meta.len()); result.file_count += 1; }
        } else if meta.is_dir() {
            match fs::read_dir(&path) {
                Ok(entries) => for entry in entries {
                    if stack.len() >= *remaining || Instant::now() >= deadline { result.partial = true; break; }
                    match entry { Ok(entry) => stack.push(entry.path()), Err(_) => result.partial = true }
                },
                Err(_) => result.partial = true,
            }
        } else { result.partial = true; }
    }
    Ok(result)
}

pub fn discover(home: &Path, scope: Option<&Path>) -> (Vec<Location>, Vec<String>) {
    let started=Instant::now();let discovery_deadline=started+Duration::from_secs(2);let deadline=started+Duration::from_secs(7);
    let mut remaining=50_000;let mut inspected=0;let mut locations=vec![];let mut errors=vec![];
    let mut queue=VecDeque::new();let mut seen=HashSet::new();let mut candidates=vec![];
    for root in known_locations(home,scope){if let Ok(meta)=fs::symlink_metadata(&root){queue.push_back((root,0,meta.dev(),false));}}
    while let Some((path,depth,device,in_collection))=queue.pop_front(){
        if inspected>=50_000||Instant::now()>=discovery_deadline||session::inspection_cancelled(home){errors.push("Application-storage discovery is partial: metadata/time budget reached; continue inventory or inspect a narrower location".into());break;}
        inspected+=1;
        if !seen.insert(path.clone())||discovery_inventory::excluded(home,&path){continue;}
        let Ok(meta)=fs::symlink_metadata(&path)else{errors.push(format!("Cannot inspect {}",path.display()));continue;};
        if meta.file_type().is_symlink()||meta.dev()!=device||meta.uid()!=unsafe{libc::getuid()}||!fs::canonicalize(&path).is_ok_and(|p|p==path){continue;}
        // Do not enter recognized projects or collections' project subfolders.
        // The entire project is one warning/selection row, regardless of vendor.
        let large_file=meta.blocks().saturating_mul(512)>=MIN_LARGE_FILE;
        let project_file=PROJECT_FILES.contains(&extension(&path).as_str());
        let exact_file=scope.is_some_and(|s|s==path.as_path());
        if (meta.is_dir()&&(PROJECT_BUNDLES.contains(&extension(&path).as_str())||in_collection)) ||
            (meta.is_file()&&(large_file||project_file||exact_file)){
            if risk(home,&path).is_some(){candidates.push((meta.blocks().saturating_mul(512),path));}
            continue;
        }
        if traversal_excluded(home,&path)||!meta.is_dir(){continue;}
        if depth>=8{errors.push(format!("Application-storage depth limit reached under {}",path.display()));continue;}
        let children=match fs::read_dir(&path){Ok(entries)=>entries,Err(_)=>{errors.push(format!("Cannot list {}",path.display()));continue;}};
        let mut entries=vec![];let mut any_directories=false;let is_collection=collection(&path);
        for entry in children{
            if entries.len()>=1000||entries.len()+queue.len()+inspected>=50_000||Instant::now()>=discovery_deadline{errors.push(format!("Application-storage enumeration is partial under {}",path.display()));break;}
            match entry{Ok(entry)=>{any_directories|=entry.file_type().is_ok_and(|m|m.is_dir());entries.push(entry.path());},Err(_)=>errors.push(format!("Some entries could not be listed under {}",path.display()))}
        }
        // Loose recording/model files can be individually small but large together.
        if is_collection&&!any_directories&&scope.is_none_or(|s|path.starts_with(s))&&risk(home,&path).is_some(){candidates.push((0,path));continue;}
        entries.sort();queue.extend(entries.into_iter().map(|p|(p,depth+1,device,is_collection)));
    }
    // Large individual files first; directory/project totals are measured below.
    candidates.sort_by(|a,b|b.0.cmp(&a.0).then_with(||a.1.cmp(&b.1)));
    if candidates.len()>500{candidates.truncate(500);errors.push("Application-storage review is limited to 500 locations; continue inventory for remaining files".into());}
    for (_,path) in candidates{
        if Instant::now()>=deadline||remaining==0{errors.push("Application-storage measurement is partial: budget reached; inspect remaining locations individually".into());break;}
        match measure(home,&path,deadline,&mut remaining){Ok(item)if item.bytes>0||item.partial=>retain(&mut locations,item),Ok(_)=>{},Err(error)=>errors.push(format!("{}: {error}",path.display()))}
    }
    errors.truncate(80);
    locations.sort_by(|a,b| b.bytes.cmp(&a.bytes).then_with(|| a.path.cmp(&b.path)));
    (locations, errors)
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn major_project_formats_and_unrecognized_app_payloads_are_discovered_without_vendor_paths() {
        let home=fs::canonicalize(std::env::temp_dir()).unwrap().join(format!("br-generic-storage-{}-{}",std::process::id(),crate::model::now()));
        let unknown=home.join("Library/Application Support/An App Never Listed/custom-shards/large.payload");
        fs::create_dir_all(unknown.parent().unwrap()).unwrap();fs::write(&unknown,vec![1;33*1024*1024]).unwrap();
        let movie=home.join("Movies/Another Unknown Recorder/take.mov");fs::create_dir_all(movie.parent().unwrap()).unwrap();fs::hard_link(&unknown,&movie).unwrap();
        let custom=home.join(".unlisted-tool-shards/a/weights.payload");fs::create_dir_all(custom.parent().unwrap()).unwrap();fs::hard_link(&unknown,&custom).unwrap();
        let projects=["Music/Album.logicx", "Documents/Film.fcpbundle", "Movies/Session.screenstudio", "Documents/Workstation.vmwarevm"];
        for relative in projects{let path=home.join(relative);fs::create_dir_all(path.join("Cache")).unwrap();fs::write(path.join("Cache/original.bin"),vec![1;4096]).unwrap();}
        let document=home.join("Pictures/artwork.psd");fs::create_dir_all(document.parent().unwrap()).unwrap();fs::write(&document,vec![1;4096]).unwrap();
        let session=home.join("Library/Containers/org.never-listed.recorder/Data/Library/Application Support/Unknown/sessions/Session A");
        fs::create_dir_all(session.join("Cache")).unwrap();fs::write(session.join("Cache/source.blob"),vec![1;4096]).unwrap();
        let cache=home.join("Library/Application Support/Other App/Cache");fs::create_dir_all(&cache).unwrap();fs::hard_link(&unknown,cache.join("payload.bin")).unwrap();
        let linked=home.join("Movies/Linked.cap");std::os::unix::fs::symlink(home.join("Music/Album.logicx"),&linked).unwrap();
        let (items,errors)=discover(&home,None);assert!(errors.is_empty(),"{errors:?}");
        let find=|path:&Path|items.iter().find(|item|Path::new(&item.path)==path||item.aliases.iter().any(|alias|Path::new(alias)==path)).unwrap();
        assert_eq!(risk(&home,&unknown).unwrap().recoverability,"unknown");assert_eq!(risk(&home,&custom).unwrap().recoverability,"unknown");assert_eq!(find(&movie).risk.recoverability,"not-rebuildable");
        // All three fixture paths are hard links: one row, strongest loss warning,
        // aliases retained instead of counting the same physical file three times.
        assert_eq!(find(&unknown).path,find(&movie).path);assert_eq!(find(&custom).path,find(&movie).path);assert_eq!(find(&movie).aliases.len(),2);
        for relative in projects{assert_eq!(find(&home.join(relative)).risk.severity,"critical");}
        assert_eq!(find(&document).risk.severity,"critical");assert_eq!(find(&session).risk.recoverability,"unknown");
        assert!(!items.iter().any(|item|Path::new(&item.path).starts_with(&cache)||Path::new(&item.path)==linked));
        let action=crate::cleanup_discovery::action("Misleading cache",session.join("Cache"),vec![],"Fixture");assert!(session::validate_action(&home,&action).is_err());
        let (scoped,errors)=discover(&home,Some(&home.join("Documents")));assert!(errors.is_empty());assert!(!scoped.is_empty());assert!(scoped.iter().all(|item|Path::new(&item.path).starts_with(home.join("Documents"))));
        let small=home.join("Movies/small.webm");fs::write(&small,vec![1;4096]).unwrap();
        let (exact,errors)=discover(&home,Some(&small));assert!(errors.is_empty());assert_eq!(exact.len(),1);assert_eq!(exact[0].path,small.to_string_lossy());assert_eq!(exact[0].risk.severity,"critical");
        assert!(items.iter().all(|item|item.requires_selection&&item.review_only&&!item.cleanup_eligible));
        assert!(unknown.exists());fs::remove_dir_all(home).unwrap();
    }
    #[test]
    fn cap_projects_are_measured_but_never_cleanup_candidates() {
        let home = fs::canonicalize(std::env::temp_dir()).unwrap().join(format!("br-review-{}-{}", std::process::id(), crate::model::now()));
        let root = home.join("Library/Application Support/so.cap.desktop/recordings"); let project = root.join("Example.cap");
        fs::create_dir_all(project.join("content/Cache")).unwrap(); fs::write(project.join("content/Cache/source.mp4"), vec![0;4096]).unwrap();
        fs::hard_link(project.join("content/Cache/source.mp4"), project.join("duplicate.mp4")).unwrap();
        fs::write(project.join(".env.private"), b"never inspect").unwrap();
        let (items, _) = discover(&home, None); assert_eq!(items.len(),1); let item = &items[0];
        assert_eq!(item.logical_bytes,4096); assert_eq!(item.file_count,1); assert!(item.partial);
        assert_eq!(item.risk.severity,"critical"); assert_eq!(item.risk.recoverability,"not-rebuildable"); assert!(!item.cleanup_eligible);
        assert!(known_locations(&home,Some(&home.join("Downloads"))).is_empty());
        assert!(discover(&home,Some(&home.join("Downloads"))).0.is_empty());
        let action = crate::cleanup_discovery::action("Not a cache", project.join("content/Cache"), vec![], "fixture");
        assert!(session::validate_action(&home,&action).is_err()); assert!(project.join("content/Cache/source.mp4").exists());
        assert!(session::tool_trash(&home,&project.join("content/Cache").to_string_lossy()).is_err());
        let parent=measure(&home,&root,Instant::now()+Duration::from_secs(1),&mut 100).unwrap();
        let mut retained=items.clone();retain(&mut retained,parent);assert_eq!(retained.len(),1);assert_eq!(retained[0].path,item.path);
        let budget = measure(&home,&project,Instant::now(),&mut 10).unwrap(); assert!(budget.partial); assert_eq!(budget.bytes,0);
        std::os::unix::fs::symlink(&project,root.join("Linked.cap")).unwrap();
        assert_eq!(discover(&home,None).0.len(),1);
        fs::remove_dir_all(home).unwrap();
    }
    #[test]
    fn unknown_app_data_is_not_claimed_rebuildable_and_old_discoveries_still_load() {
        let home=Path::new("/Users/fixture");
        assert_eq!(risk(home,&home.join("Library/Application Support/Unlisted/projects")).unwrap().recoverability,"unknown");
        assert!(risk(home,&home.join("Library/Caches/Example")).is_none());
        assert!(risk(home,&home.join("Library/Caches/Example/icon.png")).is_none());
        assert_eq!(risk(home,&home.join("Documents/Cache/source.mov")).unwrap().severity,"critical");
        assert_eq!(risk(home,&home.join("Movies/demo.mov")).unwrap().severity,"critical");
        let old=serde_json::json!({"candidates":[],"manual":[],"coverage":[],"errors":[],"discoveredAt":0,"snapshotHash":"fixture"});
        let discovery:crate::cleanup_discovery::Discovery=serde_json::from_value(old).unwrap();
        assert!(discovery.review_locations.is_empty());
    }
}
