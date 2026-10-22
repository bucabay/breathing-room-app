"""Offline packet validation; no builds, installs, browser or cleanup."""
import datetime
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP = ROOT.parents[3]
packet = json.loads((ROOT / 'research.json').read_text())
checks = []


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


assert packet['status'] == 'blocked' and packet['draftingAllowed'] is False
assert packet['identity']['canonicalOwnerId'] == 'cleaner-by-ciro-cesar-maciel'
assert packet['identity']['aliasDecision']['skip'] is False
checks.append('PASS: explicit blocked drafting gate, distinct canonical identity and no alias skip.')
text = {}
for source in packet['sources']:
    path = APP / source['snapshotPath']
    assert sha(path) == source['sha256'], source['id']
    raw = path.read_text()
    if source['id'] in ('official', 'discovery'):
        raw = json.loads(raw)['text']
    text[source['id']] = raw
checks.append(f"PASS: all {len(packet['sources'])} retained source/register SHA-256 values match actual files.")
for claim in packet['claims'] + packet['breathingRoom']['comparisonClaims']:
    assert claim['supportingExcerpt'] in text[claim['sourceIds'][0]], claim['id']
    assert claim['checkedAtUtc']
    assert claim.get('sourceUrl') or claim.get('sourceUrls')
checks.append('PASS: 23 competitor claims and 4 reused Breathing Room register excerpts match retained text, with URLs and check timestamps.')
ids = {c['id'] for c in packet['claims']}
for row in packet['productMatrix']:
    assert set(row['claimIds']) <= ids
checks.append(f"PASS: {len(packet['productMatrix'])} matrix rows resolve to claim IDs.")
competitor, br = packet['visuals']
assert competitor['reuse']['status'] == 'link-only'
assert competitor['originalPath'] is None and competitor['originalSha256'] is None
assert 'docs/cleanup.webp' in competitor['assetUrl']
assert 'docs/cleanup.webp' in text['readme']
assert sha(Path(br['sourcePath'])) == br['originalSha256']
assert br['actualNativeScan'] is False
assert 'Example data only' in br['caption']
checks.append('PASS: official Cleanup image reference exists in README; no downloaded image/hash invented; selected first-party preview hash and example/native labels verified.')
assert packet['versionScope']['repositoryVersion'] == text['version'].strip() == '0.4.0'
assert packet['versionScope']['publishedRelease']['tag_name'] == 'v0.4.0'
assert packet['blockers'] and packet['unknowns']
assert all(packet['briefs'].get(k) for k in ['workflow', 'comparison', 'interactionPass'])
assert (ROOT / 'research.md').is_file()
checks.append('PASS: version scope, distinct briefs, interaction handoff, unknowns and blocking diagnostic present.')
result = dict(checkedAtUtc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
              status='passed-structural-checks-research-still-blocked', checks=checks,
              limitations=['Competitor screenshot pixels/rights not approved.', 'No native runtime or binary testing.',
                           'No site content changed: site checks/build/tests not run or claimed.',
                           'Initial collector excerpt assertion failed for curly apostrophe; exact-source correction passed on rerun.'])
(ROOT / 'validation.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
