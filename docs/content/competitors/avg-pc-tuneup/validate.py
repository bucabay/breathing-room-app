"""Read-only research validation; writes only this packet's validation log."""
import hashlib
import json
import re
import struct
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
packet = json.loads((HERE / 'research.json').read_text())
checks = []


def check(name, passed, detail):
    checks.append({'check': name, 'passed': bool(passed), 'detail': detail})


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def norm(text):
    return re.sub(r'\s+', ' ', text).casefold()


sources = {s['id']: s for s in packet['sources']}
claims = {c['id']: c for c in packet['claims']}
support = json.loads((HERE / 'sources/support-excerpts.json').read_text())
texts = {}
for sid, source in sources.items():
    path = ROOT / source['path']
    check('source-path:' + sid, path.is_file(), source['path'])
    if source.get('sha256'):
        check('source-hash:' + sid, digest(path) == source['sha256'], digest(path))
    if sid in ('faq', 'guide', 'install', 'requirements'):
        item = next(s for s in support['sources'] if s['id'] == sid)
        texts[sid] = ' '.join(x['text'] for x in item['excerpts'])
    else:
        texts[sid] = path.read_text()
        if sid in ('pc', 'mac'):
            texts[sid] = json.loads(texts[sid])['text']
        if sid == 'discovery':
            texts[sid] = ' '.join(a['text'] for a in json.loads(texts[sid])['links'])
        if sid == 'br':
            texts[sid] += '\n' + '\n'.join(
                (ROOT / p).read_text() for p in
                ('README.md', 'RELEASE_NOTES.md', 'src-tauri/tauri.conf.json',
                 'src-tauri/src/cleanup_discovery.rs'))

for claim in packet['claims']:
    check('claim-sources:' + claim['id'],
          all(s in sources for s in claim['sourceIds']), claim['sourceIds'])
    for excerpt in claim['excerpts']:
        check('claim-excerpt:' + claim['id'],
              any(norm(excerpt) in norm(texts[s]) for s in claim['sourceIds']), excerpt)
    check('claim-state:' + claim['id'],
          claim['state'] in ('verified', 'not-verified', 'contradicted', 'stale'), claim['state'])

for row in packet['matrix']:
    check('matrix-refs:' + row['dimension'],
          all(c in claims for c in row['claimIds']), row['claimIds'])

br = next(v for v in packet['visuals'] if v['productId'] == 'breathing-room')
image = ROOT / br['originalPath']
check('br-visual-hash', digest(image) == br['originalSha256'], digest(image))
width, height = struct.unpack('>II', image.read_bytes()[16:24])
check('br-visual-dimensions', (width, height) == (br['widthPx'], br['heightPx']), [width, height])
check('br-example-label', 'Example data only' in br['caption'] and br['dataMode'] == 'example', br['caption'])
avg = next(v for v in packet['visuals'] if v['productId'] == 'avg-pc-tuneup')
mac = json.loads((HERE / 'sources/mac-official.json').read_text())
check('avg-real-asset-dom', any(i['src'] == avg['assetUrl'] for i in mac['images']), avg['assetUrl'])
check('rights-gate-honest', avg['reuse']['status'] == 'link-only' and avg['originalPath'] is None
      and avg['originalSha256'] is None and not packet['validation']['draftingAllowed'],
      'No third-party downloadable original or publication clearance claimed')
check('canonical-owner', packet['identity']['canonicalOwnerId'] == 'avg-pc-tuneup'
      and packet['identity']['aliasDecision']['skipSeparateAliasDrafts'], 'Alias drafts suppressed under one owner')
check('blocked-state', packet['status'] == 'blocked' and len(packet['blockers']) > 0,
      'Image reuse blocks drafting; claim-specific OS/trial conditions retained')
check('json-parse', True, 'research.json, mac-official.json and support-excerpts.json parsed')
result = {
    'checkedAtUtc': datetime.now(timezone.utc).isoformat(),
    'command': 'python3 docs/content/competitors/avg-pc-tuneup/validate.py',
    'passed': all(c['passed'] for c in checks),
    'checks': checks,
    'artifactSha256': {
        str(p.relative_to(ROOT)): digest(p) for p in sorted(HERE.rglob('*'))
        if p.is_file() and p.name != 'validation.json'
    },
    'limitations': 'Structural integrity and retained-excerpt matching, not independent fact/rights/native QA. Website unchanged; site builds not applicable.'
}
(HERE / 'validation.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'passed': result['passed'], 'checks': len(checks),
                  'failures': [c for c in checks if not c['passed']]}, indent=2))
raise SystemExit(0 if result['passed'] else 1)
