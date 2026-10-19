import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { reviewStorageGroups, selectedReviewLocations, reviewStorageLocations } from "../src/lib/review-storage.ts";
import type { ReviewStorageLocation } from "../src/lib/agent-cleanup.ts";

const original: ReviewStorageLocation = {
  path: "/fixture/Example.cap", title: "Example.cap", bytes: 4096, logicalBytes: 4096,
  modifiedAt: 0, fileCount: 1, partial: false, severity: "critical",
  recoverability: "not-rebuildable", warning: "Originals cannot be rebuilt.",
  reviewOnly: true, cleanupEligible: false, requiresSelection: true,
};
test("originals and unknown data have distinct review severities, with no default selection", () => {
  const unknown = { ...original, path: "/fixture/Other", severity: "warning" as const, recoverability: "unknown" as const };
  const groups = reviewStorageGroups([original, unknown]);
  assert.deepEqual(groups.critical, [original]); assert.deepEqual(groups.warning, [unknown]);
  assert.deepEqual(selectedReviewLocations([original, unknown], []), []);
  assert.deepEqual(selectedReviewLocations([original, unknown], [original.path]), [original]);
  assert.deepEqual(selectedReviewLocations([original], ["action-id"]), []);
  assert.deepEqual(selectedReviewLocations([{ ...original, cleanupEligible: true } as unknown as ReviewStorageLocation], [original.path]), []);
});
test("review renderer requires selection, warns of original loss and cannot approve cleanup", () => {
  const source = readFileSync(new URL("../src/components/review-storage.tsx", import.meta.url), "utf8");
  assert.match(source, /useState<string\[\]>\(\[\]\)/);
  assert.match(source, /disabled=\{!checked\}/);
  assert.match(source, /item\.warning/);
  assert.match(source, /source footage and editable timeline/);
  assert.doesNotMatch(source, /agentCleanupApprove|onApprove|execute_approved_action/);
});
test("inventory originals join review without duplicating project interiors or inaccessible files", () => {
  const media = { ...original, path: "/fixture/Other.mov", kind: "file", category: "media", owned: true, state: "complete" };
  assert.equal(reviewStorageLocations([original], [media]).length, 2);
  assert.deepEqual(reviewStorageLocations([original], [{ ...media, path: `${original.path}/content/source.mp4` }]), [original]);
  assert.deepEqual(reviewStorageLocations([], [{ ...media, state: "inaccessible" }]), []);
  assert.deepEqual(reviewStorageLocations([], [{ ...media, owned: false }]), []);
});
