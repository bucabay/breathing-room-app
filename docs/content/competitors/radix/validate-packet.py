"""Validate retained Radix research and emit the authorized job receipt."""
import datetime
import hashlib
import json
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parent
APP = ROOT.parents[3]
receipt_path = APP / 'docs/content/.runtime/research-radix.1792620108966733000.receipt.json'
checks = []

def check(name, condition, detail):
    checks.append({'check': name, 'passed': bool(condition), 'detail': detail})

packet = json.loads((ROOT / 'research.json').read_text())
sources = {s['id']: s for s in packet['sources']}
claims = {c['id']: c for c in packet['claims']}
check('identity-and-scope', packet['identity']['canonicalOwnerId'] == 'radix' and packet['identity']['canonicalHomepage'] == 'https://tryradix.app/' and not packet['identity']['skipDecision']['skip'], 'Distinct relevant Mac product; no alias/old-domain duplicate draft; only research output.')
check('claim-ledger', len(claims) == len(packet['claims']) and all(c['sourceIds'] and c['supportingExcerpt'] and c['checkedAtUtc'] and c['scope'] and all(s in sources for s in c['sourceIds']) for c in claims.values()), f'{len(claims)} unique claim IDs with source references, excerpts, timestamps, states and scope.')
for source in sources.values():
    path = ROOT / source['snapshotPath'] if source.get('snapshotPath') else APP / source['path']
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    check('source-hash:' + source['id'], actual == source['sha256'], str(path.relative_to(APP)))
check('matrix-claim-resolution', all(all(c in claims for c in r['radixClaimIds'] + r['breathingRoomClaimIds']) for r in packet['productMatrix']), f"{len(packet['productMatrix'])} matrix rows resolve to retained claim IDs.")
for visual in packet['visuals']:
    path = APP / visual['originalPath']
    raw = path.read_bytes()
    dims = struct.unpack('>II', raw[16:24])
    check('visual-integrity:' + visual['id'], raw[:8] == b'\x89PNG\r\n\x1a\n' and hashlib.sha256(raw).hexdigest() == visual['originalSha256'] and dims == (visual['widthPx'], visual['heightPx']), f'PNG {dims[0]}x{dims[1]}, hash and dimensions match; image separately opened/read with image tool.')
    check('visual-provenance:' + visual['id'], bool(visual['sourcePageUrl'] and visual['alt'] and visual['caption'] and visual['reuse']['basis']) and visual['publishedPath'] is None and all(c in claims for c in visual['supportedClaimIds']), 'Source, caption, alt, reuse basis and claim mappings present; no published asset claimed.')
release = json.loads((ROOT / 'sources/latest-release.json').read_text())
check('release-conditions', release['tag_name'] == 'v1.8.0' and not release['draft'] and not release['prerelease'] and 'macOS 14.0+' in release['body'] and 'universal binary for Intel and Apple silicon systems' in release['body'], 'Official retained API supports exact version, release state and architecture/OS conditions; not binary execution.')
licence = (ROOT / 'sources/LICENSE.txt').read_text()
readme = (ROOT / 'sources/README.md').read_text()
check('image-licence-chain', 'Copyright (c) 2026 Colin Kim' in licence and 'associated documentation files' in licence and 'permission notice shall be included' in licence and 'docs/images/radix-scan-comparison.png' in readme and '[MIT License](LICENSE)' in readme, 'Official README embeds retained image; full MIT copyright/permission/disclaimer retained; distribution requirement recorded.')
br = next(v for v in packet['visuals'] if v['productId'] == 'breathing-room')
check('preview-labels', br['dataMode'] == 'example' and 'Example data only' in br['caption'] and 'not a native scan' in br['caption'] and '2026-10-21' in br['originalPath'], 'Selected October 21 current-source browser preview is explicitly example data, not native measurement.')
check('unknowns-not-negative-features', all(claims[c]['state'] == 'not-verified' for c in ['unknown-radix-monitoring','unknown-radix-dev','unknown-radix-signing']), 'Unknown monitoring/adapters/signing are retained as not verified, not No.')
markdown = (ROOT / 'research.md').read_text()
check('briefs-and-handoff', all(s in markdown for s in ['Distinct workflow article brief','Concise comparison brief','Breathing Room, which we build','Independent review','No site build or native test']), 'Separate workflow/comparison intents, affiliation, independent-review and unperformed-check boundaries present.')
check('research-readiness', not packet['gates']['criticalResearchBlockers'] and packet['gates']['publicationStatus'] == 'not-approved', 'Complete research packet does not claim draft or publication approval.')
outcome = 'passed' if all(c['passed'] for c in checks) else 'failed'
validation = {'jobId':'research-radix','checkedAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'outcome':outcome,'checks':checks,'limitations':['Structural/provenance checks plus documentary and image inspection, not product runtime tests.','No website content changed; site builds and browser rendering QA not run.','Independent draft/publication review pending.']}
(ROOT / 'validation.json').write_text(json.dumps(validation, indent=2) + '\n')
artifacts = [str(p.relative_to(APP)) for p in sorted(ROOT.rglob('*')) if p.is_file()]
receipt = {'jobId':'research-radix','status':'done' if outcome == 'passed' else 'blocked','artifacts':artifacts,'validation':[f"{sum(c['passed'] for c in checks)}/{len(checks)} packet checks passed; see docs/content/competitors/radix/validation.json.", 'Both actual product images opened/read; retained original image and source SHA-256 checked.', 'No site build, native/runtime testing or independent publication review claimed.'],'diagnostic':'Research packet complete: reused batch-2 identity/platform/free-offer records; official repository confirms MIT licence, snapshot workflow, v1.8.0 universal macOS 14+ release and licensed UI asset. Radix remains its own canonical owner. Unknown capabilities/signing remain not verified. Drafting is bounded to retained evidence; publication and independent review remain pending.' if outcome == 'passed' else 'Packet validation failed: ' + ', '.join(c['check'] for c in checks if not c['passed'])}
receipt_path.write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps({'outcome':outcome,'passed':sum(c['passed'] for c in checks),'total':len(checks),'receipt':str(receipt_path),'failed':[c for c in checks if not c['passed']]}, indent=2))
raise SystemExit(0 if outcome == 'passed' else 1)
