import type { DailyApproval } from "./agent-cleanup";

export const approvalPreviewLimit=3;
export function shortApprovalPath(path:string,maxLength=52):string{
  const compact=path.replace(/^\/Users\/[^/]+(?=\/|$)/,"~");
  if(compact.length<=maxLength)return compact;
  const tail=compact.slice(-(maxLength-4));return `…/${tail.replace(/^\/+/,"")}`;
}
export function approvalMethod(approval:DailyApproval):string{
  return approval.action.kind==="trash"?"Trash":approval.action.command[0]?.split("/").pop()||"Tool";
}
export function filterApprovals(approvals:DailyApproval[],query:string):DailyApproval[]{
  const search=query.trim().toLocaleLowerCase();
  return search?approvals.filter(({action})=>[action.title,...action.paths,...action.command].join("\n").toLocaleLowerCase().includes(search)):approvals;
}
