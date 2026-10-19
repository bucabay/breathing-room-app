import { useMemo, useRef, useState } from "react";
import { ArrowLeft, ChevronRight, File, FolderOpen, LoaderCircle } from "lucide-react";
import { api } from "@/lib/api";
import { formatBytes, type StorageReport } from "@/lib/model";
import { UsageBar } from "./charts";

export function useDiskExplorer(report: StorageReport | null) {
  const [path, setPath] = useState("/");
  const [files, setFiles] = useState<Awaited<ReturnType<typeof api.browseStorage>> | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const request = useRef(0);
  const dirs = report?.directories ?? [];
  const measured = useMemo(() => new Map(dirs.map(dir => [dir.path, dir])), [dirs]);
  const open = async (next: string) => {
    const current = ++request.current;
    setPath(next); setBusy(true); setError(""); setFiles(null);
    if (next === "/") { setBusy(false); return; }
    try { const result = await api.browseStorage(next); if (current === request.current) setFiles(result); } catch (e) { if (current === request.current) setError(String(e)); }
    finally { if (current === request.current) setBusy(false); }
  };
  const entries = path === "/" ? dirs.filter(d => d.parent === "/").map(d => ({ ...d, directory: true, symlink: false })) :
    (files?.entries ?? []).map(e => {
      const size = measured.get(e.path);
      return { ...e, bytes: e.directory ? size?.bytes ?? 0 : e.bytes, partial: e.directory ? size?.partial ?? true : false };
    });
  const sorted = [...entries].sort((a, b) => b.bytes - a.bytes);
  return { path, busy, error, entries: sorted, open };
}

export function DiskExplorer({ explorer, onReview, highlighted }: { explorer: ReturnType<typeof useDiskExplorer>; onReview: (path: string) => void; highlighted: string | null }) {
  const { path, busy, error, entries: sorted, open } = explorer;
  return <div className="space-explorer">
    <div className="disk-breadcrumb"><button className="text-button" onClick={() => void open(path.split("/").slice(0, -1).join("/") || "/")} disabled={path === "/" || busy}><ArrowLeft size={17} />Back</button><code>{path === "/" ? "Macintosh HD · Data volume" : path}</code></div>
    {error && <div className="activation-note">{error}</div>}
    <div className="storage-list">{busy ? <div className="empty-state"><LoaderCircle className="spin" />Reading folder…</div> : sorted.map(entry => <div className={`disk-entry-row ${highlighted === entry.path ? "space-highlighted-row" : ""}`} id={`space-entry-${encodeURIComponent(entry.path)}`} key={entry.path}><button className="disk-entry" disabled={!entry.directory || entry.symlink} onClick={() => void open(entry.path)}>
      <span className={`app-icon ${entry.directory ? "blue" : "mint"}`}>{entry.directory ? <FolderOpen size={25} /> : <File size={24} />}</span><span className="disk-entry-name"><strong>{entry.name}</strong><small>{entry.symlink ? "Symbolic link · not followed" : entry.directory ? entry.partial ? "Partial or unmeasured directory" : "Folder including descendants" : "File · allocated size"}</small></span><UsageBar value={entry.bytes} maximum={sorted[0]?.bytes ?? 1} color="#3b82f6" /><strong>{entry.bytes ? formatBytes(entry.bytes) : entry.directory ? "Unmeasured" : "0 B"}</strong>{entry.directory && !entry.symlink && <ChevronRight size={18} />}
    </button><button className="text-button disk-review-button" disabled={entry.symlink} onClick={() => onReview(entry.path)}>Ask your agent</button></div>)}{!busy && !sorted.length && !error && <div className="empty-state">No accessible entries measured here.</div>}</div>
  </div>;
}
