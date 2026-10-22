"""Build this research-only packet from retained public evidence; no network access."""
import datetime
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat()
REVIEWER = "research-jwizard-cleaner scheduled worker (not independent review)"


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def rel(path):
    return str(Path(path).relative_to(ROOT))


baseline = next(r for r in json.loads((ROOT / "docs/content/verification/batch-1.json").read_text())["records"] if r["id"] == "jwizard-cleaner")
manifest = json.loads((ROOT / "docs/content/competitors.json").read_text())


def find_record(value):
    if isinstance(value, dict):
        if value.get("id") == "jwizard-cleaner":
            return value
        for child in value.values():
            found = find_record(child)
            if found:
                return found
    if isinstance(value, list):
        for child in value:
            found = find_record(child)
            if found:
                return found


sources = []
conflict_path = HERE / "sources/mac-webfetch-version.json"
sources.append({"id": "mac-webfetch-version", "url": "https://jwizard.com/cleaning-program-for-mac/", "finalUrl": "https://jwizard.com/cleaning-program-for-mac/", "retrievedAtUtc": None, "checkedOn": "2026-10-21", "snapshotPath": rel(conflict_path), "sha256": digest(conflict_path), "method": "Manually retained narrow WebFetch excerpt, not a full raw response"})
for key in ["mac", "mac-faq", "privacy", "refund", "uninstaller"]:
    path = HERE / f"sources/{key}-browser.json"
    data = json.loads(path.read_text())
    sources.append({"id": key, "publisher": "JWIZARD Cleaner official website", "title": data["title"],
                    "url": data["url"], "finalUrl": data["url"], "retrievedAtUtc": data["retrievedAtUtc"],
                    "publicationDate": "2026-01-12" if key in ["privacy", "refund"] else None,
                    "scope": "Mac desktop offer" if key in ["mac", "mac-faq", "uninstaller"] else "Vendor-wide policy; not a runtime audit",
                    "snapshotPath": rel(path), "sha256": digest(path), "method": "Owned Chrome tab; visible DOM text, no cookies or hidden account data"})
for key, path, url, stamp in [
    ("baseline-home", baseline["sources"][0]["snapshotPath"], baseline["officialUrl"], baseline["sources"][0]["retrievedAt"]),
    ("discovery", baseline["discovery"]["snapshotPath"], baseline["discovery"]["sourceUrl"], baseline["discovery"]["retrievedAt"]),
    ("br-capabilities", "docs/content/capabilities.md", "https://breathing-room.chatic.ai/", "2026-10-21"),
    ("br-readme", "README.md", "https://github.com/bucabay/breathing-room-app", NOW),
]:
    sources.append({"id": key, "url": url, "finalUrl": url, "snapshotPath": path, "sha256": digest(ROOT / path),
                    "retrievedAtUtc": stamp, "method": "Reused verified baseline" if key in ["baseline-home", "discovery", "br-capabilities"] else "Current local source read; not distributed-binary QA"})
claims = []


def claim(key, wording, source, excerpt, location="comparison matrix", state="verified", conditions="Vendor documentation, not hands-on testing"):
    claims.append({"id": key, "wording": wording, "sourceIds": [source], "sourceUrl": next(s["url"] for s in sources if s["id"] == source),
                   "excerpt": excerpt, "checkedAtUtc": next(s["retrievedAtUtc"] for s in sources if s["id"] == source),
                   "reviewedAtUtc": NOW, "intendedLocation": location, "state": state,
                   "evidenceClass": "documented" if state == "verified" else "unknown", "conditions": conditions, "reviewer": REVIEWER})


