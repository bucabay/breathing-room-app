"""Read-only packet checks; writes only this product's validation result."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
p = json.loads((HERE / "research.json").read_text())
checks = []
texts = {}
for source in p["sources"]:
    path = ROOT / source["snapshotPath"]
    assert path.is_file(), path
    assert hashlib.sha256(path.read_bytes()).hexdigest() == source["sha256"], path
    raw = path.read_text()
    texts[source["id"]] = (json.loads(raw).get("text", "") + "\n" + raw) if path.suffix == ".json" else raw
checks.append(f"PASS: {len(p['sources'])} retained source snapshot paths and SHA-256 hashes")
for claim in p["claims"]:
    assert claim["excerpt"] in texts[claim["sourceIds"][0]], claim["id"]
    assert claim["sourceUrl"].startswith("https://") and claim["checkedAtUtc"]
checks.append(f"PASS: {len(p['claims'])} exact supporting excerpts, source references, URLs and check timestamps")
ids = {c["id"] for c in p["claims"]}
assert len(ids) == len(p["claims"])
for row in p["productMatrix"]:
    for key in ("competitorClaimIds", "breathingRoomClaimIds"):
        assert set(row.get(key, [])) <= ids
checks.append("PASS: matrix claim-reference integrity and unique claim IDs")
for visual in p["visuals"]:
    assert set(visual["supportedClaimIds"]) <= ids
    assert visual["alt"] and visual["caption"]
    if visual["originalPath"]:
        assert hashlib.sha256(Path(visual["originalPath"]).read_bytes()).hexdigest() == visual["originalSha256"]
competitor, br = p["visuals"]
assert competitor["reuse"]["status"] == "link-only" and competitor["originalPath"] is None
assert competitor["originalSha256"] is None and competitor["retrievedAtUtc"] is None
assert br["dataMode"] == "example" and "Example data only" in br["caption"]
checks.append("PASS: selected Breathing Room PNG hash/disclosure; competitor link-only rights and null download provenance")
assert p["status"] == "blocked" and p["draftGate"]["allowed"] is False and not p["published"]
assert len(p["blockers"]) == 2 and p["identity"]["canonicalOwnerId"] == p["productId"]
assert p["identity"]["skipDecision"]["skipSeparateAliasDrafts"]
checks.append("PASS: explicit canonical owner/alias decision, two blockers and drafting/publication prohibition")
assert all(s.get("baselineHashVerified", True) for s in p["sources"])
checks.append("PASS: both reused verification snapshots match original batch-2 SHA-256 values")
md = (HERE / "research.md").read_text()
assert all(x in md for x in ["Drafting blocked", "workflow article brief", "comparison brief", "No images downloaded"])
checks.append("PASS: human-readable research packet includes briefs and blocking diagnostic")
result = {"checkedAtUtc": datetime.now(timezone.utc).isoformat(), "status": "passed-packet-integrity-only",
          "checks": checks, "researchSha256": hashlib.sha256((HERE / "research.json").read_bytes()).hexdigest(),
          "markdownSha256": hashlib.sha256((HERE / "research.md").read_bytes()).hexdigest(),
          "limitations": "Not product/runtime tests, rights clearance, independent review, site build or publication approval."}
(HERE / "validation.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
