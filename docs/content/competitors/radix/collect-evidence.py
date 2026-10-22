"""Read-only public evidence collection; writes only this product folder."""
import datetime
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parent
(ROOT / 'sources').mkdir(exist_ok=True)
(ROOT / 'assets').mkdir(exist_ok=True)
records = []

def get(source_id, url, relative):
    request = urllib.request.Request(url, headers={'User-Agent': 'BreathingRoom-editorial-research', 'Accept': '*/*'})
    with urllib.request.urlopen(request, timeout=60) as response:
        data = response.read()
        final_url = response.url
        status = response.status
    path = ROOT / relative
    path.write_bytes(data)
    records.append(dict(id=source_id, url=url, finalUrl=final_url, retrievedAtUtc=datetime.datetime.now(datetime.timezone.utc).isoformat(), httpStatus=status, path=str(path.relative_to(ROOT)), sha256=hashlib.sha256(data).hexdigest(), bytes=len(data)))
    return data

commit = json.loads(get('repository-head', 'https://api.github.com/repos/colinvkim/Radix/commits/main', 'sources/repository-head.json'))['sha']
get('readme', f'https://raw.githubusercontent.com/colinvkim/Radix/{commit}/README.md', 'sources/README.md')
get('license', f'https://raw.githubusercontent.com/colinvkim/Radix/{commit}/LICENSE', 'sources/LICENSE.txt')
get('release', 'https://api.github.com/repos/colinvkim/Radix/releases/latest', 'sources/latest-release.json')
# README embeds this exact public repository UI image. The repository MIT licence
# is retained before copying; no separate exclusion is stated in README/LICENSE.
get('radix-comparison-image', f'https://raw.githubusercontent.com/colinvkim/Radix/{commit}/docs/images/radix-scan-comparison.png', 'assets/radix-scan-comparison-original.png')
(ROOT / 'sources/retrievals.json').write_text(json.dumps({'commit': commit, 'sources': records}, indent=2) + '\n')
print(json.dumps({'commit': commit, 'sources': records}, indent=2))
