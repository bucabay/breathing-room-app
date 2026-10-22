"""Local research checks only; does not fetch pages or exercise either product."""
import datetime
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
APP = ROOT.parents[3]


def normalized(value):
    return re.sub(r'[^a-z0-9]+', ' ', value.lower()).strip()


def main():
    packet = json.loads((ROOT / 'research.json').read_text())
    index = json.loads((ROOT / 'sources/index.json').read_text())
    checks = []

    def check(name, condition):
        checks.append({'check': name, 'passed': bool(condition)})

    source_ids = {s['id'] for s in packet['sourceLedger']}
    text = {s['id']: s['text'] for s in index}
    for source in packet['sourceLedger']:
        path = source['snapshotPath']
        p = APP / path if path.startswith('docs/') else ROOT / path
        check('source hash: ' + source['id'], hashlib.sha256(p.read_bytes()).hexdigest() == source['sha256'])
        if source['id'] == 'home':
            text['home'] = json.loads(p.read_text())['text']
    discovery = packet['discovery']
    check('baseline discovery hash', hashlib.sha256((APP / discovery['snapshotPath']).read_bytes()).hexdigest() == discovery['sha256'])
    check('claim IDs unique', len({c['id'] for c in packet['claimLedger']}) == len(packet['claimLedger']))
    for claim in packet['claimLedger']:
        check('claim sources resolve: ' + claim['id'], set(claim['sourceIds']) <= source_ids)
        check('claim date/scope/URL: ' + claim['id'], claim['checkedOn'] == '2026-10-21' and bool(claim['conditions']) and claim['sourceUrl'].startswith('https://amplecapacity.com/'))
        # Excerpts may combine adjacent passages. Check each sentence/semicolon
        # segment in order-independent normalized source text, not generated prose.
        combined = normalized(' '.join(text[s] for s in claim['sourceIds']))
        pieces = [normalized(p) for p in re.split(r'(?<=[.!?])\s+|;\s+', claim['excerpt']) if p.strip()]
        check('supporting excerpt present: ' + claim['id'], all(p in combined for p in pieces))
    claims = {c['id'] for c in packet['claimLedger']}
    for key, cell in packet['productMatrix'].items():
        check('matrix claims resolve: ' + key, set(cell['claimIds']) <= claims)
    preview = packet['visuals'][1]
    check('selected preview original hash', hashlib.sha256((APP / preview['originalPath']).read_bytes()).hexdigest() == preview['originalSha256'])
    check('selected preview example/native labels', preview['dataMode'] == 'example' and 'Example data only' in preview['caption'] and 'not a native scan' in preview['caption'])
    competitor = packet['visuals'][0]
    check('uncleared competitor asset link-only, not downloaded', competitor['reuse']['status'] == 'link-only' and competitor['originalPath'] is None and competitor['originalSha256'] is None)
    check('blocked gates preserved', packet['status'] == 'blocked' and not packet['draftingAllowed'] and len(packet['blockers']) >= 1 and packet['published'] is False)
    check('canonical identity retained', packet['identity']['canonicalOwnerId'] == 'amplecapacity')
    result = {
        'jobId': 'research-amplecapacity',
        'checkedAtUtc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'checks': checks,
        'passed': sum(c['passed'] for c in checks),
        'failed': sum(not c['passed'] for c in checks),
        'limitations': ['Structural and retained-source checks, not independent editorial review or native product tests', 'No site changes, so no site build/test run', 'Competitor image not fetched: unclear reuse rights'],
    }
    (ROOT / 'validation.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
    return 1 if result['failed'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