claim("identity", "JWIZARD Cleaner is the official product family at jwizard.com; compare its Mac edition here.", "baseline-home", "JWIZARD Cleaner for Mac", "identity")
claim("platform", "The Mac page lists macOS 12 and above.", "mac", "macOS 12 and above")
claim("version", "The live browser page displays 1.15.2, 31 August 2026; a text-fetch representation displayed 1.12.2, 24 March 2025.", "mac", "1.15.2, 31 August 2026", conditions="Display observation only. Do not certify latest downloadable binary; version conflict is retained, not silently resolved.")
claim("xcode", "The vendor advertises Xcode cache, temporary-file and old-build cleanup.", "mac", "Keep your Xcode workflow stable by removing its cache, temporary files, and old builds with JWIZARD Cleaner.", "workflow brief")
claim("scan", "The Mac page advertises Smart Scan plus system, browser, app and duplicate-file cleanup.", "mac", 'Apply "Smart Scan" mode', conditions="Capabilities advertised on this page; instant scans and performance gains not verified.")
claim("approval", "The vendor says it shows a preview and requests confirmation before deletion.", "mac", "You choose what to remove. JWIZARD Cleaner always shows you a preview and asks for confirmation before deleting anything.")
claim("uninstall", "The documented Uninstaller workflow scans apps, lets users select them and provides a Delete action.", "uninstaller", 'Launch the application and open the "Uninstaller" section.', conditions="Do not repeat claims of removing every residual file, registry entries, zero risk or speedups as verified facts.")
claim("extras", "The Mac page also advertises login-item controls, device information and video compression.", "mac", "LOGIN ITEMS", conditions="No functional tests; no lossless-compression or boot-speed claims endorsed.")
claim("term", "The Mac FAQ describes a one-year licence with subscription options for 1, 2 or 5 Macs.", "mac-faq", "The product license is valid for 1 year. Subscription options are available for use on 1, 2, or 5 Macs.")
claim("price", "Exact Mac subscription price, currency, taxes, renewal amount, cancellation and trial limits are not verified.", "mac-faq", "How long is the license valid?", state="not-verified", conditions="No purchase, checkout creation or download initiated. Do not call it free, lifetime, cheaper or a particular currency/amount.")
claim("privacy", "The policy describes device information, usage data including activations/crashes/scans/errors, and IP addresses.", "privacy", "the User's device information, application usage data (activation, crashes, scans, errors), and IP address.", conditions="Vendor-wide policy, not observed telemetry; does not establish an all-offline Mac workflow or uploaded file contents.")
claim("refund", "Website refunds are conditional, not an unconditional 30-day guarantee: report problems within 72 hours, cooperate with support, and refund eligibility is limited to unresolved issues within 30 days.", "refund", "All problems and issues must be reported within 72 hours after purchase", conditions="Policy updated January 12, 2026; one refund/customer, exclusions and potential 9% deduction for other approved reasons. Store purchases follow store policy.")
claim("license", "AlternativeTo labels the product proprietary; an official source-code licence or public repository was not established in checked pages.", "discovery", "Proprietary", state="not-verified", conditions="Directory label is discovery, not authoritative licence proof. No open-source claim or absence-of-repository claim.")
claim("br-platform", "Breathing Room is a macOS 13+ preview; Python 3.10+ is required for disk inventory and legacy scripts, and physical Intel runtime validation remains incomplete.", "br-readme", "Python 3.10+", conditions="Current README/source agrees with reused capabilities register; not installation testing.")
claim("br-cost", "Breathing Room's core app is free; optional AI Care is advertised at $5 USD/month or $50 USD/year; hosted agent workflows require sign-in and internet.", "br-readme", "AI Care is optional: $5 USD/month or $50 USD/year.", conditions="Public-offer verification reused from capabilities.md dated 2026-10-21; entitlement limits, payment/activation not tested.")
claim("br-controls", "Breathing Room documents exact-location/method cleanup review, app/helper CPU/memory inspection and activity history; these are source/documentation claims, not certified release parity.", "br-readme", "Review each proposed action's location, method, size, explanation, and rebuild or", conditions="Optional verified-Ruff automatic mode is an exception to universal per-action approval language; daily care reuses exact approvals and requires the app running. Sampled activity does not prove file authorship.")
claim("br-preview", "The preview is not notarized; do not recommend disabling Gatekeeper.", "br-readme", "The preview is not notarized.", conditions="Capabilities register/public release further disclose Apple Development rather than Developer ID signing; no new binary signature inspection.")

