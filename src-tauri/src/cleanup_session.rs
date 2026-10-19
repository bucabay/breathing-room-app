//! One native cleanup runner. Remote reasoning, SQLite journal, local approved actions.
use crate::{model::now, system};
use serde::{Deserialize, Serialize};
use serde_json::{json, Value};
use sha2::Digest;
use std::{collections::HashSet, fs, io::{BufReader, Read}, os::unix::{fs::{MetadataExt, PermissionsExt}, process::CommandExt}, path::{Path, PathBuf}, process::{Command, Stdio}, thread, time::{Duration, Instant}};
thread_local!{static CURRENT_RUN:std::cell::RefCell<Option<String>>=const{std::cell::RefCell::new(None)};}
pub(crate) fn run_scoped<T>(id:&str,work:impl FnOnce()->T)->T{
    struct Scope(Option<String>);impl Drop for Scope{fn drop(&mut self){CURRENT_RUN.with(|run|{run.replace(self.0.take());});}}
    let _scope=Scope(CURRENT_RUN.with(|run|run.replace(Some(id.into()))));work()
}

#[derive(Clone, Debug, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct Action {
    pub id: String, pub title: String, pub reason: String, pub impact: String,
    pub kind: String, pub paths: Vec<String>,
    #[serde(default)] pub command: Vec<String>,
    #[serde(default)] pub cwd: Option<String>,
    #[serde(default)] pub estimated_bytes: u64,
    #[serde(default = "permission_mode")] pub mode: String,
    #[serde(default)] pub native_rule: String,
}
fn permission_mode()->String{"permission".into()}
#[derive(Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct Outcome {
    pub id: String, pub ok: bool, pub detail: String,
    #[serde(default)] pub status: String,
    #[serde(default)] pub before_bytes: Option<u64>,
    #[serde(default)] pub after_bytes: Option<u64>,
    #[serde(default)] pub removed_bytes: Option<u64>,
    #[serde(default)] pub percent_cleaned: Option<f64>,
    #[serde(default)] pub pending_trash_bytes: u64,
}
impl Outcome{pub(crate) fn started(id:String)->Self{Self{id,ok:false,detail:"Action started; reconcile an interrupted outcome before retrying".into(),status:"running".into(),before_bytes:None,after_bytes:None,removed_bytes:None,percent_cleaned:None,pending_trash_bytes:0}}}
#[derive(Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct Run {
    pub id: String, pub status: String, pub model: String, pub request: String,
    pub overview: String, pub actions: Vec<Action>, pub approved_ids: Vec<String>,
    pub activity: Vec<String>, pub outcomes: Vec<Outcome>, pub recovered_bytes: u64,
    pub session_id: Option<String>, pub error: Option<String>, pub updated_at: u64,
    #[serde(default)] pub measurements: std::collections::BTreeMap<String,u64>,
    #[serde(default)] pub verified_actions: Vec<String>,
    #[serde(default)] pub scope: String,
    #[serde(default)] pub account_id: Option<String>,
    #[serde(default)] pub api_origin: Option<String>,
    #[serde(default)] pub schema_version: u32,
    #[serde(default)] pub discovery: Option<crate::cleanup_discovery::Discovery>,
    #[serde(default)] pub automatic_ids: Vec<String>,
    #[serde(default)] pub automatic_enabled: bool,
    #[serde(default)] pub results: Option<CleanupResults>,
    #[serde(default)] pub discovery_options: crate::cleanup_discovery::Options,
}
#[derive(Clone,Serialize,Deserialize)]
#[serde(rename_all="camelCase")]
pub struct CleanupResults{pub schema_version:u32,pub success:usize,pub failed:usize,pub skipped:usize,pub before_bytes:Option<u64>,pub removed_bytes:Option<u64>,pub percent_cleaned:Option<f64>,pub pending_trash_bytes:u64,pub available_space_change:Option<i64>,pub items:Vec<Outcome>}
fn random_id() -> Result<String,String> {
    let mut bytes = [0u8;16]; fs::File::open("/dev/urandom").and_then(|mut f|f.read_exact(&mut bytes)).map_err(|e|e.to_string())?;
    Ok(bytes.iter().map(|b|format!("{b:02x}")).collect())
}
fn valid_id(id:&str)->bool { id.len()==32 && id.bytes().all(|b|b.is_ascii_hexdigit()) }
fn folder(home:&Path)->Result<PathBuf,String>{
    let path=home.join("Library/Application Support/app.breathingroom.mac/agent-cleanup");
    fs::create_dir_all(&path).map_err(|e|e.to_string())?;
    if fs::canonicalize(&path).map_err(|e|e.to_string())? != path {return Err("Agent storage contains a symlink".into());}
    fs::set_permissions(&path,fs::Permissions::from_mode(0o700)).map_err(|e|e.to_string())?;
    Ok(path)
}
fn load(home:&Path,id:&str)->Result<Run,String>{
    if !valid_id(id){return Err("Invalid agent session".into());}
    if let Some(value)=crate::runtime_store::load_run(home,id)?{return serde_json::from_value(value).map_err(|_|"Invalid saved agent state".into());}
    let path=folder(home)?.join(format!("{id}.json"));
    let meta=fs::symlink_metadata(&path).map_err(|_|"This cleanup session is no longer available")?;
    if meta.file_type().is_symlink()||meta.len()>2_000_000{return Err("Invalid agent state".into());}
    let mut run:Run=serde_json::from_slice(&fs::read(path).map_err(|e|e.to_string())?).map_err(|_|"Invalid agent state")?;
    if ["inspecting","executing"].contains(&run.status.as_str()){run.status="failed".into();run.error=Some("Previous agent run was interrupted. Start a new inspection.".into());}
    save(home,&run)?;Ok(run)
}
fn save(home:&Path,run:&Run)->Result<(),String>{
    crate::runtime_store::save_run(home,&run.id,&serde_json::to_value(run).map_err(|e|e.to_string())?)
}
use std::os::unix::fs::OpenOptionsExt;
use std::os::fd::AsRawFd;
fn update(home:&Path,id:&str,change:impl FnOnce(&mut Run)->Result<(),String>)->Result<Run,String>{
    update_claimed(home,id,false,change)
}
fn update_claimed(home:&Path,id:&str,claim:bool,change:impl FnOnce(&mut Run)->Result<(),String>)->Result<Run,String>{
    if !valid_id(id){return Err("Invalid agent session".into());}
    let lock=fs::OpenOptions::new().read(true).write(true).create(true).truncate(false).mode(0o600).open(folder(home)?.join(format!("{id}.lock"))).map_err(|e|e.to_string())?;
    if unsafe{libc::flock(lock.as_raw_fd(),libc::LOCK_EX)}!=0{return Err("Agent state is busy".into());}
    let mut run=load(home,id)?;change(&mut run)?;run.updated_at=now();if claim{crate::runtime_store::claim_run(home,id,&serde_json::to_value(&run).map_err(|e|e.to_string())?)?;}else{save(home,&run)?;}Ok(run)
}
pub fn state(id:String)->Result<Run,String>{
    let home=system::user_home()?;let mut run=load(&home,&id)?;
    if ["inspecting","executing"].contains(&run.status.as_str())&&!crate::runtime_store::owner_alive(&home,&id){return update(&home,&id,|r|{r.status="failed".into();r.error=Some("The app stopped during this run. Resume inspection, or review interrupted action outcomes.".into());Ok(())});}
    // Restored discovery runs must not display legacy unverified model prose.
    if run.discovery.is_some()&&["review","executing","done","cancelled","failed"].contains(&run.status.as_str()){run.overview=verified_overview(&run,&run.actions);}
    Ok(run)
}
fn verified_overview(run:&Run,actions:&[Action])->String{
    let Some(discovery)=&run.discovery else{return run.overview.clone();};
    let bytes=actions.iter().map(|a|a.estimated_bytes).fold(0u64,u64::saturating_add);
    let mut text=format!("Native-verified review: {} selected locations from {} measured cleanup candidates ({} allocated bytes at the selected source locations). Sizes are not guaranteed reclaimable space; owning-tool prune may remove only part, and Trash must be emptied separately. Review each action's method and impact before approving.",actions.len(),discovery.candidates.len(),bytes);
    if let Some(inventory)=&discovery.inventory{text.push_str(&format!(" Inventory inspected {} files and {} directories; {}.",inventory.files_inspected,inventory.directories_inspected,if inventory.partial{"coverage is partial"}else{"requested metadata traversal completed"}));}
    if !discovery.review_locations.is_empty(){text.push_str(&format!(" {} personal/editor storage locations are listed separately for explicit owning-app review, not included in cleanup or space-saving totals.",discovery.review_locations.len()));}
    if discovery.agent.as_ref().is_some_and(|a|a.status=="failed"){text.push_str(" Agent investigation was unavailable; retained native findings remain available for review.");}
    if !discovery.errors.is_empty(){text.push_str(" Discovery reported coverage or investigation gaps; see inspection details.");}
    text
}
pub fn latest()->Result<Option<Run>,String>{crate::runtime_store::latest(&system::user_home()?)?.map(state).transpose()}
pub fn cancel(id:String)->Result<(),String>{
    let home=system::user_home()?;
    update(&home,&id,|run|{if ["inspecting","executing"].contains(&run.status.as_str()){run.status="cancelled".into();}Ok(())})?;Ok(())
}
fn append(home:&Path,id:&str,message:String){
    let _=update(home,id,|run|{run.activity.push(message);if run.activity.len()>80{run.activity.remove(0);}Ok(())});
}
pub(crate) fn activity(home:&Path,id:&str,message:String){append(home,id,message)}
pub(crate) fn remote_session(home:&Path,id:&str,session:String,model:String)->Result<(),String>{update(home,id,|r|{r.session_id=Some(session);r.model=model;Ok(())})?;Ok(())}

