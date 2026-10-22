"""Read-only evidence checks; writes only this packet's validation.json."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
import struct

ROOT = Path(__file__).resolve().parents[4]
OWNED = Path(__file__).resolve().parent
packet = json.loads((OWNED / "research.json").read_text())
results = []


def check(name, condition, detail):
    results.append({"check": name, "passed": bool(condition), "detail": detail})


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


check("ownership", packet["canonicalOwnerId"] == "imymac--cleaner", "Canonical owner is this product, not a guessed cross-vendor alias")
check("blocked-gates", packet["status"] == "blocked" and not packet["draftingAllowed"] and not packet["published"], "No drafting/publication approval while critical evidence is missing")
source_ids = {s["id"] for s in packet["sources"]}
claim_ids = {c["id"] for c in packet["claims"]}
check("unique-ids", len(source_ids) == len(packet["sources"]) and len(claim_ids) == len(packet["claims"]), "No duplicate source or claim IDs")
for claim in packet["claims"]:
    check("claim:" + claim["id"], bool(claim["excerpt"]) and bool(claim["checkedOn"]) and set(claim["sourceIds"]) <= source_ids, "Excerpt/date/source references retained")
for cell in packet["matrix"]:
    check("matrix:" + cell["dimension"], set(cell["claimIds"]) <= claim_ids and (bool(cell["claimIds"]) or cell.get("state") == "not-verified"), "Factual cells reference claims; unknowns explicitly not verified")
for source in packet["sources"]:
    path = ROOT / source["snapshotPath"]
    check("source-exists:" + source["id"], path.is_file(), str(path.relative_to(ROOT)))
    if source.get("sha256"):
        check("source-hash:" + source["id"], sha(path) == source["sha256"], sha(path))
    if source.get("metadataPath"):
        meta = json.loads((ROOT / source["metadataPath"]).read_text())
        text_path = ROOT / meta["textPath"]
        check("metadata:" + source["id"], meta["finalUrl"] == source["finalUrl"] and meta["retrievedAtUtc"] == source["retrievedAtUtc"] and meta["httpStatus"] == 200, "Actual final URL/retrieval timestamp/HTTP result match retained metadata")
        check("text-hash:" + source["id"], sha(text_path) == meta["textSha256"], sha(text_path))

def norm(value):
    return re.sub(r"\s+", " ", value).strip()

guide = norm((OWNED / "sources/guide.txt").read_text())
pricing = norm((OWNED / "sources/pricing.txt").read_text())
for cid in ["modules", "approval", "cache-categories", "menu-monitor", "installation"]:
    claim = next(c for c in packet["claims"] if c["id"] == cid)
    check("exact-guide-excerpt:" + cid, norm(claim["excerpt"]) in guide, "Quoted supporting text occurs in retained official guide")
trial = next(c for c in packet["claims"] if c["id"] == "trial")
check("exact-trial-excerpt", norm(trial["excerpt"]) in pricing, "Literal 500M limit retained without invented units")
html = (OWNED / "sources/pricing.html").read_text()
prices = re.findall(r'license-item-price-now[^>]*>\s*\$(\d+\.\d+)', html)
check("advertised-plan-prices", prices == [o["displayAmount"] for o in packet["pricingDetails"]["offers"]], repr(prices))
check("pricing-conditions", all(s in pricing for s in ["Automatically renew", "Excl. Sales Tax", "One-time purchase"]), "Renewal/tax/lifetime conditions retained")
competitor, preview = packet["visuals"]
guide_html = (OWNED / "sources/guide.html").read_text()
check("official-ui-reference", '/image/imymac/system-junk/select-system-junk-to-clean.png' in guide_html and competitor["assetUrl"].startswith("https://www.imymac.com/"), "Exact competitor app-image path embedded in retained official guide")
check("image-rights-not-waived", competitor["reuse"]["status"] == "link-only" and competitor["originalPath"] is None and competitor["originalSha256"] is None, "No third-party image download, invented hash or invented licence")
asset = ROOT / preview["originalPath"]
check("preview-hash", sha(asset) == preview["originalSha256"], sha(asset))
width, height = struct.unpack(">II", asset.read_bytes()[16:24])
check("preview-dimensions", [width, height] == [preview["widthPx"], preview["heightPx"]], f"{width}x{height}")
inventory = json.loads((ROOT / "docs/content/screenshots.json").read_text())
record = next(a for a in inventory["assets"] if a["id"] == preview["id"])
check("preview-disclosure", preview["caption"] == record["caption"] and preview["originalSha256"] == record["sha256"] and preview["dataMode"] == "example", "Required current-source/example-data/non-native caption and provenance match inventory")
discovery = ROOT / packet["discovery"]["snapshotPath"]
discovery_hash = sha(discovery)
about = json.loads(discovery.read_text())
check("discovery-snapshot", about["url"] == packet["discovery"]["listingUrl"] and about["retrievedAt"] == packet["discovery"]["retrievedAtUtc"], discovery_hash)
check("briefs-and-tradeoffs", all(packet["briefs"][b]["notAnArticle"] for b in ["workflow", "comparison"]) and all(packet["advantagesAndTradeoffs"][k] for k in ["imymacAdvantages", "imymacTradeoffs", "breathingRoomAdvantages", "breathingRoomTradeoffs"]), "Distinct briefs, not drafts; both products' advantages and limitations retained")
report = {"checkedAtUtc": datetime.now(timezone.utc).isoformat(), "command": "python3 docs/content/competitors/imymac--cleaner/validate.py", "scope": "Local documentary integrity only; no browser/native/cleanup test or site build", "passed": all(r["passed"] for r in results), "checkCount": len(results), "results": results, "discoverySha256": discovery_hash, "packetHashes": {name: sha(OWNED / name) for name in ["research.json", "research.md"]}, "blockingEvidenceRemains": packet["gates"]["diagnostic"]}
(OWNED / "validation.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps({"passed": report["passed"], "checkCount": len(results), "failed": [r for r in results if not r["passed"]]}, indent=2))
raise SystemExit(0 if report["passed"] else 1)
