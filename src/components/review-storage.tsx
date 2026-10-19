import { useState } from "react";
import { ChevronDown, FolderSearch, TriangleAlert } from "lucide-react";
import type { ReviewStorageLocation } from "@/lib/agent-cleanup";
import { selectedReviewLocations } from "@/lib/review-storage";
import { Button } from "./ui/button";
import { FindingList } from "./finding-list";

export function ReviewStorage({ items, onReveal }: { items: ReviewStorageLocation[]; onReveal: (path: string) => void }) {
  const [selected, setSelected] = useState<string[]>([]);
  const [visible, setVisible] = useState(30);
  if (!items.length) return null;
  const chosen = selectedReviewLocations(items, selected);
  const rows = items.slice(0, visible).map(item => ({ id: item.path, title: item.title, paths: [item.path,...(item.aliases||[])], bytes: item.bytes,
    partial: item.partial, severity: item.severity, badge: item.recoverability === "not-rebuildable" ? "Not rebuildable" : "Recovery unknown" }));
  return <details className="manual-inspection">
    <summary><span><strong>Manual inspection</strong><small>Originals and app data. Not included in cleanup.</small></span><span className="manual-inspection-count">{items.length} locations</span><ChevronDown size={18}/></summary>
    <div className="manual-inspection-note"><TriangleAlert size={17}/><p>These files may be irreplaceable. Select individual locations to inspect their warning and open them in Finder. Nothing here can be cleaned automatically or included in select-all cleanup.</p></div>
    <FindingList items={rows} selected={chosen.map(item => item.path)} selectionLabel="manual review" expandSelected onToggle={(path, checked) => setSelected(current => checked ? [...current, path] : current.filter(value => value !== path))} renderDetails={(row, checked) => {
      const item = items.find(item => item.path === row.id)!;
      return <><p className="manual-loss-warning"><TriangleAlert size={16}/>{item.warning}</p>{checked && <p>Selected for review only. Removal can lose source footage and editable timeline data, unique files or virtual-machine state. Verify a separate usable backup first.</p>}<code>{item.path}</code>{item.aliases?.length?<><p>These hard-linked paths share the same file and are counted once:</p>{item.aliases.map(path=><code key={path}>{path}</code>)}</>:null}<Button variant="outline" disabled={!checked} onClick={() => onReveal(item.path)}><FolderSearch size={16}/>Show in Finder</Button></>;
    }}/>
    {items.length > visible && <Button className="manual-inspection-more" variant="outline" onClick={() => setVisible(count => count + 30)}>Show more locations ({items.length - visible} remaining)</Button>}
    <p className="manual-inspection-footer">{chosen.length} selected for review · no deletion approved. Sizes are not promised recoverable space.</p>
  </details>;
}
