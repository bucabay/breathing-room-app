"""Validate this excluded-product packet; never touch queue or site state."""
import hashlib
import html
import json
import pathlib
import re

root = pathlib.Path(__file__).resolve().parent
app = root.parents[3]
packet = json.loads((root / "research.json").read_text())
checks = []


def check(name, condition):
    checks.append({"check": name, "passed": bool(condition)})


check("correct job and canonical owner", packet["jobId"] == "research-cleanup-phone-storage-cleaner"
      and packet["canonicalOwnerId"] == "cleanup-phone-storage-cleaner")
check("explicit skip and no drafting/publication", packet["eligibility"]["decision"] == "skip"
      and not packet["eligibility"]["draftingAllowed"] and not packet["eligibility"]["publicationEligible"])
claim_ids = {c["id"] for c in packet["claims"]}
source_ids = {s["id"] for s in packet["sources"]}
check("all claims have dates, excerpts, source URLs and valid source IDs",
      all(c.get("checkedDate") and c.get("excerpt") and c.get("sourceUrl")
          and c["sourceId"] in source_ids for c in packet["claims"]))
check("matrix claim references resolve", all(set(row["claimIds"]) <= claim_ids for row in packet["matrix"]))
for source in packet["sources"]:
    if "snapshotPath" in source:
        path = pathlib.Path(source["snapshotPath"])
        path = app / path if source.get("reused") else root / path
        check("source hash " + source["id"], hashlib.sha256(path.read_bytes()).hexdigest() == source["sha256"])
discovery = packet["discovery"]
check("reused discovery hash", hashlib.sha256((app / discovery["rawCapture"]).read_bytes()).hexdigest() == discovery["sha256"])
apple = html.unescape((root / "sources/apple.html").read_text())
text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", apple))
for excerpt in ["Only for iPhone", "Requires iOS 15.0 or later.", "DEEP FLOW SOFTWARE SERVICES",
                "6.24.0", "2026-10-12", "Data Used to Track You", "$5.95", "$7.39", "$7.99", "$9.99", "$11.99"]:
    check("retained Apple evidence: " + excerpt, excerpt in apple or excerpt in text)
for visual in packet["visuals"]:
    if visual["productId"] == "cleanup-phone-storage-cleaner":
        source = root / "sources" / ("apple.html" if visual["sourceId"] == "apple" else "product-site.html")
        check("public source contains exact asset URL: " + visual["id"], visual["assetUrl"] in html.unescape(source.read_text()))
        check("uncleared visual remains link-only: " + visual["id"], visual["reuse"]["status"] == "link-only"
              and visual["originalPath"] is None and visual["originalSha256"] is None)
    else:
        check("first-party preview original hash", hashlib.sha256((app / visual["originalPath"]).read_bytes()).hexdigest() == visual["originalSha256"])
        check("first-party caption labels example/native limitations", "Example data only" in visual["caption"]
              and "not a native scan" in visual["caption"])
check("no image downloaded into owned folder", not any(p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"} for p in root.rglob("*")))
report = {"status": "passed" if all(c["passed"] for c in checks) else "failed", "checks": checks,
          "limits": "Structural/source-byte checks only; no runtime, image-rights clearance, site build or independent publication review."}
(root / "validation.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
raise SystemExit(0 if report["status"] == "passed" else 1)