pub fn runtime_path(home:&Path)->String{
    let mut paths=vec![home.join(".opencode/bin"),home.join(".local/bin"),home.join(".cargo/bin"),home.join(".bun/bin")];
    // Version managers install outside Finder's PATH. Discover them in native code.
    for root in [home.join(".nvm/versions/node"),home.join(".fnm/node-versions")] {
        if let Ok(entries)=fs::read_dir(root){let mut versions:Vec<_>=entries.flatten().map(|e|e.path()).collect();versions.sort();versions.reverse();
            for version in versions { paths.push(version.join("bin"));paths.push(version.join("installation/bin")); }
        }
    }
    paths.extend([PathBuf::from("/opt/homebrew/bin"),PathBuf::from("/usr/local/bin"),PathBuf::from("/usr/bin"),PathBuf::from("/bin"),PathBuf::from("/usr/sbin"),PathBuf::from("/sbin")]);
    paths.iter().map(|p|p.to_string_lossy()).collect::<Vec<_>>().join(":")
}
fn binary(home:&Path,name:&str)->Option<PathBuf>{
    runtime_path(home).split(':').map(|p|Path::new(p).join(name)).find(|p|p.is_file() && fs::metadata(p).is_ok_and(|m|m.permissions().mode()&0o111!=0))
}
pub(crate) fn tool_available(home:&Path,name:&str)->bool{binary(home,name).is_some()}
pub(crate) fn inspection_cancelled(home:&Path)->bool{CURRENT_RUN.with(|id|id.borrow().as_ref().is_some_and(|id|load(home,id).is_ok_and(|r|r.status=="cancelled")))}
fn output(home:&Path,argv:&[String],cwd:Option<&Path>,seconds:u64)->Result<String,String>{
    let (text,error,status)=capture_output(home,argv,cwd,seconds)?;
    if status.success(){return Ok(text);}
    let reason=if error.contains("Permission denied")||error.contains("EACCES")||error.contains("Operation not permitted"){"permission denied"}else if error.contains("lock")||error.contains("busy"){"resource is busy"}else{"command failed"};
    Err(format!("{}: {reason} (exit {})",argv[0],status.code().unwrap_or(-1)))
}
fn capture_output(home:&Path,argv:&[String],cwd:Option<&Path>,seconds:u64)->Result<(String,String,std::process::ExitStatus),String>{
    let program=argv.first().ok_or("Empty command")?;
    let name=Path::new(program).file_name().and_then(|p|p.to_str()).ok_or("Invalid program")?;
    let executable=binary(home,name).ok_or_else(||format!("{name} is not installed on this Mac"))?;
    if program.starts_with('/')&&Path::new(program)!=executable{return Err("Use the installed owning-app executable".into());}
    let mut command=Command::new(executable);command.args(&argv[1..]).env("PATH",runtime_path(home)).current_dir(cwd.unwrap_or(home));
    let agent_child=CURRENT_RUN.with(|run|run.borrow().clone()).or_else(||std::env::var("BREATHING_ROOM_AGENT_RUN").ok());
    command.process_group(0);
    command.stdin(Stdio::null()).stdout(Stdio::piped()).stderr(Stdio::piped());
    let mut child=command.spawn().map_err(|_|format!("Could not start {program}"))?;
    let stdout=child.stdout.take().unwrap();let stderr=child.stderr.take().unwrap();
    let (sender,receiver)=std::sync::mpsc::channel();let errors=sender.clone();
    thread::spawn(move||{let mut text=String::new();let _=BufReader::new(stdout).take(1_000_000).read_to_string(&mut text);let _=sender.send((false,text));});
    thread::spawn(move||{let mut text=String::new();let _=BufReader::new(stderr).take(100_000).read_to_string(&mut text);let _=errors.send((true,text));});
    let deadline=Instant::now()+Duration::from_secs(seconds);
    loop {match child.try_wait(){
        Ok(Some(status))=>{
            // A background helper can inherit the pipes after its parent exits.
            // Keep draining under the SAME deadline; joining readers can hang forever.
            let mut text=String::new();let mut error=String::new();
            for _ in 0..2{match receiver.recv_timeout(deadline.saturating_duration_since(Instant::now())){
                Ok((stderr,output))=>{if stderr{error=output;}else{text=output;}},
                Err(_)=>{unsafe{libc::kill(-(child.id() as i32),libc::SIGKILL);}return Err(format!("{program} output exceeded its time limit"));}
            }}return Ok((text,error,status));
        },
        Ok(None) if Instant::now()<deadline&&!agent_child.as_ref().is_some_and(|id|load(home,id).is_ok_and(|r|r.status=="cancelled"))=>thread::sleep(Duration::from_millis(50)),
        _=>{unsafe{libc::kill(-(child.id() as i32),libc::SIGKILL);}let _=child.kill();let _=child.wait();return Err(format!("{program} stopped or exceeded its time limit"));}
    }}
}
pub fn connection()->Value {crate::remote_agent::connection()}

