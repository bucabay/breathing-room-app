"""Read-only public evidence collection; never runs product code or installers."""
import concurrent.futures
import datetime
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parent
APP = ROOT.parents[3]
RAW = 'https://raw.githubusercontent.com/omlahore/RemoveMacAI/'
SOURCES = {
    'release': ('https://api.github.com/repos/omlahore/RemoveMacAI/releases/latest', 'release.json'),
    'readme-release': (RAW + 'v1.1.4/README.md', 'README-v1.1.4.md'),
    'readme-main': (RAW + 'main/README.md', 'README-main.md'),
    'license': (RAW + 'v1.1.4/LICENSE', 'LICENSE.txt'),
    'third-party': (RAW + 'v1.1.4/THIRD-PARTY-NOTICES.md', 'THIRD-PARTY-NOTICES.md'),
    'repo': ('https://api.github.com/repos/omlahore/RemoveMacAI', 'repo.json'),
}


def retrieve(item):
    key, (url, name) = item
    request = urllib.request.Request(url, headers={'User-Agent': 'BreathingRoom-documentary-research'})
    with urllib.request.urlopen(request, timeout=45) as response:
        data = response.read()
        final = response.url
        status = response.status
    destination = ROOT / 'sources' / name
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(data)
    return {'id': key, 'url': url, 'finalUrl': final, 'httpStatus': status,
            'retrievedAtUtc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'path': str(destination.relative_to(APP)), 'sha256': hashlib.sha256(data).hexdigest()}


if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        ledger = list(pool.map(retrieve, SOURCES.items()))
    # The repository MIT licence explicitly covers associated documentation files.
    # Retain it with the unmodified documentation screenshot; do not infer trademark rights.
    license_text = (ROOT / 'sources/LICENSE.txt').read_text()
    assert 'associated documentation files' in license_text
    image = retrieve(('competitor-ui', (RAW + 'v1.1.4/docs/screens/overview-light.webp', 'overview-light-original.webp')))
    ledger.append(image)
    (ROOT / 'sources/ledger.json').write_text(json.dumps(ledger, indent=2) + '\n')
    print(json.dumps(ledger, indent=2))
