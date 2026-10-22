"""Read-only public source retention for the DriveScape research job; no binaries."""
import datetime
import hashlib
import json
from pathlib import Path
from html.parser import HTMLParser
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
class Parser(HTMLParser):
    def __init__(self):
        super().__init__(); self.images = []; self.links = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ('img', 'source'): self.images.append(a)
        if tag == 'a' and 'href' in a: self.links.append(a['href'])

urls = {
    'press': 'https://drivescape.dev/press',
    'eula': 'https://drivescape.dev/eula',
    'changelog': 'https://drivescape.dev/changelog',
    'privacy': 'https://drivescape.dev/privacy',
    'how-it-works': 'https://drivescape.dev/en/how-it-works',
    'repository': 'https://github.com/BrickLogic/ChartyDriveReleases',
    'listing-visuals': 'https://alternativeto.net/software/drivescape/about/',
    'release-latest': 'https://api.github.com/repos/BrickLogic/ChartyDriveReleases/releases/latest',
}
records = []
for name, url in urls.items():
    record = {'id': name, 'url': url, 'retrievedAtUtc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        with urlopen(Request(url, headers={'User-Agent': 'BreathingRoomContentResearch/1.0'}), timeout=45) as r:
            data = r.read(); record.update(finalUrl=r.url, httpStatus=r.status)
        suffix = '.json' if name == 'release-latest' else '.html'
        p = ROOT / 'sources' / (name + suffix); p.parent.mkdir(exist_ok=True); p.write_bytes(data)
        record.update(path=str(p.relative_to(ROOT)), sha256=hashlib.sha256(data).hexdigest())
        if suffix == '.html':
            parser = Parser(); parser.feed(data.decode('utf-8'))
            record.update(images=parser.images)
        else:
            release = json.loads(data)
            record.update(tag=release.get('tag_name'), publishedAt=release.get('published_at'), assets=[a['name'] for a in release.get('assets', [])])
    except Exception as e:
        record['error'] = str(e)
    records.append(record)
(ROOT / 'source-retrievals.json').write_text(json.dumps(records, indent=2) + '\n')
print(json.dumps(records, indent=2))
