import test from "node:test";
import assert from "node:assert/strict";
import {createRequire} from "node:module";
import {buildSync} from "esbuild";
test("used-up allowance banner is a non-closable AI Care prompt at the top",()=>{
  const {outputFiles}=buildSync({stdin:{contents:`import {renderToStaticMarkup} from "react-dom/server";import {CleanupQuotaBanner} from "./src/components/cleanup-quota-banner";export function render(quota){return renderToStaticMarkup(<CleanupQuotaBanner quota={quota} onOpen={()=>{}}/>)};`,loader:"tsx",resolveDir:new URL("..",import.meta.url).pathname},bundle:true,platform:"node",format:"cjs",jsx:"automatic",write:false});
  const module={exports:{}};new Function("require","module","exports",outputFiles[0].text)(createRequire(import.meta.url),module,module.exports);
  const free=module.exports.render({plan:"free",limit:4,used:4,remaining:0,period:"2026-11",resetsAt:Date.UTC(2026,11,1)/1000});
  assert.match(free,/role="alert"/);
  assert.match(free,/You’ve used all 4 free cleanups this month\./);
  assert.match(free,/AI Care includes 100 cleanups a month/);
  assert.match(free,/Get AI Care/);
  assert.equal((free.match(/aria-label="Dismiss/g)||[]).length,0);
  const paid=module.exports.render({plan:"ai_care",limit:100,used:100,remaining:0,period:"2026-11",resetsAt:Date.UTC(2026,11,1)/1000});
  assert.match(paid,/You’ve used all 100 AI Care cleanups this month\./);
  assert.match(paid,/Manage AI Care/);
});
