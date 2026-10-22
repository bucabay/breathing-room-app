"""Assemble the Mole research packet from retained public evidence; no network calls."""
import datetime
import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent


class Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def norm(text):
    return " ".join(text.split())


sources = []
texts = {}
for sid, name in [("directory", "mole-directory"), ("homepage", "mole-official"), ("repository", "mole-cli-extra")]:
    path = ROOT / "docs/content/.runtime/verification-1" / (name + ".json")
    data = json.loads(path.read_text())
    texts[sid] = data["text"]
    sources.append({
        "id": sid, "publisher": "AlternativeTo" if sid == "directory" else "Tw93 / Mole",
        "url": data.get("sourceUrl", data.get("url", data.get("officialUrl"))),
        "finalUrl": data.get("finalUrl", data.get("url")),
        "retrievedAtUtc": data["retrievedAt"], "snapshotPath": str(path.relative_to(ROOT)),
        "sha256": digest(path), "method": "reused existing verification-1 snapshot; not fetched again",
        "publicationDate": None,
        "scope": "directory discovery only" if sid == "directory" else "mutable official page / repository default-branch documentation; not runtime testing",
    })

for sid in ("terms", "docs", "releases", "visual-source"):
    meta = json.loads((OUT / "sources" / (sid + ".meta.json")).read_text())
    path = ROOT / meta["path"]
    assert digest(path) == meta["sha256"]
    parser = Text()
    parser.feed(path.read_text())
    texts[sid] = " ".join(parser.parts)
    sources.append({"id": sid, "publisher": "Tw93 / Mole", "url": meta["url"],
                    "finalUrl": meta["finalUrl"], "retrievedAtUtc": meta["retrievedAtUtc"],
                    "snapshotPath": meta["path"], "sha256": meta["sha256"],
                    "publicationDate": "October 2026" if sid in ("terms", "docs") else None,
                    "method": "public unauthenticated HTTPS GET; retained HTML",
                    "scope": "vendor documentation; some docs explicitly describe Preview-only features"})

cap = ROOT / "docs/content/capabilities.md"
texts["breathing-room"] = cap.read_text()
sources.append({"id": "breathing-room", "publisher": "Breathing Room first-party evidence register",
                "url": "https://breathing-room.chatic.ai/", "finalUrl": None,
                "retrievedAtUtc": None, "checkedOn": "2026-10-21",
                "snapshotPath": str(cap.relative_to(ROOT)), "sha256": digest(cap),
                "method": "reused same-day source/code/public-offer verification; no redundant live retrieval",
                "scope": "0.1.0-preview.1 public offer versus local source implementation; not binary parity"})

claims = []


def claim(cid, wording, sid, excerpt, scope, location="comparison matrix / workflow article"):
    assert norm(excerpt) in norm(texts[sid]), (cid, "excerpt absent")
    source = next(s for s in sources if s["id"] == sid)
    claims.append({"id": cid, "wording": wording, "sourceIds": [sid],
                   "sourceUrl": source["url"], "excerpt": excerpt,
                   "checkedOn": "2026-10-21", "sourceRetrievedAtUtc": source["retrievedAtUtc"],
                   "evidenceClass": "first-party evidence-register reuse" if sid == "breathing-room" else "official documented behavior / offer, not hands-on observation",
                   "state": "verified", "scope": scope, "intendedLocation": location,
                   "reviewer": "research-mole worker; independent editorial review pending"})


claim("identity", "Mole at mole.fit and tw93/Mole are the native-app and CLI product family maintained by Tw93.", "repository",
      "This repo is the free open-source CLI", "Repository links Mole for Mac; homepage links this same repository. CLI is not the native app source.")
claim("official-domain", "Use mole.fit, not similarly named third-party domains.", "repository",
      "molemac.com\n,\nmoleapp.net\nand\nmolefit.com\nare not Mole", "Explicit publisher disambiguation; do not merge community products.")
claim("native-license", "Mole for Mac is proprietary; GPL-3.0 describes the CLI, not the native app.", "repository",
      "is a separate proprietary app", "License section names Mole for Mac immediately before this passage. Resolves batch nativeAppLicense unknown.")
