"""Offline checks of this research packet. Does not execute retained vendor code."""
import hashlib
import json
import struct
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP = ROOT.parents[3]
checks = []


def check(name, condition):
    checks.append({"check": name, "outcome": "pass" if condition else "fail"})


packet = json.loads((ROOT / "research.json").read_text())
ledger = json.loads((ROOT / "source-ledger.json").read_text())
check("Research JSON and source ledger parse; expected task and blocked status", packet["jobId"] == "research-backapp" and packet["status"] == "blocked")
check("Ten retained official sources with unique IDs", len(ledger) == len({s["id"] for s in ledger}) == 10)
for source in ledger + packet["reusedSources"]:
    path = APP / source["snapshotPath"]
    check("Retained source SHA-256: " + source["id"], path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == source["sha256"])
for prefix in ("", "edge"):
    obj = packet["discovery"]
    pathkey, hashkey = ("snapshotPath", "sha256") if not prefix else ("edgeSnapshotPath", "edgeSha256")
    check("Discovery snapshot hash: " + (prefix or "listing"), hashlib.sha256((APP / obj[pathkey]).read_bytes()).hexdigest() == obj[hashkey])
check("Baseline verification hash retained", hashlib.sha256((APP / packet["baselineReuse"]["path"]).read_bytes()).hexdigest() == packet["baselineReuse"]["sha256"])
source_ids = {s["id"] for s in ledger + packet["reusedSources"]}
claim_ids = {c["id"] for c in packet["claims"]}
check("All claims point to known source IDs and carry wording/excerpt/locator/state", all(set(c["sourceIds"]) <= source_ids and all(c.get(k) for k in ("wording", "excerpt", "locator", "state")) for c in packet["claims"]))
check("Claim date/reviewer defaults present", packet["claimDefaults"]["checkedOn"] == "2026-10-21" and bool(packet["claimDefaults"]["reviewer"]))
check("All comparison matrix claim links resolve", all(set(row["backappClaimIds"] + row["breathingRoomClaimIds"]) <= claim_ids for row in packet["productMatrix"]))
for visual in packet["visuals"]:
    data = (APP / visual["originalPath"]).read_bytes()
    check("PNG hash and dimensions: " + visual["id"], hashlib.sha256(data).hexdigest() == visual["originalSha256"] and data[:8] == b"\x89PNG\r\n\x1a\n" and struct.unpack(">II", data[16:24]) == (visual["widthPx"], visual["heightPx"]))
    check("Visual caption, alt, permission basis and unmodified original: " + visual["id"], bool(visual["caption"] and visual["alt"] and visual["reuse"]["basis"]) and not visual["edits"] and visual["publishedPath"] is None)
check("MIT copyright, documentation grant and notice condition retained", all(t in (ROOT / "sources/LICENSE.txt").read_text() for t in ("Copyright (c) 2026 Markus Lind", "associated documentation files", "permission notice shall be included")))
check("Both main and v1.0.0 source targets say 26.2 twice", all((ROOT / "sources" / f).read_text().count("MACOSX_DEPLOYMENT_TARGET = 26.2;") == 2 for f in ("project.pbxproj", "project-v1.0.0.pbxproj")))
release = json.loads((ROOT / "sources/release.json").read_text())
check("Stable release tag and asset version agree with cask", release["tag_name"] == "v1.0.0" and not release["draft"] and not release["prerelease"] and 'version "1.0.0"' in (ROOT / "sources/backapp.rb").read_text() and release["assets"][0]["name"] == "BackApp-1.0.0-macos.zip")
check("Reported release digest equals cask; not a binary checksum test", release["assets"][0]["digest"].removeprefix("sha256:") in (ROOT / "sources/backapp.rb").read_text())
check("Adjacent canonical owner and explicit alias/skip decisions", packet["identity"]["classification"] == "adjacent" and packet["identity"]["canonicalOwnerId"] == "backapp" and packet["identity"]["aliasSkipDecision"] == "do-not-skip-as-alias" and packet["identity"]["skipDecision"]["skip"] is False)
check("Critical missing OS evidence blocks drafting", any(u["critical"] and u["field"] == "compiled minimum macOS" for u in packet["unknowns"]) and packet["gates"]["drafting"].startswith("blocked"))
check("Distinct workflow and comparison briefs present", all(packet["briefs"][k].get("primaryIntent") for k in ("workflow", "comparison")) and packet["briefs"]["workflow"]["slug"] != packet["briefs"]["comparison"]["slug"])
passed = all(c["outcome"] == "pass" for c in checks)
result = {
    "jobId": "research-backapp", "validatedAtUtc": datetime.now(timezone.utc).isoformat(),
    "command": "python3 docs/content/competitors/backapp/validate.py",
    "outcome": "pass" if passed else "fail", "checks": checks,
    "limitations": "Offline JSON/reference/hash/header/evidence consistency checks only. Both PNGs separately opened and read with image tool. No vendor code, native app, installer, website build, network or independent publication review run by this validator.",
    "artifactHashes": {str(p.relative_to(APP)): hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT / "research.json", ROOT / "research.md", ROOT / "source-ledger.json")}
}
(ROOT / "validation.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
raise SystemExit(0 if passed else 1)
