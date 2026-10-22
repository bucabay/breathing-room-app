"""Read-only public HTML evidence collection; no installers, accounts or images."""
import datetime
import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).parent
SOURCES = {
    "mac-product": "https://cleanerone.trendmicro.com/cleaner-one-pro-for-mac/",
    "purchase": "https://cleanerone.trendmicro.com/cleaner-one-pro-buy/",
    "faq": "https://cleanerone.trendmicro.com/blog/cleaner-one-pro-faq/",
    "installation": "https://helpcenter.trendmicro.com/en-us/article/TMKA-10020",
    "edition-differences": "https://cleanerone.trendmicro.com/blog/cleaner-one-apps-features/",
    "renewal": "https://cleanerone.trendmicro.com/blog/how-do-i-cancel-automatic-renewal-subscription-for-cleaner-one-pro/",
    "legal": "https://www.trendmicro.com/en_us/about/legal.html",
}


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text, self.links, self.images = [], [], []
        self.hidden = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("script", "style"):
            self.hidden += 1
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag == "img":
            self.images.append({k: v for k, v in a.items() if k in ("src", "alt", "data-src") and not (v or "").startswith("data:")})

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.hidden = max(0, self.hidden - 1)

    def handle_data(self, data):
        if not self.hidden and data.strip():
            self.text.append(data.strip())


if __name__ == "__main__":
    out = ROOT / "sources"
    out.mkdir(exist_ok=True)
    for name, url in SOURCES.items():
        if (out / f"{name}.json").exists():
            continue
        with urlopen(Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=60) as response:
            raw, final, status = response.read(), response.url, response.status
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        (out / f"{name}.html").write_bytes(raw)
        page = Page()
        page.feed(raw.decode("utf-8", errors="replace"))
        record = dict(id=name, sourceUrl=url, finalUrl=final, retrievedAtUtc=timestamp,
                      httpStatus=status, sha256=hashlib.sha256(raw).hexdigest(),
                      snapshotPath=f"sources/{name}.html", text="\n".join(page.text),
                      links=page.links, images=page.images)
        (out / f"{name}.json").write_text(json.dumps(record, indent=2) + "\n")
        print(name, status, timestamp, record["sha256"])
