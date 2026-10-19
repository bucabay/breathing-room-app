import test from "node:test";
import assert from "node:assert/strict";
import {createRequire} from "node:module";
import {buildSync} from "esbuild";

test("preview shows only three compact rows; the separate screen retains all exact details",()=>{
  const {outputFiles}=buildSync({stdin:{contents:`import {renderToStaticMarkup} from "react-dom/server";import {ApprovedLocationsPreview,ApprovedLocationsScreen} from "./src/components/approved-locations";export function render(approvals,full=false){const props={approvals,onRevoke:async()=>{},onError:()=>{}};return renderToStaticMarkup(full?<ApprovedLocationsScreen {...props} onBack={()=>{}}/>:<ApprovedLocationsPreview {...props} onViewAll={()=>{}}/>);}`,loader:"tsx",resolveDir:new URL("..",import.meta.url).pathname},bundle:true,platform:"node",format:"cjs",jsx:"automatic",write:false});
  const module={exports:{}};new Function("require","module","exports",outputFiles[0].text)(createRequire(import.meta.url),module,module.exports);
  const approvals=Array.from({length:8},(_,index)=>({key:`native-key-${index}`,approvedAt:1,action:{id:String(index),title:`Cache ${index}`,kind:"trash",paths:[`/Users/example/Projects/long-project/build-${index}/<source>`],command:[],reason:"Measured",impact:"Rebuild required",estimatedBytes:1}}));
  const preview=module.exports.render(approvals);assert.equal((preview.match(/class="approved-location-row"/g)||[]).length,3);assert.match(preview,/View all 8 approvals/);assert.doesNotMatch(preview,/Cache 3/);assert.match(preview,/~\/Projects\//);assert.doesNotMatch(preview,/<source>/);
  const full=module.exports.render(approvals,true);assert.equal((full.match(/class="approved-location-row"/g)||[]).length,8);assert.match(full,/Back to Daily care/);assert.match(full,/Filter approved locations/);assert.match(full,/Cache 7/);assert.match(full,/\/Users\/example\/Projects\/long-project\/build-7\/&lt;source&gt;/);assert.match(full,/Revoke approval/);
});
