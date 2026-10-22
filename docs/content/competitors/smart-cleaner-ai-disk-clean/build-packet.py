"""Build this product's evidence packet from retained public/source records only."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
PRODUCT = "smart-cleaner-ai-disk-clean"
now = datetime.now(timezone.utc).isoformat()

def load(path):
    return json.loads(path.read_text())

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def relative(path):
    return str(path.relative_to(ROOT))

def save(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")

baseline = next(p for p in load(ROOT / "docs/content/verification/batch-2.json")["records"] if p["id"] == PRODUCT)
manifest = next(p for p in load(ROOT / "docs/content/competitors.json")["competitors"] if p["id"] == PRODUCT)
sources = []
texts = {}

def source(sid, path, url, publisher, retrieved, scope, final=None):
    data = load(path)
    texts[sid] = data.get("text", "") + "\n" + json.dumps(data, ensure_ascii=False)
    sources.append({"id": sid, "publisher": publisher, "title": data.get("title", sid),
                    "url": url, "finalUrl": final or data.get("url", url),
                    "retrievedAtUtc": retrieved, "publicationOrUpdateDate": None,
                    "scope": scope, "snapshotPath": relative(path), "sha256": digest(path)})

for sid, original, name, url, when, publisher, scope in [
    ("S1", baseline["sources"][0]["rawCapture"], "baseline-official.json", baseline["officialUrl"], baseline["sources"][0]["retrievedAt"], "DijitalWorlds", "Reused current batch-2 official DOM; vendor descriptions, not tests"),
    ("S2", baseline["discovery"]["rawCapture"], "baseline-directory.json", baseline["discovery"]["sourceUrl"], baseline["discovery"]["retrievedAt"], "AlternativeTo", "Discovery only; no feature verification"),
]:
    path = HERE / "sources" / name
    path.write_bytes((ROOT / original).read_bytes())
    source(sid, path, url, publisher, when, scope)
    sources[-1]["reusedFrom"] = original
    sources[-1]["baselineHashVerified"] = digest(path) == (baseline["sources"][0]["sha256"] if sid == "S1" else baseline["discovery"]["sha256"])

for sid, name, url, publisher, scope in [
    ("S3", "app-store-dom.json", "https://apps.apple.com/us/app/smart-cleaner-ai-disk-clean/id6764714299?mt=12", "Apple App Store / developer-supplied listing", "US storefront, displayed version 1.1.6; documentary availability and purchase terms only"),
    ("S4", "official-visual-dom.json", baseline["officialUrl"], "DijitalWorlds", "Targeted screenshot URL and permission-link discovery; not a baseline fact refresh"),
    ("S5", "website-terms-dom.json", "https://dijitalworlds.com/en/terms-of-service/", "DijitalWorlds", "Website asset reuse restrictions; not software EULA"),
]:
    path = HERE / "sources" / name
    source(sid, path, url, publisher, load(path)["retrievedAtUtc"], scope)
sources[-1]["publicationOrUpdateDate"] = "2026-10-18"

br_path = HERE / "sources" / "breathing-room-readme.txt"
br_path.write_text((ROOT / "README.md").read_text())
texts["S6"] = br_path.read_text()
sources.append({"id": "S6", "publisher": "Breathing Room (first party)", "title": "README working-tree snapshot",
                "url": "https://github.com/bucabay/breathing-room-app/blob/main/README.md", "finalUrl": None,
                "retrievedAtUtc": now, "publicationOrUpdateDate": None,
                "scope": "Local source recheck; not current-binary runtime verification. Public offer independently checked in capabilities.md on 2026-10-21, reused without network refetch.",
                "snapshotPath": relative(br_path), "sha256": digest(br_path), "originalPath": "README.md"})

claims = []
def claim(cid, wording, sid, excerpt, scope, state="verified", location="comparison matrix and workflow evidence"):
    assert excerpt in texts[sid], (cid, excerpt)
    src = next(s for s in sources if s["id"] == sid)
    claims.append({"id": cid, "wording": wording, "state": state, "evidenceClass": "documented-not-tested",
                   "sourceIds": [sid], "sourceUrl": src["url"], "excerpt": excerpt,
                   "checkedAtUtc": src["retrievedAtUtc"], "reviewer": "scheduled research worker (not independent review)",
                   "scopeAndConditions": scope, "intendedLocation": location})

claim("C01", "The vendor identifies the app as Smart Cleaner AI: Disk Clean, by DijitalWorlds (Cemal Hekimoglu).", "S1", "Developer\nDijitalWorlds (Cemal Hekimoglu)", "Vendor name and identity; store ID cross-link establishes punctuation variants as the same app.")
claim("C02", "The official download link is Mac App Store ID 6764714299; the US listing is live and says Only for Mac.", "S3", "Only for Mac", "Public listing availability only; no installation or region-wide availability test.")
claim("C03", "The US listing requires macOS 14.6 or later.", "S3", "Requires macOS 14.6 or later.", "Do not imply Windows/Linux support.")
claim("C04", "The vendor says it supports Apple Silicon and Intel Macs on macOS 14.6+.", "S1", "natively built for Apple silicon Macs and also runs on Intel Macs running macOS 14.6 or later.", "Vendor claim, not architecture or runtime test.")
claim("C05", "The US App Store displays version 1.1.6, with the date label Sep 3.", "S3", "Version 1.1.6\nSep 3", "Year is not shown in retained visible DOM; do not infer year or verify latest across channels.")
claim("C06", "The app is free to download with in-app purchases; that does not mean all cleanup is free.", "S3", "Free · In‑App Purchases", "US storefront; no monetary amount exposed in the checked public listing.")
claim("C07", "The listing offers auto-renewable Yearly Pro or one-time Lifetime Pro for supported cleanup actions.", "S3", "Cleanup actions require either an auto-renewable Yearly Pro subscription or a one-time Lifetime Pro purchase.", "Exact price, currency, tax, trial and discount unverified; never invent a dollar price.")
claim("C08", "Yearly Pro renews unless cancelled at least 24 hours before period end; Lifetime Pro does not renew.", "S3", "Yearly Pro renews automatically unless cancelled at least 24 hours before the end of the current subscription period.", "Apple ID billing on confirmation; manage/cancel in App Store settings. Lifetime nonrenewal is separately stated in this same source.")
claim("C09", "The vendor documents local disk scanning, AI categorization and cleanup without receiving files.", "S1", "Disk scanning, AI categorization, and cleanup happen locally on your Mac. DijitalWorlds does not operate scanning servers or receive your files.", "Attributed vendor privacy assertion; not a network audit or independent guarantee.")
claim("C10", "The vendor says no app login or signup is required.", "S1", "Install, open, clean. No login, no email, no signup.", "Distinct from Apple ID requirements for App Store distribution/IAP.")
claim("C11", "The listing documents explicit review/approval before selected items are moved to Trash.", "S3", "You always review and approve items before they are moved to the Trash.", "Documented model only; not a blanket safety guarantee or proof every operation is reversible.")
claim("C12", "The listing documents exact duplicate files and photos within selected accessible locations.", "S3", "Find exact duplicate files and photos inside selected and accessible locations.", "Do not extend to similar-photo grouping; website also says exact and similar, so use narrower exact-only wording.")
claim("C13", "The vendor documents an interactive sunburst disk map.", "S1", "interactive sunburst map of folders and files.", "Do not claim completeness across inaccessible locations or speed.")
claim("C14", "The vendor specifically documents Xcode DerivedData review and warns of rebuild/indexing costs.", "S1", "Developer Caches (Xcode DerivedData)\nRegenerates on Next Build", "No measured 20+ GB recovery claim; source marketing figures are not tests.")
claim("C15", "Whether full app uninstall is free or Pro-only is conflicted between official sources.", "S3", "Scanning, storage analysis, app uninstalling, login-item management, cloud-folder review, and AI-guided suggestions are free.", "S1 says Removing apps with the uninstaller requires Pro. Do not choose the favorable version or publish an unqualified tier cell.", "contradicted")
claim("C16", "The developer's App Store privacy declaration is Data Not Collected.", "S3", "Data Not Collected", "Developer self-report; Apple says practices can vary. Product policy fetch returned generic fallback; no independent privacy audit.")
claim("C17", "Website terms require express prior written consent to republish site content, including images.", "S5", "You may not modify, reproduce, republish, distribute, transmit, or exploit any portion of the Site without our express prior written consent.", "Commercial editorial image reuse not cleared; no permission request sent.")
claim("C18", "The official app UI asset URL is exposed as Smart Cleaner AI: Disk Clean dashboard.", "S4", "Smart Cleaner AI: Disk Clean dashboard", "DOM image metadata only, not independent pixel inspection or version certification; link-only.")
claim("B01", "Breathing Room is a testing/development preview, Apple Development signed, not Developer ID signed or notarized.", "S6", "**not Developer ID signed or notarized**", "README source rechecked; reuse capabilities.md release verification. No installer/runtime test in this job.")
claim("B02", "Breathing Room requires macOS 13+, Python 3.10+ for inventory/legacy scripts; physical Intel remains untested.", "S6", "**Python 3.10+** for disk inventory and legacy cleanup scripts.", "Universal installer advertised, not proof of execution on both architectures.")
claim("B03", "Breathing Room's core local app is free; optional AI Care is advertised at $5 USD/month or $50 USD/year.", "S6", "**AI Care is optional: $5 USD/month or $50 USD/year.**", "Reused current published offer verification in capabilities.md; not checkout test, entitlement audit or unlimited-AI claim.")
claim("B04", "Breathing Room's hosted agent needs internet/sign-in and may send paths and storage information; AI is not entirely offline.", "S6", "question and relevant tool output, including file paths and storage information.", "Source/privacy boundary; no backend audit.")
claim("B05", "Breathing Room documents Space exploration, app/helper CPU/memory and Activity for recurring growth.", "S6", "Follow free-space history, observed file/folder changes, app starts, and sampled disk I/O to investigate recurring storage growth.", "Source implementations corroborated in capabilities.md; not proof of distributed-binary parity or complete writer attribution.")
claim("B06", "Breathing Room daily care reuses exact saved locations/methods and requires the app running.", "S6", "Breathing Room must remain running.", "New locations need review; optional narrow automatic Ruff-cache mode documented in capabilities.md prevents an unconditional never-auto-deletes claim.")
claim("B07", "Moving files to Trash is not immediate disk space recovery.", "S6", "Moving files to Trash is not the same as\nimmediately reclaiming disk space", "Do not add sizes, cleanup outcomes and free-space deltas as savings.")

screenshots = load(ROOT / "docs/content/screenshots.json")
br = next(a for a in screenshots["assets"] if a["id"] == "current-space-browser-preview")
assert digest(Path(br["sourcePath"])) == br["sha256"]
visuals = [
    {"id": "competitor-official-dashboard", "productId": PRODUCT, "view": "Dashboard (official DOM label)",
     "kind": "official-asset", "sourcePageUrl": baseline["officialUrl"],
     "assetUrl": "https://dijitalworlds.com/images/maccleaner/v2/window-dashboard.webp",
     "retrievedAtUtc": None, "assetUrlObservedAtUtc": next(s for s in sources if s["id"] == "S4")["retrievedAtUtc"],
     "capturedAtUtc": None, "capturedBy": None, "productVersion": None, "buildOrCommit": None, "osVersion": None,
     "dataMode": "vendor-illustration", "originalPath": None, "originalSha256": None,
     "publishedPath": None, "publishedSha256": None, "widthPx": 1600, "heightPx": 1210,
     "dimensionsBasis": "naturalWidth/naturalHeight of loaded image in official page DOM; not pixel review",
     "edits": [], "privacyReview": {"status": "pending", "redactions": []},
     "reuse": {"status": "link-only", "basis": "Website terms section 3 restrict republication without written consent; no consent recorded.",
               "evidenceUrlOrPath": "sources/website-terms-dom.json", "credit": "DijitalWorlds / Cemal Hekimoglu"},
     "caption": "Official Smart Cleaner AI dashboard illustration from DijitalWorlds; app version, capture date and displayed data are not independently verified. Linked, not licensed for republication.",
     "alt": "Official Smart Cleaner AI dashboard illustration, as labeled by the vendor.", "supportedClaimIds": ["C18"],
     "limitations": ["No image bytes downloaded; no original asset hash possible.", "Not independently visually inspected; cannot certify genuine unmodified app capture.", "Does not satisfy on-page visual gate."],
     "review": {"status": "pending", "reviewer": None, "reviewedAtUtc": None}},
    {"id": br["id"], "productId": "breathing-room", "view": br["view"], "kind": "browser-preview",
     "sourcePageUrl": br["sourceUrl"], "assetUrl": None, "capturedAtUtc": br["capturedOn"], "retrievedAtUtc": None,
     "capturedBy": "screenshot-library job per screenshots.json", "productVersion": None,
     "buildOrCommit": br["sourceCommit"], "osVersion": None, "dataMode": "example",
     "originalPath": br["sourcePath"], "originalSha256": br["sha256"], "publishedPath": None, "publishedSha256": None,
     "widthPx": br["width"], "heightPx": br["height"], "edits": [], "privacyReview": br["privacyReview"],
     "reuse": {"status": "cleared", "basis": br["reuseBasis"], "evidenceUrlOrPath": "docs/content/screenshots.json", "credit": "Breathing Room (which we build)"},
     "caption": br["caption"], "alt": br["alt"], "supportedClaimIds": ["B05"],
     "limitations": br["limitations"] + ["Current-source as of the October 21 capture, not guaranteed current release UI. Keep example banner visible; selected PNG opened/read in this research job."],
     "review": {"status": "research-visual-inspected-not-independent-publication-review", "reviewer": "scheduled research worker", "reviewedAtUtc": now}}
]

packet = {
    "schemaVersion": 1, "jobId": "research-" + PRODUCT, "productId": PRODUCT,
    "status": "blocked", "stage": "research", "published": False, "createdAtUtc": now,
    "dateNote": "Task context says October 22, 2026; retained browser and host clocks report October 21 UTC. Preserve actual UTC retrieval timestamps; do not relabel old verification as a new check.",
    "identity": {"officialName": baseline["officialName"], "storeName": "Smart Cleaner AI - Disk Clean", "developer": "DijitalWorlds / Cemal Hekimoglu",
                 "homepage": baseline["officialUrl"], "appStoreId": "6764714299", "officialRepository": None,
                 "repositoryStatus": "not verified; no repository link in checked official product/store links; not evidence that none exists",
                 "canonicalOwnerId": PRODUCT, "aliases": ["Smart Cleaner AI", "Smart Cleaner AI: Disk Clean", "Smart Cleaner AI - Disk Clean"],
                 "aliasEvidence": "S1 links to S3's stable store ID; S3 links back to S1 homepage. Punctuation/short-title variants, not separate products.",
                 "aliasSkipDecision": "skip separate drafts for name variants; retain this canonical owner. No evidence connects this app to PowerMyMac; no merge and no research of that other queue job.",
                 "classification": "direct-mac-storage-review-and-cleanup-overlap", "classificationBasis": ["C03", "C11", "C12", "C13"],
                 "fitLimit": "Direct storage workflow overlap, not demonstrated equivalence in ongoing monitoring, helper grouping or developer adapters. No Windows/Linux replacement claim.",
                 "skipDecision": {"skipProduct": False, "skipSeparateAliasDrafts": True, "reason": "Live distinct official Mac product. Draft blocked on evidence, not dead/irrelevant/alias."}},
    "discovery": {**baseline["discovery"], "edges": manifest["edges"],
                  "rawPath": "sources/baseline-directory.json", "rawSha256": digest(HERE / "sources/baseline-directory.json"),
                  "upstreamEdgeNote": "Pagination edge provenance reused from competitors.json. Do not treat directory claims as verified product facts."},
    "reusedEvidence": ["docs/content/verification/batch-2.json", "docs/content/capabilities.md", "docs/content/screenshots.json", "docs/content/verification/alias-decisions.json"],
    "sources": sources, "claims": claims,
    "exactVersionAndPricing": {"version": "1.1.6", "channel": "US Mac App Store visible listing", "versionDateLabel": "Sep 3", "versionDateYear": None,
                               "minimumMacOS": "14.6", "download": "Free with IAP", "plans": ["Yearly Pro auto-renewable", "Lifetime Pro one-time"],
                               "amount": None, "currency": None, "trial": None, "tax": None, "priceUnknownTreatment": "Omit amounts or say not verified; refresh before publication without checkout/signup.",
                               "tierConflictClaimId": "C15", "claimIds": ["C03", "C05", "C06", "C07", "C08", "C15"]},
    "productMatrix": [
        {"dimension": "macOS / architecture", "competitor": "macOS 14.6+; vendor says Intel and Apple Silicon", "competitorClaimIds": ["C03", "C04"], "breathingRoomClaimIds": ["B01", "B02"]},
        {"dimension": "license / repo", "competitor": "Software licence/EULA and public repository not verified; website copyright does not establish software licence", "competitorClaimIds": [], "breathingRoom": "Apache-2.0 desktop source per capabilities.md; hosted service not included"},
        {"dimension": "local vs hosted / account", "competitor": "Vendor says on-device, no app account", "competitorClaimIds": ["C09", "C10", "C16"], "breathingRoomClaimIds": ["B04"]},
        {"dimension": "scan / approval / removal", "competitor": "Exact duplicates, disk map and reviewed Trash moves; not tested", "competitorClaimIds": ["C11", "C12", "C13"], "breathingRoomClaimIds": ["B05", "B06", "B07"]},
        {"dimension": "app/helper grouping / recurring-growth monitoring", "competitor": "not verified; do not write No", "competitorClaimIds": [], "breathingRoomClaimIds": ["B05"]},
        {"dimension": "developer caches", "competitor": "Vendor documents Xcode DerivedData; package-manager adapter coverage not verified", "competitorClaimIds": ["C14"], "breathingRoom": "Source adapter scope documented in capabilities.md; no cache compatibility test here"},
        {"dimension": "pricing / app uninstall tier", "competitor": "Free download; Yearly/Lifetime Pro; amounts unknown; uninstall tier conflict", "competitorClaimIds": ["C06", "C07", "C08", "C15"], "breathingRoomClaimIds": ["B03"]},
        {"dimension": "install/runtime", "competitor": "Mac App Store; accessible-location permissions apply; no runtime test", "competitorClaimIds": ["C02", "C03", "C12"], "breathingRoomClaimIds": ["B01", "B02", "B04", "B06"]}
    ],
    "visuals": visuals,
    "briefs": {
        "workflow": {"title": "Review Mac cleanup candidates before paying for removal", "slug": "review-mac-cleanup-candidates-before-paying", "track": "search-reference",
                     "primaryIntent": "Use Smart Cleaner AI's documented free scanning/maps to separate duplicates, rebuildable Xcode data and personal files before any paid removal decision.",
                     "outline": ["Inventory first; scanning is not cleanup permission", "Compare exact duplicates by location and purpose", "Treat Xcode DerivedData as rebuildable, not cost-free", "Check Pro conditions and the conflicting uninstall tier", "Distinguish Trash moves from free-space recovery", "Choose ongoing investigation when storage returns"],
                     "interactionHandoff": "Non-mutating checklist: need a duplicate review, cache review, uninstall, or recurring-growth investigation? Show relevant documented workflow and unknowns; no savings calculator or deletion controls.",
                     "visualPlan": "Official dashboard immediately after lead once rights/capture clear; disclosed BR Space example preview later. Keep both pending per-page independent review."},
        "comparison": {"title": "Smart Cleaner AI vs Breathing Room: cleanup review or ongoing investigation?", "slug": PRODUCT,
                       "primaryIntent": "Concise Mac choice, not an alternatives doorway", "rows": ["macOS/runtime", "local vs hosted", "duplicate/map review", "approval and Trash semantics", "uninstall tier conflict", "monitoring evidence", "pricing conditions"],
                       "disclosure": "Breathing Room, which we build", "crossLinks": ["/comparisons/", "/blog/review-mac-cleanup-candidates-before-paying/"],
                       "toolLink": "Only link an existing verified relevant tool; do not invent a route."}},
    "truthfulAdvantagesAndTradeoffs": {
        "competitorAdvantages": ["Vendor-documented on-device workflow with no app account (C09/C10), unlike BR hosted AI (B04).", "Documented exact duplicate finder and sunburst map (C12/C13); do not invent equivalent BR duplicate functionality.", "Live Mac App Store distribution (C02) and yearly/lifetime choice (C07); no claim it is cheaper or safer."],
        "competitorLimits": ["macOS 14.6 minimum (C03).", "Pro cleanup is not synonymous with free scanning (C06/C07).", "Uninstall tier conflicts (C15); prices, monitoring/helper grouping and runtime outcomes unknown."],
        "breathingRoomFit": ["Recurring-growth investigation and app/helper context are source-documented (B05), not evidence the competitor lacks them.", "Free local app and optional advertised AI Care (B03); not an all-free/all-local AI substitute."],
        "breathingRoomLimits": ["Non-notarized preview and Python requirement (B01/B02), no clean-machine or physical-Intel validation claimed.", "Hosted AI/sign-in/data boundary (B04); app-running daily-care constraint (B06).", "Do not claim duplicate-finder, full uninstaller, savings, speed or binary feature parity without new evidence."]},
    "unknowns": ["Exact IAP amounts, currency, tax, trial/discount conditions", "Version-date year and newest release across other channels", "Software licence/EULA and repository", "Actual image capture version/date and reuse permission", "Independent app/network/runtime tests", "Competitor process/helper grouping, recurring growth, other developer adapters"],
    "accessDiagnostics": ["WebFetch of app privacy, app terms and website terms returned generic DijitalWorlds Markdown fallback rather than requested policies; not used as policy evidence.", "Owned Chrome tab 164 read actual website terms, then App Store DOM. No cookies, browser storage or hidden payload extraction. No controls submitted.", "No image assets downloaded because commercial republication permission was not established. Website terms observed; stopped further vendor requests."],
    "blockers": [
        {"id": "visual-rights", "diagnostic": "Official dashboard URL identified but website terms restrict republication; no written consent. No licensed/cleared competitor UI asset or independent pixel/capture review. Link-only research fallback does not satisfy required on-page gate.", "resolution": "Authorized owner supplies permission/appropriately licensed authentic app UI and provenance; do not send permission requests in this job."},
        {"id": "uninstall-tier-conflict", "diagnostic": "S1 vendor page says app removal requires Pro; S3 store description says app uninstalling is free. Cannot verify exact free/paid uninstall boundary.", "resolution": "Obtain version-specific official clarification or permitted independent evidence before drafting this material pricing claim; do not silently prefer one source."}
    ],
    "draftGate": {"allowed": False, "reason": "Critical visual evidence and material tier conflict unresolved", "independentReview": "pending separate stage", "score": None},
    "validation": {"method": "validate-packet.py, outputs validation.json", "siteChecks": "not run; no site content/assets changed", "handsOnTests": "none; no app installation, scan, deletion, signup, purchase or hosted AI call"}
}
save(HERE / "research.json", packet)
print("Wrote", relative(HERE / "research.json"), "with", len(claims), "claims and", len(sources), "sources")
