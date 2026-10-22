"""Read-only public evidence capture; no binaries, images, accounts or checkout."""
import datetime
import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urljoin

ROOT = Path(__file__).parent


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.links = []
        self.images = []
        self.hidden = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ('script', 'style'):
            self.hidden += 1
        if tag == 'a' and 'href' in a:
            self.links.append(a['href'])
        if tag == 'img':
            self.images.append(a)

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.hidden = max(0, self.hidden - 1)

    def handle_data(self, data):
        if not self.hidden and data.strip():
            self.text.append(data.strip())


if __name__ == '__main__':
    out = []
    for slug in ('download', 'pricing', 'privacy', 'terms', 'refunds', 'contact'):
        url = f'https://amplecapacity.com/{slug}.html'
        with urlopen(Request(url, headers={'User-Agent': 'BreathingRoom-Research/1.0'}), timeout=40) as response:
            raw = response.read()
            retrieved = datetime.datetime.now(datetime.timezone.utc).isoformat()
            final_url = response.url
            status = response.status
        folder = ROOT / 'sources'
        folder.mkdir(exist_ok=True)
        path = folder / f'{slug}.html'
        path.write_bytes(raw)
        page = Page()
        page.feed(raw.decode('utf-8'))
        record = {
            'id': slug, 'url': url, 'finalUrl': final_url,
            'retrievedAtUtc': retrieved, 'httpStatus': status,
            'snapshotPath': str(path.relative_to(ROOT)),
            'sha256': hashlib.sha256(raw).hexdigest(),
            'text': '\n'.join(page.text),
            'links': [urljoin(final_url, v) for v in page.links],
            'images': [{**v, 'absoluteSrc': urljoin(final_url, v.get('src', ''))} for v in page.images],
        }
        out.append(record)
    (ROOT / 'sources' / 'index.json').write_text(json.dumps(out, indent=2) + '\n')
    for record in out:
        print(record['id'], record['httpStatus'], record['sha256'])
        print('Images:', json.dumps(record['images']))
