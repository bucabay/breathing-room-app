"""Read-only structural/evidence checks; never certifies publication or runtime behavior."""
import hashlib
import json
from pathlib import Path

FOLDER = Path(__file__).resolve().parent
ROOT = FOLDER.parents[3]
packet = json.loads((FOLDER / "research.json").read_text())
sources = {source["id"]: source for source in packet["sources"]}
claims = {claim["id"]: claim for claim in packet["claims"]}
checked_hashes = 0
for source in sources.values():
    if source.get("snapshotPath"):
        path = ROOT / source["snapshotPath"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == source["sha256"]
        checked_hashes += 1
discovery = packet["discovery"]
assert hashlib.sha256((ROOT / discovery["snapshotPath"]).read_bytes()).hexdigest() == discovery["sha256"]
for claim in claims.values():
    assert set(claim["sourceIds"]) <= sources.keys()
    assert claim["excerpt"] and claim["checkedOnUtc"] and claim["scope"]
for cell in packet["productMatrix"].values():
    assert set(cell["claimIds"]) <= claims.keys()
release = json.loads((FOLDER / "sources/release-2013.json").read_text())
for value in ["7.0", "10.6.8", "$39.99 USD", "50%", "scheduling tool"]:
    assert value.lower() in release["text"].lower(), value
download = json.loads((FOLDER / "sources/download-v7.json").read_text())
for value in ["Enter Password to Download", "Download card", "pre_setup.app", "MacTuneUpv7.0.1.dmg"]:
    assert value in download["text"], value
for source_id, name in [("S1", "homepage"), ("S3", "release-2013"), ("S4", "download-v7")]:
    snapshot = json.loads((FOLDER / f"sources/{name}.json").read_text())
    assert snapshot["url"] == sources[source_id]["finalUrl"]
    assert snapshot["retrievedAtUtc"] == sources[source_id]["retrievedAtUtc"]
for visual in packet["visuals"]:
    if visual.get("originalPath"):
        assert hashlib.sha256((ROOT / visual["originalPath"]).read_bytes()).hexdigest() == visual["originalSha256"]
media = json.loads((FOLDER / "sources/official-media.json").read_text())
assert len(media) == 15
assert any(item["source_url"] == packet["visuals"][1]["assetUrl"] for item in media)
assert packet["status"] == "blocked" and not packet["published"]
assert packet["identity"]["canonicalOwnerId"] == "mactuneup"
assert packet["identity"]["skipDecision"]["skipDrafting"]
assert not packet["identity"]["skipDecision"]["verifiedDead"]
assert len(packet["blockers"]) == 2
assert packet["safety"]["ownedBrowserTabClosed"]
print(json.dumps({
    "status": "pass-structural-only",
    "sourceSnapshotHashes": checked_hashes,
    "discoverySnapshotHashes": 1,
    "selectedPreviewHashes": 1,
    "claimSourceMappings": len(claims),
    "matrixClaimMappings": len(packet["productMatrix"]),
    "publicMediaEntries": len(media),
    "numericAndInstallerExcerpts": "pass",
    "domFinalUrlsAndTimestamps": "pass",
    "blockedDraftingInvariants": "pass",
    "publicationApproval": False,
}, indent=2))
