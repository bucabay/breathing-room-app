"""Validate only this job's artifacts and emit its blocked handoff receipt."""
import datetime
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP = ROOT.parents[3]
P = json.loads((ROOT / 'research.json').read_text())
checks = []
def check(name, condition):
    if not condition:
        raise AssertionError(name)
    checks.append({'check': name, 'result': 'passed'})
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

sources = {s['id']: s for s in P['sources']}
claims = {c['id']: c for c in P['claims']}
check('Unique source and claim IDs: 15 sources, 28 claims', len(sources) == 15 and len(claims) == 28)
for s in sources.values():
    check('Source snapshot SHA-256: ' + s['id'], sha(APP / s['snapshotPath']) == s['sha256'])
    if s.get('rawSnapshotPath'):
        check('Original public HTML SHA-256: ' + s['id'], sha(APP / s['rawSnapshotPath']) == s['rawSha256'])
for c in claims.values():
    check('Source-backed excerpt and check date: ' + c['id'],
          bool(c['checkedAtUtc']) and all(i in sources for i in c['sourceIds']) and
          ' '.join(c['supportingExcerpt'].split()) in ' '.join(sources[c['sourceIds'][0]]['text'].split()))
for r in P['productMatrix']:
    check('Matrix claim IDs resolve: ' + r['dimension'], bool(r['claimIds']) and all(i in claims for i in r['claimIds']))
check('Canonical owner and relevant-product decision', P['identity']['canonicalOwnerId'] == 'cleanmymac' and not P['identity']['skipDecision']['skipProduct'])
check('Historical alias skip and PowerMyMac distinct identity',
      P['identity']['aliases'][0]['skipSeparateDraft'] and P['identity']['suspectedAliases'][0]['canonicalOwnerId'] != 'cleanmymac')
check('Both distinct briefs present and drafting blocked', all(not b['draftingAllowed'] for b in P['briefs'].values()) and len(P['briefs']) == 2)
br = next(v for v in P['visuals'] if v['productId'] == 'breathing-room')
check('Selected first-party PNG SHA-256 matches inventory', sha(Path(br['originalPath'])) == br['originalSha256'])
check('Preview caption explicitly discloses example data and no native results', 'Example data only' in br['caption'] and 'not a native scan' in br['caption'])
competitor = next(v for v in P['visuals'] if v['productId'] == 'cleanmymac')
check('Official competitor app asset URL appears in retained support HTML', competitor['assetUrl'] in (ROOT / 'sources/smart-care.html').read_text())
check('Uncleared competitor image is link-only, no invented capture/hash', competitor['reuse']['status'] == 'link-only' and competitor['originalPath'] is None and competitor['originalSha256'] is None and competitor['capturedAtUtc'] is None)
check('Store browser snapshot confirms human-verification gate', 'double check that you are human' in (ROOT / 'sources/store-browser.txt').read_text())
kit = json.loads((ROOT / 'sources/media-kit-manifest.json').read_text())
check('Official media-kit access failure retained accurately', kit['error'] == 'HTTP Error 403: Forbidden')
check('Critical pricing and image blockers remain explicit', P['status'] == 'blocked' and not P['draftingGate']['allowed'] and {b['id'] for b in P['blockers']} == {'exact-pricing', 'competitor-visual'})
check('Human-readable packet and source collector present', all((ROOT / x).is_file() for x in ['research.md','collect_sources.py','build_packet.py']))

files = sorted(p for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name != 'validation.json')
result = dict(jobId=P['jobId'], checkedAtUtc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
              result='passed-structural-and-evidence-checks; drafting-remains-blocked', checkCount=len(checks), checks=checks,
              artifactHashes={str(p.relative_to(APP)): sha(p) for p in files},
              notPerformed=['Native app/runtime testing', 'cleanup', 'site build/tests (no site edits)', 'independent rendered-page publication review'],
              browser='Existing listener used, owned tab33 only; stopped at public store challenge and closed owned tab. No profile recovery needed.')
(ROOT / 'validation.json').write_text(json.dumps(result, indent=2) + '\n')
artifacts = [str(p.relative_to(APP)) for p in files] + [str((ROOT / 'validation.json').relative_to(APP))]
receipt = dict(jobId='research-cleanmymac', status='blocked', artifacts=artifacts,
               validation=[f'{len(checks)} structural/evidence checks passed; see docs/content/competitors/cleanmymac/validation.json.',
                           '28 source-linked claim excerpts validated; reused verification and original HTML hashes checked.',
                           'Current-source Space PNG opened, example-data disclosures inspected, SHA-256 matched.',
                           'Official store GET 403; owned Chrome tab confirmed human-verification gate; stopped and closed tab.',
                           'Official press-kit GET 403; competitor screenshot retained link-only, no image download or invented rights.',
                           'No website edits, builds, native testing, cleanup, accounts, purchases, messages or queue changes.'],
               diagnostic='Research packet retained for relevant direct competitor CleanMyMac. CleanMyMac X grouped as prior major; PowerMyMac resolved as distinct iMyMac product. Drafting blocked: exact payable price/currency/billing/device/tax/renewal conditions unavailable behind store verification, and required competitor screenshot lacks cleared reuse/access (press kit 403). Official app screenshot URL and labelled Breathing Room preview recorded. No publication approval.')
receipt_path = APP / 'docs/content/.runtime/research-cleanmymac.1792610163411500000.receipt.json'
receipt_path.write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(dict(checksPassed=len(checks), status=receipt['status'], receipt=str(receipt_path), artifacts=len(artifacts)), indent=2))
