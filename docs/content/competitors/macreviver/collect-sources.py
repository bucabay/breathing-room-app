"""Read-only public documentary collection; no binaries, images or accounts."""
import concurrent.futures
import datetime
import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
BASE = 'https://www.reviversoft.com/'
URLS = {
    'quick-cleanup': BASE + 'support/macreviver/how-do-i-use-quick-cleanup-to-clean-unnecessary-files-in-macreviver/',
    'disk-usage': BASE + 'support/macreviver/how-do-i-use-disk-usage-to-find-the-folders-and-files-that-take-up-the-most-space-in-macreviver/',
    'registration': BASE + 'support/macreviver/how-do-i-register-my-copy-of-macreviver/',
    'downloads': BASE + 'download/',
    'store': BASE + 'store/',
    'terms': BASE + 'terms-of-use/',
    'legacy-offer': BASE + 'macreviver/lp/download-ready-rw/index.php',
    'overview': BASE + 'support/macreviver/why-should-i-use-macreviver/',
    'eula': BASE + 'eula/',
}

class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text, self.images, self.links = [], [], []
        self.ignore = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ('script', 'style'):
            self.ignore += 1
        if tag == 'img':
            self.images.append(a)
        if tag == 'a' and a.get('href'):
            self.links.append(a['href'])

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.ignore = max(0, self.ignore - 1)

    def handle_data(self, data):
        if not self.ignore and data.strip():
            self.text.append(data.strip())

def collect(item):
    key, url = item
    if (ROOT / 'sources' / (key + '.json')).exists():
        return {'id': key, 'result': 'reused-existing-snapshot'}
    record = {'id': key, 'sourceUrl': url, 'retrievedAtUtc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        with urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=45) as response:
            data = response.read()
            record.update(finalUrl=response.url, httpStatus=response.status)
        path = ROOT / 'sources' / (key + '.html')
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        p = Parser()
        p.feed(data.decode('utf-8', errors='replace'))
        record.update(snapshotPath=str(path.relative_to(ROOT)), sha256=hashlib.sha256(data).hexdigest(), text='\n'.join(p.text), images=p.images, links=p.links)
    except Exception as error:
        record['error'] = str(error)
    (ROOT / 'sources' / (key + '.json')).write_text(json.dumps(record, indent=2) + '\n')
    return {'id': key, 'error': record.get('error'), 'finalUrl': record.get('finalUrl')}

if __name__ == '__main__':
    (ROOT / 'sources').mkdir(parents=True, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        print(json.dumps(list(pool.map(collect, URLS.items())), indent=2))
