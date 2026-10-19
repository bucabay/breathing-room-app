import { useMemo } from "react";
import { ChevronDown, File, Sparkles } from "lucide-react";
import { buckets, categories, formatBytes, profileBuckets, type Bucket, type Profile, type StorageReport } from "@/lib/model";
import { spaceColors, spaceTabs, type SpaceTab } from "@/lib/space-view";
import { StoragePie, UsageBar } from "./charts";
import { DiskExplorer, useDiskExplorer } from "./disk-explorer";
import { Button } from "./ui/button";

export function SpaceView({ report, profiles, view, onViewChange, selected, onSelect, onReview }: {
  report: StorageReport | null; profiles: Profile[]; view: SpaceTab; onViewChange: (view: SpaceTab) => void;
  selected: string | null; onSelect: (id: string | null) => void; onReview: (path: string) => void;
}) {
  const explorer = useDiskExplorer(report);
  const groups = useMemo(() => profileBuckets(buckets((report?.groups ?? []).filter(group => group.category !== "unmapped"), view === "owner" || view === "project" ? view : "category"), profiles), [report, view, profiles]);
  const files = useMemo(() => [...(report?.largeFiles ?? [])].sort((a, b) => b.bytes - a.bytes), [report]);
  const items: Bucket[] = view === "explore" ? explorer.entries.filter(entry => !entry.symlink).map((entry, index) => ({ id: entry.path, name: entry.name, bytes: entry.bytes, files: 0, color: spaceColors[index % spaceColors.length], groups: [] })) : view === "large" ? files.map((file, index) => ({ id: file.path, name: file.path.split("/").pop() || file.path, bytes: file.bytes, files: 1, color: spaceColors[index % spaceColors.length], groups: [] })) : groups.map((group, index) => ({ ...group, color: view === "category" ? group.color : spaceColors[index % spaceColors.length] }));
  const label = spaceTabs.find(tab => tab.id === view)!.name;
  const description = view === "explore" ? "Share of this folder’s measured contents. Open a folder to look inside." : view === "large" ? "Share of the large files listed below. Review before deciding what to remove." : "Each slice shows a share of measured storage. Select one to look closer.";
  const select = (id: string) => {
    onSelect(id === selected ? null : id);
    if (id !== "space-other") requestAnimationFrame(() => document.getElementById(`space-entry-${encodeURIComponent(id)}`)?.scrollIntoView({ behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "instant" : "smooth", block: "nearest" }));
  };
  const changeTab = (next: SpaceTab) => { onViewChange(next); onSelect(null); };
  return <section className="space-browser panel" aria-label="Storage explorer">
    <StoragePie items={items} label={label} description={description} selected={selected} onSelect={select} />
    <div className="space-tabs" role="tablist" aria-label="Storage views">{spaceTabs.map((tab, index) => <button key={tab.id} id={`space-tab-${tab.id}`} role="tab" aria-selected={view === tab.id} aria-controls="space-list" tabIndex={view === tab.id ? 0 : -1} onClick={() => changeTab(tab.id)} onKeyDown={event => {
      const next = event.key === "ArrowRight" ? (index + 1) % spaceTabs.length : event.key === "ArrowLeft" ? (index + spaceTabs.length - 1) % spaceTabs.length : event.key === "Home" ? 0 : event.key === "End" ? spaceTabs.length - 1 : -1;
      if (next >= 0) { event.preventDefault(); changeTab(spaceTabs[next].id); document.getElementById(`space-tab-${spaceTabs[next].id}`)?.focus(); }
    }}>{tab.name}</button>)}</div>
    <div className="space-list-content" id="space-list" role="tabpanel" aria-labelledby={`space-tab-${view}`}>
      {view === "explore" ? <DiskExplorer explorer={explorer} onReview={onReview} highlighted={selected} /> : view === "large" ? <div className="large-file-list">{files.length ? files.map((file, index) => <div className={`large-file-row ${selected === file.path ? "space-highlighted-row" : ""}`} id={`space-entry-${encodeURIComponent(file.path)}`} key={file.path}><File size={22} style={{ color: spaceColors[index % spaceColors.length] }} /><div><strong>{file.path.split("/").pop()}</strong><small title={file.path}>{file.path}</small></div><span>{formatBytes(file.bytes)}</span><Button variant="outline" className="big-button" onClick={() => onReview(file.path)}><Sparkles />Ask your agent</Button></div>) : <div className="empty-state">No large files found in the current scan.</div>}</div> : <div className="storage-list">{items.length ? items.map(bucket => <StorageRow key={bucket.id} bucket={bucket} maximum={items[0].bytes} expanded={selected === bucket.id} onReview={onReview} onClick={() => onSelect(selected === bucket.id ? null : bucket.id)} />) : <div className="empty-state">{report ? "No measured storage in this view." : "Reading your storage…"}</div>}</div>}
    </div>
  </section>;
}

function StorageRow({ bucket, maximum, expanded, onClick, onReview }: { bucket: Bucket; maximum: number; expanded: boolean; onClick: () => void; onReview: (scope: string) => void }) {
  return <div className="storage-row" id={`space-entry-${encodeURIComponent(bucket.id)}`}><button className="storage-row-main" onClick={onClick} aria-expanded={expanded}><span className="category-dot" style={{ background: bucket.color }} /><span className="storage-row-name"><strong>{bucket.name}</strong><small>{bucket.files ? `${bucket.files.toLocaleString()} files` : `${bucket.groups.length} locations`}</small></span><UsageBar value={bucket.bytes} maximum={maximum} color={bucket.color} /><strong>{formatBytes(bucket.bytes)}</strong><ChevronDown size={18} /></button>{expanded && <div className="storage-row-detail">{bucket.groups.map(group => <div key={group.id}><span>{group.project || group.owner}<small>{categories[group.category]?.name ?? group.category}</small></span><strong>{formatBytes(group.bytes)}</strong>{group.id.startsWith("/") && !group.id.includes("[files in") && <button className="text-button" onClick={() => onReview(group.id.replace("/System/Volumes/Data", ""))}>Ask your agent</button>}</div>)}</div>}</div>;
}
