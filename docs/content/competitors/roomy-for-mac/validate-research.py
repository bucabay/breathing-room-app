"""Read-only validation, writing results only inside this job's folder."""
import datetime
import hashlib
import json
from pathlib import Path
import struct

ROOT = Path('/Users/gabe/code/breathing-room-app')
OUT = Path(__file__).parent
p = json.loads((OUT/'research.json').read_text())
checks = []
def check(name, result):
    assert result, name
    checks.append({'check':name,'result':'passed'})
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
check('Canonical identity and explicit non-alias skip decision', p['identity']['canonicalOwnerId']=='roomy-for-mac' and p['identity']['skipDecision'] is False)
source_ids = {s['id'] for s in p['sources']}
claim_ids = {c['id'] for c in p['claims']}
check('All 22 claims have source URLs, excerpts, check dates and supported source IDs', len(claim_ids)==22 and all(c['sourceUrl'] and c['excerpt'] and c['checkedAtUtc'] and set(c['sourceIds'])<=source_ids for c in p['claims']))
check('Every verified matrix cell maps to existing claim IDs; unknowns remain not verified', all((row['claimIds'] and set(row['claimIds'])<=claim_ids) if row['state']=='verified' else row['value']=='not verified' for row in p['matrix']))
for s in p['sources']:
    if s.get('rawCapture') and s.get('verifiedHash'):
        check('Retained source hash: '+s['id'], sha(ROOT/s['rawCapture']) == s['verifiedHash'])
home = json.loads((ROOT/'docs/content/.runtime/verification-2/roomy-for-mac-official.json').read_text())
for c in p['claims']:
    if c['sourceIds']==['homepage']:
        check('Homepage excerpt matches retained current baseline (whitespace-normalized): '+c['id'], ' '.join(c['excerpt'].split()) in ' '.join(home['text'].split()))
for a in p['visuals']:
    path = Path(a.get('sourcePath') or ROOT/a['originalPath'])
    data = path.read_bytes()
    check('Original image SHA-256: '+a['id'], hashlib.sha256(data).hexdigest()==(a.get('sha256') or a['originalSha256']))
    check('Actual PNG signature: '+a['id'], data[:8]==b'\x89PNG\r\n\x1a\n')
    dims = struct.unpack('>II',data[16:24])
    check('PNG dimensions: '+a['id'], dims==(a.get('width') or a['widthPx'],a.get('height') or a['heightPx']))
    check('Alt text, caption and no invented publication asset: '+a['id'], bool(a['alt'] and a['caption']) and a['publishedPath'] is None)
    if a.get('productId')=='roomy-for-mac':
        check('Explicit official editorial reuse permission: '+a['id'], a['reuse']['status']=='cleared' and a['reuse']['evidenceUrlOrPath']=='https://roomymac.com/press')
    else:
        check('Breathing Room example/native disclosure retained', 'Example data only' in a['caption'] and 'not a native scan' in a['caption'])
check('Distinct workflow/comparison primary intents', p['briefs']['workflow']['primaryIntent'] != p['briefs']['comparison']['primaryIntent'])
check('Unknowns retained and publication not approved', len(p['unknowns'])>=8 and not p['draftGate']['publicationApproved'])
check('No unresolved critical research blockers', not p['criticalBlockers'])
result = {'jobId':'research-roomy-for-mac','checkedAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'status':'passed','checks':checks,
    'manualChecks':['Opened and read both actual Roomy press PNGs and selected Breathing Room Space PNG.',
      'Read official press/security/changelog/install/EULA pages; retained excerpts and explicit editorial reuse terms.',
      'No app/site build, native runtime test, independent editorial approval or responsive rendering claimed.'],
    'artifactHashes':{str(path.relative_to(ROOT)):sha(path) for path in [OUT/'research.json', OUT/'research.md']}}
(OUT/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'passed','checks':len(checks),'artifactHashes':result['artifactHashes']},indent=2))