br = next(a for a in json.loads((ROOT / "docs/content/screenshots.json").read_text())["assets"] if a["id"] == "current-space-browser-preview")
assert digest(br["sourcePath"]) == br["sha256"]
visuals = [{"id": "jwizard-mac-xcode-official", "productId": "jwizard-cleaner", "view": "Xcode cleanup vendor app illustration",
            "kind": "official-asset", "sourcePageUrl": "https://jwizard.com/cleaning-program-for-mac/",
            "assetUrl": "https://jwizard.com/images/mac/xcode-en.webp", "capturedAtUtc": None, "capturedBy": None,
            "retrievedAtUtc": None, "sourcePageInspectedAtUtc": next(s["retrievedAtUtc"] for s in sources if s["id"] == "mac"), "productVersion": None,
            "dataMode": "vendor-illustration", "originalPath": None, "originalSha256": None, "publishedPath": None, "publishedSha256": None,
            "widthPx": None, "heightPx": None, "edits": [], "privacyReview": {"status": "pending", "redactions": []},
            "reuse": {"status": "link-only", "basis": "Public official app-illustration link; no licence/permission for republication established. Do not download, hotlink or publish until cleared.", "evidenceUrlOrPath": "https://jwizard.com/cleaning-program-for-mac/", "credit": "JWIZARD Cleaner"},
            "caption": "JWIZARD's official Xcode-cleanup illustration. Vendor-provided example; app version and capture date unknown; not our test result.",
            "alt": "Official JWIZARD Cleaner Mac Xcode cleanup illustration, linked from the vendor page.",
            "supportedClaimIds": ["xcode"], "limitations": ["Source page and exact image URL verified in browser snapshot/a11y output; image pixels not independently inspected.", "No asset downloaded because reuse permission is unresolved; no original hash invented.", "A linked illustration does not satisfy the on-page image gate."], "review": {"status": "pending"}},
           {"id": br["id"], "productId": "breathing-room", "view": br["view"], "kind": "browser-preview",
            "sourcePageUrl": br["sourceUrl"], "assetUrl": None, "capturedAtUtc": br["capturedOn"], "retrievedAtUtc": None,
            "buildOrCommit": br["sourceCommit"], "productVersion": None, "osVersion": None, "dataMode": "example",
            "originalPath": br["sourcePath"], "originalSha256": br["sha256"], "publishedPath": None, "publishedSha256": None,
            "widthPx": br["width"], "heightPx": br["height"], "edits": [], "privacyReview": br["privacyReview"],
            "reuse": {"status": "cleared", "basis": br["reuseBasis"], "evidenceUrlOrPath": "docs/content/screenshots.json", "credit": "Breathing Room"},
            "caption": br["caption"], "alt": br["alt"], "supportedClaimIds": ["br-controls"],
            "limitations": br["limitations"] + ["Current-source status refers to the October 21 capture, not proof of the latest distributed binary. Preserve both visible example-data banners."],
            "review": {"status": "research-inspected", "reviewer": REVIEWER, "reviewedAtUtc": NOW, "note": "PNG opened/read; example banners and Space categories visible; assistant composer overlaps chart. Page-context/mobile review remains pending."}}]

