fn main() {
    let args: Vec<String> = std::env::args().collect();
    match args.get(1).map(String::as_str) {
        Some("assistant-ask")=>match breathing_room_lib::remote_agent::ask(args.get(2).cloned().unwrap_or_else(||"What can you help with?".into())){Ok(reply)=>println!("{reply}"),Err(error)=>{eprintln!("{error}");std::process::exit(1);}},
        Some("agent-ledger")=>match breathing_room_lib::runtime_store::stats(){Ok(value)=>println!("{value}"),Err(error)=>{eprintln!("{error}");std::process::exit(1);}},
        Some("agent-login")=>match breathing_room_lib::remote_agent::auth_start(args.get(2).cloned().unwrap_or_else(||"google".into())){
            Ok(login)=>{println!("Complete sign-in in your browser. The app will receive the result automatically.");let id=login["id"].as_str().unwrap().to_owned();loop{match breathing_room_lib::remote_agent::auth_poll(id.clone()){Ok(value)if value["status"]=="pending"=>std::thread::sleep(std::time::Duration::from_secs(2)),Ok(_)=>{println!("Signed in to Breathing Room.");break;},Err(error)=>{eprintln!("{error}");std::process::exit(1);}}}},Err(error)=>{eprintln!("{error}");std::process::exit(1);}
        },
        Some("disk-map-cache") => match breathing_room_lib::disk_map_cache::load() {
            Ok(report)=>println!("{}",serde_json::json!({"cached":report.is_some(),"scannedAt":report.as_ref().and_then(|r|r["scannedAt"].as_u64()),"directories":report.as_ref().and_then(|r|r["directories"].as_array()).map(Vec::len)})),
            Err(error)=>{eprintln!("{error}");std::process::exit(1);}
        },
        #[cfg(feature = "gui")]
        Some("map-disk") => match breathing_room_lib::assistant::packaged_space() {
            Ok(report)=>println!("{}",serde_json::json!({"scannedAt":report["scannedAt"],"directories":report["directories"].as_array().map(Vec::len),"partial":report["partial"],"warnings":report["warnings"]})),
            Err(error)=>{eprintln!("{error}");std::process::exit(1);}
        },
        Some("cleanup-agent-tools") => { if let Err(error)=breathing_room_lib::cleanup_session::mcp(){eprintln!("{error}");std::process::exit(1);} },
        Some("agent-connection") => println!("{}",breathing_room_lib::cleanup_session::connection()),
        Some("agent-discover")=>{
            let result=breathing_room_lib::cleanup_session::discover_only(args.get(2).map(String::as_str).unwrap_or("everyday,developer,builder,creator"),args.get(3).map(String::as_str).unwrap_or(""));match result{Ok(value)=>println!("{value}"),Err(error)=>{eprintln!("{error}");std::process::exit(1);}}
        },
        Some("agent-inspect") => match breathing_room_lib::cleanup_session::inspect(args.get(2).cloned().unwrap_or_else(||"Inspect disk caches and propose safe cleanup; do not change files.".into()),args.get(4).cloned().unwrap_or_default(),args.get(3).cloned().unwrap_or_else(||"@cf/qwen/qwen3-30b-a3b-fp8".into())) {
            Ok(id)=>{println!("{id}");loop{match breathing_room_lib::cleanup_session::state(id.clone()){Ok(run) if run.status=="inspecting"=>std::thread::sleep(std::time::Duration::from_millis(200)),Ok(run)=>{println!("{}",serde_json::to_string(&run).unwrap());break;},Err(error)=>{eprintln!("{error}");break;}}}},Err(error)=>{eprintln!("{error}");std::process::exit(1);}
        },
        Some("agent-state") => match breathing_room_lib::cleanup_session::state(args.get(2).cloned().unwrap_or_default()) {
            Ok(run)=>println!("{}",serde_json::to_string(&run).unwrap()),Err(error)=>{eprintln!("{error}");std::process::exit(1);}
        },
        Some("agent-cancel") => {let _=breathing_room_lib::cleanup_session::cancel(args.get(2).cloned().unwrap_or_default());},
        #[cfg(feature = "gui")]
        Some("capabilities") => println!("{}", breathing_room_lib::capabilities()),
        #[cfg(feature = "gui")]
        Some("monitor-check") => match breathing_room_lib::monitor::diagnostic() {
            Ok(value) => println!("{}", serde_json::to_string_pretty(&value).unwrap()),
            Err(error) => { eprintln!("{error}"); std::process::exit(1); }
        },
        #[cfg(feature = "gui")]
        Some("cleanup-discover") | Some("cleanup-catalog") => {
            let mut script_args = vec![if args[1] == "cleanup-catalog" { "catalog".into() } else { "discover".into() }];
            script_args.extend(args.iter().skip(2).cloned());
            match breathing_room_lib::assistant::packaged_cli(&script_args) {
                Ok(value) => println!("{}", value),
                Err(error) => { eprintln!("{error}"); std::process::exit(1); }
            }
        }
        Some("scan") => {
            let mut settings = breathing_room_lib::model::Settings::default();
            settings.scan_paths = args.iter().skip(2).cloned().collect();
            match breathing_room_lib::storage::scan(&settings, &std::sync::atomic::AtomicBool::new(false)) {
                Ok(report) => println!("{}", serde_json::to_string_pretty(&report).unwrap()),
                Err(error) => { eprintln!("{error}"); std::process::exit(1); }
            }
        }
        Some("apps") => match breathing_room_lib::processes::groups() {
            Ok(report) => println!("{}", serde_json::to_string_pretty(&report).unwrap()),
            Err(error) => { eprintln!("{error}"); std::process::exit(1); }
        },
        Some(_) => println!("Breathing Room\n  scan [home-folder-paths…] — bounded read-only storage scan\n  apps — read-only app/process groups\n  no arguments — desktop app"),
        None => {
            #[cfg(feature = "gui")]
            breathing_room_lib::run();
            #[cfg(not(feature = "gui"))]
            println!("Use scan or apps; build with the gui feature for the desktop app.");
        }
    }
}
