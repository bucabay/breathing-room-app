"""Read-only public evidence retention; writes only this competitor's packet."""
import datetime
import hashlib
import json
from pathlib import Path
from html.parser import HTMLParser
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
APP = ROOT.parents[3]

class Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.skip = 0
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'): self.skip += 1
    def handle_endtag(self, tag):
        if tag in ('script', 'style'): self.skip = max(0, self.skip - 1)
    def handle_data(self, data):
        if not self.skip and data.strip(): self.parts.append(data.strip())

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def rel(path):
    return str(path.relative_to(APP))

def write(name, value):
    (ROOT / name).write_text(json.dumps(value, indent=2) + '\n')

def main():
    baseline = json.loads((APP / 'docs/content/verification/batch-1.json').read_text())
    # Retain the matching record without re-fetching its already-current homepage.
    records = baseline.get('products', baseline.get('records', []))
    if not records:
        records = next(v for v in baseline.values() if isinstance(v, list) and v and isinstance(v[0], dict) and 'id' in v[0])
    record = next(x for x in records if x['id'] == 'aiseesoft-mac-cleaner')
    write('baseline-reused.json', record)
    sources = []
    for sid, path in [('official-home', record['sources'][0]['snapshotPath']), ('directory', record['discovery']['snapshotPath'])]:
        p = APP / path
        d = json.loads(p.read_text())
        sources.append({'id': sid, 'url': d.get('officialUrl', d.get('url')), 'finalUrl': d.get('finalUrl', d.get('url')), 'retrievedAtUtc': d.get('retrievedAt'), 'snapshotPath': path, 'sha256': sha(p), 'reused': True, 'publicationDate': None, 'scope': 'Public vendor documentation' if sid == 'official-home' else 'Discovery only'})
    evidence = ROOT / 'sources'
    evidence.mkdir(exist_ok=True)
    for sid, url in [('guide', 'https://www.aiseesoft.com/mac-cleaner/tutorial.html'), ('purchase', 'https://www.aiseesoft.com/purchase/mac-cleaner.html')]:
        with urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=45) as response:
            raw = response.read()
            final = response.url
            status = response.status
        at = datetime.datetime.now(datetime.timezone.utc).isoformat()
        html = evidence / (sid + '.html')
        html.write_bytes(raw)
        parser = Text()
        parser.feed(raw.decode('utf-8', errors='replace'))
        text = evidence / (sid + '.txt')
        text.write_text('\n'.join(parser.parts) + '\n')
        sources.append({'id': sid, 'url': url, 'finalUrl': final, 'retrievedAtUtc': at, 'httpStatus': status, 'snapshotPath': rel(html), 'sha256': sha(html), 'textPath': rel(text), 'textSha256': sha(text), 'publicationDate': None, 'scope': 'Unversioned public vendor documentation', 'reused': False})
    write('sources.json', sources)
    print(json.dumps({'retainedSources': len(sources), 'homepageRefetched': False, 'imageDownloads': 0}, indent=2))

if __name__ == '__main__': main()