claim("cli-license", "The CLI is free, open source and GPL-3.0 licensed.", "docs",
      "is free, open source, and GPL-3.0 licensed", "CLI only; native Mac app terms are separate.")
claim("native-platform", "The native Mac app advertises macOS 14+.", "homepage", "macOS 14+", "Native app; architecture/signing not independently established.")
claim("cli-platform", "The Mac CLI documents macOS 12+ and Intel/Apple Silicon support.", "repository",
      "Mole requires macOS 12 or newer and supports both Intel and Apple Silicon Macs.", "Default-branch README; no installed version tested.")
claim("native-price", "The Mac app advertises $19 once, no subscription, covering two Macs; Windows is sold separately.", "homepage",
      "Covers 2 Macs, Windows sold separately", "Homepage Pricing also says '$', '19', 'Pay once, no subscription.' Currency code, tax and regional totals not verified; do not label USD as established.")
claim("native-terms", "Current retail licences are perpetual, non-transferable and allow two same-platform devices at once.", "terms",
      "you receive a non-exclusive, non-transferable, perpetual license", "Terms October 2026; activation cap and same-platform transfer/deactivation conditions apply.")
claim("native-trial", "Scanning is free; each named paid tool works twice before requiring a licence.", "docs",
      "each paid tool (Clean, Software, Optimize, and moving items to Trash in Analyze) works twice for free", "Not a timed free trial. Actual activation was not tested.")
claim("refund", "The homepage advertises a 14-day refund, requested by email with Payment ID; completion deactivates the key.", "homepage",
      "within 14 days of purchase with your Payment ID for a full refund", "Vendor offer only; no refund requested or tested.")
claim("preview-version", "Release notes label v1.18.0 build 338 as Preview; v1.17.0 Vega is dated 2026-10-18.", "releases",
      "v1.18.0 Preview", "Do not call homepage footer v1.18.0 stable. No installer downloaded or executed.")
claim("docs-preview", "Some documented features are Preview-only pending the next release.", "docs",
      "Some features on this page are in the", "Opening notice links Preview build; fine-grained current stable parity must be checked before detailed claims.")
claim("native-clean", "Clean lists caches, developer/AI data, leftovers and System Data for review; Manage Separately excludes backups, iCloud files, VMs and models from the cleanup total.", "docs",
      "The Manage Separately group lists backups, local iCloud files, virtual machines and models, outside the cleanup total.", "Vendor docs, potentially mixed stable/Preview; not a guarantee that every personal file is protected.")
claim("native-delete", "Mole's caches are permanently deleted by default, with an option to use Trash.", "docs",
      "Caches are permanently deleted by default, with a Trash option in Settings", "Do not generalize review-before-delete to reversibility; snapshot release and unified-log removal are separate risks.")
claim("native-analyze", "Analyze's Move to Trash context action moves an item immediately; already-trashed items ask before permanent deletion.", "docs",
      "moves the item right away, like Finder", "Analyze differs from Clean/Uninstall full-list confirmation. No action performed.")
claim("native-rebuild", "Package caches and generated build output are review-only by default in the Mac app.", "docs",
      "Review-only items stay unselected until you confirm", "Docs may include Preview features; do not copy CLI purge behavior to the native app.")
claim("cli-delete", "The CLI README says clean, purge and installer delete permanently; uninstall, analyze and slim use Trash by default after confirmation.", "repository",
      "delete permanently", "Safety section; clean also empties ~/.Trash by default unless protected. These are documented claims, not tests.")
claim("cli-purge", "CLI purge finds rebuildable project artifacts; recently active or unverified activity items start unselected.", "repository",
      "Artifacts with file activity in the last 7 days, or activity Mole cannot verify, are unselected by default.", "README default branch; exact stable CLI version not verified. Rebuild may require time/network.")
claim("native-local", "Mole says scans and cleanup stay on the Mac without uploading files/results.", "homepage",
      "Scans and cleanup stay on your Mac; files and results are never uploaded.", "Attributed vendor statement, not a network audit; activation/update network calls exist.")
claim("activation-network", "Mole licence activation and update checks require network destinations documented in its FAQ.", "homepage",
      "allow mole.fit, cdn.tw93.fun, and live.dodopayments.com", "Do not claim the entire native app is network-free.")
