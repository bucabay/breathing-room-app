"""Offline evidence/packet validation. Does not certify product runtime or publication."""
import datetime
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).parent
APP = ROOT.parents[3]
p = json.loads((ROOT / "research.json").read_text())
checks = []


def check(name, outcome):
    checks.append(dict(name=name, passed=bool(outcome)))
    assert outcome, name


def resolve(path):
    path = Path(path)
    return path if path.is_absolute() else ROOT / path


texts = {}
for s in p["sources"]:
    path = resolve(s["snapshotPath"])
    check(f"source-hash:{s['id']}", hashlib.sha256(path.read_bytes()).hexdigest() == s["snapshotSha256"])
    d = json.loads(path.read_text()) if path.suffix == ".json" else None
    texts[s["id"]] = d["text"] if d else path.read_text()
    if s.get("rawSnapshotPath"):
        check(f"raw-hash:{s['id']}", hashlib.sha256(resolve(s["rawSnapshotPath"]).read_bytes()).hexdigest() == s["rawSnapshotSha256"])
for c in p["claims"]:
    check(f"exact-normalized-excerpt:{c['id']}", all(" ".join(c["excerpt"].split()) in " ".join(texts[s].split()) for s in c["sourceIds"]))
    check(f"claim-scope:{c['id']}", c["checkedOn"] == "2026-10-21" and c["sourceUrl"].startswith("https://") and c["conditions"])
ids = {c["id"] for c in p["claims"]} | {u["id"] for u in p["unknowns"]}
check("matrix-reference-integrity", all(ref in ids for row in p["productMatrix"] for key in ["cleanerOnePro", "breathingRoom"] for ref in row[key]))
check("canonical-alias-decision", p["identity"]["canonicalOwnerId"] == "cleaner-one-pro-mac" and p["identity"]["aliases"][0]["skipSeparateDraft"] and not p["identity"]["skip"])
check("baseline-hash", p["reusedVerification"]["baselineSha256Matches"])
d = p["discovery"]
check("discovery-hash", hashlib.sha256((APP / d["snapshotPath"]).read_bytes()).hexdigest() == d["snapshotSha256"])
check("discovery-edge", d["edges"][0]["edgeUrl"] == "https://alternativeto.net/software/cleanmymac/?p=3")
v, br = p["visuals"]
check("competitor-link-only-no-download", v["reuse"]["status"] == "link-only" and not v["downloaded"] and v["originalSha256"] is None and v["publishedPath"] is None)
check("competitor-image-is-official-page-asset", v["assetUrl"].removeprefix("https://cleanerone.trendmicro.com") in texts["mac-product"] or v["assetUrl"].removeprefix("https://cleanerone.trendmicro.com") in (ROOT / "sources/mac-product.html").read_text())
check("br-original-hash", hashlib.sha256(Path(br["originalPath"]).read_bytes()).hexdigest() == br["originalSha256"])
check("br-example-labels", br["dataMode"] == "example" and len(br["requiredLabels"]) == 2 and "not a native scan" in br["caption"])
check("blocked-not-published", p["status"] == "blocked" and p["draftingGate"]["status"] == "blocked" and not p["published"])
check("critical-unknown-mapped", any(u["id"] == "visual-rights" and u["critical"] for u in p["unknowns"]))
check("distinct-brief-intents", p["workflowBrief"]["primaryIntent"] != p["comparisonBrief"]["primaryIntent"] and p["workflowBrief"]["slug"] != p["comparisonBrief"]["slug"])
check("markdown-handoff", all(x in (ROOT / "research.md").read_text() for x in ["drafting blocked", "Locale=ru-ru", "link-only", "Python", "Trend Cleaner Pro"]))
artifacts = {str(f.relative_to(ROOT)): hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(ROOT.rglob("*")) if f.is_file() and f.name != "validation.json"}
result = dict(checkedAtUtc=datetime.datetime.now(datetime.timezone.utc).isoformat(), status="passed-structural-evidence-checks", checks=checks, passed=len(checks), failed=0,
              artifactsSha256=artifacts, limitations=["No competitor/native execution, deletion, benchmark or installer verification.", "Competitor screenshot rights unresolved: drafting remains blocked despite structural check pass.", "No site edits; no site build/test or independent publication/visual score claimed."])
(ROOT / "validation.json").write_text(json.dumps(result, indent=2) + "\n")
print(f"PASS: {len(checks)} checks; {len(artifacts)} artifact hashes. Drafting remains BLOCKED: competitor image rights.")
