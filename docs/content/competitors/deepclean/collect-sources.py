"""Read-only public source archival; writes only this research folder. No images."""
import concurrent.futures
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
        self.parts = []
        self.hidden = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("style", "script"):
            self.hidden += 1

    def handle_endtag(self, tag):
        if tag in ("style", "script"):
            self.hidden = max(0, self.hidden - 1)

    def handle_data(self, data):
        if not self.hidden and data.strip():
            self.parts.append(data.strip())


def archive(item):
    key, url = item
    record = {"id": key, "url": url, "retrievedAtUtc": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        with urllib.request.urlopen(url, timeout=45) as response:
            raw = response.read()
            record.update(finalUrl=response.url, httpStatus=response.status)
        path = ROOT / "sources" / (key + ".html")
        path.write_bytes(raw)
        parser = Text()
        parser.feed(raw.decode("utf-8"))
        text_path = path.with_suffix(".txt")
        text_path.write_text("\n".join(parser.parts) + "\n")
        record.update(snapshotPath=str(path.relative_to(ROOT)), sha256=hashlib.sha256(raw).hexdigest(), textPath=str(text_path.relative_to(ROOT)))
    except Exception as exc:
        record["error"] = str(exc)
    return record


if __name__ == "__main__":
    urls = {key: "https://deepclean.app/" + suffix for key, suffix in {
        "about": "about", "terms": "terms", "privacy": "privacy", "download": "download",
        "press": "press/", "developer-tools": "features/developer-tools"
    }.items()}
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        records = list(pool.map(archive, urls.items()))
    (ROOT / "sources" / "retrievals.json").write_text(json.dumps(records, indent=2) + "\n")
    print(json.dumps(records, indent=2))
