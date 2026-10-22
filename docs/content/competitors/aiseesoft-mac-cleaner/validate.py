"""Structural/evidence validation only, not a publication or runtime test."""
import hashlib
import json
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP = ROOT.parents[3]
d = json.loads((ROOT / 'research.json').read_text())
checks = []
def check(ok, message):
    assert ok, message
    checks.append(message)

sources = {s['id']: s for s in d['sources']}
for s in sources.values():
    p = APP / s['snapshotPath']
    check(hashlib.sha256(p.read_bytes()).hexdigest() == s['sha256'], f"Source hash matches: {s['id']}")
    if s.get('textPath'):
        check(hashlib.sha256((APP / s['textPath']).read_bytes()).hexdigest() == s['textSha256'], f"Text hash matches: {s['id']}")
for c in d['claims']:
    s = sources[c['sourceIds'][0]]
    p = APP / s.get('textPath', s['snapshotPath'])
    text = p.read_text()
    if p.suffix == '.json': text = json.loads(text)['text']
    check(c['excerpt'] in text, f"Claim excerpt retained: {c['id']}")
    check(bool(c['sourceUrl'] and c.get('checkedAtUtc', c.get('checkedOn'))), f"Claim URL/date present: {c['id']}")
ids = {c['id'] for c in d['claims']}
check(len(ids) == len(d['claims']), 'Claim IDs unique')
for row in d['matrix']:
    check(all(x in ids for x in row['claimIds'] + row['breathingRoomClaimIds']), f"Matrix references resolve: {row['dimension']}")
v = d['visuals'][0]
check('/images/mac-cleaner/clean-large-old-files.jpg' in (APP / sources['guide']['snapshotPath']).read_text(), 'Official guide contains selected competitor app-UI asset reference')
check(v['reuse']['status'] == 'link-only' and v['originalSha256'] is None and v['originalPath'] is None, 'No unpermitted image download or invented image hash')
v = d['visuals'][1]
image = Path(v['originalPath']).read_bytes()
check(hashlib.sha256(image).hexdigest() == v['originalSha256'], 'Breathing Room preview SHA-256 matches inventory')
check(struct.unpack('>II', image[16:24]) == (v['widthPx'], v['heightPx']), 'Breathing Room preview PNG dimensions match')
check('Example data only' in v['caption'] and 'not a native scan' in v['caption'], 'Required example-data/native limitation caption retained')
check(d['identity']['canonicalOwnerId'] == d['productId'] and not d['identity']['aliasSkipDecision']['skip'], 'Distinct identity/canonical owner and explicit non-skip decision recorded')
check(d['status'] == 'blocked' and not d['review']['draftingAllowed'] and not d['published'], 'Critical missing rights evidence blocks drafting/publication')
check(d['versionAndPlatform']['exactVersion'] is None, 'Unverified exact version remains null')
check(len(d['blockers']) == 2 and 'bundle-renewal' in ids, 'Compatibility conflict, rights blocker and bundle renewal retained')
inventory = {str(p.relative_to(APP)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(ROOT.rglob('*')) if p.is_file() and p.name != 'validation.json'}
check(all(not p.is_symlink() for p in ROOT.rglob('*')), 'Owned packet inventory has no symlinks; file hashes recorded')
result = {'status': 'passed-structural-checks-research-still-blocked', 'checks': checks, 'count': len(checks), 'artifactSha256': inventory, 'limitations': ['Not independent editorial approval, screenshot visual clearance, native test, installer check or site build.', 'Competitor image not downloaded or visually inspected.']}
(ROOT / 'validation.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'status': result['status'], 'checksPassed': len(checks)}, indent=2))
