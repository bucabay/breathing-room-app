"""Read-only packet checks; writes only this product's validation report."""
import datetime
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
packet = json.loads((HERE / "research.json").read_text())
checks = []


def check(name, passed):
    checks.append({"check": name, "passed": bool(passed)})


sources = {s["id"]: s for s in packet["sources"]}
check("unique source and claim IDs", len(sources) == len(packet["sources"]) and len({c["id"] for c in packet["claims"]}) == len(packet["claims"]))
for source in sources.values():
    path = ROOT / source["snapshotPath"]
    check("source exists/hash: " + source["id"], path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == source["sha256"])
    source["validationText"] = path.read_text()
    if path.suffix == ".json":
        data = json.loads(path.read_text())
        source["validationText"] = data.get("text", data.get("excerpt", ""))
for c in packet["claims"]:
    check("source refs and URL: " + c["id"], all(s in sources for s in c["sourceIds"]) and c["sourceUrl"] == sources[c["sourceIds"][0]]["url"])
    check("literal excerpt retained: " + c["id"], c["excerpt"] in sources[c["sourceIds"][0]]["validationText"])
    check("claim has scope/date/state: " + c["id"], c["checkedAtUtc"] and c["conditions"] and c["state"] in ["verified", "not-verified", "contradicted", "stale"])
check("canonical owner and no unsupported alias skip", packet["identity"]["canonicalOwnerId"] == "jwizard-cleaner" and packet["identity"]["aliasSkipDecision"]["skip"] is False)
check("blocked state retained", packet["status"] == "blocked" and not packet["draftingAllowed"] and not packet["publicationEligible"] and len(packet["blockers"]) > 0)
competitor, br = packet["visuals"]
check("competitor link-only, no invented asset/hash", competitor["reuse"]["status"] == "link-only" and competitor["originalPath"] is None and competitor["originalSha256"] is None and competitor["assetUrl"].startswith("https://jwizard.com/images/mac/"))
check("Breathing Room original hash", hashlib.sha256(Path(br["originalPath"]).read_bytes()).hexdigest() == br["originalSha256"])
check("example/native labels retained", "Example data only" in br["caption"] and "not a native scan" in br["caption"] and br["dataMode"] == "example")
check("two distinct briefs", packet["briefs"]["workflow"]["slug"] != packet["briefs"]["comparison"]["slug"])
check("markdown handoff exists", (HERE / "research.md").is_file())
report = {"jobId": packet["jobId"], "checkedAtUtc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "checks": checks, "passed": all(c["passed"] for c in checks), "limitations": "Structural/source excerpt checks only; not native tests, rights clearance, independent editorial approval or publication QA."}
(HERE / "validation.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps({"passed": report["passed"], "checks": len(checks), "failed": [c["check"] for c in checks if not c["passed"]]}, indent=2))
raise SystemExit(0 if report["passed"] else 1)
