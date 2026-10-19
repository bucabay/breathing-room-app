import { useEffect, useRef } from "react";
import type { AgentCleanupAction } from "@/lib/agent-cleanup";
import { cleanupMode } from "@/lib/agent-cleanup";
import { cleanupSelection, toggleAllCleanup } from "@/lib/cleanup-review";
import { Button } from "./ui/button";
import { FindingList } from "./finding-list";

export function CleanupActionList({ actions, selected, onSelected, onApprove, disabled = false }: {
  actions: AgentCleanupAction[]; selected: string[]; onSelected: (ids: string[]) => void;
  onApprove: (ids: string[]) => void; disabled?: boolean;
}) {
  const selection = cleanupSelection(actions, selected);
  const selectAll = useRef<HTMLInputElement>(null);
  useEffect(() => { if (selectAll.current) selectAll.current.indeterminate = selection.partial; }, [selection.partial]);
  const rows = actions.map(action => ({ id: action.id, title: action.title, paths: action.paths, bytes: action.estimatedBytes,
    badge: ({ automatic: "Automatic eligible", permission: "Needs approval", command: "Tool command" } as const)[cleanupMode(action)] }));
  return <div className="cleanup-findings">
    <div className="cleanup-list-toolbar"><label><input ref={selectAll} type="checkbox" checked={selection.all} aria-label="Select all cleanup locations" disabled={disabled || !actions.length} onChange={event => onSelected(toggleAllCleanup(actions, event.target.checked))}/>Select all cleanup</label><span>{selection.ids.length} of {actions.length} selected</span></div>
    <FindingList items={rows} selected={selection.ids} selectionLabel="cleanup" disabled={disabled} onToggle={(id, checked) => onSelected(checked ? [...selection.ids, id] : selection.ids.filter(value => value !== id))} renderDetails={item => {
      const action = actions.find(action => action.id === item.id)!;
      return <><p>{action.reason}</p><p>{action.impact}</p>{action.paths.map(path => <code key={path}>{path}</code>)}<code>{action.kind === "trash" ? "Move to Trash" : action.command.join(" ")}</code><Button variant="outline" disabled={disabled} onClick={() => onApprove([action.id])}>{action.kind === "command" ? "Approve & run command" : "Approve & move to Trash"}</Button></>;
    }}/>
  </div>;
}