claim("native-on-demand", "The Clean page says it does not send scheduled cleanup reminders or keep scanning the disk in the background.", "visual-source",
      "Mole does not send scheduled cleanup reminders or keep scanning your disk in the background.", "Clean workflow only; not absence of all monitoring or scan refresh features.")
claim("native-growth-preview", "Preview 1.18 notes describe growth since an older Analyze map, including named growing files/folders.", "releases",
      "When the disk has grown by 1 GB or more since a map at least a day old", "v1.18.0 Preview only; invalidates blanket 'Mole has no growth tracking' wording.")
claim("native-grouping", "Release 1.15 notes describe app grouping with combined CPU/memory and expandable details.", "releases",
      "Processes are grouped by app with combined memory and CPU usage", "Published changelog behavior, not independently observed; never claim grouping is unique to Breathing Room.")
claim("breathing-preview", "Breathing Room is a free Apache-2.0 maintenance preview; source implementation is not proof of distributed feature parity.", "breathing-room",
      "Source implementation is not proof that every feature works in the distributed installer.", "Same-day capability register; version 0.1.0-preview.1; macOS 13+, universal advertised, physical Intel untested.")
claim("breathing-price", "Breathing Room's local core is free; optional hosted AI Care is advertised at $5 USD/month or $50 USD/year.", "breathing-room",
      "$5 USD/month or $50 USD/year", "Published offer, not paid entitlement enforcement; limits and checkout completion unverified.")
claim("breathing-caveats", "Breathing Room's preview requires Python 3.10+ for inventory and is not Developer ID signed or notarized.", "breathing-room",
      "Python **3.10+**", "Release says Apple Development signed; do not advise bypassing protections. Authenticated hosted AI sends relevant data off-device.")
claim("breathing-care", "Breathing Room source daily care uses saved exact approvals while the app runs; optional interactive Ruff automation is a separate exception.", "breathing-room",
      "only remembered exact approvals are eligible", "Source-confirmed, not binary/runtime test; daily care is advertised within paid AI Care.")

library = json.loads((ROOT / "docs/content/screenshots.json").read_text())
br = next(a for a in library["assets"] if a["id"] == "current-space-browser-preview")
assert digest(Path(br["sourcePath"])) == br["sha256"]
visuals = [{
    "id": "mole-clean-official", "productId": "mole", "view": "Native Clean tab",
    "kind": "official-asset", "sourcePageUrl": "https://mole.fit/mac-cleaner",
    "assetUrl": "https://mole.fit/img/en/clean.jpg", "capturedAtUtc": None,
    "retrievedAtUtc": None, "sourcePageRetrievedAtUtc": next(s["retrievedAtUtc"] for s in sources if s["id"] == "visual-source"),
    "capturedBy": None, "productVersion": None, "dataMode": "vendor-illustration",
    "originalPath": None, "originalSha256": None, "publishedPath": None, "publishedSha256": None,
    "widthPx": 2584, "heightPx": 1741, "dimensionBasis": "official img HTML attributes; not decoded image dimensions",
    "edits": [], "privacyReview": {"status": "pending", "redactions": []},
    "reuse": {"status": "link-only", "basis": "No screenshot reuse permission found. Terms reserve Tw93's content rights; public visibility is not a licence.",
              "evidenceUrlOrPath": "https://mole.fit/terms", "credit": "Mole / Tw93; official Clean-tab visual (link only)"},
    "caption": "Mole's official Clean-tab visual. Vendor illustration; version and capture date not supplied. No measured result from our testing.",
    "alt": "Mole Clean tab with Earth, the space a scan found and a button to review results.",
    "supportedClaimIds": ["native-clean"], "limitations": ["Exact source img and responsive WebP references found in retained HTML; asset not downloaded or visually approved.", "Link-only fallback does not meet the on-page screenshot gate."],
    "review": {"status": "pending", "reviewer": None, "reviewedAtUtc": None}
}, {
    **br, "productId": "breathing-room", "originalPath": br["sourcePath"], "originalSha256": br["sha256"],
    "publishedPath": None, "publishedSha256": None, "selectedPurpose": "Later figure: category/owner exploration before removal decisions",
    "requiredLabels": ["Current-source browser preview", "Example data only", "Not a native scan, measured activity or cleanup result"],
    "reuse": {"status": "cleared", "basis": br["reuseBasis"], "evidenceUrlOrPath": "docs/content/screenshots.json", "credit": "Breathing Room (which we build)"},
    "researchVisualInspection": "Opened actual PNG with image-capable read tool in research-mole: visible example-data banner, categories, project/development row and partly overlapping assistant composer. No native results inferred. Keep banner visible and choose a readable contextual presentation.",
    "review": {"status": "pending per-article review", "reviewer": None, "reviewedAtUtc": None}
}]

