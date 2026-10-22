import { readFileSync, writeFileSync, realpathSync, mkdirSync, copyFileSync, existsSync } from 'node:fs';
import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';
import { createHash } from 'node:crypto';
import assert from 'node:assert/strict';

const site = '/Users/gabe/code/breathing-room/website';
const app = '/Users/gabe/code/breathing-room-app';
const out = `${app}/docs/content/roundups/free-mac-cleaners-2026`;
const asset = `${site}/public/assets/roundups/free-mac-cleaners-2026`;
const article = `${site}/src/content/blog/free-mac-cleaners-2026.md`;
const requireAstro = createRequire(realpathSync(`${site}/node_modules/astro/package.json`));
const { createSatteriMarkdownProcessor } = await import(pathToFileURL(requireAstro.resolve('@astrojs/markdown-satteri')));
const { parseFrontmatter } = await import(pathToFileURL(`${site}/node_modules/astro/dist/markdown/index.js`));
const { z } = await import(pathToFileURL(`${site}/node_modules/astro/dist/zod.js`));
const { isPublished } = await import(pathToFileURL(`${site}/src/lib/publication.ts`));
const input = readFileSync(article, 'utf8');
const fm = parseFrontmatter(input);
const schemaText = readFileSync(`${site}/src/content.config.ts`, 'utf8').split('const schema = ')[1].split('\n\nexport const collections')[0].trim().replace(/;$/, '');
const schema = new Function('z', `return (${schemaText})`)(z);
const data = schema.parse(fm.frontmatter);
const body = input.split('---').slice(2).join('---');
assert.equal(data.status, 'review');
assert.equal(data.published, false);
assert.equal(isPublished(data), false);
assert.equal((body.match(/^### [1-7]\. /gm) || []).length, 7);
assert.equal((body.match(/<figure>/g) || []).length, 2);
assert.equal((body.match(/^# /gm) || []).length, 0);
assert.ok(body.trim().startsWith('<figure>'));
assert.ok(!/\[INTERNAL-LINK|\[IMAGE|TODO|TBD/.test(body));
mkdirSync(`${out}/preview`, { recursive: true });
const sourcePreview = `${app}/docs/content/assets/breathing-room/space-preview-2026-10-21.png`;
const hash = p => createHash('sha256').update(readFileSync(p)).digest('hex');
assert.equal(hash(sourcePreview), '9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a');
copyFileSync(sourcePreview, `${asset}/breathing-room-space-preview.png`);
const links = [...body.matchAll(/\]\((\/[^)]+)\)/g)].map(m => m[1]);
for (const link of links) assert.ok(existsSync(`${site}/src/pages${link}index.astro`) || existsSync(`${site}/src/pages${link.slice(0,-1)}.astro`), link);
for (const src of [...body.matchAll(/src="(\/assets\/[^\"]+)"/g)].map(m => m[1])) assert.ok(existsSync(`${site}/public${src}`));
const processor = await createSatteriMarkdownProcessor();
const rendered = await processor.render(body);
const html = rendered.code;
assert.ok(html.includes('<table>'));
assert.equal((html.match(/<figure>/g) || []).length, 2);
const escape = s => s.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('"','&quot;');
// Isolated readability fixture only: no shared Astro build, no public draft route.
const fixture = `<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><meta name="robots" content="noindex,nofollow"><title>${escape(data.title)} — isolated draft fixture</title><style>html{color-scheme:light dark}body{font:18px/1.65 system-ui,sans-serif;max-width:780px;margin:auto;padding:24px;background:light-dark(#fff,#10151e);color:light-dark(#172235,#e4edfa)}h1{line-height:1.15}img{max-width:100%;height:auto}figure{margin:24px 0}figcaption{font-size:15px}a{color:light-dark(#234bad,#9ac4ff)}.table-wrap{overflow:auto}table{border-collapse:collapse;min-width:720px;font-size:15px}td,th{border:1px solid #8491a3;padding:12px;text-align:left;vertical-align:top}h2,h3{line-height:1.25;margin-top:2em}</style><body><p>UNPUBLISHED · isolated Markdown readability fixture, not site-layout approval</p><h1>${escape(data.title)}</h1><p>${escape(data.description)}</p>${html.replace('<table>','<div class="table-wrap" tabindex="0" aria-label="Comparison table, horizontally scrollable"><table>').replace('</table>','</table></div>')}</body></html>`;
writeFileSync(`${out}/preview/index.html`, fixture);
mkdirSync(`${out}/preview/assets/roundups/free-mac-cleaners-2026`, {recursive:true});
for(const name of ['free-choice-workflow.svg','breathing-room-space-preview.png']) copyFileSync(`${asset}/${name}`,`${out}/preview/assets/roundups/free-mac-cleaners-2026/${name}`);
const report = {
  checkedAtUtc: new Date().toISOString(),
  checks: ['Actual site content schema: PASS','Review/unpublished flags: PASS','Actual isPublished excludes record: PASS','Exactly seven numbered selections: PASS','Two figures with top visual: PASS','No placeholder markers: PASS','Internal links resolve to existing tool page sources: PASS','Asset paths exist: PASS','First-party original SHA-256 matches library: PASS','Astro Satteri Markdown renders table and two figures: PASS'],
  bodyWhitespaceWords:body.split(/\s+/).filter(Boolean).length,
  descriptionCharacters:data.description.length,
  sources:data.sources.length,
  hashes:{article:hash(article),diagram:hash(`${asset}/free-choice-workflow.svg`),preview:hash(`${asset}/breathing-room-space-preview.png`)},
  pending:['Full site check/build/tests not run: shared outputs forbidden by this task','Independent factual/editorial review','Production layout, canonical/social/schema and feed exclusion review','Responsive readability fixture inspection is not production layout approval']
};
writeFileSync(`${out}/validation.json`,JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify(report,null,2));
