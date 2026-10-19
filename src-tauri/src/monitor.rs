//! Local, bounded observational telemetry. File paths never imply a proven writer PID.
use crate::{anomalies::{AlertConfig, Detector}, fswatch::{self, Change, WatchState}, model::{now, Process}, processes, system};
use rusqlite::{params, Connection, OptionalExtension};
use serde::{Deserialize, Serialize};
use serde_json::{json, Value};
use std::{collections::{BTreeMap, HashMap, VecDeque}, ffi::CString, fs, os::unix::fs::MetadataExt,
    path::{Path, PathBuf}, sync::{atomic::Ordering, mpsc, Arc, Mutex}, time::{Duration, Instant}};
use std::os::unix::fs::PermissionsExt;

#[derive(Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct Config { pub enabled: bool, pub file_events: bool, pub process_io: bool, pub interval_seconds: u64, #[serde(default)] pub alerts: AlertConfig }
impl Default for Config { fn default() -> Self { Self { enabled: true, file_events: true, process_io: true, interval_seconds: 5, alerts:AlertConfig::default() } } }

#[derive(Clone, Debug, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct LogEvent {
    pub timestamp: u64, pub kind: String, pub path: String, pub owner: String, pub workflow: String,
    pub attribution: String, pub pid: Option<i32>, pub process_identity: String, pub flags: u32,
    pub size_bytes: Option<u64>, pub delta_bytes: Option<i64>, pub read_bytes: u64, pub write_bytes: u64,
    pub detail: String,
}
impl LogEvent {
    fn new(kind: &str, path: String, owner: String, workflow: String, attribution: &str) -> Self {
        Self { timestamp: now(), kind: kind.into(), path, owner, workflow, attribution: attribution.into(),
            pid: None, process_identity: String::new(), flags: 0, size_bytes: None, delta_bytes: None,
            read_bytes: 0, write_bytes: 0, detail: String::new() }
    }
}

pub struct Monitor {
    pub detector: Mutex<Detector>,
    pub config: Mutex<Config>, db: Mutex<Connection>, pub watch: Arc<WatchState>,
    status: Mutex<Value>, folder: PathBuf,
    publisher: Mutex<Option<Arc<dyn Fn(Value)+Send+Sync>>>,
}

