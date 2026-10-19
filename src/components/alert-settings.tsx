import { useEffect, useState } from "react";
import { Bell, ChevronDown } from "lucide-react";
import { api } from "@/lib/api";
import { defaultAlerts, type MonitorConfig } from "@/lib/live";
import { Button } from "./ui/button";

export function AlertSettings({config,onSaved}:{config:MonitorConfig;onSaved:()=>void}) {
  const [alerts,setAlerts]=useState({...defaultAlerts,...config.alerts});
  const [busy,setBusy]=useState(false); const [message,setMessage]=useState("");
  const serialized=JSON.stringify(config.alerts);
  useEffect(()=>{setAlerts({...defaultAlerts,...JSON.parse(serialized??"{}")});},[serialized]);
  const save=async()=>{setBusy(true);setMessage("");try {
    // Read current config so another window's pause/settings change isn't overwritten.
    const current=await api.live(); await api.configureMonitor({...current.config??config,alerts});
    onSaved();setMessage("Alert preferences saved.");
  }catch(e){setMessage(String(e));}finally{setBusy(false);}};
  return <details id="activity-alert-settings" className="activity-monitor-settings alert-settings">
    <summary><Bell size={17}/>Activity alerts <ChevronDown size={16}/></summary>
    <form onSubmit={e=>{e.preventDefault();void save();}}>
      <label className="toggle-row"><input type="checkbox" checked={alerts.enabled} onChange={e=>setAlerts({...alerts,enabled:e.target.checked})}/><span>Automatically show Activity for sustained high usage</span></label>
      <div className="monitor-control-grid">
        <div className="field-label"><label><input type="checkbox" checked={alerts.cpuEnabled} onChange={e=>setAlerts({...alerts,cpuEnabled:e.target.checked})}/> CPU alerts</label><label htmlFor="alert-cpu-threshold">Per-app CPU threshold (%)</label><input id="alert-cpu-threshold" type="number" min="1" max="10000" step="1" required value={alerts.cpuThreshold} onChange={e=>setAlerts({...alerts,cpuThreshold:e.target.valueAsNumber})}/></div>
        <div className="field-label"><label><input type="checkbox" checked={alerts.writesEnabled} onChange={e=>setAlerts({...alerts,writesEnabled:e.target.checked})}/> Disk-write alerts</label><label htmlFor="alert-write-threshold">Per-app writes (MB/s)</label><input id="alert-write-threshold" type="number" min="0.1" max="10000" step="0.1" required value={alerts.writeMbPerSecond} onChange={e=>setAlerts({...alerts,writeMbPerSecond:e.target.valueAsNumber})}/></div>
        <label className="field-label">Sustained for (seconds)<input type="number" min="5" max="600" required value={alerts.sustainedSeconds} onChange={e=>setAlerts({...alerts,sustainedSeconds:e.target.valueAsNumber})}/></label>
        <label className="field-label">Between automatic openings (seconds)<input type="number" min="0" max="3600" required value={alerts.cooldownSeconds} onChange={e=>setAlerts({...alerts,cooldownSeconds:e.target.valueAsNumber})}/></label>
      </div>
      <p>100% CPU means one fully occupied core; apps and their observed helpers are combined. Writes use sampled counters, not per-file attribution. Dismissed episodes stay quiet until usage recovers.</p>
      {!config.processIo&&alerts.writesEnabled&&<p className="activation-note">Enable “Sample process disk I/O” below to detect heavy writes.</p>}
      <p>Alerts run while Breathing Room is running. Enable “Keep running in the menu bar” in Daily care to continue after closing the main window.</p>
      <Button variant="outline" disabled={busy} type="submit">{busy?"Saving…":"Save alert preferences"}</Button>
      {message&&<p role="status">{message}</p>}
    </form>
  </details>;
}
