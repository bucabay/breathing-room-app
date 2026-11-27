import { useState } from "react";
import { AlertTriangle, ChevronDown, Info, RotateCcw } from "lucide-react";
import { formatBytes, type RestartSpace } from "@/lib/model";
import { restartRecommended } from "@/lib/swap";

/**
 * Explains disk that macOS rebuilds after a restart. This card is
 * deliberately read-only: swap and the sleep image are owned by macOS and
 * are never offered as cleanup targets. Collapsed by default; the detailed
 * measurements and restart comparison expand on click. When swap crosses the
 * warning threshold, the recommendation is visible without expanding.
 */
export function RestartSpaceCard({ data }: { data: RestartSpace | null }) {
  const [open, setOpen] = useState(false);
  if (!data) return null;
  const reclaim = data.restartReclaimBytes;
  const pressure = data.memoryPressure?.label ?? "unknown";
  const swap = data.items.find(item => item.id === "swap");
  const sleep = data.items.find(item => item.id === "sleep-image");
  const snapshots = data.items.find(item => item.id === "snapshots");
  const last = data.lastRestart;
  const rows = [swap, sleep, snapshots].filter(item => item && (item.bytes == null ? item.files > 0 : item.bytes > 0));
  const recommended = restartRecommended(data);
  const swapInUse = data.swap.usedBytes;
  const swapAmount = data.swapFileBytes > 0 ? data.swapFileBytes : (swapInUse ?? 0);
  if (reclaim === 0 && rows.length === 0 && !last && !recommended) return null;
  return <section className={`restart-space panel ${pressure} ${recommended ? "restart-recommended" : ""}`} aria-labelledby="restart-space-title">
    <div className="restart-space-head">
      <div className="restart-space-copy">
        <span className={`restart-space-eyebrow ${recommended ? "warn" : ""}`}>
          {recommended ? <AlertTriangle size={14} aria-hidden="true" /> : <RotateCcw size={14} aria-hidden="true" />}
          {recommended ? "Restart recommended" : "Space macOS rebuilds"}
        </span>
        <strong id="restart-space-title" className="restart-space-total">{reclaim > 0 ? formatBytes(reclaim) : "None measured"}</strong>
        <span className="restart-space-lede">Memory swap and the sleep image macOS is holding on disk. macOS rebuilds both at boot, and they grow again as memory pressure returns.</span>
        {recommended && <div className="restart-space-advice" role="status">
          <strong>Restart to release {formatBytes(swapAmount)} of swap files.</strong>
          <p>{swapInUse != null
            ? `Your Mac is using ${formatBytes(swapInUse)} of swap, above the 2 GB warning level.`
            : `macOS is holding ${formatBytes(data.swapFileBytes)} of swap files, above the 2 GB warning level.`}
            {" "}Save your work, then restart when it suits you. macOS rebuilds swap at boot; Breathing Room never deletes it while macOS is using it.</p>
        </div>}
        {!open && rows.length > 0 && <ul className="restart-space-legend" aria-label="Rebuilt storage detail">
          {rows.map(item => item && <li key={item.id}>
            <span className={`restart-space-dot ${item.id}`} aria-hidden="true" />
            <span>{item.name}</span>
            <strong>{item.bytes != null ? formatBytes(item.bytes) : `${item.files} snapshot${item.files === 1 ? "" : "s"}`}</strong>
          </li>)}
        </ul>}
      </div>
      <button type="button" className="restart-space-action" aria-expanded={open} aria-controls="restart-space-details" onClick={() => setOpen(value => !value)}>
        {open ? "Hide details" : "Show details"}<ChevronDown className={open ? "rotated" : undefined} size={16} aria-hidden="true" />
      </button>
    </div>
    {open && <div className="restart-space-details" id="restart-space-details">
      <div className="restart-space-main">
        <p>They are not leftover clutter, and Breathing Room does not delete them while macOS is using them.</p>
        <p className="restart-space-pressure">Memory pressure: <strong>{pressure}</strong>{data.swap.usedBytes != null && <> · {formatBytes(data.swap.usedBytes)} of swap in use</>}.</p>
        {last ? <div className="restart-space-last">
          <strong>{last.freedBytes >= 0 ? `${formatBytes(last.freedBytes)} came back` : `${formatBytes(Math.abs(last.freedBytes))} less free`}</strong>
          <small>since your last restart · {formatBytes(last.availableBeforeBytes)} → {formatBytes(last.availableAfterBytes)} free</small>
        </div> : <p className="restart-space-last-note">Keep Breathing Room open for a full session and the next restart will show what came back.</p>}
      </div>
      <ul className="restart-space-list" aria-label="Rebuilt storage detail">
        {rows.map(item => item && <li key={item.id}>
          <span className={`restart-space-dot ${item.id}`} aria-hidden="true" />
          <span className="restart-space-row">
            <strong>{item.name}</strong>
            <small>{item.description}</small>
          </span>
          <span className="restart-space-value">{item.bytes != null ? formatBytes(item.bytes) : item.files > 0 ? `${item.files} snapshot${item.files === 1 ? "" : "s"}` : "None"}</span>
        </li>)}
      </ul>
    </div>}
    {open && <p className="restart-space-foot"><Info size={13} aria-hidden="true" />A restart is the supported way to release these files. They can already be back once memory pressure returns, so free space right after boot is the clearest comparison.</p>}
  </section>;
}
