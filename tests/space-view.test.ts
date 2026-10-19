import { test } from "node:test";
import assert from "node:assert/strict";
import { spaceSlices } from "../src/lib/space-view.ts";
import type { Bucket } from "../src/lib/model.ts";

const item = (id: string, bytes: number): Bucket => ({ id, name: id, bytes, color: "#3b82f6", files: 1, groups: [] });

test("pie percentages use the displayed measured sizes and conserve the remainder", () => {
  const slices = spaceSlices([item("a", 300), item("b", 200), item("c", 60), item("d", 40)], 2);
  assert.deepEqual(slices.map(slice => [slice.id, slice.bytes]), [["a", 300], ["b", 200], ["space-other", 100]]);
  assert.equal(slices.reduce((sum, slice) => sum + slice.bytes, 0), 600);
  assert.ok(Math.abs(slices.reduce((sum, slice) => sum + slice.percent, 0) - 100) < 1e-9);
  assert.equal(slices[0].percent, 50);
});

test("empty and unknown measurements never become pie slices", () => {
  assert.deepEqual(spaceSlices([item("empty", 0), item("unknown", NaN), item("invalid", -1)]), []);
  assert.equal(spaceSlices([item("only", 50)])[0].percent, 100);
});
