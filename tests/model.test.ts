import { test } from "node:test";
import assert from "node:assert/strict";
import { buckets, dailyDue, defaultSettings, formatBytes, type StorageGroup } from "../src/lib/model.ts";
const inventory: StorageGroup[] = [
  { id: "1", name: "npm", owner: "npm", category: "development", project: "", bytes: 100, files: 2 },
  { id: "2", name: "Website", owner: "Projects", category: "development", project: "Website", bytes: 200, files: 3 },
  { id: "3", name: "Images", owner: "Personal", category: "images", project: "", bytes: 400, files: 4 },
];
test("every storage view conserves the same measured inventory", () => {
  for (const view of ["category", "owner", "project"] as const) assert.equal(buckets(inventory, view).reduce((n, b) => n + b.bytes, 0), 700);
  assert.equal(buckets(inventory, "project").find((b) => b.id === "Outside projects")?.bytes, 500);
});
test("daily scheduling respects disabled settings, local days and midnight windows", () => {
  const settings = { ...defaultSettings, enabled: true, hour: 23, windowHours: 3 };
  assert.equal(dailyDue(settings, "", new Date(2026, 9, 3, 0)), true);
  assert.equal(dailyDue(settings, "2026-10-3", new Date(2026, 9, 3, 0)), false);
  assert.equal(dailyDue(settings, "", new Date(2026, 9, 3, 3)), false);
  assert.equal(dailyDue({ ...settings, enabled: false }, "", new Date(2026, 9, 3, 0)), false);
});
test("unknown and negative sizes are never shown as recovered bytes", () => {
  assert.equal(formatBytes(NaN), "Unavailable"); assert.equal(formatBytes(-1), "Unavailable"); assert.equal(formatBytes(0), "0 B");
});
