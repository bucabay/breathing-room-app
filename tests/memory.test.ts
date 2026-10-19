import test from "node:test";
import assert from "node:assert/strict";
import { memoryUsage, memoryTrend } from "../src/lib/memory.ts";
import { createMetricsCache } from "../src/lib/metrics-cache.ts";

test("RAM percentages and byte totals derive from the shared cached sample",()=>{
  const cache=createMetricsCache();cache.updateLive({ready:true,timestamp:1,memoryUsedBytes:12e9,memoryTotalBytes:16e9});
  assert.deepEqual(memoryUsage(cache.getSnapshot()),{used:12e9,total:16e9,percent:75});
  cache.updateLive({ready:true,timestamp:2,memoryUsedBytes:8e9,memoryTotalBytes:16e9});assert.equal(memoryUsage(cache.getSnapshot())!.percent,50);
});
test("missing or invalid memory never appears as zero usage",()=>{
  assert.equal(memoryUsage(null),null);
  for(const [used,total] of [[null,16],[0,0],[-1,16],[17,16],[NaN,16],[4,Infinity]])assert.equal(memoryUsage({ready:true,memoryUsedBytes:used,memoryTotalBytes:total}),null);
  assert.equal(memoryUsage({ready:true,memoryUsedBytes:0,memoryTotalBytes:16})!.percent,0);
});
test("RAM sparkline uses only measured history, never inventing zeroes for old snapshots",()=>{
  const history=[undefined,null,NaN,-1,101,0,45,63].map((memoryPercent,index)=>({timestamp:index,availableBytes:1,cpuPercent:null,writeBytesPerSecond:0,memoryPercent}));
  assert.deepEqual(memoryTrend({ready:true,history}),[0,45,63]);assert.deepEqual(memoryTrend(null),[]);
});
