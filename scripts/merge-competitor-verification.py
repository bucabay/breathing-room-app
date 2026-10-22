#!/usr/bin/env python3
"""Merge complete, source-cited baseline verification batches without approving publication."""
from collections import Counter
import datetime
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "docs/content"


def valid_url(value):
    parsed = urlparse(value)
    return parsed.scheme in ("https", "http") and bool(parsed.netloc) and not parsed.username and not parsed.password


def merge():
    path = CONTENT / "competitors.json"
    manifest = json.loads(path.read_text())
    products = manifest["competitors"]
    records = {}
    for batch, start in ((1, 0), (2, 75)):
        data = json.loads((CONTENT / f"verification/batch-{batch}.json").read_text())
        expected = [product["id"] for product in products[start:start + 75]]
        assert data["inputIds"] == expected, f"Batch {batch}: wrong input ordering/coverage"
        actual = [record["id"] for record in data["records"]]
        assert len(actual) == len(set(actual)) == len(expected) and set(actual) == set(expected), f"Batch {batch}: missing/duplicate outcomes"
        for record in data["records"]:
            assert record["status"] in ("verified", "partial", "blocked")
            if record.get("officialUrl"):
                assert valid_url(record["officialUrl"]), f"Invalid official URL: {record['id']}"
            for fact in record.get("facts", []):
                assert fact.get("field") and "value" in fact and fact.get("excerpt", "").strip()
                assert valid_url(fact.get("sourceUrl", "")), f"Missing source URL: {record['id']}"
                assert datetime.datetime.fromisoformat(fact["retrievedAt"].replace("Z", "+00:00")).tzinfo is not None
            if record["status"] == "verified":
                assert record.get("officialUrl") and record.get("facts"), f"Verified without supporting official facts: {record['id']}"
            records[record["id"]] = record
    assert len(records) == len(products) == 150
    alias_path = CONTENT / "verification/alias-decisions.json"
    decisions = json.loads(alias_path.read_text()) if alias_path.exists() else {"decisions": []}
    aliases = {}
    for decision in decisions["decisions"]:
        assert decision["status"] in ("confirmed-same-product", "distinct-products", "unresolved")
        assert decision["aliasId"] in records and decision["canonicalId"] in records
        if decision["status"] == "confirmed-same-product":
            assert decision.get("excerpt") and valid_url(decision.get("sourceUrl", ""))
            assert decision["aliasId"] != decision["canonicalId"]
            aliases[decision["aliasId"]] = decision["canonicalId"]
    for alias in aliases:
        chain, current = set(), alias
        while current in aliases:
            assert current not in chain, "Alias cycle"
            chain.add(current)
            current = aliases[current]
        aliases[alias] = current
    for product in products:
        record = records[product["id"]]
        product["canonicalProductUrl"] = record.get("officialUrl")
        product["officialName"] = record.get("officialName")
        product["baselineVerification"] = record
        product["verificationStatus"] = f"official-baseline-{record['status']}; independent article approval still required"
        product["publicationEligible"] = False
        product["canonicalOwnerId"] = aliases.get(product["id"], product["id"])
        product["researchEligible"] = product["id"] not in aliases
    counts = dict(Counter(record["status"] for record in records.values()))
    manifest["counts"]["baselineVerification"] = counts
    manifest["counts"]["confirmedAliases"] = len(aliases)
    manifest["counts"]["canonicalResearchTargets"] = len(products) - len(aliases)
    manifest["counts"]["verifiedEligibleProducts"] = 0
    manifest["vendorAliasDecisions"] = decisions["decisions"]
    manifest["vendorAliasDeduplicationComplete"] = not any(decision["status"] == "unresolved" for decision in decisions["decisions"]) and alias_path.exists()
    manifest["status"] = "baseline-verification-complete-with-explicit-outcomes"
    temp = path.with_suffix(".verified.pending.json")
    temp.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    temp.replace(path)
    report = ["# Official-source verification summary", "", f"All150 discovered listing IDs have a recorded baseline verification outcome: {counts}. Confirmed same-product aliases: {len(aliases)}. Canonical research targets: {len(products) - len(aliases)}.", "", "Verified means the cited baseline facts were established, not that every feature was tested, an app was installed, screenshots are cleared, or publication was approved. Partial/blocked records retain exact missing evidence and errors. All publication eligibility remains false pending per-article research and independent review.", "", "| Product | Outcome | Official source | Canonical owner |", "| --- | --- | --- | --- |"]
    for product in products:
        report.append(f"| {product['name']} | {product['baselineVerification']['status']} | {product.get('canonicalProductUrl') or 'not verified'} | {product['canonicalOwnerId']} |")
    (CONTENT / "verification/README.md").write_text("\n".join(report) + "\n")
    print(json.dumps({"baselineOutcomes": counts, "confirmedAliases": len(aliases), "canonicalResearchTargets": len(products) - len(aliases)}))


if __name__ == "__main__":
    merge()