fn checked_path(home:&Path,raw:&str)->Result<PathBuf,String>{
    let path=if let Some(rest)=raw.strip_prefix("~/"){home.join(rest)}else{PathBuf::from(raw)};
    if !path.is_absolute()||path.components().any(|c|matches!(c,std::path::Component::ParentDir)){return Err("Use an exact absolute location".into());}
    let canonical=fs::canonicalize(&path).map_err(|_|"This location is unavailable")?;
    if canonical!=path{return Err("This location contains a symlink".into());}
    if path.components().any(|c|[".ssh",".gnupg",".aws","Keychains","CloudStorage","Mobile Documents","Mail","Messages",".Trash"].contains(&c.as_os_str().to_string_lossy().as_ref())) {return Err("Personal, synced or credential storage is preserved".into());}
    if path.components().any(|c|c.as_os_str().to_string_lossy().starts_with(".env")){return Err("Credential/environment files are preserved".into());}
    if path.components().any(|c|{let name=c.as_os_str().to_string_lossy();["MobileSync","Local Storage","Session Storage","IndexedDB","Service Worker","Sync Data"].contains(&name.as_ref())||["backup","backups"].contains(&name.to_lowercase().as_str())||name.ends_with(".photoslibrary")||name.ends_with(".musiclibrary")}){return Err("Backups, media libraries and browser databases are preserved".into());}
    let supported=path.starts_with(home)||["/Library/Caches","/Library/Developer","/Applications","/opt/homebrew","/usr/local","/Volumes"].iter().any(|p|path.starts_with(p));
    if !supported{return Err("Outside supported inspection locations".into());}Ok(path)
}
fn trash_path(home:&Path,raw:&str)->Result<PathBuf,String>{
    let path=checked_path(home,raw)?;
    if crate::review_storage::protected_storage(home,&path){return Err("App projects, media collections and original recordings require owning-app review".into());}
    if path.strip_prefix(home).is_ok_and(|relative|relative.components().any(|component|{let name=component.as_os_str().to_string_lossy();name=="extensions"||name.ends_with(".app")})){return Err("Installed applications and extension trees need owning-app controls; packaged files are preserved".into());}
    if path==home||!path.starts_with(home)||fs::metadata(&path).map_err(|e|e.to_string())?.uid()!=unsafe{libc::getuid()}{return Err("Only exact owned cache/generated locations can be moved".into());}
    let relative=path.strip_prefix(home).unwrap().to_string_lossy();let name=path.file_name().unwrap_or_default().to_string_lossy().to_lowercase();
    let cache=relative.starts_with("Library/Caches/")||relative.starts_with(".cache/")||relative.contains("/Library/Caches/");
    let tool_generated=path.starts_with(home.join(".npm/_npx"))||path.starts_with(home.join("Library/Developer/Xcode/DerivedData"));
    let project_generated=["node_modules","target","dist",".next",".pytest_cache",".mypy_cache",".ruff_cache"].contains(&name.as_str())&&path.ancestors().skip(1).take_while(|parent|parent.starts_with(home)&&*parent!=home).any(|parent|["package.json","Cargo.toml","pyproject.toml","go.mod"].iter().any(|marker|parent.join(marker).is_file()));
    let app_cache=["cache","caches","code cache","gpucache","cacheddata","media cache","media cache files"].contains(&name.as_str())&&(relative.starts_with("Library/Application Support/")||relative.starts_with("Library/Containers/"));
    let generated=project_generated||app_cache;
    let installer=relative.starts_with("Downloads/")&&["dmg","pkg","iso"].iter().any(|ext|path.extension().is_some_and(|e|e==*ext));
    if !cache&&!generated&&!installer&&!tool_generated{return Err("This location needs its owning-app controls; originals are preserved".into());}
    if path.join(".git").exists()||((path.join("package.json").exists()||path.join("Cargo.toml").exists())&&!(project_generated&&name==".next")){return Err("A whole project cannot be moved by cache cleanup".into());}
    if let Some(repo)=path.ancestors().skip(1).find(|parent|parent.starts_with(home)&&parent.join(".git").exists()){
        let relative=path.strip_prefix(repo).map_err(|_|"Project scope changed")?;
        if !output(home,&["git".into(),"-C".into(),repo.to_string_lossy().into_owned(),"ls-files".into(),"--".into(),relative.to_string_lossy().into_owned()],None,5)?.trim().is_empty(){return Err("Tracked project files are preserved".into());}
    }
    Ok(path)
}
pub fn validate_action(home:&Path,action:&Action)->Result<(),String>{
    if action.id.is_empty()||action.id.len()>80||action.paths.is_empty()||action.paths.len()>8{return Err("Cleanup actions need exact locations and IDs".into());}
    for path in &action.paths {checked_path(home,path)?;}
    if action.paths.iter().any(|path|crate::review_storage::protected_storage(home,Path::new(path))){return Err("App projects, media collections and original recordings require owning-app review; they cannot be removed by cache cleanup".into());}
    match action.kind.as_str(){
        "trash"=>{for path in &action.paths{trash_path(home,path)?;}Ok(())},
        "command"=>{
            if action.command.len()<2||action.command.len()>24{return Err("Provide a precise owning-app command".into());}
            let args=action.command.iter().map(String::as_str).collect::<Vec<_>>();let name=Path::new(args[0]).file_name().unwrap_or_default().to_string_lossy();let tail=&args[1..];
            let installed=binary(home,&name).ok_or_else(||format!("{name} is not installed; use another verified method"))?;
            if (args[0].starts_with('/')&&Path::new(args[0])!=installed)||(!args[0].starts_with('/')&&args[0].contains('/')){return Err("Use the installed owning-app command".into());}
            let allowed=match name.as_ref(){
                "npm"=>tail.starts_with(&["cache","clean"]),"uv"=>tail.starts_with(&["cache","prune"])||tail.starts_with(&["cache","clean"]),
                "python3"=>tail.starts_with(&["-m","pip","cache","purge"]),"pip"|"pip3"=>tail.starts_with(&["cache","purge"]),
                "pnpm"=>tail.starts_with(&["store","prune"]),"yarn"=>tail.starts_with(&["cache","clean"]),"bun"=>tail.starts_with(&["pm","cache","rm"]),
                "go"=>tail.first()==Some(&"clean")&&tail.iter().any(|arg|["-cache","-modcache","-testcache","-fuzzcache"].contains(arg)),
                "cargo"=>tail.first()==Some(&"clean"),"brew"=>tail.first()==Some(&"cleanup"),
                "docker"=>tail.starts_with(&["builder","prune"])||tail.starts_with(&["buildx","prune"]),
                "xcrun"=>tail.starts_with(&["simctl","runtime","delete"])&&tail.len()==4&&tail[3].len()==36&&tail[3].bytes().all(|b|b.is_ascii_hexdigit()||b==b'-'),
                _=>false,
            };
            if !allowed||args.iter().any(|s|s.contains('\n')||s.contains('\0')){return Err("Use a supported owning-app cleanup command or an exact Trash action".into());}
            if let Some(cwd)=&action.cwd{checked_path(home,cwd)?;}
            for arg in tail{let value=arg.split_once('=').map(|(_,v)|v).unwrap_or(arg);if value.starts_with('/')||value.starts_with("~/"){checked_path(home,value)?;}}
            if name=="cargo"{let cwd=action.cwd.as_ref().ok_or("Cargo cleanup needs a verified project directory")?;if !checked_path(home,cwd)?.join("Cargo.toml").is_file(){return Err("Cargo project marker is missing".into());}}
            validate_command_scope(home,action,&name,tail)?;
            Ok(())
        },_=>Err("Unknown cleanup action".into())
    }
}
fn exact_flags(tail:&[&str],prefix:&[&str],flags:&[&str],location_flag:Option<&str>)->bool{
    if !tail.starts_with(prefix){return false;}let mut index=prefix.len();
    while index<tail.len(){let arg=tail[index];if flags.contains(&arg){index+=1;continue;}
        if let Some(flag)=location_flag{if arg==flag&&index+1<tail.len(){index+=2;continue;}if arg.starts_with(&format!("{flag}=")){index+=1;continue;}}
        return false;
    }true
}
fn validate_command_scope(home:&Path,action:&Action,name:&str,tail:&[&str])->Result<(),String>{
    let cwd=action.cwd.as_deref().map(|path|checked_path(home,path)).transpose()?;
    let query=|argv:Vec<String>|output(home,&argv,cwd.as_deref(),8);
    let mut roots=vec![];let mut location_flag=None;
    let allowed=match name{
        "npm"=>{roots.push(query(vec!["npm".into(),"config".into(),"get".into(),"cache".into()])?);location_flag=Some("--cache");exact_flags(tail,&["cache","clean"],&["--force"],location_flag)},
        "uv"=>{roots.push(query(vec!["uv".into(),"cache".into(),"dir".into()])?);location_flag=Some("--cache-dir");(tail.starts_with(&["cache","prune"])||tail.starts_with(&["cache","clean"]))&&exact_flags(tail,&tail[..2],&[],location_flag)},
        "python3"=>{roots.push(query(vec!["python3".into(),"-m".into(),"pip".into(),"cache".into(),"dir".into()])?);tail==["-m","pip","cache","purge"]},
        "pip"|"pip3"=>{roots.push(query(vec![name.into(),"cache".into(),"dir".into()])?);tail==["cache","purge"]},
        "pnpm"=>{roots.push(query(vec!["pnpm".into(),"store".into(),"path".into()])?);tail==["store","prune"]},
        "yarn"=>{roots.push(query(vec!["yarn".into(),"cache".into(),"dir".into()])?);tail==["cache","clean"]},
        "bun"=>{roots.push(query(vec!["bun".into(),"pm".into(),"cache".into()])?);tail==["pm","cache","rm"]},
        "go"=>{
            if tail.len()<2||tail[0]!="clean"||tail[1..].iter().any(|arg|!["-cache","-modcache","-testcache","-fuzzcache"].contains(arg)){return Err("Only explicitly selected Go cache targets are supported".into());}
            if tail.contains(&"-modcache"){roots.push(query(vec!["go".into(),"env".into(),"GOMODCACHE".into()])?);}
            if tail.iter().any(|arg|["-cache","-testcache","-fuzzcache"].contains(arg)){roots.push(query(vec!["go".into(),"env".into(),"GOCACHE".into()])?);}true
        },
        "cargo"=>{
            if tail!=["clean"]{return Err("Use cargo clean in the exact verified project, without alternate manifests".into());}
            let metadata:Value=serde_json::from_str(&query(vec!["cargo".into(),"metadata".into(),"--no-deps".into(),"--offline".into(),"--locked".into(),"--format-version".into(),"1".into()])?).map_err(|_|"Could not verify Cargo's actual target directory")?;
            let root=metadata["target_directory"].as_str().ok_or("Cargo target directory missing")?;trash_path(home,root)?;roots.push(root.into());true
        },
        _=>return Err("This command needs owning-app review. Use an exact verified generated/cache Trash action instead.".into()),
    };
    if !allowed{return Err("Cleanup command contains unsupported arguments".into());}
    let roots=roots.iter().map(|root|checked_path(home,root.trim())).collect::<Result<Vec<_>,_>>()?;
    for root in &roots{if !root.starts_with(home)||fs::metadata(root).map_err(|e|e.to_string())?.uid()!=unsafe{libc::getuid()}{return Err("Owning-tool cache is not an owned user location".into());}}
    let actual=if name=="npm"&&action.paths.iter().all(|path|Path::new(path)==roots[0].join("_cacache")){vec![roots[0].join("_cacache")]}else{roots.clone()};
    if !same_scope(&action.paths,&actual){return Err("Selected paths do not match the owning tool's actual cleanup targets".into());}
    if let Some(flag)=location_flag{
        for (index,arg) in tail.iter().enumerate(){let value=if *arg==flag{tail.get(index+1).copied()}else{arg.strip_prefix(&format!("{flag}="))};if let Some(value)=value{if checked_path(home,value)?!=roots[0]{return Err("Cache override does not match the verified owning-tool location".into());}}}
    }Ok(())
}
fn same_scope(paths:&[String],roots:&[PathBuf])->bool{paths.len()==roots.len()&&paths.iter().all(|path|roots.iter().any(|root|root==Path::new(path)))&&roots.iter().all(|root|paths.iter().any(|path|root==Path::new(path)))}
pub(crate) fn action_key(action:&Action)->String{json!({"kind":action.kind,"paths":action.paths,"command":action.command,"cwd":action.cwd}).to_string()}
pub(crate) fn record_measurement(home:&Path,id:&str,path:String,bytes:u64)->Result<(),String>{update(home,id,|run|{run.measurements.insert(path,bytes);Ok(())})?;Ok(())}
pub(crate) fn record_verification(home:&Path,id:&str,action:&Action)->Result<(),String>{let key=action_key(action);update(home,id,|run|{if !run.verified_actions.contains(&key){run.verified_actions.push(key);}Ok(())})?;Ok(())}

