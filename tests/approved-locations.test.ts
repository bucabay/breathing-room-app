import test from "node:test";
import assert from "node:assert/strict";
import {approvalMethod,approvalPreviewLimit,filterApprovals,shortApprovalPath} from "../src/lib/approved-locations.ts";
import type {DailyApproval} from "../src/lib/agent-cleanup.ts";

const approval:DailyApproval={key:"exact-native-key",approvedAt:1,action:{id:"cache",title:"npm downloads",kind:"command",paths:["/Users/example/Library/Caches/npm/downloads"],command:["/opt/homebrew/bin/npm","cache","clean","--force"],reason:"Measured cache",impact:"Downloads again",estimatedBytes:10}};
test("approval preview caps rows and shortens display without altering native values",()=>{
  assert.equal(approvalPreviewLimit,3);assert.equal(shortApprovalPath("/Users/example/.npm/_cacache"),"~/.npm/_cacache");
  const path="/Users/example/"+"very-long-project/".repeat(8)+".next";assert.ok(shortApprovalPath(path).length<=52);assert.ok(shortApprovalPath(path).endsWith(".next"));
  assert.equal(approvalMethod(approval),"npm");assert.equal(approvalMethod({...approval,action:{...approval.action,kind:"trash"}}),"Trash");
  assert.equal(approval.action.paths[0],"/Users/example/Library/Caches/npm/downloads");assert.equal(approval.key,"exact-native-key");
});
test("the full list can filter titles, full locations and method arguments",()=>{
  for(const query of ["NPM","Library/Caches","--force"])assert.deepEqual(filterApprovals([approval],query),[approval]);
  assert.deepEqual(filterApprovals([approval],"absent"),[]);assert.deepEqual(filterApprovals([approval]," "),[approval]);
});
