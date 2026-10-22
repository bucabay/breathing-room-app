"""Read-only public-source collection; never installs or executes product code."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
DEST = ROOT / 'sources'
DEST.mkdir(exist_ok=True)
records = []

def get(name, url):
    with urlopen(Request(url, headers={'User-Agent': 'BreathingRoom-documentary-research'}), timeout=60) as response:
        data = response.read()
        record = {'id': name, 'url': url, 'finalUrl': response.url,
                  'retrievedAtUtc': datetime.now(timezone.utc).isoformat(),
                  'httpStatus': response.status, 'path': str((DEST / name).relative_to(ROOT)),
                  'sha256': hashlib.sha256(data).hexdigest()}
    (DEST / name).write_bytes(data)
    records.append(record)
    return data

commit = json.loads(get('commit.json', 'https://api.github.com/repos/Better-Linux/CleanMyLinux/commits/main'))['sha']
for name, path in [('README.md', 'README.md'), ('LICENSE', 'LICENSE')]:
    get(name, f'https://raw.githubusercontent.com/Better-Linux/CleanMyLinux/{commit}/{path}')
get('release.json', 'https://api.github.com/repos/Better-Linux/CleanMyLinux/releases/latest')
get('tree.json', f'https://api.github.com/repos/Better-Linux/CleanMyLinux/git/trees/{commit}?recursive=1')
(DEST / 'manifest.json').write_text(json.dumps({'commit': commit, 'sources': records}, indent=2) + '\n')
print(json.dumps({'commit': commit, 'sources': records}, indent=2))
