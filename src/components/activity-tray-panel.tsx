import { useCallback, useEffect, useRef, useState, type ReactNode } from "react";
import { invoke } from "@tauri-apps/api/core";
import { listen } from "@tauri-apps/api/event";
import { Activity, ArrowUpRight, Bell, ExternalLink, MemoryStick, Pause, Pin, Play, Radio, X } from "lucide-react";
import { api, native } from "@/lib/api";
import { formatBytes } from "@/lib/model";
import { type ActivityLog, initialMonitorConfig } from "@/lib/live";
import { ActivityRow, DiskTimeline } from "./activity-page";
import { Sparkline } from "./live-status";
import { panelNavigationUrl, type PanelNavigation } from "@/lib/panel-navigation";
import { useMetrics } from "@/hooks/use-metrics";
import { memoryUsage, memoryTrend } from "@/lib/memory";

export default function ActivityTrayPanel() {
  const status=useMetrics();const [log,setLog]=useState<ActivityLog|null>(null);
  const [pinned,setPinned]=useState(false);const [visible,setVisible]=useState(!native);
  const [filter,setFilter]=useState("all");const [error,setError]=useState("");
  const busy=useRef(false);const lastFeed=useRef("");const config=status?.config??initialMonitorConfig;
  const memory=config.enabled?memoryUsage(status):null;
  const refresh=useCallback(async()=>{
    if(busy.current)return;busy.current=true;
    try{const live=await api.live();
      const key=`${live.timestamp}:${filter}`;
      if(lastFeed.current!==key){const feed=await api.activityLog(filter,"");setLog(feed);lastFeed.current=key;}
      setError("");
    }catch(e){setError(String(e));}finally{busy.current=false;}
  },[filter]);
  useEffect(()=>{
    if(!native)return;
    let active=true;let unlisten:(()=>void)|undefined;
    const update=(state:{pinned:boolean;visible:boolean})=>{if(active){setPinned(state.pinned);setVisible(state.visible);}};
    void (async()=>{try{
      const stop=await listen<{pinned:boolean;visible:boolean}>("activity-panel-state",event=>update(event.payload));
      if(!active){stop();return;}unlisten=stop;
      update(await invoke("activity_panel_state"));
    }catch(e){if(active)setError(String(e));}})();
    return()=>{active=false;unlisten?.();};
  },[]);
  useEffect(()=>{
    if(!visible)return;
    void refresh();const timer=setInterval(()=>void refresh(),1000);
    return()=>clearInterval(timer);
  },[visible,refresh]);
  const action=async(command:string,args?:Record<string,unknown>)=>{try{if(native)await invoke(command,args);}catch(e){setError(String(e));}};
  const navigate=async(destination:PanelNavigation)=>{
    if(native)await action("open_activity_main",{destination});
    else window.location.assign(panelNavigationUrl(destination));
  };
  const route=(destination:PanelNavigation,children:ReactNode,className:string,label:string)=><a href={panelNavigationUrl(destination)} className={className} aria-label={label} title={label} onClick={event=>{if(native){event.preventDefault();void navigate(destination);}}}>{children}</a>;
  useEffect(()=>{const escape=(e:KeyboardEvent)=>{if(e.key==="Escape"&&native)void invoke("dismiss_activity_panel");};window.addEventListener("keydown",escape);return()=>window.removeEventListener("keydown",escape);},[]);
  const toggleMonitor=async()=>{try{const live=await api.live();await api.configureMonitor({...live.config??config,enabled:!live.config?.enabled});await refresh();}catch(e){setError(String(e));}};
  return <main className="tray-activity" aria-label="Activity panel" data-visible={visible}>
    <header className="tray-header">{route({page:"activity"},<><Activity size={20}/><span><h1>Activity</h1><small>{!native?"Example activity":config.enabled?"Watching your Mac":"Monitoring paused"}</small></span></>,"tray-brand tray-route","Open Activity in main app")}
      <div><button className={`icon-button ${pinned?"tray-pinned":""}`} aria-label={pinned?"Unpin panel":"Pin panel"} aria-pressed={pinned} onClick={()=>{setPinned(!pinned);void action("pin_activity_panel",{pinned:!pinned});}}><Pin size={17}/></button><button className="icon-button" aria-label="Dismiss Activity" onClick={()=>void action("dismiss_activity_panel")}><X size={18}/></button></div>
    </header>
    <div className="tray-scroll">
      {error&&<p className="cleanup-error" role="alert">{error}</p>}
      {(status?.processError||status?.databaseError||status?.watchError)&&<p className="activation-note">{status.processError||status.databaseError||status.watchError}</p>}
      {!!status?.anomalies?.length&&<section className="tray-anomalies" aria-label="High usage"><h2><Bell size={17}/>High usage detected</h2>{status.anomalies.map(a=><article key={a.id}>{route(a.kind==="cpu"?{page:"apps",search:a.name,appId:a.path}:{page:"activity",search:a.name,section:"writers"},<><strong>{a.name}</strong><span>{a.kind==="cpu"?`${a.value.toFixed(0)}% CPU`:`${formatBytes(a.value)}/s writes`}</span><p>{a.value<a.threshold?"Usage settling after exceeding":"Exceeded"} {a.kind==="cpu"?`${a.threshold.toFixed(0)}%`:`${formatBytes(a.threshold)}/s`} for at least {config.alerts.sustainedSeconds}s</p></>,"tray-anomaly-route tray-route",`View ${a.name} ${a.kind==="cpu"?"in Apps":"disk activity"}`)}</article>)}</section>}
      <section className="tray-metrics" aria-label="Live metrics"><div>{route({page:"apps"},<><span><Activity size={14}/>System CPU</span><strong>{status?.cpuPercent!=null?`${status.cpuPercent.toFixed(0)}%`:"—"}</strong><Sparkline values={status?.history?.map(p=>p.cpuPercent??0)??[]} color="#a079ef"/></>,"tray-metric-route tray-route","View CPU usage in Apps")}</div><div>{route({page:"apps"},<><span><MemoryStick size={14}/>RAM</span><strong>{memory?`${memory.percent.toFixed(0)}%`:"—"}</strong><small>{memory?`${formatBytes(memory.used)} / ${formatBytes(memory.total)}`:"Memory unavailable"}</small><Sparkline values={config.enabled?memoryTrend(status):[]} color="#16a085"/></>,"tray-metric-route tray-route","View memory usage in Apps")}</div><div>{route({page:"activity",section:"writers"},<><span><ArrowUpRight size={14}/>Disk writes</span><strong>{status?.writeBytesPerSecond!=null?`${formatBytes(status.writeBytesPerSecond)}/s`:"—"}</strong></>,"tray-metric-route tray-route","View apps writing to disk")}{route({page:"space"},<small>{status?.availableBytes!=null?`${formatBytes(status.availableBytes)} free`:"Waiting for a sample"}</small>,"tray-route","View available disk space")}</div></section>
      {!!status?.topCpuApps?.length&&route({page:"apps",search:status.topCpuApps[0].name,appId:status.topCpuApps[0].path},<><span>Highest app CPU</span><strong>{status.topCpuApps[0].name} <b>{status.topCpuApps[0].cpu.toFixed(0)}%</b></strong><small>100% = one core · observed helpers included</small></>,"tray-top-app tray-route",`View ${status.topCpuApps[0].name} in Apps`)}
      <div className="tray-minute"><span>Last minute</span>{route({page:"apps"},<b>+{status?.minute?.appsStarted??0} apps</b>,"tray-route","View running apps")}{route({page:"activity",filter:"files",section:"feed"},<b>+{(status?.minute?.filesCreated??0)+(status?.minute?.fileChanges??0)} changes</b>,"tray-route","View file changes")}{route({page:"activity",filter:"files",section:"feed"},<b>+{status?.minute?.foldersCreated??0} folders</b>,"tray-route","View folder activity")}</div>
      {route({page:"space"},<DiskTimeline samples={log?.diskHistory??[]}/>,"tray-timeline-route tray-route","View disk space in main app")}
      <div className="tray-feed-heading">{route({page:"activity",filter:filter as PanelNavigation["filter"],section:"feed"},<h2>Recent activity</h2>,"tray-route","View full activity feed")}<select aria-label="Filter activity" value={filter} onChange={e=>setFilter(e.target.value)}><option value="all">All</option><option value="files">Files & folders</option><option value="processes">Processes</option></select></div>
      <div className="activity-feed panel">{log?.events.slice(0,20).map(event=>{
        const open=()=>void navigate({page:"activity",eventId:event.id,search:event.path||event.owner,filter:"all",section:"feed"});
        return <ActivityRow key={event.id} event={event} expanded={false} toggle={open} open={open}/>;
      })}{!log?.events.length&&<div className="empty-state"><Radio size={22}/><p>{config.enabled?"Listening for changes…":"Monitoring paused"}</p></div>}</div>
    </div>
    <footer className="tray-footer"><button className="icon-button" aria-label={config.enabled?"Pause monitoring":"Resume monitoring"} onClick={()=>void toggleMonitor()}>{config.enabled?<Pause size={16}/>:<Play size={16}/>}</button>{route({page:"activity",settings:true},<><Bell size={14}/>Alert settings</>,"text-button tray-route","Open alert settings")}{route({page:"activity"},<>Full Activity <ExternalLink size={14}/></>,"text-button tray-route","Open full Activity")}</footer>
  </main>;
}
