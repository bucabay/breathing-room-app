"""Read-only public-source capture; writes only this research directory."""
import concurrent.futures
import datetime
import hashlib
import io
import json
from pathlib import Path
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parent
SOURCES = {
    'store': 'https://cindori.com/store/sensei',
    'press': 'https://cindori.com/press',
    'older-versions': 'https://cindori.com/support/sensei/general/download-older-sensei',
    'eula': 'https://cindori.com/support/order/legal/license-agreement',
    'release-1.6': 'https://cindori.com/news/sensei-1.6',
    'vendor-comparison': 'https://cindori.com/reviews/stats-vs-sensei-mac-monitoring',
    'about': 'https://cindori.com/about',
    'upgrade': 'https://cindori.com/store/upgrade',
}

def capture(item):
    name, url = item
    with urllib.request.urlopen(url, timeout=60) as response:
        data = response.read()
        record = dict(id=name, url=url, finalUrl=response.url,
                      retrievedAtUtc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                      httpStatus=response.status, sha256=hashlib.sha256(data).hexdigest(),
                      snapshotPath=str((ROOT / 'sources' / (name + '.html')).relative_to(ROOT)),
                      publicationDate=None)
    (ROOT / record['snapshotPath']).write_bytes(data)
    return record

if __name__ == '__main__':
    (ROOT / 'sources').mkdir(exist_ok=True)
    (ROOT / 'assets').mkdir(exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        records = list(pool.map(capture, SOURCES.items()))
    url = 'https://cdn.cindori.com/apps/press/SenseiPressKit.zip'
    with urllib.request.urlopen(url, timeout=90) as response:
        data = response.read()
        record = dict(id='press-kit', url=url, finalUrl=response.url,
                      retrievedAtUtc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                      httpStatus=response.status, sha256=hashlib.sha256(data).hexdigest(),
                      snapshotPath='sources/SenseiPressKit.zip', publicationDate=None)
    (ROOT / record['snapshotPath']).write_bytes(data)
    archive = zipfile.ZipFile(io.BytesIO(data))
    record['members'] = [dict(name=i.filename, bytes=i.file_size) for i in archive.infolist()]
    selected = {
        'Sensei Press Kit/Welcome.pdf': 'sources/Welcome.pdf',
        'Sensei Press Kit/Questions Ansers.pdf': 'sources/Questions-Answers.pdf',
        'Sensei Press Kit/Artwork/Clean/Web/Clean Desktop Dark.png': 'assets/sensei-clean-original.png',
        'Sensei Press Kit/Artwork/Storage/Web/Disk Health Desktop Dark.png': 'assets/sensei-drive-health-original.png',
    }
    record['selectedAssets'] = []
    for member, target in selected.items():
        original = archive.read(member)
        (ROOT / target).write_bytes(original)
        record['selectedAssets'].append(dict(member=member, path=target,
            sha256=hashlib.sha256(original).hexdigest(), bytes=len(original)))
    records.append(record)
    (ROOT / 'sources/index.json').write_text(json.dumps(records, indent=2) + '\n')
    print(json.dumps([dict(id=r['id'], status=r['httpStatus'], sha256=r['sha256']) for r in records], indent=2))