#[cfg(any())]
fn config(home:&Path,run:&Run,phase:&str)->Result<Value,String>{
    let metadata=output(home,&["opencode".into(),"debug".into(),"config".into()],Some(&folder(home)?),20).ok().and_then(|s|serde_json::from_str::<Value>(&s).ok()).unwrap_or(json!({}));
    let mut mcp=serde_json::Map::new();
    if let Some(old)=metadata["mcp"].as_object(){for name in old.keys(){mcp.insert(name.clone(),json!({"enabled":false}));}}
    mcp.insert("cleanup".into(),json!({"type":"local","command":[std::env::current_exe().map_err(|e|e.to_string())?,"cleanup-agent-tools"],"enabled":true,"timeout":90000,"environment":{"BREATHING_ROOM_AGENT_RUN":run.id,"BREATHING_ROOM_AGENT_PHASE":phase}}));
    let prompt=if phase=="inspect"{
        "You are the user's disk cleanup agent. Inspect the actual Mac with cleanup tools, like a thorough CLI coding agent asked to free disk space. Honor explicit location scope; a general request to free disk space requires BROAD discovery, not just the first few package caches. Start with inspect_disk, then inspect_tree to rank the actual sizes of user caches, hidden tool caches, Library/Developer, Application Support cache subdirectories, and generated artifacts in workspaces (inspect_tree depth 5-6). Use the returned starting locations as leads, not a fixed allowlist. Drill into the largest results; follow listing pagination. Do not stop because a few small caches were checked or an action was rejected. Cover the applicable categories before returning a concise plan; discovery breadth is independent of presentation length. Preserve originals/settings/credentials/backups, browser profiles/site data and source worktrees. Runtime dependencies or browser binaries may be in use: explain close-app/reinstall requirements and don't label all cache-named data disposable. Prefer owning-app cache commands and generated artifacts. Exact npm _npx cache and Xcode DerivedData Trash moves are supported; preserve Xcode UserData/Archives/device data. If verification rejects one method, check an applicable supported method or report the location as manual; continue discovery. Measure each final candidate with inspect_location and verify COMPLETE actions with verify_action. Do not mutate anything before approval. Never add parent and child sizes together or include overlapping actions. Sizes are measured locations, not guaranteed reclaimed bytes; Trash reclaims space only when emptied. Return the most useful non-overlapping actions, up to 24, with larger manual opportunities and coverage gaps in overview. For a focused request inspect only that scope. Return ONLY JSON: {overview:string,actions:[{id:string,title:string,reason:string,impact:string,kind:'command'|'trash',paths:string[],command:string[],cwd:string|null,estimatedBytes:number}]}. Each command is an exact argv without shell syntax; trash actions have empty command arrays. No unsupported action may be included. Never claim you cleaned anything."
    }else{
        "The user approved the supplied exact cleanup actions. Continue this same session and execute every approved action using cleanup execute_approved_action, checking current locations as needed. Prefer the owning-app tools in the approved plan. You cannot run unapproved commands or delete additional locations. One failed action must not stop other approved actions. Report what actually completed and any follow-up, concisely. Tools record authoritative outcomes."
    };
    let prompt=if phase=="inspect"{format!("{prompt}\nFor sudden space loss or space returning after cleanup, use inspect_recent_space with the user's time window. In broad cleanup also check inspect_disk's recentSpaceTemporaryRoot with this tool: builds/browser/release workspaces may live outside home. Drill into the largest recent directory groups. Creation and modification times plus current allocated sizes are evidence, not measured growth or process attribution. Preserve temporary source/worktrees and active builds; report partial coverage and unsupported cleanup as manual. Recent files are never automatically disposable.")}else{prompt.to_owned()};
    Ok(json!({"share":"disabled","snapshot":false,"logLevel":"ERROR","mcp":mcp,"permission":{"*":"deny","cleanup_*":"allow"},"agent":{"title":{"disable":true},"summary":{"disable":true},"breathingroom":{"mode":"primary","description":"Inspect disk and execute the user-approved cleanup","steps":64,"prompt":prompt,"permission":{"*":"deny","cleanup_*":"allow"}}}}))
}
#[cfg(any())]
fn legacy_agent_turn(home:&Path,id:&str,phase:&str,prompt:&str)->Result<String,String>{
    let run=load(home,id)?;let executable=binary(home,"opencode").ok_or("OpenCode is not installed. Install it, then try again.")?;
    let mut command=Command::new(executable);command.args(["run","--format","json","--agent","breathingroom","--model",&run.model,"--title","Breathing Room cleanup"]);
    if let Some(session)=&run.session_id{command.args(["--session",session]);}
    command.arg(prompt).current_dir(folder(home)?).env("PATH",runtime_path(home)).env_remove("OPENCODE_PERMISSION").env("OPENCODE_CONFIG_CONTENT",config(home,&run,phase)?.to_string()).env("OPENCODE_DISABLE_PROJECT_CONFIG","true").env("OPENCODE_DISABLE_CLAUDE_CODE","true").stdin(Stdio::null()).stdout(Stdio::piped()).stderr(Stdio::piped()).process_group(0);
    if run.model.starts_with("groq/"){if let Some(key)=groq_key(home){command.env("GROQ_API_KEY",key);}}
    let mut child=command.spawn().map_err(|_|"Could not start the OpenCode agent")?;
    let stdout=child.stdout.take().unwrap();let stderr=child.stderr.take().unwrap();
    let captured=std::sync::Arc::new(std::sync::Mutex::new((String::new(),None::<String>,String::new())));
    let captured_reader=captured.clone();let h=home.to_path_buf();let rid=id.to_owned();
    let inspection=phase=="inspect";
    let reader=thread::spawn(move||{
        for line in BufReader::new(stdout).lines().map_while(Result::ok){if line.len()>1_000_000{continue;}
            if let Ok(event)=serde_json::from_str::<Value>(&line){
                if let Some(session)=event["sessionID"].as_str().or(event["part"]["sessionID"].as_str()) {if load(&h,&rid).is_ok_and(|r|r.session_id.is_none()){let _=update(&h,&rid,|current|{if current.session_id.is_none(){current.session_id=Some(session.into());}Ok(())});}}
                if event["type"]=="text"{if let Some(text)=event["part"]["text"].as_str(){let mut c=captured_reader.lock().unwrap();let message=event["part"]["messageID"].as_str().unwrap_or("");if c.2!=message{c.0.clear();c.2=message.into();}if c.0.len()<1_000_000{c.0.push_str(text);}}}
                if inspection&&event["type"]=="tool_use"&&event["part"]["state"]["status"]=="completed"{if let Some(tool)=event["part"]["tool"].as_str(){append(&h,&rid,format!("Agent: {}",tool.replace("cleanup_","")));}}
                if event["type"]=="error"{captured_reader.lock().unwrap().1=Some(format!("Agent connection failed ({}). Check the selected model in OpenCode.",event["error"]["data"]["statusCode"].as_u64().map(|n|n.to_string()).unwrap_or_else(||"provider error".into())));}
            }
        }
    });
    let drain=thread::spawn(move||{let _=std::io::copy(&mut BufReader::new(stderr),&mut std::io::sink());});
    let deadline=Instant::now()+Duration::from_secs(600);
    let status=loop{match child.try_wait(){Ok(Some(status))=>break Ok(status),Ok(None) if Instant::now()<deadline&&load(home,id).is_ok_and(|r|r.status!="cancelled")=>thread::sleep(Duration::from_millis(100)),_=>{unsafe{libc::kill(-(child.id() as i32),libc::SIGKILL);}let _=child.wait();break Err("Agent stopped or exceeded its time limit".to_string());}}};
    let _=reader.join();let _=drain.join();let captured=captured.lock().unwrap();
    if let Some(error)=&captured.1{return Err(error.clone());}
    if !status?.success(){return Err("The OpenCode agent could not complete this step. Check its provider connection and retry.".into());}
    if captured.0.trim().is_empty(){return Err("The agent returned no response. Check your model connection and retry.".into());}Ok(captured.0.clone())
}
pub fn inspect(request:String,scope:String,_model:String)->Result<String,String>{inspect_with_options(request,scope,false)}
pub(crate) fn inventory_roots(home:&Path,scope:&str,options:&crate::cleanup_discovery::Options)->Result<Vec<PathBuf>,String>{
    if !scope.is_empty(){return Ok(vec![read_path(home,scope)?]);}
    let mut roots=crate::review_storage::known_locations(home,None);roots.extend(options.roots.iter().filter_map(|root|tool_path(home,root).ok()));roots.push(home.into());if Path::new("/Applications").is_dir(){roots.push(PathBuf::from("/Applications"));}Ok(roots)
}
pub(crate) fn read_path(home:&Path,raw:&str)->Result<PathBuf,String>{
    if let Ok(path)=tool_path(home,raw){return Ok(path);}
    let path=raw.strip_prefix("~/").map(|rest|home.join(rest)).unwrap_or_else(||PathBuf::from(raw));
    if !path.is_absolute()||path.components().any(|c|matches!(c,std::path::Component::ParentDir))||fs::canonicalize(&path).ok().as_ref()!=Some(&path)||crate::discovery_inventory::excluded(home,&path)||fs::metadata(&path).map(|m|m.uid()!=unsafe{libc::getuid()}).unwrap_or(true){return Err("Use an exact owned, non-protected inspection location".into());}Ok(path)
}
pub(crate) fn inspection_path(home:&Path,id:&str,raw:&str)->Result<PathBuf,String>{let path=read_path(home,raw)?;let run=load(home,id)?;if !run.scope.is_empty()&&!path.starts_with(read_path(home,&run.scope)?){return Err("Outside this inspection's requested scope".into());}Ok(path)}
pub(crate) fn claim_discovery_tool(home:&Path,id:&str)->Result<(),String>{update(home,id,|run|{
    if let Some(agent)=run.discovery.as_mut().and_then(|d|d.agent.as_mut()){if agent.triggered&&run.status=="inspecting"{if agent.tool_calls>=agent.policy.max_tool_calls{return Err("Agent discovery tool budget reached; finalize using retained findings".into());}agent.tool_calls+=1;agent.status="running".into();}}Ok(())
})?;Ok(())}
pub(crate) fn learned_rule(home:&Path,id:&str)->Result<(),String>{update(home,id,|run|{if let Some(agent)=run.discovery.as_mut().and_then(|d|d.agent.as_mut()){agent.learned_rules+=1;}Ok(())})?;Ok(())}
pub(crate) fn record_inventory(home:&Path,id:&str,summary:crate::discovery_inventory::Summary)->Result<(),String>{update(home,id,|run|{let discovery=run.discovery.as_mut().ok_or("Native discovery has not finished")?;for row in &summary.largest{if let Some(path)=row["path"].as_str(){note_source(discovery,path,"inventory");}}discovery.inventory=Some(summary);Ok(())})?;Ok(())}
fn note_source(discovery:&mut crate::cleanup_discovery::Discovery,path:&str,source:&str){let sources=discovery.sources.entry(path.into()).or_default();if !sources.iter().any(|old|old==source){sources.push(source.into());sources.sort();}discovery.observed_at.insert(path.into(),now());}
fn merge_discovery(run:&mut Run, incoming:crate::cleanup_discovery::Discovery)->Result<(),String>{
    if run.status!="inspecting"{return Ok(());}
    let target=run.discovery.as_mut().ok_or("Discovery missing")?;
    for action in incoming.candidates{
        for path in &action.paths{note_source(target,path,"known-locations");}
        if let Some(existing)=target.candidates.iter_mut().find(|old|old.id==action.id){*existing=action.clone();}
        else if !target.candidates.iter().any(|old|old.paths.iter().any(|a|action.paths.iter().any(|b|Path::new(a).starts_with(b)||Path::new(b).starts_with(a)))){target.candidates.push(action.clone());}
        else{continue;}
        for path in &action.paths{run.measurements.insert(path.clone(),action.estimated_bytes);}
        let key=action_key(&action);if !run.verified_actions.contains(&key){run.verified_actions.push(key);}
    }
    for item in incoming.review_locations{note_source(target,&item.path,"known-locations");crate::review_storage::retain(&mut target.review_locations,item);}
    for item in incoming.manual{if !target.manual.iter().any(|old|old.path==item.path){target.manual.push(item);}}
    target.coverage.extend(incoming.coverage);target.errors.extend(incoming.errors);
    target.candidates.sort_by(|a,b|b.estimated_bytes.cmp(&a.estimated_bytes).then_with(||a.id.cmp(&b.id)));
    target.snapshot_hash=format!("{:x}",sha2::Sha256::digest(serde_json::to_vec(&target.candidates).map_err(|e|e.to_string())?));Ok(())
}
fn discovery_lane(home:&Path,id:&str,name:&str,work:impl FnOnce()->Result<(),String>){
    let result=run_scoped(id,work);
    let _=update(home,id,|run|{if let Some(discovery)=run.discovery.as_mut(){discovery.pending_sources.retain(|source|source!=name);if let Err(error)=&result{discovery.errors.push(format!("{name} discovery incomplete: {error}"));}}Ok(())});
}
pub(crate) fn record_review_location(home:&Path,id:&str,item:crate::review_storage::Location)->Result<(),String>{update(home,id,|run|{
    if run.status!="inspecting"{return Ok(());}
    if let Some(discovery)=run.discovery.as_mut(){
        note_source(discovery,&item.path,"agent");
        crate::review_storage::retain(&mut discovery.review_locations,item);
    }Ok(())
})?;Ok(())}
pub fn inventory_page(id:String,offset:usize,category:Option<String>)->Result<Value,String>{let home=system::user_home()?;let _=load(&home,&id)?;crate::discovery_inventory::list(&home,&id,offset,50,category.as_deref(),"file",50*1024*1024)}
pub(crate) fn register_candidate(home:&Path,id:&str,path:&str,method:&str,title:&str,reason:&str,impact:&str)->Result<Action,String>{
    if title.is_empty()||title.len()>160||reason.len()>1200||impact.len()>1200{return Err("Invalid candidate description".into());}
    let path=inspection_path(home,id,path)?;
    let command=if method=="trash"{vec![]}else{let (key,_,command,_)=crate::cleanup_discovery::CACHE_QUERIES.iter().find(|(key,_,_,_)|*key==method).ok_or("Use trash or a registered owning-tool cache method")?;std::iter::once(if key.starts_with("go-"){"go"}else{key}).chain(command.iter().copied()).map(str::to_owned).collect()};
    let mut candidate=crate::cleanup_discovery::action(title,path.clone(),command,impact);candidate.reason=reason.into();validate_action(home,&candidate)?;candidate.estimated_bytes=crate::cleanup_discovery::measured(home,&path)?;if candidate.estimated_bytes==0{return Err("The location is empty".into());}
    let mut result=candidate.clone();update(home,id,|run|{
        if run.status!="inspecting"{return Err("Candidates can only be registered during inspection".into());}
        let discovery=run.discovery.as_mut().ok_or("Run native discovery first")?;
        note_source(discovery,&path.to_string_lossy(),"agent");
        if let Some(existing)=discovery.candidates.iter().find(|existing|existing.id==candidate.id){result=existing.clone();return Ok(());}
        if discovery.candidates.iter().flat_map(|c|&c.paths).any(|old|path.starts_with(old)||Path::new(old).starts_with(&path)){return Err("This candidate overlaps an existing native candidate".into());}
        run.measurements.insert(path.to_string_lossy().into_owned(),candidate.estimated_bytes);run.verified_actions.push(action_key(&candidate));discovery.candidates.push(candidate.clone());discovery.candidates.sort_by(|a,b|b.estimated_bytes.cmp(&a.estimated_bytes));
        discovery.snapshot_hash=format!("{:x}",sha2::Sha256::digest(serde_json::to_vec(&discovery.candidates).map_err(|e|e.to_string())?));Ok(())
    })?;Ok(result)
}
pub fn discover_only(profiles:&str,scope:&str)->Result<Value,String>{
    let profiles=profiles.split(',').map(str::to_owned).collect::<Vec<_>>();
    if profiles.iter().any(|p|!["everyday","developer","builder","creator"].contains(&p.as_str())){return Err("Use comma-separated everyday,developer,builder,creator profiles".into());}
    let started=Instant::now();let home=system::user_home()?;let options=crate::cleanup_discovery::Options{profiles,roots:vec![],..Default::default()};let inventory=crate::discovery_inventory::scan(&home,&random_id()?,inventory_roots(&home,scope,&options)?,10,100_000)?;let mut discovery=crate::cleanup_discovery::scan(&home,scope,&options,|_|{})?;discovery.inventory=Some(inventory);discovery.agent=Some(crate::cleanup_discovery::assistance(&discovery,&options.policy));
    Ok(json!({"elapsedMs":started.elapsed().as_millis(),"discovery":discovery}))
}
pub fn inspect_with_options(request:String,scope:String,automatic_enabled:bool)->Result<String,String>{
    inspect_configured(request,scope,automatic_enabled,crate::cleanup_discovery::Options::default())
}
pub fn inspect_configured(request:String,scope:String,automatic_enabled:bool,options:crate::cleanup_discovery::Options)->Result<String,String>{
    if request.trim().is_empty()||request.len()>2000||scope.len()>1000{return Err("Invalid cleanup request".into());}
    options.policy.validate()?;
    let home=system::user_home()?;let id=random_id()?;let account=crate::remote_agent::account_id()?;
    let run=Run{id:id.clone(),status:"inspecting".into(),model:"@cf/qwen/qwen3-30b-a3b-fp8".into(),request,scope,account_id:Some(account),api_origin:Some(crate::remote_agent::base_url()?),overview:String::new(),actions:vec![],approved_ids:vec![],activity:vec!["Discovering exact cleanup candidates before AI review.".into()],outcomes:vec![],recovered_bytes:0,session_id:None,error:None,updated_at:now(),measurements:Default::default(),verified_actions:vec![],schema_version:2,discovery:None,automatic_ids:vec![],automatic_enabled:automatic_enabled&&!options.daily_care,results:None,discovery_options:options};crate::runtime_store::create_run(&home,&id,&serde_json::to_value(&run).map_err(|e|e.to_string())?)?;
    spawn_inspection(home,id.clone());Ok(id)
}
fn spawn_inspection(home:PathBuf,id:String){
    let h=home.clone();let rid=id.clone();thread::spawn(move||{
        let outcome=run_scoped(&rid,||{
            let saved=load(&h,&rid)?;
            if saved.discovery.is_none(){
                let mut discovery=crate::cleanup_discovery::Discovery{discovered_at:now(),snapshot_hash:format!("{:x}",sha2::Sha256::digest(b"[]")),pending_sources:vec!["known-locations".into(),"inventory".into(),"recent".into()],..Default::default()};
                let mut assistance=crate::cleanup_discovery::assistance(&discovery,&saved.discovery_options.policy);assistance.reason="Independent agent exploration, known/app locations, general inventory and recent-space discovery run in parallel. All native-verified findings are merged before review.".into();discovery.agent=Some(assistance);
                update(&h,&rid,|current|{current.discovery=Some(discovery);Ok(())})?;
            }
            let assisted=load(&h,&rid)?.discovery.as_ref().and_then(|d|d.agent.as_ref()).is_some_and(|a|a.triggered);
            if let Some(agent)=load(&h,&rid)?.discovery.and_then(|d|d.agent){append(&h,&rid,agent.reason);}
            // Join all native lanes before final review, including when inference
            // finishes early or fails. Atomic merges never replace agent findings.
            let pending=load(&h,&rid)?.discovery.unwrap().pending_sources;
            let agent_result=thread::scope(|threads|{
                if pending.iter().any(|s|s=="known-locations"){threads.spawn(||discovery_lane(&h,&rid,"known-locations",||{
                    let found=crate::cleanup_discovery::scan(&h,&saved.scope,&saved.discovery_options,|title|append(&h,&rid,format!("Known/app discovery: {title}")))?;
                    update(&h,&rid,|run|merge_discovery(run,found))?;Ok(())
                }));}
                if pending.iter().any(|s|s=="inventory"){threads.spawn(||discovery_lane(&h,&rid,"inventory",||{
                    let inventory=crate::discovery_inventory::scan(&h,&rid,inventory_roots(&h,&saved.scope,&saved.discovery_options)?,10,100_000)?;record_inventory(&h,&rid,inventory)
                }));}
                if pending.iter().any(|s|s=="recent"){threads.spawn(||discovery_lane(&h,&rid,"recent",||{
                    let roots=if saved.scope.is_empty(){std::iter::once(h.clone()).chain(crate::recent_space::temporary_root()).collect::<Vec<_>>()}else{vec![inspection_path(&h,&rid,&saved.scope)?]};
                    for root in roots{
                        let finding=crate::recent_space::inspect(&h,&rid,&json!({"path":root,"hours":24,"seconds":5,"maxEntries":50000,"limit":20}))?;
                        update(&h,&rid,|run|{if let Some(discovery)=run.discovery.as_mut(){discovery.recent_findings.push(finding.clone());discovery.coverage.push(format!("Recent-space metadata under {}: partial {}; current bytes are not measured growth.",root.display(),finding["coverage"]["partial"]));}Ok(())})?;
                        // Exact recent files carry native risk metadata into the
                        // same review list, not a separate text-only report.
                        for row in finding["largestRecentFiles"].as_array().into_iter().flatten().take(12){if let Some(path)=row["path"].as_str(){
                            let measured=crate::review_storage::measure(&h,Path::new(path),Instant::now()+Duration::from_secs(1),&mut 1000);
                            update(&h,&rid,|run|{if let Some(discovery)=run.discovery.as_mut(){note_source(discovery,path,"recent");if let Ok(item)=measured{crate::review_storage::retain(&mut discovery.review_locations,item);}}Ok(())})?;
                        }}
                    }Ok(())
                }));}
                crate::remote_agent::turn(&h,&rid)
            });
            match agent_result{Ok(text)=>{update(&h,&rid,|run|{if let Some(agent)=run.discovery.as_mut().and_then(|d|d.agent.as_mut()){if agent.triggered{agent.status="completed".into();}}Ok(())})?;Ok(text)},Err(error) if assisted&&load(&h,&rid)?.status!="cancelled"=>{
                update(&h,&rid,|run|{if let Some(discovery)=run.discovery.as_mut(){discovery.errors.push(format!("Agent discovery did not complete: {error}. Predefined and already verified results remain available."));if let Some(agent)=discovery.agent.as_mut(){agent.status="failed".into();}}Ok(())})?;
                let run=load(&h,&rid)?;Ok(json!({"overview":"Agent-assisted discovery was unavailable. Review the preserved native findings and general storage inventory.","candidateIds":run.discovery.unwrap().candidates.iter().take(24).map(|c|c.id.clone()).collect::<Vec<_>>()}).to_string())
            },Err(error)=>Err(error)}
        });
        let parsed=outcome.and_then(|text|{
                let text=text.trim().strip_prefix("```json").or_else(||text.trim().strip_prefix("```")).unwrap_or(text.trim()).trim().trim_end_matches("```").trim().to_owned();
                let start=text.find('{').ok_or("The agent did not return a review plan")?;
                let value:Value=serde_json::Deserializer::from_str(&text[start..]).into_iter::<Value>().next().ok_or("The agent did not return a review plan")?.map_err(|_|"The agent did not return a complete review plan")?;
                if load(&h,&rid)?.discovery.is_some()&&value.get("candidateIds").is_none(){return Err("Discovery reviews must select native candidate IDs".into());}
                let proposed:Vec<Action>=if value.get("candidateIds").is_some(){
                    let ids:Vec<String>=serde_json::from_value(value["candidateIds"].clone()).map_err(|_|"Candidate IDs missing")?;
                    let evidence=load(&h,&rid)?;
                    let discovery=evidence.discovery.as_ref().ok_or("Discovery missing")?;
                    combined_candidates(discovery,&ids)?
                }else{serde_json::from_value(value["actions"].clone()).map_err(|_|"The agent plan was incomplete")?};
                let evidence=load(&h,&rid)?;let mut actions=vec![];let mut manual=vec![];
                for mut action in proposed {
                    match validate_action(&h,&action){Ok(()) if evidence.verified_actions.contains(&action_key(&action))&&action.paths.iter().all(|path|evidence.measurements.contains_key(path))=>{
                        let overlaps=actions.iter().flat_map(|a:&Action|&a.paths).any(|old|action.paths.iter().any(|new|Path::new(old).starts_with(new)||Path::new(new).starts_with(old)))||action.paths.iter().enumerate().any(|(i,path)|action.paths.iter().skip(i+1).any(|other|Path::new(path).starts_with(other)||Path::new(other).starts_with(path)));
                        if overlaps{manual.push(format!("{} overlaps another measured location and is excluded.",action.title));continue;}
                        action.estimated_bytes=action.paths.iter().map(|p|evidence.measurements.get(p).copied().unwrap_or(0)).sum();actions.push(action);
                    },Ok(())=>manual.push(format!("{} was not measured and verified; ask the agent to check it again.",action.title)),Err(reason)=>manual.push(format!("{}: {reason}",action.title))}
                }
                if evidence.discovery.is_none()&&actions.len()>24{return Err("The agent returned too many actions; ask for a smaller cleanup".into());}
                let mut seen=HashSet::new();for action in &actions{if !seen.insert(action.id.clone()){return Err("The agent duplicated an action".into());}validate_action(&h,action)?;}
                let overview=if evidence.discovery.is_some(){let mut summary=verified_overview(&evidence,&actions);if !manual.is_empty(){summary.push_str(" Some proposed locations were excluded by native validation.");}summary}else{format!("{}{}",value["overview"].as_str().unwrap_or("Review the agent's verified cleanup plan."),if manual.is_empty(){String::new()}else{format!("\n{}",manual.join("\n"))})};
                Ok((overview,actions))
            });
        let reviewed=update(&h,&rid,|current|{if current.status=="cancelled"{return Ok(());}match parsed{Ok((overview,actions))=>{current.status="review".into();current.overview=overview;current.automatic_ids=actions.iter().filter(|a|a.mode=="automatic").map(|a|a.id.clone()).collect();current.actions=actions;},Err(error)=>{current.status="failed".into();current.error=Some(error);}}Ok(())});
        if let Ok(reviewed)=reviewed{
            if reviewed.discovery_options.daily_care{
                let ids=if reviewed.status=="review"{crate::daily_care::approved_ids(&h,&reviewed)}else{Ok(vec![])};
                match ids{
                    Ok(ids) if !ids.is_empty()=>{if ids.len()<reviewed.actions.len(){let _=crate::daily_care::publish(&h,&reviewed);}if let Err(error)=authorize_and_execute(rid.clone(),ids,ApprovalSource::Daily){let _=update(&h,&rid,|run|{run.error=Some(error);Ok(())});let _=crate::daily_care::publish(&h,&load(&h,&rid).unwrap_or(reviewed));}},
                    Err(error)=>{let _=update(&h,&rid,|run|{run.error=Some(error);Ok(())});let _=crate::daily_care::publish(&h,&load(&h,&rid).unwrap_or(reviewed));},
                    _=>{let _=crate::daily_care::publish(&h,&reviewed);}
                }
            }else if reviewed.status=="review"&&reviewed.automatic_enabled&&!reviewed.automatic_ids.is_empty(){let _=authorize_and_execute(rid,reviewed.automatic_ids,ApprovalSource::Automatic);}
        }
    });
}
pub fn resume(id:String)->Result<(),String>{
    let home=system::user_home()?;
    let account=crate::remote_agent::account_id()?;
    update_claimed(&home,&id,true,|run|{
        if run.status!="failed"||!run.approved_ids.is_empty(){return Err("Only interrupted inspections can be resumed. Started cleanup actions are not replayed.".into());}
        if run.account_id.as_deref()!=Some(account.as_str()){return Err("Use the account that started this inspection".into());}
        if !resumable_failure(run.error.as_deref()){return Err("This inference attempt failed. Start a new inspection instead of resuming the failed step.".into());}
        run.status="inspecting".into();run.error=None;Ok(())
    })?;
    spawn_inspection(home,id);Ok(())
}
fn resumable_failure(error:Option<&str>)->bool{
    error.is_some_and(|error|error.starts_with("Agent connection interrupted.")||error.starts_with("Inspection reached its time limit.")||error.starts_with("The app stopped during this run."))
}
#[derive(Clone,Copy)]enum ApprovalSource{User,Daily,Automatic}
pub fn approve(id:String,ids:Vec<String>)->Result<(),String>{authorize_and_execute(id,ids,ApprovalSource::User)}
fn authorize_and_execute(id:String,ids:Vec<String>,source:ApprovalSource)->Result<(),String>{
    let home=system::user_home()?;
    let account=crate::remote_agent::local_account_id()?;
    let approved=update_claimed(&home,&id,true,|run|{
        if !["review","done"].contains(&run.status.as_str())||ids.is_empty()||ids.len()!=ids.iter().collect::<HashSet<_>>().len()||ids.iter().any(|id|!run.actions.iter().any(|a|&a.id==id)||run.outcomes.iter().any(|o|&o.id==id)){return Err("Approve unattempted actions from the current review plan".into());}
        if run.account_id.as_deref()!=Some(account.as_str()){return Err("Use the account that inspected these locations".into());}
        for action in run.actions.iter().filter(|a|ids.contains(&a.id)){if !run.verified_actions.contains(&action_key(action)){return Err("This action was not verified by the agent".into());}}
        match source{
            ApprovalSource::User=>{},
            ApprovalSource::Daily=>{for action in run.actions.iter().filter(|a|ids.contains(&a.id)){if !crate::daily_care::allowed(&home,run,action)?{return Err("Daily care needs a saved approval for this exact location and method".into());}}},
            ApprovalSource::Automatic=>{if !run.automatic_enabled||ids.iter().any(|id|!run.automatic_ids.contains(id)){return Err("Automatic cache eligibility was not enabled for this run".into());}},
        }
        run.approved_ids.extend(ids.clone());run.status="executing".into();Ok(())
    })?;
    if matches!(source,ApprovalSource::User){if let Err(error)=crate::daily_care::remember(&home,&approved,&ids){let _=update(&home,&id,|run|{if run.status=="executing"{run.status="review".into();run.approved_ids.retain(|id|!ids.contains(id));}Ok(())});return Err(error);}}
    thread::spawn(move||{
        let before=system::disk_space().ok().map(|(_,free)|free);
        let mut failure=None;
        // Approved actions are deterministic. Execution needs no inference call.
        for action_id in &ids{
            if load(&home,&id).is_ok_and(|r|r.status=="cancelled"){break;}
            if let Err(error)=crate::cleanup_tools::execute_local(&home,&id,action_id){failure=Some(error);}
        }
        let finished=update(&home,&id,|current|{
            for action in current.actions.iter().filter(|a|current.approved_ids.contains(&a.id)){if !current.outcomes.iter().any(|o|o.id==action.id){let mut item=Outcome::started(action.id.clone());item.status="skipped".into();item.detail="Action was not completed".into();current.outcomes.push(item);}}
            let delta=before.zip(system::disk_space().ok().map(|(_,free)|free)).map(|(before,after)|(after as i128-before as i128).clamp(i64::MIN as i128,i64::MAX as i128) as i64);
            current.recovered_bytes=delta.unwrap_or(0).max(0) as u64;
            current.results=Some(summarize_results(&current.outcomes,delta));
            if current.status!="cancelled"{current.status="done".into();}current.error=failure;Ok(())
        });
        if let Ok(run)=finished{let _=crate::daily_care::publish(&home,&run);}
    });Ok(())
}
pub(crate) fn begin_action(home:&Path,id:&str,action_id:&str)->Result<(Action,Option<Outcome>),String>{
    let mut result=None;
    update(home,id,|run|{
        if run.status!="executing"||!run.approved_ids.iter().any(|id|id==action_id){return Err("The user has not approved this action".into());}
        let action=run.actions.iter().find(|a|a.id==action_id).ok_or("Unknown approved action")?.clone();
        if run.discovery_options.daily_care&&!crate::daily_care::allowed(home,run,&action)?{return Err("This saved approval was revoked before execution".into());}
        let previous=run.outcomes.iter().find(|o|o.id==action_id).cloned();
        if previous.is_none(){run.outcomes.push(Outcome::started(action_id.into()));run.activity.push(format!("Cleaning: {}",action.title));}
        result=Some((action,previous));Ok(())
    })?;Ok(result.unwrap())
}
pub(crate) fn finish_action(home:&Path,id:&str,result:Outcome)->Result<(),String>{update(home,id,|r|{let outcome=r.outcomes.iter_mut().find(|o|o.id==result.id).ok_or("Action was not started")?;*outcome=result;Ok(())})?;Ok(())}
fn select_candidates(discovery:&crate::cleanup_discovery::Discovery,ids:&[String])->Result<Vec<Action>,String>{
    if ids.len()>24||ids.iter().collect::<HashSet<_>>().len()!=ids.len(){return Err("Invalid candidate selection".into());}
    ids.iter().map(|id|discovery.candidates.iter().find(|a|&a.id==id).cloned().ok_or("Unknown native candidate".into())).collect()
}
fn combined_candidates(discovery:&crate::cleanup_discovery::Discovery,ids:&[String])->Result<Vec<Action>,String>{
    let mut combined=select_candidates(discovery,ids)?;
    for candidate in &discovery.candidates{if !combined.iter().any(|old|old.id==candidate.id){combined.push(candidate.clone());}}Ok(combined)
}
fn summarize_results(items:&[Outcome],available_space_change:Option<i64>)->CleanupResults{
    let before_bytes=items.iter().map(|item|item.before_bytes).sum::<Option<u64>>();
    let removed_bytes=items.iter().map(|item|item.removed_bytes).sum::<Option<u64>>();
    let percent_cleaned=before_bytes.zip(removed_bytes).filter(|(before,_)|*before>0).map(|(before,removed)|100.0*removed as f64/before as f64);
    CleanupResults{schema_version:2,success:items.iter().filter(|o|o.status=="success").count(),failed:items.iter().filter(|o|o.status=="failed").count(),skipped:items.iter().filter(|o|o.status=="skipped").count(),before_bytes,removed_bytes,percent_cleaned,pending_trash_bytes:items.iter().map(|o|o.pending_trash_bytes).sum(),available_space_change,items:items.to_vec()}
}

