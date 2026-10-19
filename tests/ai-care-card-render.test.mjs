import test from "node:test";
import assert from "node:assert/strict";
import {createRequire} from "node:module";
import {buildSync} from "esbuild";
test("home and sidebar use the same plain-language card with one full-area native button",()=>{
  const {outputFiles}=buildSync({stdin:{contents:`import {renderToStaticMarkup} from "react-dom/server";import {AiCareCard} from "./src/components/ai-care-card";export function render(placement){return renderToStaticMarkup(<AiCareCard placement={placement} onOpen={()=>{}}/>)};export function click(placement){let opened=0;const node=AiCareCard({placement,onOpen:()=>opened++});node.props.onClick();return {type:node.type,opened};}`,loader:"tsx",resolveDir:new URL("..",import.meta.url).pathname},bundle:true,platform:"node",format:"cjs",jsx:"automatic",write:false});
  const module={exports:{}};new Function("require","module","exports",outputFiles[0].text)(createRequire(import.meta.url),module,module.exports);
  for(const placement of ["home","sidebar"]){const html=module.exports.render(placement);assert.match(html,/^<button /);assert.equal((html.match(/<button /g)||[]).length,1);assert.match(html,/type="button"/);assert.match(html,/aria-haspopup="dialog"/);if(placement==="sidebar"){assert.match(html,/ai-care-eyebrow/);assert.match(html,/AI Care/);assert.match(html,/Daily cleanup\. Only what you approve\./);assert.doesNotMatch(html,/Automatic daily cleanup|Choose a time/);}else{assert.match(html,/Automatic daily cleanup/);assert.match(html,/Choose a time\. Clean approved items/);}assert.doesNotMatch(html,/A little intelligence|Care, with context/);assert.deepEqual(module.exports.click(placement),{type:"button",opened:1});}
});
