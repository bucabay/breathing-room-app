"""Validate retained research structure and provenance, without network or app execution."""
import datetime
import hashlib
import json
from pathlib import Path
import struct

OWNED = Path(__file__).resolve().parent
ROOT = OWNED.parents[3]
packet = json.loads((OWNED / "research.json").read_text())
checks = []

def check(name, condition):
    checks.append({"check": name, "result": "pass" if condition else "fail"})

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

source_ids = {source["id"] for source in packet["sources"]}
claim_ids = {claim["id"] for claim in packet["claims"]}
check("source IDs unique", len(source_ids) == len(packet["sources"]))
check("claim IDs unique", len(claim_ids) == len(packet["claims"]))
check("every claim maps to existing sources and has a check date/scope", all(
    set(claim["sourceIds"]) <= source_ids and claim["sourceIds"]
    and claim["checkedOn"] == "2026-10-21" and claim["conditions"]
    for claim in packet["claims"]))
check("every matrix cell maps to claims", all(set(row["claimIds"]) <= claim_ids and row["claimIds"] for row in packet["productMatrix"]))
check("all sources have exact URL, excerpts and checked date", all(source["url"] and source["excerpts"] and source["checkedOn"] for source in packet["sources"]))
for source in packet["sources"]:
    if source.get("snapshotPath"):
        path = ROOT / source["snapshotPath"]
        check(f"{source['id']}: retained snapshot exists", path.is_file())
        if source.get("sha256"):
            check(f"{source['id']}: snapshot SHA-256 matches", digest(path) == source["sha256"])
        if source.get("textSha256"):
            retained = json.loads(path.read_text())
            check(f"{source['id']}: response-text SHA-256 matches", hashlib.sha256(retained["text"].encode()).hexdigest() == source["textSha256"])
            check(f"{source['id']}: excerpts occur in retained response", all(excerpt in retained["text"] for excerpt in source["excerpts"]))
            check(f"{source['id']}: HTTP 200 and retrieval time retained", retained["status"] == 200 and retained["retrievedAtUtc"] == source["retrievedAtUtc"])

discovery = packet["discovery"]
check("directory snapshot SHA-256 matches", digest(ROOT / discovery["snapshotPath"]) == discovery["sha256"])
baseline = json.loads((ROOT / "docs/content/verification/batch-1.json").read_text())

def locate(value):
    if isinstance(value, dict):
        if value.get("id") == "app-eraser":
            return value
        for child in value.values():
            found = locate(child)
            if found:
                return found
    elif isinstance(value, list):
        for child in value:
            found = locate(child)
            if found:
                return found
    return None

record = locate(baseline)
check("baseline reused identity matches current packet", record["officialUrl"] == packet["identity"]["homepage"])
manifest = locate(json.loads((ROOT / "docs/content/competitors.json").read_text()))
check("discovery edges match existing manifest", all(
    any(edge["edgeUrl"] == original["edgeUrl"] and edge["retrievedAtUtc"] == original["retrievedAt"] for original in manifest["edges"])
    for edge in discovery["edges"]))
visual = packet["visuals"][1]
image = ROOT / visual["originalPath"]
check("Breathing Room original SHA-256 matches", digest(image) == visual["originalSha256"])
data = image.read_bytes()
check("Breathing Room PNG dimensions match", data[:8] == b"\x89PNG\r\n\x1a\n" and struct.unpack(">II", data[16:24]) == (visual["widthPx"], visual["heightPx"]))
check("example-data/native limitations preserved", "Example data only" in visual["caption"] and "not a native scan" in visual["caption"])
check("competitor image not misrepresented as cleared/downloaded", packet["visuals"][0]["reuse"]["status"] == "link-only" and packet["visuals"][0]["originalPath"] is None and packet["visuals"][0]["originalSha256"] is None)
check("critical gaps block drafting and publication", packet["status"] == "blocked" and not packet["draftingAllowed"] and not packet["publicationAllowed"] and any(b["critical"] for b in packet["blockers"]))
check("identity and alias skip decision present", packet["identity"]["canonicalOwnerId"] == "app-eraser" and packet["identity"]["skipDecision"]["skip"] is False)
check("distinct workflow and comparison briefs", packet["briefs"]["workflow"]["intent"] != packet["briefs"]["comparison"]["intent"] and packet["briefs"]["workflow"]["slug"] != packet["briefs"]["comparison"]["slug"])
check("human-readable packet exists", (OWNED / "research.md").stat().st_size > 0)
result = {
    "jobId": "research-app-eraser",
    "validatedAtUtc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "command": "python3 docs/content/competitors/app-eraser/validate-packet.py",
    "checks": checks,
    "passed": sum(c["result"] == "pass" for c in checks),
    "failed": sum(c["result"] == "fail" for c in checks),
    "artifactSha256": {str(path.relative_to(ROOT)): digest(path) for path in sorted(OWNED.rglob("*")) if path.is_file() and path.name != "validation.json"},
    "limitations": "Structural/provenance checks only. Does not clear licensing, substitute for image inspection, establish runtime behavior or approve publication. No site changes/build/tests or browser QA."
}
(OWNED / "validation.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
raise SystemExit(1 if result["failed"] else 0)
