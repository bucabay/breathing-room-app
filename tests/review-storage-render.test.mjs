import test from "node:test";
import assert from "node:assert/strict";
import { createRequire } from "node:module";
import { buildSync } from "esbuild";

test("manual inspection is collapsed and uses compact shared rows with unchecked selection", () => {
  const { outputFiles } = buildSync({
    stdin: { contents: `import { renderToStaticMarkup } from "react-dom/server";
      import { ReviewStorage } from "./src/components/review-storage";
      export function render(items) { return renderToStaticMarkup(<ReviewStorage items={items} onReveal={() => { throw new Error("Unexpected reveal"); }} />); }`,
      loader: "tsx", resolveDir: new URL("..", import.meta.url).pathname },
    bundle: true, platform: "node", format: "cjs", jsx: "automatic", write: false,
  });
  const module = { exports: {} };
  new Function("require", "module", "exports", outputFiles[0].text)(createRequire(import.meta.url), module, module.exports);
  const item = { path: "/fixture/<script>.cap", title: "<script>.cap", bytes: 4096, logicalBytes: 4096,
    modifiedAt: 0, fileCount: 1, partial: false, severity: "critical", recoverability: "not-rebuildable",
    warning: "Original footage cannot be rebuilt.", reviewOnly: true, cleanupEligible: false, requiresSelection: true };
  const html = module.exports.render([item, { ...item, path: "/fixture/Unknown", title: "Unknown", severity: "warning", recoverability: "unknown" }]);
  assert.equal((html.match(/type="checkbox"/g) || []).length, 2);
  assert.equal((html.match(/disabled=""/g) || []).length, 2);
  assert.doesNotMatch(html, /checked=""|<script>/);
  assert.match(html, /&lt;script&gt;\.cap/);
  assert.match(html, /Not rebuildable/);
  assert.match(html, /Recovery unknown/);
  assert.match(html, /<details class="manual-inspection">/);
  assert.doesNotMatch(html, /<details[^>]*\bopen(?:=|\s|>)/);
  assert.equal((html.match(/class="finding-list"/g) || []).length, 1);
  assert.equal((html.match(/class="finding-row /g) || []).length, 2);
  assert.match(html, /Original footage cannot be rebuilt/);
  assert.match(html, /0 selected for review/);
  assert.equal(module.exports.render([]), "");
});