pub fn mcp()->Result<(),String>{crate::cleanup_tools::serve()}
pub(crate) fn tool_run(home:&Path,id:&str)->Result<Run,String>{load(home,id)}
pub(crate) fn tool_path(home:&Path,raw:&str)->Result<PathBuf,String>{checked_path(home,raw)}
pub(crate) fn tool_output(home:&Path,argv:&[String],cwd:Option<&Path>,seconds:u64)->Result<String,String>{output(home,argv,cwd,seconds)}
pub(crate) fn tool_tree_output(home:&Path,path:&Path,depth:u64)->Result<(String,String,std::process::ExitStatus),String>{capture_output(home,&["du".into(),"-kx".into(),"-d".into(),depth.to_string(),path.to_string_lossy().into_owned()],None,60)}
pub(crate) fn tool_trash(home:&Path,raw:&str)->Result<PathBuf,String>{trash_path(home,raw)}

#[cfg(test)] pub(crate) fn fixture_run(home:&Path,action:Action,approved:bool)->Run{
    let id=random_id().unwrap();
    let run=Run{id,status:if approved{"executing".into()}else{"review".into()},model:"fixture/model".into(),request:"Fixture only".into(),scope:String::new(),account_id:None,api_origin:None,overview:"Fixture".into(),approved_ids:if approved{vec![action.id.clone()]}else{vec![]},actions:vec![action],activity:vec![],outcomes:vec![],recovered_bytes:0,session_id:None,error:None,updated_at:now(),measurements:Default::default(),verified_actions:vec![],schema_version:2,discovery:None,automatic_ids:vec![],automatic_enabled:false,results:None,discovery_options:Default::default()};
    save(home,&run).unwrap();run
}
#[cfg(test)]pub(crate) fn fixture_add_approved(home:&Path,id:&str,action:Action){update(home,id,|run|{run.approved_ids.push(action.id.clone());run.actions.push(action);Ok(())}).unwrap();}
#[cfg(test)]pub(crate) fn fixture_inspecting(home:&Path,id:&str){update(home,id,|run|{run.status="inspecting".into();let discovery=crate::cleanup_discovery::Discovery::default();let mut discovered=discovery.clone();discovered.agent=Some(crate::cleanup_discovery::assistance(&discovery,&Default::default()));run.discovery=Some(discovered);Ok(())}).unwrap();}

