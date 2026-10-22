"""Offline structural and provenance checks; not editorial/runtime certification."""
import datetime
import hashlib
import json
from pathlib import Path
import struct
import subprocess

ROOT = Path(__file__).resolve().parent
APP = ROOT.parents[3]
packet = json.loads((ROOT / 'research.json').read_text())
checks = []


def check(name, ok, detail):
    checks.append({'check': name, 'outcome': 'pass' if ok else 'fail', 'detail': detail})


sources = {s['id']: s for s in packet['sources']}
for source in sources.values():
    path = APP / source['path']
    check('source-hash:' + source['id'], path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == source['sha256'], source['path'])
for claim in packet['claims']:
    text = (APP / sources[claim['sourceIds'][0]]['path']).read_text()
    if claim['sourceIds'][0] == 'baseline-home':
        text = json.loads(text)['text']
    # GitHub may serialize JSON with or without whitespace.
    if claim['sourceIds'][0] == 'release':
        text = json.dumps(json.loads(text), separators=(',', ':'))
    check('claim-excerpt:' + claim['id'], claim['excerpt'] in text, claim['sourceUrls'][0])
ids = {c['id'] for c in packet['claims']}
check('matrix-claim-links', all(c in ids for row in packet['matrix'].values() for c in row), 'Every verified matrix cell maps to a retained claim.')
for visual in packet['visuals']:
    path = APP / visual['originalPath']
    check('visual-hash:' + visual['id'], hashlib.sha256(path.read_bytes()).hexdigest() == visual['originalSha256'], visual['originalPath'])
    check('visual-provenance:' + visual['id'], bool(visual['caption'] and visual['alt'] and visual['reuse']['basis']) and visual['publishedPath'] is None, 'Caption, alt, reuse basis; unpublished original.')
br = packet['visuals'][1]
png = (APP / br['originalPath']).read_bytes()
check('br-png-dimensions', struct.unpack('>II', png[16:24]) == (br['widthPx'], br['heightPx']), 'PNG header: 2940 x 3468.')
image = packet['visuals'][0]
result = subprocess.run(['sips', '-g', 'pixelWidth', '-g', 'pixelHeight', str(APP / image['originalPath'])], capture_output=True, text=True)
check('competitor-image-dimensions', result.returncode == 0 and 'pixelWidth: 2000' in result.stdout and 'pixelHeight: 1400' in result.stdout, result.stdout.strip())
check('identity-and-gates', packet['identity']['canonicalOwnerId'] == 'removemacai' and packet['identity']['classification'] == 'adjacent' and not packet['draftGate']['publicationApproved'], 'Canonical, adjacent and not approved for publication.')
check('required-documents', (ROOT / 'research.md').is_file() and bool(packet['briefs']['workflow']) and bool(packet['briefs']['comparison']), 'Both research formats and distinct briefs present.')
log = {'jobId': 'research-removemacai', 'checkedAtUtc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
       'checks': checks, 'passed': sum(x['outcome'] == 'pass' for x in checks),
       'failed': sum(x['outcome'] == 'fail' for x in checks),
       'visualInspection': 'Worker opened/read the actual official WebP and first-party PNG with image-capable read tool; separate independent publication review pending.',
       'siteBuild': 'Not run: no marketing files changed.', 'productRuntime': 'Not run: no product code executed.',
       'assemblyHistory': 'Initial build-packet.py attempt failed KeyError products; corrected to existing records key and rerun successfully (23 claims/10 sources).'}
(ROOT / 'validation.json').write_text(json.dumps(log, indent=2) + '\n')
print(json.dumps(log, indent=2))
raise SystemExit(bool(log['failed']))
