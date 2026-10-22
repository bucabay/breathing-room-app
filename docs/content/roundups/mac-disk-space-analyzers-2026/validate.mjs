import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import { createRequire } from 'node:module';

const site = '/Users/gabe/code/breathing-room/website';
const owned = path.dirname(new URL(import.meta.url).pathname);
const require = createRequire(await fs.realpath(`${site}/node_modules/astro/package.json`));
const { parse } = require('yaml');
const { z } = require('zod');
const { createSatteriMarkdownProcessor } = await import(require.resolve('@astrojs/markdown-satteri'));
const file = `${site}/src/content/blog/mac-disk-space-analyzers-2026.md`;
const raw = await fs.readFile(file, 'utf8');
const [, yaml, body] = raw.split(/^---\s*$/m);
const schema = z.object({
  title: z.string().trim().min(1), description: z.string().trim().min(1),
  status: z.enum(['draft', 'review', 'published']), published: z.boolean(),
  date: z.coerce.date(), updated: z.coerce.date().optional(), author: z.string().trim().min(1),
  sources: z.array(z.object({ title: z.string().trim().min(1), url: z.url({protocol: /^https?$/}), checked: z.iso.date() }))
}).refine(d => !d.updated || d.updated >= d.date);
const data = schema.parse(parse(yaml));
assert.equal(data.status, 'review');
assert.equal(data.published, false);
assert.equal((body.match(/^### [1-8]\. /gm) || []).length, 8);
assert.equal((body.match(/<figure>/g) || []).length, 2);
assert.equal((body.match(/^# /gm) || []).length, 0);
assert(!body.includes('[INTERNAL-LINK'));
const assets = [...new Set([...body.matchAll(/(?:src|href)="(\/assets\/[^\"]+)"/g)].map(m => m[1]))];
const hashes = {};
for (const a of assets) {
  const bytes = await fs.readFile(`${site}/public${a}`);
  hashes[a] = crypto.createHash('sha256').update(bytes).digest('hex');
}
assert.equal(hashes['/assets/roundups/mac-disk-space-analyzers-2026/breathing-room-space-preview.png'], '9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a');
const processor = await createSatteriMarkdownProcessor({ syntaxHighlight: false });
const rendered = await processor.render(body);
assert(rendered.code.includes('<table>'));
assert.equal((rendered.code.match(/<h3 /g) || []).length, 8);
// This isolated fixture does not alter Astro's draft filtering or shared output.
const html = `<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><meta name="robots" content="noindex,nofollow"><title>Review fixture: ${data.title}</title><style>
*{box-sizing:border-box}body{font:18px/1.65 system-ui;margin:auto;padding:24px;max-width:900px;color:#17283a;background:#fff}h1{line-height:1.15}h2,h3{line-height:1.3}a{color:#245bb1}img{max-width:100%;height:auto}figure{margin:24px 0}figure:first-of-type img{display:block;margin:auto;width:480px}figcaption{font-size:15px}table{display:block;overflow:auto;border-collapse:collapse;font-size:15px}td,th{min-width:150px;border:1px solid #8394a6;padding:10px;vertical-align:top}td:first-child,th:first-child{min-width:130px}body.dark{color:#e7eef6;background:#101820}body.dark a{color:#9bc5ff}body.dark td,body.dark th{border-color:#8498af} .fixture{border:1px solid;padding:10px;font-size:14px}
</style><body><p class="fixture">Isolated draft review fixture, not the site layout or a public route. Scroll the comparison table horizontally.</p><h1>${data.title}</h1><p>${data.description}</p>${rendered.code}</body></html>`;
await fs.writeFile(`${owned}/preview.html`, html);
const result = {checkedAtUtc: new Date().toISOString(), schema: 'pass (matches current content fields)', draftState: 'review/unpublished', shortlistCount: 8, figureCount: 2, wordCountWhitespace: body.trim().split(/\s+/).length, titleCharacters: data.title.length, descriptionCharacters: data.description.length, sourceCount: data.sources.length, markdownRender: 'pass using installed Astro Satteri processor; table and eight h3 sections present', assets: hashes, articleSha256: crypto.createHash('sha256').update(raw).digest('hex'), sharedBuild: 'not run: job prohibits shared build output', independentReview: 'pending'};
await fs.writeFile(`${owned}/validation.json`, JSON.stringify(result, null, 2) + '\n');
console.log(JSON.stringify(result, null, 2));
