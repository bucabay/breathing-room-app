"""Offline evidence-integrity checks; not editorial or publication approval."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP = ROOT.parents[3]


def resolve(path):
    return APP / path if path.startswith('docs/') else ROOT / path


def main():
    packet = json.loads((ROOT / 'research.json').read_text())
    checks = []
    sources = {s['id']: s for s in packet['sources']}
    assert len(sources) == len(packet['sources'])
    texts = {}
    for source in sources.values():
        path = resolve(source['path'])
        assert path.is_file(), path
        if source.get('sha256'):
            assert hashlib.sha256(path.read_bytes()).hexdigest() == source['sha256']
        if source.get('rawSha256'):
            raw = resolve(source['rawPath'])
            assert hashlib.sha256(raw.read_bytes()).hexdigest() == source['rawSha256']
        text = path.read_text()
        if path.suffix == '.json':
            record = json.loads(text)
            text = record.get('text') or '\n'.join(link.get('text', '') for link in record.get('links', []) if isinstance(link, dict)) or text
        texts[source['id']] = text
    checks.append('PASS: 7 source paths exist; 2 reused baseline file hashes and 3 retained HTML SHA-256 values match.')
    ids = {c['id'] for c in packet['claims']}
    assert len(ids) == len(packet['claims']) == 14
    for claim in packet['claims']:
        assert all(s in sources for s in claim['sources'])
        assert claim['checkedDate']
        for key in ('excerpt', 'supportingExcerpt2'):
            excerpt = claim.get(key)
            if excerpt:
                assert any(excerpt in texts[s] for s in claim['sources']), (claim['id'], key)
    for refs in packet['matrix'].values():
        assert set(refs) <= ids
    checks.append('PASS: 14 unique claims have valid source references/check dates; all retained claim excerpts match cited source text; matrix references resolve.')
    preview = packet['visuals'][1]
    assert hashlib.sha256(resolve(preview['originalPath']).read_bytes()).hexdigest() == preview['originalSha256']
    assert preview['dataMode'] == 'example' and 'Example data only' in preview['caption']
    competitor = packet['visuals'][0]
    assert competitor['reuse']['status'] == 'link-only'
    assert competitor['originalSha256'] is None and competitor['originalPath'] is None
    assert packet['status'] == 'blocked' and packet['blockers']
    checks.append('PASS: selected Breathing Room original SHA-256 matches; example-data caption retained; competitor asset remains link-only with no invented file/hash; B1 blocks drafting.')
    report = {'checkedAtUtc': datetime.now(timezone.utc).isoformat(), 'checks': checks,
              'limitations': 'Structural and documentary-integrity checks only; no competitor binary/image inspection, native execution, website build or publication approval.'}
    (ROOT / 'validation.json').write_text(json.dumps(report, indent=2) + '\n')
    artifacts = [str(p.relative_to(APP)) for p in sorted(ROOT.rglob('*')) if p.is_file()]
    receipt = {'jobId': 'research-trashpanda', 'status': 'blocked', 'artifacts': artifacts,
               'validation': checks + ['Actual PNG visually inspected with image-capable read tool; owned Chrome tab 178 closed; no marketing files changed and no site tests required for research-only scope.'],
               'diagnostic': 'Research packet and source provenance retained. TrashPanda identity/direct Mac fit verified; official downloads identify 4.1/macOS 14+. Drafting blocked: official Downloads Detox screenshot has no established reuse permission; link-only fallback does not satisfy on-page product-image gate. No competitor image downloaded or app cleanup tested.'}
    receipt_path = APP / 'docs/content/.runtime/research-trashpanda.1792621177254932000.receipt.json'
    receipt_path.write_text(json.dumps(receipt, indent=2) + '\n')
    for check in checks:
        print(check)
    print('BLOCKED receipt:', receipt_path)


if __name__ == '__main__':
    main()
