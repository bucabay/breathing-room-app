"""Read-only packet checks; writes only this job's validation result."""
import hashlib
import json
import struct
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
FOLDER = Path(__file__).resolve().parent
packet = json.loads((FOLDER / 'research.json').read_text())
checks = []


def check(label, condition):
    checks.append({'check': label, 'passed': bool(condition)})


def normalized(text):
    return ' '.join(text.split())


sources = {s['id']: s for s in packet['sources']}
for source in sources.values():
    path = ROOT / source['path']
    check('source hash: ' + source['id'],
          hashlib.sha256(path.read_bytes()).hexdigest() == source['sha256'])

claim_ids = {c['id'] for c in packet['claims']}
check('unique claim IDs', len(claim_ids) == len(packet['claims']))
for claim in packet['claims']:
    check('claim evidence references: ' + claim['id'],
          bool(claim['sourceIds']) and all(s in sources for s in claim['sourceIds'])
          and bool(claim['excerpt']) and bool(claim['checkedDate'])
          and bool(claim['conditions']) and bool(claim['reviewer']))
for row in packet['matrix']:
    check('matrix references: ' + row['dimension'],
          all(c in claim_ids for c in row['competitorClaimIds'] + row['breathingRoomClaimIds']))

mac = normalized((FOLDER / 'sources/mac-store.txt').read_text())
for excerpt in ['Mac Requires macOS 10.15 or later.', 'Version 7.7 12/12/2024',
                'Clean Doctor Pro - 1 Year $24.99',
                'Clean Doctor Pro - 1 Week $3.99',
                'Clean Doctor Pro - 1 Month $7.99',
                'Junk Files Cleaner: Delete system junk, broken data, and caches.',
                'Uninstall apps: Find and delete unwanted apps completely.',
                'Data Used to Track You']:
    check('retained Mac passage: ' + excerpt, excerpt in mac)
terms = normalized((FOLDER / 'sources/terms.txt').read_text())
for excerpt in ['Last updated: June 2020', 'Current subscription price starts at $7.99/week.',
                'unless expressly permitted', 'All rights not expressly granted herein are reserved.']:
    check('retained terms passage: ' + excerpt, excerpt in terms)
home = (FOLDER / 'sources/developer-home.html').read_text()
check('developer same-ID product card', 'data-app-id="855008026"' in home and 'AI Cleaner Max' in home)
visual = packet['visuals'][0]
mac_html = (FOLDER / 'sources/mac-store.html').read_text()
locations = json.loads((FOLDER / 'sources/mac-screenshot-locations.json').read_text())
check('actual screenshot URL retained in Mac HTML', visual['assetUrl'] in mac_html
      and visual['assetUrl'] in locations['urls'] and 'product_media_mac_' in mac_html)
check('no competitor image download or invented image hash',
      visual['originalPath'] is None and visual['originalSha256'] is None
      and visual['reuse']['status'] == 'link-only')
preview = packet['visuals'][1]
data = (ROOT / preview['originalPath']).read_bytes()
check('selected preview original hash', hashlib.sha256(data).hexdigest() == preview['originalSha256'])
check('selected PNG signature and dimensions', data[:8] == b'\x89PNG\r\n\x1a\n'
      and struct.unpack('>II', data[16:24]) == (preview['widthPx'], preview['heightPx']))
check('explicit example-data caption', 'Example data only' in preview['caption']
      and 'not a native scan' in preview['caption'] and preview['dataMode'] == 'example')
check('alias owner and skip decision', packet['canonicalOwnerId'] == 'clean-doctor'
      and packet['identity']['aliasSkipDecision']['skipSeparateAliasDrafts']
      and not packet['identity']['aliasSkipDecision']['skipThisOwner'])
check('critical evidence blocks drafting', packet['status'] == 'blocked'
      and not packet['gates']['draftingAllowed'] and not packet['gates']['publicationAllowed']
      and len(packet['gates']['blockers']) == 2)
readme = (ROOT / 'README.md').read_text()
config = json.loads((ROOT / 'src-tauri/tauri.conf.json').read_text())
billing = json.loads((ROOT / 'src/billing-config.json').read_text())
check('Breathing Room version and minimum OS cross-check',
      config['version'] == '0.1.0-preview.1' and config['bundle']['macOS']['minimumSystemVersion'] == '13.0')
check('Breathing Room current documented runtime and price limits',
      '**Python 3.10+**' in readme and 'preview is not notarized' in readme
      and billing['monthlyAmount'] == 500 and billing['annualAmount'] == 5000
      and billing['currency'] == 'usd')
local_evidence = [{
    'path': p,
    'sha256': hashlib.sha256((ROOT / p).read_bytes()).hexdigest()
} for p in ['README.md', 'src-tauri/tauri.conf.json', 'src/billing-config.json']]
result = {
    'jobId': packet['jobId'], 'checkedAtUtc': datetime.now(timezone.utc).isoformat(),
    'command': 'python3 docs/content/competitors/clean-doctor/validate.py',
    'passed': all(c['passed'] for c in checks),
    'passedChecks': sum(c['passed'] for c in checks), 'totalChecks': len(checks),
    'checks': checks, 'localEvidenceHashes': local_evidence,
    'limitations': ['Documentary checks, not product execution or visual-rights clearance.',
                    'No website edits; website check/build/test not run.']
}
(FOLDER / 'validation.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
raise SystemExit(0 if result['passed'] else 1)
