"""Read-only public-source retention for DiskMaid research (no image download)."""
import datetime
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parent
SOURCES = {
    'app-store': 'https://apps.apple.com/us/app/id6758129723',
    'terms': 'https://nalarin.com/mymacmaid/terms',
    'privacy': 'https://nalarin.com/mymacmaid/privacy',
    'official-visual-locators': 'https://nalarin.com/diskmaid',
}

if __name__ == '__main__':
    out = ROOT / 'sources'
    out.mkdir(exist_ok=True)
    records = []
    for key, url in SOURCES.items():
        try:
            response = urllib.request.urlopen(url, timeout=45)
        except Exception as error:
            records.append({'id': key, 'url': url, 'error': str(error), 'retrievedAtUtc': datetime.datetime.now(datetime.timezone.utc).isoformat()})
            continue
        with response:
            body = response.read()
            record = {
                'id': key, 'url': url, 'finalUrl': response.url,
                'httpStatus': response.status,
                'retrievedAtUtc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                'path': str((out / (key + '.html')).relative_to(ROOT)),
                'sha256': hashlib.sha256(body).hexdigest(),
                'purpose': 'Missing terms/platform/availability/privacy evidence or exact official screenshot locators; not a repeat feature verification.',
            }
        (out / (key + '.html')).write_bytes(body)
        records.append(record)
    (out / 'manifest.json').write_text(json.dumps(records, indent=2) + '\n')
    print(json.dumps(records, indent=2))
