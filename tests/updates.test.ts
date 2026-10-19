import test from "node:test";
import assert from "node:assert/strict";
import { updateMessage, type UpdateCheck } from "../src/lib/updates.ts";
const result: UpdateCheck = { configured: false, currentVersion: "0.1.0", version: null, notes: null, installed: false };
test("an unconfigured updater never claims the installed app is up to date", () => {
  assert.match(updateMessage(result), /aren’t connected/);
  assert.match(updateMessage({ ...result, configured: true }), /up to date/);
});
test("available and installed updates have different user decisions", () => {
  assert.match(updateMessage({ ...result, configured: true, version: "0.2.0" }), /signature/);
  assert.match(updateMessage({ ...result, configured: true, installed: true }), /Restart when/);
});
