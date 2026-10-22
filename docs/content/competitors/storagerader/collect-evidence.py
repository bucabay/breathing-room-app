"""Retain only missing official evidence. No image or binary downloads."""
import datetime
import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent


class Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hidden = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.hidden += 1

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.hidden = max(0, self.hidden - 1)

    def handle_data(self, data):
        if not self.hidden and data.strip():
            self.parts.append(data.strip())


if __name__ == '__main__':
    evidence = ROOT / 'evidence'
    evidence.mkdir(exist_ok=True)
    for name, url in [
        ('about', 'https://storageradar.app/about/'),
        ('direct', 'https://storageradar.app/direct/'),
        ('changelog', 'https://storageradar.app/changelog/'),
        ('privacy', 'https://storageradar.app/privacy/'),
    ]:
        with urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=45) as response:
            raw = response.read()
            final = response.url
            status = response.status
        (evidence / (name + '.html')).write_bytes(raw)
        parser = Text()
        parser.feed(raw.decode('utf-8'))
        record = dict(url=url, finalUrl=final, httpStatus=status,
                      retrievedAtUtc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                      rawPath=str((evidence / (name + '.html')).relative_to(ROOT)),
                      rawSha256=hashlib.sha256(raw).hexdigest(), text='\n'.join(parser.parts))
        (evidence / (name + '.json')).write_text(json.dumps(record, indent=2) + '\n')
        print(name, status, record['rawSha256'])
