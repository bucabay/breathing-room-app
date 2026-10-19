import type { AgentCleanupOutcome, AgentCleanupRun } from "./agent-cleanup";

export type CleanupOutcomeGroup = "cleaned" | "failed" | "skipped";
export function outcomeGroup(outcome: AgentCleanupOutcome): CleanupOutcomeGroup {
  if (outcome.status === "skipped") return "skipped";
  if (outcome.status === "running" || outcome.status === "failed") return "failed";
  return outcome.ok ? "cleaned" : "failed";
}
export function cleanupResultSummary(run: AgentCleanupRun) {
  const groups = { cleaned: [], failed: [], skipped: [] } as Record<CleanupOutcomeGroup, AgentCleanupOutcome[]>;
  for (const outcome of run.outcomes) groups[outcomeGroup(outcome)].push(outcome);
  const before = run.results?.beforeBytes ?? null;
  const removed = run.results?.removedBytes ?? null;
  const measured = before != null && removed != null && before > 0;
  return {
    groups, measured,
    before, removed,
    remaining: measured ? Math.max(0, before - removed) : null,
    percent: measured ? Math.min(100, Math.max(0, removed / before * 100)) : null,
    pendingTrash: run.results?.pendingTrashBytes ?? null,
    spaceChange: run.results?.availableSpaceChange ?? null,
  };
}

export function trashCompletion(run: AgentCleanupRun): { bytes:number|null; locations:number } | null {
  const moved=run.outcomes.filter(outcome=>{
    if((outcome.pendingTrashBytes??0)>0)return true;
    return run.actions.some(action=>action.id===outcome.id&&action.kind==="trash")&&outcomeGroup(outcome)==="cleaned"&&outcome.removedBytes!==0;
  });
  if(!moved.length)return null;
  const sizes=moved.map(outcome=>(outcome.pendingTrashBytes??0)>0?outcome.pendingTrashBytes!:outcome.removedBytes??null);
  return {locations:moved.length,bytes:sizes.every(size=>size!=null&&Number.isFinite(size)&&size>=0)?sizes.reduce<number>((sum,size)=>sum+size!,0):null};
}
