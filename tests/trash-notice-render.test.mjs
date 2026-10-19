import test from "node:test";
import assert from "node:assert/strict";
import {createRequire} from "node:module";
import {readFileSync} from "node:fs";
import {buildSync} from "esbuild";

test("completion popover explains Trash and offers Finder, never permanent deletion",()=>{
  const {outputFiles}=buildSync({stdin:{contents:`import {renderToStaticMarkup} from "react-dom/server";import {TrashCleanupNotice} from "./src/components/trash-cleanup-notice";export function render(preview){return renderToStaticMarkup(<TrashCleanupNotice bytes={1024} preview={preview} onOpen={()=>{throw new Error("unexpected action")}} onDismiss={()=>{}}/>);}
export function dismiss(){let visible=true;const node=TrashCleanupNotice({bytes:1024,preview:false,onOpen:()=>{},onDismiss:()=>{visible=false}});const close=node.props.children.find(child=>child?.props?.["aria-label"]==="Dismiss Trash reminder");close.props.onClick();return visible;}`,loader:"tsx",resolveDir:new URL("..",import.meta.url).pathname},bundle:true,platform:"node",format:"cjs",jsx:"automatic",write:false});
  const module={exports:{}};new Function("require","module","exports",outputFiles[0].text)(createRequire(import.meta.url),module,module.exports);
  const html=module.exports.render(false);assert.match(html,/Cleanup moved files to Trash/);assert.match(html,/Empty Trash in Finder to reclaim/);assert.match(html,/unrelated files/);assert.match(html,/Open Trash/);assert.doesNotMatch(html,/disabled=""/);assert.doesNotMatch(html,/>Empty Trash<|permanently delete all/);
  assert.match(module.exports.render(true),/disabled=""/);
  assert.match(html,/Dismiss Trash reminder/);assert.doesNotMatch(html,/Collapse|trash-cleanup-compact/);assert.equal(module.exports.dismiss(),false);
  const app=readFileSync(new URL("../src/App.tsx",import.meta.url),"utf8");assert.ok(app.indexOf("<TrashCleanupNotice")>app.indexOf('className="status-dock"'));assert.match(app,/if\(isNew&&moved\)/);
  assert.match(app,/onDismiss=\{\(\)=>setTrashNotice\(null\)\}/);
  const native=readFileSync(new URL("../src-tauri/src/lib.rs",import.meta.url),"utf8");const command=native.slice(native.indexOf("fn open_trash"),native.indexOf("async fn assistant_message"));assert.match(command,/native::open_trash\(\)/);assert.doesNotMatch(command,/remove_dir|unlink|empty trash|osascript|rm -|\/usr\/bin\/open/);
  const bridge=readFileSync(new URL("../src-tauri/src/native.rs",import.meta.url),"utf8");const open=bridge.slice(bridge.indexOf("pub fn open_trash"),bridge.indexOf("pub fn low_battery"));assert.match(open,/URLsForDirectory:inDomains:/);assert.match(open,/openURL:/);assert.doesNotMatch(open,/remove_dir|unlink|osascript/);
  const css=readFileSync(new URL("../src/index.css",import.meta.url),"utf8");assert.match(css,/\.status-dock:has\(\.trash-cleanup-notice\).*border-color:var\(--gain\)/);assert.match(css,/border-left:4px solid var\(--gain\)/);
});
