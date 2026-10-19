import { Activity, ArrowDownLeft, ArrowUpRight, ChevronDown, FilePlus2, FolderPlus, HardDrive, MemoryStick, Radio, Rocket } from "lucide-react";
import { formatBytes, type Page } from "@/lib/model";
import type { LiveStatus } from "@/lib/live";
import { native } from "@/lib/api";
import { memoryUsage, memoryTrend } from "@/lib/memory";

export function Sparkline({ values, color }: { values: number[]; color: string }) {
  const max=Math.max(1,...values);
  const points=values.map((v,i)=>`${i/Math.max(1,values.length-1)*100},${30-v/max*26}`).join(" ");
  return <svg className="live-sparkline" viewBox="0 0 100 34" aria-hidden="true"><polyline fill="none" stroke={color} strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" points={points} /></svg>;
}
export function LiveStatusBar({ status, navigate, compact = false, onExpand }: { status: LiveStatus | null; navigate: (page: Page) => void; compact?: boolean; onExpand?: () => void }) {
  const enabled=status?.config?.enabled ?? true;
  const used=status?.totalBytes ? 1-(status.availableBytes??0)/status.totalBytes : 0;
  const circumference=2*Math.PI*18;
  const low=(status?.availableBytes??Infinity)<10e9;
  const minute=enabled?status?.minute:undefined;
  const memory=enabled?memoryUsage(status):null;
  const memoryLabel=!enabled?"Monitor paused":memory?`${formatBytes(memory.used)} of ${formatBytes(memory.total)} RAM · ${memory.percent.toFixed(0)}% used`:"Memory unavailable";
  if (compact) return <section className="compact-metrics" aria-label="Live Mac metrics">
    <button className={`icon-button ${low ? "disk-tight" : ""}`} onClick={() => navigate("space")} title={status?.ready ? `${formatBytes(status.availableBytes ?? 0)} free` : "Reading disk…"} aria-label={status?.ready ? `Disk space: ${formatBytes(status.availableBytes ?? 0)} free. View storage` : "View disk space"}><HardDrive size={16}/></button>
    <button className="icon-button" onClick={() => navigate("apps")} title={!enabled ? "Monitor paused" : `${status?.cpuPercent?.toFixed(0) ?? "—"}% CPU · ${status?.appCount ?? 0} apps`} aria-label={!enabled ? "Monitor paused. View apps" : `CPU: ${status?.cpuPercent?.toFixed(0) ?? "unavailable"} percent. View apps`}><Activity size={16}/></button>
    <button className="icon-button" onClick={() => navigate("apps")} title={memoryLabel} aria-label={`${memoryLabel}. View app memory`}><MemoryStick size={16}/></button>
    <button className="icon-button" onClick={() => navigate("activity")} title={status?.writeBytesPerSecond != null ? `${formatBytes(Math.round(status.writeBytesPerSecond))}/s writes` : "I/O unavailable"} aria-label="View disk I/O activity"><ArrowUpRight size={16}/></button>
    <button className="icon-button" onClick={() => navigate("activity")} title={`${minute?.appsStarted ?? 0} apps started · ${(minute?.filesCreated ?? 0) + (minute?.fileChanges ?? 0)} file changes · ${minute?.foldersCreated ?? 0} folders`} aria-label="View recent activity"><Radio size={16}/></button>
    <button className="icon-button" onClick={onExpand} title="Expand metrics" aria-label="Expand metrics" aria-expanded={false} aria-controls="expanded-metrics"><ChevronDown size={16}/></button>
  </section>;
  return <section className="live-status-strip" aria-label="Live Mac status">
    <button className={`live-metric live-disk ${low?"disk-tight":""}`} onClick={()=>navigate("space")} aria-label="View live disk space">
      <svg className="mini-disk-ring" viewBox="0 0 46 46" role="img" aria-label={status?.ready ? `${Math.round(used*100)}% disk used` : "Disk sample pending"}><circle cx="23" cy="23" r="18" fill="none" stroke="var(--ring-track)" strokeWidth="6" /><circle cx="23" cy="23" r="18" fill="none" stroke={low?"#ef6b76":"#4f8cff"} strokeWidth="6" strokeDasharray={`${used*circumference} ${circumference}`} transform="rotate(-90 23 23)" /><text x="23" y="26" textAnchor="middle" fontSize="10" fill="currentColor">{status?.ready?`${Math.round(used*100)}%`:"—"}</text></svg>
      <span><strong>{status?.ready?`${formatBytes(status.availableBytes??0)} free`:"Reading disk…"}</strong><small><HardDrive size={11}/>{status?.freeChangeBytes ? `${status.freeChangeBytes>0?"+":"−"}${formatBytes(Math.abs(status.freeChangeBytes))} since sample` : "Disk space"}</small></span>
    </button>
    <button className="live-metric live-cpu" onClick={()=>navigate("apps")} aria-label="View live process activity"><span className="live-social-icon violet"><Activity size={21}/></span><span><strong>{!enabled?"Monitor paused":status?.cpuPercent!=null?`${status.cpuPercent.toFixed(0)}% CPU`:"Sampling apps…"}</strong><small>{status?.appCount??0} apps · {status?.processCount??0} processes</small></span><Sparkline values={status?.history?.map(p=>p.cpuPercent??0)??[]} color="#a079ef"/></button>
    <button className="live-metric live-memory" onClick={()=>navigate("apps")} aria-label={`${memoryLabel}. View app memory`}><span className="live-social-icon mint"><MemoryStick size={21}/></span><span><strong>{!enabled?"Monitor paused":memory?`${memory.percent.toFixed(0)}% RAM`:"Reading memory…"}</strong><small>{memory?`${formatBytes(memory.used)} / ${formatBytes(memory.total)}`:"Memory unavailable"}</small></span><Sparkline values={enabled?memoryTrend(status):[]} color="#16a085"/></button>
    <button className="live-metric live-io" onClick={()=>navigate("activity")} aria-label="View disk writes"><span className="live-social-icon mint"><ArrowUpRight size={21}/></span><span><strong>{status?.writeBytesPerSecond!=null?`${formatBytes(Math.round(status.writeBytesPerSecond))}/s writes`:"I/O unavailable"}</strong><small><ArrowDownLeft size={11}/>{status?.readBytesPerSecond!=null?`${formatBytes(Math.round(status.readBytesPerSecond))}/s reads`:"Sampled process I/O"}</small></span></button>
    <button className="live-pulses" onClick={()=>navigate("activity")} aria-label="Open live activity log"><span className="pulse-chip pulse-apps" key={`apps-${minute?.appsStarted}`}><Rocket size={15}/><b>+{minute?.appsStarted??0}</b> apps</span><span className="pulse-change-row"><span className="pulse-chip pulse-files" key={`files-${minute?.filesCreated}-${minute?.fileChanges}`}><FilePlus2 size={15}/><b>+{(minute?.filesCreated??0)+(minute?.fileChanges??0)}</b> changes</span><small><Radio size={11}/>{!native?"Example activity":enabled?"Last minute · live":"Capture paused"}</small></span><span className="pulse-chip pulse-folders" key={`folders-${minute?.foldersCreated}`}><FolderPlus size={15}/><b>+{minute?.foldersCreated??0}</b> folders</span></button>
  </section>;
}
