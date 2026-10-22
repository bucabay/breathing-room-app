"""Read-only evidence checks; writes only this product's validation log."""
import datetime
import hashlib
import json
from pathlib import Path
import struct

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
packet_path = HERE / "research.json"
packet = json.loads(packet_path.read_text())
checks = []


def check(name, condition):
    checks.append({"check": name, "outcome": "pass" if condition else "fail"})
    if not condition:
        raise AssertionError(name)


check("JSON parses and remains blocked, research-only, unpublished",
      packet["status"] == "blocked" and not packet["draftGate"]["ready"]
      and not packet["draftGate"]["publicationEligible"])
sources = {s["id"]: s for s in packet["sources"]}
claims = {c["id"]: c for c in packet["claims"]}
check("Unique source and claim IDs", len(sources) == len(packet["sources"])
      and len(claims) == len(packet["claims"]))
check("Every claim resolves to cited source IDs and a defined evidence state",
      all(c["sourceIds"] and all(s in sources for s in c["sourceIds"])
          and c["state"] in {"verified", "not-verified", "contradicted", "stale"}
          for c in claims.values()))
check("Every brief claim resolves", all(cid in claims for b in packet["briefs"].values()
                                       for cid in b["claimIds"]))
check("Every source retains URL and supporting excerpts", all(
    s.get("url", "").startswith("https://") and s.get("excerpts") for s in sources.values()))
for record in [sources["S1"], packet["discovery"]]:
    path = ROOT / record["snapshotPath"]
    check("Retained snapshot SHA-256: " + record["snapshotPath"],
          hashlib.sha256(path.read_bytes()).hexdigest() == record["sha256"])
baseline = json.loads((ROOT / sources["S1"]["snapshotPath"]).read_text())
check("Homepage excerpts match retained original text",
      all(x in baseline["text"] for x in sources["S1"]["excerpts"]))
batch2 = json.loads((ROOT / "docs/content/verification/batch-2.json").read_text())
check("Batch 2 has no duplicate dusty-storage baseline",
      not any(r.get("id") == "dusty-storage" for r in batch2["records"]))
check("Canonical ownership retained; no alias merge",
      packet["identity"]["canonicalOwnerId"] == "dusty-storage"
      and not packet["identity"]["aliasDecision"]["skipAsAlias"])
for visual in packet["visuals"]:
    if visual["productId"] == "breathing-room":
        data = (ROOT / visual["originalPath"]).read_bytes()
        check("Selected Breathing Room original hash matches",
              hashlib.sha256(data).hexdigest() == visual["originalSha256"])
        check("Selected Breathing Room PNG dimensions match",
              struct.unpack(">II", data[16:24]) == (visual["widthPx"], visual["heightPx"]))
        check("Required example/native disclaimer retained",
              "Example data only; not a native scan" in visual["caption"])
    else:
        check("Uncleared competitor image stays link-only with no invented hash",
              visual["reuse"]["status"] == "link-only"
              and visual["originalPath"] is None and visual["originalSha256"] is None)
check("Exact privacy and safety claims excluded rather than fabricated",
      claims["C12"]["state"] == "contradicted"
      and claims["C13"]["state"] == "not-verified"
      and claims["C14"]["state"] == "not-verified")
report = {
    "checkedAtUtc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "command": "python3 docs/content/competitors/dusty-storage/validate.py",
    "status": "passed-structural-checks-draft-gate-still-blocked",
    "checks": checks,
    "artifactHashes": {name: hashlib.sha256((HERE / name).read_bytes()).hexdigest()
                       for name in ["research.json", "research.md", "validate.py"]},
    "manualChecks": [
        "Read PLAN, EDITORIAL, capabilities, screenshots, retained baseline and alias records.",
        "Five official missing-evidence pages read with WebFetch; selected passages retained and manually compared, not automated full-page validation.",
        "Owned Chrome tab 101 feature-page DOM confirms loaded official image candidate 1920x989 and all-rights-reserved footer; tab closed after read-only inspection.",
        "Actual selected first-party PNG opened and read; disclosures visible and chart overlap noted."
    ],
    "notPerformed": ["competitor image download or full visual review", "native/installer/cleanup tests",
                     "account or payment testing", "independent review", "site edits/build/tests"],
    "blocker": "VISUAL-RIGHTS: no competitor image republication permission established; official link-only fallback does not satisfy on-page image gate."
}
(HERE / "validation.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
