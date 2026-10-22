"""Read-only public-source retention for research-backapp; no installation or app execution."""
import hashlib
import json
import struct
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP = ROOT.parents[3]
COMMIT = "ebf4502d32ebe5b801b00e86653a4dd2fb3ba201"
RAW = f"https://raw.githubusercontent.com/li-nd/BackApp/{COMMIT}/"


def collect():
    sources = []
    for sid, url, name in [
        ("install", RAW + "docs/install.md", "install.md"),
        ("usage", RAW + "docs/usage.md", "usage.md"),
        ("readme", RAW + "README.md", "README.md"),
        ("license", RAW + "LICENSE", "LICENSE.txt"),
        ("snapshot-model", RAW + "BackApp/Models/Snapshot.swift", "Snapshot.swift"),
        ("project", RAW + "BackApp.xcodeproj/project.pbxproj", "project.pbxproj"),
        ("tagged-project", "https://raw.githubusercontent.com/li-nd/BackApp/v1.0.0/BackApp.xcodeproj/project.pbxproj", "project-v1.0.0.pbxproj"),
        ("release", "https://api.github.com/repos/li-nd/BackApp/releases/latest", "release.json"),
        ("cask", "https://raw.githubusercontent.com/li-nd/homebrew-apps/main/Casks/backapp.rb", "backapp.rb"),
        ("competitor-visual", RAW + "docs/screenshots/4-snapshot-compare.png", "snapshot-compare-original.png"),
    ]:
        path = ROOT / ("assets" if sid == "competitor-visual" else "sources") / name
        path.parent.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(url, headers={"User-Agent": "BreathingRoom-evidence-research"})
        with urllib.request.urlopen(req, timeout=45) as response:
            data = response.read()
            final_url = response.url
            status = response.status
        path.write_bytes(data)
        record = {
            "id": sid, "url": url, "finalUrl": final_url,
            "retrievedAtUtc": datetime.now(timezone.utc).isoformat(),
            "httpStatus": status, "snapshotPath": str(path.relative_to(APP)),
            "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data),
            "publisher": "Markus Lind / li-nd", "publicationDate": None,
            "scope": "Pinned repository documentation/source; not a runtime test" if RAW in url else "Public release/tap metadata; not binary validation",
        }
        if sid == "competitor-visual":
            assert data[:8] == b"\x89PNG\r\n\x1a\n"
            record["widthPx"], record["heightPx"] = struct.unpack(">II", data[16:24])
        sources.append(record)
    (ROOT / "source-ledger.json").write_text(json.dumps(sources, indent=2) + "\n")
    print(json.dumps(sources, indent=2))


if __name__ == "__main__":
    collect()
