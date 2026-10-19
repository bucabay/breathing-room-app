import test from "node:test";
import assert from "node:assert/strict";
import { cleanupResultSummary, outcomeGroup, trashCompletion } from "../src/lib/cleanup-results.ts";
import type { AgentCleanupRun } from "../src/lib/agent-cleanup.ts";

test("results distinguish successful, skipped and interrupted outcomes without inventing space savings",()=>{
  const run={outcomes:[{id:"clean",ok:true,detail:"done"},{id:"skip",ok:true,status:"skipped",detail:"already absent"},{id:"failure",ok:false,status:"failed",detail:"permission denied"},{id:"interrupted",ok:false,status:"running",detail:"unknown"}]} as AgentCleanupRun;
  const summary=cleanupResultSummary(run);
  assert.equal(summary.groups.cleaned.length,1);assert.equal(summary.groups.failed.length,2);assert.equal(summary.groups.skipped.length,1);
  assert.equal(summary.measured,false);assert.equal(summary.removed,null);assert.equal(summary.percent,null);
  assert.equal(outcomeGroup(run.outcomes[1]),"skipped");
});
test("Trash reminders require actual moves, not commands, skipped actions or empty locations",()=>{
  const run={actions:[{id:"trash",kind:"trash"},{id:"command",kind:"command"}],outcomes:[{id:"trash",ok:true,status:"success",removedBytes:512,pendingTrashBytes:512}]} as AgentCleanupRun;
  assert.deepEqual(trashCompletion(run),{locations:1,bytes:512});
  for(const outcome of [{id:"command",ok:true,status:"success",removedBytes:512},{id:"trash",ok:true,status:"skipped",removedBytes:0},{id:"trash",ok:true,status:"success",removedBytes:0},{id:"trash",ok:false,status:"failed"},{id:"trash",ok:false,status:"running"}])assert.equal(trashCompletion({...run,outcomes:[outcome]} as AgentCleanupRun),null);
  assert.deepEqual(trashCompletion({...run,outcomes:[{id:"trash",ok:true,detail:"Moved"}]}),{locations:1,bytes:null});
  assert.deepEqual(trashCompletion({...run,outcomes:[{id:"trash",ok:true,detail:"Moved; size unknown",pendingTrashBytes:0,removedBytes:null}]}),{locations:1,bytes:null});
  assert.deepEqual(trashCompletion({...run,outcomes:[{id:"trash",ok:false,status:"failed",detail:"Partially moved",pendingTrashBytes:256}]}),{locations:1,bytes:256});
});
test("the chart measures source-location removal without treating Trash or free-space change as extra cleaned bytes",()=>{
  const run={outcomes:[],results:{beforeBytes:1000,removedBytes:600,pendingTrashBytes:400,availableSpaceChange:-50}} as unknown as AgentCleanupRun;
  const summary=cleanupResultSummary(run);assert.equal(summary.percent,60);assert.equal(summary.remaining,400);assert.equal(summary.removed,600);assert.equal(summary.pendingTrash,400);assert.equal(summary.spaceChange,-50);
});
