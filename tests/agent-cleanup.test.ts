import test from "node:test";
import assert from "node:assert/strict";
import { cleanupMode, pendingCleanupActions, type AgentCleanupRun } from "../src/lib/agent-cleanup.ts";
test("old plans retain command/permission authority and attempted actions cannot be selected again",()=>{
  const action={id:"command",title:"cache",reason:"fixture",impact:"download",kind:"command" as const,paths:["/fixture"],command:["npm","cache","clean"],estimatedBytes:100};
  const run={actions:[action,{...action,id:"trash",kind:"trash" as const,command:[]}],outcomes:[{id:"command",ok:false,detail:"interrupted"}]} as AgentCleanupRun;
  assert.equal(cleanupMode(action),"command");assert.equal(cleanupMode(run.actions[1]),"permission");assert.deepEqual(pendingCleanupActions(run).map(action=>action.id),["trash"]);
});
