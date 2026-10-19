//! Read-only conversational tools. No cleanup session, signals or configuration changes.
use crate::{model::now, system};
use serde_json::{json, Value};
use std::path::Path;

pub(crate) fn inspect(home:&Path,name:&str,args:&Value)->Result<Value,String>{
    match name{
        "inspect_memory"=>{
            let vm=system::output("/usr/bin/vm_stat",&[],5)?;
            let total=system::output("/usr/sbin/sysctl",&["-n","hw.memsize"],5)?.trim().parse::<u64>().map_err(|_|"Physical RAM unavailable")?;
            let physical_used=physical_used_bytes(total,&vm);
            let swap=system::output("/usr/sbin/sysctl",&["vm.swapusage"],5).ok();
            let pressure=system::output("/usr/sbin/sysctl",&["-n","kern.memorystatus_vm_pressure_level"],5).ok();
            let mut processes=crate::processes::sample()?;processes.sort_by(|a,b|b.memory_bytes.cmp(&a.memory_bytes));
            Ok(json!({"timestamp":now(),"physicalTotalBytes":total,"physicalUsedBytes":physical_used,"physicalAvailableBytes":physical_used.map(|used|total.saturating_sub(used)),"vmCounters":vm,"swap":swap,"pressureLevel":pressure.map(|v|v.trim().to_owned()),"pressureLegend":{"1":"normal","2":"warning","4":"critical"},"largestProcesses":processes.into_iter().take(20).map(|p|json!({"pid":p.pid,"name":p.name,"rssBytes":p.memory_bytes})).collect::<Vec<_>>(),"note":"Use physicalUsedBytes for physical RAM occupancy: anonymous minus purgeable + wired + compressor pages, matching the app's live metrics. Do not substitute active+wired, omit compression, or sum process RSS. Process RSS may double-count shared pages; available RAM includes reclaimable file cache."}))
        },
        "inspect_cpu"=>{
            let text=system::output("/usr/bin/top",&["-l","2","-s","1","-n","15","-o","cpu","-stats","pid,command,cpu,mem"],8)?;
            Ok(json!({"timestamp":now(),"coreCount":std::thread::available_parallelism().map(|n|n.get()).ok(),"sampleSeconds":1,"sample":last_top_sample(&text),"note":"Second top sample over a one-second interval, not cumulative CPU time. Per-process 100% is one core; system CPU utilization is across all cores. This is a short snapshot, not proof of a sustained problem."}))
        },
        "inspect_recent_files"=>{
            let path=args["path"].as_str().map(str::to_owned).unwrap_or_else(||home.to_string_lossy().into_owned());
            crate::recent_space::metadata(home,&path,&json!({"hours":args["hours"].as_u64().unwrap_or(24),"seconds":5,"maxEntries":50000,"limit":20}))
        },
        _=>Err("Unknown read-only system tool".into())
    }
}
fn last_top_sample(text:&str)->&str{let start=text.match_indices("Processes:").last().map(|(index,_)|index).unwrap_or(0);&text[start..]}
fn physical_used_bytes(total:u64,text:&str)->Option<u64>{
    let page_size=text.lines().next()?.split("page size of ").nth(1)?.split_whitespace().next()?.parse::<u64>().ok()?;
    let pages=|label:&str|text.lines().find_map(|line|{let (key,value)=line.split_once(':')?;(key.trim()==label).then(||value.trim().trim_end_matches('.').parse::<u64>().ok()).flatten()});
    if total==0||page_size==0{return None;}
    pages("Anonymous pages")?.saturating_sub(pages("Pages purgeable")?).checked_add(pages("Pages wired down")?)?.checked_add(pages("Pages occupied by compressor")?)?.checked_mul(page_size).map(|bytes|bytes.min(total))
}
#[cfg(test)]mod tests{
    #[test]fn cpu_uses_second_interval_sample(){assert_eq!(super::last_top_sample("Processes: first\nCPU usage: 90%\nProcesses: second\nCPU usage: 10%"),"Processes: second\nCPU usage: 10%");}
    #[test]fn physical_memory_uses_nonpurgeable_anonymous_wired_and_compressed_pages(){
        let vm="Mach Virtual Memory Statistics: (page size of 100 bytes)\nAnonymous pages: 80.\nPages purgeable: 10.\nPages wired down: 20.\nPages occupied by compressor: 10.\nPages active: 9999.\n";
        assert_eq!(super::physical_used_bytes(16000,vm),Some(10000));assert_eq!(super::physical_used_bytes(0,vm),None);assert_eq!(super::physical_used_bytes(16000,"unavailable"),None);
    }
    #[cfg(target_os="macos")]
    #[test]fn live_system_tools_return_measured_counters_without_mutation(){
        let home=crate::system::user_home().unwrap();let memory=super::inspect(&home,"inspect_memory",&serde_json::json!({})).unwrap();assert!(memory["physicalTotalBytes"].as_u64().unwrap()>0);assert!(memory["physicalUsedBytes"].as_u64().unwrap()>0);assert!(memory["vmCounters"].as_str().unwrap().contains("page size"));
        let cpu=super::inspect(&home,"inspect_cpu",&serde_json::json!({})).unwrap();assert_eq!(cpu["sampleSeconds"],1);assert!(cpu["sample"].as_str().unwrap().contains("CPU usage"));
    }
}
