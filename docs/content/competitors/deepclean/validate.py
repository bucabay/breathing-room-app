"""Validate this research packet without network, app execution or site mutation."""
import datetime
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
APP = ROOT.parents[3]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalized(text):
    return re.sub(r"\s+", " ", text.replace("**", "")).strip()


def main():
    packet = json.loads((ROOT / "research.json").read_text())
    archives = json.loads((ROOT / "sources/retrievals.json").read_text())
    checks = []
    provenance = []
    texts = {}
    for source in packet["sources"]:
        record = dict(source)
        if "archiveRecord" in source:
            archive = next(a for a in archives if a["id"] == source["id"])
            path = ROOT / archive["snapshotPath"]
            assert sha(path) == archive["sha256"], source["id"]
            record.update(archive)
            texts[source["id"]] = (ROOT / archive["textPath"]).read_text()
            checks.append(source["id"] + ": original HTML SHA-256 matches retrieval register")
        elif "snapshotPath" in source:
            path = APP / source["snapshotPath"]
            if not path.exists():
                path = ROOT / source["snapshotPath"]
            record["retainedFileSha256"] = sha(path)
            if "sha256" in source:
                assert record["retainedFileSha256"] == source["sha256"]
            if source["id"].startswith("baseline-"):
                original = json.loads(path.read_text())
                record["retrievedAtUtc"] = original["retrievedAt"]
                texts[source["id"]] = original["text"]
            elif source["id"] == "br-capabilities":
                texts[source["id"]] = path.read_text()
        provenance.append(record)
    discovery = APP / packet["discovery"]["snapshotPath"]
    provenance.append({"id": "discovery-snapshot", "path": str(discovery.relative_to(APP)), "sha256": sha(discovery)})
    count = 0
    for claim in packet["claims"]:
        assert all(s in {x["id"] for x in packet["sources"]} for s in claim["sourceIds"])
        for key in ("excerpt", "supportingExcerpt", "conflictingExcerpt"):
            if key in claim:
                assert any(normalized(claim[key]) in normalized(texts.get(s, "")) for s in claim["sourceIds"]), (claim["id"], key)
                count += 1
    checks.append(f"{len(packet['claims'])} claim source mappings and {count} supporting/conflicting excerpts matched retained source text; whitespace/Markdown emphasis normalized")
    visual = packet["visuals"][1]
    assert sha(APP / visual["originalPath"]) == visual["originalSha256"]
    checks.append("Selected current-source Breathing Room Space PNG SHA-256 matches screenshot library")
    visual_meta = (ROOT / "sources/listing-visual-dom.json").read_text()
    assert packet["visuals"][0]["assetUrl"] in visual_meta
    checks.append("Exact DeepClean Developer Tools asset URL present in retained live DOM metadata; no download/license inferred")
    assert packet["draftingAllowed"] is False and packet["status"] == "blocked"
    assert packet["identity"]["canonicalOwnerId"] == "deepclean"
    assert packet["visuals"][0]["reuse"]["status"] == "link-only"
    assert packet["visuals"][0]["originalSha256"] is None
    checks.append("Blocked drafting, canonical owner and link-only/no-downloaded-asset guards consistent")
    assert "Example data only" in visual["caption"]
    assert "not a native scan" in visual["caption"]
    checks.append("Required example-data/non-native caption labels retained")
    (ROOT / "source-provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")
    for path in ROOT.rglob("*.json"):
        json.loads(path.read_text())
    checks.append("All existing owned JSON files parse")
    result = {
        "checkedAtUtc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "command": "python3 docs/content/competitors/deepclean/validate.py",
        "outcome": "passed-structural-evidence-checks; drafting-still-blocked",
        "checks": checks,
        "artifactHashes": {str(p.relative_to(ROOT)): sha(p) for p in ROOT.rglob("*") if p.is_file() and p.name != "validation.json"},
        "notPerformed": ["native tests", "installer/image download", "cleanup", "permission request", "site check/build/test", "rendered-page QA", "independent review"]
    }
    (ROOT / "validation.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
