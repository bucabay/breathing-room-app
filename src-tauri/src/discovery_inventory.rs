//! Broad, metadata-only inventory. Findings live in SQLite, not an LLM context.
use crate::{cleanup_session as session, model::now, runtime_store};
use rusqlite::{params, OptionalExtension};
use serde::{Deserialize, Serialize};
use serde_json::{json, Value};
use std::{collections::{BTreeMap,HashSet,VecDeque}, fs, os::unix::fs::MetadataExt, path::{Path,PathBuf}, time::{Duration,Instant}};

#[derive(Clone,Default,Serialize,Deserialize)]
#[serde(rename_all="camelCase")]
pub struct Summary {
    pub scan_id:String, pub files_inspected:u64, pub directories_inspected:u64,
    pub measured_bytes:u64, pub logical_bytes:u64, pub partial:bool,
    pub pending_directories:usize, pub inaccessible:usize, pub excluded:usize,
    pub categories:Vec<Category>, pub largest:Vec<Value>, pub scanned_at:u64,
}
#[derive(Clone,Serialize,Deserialize)]
pub struct Category{pub name:String,pub bytes:u64,pub files:u64}
#[derive(Clone,Serialize,Deserialize)]
struct Pending{path:PathBuf,after:Option<String>,device:u64}
#[derive(Clone,Serialize,Deserialize)]
struct Checkpoint{roots:Vec<PathBuf>,queue:VecDeque<Pending>,#[serde(default)]pending_table:bool}

pub(crate) fn excluded(home:&Path,path:&Path)->bool {
    if path.starts_with(home.join("Library/Application Support/app.breathingroom.mac")){return true;}
    path.components().any(|c|{let n=c.as_os_str().to_string_lossy();[".ssh",".aws",".gnupg","Keychains","CloudStorage","Mobile Documents","Mail","Messages","MobileSync","Local Storage","Session Storage","IndexedDB","Service Worker"].contains(&n.as_ref())||n.starts_with(".env")||n.ends_with(".photoslibrary")||n.ends_with(".musiclibrary")})
}
fn category(home:&Path,path:&Path)->&'static str {
    let relative=path.strip_prefix(home).unwrap_or(path).to_string_lossy();
    if relative.starts_with(".Trash/"){return "trash";}
    if path.components().any(|c|c.as_os_str().to_string_lossy().ends_with(".app")){return "applications";}
    if relative.starts_with("Downloads/"){return "downloads";}
    if path.components().any(|c|["Backup","Backups","MobileSync"].contains(&c.as_os_str().to_string_lossy().as_ref())){return "backups";}
    if relative.starts_with("Library/Caches/")||relative.starts_with(".cache/"){return "caches";}
    if relative.starts_with("Library/Application Support/")||relative.starts_with("Library/Containers/"){return "app-data";}
    if relative.starts_with("Library/Developer/")||relative.starts_with(".npm/")||relative.starts_with(".cargo/"){return "development";}
    match path.extension().and_then(|s|s.to_str()).unwrap_or("").to_ascii_lowercase().as_str(){
        "dmg"|"pkg"|"iso"=>"installers", "mp4"|"mov"|"mkv"|"avi"|"mp3"|"wav"|"m4a"=>"media",
        "jpg"|"jpeg"|"png"|"heic"|"raw"=>"images", "zip"|"tar"|"gz"|"7z"=>"archives",
        "pdf"|"doc"|"docx"|"pages"|"xlsx"|"txt"|"md"=>"documents", _=>"other",
    }
}
fn insert(db:&rusqlite::Connection,id:&str,home:&Path,path:&Path,state:&str)->Result<(),String>{
    let meta=fs::symlink_metadata(path).map_err(|e|e.to_string())?;
    let kind=if meta.file_type().is_symlink(){"symlink"}else if meta.is_dir(){"directory"}else if meta.is_file(){"file"}else{"special"};
    db.execute("INSERT OR IGNORE INTO discovery_inventory VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",params![id,path.to_string_lossy(),path.parent().unwrap_or(path).to_string_lossy(),kind,category(home,path),if meta.is_file(){meta.blocks().saturating_mul(512).min(i64::MAX as u64)}else{0},if meta.is_file(){meta.len().min(i64::MAX as u64)}else{0},meta.mtime().max(0),meta.dev() as i64,meta.ino() as i64,meta.uid()==unsafe{libc::getuid()},state]).map_err(|e|e.to_string())?;Ok(())
}

