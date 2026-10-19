import test from "node:test";
import assert from "node:assert/strict";
import { createMetricsCache, withCurrentDisk } from "../src/lib/metrics-cache.ts";
import type { StorageReport, AppGroup } from "../src/lib/model.ts";

const report={totalBytes:1000,availableBytes:50,scannedAt:10,scannedBytes:400,identifiedBytes:400,groups:[],directories:[]} as unknown as StorageReport;
test("all disk views project the same cached capacity without altering inventory",()=>{
  const cache=createMetricsCache();cache.seedDisk(report);
  cache.updateLive({ready:true,timestamp:20,diskTimestamp:20,totalBytes:1000,availableBytes:250,cpuPercent:12});
  const current=withCurrentDisk(report,cache.getSnapshot())!;
  assert.equal(current.availableBytes,250);assert.equal(current.availableBytes,cache.getSnapshot()!.availableBytes);
  assert.equal(current.usedBytes,750);assert.equal(current.unmappedBytes,350);assert.equal(current.scannedAt,10);
  assert.equal(current.groups,report.groups);assert.equal(report.availableBytes,50);
  cache.seedDisk({...report,availableBytes:1,scannedAt:30});assert.equal(cache.getSnapshot()!.availableBytes,250);
});
test("fresh calls notify consumers while stale and invalid reads cannot replace good metrics",()=>{
  const cache=createMetricsCache();let updates=0;const stop=cache.subscribe(()=>updates++);
  cache.updateLive({ready:true,timestamp:20,diskTimestamp:21,totalBytes:1000,availableBytes:300,cpuPercent:9});
  cache.updateLive({ready:true,timestamp:19,totalBytes:1000,availableBytes:40,cpuPercent:99});assert.equal(updates,1);
  cache.updateLive({ready:false,timestamp:22,totalBytes:0,availableBytes:0,cpuPercent:null});
  assert.equal(cache.getSnapshot()!.availableBytes,300);assert.equal(cache.getSnapshot()!.cpuPercent,null);assert.equal(updates,2);
  cache.updateLive({ready:true,timestamp:23,diskTimestamp:20,totalBytes:1000,availableBytes:60});assert.equal(cache.getSnapshot()!.availableBytes,300);
  stop();cache.updateLive({ready:true,timestamp:24,totalBytes:1000,availableBytes:400});assert.equal(updates,3);
});
test("app rows and aggregate CPU are cached as a single monitor sample",()=>{
  const cache=createMetricsCache();const apps=[{id:"app",cpu:120,cpuAvailable:true}] as AppGroup[];
  cache.updateLive({ready:true,timestamp:20,cpuPercent:15,coreCount:8,appGroups:apps});
  assert.equal(cache.getSnapshot()!.appGroups,apps);assert.equal(cache.getSnapshot()!.cpuPercent,15);
  const next=[{id:"app",cpu:40,cpuAvailable:true}] as AppGroup[];
  cache.updateLive({ready:true,timestamp:25,cpuPercent:5,coreCount:8,appGroups:next});
  assert.equal(cache.getSnapshot()!.appGroups![0].cpu,cache.getSnapshot()!.cpuPercent!*8);
});