fn initialize(connection: &Connection) -> rusqlite::Result<()> {
    connection.execute_batch("PRAGMA journal_mode=WAL; PRAGMA synchronous=NORMAL; PRAGMA auto_vacuum=INCREMENTAL; PRAGMA wal_autocheckpoint=512;
      CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY, timestamp INTEGER NOT NULL, kind TEXT NOT NULL, path TEXT NOT NULL,
        owner TEXT NOT NULL, workflow TEXT NOT NULL, attribution TEXT NOT NULL, pid INTEGER,
        process_identity TEXT NOT NULL, flags INTEGER NOT NULL, size_bytes INTEGER, delta_bytes INTEGER,
        read_bytes INTEGER NOT NULL, write_bytes INTEGER NOT NULL, detail TEXT NOT NULL);
      CREATE INDEX IF NOT EXISTS events_time ON events(timestamp);
      CREATE INDEX IF NOT EXISTS events_kind_time ON events(kind,timestamp);
      CREATE TABLE IF NOT EXISTS disk_samples (id INTEGER PRIMARY KEY, timestamp INTEGER NOT NULL,
        total_bytes INTEGER NOT NULL, available_bytes INTEGER NOT NULL, cpu_percent REAL,
        read_bytes INTEGER NOT NULL, write_bytes INTEGER NOT NULL, sample_ms REAL NOT NULL);
      CREATE TABLE IF NOT EXISTS file_state (path TEXT PRIMARY KEY, identity TEXT NOT NULL,
        size_bytes INTEGER NOT NULL, timestamp INTEGER NOT NULL);")
}
fn insert(connection: &Connection, event: &LogEvent) -> rusqlite::Result<()> {
    connection.execute("INSERT INTO events(timestamp,kind,path,owner,workflow,attribution,pid,process_identity,flags,size_bytes,delta_bytes,read_bytes,write_bytes,detail)
      VALUES(?1,?2,?3,?4,?5,?6,?7,?8,?9,?10,?11,?12,?13,?14)", params![event.timestamp,event.kind,event.path,event.owner,event.workflow,event.attribution,event.pid,event.process_identity,event.flags,event.size_bytes,event.delta_bytes,event.read_bytes,event.write_bytes,event.detail])?;
    Ok(())
}
fn retention(connection: &Connection) -> rusqlite::Result<()> {
    connection.execute("DELETE FROM events WHERE timestamp < ?1 OR id < COALESCE((SELECT id FROM events ORDER BY id DESC LIMIT 1 OFFSET 49999),0)", [now().saturating_sub(7*86400)])?;
    connection.execute("DELETE FROM disk_samples WHERE timestamp < ?1 OR id < COALESCE((SELECT id FROM disk_samples ORDER BY id DESC LIMIT 1 OFFSET 19999),0)", [now().saturating_sub(7*86400)])?;
    connection.execute("DELETE FROM file_state WHERE timestamp < ?1 OR path IN (SELECT path FROM file_state ORDER BY timestamp DESC LIMIT -1 OFFSET 50000)", [now().saturating_sub(7*86400)])?;
    Ok(())
}

pub fn normalized_path(raw: &str) -> String {
    raw.strip_prefix("/System/Volumes/Data").filter(|p| p.starts_with('/')).unwrap_or(raw).to_string()
}
pub fn attribution(path: &str, home: &Path) -> (String, String) {
    let relative = Path::new(path).strip_prefix(home).unwrap_or(Path::new(path));
    let parts: Vec<_> = relative.components().map(|p| p.as_os_str().to_string_lossy().into_owned()).collect();
    if let Some(first) = parts.first() {
        for (prefix, owner) in [(".npm", "npm"), (".bun", "Bun"), (".cargo", "Rust / Cargo"), (".gradle", "Gradle"), (".m2", "Maven"), (".ollama", "Ollama")] {
            if first == prefix { return (owner.into(), "Development caches".into()); }
        }
        if ["code", "Projects", "workspace", "Work"].contains(&first.as_str()) && parts.len() > 1 {
            return ("Project tools".into(), format!("{}/{}", first, parts[1]));
        }
    }
    if parts.first().is_some_and(|p| p == "Library") && parts.len() > 2 {
        let owner = match parts[2].as_str() { "Google" => "Google Chrome", "Code" => "Visual Studio Code", "Cursor" => "Cursor", "pip" => "Python / pip", "uv" => "Python / uv", "Homebrew" => "Homebrew", other => other };
        return (owner.into(), if parts[1] == "Caches" { "App caches" } else { "App data" }.into());
    }
    if parts.first().is_some_and(|p| ["Downloads", "Documents", "Pictures", "Movies", "Music", "Desktop"].contains(&p.as_str())) {
        return ("Unattributed".into(), parts[0].clone());
    }
    ("Unattributed".into(), "System / shared files".into())
}
pub fn event_kind(flags: u32) -> &'static str {
    if flags & 0x7 != 0 { "coverage_gap" }
    else if flags & 0x200 != 0 { "removed" }
    else if flags & 0x800 != 0 { "renamed" }
    else if flags & 0x100 != 0 { if flags & 0x20000 != 0 { "folder_created" } else { "file_created" } }
    else if flags & 0x1000 != 0 { "file_changed" }
    else { "metadata_changed" }
}
fn reconcile(connection: &Connection, change: &Change, home: &Path) -> rusqlite::Result<LogEvent> {
    let path = normalized_path(&change.path);
    let (owner, workflow) = attribution(&path, home);
    let kind = event_kind(change.flags);
    let mut event = LogEvent::new(kind, path.clone(), owner, workflow, "Path inference · writer unknown");
    event.timestamp = change.at; event.flags = change.flags;
    event.detail = format!("FSEvents notification {} · changes may be coalesced", change.event_id);
    if kind == "coverage_gap" { event.detail = "macOS dropped/coalesced events; a full scan is needed for complete attribution".into(); return Ok(event); }
    let previous: Option<(String,u64)> = connection.query_row("SELECT identity,size_bytes FROM file_state WHERE path=?1", [&path], |row| Ok((row.get(0)?,row.get(1)?))).optional()?;
    match fs::symlink_metadata(&path) {
        Ok(metadata) if metadata.is_file() && !metadata.file_type().is_symlink() => {
            let identity = format!("{}:{}", metadata.dev(), metadata.ino());
            if kind == "file_created" && previous.as_ref().is_some_and(|(old_id,_)|old_id==&identity) {
                event.kind="file_changed".into();
                event.detail.push_str(" · creation flag repeated for an already observed file");
            }
            let bytes = metadata.blocks().saturating_mul(512);
            event.size_bytes = Some(bytes);
            event.delta_bytes = match previous {
                Some((old_id, size)) if old_id == identity && kind != "renamed" => Some(bytes as i64 - size as i64),
                None if kind == "file_created" => { event.detail.push_str(" · estimated zero baseline for newly observed creation"); Some(bytes.min(i64::MAX as u64) as i64) },
                _ => None,
            };
            connection.execute("INSERT INTO file_state(path,identity,size_bytes,timestamp) VALUES(?1,?2,?3,?4) ON CONFLICT(path) DO UPDATE SET identity=excluded.identity,size_bytes=excluded.size_bytes,timestamp=excluded.timestamp", params![path,identity,bytes,event.timestamp])?;
        }
        Err(_) if kind == "removed" => {
            event.delta_bytes = previous.map(|(_, size)| -(size.min(i64::MAX as u64) as i64));
            connection.execute("DELETE FROM file_state WHERE path=?1", [&path])?;
        }
        _ => {}
    }
    Ok(event)
}

fn fair_changes(pending: BTreeMap<String,Change>, limit: usize) -> Vec<Change> {
    let mut folders:BTreeMap<String,VecDeque<Change>>=BTreeMap::new();
    for change in pending.into_values() {
        let folder=Path::new(&change.path).parent().unwrap_or(Path::new("/")).to_string_lossy().into_owned();
        folders.entry(folder).or_default().push_back(change);
    }
    let mut selected=vec![];
    while selected.len()<limit && !folders.is_empty() {
        for queue in folders.values_mut() {
            if selected.len()>=limit {break;}
            if let Some(change)=queue.pop_front(){selected.push(change);}
        }
        folders.retain(|_,queue|!queue.is_empty());
    }
    selected
}

