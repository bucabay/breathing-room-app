import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { cleanupSelection, toggleAllCleanup } from "../src/lib/cleanup-review.ts";
import type { AgentCleanupAction } from "../src/lib/agent-cleanup.ts";

const actions: AgentCleanupAction[] = ["cache-a", "cache-b"].map(id => ({ id, title: id, reason: "Rebuildable", impact: "Downloads again", kind: "trash", paths: [`/fixture/${id}`], command: [], estimatedBytes: 100 }));
test("select-all and cleanup totals cannot include manual paths or stale action IDs", () => {
  assert.deepEqual(toggleAllCleanup(actions, true), ["cache-a", "cache-b"]);
  assert.deepEqual(toggleAllCleanup(actions, false), []);
  assert.deepEqual(cleanupSelection(actions, ["cache-a", "/fixture/Original.cap", "attempted-action"]), { ids: ["cache-a"], all: false, partial: true, bytes: 100 });
  assert.deepEqual(cleanupSelection(actions, ["cache-a", "cache-a", "cache-b"]), { ids: ["cache-a", "cache-b"], all: true, partial: false, bytes: 200 });
  assert.deepEqual(cleanupSelection([], ["/fixture/Original.cap"]), { ids: [], all: false, partial: false, bytes: 0 });
});
test("cleanup precedes manual inspection and secondary diagnostics in the same review screen", () => {
  const source = readFileSync(new URL("../src/components/cleanup-assistant.tsx", import.meta.url), "utf8");
  assert.ok(source.indexOf("<CleanupActionList") < source.indexOf("<ReviewStorage"));
  assert.ok(source.indexOf("<ReviewStorage") < source.indexOf('className="cleanup-inspection-details"'));
  for (const file of ["cleanup-action-list.tsx", "review-storage.tsx"]) {
    const source = readFileSync(new URL(`../src/components/${file}`, import.meta.url), "utf8");
    assert.match(source, /<FindingList /);
  }
  const shared = readFileSync(new URL("../src/components/finding-list.tsx", import.meta.url), "utf8");
  assert.doesNotMatch(shared, /agentCleanupApprove|execute_approved_action/);
});
