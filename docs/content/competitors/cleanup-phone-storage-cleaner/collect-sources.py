"""Retain public textual evidence only; do not download third-party images."""
import datetime
import hashlib
import json
import pathlib
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent
SOURCES = {
    "apple": "https://apps.apple.com/us/app/cleanup-phone-storage-cleaner/id1510944943",
    "terms": "https://cleanup.photos/terms",
    "product-site": "https://cleanupapp.co/",
}
records = []
for key, url in SOURCES.items():
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=45) as response:
        data = response.read()
        target = ROOT / "sources" / (key + ".html")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        records.append({"id": key, "url": url, "finalUrl": response.url,
                        "retrievedAtUtc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                        "httpStatus": response.status, "path": str(target.relative_to(ROOT)),
                        "sha256": hashlib.sha256(data).hexdigest()})
(ROOT / "sources" / "manifest.json").write_text(json.dumps(records, indent=2) + "\n")
print(json.dumps(records, indent=2))
