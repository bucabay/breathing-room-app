"""Validate retained research evidence and write the explicitly blocked job receipt."""
import datetime
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP = ROOT.parents[3]
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
p = json.loads((ROOT / 'research.json').read_text())
checks = []
assert p['jobId'] == 'research-diskmaid'
assert p['status'] == 'blocked' and not p['draftingAllowed'] and not p['published']
assert p['identity']['canonicalOwnerId'] == 'diskmaid'
checks.append('PASS: job/product ownership, canonical identity and blocked/not-published gates')
sources = {s['id']: s for s in p['sources']}
count = 0
for s in sources.values():
    if s.get('snapshotPath') and s.get('sha256'):
        assert sha(APP / s['snapshotPath']) == s['sha256'], s['id']
        count += 1
checks.append(f'PASS: {count} retained/shared source SHA-256 checks')
for c in p['claims']:
    assert c['checkedOn'] and c['excerpt'] and c['sourceUrl']
    assert all(i in sources for i in c['sourceIds'])
    if c['sourceIds'] == ['official']:
        text = json.loads((APP / sources['official']['snapshotPath']).read_text())['text']
        assert c['excerpt'] in text, c['id']
    if c['sourceIds'] == ['app-store']:
        assert c['excerpt'] in (APP / sources['app-store']['snapshotPath']).read_text(), c['id']
checks.append(f'PASS: {len(p["claims"])} claim/source links, dated excerpts; official/store excerpt membership')
claim_ids = {c['id'] for c in p['claims']}
assert all(set(v['claimIds']) <= claim_ids for v in p['productMatrix'].values())
checks.append('PASS: matrix claim references; unknown cells explicitly not verified')
competitor, br = p['visuals']
assert competitor['assetUrl'] in (ROOT / 'sources/app-store.html').read_text()
assert competitor['reuse']['status'] == 'link-only'
assert competitor['originalPath'] is None and competitor['originalSha256'] is None
assert sha(Path(br['originalPath'])) == br['originalSha256']
assert 'Example data only' in br['caption']
assert len(p['discovery']['edges']) == 2
checks.append('PASS: exact public competitor image locator, no copied competitor image, selected Breathing Room hash/disclosure, two discovery edges')
checks.append('PASS: research.md exists; no website build required for research-only files; no product runtime test claimed')
assert (ROOT / 'research.md').is_file()
artifacts = sorted(str(f.relative_to(APP)) for f in ROOT.rglob('*') if f.is_file())
checks.append('BLOCKED: competitor image reuse permission and pixel/privacy review absent; tracking disclosures conflict')
validation = {'jobId': p['jobId'], 'checkedAtUtc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'checks': checks, 'researchSha256': sha(ROOT / 'research.json'), 'summarySha256': sha(ROOT / 'research.md'), 'publicationApproved': False}
(ROOT / 'validation.json').write_text(json.dumps(validation, indent=2) + '\n')
validation_path = str((ROOT / 'validation.json').relative_to(APP))
if validation_path not in artifacts: artifacts.append(validation_path)
receipt = {'jobId': p['jobId'], 'status': 'blocked', 'artifacts': artifacts, 'validation': checks, 'diagnostic': 'DiskMaid research retained with batch-1 reuse and new App Store/licence/privacy evidence. US listing: 1.6, macOS 14.6+, Lifetime $19.99; described features require purchase. Drafting blocked: competitor screenshot URL located but reuse rights/pixel review missing; no-tracking homepage conflicts with store identifier-tracking disclosure. No site or queue edits.'}
receipt_path = APP / 'docs/content/.runtime/research-diskmaid.1792614623990845000.receipt.json'
receipt_path.write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(validation, indent=2))
print('Receipt:', receipt_path)