#[repr(C)]
#[derive(Default)]
struct RUsage { uuid: [u8;16], counters: [u64;18] }
#[link(name = "proc")]
extern "C" { fn proc_pid_rusage(pid: i32, flavor: i32, buffer: *mut std::ffi::c_void) -> i32; }
fn io_counters(pid: i32) -> Option<(u64,u64,u64,u64,u64)> {
    let mut usage = RUsage::default();
    if unsafe { proc_pid_rusage(pid, 2, &mut usage as *mut _ as *mut std::ffi::c_void) } != 0 { return None; }
    Some((usage.counters[8],usage.counters[16],usage.counters[17],usage.counters[6],usage.counters[0].saturating_add(usage.counters[1])))
}
fn disk() -> Option<(u64,u64)> {
    let path = CString::new("/System/Volumes/Data").ok()?;
    let mut info: libc::statvfs = unsafe { std::mem::zeroed() };
    if unsafe { libc::statvfs(path.as_ptr(), &mut info) } != 0 { return None; }
    Some(((info.f_blocks as u64).saturating_mul(info.f_frsize),(info.f_bavail as u64).saturating_mul(info.f_frsize)))
}
fn memory_used(total:u64,page_size:u64,anonymous:u64,purgeable:u64,wired:u64,compressed:u64)->Option<u64>{
    if total==0||page_size==0{return None;}
    // Physical RAM occupied by non-purgeable anonymous pages, wired memory and
    // the compressor. Reclaimable file cache is excluded; this is not summed RSS.
    anonymous.saturating_sub(purgeable).checked_add(wired)?.checked_add(compressed)?.checked_mul(page_size).map(|bytes|bytes.min(total))
}
fn system_memory()->Option<(u64,u64)>{
    static TOTAL:std::sync::OnceLock<Option<u64>>=std::sync::OnceLock::new();
    static HOST:std::sync::OnceLock<libc::mach_port_t>=std::sync::OnceLock::new();
    let total=(*TOTAL.get_or_init(||{let mut bytes=0u64;let mut size=std::mem::size_of::<u64>();let result=unsafe{libc::sysctlbyname(c"hw.memsize".as_ptr(),&mut bytes as *mut _ as *mut libc::c_void,&mut size,std::ptr::null_mut(),0)};if result==0&&size==8&&bytes>0{Some(bytes)}else{None}}))?;
    // libc deprecates its binding, not the macOS API. Retain one read-only host
    // send right for the process lifetime rather than leaking a right per sample.
    #[allow(deprecated)]
    let host=*HOST.get_or_init(||unsafe{libc::mach_host_self()});
    let mut stats:libc::vm_statistics64=unsafe{std::mem::zeroed()};let mut count=libc::HOST_VM_INFO64_COUNT;
    let result=unsafe{libc::host_statistics64(host,libc::HOST_VM_INFO64,&mut stats as *mut _ as libc::host_info64_t,&mut count)};
    let needed=(std::mem::offset_of!(libc::vm_statistics64,internal_page_count)+std::mem::size_of::<libc::natural_t>())/std::mem::size_of::<libc::integer_t>();
    let page_size=unsafe{libc::sysconf(libc::_SC_PAGESIZE)};
    if result!=libc::KERN_SUCCESS||(count as usize)<needed||page_size<=0{return None;}
    let used=memory_used(total,page_size as u64,stats.internal_page_count as u64,stats.purgeable_count as u64,stats.wire_count as u64,stats.compressor_page_count as u64)?;
    Some((total,used))
}
fn identity(p: &Process) -> String { format!("{}:{}:{}:{}",p.pid,p.uid,p.started,p.executable) }
fn app(p: &Process) -> (String,String) {
    if let Some(end) = p.executable.find(".app/") {
        let path = p.executable[..end+4].to_string();
        (Path::new(&path).file_stem().map(|v| v.to_string_lossy().into_owned()).unwrap_or(p.name.clone()),path)
    } else { (p.name.clone(),p.executable.clone()) }
}
fn process_transitions(previous: &HashMap<String,Process>, current: &HashMap<String,Process>, seeded: bool) -> Vec<LogEvent> {
    if !seeded { return vec![]; }
    let mut result = vec![];
    let previous_apps: std::collections::HashSet<_> = previous.values().filter(|p| p.executable.contains(".app/")).map(|p| app(p).1).collect();
    let mut started_apps = std::collections::HashSet::new();
    for (id,p) in current {
        if previous.contains_key(id) { continue; }
        let (name,path) = app(p);
        let mut event = LogEvent::new("process_started", path.clone(),name.clone(),"Processes".into(),"Observed process identity");
        event.pid = Some(p.pid); event.process_identity = id.clone(); event.detail = format!("{} · parent PID {} · sampled start",p.name,p.parent_pid); result.push(event);
        if p.executable.contains(".app/") && !previous_apps.contains(&path) && started_apps.insert(path.clone()) {
            let mut event = LogEvent::new("app_started",path,name,"Apps".into(),"Observed bundle transition");
            event.pid=Some(p.pid); event.process_identity=id.clone(); result.push(event);
        }
    }
    for (id,p) in previous {
        if current.contains_key(id) { continue; }
        let (name,path) = app(p);
        let mut event = LogEvent::new("process_exited",path,name,"Processes".into(),"Missing from next successful sample");
        event.pid=Some(p.pid); event.process_identity=id.clone(); result.push(event);
    }
    result
}