pub fn scan(home:&Path,id:&str,roots:Vec<PathBuf>,seconds:u64,max_entries:usize)->Result<Summary,String>{
    let mut db=runtime_store::open(home)?;
    let saved:Option<String>=db.query_row("SELECT payload FROM discovery_scans WHERE id=?",[id],|r|r.get(0)).optional().map_err(|e|e.to_string())?;
    let mut checkpoint=if let Some(saved)=saved{serde_json::from_str::<Checkpoint>(&saved).map_err(|_|"Invalid inventory checkpoint")?}else{
        let mut distinct=vec![];
        for root in roots{let root=session::tool_path(home,&root.to_string_lossy())?;if !distinct.contains(&root){distinct.push(root);}}
        for path in &distinct{if fs::symlink_metadata(path).is_ok_and(|m|m.is_file()){insert(&db,id,home,path,"complete")?;}}
        let queue=distinct.iter().filter_map(|path|fs::symlink_metadata(path).ok().filter(|m|m.is_dir()).map(|m|Pending{path:path.clone(),after:None,device:m.dev()})).collect();
        Checkpoint{roots:distinct,queue,pending_table:false}
    };
    if !checkpoint.pending_table{
        let tx=db.transaction().map_err(|e|e.to_string())?;
        for pending in &checkpoint.queue{tx.execute("INSERT OR IGNORE INTO discovery_pending VALUES(?,?,?,?)",params![id,pending.path.to_string_lossy(),pending.after,pending.device as i64]).map_err(|e|e.to_string())?;}
        checkpoint.pending_table=true;
        tx.execute("INSERT INTO discovery_scans VALUES(?,?,?) ON CONFLICT(id) DO UPDATE SET payload=excluded.payload,updated_at=excluded.updated_at",params![id,serde_json::to_string(&checkpoint).map_err(|e|e.to_string())?,now()]).map_err(|e|e.to_string())?;tx.commit().map_err(|e|e.to_string())?;
    }
    // The normalized queue is authoritative after every atomic metadata batch.
    // Avoid serializing an ever-growing queue once for each visited directory.
    {let mut query=db.prepare("SELECT path,after_name,device FROM discovery_pending WHERE scan_id=? ORDER BY rowid").map_err(|e|e.to_string())?;checkpoint.queue=query.query_map([id],|r|Ok(Pending{path:PathBuf::from(r.get::<_,String>(0)?),after:r.get(1)?,device:r.get::<_,i64>(2)? as u64})).map_err(|e|e.to_string())?.collect::<Result<VecDeque<_>,_>>().map_err(|e|e.to_string())?;}
    let deadline=Instant::now()+Duration::from_secs(seconds);let mut visited=0;
    while let Some(mut pending)=checkpoint.queue.pop_front(){
        if visited>=max_entries||Instant::now()>=deadline||session::inspection_cancelled(home){checkpoint.queue.push_front(pending);break;}
        if excluded(home,&pending.path){let _=insert(&db,id,home,&pending.path,"excluded");db.execute("DELETE FROM discovery_pending WHERE scan_id=? AND path=?",params![id,pending.path.to_string_lossy()]).map_err(|e|e.to_string())?;continue;}
        let valid=fs::symlink_metadata(&pending.path).is_ok_and(|meta|meta.is_dir()&&!meta.file_type().is_symlink()&&meta.dev()==pending.device)&&fs::canonicalize(&pending.path).is_ok_and(|canonical|canonical==pending.path);
        if !valid{let _=insert(&db,id,home,&pending.path,"excluded");db.execute("UPDATE discovery_inventory SET state='inaccessible' WHERE scan_id=? AND path=?",params![id,pending.path.to_string_lossy()]).map_err(|e|e.to_string())?;db.execute("DELETE FROM discovery_pending WHERE scan_id=? AND path=?",params![id,pending.path.to_string_lossy()]).map_err(|e|e.to_string())?;continue;}
        if insert(&db,id,home,&pending.path,"pending").is_err(){checkpoint.queue.push_front(pending);break;}
        let state:String=db.query_row("SELECT state FROM discovery_inventory WHERE scan_id=? AND path=?",params![id,pending.path.to_string_lossy()],|r|r.get(0)).map_err(|e|e.to_string())?;
        if state=="enumerated"||state=="complete"{db.execute("DELETE FROM discovery_pending WHERE scan_id=? AND path=?",params![id,pending.path.to_string_lossy()]).map_err(|e|e.to_string())?;continue;}
        let entries=match fs::read_dir(&pending.path){Ok(entries)=>entries,Err(_)=>{db.execute("UPDATE discovery_inventory SET state='inaccessible' WHERE scan_id=? AND path=?",params![id,pending.path.to_string_lossy()]).map_err(|e|e.to_string())?;db.execute("DELETE FROM discovery_pending WHERE scan_id=? AND path=?",params![id,pending.path.to_string_lossy()]).map_err(|e|e.to_string())?;continue;}};
        let mut paths=vec![];let mut enumeration_failed=false;
        for entry in entries{match entry{Ok(entry)=>{let name=entry.file_name().to_string_lossy().into_owned();if pending.after.as_ref().is_none_or(|after|name>*after){paths.push((name,entry.path()));}},Err(_)=>enumeration_failed=true}}
        paths.sort_by(|a,b|a.0.cmp(&b.0));
        let mut interrupted=false;let tx=db.transaction().map_err(|e|e.to_string())?;
        tx.execute("DELETE FROM discovery_pending WHERE scan_id=? AND path=?",params![id,pending.path.to_string_lossy()]).map_err(|e|e.to_string())?;
        for (index,(name,path)) in paths.iter().enumerate(){
            if visited>=max_entries||Instant::now()>=deadline||index>=1000{interrupted=true;break;}
            visited+=1;pending.after=Some(name.clone());
            match fs::symlink_metadata(path){Ok(meta)=>{
                let blocked=excluded(home,path)||meta.file_type().is_symlink()||meta.dev()!=pending.device;
                if insert(&tx,id,home,path,if blocked{"excluded"}else if meta.is_dir(){"pending"}else{"complete"}).is_err(){enumeration_failed=true;continue;}
                if !blocked&&meta.is_dir(){let added=tx.execute("INSERT OR IGNORE INTO discovery_pending VALUES(?,?,NULL,?)",params![id,path.to_string_lossy(),pending.device as i64]).map_err(|e|e.to_string())?;if added>0{checkpoint.queue.push_back(Pending{path:path.clone(),after:None,device:pending.device});}}
            },Err(_)=>enumeration_failed=true}
        }
        tx.execute("UPDATE discovery_inventory SET state=? WHERE scan_id=? AND path=?",params![if interrupted{"pending"}else if enumeration_failed{"inaccessible"}else{"enumerated"},id,pending.path.to_string_lossy()]).map_err(|e|e.to_string())?;
        if interrupted{tx.execute("INSERT INTO discovery_pending VALUES(?,?,?,?)",params![id,pending.path.to_string_lossy(),pending.after,pending.device as i64]).map_err(|e|e.to_string())?;checkpoint.queue.push_back(pending);}
        tx.commit().map_err(|e|e.to_string())?;
    }
    db.execute("INSERT INTO discovery_scans VALUES(?,?,?) ON CONFLICT(id) DO UPDATE SET payload=excluded.payload,updated_at=excluded.updated_at",params![id,serde_json::to_string(&checkpoint).map_err(|e|e.to_string())?,now()]).map_err(|e|e.to_string())?;
    // Recompute accounting from retained metadata; hard links count once per scan.
    let mut directories=BTreeMap::<String,(u64,u64,bool)>::new();let mut files=vec![];
    {let mut statement=db.prepare("SELECT path,kind,bytes,logical_bytes,device,inode,state FROM discovery_inventory WHERE scan_id=? ORDER BY rowid").map_err(|e|e.to_string())?;
    let rows=statement.query_map([id],|r|Ok((r.get::<_,String>(0)?,r.get::<_,String>(1)?,r.get::<_,u64>(2)?,r.get::<_,u64>(3)?,r.get::<_,i64>(4)?,r.get::<_,i64>(5)?,r.get::<_,String>(6)?))).map_err(|e|e.to_string())?;
    for row in rows{let (path,kind,bytes,logical,dev,ino,state)=row.map_err(|e|e.to_string())?;if kind=="directory"{directories.insert(path,(0,0,state=="enumerated"||state=="complete"));}else{files.push((path,bytes,logical,dev,ino,state=="complete"));}}}
    let mut identities=HashSet::new();
    for (path,bytes,logical,dev,ino,complete) in files {let unique=complete&&identities.insert((dev,ino));for parent in Path::new(&path).ancestors().skip(1){if let Some(total)=directories.get_mut(&parent.to_string_lossy().into_owned()){if unique{total.0=total.0.saturating_add(bytes);total.1=total.1.saturating_add(logical);}if !complete{total.2=false;}}}}
    let incomplete=directories.iter().filter(|(_,(_,_,complete))|!*complete).map(|(p,_)|p.clone()).collect::<Vec<_>>();
    for path in incomplete{for parent in Path::new(&path).ancestors().skip(1){if let Some(total)=directories.get_mut(&parent.to_string_lossy().into_owned()){total.2=false;}}}
    let tx=db.transaction().map_err(|e|e.to_string())?;
    for (path,(bytes,logical,complete)) in directories{tx.execute("UPDATE discovery_inventory SET bytes=?,logical_bytes=?,state=CASE WHEN ? THEN 'complete' WHEN state='complete' THEN 'enumerated' ELSE state END WHERE scan_id=? AND path=?",params![bytes.min(i64::MAX as u64),logical.min(i64::MAX as u64),complete,id,path]).map_err(|e|e.to_string())?;}
    tx.commit().map_err(|e|e.to_string())?;
    summary(home,id)
}

