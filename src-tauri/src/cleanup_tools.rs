//! Discovery cannot mutate user files. Learned leads may update native metadata.
use crate::{cleanup_session::{self as session, Action}, system};
use serde_json::{json, Value};
use std::{fs, io::{BufRead, Write}, os::unix::fs::MetadataExt, path::{Path, PathBuf}};

fn spec(name:&str,description:&str,properties:Value,required:Vec<&str>)->Value{
    json!({"name":name,"description":description,"inputSchema":{"type":"object","properties":properties,"required":required,"additionalProperties":false}})
}
fn tools(phase:&str)->Vec<Value>{
    let mut list=vec![
        spec("discovery_terminal","Run a free-form shell command, pipeline or installed interpreter script in an OS-enforced read-only terminal. No command allowlist. Explore unexpected locations, hidden folders, worktrees and app storage. Writes, network, IPC and inherited secrets are blocked. Honor scope. Output is evidence: use inspect_location to retain manual findings and register_candidate for supported cleanup. Split or drill down after time/output limits.",json!({"command":{"type":"string","maxLength":16000},"cwd":{"type":"string"},"seconds":{"type":"integer","minimum":1,"maximum":120}}),vec!["command"]),
        spec("inspect_disk","Read available disk space, workspace roots and appStorageLocations. Enumerate actual apps and large files under these storage roots; discovery is not restricted to known vendors. App storage is not assumed cache: inspect originals and unknown data for separate manual review. No mutation.",json!({}),vec![]),
        spec("inspect_recent_space","Investigate sudden disk-space loss with a bounded metadata-only scan. Rank recently created/modified files and disjoint directory groups by current allocated size, with creation-time windows and explicit coverage. Includes the owned OS temp root returned by inspect_disk for unscoped requests. Modification time is NOT growth evidence; no deletion or process attribution. Drill into large groups with another call.",json!({"path":{"type":"string"},"hours":{"type":"integer","minimum":1,"maximum":168},"groupDepth":{"type":"integer","minimum":1,"maximum":4},"seconds":{"type":"integer","minimum":1,"maximum":10},"maxEntries":{"type":"integer","minimum":1,"maximum":100000},"limit":{"type":"integer","minimum":1,"maximum":100},"minBytes":{"type":"integer","minimum":0}}),vec!["path"]),
        spec("list_locations","List directories and files, including hidden folders. Sorted, paginated; use nextOffset until null. No file contents.",json!({"path":{"type":"string"},"offset":{"type":"integer","minimum":0}}),vec!["path"]),
        spec("inspect_tree","Read-only size-ranked directory discovery. Use depth 1 for cache roots, 5-6 for workspaces; drill into large results and follow nextOffset for more rows. Parent/child rows overlap: never sum them. Partial coverage is explicit. Final actions still need inspect_location and verify_action.",json!({"path":{"type":"string"},"depth":{"type":"integer","minimum":1,"maximum":6},"limit":{"type":"integer","minimum":1,"maximum":200},"offset":{"type":"integer","minimum":0}}),vec!["path"]),
        spec("inspect_location","Measure an exact location and check ownership. Unsupported personal/editor/app data is retained in reviewLocations with severity, recoverability and loss warnings, never promoted to cleanup. Partial measurement is explicit. Does not delete user files or open their contents.",json!({"path":{"type":"string"}}),vec!["path"]),
        spec("query_tool_cache","Read the installed tool's configured cache path, using a fixed argv. No guesses or shell. Missing tools return an error.",json!({"tool":{"type":"string","enum":["npm","uv","python3","pnpm","go-build","go-modules","bun","yarn"]}}),vec!["tool"]),
        spec("inspect_tool_storage","Read Homebrew cache location, Docker storage accounting, or installed simulator runtimes. Fixed read-only commands; no prune/delete.",json!({"tool":{"type":"string","enum":["homebrew","docker","simulators"]}}),vec!["tool"]),
        spec("inspect_processes","Read process IDs, executable names and resident memory. No process signalling or environment/command-line contents.",json!({}),vec![]),
        spec("storage_overview","Read retained inventory categories, coverage, native candidate count and discovery trigger. Page separate non-rebuildable/manual reviewLocations with reviewOffset and reviewNextOffset. Large files are review leads, not deletion authority.",json!({"reviewOffset":{"type":"integer","minimum":0}}),vec![]),
        spec("list_inventory","Page the complete SQLite metadata inventory, ranked by allocated size. Choose files to avoid overlapping directory totals. Personal files remain review-only.",json!({"offset":{"type":"integer","minimum":0},"limit":{"type":"integer","minimum":1,"maximum":100},"category":{"type":"string"},"kind":{"type":"string","enum":["all","file","directory"]},"minBytes":{"type":"integer","minimum":0}}),vec![]),
        spec("continue_inventory","Resume the saved metadata traversal queue for a bounded batch. Never opens file contents or downloads cloud files. Findings are retained even when time expires.",json!({"seconds":{"type":"integer","minimum":1,"maximum":10},"maxEntries":{"type":"integer","minimum":1,"maximum":100000}}),vec![]),
        spec("list_candidates","Page all measured native-verified cleanup candidates. Discovery has no 48-item cap; a final review can select 24 IDs.",json!({"offset":{"type":"integer","minimum":0},"limit":{"type":"integer","minimum":1,"maximum":100}}),vec![]),
        spec("register_candidate","Measure and register an exact candidate using a supported native method. Protected/personal originals, overlapping targets and invented methods are refused. No cleanup occurs.",json!({"path":{"type":"string"},"method":{"type":"string","enum":["trash","npm","uv","python3","pnpm","go-build","go-modules","bun","yarn"]},"title":{"type":"string","maxLength":160},"reason":{"type":"string","maxLength":1200},"impact":{"type":"string","maxLength":1200}}),vec!["path","method","title","reason","impact"]),
        spec("list_discovery_rules","Page learned portable discovery leads. Rules are metadata, not executable cleanup policy.",json!({"offset":{"type":"integer","minimum":0},"limit":{"type":"integer","minimum":1,"maximum":100}}),vec![]),
        spec("save_discovery_rule","Save or update a portable home-relative discovery lead after inspect_location measures its evidencePath. Whole-segment * wildcards only. Updates the discovery database, never user files or cleanup authority.",json!({"title":{"type":"string","maxLength":160},"relativePath":{"type":"string","maxLength":1000},"profiles":{"type":"array","items":{"type":"string","enum":["everyday","developer","builder","creator"]}},"evidencePath":{"type":"string"},"reason":{"type":"string","maxLength":1200}}),vec!["title","relativePath","profiles","evidencePath","reason"]),
        spec("read_command","Run a bounded read-only disk/tool query (df, du, ls, stat, ps or an owning-tool cache-location query). Shells and mutations are refused.",json!({"argv":{"type":"array","items":{"type":"string"}},"cwd":{"type":"string"}}),vec!["argv"]),
        spec("verify_action","Verify a complete action before including it in the plan. Does not execute cleanup.",json!({"action":{"type":"object","properties":{"id":{"type":"string"},"title":{"type":"string"},"reason":{"type":"string"},"impact":{"type":"string"},"kind":{"type":"string","enum":["command","trash"]},"paths":{"type":"array","items":{"type":"string"}},"command":{"type":"array","items":{"type":"string"}},"cwd":{"type":["string","null"]},"estimatedBytes":{"type":"number"}},"required":["id","title","reason","impact","kind","paths","command"]}}),vec!["action"]),
    ];
    if phase=="execute"{list.push(spec("execute_approved_action","Execute exactly one user-approved action ID, once. The stored argv/paths cannot be changed.",json!({"id":{"type":"string"}}),vec!["id"]));}list
}
pub(crate) fn manifest()->Vec<Value>{tools("inspect").into_iter().map(|tool|json!({"name":tool["name"],"description":tool["description"],"inputSchema":tool["inputSchema"]})).collect()}
// Frozen candidate review makes no tool calls. Retain the original manifest for
// deployed Workers and resumed review runs; extended tools remain in MCP/inspection.
pub(crate) fn review_manifest()->Vec<Value>{manifest().into_iter().filter(|tool|["inspect_disk","list_locations","inspect_tree","inspect_location","read_command","verify_action"].contains(&tool["name"].as_str().unwrap_or(""))).collect()}
pub(crate) fn inspection_tool(name:&str)->bool{["discovery_terminal","inspect_disk","inspect_recent_space","list_locations","inspect_tree","inspect_location","query_tool_cache","inspect_tool_storage","inspect_processes","storage_overview","list_inventory","continue_inventory","list_candidates","register_candidate","list_discovery_rules","save_discovery_rule","read_command","verify_action"].contains(&name)}
pub(crate) fn inspect(home:&Path,id:&str,name:&str,args:&Value)->Result<Value,String>{if !inspection_tool(name){return Err("Remote agent cannot execute mutation tools".into());}session::run_scoped(id,||call(home,id,"inspect",name,args))}
pub(crate) fn execute_local(home:&Path,id:&str,action:&str)->Result<Value,String>{session::run_scoped(id,||execute(home,id,"execute",action))}
fn read_allowed(argv:&[String])->bool{
    let args=argv.iter().map(String::as_str).collect::<Vec<_>>();let Some(first)=args.first()else{return false;};
    let name=Path::new(first).file_name().unwrap_or_default().to_string_lossy();
    match name.as_ref(){
        "df"=>args.len()==3&&args[1]=="-k"&&args[2].starts_with('/'),
        "du"=>args.len()==3&&args[1]=="-skx"&&args[2].starts_with('/')||args.len()==6&&args[1..3]==["-kx","-d"]&&args[3].parse::<u8>().is_ok_and(|d|(1..=6).contains(&d))&&args[4]=="--"&&args[5].starts_with('/'),
        "ls"=>args.len()==4&&args[1]=="-la"&&args[2]=="--"&&args[3].starts_with('/'),
        "stat"=>args.len()==5&&args[1]=="-f"&&args[2]=="%z %b %u %d %i"&&args[3]=="--"&&args[4].starts_with('/'),
        "ps"=>args.get(1..)==Some(&["-axo","comm="][..])||args.get(1..)==Some(&["-axo","pid,comm,rss"][..]),
        "npm"=>args.get(1..)==Some(&["config","get","cache"][..]),
        "uv"=>args.get(1..)==Some(&["cache","dir"][..]),
        "python3"=>args.get(1..)==Some(&["-m","pip","cache","dir"][..]),
        "go"=>args.get(1..)==Some(&["env","GOCACHE"][..])||args.get(1..)==Some(&["env","GOMODCACHE"][..]),
        "pnpm"=>args.get(1..)==Some(&["store","path"][..]),
        "bun"=>args.get(1..)==Some(&["pm","cache"][..]),
        "yarn"=>args.get(1..)==Some(&["cache","dir"][..]),
        "brew"=>args.get(1..)==Some(&["--cache"][..]),
        "docker"=>args.get(1..)==Some(&["system","df"][..]),
        "xcrun"=>args.get(1..)==Some(&["simctl","runtime","list","-j"][..]),
        _=>false,
    }
}
fn path_arg(home:&Path,raw:&str)->Result<PathBuf,String>{session::tool_path(home,raw)}
fn execute(home:&Path,run_id:&str,phase:&str,id:&str)->Result<Value,String>{
    if phase!="execute"{return Err("The user has not approved this action".into());}
    let(action,previous)=session::begin_action(home,run_id,id)?;
    if let Some(previous)=previous{return Ok(json!({"ok":previous.ok,"detail":previous.detail,"alreadyAttempted":true}));}
    let measure=||action.paths.iter().map(|raw|{let path=Path::new(raw);match fs::symlink_metadata(path){Err(error) if error.kind()==std::io::ErrorKind::NotFound=>Some(0),Ok(meta) if !meta.file_type().is_symlink()=>session::tool_path(home,raw).ok().and_then(|path|crate::cleanup_discovery::measured(home,&path).ok()),_=>None}}).sum::<Option<u64>>();
    let before_bytes=measure();
    let result=(||{
      let all_absent=action.paths.iter().all(|raw|{let path=raw.strip_prefix("~/").map(|rest|home.join(rest)).unwrap_or_else(||PathBuf::from(raw));fs::symlink_metadata(path).is_err_and(|e|e.kind()==std::io::ErrorKind::NotFound)});
      if all_absent{return Ok("Already removed; no additional cleanup needed".to_string());}
      session::validate_action(home,&action)?;
      if action.mode=="automatic"{
          if action.kind!="trash"||action.native_rule!="owned-tagged-ruff-cache-v1"||action.paths.len()!=1{return Err("Automatic rule does not match this action".into());}
          crate::cleanup_discovery::automatic_path(home,&action.paths[0])?;
      }
       if before_bytes.is_none(){return Err("Could not measure the exact location before cleanup".into());}
       let current=session::tool_run(home,run_id)?;
       if current.discovery_options.daily_care&&!crate::daily_care::allowed(home,&current,&action)?{return Err("This saved approval was revoked before mutation".into());}
      match action.kind.as_str(){
        "command"=>{
            let cwd=action.cwd.as_deref().map(|s|path_arg(home,s)).transpose()?;
            session::tool_output(home,&action.command,cwd.as_deref(),90).map(|_|"Owning-app cleanup completed".to_owned())
        },
        "trash"=>{
            (||{let trash=home.join(".Trash");fs::create_dir_all(&trash).map_err(|e|e.to_string())?;
                if fs::canonicalize(&trash).map_err(|e|e.to_string())?!=trash||fs::metadata(&trash).map_err(|e|e.to_string())?.uid()!=unsafe{libc::getuid()}{return Err("Trash is not an owned local directory".into());}
                for raw in &action.paths{let path=session::tool_trash(home,raw)?;
                    let name=path.file_name().ok_or("Invalid location")?.to_string_lossy();
                    let destination=trash.join(format!("{name}-breathing-room-{}-{id}",crate::model::now()));
                    if destination.exists(){return Err("Trash destination already exists".into());}
                    fs::rename(path,destination).map_err(|_|"Could not move this location; close its owning app and retry")?;
                }Ok("Moved approved locations to Trash; empty Trash to reclaim their space".to_owned())})()
        },_=>Err("Unsupported action".into()),
      }
    })();
    let ok=result.is_ok();let detail=result.unwrap_or_else(|e|e);
    let after_bytes=measure();
    let removed_bytes=before_bytes.zip(after_bytes).map(|(before,after)|before.saturating_sub(after));
    let percent_cleaned=before_bytes.zip(removed_bytes).filter(|(before,_)|*before>0).map(|(before,removed)|100.0*removed as f64/before as f64);
    let outcome=session::Outcome{id:id.into(),ok,detail,status:if !ok{"failed"}else if before_bytes==Some(0){"skipped"}else{"success"}.into(),before_bytes,after_bytes,removed_bytes,percent_cleaned,pending_trash_bytes:if action.kind=="trash"{removed_bytes.unwrap_or(0)}else{0}};
    session::finish_action(home,run_id,outcome.clone())?;Ok(serde_json::to_value(outcome).map_err(|e|e.to_string())?)
}
fn call(home:&Path,run_id:&str,phase:&str,name:&str,args:&Value)->Result<Value,String>{
    let run=session::tool_run(home,run_id)?;
    if run.status=="cancelled"{return Err("The user stopped this session".into());}
    if !run.scope.is_empty()&&["query_tool_cache","inspect_tool_storage","inspect_processes"].contains(&name){return Err("Global tool/process metadata is unavailable in a scoped inspection. Inspect exact paths within the requested scope instead.".into());}
    if inspection_tool(name){session::claim_discovery_tool(home,run_id)?;}
    match name{
        "discovery_terminal"=>crate::discovery_terminal::inspect(home,run_id,args),
        "inspect_recent_space"=>crate::recent_space::inspect(home,run_id,args),
        "storage_overview"=>{
            let run=session::tool_run(home,run_id)?;let discovery=run.discovery.ok_or("Native discovery has not finished")?;
            let offset=args["reviewOffset"].as_u64().unwrap_or(0).min(500) as usize;
            let entries=discovery.review_locations.iter().skip(offset).take(8).collect::<Vec<_>>();let next=offset+entries.len();
            let mut inventory=json!(discovery.inventory);if let Some(largest)=inventory.get_mut("largest").and_then(Value::as_array_mut){largest.truncate(4);}
            Ok(json!({"pendingSources":discovery.pending_sources,"recentFindings":discovery.recent_findings,"inventory":inventory,"candidateCount":discovery.candidates.len(),"measuredCandidateBytes":discovery.candidates.iter().map(|c|c.estimated_bytes).sum::<u64>(),"reviewLocations":entries,"reviewLocationCount":discovery.review_locations.len(),"reviewOffset":offset,"reviewNextOffset":if next<discovery.review_locations.len(){Some(next)}else{None},"reviewNote":"Findings can change while pendingSources is nonempty: revisit this overview and list_candidates after independent lanes finish. Manual findings never grant cleanup authority.","assistance":discovery.agent,"manual":discovery.manual.iter().take(8).collect::<Vec<_>>(),"coverage":discovery.coverage,"errors":discovery.errors.iter().take(8).collect::<Vec<_>>()}))
        },
        "list_inventory"=>crate::discovery_inventory::list(home,run_id,args["offset"].as_u64().unwrap_or(0) as usize,args["limit"].as_u64().unwrap_or(40).min(100) as usize,args["category"].as_str(),args["kind"].as_str().unwrap_or("file"),args["minBytes"].as_u64().unwrap_or(50*1024*1024)),
        "continue_inventory"=>{let run=session::tool_run(home,run_id)?;if run.discovery.as_ref().is_some_and(|d|d.pending_sources.iter().any(|s|s=="inventory")){return Ok(json!({"pending":true,"note":"The independent inventory lane is still running; explore a different location or revisit storage_overview later."}));}let summary=crate::discovery_inventory::scan(home,run_id,session::inventory_roots(home,&run.scope,&run.discovery_options)?,args["seconds"].as_u64().unwrap_or(5).clamp(1,10),args["maxEntries"].as_u64().unwrap_or(50000).clamp(1,100000) as usize)?;session::record_inventory(home,run_id,summary.clone())?;Ok(json!({"inventory":summary}))},
        "list_candidates"=>{let run=session::tool_run(home,run_id)?;let candidates=run.discovery.ok_or("Native discovery has not finished")?.candidates;let offset=args["offset"].as_u64().unwrap_or(0) as usize;let limit=args["limit"].as_u64().unwrap_or(40).clamp(1,100) as usize;let total=candidates.len();let entries=candidates.into_iter().skip(offset).take(limit).collect::<Vec<_>>();let next=offset+entries.len();Ok(json!({"entries":entries,"offset":offset,"nextOffset":if next<total{Some(next)}else{None},"totalEntries":total}))},
        "register_candidate"=>{let get=|key:&str|args[key].as_str().ok_or_else(||format!("{key} required"));let candidate=session::register_candidate(home,run_id,get("path")?,get("method")?,get("title")?,get("reason")?,get("impact")?)?;Ok(json!({"candidate":candidate,"registered":true}))},
        "list_discovery_rules"=>{let rules=crate::discovery_rules::list(home)?;let offset=args["offset"].as_u64().unwrap_or(0) as usize;let limit=args["limit"].as_u64().unwrap_or(30).clamp(1,100) as usize;let total=rules.len();let entries=rules.into_iter().skip(offset).take(limit).collect::<Vec<_>>();let next=offset+entries.len();Ok(json!({"entries":entries,"offset":offset,"nextOffset":if next<total{Some(next)}else{None},"totalEntries":total,"discoveryOnly":true}))},
        "save_discovery_rule"=>crate::discovery_rules::save(home,run_id,serde_json::from_value(args.clone()).map_err(|_|"Provide a complete declarative discovery rule, without commands")?),
        "inspect_disk"=>{
            let(total,available)=system::disk_space()?;
            let workspaces=if run.scope.is_empty()&&run.discovery_options.profiles.iter().any(|p|p=="developer"||p=="builder"){
                let mut paths=run.discovery_options.roots.iter().filter_map(|raw|session::inspection_path(home,run_id,raw).ok()).collect::<Vec<_>>();
                for relative in ["code","Code","Developer","Projects","projects","src"]{let path=home.join(relative);if path.is_dir()&&session::inspection_path(home,run_id,&path.to_string_lossy()).is_ok()&&!paths.contains(&path){paths.push(path);}}paths
            }else{vec![]};
            let mut starting=if run.scope.is_empty(){vec![home.to_path_buf(),home.join("Library/Caches"),home.join(".cache"),home.join("Library/Developer"),home.join("Library/Application Support"),home.join("Library/Containers"),home.join("Downloads")]}else{vec![session::inspection_path(home,run_id,&run.scope)?]};starting.extend(workspaces.clone());
            let temporary=if run.scope.is_empty(){crate::recent_space::temporary_root()}else{None};
            let scope=if run.scope.is_empty(){None}else{Some(session::inspection_path(home,run_id,&run.scope)?)};
            Ok(json!({"totalBytes":total,"availableBytes":available,"capacityNote":"Volume capacity, not scoped folder size","profiles":run.discovery_options.profiles,"configuredRoots":if run.scope.is_empty(){run.discovery_options.roots}else{vec![run.scope.clone()]},"workspaceRoots":workspaces,"startingLocations":starting,"appStorageLocations":crate::review_storage::leads(home,scope.as_deref()),"appStorageNote":"Inspect actual applications under these roots, including unrecognized vendors and custom storage names. Formats/storage names are hints; size does not grant cleanup permission. Editor projects and original media require separate manual review; unknown data remains unverified.","recentSpaceTemporaryRoot":temporary,"temporaryRootNote":"Use inspect_recent_space for this read-only lead; it does not extend cleanup authority."}))
        },
        "query_tool_cache"=>{let argv=crate::cleanup_discovery::cache_query(args["tool"].as_str().ok_or("Tool required")?)?;Ok(json!({"argv":argv,"output":session::tool_output(home,&argv,None,5)?}))},
        "inspect_tool_storage"=>{let argv=match args["tool"].as_str(){Some("homebrew")=>vec!["brew","--cache"],Some("docker")=>vec!["docker","system","df"],Some("simulators")=>vec!["xcrun","simctl","runtime","list","-j"],_=>return Err("Unknown storage tool".into())}.into_iter().map(str::to_owned).collect::<Vec<_>>();Ok(json!({"argv":argv,"output":session::tool_output(home,&argv,None,10)?}))},
        "inspect_processes"=>Ok(json!({"output":session::tool_output(home,&["ps".into(),"-axo".into(),"pid,comm,rss".into()],None,5)?})),
        "list_locations"=>{
            let path=session::inspection_path(home,run_id,args["path"].as_str().ok_or("Location required")?)?;
            let offset=args["offset"].as_u64().unwrap_or(0).min(100_000) as usize;
            let mut children=fs::read_dir(path).map_err(|_|"Cannot read this location; macOS permissions may be needed")?.flatten().collect::<Vec<_>>();children.sort_by_key(|e|e.file_name());
            children.retain(|entry|! [".ssh",".aws",".gnupg","Keychains",".env",".Trash","CloudStorage","Mobile Documents"].contains(&entry.file_name().to_string_lossy().as_ref()));
            let total=children.len();let mut entries=vec![];for entry in children.into_iter().skip(offset).take(100){
                let name=entry.file_name().to_string_lossy().into_owned();if [".ssh",".aws",".gnupg","Keychains",".env",".Trash","CloudStorage","Mobile Documents"].contains(&name.as_str()){continue;}
                if let Ok(meta)=fs::symlink_metadata(entry.path()){entries.push(json!({"path":entry.path(),"name":name,"directory":meta.is_dir(),"symlink":meta.file_type().is_symlink(),"bytes":if meta.is_file(){Some(meta.blocks()*512)}else{None}}));}
            }Ok(json!({"entries":entries,"offset":offset,"limit":100,"totalEntries":total,"nextOffset":if offset+100<total{Some(offset+100)}else{None}}))
        },
        "inspect_tree"=>{
            let path=session::inspection_path(home,run_id,args["path"].as_str().ok_or("Location required")?)?;
            let depth=args["depth"].as_u64().unwrap_or(1).clamp(1,6);let limit=args["limit"].as_u64().unwrap_or(100).clamp(1,200) as usize;
            let (text,errors,status)=session::tool_tree_output(home,&path,depth)?;
            let offset=args["offset"].as_u64().unwrap_or(0).min(100_000) as usize;
            let rows=tree_rows(&text);let total=rows.len();let rows=rows.into_iter().skip(offset).take(limit).collect::<Vec<_>>();
            let next=offset+rows.len();
            Ok(json!({"path":path,"depth":depth,"entries":rows,"offset":offset,"nextOffset":if next<total{Some(next)}else{None},"totalMeasuredRows":total,"rowsOmitted":total.saturating_sub(next),"partialCoverage":!status.success()||text.len()>=1_000_000,"coverageNotes":errors.lines().take(12).collect::<Vec<_>>(),"overlappingRows":true}))
        },
        "inspect_location"=>{
            let path=session::inspection_path(home,run_id,args["path"].as_str().ok_or("Location required")?)?;
            let candidate=crate::cleanup_discovery::action("Inspection",path.clone(),vec![],"Inspection only");
            if session::validate_action(home,&candidate).is_err()&&crate::review_storage::risk(home,&path).is_some(){
                let item=crate::review_storage::measure(home,&path,std::time::Instant::now()+std::time::Duration::from_secs(5),&mut 50_000)?;
                if !item.partial{session::record_measurement(home,run_id,item.path.clone(),item.bytes)?;}
                session::record_review_location(home,run_id,item.clone())?;
                return serde_json::to_value(item).map_err(|e|e.to_string());
            }
            let text=session::tool_output(home,&["du".into(),"-skx".into(),path.to_string_lossy().into_owned()],None,20)?;
            let bytes=text.split_whitespace().next().and_then(|n|n.parse::<u64>().ok()).ok_or("Could not measure this location")?*1024;
            session::record_measurement(home,run_id,path.to_string_lossy().into_owned(),bytes)?;
            Ok(json!({"path":path,"bytes":bytes,"owned":fs::metadata(path).map_err(|e|e.to_string())?.uid()==unsafe{libc::getuid()}}))
        },
        "read_command"=>{
            let argv:Vec<String>=serde_json::from_value(args["argv"].clone()).map_err(|_|"Command must be argv")?;
            if argv.len()>24||!read_allowed(&argv)||argv.iter().any(|s|s.contains('\n')||s.contains('\0')){return Err("Only read-only inspection commands are available before approval".into());}
            if !run.scope.is_empty()&&!Path::new(&argv[0]).file_name().is_some_and(|name|["df","du","ls","stat"].iter().any(|allowed|name==*allowed)){return Err("Global tool/process metadata is unavailable in a scoped inspection".into());}
            for arg in &argv[1..]{if arg.starts_with('/')||arg.starts_with("~/"){if !(Path::new(&argv[0]).file_name().is_some_and(|n|n=="df")&&arg=="/"){session::inspection_path(home,run_id,arg)?;}}}
            let cwd=args["cwd"].as_str().map(|s|session::inspection_path(home,run_id,s)).transpose()?;
            Ok(json!({"output":session::tool_output(home,&argv,cwd.as_deref(),25)?}))
        },
        "verify_action"=>{let action:Action=serde_json::from_value(args["action"].clone()).map_err(|_|"Provide a complete action")?;
            for path in &action.paths{session::inspection_path(home,run_id,path)?;}
            if let Some(cwd)=&action.cwd{session::inspection_path(home,run_id,cwd)?;}
            match session::validate_action(home,&action){Ok(())=>{session::record_verification(home,run_id,&action)?;Ok(json!({"allowed":true}))},Err(reason)=>Ok(json!({"allowed":false,"reason":reason}))}
        },
        "execute_approved_action"=>execute(home,run_id,phase,args["id"].as_str().ok_or("Action ID required")?),
        _=>Err("Unknown cleanup tool".into())
    }
}
fn tree_rows(text:&str)->Vec<Value>{
    let mut rows=text.lines().filter_map(|line|{let (size,path)=line.split_once('\t')?;let bytes=size.trim().parse::<u64>().ok()?.checked_mul(1024)?;Some(json!({"path":path,"bytes":bytes}))}).collect::<Vec<_>>();
    rows.sort_by(|a,b|b["bytes"].as_u64().cmp(&a["bytes"].as_u64()).then_with(||a["path"].as_str().cmp(&b["path"].as_str())));rows
}
pub fn serve()->Result<(),String>{
    let home=system::user_home()?;let run_id=std::env::var("BREATHING_ROOM_AGENT_RUN").map_err(|_|"Missing agent session")?;
    let phase=std::env::var("BREATHING_ROOM_AGENT_PHASE").unwrap_or_else(|_|"inspect".into());
    session::tool_run(&home,&run_id)?;
    let stdin=std::io::stdin();let mut stdout=std::io::stdout().lock();
    for line in stdin.lock().lines().map_while(Result::ok){if line.len()>1_000_000{continue;}let Ok(message)=serde_json::from_str::<Value>(&line)else{continue;};
        let Some(id)=message.get("id")else{continue;};
        let result=match message["method"].as_str().unwrap_or(""){
            "initialize"=>Ok(json!({"protocolVersion":"2024-11-05","capabilities":{"tools":{}},"serverInfo":{"name":"breathing-room-cleanup","version":"1.0.0"}})),
            "ping"=>Ok(json!({})),"tools/list"=>Ok(json!({"tools":tools(&phase)})),
            "tools/call"=>{let params=&message["params"];let result=call(&home,&run_id,&phase,params["name"].as_str().unwrap_or(""),&params["arguments"]);
                let error=result.is_err();let value=result.unwrap_or_else(|e|json!({"error":e}));
                Ok(json!({"content":[{"type":"text","text":value.to_string()}],"isError":error}))
            },_=>Err("Unknown MCP method".to_string()),
        };
        let response=match result{Ok(value)=>json!({"jsonrpc":"2.0","id":id,"result":value}),Err(error)=>json!({"jsonrpc":"2.0","id":id,"error":{"code":-32601,"message":error}})};
        writeln!(stdout,"{response}").map_err(|e|e.to_string())?;stdout.flush().map_err(|e|e.to_string())?;
    }Ok(())
}

