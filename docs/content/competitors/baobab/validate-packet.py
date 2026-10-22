"""Local integrity checks only; no network, native application or site mutations."""
import datetime
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parent
APP = ROOT.parents[3]


class Text(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.parts = []
        self.feed(html)

    def handle_data(self, value):
        self.parts.append(value)

    def normalized(self):
        return ' '.join(' '.join(self.parts).split())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


checks = []


def check(name, condition):
    assert condition, name
    checks.append({'check': name, 'outcome': 'passed'})


packet = json.loads((ROOT / 'research.json').read_text())
index = json.loads((ROOT / 'evidence-index.json').read_text())
check('JSON packets parse; canonical identity and research-only gates consistent',
      packet['identity']['canonicalOwnerId'] == 'baobab'
      and packet['gates']['researchComplete']
      and not packet['publicationApproved']
      and not packet['gates']['draftingBlocked'])
for item in index:
    path = ROOT / item['path']
    check('Retained original hash/bytes: ' + item['id'],
          sha(path) == item['sha256'] and path.stat().st_size == item['bytes'])

source_ids = {s['id'] for s in packet['sourceLedger']}
claim_ids = {c['id'] for c in packet['claimLedger']}
check('Unique claim and source IDs', len(source_ids) == len(packet['sourceLedger'])
      and len(claim_ids) == len(packet['claimLedger']))
for claim in packet['claimLedger']:
    check('Claim ledger support fields: ' + claim['id'],
          set(claim['sources']) <= source_ids and all(claim.get(k) for k in
          ['excerpt', 'checkedOn', 'scope', 'reviewer', 'evidenceClass', 'location']))
for row in packet['productMatrix']:
    check('Matrix claim references: ' + row['dimension'],
          set(row['claimIds'] + row.get('breathingRoomClaimIds', [])) <= claim_ids)

brew = json.loads((ROOT / 'evidence/homebrew.json').read_text())
check('Package version/licence/dependencies match retained distributor data',
      brew['versions']['stable'] == '50.0' and brew['license'] == 'GPL-2.0-or-later'
      and {'gtk4', 'libadwaita', 'glib'} <= set(brew['dependencies'])
      and not brew['deprecated'] and not brew['disabled'])
check('Exact Mac and Linux bottle keys match record', set(brew['bottle']['stable']['files']) ==
      {'arm64_golden_gate', 'arm64_tahoe', 'arm64_sequoia', 'arm64_sonoma',
       'sonoma', 'arm64_linux', 'x86_64_linux'})
html = (ROOT / 'evidence/gnome-visual-page.html').read_text()
page_text = Text(html).normalized()
check('Official image URL and GPL app-content notice retained',
      packet['visuals'][0]['assetUrl'] in html
      and 'App specific content © The respective app contributors (GPL-2.0+)' in page_text)
check('Official contribution page links canonical repository',
      packet['identity']['repository'] in (ROOT / 'evidence/gnome-contribute.html').read_text())
for filename, passage in [
    ('trash-help.html', 'select Move to Trash'),
    ('trash-help.html', 'empty the Trash'),
    ('remote-help.html', 'accessible remotely'),
    ('permissions-help.html', "won't be used to compute the chart"),
]:
    check('Supporting passage retained: ' + filename + ' / ' + passage,
          passage in Text((ROOT / 'evidence' / filename).read_text()).normalized())

asset_hashes = {}
for visual in packet['visuals']:
    path = APP / visual['originalPath']
    data = path.read_bytes()
    dimensions = struct.unpack('>II', data[16:24])
    check('PNG bytes/dimensions/hash: ' + visual['id'],
          data[:8] == b'\x89PNG\r\n\x1a\n'
          and dimensions == (visual['widthPx'], visual['heightPx'])
          and sha(path) == visual['originalSha256'])
    check('Visual provenance, permission, caption and alt: ' + visual['id'],
          visual['reuse']['status'] == 'cleared' and visual['caption']
          and visual['alt'] and visual['sourcePageUrl']
          and visual['publishedPath'] is None and visual['publishedSha256'] is None)
    asset_hashes[visual['originalPath']] = sha(path)

baseline_path = APP / 'docs/content/.runtime/verification-1/baobab-official.json'
check('Reused verified baseline original hash matches batch register',
      sha(baseline_path) == packet['sourceLedger'][0]['sha256'])
baseline_record = next(p for p in json.loads((APP / 'docs/content/verification/batch-1.json').read_text())['records'] if p['id'] == 'baobab')
check('Corresponding batch-1 record reused', baseline_record['officialName'] == 'Disk Usage Analyzer')
inventory = json.loads((APP / 'docs/content/screenshots.json').read_text())
space = next(a for a in inventory['assets'] if a['id'] == 'current-space-browser-preview')
check('Required first-party caption matches current inventory exactly',
      packet['visuals'][1]['caption'] == space['caption'])

reference_paths = [
    'docs/content/verification/batch-1.json',
    'docs/content/.runtime/verification-1/baobab-official.json',
    'docs/content/.runtime/verification-1/baobab-directory.json',
    'docs/content/capabilities.md', 'docs/content/screenshots.json',
]
result = {
    'jobId': 'research-baobab',
    'validatedAtUtc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'command': 'python3 docs/content/competitors/baobab/validate-packet.py',
    'checks': checks,
    'checkCount': len(checks),
    'referenceSha256': {p: sha(APP / p) for p in reference_paths},
    'artifactSha256': {p.name: sha(p) for p in [ROOT / 'research.json', ROOT / 'research.md', ROOT / 'evidence-index.json']},
    'assetSha256': asset_hashes,
    'manualVisualCheck': 'Both PNGs opened and read using image-capable read tool on 2026-10-21; independent rendered-page review remains pending.',
    'notPerformed': ['Native app installation/testing', 'Cleanup', 'Site check/build/test (no site edits)', 'Browser automation', 'Independent publication review'],
    'limitations': 'Integrity and selected excerpt checks, not semantic proof of every claim or publication approval.',
    'correctionHistory': 'Initial local check failed because the scan-image height was entered as 710 instead of PNG-header 722. Corrected from original bytes; also corrected baseline parser key from products to records before successful rerun.'
}
(ROOT / 'validation.json').write_text(json.dumps(result, indent=2) + '\n')
print(f'PASS: {len(checks)} structural, provenance and selected evidence checks; publication gates pending.')