packet = {
    "schemaVersion": 1, "jobId": "research-mole", "productId": "mole", "canonicalOwnerId": "mole",
    "checkedOn": "2026-10-21", "status": "blocked", "stage": "research", "published": False,
    "identity": {"name": "Mole", "publisher": "Tw93", "homepage": "https://mole.fit/", "repository": "https://github.com/tw93/Mole",
                 "repositoryScope": "Free CLI only; not source for proprietary native Mac app", "aliases": ["Mole for Mac", "Mole CLI", "mo"],
                 "aliasDecision": "Keep one Mole packet; do not make separate doorway articles for the CLI/native app or mo command. Not an alias skip of this product.",
                 "skip": False, "aliasSkipDecision": "No separate aliases drafted; canonical Mole remains eligible.",
                 "powerMyMac": "No evidence in checked Mole sources identifies PowerMyMac as an alias. Do not merge or draft that separate queue item here.",
                 "excludedLookalikes": ["molemac.com", "moleapp.net", "molefit.com", "community Windows app at mole.bluecatbot.com"],
                 "fit": "direct Mac maintenance overlap", "fitReason": "Mac cleanup, disk analysis, monitoring and developer artifacts overlap; native and CLI workflows/prices/platform floors differ.",
                 "platformIntent": "Compare Mac workflows. Official native Windows edition is separate; no Windows support is implied for Breathing Room."},
    "reuseFirst": {"path": "docs/content/verification/batch-1.json", "recordId": "mole", "result": "Reused current homepage, repository and discovery snapshots. Native licence resolved from already-retained repository License section; no refetch.", "batch2": "No corresponding Mole record needed."},
    "discovery": {"url": "https://alternativeto.net/software/mole/about/", "seedUrl": "https://alternativeto.net/software/cleanmymac/", "edgeUrl": "https://alternativeto.net/software/cleanmymac/", "edgeRetrievedAtUtc": "2026-10-21T18:36:14.532Z", "aboutRetrievedAtUtc": "2026-10-21T19:04:48.234Z", "officialDestination": "https://mole.fit/?atp=alternativeto", "sourceId": "directory", "manifestPath": "docs/content/competitors.json", "method": "reused live-browser-rendered manifest edge and verification snapshot; no directory refetch"},
    "versions": {"nativePreview": "1.18.0 (338)", "latestNonPreviewEntryObserved": "1.17.0 Vega, 2026-10-18", "cliStable": None, "cliScope": "retained default-branch README, not pinned-release parity", "breathingRoom": "0.1.0-preview.1; current-source screenshot differs from tagged release"},
    "sources": sources, "claims": claims,
    "matrix": [
        {"dimension": k, "claimIds": ids} for k, ids in [
            ("macOS / runtime / installation", ["native-platform", "cli-platform", "breathing-caveats"]),
            ("licence / pricing / trial", ["native-license", "cli-license", "native-price", "native-terms", "native-trial", "refund", "breathing-price"]),
            ("local versus hosted", ["native-local", "activation-network", "breathing-caveats"]),
            ("scan and cleanup model", ["native-clean", "cli-purge", "breathing-preview"]),
            ("approval / deletion", ["native-delete", "native-analyze", "cli-delete", "breathing-care"]),
            ("helper grouping", ["native-grouping"]),
            ("recurring growth / care", ["native-on-demand", "native-growth-preview", "breathing-care"]),
            ("developer caches / rebuilding", ["native-rebuild", "cli-purge"])
        ]
    ],
    "visuals": visuals,
    "unknowns": ["Native price currency code, tax and regional totals", "Native CPU architecture floor, installer notarization/signing and exact runtime prerequisite policy", "CLI newest stable version and default-branch-to-release feature parity", "Per-feature stable versus Preview native parity", "Mole diagnostic/telemetry scope beyond attributed local scan statement", "Independent permission, privacy and contextual visual approval"],
    "blockers": [{"id": "competitor-image-rights", "severity": "critical-drafting-gate", "diagnostic": "Official Clean screenshot URL exists, but terms reserve content ownership and no reuse licence was located. No image downloaded. Link-only fallback does not satisfy EDITORIAL required on-page competitor UI gate.", "resolution": "Retain written permission or a published licence covering the exact asset, then download permitted original, hash/decode/inspect it and review privacy/context. Permission outreach is not authorized in this job."}],
    "blockedClaims": ["No native feature is described as tested or certified safe; no performance/storage savings measured.", "Do not call 1.18.0 stable or publish granular Preview behavior as 1.17 behavior.", "Do not claim Mole lacks grouped processes or growth comparison.", "Do not call the paid native app GPL/free, or a $19 licence unlimited-device/cross-platform.", "Do not publish a runnable CLI tutorial without authorized independent reproduction."],
    "briefs": {
        "workflow": {"title": "Before purging Mac build artifacts: review rebuild cost, age and removal method", "slug": "review-mac-build-artifacts-before-purging", "track": "search/reference workflow", "primaryIntent": "Decide which developer build artifacts to remove without confusing dependency downloads, generated output and project state.", "description": "Use Mole's distinct CLI purge and native Clean workflows to plan artifact removal, checking rebuild cost and permanent deletion versus Trash. This is documented workflow analysis, not a cleanup test.", "outline": ["Top official Mole Clean visual after lead, only once rights clear", "Separate package caches, generated output, downloaded dependencies and original project state", "Read CLI purge selection/age and permanent-deletion boundaries; do not execute examples", "Contrast native review-only candidates and flag Preview-specific additions", "Check backup, active work, reproducibility, bandwidth and removal destination before approval", "Later current-source Breathing Room Space preview, labeled example data", "Choose a terminal workflow or an inspection/care preview with disclosed runtime, hosted AI and signing caveats"], "interactionPass": "Hand off a static decision checklist: generated vs original; lockfile and sources available; active project; offline rebuild possible; Trash vs permanent. It must not imply a browser tool scanned files.", "links": ["/comparisons/mole/", "/comparisons/", "/tools/"], "length": "Earned; roughly 900–1500 words, no padding or invented FAQ"},
        "comparison": {"title": "Breathing Room vs Mole: native app, CLI and care workflows", "slug": "mole", "primaryIntent": "Choose a Mac maintenance workflow, not an assertion that every edition is interchangeable.", "structure": ["Conclusion and affiliation: Breathing Room, which we build", "Separate native Mole $19/two-Mac perpetual offer and free GPL CLI", "Concise sourced platform, approval/removal, disk analysis, process grouping, growth and hosted-boundary matrix", "Preview/runtime and installation caveats on both sides", "Who should choose Mole; who may prefer Breathing Room; workflow link"], "workflowLink": "/blog/review-mac-build-artifacts-before-purging/"}
    },
    "advantagesAndTradeoffs": {
        "mole": ["Free inspectable CLI for terminal-oriented users; GPL does not extend to the native app.", "Native app offers app update/uninstall, disk analysis and system monitoring; pricing is one-time for two Macs rather than a subscription.", "Mole already documents helper grouping and Preview growth comparison; do not invent a feature gap.", "Deletion modes vary: default cache removal and CLI purge can be permanent; review is not guaranteed reversibility."],
        "breathingRoom": ["May fit owners who want source-implemented ownership/category views, local history and exact-approval daily care; binary parity remains unverified.", "Free local core with optional paid authenticated hosted AI, not entirely offline assistance.", "Preview lacks Developer ID signing/notarization and clean-machine/physical-Intel validation; Python 3.10+ prerequisite matters.", "No benchmark evidence establishes safer/faster cleanup or higher space recovery than Mole."]},
    "execution": {"handsOnTesting": False, "cleanupPerformed": False, "accountsOrPayments": False, "browserUsed": False, "browserReason": "Existing current snapshots and public HTML supply facts/asset references; no browser capture needed and no image reuse permission established.", "imageDownloads": 0, "siteEdits": False, "independentReview": "pending separate stage", "siteBuilds": "not applicable: no marketing files changed"}
}
# Retry evidence is deliberately separate from current product-fact refreshes.
# These files are inspected source data only; never import or execute them.
tree = json.loads((OUT / "sources/cli-tree.json").read_text())
revision = tree["sha"]
retry_ids = {}
for name in ("cli-tree", "cli-README.md", "cli-LICENSE", "cli-mole",
             "cli-lib-core-common.sh", "cli-lib-core-commands.sh",
             "cli-lib-core-base.sh", "cli-lib-core-help.sh", "cli-lib-core-log.sh"):
    meta = json.loads((OUT / "sources" / (name + ".meta.json")).read_text())
    path = ROOT / meta["path"]
    assert digest(path) == meta["sha256"], name
    sid = "retry-" + name
    retry_ids[name] = sid
    texts[sid] = path.read_text()
    sources.append({"id": sid, "publisher": "Tw93 / Mole GitHub repository",
                    **{k: meta[k] for k in ("url", "finalUrl", "retrievedAtUtc", "sha256")},
                    "snapshotPath": meta["path"], "publicationDate": None,
                    "scope": "CLI visual-rights / capture feasibility only; pinned tree " + revision,
                    "method": "public unauthenticated GET; source retained and read, not executed"})

