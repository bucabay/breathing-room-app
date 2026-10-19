//! Discover exact measured/native-verified candidates before asking an LLM to rank them.
use crate::{cleanup_session as session, model::now};
use serde::{Serialize,Deserialize};
use serde_json::json;
use sha2::{Digest,Sha256};
use std::{collections::{HashSet,VecDeque},fs,os::unix::fs::MetadataExt,path::{Path,PathBuf},time::{Duration,Instant}};

#[derive(Clone,Serialize,Deserialize,Default)]
#[serde(rename_all="camelCase")]
pub struct Discovery{pub candidates:Vec<session::Action>,pub manual:Vec<Manual>,pub coverage:Vec<String>,pub errors:Vec<String>,pub discovered_at:u64,pub snapshot_hash:String,
    #[serde(default)]pub review_locations:Vec<crate::review_storage::Location>,
    #[serde(default)]pub inventory:Option<crate::discovery_inventory::Summary>,
    #[serde(default)]pub agent:Option<Assistance>,
    #[serde(default)]pub pending_sources:Vec<String>,
    #[serde(default)]pub recent_findings:Vec<serde_json::Value>,
    #[serde(default)]pub sources:std::collections::BTreeMap<String,Vec<String>>,
    #[serde(default)]pub observed_at:std::collections::BTreeMap<String,u64>}
#[derive(Clone,Serialize,Deserialize)]
#[serde(rename_all="camelCase")]
pub struct Assistance{pub triggered:bool,pub reason:String,pub useful_locations:usize,pub measured_candidate_bytes:u64,pub policy:Policy,pub tool_calls:usize,pub learned_rules:usize,pub status:String}
#[derive(Clone,Serialize,Deserialize)]
#[serde(rename_all="camelCase")]
pub struct Policy{pub minimum_locations:usize,pub minimum_bytes:u64,pub useful_location_bytes:u64,pub max_turns:usize,pub max_tool_calls:usize}
impl Default for Policy{fn default()->Self{Self{minimum_locations:4,minimum_bytes:2*1024*1024*1024,useful_location_bytes:64*1024*1024,max_turns:24,max_tool_calls:128}}}
impl Policy{pub fn validate(&self)->Result<(),String>{if self.minimum_locations>100||self.minimum_bytes>1024*1024*1024*1024||self.useful_location_bytes>1024*1024*1024*1024||!(1..=32).contains(&self.max_turns)||!(1..=192).contains(&self.max_tool_calls){return Err("Invalid agent discovery limits".into());}Ok(())}}
#[derive(Clone,Serialize,Deserialize)]
#[serde(rename_all="camelCase")]
pub struct Options{pub profiles:Vec<String>,pub roots:Vec<String>,#[serde(default)]pub policy:Policy,#[serde(default)]pub daily_care:bool}
impl Default for Options{fn default()->Self{Self{profiles:vec!["everyday".into(),"developer".into(),"builder".into(),"creator".into()],roots:vec![],policy:Policy::default(),daily_care:false}}}
impl Options{fn projects(&self)->bool{self.profiles.iter().any(|p|p=="developer"||p=="builder")}}
// Shared by automatic discovery and typed inspection tools. No shell interpolation.
pub const CACHE_QUERIES:&[(&str,&[&str],&[&str],&str)]=&[
    ("npm", &["config","get","cache"], &["cache","clean","--force"], "npm package cache"),
    ("uv", &["cache","dir"], &["cache","prune"], "Unused uv package cache"),
    ("python3", &["-m","pip","cache","dir"], &["-m","pip","cache","purge"], "pip package downloads"),
    ("pnpm", &["store","path"], &["store","prune"], "Unreferenced pnpm packages"),
    ("go-build", &["env","GOCACHE"], &["clean","-cache"], "Go build cache"),
    ("go-modules", &["env","GOMODCACHE"], &["clean","-modcache"], "Go module cache"),
    ("bun", &["pm","cache"], &["pm","cache","rm"], "Bun package cache"),
    ("yarn", &["cache","dir"], &["cache","clean"], "Yarn package cache"),
];
pub fn cache_query(tool:&str)->Result<Vec<String>,String>{let (_,query,_,_)=CACHE_QUERIES.iter().find(|(name,_,_,_)|*name==tool).ok_or("Unknown cache tool")?;Ok(std::iter::once(if tool.starts_with("go-"){"go"}else{tool}).chain(query.iter().copied()).map(str::to_owned).collect())}
fn excluded(name:&str)->bool{[".ssh",".aws",".gnupg","Keychains","CloudStorage","Mobile Documents","Mail","Messages",".Trash","node_modules","target","dist",".next",".git",".worktrees",".venv","vendor",".ruff_cache",".pytest_cache",".mypy_cache","extensions","Local Storage","Session Storage","IndexedDB","Service Worker","Sync Data","shared_proto_db","optimization_guide_model_store"].contains(&name)||name.starts_with(".env")||name.ends_with(".app")}
const PROJECT_MARKERS:&[&str]=&["package.json","Cargo.toml","pyproject.toml","go.mod"];
const ARTIFACTS:&[&str]=&[".next","dist","target",".ruff_cache",".pytest_cache",".mypy_cache"];
const APP_CACHES:&[&str]=&["Cache","Caches","Code Cache","GPUCache","CachedData","Media Cache","Media Cache Files"];
// Enumerate metadata only, never follow symlinks or cross a volume implicitly.
// Callers share the directory and wall-clock budget across roots.
fn walk(home:&Path,root:&Path,max_depth:usize,deadline:Instant,remaining:&mut usize,errors:&mut Vec<String>,mut visit:impl FnMut(&Path)->bool){
    let device=fs::symlink_metadata(root).map(|m|m.dev()).ok();
    let mut queue=VecDeque::from([(root.to_path_buf(),0)]);
    let mut budget_noted=false;
    while let Some((path,depth))=queue.pop_front(){
        if *remaining==0||Instant::now()>=deadline{errors.push(format!("Directory/time budget reached under {}",root.display()));break;}
        *remaining-=1;
        if *remaining%64==0&&session::inspection_cancelled(home){errors.push("Discovery cancelled".into());break;}
        let Ok(meta)=fs::symlink_metadata(&path)else{errors.push(format!("Cannot inspect {}",path.display()));continue;};
        if !meta.is_dir()||meta.file_type().is_symlink()||Some(meta.dev())!=device{continue;}
        if !visit(&path)||depth>=max_depth{continue;}
        match fs::read_dir(&path){Ok(entries)=>{
            let mut children=vec![];
            for entry in entries{if queue.len()+children.len()>=*remaining{if !budget_noted{errors.push(format!("Directory budget limits enumeration under {}",root.display()));budget_noted=true;}break;}match entry{Ok(entry)=>{let name=entry.file_name();if !excluded(&name.to_string_lossy())&&entry.file_type().is_ok_and(|kind|kind.is_dir()&&!kind.is_symlink()){children.push(entry.path());}},Err(_)=>errors.push(format!("Incomplete enumeration under {}",path.display()))}}
            children.sort();queue.extend(children.into_iter().map(|p|(p,depth+1)));
        },Err(_)=>errors.push(format!("Cannot enumerate {} (permissions or unavailable)",path.display()))}
    }
}
#[derive(Clone,Serialize,Deserialize)]pub struct Manual{pub path:String,pub reason:String}
const TAG:&str="Signature: 8a477f597d28d172789f06886806bc55";
pub fn automatic_path(home:&Path,raw:&str)->Result<PathBuf,String>{
    let path=session::tool_path(home,raw)?;
    if path.file_name().is_none_or(|name|name!=".ruff_cache"){return Err("Only registered Ruff lint caches can be cleared automatically".into());}
    session::tool_trash(home,raw)?;
    let marker=path.join("CACHEDIR.TAG");let meta=fs::symlink_metadata(&marker).map_err(|_|"Cache tag missing")?;
    if meta.file_type().is_symlink()||meta.len()>4096||meta.uid()!=unsafe{libc::getuid()}{return Err("Cache tag is not owned regular metadata".into());}
    let tag=fs::read_to_string(marker).map_err(|_|"Cache tag is unavailable")?;
    if !tag.starts_with(TAG){return Err("Cache tag signature does not match".into());}
    // Keep automatic cleanup small and independent of arbitrary app/profile data.
    let mut stack=vec![path.clone()];let mut seen=0;
    while let Some(dir)=stack.pop(){for entry in fs::read_dir(dir).map_err(|_|"Cache inspection incomplete")?{let entry=entry.map_err(|_|"Cache inspection incomplete")?;seen+=1;if seen>20000{return Err("Cache is too large for automatic inspection".into());}let meta=fs::symlink_metadata(entry.path()).map_err(|_|"Cache changed")?;
        if meta.file_type().is_symlink()||meta.uid()!=unsafe{libc::getuid()}||entry.file_name().to_string_lossy().starts_with(".env")||[".git",".ssh","credentials","auth.json"].contains(&entry.file_name().to_string_lossy().as_ref()){return Err("Cache contains linked or protected entries".into());}
        if meta.is_dir(){stack.push(entry.path());}else if !meta.is_file(){return Err("Cache contains unsupported entries".into());}
    }}Ok(path)
}
pub fn measured(home:&Path,path:&Path)->Result<u64,String>{
    let text=session::tool_output(home,&["du".into(),"-skx".into(),path.to_string_lossy().into_owned()],None,15)?;
    text.split_whitespace().next().and_then(|n|n.parse::<u64>().ok()).and_then(|n|n.checked_mul(1024)).ok_or("Could not measure allocated size".into())
}
pub(crate) fn action(title:&str,path:PathBuf,command:Vec<String>,impact:&str)->session::Action{
    let kind=if command.is_empty(){"trash"}else{"command"};
    let paths=vec![path.to_string_lossy().into_owned()];let key=json!({"kind":kind,"paths":paths,"command":command});
    let digest=format!("{:x}",Sha256::digest(key.to_string().as_bytes()));
    let id=format!("c-{}",&digest[..12]);
    let title=title.chars().scan(0usize,|units,ch|{if *units+ch.len_utf16()>160{None}else{*units+=ch.len_utf16();Some(ch)}}).collect();
    session::Action{id,title,reason:"Measured native cleanup candidate".into(),impact:impact.into(),kind:kind.into(),paths,command,cwd:None,estimated_bytes:0,mode:if kind=="command"{"command"}else{"permission"}.into(),native_rule:"native-exact-scope-v2".into()}
}
fn add(home:&Path,scope:Option<&Path>,found:&mut Discovery,mut item:session::Action,deadline:Instant){
    if Instant::now()>=deadline||session::inspection_cancelled(home){return;}
    if let Some(scope)=scope{if item.paths.iter().any(|path|!Path::new(path).starts_with(scope)){return;}}
    if found.candidates.iter().any(|old|old.paths.iter().any(|old_path|item.paths.iter().any(|new|Path::new(old_path).starts_with(new)||Path::new(new).starts_with(old_path)))){return;}
    let checked=(||{session::validate_action(home,&item)?;let seconds=deadline.saturating_duration_since(Instant::now()).as_secs().min(10);if seconds==0{return Err("Discovery time budget reached".into());}let text=session::tool_output(home,&["du".into(),"-skx".into(),item.paths[0].clone()],None,seconds)?;let bytes=text.split_whitespace().next().and_then(|n|n.parse::<u64>().ok()).and_then(|n|n.checked_mul(1024)).ok_or("Could not measure allocated size")?;if bytes==0{return Err("Empty location".into());}Ok(bytes)})();
    match checked{Ok(bytes)=>{item.estimated_bytes=bytes;if Path::new(&item.paths[0]).file_name().is_some_and(|name|name==".ruff_cache")&&bytes<=512*1024*1024&&automatic_path(home,&item.paths[0]).is_ok(){item.mode="automatic".into();item.native_rule="owned-tagged-ruff-cache-v1".into();item.impact="Ruff analysis cache regenerates on the next lint run. Moved to Trash; space is reclaimed only when Trash is emptied.".into();}found.candidates.push(item);},Err(reason)=>{if reason!="Empty location"{
        let path=Path::new(&item.paths[0]);
        if crate::review_storage::risk(home,path).is_some(){if let Ok(location)=crate::review_storage::measure(home,path,deadline.min(Instant::now()+Duration::from_secs(2)),&mut 10_000){if location.bytes>0||location.partial{crate::review_storage::retain(&mut found.review_locations,location);}}}
        found.manual.push(Manual{path:item.paths[0].clone(),reason});
    }}}
}
pub fn scan(home:&Path,scope_raw:&str,options:&Options,mut progress:impl FnMut(&str))->Result<Discovery,String>{
    options.policy.validate()?;
    let scope=if scope_raw.is_empty(){None}else{Some(session::read_path(home,scope_raw)?)};
    let mut found=Discovery{discovered_at:now(),..Default::default()};let deadline=Instant::now()+Duration::from_secs(110);
    progress("Large files and projects across application/media storage (review only)");
    let (locations,errors)=crate::review_storage::discover(home,scope.as_deref());
    found.review_locations=locations;found.errors.extend(errors);
    // One read-only owning-tool lookup supplies the exact path AND method; no model guessing.
    for (key,_,command,title) in CACHE_QUERIES.iter().filter(|_|options.projects()&&scope.is_none()){
        let tool=if key.starts_with("go-"){"go"}else{key};
        if Instant::now()>deadline||session::inspection_cancelled(home){break;}if !session::tool_available(home,tool){continue;}progress(title);
        let argv=cache_query(key)?;
        if let Ok(output)=session::tool_output(home,&argv,None,5){if let Ok(root)=session::tool_path(home,output.trim()){
            let path=if tool=="npm"&&root.join("_cacache").is_dir(){root.join("_cacache")}else{root};
            let argv=std::iter::once(tool.to_string()).chain(command.iter().map(|s|s.to_string())).collect();
            add(home,scope.as_deref(),&mut found,action(title,path,argv,"The owning tool removes cache data. Stop related installs/builds first; packages may need downloading again. Prune may remove only part of the measured store."),deadline);
        }}
    }
    for (relative,title,impact) in [
        (".npm/_npx","Cached npx environments","Stop npx jobs first. Later runs download packages again. Moving to Trash reclaims space only when emptied."),
        ("Library/Developer/Xcode/DerivedData","Xcode generated build data","Quit Xcode and stop builds first. Indexes and builds regenerate; archives and settings are preserved."),
        ("Library/Caches/ms-playwright","Downloaded Playwright browsers","Stop automation first. Reinstall required browsers before running tests again."),
        (".cache/pre-commit","Generated pre-commit environments","Stop hooks first. Environments reinstall on the next hook run."),
        (".cache/prisma","Prisma downloaded engines","Stop Prisma jobs first. Engines may need downloading again."),
        ("Library/Caches/dotslash","DotSlash downloaded binaries","Stop dependent tool jobs first. Binaries download again when needed."),
    ].into_iter().filter(|_|options.projects()){let path=home.join(relative);if scope.as_ref().is_some_and(|s|!path.starts_with(s)){continue;}if path.exists()&&Instant::now()<deadline{progress(title);add(home,scope.as_deref(),&mut found,action(title,path,vec![],impact),deadline);}}
    // Browser/app caches are exact subdirectories, never complete profiles or databases.
    let mut remaining=3000;let mut errors=vec![];let mut leads=vec![];
    for base in [home.join("Library/Caches"),home.join(".cache"),home.join("Library/Application Support"),home.join("Library/Containers")]{
        let base=match &scope{Some(s) if s.starts_with(&base)=>s.clone(),Some(s) if !base.starts_with(s)=>continue,_=>base};
        if !base.is_dir(){continue;}
        walk(home,&base,6,deadline,&mut remaining,&mut errors,|path|{
            if scope.as_ref().is_some_and(|s|!path.starts_with(s)&&!s.starts_with(path)){return false;}
            if path!=base&&APP_CACHES.iter().any(|name|path.file_name().is_some_and(|n|n==*name)){leads.push(path.to_path_buf());return false;}
            // Dedicated cache roots: inspect their actual children, not a fixed vendor list.
            if path.parent()==Some(base.as_path())&&(base==home.join("Library/Caches")||base==home.join(".cache")){leads.push(path.to_path_buf());return false;}
            !PROJECT_MARKERS.iter().any(|marker|path.join(marker).is_file())
        });
    }
    let mut pending=leads.into_iter().map(|path|{let title=format!("App/tool cache · {}",path.strip_prefix(home).unwrap_or(&path).display());action(&title,path,vec![],"Quit the owning app and stop related jobs first. Review the exact cache; downloaded dependencies may need reinstalling. Empty Trash to reclaim space.")}).collect::<Vec<_>>();
    // Size-ranked directory discovery survives protected siblings. Use known project
    // evidence to find generated artifacts, without traversing dependencies/worktrees.
    if options.projects(){
        remaining+=7000;
        let mut roots=vec![];
        if let Some(scope)=&scope{roots.push(scope.clone());}else{for raw in &options.roots{match session::tool_path(home,raw){Ok(path)=>roots.push(path),Err(reason)=>errors.push(format!("Configured root {raw}: {reason}"))}}for relative in ["code","Code","Developer","Projects","projects","src"]{let path=home.join(relative);if path.is_dir(){roots.push(path);}}roots.push(home.to_path_buf());}
        let mut seen=HashSet::new();let mut artifacts=vec![];
        for root in roots{walk(home,&root,8,deadline,&mut remaining,&mut errors,|path|{
            if !seen.insert(path.to_path_buf()){return false;}
            if path.parent()==Some(home)&&["Library",".cache",".npm",".cargo",".bun",".nvm",".fnm",".local",".rustup"].iter().any(|name|path.file_name().is_some_and(|n|n==*name)){return false;}
            if PROJECT_MARKERS.iter().any(|marker|path.join(marker).is_file()){for name in ARTIFACTS{let artifact=path.join(name);if artifact.is_dir(){artifacts.push(artifact);}}}
            true
        });}
        let mut project_pending=vec![];
        for path in artifacts{let title=format!("Project artifact · {}",path.strip_prefix(home).unwrap_or(&path).display());project_pending.push(action(&title,path,vec![],"Generated project data. Stop related builds first; rebuild costs apply. Tracked files are preserved. Trash moves need emptying to reclaim space."));}
        project_pending.append(&mut pending);pending=project_pending;
    }
    for item in pending{progress(&item.title);add(home,scope.as_deref(),&mut found,item,deadline);}
    // Reuse learned portable leads; native policy still decides removability.
    for rule in crate::discovery_rules::list(home)?.into_iter().filter(|rule|scope.is_none()&&rule.profiles.iter().any(|p|options.profiles.contains(p))){
        for path in crate::discovery_rules::matching(home,&rule,deadline){progress(&format!("Learned lead: {}",rule.title));add(home,scope.as_deref(),&mut found,action(&rule.title,path,vec![],"Learned discovery lead. Native cache/generated-data validation still applies; review its owning app and rebuild costs."),deadline);}
    }
    if let Some(scope)=scope.as_deref(){if scope.is_dir()&&Instant::now()<deadline{add(home,Some(scope),&mut found,action("Requested location",scope.into(),vec![],"Review this exact generated/cache location. Trash must be emptied to reclaim its space."),deadline);}}
    found.errors.extend(errors.into_iter().take(80));
    found.coverage.push(format!("Profiles: {}. Actual app/cache directories (depth ≤6); {}. Learned portable leads are re-inspected with native validation. Shared detector budget: 10000 directories, 110 seconds; symlinks, cloud/credential storage and implicit volume crossings skipped. All verified candidates are retained; presentation and model review are paginated/batched.",options.profiles.join(", "),if options.projects(){"configured owning-tool caches and home/configured-root projects (depth ≤8)"}else{"project discovery disabled by workflow selection"}));
    if Instant::now()>deadline{found.errors.push("Discovery deadline reached; remaining locations were not measured.".into());}
    if found.manual.len()>160{found.manual.truncate(160);found.errors.push("Additional manual-only locations omitted from this bounded review.".into());}
    found.candidates.sort_by(|a,b|b.estimated_bytes.cmp(&a.estimated_bytes));
    found.snapshot_hash=format!("{:x}",Sha256::digest(serde_json::to_vec(&found.candidates).map_err(|e|e.to_string())?));
    Ok(found)
}
pub fn assistance(discovery:&Discovery,policy:&Policy)->Assistance{
    let useful_locations=discovery.candidates.iter().filter(|c|c.estimated_bytes>=policy.useful_location_bytes).count();
    let bytes=discovery.candidates.iter().map(|c|c.estimated_bytes).fold(0u64,u64::saturating_add);
    let below_targets=useful_locations<policy.minimum_locations||bytes<policy.minimum_bytes;
    Assistance{triggered:true,reason:format!("Predefined scan found {useful_locations} useful locations and {bytes} measured candidate bytes (targets {} locations / {} bytes, {}). Agent discovery will inspect coverage gaps and recent-space leads and contribute additional native-verified candidates before review.",policy.minimum_locations,policy.minimum_bytes,if below_targets{"below targets"}else{"targets met; discovery is not complete"}),useful_locations,measured_candidate_bytes:bytes,policy:policy.clone(),tool_calls:0,learned_rules:0,status:"pending".into()}
}
#[cfg(test)]mod tests{
    use super::*;
    fn fixture()->PathBuf{static NEXT:std::sync::atomic::AtomicUsize=std::sync::atomic::AtomicUsize::new(0);let path=fs::canonicalize(std::env::temp_dir()).unwrap().join(format!("br-discovery-{}-{}-{}",std::process::id(),std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).unwrap().as_nanos(),NEXT.fetch_add(1,std::sync::atomic::Ordering::Relaxed)));fs::create_dir_all(&path).unwrap();path}
    #[test]fn agent_contributes_even_after_native_size_and_location_targets_are_met(){let policy=Policy::default();let mut discovery=Discovery::default();assert!(assistance(&discovery,&policy).triggered);for i in 0..4{let mut item=action("Fixture",PathBuf::from(format!("/fixture/{i}")),vec![],"Fixture");item.estimated_bytes=1024*1024*1024;discovery.candidates.push(item);}let assistance=assistance(&discovery,&policy);assert!(assistance.triggered);assert!(assistance.reason.contains("targets met"));assert_eq!(assistance.status,"pending");discovery.candidates.truncate(1);for i in 1..10{let mut item=action("Tiny",PathBuf::from(format!("/fixture/tiny{i}")),vec![],"Fixture");item.estimated_bytes=1024;discovery.candidates.push(item);}assert_eq!(super::assistance(&discovery,&policy).useful_locations,1);}
    #[test]fn developer_discovers_nested_cargo_builds_in_manual_and_daily_flows(){
        let h=fixture();let project=h.join("code/breathing-room/src-tauri");let target=project.join("target");fs::create_dir_all(target.join("debug")).unwrap();fs::write(project.join("Cargo.toml"),b"[package]\nname = \"fixture\"\nversion = \"0.1.0\"\n").unwrap();fs::write(target.join("debug/artifact"),b"fixture build").unwrap();
        for daily_care in [false,true]{let options=Options{profiles:vec!["developer".into()],daily_care,..Default::default()};let found=scan(&h,"",&options,|_|{}).unwrap();assert!(found.candidates.iter().any(|c|c.paths==vec![target.to_string_lossy().into_owned()]));}
        let found=scan(&h,"",&Options{profiles:vec!["everyday".into()],..Default::default()},|_|{}).unwrap();assert!(!found.candidates.iter().any(|c|c.paths==vec![target.to_string_lossy().into_owned()]));assert!(target.join("debug/artifact").exists());fs::remove_dir_all(h).unwrap();
    }
    #[test]fn native_candidate_inventory_has_no_48_item_retention_cap(){let h=fixture();let root=h.join("Library/Caches");fs::create_dir_all(&root).unwrap();let mut found=Discovery::default();for i in 0..55{let path=root.join(format!("fixture-{i}"));fs::create_dir(&path).unwrap();fs::write(path.join("blob"),b"fixture").unwrap();add(&h,None,&mut found,action("Fixture",path,vec![],"Fixture"),Instant::now()+Duration::from_secs(10));}assert_eq!(found.candidates.len(),55);fs::remove_dir_all(h).unwrap();}
    #[test]fn arbitrary_workspace_names_and_nested_monorepos_are_discovered_without_following_links(){
        let h=fixture();let workspace=h.join("Documents/Client Work/website/packages/service");fs::create_dir_all(workspace.join(".next")).unwrap();fs::write(workspace.join("package.json"),b"{}").unwrap();
        let hidden=h.join("Documents/Client Work/website/node_modules/dependency");fs::create_dir_all(&hidden).unwrap();fs::write(hidden.join("package.json"),b"{}").unwrap();
        let private=h.join("CloudStorage/project");fs::create_dir_all(&private).unwrap();fs::write(private.join("package.json"),b"{}").unwrap();
        let installed=h.join(".arbitrary-editor/extensions/package");fs::create_dir_all(&installed).unwrap();fs::write(installed.join("package.json"),b"{}").unwrap();
        std::os::unix::fs::symlink(&workspace,h.join("linked-project")).unwrap();
        let mut roots=vec![];let mut remaining=100;let mut errors=vec![];
        walk(&h,&h,8,Instant::now()+Duration::from_secs(2),&mut remaining,&mut errors,|p|{if PROJECT_MARKERS.iter().any(|m|p.join(m).is_file()){roots.push(p.to_path_buf());}true});
        assert_eq!(roots,vec![workspace]);assert!(errors.is_empty());fs::remove_dir_all(h).unwrap();
    }
    #[test]fn discovery_finds_unlisted_apps_and_honors_explicit_scope(){
        let h=fixture();let root=h.join("Library/Application Support");let cache=root.join("An Unlisted Editor/Profiles/custom/Code Cache");fs::create_dir_all(&cache).unwrap();fs::write(cache.join("blob"),b"fixture").unwrap();
        let options=Options{profiles:vec!["everyday".into()],roots:vec![],..Default::default()};let found=scan(&h,&cache.to_string_lossy(),&options,|_|{}).unwrap();
        assert_eq!(found.candidates.len(),1);assert_eq!(found.candidates[0].paths,vec![cache.to_string_lossy().into_owned()]);assert!(found.candidates[0].estimated_bytes>0);assert_eq!(found.candidates[0].mode,"permission");
        fs::remove_dir_all(h).unwrap();
    }
    #[test]fn traversal_reports_budget_exhaustion(){let h=fixture();for i in 0..8{fs::create_dir(h.join(i.to_string())).unwrap();}let mut errors=vec![];walk(&h,&h,8,Instant::now()+Duration::from_secs(2),&mut 2,&mut errors,|_|true);assert!(!errors.is_empty());fs::remove_dir_all(h).unwrap();}
    #[test]fn workflow_profiles_compose(){assert!(!Options{profiles:vec!["creator".into()],roots:vec![],..Default::default()}.projects());assert!(Options{profiles:vec!["creator".into(),"builder".into()],roots:vec![],..Default::default()}.projects());assert!(Options{profiles:vec!["developer".into()],roots:vec![],..Default::default()}.projects());}
    #[test]fn installed_extension_artifacts_cannot_be_proposed_even_with_project_markers(){let h=fixture();let project=h.join(".unlisted-editor/extensions/plugin");let dist=project.join("dist");fs::create_dir_all(&dist).unwrap();fs::write(project.join("package.json"),b"{}").unwrap();let candidate=action("Packaged runtime",dist,vec![],"Fixture");assert!(session::validate_action(&h,&candidate).unwrap_err().contains("packaged files are preserved"));fs::remove_dir_all(h).unwrap();}
    #[test]fn cache_names_inside_backups_and_browser_databases_do_not_authorize_cleanup(){let h=fixture();for relative in ["Library/Application Support/MobileSync/Backup/device/Cache","Library/Application Support/Browser/Default/IndexedDB/Cache"]{let path=h.join(relative);fs::create_dir_all(&path).unwrap();assert!(session::validate_action(&h,&action("Original data",path,vec![],"Fixture")).unwrap_err().contains("databases are preserved"));}fs::remove_dir_all(h).unwrap();}
    #[test]fn only_owned_tagged_ruff_artifacts_are_automatic(){let h=fs::canonicalize(std::env::temp_dir()).unwrap().join(format!("br-auto-{}",now()));let path=h.join("code/project/.ruff_cache");fs::create_dir_all(&path).unwrap();fs::write(h.join("code/project/pyproject.toml"),b"[project]").unwrap();assert!(automatic_path(&h,&path.to_string_lossy()).is_err());fs::write(path.join("CACHEDIR.TAG"),TAG).unwrap();assert!(automatic_path(&h,&path.to_string_lossy()).is_ok());std::os::unix::fs::symlink(h.join("code/project/pyproject.toml"),path.join("linked")).unwrap();assert!(automatic_path(&h,&path.to_string_lossy()).is_err());fs::remove_dir_all(h).unwrap();}
}