packet = {
    "schemaVersion": 1, "jobId": "research-jwizard-cleaner", "productId": "jwizard-cleaner", "status": "blocked", "stage": "research",
    "reviewedAtUtc": NOW, "dateNote": "Actual local/browser UTC retrieval clock is 2026-10-21; dates are retained, not advanced to the session's October 22 date.",
    "ownership": [rel(HERE)], "publicationEligible": False, "draftingAllowed": False,
    "identity": {"officialName": "JWIZARD Cleaner for Mac", "familyName": "JWIZARD Cleaner", "homepage": "https://jwizard.com/", "productUrl": "https://jwizard.com/cleaning-program-for-mac/", "officialRepository": None,
                 "repositoryStatus": "Not established; no repository linked in checked official pages", "canonicalOwnerId": "jwizard-cleaner",
                 "aliases": ["JWIZARD Mac Cleaner", "JWizard Cleaner"], "aliasEvidenceClaimIds": ["identity"],
                 "aliasSkipDecision": {"skip": False, "reason": "Same-brand Mac/family spelling variants share this canonical owner; no separate draft for a spelling or platform edition. No evidence links JWIZARD to PowerMyMac; no cross-product merge inferred."},
                 "classification": "direct-mac-cleanup-overlap", "reason": "Native Mac edition advertises cleanup and review controls; vendor family also has separate Windows/Android/iPhone editions. Breathing Room is not a Windows replacement.",
                 "vendorLegalIdentity": "Footer provides admin@familyshieldtechnologies.com; registered legal entity and ownership not independently established."},
    "baselineReuse": {"path": "docs/content/verification/batch-1.json", "recordId": baseline["id"], "record": baseline,
                      "policy": "Identity/homepage/family facts reused without refetching homepage or directory; new reads limited to missing Mac details and policy/visual evidence."},
    "discovery": {**baseline["discovery"], "sha256": digest(ROOT / baseline["discovery"]["snapshotPath"]), "edges": find_record(manifest)["edges"], "method": "Retained live-browser directory discovery; not feature proof"},
    "sources": sources, "claims": claims,
    "productMatrix": {"macOS": "platform", "versionDisplay": "version", "license": "license", "pricing": ["term", "price", "refund"], "localVsHosted": "privacy", "scanCleanup": ["scan", "xcode", "uninstall"], "approval": "approval", "otherUtilities": "extras",
                      "notVerified": ["Mac architecture requirements", "Installer signing/notarization", "Runtime dependencies", "Exact price/currency/tax/renewal/limits", "Offline cleanup capability", "CPU/memory helper grouping", "Recurring-growth history/scheduler", "Exact Xcode paths and rebuild behavior", "npm/pnpm/uv cache coverage", "Trash versus permanent deletion/rollback", "Official source-code licence/repository"],
                      "unknownRule": "Unknown is not No. Browser/library/device information is not proof of helper grouping, history or scheduled growth monitoring."},
    "breathingRoomComparison": {"claimIds": ["br-platform", "br-cost", "br-controls", "br-preview"], "sourceRegister": "docs/content/capabilities.md", "version": "0.1.0-preview.1", "sourceConfigChecks": ["README.md:45-164", "src-tauri/tauri.conf.json:4,49-51", "src/billing-config.json:5-8"], "caveats": ["Source implementation does not certify distributed-release parity.", "Free local app is not entirely offline hosted AI.", "App must run for scheduled care; optional Ruff auto-mode prevents a blanket never-deletes-without-asking claim.", "Public GitHub download bypasses website registration, not macOS protections."]},
    "visuals": visuals,
    "briefs": {
        "workflow": {"track": "search-reference", "title": "Review Xcode cleanup candidates without confusing rebuildable files with project data", "slug": "review-xcode-cleanup-candidates", "primaryIntent": "Mac developers deciding what an Xcode cleanup scan authorizes, not a generic JWIZARD alternatives keyword page", "outline": ["Separate a vendor's Xcode category label from proof of a disposable path", "Review candidate identity, current project use, rebuild/download cost and backups before approval", "JWIZARD's documented Xcode category versus Breathing Room's exact-action review model", "Do not claim path-specific Xcode advice or measured savings without separate evidence"], "limitations": "Do not draft exact deletion instructions: JWIZARD's actual Xcode paths and Apple current documentation are not in this packet. No cleanup executed.", "visualPlan": "Official JWIZARD Xcode app illustration after lead if rights cleared; labelled Breathing Room Space browser preview beside inventory-versus-permission explanation", "interactionHandoff": "Non-mutating decision checklist: know the path/owner, preserve originals, understand rebuild cost, review method, approve deliberately. No filesystem access or automatic Delete button."},
        "comparison": {"title": "Breathing Room vs JWIZARD Cleaner for Mac", "slug": "jwizard-cleaner", "primaryIntent": "Choose between documented Mac cleanup workflows and inspection needs", "outline": ["Conclusion with affiliation: Breathing Room, which we build", "Concise matrix: platform, advertised cleanup scope, review controls, licence term and honestly unknown price", "When JWIZARD's advertised Xcode/uninstaller/duplicate utilities fit", "When Breathing Room's storage/activity inspection preview fits, with runtime/hosted/signing caveats", "Link deeper workflow and /comparisons/ hub; no separate alternatives doorway"], "gates": "Research blocked; no site records created; preserve draft/unpublished state at later stages"}},
    "advantagesAndTradeoffs": {"jwizard": ["Advertises dedicated Mac Xcode, app-uninstaller, duplicate and video utilities; these are not certified equivalent Breathing Room features.", "Documents macOS 12+ versus Breathing Room's 13+ requirement; no cross-version tests.", "Documents preview/confirmation and 1/2/5-Mac annual licences; unknown price/rights/runtime details prevent stronger value or safety recommendations.", "Conditional refund terms must not be presented as no-questions-asked."], "breathingRoom": ["Documented storage views, grouped app/helper sampling and activity history fit investigation; competitor equivalents remain unknown, not absent.", "Free local core and optional advertised AI Care have explicit hosted/sign-in boundaries.", "Non-notarized preview, Python dependency and incomplete Intel/installer validation are material trade-offs, not footnotes."]},
    "conflicts": [{"field": "Mac version", "browser": "1.15.2, 31 August 2026", "webfetch": "1.12.2, 24 March 2025", "resolution": "Use only attributed live-browser display if needed. Latest downloadable artifact version remains unverified; no binary downloaded."}],
    "accessLog": [{"method": "Python urllib public HTTP", "urls": [s["url"] for s in sources if s["id"] in ["mac", "privacy", "refund", "uninstaller"]], "result": "HTTP 403; no snapshots produced; no retries or cookie extraction. Public browser navigation separately worked."}, {"method": "Chrome DevTools", "ownedPageIds": [117, 119, 120, 121], "result": "Visible pages read; licence FAQ expanded; no cookie consent, download, sign-in, checkout or other submissions"}],
    "blockers": [{"id": "competitor-visual-rights", "severity": "critical", "diagnostic": "Exact official app illustration URL found, but no republication permission/licence established. Link-only fallback does not satisfy required on-page competitor visual; do not draft until rights/access/provenance are cleared or an explicit policy decision authorizes an alternative.", "unblock": "Obtain independently verifiable permitted screenshot/reuse basis without unauthorized messaging; then retain original bytes/hash, dimensions, visual/privacy review and credit."}],
    "noncriticalUnknowns": ["Exact competitor price can remain visibly not verified; prohibit cheaper/free/lifetime claims.", "Latest downloadable version cannot be inferred from conflicting page representations.", "Official repository and precise proprietary licence terms are not established.", "Workflow brief needs Apple/path-level evidence before actionable Xcode deletion instructions."],
    "validation": {"nativeTests": "not performed", "cleanup": "not performed", "siteChecks": "not applicable: no marketing edits", "independentReview": "pending", "publicationScore": None}
}
(HERE / "research.json").write_text(json.dumps(packet, indent=2, ensure_ascii=False) + "\n")
print("Built", rel(HERE / "research.json"), "with", len(sources), "sources and", len(claims), "claims; drafting remains blocked.")
