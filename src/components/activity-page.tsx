import { useCallback, useEffect, useRef, useState } from "react";
import { Activity, ArrowDownLeft, ArrowUpRight, Check, ChevronDown, Code2, ExternalLink, FilePlus2, FolderPlus, Gauge, LoaderCircle, Pause, Play, Radio, Rocket, Search, Settings2, Sparkles, Trash2 } from "lucide-react";
import { api, native } from "@/lib/api";
import { initialMonitorConfig, type ActivityEntry, type ActivityLog, type LiveStatus } from "@/lib/live";
import { formatBytes } from "@/lib/model";
import { Button } from "./ui/button";
import { UsageBar } from "./charts";
import { AlertSettings } from "./alert-settings";
import type { PanelNavigation } from "@/lib/panel-navigation";
import { scrollPanelDestination } from "@/lib/panel-scroll";

const kinds: Record<string,{name:string;icon:typeof Activity;color:string}>={
  app_started:{name:"App started",icon:Rocket,color:"violet"},process_started:{name:"Process started",icon:Play,color:"violet"},process_exited:{name:"Process exited",icon:Pause,color:"blue"},
  file_created:{name:"File created",icon:FilePlus2,color:"mint"},file_changed:{name:"File changed",icon:Code2,color:"blue"},folder_created:{name:"Folder created",icon:FolderPlus,color:"orange"},
  removed:{name:"Removed",icon:Trash2,color:"orange"},renamed:{name:"Renamed",icon:ArrowUpRight,color:"blue"},metadata_changed:{name:"Metadata changed",icon:Activity,color:"blue"},
  process_io:{name:"Process I/O",icon:ArrowUpRight,color:"mint"},coverage_gap:{name:"Coverage gap",icon:Radio,color:"orange"},
};
export function ActivityPage({status,onRefresh,onReview,navigation,navigationRequest=0}:{status:LiveStatus|null;onRefresh:()=>void;onReview:(path:string)=>void;navigation?:PanelNavigation;navigationRequest?:number}) {
  const [log,setLog]=useState<ActivityLog|null>(null);
  const [filter,setFilter]=useState(navigation?.filter??"all");const [search,setSearch]=useState(navigation?.search??"");const [debounced,setDebounced]=useState(navigation?.search??"");
  const [error,setError]=useState("");const [saving,setSaving]=useState(false);const [expanded,setExpanded]=useState<number|null>(navigation?.eventId??null);
  const queryVersion=useRef(0);
  const config=status?.config??initialMonitorConfig;
  useEffect(()=>{
    if(!navigation)return;
    setFilter(navigation.filter??"all");setSearch(navigation.search??"");setDebounced(navigation.search??"");setExpanded(navigation.eventId??null);
  },[navigation,navigationRequest]);
  useEffect(()=>{
    if(!navigation)return;
    const id=navigation.eventId?`activity-event-${navigation.eventId}`:navigation.settings?"activity-alert-settings":navigation.section?`activity-${navigation.section}`:null;
    const target=id?document.getElementById(id):null;
    if(target instanceof HTMLDetailsElement)target.open=true;
    return scrollPanelDestination(id?()=>document.getElementById(id):undefined);
  },[navigation,navigationRequest,log!==null,log?.events.some(e=>e.id===navigation?.eventId)]);
  useEffect(()=>{const timer=setTimeout(()=>setDebounced(search),250);return()=>clearTimeout(timer);},[search]);
  const refresh=useCallback(async()=>{const version=++queryVersion.current;try{const result=await api.activityLog(filter,debounced);if(version===queryVersion.current){setLog(result);setError("");}}catch(e){if(version===queryVersion.current)setError(String(e));}},[filter,debounced]);
  useEffect(()=>{void refresh();const timer=setInterval(()=>{if(document.visibilityState==="visible")void refresh();},5000);return()=>{queryVersion.current++;clearInterval(timer);};},[refresh]);
  const configure=async(next:typeof config)=>{setSaving(true);try{await api.configureMonitor(next);onRefresh();}catch(e){setError(String(e));}finally{setSaving(false);}};
  const loadMore=async()=>{if(!log?.events.length)return;try{const next=await api.activityLog(filter,debounced,log.events[log.events.length-1].id);setLog({...next,events:[...log.events,...next.events]});}catch(e){setError(String(e));}};
  return <section className="activity-page">
    <div className="page-heading"><div><h1>Your Mac, in motion.</h1><p>See what starts, what changes, and where space grows.</p></div><Button variant="outline" className="big-button" disabled={saving} onClick={()=>void configure({...config,enabled:!config.enabled})}>{saving?<LoaderCircle className="spin"/>:config.enabled?<Pause/>:<Play/>}{config.enabled?"Pause monitoring":"Resume monitoring"}</Button></div>
    <div className="activity-story-row"><Story icon={Rocket} color="violet" count={status?.minute?.appsStarted??0} label="apps started" detail={`${status?.minute?.processesStarted??0} new processes`}/><Story icon={FilePlus2} color="blue" count={(status?.minute?.filesCreated??0)+(status?.minute?.fileChanges??0)} label="file changes" detail={`${status?.minute?.filesCreated??0} creations observed`}/><Story icon={FolderPlus} color="orange" count={status?.minute?.foldersCreated??0} label="new folders" detail="In the last minute"/><Story icon={ArrowUpRight} color="mint" count={null} value={status?.writeBytesPerSecond!=null?`${formatBytes(Math.round(status.writeBytesPerSecond))}/s`:"—"} label="observed writes" detail={`${status?.sampledIoProcesses??0} process counters`}/></div>
    {error&&<div className="cleanup-error" role="alert">{error}</div>}
    {(status?.watchError||status?.databaseError||status?.processError)&&<div className="activation-note">{status.watchError||status.databaseError||status.processError}</div>}
    <AlertSettings config={config} onSaved={onRefresh}/>
    <details className="activity-monitor-settings"><summary><Settings2 size={17}/>Monitoring & storage <ChevronDown size={16}/></summary>
      <div className="monitor-control-grid"><label className="toggle-row"><input type="checkbox" checked={config.fileEvents} disabled={saving} onChange={e=>void configure({...config,fileEvents:e.target.checked})}/><span>Individual file events <small>Turn off for lighter folder-only notifications</small></span></label><label className="toggle-row"><input type="checkbox" checked={config.processIo} disabled={saving} onChange={e=>void configure({...config,processIo:e.target.checked})}/><span>Sample process disk I/O <small>Observed counters, not per-file writer identity</small></span></label><label className="field-label">Sampling interval<select aria-label="Sampling interval" value={config.intervalSeconds} disabled={saving} onChange={e=>void configure({...config,intervalSeconds:Number(e.target.value)})}><option value={5}>5 seconds · live</option><option value={15}>15 seconds · lighter</option></select></label></div>
      <div className="monitor-resource-pills"><span><Gauge size={14}/>{status?.monitorCpuPercent?.toFixed(1)??"—"}% app CPU · one core</span><span>{formatBytes(status?.monitorMemoryBytes??0)} app RSS</span><span>{status?.sampleMs?.toFixed(0)??"—"} ms per sample</span><span>{status?.dropped??0} dropped notifications</span></div>
      <p>{status?.watching?"Watching the Data volume":"Filesystem watcher paused or unavailable"}. Seven-day retention, bounded queues, at most 50,000 events. Reads and short-lived processes may be missed; filesystem changes may be coalesced. Path-based ownership is inferred.</p><code className="source-url">{status?.databasePath??"Local activity.sqlite"}</code>
    </details>
    <div id="activity-timeline"><DiskTimeline samples={log?.diskHistory??[]}/></div>
    <div className="activity-insights-grid"><section className="panel activity-insights"><div className="panel-heading"><h2>Where space grew</h2><FilePlus2 size={20}/></div><p>Observed allocation increases · last 24 hours</p>{log?.growth.length?log.growth.map(group=><div className="growth-row" key={`${group.owner}:${group.workflow}`}><span className="app-icon violet"><FolderPlus size={23}/></span><div><strong>{group.workflow}</strong><small>{group.owner} · inferred from path</small><UsageBar value={group.bytes} maximum={Math.max(...log.growth.map(g=>g.bytes))} color="#9c78e8"/></div><strong>+{formatBytes(group.bytes)}</strong><button className="icon-button" aria-label={`Ask the agent about growth in ${group.workflow}`} onClick={()=>onReview(group.path)}><Sparkles size={18}/></button></div>):<div className="empty-state">Growth appears after files are observed and change. New creations use an estimated zero baseline.</div>}</section>
      <section id="activity-writers" className="panel activity-insights"><div className="panel-heading"><h2>Apps writing to disk</h2><ArrowUpRight size={20}/></div><p>Sampled write-counter increases · last hour</p>{log?.writers.length?log.writers.map(group=><div className="growth-row" key={group.owner}><span className="app-icon mint"><Activity size={23}/></span><div><strong>{group.owner}</strong><small>{group.events} I/O samples</small><UsageBar value={group.bytes} maximum={log.writers[0].bytes} color="#21af97"/></div><strong>{formatBytes(group.bytes)}</strong></div>):<div className="empty-state">Writing apps appear after two successful counter samples.</div>}<p className="metric-note">An app’s I/O counter does not prove it wrote a particular file.</p></section></div>
    <div className="section-heading"><h2>Live activity</h2><span>{log?.storedEvents.toLocaleString()??0} stored events · {native?"local SQLite":"example data"}</span></div>
    <div className="apps-toolbar"><label className="search-field"><Search size={20}/><input value={search} onChange={e=>setSearch(e.target.value)} placeholder="Find an app, folder, or workflow" aria-label="Search activity"/></label><div className="segmented">{(["all","files","processes"] as const).map(f=><button key={f} className={filter===f?"selected":""} aria-pressed={filter===f} onClick={()=>setFilter(f)}>{f==="all"?"All activity":f==="files"?"Files & folders":"Processes"}</button>)}</div></div>
    <div id="activity-feed" className="activity-feed panel">{log?.events.map(event=><ActivityRow key={event.id} event={event} expanded={expanded===event.id} toggle={()=>setExpanded(expanded===event.id?null:event.id)} review={()=>onReview(event.path)}/>)}{!log?.events.length&&<div className="empty-state"><Radio size={28}/><h3>{config.enabled?"Listening for changes…":"Monitoring paused"}</h3><p>Activity is recorded from now, while this app is running.</p></div>}</div>
    {!!log?.events.length&&<Button variant="outline" className="big-button" onClick={loadMore}>Load older activity</Button>}
  </section>;
}
function Story({icon:Icon,color,count,value,label,detail}:{icon:typeof Activity;color:string;count:number|null;value?:string;label:string;detail:string}) {
  return <div className={`activity-story story-${color}`}><span className={`story-icon-ring ${color}`}><Icon size={25}/></span><div><strong>{count===null?value:`+${count}`}</strong><span>{label}</span><small>{detail}</small></div></div>;
}
export function DiskTimeline({samples}:{samples:ActivityLog["diskHistory"]}) {
  const values=samples.map(s=>s.availableBytes);
  const low=Math.min(...values),high=Math.max(...values),span=Math.max(1e6,high-low);
  const points=values.map((v,i)=>`${i/Math.max(1,values.length-1)*600},${100-(v-low)/span*80}`).join(" ");
  const delta=values.length>1?values[values.length-1]-values[0]:0;
  return <section className="panel disk-timeline"><div className="panel-heading"><div><h2>Space over time</h2><p>Available disk space · recorded locally</p></div><strong className={delta<0?"activity-growth":"gain"}>{delta<0?"−":"+"}{formatBytes(Math.abs(delta))}</strong></div>{values.length>1?<><svg viewBox="0 0 600 120" role="img" aria-label={`Free disk space changed by ${formatBytes(Math.abs(delta))} across ${samples.length} samples`}><defs><linearGradient id="disk-space-fill" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor="#4f8cff" stopOpacity=".25"/><stop offset="100%" stopColor="#4f8cff" stopOpacity="0"/></linearGradient></defs><polygon points={`0,120 ${points} 600,120`} fill="url(#disk-space-fill)"/><polyline points={points} fill="none" stroke="#4f8cff" strokeWidth="3" strokeLinejoin="round" strokeLinecap="round"/></svg><div className="timeline-labels"><span>{new Date(samples[0].timestamp*1000).toLocaleTimeString()} · {formatBytes(values[0])} free</span><span>{new Date(samples[samples.length-1].timestamp*1000).toLocaleTimeString()} · {formatBytes(values[values.length-1])} free</span></div></>:<div className="empty-state">The timeline starts after two disk samples.</div>}</section>;
}
export function ActivityRow({event,expanded,toggle,review,open}:{event:ActivityEntry;expanded:boolean;toggle:()=>void;review?:()=>void;open?:()=>void}) {
  const kind=kinds[event.kind]??{name:event.kind,icon:Activity,color:"blue"};const Icon=kind.icon;
  const isFile=["file_created","file_changed","folder_created","metadata_changed","renamed"].includes(event.kind);
  const name=event.kind.startsWith("process")||event.kind==="app_started"?event.owner:event.path.split("/").pop();
  const title=<><strong>{kind.name}<span>{name}</span></strong><small>{event.workflow} · {new Date(event.timestamp*1000).toLocaleTimeString()}</small></>;
  const size=<span className="activity-event-size">{event.writeBytes>0?<strong className="gain"><ArrowUpRight size={13}/>{formatBytes(event.writeBytes)}</strong>:event.deltaBytes!=null?<strong className={event.deltaBytes>0?"activity-growth":"gain"}>{event.deltaBytes>0?"+":"−"}{formatBytes(Math.abs(event.deltaBytes))}</strong>:<span>Observed</span>}</span>;
  const icon=<span className={`activity-event-icon ${kind.color}`}><Icon size={19}/></span>;
  return <article id={`activity-event-${event.id}`} className="activity-feed-row">{open?<button className="activity-feed-main activity-feed-open" aria-label={`Open ${kind.name}: ${name} in main app`} onClick={open}>{icon}<span className="activity-event-title">{title}</span>{size}<ExternalLink size={15}/></button>:<div className="activity-feed-main">{icon}<button className="activity-event-title" aria-expanded={expanded} onClick={toggle}>{title}</button>{size}<button className="icon-button" aria-label={`Details for activity ${event.id}`} onClick={toggle}><ChevronDown size={17}/></button></div>}
    {expanded&&<div className="activity-event-detail"><code>{event.path}</code><p>{event.detail}</p><p>{event.attribution}{event.pid!=null?` · PID ${event.pid}`:""}</p>{event.readBytes>0&&<p><ArrowDownLeft size={13}/>{formatBytes(event.readBytes)} observed reads</p>}<p>Current allocated size: {event.sizeBytes==null?"Unavailable":formatBytes(event.sizeBytes)}. Flags: {event.flags}.</p>{isFile&&review&&<Button variant="outline" className="big-button" onClick={review}><Sparkles/>Ask your agent</Button>}<small><Check size={12}/>Structured local observation, not automatic deletion permission.</small></div>}
  </article>;
}
