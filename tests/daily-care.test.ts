import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

test("manual, conversational and scheduled care enter the shared agent, with no local-rules daily endpoint",()=>{
  const native=readFileSync(new URL("../src-tauri/src/lib.rs",import.meta.url),"utf8");
  const api=readFileSync(new URL("../src/lib/api.ts",import.meta.url),"utf8");
  assert.equal((native.match(/cleanup_session::inspect_configured\(/g)||[]).length,3);
  assert.match(native,/"start_disk_discovery"=>\{let id=cleanup_session::inspect_configured/);
  assert.equal(native.includes("fn daily("),false);assert.equal(native.includes("run_daily_care"),false);
  assert.equal(api.includes('invoke("run_daily_care"'),false);
  assert.ok(api.includes('invoke("agent_cleanup_inspect", { request, scope, model, automatic, limits,daily })'));
});