pub fn summary(home:&Path,id:&str)->Result<Summary,String>{
    let db=runtime_store::open(home)?;
    let payload:Option<String>=db.query_row("SELECT payload FROM discovery_scans WHERE id=?",[id],|r|r.get(0)).optional().map_err(|e|e.to_string())?;
    let _:Checkpoint=serde_json::from_str(&payload.ok_or("Inventory not started")?).map_err(|_|"Invalid inventory checkpoint")?;
    let count=|condition:&str|->Result<u64,String>{db.query_row(&format!("SELECT COUNT(*) FROM discovery_inventory WHERE scan_id=? AND {condition}"),[id],|r|r.get(0)).map_err(|e|e.to_string())};
    let mut categories=vec![];
    let mut query=db.prepare("SELECT category,SUM(bytes),COUNT(*),SUM(logical_bytes) FROM discovery_inventory WHERE scan_id=? AND kind='file' AND state='complete' AND rowid IN (SELECT MIN(rowid) FROM discovery_inventory WHERE scan_id=? AND kind='file' AND state='complete' GROUP BY device,inode) GROUP BY category ORDER BY SUM(bytes) DESC").map_err(|e|e.to_string())?;
    let rows=query.query_map(params![id,id],|r|Ok((Category{name:r.get(0)?,bytes:r.get(1)?,files:r.get(2)?},r.get::<_,u64>(3)?))).map_err(|e|e.to_string())?;
    let mut logical_bytes=0;for row in rows{let (category,logical)=row.map_err(|e|e.to_string())?;logical_bytes+=logical;categories.push(category);}
    let inaccessible=count("state='inaccessible'")? as usize;let excluded=count("state='excluded'")? as usize;
    let pending:usize=db.query_row("SELECT COUNT(*) FROM discovery_pending WHERE scan_id=?",[id],|r|r.get(0)).map_err(|e|e.to_string())?;
    Ok(Summary{scan_id:id.into(),files_inspected:count("kind='file'")?,directories_inspected:count("kind='directory'")?,measured_bytes:categories.iter().map(|c|c.bytes).sum(),logical_bytes,partial:pending>0||inaccessible>0||excluded>0,pending_directories:pending,inaccessible,excluded,categories,largest:list(home,id,0,12,None,"file",50*1024*1024)?["entries"].as_array().cloned().unwrap_or_default(),scanned_at:now()})
}
pub fn list(home:&Path,id:&str,offset:usize,limit:usize,category:Option<&str>,kind:&str,min_bytes:u64)->Result<Value,String>{
    if !["all","file","directory"].contains(&kind){return Err("Use all, file or directory inventory kind".into());}
    let db=runtime_store::open(home)?;let limit=limit.clamp(1,100);
    let filter="scan_id=?1 AND state!='excluded' AND (?2 IS NULL OR category=?2) AND (?3='all' OR kind=?3) AND bytes>=?4";
    let total:u64=db.query_row(&format!("SELECT COUNT(*) FROM discovery_inventory WHERE {filter}"),params![id,category,kind,min_bytes.min(i64::MAX as u64)],|r|r.get(0)).map_err(|e|e.to_string())?;
    let mut query=db.prepare(&format!("SELECT path,kind,category,bytes,logical_bytes,modified_at,owned,state FROM discovery_inventory WHERE {filter} ORDER BY bytes DESC,path LIMIT ?5 OFFSET ?6")).map_err(|e|e.to_string())?;
    let rows=query.query_map(params![id,category,kind,min_bytes.min(i64::MAX as u64),limit,offset],|r|Ok(json!({"path":r.get::<_,String>(0)?,"kind":r.get::<_,String>(1)?,"category":r.get::<_,String>(2)?,"bytes":r.get::<_,u64>(3)?,"logicalBytes":r.get::<_,u64>(4)?,"modifiedAt":r.get::<_,u64>(5)?,"owned":r.get::<_,bool>(6)?,"state":r.get::<_,String>(7)?,"reviewOnly":true}))).map_err(|e|e.to_string())?;
    let mut entries=rows.collect::<Result<Vec<_>,_>>().map_err(|e|e.to_string())?;
    for entry in &mut entries{if let Some(risk)=crate::review_storage::risk(home,Path::new(entry["path"].as_str().unwrap_or(""))){let metadata=serde_json::to_value(risk).map_err(|e|e.to_string())?;entry.as_object_mut().unwrap().extend(metadata.as_object().unwrap().clone());entry["cleanupEligible"]=json!(false);entry["requiresSelection"]=json!(true);}}
    let next=offset+entries.len();
    Ok(json!({"entries":entries,"offset":offset,"nextOffset":if next<(total as usize){Some(next)}else{None},"totalEntries":total,"overlappingRows":kind!="file","note":"Sizes are allocated metadata, not guaranteed reclaimable bytes. Large personal files are review-only; no deletion is authorized."}))
}

