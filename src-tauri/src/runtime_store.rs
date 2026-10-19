//! Native, private SQLite journal/cache and origin-scoped application sessions.
use crate::model::now;
use rusqlite::{params, Connection, OptionalExtension};
use serde_json::{json, Value};
use std::{fs, os::unix::fs::{MetadataExt, PermissionsExt}, path::{Path,PathBuf}, time::Duration};

pub(crate) fn path(home:&Path)->PathBuf { home.join("Library/Application Support/app.breathingroom.mac/agent-runtime.sqlite") }
pub(crate) fn open(home:&Path)->Result<Connection,String>{
    let file=path(home);let folder=file.parent().unwrap();
    fs::create_dir_all(folder).map_err(|e|e.to_string())?;
    if fs::canonicalize(folder).map_err(|e|e.to_string())?!=folder{return Err("Runtime storage contains a symlink".into());}
    fs::set_permissions(folder,fs::Permissions::from_mode(0o700)).map_err(|e|e.to_string())?;
    if let Ok(meta)=fs::symlink_metadata(&file){if meta.file_type().is_symlink()||meta.uid()!=unsafe{libc::getuid()}{return Err("Invalid runtime database".into());}}
    let db=Connection::open(&file).map_err(|e|e.to_string())?;
    fs::set_permissions(&file,fs::Permissions::from_mode(0o600)).map_err(|e|e.to_string())?;
    db.busy_timeout(Duration::from_secs(5)).map_err(|e|e.to_string())?;
    db.execute_batch("PRAGMA journal_mode=WAL; PRAGMA foreign_keys=ON;
      CREATE TABLE IF NOT EXISTS agent_runs(id TEXT PRIMARY KEY,payload TEXT NOT NULL,owner_pid INTEGER NOT NULL,updated_at INTEGER NOT NULL);
      CREATE TABLE IF NOT EXISTS agent_steps(run_id TEXT NOT NULL,step INTEGER NOT NULL,input_hash TEXT NOT NULL,reply TEXT NOT NULL,PRIMARY KEY(run_id,step));
      CREATE TABLE IF NOT EXISTS tool_results(run_id TEXT NOT NULL,call_id TEXT NOT NULL,input_hash TEXT NOT NULL,payload TEXT NOT NULL,PRIMARY KEY(run_id,call_id));
      CREATE TABLE IF NOT EXISTS cache_entries(key TEXT PRIMARY KEY,payload TEXT NOT NULL,updated_at INTEGER NOT NULL,expires_at INTEGER);
      CREATE TABLE IF NOT EXISTS usage_events(id TEXT PRIMARY KEY,run_id TEXT NOT NULL,model TEXT NOT NULL,prompt_tokens INTEGER,completion_tokens INTEGER,neuron_estimate REAL,payload TEXT NOT NULL,created_at INTEGER NOT NULL);
      CREATE TABLE IF NOT EXISTS account_snapshots(subject TEXT PRIMARY KEY,payload TEXT NOT NULL,updated_at INTEGER NOT NULL);
      CREATE TABLE IF NOT EXISTS auth_sessions(origin TEXT PRIMARY KEY,payload TEXT NOT NULL,updated_at INTEGER NOT NULL);
      CREATE TABLE IF NOT EXISTS sync_outbox(id TEXT PRIMARY KEY,kind TEXT NOT NULL,payload TEXT NOT NULL,created_at INTEGER NOT NULL,synced_at INTEGER);
      CREATE TABLE IF NOT EXISTS discovery_scans(id TEXT PRIMARY KEY,payload TEXT NOT NULL,updated_at INTEGER NOT NULL);
      CREATE TABLE IF NOT EXISTS discovery_pending(scan_id TEXT NOT NULL,path TEXT NOT NULL,after_name TEXT,device INTEGER NOT NULL,PRIMARY KEY(scan_id,path));
      CREATE TABLE IF NOT EXISTS discovery_inventory(scan_id TEXT NOT NULL,path TEXT NOT NULL,parent TEXT NOT NULL,kind TEXT NOT NULL,category TEXT NOT NULL,bytes INTEGER NOT NULL,logical_bytes INTEGER NOT NULL,modified_at INTEGER NOT NULL,device INTEGER NOT NULL,inode INTEGER NOT NULL,owned INTEGER NOT NULL,state TEXT NOT NULL,PRIMARY KEY(scan_id,path));
      CREATE INDEX IF NOT EXISTS discovery_inventory_size ON discovery_inventory(scan_id,bytes DESC,path);
      CREATE TABLE IF NOT EXISTS discovery_rules(id TEXT PRIMARY KEY,payload TEXT NOT NULL,enabled INTEGER NOT NULL DEFAULT 1,updated_at INTEGER NOT NULL);
      CREATE TABLE IF NOT EXISTS cleanup_approvals(account TEXT NOT NULL,origin TEXT NOT NULL,action_key TEXT NOT NULL,payload TEXT NOT NULL,enabled INTEGER NOT NULL DEFAULT 1,approved_at INTEGER NOT NULL,PRIMARY KEY(account,origin,action_key));
      CREATE TABLE IF NOT EXISTS daily_notifications(run_id TEXT PRIMARY KEY,account TEXT NOT NULL,origin TEXT NOT NULL,payload TEXT NOT NULL,seen INTEGER NOT NULL DEFAULT 0,updated_at INTEGER NOT NULL);
      PRAGMA user_version=1;").map_err(|e|e.to_string())?;
    Ok(db)
}
pub(crate) fn auth_load(home:&Path,origin:&str)->Result<Option<Value>,String>{
    let text:Option<String>=open(home)?.query_row("SELECT payload FROM auth_sessions WHERE origin=?",[origin],|row|row.get(0)).optional().map_err(|_|"Could not read the saved app session")?;
    text.map(|text|serde_json::from_str(&text).map_err(|_|"Saved app session is invalid; sign in again".into())).transpose()
}
pub(crate) fn auth_save(home:&Path,origin:&str,value:&Value)->Result<(),String>{
    let text=value.to_string();if text.len()>65536{return Err("App session exceeds its storage limit".into());}
    open(home)?.execute("INSERT INTO auth_sessions VALUES(?,?,?) ON CONFLICT(origin) DO UPDATE SET payload=excluded.payload,updated_at=excluded.updated_at",params![origin,text,now()]).map_err(|_|"Could not save the app session")?;Ok(())
}
pub(crate) fn auth_clear(home:&Path,origin:&str)->Result<(),String>{
    let db=open(home)?;db.execute_batch("PRAGMA secure_delete=ON;").map_err(|_|"Could not clear the app session")?;
    db.execute("DELETE FROM auth_sessions WHERE origin=?",[origin]).map_err(|_|"Could not clear the app session")?;
    let _=db.execute_batch("PRAGMA wal_checkpoint(TRUNCATE);");Ok(())
}
pub(crate) fn cache_get(home:&Path,key:&str)->Result<Option<Value>,String>{
    let db=open(home)?;
    let text:Option<String>=db.query_row("SELECT payload FROM cache_entries WHERE key=? AND (expires_at IS NULL OR expires_at>?)",params![key,now()],|r|r.get(0)).optional().map_err(|e|e.to_string())?;
    Ok(text.and_then(|s|serde_json::from_str(&s).ok()))
}
pub(crate) fn cache_put(home:&Path,key:&str,value:&Value,ttl:Option<u64>)->Result<(),String>{
    let text=value.to_string();if text.len()>32*1024*1024{return Err("Cache entry is too large".into());}
    open(home)?.execute("INSERT INTO cache_entries VALUES(?,?,?,?) ON CONFLICT(key) DO UPDATE SET payload=excluded.payload,updated_at=excluded.updated_at,expires_at=excluded.expires_at",params![key,text,now(),ttl.map(|n|now()+n)]).map_err(|e|e.to_string())?;Ok(())
}
pub(crate) fn save_run(home:&Path,id:&str,value:&Value)->Result<(),String>{
    let text=value.to_string();if text.len()>32*1024*1024{return Err("Run state is too large".into());}
    open(home)?.execute("INSERT INTO agent_runs VALUES(?,?,?,?) ON CONFLICT(id) DO UPDATE SET payload=excluded.payload,updated_at=excluded.updated_at",params![id,text,std::process::id(),now()]).map_err(|e|e.to_string())?;Ok(())
}
pub(crate) fn create_run(home:&Path,id:&str,value:&Value)->Result<(),String>{
    let _update_gate=crate::update_gate::operation()?;
    let mut db=open(home)?;let tx=db.transaction_with_behavior(rusqlite::TransactionBehavior::Immediate).map_err(|e|e.to_string())?;
    require_idle(&tx,id)?;
    tx.execute("INSERT INTO agent_runs VALUES(?,?,?,?)",params![id,value.to_string(),std::process::id(),now()]).map_err(|e|e.to_string())?;tx.commit().map_err(|e|e.to_string())
}
fn require_idle(tx:&rusqlite::Transaction<'_>,id:&str)->Result<(),String>{
    let owners={let mut query=tx.prepare("SELECT owner_pid FROM agent_runs WHERE id<>? AND json_extract(payload,'$.status') IN ('inspecting','executing')").map_err(|e|e.to_string())?;let rows=query.query_map([id],|r|r.get::<_,i32>(0)).map_err(|e|e.to_string())?;rows.collect::<Result<Vec<_>,_>>().map_err(|e|e.to_string())?};
    if owners.into_iter().any(|pid|pid>0&&unsafe{libc::kill(pid,0)}==0){return Err("Your cleanup agent is already running. Review or stop that run before starting another inspection.".into());}Ok(())
}
pub(crate) fn load_run(home:&Path,id:&str)->Result<Option<Value>,String>{
    let text:Option<String>=open(home)?.query_row("SELECT payload FROM agent_runs WHERE id=?",[id],|r|r.get(0)).optional().map_err(|e|e.to_string())?;
    text.map(|s|serde_json::from_str(&s).map_err(|_|"Invalid run state".into())).transpose()
}
pub(crate) fn claim_run(home:&Path,id:&str,value:&Value)->Result<(),String>{
    let _update_gate=crate::update_gate::operation()?;
    let text=value.to_string();if text.len()>32*1024*1024{return Err("Run state is too large".into());}
    let mut db=open(home)?;let tx=db.transaction_with_behavior(rusqlite::TransactionBehavior::Immediate).map_err(|e|e.to_string())?;require_idle(&tx,id)?;
    let changed=tx.execute("UPDATE agent_runs SET owner_pid=?,payload=?,updated_at=? WHERE id=?",params![std::process::id(),text,now(),id]).map_err(|e|e.to_string())?;if changed!=1{return Err("This agent run is no longer available".into());}tx.commit().map_err(|e|e.to_string())
}
pub(crate) fn owner_alive(home:&Path,id:&str)->bool{
    let pid=open(home).ok().and_then(|db|db.query_row("SELECT owner_pid FROM agent_runs WHERE id=?",[id],|r|r.get::<_,i32>(0)).ok());
    pid.is_some_and(|pid|pid>0&&unsafe{libc::kill(pid,0)}==0)
}
pub(crate) fn require_no_active_agent(home:&Path)->Result<(),String>{
    let mut db=open(home)?;let tx=db.transaction_with_behavior(rusqlite::TransactionBehavior::Immediate).map_err(|e|e.to_string())?;require_idle(&tx, "")
}
pub(crate) fn latest(home:&Path)->Result<Option<String>,String>{
    open(home)?.query_row("SELECT id FROM agent_runs WHERE json_extract(payload,'$.model') LIKE '@cf/%' ORDER BY updated_at DESC,rowid DESC LIMIT 1",[],|r|r.get(0)).optional().map_err(|e|e.to_string())
}
pub(crate) fn step(home:&Path,run:&str,index:u64,input:&str)->Result<Option<Value>,String>{
    let row:Option<(String,String)>=open(home)?.query_row("SELECT input_hash,reply FROM agent_steps WHERE run_id=? AND step=?",params![run,index],|r|Ok((r.get(0)?,r.get(1)?))).optional().map_err(|e|e.to_string())?;
    match row{Some((hash,text)) if hash==input=>serde_json::from_str(&text).map(Some).map_err(|_|"Invalid saved step".into()),Some(_)=>Err("Saved step input changed".into()),None=>Ok(None)}
}
pub(crate) fn save_step(home:&Path,run:&str,index:u64,input:&str,reply:&Value)->Result<(),String>{
    let mut db=open(home)?;let tx=db.transaction().map_err(|e|e.to_string())?;
    let existing:Option<(String,String)>=tx.query_row("SELECT input_hash,reply FROM agent_steps WHERE run_id=? AND step=?",params![run,index],|r|Ok((r.get(0)?,r.get(1)?))).optional().map_err(|e|e.to_string())?;
    if let Some((hash,text))=existing{if hash!=input||text!=reply.to_string(){return Err("A completed step cannot be overwritten".into());}return Ok(());}
    tx.execute("INSERT OR IGNORE INTO agent_steps VALUES(?,?,?,?)",params![run,index,input,reply.to_string()]).map_err(|e|e.to_string())?;
    let usage=reply["usage"].clone();let model=reply["model"].as_str().unwrap_or("unknown");
    let prompt=usage["prompt_tokens"].as_u64();let completion=usage["completion_tokens"].as_u64();
    let neurons=if model=="@cf/qwen/qwen3-30b-a3b-fp8"{prompt.zip(completion).map(|(p,c)|p as f64*4625.0/1e6+c as f64*30475.0/1e6)}else{None};
    let event=reply["eventId"].as_str().map(str::to_owned).unwrap_or_else(||format!("{run}:{index}"));
    tx.execute("INSERT OR IGNORE INTO usage_events VALUES(?,?,?,?,?,?,?,?)",params![event,run,model,prompt,completion,neurons,usage.to_string(),now()]).map_err(|e|e.to_string())?;
    tx.execute("INSERT OR IGNORE INTO sync_outbox VALUES(?,'ai_usage',?,?,NULL)",params![event,json!({"model":model,"usage":usage,"neuronEstimate":neurons}).to_string(),now()]).map_err(|e|e.to_string())?;
    tx.commit().map_err(|e|e.to_string())
}
pub(crate) fn tool_result(home:&Path,run:&str,id:&str,input:&str)->Result<Option<Value>,String>{
    let row:Option<(String,String)>=open(home)?.query_row("SELECT input_hash,payload FROM tool_results WHERE run_id=? AND call_id=?",params![run,id],|r|Ok((r.get(0)?,r.get(1)?))).optional().map_err(|e|e.to_string())?;
    match row{Some((hash,text))if hash==input=>serde_json::from_str(&text).map(Some).map_err(|_|"Invalid saved tool result".into()),Some(_)=>Err("Agent reused a tool call ID with different arguments".into()),None=>Ok(None)}
}
pub(crate) fn save_tool(home:&Path,run:&str,id:&str,input:&str,result:&Value)->Result<(),String>{open(home)?.execute("INSERT OR IGNORE INTO tool_results VALUES(?,?,?,?)",params![run,id,input,result.to_string()]).map_err(|e|e.to_string())?;Ok(())}
pub(crate) fn account(home:&Path,value:&Value)->Result<(),String>{
    let subject=value["subject"].as_str().ok_or("Account identity missing")?;
    open(home)?.execute("INSERT INTO account_snapshots VALUES(?,?,?) ON CONFLICT(subject) DO UPDATE SET payload=excluded.payload,updated_at=excluded.updated_at",params![subject,value.to_string(),now()]).map_err(|e|e.to_string())?;Ok(())
}
pub fn stats()->Result<Value,String>{stats_at(&crate::system::user_home()?)}
fn stats_at(home:&Path)->Result<Value,String>{
    let db=open(home)?;
    let (requests,prompt,completion,neurons):(u64,Option<u64>,Option<u64>,Option<f64>)=db.query_row("SELECT COUNT(*),SUM(prompt_tokens),SUM(completion_tokens),SUM(neuron_estimate) FROM usage_events",[],|r|Ok((r.get(0)?,r.get(1)?,r.get(2)?,r.get(3)?))).map_err(|e|e.to_string())?;
    Ok(json!({"requests":requests,"promptTokens":prompt,"completionTokens":completion,"neuronEstimate":neurons,"creditsVerified":false}))
}
#[cfg(test)]mod tests{
    use super::*;
    fn home()->PathBuf{static NEXT:std::sync::atomic::AtomicUsize=std::sync::atomic::AtomicUsize::new(0);fs::canonicalize(std::env::temp_dir()).unwrap().join(format!("br-sqlite-{}-{}-{}",std::process::id(),std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).unwrap().as_nanos(),NEXT.fetch_add(1,std::sync::atomic::Ordering::Relaxed)))}
    #[test]fn journal_and_usage_are_idempotent_and_unknown_usage_stays_unknown(){
        let h=home();let reply=json!({"model":"@cf/qwen/qwen3-30b-a3b-fp8","usage":{},"eventId":"event1"});
        save_step(&h,"run",0,"fingerprint",&reply).unwrap();save_step(&h,"run",0,"fingerprint",&reply).unwrap();
        assert_eq!(step(&h,"run",0,"fingerprint").unwrap(),Some(reply));assert!(step(&h,"run",0,"changed").is_err());
        let stats=stats_at(&h).unwrap();assert_eq!(stats["requests"],1);assert!(stats["neuronEstimate"].is_null());assert!(stats["promptTokens"].is_null());
        fs::remove_dir_all(h).unwrap();
    }
    #[test]fn cache_survives_new_connections_and_never_issues_credit(){let h=home();cache_put(&h,"disk",&json!({"bytes":12}),None).unwrap();assert_eq!(cache_get(&h,"disk").unwrap(),Some(json!({"bytes":12})));assert_eq!(stats_at(&h).unwrap()["creditsVerified"],false);fs::remove_dir_all(h).unwrap();}
    #[test]fn update_idle_check_blocks_active_agents_but_allows_retained_review_plans(){let h=home();save_run(&h,"agent",&json!({"status":"inspecting"})).unwrap();assert!(require_no_active_agent(&h).is_err());save_run(&h,"agent",&json!({"status":"executing"})).unwrap();assert!(require_no_active_agent(&h).is_err());save_run(&h,"agent",&json!({"status":"review"})).unwrap();assert!(require_no_active_agent(&h).is_ok());fs::remove_dir_all(h).unwrap();}
    #[test]fn all_agent_entry_points_share_the_same_active_run_claim(){let h=home();let value=json!({"status":"inspecting","model":"@cf/fixture"});create_run(&h,"manual",&value).unwrap();assert!(create_run(&h,"daily",&value).unwrap_err().contains("already running"));save_run(&h,"manual",&json!({"status":"review"})).unwrap();create_run(&h,"daily",&value).unwrap();assert!(create_run(&h,"another-manual",&value).is_err());fs::remove_dir_all(h).unwrap();}
    #[test]fn resume_claim_is_atomic_and_cannot_overlap_daily_or_manual_runs(){let h=home();save_run(&h,"interrupted",&json!({"status":"failed"})).unwrap();create_run(&h,"daily",&json!({"status":"inspecting"})).unwrap();assert!(claim_run(&h,"interrupted",&json!({"status":"inspecting"})).is_err());assert_eq!(load_run(&h,"interrupted").unwrap().unwrap()["status"],"failed");save_run(&h,"daily",&json!({"status":"done"})).unwrap();claim_run(&h,"interrupted",&json!({"status":"inspecting"})).unwrap();assert!(create_run(&h,"manual",&json!({"status":"inspecting"})).is_err());fs::remove_dir_all(h).unwrap();}
    #[test]fn tool_ids_cannot_be_reused_for_different_inputs(){let h=home();save_tool(&h,"run","call","same",&json!({"bytes":7})).unwrap();assert!(tool_result(&h,"run","call","changed").is_err());fs::remove_dir_all(h).unwrap();}
    #[test]fn app_sessions_persist_are_origin_scoped_and_never_enter_sync(){let h=home();let value=json!({"accessToken":"fixture-only","account":{"subject":"fixture"}});auth_save(&h,"https://one.test",&value).unwrap();assert_eq!(auth_load(&h,"https://one.test").unwrap(),Some(value));assert!(auth_load(&h,"https://two.test").unwrap().is_none());let db=open(&h).unwrap();assert_eq!(db.query_row("SELECT COUNT(*) FROM sync_outbox",[],|row|row.get::<_,i64>(0)).unwrap(),0);drop(db);auth_clear(&h,"https://one.test").unwrap();assert!(auth_load(&h,"https://one.test").unwrap().is_none());fs::remove_dir_all(h).unwrap();}
}