#[cfg(test)]mod parallel_discovery_tests{
    use super::*;
    #[test]fn native_merges_preserve_agent_candidates_and_all_locations_reach_review(){
        let home=fs::canonicalize(std::env::temp_dir()).unwrap().join(format!("br-merge-{}-{}",std::process::id(),now()));fs::create_dir_all(&home).unwrap();
        let agent=crate::cleanup_discovery::action("Agent",home.join("Library/Caches/agent"),vec![],"Rebuild");let mut run=fixture_run(&home,agent.clone(),false);run.status="inspecting".into();run.discovery=Some(crate::cleanup_discovery::Discovery{candidates:vec![agent.clone()],..Default::default()});
        let candidates=(0..55).map(|index|crate::cleanup_discovery::action("Native",home.join(format!("Library/Caches/native-{index}")),vec![],"Rebuild")).collect();
        merge_discovery(&mut run,crate::cleanup_discovery::Discovery{candidates,..Default::default()}).unwrap();
        let discovery=run.discovery.as_ref().unwrap();assert_eq!(discovery.candidates.len(),56);assert!(discovery.candidates.iter().any(|item|item.id==agent.id));assert_eq!(combined_candidates(discovery,&[agent.id]).unwrap().len(),56);assert_eq!(discovery.sources.values().filter(|sources|sources.contains(&"known-locations".into())).count(),55);
        let repeated=discovery.candidates[1].clone();merge_discovery(&mut run,crate::cleanup_discovery::Discovery{candidates:vec![repeated],..Default::default()}).unwrap();assert_eq!(run.discovery.unwrap().candidates.len(),56);fs::remove_dir_all(home).unwrap();
    }
}

