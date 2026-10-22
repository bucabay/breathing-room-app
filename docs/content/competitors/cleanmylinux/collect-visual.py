"""Download only the official repository's MIT-licensed documentation preview."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen

root = Path(__file__).resolve().parent
commit = json.loads((root / 'sources/manifest.json').read_text())['commit']
url = f'https://raw.githubusercontent.com/Better-Linux/CleanMyLinux/{commit}/public/image.png'
with urlopen(url, timeout=60) as response:
    data = response.read()
    final_url = response.url
assert data.startswith(b'\x89PNG\r\n\x1a\n')
(root / 'assets').mkdir(exist_ok=True)
(root / 'assets/cleanmylinux-official-preview.png').write_bytes(data)
record = {'url': url, 'finalUrl': final_url, 'retrievedAtUtc': datetime.now(timezone.utc).isoformat(),
          'path': 'assets/cleanmylinux-official-preview.png', 'sha256': hashlib.sha256(data).hexdigest(),
          'widthPx': int.from_bytes(data[16:20], 'big'), 'heightPx': int.from_bytes(data[20:24], 'big'),
          'reuseBasis': 'Repository README documentation image under root MIT LICENSE; retain complete copyright and permission notice in sources/LICENSE; no trademark endorsement inferred.'}
(root / 'sources/visual-download.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record, indent=2))
