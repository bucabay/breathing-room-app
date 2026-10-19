import test from "node:test";
import assert from "node:assert/strict";
import { selectionSummary, locationStatus } from "../src/lib/cleanup-selection.ts";
import type { CleanupLocation } from "../src/lib/cleanup.ts";

const location = (id: string, executable: boolean, kind: CleanupLocation["kind"], bytes = 100): CleanupLocation => ({
  id, ruleId: id, name: id, executable, kind, bytes, complete: true, reason: "", path: `/example/${id}`,
  type: "cache", category: "development", profiles: [], files: 1, adapter: "fixture", description: "", impact: "", impactLevel: 2,
  minAgeDays: 0, source: "", evidence: "", patterns: [], judgment: null,
});
test("mixed review selection retains all items but isolates cleanup-eligible IDs", () => {
  const plan = { candidates: [location("cache", true, "tool", 300), location("media", false, "review", 500), location("headers", true, "trash", 200)] };
  const summary = selectionSummary(plan, ["cache", "media", "headers", "cache", "unknown"]);
  assert.deepEqual(summary.items.map(c => c.id), ["cache", "media", "headers"]);
  assert.deepEqual(summary.eligible.map(c => c.id), ["cache", "headers"]);
  assert.deepEqual(summary.reviewOnly.map(c => c.id), ["media"]);
  assert.equal(summary.bytes, 1000);
  assert.equal(summary.eligibleBytes, 500);
  assert.equal(summary.permanent, 1);
  assert.equal(summary.trash, 1);
});
test("partial and inspection-only inventories cannot execute even if incorrectly flagged", () => {
  const partial = { ...location("partial", true, "trash"), complete: false };
  const inspect = location("inspect", true, "review");
  const summary = selectionSummary({ candidates: [partial, inspect] }, ["partial", "inspect"]);
  assert.equal(summary.items.length, 2);
  assert.equal(summary.eligible.length, 0);
  assert.equal(summary.reviewOnly.length, 2);
});
test("location status explains readiness, incomplete coverage and recent activity", () => {
  assert.equal(locationStatus(location("ready", true, "tool")).label, "Ready to clean");
  assert.equal(locationStatus({ ...location("partial", false, "trash"), complete: false }).label, "Incomplete scan");
  assert.equal(locationStatus({ ...location("active", false, "trash"), reason: "Recently changed" }).label, "Recently used");
  assert.equal(locationStatus(location("unknown", false, "review")).label, "Agent will find cleanup");
});