claim("cli-visual-reference", "The official CLI README references docs/img/big-mole.png as Mole cleanup results.",
      retry_ids["cli-README.md"], '<img src="./docs/img/big-mole.png" alt="Mole cleanup results" width="1000" />',
      "Pinned README identifies the candidate; image bytes not retrieved, inspected or licensed by inference.", "research visual provenance")
claim("cli-help-startup", "The inspected CLI loads common.sh before dispatching --help; common.sh invokes temporary-directory preparation.",
      retry_ids["cli-lib-core-common.sh"], 'prepare_mole_tmpdir > /dev/null',
      "Read alongside pinned entrypoint sources before main; base.sh preparation can reach guarded stale-temp pruning. Not an execution observation.", "research capture feasibility")
claim("cli-prune-path", "Temporary-directory preparation can reach a guarded stale-file deletion routine before help dispatch.",
      retry_ids["cli-lib-core-base.sh"], 'prune_stale_mole_temp_files "$MOLE_RESOLVED_TMPDIR"',
      "base.sh lines 1230–1262 and 1297–1358: pruning restricted to dedicated Mole cache/temp roots; do not imply every help invocation deletes files. No scripts run.", "research capture feasibility")
packet["visuals"].append({
    "id": "mole-cli-official-candidate", "productId": "mole", "view": "CLI cleanup results, as named by README; image uninspected",
    "kind": "official-asset", "sourcePageUrl": f"https://github.com/tw93/Mole/blob/{revision}/README.md",
    "assetUrl": f"https://raw.githubusercontent.com/tw93/Mole/{revision}/docs/img/big-mole.png",
    "capturedAtUtc": None, "retrievedAtUtc": None, "capturedBy": None, "productVersion": None,
    "buildOrCommit": revision, "dataMode": "unknown", "originalPath": None, "originalSha256": None,
    "publishedPath": None, "publishedSha256": None, "widthPx": None, "heightPx": None, "edits": [],
    "upstreamGitBlobSha1": next(e["sha"] for e in tree["tree"] if e["path"] == "docs/img/big-mole.png"),
    "privacyReview": {"status": "pending", "redactions": []},
    "reuse": {"status": "link-only", "basis": "Repository GPL-3.0 statement establishes CLI licensing, not explicit scope for this image. No asset-specific permission located in inspected README, LICENSE or tree paths. Do not download or publish by inference.",
              "evidenceUrlOrPath": f"https://github.com/tw93/Mole/blob/{revision}/README.md#license", "credit": "Mole CLI / Tw93; official repository README visual (link only)"},
    "caption": "Official Mole CLI README visual, labeled cleanup results by its publisher. Version, capture date and image contents not independently verified; not our test result.",
    "alt": None, "altDiagnostic": "Publication alt text requires permitted image retrieval and actual visual inspection; README alt alone is not an independent image description.",
    "supportedClaimIds": ["cli-visual-reference"],
    "limitations": ["Candidate reference only, not an approved app screenshot.", "Upstream Git blob SHA-1 is not a downloaded original SHA-256.", "GPL code licence not assumed to cover image; native app rights remain separate."],
    "review": {"status": "blocked pending rights and visual inspection", "reviewer": None, "reviewedAtUtc": None}
})
packet["retryInvestigation"] = {
    "requestedByUser": True, "checkedOn": "2026-10-21", "revision": revision,
    "scope": "Reuse existing packet and investigate CLI visual rights or genuine non-mutating capture, not repeat native asset request.",
    "officialAssetRoute": "Pinned README links big-mole.png; tree has GPL LICENSE but no image-specific licence/permission file identified. Root GPL and image co-location alone are not treated as clearance. No image bytes fetched.",
    "captureRoute": "command -v mo and command -v mole returned no path (shell exit 1). Entrypoint and startup sources read only. Before --help dispatch, common.sh invokes prepare_mole_tmpdir and entrypoint installs cleanup_temp_files trap. base.sh can probe/write temporary roots and prune old files in its dedicated cache/temp root. A complete non-mutating execution path has not been established; no install, command execution, fabricated terminal rendering or extracted-help substitute used.",
    "captureLimitations": "This is a source-level rejection of an unaudited live capture, not proof a specially reviewed isolated run is impossible. Remaining transitive modules, environment, approved execution surface and capture-output rights need review; do not bypass init or stub output and label it genuine UI.",
    "decision": "Retain critical image gate. CLI-only framing remains an option only after permitted actual CLI image/capture and inspection; do not use a CLI image as evidence of paid native capabilities.",
    "neededEvidenceOrDecision": [
        f"Published image-specific licence or retained owner permission covering docs/img/big-mole.png at {revision}, including reproduction scope and attribution/redistribution conditions; then permitted download, SHA-256, decode, privacy and visual review.",
        "Alternatively, an independently audited, explicitly authorized no-install/no-cleanup capture path for genuine CLI UI, plus an established reuse basis for captured output; retain exact version/OS/procedure/raw capture and inspect actual image. No authorization to change safety constraints is presumed.",
        "Native Clean image remains link-only unless permission specifically covers https://mole.fit/img/en/clean.jpg. No outreach authorized."
    ]
}
packet["blockers"][0].update({
    "diagnostic": "Native Clean image still rights-blocked. Retry found official CLI big-mole.png reference but no asset-specific licence scope; GPL code licence alone is not clearance. Neither CLI command on PATH; --help startup has temp preparation/pruning and exit cleanup hooks, so a genuine non-mutating capture was not established. No images downloaded or third-party code executed.",
    "resolution": "Resolve exact CLI image permission and inspect permitted bytes, or independently establish an authorized genuine non-mutating CLI capture and output reuse basis. See retryInvestigation. Required competitor-app image gate remains unwaived."
})
packet["execution"]["browserReason"] = "Read-only official GitHub tree/source inspection was sufficient for retry feasibility; no browser capture, cookie access or Chrome recovery needed."
packet["briefs"]["workflow"]["retryScope"] = "If CLI image rights clear, narrow to documented CLI purge artifact review; keep native Clean only as a distinctly labeled paid edition/context note, not a capability demonstrated by CLI visual. Existing draft gate remains blocked."
packet["briefs"]["comparison"]["cliOnlyAlternative"] = "Breathing Room vs Mole CLI: artifact review and removal choices. Scope all Mole feature rows to retained CLI README; paid native $19/two-Mac offer is context, not CLI pricing or demonstrated GUI capability. No separate doorway page; use canonical mole slug."
(OUT / "research.json").write_text(json.dumps(packet, indent=2, ensure_ascii=False) + "\n")
print(f"PASS: {len(claims)} claim excerpts matched retained sources; {len(sources)} source records; selected preview hash matched.")
