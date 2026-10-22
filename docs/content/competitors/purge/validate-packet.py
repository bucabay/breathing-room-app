"""Read-only documentary/artifact checks; not app tests or publication approval."""
import hashlib
import json
import pathlib
import struct

ROOT = pathlib.Path(__file__).resolve().parent
APP = ROOT.parents[3]
packet = json.loads((ROOT / 'research.json').read_text())
sources = {s['id']: s for s in packet['sources']}
checks = []


def check(ok, text):
    assert ok, text
    checks.append(text)


for source in sources.values():
    p = APP / source['snapshotPath']
    check(hashlib.sha256(p.read_bytes()).hexdigest() == source['sha256'], 'Source hash matched: ' + source['id'])
for claim in packet['claims']:
    check(all(x in sources for x in claim['sourceIds']), 'Source references resolve: ' + claim['id'])
    source = sources[claim['sourceIds'][0]]
    raw = (APP / source['snapshotPath']).read_text()
    text = json.dumps(json.loads(raw), ensure_ascii=False) if source['snapshotPath'].endswith('.json') else raw
    # Markdown emphasis and list formatting are not substantive differences in quotations.
    normalize = lambda s: ' '.join(s.replace('*', '').split())
    check(normalize(claim['excerpt']) in normalize(text), 'Retained supporting excerpt found: ' + claim['id'])
    check(bool(claim['checkedOn'] and claim['scope'] and claim['sourceUrl']), 'Claim dates/scope/URL present: ' + claim['id'])
for visual in packet['screenshots']:
    p = pathlib.Path(visual['originalPath'])
    if not p.is_absolute():
        p = APP / p
    b = p.read_bytes()
    check(hashlib.sha256(b).hexdigest() == visual['originalSha256'], 'Original visual hash matched: ' + visual['id'])
    check(b[:8] == b'\x89PNG\r\n\x1a\n' and struct.unpack('>II', b[16:24]) == (visual['widthPx'], visual['heightPx']), 'PNG dimensions verified: ' + visual['id'])
    check(bool(visual['caption'] and visual['alt'] and visual['reuse']['basis']), 'Visual caption/alt/reuse basis present: ' + visual['id'])
check(packet['identity']['canonicalOwnerId'] == 'purge', 'Canonical owner is purge; descriptive alias not separately drafted')
check(not packet['gates']['criticalBlockers'], 'No critical research blockers for bounded briefs; publication approval remains pending')
check((ROOT / 'research.md').is_file(), 'Readable research and distinct workflow/comparison handoff exist')
check('Permission is hereby granted' in (ROOT / 'sources/license-v1.12.0.txt').read_text(), 'Full MIT notice retained for documentation asset reuse')
print(json.dumps({'status': 'passed', 'checkCount': len(checks), 'checks': checks,
                  'notPerformed': ['native/runtime testing', 'cleanup', 'installation', 'website check/build/test', 'publication review']}, indent=2))
