"""Read-only packet checks; never imports or executes competitor code."""
import hashlib
import json
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
FOLDER = Path(__file__).resolve().parent
packet = json.loads((FOLDER / "research.json").read_text())
retrievals = json.loads((FOLDER / "retrievals.json").read_text())
checks = []

def check(condition, description):
    if not condition:
        raise AssertionError(description)
    checks.append(description)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

by_id = {r["id"]: r for r in retrievals}
sources = {s["id"]: s for s in packet["sourceLedger"]}
claims = {c["id"]: c for c in packet["claimLedger"]}
check(len(sources) == len(packet["sourceLedger"]), "Unique source IDs")
check(len(claims) == len(packet["claimLedger"]), "Unique claim IDs")
for item in retrievals:
    path = ROOT / item["snapshotPath"]
    check(sha(path) == item["sha256"], f"Original hash verified: {path.name}")
for source in sources.values():
    if "retrievalId" in source:
        r = by_id[source["retrievalId"]]
        check(source["url"] == r["sourceUrl"], f"Retrieval URL mapping: {source['id']}")
    if "snapshotPath" in source:
        check((ROOT / source["snapshotPath"]).is_file(), f"Source snapshot exists: {source['id']}")
    if "sha256" in source:
        check(sha(ROOT / source["snapshotPath"]) == source["sha256"], f"Reused source hash: {source['id']}")
for claim in claims.values():
    check(bool(claim["sourceIds"]) and all(s in sources for s in claim["sourceIds"]), f"Claim sources resolve: {claim['id']}")
    check(bool(claim["excerpt"]) and bool(claim["checkedDate"]) and bool(claim["evidenceClass"]), f"Claim evidence fields: {claim['id']}")
for row in packet["matrix"]:
    for field in ["claimIds", "breathingRoomClaimIds"]:
        check(all(c in claims for c in row.get(field, [])), f"Matrix {field} resolve: {row['dimension']}")
for visual in packet["visuals"]:
    path = ROOT / visual["originalPath"]
    check(sha(path) == visual["originalSha256"], f"Visual original hash: {visual['id']}")
    data = path.read_bytes()
    check(data[:8] == b"\x89PNG\r\n\x1a\n", f"PNG signature: {visual['id']}")
    dims = struct.unpack(">II", data[16:24])
    check(dims == (visual["widthPx"], visual["heightPx"]), f"PNG dimensions {dims}: {visual['id']}")
    check(bool(visual["caption"]) and bool(visual["alt"]) and bool(visual["reuse"]["basis"]), f"Visual disclosure and reuse fields: {visual['id']}")
    check(visual["publishedPath"] is None and visual["publishedSha256"] is None, f"No invented published derivative: {visual['id']}")
discovery = packet["discovery"]
for path_field, hash_field in [("snapshotPath", "sha256"), ("edgeSnapshotPath", "edgeSha256")]:
    check(sha(ROOT / discovery[path_field]) == discovery[hash_field], f"Discovery hash: {path_field}")
release = json.loads((FOLDER / "release-latest.json").read_text())
check(release["tag_name"] == "v1.6.0" and not release["draft"] and not release["prerelease"], "Official latest release is v1.6.0 non-draft/non-prerelease")
check({"mac-cleanup-go_1.6.0_darwin_amd64.tar.gz", "mac-cleanup-go_1.6.0_darwin_arm64.tar.gz"}.issubset({a["name"] for a in release["assets"]}), "Both Darwin architecture archive names present")
license_text = (FOLDER / "LICENSE-v1.6.0.txt").read_text()
check("associated documentation files" in license_text and "free of charge" in license_text and "copyright notice and this permission notice" in license_text, "MIT scope, no-fee grant and notice condition retained")
readme = (FOLDER / "readme-v1.6.0.md").read_text()
check("Targets (as of v1.3.6)" in readme and "Risky categories are unselected by default" in readme, "README count-version and risky-default caveats supported")
check(packet["identity"]["canonicalOwnerId"] == "mac-cleanup-go" and not packet["identity"]["aliasSkipDecision"]["skip"], "Canonical ownership and explicit no-skip decision recorded")
check(not packet["gates"]["publicationApproved"], "No publication approval inferred")
print(json.dumps({"status": "passed", "checksPassed": len(checks), "checks": checks, "limitations": ["Structural and retained-evidence integrity checks only; not native tests, independent editorial review, screenshot rights legal audit or site build.", "Actual PNGs were opened separately using the image read tool."]}, indent=2))