impl Monitor {
    pub fn start() -> Result<Arc<Self>, String> {
        let folder = dirs::data_local_dir().ok_or("Local database folder unavailable")?.join("app.breathingroom.mac");
        fs::create_dir_all(&folder).map_err(|e| e.to_string())?;
        fs::set_permissions(&folder,fs::Permissions::from_mode(0o700)).map_err(|e|e.to_string())?;
        let config = fs::read(folder.join("monitor.json")).ok().and_then(|b| serde_json::from_slice::<Config>(&b).ok()).filter(|c| [5,15].contains(&c.interval_seconds) && c.alerts.validate().is_ok()).unwrap_or_default();
        let db = Connection::open(folder.join("activity.sqlite")).map_err(|e| e.to_string())?;
        db.busy_timeout(Duration::from_millis(500)).map_err(|e| e.to_string())?;
        initialize(&db).map_err(|e| e.to_string())?;
        fs::set_permissions(folder.join("activity.sqlite"),fs::Permissions::from_mode(0o600)).map_err(|e|e.to_string())?;
        retention(&db).map_err(|e|e.to_string())?;
        let watch = Arc::new(WatchState::default());
        watch.enabled.store(config.enabled && !crate::native::sandboxed(),Ordering::Relaxed);
        watch.file_events.store(config.file_events,Ordering::Relaxed);
        let cached=db.query_row("SELECT timestamp,total_bytes,available_bytes FROM disk_samples ORDER BY id DESC LIMIT 1",[],|row|Ok(json!({"ready":true,"timestamp":row.get::<_,u64>(0)?,"totalBytes":row.get::<_,u64>(1)?,"availableBytes":row.get::<_,u64>(2)?,"cpuPercent":null,"cached":true}))).unwrap_or(json!({"ready":false}));
        let monitor = Arc::new(Self { detector:Mutex::new(Detector::default()), config: Mutex::new(config), db: Mutex::new(db), watch: watch.clone(), status: Mutex::new(cached), folder, publisher:Mutex::new(None) });
        let (sender,receiver) = mpsc::sync_channel(10000);
        fswatch::start("/System/Volumes/Data".into(),sender,watch);
        let worker=monitor.clone(); std::thread::spawn(move || worker.worker(receiver));
        Ok(monitor)
    }
    pub fn configure(&self, config: Config) -> Result<(),String> {
        if ![5,15].contains(&config.interval_seconds) { return Err("Choose 5 or 15 second sampling".into()); }
        config.alerts.validate()?;
        let temp=self.folder.join("monitor.tmp");
        fs::write(&temp,serde_json::to_vec(&config).map_err(|e|e.to_string())?).map_err(|e|e.to_string())?;
        fs::rename(temp,self.folder.join("monitor.json")).map_err(|e|e.to_string())?;
        self.watch.enabled.store(config.enabled && !crate::native::sandboxed(),Ordering::Relaxed);
        self.watch.file_events.store(config.file_events,Ordering::Relaxed);
        *self.config.lock().map_err(|_|"Monitor preferences unavailable")?=config;
        if let Ok(mut detector)=self.detector.lock() { detector.reset(); }
        if let Ok(db)=self.db.lock(){
            let mut event=LogEvent::new("monitor_config",String::new(),"Breathing Room".into(),"Monitoring".into(),"User monitoring preferences");
            event.detail="Monitoring settings changed; pauses and stream restarts can leave observation gaps".into();
            let _=insert(&db,&event);
        }
        self.publish();Ok(())
    }
    pub fn set_publisher(&self,publisher:Arc<dyn Fn(Value)+Send+Sync>){if let Ok(mut slot)=self.publisher.lock(){*slot=Some(publisher);}}
    fn publish(&self){let publisher=self.publisher.lock().ok().and_then(|slot|slot.clone());if let Some(publisher)=publisher{publisher(self.live());}}
    pub fn apps(&self)->Result<Value,String>{
        let enabled=self.config.lock().map_err(|_|"Monitor configuration unavailable")?.enabled;
        if enabled{if let Some(groups)=self.status.lock().map_err(|_|"Metrics cache unavailable")?.get("appGroups").filter(|v|v.is_array()).cloned(){return Ok(groups);}}
        // Bootstrap once; subsequent reads reuse the monitor's interval sample.
        let groups=processes::groups()?;let mut value=json!(groups);
        if let Some(groups)=value.as_array_mut(){for group in groups{group["cpuAvailable"]=json!(false);}}
        if let Ok(mut status)=self.status.lock(){if enabled&&status["appGroups"].is_array(){return Ok(status["appGroups"].clone());}status["appCount"]=json!(groups.len());status["processCount"]=json!(groups.iter().map(|g|g.processes.len()).sum::<usize>());status["appGroups"]=value.clone();}
        self.publish();Ok(value)
    }
    pub fn refresh_disk(&self){
        let Some((total,available))=disk()else{return;};
        let changed=if let Ok(mut status)=self.status.lock(){let changed=status["totalBytes"]!=json!(total)||status["availableBytes"]!=json!(available);status["totalBytes"]=json!(total);status["availableBytes"]=json!(available);status["diskTimestamp"]=json!(now());status["ready"]=json!(true);changed}else{false};
        if changed{self.publish();}
    }
    pub fn live(&self) -> Value {
        let mut value=self.status.lock().map(|v|v.clone()).unwrap_or(json!({"ready":false}));
        let config=self.config.lock().map(|c|c.clone()).unwrap_or_default();
        if !config.enabled {
            value["topCpuApps"]=json!([]); value["topWriters"]=json!([]);
            value["cpuPercent"]=Value::Null;value["readBytesPerSecond"]=Value::Null;value["writeBytesPerSecond"]=Value::Null;
            value["memoryUsedBytes"]=Value::Null;value["memoryTotalBytes"]=Value::Null;
            value["minute"]=json!({"appsStarted":0,"processesStarted":0,"filesCreated":0,"fileChanges":0,"foldersCreated":0});
            if let Some(groups)=value["appGroups"].as_array_mut(){for group in groups{group["cpuAvailable"]=json!(false);}}
        }
        value["anomalies"]=json!(self.detector.lock().map(|mut d|{d.expire_stale(now(),config.interval_seconds);d.active()}).unwrap_or_default());
        value["config"]=serde_json::to_value(config).unwrap();
        value["watching"]=json!(self.watch.running.load(Ordering::Relaxed));
        value["dropped"]=json!(self.watch.dropped.load(Ordering::Relaxed));
        value["watchError"]=json!(self.watch.error.lock().map(|v|v.clone()).unwrap_or_default());
        value["databasePath"]=json!(self.folder.join("activity.sqlite"));
        value
    }
    pub fn history(&self, filter: &str, search: &str, before: i64) -> Result<Value,String> {
        let db=self.db.lock().map_err(|_|"Activity database unavailable")?;
        let mut stmt=db.prepare("SELECT id,timestamp,kind,path,owner,workflow,attribution,pid,flags,size_bytes,delta_bytes,read_bytes,write_bytes,detail FROM events WHERE (?1='all' OR (?1='files' AND kind IN ('file_created','file_changed','folder_created','removed','renamed','metadata_changed','coverage_gap')) OR (?1='processes' AND kind IN ('process_started','process_exited','app_started','process_io'))) AND (?2='' OR instr(lower(path||' '||owner||' '||workflow),lower(?2))>0) AND (?3=0 OR id<?3) ORDER BY id DESC LIMIT 100").map_err(|e|e.to_string())?;
        let rows=stmt.query_map(params![filter,search,before],|r| Ok(json!({"id":r.get::<_,i64>(0)?,"timestamp":r.get::<_,u64>(1)?,"kind":r.get::<_,String>(2)?,"path":r.get::<_,String>(3)?,"owner":r.get::<_,String>(4)?,"workflow":r.get::<_,String>(5)?,"attribution":r.get::<_,String>(6)?,"pid":r.get::<_,Option<i32>>(7)?,"flags":r.get::<_,u32>(8)?,"sizeBytes":r.get::<_,Option<u64>>(9)?,"deltaBytes":r.get::<_,Option<i64>>(10)?,"readBytes":r.get::<_,u64>(11)?,"writeBytes":r.get::<_,u64>(12)?,"detail":r.get::<_,String>(13)?}))).map_err(|e|e.to_string())?;
        let events:Vec<Value>=rows.collect::<Result<_,_>>().map_err(|e|e.to_string())?;
        let growth=query_groups(&db,"SELECT owner,workflow,SUM(CASE WHEN delta_bytes>0 THEN delta_bytes ELSE 0 END),COUNT(*),MAX(path) FROM events WHERE timestamp>=?1 AND kind IN ('file_created','file_changed') GROUP BY owner,workflow HAVING SUM(CASE WHEN delta_bytes>0 THEN delta_bytes ELSE 0 END)>0 ORDER BY 3 DESC LIMIT 12", now().saturating_sub(86400))?;
        let writers=query_groups(&db,"SELECT owner,'Observed process I/O',SUM(write_bytes),COUNT(*),MAX(path) FROM events WHERE timestamp>=?1 AND kind='process_io' GROUP BY owner HAVING SUM(write_bytes)>0 ORDER BY 3 DESC LIMIT 8",now().saturating_sub(3600))?;
        let count: i64=db.query_row("SELECT COUNT(*) FROM events",[],|r|r.get(0)).map_err(|e|e.to_string())?;
        let mut samples_stmt=db.prepare("SELECT timestamp,total_bytes,available_bytes,cpu_percent FROM disk_samples ORDER BY id DESC LIMIT 720").map_err(|e|e.to_string())?;
        let mut samples:Vec<Value>=samples_stmt.query_map([],|r|Ok(json!({"timestamp":r.get::<_,u64>(0)?,"totalBytes":r.get::<_,u64>(1)?,"availableBytes":r.get::<_,u64>(2)?,"cpuPercent":r.get::<_,Option<f64>>(3)?}))).map_err(|e|e.to_string())?.collect::<Result<_,_>>().map_err(|e|e.to_string())?;
        samples.reverse();
        Ok(json!({"events":events,"growth":growth,"writers":writers,"diskHistory":samples,"storedEvents":count,"retentionDays":7}))
    }
    fn worker(self: Arc<Self>,receiver:mpsc::Receiver<Change>) {
        let home=system::user_home().unwrap_or_default();
        let mut previous=HashMap::new(); let mut seeded=false;
        let mut old_io:HashMap<i32,(u64,u64,u64)>=HashMap::new();
        let mut last=Instant::now(); let mut prune=Instant::now(); let mut old_free=None;
        let mut old_dropped=0; let mut history:Vec<Value>=vec![];
        let mut own_cpu=cpu_time(); let mut old_cpu:HashMap<String,u64>=HashMap::new();
        loop {
            let config=self.config.lock().map(|c|c.clone()).unwrap_or_default();
            if !config.enabled {
                if let Ok(mut detector)=self.detector.lock() {detector.reset();}
                while receiver.try_recv().is_ok() {}
                previous.clear(); seeded=false; old_io.clear(); old_cpu.clear(); last=Instant::now(); own_cpu=cpu_time();
                std::thread::sleep(Duration::from_millis(500)); continue;
            }
            std::thread::sleep(Duration::from_secs(config.interval_seconds));
            if !self.config.lock().map(|c|c.enabled).unwrap_or(false) { continue; }
            let tick=Instant::now(); let seconds=last.elapsed().as_secs_f64().max(1.0); last=tick;
            let mut pending:BTreeMap<String,Change>=BTreeMap::new();
            for _ in 0..10000 {
                let Ok(change)=receiver.try_recv() else { break; };
                pending.entry(change.path.clone()).and_modify(|old|{old.flags|=change.flags; old.at=change.at; old.event_id=change.event_id;}).or_insert(change);
            }
            let mut events=vec![];
            if pending.len()>500 { self.watch.dropped.fetch_add((pending.len()-500) as u64,Ordering::Relaxed); }
            let changes=fair_changes(pending,500);
            let dropped=self.watch.dropped.load(Ordering::Relaxed);
            if dropped>old_dropped {
                let mut event=LogEvent::new("coverage_gap","/System/Volumes/Data".into(),"Monitor".into(),"Coverage".into(),"Bounded queue overflow");
                event.detail=format!("{} notifications omitted under load; disk coverage requires a new scan",dropped-old_dropped); events.push(event); old_dropped=dropped;
            }
            let sampled=processes::sample();
            let process_error=sampled.as_ref().err().cloned().unwrap_or_default();
            if sampled.is_err() {old_cpu.clear();old_io.clear();}
            let mut cpu=None; let mut process_count=previous.len(); let mut app_count=0;let mut app_groups=Value::Null;
            let mut read=0u64; let mut write=0u64; let mut sampled_io=0usize; let mut top_writers=vec![]; let mut top_cpu=vec![]; let mut alert_values=vec![];
            if let Ok(processes)=sampled {
                let mut current:HashMap<_,_>=processes.into_iter().filter(|p|p.pid!=std::process::id() as i32 && !(p.parent_pid==std::process::id() as i32 && p.name=="ps")).map(|p|(identity(&p),p)).collect();
                let counters:HashMap<_,_>=current.values().filter_map(|p|io_counters(p.pid).map(|u|(p.pid,u))).collect();
                let mut next_cpu=HashMap::new(); let mut cpu_pids=std::collections::HashSet::new();
                for (id,p) in current.iter_mut() {
                    p.cpu=0.0;
                    if let Some(u)=counters.get(&p.pid) {
                        if seconds <= (config.interval_seconds*2+2) as f64 {
                            if let Some(old)=old_cpu.get(id) { if u.4>=*old {p.cpu=(u.4-*old) as f64/1e9/seconds*100.0; cpu_pids.insert(p.pid);} }
                        }
                        next_cpu.insert(id.clone(),u.4);
                    }
                }
                old_cpu=next_cpu;
                process_count=current.len();
                let cores=std::thread::available_parallelism().map(|n|n.get()).unwrap_or(1) as f64;
                cpu=if cpu_pids.is_empty(){None}else{Some((current.values().map(|p|p.cpu).sum::<f64>()/cores).min(100.0))};
                let groups=processes::group_samples(current.values().cloned().collect());
                app_count=groups.len();
                app_groups=json!(groups);
                if let Some(groups)=app_groups.as_array_mut(){for group in groups{let available=group["processes"].as_array().is_some_and(|ps|ps.iter().any(|p|p["pid"].as_i64().is_some_and(|pid|cpu_pids.contains(&(pid as i32)))));group["cpuAvailable"]=json!(available);if let Some(ps)=group["processes"].as_array_mut(){for p in ps{p["cpuAvailable"]=json!(p["pid"].as_i64().is_some_and(|pid|cpu_pids.contains(&(pid as i32))));}}}}
                let mut owners=HashMap::new();
                for group in groups {
                    let path=group.bundle_path.clone().unwrap_or_else(||group.id.clone());
                    for process in &group.processes {owners.insert(process.pid,(group.name.clone(),path.clone()));}
                    // Background processes include their start identity to avoid PID reuse sustaining an episode.
                    let id=if group.bundle_path.is_some() {group.id.clone()} else {format!("{}:{}",group.id,group.processes.first().map(|p|p.started.as_str()).unwrap_or(""))};
                    if group.processes.iter().any(|p|cpu_pids.contains(&p.pid)) {
                        alert_values.push((id,group.name.clone(),path.clone(),"cpu".into(),group.cpu));
                        top_cpu.push(json!({"name":group.name,"path":path,"cpu":group.cpu}));
                    }
                }
                top_cpu.sort_by(|a,b|b["cpu"].as_f64().unwrap_or(0.0).total_cmp(&a["cpu"].as_f64().unwrap_or(0.0))); top_cpu.truncate(5);
                events.extend(process_transitions(&previous,&current,seeded));
                if config.process_io {
                    let mut next_io=HashMap::new(); let mut grouped:HashMap<String,(String,u64,u64)>=HashMap::new();
                    for p in current.values() {
                        if let Some(&(started,r,w,_,_))=counters.get(&p.pid) {
                            sampled_io+=1;
                            if let Some((old_start,old_r,old_w))=old_io.get(&p.pid) {
                                if *old_start==started && seconds <= (config.interval_seconds*2+2) as f64 {
                                    let dr=r.saturating_sub(*old_r); let dw=w.saturating_sub(*old_w); read+=dr; write+=dw;
                                    let (name,path)=owners.get(&p.pid).cloned().unwrap_or_else(||app(p));
                                    let path=if path.starts_with("background:"){format!("{path}:{started}")}else{path};
                                    let g=grouped.entry(path).or_insert((name,0,0));g.1+=dr;g.2+=dw;
                                }
                            }
                            next_io.insert(p.pid,(started,r,w));
                        }
                    }
                    old_io=next_io;
                    for (path,(name,r,w)) in grouped {
                        alert_values.push((path.clone(),name.clone(),path.clone(),"writes".into(),w as f64/seconds));
                        if w>0 { top_writers.push(json!({"name":name,"path":path,"bytesPerSecond":w as f64/seconds})); }
                        if r>0 || w>0 {let mut e=LogEvent::new("process_io",path,name,"Process I/O".into(),"Observed cumulative counter delta · not file attribution");e.read_bytes=r;e.write_bytes=w;events.push(e);}
                    }
                    top_writers.sort_by(|a,b|b["bytesPerSecond"].as_f64().unwrap_or(0.0).total_cmp(&a["bytesPerSecond"].as_f64().unwrap_or(0.0)));top_writers.truncate(5);
                } else { old_io.clear(); }
                previous=current; seeded=true;
            }
            if app_groups.is_null(){app_groups=json!(processes::groups().unwrap_or_default());if let Some(groups)=app_groups.as_array_mut(){app_count=groups.len();for group in groups{group["cpuAvailable"]=json!(false);}}}
            if let Ok(mut detector)=self.detector.lock() {detector.sample(now(),config.interval_seconds,&config.alerts,alert_values);}
            let mut db_error=String::new(); let (total,free)=disk().unwrap_or_else(||self.status.lock().map(|s|(s["totalBytes"].as_u64().unwrap_or(0),s["availableBytes"].as_u64().unwrap_or(0))).unwrap_or((0,0)));
            let free_change=old_free.map(|f:u64|free as i64-f as i64);old_free=Some(free);
            let mut minute=json!({"appsStarted":0,"processesStarted":0,"filesCreated":0,"fileChanges":0,"foldersCreated":0});
            if let Ok(mut db)=self.db.lock() {
                let result=(|| -> rusqlite::Result<()> {
                    let tx=db.transaction()?;
                    for change in &changes {
                        if let Ok(event)=reconcile(&tx,change,&home) { events.push(event); }
                    }
                    for event in events.iter().take(1200) { insert(&tx,event)?; }
                    tx.execute("INSERT INTO disk_samples(timestamp,total_bytes,available_bytes,cpu_percent,read_bytes,write_bytes,sample_ms) VALUES(?1,?2,?3,?4,?5,?6,?7)",params![now(),total,free,cpu,read,write,tick.elapsed().as_secs_f64()*1000.0])?;
                    if prune.elapsed()>Duration::from_secs(60) { retention(&tx)?; prune=Instant::now(); }
                    tx.commit()?;
                    let mut stmt=db.prepare("SELECT kind,COUNT(*) FROM events WHERE timestamp>=?1 GROUP BY kind")?;
                    let counts=stmt.query_map([now().saturating_sub(60)],|r|Ok((r.get::<_,String>(0)?,r.get::<_,u64>(1)?)))?;
                    for count in counts { let (kind,n)=count?; let key=match kind.as_str(){"app_started"=>"appsStarted","process_started"=>"processesStarted","file_created"=>"filesCreated","file_changed"=>"fileChanges","folder_created"=>"foldersCreated",_=>continue};minute[key]=json!(n); }
                    Ok(())
                })();
                if let Err(e)=result {db_error=e.to_string();}
            }
            let new_cpu=cpu_time(); let overhead=(new_cpu-own_cpu).max(0.0)/seconds*100.0;own_cpu=new_cpu;
            let memory=io_counters(std::process::id() as i32).map(|u|u.3);
            let ram=system_memory();
            history.push(json!({"timestamp":now(),"availableBytes":free,"cpuPercent":cpu,"memoryPercent":ram.map(|(total,used)|100.0*used as f64/total as f64),"writeBytesPerSecond":write as f64/seconds}));if history.len()>60 {history.remove(0);}
            if let Ok(mut status)=self.status.lock(){ *status=json!({"ready":total>0,"timestamp":now(),"diskTimestamp":now(),"totalBytes":total,"availableBytes":free,"freeChangeBytes":free_change,
                "cpuPercent":cpu,"coreCount":std::thread::available_parallelism().map(|n|n.get()).unwrap_or(1),"appGroups":app_groups,"processCount":process_count,"appCount":app_count,"readBytesPerSecond":if sampled_io>0{Some(read as f64/seconds)}else{None},"writeBytesPerSecond":if sampled_io>0{Some(write as f64/seconds)}else{None},
                "sampledIoProcesses":sampled_io,"minute":minute,"history":history,"topWriters":top_writers,"topCpuApps":top_cpu,"monitorCpuPercent":overhead,"monitorMemoryBytes":memory,"memoryTotalBytes":ram.map(|r|r.0),"memoryUsedBytes":ram.map(|r|r.1),"sampleMs":tick.elapsed().as_secs_f64()*1000.0,
                 "processError":process_error,"databaseError":db_error,"coverage":"FSEvents changes; sampled process starts/I/O; protected paths may be absent. No per-file writer PID or read tracing."}); }
            self.publish();
        }
    }
}
fn query_groups(db:&Connection,sql:&str,since:u64)->Result<Vec<Value>,String>{
    let mut stmt=db.prepare(sql).map_err(|e|e.to_string())?;
    let result=stmt.query_map([since],|r|Ok(json!({"owner":r.get::<_,String>(0)?,"workflow":r.get::<_,String>(1)?,"bytes":r.get::<_,u64>(2)?,"events":r.get::<_,u64>(3)?,"path":r.get::<_,String>(4)?}))).map_err(|e|e.to_string())?;
    result.collect::<Result<Vec<_>,_>>().map_err(|e|e.to_string())
}
fn cpu_time()->f64 {
    let mut r:libc::rusage=unsafe{std::mem::zeroed()};unsafe{libc::getrusage(libc::RUSAGE_SELF,&mut r);}
    r.ru_utime.tv_sec as f64+r.ru_stime.tv_sec as f64+(r.ru_utime.tv_usec+r.ru_stime.tv_usec) as f64/1e6
}

