import type { Bucket } from "@/lib/model";
import { formatBytes } from "@/lib/model";
import { spaceSlices } from "@/lib/space-view";

export function StoragePie({ items, label, description, selected, onSelect }: { items: Bucket[]; label: string; description: string; selected?: string | null; onSelect: (id: string) => void }) {
  const slices = spaceSlices(items);
  let angle = -Math.PI / 2;
  return <section className="space-breakdown" aria-label={`${label} storage breakdown`}>
    <div className="space-pie"><svg viewBox="0 0 320 320" aria-label={`${label}: ${slices.map(item => `${item.name} ${item.percent.toFixed(1)}%`).join(", ")}`}>
      {!slices.length && <circle cx="160" cy="160" r="145" fill="var(--ring-track)" />}
      {slices.map(item => {
        const start = angle; angle += item.percent / 100 * Math.PI * 2;
        const point = (a: number) => `${160 + 145 * Math.cos(a)},${160 + 145 * Math.sin(a)}`;
        const path = slices.length === 1 ? "M 160,15 A 145,145 0 1,1 160,305 A 145,145 0 1,1 160,15 Z" : `M 160,160 L ${point(start)} A 145,145 0 ${item.percent > 50 ? 1 : 0},1 ${point(angle)} Z`;
        return <path key={item.id} d={path} fill={item.color} stroke="var(--panel)" strokeWidth="2.5" strokeLinejoin="round" className={`space-pie-slice ${selected === item.id ? "selected" : ""}`} role="button" tabIndex={0} aria-label={`${item.name}: ${formatBytes(item.bytes)}, ${item.percent.toFixed(1)}%`} aria-pressed={selected === item.id} onClick={() => onSelect(item.id)} onKeyDown={event => { if (event.key === "Enter" || event.key === " ") { event.preventDefault(); onSelect(item.id); } }}><title>{item.name}: {formatBytes(item.bytes)} · {item.percent.toFixed(1)}%</title></path>;
      })}
    </svg></div>
    <div className="space-breakdown-content"><div className="space-breakdown-heading"><h2>{label}</h2><p>{description}</p></div>
      <div className="space-pie-key">{slices.map(item => <button key={item.id} className={selected === item.id ? "selected" : ""} onClick={() => onSelect(item.id)} aria-pressed={selected === item.id}><i style={{ background: item.color }} /><span><strong>{formatBytes(item.bytes)}</strong><small>{item.name}<span>{item.percent.toFixed(1)}%</span></small></span></button>)}</div>
      {!slices.length && <p className="space-chart-empty">No measured sizes in this view yet.</p>}
    </div>
  </section>;
}

export function StorageRing({ total, available, buckets, onSelect }: { total: number; available: number; buckets: Bucket[]; onSelect?: (id: string) => void }) {
  const circumference = 2 * Math.PI * 107;
  const denominator = Math.max(total, available + buckets.reduce((sum, b) => sum + b.bytes, 0));
  let offset = 0;
  const sections = buckets.map((b) => {
    const length = b.bytes / denominator * circumference; const start = offset; offset += length;
    return <circle key={b.id} cx="144" cy="144" r="107" fill="none" stroke={b.color} strokeWidth="28"
      strokeDasharray={`${Math.max(0, length - 3)} ${circumference}`} strokeDashoffset={-start} transform="rotate(-90 144 144)"
      className={onSelect ? "ring-segment" : ""} onClick={() => onSelect?.(b.id)} role={onSelect ? "button" : undefined}
      tabIndex={onSelect ? 0 : undefined} aria-label={`${b.name}: ${formatBytes(b.bytes)}`}
      onKeyDown={(e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); onSelect?.(b.id); } }}><title>{b.name}: {formatBytes(b.bytes)}</title></circle>;
  });
  const freeLength = available / denominator * circumference;
  return <div className="storage-ring">
    <svg viewBox="0 0 288 288" aria-label={`Disk capacity ${formatBytes(total)}. Available ${formatBytes(available)}.`}>
      <circle cx="144" cy="144" r="107" fill="none" stroke="var(--ring-track)" strokeWidth="28" />
      {sections}
      <circle cx="144" cy="144" r="107" fill="none" stroke="var(--free-color)" strokeWidth="28"
        strokeDasharray={`${Math.max(0, freeLength - 3)} ${circumference}`} strokeDashoffset={-(circumference - freeLength)} transform="rotate(-90 144 144)" />
    </svg>
    <div className="ring-label"><span className="ring-number">{(available / 1e9).toFixed(1)}</span><span>GB available</span><small>of {formatBytes(total)}</small></div>
  </div>;
}
export function UsageBar({ value, maximum, color }: { value: number; maximum: number; color: string }) {
  return <div className="usage-bar" aria-hidden="true"><span style={{ width: `${Math.max(0, Math.min(100, value / Math.max(maximum, 1) * 100))}%`, background: color }} /></div>;
}
