import { Trash2, X } from "lucide-react";
import { formatBytes } from "@/lib/model";
import { Button } from "./ui/button";

export function TrashCleanupNotice({bytes,preview,onOpen,onDismiss}:{bytes:number|null;preview:boolean;onOpen:()=>void;onDismiss:()=>void}){
  return <div id="trash-cleanup-status" className="global-maintenance trash-cleanup-notice" role="status" aria-live="polite">
    <span className="global-maintenance-icon"><Trash2 size={23}/></span>
    <div><strong>{preview?"Preview: files would move to Trash":"Cleanup moved files to Trash"}</strong><p>{preview?"No Mac changes in this preview. ":""}{bytes!=null?`${formatBytes(bytes)} moved from cleanup locations. `:""}Empty Trash in Finder to reclaim the space.</p><small>Review Trash first—it may contain unrelated files. Finder handles permanent deletion and confirmation.</small></div>
    <Button variant="outline" disabled={preview} onClick={onOpen}><Trash2 size={16}/>Open Trash</Button>
    <button className="icon-button" aria-label="Dismiss Trash reminder" title="Dismiss reminder" onClick={onDismiss}><X size={16}/></button>
  </div>;
}
