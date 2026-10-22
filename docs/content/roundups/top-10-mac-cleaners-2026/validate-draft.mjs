import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const owned = path.dirname(fileURLToPath(import.meta.url));
const website = '/Users/gabe/code/breathing-room/website';
const article = `${website}/src/content/blog/top-10-mac-cleaners-2026.md`;
const require = createRequire(`${website}/package.json`);
const astroRequire = createRequire(require.resolve('astro/package.json'));
const YAML = astroRequire('yaml');
const { z } = astroRequire('zod');
const { createSatteriMarkdownProcessor } = await import(astroRequire.resolve('@astrojs/markdown-satteri'));
const raw = fs.readFileSync(article, 'utf8');
const [, front, body] = raw.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
const data = YAML.parse(front);
// Evaluate the actual current site schema, without invoking loaders or writing .astro/dist.
const config = fs.readFileSync(`${website}/src/content.config.ts`, 'utf8');
const expression = config.match(/const schema = ([\s\S]*?);\n\nexport const collections/)[1];
const schema = new Function('z', `return (${expression});`)(z);
schema.parse(data);
assert.equal(data.status, 'review');
assert.equal(data.published, false);
assert.equal(String(data.date), '2026-10-22');
const headings = [...body.matchAll(/^### (\d+)\. (.+)$/gm)];
assert.deepEqual(headings.map(h => Number(h[1])), Array.from({ length: 10 }, (_, i) => i + 1));
assert(!/^# /m.test(body), 'H1 supplied by template');
assert(body.trimStart().startsWith('!['), 'top visual follows description');
const images = [...body.matchAll(/!\[([^\]]+)\]\(([^)]+)\)/g)];
assert.equal(images.length, 2);
for (const [, alt, src] of images) {
  assert(alt.length > 30);
  assert(fs.existsSync(`${website}/public${src}`));
}
const internal = [...body.matchAll(/(?<!!)\[[^\]]+\]\((\/[^)]+)\)/g)].map(m => m[1]);
const live = ['/tools/storage-headroom/', '/tools/', '/comparisons/'];
assert(internal.every(p => live.includes(p) || p.startsWith('/assets/roundups/top-10-mac-cleaners-2026/')));
const rendered = await (await createSatteriMarkdownProcessor({ syntaxHighlight: false })).render(body);
assert.equal((rendered.code.match(/<h3\b/g) || []).length, 10);
assert.equal((rendered.code.match(/<table\b/g) || []).length, 1);
const plain = rendered.code.replace(/<[^>]+>/g, ' ').replace(/&#?\w+;/g, ' ');
const wordCount = plain.trim().split(/\s+/).length;
const escape = s => String(s).replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('"', '&quot;');
let html = rendered.code.replace(/src="(\/assets\/[^"]+)"/g, (_, src) => {
  const mime = src.endsWith('.svg') ? 'image/svg+xml' : 'image/png';
  return `src="data:${mime};base64,${fs.readFileSync(`${website}/public${src}`).toString('base64')}"`;
});
html = html.replace('<table>', '<div class="table-scroll" tabindex="0" aria-label="Scrollable workflow comparison"><table>').replace('</table>', '</table></div>');
fs.writeFileSync(`${owned}/review.html`, `<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><meta name="robots" content="noindex,nofollow"><title>Draft fixture: ${escape(data.title)}</title><style>:root{color-scheme:light dark}body{font:18px/1.65 system-ui,sans-serif;margin:auto;padding:24px;max-width:800px}img{max-width:100%;height:auto;display:block}h1{font-size:2rem;line-height:1.2}h2,h3{line-height:1.3}a{color:light-dark(#1753a4,#9bcdff)}.table-scroll{overflow:auto}table{border-collapse:collapse;min-width:660px}th,td{text-align:left;vertical-align:top;border:1px solid #82909a;padding:12px}.fixture{border:2px solid #82909a;padding:12px}</style><main><p class="fixture">Unpublished review fixture, not the site layout. No publication metadata or site-build approval is implied.</p><h1>${escape(data.title)}</h1><p>${escape(data.description)}</p>${html}</main></html>`);
const hash = p => crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const result = { checkedAtUtc: new Date().toISOString(), status: 'passed-scoped-draft-checks', schema: 'actual src/content.config.ts expression via installed Zod', publication: 'review / false', numberedSelections: headings.length, tableRows: (rendered.code.match(/<tr>/g) || []).length - 1, usefulImages: images.length, bodyWordCountRendered: wordCount, titleLength: data.title.length, descriptionLength: data.description.length, internalDestinations: internal, sourceRecords: data.sources.length, articleSha256: hash(article), assets: images.map(([,alt,src]) => ({src,alt,sha256:hash(`${website}/public${src}`)})), notRun: ['pnpm check/build/test: shared output forbidden by task', 'production-layout rendered review', 'independent editorial/factual approval'] };
fs.writeFileSync(`${owned}/validation.json`, JSON.stringify(result, null, 2) + '\n');
console.log(JSON.stringify(result, null, 2));
