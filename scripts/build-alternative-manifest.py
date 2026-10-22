#!/usr/bin/env python3
"""Build discovery records from actual rendered AlternativeTo page captures."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "docs/content"
CAPTURES = CONTENT / ".runtime"
SEEDS = {"cleanmymac": ("CleanMyMac", 10, 113), "mole": ("Mole", 9, 101)}


def build():
    products, pages, seed_counts = {}, [], {}
    for seed, (name, last, expected) in SEEDS.items():
        identities = set()
        for number in range(1, last + 1):
            path = CAPTURES / f"{seed}-{number}.json"
            raw = path.read_bytes()
            data = json.loads(raw)
            assert data["url"].split("?")[0] == f"https://alternativeto.net/software/{seed}/"
            assert data["products"], f"Empty/challenged page: {path}"
            if number == last:
                assert data["next"] is None, f"Pagination not exhausted: {seed}"
            else:
                assert any(link["url"] == f"https://alternativeto.net/software/{seed}/?p={number + 1}" for link in data["pagination"])
            unique_on_page = {p["listingUrl"]: p for p in data["products"]}
            pages.append({"seedId": seed, "url": data["url"], "retrievedAt": data["retrievedAt"], "rawCapture": str(path.relative_to(ROOT)), "sha256": hashlib.sha256(raw).hexdigest(), "uniqueListings": len(unique_on_page), "next": data["next"]})
            for url, item in unique_on_page.items():
                identities.add(url)
                record = products.setdefault(url, {"id": url.split("/software/")[1].split("/")[0], "name": item["name"], "listingUrl": url, "canonicalProductUrl": None, "classification": "not-verified", "researchEligible": True, "publicationEligible": False, "verificationStatus": "directory-discovered; official product facts and vendor-level aliases require review", "directoryText": item["directoryText"], "edges": []})
                record["edges"].append({"seedId": seed, "seedUrl": f"https://alternativeto.net/software/{seed}/", "edgeUrl": data["url"], "retrievedAt": data["retrievedAt"], "evidenceType": "live-browser-rendered-listing"})
        assert len(identities) == expected, f"Count mismatch: {seed}: {len(identities)} vs {expected}"
        seed_counts[seed] = len(identities)
    excluded = products.pop("https://alternativeto.net/software/breathing-room/about/")
    ordered = sorted(products.values(), key=lambda p: (0 if p["id"] in SEEDS else 1, 0 if "\nMac\n" in p["directoryText"] else 1, p["name"].casefold()))
    manifest = {
        "schemaVersion": 2, "status": "discovery-complete", "retrievedDate": "2026-10-21", "publicationStatus": "research-only",
        "breathingRoomListing": "https://alternativeto.net/software/breathing-room/about/",
        "breathingRoomAlternatives": "https://alternativeto.net/software/breathing-room/",
        "confirmedRelationships": [{"name": name, "id": seed, "aboutUrl": f"https://alternativeto.net/software/{seed}/about/", "alternativesUrl": f"https://alternativeto.net/software/{seed}/", "evidence": "Live Breathing Room listing states bucabay added Breathing Room as alternative to CleanMyMac and Mole; its alternatives page lists those two."} for seed, (name, _, _) in SEEDS.items()],
        "counts": {"confirmedPublishedRelationships": 2, "seedListings": seed_counts, "retrievedListingPages": len(pages), "uniqueListingIdentitiesIncludingSelf": len(products) + 1, "competitorListingIdentities": len(products), "verifiedEligibleProducts": 0},
        "paginationComplete": True, "listingUrlDeduplicationComplete": True, "vendorAliasDeduplicationComplete": False,
        "limitations": ["150 distinct competitor listing identities are not proof of 150 independent vendors or direct Mac substitutes.", "Directory platform, pricing, feature and discontinuation metadata require official-source verification.", "Possible aliases include PowerMyMac and iMyMac - PowerMyMac; review before assigning distinct posts.", "Raw captures are local/gitignored; the public manifest retains exact page URLs, timestamps, hashes and rendered excerpts."],
        "listingPages": pages, "competitors": ordered, "excludedProducts": [{"id": excluded["id"], "name": excluded["name"], "reason": "Our own product is not a competitor", "edges": excluded["edges"]}],
    }
    (CONTENT / "competitors.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    lines = ["# Competitor research checklist", "", "150 distinct AlternativeTo listing identities from the full CleanMyMac (113) and Mole (101) lists; 19 rendered pages traversed. Breathing Room excluded. This is a research backlog, not 150 verified vendors or publishable articles.", "", "Each item requires official-site identity/alias verification, platform fit, current evidence, screenshot provenance, original article/comparison drafts, and independent review. Merge aliases; use honest platform-replacement angles for non-Mac tools. The expansion job will create staged execution jobs after shared prerequisites pass.", ""]
    for product in ordered:
        seeds = ", ".join(sorted({edge["seedId"] for edge in product["edges"]}))
        lines.append(f"- [ ] [{product['name']}]({product['listingUrl']}) — `{product['id']}`; seeds: {seeds}; verify identity and distinct intent before drafting.")
    (CONTENT / "CONTENT-CHECKLIST.md").write_text("\n".join(lines) + "\n")
    print(json.dumps(manifest["counts"]))


if __name__ == "__main__":
    build()
