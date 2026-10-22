"""Read-only public evidence collection for research-cleanmymac; no app execution."""
import datetime
import hashlib
import json
from pathlib import Path
import urllib.request
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parent

class Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hidden = 0
        self.parts = []
        self.links = []
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.hidden += 1
        a = dict(attrs)
        if tag == 'a' and a.get('href'):
            self.links.append(a['href'])
    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.hidden = max(0, self.hidden - 1)
    def handle_data(self, data):
        if not self.hidden and data.strip():
            self.parts.append(data.strip())

URLS = {
    'press': 'https://macpaw.com/press',
    'smart-care': 'https://macpaw.com/support/cleanmymac/knowledgebase/smart-care',
    'purchase': 'https://macpaw.com/support/cleanmymac/knowledgebase/purchase-and-subscription',
    'whats-new': 'https://macpaw.com/cleanmymac/whats-new',
    'eula': 'https://macpaw.com/eula',
    'powermymac': 'https://www.imymac.com/powermymac/',
}

if __name__ == '__main__':
    out = ROOT / 'sources'
    out.mkdir(exist_ok=True)
    for name, url in URLS.items():
        record = {'url': url, 'retrievedAtUtc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=45) as r:
                raw = r.read()
                record.update(finalUrl=r.url, httpStatus=r.status, rawSha256=hashlib.sha256(raw).hexdigest())
            (out / (name + '.html')).write_bytes(raw)
            parser = Text()
            parser.feed(raw.decode('utf-8', errors='replace'))
            record.update(text='\n'.join(parser.parts), links=parser.links, snapshotPath=str((out / (name + '.html')).relative_to(ROOT)))
        except Exception as e:
            record['error'] = str(e)
        (out / (name + '.json')).write_text(json.dumps(record, indent=2) + '\n')
        print(name, record.get('httpStatus', record.get('error')), len(record.get('text', '')))
