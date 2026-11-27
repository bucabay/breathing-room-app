import test from "node:test";
import assert from "node:assert/strict";
import {createRequire} from "node:module";
import {buildSync} from "esbuild";

const space=(usedBytes,swapFileBytes=usedBytes)=>({
  timestamp:0,totalBytes:500*1024**3,availableBytes:100*1024**3,bootedAt:1700000000,uptimeSeconds:7200,
  swap:{totalBytes:4*1024**3,usedBytes,freeBytes:4*1024**3-usedBytes},
  swapFiles:4,swapFileBytes,sleepImageBytes:2*1024**3,hibernateMode:3,localSnapshotCount:2,
  memoryPressure:{level:1,label:"normal"},restartReclaimBytes:swapFileBytes+2*1024**3,estimatedAvailableAfterRestartBytes:106*1024**3,
  items:[
    {id:"swap",name:"Memory swap",bytes:swapFileBytes,files:4,description:"Rebuilt at boot."},
    {id:"sleep-image",name:"Sleep image",bytes:2*1024**3,files:1,description:"Rebuilt at boot."},
    {id:"snapshots",name:"Local snapshots",bytes:null,files:2,description:"May be released."},
  ],lastRestart:null,warnings:[],note:"",
});

test("high swap shows a visible restart recommendation without expanding the card",()=>{
  const {outputFiles}=buildSync({stdin:{contents:`import {renderToStaticMarkup} from "react-dom/server";import {RestartSpaceCard} from "./src/components/restart-space";export function render(data){return renderToStaticMarkup(<RestartSpaceCard data={data}/>)};`,loader:"tsx",resolveDir:new URL("..",import.meta.url).pathname},bundle:true,platform:"node",format:"cjs",jsx:"automatic",alias:{"@":new URL("../src",import.meta.url).pathname},write:false});
  const module={exports:{}};new Function("require","module","exports",outputFiles[0].text)(createRequire(import.meta.url),module,module.exports);
  const high=module.exports.render(space(3*1024**3));
  assert.match(high,/Restart recommended/);
  assert.match(high,/Restart to release 3\.2 GB of swap files\./);
  assert.match(high,/never deletes it while macOS is using it/);
  assert.match(high,/role="status"/);
  const low=module.exports.render(space(512*1024**2));
  assert.doesNotMatch(low,/Restart recommended|Restart to release/);
  assert.match(low,/Space macOS rebuilds/);
});
