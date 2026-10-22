"""Offline structural, provenance and exact-excerpt checks; no product execution."""
import datetime
import hashlib
import json
from pathlib import Path
import struct
import zipfile

ROOT = Path(__file__).resolve().parent
APP = ROOT.parents[3]
packet = json.loads((ROOT / 'research.json').read_text())
checks = []

def check(condition, message):
    assert condition, message
    checks.append(message)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

sources = {s['id']: s for s in packet['sources']}
ids = {c['id'] for c in packet['claims']}
check(len(ids) == len(packet['claims']), 'Claim IDs unique')
for s in sources.values():
    p = APP / s['snapshotPath']
    check(p.is_file() and sha(p) == s['sha256'], 'Source snapshot hash matches: ' + s['id'])
    if 'textPath' in s:
        check(sha(APP / s['textPath']) == s['textSha256'], 'Source text hash matches: ' + s['id'])
for c in packet['claims']:
    check(bool(c['checkedDate']) and c['state'] in ('verified','not-verified'), 'Claim date/state present: ' + c['id'])
    if c['state'] == 'not-verified':
        check(c['sourceIds'] == [] and c['excerpt'] is None, 'Unknown remains explicitly unknown: ' + c['id'])
        continue
    for sid in c['sourceIds']:
        s=sources[sid]
        p=APP / s.get('textPath',s['snapshotPath'])
        text=p.read_text()
        if sid=='baseline-official':
            text=json.loads(text)['text']
        check(c['excerpt'] in text, 'Exact claim excerpt found: ' + c['id'])
for row in packet['matrix']:
    check(all(cid in ids for cid in row['senseiClaimIds']+row['breathingRoomClaimIds']), 'Matrix claim references resolve: ' + row['dimension'])
kit=sources['press-kit']
with zipfile.ZipFile(APP / kit['snapshotPath']) as archive:
    for item in kit['selectedAssets']:
        check(hashlib.sha256(archive.read(item['member'])).hexdigest() == item['sha256'], 'Archive member original hash: ' + item['path'])
for v in packet['visuals']:
    p=APP / v['originalPath']
    check(p.is_file() and sha(p)==v['originalSha256'], 'Visual original hash matches: ' + v['id'])
    check(struct.unpack('>II',p.read_bytes()[16:24])==(v['widthPx'],v['heightPx']), 'PNG dimensions match: ' + v['id'])
    check(bool(v['caption']) and bool(v['alt']) and bool(v['reuse']['basis']), 'Caption, alt and reuse basis present: ' + v['id'])
    check(v['publishedPath'] is None and v['publishedSha256'] is None, 'No invented published derivative: ' + v['id'])
check(packet['identity']['canonicalOwnerId']=='disk-sensei' and packet['identity']['aliasDecision']['skipSeparateAliasDraft'], 'Canonical owner and alias-skip decision explicit')
check(not packet['publicationApproved'] and not packet['ownership']['websiteEdits'] and not packet['ownership']['queueEdits'], 'Research-only and publication boundaries retained')
check(all((ROOT / n).is_file() for n in ['research.json','research.md']), 'Both required research artifacts exist')
result=dict(status='passed',checkedAtUtc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    command='python3 docs/content/competitors/disk-sensei/validate.py',checksPassed=len(checks),checks=checks,
    limitations=['Documentary/structural validation, not app tests, installation, benchmark, legal opinion or publication approval.',
                'Actual PNGs and press PDFs separately opened/read during research.',
                'No site changes; website check/build/test and browser rendering not performed.'])
(ROOT/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS:',len(checks),'offline provenance/structure checks')
