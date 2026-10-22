"""Read-only public evidence capture, scoped to this research packet."""
import concurrent.futures
import datetime
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parent
SOURCES = {
    'gnome-visual-page': 'https://apps.gnome.org/Baobab/',
    'homebrew': 'https://formulae.brew.sh/api/formula/baobab.json',
    'gnome-contribute': 'https://welcome.gnome.org/app/Baobab/',
    'trash-help': 'https://help.gnome.org/baobab/question-trash.html',
    'remote-help': 'https://help.gnome.org/baobab/scan-remote.html',
    'permissions-help': 'https://help.gnome.org/baobab/problem-permissions.html',
    'scan-image': 'https://static.gnome.org/catalog/app-screenshot/org.gnome.baobab/image-2_orig.png',
}


def capture(item):
    key, url = item
    request = urllib.request.Request(url, headers={'User-Agent': 'BreathingRoomContentResearch/1.0'})
    with urllib.request.urlopen(request, timeout=60) as response:
        data = response.read()
        suffix = '.png' if key == 'scan-image' else '.json' if key == 'homebrew' else '.html'
        path = ROOT / 'evidence' / (key + suffix)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return dict(id=key, url=url, finalUrl=response.url, httpStatus=response.status,
                    retrievedAtUtc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    path=str(path.relative_to(ROOT)), sha256=hashlib.sha256(data).hexdigest(), bytes=len(data))


if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        records = list(executor.map(capture, SOURCES.items()))
    (ROOT / 'evidence-index.json').write_text(json.dumps(records, indent=2) + '\n')
    print(json.dumps(records, indent=2))