pub fn diagnostic() -> Result<Value,String> {
    let monitor=Monitor::start()?;
    if !monitor.config.lock().map_err(|_|"Settings unavailable")?.enabled { return Err("Monitoring is paused; enable it in Activity before running this check".into()); }
    std::thread::sleep(Duration::from_secs(6));
    let root=std::env::temp_dir().join(format!("breathing-live-check-{}",std::process::id()));
    let script="import os,sys,time; p=sys.argv[1]; os.mkdir(p); f=open(p+'/generated-test.bin','wb'); f.write(b'x'*1048576); f.flush(); os.fsync(f.fileno()); time.sleep(7); f.write(b'x'*1048576); f.flush(); os.fsync(f.fileno()); f.close()";
    let child=std::process::Command::new("/usr/bin/python3").args(["-c",script]).arg(&root).status().map_err(|e|e.to_string())?;
    if !child.success(){return Err("Owned fixture could not run".into());}
    std::thread::sleep(Duration::from_secs(6));
    let canonical=root.canonicalize().map_err(|e|e.to_string())?;
    let log=monitor.history("files",canonical.to_str().unwrap_or("breathing-live-check"),0)?;
        let live=monitor.live();
    monitor.watch.shutdown.store(true,Ordering::Relaxed);monitor.watch.enabled.store(false,Ordering::Relaxed);
    fs::remove_dir_all(&root).map_err(|e|e.to_string())?;
    Ok(json!({"watching":live["watching"],"fixtureEvents":log["events"],"sampledIoProcesses":live["sampledIoProcesses"],"processCount":live["processCount"],
        "monitorCpuPercent":live["monitorCpuPercent"],"monitorMemoryBytes":live["monitorMemoryBytes"],"sampleMs":live["sampleMs"],"dropped":live["dropped"],"databaseError":live["databaseError"],"watchError":live["watchError"]}))
}

