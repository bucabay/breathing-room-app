// Stage immutable universal preview assets. Publish assets before promoting feed.
import { copyFileSync, existsSync, mkdirSync, readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
const root = fileURLToPath(new URL('../', import.meta.url));
const version = JSON.parse(readFileSync(join(root, 'package.json'), 'utf8')).version;
const bundle = join(root, 'src-tauri/target/universal-apple-darwin/release/bundle');
const output = join(root, 'build/releases', `v${version}`);
if (existsSync(output)) throw new Error('Release staging directory exists; review it instead of overwriting an existing release.');
const dmg = readdirSync(join(bundle, 'dmg')).filter(name => name.endsWith('.dmg'));
if (dmg.length !== 1) throw new Error('Expected exactly one universal DMG');
const names = {
  [join(bundle, 'dmg', dmg[0])]: `Breathing-Room_${version}_universal.dmg`,
  [join(bundle, 'macos/Breathing Room.app.tar.gz')]: `Breathing-Room_${version}_universal.app.tar.gz`,
  [join(bundle, 'macos/Breathing Room.app.tar.gz.sig')]: `Breathing-Room_${version}_universal.app.tar.gz.sig`,
};
const signature = readFileSync(join(bundle, 'macos/Breathing Room.app.tar.gz.sig'), 'utf8').trim();
const trusted = Buffer.from(signature, 'base64').toString('utf8').split('\n').find(line => line.startsWith('trusted comment:'));
if (!trusted?.split('\t').includes(`version:${version}`)) throw new Error('Updater signature must bind the exact published version');
mkdirSync(output, { recursive: true });
for (const [source, name] of Object.entries(names)) copyFileSync(source, join(output, name));
const archiveUrl = `https://github.com/bucabay/breathing-room-app/releases/download/v${version}/Breathing-Room_${version}_universal.app.tar.gz`;
const platform = { url: archiveUrl, signature };
const manifest = {
  version,
  notes: readFileSync(join(root, 'RELEASE_NOTES.md'), 'utf8'),
  pub_date: new Date().toISOString(),
  platforms: { 'darwin-aarch64': platform, 'darwin-x86_64': platform },
};
writeFileSync(join(output, 'preview.json'), JSON.stringify(manifest, null, 2) + '\n');
const sums = [...Object.values(names), 'preview.json'].map(name => `${createHash('sha256').update(readFileSync(join(output, name))).digest('hex')}  ${name}`).join('\n');
writeFileSync(join(output, 'SHA256SUMS.txt'), sums + '\n');
console.log(`Staged universal release assets in ${output}. Verify signatures and upload before promoting updates/preview.json.`);
