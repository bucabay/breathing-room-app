"""Validate owned research structure and byte provenance, not publication quality."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

root = Path(__file__).resolve().parent
app = root.parents[3]
packet = json.loads((root / 'research.json').read_text())
checks = []

def check(name, condition):
    assert condition, name
    checks.append({'check': name, 'outcome': 'pass'})

check('Required research files exist and Markdown is nonempty', all((root / n).is_file() and (root / n).stat().st_size > 0 for n in ['research.json', 'research.md']))
check('Task, canonical owner and alias decision recorded', packet['jobId'] == 'research-cleanmylinux' and packet['canonicalOwnerId'] == 'cleanmylinux' and packet['aliasDecision']['skipSeparateDraft'] is False)
ids = {s['id'] for s in packet['sources']}
check('All 18 claims have source URLs, excerpts, dates, locators, state and valid source IDs', len(packet['claims']) == 18 and all(c['sourceUrl'].startswith('https://') and c['excerpt'] and c['checkedAtUtc'] and c['locator'] and c['state'] in ['verified', 'not-verified', 'contradicted', 'stale'] and set(c['sourceIds']) <= ids for c in packet['claims']))
hashed = 0
for s in packet['sources']:
    if 'sha256' in s:
        path = root / s['path']
        check('Source bytes match SHA-256: ' + s['id'], path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == s['sha256'])
        hashed += 1
check('11 retained sources have whole-file hashes', hashed == 11)
for v in packet['visuals']:
    path = Path(v.get('sourcePath', root / v.get('originalPath', '')))
    check('Visual bytes and PNG dimensions match: ' + v['id'], path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == v['originalSha256'] and path.read_bytes().startswith(b'\x89PNG\r\n\x1a\n') and int.from_bytes(path.read_bytes()[16:20], 'big') == v['widthPx'] and int.from_bytes(path.read_bytes()[20:24], 'big') == v['heightPx'])
    check('Visual caption, alt, rights and unpublished status: ' + v['id'], bool(v['caption'] and v['alt'] and v['reuse']['basis']) and v['publishedPath'] is None and v['publishedSha256'] is None)
check('MIT notice retained with original copyright and permission conditions', all(x in (root / 'sources/LICENSE').read_text() for x in ['Copyright (c) 2026 Better Linux', 'The above copyright notice and this permission notice shall be included']))
check('Mac preview caption retains example/native limitations', all(x in packet['visuals'][1]['caption'] for x in ['Example data only', 'not a native scan', 'cleanup result']))
check('Compatibility contradiction explicitly prevents exact minimum/install claims', any(c['id'] == 'compatibility-conflict' and c['state'] == 'not-verified' for c in packet['claims']) and bool(packet['decision']['blockedClaims']))
check('Distinct workflow/comparison intents and adjacent platform fit recorded', packet['classification'] == 'adjacent-platform-specific' and packet['briefs']['article']['slug'] != packet['briefs']['comparison']['slug'])
check('Release metadata distinguishes beta name from API prerelease flag', packet['release']['tag'] == 'v1.0.0-beta.2' and packet['release']['apiPrereleaseFlag'] is False)
check('No publication or native-test approval claimed', packet['decision']['publicationApproved'] is False and packet['validation']['handsOnTests'] is False and packet['validation']['siteChanged'] is False)
result = {'jobId': packet['jobId'], 'validatedAtUtc': datetime.now(timezone.utc).isoformat(),
          'command': 'python3 docs/content/competitors/cleanmylinux/validate-packet.py', 'status': 'pass',
          'checks': checks, 'manualChecks': ['Opened/read both actual product PNGs with image-capable read tool.',
                                           'Reused matching batch-2 official/directory captures; did not refetch baseline homepage.',
                                           'Read official pinned README, MIT licence and release metadata; flagged distro/GLIBC conflict.'],
          'limitations': ['Structural/hash checks are not independent factual, legal, native runtime or rendered-page approval.',
                         'No website changes: site check/build/test not run or required at this research-only stage.',
                         'Initial packet assembly failed with KeyError products; corrected manifest key to competitors and reran successfully.']}
(root / 'validation.json').write_text(json.dumps(result, indent=2) + '\n')
artifacts = [str(p.relative_to(app)) for p in sorted(root.rglob('*')) if p.is_file()]
receipt = {'jobId': 'research-cleanmylinux', 'status': 'done', 'artifacts': artifacts,
           'validation': [f'{len(checks)} structural/provenance checks passed; see docs/content/competitors/cleanmylinux/validation.json.',
                          '18 claims link dated source excerpts; 11 source hashes and both PNG hashes/dimensions match.',
                          'Both actual product images opened and visually inspected; original competitor bytes and MIT notice retained.',
                          'No site edits or native runtime tests; independent publication review pending.'],
           'diagnostic': 'Research packet complete for bounded Linux-to-Mac transition intent. Distinct Better Linux identity, v1.0.0-beta.2 public release metadata, MIT documentation visual and current-source example-data Breathing Room view retained. Commercial terms remain unverified; distro/GLIBC conflict blocks exact Linux installation recommendations, not the bounded comparison. No queue or site mutation.'}
receipt_path = app / 'docs/content/.runtime/research-cleanmylinux.1792622155237520000.receipt.json'
receipt_path.write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps({'status': result['status'], 'checksPassed': len(checks), 'receipt': str(receipt_path), 'artifactCount': len(artifacts)}, indent=2))
