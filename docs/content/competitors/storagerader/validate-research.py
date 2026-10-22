"""Read-only packet checks except for the owned validation log."""
import datetime
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
app = root.parents[3]
packet = json.loads((root / 'research.json').read_text())
checks = []
for source in packet['sources']:
    path = app / source['rawPath']
    assert hashlib.sha256(path.read_bytes()).hexdigest() == source['sha256'], source['id']
    checks.append(f"{source['id']}: retained raw SHA-256 matches")
sources = {source['id']: source for source in packet['sources']}
for claim in packet['claims']:
    assert claim['excerpt'] in sources[claim['sourceIds'][0]]['text'], claim['id']
    assert claim['sourceUrls'] and claim['checkedAtUtc'] and claim['scope']
checks.append(f"All {len(packet['claims'])} competitor claims have exact supporting excerpts, URLs, timestamps and scope")
for row in packet['productMatrix']:
    assert all(any(c['id'] == id_ for c in packet['claims']) for id_ in row['claimIds'])
checks.append('All product matrix claim references resolve; unsupported dimensions explicitly remain not verified')
br = packet['breathingRoomEvidence']
register = app / br['path']
assert hashlib.sha256(register.read_bytes()).hexdigest() == br['registerSha256']
for claim in br['claims']:
    assert claim['excerpt'] in register.read_text() and claim['sourceUrls'] and claim['checkedOn']
checks.append('All six Breathing Room caveat claims map to dated reused register excerpts/URLs; register hash matches')
preview = packet['visuals'][1]
assert hashlib.sha256(Path(preview['originalPath']).read_bytes()).hexdigest() == preview['originalSha256']
assert preview['dataMode'] == 'example' and 'Example data only' in preview['caption']
assert preview['buildOrCommit'] and preview['capturedAtUtc']
checks.append('Selected first-party PNG original hash, capture provenance and required example-data caption match inventory')
assert packet['identity']['canonicalOwnerId'] == 'storagerader'
assert packet['identity']['aliasDecision']['skipSeparateAliasDrafts']
assert not packet['identity']['aliasDecision']['skipThisCanonicalProduct']
assert not packet['draftingAllowed'] and packet['status'] == 'blocked'
assert packet['visuals'][0]['reuse']['status'] == 'link-only'
assert packet['visuals'][0]['originalPath'] is None
assert not any(p.suffix.lower() in ('.png', '.jpg', '.jpeg', '.webp', '.gif', '.dmg') for p in root.rglob('*'))
checks.append('Canonical alias deduplication and critical visual-rights block enforced; no competitor image or binary downloaded')
assert (root / 'research.md').is_file()
checks.append('Both required research artifacts exist; no publication approval asserted')
log = dict(checkedAtUtc=datetime.datetime.now(datetime.timezone.utc).isoformat(), status='passed-packet-integrity-only',
           command='PYTHONDONTWRITEBYTECODE=1 python3 docs/content/competitors/storagerader/validate-research.py',
           checks=checks, limitations=['These are packet integrity checks, not rights clearance, app tests or independent editorial approval.',
                                      'Marketing check/build/test not run: no site files edited.',
                                      'Competitor visual not opened or downloaded; gate remains blocked.'])
(root / 'validation.json').write_text(json.dumps(log, indent=2) + '\n')
print(json.dumps(log, indent=2))