#[cfg(test)]
mod tests {
    #[test]
    fn physical_memory_accounting_excludes_reclaimable_cache_and_bounds_usage(){
        assert_eq!(super::memory_used(16000,100,80,10,20,10),Some(10000));
        assert_eq!(super::memory_used(16000,100,0,10,20,10),Some(3000));
        assert_eq!(super::memory_used(16000,100,1000,0,20,10),Some(16000));
        assert_eq!(super::memory_used(0,100,80,0,0,0),None);
        assert_eq!(super::memory_used(16000,100,u64::MAX,0,1,0),None);
    }
    #[test]
    fn native_ram_sample_uses_physical_memory_not_process_rss(){
        let(total,used)=super::system_memory().expect("Native VM counters should be available on the development Mac");assert!(total>0);assert!(used>0&&used<=total);
    }
    #[test]
    fn app_reads_and_published_cpu_share_one_cached_sample() {
        use super::*;
        let monitor=Monitor{detector:Mutex::new(Detector::default()),config:Mutex::new(Config::default()),db:Mutex::new(Connection::open_in_memory().unwrap()),watch:Arc::new(WatchState::default()),folder:PathBuf::new(),publisher:Mutex::new(None),status:Mutex::new(json!({"ready":true,"timestamp":10,"cpuPercent":10.0,"coreCount":8,"appGroups":[{"id":"fixture","cpu":80.0,"cpuAvailable":true}]}))};
        assert_eq!(monitor.apps().unwrap(),monitor.live()["appGroups"]);
        let received=Arc::new(Mutex::new(Value::Null));let sink=received.clone();
        monitor.set_publisher(Arc::new(move|snapshot|{*sink.lock().unwrap()=snapshot;}));monitor.publish();
        assert_eq!(received.lock().unwrap()["cpuPercent"],10.0);
        assert_eq!(received.lock().unwrap()["appGroups"][0]["cpu"],80.0);
        monitor.config.lock().unwrap().enabled=false;
        let paused=monitor.live();assert!(paused["cpuPercent"].is_null());assert_eq!(paused["appGroups"][0]["cpuAvailable"],false);
        assert_eq!(monitor.status.lock().unwrap()["appGroups"][0]["cpuAvailable"],true);
    }
    #[test]
    fn older_monitor_preferences_keep_their_values_and_gain_alert_defaults() {
        let config:super::Config=serde_json::from_str(r#"{"enabled":false,"fileEvents":false,"processIo":false,"intervalSeconds":15}"#).unwrap();
        assert!(!config.enabled);assert_eq!(config.interval_seconds,15);
        assert_eq!(config.alerts,crate::anomalies::AlertConfig::default());
    }
    #[test]
    fn native_cpu_counter_is_monotonic_nanoseconds() {
        let before=super::io_counters(std::process::id() as i32).unwrap();
        let mut value=1u64;
        // Accumulate real CPU work, allowing for fast CPUs and delayed kernel
        // accounting. A single fixed batch is not guaranteed to consume 1 ms.
        let deadline=std::time::Instant::now()+std::time::Duration::from_secs(1);
        let after=loop {
            for _ in 0..2_000_000 {value=std::hint::black_box(value.wrapping_mul(31).wrapping_add(1));}
            std::thread::sleep(std::time::Duration::from_millis(10));
            let sample=super::io_counters(std::process::id() as i32).unwrap();
            if sample.4>before.4+1_000_000||std::time::Instant::now()>=deadline {break sample;}
        };
        assert_eq!(before.0,after.0);assert!(after.4>before.4+1_000_000,"CPU counter did not advance: before={}, after={}",before.4,after.4);assert!(after.3>0);
    }
    use super::*;
    #[test]
    fn flags_are_observations_not_writer_claims(){assert_eq!(event_kind(0x100|0x20000),"folder_created");assert_eq!(event_kind(0x1000),"file_changed");assert_eq!(event_kind(0x3),"coverage_gap");}
    #[test]
    fn path_attribution_preserves_workflow_and_unknown_writer(){let home=Path::new("/Users/test");assert_eq!(attribution("/Users/test/code/site/.next/cache/x",home),("Project tools".into(),"code/site".into()));assert_eq!(attribution("/Users/test/.npm/blob",home).0,"npm");assert_eq!(normalized_path("/System/Volumes/Data/Users/test/code"),"/Users/test/code");}
    #[test]
    fn sqlite_first_observation_is_unknown_then_tracks_real_growth_and_removal(){
        let db=Connection::open_in_memory().unwrap();initialize(&db).unwrap();
        let root=std::env::temp_dir().join(format!("breathing-monitor-{}-{}",std::process::id(),now()));fs::create_dir_all(&root).unwrap();let path=root.join("fixture");fs::write(&path,vec![1u8;4096]).unwrap();
        let change=Change{path:path.to_string_lossy().into_owned(),flags:0x1000,event_id:1,at:now()};
        let first=reconcile(&db,&change,&root).unwrap();assert!(first.delta_bytes.is_none());insert(&db,&first).unwrap();
        fs::write(&path,vec![1u8;131072]).unwrap();let growth=reconcile(&db,&change,&root).unwrap();assert!(growth.delta_bytes.unwrap()>0);
        fs::remove_file(&path).unwrap();let removed=reconcile(&db,&Change{flags:0x200,..change},&root).unwrap();assert!(removed.delta_bytes.unwrap()<0);fs::remove_dir(&root).unwrap();
    }
    #[test]
    fn process_baseline_does_not_report_all_apps_as_new(){
        let p=processes::parse_line("123 1 501 0 100 Fri Oct 2 09:00:00 2026 /Applications/Test.app/Contents/MacOS/Test",501).unwrap();let current=HashMap::from([(identity(&p),p)]);
        assert!(process_transitions(&HashMap::new(),&current,false).is_empty());let transitions=process_transitions(&HashMap::new(),&current,true);assert_eq!(transitions.iter().filter(|e|e.kind=="app_started").count(),1);
    }
    #[test]
    fn build_burst_cannot_starve_unrelated_folder_events(){
        let mut pending=BTreeMap::new();
        for i in 0..1000 { let path=format!("/a/build/{i}");pending.insert(path.clone(),Change{path,flags:0x100,event_id:i,at:now()}); }
        let path="/z/other/important".to_string();pending.insert(path.clone(),Change{path:path.clone(),flags:0x100,event_id:1001,at:now()});
        assert!(fair_changes(pending,10).iter().any(|c|c.path==path));
    }
    #[test]
    fn retention_removes_old_events_without_erasing_current_observations(){
        let db=Connection::open_in_memory().unwrap();initialize(&db).unwrap();
        let mut old=LogEvent::new("file_changed","/fixture/old".into(),"Tool".into(),"Project".into(),"Observed");old.timestamp=now()-8*86400;
        let new=LogEvent::new("file_changed","/fixture/current".into(),"Tool".into(),"Project".into(),"Observed");insert(&db,&old).unwrap();insert(&db,&new).unwrap();retention(&db).unwrap();
        let count:u64=db.query_row("SELECT COUNT(*) FROM events",[],|r|r.get(0)).unwrap();assert_eq!(count,1);
        let path:String=db.query_row("SELECT path FROM events",[],|r|r.get(0)).unwrap();assert_eq!(path,"/fixture/current");
    }
}