#[cfg(test)]mod tests{
    use super::*;
    #[test]fn editor_and_unknown_storage_reaches_json_without_cleanup_authority(){
        let home=fs::canonicalize(std::env::temp_dir()).unwrap().join(format!("br-editor-tool-{}-{}",std::process::id(),crate::model::now()));
        let project=home.join("Library/Application Support/so.cap.desktop/recordings/Demo.cap");
        let other=home.join("Library/Application Support/Unlisted/projects");
        fs::create_dir_all(project.join("content")).unwrap();fs::write(project.join("content/source.mp4"),vec![0;4096]).unwrap();
        fs::create_dir_all(&other).unwrap();fs::write(other.join("project.bin"),vec![0;4096]).unwrap();
        let action=crate::cleanup_discovery::action("Fixture",other.clone(),vec![],"Fixture");
        let run=session::fixture_run(&home,action,false);session::fixture_inspecting(&home,&run.id);
        let disk=call(&home,&run.id,"inspect","inspect_disk",&json!({})).unwrap();assert_eq!(disk["appStorageLocations"][0]["path"],json!(home.join("Library/Application Support")));assert!(disk["appStorageLocations"][0].get("owner").is_none());
        let result=call(&home,&run.id,"inspect","inspect_location",&json!({"path":project})).unwrap();
        assert_eq!(result["severity"],"critical");assert_eq!(result["recoverability"],"not-rebuildable");assert_eq!(result["cleanupEligible"],false);assert_eq!(result["requiresSelection"],true);
        let unknown=call(&home,&run.id,"inspect","inspect_location",&json!({"path":other})).unwrap();assert_eq!(unknown["recoverability"],"unknown");
        let overview=call(&home,&run.id,"inspect","storage_overview",&json!({})).unwrap();assert_eq!(overview["reviewLocationCount"],2);assert_eq!(overview["candidateCount"],0);assert_eq!(overview["measuredCandidateBytes"],0);
        assert!(call(&home,&run.id,"inspect","register_candidate",&json!({"path":project,"method":"trash","title":"Editor","reason":"Large","impact":"Fixture"})).is_err());
        let mut stored=session::tool_run(&home,&run.id).unwrap();assert!(stored.approved_ids.is_empty());
        let downloads=home.join("Downloads");fs::create_dir(&downloads).unwrap();stored.scope=downloads.to_string_lossy().into_owned();crate::runtime_store::save_run(&home,&stored.id,&serde_json::to_value(&stored).unwrap()).unwrap();
        let scoped=call(&home,&run.id,"inspect","inspect_disk",&json!({})).unwrap();assert_eq!(scoped["appStorageLocations"][0]["path"],json!(downloads));assert_eq!(scoped["appStorageLocations"].as_array().unwrap().len(),1);
        assert!(call(&home,&run.id,"inspect","inspect_location",&json!({"path":project})).is_err());
        assert!(project.join("content/source.mp4").exists());fs::remove_dir_all(home).unwrap();
    }
    #[test]fn agent_discovers_and_learns_without_changing_cleanup_authority(){
        let home=fs::canonicalize(std::env::temp_dir()).unwrap().join(format!("br-learn-{}-{}",std::process::id(),crate::model::now()));let path=home.join("Library/Application Support/Unlisted/Profiles/custom/Deep/More/Extra/Cache");fs::create_dir_all(&path).unwrap();fs::write(path.join("blob"),b"fixture").unwrap();
        let fixture=Action{id:"fixture".into(),title:"Fixture".into(),reason:String::new(),impact:String::new(),kind:"trash".into(),paths:vec![path.to_string_lossy().into_owned()],command:vec![],cwd:None,estimated_bytes:0,mode:"permission".into(),native_rule:String::new()};let run=session::fixture_run(&home,fixture,false);session::fixture_inspecting(&home,&run.id);
        let rule=json!({"title":"Unlisted app cache","relativePath":"Library/Application Support/Unlisted/Profiles/*/Deep/More/Extra/Cache","profiles":["everyday"],"evidencePath":path,"reason":"Observed regenerable app cache; discovery lead only"});
        assert!(call(&home,&run.id,"inspect","save_discovery_rule",&rule).is_err());
        call(&home,&run.id,"inspect","inspect_location",&json!({"path":path})).unwrap();assert_eq!(call(&home,&run.id,"inspect","save_discovery_rule",&rule).unwrap()["saved"],true);
        let registered=call(&home,&run.id,"inspect","register_candidate",&json!({"path":path,"method":"trash","title":"Unlisted cache","reason":"Measured","impact":"Quit app first; cache regenerates"})).unwrap();assert_eq!(registered["candidate"]["mode"],"permission");assert!(path.join("blob").exists());
        let found=crate::cleanup_discovery::scan(&home,"",&crate::cleanup_discovery::Options{profiles:vec!["everyday".into()],roots:vec![],..Default::default()},|_|{}).unwrap();assert!(found.candidates.iter().any(|c|c.paths==vec![path.to_string_lossy().into_owned()]));assert_eq!(found.candidates.iter().find(|c|c.paths[0]==path.to_string_lossy()).unwrap().mode,"permission");
        assert!(call(&home,&run.id,"inspect","register_candidate",&json!({"path":home,"method":"trash","title":"Whole home","reason":"Large","impact":"Delete everything"})).is_err());assert!(path.join("blob").exists());fs::remove_dir_all(home).unwrap();
    }
    #[test]fn inspection_has_no_execution_tool(){assert!(!tools("inspect").iter().any(|t|t["name"]=="execute_approved_action"));assert!(tools("execute").iter().any(|t|t["name"]=="execute_approved_action"));}
    #[test]fn developer_recent_space_leads_can_contribute_nested_cargo_candidates_without_cleanup(){
        let home=fs::canonicalize(std::env::temp_dir()).unwrap().join(format!("br-recent-cargo-{}-{}",std::process::id(),crate::model::now()));let project=home.join("code/breathing-room/src-tauri");let target=project.join("target");fs::create_dir_all(target.join("debug")).unwrap();fs::write(project.join("Cargo.toml"),b"[package]\nname=\"fixture\"\nversion=\"0.1.0\"\n").unwrap();fs::write(target.join("debug/artifact"),b"fixture build").unwrap();
        let action=crate::cleanup_discovery::action("Fixture",target.clone(),vec![],"Fixture");let mut run=session::fixture_run(&home,action,false);run.discovery_options.profiles=vec!["developer".into()];crate::runtime_store::save_run(&home,&run.id,&serde_json::to_value(&run).unwrap()).unwrap();session::fixture_inspecting(&home,&run.id);
        let disk=call(&home,&run.id,"inspect","inspect_disk",&json!({})).unwrap();assert_eq!(disk["workspaceRoots"],json!([home.join("code")]));
        let recent=call(&home,&run.id,"inspect","inspect_recent_space",&json!({"path":home.join("code"),"minBytes":0})).unwrap();assert!(recent.to_string().contains("artifact"));
        let candidate=call(&home,&run.id,"inspect","register_candidate",&json!({"path":target,"method":"trash","title":"Cargo build artifacts","reason":"Recent-space lead with native Cargo project evidence","impact":"Stop builds first; rebuild required; empty Trash to reclaim space"})).unwrap();assert_eq!(candidate["registered"],true);assert!(target.join("debug/artifact").exists());assert!(session::tool_run(&home,&run.id).unwrap().approved_ids.is_empty());fs::remove_dir_all(home).unwrap();
    }
    #[test]fn owned_custom_locations_support_review_without_expanding_cleanup_authority(){
        let temp=crate::recent_space::temporary_root().unwrap();
        let home=temp.join(format!("br-recent-home-{}-{}",std::process::id(),crate::model::now()));
        let outside=temp.join(format!("br-recent-outside-{}-{}",std::process::id(),crate::model::now()));
        fs::create_dir_all(&home).unwrap();fs::create_dir_all(&outside).unwrap();fs::write(outside.join("artifact"),b"fixture").unwrap();
        let action=crate::cleanup_discovery::action("Fixture",outside.clone(),vec![],"Fixture");let run=session::fixture_run(&home,action.clone(),false);
        assert!(call(&home,&run.id,"inspect","inspect_recent_space",&json!({"path":outside,"minBytes":0})).is_ok());
        let review=call(&home,&run.id,"inspect","inspect_location",&json!({"path":outside})).unwrap();assert_eq!(review["cleanupEligible"],false);assert_eq!(review["recoverability"],"unknown");
        assert!(session::validate_action(&home,&action).is_err());assert!(outside.join("artifact").exists());
        fs::remove_dir_all(home).unwrap();fs::remove_dir_all(outside).unwrap();
    }
    #[test]fn scoped_tools_reject_global_metadata_and_command_bypasses(){
        let home=fs::canonicalize(std::env::temp_dir()).unwrap().join(format!("br-scoped-tools-{}-{}",std::process::id(),crate::model::now()));let scope=home.join("project/dist");fs::create_dir_all(&scope).unwrap();fs::write(home.join("project/package.json"),b"{}").unwrap();
        let action=crate::cleanup_discovery::action("Fixture",scope.clone(),vec![],"Fixture");let mut run=session::fixture_run(&home,action,false);run.scope=scope.to_string_lossy().into_owned();crate::runtime_store::save_run(&home,&run.id,&serde_json::to_value(&run).unwrap()).unwrap();
        for (name,args) in [("query_tool_cache",json!({"tool":"npm"})),("inspect_tool_storage",json!({"tool":"homebrew"})),("inspect_processes",json!({})),("read_command",json!({"argv":["brew","--cache"]})),("read_command",json!({"argv":["ps","-axo","pid,comm,rss"]}))]{assert!(call(&home,&run.id,"inspect",name,&args).unwrap_err().contains("Global tool/process metadata"));}
        let disk=call(&home,&run.id,"inspect","inspect_disk",&json!({})).unwrap();assert_eq!(disk["startingLocations"],json!([scope]));
        assert_eq!(disk["recentSpaceTemporaryRoot"],Value::Null);
        assert!(call(&home,&run.id,"inspect","inspect_recent_space",&json!({"path":home})).is_err());
        assert!(call(&home,&run.id,"inspect","inspect_recent_space",&json!({"path":scope})).is_ok());
        assert!(call(&home,&run.id,"inspect","read_command",&json!({"argv":["ls","-la","--",scope],"cwd":home})).is_err());
        let outside=crate::cleanup_discovery::action("Outside",home.join("project"),vec![],"Fixture");assert!(call(&home,&run.id,"inspect","verify_action",&json!({"action":outside})).unwrap_err().contains("requested scope"));
        assert!(call(&home,&run.id,"inspect","list_locations",&json!({"path":scope})).is_ok());fs::remove_dir_all(home).unwrap();
    }
    #[test]fn inspection_rejects_shells_and_mutations(){assert!(!read_allowed(&["npm".into(),"cache".into(),"clean".into()]));assert!(!read_allowed(&["sh".into(),"-c".into(),"du ~; rm -rf ~".into()]));assert!(read_allowed(&["npm".into(),"config".into(),"get".into(),"cache".into()]));}
    #[test]fn read_commands_reject_unbounded_or_link_following_flags_and_arbitrary_formats(){
        for command in [vec!["du","-L","/Users/test"],vec!["ls","-R","/Users/test"],vec!["stat","-f","%Y","/Users/test"],vec!["which","sh"],vec!["npm","config","set","cache","/tmp/other"]]{assert!(!read_allowed(&command.into_iter().map(str::to_owned).collect::<Vec<_>>()));}
        assert!(read_allowed(&["du","-skx","/Users/test/Library/Caches"].map(str::to_owned)));
        assert!(read_allowed(&["bun","pm","cache"].map(str::to_owned)));
    }
    #[test]fn remote_tool_allowlist_excludes_execution(){assert!(!inspection_tool("execute_approved_action"));assert!(!manifest().iter().any(|tool|tool["name"]=="execute_approved_action"));}
    #[test]fn frozen_review_retains_the_deployed_six_tool_contract(){assert_eq!(review_manifest().len(),6);assert!(manifest().iter().any(|tool|tool["name"]=="inspect_recent_space"));assert!(review_manifest().iter().all(|tool|inspection_tool(tool["name"].as_str().unwrap())));}
    #[test]fn tree_sizes_are_ranked_and_preserve_paths_with_spaces(){
        let rows=tree_rows("4\t/fixture/small\n2048\t/fixture/large cache\nnot-a-size\t/fixture/unavailable\n");
        assert_eq!(rows.len(),2);assert_eq!(rows[0]["path"],"/fixture/large cache");assert_eq!(rows[0]["bytes"],2097152);
    }
    #[test]fn paginated_discovery_reaches_entries_beyond_first_hundred(){
        let home=fs::canonicalize(std::env::temp_dir()).unwrap().join(format!("breathing-list-fixture-{}",std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).unwrap().as_nanos()));
        let root=home.join("Library/Caches");fs::create_dir_all(&root).unwrap();
        for i in 0..130{fs::create_dir(root.join(format!("cache-{i:03}"))).unwrap();}
        let action=Action{id:"fixture".into(),title:"Fixture".into(),reason:String::new(),impact:String::new(),kind:"trash".into(),paths:vec![root.join("cache-129").to_string_lossy().into_owned()],command:vec![],cwd:None,estimated_bytes:0,mode:"permission".into(),native_rule:String::new()};
        let run=session::fixture_run(&home,action,false);
        let first=call(&home,&run.id,"inspect","list_locations",&json!({"path":root})).unwrap();assert_eq!(first["nextOffset"],100);assert_eq!(first["entries"].as_array().unwrap().len(),100);
        let second=call(&home,&run.id,"inspect","list_locations",&json!({"path":root,"offset":100})).unwrap();assert_eq!(second["nextOffset"],Value::Null);assert_eq!(second["entries"].as_array().unwrap().len(),30);assert_eq!(second["entries"][29]["name"],"cache-129");
        fs::remove_dir_all(home).unwrap();
    }
    #[test]fn mutations_require_the_approved_id_and_cannot_replay(){
        let root=fs::canonicalize(std::env::temp_dir()).unwrap().join(format!("breathing-agent-fixture-{}",std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).unwrap().as_nanos()));
        let target=root.join("Library/Caches/fixture");fs::create_dir_all(&target).unwrap();fs::write(target.join("cache.bin"),b"fixture").unwrap();
        let action=Action{id:"fixture-cache".into(),title:"Fixture cache".into(),reason:"Temporary test data".into(),impact:"Fixture only".into(),kind:"trash".into(),paths:vec![target.to_string_lossy().into_owned()],command:vec![],cwd:None,estimated_bytes:7,mode:"permission".into(),native_rule:String::new()};
        let unapproved=session::fixture_run(&root,action.clone(),false);
        assert!(execute(&root,&unapproved.id,"inspect",&action.id).is_err());assert!(target.exists());
        let approved=session::fixture_run(&root,action.clone(),true);
        assert!(execute(&root,&approved.id,"execute","different-id").is_err());assert!(target.exists());
        assert_eq!(execute(&root,&approved.id,"execute",&action.id).unwrap()["ok"],true);assert!(!target.exists());
        assert_eq!(execute(&root,&approved.id,"execute",&action.id).unwrap()["alreadyAttempted"],true);
        assert_eq!(fs::read_dir(root.join(".Trash")).unwrap().count(),1);
        fs::remove_dir_all(root).unwrap();
    }
    #[test]fn concurrent_approved_calls_claim_the_action_once(){
        let root=fs::canonicalize(std::env::temp_dir()).unwrap().join(format!("breathing-concurrent-fixture-{}",std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).unwrap().as_nanos()));
        let target=root.join("Library/Caches/fixture");fs::create_dir_all(&target).unwrap();fs::write(target.join("owned.txt"),b"fixture").unwrap();
        let action=Action{id:"fixture".into(),title:"Fixture".into(),reason:"Owned test data".into(),impact:"Fixture only".into(),kind:"trash".into(),paths:vec![target.to_string_lossy().into_owned()],command:vec![],cwd:None,estimated_bytes:7,mode:"permission".into(),native_rule:String::new()};
        let run=session::fixture_run(&root,action,true);
        let threads=(0..2).map(|_|{let h=root.clone();let id=run.id.clone();std::thread::spawn(move||execute_local(&h,&id,"fixture").unwrap())}).collect::<Vec<_>>();
        let results=threads.into_iter().map(|thread|thread.join().unwrap()).collect::<Vec<_>>();
        assert_eq!(results.iter().filter(|reply|reply["alreadyAttempted"]==true).count(),1);
        assert_eq!(fs::read_dir(root.join(".Trash")).unwrap().count(),1);assert_eq!(session::tool_run(&root,&run.id).unwrap().outcomes.len(),1);
        fs::remove_dir_all(root).unwrap();
    }
    #[test]fn failed_action_preserves_originals_and_does_not_prevent_next_approved_action(){
        let home=fs::canonicalize(std::env::temp_dir()).unwrap().join(format!("br-independent-{}",std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).unwrap().as_nanos()));
        let original=home.join("Documents/original");let cache=home.join("Library/Caches/fixture");
        for path in [&original,&cache]{fs::create_dir_all(path).unwrap();fs::write(path.join("data"),b"fixture").unwrap();}
        let first=Action{id:"rejected".into(),title:"Original".into(),reason:String::new(),impact:String::new(),kind:"trash".into(),paths:vec![original.to_string_lossy().into_owned()],command:vec![],cwd:None,estimated_bytes:0,mode:"permission".into(),native_rule:String::new()};
        let mut second=first.clone();second.id="cache".into();second.paths=vec![cache.to_string_lossy().into_owned()];
        let run=session::fixture_run(&home,first,true);session::fixture_add_approved(&home,&run.id,second);
        let rejected=execute_local(&home,&run.id,"rejected").unwrap();let cleaned=execute_local(&home,&run.id,"cache").unwrap();
        assert_eq!(rejected["status"],"failed");assert_eq!(rejected["percentCleaned"],0.0);assert!(original.join("data").exists());
        assert_eq!(cleaned["status"],"success");assert_eq!(cleaned["percentCleaned"],100.0);assert!(cleaned["pendingTrashBytes"].as_u64().unwrap()>0);assert!(!cache.exists());
        assert_eq!(session::tool_run(&home,&run.id).unwrap().outcomes.len(),2);fs::remove_dir_all(home).unwrap();
    }
}