#[cfg(test)] mod tests {
    use super::*;
    fn action(command:&[&str])->Action{Action{id:"test".into(),title:"Cache".into(),reason:"Fixture".into(),impact:"Re-download".into(),kind:"command".into(),paths:vec!["/opt/homebrew".into()],command:command.iter().map(|v|v.to_string()).collect(),cwd:None,estimated_bytes:0,mode:"command".into(),native_rule:String::new()}}
    #[test]fn shell_commands_cannot_be_approved(){let home=system::user_home().unwrap();assert!(validate_action(&home,&action(&["sh","-c","rm -rf ~"])).is_err());assert!(validate_action(&home,&action(&["rm","-rf","/"])).is_err());}
    #[test]fn runtime_path_discovers_version_managers_without_shell_startup(){let home=Path::new("/fixture");assert!(runtime_path(home).contains("/fixture/.opencode/bin"));}
    #[test]fn ids_cannot_escape_session_storage(){assert!(!valid_id("../state"));assert!(valid_id(&"a".repeat(32)));}
    #[test]fn terminal_model_failures_require_a_fresh_inspection(){assert!(!resumable_failure(Some("The model did not return a complete valid plan. Inspect again")));assert!(!resumable_failure(Some("The previous inference step failed. Start a new inspection")));assert!(resumable_failure(Some("Agent connection interrupted. Resume this inspection to retrieve saved steps")));assert!(resumable_failure(Some("The app stopped during this run. Resume inspection, or review interrupted action outcomes.")));}
    #[test]fn exited_commands_cannot_hang_on_inherited_background_pipes(){let home=fs::canonicalize(std::env::temp_dir()).unwrap().join(format!("br-pipe-timeout-{}",random_id().unwrap()));let bin=home.join(".local/bin");fs::create_dir_all(&bin).unwrap();let command=bin.join("fixture-pipe");fs::write(&command,b"#!/bin/sh\n/bin/sleep 20 &\nexit 0\n").unwrap();fs::set_permissions(&command,fs::Permissions::from_mode(0o700)).unwrap();let started=Instant::now();let result=capture_output(&home,&["fixture-pipe".into()],None,1);assert!(result.is_err());assert!(started.elapsed()<Duration::from_secs(3));fs::remove_dir_all(home).unwrap();}
    #[test]fn model_selection_cannot_invent_ids_or_change_native_authority(){let native=action(&["npm","cache","clean","--force"]);let discovery=crate::cleanup_discovery::Discovery{candidates:vec![native.clone()],..Default::default()};assert!(select_candidates(&discovery,&["invented".into()]).is_err());assert!(select_candidates(&discovery,&["test".into(),"test".into()]).is_err());let selected=select_candidates(&discovery,&["test".into()]).unwrap();assert_eq!(selected[0].command,native.command);assert_eq!(selected[0].mode,"command");}
    #[test]fn restored_review_summary_uses_native_counts_not_model_claims(){
        let home=fs::canonicalize(std::env::temp_dir()).unwrap().join(format!("br-overview-{}",random_id().unwrap()));
        let mut native=action(&["npm","cache","clean","--force"]);native.estimated_bytes=4096;
        let mut run=fixture_run(&home,native.clone(),false);run.overview="Found 24 caches and 12.5GB; already cleaned everything".into();
        run.discovery=Some(crate::cleanup_discovery::Discovery{candidates:vec![native],inventory:Some(crate::discovery_inventory::Summary{files_inspected:7,directories_inspected:2,partial:true,..Default::default()}),..Default::default()});save(&home,&run).unwrap();
        let restored=state_at_for_test(&home,&run.id);assert!(restored.contains("1 selected locations from 1 measured cleanup candidates"));assert!(restored.contains("4096 allocated bytes"));assert!(restored.contains("coverage is partial"));assert!(!restored.contains("12.5GB"));assert!(!restored.contains("already cleaned"));fs::remove_dir_all(home).unwrap();
    }
    fn state_at_for_test(home:&Path,id:&str)->String{let run=load(home,id).unwrap();verified_overview(&run,&run.actions)}
    #[test]fn result_percent_is_weighted_and_unknown_sizes_stay_unknown(){let mut first=Outcome::started("first".into());first.status="success".into();first.ok=true;first.before_bytes=Some(100);first.removed_bytes=Some(50);first.pending_trash_bytes=50;let mut second=Outcome::started("second".into());second.status="failed".into();second.before_bytes=Some(900);second.removed_bytes=Some(0);let result=summarize_results(&[first.clone(),second.clone()],Some(-20));assert_eq!(result.percent_cleaned,Some(5.0));assert_eq!(result.pending_trash_bytes,50);assert_eq!(result.failed,1);assert_eq!(result.available_space_change,Some(-20));second.before_bytes=None;assert_eq!(summarize_results(&[first,second],None).percent_cleaned,None);}
    #[test]fn command_scopes_must_include_exact_targets(){assert!(same_scope(&["/fixture/cache".into()],&[PathBuf::from("/fixture/cache")]));assert!(!same_scope(&["/fixture".into()],&[PathBuf::from("/fixture/cache")]));assert!(!same_scope(&["/fixture/cache".into()],&[PathBuf::from("/fixture/cache"),PathBuf::from("/fixture/modules")]));assert!(!exact_flags(&["cache","clean","--force","--unknown"],&["cache","clean"],&["--force"],Some("--cache")));}
    #[test]fn inspector_cannot_move_a_whole_home_or_personal_documents(){let home=system::user_home().unwrap();assert!(trash_path(&home,&home.to_string_lossy()).is_err());assert!(trash_path(&home,&home.join("Documents").to_string_lossy()).is_err());}
    #[test]fn generated_tool_scopes_do_not_include_adjacent_data(){
        let home=fs::canonicalize(std::env::temp_dir()).unwrap().join(format!("breathing-scope-{}",random_id().unwrap()));
        for name in [".npm/_npx",".npm/_npx-other","Library/Developer/Xcode/DerivedData","Library/Developer/Xcode/UserData","Library/Developer/Xcode/Archives"]{fs::create_dir_all(home.join(name)).unwrap();}
        assert!(trash_path(&home,&home.join(".npm/_npx").to_string_lossy()).is_ok());
        assert!(trash_path(&home,&home.join("Library/Developer/Xcode/DerivedData").to_string_lossy()).is_ok());
        for name in [".npm/_npx-other","Library/Developer/Xcode/UserData","Library/Developer/Xcode/Archives"]{assert!(trash_path(&home,&home.join(name).to_string_lossy()).is_err());}
        fs::write(home.join(".npm/_npx/package.json"),b"{}").unwrap();assert!(trash_path(&home,&home.join(".npm/_npx").to_string_lossy()).is_err());
        fs::remove_dir_all(home).unwrap();
    }
    #[test]fn generated_names_need_project_or_app_evidence(){
        let home=fs::canonicalize(std::env::temp_dir()).unwrap().join(format!("breathing-evidence-{}",random_id().unwrap()));
        for name in ["Pictures/target","Documents/cache","code/project/dist","code/project/.next"]{fs::create_dir_all(home.join(name)).unwrap();}
        fs::write(home.join("code/project/package.json"),b"{}").unwrap();fs::write(home.join("code/project/.next/package.json"),b"{}").unwrap();
        for name in ["Pictures/target","Documents/cache"]{assert!(trash_path(&home,&home.join(name).to_string_lossy()).is_err());}
        for name in ["code/project/dist","code/project/.next"]{assert!(trash_path(&home,&home.join(name).to_string_lossy()).is_ok());}
        fs::remove_dir_all(home).unwrap();
    }
}
