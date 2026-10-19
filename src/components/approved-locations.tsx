import {useEffect,useRef,useState} from "react";
import {ArrowLeft,ChevronDown,ChevronRight,ShieldCheck} from "lucide-react";
import type {DailyApproval} from "@/lib/agent-cleanup";
import {approvalMethod,approvalPreviewLimit,filterApprovals,shortApprovalPath} from "@/lib/approved-locations";
import {Button} from "./ui/button";

interface ApprovalProps{approvals:DailyApproval[];onRevoke:(key:string)=>Promise<void>;onError:(error:unknown)=>void}
export function ApprovedLocationRows({approvals,onRevoke,onError}:ApprovalProps){
  const [revoking,setRevoking]=useState<string|null>(null);
  const revoke=async(key:string)=>{if(revoking)return;setRevoking(key);try{await onRevoke(key);}catch(error){onError(error);}finally{setRevoking(null);}};
  return <ul className="approved-location-list">{approvals.map(approval=><li key={approval.key}><details className="approved-location-row">
    <summary><span className="approved-location-label"><strong title={approval.action.title}>{approval.action.title}</strong><code title={approval.action.paths.join("\n")}>{shortApprovalPath(approval.action.paths[0]||"No location")}{approval.action.paths.length>1?` (+${approval.action.paths.length-1})`:""}</code></span><span className="approved-location-method" title={approval.action.kind==="trash"?"Move to Trash":approval.action.command.join(" ")}>{approvalMethod(approval)}</span><ChevronDown size={16}/></summary>
    <div className="approved-location-details">{approval.action.paths.map(path=><code key={path}>{path}</code>)}<p>{approval.action.kind==="trash"?"Move to Trash":approval.action.command.join(" ")}</p>{approval.action.cwd&&<p>Working directory: <code>{approval.action.cwd}</code></p>}<p>{approval.action.impact}</p><Button variant="outline" disabled={revoking!==null} onClick={()=>void revoke(approval.key)}>{revoking===approval.key?"Revoking…":"Revoke approval"}</Button></div>
  </details></li>)}</ul>;
}
export function ApprovedLocationsPreview({approvals,onViewAll,...props}:ApprovalProps&{onViewAll:()=>void}){
  return <section className="settings-panel panel approved-locations-preview"><h2><ShieldCheck size={22}/>Previously approved locations</h2><p className="metric-note">Daily care can reuse these exact locations and methods. New findings still need approval.</p>
    {approvals.length?<><ApprovedLocationRows approvals={approvals.slice(0,approvalPreviewLimit)} {...props}/><button id="daily-approvals-view-all" className="text-button approved-locations-view-all" onClick={onViewAll}>View all {approvals.length} {approvals.length===1?"approval":"approvals"}<ChevronRight size={15}/></button></>:<p className="metric-note">No saved approvals for this account. Approve locations in the Assistant first.</p>}
    <p className="metric-note">Rechecked every run. Moving to Trash does not reclaim space until Trash is emptied.</p>
  </section>;
}
export function ApprovedLocationsScreen({approvals,onBack,...props}:ApprovalProps&{onBack:()=>void}){
  const [query,setQuery]=useState("");const heading=useRef<HTMLHeadingElement>(null);
  useEffect(()=>{window.scrollTo({top:0,behavior:"instant"});heading.current?.focus({preventScroll:true});},[]);
  const filtered=filterApprovals(approvals,query);
  return <section className="approved-locations-screen" aria-labelledby="approved-locations-title"><Button variant="outline" onClick={onBack}><ArrowLeft size={16}/>Back to Daily care</Button><div className="page-heading"><div><h1 id="approved-locations-title" ref={heading} tabIndex={-1}>Previously approved locations</h1><p>{approvals.length} saved {approvals.length===1?"approval":"approvals"}. Expand a row to inspect its exact method or revoke it.</p></div></div><p className="metric-note">Approval matches the exact path, command, working directory, native rule and signed-in account—not a parent folder or a tool name. Revoking stops future reuse; it does not restore files already cleaned.</p><label className="field-label approved-locations-filter">Filter approved locations<input type="search" value={query} onChange={event=>setQuery(event.target.value)} placeholder="Find an app, folder or tool…"/></label><div className="panel"><ApprovedLocationRows approvals={filtered} {...props}/>{!filtered.length&&<p className="approved-locations-empty">{approvals.length?"No approvals match your search.":"No saved approvals for this account."}</p>}</div><p className="metric-note">{query.trim()?`${filtered.length} of ${approvals.length} approvals shown. `:""}Every location is measured and validated again before cleanup. Per-inspection automatic Ruff cleanup is not a saved approval.</p></section>;
}
