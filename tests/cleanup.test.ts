import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

const catalog = JSON.parse(readFileSync(new URL("../scripts/cleanup/catalog.json", import.meta.url), "utf8"));
test("each usage workflow has ten distinct discovery types and offline adapters", () => {
  assert.equal(catalog.rules.length, 100);
  for (const profile of Object.keys(catalog.profiles)) {
    const rules = catalog.rules.filter((r: { profiles: string[] }) => r.profiles.includes(profile));
    assert.ok(new Set(rules.map((r: { type: string }) => r.type)).size >= 10, profile);
  }
  for (const rule of catalog.rules) {
    assert.ok(rule.patterns.length);
    assert.ok(["tool-cache.py", "trash-selected.py", "inspect-only.py"].includes(rule.adapter));
    assert.ok(rule.impactLevel >= 1 && rule.impactLevel <= 5);
    assert.ok(!("command" in rule));
  }
});
