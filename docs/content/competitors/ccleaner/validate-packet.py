"""Validate retained evidence, then write this job's blocked receipt."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

root = Path(__file__).resolve().parents[4]
out = Path(__file__).resolve().parent
p = json.loads((out/'research.json').read_text())
checks = []
def check(condition, message):
    assert condition, message
    checks.append(message + ': PASS')
check(p['jobId']=='research-ccleaner' and p['status']=='blocked' and not p['draftingAllowed'], 'Correct job and explicit blocked drafting gate')
ids = {s['id'] for s in p['sources']}
for s in p['sources']:
    path = root/s['snapshotPath']
    check(hashlib.sha256(path.read_bytes()).hexdigest()==s['sha256'], 'Source snapshot hash '+s['id'])
for c in p['claims']:
    check(set(c['sourceIds'])<=ids and bool(c['sourceUrls']) and bool(c['excerpt']) and c['checkedOn']=='2026-10-21', 'Claim source/date/excerpt coverage '+c['id'])
    if c['sourceIds'][0] in ['mac','download','terms']:
        s = next(s for s in p['sources'] if s['id']==c['sourceIds'][0])
        text = json.loads((root/s['snapshotPath']).read_text())['text']
        check(c['excerpt'] in text, 'Exact retained official excerpt '+c['id'])
v = p['visuals'][1]
check(hashlib.sha256(Path(v['originalPath']).read_bytes()).hexdigest()==v['originalSha256'], 'Selected Breathing Room preview original hash')
check('Example data only' in v['caption'] and 'not a native' in v['caption'], 'Example-data and non-native labels retained')
check(p['visuals'][0]['originalPath'] is None and p['visuals'][0]['originalSha256'] is None and p['visuals'][0]['reuse']['status']=='denied', 'Restricted competitor image not downloaded or falsely cleared')
check(len(p['blockers'])==3 and bool(p['briefs']['workflow']) and bool(p['briefs']['comparison']), 'Precise blockers and both distinct briefs present')
check(p['identity']['canonicalOwnerId']=='ccleaner' and not p['identity']['aliasSkipDecision']['skip'], 'Canonical identity and explicit alias skip decision')
check((out/'research.md').stat().st_size>1000, 'Human-readable research handoff exists')
report = dict(checkedAtUtc=datetime.now(timezone.utc).isoformat(),status='passed-structural-checks-with-drafting-blockers',checks=checks,notRun=['No competitor app execution or cleanup','No marketing build/check/tests: no site edits','No screenshot pixel approval or independent editorial review'])
(out/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
artifacts = [str(x.relative_to(root)) for x in sorted(out.rglob('*')) if x.is_file()]
receipt = dict(jobId='research-ccleaner',status='blocked',artifacts=artifacts,validation=[f'python3 docs/content/competitors/ccleaner/build-packet.py: passed; exact source excerpts asserted',f'python3 docs/content/competitors/ccleaner/validate-packet.py: {len(checks)} structural/hash/excerpt checks passed','Read-only owned Chrome tab 75: Mac product/download/terms DOM retained; tab closed','No website edits, app execution, image download or publication approval'],diagnostic='Research packet retained using batch-1 baseline plus official Mac sources. Drafting blocked: official image-copy/direct-link restrictions without permission; conflicting macOS requirements (10.10+ download versus 10.12–13 product list); USD 24.95/44.95 display lacks complete billing/renewal/tax/promotion conditions. Current example-data Breathing Room Activity preview selected and hash verified.')
receipt_path = root/'docs/content/.runtime/research-ccleaner.1792613428630254000.receipt.json'
receipt_path.write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'checksPassed':len(checks),'receipt':str(receipt_path),'status':receipt['status']},indent=2))
