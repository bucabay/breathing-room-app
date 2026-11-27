import test from "node:test";
import assert from "node:assert/strict";
import { SWAP_RESTART_THRESHOLD_BYTES, restartRecommended } from "../src/lib/swap.ts";
import type { RestartSpace } from "../src/lib/model.ts";

const space=(usedBytes:number|null,swapFileBytes:number):RestartSpace=>({
  timestamp:0,totalBytes:0,availableBytes:0,bootedAt:null,uptimeSeconds:null,
  swap:{totalBytes:4*1024**3,usedBytes,freeBytes:0},swapFiles:1,swapFileBytes,sleepImageBytes:0,
  hibernateMode:null,localSnapshotCount:0,memoryPressure:{level:null,label:"normal"},
  restartReclaimBytes:swapFileBytes,estimatedAvailableAfterRestartBytes:0,items:[],lastRestart:null,warnings:[],note:"",
});

test("restart is recommended at or above the swap threshold",()=>{
  assert.equal(SWAP_RESTART_THRESHOLD_BYTES,2*1024**3);
  assert.equal(restartRecommended(null),false);
  assert.equal(restartRecommended(space(0,0)),false);
  assert.equal(restartRecommended(space(SWAP_RESTART_THRESHOLD_BYTES-1,0)),false);
  assert.equal(restartRecommended(space(SWAP_RESTART_THRESHOLD_BYTES,0)),true);
  assert.equal(restartRecommended(space(3*1024**3,3*1024**3)),true);
});

test("swap files still trigger the note when usage counters are unavailable",()=>{
  assert.equal(restartRecommended(space(null,SWAP_RESTART_THRESHOLD_BYTES)),true);
  assert.equal(restartRecommended(space(null,SWAP_RESTART_THRESHOLD_BYTES-1)),false);
});
