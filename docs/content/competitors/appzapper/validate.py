"""Read-only research-packet checks; does not execute product code or mutate queue."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PACKET = Path(__file__).with_name("research.json")
data = json.loads(PACKET.read_text())
assert data["jobId"] == "research-appzapper"
assert data["identity"]["canonicalOwnerId"] == "appzapper"
assert data["status"] == "blocked" and not data["handoff"]["draftingAllowed"]
assert not data["published"] and not data["handoff"]["siteEdits"]
sources = {s["id"]: s for s in data["sources"]}
claims = {c["id"]: c for c in data["claims"]}
assert len(claims) == len(data["claims"])
for claim in claims.values():
    assert claim["excerpt"] and claim["scope"] and claim["checkedOn"] == "2026-10-21"
    assert claim["sourceIds"] and all(s in sources for s in claim["sourceIds"])
for row in data["matrix"]:
    assert all(c in claims for c in row["claimIds"] + row["breathingRoomClaimIds"])
hash_count = 0
for source in sources.values():
    if source.get("snapshotPath") and source.get("sha256"):
        path = ROOT / source["snapshotPath"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == source["sha256"], path
        hash_count += 1
for visual in data["visuals"]:
    assert visual["caption"] and visual["alt"] and visual["reuse"]["basis"]
    if visual["productId"] == "appzapper":
        assert visual["reuse"]["status"] == "link-only"
        assert visual["originalPath"] is None and visual["originalSha256"] is None
    else:
        assert "Example data only" in visual["caption"]
        path = ROOT / visual["originalPath"]
        raw = path.read_bytes()
        assert raw[:8] == b"\x89PNG\r\n\x1a\n"
        assert int.from_bytes(raw[16:20], "big") == visual["widthPx"]
        assert int.from_bytes(raw[20:24], "big") == visual["heightPx"]
        assert hashlib.sha256(raw).hexdigest() == visual["originalSha256"]
        hash_count += 1
html = (PACKET.parent / "sources/homepage-html-tool-output.txt").read_text()
assert '/site/appzapper-3000/assets/step2.png' in html
assert '"priceCurrency": "USD"' in html
assert '"price": "18.00"' in html
baseline = json.loads((ROOT / "docs/content/verification/batch-1.json").read_text())
assert 'AppZapper 3000' in json.dumps(baseline)
for brief in data["briefs"].values():
    assert brief["draftGate"] == "blocked-image-rights-and-visual-inspection"
assert Path(__file__).with_name("research.md").is_file()
print(f"PASS: JSON structure; {len(claims)} claim/source mappings; {len(data['matrix'])} matrix rows; {hash_count} source/asset hashes; PNG dimensions; official asset/USD metadata; blocked visual/draft gates; both briefs.")
print("LIMIT: structural checks are not image-rights clearance, visual inspection, native testing, or independent publication review.")
