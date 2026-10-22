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
const raw = await fs.readFile(`${site}/src/content/blog/mac-cleanup-tools-developers-2026.md`, 'utf8');
const [, yaml, body] = raw.split(/^---\s*$/m);
const schema = z.object({
  title: z.string().trim().min(1), description: z.string().trim().min(1),
  status: z.enum(['draft', 'review', 'published']), published: z.boolean(),
  date: z.coerce.date(), updated: z.coerce.date().optional(), author: z.string().trim().min(1),
  sources: z.array(z.object({ title: z.string().trim().min(1), url: z.url({protocol: /^https?$/}), checked: z.iso.date() }))
}).refine(d => !d.updated || d.updated >= d.date);
const data = schema.parse(parse(yaml));
assert.equal(data.status, 'review'); assert.equal(data.published, false);
assert.equal(data.title, '7 Mac cleanup tools for developers in 2026');
assert.deepEqual([...body.matchAll(/^### (\d)\. /gm)].map(m => +m[1]), [1,2,3,4,5,6,7]);
assert.equal((body.match(/<figure>/g) || []).length, 2);
assert(!/^# /m.test(body)); assert(!body.includes('[INTERNAL-LINK'));
assert(data.description.length >= 150 && data.description.length <= 160);
const hash = b => crypto.createHash('sha256').update(b).digest('hex');
const assets = {};
for (const a of new Set([...body.matchAll(/(?:src|href)="(\/assets\/[^\"]+)"/g)].map(m => m[1]))) {
  assets[a] = hash(await fs.readFile(`${site}/public${a}`));
}
assert.equal(assets['/assets/roundups/mac-cleanup-tools-developers-2026/breathing-room-space-preview.png'], '9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a');
const processor = await createSatteriMarkdownProcessor({ syntaxHighlight: false });
const rendered = await processor.render(body);
assert(rendered.code.includes('<table>')); assert.equal((rendered.code.match(/<h3 /g)||[]).length, 7);
const html = `<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><meta name="robots" content="noindex,nofollow"><title>Draft review: ${data.title}</title><style>
*{box-sizing:border-box}body{font:18px/1.65 system-ui;max-width:900px;margin:auto;padding:24px;color:#17283a;background:white}h1,h2,h3{line-height:1.25}a{color:#245bb1}img{max-width:100%;height:auto}figure{margin:24px 0}figure:first-of-type img{display:block;width:480px;margin:auto}figcaption{font-size:15px}table{display:block;overflow:auto;border-collapse:collapse;font-size:15px}td,th{min-width:150px;border:1px solid #8394a6;padding:10px;vertical-align:top}body.dark{color:#e7eef6;background:#101820}body.dark a{color:#9bc5ff}
</style><body><p>Isolated draft fixture; not the marketing layout or publication approval.</p><h1>${data.title}</h1><p>${data.description}</p>${rendered.code}</body></html>`;
await fs.writeFile(`${owned}/preview.html`, html);
const result = { checkedAtUtc: new Date().toISOString(), schema:'pass: current field shape', draftState:'review/unpublished', shortlistCount:7, figureCount:2, bodyWhitespaceWords:body.trim().split(/\s+/).length, descriptionCharacters:data.description.length, sourceCount:data.sources.length, markdownRender:'pass: installed Astro Satteri; seven numbered sections and comparison table', articleSha256:hash(raw), assets, sharedBuild:'not run: prohibited shared output', independentReview:'pending' };
await fs.writeFile(`${owned}/validation.json`, JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result,null,2));
