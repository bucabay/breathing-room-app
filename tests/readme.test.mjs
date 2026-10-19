import test from 'node:test';
import assert from 'node:assert/strict';
import { existsSync, readFileSync } from 'node:fs';
const root = new URL('../', import.meta.url);
test('project README links the website and includes valid, labeled example-data screenshots', () => {
  const readme = readFileSync(new URL('README.md', root), 'utf8');
  assert.ok(readme.includes('[Website](https://breathing-room.chatic.ai/)'));
  assert.ok(readme.includes('https://breathing-room.chatic.ai/download/'));
  assert.ok(readme.includes('earlier browser preview'));
  assert.doesNotMatch(readme, /\$4\.99|\$5 (?:once|one.time)|github\.com\/bucabay\/breathing-room(?:\)|\/)/);
  const images = [...readme.matchAll(/!\[[^\]]+\]\(([^)]+)\)/g)];
  assert.ok(images.length >= 1);
  for (const [, path] of images) {
    assert.ok(path.startsWith('docs/screenshots/'));
    const png = readFileSync(new URL(path, root));
    assert.equal(png.subarray(0, 8).toString('hex'), '89504e470d0a1a0a');
    assert.ok(png.readUInt32BE(16) >= 900 && png.readUInt32BE(20) >= 600);
  }
  for (const [, target] of readme.matchAll(/(?<!!)\[[^\]]+\]\(([^)]+)\)/g)) {
    if (!target.startsWith('https://') && !target.startsWith('#')) assert.ok(existsSync(new URL(target, root)), target);
  }
});
