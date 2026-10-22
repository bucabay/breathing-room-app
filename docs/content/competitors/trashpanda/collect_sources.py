"""Read-only public-source retention for research-trashpanda; no image downloads."""
import hashlib
import json
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent


class VisibleText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hidden = 0
        self.parts = []
        self.images = []
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ('script', 'style'):
            self.hidden += 1
        if tag == 'img':
            self.images.append(attrs)
        if tag == 'a' and attrs.get('href'):
            self.links.append(attrs['href'])

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.hidden = max(0, self.hidden - 1)

    def handle_data(self, data):
        if not self.hidden and data.strip():
            self.parts.append(data.strip())


def main():
    target = ROOT / 'sources'
    target.mkdir(exist_ok=True)
    for name in ('downloads', 'terms', 'updates'):
        url = f'https://trashpandamacos.vercel.app/{name}'
        with urlopen(Request(url, headers={'User-Agent': 'BreathingRoom documentary research'}), timeout=40) as response:
            raw = response.read()
            final = response.url
            status = response.status
        parser = VisibleText()
        parser.feed(raw.decode('utf-8'))
        html_path = target / f'{name}.html'
        html_path.write_bytes(raw)
        record = dict(url=url, finalUrl=final, httpStatus=status,
                      retrievedAtUtc=datetime.now(timezone.utc).isoformat(),
                      rawPath=str(html_path.relative_to(ROOT)),
                      rawSha256=hashlib.sha256(raw).hexdigest(),
                      text='\n'.join(parser.parts), images=parser.images,
                      links=parser.links)
        (target / f'{name}.json').write_text(json.dumps(record, indent=2) + '\n')
        print(name, status, final, record['rawSha256'])


if __name__ == '__main__':
    main()
