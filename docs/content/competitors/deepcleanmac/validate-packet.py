"""Validate retained evidence and blocked-state honesty without network or native actions."""
import datetime
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
p = json.loads((OUT / 'research.json').read_text())
checks = []


def check(name, condition):
    assert condition, name
    checks.append({'check': name, 'outcome': 'pass'})


check('Research is blocked, not draft/publication ready',
      p['status'] == 'blocked' and not p['draftingGate']['ready'] and not p['draftingGate']['publicationReady'])
check('Correct owner and no alias merge invented',
      p['productId'] == p['canonicalOwnerId'] == 'deepcleanmac' and not p['identity']['aliases'])
check('Research markdown and JSON present', (OUT / 'research.md').stat().st_size > 1000)
sources = {s['id']: s for s in p['sources']}
for s in sources.values():
    path = ROOT / s['snapshotPath']
    check('Snapshot exists and SHA-256 matches: ' + s['id'],
          path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == s['sha256'])
claims = {c['id']: c for c in p['claims']}
check('Claim IDs unique', len(claims) == len(p['claims']))
for c in claims.values():
    check('Claim has exact excerpt, source URL and check date: ' + c['id'],
          bool(c['excerpt']) and c['sourceUrl'].startswith('https://')
          and bool(c.get('checkedAtUtc') or c.get('checkedOn'))
          and all(s in sources for s in c['sourceIds']))
    s = sources[c['sourceIds'][0]]
    path = ROOT / s['snapshotPath']
    text = path.read_text() if path.suffix == '.md' else json.loads(path.read_text())['text']
    check('Supporting excerpt exists in retained source: ' + c['id'], c['excerpt'] in text)
for row in p['productMatrix']:
    check('Matrix references known claims: ' + row['dimension'],
          all(id in claims for id in row['competitorClaimIds'] + row['breathingRoomClaimIds']))
check('Both necessary visuals recorded', len(p['visuals']) == 2)
competitor, br = p['visuals']
check('Competitor URL retained; unclear rights not waived or copied',
      competitor['reuse']['status'] == 'link-only' and competitor['assetUrl'].startswith('https://img.alternativeto.net/')
      and competitor['originalPath'] is None and competitor['originalSha256'] is None
      and competitor['publishedPath'] is None)
check('Current first-party example preview hash and labels intact',
      br['id'] == 'current-space-browser-preview' and br['dataMode'] == 'example'
      and 'Example data only' in br['caption']
      and hashlib.sha256(Path(br['originalPath']).read_bytes()).hexdigest() == br['originalSha256'])
check('Both critical diagnostics present',
      {b['id'] for b in p['blockers']} == {'competitor-image-rights', 'exact-price-discrepancy'})
check('Unknowns remain explicitly unverified', all(u['state'] == 'not-verified' for u in p['unknowns']))
check('Separate workflow and comparison briefs are not drafts',
      all(b['state'] == 'planning-only-blocked-not-a-draft' for b in p['briefs'].values())
      and p['briefs']['workflow']['slug'] != p['briefs']['comparison']['slug'])
check('Independent review not invented', p['draftingGate']['independentReview'] == 'pending' and p['draftingGate']['score'] is None)
result = {'jobId':'research-deepcleanmac','validatedAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'result':'pass-research-structure; drafting-blocked','checks':checks,
          'notPerformed':['Competitor installation/runtime/cleanup tests','Purchases/account/contact workflows',
                          'Website check/build/test (no website edits)','Independent editorial/rendered review'],
          'artifactHashes':{f.name:hashlib.sha256(f.read_bytes()).hexdigest()
                            for f in [OUT/'research.json',OUT/'research.md',OUT/'build-packet.py',OUT/'validate-packet.py']}}
(OUT / 'validation.json').write_text(json.dumps(result, indent=2) + '\n')
print(f'PASS: {len(checks)} checks; evidence packet retained, drafting remains blocked.')
