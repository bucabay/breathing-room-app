import { useId, useState, type ReactNode } from "react";
import { ChevronDown } from "lucide-react";
import { formatBytes } from "@/lib/model";

export interface FindingListItem {
  id: string; title: string; paths: string[]; bytes: number; badge: string;
  severity?: "warning" | "critical"; partial?: boolean;
}

interface FindingListProps {
  items: FindingListItem[]; selected: string[]; selectionLabel: "cleanup" | "manual review";
  onToggle: (id: string, checked: boolean) => void; disabled?: boolean;
  expandSelected?: boolean; renderDetails: (item: FindingListItem, checked: boolean) => ReactNode;
}

function FindingRow({ item, selected, selectionLabel, onToggle, disabled, expandSelected, renderDetails }: Omit<FindingListProps, "items" | "selected"> & { item: FindingListItem; selected: boolean }) {
  const [expanded, setExpanded] = useState(!!(expandSelected && selected));
  const detailsId = useId();
  const open = expanded;
  return <li className={`finding-row ${selected ? "selected" : ""}`}>
    <div className="finding-row-main">
      <input type="checkbox" checked={selected} disabled={disabled} aria-label={`Select ${item.title} for ${selectionLabel}`} onChange={event => { if (expandSelected && event.target.checked) setExpanded(true); onToggle(item.id, event.target.checked); }}/>
      <div className="finding-row-location"><strong>{item.title}</strong><code title={item.paths.join("\n")}>{item.paths[0]}</code></div>
      <span className={`finding-row-badge ${item.severity || ""}`}>{item.badge}</span>
      <span className="finding-row-size">{item.partial ? "≥ " : ""}{formatBytes(item.bytes)}{item.partial && <small>Partial measurement</small>}</span>
      <button type="button" className="finding-row-disclosure" aria-label={`${open ? "Hide" : "Show"} details for ${item.title}`} aria-expanded={open} aria-controls={detailsId} onClick={() => setExpanded(value => !value)}><ChevronDown size={17}/></button>
    </div>
    <div id={detailsId} className="finding-row-details" hidden={!open}>{renderDetails(item, selected)}</div>
  </li>;
}

export function FindingList({ items, selected, ...props }: FindingListProps) {
  return <ul className="finding-list">{items.map(item => <FindingRow key={item.id} item={item} selected={selected.includes(item.id)} {...props}/>)}</ul>;
}
