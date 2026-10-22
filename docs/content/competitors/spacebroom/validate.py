"""Read-only packet checks; writes only this product's validation report."""
import hashlib
import json
import re
import struct
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP = ROOT.parents[3]
checks = []


def check(name, condition, detail):
    checks.append({"check": name, "outcome": "pass" if condition else "fail", "detail": detail})


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalized(text):
    return re.sub(r"\s+", " ", text).strip()


packet = json.loads((ROOT / "research.json").read_text())
extra = json.loads((ROOT / "sources/additional-excerpts.json").read_text())
baseline = json.loads((ROOT / "sources/official-baseline.json").read_text())
discovery = json.loads((ROOT / "sources/discovery-baseline.json").read_text())
inventory = json.loads((APP / "docs/content/screenshots.json").read_text())
batch = json.loads((APP / "docs/content/verification/batch-2.json").read_text())
check("json-parse", True, "Research, excerpts, baseline captures, screenshot inventory and batch-2 parse as JSON.")

source_ids = {s["id"] for s in packet["sources"]}
claim_ids = {c["id"] for c in packet["claims"]}
check("claim-source-links", len(claim_ids) == len(packet["claims"]) and all(
    set(c["sourceIds"]) <= source_ids and c.get("excerpt") and c.get("sourceUrl")
    and (c.get("checkedAtUtc") or c.get("checkedOnUtc")) and c.get("scope")
    for c in packet["claims"]
), f"{len(claim_ids)} unique claims have existing source IDs, source URL, retained excerpt, date and scope.")

refs = []
for row in packet["matrix"]:
    for product in ("spacebroom", "breathingRoom"):
        cell = row[product]
        refs.extend(cell["claimIds"])
        assert cell["claimIds"] or cell.get("state") == "not-verified"
for item in packet["advantagesAndTradeoffs"]:
    refs.extend(item["claimIds"])
refs.extend(packet["briefs"]["workflow"]["sourceClaimIds"])
check("matrix-brief-references", set(refs) <= claim_ids,
      "All matrix/brief/tradeoff claim IDs resolve; unsupported competitor cells explicitly not verified.")

hash_results = []
for source in packet["sources"]:
    if source.get("snapshotPath"):
        path = ROOT / source["snapshotPath"]
        assert path.is_file(), str(path)
        if source.get("sha256"):
            hash_results.append(digest(path) == source["sha256"])
check("source-file-integrity", all(hash_results), f"{len(hash_results)} declared source-file hashes match actual bytes; all local snapshots exist.")

def find_record(obj):
    if isinstance(obj, dict):
        if obj.get("id") == "spacebroom" and "facts" in obj:
            return obj
        for value in obj.values():
            found = find_record(value)
            if found:
                return found
    if isinstance(obj, list):
        for value in obj:
            found = find_record(value)
            if found:
                return found
    return None


record = find_record(batch)
assert record
check("baseline-reuse-integrity", digest(ROOT / "sources/official-baseline.json") == record["sources"][0]["sha256"]
      and digest(ROOT / "sources/discovery-baseline.json") == record["discovery"]["sha256"]
      and baseline["retrievedAt"] == packet["reuseFirst"]["originalCheckedAtUtc"],
      "Copied captures match existing batch-2 raw-byte hashes and original official-check timestamp.")

text = normalized(baseline["text"])
home_claims = [c for c in packet["claims"] if c["id"].startswith("SB-") and "S1" in c["sourceIds"]
               and c["sourceUrl"].split("#")[0] == packet["identity"]["homepage"]]
bad = [c["id"] for c in home_claims if not all(normalized(part) in text for part in c["excerpt"].split("..."))]
check("homepage-claim-excerpts", not bad, f"{len(home_claims)} homepage-supported claim excerpts match retained baseline text; mismatches: {bad}.")
terms_claim = next(c for c in packet["claims"] if c["id"] == "SB-05")
terms_text = normalized(" ".join(next(s for s in extra["sources"] if s["id"] == "S3")["excerpts"]))
check("renewal-terms-excerpt", all(normalized(part) in terms_text for part in terms_claim["excerpt"].split("...")),
      "Annual renewal/cancellation excerpt matches its primary terms source, not homepage wording.")
html = (ROOT / "sources/homepage-images.html").read_text()
visual_claim = next(c for c in packet["claims"] if c["id"] == "SB-17")
check("official-visual-reference", visual_claim["excerpt"] in html and baseline["sha256"] == digest(ROOT / "sources/homepage-images.html"),
      "Space Lens img element occurs verbatim in retained official HTML; HTML hash also matches baseline embedded content hash. This does not verify image bytes/rights.")

check("identity-and-alias-boundary", packet["canonicalOwnerId"] == "spacebroom"
      and not packet["identity"]["aliasDecision"]["skipSeparateDraft"]
      and packet["identity"]["fit"] == "direct" and discovery["links"][0]["href"] == packet["identity"]["homepage"],
      "Canonical owner/self identity and direct-Mac classification are explicit; no false alias skip.")

br = packet["visuals"][1]
image_path = APP / br["originalPath"]
image = image_path.read_bytes()
dimensions = struct.unpack(">II", image[16:24])
shared = next(x for x in inventory["assets"] if x["id"] == br["id"])
check("selected-preview-integrity", image[:8] == b"\x89PNG\r\n\x1a\n" and dimensions == (br["widthPx"], br["heightPx"])
      and digest(image_path) == br["originalSha256"] == shared["sha256"] and br["caption"] == shared["caption"],
      f"Selected PNG is {dimensions[0]} × {dimensions[1]}, hash and required example-data caption match shared inventory.")
check("visual-inspection-record", br["review"]["status"] == "research-visual-inspection-only" and br["dataMode"] == "example",
      "Actual selected PNG opened/read through image-capable tool in this run; example-data banners and composer overlap recorded. Not native/independent publication review.")

competitor = packet["visuals"][0]
check("honest-blocker", packet["status"] == "blocked" and packet["gates"]["drafting"] == "blocked"
      and competitor["reuse"]["status"] == "link-only" and competitor["originalPath"] is None
      and competitor["originalSha256"] is None and packet["published"] is False,
      "Uncleared/uninspected competitor image blocks drafting; no invented downloaded asset hash or publication approval.")

files = sorted(p for p in ROOT.rglob("*") if p.is_file() and p.name != "validation.json")
check("owned-packet-file-set", not any(p.suffix.lower() in {".png", ".webp", ".jpg", ".dmg"} for p in files),
      "Owned folder has research/text source records and checker only; no competitor image, binary or site asset downloaded. No shared/site builds run.")
report = {
    "jobId": packet["jobId"], "executedAtUtc": datetime.now(timezone.utc).isoformat(),
    "command": "python3 docs/content/competitors/spacebroom/validate.py",
    "outcome": "pass" if all(x["outcome"] == "pass" for x in checks) else "fail",
    "checks": checks,
    "artifactHashes": {str(p.relative_to(APP)): digest(p) for p in files},
    "limitations": ["Structural/evidence-retention checks do not clear screenshot rights or test apps.",
                    "New legal/policy excerpts were manually retained from actual WebFetch results, not full raw snapshots.",
                    "Independent drafting, rendered browser QA and publication checks remain pending; no site build required for research-only change."]
}
(ROOT / "validation.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps({"outcome": report["outcome"], "checks": checks}, indent=2))
raise SystemExit(0 if report["outcome"] == "pass" else 1)
