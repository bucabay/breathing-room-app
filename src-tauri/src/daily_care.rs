//! Daily care is a policy on the shared agent runner, not a discovery/execution engine.
use crate::{cleanup_session::{self as session,Action,Run},model::now,runtime_store as store,remote_agent,system};
use rusqlite::{params,OptionalExtension};
use serde::{Deserialize,Serialize};
use serde_json::json;
use sha2::{Digest,Sha256};
use std::{path::Path,sync::{Arc,OnceLock}};

#[derive(Clone,Serialize,Deserialize)]
#[serde(rename_all="camelCase")]
pub struct Approval{pub key:String,pub action:Action,pub approved_at:u64}
#[derive(Clone,Serialize,Deserialize)]
#[serde(rename_all="camelCase")]
pub struct Notification{pub run_id:String,pub title:String,pub body:String,pub pending_count:usize,pub status:String,pub seen:bool,pub updated_at:u64,pub recovered_bytes:u64,#[serde(default)]pub needs_attention:bool}
type Publisher=Arc<dyn Fn(Notification,bool)+Send+Sync>;
static PUBLISHER:OnceLock<Publisher>=OnceLock::new();
pub fn set_publisher(publisher:Publisher){let _=PUBLISHER.set(publisher);}
fn context(run:&Run)->Result<(&str,&str),String>{Ok((run.account_id.as_deref().ok_or("Approval account missing")?,run.api_origin.as_deref().ok_or("Approval origin missing")?))}
pub(crate) fn key(action:&Action)->String{format!("{:x}",Sha256::digest(json!({"action":session::action_key(action),"nativeRule":action.native_rule}).to_string().as_bytes()))}
fn write_approval(home:&Path,run:&Run,action:&Action,explicit:bool)->Result<(),String>{
    let(account,origin)=context(run)?;let key=key(action);let approval=Approval{key:key.clone(),action:action.clone(),approved_at:now()};
    let sql=if explicit{"INSERT INTO cleanup_approvals VALUES(?,?,?,?,1,?) ON CONFLICT(account,origin,action_key) DO UPDATE SET payload=excluded.payload,enabled=1,approved_at=excluded.approved_at"}else{"INSERT OR IGNORE INTO cleanup_approvals VALUES(?,?,?,?,1,?)"};
    store::open(home)?.execute(sql,params![account,origin,key,serde_json::to_string(&approval).map_err(|e|e.to_string())?,approval.approved_at]).map_err(|e|e.to_string())?;Ok(())
}
pub(crate) fn remember(home:&Path,run:&Run,ids:&[String])->Result<(),String>{
    let(account,origin)=context(run)?;let mut db=store::open(home)?;let tx=db.transaction_with_behavior(rusqlite::TransactionBehavior::Immediate).map_err(|e|e.to_string())?;
    for action in run.actions.iter().filter(|a|ids.contains(&a.id)){
        if !run.verified_actions.contains(&session::action_key(action)){return Err("Only native-verified approvals can be remembered".into());}
        let key=key(action);let approval=Approval{key:key.clone(),action:action.clone(),approved_at:now()};
        tx.execute("INSERT INTO cleanup_approvals VALUES(?,?,?,?,1,?) ON CONFLICT(account,origin,action_key) DO UPDATE SET payload=excluded.payload,enabled=1,approved_at=excluded.approved_at",params![account,origin,key,serde_json::to_string(&approval).map_err(|e|e.to_string())?,approval.approved_at]).map_err(|e|e.to_string())?;
    }tx.commit().map_err(|e|e.to_string())
}
fn import_previous(home:&Path,account:&str,origin:&str)->Result<(),String>{
    let marker=format!("daily-approval-import:{:x}",Sha256::digest(json!([account,origin]).to_string().as_bytes()));
    if store::cache_get(home,&marker)?.is_some(){return Ok(());}
    let db=store::open(home)?;let mut query=db.prepare("SELECT payload FROM agent_runs WHERE json_extract(payload,'$.accountId')=? AND json_extract(payload,'$.apiOrigin')=?").map_err(|e|e.to_string())?;
    let rows=query.query_map(params![account,origin],|r|r.get::<_,String>(0)).map_err(|e|e.to_string())?;
    let runs=rows.collect::<Result<Vec<_>,_>>().map_err(|e|e.to_string())?;drop(query);drop(db);
    for text in runs{let Ok(run)=serde_json::from_str::<Run>(&text)else{continue;};if run.discovery_options.daily_care{continue;}
        for action in &run.actions{if run.approved_ids.contains(&action.id)&&run.verified_actions.contains(&session::action_key(action))&&!(run.automatic_enabled&&run.automatic_ids.contains(&action.id)){write_approval(home,&run,action,false)?;}}
    }
    store::cache_put(home,&marker,&json!({"importedAt":now()}),None)
}
pub(crate) fn allowed(home:&Path,run:&Run,action:&Action)->Result<bool,String>{
    let(account,origin)=context(run)?;let enabled:Option<bool>=store::open(home)?.query_row("SELECT enabled FROM cleanup_approvals WHERE account=? AND origin=? AND action_key=?",params![account,origin,key(action)],|r|r.get(0)).optional().map_err(|e|e.to_string())?;Ok(enabled==Some(true))
}
pub(crate) fn approved_ids(home:&Path,run:&Run)->Result<Vec<String>,String>{
    let(account,origin)=context(run)?;import_previous(home,account,origin)?;
    // Provider failure may leave a native fallback plan, but never authorizes a
    // scheduled mutation. It remains available for explicit user review.
    if run.discovery.as_ref().and_then(|d|d.agent.as_ref()).is_some_and(|a|a.status=="failed")||run.error.is_some(){return Ok(vec![]);}
    let mut ids=vec![];for action in &run.actions{if !run.outcomes.iter().any(|o|o.id==action.id)&&run.verified_actions.contains(&session::action_key(action))&&allowed(home,run,action)?{ids.push(action.id.clone());}}Ok(ids)
}
pub fn approvals()->Result<Vec<Approval>,String>{
    let home=system::user_home()?;let account=remote_agent::local_account_id()?;let origin=remote_agent::base_url()?;import_previous(&home,&account,&origin)?;
    let db=store::open(&home)?;let mut query=db.prepare("SELECT payload FROM cleanup_approvals WHERE account=? AND origin=? AND enabled=1 ORDER BY approved_at DESC").map_err(|e|e.to_string())?;
    let rows=query.query_map(params![account,origin],|r|r.get::<_,String>(0)).map_err(|e|e.to_string())?;rows.map(|r|serde_json::from_str(&r.map_err(|e|e.to_string())?).map_err(|e|e.to_string())).collect()
}
pub fn revoke(key:String)->Result<(),String>{
    let account=remote_agent::local_account_id()?;let origin=remote_agent::base_url()?;store::open(&system::user_home()?)?.execute("UPDATE cleanup_approvals SET enabled=0 WHERE account=? AND origin=? AND action_key=?",params![account,origin,key]).map_err(|e|e.to_string())?;Ok(())
}
pub(crate) fn publish(home:&Path,run:&Run)->Result<(),String>{
    if !run.discovery_options.daily_care||!["review","done","failed","cancelled"].contains(&run.status.as_str()){return Ok(());}
    let(account,origin)=context(run)?;
    let pending=if run.status=="cancelled"{0}else{run.actions.iter().filter(|a|!run.outcomes.iter().any(|o|o.id==a.id)&&!allowed(home,run,a).unwrap_or(false)).count()};
    let failed=run.status!="cancelled"&&(run.status=="failed"||run.error.is_some()||run.discovery.as_ref().and_then(|d|d.agent.as_ref()).is_some_and(|a|a.status=="failed"));
    let title=if run.status=="cancelled"{"Daily care stopped"}else if failed{"Daily care needs your attention"}else if pending>0{"Daily care found locations to clean"}else{"Daily care completed"};
    let body=if run.status=="cancelled"{"You stopped this run. No further cleanup actions will run.".into()}else if failed{"The agent could not complete this run. Open Breathing Room to review retained findings or retry.".into()}else if pending>0{format!("{pending} new locations need your approval. Previously approved locations can be cleaned without another approval. Open Breathing Room to review the exact plan.")}else{"The agent finished checking your Mac using your saved location approvals.".into()};
    let mut notification=Notification{run_id:run.id.clone(),title:title.into(),body,pending_count:pending,status:run.status.clone(),seen:false,updated_at:now(),recovered_bytes:run.recovered_bytes,needs_attention:failed};
    let db=store::open(home)?;let previous:Option<(String,bool)>=db.query_row("SELECT payload,seen FROM daily_notifications WHERE run_id=?",[&run.id],|r|Ok((r.get(0)?,r.get(1)?))).optional().map_err(|e|e.to_string())?;
    let mut notify_system=previous.is_none()&&(pending>0||failed);
    if let Some((text,seen))=&previous{let old:Notification=serde_json::from_str(text).map_err(|e|e.to_string())?;if old.status==notification.status&&old.pending_count==pending&&old.body==notification.body{return Ok(());}let escalated=failed&&!old.needs_attention;notification.seen=*seen&&!escalated;notify_system=escalated;}
    db.execute("INSERT INTO daily_notifications VALUES(?,?,?,?,?,?) ON CONFLICT(run_id) DO UPDATE SET payload=excluded.payload,seen=excluded.seen,updated_at=excluded.updated_at",params![run.id,account,origin,serde_json::to_string(&notification).map_err(|e|e.to_string())?,notification.seen,notification.updated_at]).map_err(|e|e.to_string())?;
    if let Some(publisher)=PUBLISHER.get(){publisher(notification,notify_system);}Ok(())
}
pub fn notifications()->Result<Vec<Notification>,String>{
    let account=match remote_agent::local_account_id(){Ok(account)=>account,Err(_)=>return Ok(vec![])};let origin=remote_agent::base_url()?;
    let db=store::open(&system::user_home()?)?;let mut query=db.prepare("SELECT payload,seen FROM daily_notifications WHERE account=? AND origin=? ORDER BY updated_at DESC LIMIT 25").map_err(|e|e.to_string())?;
    let rows=query.query_map(params![account,origin],|r|Ok((r.get::<_,String>(0)?,r.get::<_,bool>(1)?))).map_err(|e|e.to_string())?;
    rows.map(|row|{let(text,seen)=row.map_err(|e|e.to_string())?;let mut n:Notification=serde_json::from_str(&text).map_err(|e|e.to_string())?;n.seen=seen;Ok(n)}).collect()
}
pub fn mark_seen(id:String)->Result<(),String>{let account=remote_agent::local_account_id()?;let origin=remote_agent::base_url()?;store::open(&system::user_home()?)?.execute("UPDATE daily_notifications SET seen=1 WHERE run_id=? AND account=? AND origin=?",params![id,account,origin]).map_err(|e|e.to_string())?;Ok(())}

#[cfg(test)]mod tests{
    use super::*;use std::fs;
    fn fixture()->(std::path::PathBuf,Run){
        let home=fs::canonicalize(std::env::temp_dir()).unwrap().join(format!("br-daily-fixture-{}-{}",std::process::id(),std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).unwrap().as_nanos()));
        let path=home.join("Library/Caches/known");fs::create_dir_all(&path).unwrap();fs::write(path.join("blob"),b"fixture only").unwrap();
        let action=crate::cleanup_discovery::action("Known fixture",path,vec![],"Fixture only");let mut run=session::fixture_run(&home,action,false);
        run.account_id=Some("fixture-user".into());run.api_origin=Some("https://fixture.test".into());run.discovery_options.daily_care=true;run.verified_actions=run.actions.iter().map(session::action_key).collect();
        store::save_run(&home,&run.id,&json!(run)).unwrap();(home,run)
    }
    #[test]fn approvals_match_exact_method_path_rule_account_and_origin(){
        let(home,mut run)=fixture();let action=run.actions[0].clone();remember(&home,&run,&[action.id.clone()]).unwrap();assert!(allowed(&home,&run,&action).unwrap());
        let mut regenerated=action.clone();regenerated.id="new-native-id".into();regenerated.estimated_bytes=999;assert!(allowed(&home,&run,&regenerated).unwrap());
        let mut changed=action.clone();changed.command=vec!["different-method".into()];assert!(!allowed(&home,&run,&changed).unwrap());
        changed=action.clone();changed.kind="command".into();assert!(!allowed(&home,&run,&changed).unwrap());
        let mut changed=action.clone();changed.paths=vec![home.join("Library/Caches").to_string_lossy().into_owned()];assert!(!allowed(&home,&run,&changed).unwrap());
        changed=action.clone();changed.cwd=Some(home.to_string_lossy().into_owned());assert!(!allowed(&home,&run,&changed).unwrap());
        changed=action.clone();changed.native_rule="another-rule".into();assert!(!allowed(&home,&run,&changed).unwrap());
        run.account_id=Some("other-user".into());assert!(!allowed(&home,&run,&action).unwrap());run.account_id=Some("fixture-user".into());run.api_origin=Some("https://other.test".into());assert!(!allowed(&home,&run,&action).unwrap());fs::remove_dir_all(home).unwrap();
    }
    #[test]fn daily_execution_uses_shared_native_executor_and_preserves_new_locations(){
        let(home,mut run)=fixture();let known=run.actions[0].clone();remember(&home,&run,&[known.id.clone()]).unwrap();
        let unknown=home.join("Library/Caches/new");fs::create_dir_all(&unknown).unwrap();fs::write(unknown.join("original"),b"never approved").unwrap();let new=crate::cleanup_discovery::action("New fixture",unknown.clone(),vec![],"Fixture only");run.actions.push(new.clone());run.verified_actions.push(session::action_key(&new));
        assert_eq!(approved_ids(&home,&run).unwrap(),vec![known.id.clone()]);
        publish(&home,&run).unwrap();let text:String=store::open(&home).unwrap().query_row("SELECT payload FROM daily_notifications WHERE run_id=?",[&run.id],|r|r.get(0)).unwrap();assert_eq!(serde_json::from_str::<Notification>(&text).unwrap().pending_count,1);
        run.status="executing".into();run.approved_ids=vec![known.id.clone(),new.id.clone()];store::save_run(&home,&run.id,&json!(run)).unwrap();
        assert_eq!(crate::cleanup_tools::execute_local(&home,&run.id,&known.id).unwrap()["ok"],true);
        assert!(crate::cleanup_tools::execute_local(&home,&run.id,&new.id).unwrap_err().contains("revoked"));assert!(unknown.join("original").exists());assert!(!Path::new(&known.paths[0]).exists());fs::remove_dir_all(home).unwrap();
    }
    #[test]fn approval_batches_roll_back_if_any_location_lacks_native_verification(){
        let(home,mut run)=fixture();let known=run.actions[0].clone();let unverified=crate::cleanup_discovery::action("Unverified fixture",home.join("Library/Caches/unverified"),vec![],"Fixture only");run.actions.push(unverified.clone());
        assert!(remember(&home,&run,&[known.id.clone(),unverified.id.clone()]).is_err());assert!(!allowed(&home,&run,&known).unwrap());assert!(!allowed(&home,&run,&unverified).unwrap());fs::remove_dir_all(home).unwrap();
    }
    #[test]fn revocations_and_changed_filesystem_boundaries_are_rechecked_before_execution(){
        let(home,mut run)=fixture();let action=run.actions[0].clone();remember(&home,&run,&[action.id.clone()]).unwrap();run.status="executing".into();run.approved_ids=vec![action.id.clone()];store::save_run(&home,&run.id,&json!(run)).unwrap();
        store::open(&home).unwrap().execute("UPDATE cleanup_approvals SET enabled=0",[]).unwrap();assert!(crate::cleanup_tools::execute_local(&home,&run.id,&action.id).is_err());assert!(Path::new(&action.paths[0]).join("blob").exists());
        write_approval(&home,&run,&action,false).unwrap();assert!(!allowed(&home,&run,&action).unwrap());
        remember(&home,&run,&[action.id.clone()]).unwrap();let path=Path::new(&action.paths[0]);let protected=home.join("Documents/original");fs::create_dir_all(&protected).unwrap();fs::write(protected.join("keep"),b"original").unwrap();fs::remove_dir_all(path).unwrap();std::os::unix::fs::symlink(&protected,path).unwrap();
        assert_eq!(crate::cleanup_tools::execute_local(&home,&run.id,&action.id).unwrap()["ok"],false);assert!(protected.join("keep").exists());fs::remove_dir_all(home).unwrap();
    }
    #[test]fn imports_only_explicit_historical_approvals_and_never_promotes_automatic_or_failed_reviews(){
        let(home,mut run)=fixture();run.discovery_options.daily_care=false;run.approved_ids=vec![run.actions[0].id.clone()];store::save_run(&home,&run.id,&json!(run)).unwrap();
        let mut automatic=run.clone();automatic.id="a".repeat(32);automatic.actions[0].paths[0]=home.join("Library/Caches/automatic").to_string_lossy().into_owned();automatic.verified_actions=automatic.actions.iter().map(session::action_key).collect();automatic.automatic_enabled=true;automatic.automatic_ids=automatic.approved_ids.clone();store::save_run(&home,&automatic.id,&json!(automatic)).unwrap();
        import_previous(&home,"fixture-user","https://fixture.test").unwrap();assert!(allowed(&home,&run,&run.actions[0]).unwrap());assert!(!allowed(&home,&automatic,&automatic.actions[0]).unwrap());
        run.discovery_options.daily_care=true;run.error=Some("Provider unavailable".into());assert!(approved_ids(&home,&run).unwrap().is_empty());fs::remove_dir_all(home).unwrap();
    }
    #[test]fn new_findings_persist_as_one_notification_until_reviewed_and_resolved(){
        let(home,mut run)=fixture();publish(&home,&run).unwrap();publish(&home,&run).unwrap();let db=store::open(&home).unwrap();let count:i64=db.query_row("SELECT COUNT(*) FROM daily_notifications",[],|r|r.get(0)).unwrap();assert_eq!(count,1);
        let text:String=db.query_row("SELECT payload FROM daily_notifications",[],|r|r.get(0)).unwrap();let notification:Notification=serde_json::from_str(&text).unwrap();assert_eq!(notification.pending_count,1);assert_eq!(notification.run_id,run.id);assert!(!notification.body.contains(&home.to_string_lossy().to_string()));
        db.execute("UPDATE daily_notifications SET seen=1",[]).unwrap();drop(db);run.status="done".into();let mut outcome=session::Outcome::started(run.actions[0].id.clone());outcome.status="success".into();outcome.ok=true;run.outcomes.push(outcome);publish(&home,&run).unwrap();
        let db=store::open(&home).unwrap();let(text,seen):(String,bool)=db.query_row("SELECT payload,seen FROM daily_notifications",[],|r|Ok((r.get(0)?,r.get(1)?))).unwrap();assert!(seen);assert_eq!(serde_json::from_str::<Notification>(&text).unwrap().pending_count,0);drop(db);fs::remove_dir_all(home).unwrap();
    }
}