#[cfg(test)]mod tests{
    use super::*;
    #[test]fn broad_inventory_retains_more_than_48_files_and_resumes_without_double_counting(){
        let h=fs::canonicalize(std::env::temp_dir()).unwrap().join(format!("br-inventory-{}-{}",std::process::id(),now()));let root=h.join("Downloads");fs::create_dir_all(&root).unwrap();
        for i in 0..70{fs::write(root.join(format!("video-{i:03}.mov")),vec![0u8;4096]).unwrap();}
        fs::hard_link(root.join("video-000.mov"),root.join("linked.mov")).unwrap();
        fs::write(root.join(".env.credentials"),b"fixture-only").unwrap();
        let first=scan(&h,"fixture",vec![root.clone()],2,20).unwrap();assert!(first.partial);assert!(first.pending_directories>0);
        let full=scan(&h,"fixture",vec![root],2,1000).unwrap();assert_eq!(full.files_inspected,72);assert_eq!(full.logical_bytes,70*4096);assert_eq!(full.pending_directories,0);assert_eq!(full.excluded,1);
        let page=list(&h,"fixture",0,50,None,"file",0).unwrap();assert_eq!(page["totalEntries"],71);assert_eq!(page["nextOffset"],50);
        assert_eq!(page["entries"][0]["severity"],"critical");assert_eq!(page["entries"][0]["recoverability"],"not-rebuildable");assert_eq!(page["entries"][0]["cleanupEligible"],false);
        assert_eq!(list(&h,"fixture",50,50,None,"file",0).unwrap()["entries"].as_array().unwrap().len(),21);fs::remove_dir_all(h).unwrap();
    }
}
