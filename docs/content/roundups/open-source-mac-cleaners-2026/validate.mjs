import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
import { createHash } from 'node:crypto';

const root = '/Users/gabe/code/breathing-room/website';
const own = path.dirname(new URL(import.meta.url).pathname);
const require = createRequire(path.join(root, 'package.json'));
const astroRequire = createRequire(require.resolve('astro'));
const YAML = astroRequire('yaml');
const { z } = astroRequire('zod');
const file = path.join(root, 'src/content/blog/open-source-mac-cleaners-2026.md');
const text = fs.readFileSync(file, 'utf8');
const [, frontmatter, body] = text.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
const data = YAML.parse(frontmatter);
const schemaText = fs.readFileSync(path.join(root, 'src/content.config.ts'), 'utf8')
  .split('const schema = ')[1].split('\n\nexport const collections')[0];
const schema = new Function('z', `return ${schemaText}`)(z);
schema.parse(data);
assert.equal(data.status, 'review');
assert.equal(data.published, false);
assert.equal(String(data.date), '2026-10-22');
assert.equal(data.title, '7 open-source Mac maintenance tools in 2026');
const rows = body.split('\n').filter(line => /^\| \[/.test(line));
assert.equal(rows.length, 7);
assert.equal((body.match(/^## /gm) || []).length, 10);
assert.equal((body.match(/^# /gm) || []).length, 0);
assert.equal((body.match(/!\[/g) || []).length, 2);
const assetPaths = [...body.matchAll(/\]\((\/assets\/[^)]+)\)/g)].map(x => x[1]);
const hash = buffer => createHash('sha256').update(buffer).digest('hex');
const assets = [...new Set(assetPaths)].map(url => {
  const target = path.join(root, 'public', url);
  assert(fs.existsSync(target), target);
  const bytes = fs.readFileSync(target);
  return { url, bytes: bytes.length, sha256: hash(bytes) };
});
const preview = assets.find(x => x.url.endsWith('.png'));
assert.equal(preview.sha256, '9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a');
const internal = [...body.matchAll(/\]\((\/[^)]+)\)/g)].map(x => x[1]).filter(x => !x.startsWith('/assets/'));
assert.deepEqual(internal, ['/tools/']);
assert(!/\[INTERNAL-LINK|TODO|TBD/.test(body));
assert(body.includes('which we build'));
assert(body.includes('not Developer ID signed or notarized'));
assert(body.includes('ISC package conflict'));
const report = { checkedAtUtc: new Date().toISOString(), status: 'passed-scoped-static-checks',
  schema: 'Actual current site schema evaluated against parsed YAML; passed',
  shortlistRows: rows.length, bodyH2: 10, visualCount: 2,
  bodyWordCountApprox: body.replace(/\([^)]*\)/g, '').match(/\b[\w’'-]+\b/g).length,
  titleCharacters: data.title.length, descriptionCharacters: data.description.length,
  internalLinks: internal, assets, articleSha256: hash(Buffer.from(text)),
  pending: ['Shared pnpm check/build/test not run: no shared output authorized.',
    'Independent claim review and six viewport/theme rendered-page reviews not performed.',
    'Draft exclusion statically checked by status/published; built route/feed exclusion still pending.'] };
fs.writeFileSync(path.join(own, 'validation.json'), JSON.stringify(report, null, 2) + '\n');
console.log(JSON.stringify(report, null, 2));
