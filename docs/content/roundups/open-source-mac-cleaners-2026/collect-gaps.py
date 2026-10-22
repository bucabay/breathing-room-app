"""Retain missing public licence evidence only; never execute downloaded code."""
import concurrent.futures
import datetime
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).parent
URLS = {
    'depflush-license': 'https://raw.githubusercontent.com/cypriennkeneng/depflush/main/LICENSE',
    'mac-sai-license': 'https://raw.githubusercontent.com/iliyami/MacSai/main/LICENSE',
    'app-eraser-license': 'https://raw.githubusercontent.com/davunt/app-eraser/main/LICENSE',
    'app-eraser-package': 'https://raw.githubusercontent.com/davunt/app-eraser/main/package.json',
    'commons-clause': 'https://commonsclause.com/',
    'open-source-definition': 'https://opensource.org/osd',
}

def collect(item):
    key, url = item
    target = ROOT / 'sources' / (key + '.txt')
    if target.exists():
        body = target.read_bytes()
        return dict(id=key, url=url, retrievedAtUtc=None, checkedOn='2026-10-22',
                    note='Retained in initial collection; exact retrieval instant not saved.',
                    path=str(target.relative_to(ROOT)), sha256=hashlib.sha256(body).hexdigest())
    try:
        with urllib.request.urlopen(url, timeout=40) as response:
            body = response.read()
            final = response.url
    except Exception as error:
        return dict(id=key, url=url, error=str(error), checkedOn='2026-10-22')
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(body)
    return dict(id=key, url=url, finalUrl=final,
                retrievedAtUtc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                path=str(target.relative_to(ROOT)), sha256=hashlib.sha256(body).hexdigest())

if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        records = list(pool.map(collect, URLS.items()))
    (ROOT / 'sources.json').write_text(json.dumps(records, indent=2) + '\n')
    print(json.dumps(records, indent=2))
