import test from "node:test";
import assert from "node:assert/strict";
import { createRequire } from "node:module";
import { buildSync } from "esbuild";
test("answers precede actual features, with escaped untrusted content and safe source links",()=>{
  const {outputFiles}=buildSync({stdin:{contents:`import {renderToStaticMarkup} from "react-dom/server";import {AssistantConversation} from "./src/components/assistant-conversation";export function render(turns){return renderToStaticMarkup(<AssistantConversation turns={turns}/>);}`,loader:"tsx",resolveDir:new URL("..",import.meta.url).pathname},bundle:true,platform:"node",format:"cjs",jsx:"automatic",write:false});
  const module={exports:{}};new Function("require","module","exports",outputFiles[0].text)(createRequire(import.meta.url),module,module.exports);
  const html=module.exports.render([{id:"one",question:"Weather?",reply:{answer:"<script>untrusted</script>",features:["Inspect memory"],sources:["javascript:alert(1)","https://example.org/docs"]}}]);
  assert.ok(html.indexOf("assistant-answer")<html.indexOf("assistant-features"));assert.match(html,/&lt;script&gt;/);assert.doesNotMatch(html,/<script>|javascript:/);assert.match(html,/noopener noreferrer/);assert.doesNotMatch(html,/Cleanup progress|Ready for cleanup/);
});
