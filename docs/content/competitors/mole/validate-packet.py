"""Validate retained research evidence and write this retry's blocked receipt."""
import datetime
import hashlib
import json
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
packet = json.loads((OUT / "research.json").read_text())
checks = []


def check(label, condition):
    assert condition, label
    checks.append({"check": label, "result": "pass"})


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


check("JSON parses; canonical mole; research remains blocked and unpublished",
      packet["canonicalOwnerId"] == "mole" and packet["status"] == "blocked"
      and packet["stage"] == "research" and packet["published"] is False)
claims = {c["id"]: c for c in packet["claims"]}
sources = {s["id"]: s for s in packet["sources"]}
check("30 unique claim IDs with URLs/excerpts/dates/scopes and resolving source IDs",
      len(claims) == len(packet["claims"]) == 30
      and all(c["sourceUrl"] and c["excerpt"] and c["checkedOn"] and c["scope"]
              and all(s in sources for s in c["sourceIds"]) for c in claims.values()))
check("All matrix claim references resolve",
      all(cid in claims for row in packet["matrix"] for cid in row["claimIds"]))
check("17 source snapshots exist and match SHA-256",
      len(sources) == 17 and all(digest(ROOT / s["snapshotPath"]) == s["sha256"]
                                for s in sources.values()))
batch = json.loads((ROOT / "docs/content/verification/batch-1.json").read_text())
# Locate the reused record without assuming a batch root field name.
def find_mole(value):
    if isinstance(value, dict):
        if value.get("id") == "mole" and "facts" in value:
            return value
        for item in value.values():
            found = find_mole(item)
            if found:
                return found
    elif isinstance(value, list):
        for item in value:
            found = find_mole(item)
            if found:
                return found
    return None


record = find_mole(batch)
check("Existing batch-1 homepage/repository verification reused without changing hashes",
      record is not None and all(any(s["sha256"] == old["sha256"] for s in sources.values())
                                 for old in record["sources"]))
br = next(v for v in packet["visuals"] if v["productId"] == "breathing-room")
image = (ROOT / br["originalPath"]).read_bytes()
check("Selected Breathing Room PNG hash, dimensions and example/native labels retained",
      hashlib.sha256(image).hexdigest() == br["originalSha256"]
      and struct.unpack(">II", image[16:24]) == (2940, 3468)
      and "Example data only" in br["requiredLabels"]
      and "not a native scan" in br["caption"].lower())
visuals = [v for v in packet["visuals"] if v["productId"] == "mole"]
check("Both competitor asset candidates remain link-only with no invented downloaded hashes",
      len(visuals) == 2 and all(v["reuse"]["status"] == "link-only"
                               and v["originalPath"] is None and v["originalSha256"] is None
                               and v["retrievedAtUtc"] is None for v in visuals))
check("No competitor raster assets downloaded into owned folder",
      not any(p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".gif"}
              for p in OUT.rglob("*") if p.is_file()))
check("Exact CLI candidate blob and pinned README reference match retained tree/source",
      next(v for v in visuals if v["id"] == "mole-cli-official-candidate")["upstreamGitBlobSha1"]
      == "5b7e0bea82ad2d298a34fc44655634782b4e5b14"
      and 'src="./docs/img/big-mole.png"' in (OUT / "sources/cli-README.md").read_text())
md = (OUT / "research.md").read_text()
check("Both distinct briefs, CLI-only alternative and precise unresolved gate documented",
      all(s in md for s in ["Explicitly requested retry", "Exact evidence/decision needed",
                           "CLI-only brief option", "Distinct workflow article brief",
                           "Concise comparison brief", "Drafting remains blocked."])
      and packet["blockers"] and packet["retryInvestigation"]["neededEvidenceOrDecision"])
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
artifacts = [{"path": str(p.relative_to(ROOT)), "sha256": digest(p)}
             for p in sorted(OUT.rglob("*")) if p.is_file() and p.name != "validation.json"]
report = {"jobId": "research-mole", "checkedAtUtc": now,
          "status": "passed-research-structure-not-drafting-approval", "checks": checks,
          "artifacts": artifacts,
          "notRun": ["third-party CLI execution or installation", "native execution/cleanup",
                     "competitor image download/visual approval", "browser responsive QA",
                     "marketing builds (no site edits)", "independent publication review"]}
(OUT / "validation.json").write_text(json.dumps(report, indent=2) + "\n")
receipt = {
    "jobId": "research-mole", "status": "blocked",
    "artifacts": [str(OUT / n) for n in ("research.json", "research.md", "validation.json",
                                         "build-packet.py", "validate-packet.py", "sources")],
    "validation": ["build-packet.py PASS: 30 excerpts matched, 17 sources, selected preview hash matched",
                   f"validate-packet.py PASS: {len(checks)} structural/provenance/rights-gate checks",
                   "command -v mo and command -v mole: no path, shell exit 1; neither CLI executed",
                   "No website edits/builds, competitor image downloads, software installs or cleanup"],
    "diagnostic": "Retry reused verified packet. Official pinned CLI README references big-mole.png, but image-specific licence scope is unresolved; code GPL is not assumed to license images. Neither CLI on PATH. Inspected --help startup invokes temp preparation with guarded pruning and exit cleanup, so a genuine non-mutating capture was not established; no third-party code executed. Drafting remains blocked pending exact asset permission plus image inspection, or an audited authorized no-install/no-cleanup genuine CLI capture with output reuse rights. Native reserved-rights image not re-downloaded."
}
receipt_path = ROOT / "docs/content/.runtime/research-mole.1792612292851940000.receipt.json"
receipt_path.write_text(json.dumps(receipt, indent=2) + "\n")
check_receipt = json.loads(receipt_path.read_text())
assert check_receipt["status"] == "blocked"
print(f"PASS: {len(checks)} evidence checks; blocked receipt written and parsed: {receipt_path}")
