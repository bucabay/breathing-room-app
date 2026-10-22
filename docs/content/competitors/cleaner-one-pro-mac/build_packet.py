"""Build the owned research packet from retained evidence, without network access."""
import datetime
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).parent
APP = ROOT.parents[3]
CHECKED = "2026-10-21"


def load(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


baseline_path = APP / "docs/content/verification/batch-1.json"
baseline = next(x for x in load(baseline_path)["records"] if x["id"] == "cleaner-one-pro-mac")
manifest = next(x for x in load(APP / "docs/content/competitors.json")["competitors"] if x["id"] == "cleaner-one-pro-mac")
sources = []
texts = {}
for path in sorted((ROOT / "sources").glob("*.json")):
    d = load(path)
    if "text" in d:
        sid = d.get("id", path.stem)
        texts[sid] = d["text"]
        sources.append(dict(id=sid, publisher="Trend Micro", title=d.get("title", sid),
                            sourceUrl=d["sourceUrl"], finalUrl=d.get("finalUrl", d["sourceUrl"]),
                            retrievedAtUtc=d.get("retrievedAtUtc", d.get("checkedAtUtc")),
                            snapshotPath=str(path.relative_to(ROOT)), snapshotSha256=sha(path),
                            rawSnapshotPath=d.get("snapshotPath"), rawSnapshotSha256=d.get("sha256"),
                            publicationDate=None, scope="Public source text; vendor claims, not independently tested app behavior."))
for sid, relative, url in [
    ("baseline-home", baseline["sources"][0]["snapshotPath"], baseline["officialUrl"]),
    ("discovery", baseline["discovery"]["snapshotPath"], baseline["discovery"]["sourceUrl"]),
    ("br-capabilities", "docs/content/capabilities.md", "https://breathing-room.chatic.ai/"),
    ("br-readme", "README.md", "https://github.com/bucabay/breathing-room-app"),
]:
    path = APP / relative
    d = load(path) if path.suffix == ".json" else None
    texts[sid] = d["text"] if d else path.read_text()
    sources.append(dict(id=sid, publisher="AlternativeTo" if sid == "discovery" else "Breathing Room" if sid.startswith("br-") else "Trend Micro",
                        title=sid, sourceUrl=url, finalUrl=url,
                        retrievedAtUtc=d.get("retrievedAt", d.get("retrievedAtUtc")) if d else None,
                        checkedOn=CHECKED, snapshotPath=str(path), snapshotSha256=sha(path),
                        scope="Reused current evidence; no redundant public refetch."))

claims = []


def claim(cid, wording, sid, excerpt, conditions, location="comparison matrix"):
    assert " ".join(excerpt.split()) in " ".join(texts[sid].split()), (cid, "excerpt missing")
    claims.append(dict(id=cid, wording=wording, state="verified", evidenceClass="source-documented" if sid.startswith("br-") else "vendor-published" if sid != "discovery" else "discovery-only",
                       sourceIds=[sid], sourceUrl=next(s["sourceUrl"] for s in sources if s["id"] == sid),
                       excerpt=excerpt, checkedOn=CHECKED, intendedLocation=location,
                       conditions=conditions, reviewer="research-cleaner-one-pro-mac; not independent publication review"))


claim("identity", "The official product is Trend Micro Cleaner One Pro for Mac.", "mac-product", "Cleaner One Pro for Mac", "Mac edition; homepage identity reused from batch-1.", "identity and lead")
claim("regional-alias", "Trend Micro says Cleaner One Pro is called Trend Cleaner Pro in some countries.", "installation", "In some countries, this software is called Trend Cleaner Pro", "Regional name, not evidence that every historic Trend Cleaner or Dr. Cleaner edition is identical.", "identity")
claim("compatibility", "The official Mac product page specifies macOS 10.15 and later.", "mac-product", "Compatibility: macOS 10.15 and later", "Vendor minimum, not tested macOS 26 support or architecture validation.")
claim("processor", "The purchase page specifies macOS 10.15 or higher and a 64-bit processor.", "purchase", "Mac: MacOS 10.15 or higher, 64-bit processor", "Do not infer native Apple Silicon, Rosetta requirements or runtime dependencies.")
claim("scan", "The vendor documents Smart Scan and scanning to visualize storage usage.", "mac-product", "Scan your Mac to visualize and analyze what's taking up your disk space.", "Product-page capability, not execution evidence.")
claim("duplicates", "The vendor documents duplicate-file and similar-photo cleanup.", "mac-product", "Get rid of duplicate files and similar photos", "No matching-accuracy benchmark or guarantee that suggested items are disposable.", "workflow article")
claim("startup", "The vendor documents managing which startup items can open automatically.", "mac-product", "Optimize your Mac's startup by managing which items can automatically open.", "Not proof of faster boot times or a recurring-growth history feature.")
claim("app-manager", "The vendor documents app-file management by name, size or date and deleting unwanted apps.", "mac-product", "Manage app files by name, size, or date.", "Not proof of complete removal of every related file or safe deletion.")
claim("shredder", "A File Shredder is advertised.", "mac-product", "File Shredder", "Do not repeat impossible-to-recover marketing as proven secure erasure, especially on SSDs.")
claim("vulnerability", "The Mac product page advertises a vulnerability scanner.", "mac-product", "Keep your device safe from the latest threats with vulnerability scans and software updates.", "Attributed advertised scope only; not proof of malware-removal coverage or a substitute for a dedicated antivirus.")
claim("installation", "Current official support documents Mac App Store and direct-download installation paths.", "installation", "You can install Cleaner One Pro on your Mac in two ways:", "Do not equate App Store edition feature/license parity with direct edition. No installer downloaded or run.")
claim("annual", "The purchase page offers a one-year subscription with 1-device and 5-device choices.", "purchase", "One Year Subscription", "Device counts confirmed in purchase-browser.txt; not a lifetime or one-time licence.")
claim("observed-prices", "The rendered purchase page showed $19.99 for 1 device and $29.99 for 5 devices for the one-year subscription.", "purchase-observation", "$19.99$24.99\nsaved $5.00\n50% off\nLicense For 5 Devices\n$29.99$59.99", "Observed public page only, English (United States) label. ISO currency, taxes, checkout total, eligibility and renewal amount not verified. Purchase link Locale=ru-ru; do not label universally USD or compare currency-adjusted costs.")
claim("renewal", "Official cancellation guidance describes automatic renewal; cancellation keeps access through the billing period.", "renewal", "Your subscription will remain active until the end of your current billing period.", "Guidance is channel-specific. No cancellation/account workflow performed; renewal price not established.")
claim("edition-boundary", "An older official comparison distinguishes Cleaner One Lite, Cleaner One and Cleaner One Pro.", "edition-differences", "What’s the Difference Between Cleaner One Lite, Cleaner One and Cleaner One Pro?", "Historical page references Big Sur and separate distribution channels; do not copy old feature matrix as current edition parity.", "identity caveat")
claim("historical-monitor", "The older official edition table includes a Network and CPU monitor row for Pro.", "edition-differences", "Network and CPU monitor", "Historical table only, unversioned and Big Sur-era; not sufficient to prove current helper grouping. Never say competitor has no monitoring.")
claim("copyright", "The official product page reserves Trend Micro copyright.", "mac-product", "All rights reserved.", "No affirmative screenshot reuse licence found. Public availability is not permission.", "visual rights")
claim("br-preview", "Breathing Room is a macOS maintenance preview; source implementation is not proof of installer parity.", "br-capabilities", "Source implementation is not proof that every feature works in the distributed installer.", "Reuse capabilities register checked today; no native test performed.")
claim("br-version", "The current capability register identifies Breathing Room 0.1.0-preview.1 as an inspected published prerelease, not a certified newest version across every channel.", "br-capabilities", "`0.1.0-preview.1`", "Register identifies local app and release configuration; inspected release tag differs from local source HEAD. No installer executed.")
claim("br-license", "Breathing Room desktop source uses Apache License 2.0, with attribution obligations.", "br-capabilities", "Desktop source is Apache License 2.0 with NOTICE and preserved third-party attribution.", "Not a licence for the hosted service, website or all trademarks/images.")
claim("br-install", "Breathing Room requires macOS 13+ and discloses Python 3.10+; preview is not Developer ID signed or notarized.", "br-capabilities", "Python **3.10+** is a disclosed prerequisite", "See capabilities installation matrix for architecture, unsigned-release and Gatekeeper boundaries. Do not recommend bypassing protections.")
claim("br-price", "Breathing Room core is free; optional AI Care is advertised at $5 USD/month or $50 USD/year.", "br-readme", "**AI Care is optional: $5 USD/month or $50 USD/year.**", "Hosted plan, renewals/tax caveats from capabilities register; not a paid app licence or unlimited AI.")
claim("br-hosted", "Breathing Room hosted AI needs internet access and authentication, unlike its local inspection boundary.", "br-capabilities", "Hosted AI assistance requires internet access and authentication", "Relevant inventory/tool output can be sent to hosted service; no all-offline/all-data-local assertion.")
claim("br-approvals", "Breathing Room source supports reviewable cleanup and exact saved approvals for daily care, with an explicit automatic Ruff-cache option.", "br-capabilities", "users can enable automatic Trash moves for narrowly verified Ruff caches during an investigation.", "Default review is not an unconditional never-deletes-without-asking promise. Daily care needs app running.")
claim("br-growth", "Breathing Room source records activity/free-space history and samples process activity.", "br-capabilities", "Source stores free-space samples, file/folder observations, app/process events and sampled I/O locally.", "Sampled/inferred attribution is not proof which app wrote a specific file; not binary runtime verification.")
claim("br-dev", "Breathing Room source includes developer-cache discovery for named package/build tools.", "br-capabilities", "Discovery includes queries for npm, uv, pip, pnpm, Go build/module, Bun and Yarn caches", "Tools must exist, location/method validation applies; no measured savings or universal adapter compatibility.")

unknowns = [
    dict(id="version", wording="Current direct-distribution version/build and date", state="not-verified", critical=False, reason="Product/support pages inspected do not identify a direct binary version. No app installed. Scope article to documented workflow; no version-specific walkthrough."),
    dict(id="license-repo", wording="Exact applicable EULA and official source repository", state="not-verified", critical=False, reason="Commercial subscription established. Directory labels proprietary; legal index links multiple agreements without establishing exact app applicability. No official source repo established; do not assert no repo exists or apply a guessed licence."),
    dict(id="offline", wording="Cleaner One Pro local/hosted data flow and offline operation", state="not-verified", critical=False, reason="Desktop installation established; not proof of entirely offline operation, zero telemetry, or data retention. Omit privacy superiority claims."),
    dict(id="approvals", wording="Current per-item approval, undo/Trash behavior and automatic cleanup controls", state="not-verified", critical=False, reason="Vendor image has selection and Remove controls; no destructive action tested or current approval contract verified."),
    dict(id="helper-grouping", wording="Current process/helper grouping", state="not-verified", critical=False, reason="Older table mentions monitoring, not app/helper attribution. Unknown is not No."),
    dict(id="growth", wording="Current recurring-growth monitoring/history", state="not-verified", critical=False, reason="No verified current source establishing this workflow. Do not claim absence."),
    dict(id="developer", wording="Specific developer-cache adapters", state="not-verified", critical=False, reason="General junk cleaning is not evidence for npm/pnpm/Go validation or exact owning-tool commands."),
    dict(id="runtime", wording="Cleaner One Pro runtime dependencies, full disk permissions, signing/notarization, Apple Silicon execution", state="not-verified", critical=False, reason="Minimum OS/64-bit CPU documented, no binary/security inspection. No sign-in or trial/free-feature quota established."),
    dict(id="currency-renewal", wording="ISO currency, localized checkout tax/renewal price and first-term eligibility", state="not-verified", critical=False, reason="Browser en-us page shows dollar symbol but Purchase Now link Locale=ru-ru. Omit universal USD and cheaper claims; final offer not tested."),
    dict(id="visual-rights", wording="Republication rights for official Similar Photos app image", state="not-verified", critical=True, reason="Official app image identified and visually inspected, but all-rights-reserved source provides no verified affirmative licence. Link-only; not downloaded; drafting blocked by EDITORIAL visual gate."),
]

br = next(a for a in load(APP / "docs/content/screenshots.json")["assets"] if a["id"] == "current-space-browser-preview")
assert sha(Path(br["sourcePath"])) == br["sha256"]
visual_obs = load(ROOT / "sources/visual-observation.json")
visuals = [dict(id="cleaner-one-pro-similar-photos", productId="cleaner-one-pro-mac", view="Similar Photos", kind="official-asset",
                sourcePageUrl="https://cleanerone.trendmicro.com/cleaner-one-pro-for-mac/",
                assetUrl="https://cleanerone.trendmicro.com/images/en-us/clean-duplicate-on-mac.webp",
                capturedAtUtc=None, retrievedAtUtc=visual_obs["checkedAtUtc"], capturedBy=None,
                productVersion=None, buildOrCommit=None, osVersion=None, dataMode="vendor-illustration",
                originalPath=None, originalSha256=None, publishedPath=None, publishedSha256=None,
                widthPx=645, heightPx=402, edits=[], downloaded=False,
                privacyReview=dict(status="pending", redactions=[], note="Public illustration; vendor blurred details. No private user data accessed; downstream publication review still required."),
                reuse=dict(status="link-only", basis="Official publicly accessible image; copyright reserved. No verified reproduction licence or permission. Link is research fallback only.", evidenceUrlOrPath="sources/mac-product.json", credit="Trend Micro, Cleaner One Pro for Mac"),
                caption="Trend Micro's official Cleaner One Pro for Mac Similar Photos illustration; version and capture date not provided. Linked reference only, not our app test or measured cleanup result.",
                alt="Cleaner One Pro Similar Photos view grouping flower and landscape images with selection controls and a Remove button.",
                supportedClaimIds=["duplicates"], limitations=["Original bytes not downloaded because reuse rights are unverified; original/published hashes intentionally null.", "645 × 402 vendor image; do not enlarge into evidence of readable fine UI detail or current binary behavior."],
                review=dict(status="visually-inspected-link-only", reviewer="research-cleaner-one-pro-mac", reviewedOn=CHECKED)),
           dict(id=br["id"], productId="breathing-room", view=br["view"], kind=br["kind"],
                sourcePageUrl=br["sourceUrl"], assetUrl=None, capturedAtUtc=br["capturedOn"], retrievedAtUtc=None,
                capturedBy="screenshot-library job", productVersion="current-source browser preview, not certified released binary", buildOrCommit=br["sourceCommit"], osVersion=None,
                dataMode="example", originalPath=br["sourcePath"], originalSha256=br["sha256"],
                publishedPath=None, publishedSha256=None, widthPx=br["width"], heightPx=br["height"], edits=[],
                privacyReview=br["privacyReview"], reuse=dict(status="cleared", basis=br["reuseBasis"], evidenceUrlOrPath="docs/content/screenshots.json", credit="Breathing Room, which we build; publication-specific review pending"),
                caption=br["caption"], alt=br["alt"], requiredLabels=["Interactive preview · example data", "This browser preview uses example data. Actions never change your Mac."],
                supportedClaimIds=["br-preview"], limitations=br["limitations"]+["Keep example-data labels visible. Source capture is not a new native/current-binary test. Figure needs readable context on mobile."],
                review=dict(status="opened-and-read-this-job", reviewer="research-cleaner-one-pro-mac", reviewedOn=CHECKED))]

packet = dict(schemaVersion=1, jobId="research-cleaner-one-pro-mac", productId="cleaner-one-pro-mac", stage="research", status="blocked", published=False,
              generatedAtUtc=datetime.datetime.now(datetime.timezone.utc).isoformat(), checkedOn=CHECKED,
              ownership="Only docs/content/competitors/cleaner-one-pro-mac/ plus required runtime receipt; no website edits.",
              identity=dict(officialName="Cleaner One Pro for Mac", vendor="Trend Micro Incorporated", homepage=baseline["officialUrl"],
                            macProductUrl="https://cleanerone.trendmicro.com/cleaner-one-pro-for-mac/", repo=None, repoStatus="not verified",
                            canonicalOwnerId="cleaner-one-pro-mac", aliases=[dict(name="Trend Cleaner Pro", status="verified-regional-alias", claimId="regional-alias", skipSeparateDraft=True)],
                            aliasSkipDecision="Do not draft separate Trend Cleaner Pro content. This Cleaner One Pro listing remains canonical and is not skipped. Cleaner One Lite/One are edition siblings, not proven aliases; Dr. Cleaner history unverified. No verified PowerMyMac relationship and no such candidate in this product's baseline; unrelated PowerMyMac jobs untouched.",
                            classification="direct", fitReason="Native Mac storage visualization/cleanup overlaps Breathing Room; similar-photo/duplicate-file and startup/app-management scope is distinct from ongoing source-level activity/developer-cache investigation.",
                            platforms=["macOS; official minimum 10.15", "Separate Windows edition officially linked; not included in Mac comparison"],
                            platformBoundary="Breathing Room is a Mac replacement choice only; never invent Breathing Room Windows support. Do not inherit AlternativeTo Chrome OS/iOS/Chromecast tags as official compatibility.", skip=False),
              discovery=dict(**baseline["discovery"], snapshotSha256=sha(APP / baseline["discovery"]["snapshotPath"]), edges=manifest["edges"], method="Reused live-browser directory/edge records; directory proves discovery only."),
              reusedVerification=dict(batchPath=str(baseline_path.relative_to(APP)), productId=baseline["id"], originalStatus=baseline["status"],
                                      originalFacts=baseline["facts"], originalOfficialSnapshot=baseline["sources"][0],
                                      baselineSha256Matches=sha(APP / baseline["sources"][0]["snapshotPath"]) == baseline["sources"][0]["sha256"],
                                      batch2="Checked index/search; no corresponding Cleaner One Pro record required. Global PowerMyMac ambiguity does not establish an alias here."),
              sources=sources, claims=claims, unknowns=unknowns,
              productMatrix=[
                  dict(dimension="platform and version", cleanerOnePro=["compatibility", "processor", "version"], breathingRoom=["br-preview", "br-version", "br-install"]),
                  dict(dimension="licence and repository", cleanerOnePro=["annual", "license-repo"], breathingRoom=["br-license"], note="BR Apache-2.0 desktop source documented in capabilities; hosted entitlement separate."),
                  dict(dimension="local/hosted and runtime", cleanerOnePro=["installation", "offline", "runtime"], breathingRoom=["br-hosted", "br-install"]),
                  dict(dimension="scan/cleanup and approvals", cleanerOnePro=["scan", "duplicates", "app-manager", "approvals"], breathingRoom=["br-approvals"]),
                  dict(dimension="helper grouping and recurring growth", cleanerOnePro=["historical-monitor", "helper-grouping", "growth"], breathingRoom=["br-growth"]),
                  dict(dimension="developer caches", cleanerOnePro=["developer"], breathingRoom=["br-dev"]),
                  dict(dimension="pricing", cleanerOnePro=["annual", "observed-prices", "renewal", "currency-renewal"], breathingRoom=["br-price"]),
              ], visuals=visuals,
              reproduction=dict(handsOnTest=False, installersDownloaded=False, cleanupExecuted=False, benchmarks=False, browser="Owned Chrome pages 79 (purchase) and 80 (official image); both closed. Existing tabs were not read or interacted with. No recovery needed.", calculations=[]),
              workflowBrief=dict(track="search-reference", title="Review similar photos before removing them from your Mac", slug="review-similar-photos-before-removing-mac",
                                 primaryIntent="Help a Mac owner decide which visually similar photos to retain, rather than treating a detected group as disposable duplicates.",
                                 description="Cleaner One Pro documents both duplicate files and similar-photo cleanup. Use its official illustration to explain a keep/review decision; distinguish that task from investigating why Mac storage keeps growing. No hands-on matching or deletion claims.",
                                 outline=["Lead with keep/review/stop decision; official Similar Photos UI immediately below lead only after rights cleared", "Duplicate files and similar-looking photos are different review tasks; no unverified algorithm claims", "Inspect each candidate's contents and provenance; stop when original/edit/library relationships are unclear", "Separate selected file sizes from available space and do not invent storage recovery", "If the problem is repeated growth instead, use a current-source Breathing Room Space example with explicit labels and disclose affiliation", "Choose documented photo cleanup or preview investigation based on the actual job"],
                                 interactionPass=dict(decision="A short no-files-uploaded keep/review/stop checklist", fields=["Is this merely similar-looking, or have you verified the contents?", "Do you know which copy/edit is needed?", "Is recovery/backup understood?"], result="Any uncertainty means keep/review, not permission to delete.", implemented=False, handoff="Implement only in separately owned draft/site stage after visual gate; no code required for conceptual comparison."),
                                 links=["/comparisons/", "/comparisons/cleaner-one-pro-mac/", "/tools/"],
                                 boundaries=["Not an app tutorial validated against a versioned installation", "No exact click sequence, deletion method, photo-library handling or matching accuracy asserted", "Apple-specific library/backup advice requires targeted Apple sources before inclusion"]),
              comparisonBrief=dict(title="Breathing Room vs Cleaner One Pro for Mac", slug="cleaner-one-pro-mac", primaryIntent="Choose documented category/photo/startup cleaning versus a preview for storage/activity investigation.",
                                   length="Concise sourced decision matrix, not a second expanded workflow article.",
                                   lead="Cleaner One Pro documents duplicate/similar-photo tools, app management and startup-item control. Breathing Room, which we build, is a free macOS preview with source-level investigation and approval workflows; it is not a verified substitute for every Cleaner One Pro tool.",
                                   sections=["Who each fits", "Claim-linked matrix including unknown cells", "Preview/runtime/hosted and regional pricing caveats", "When not to switch", "Link to distinct photo-review workflow"],
                                   noDoorwayRule="No additional Trend Cleaner Pro or generic alternatives page."),
              advantagesAndTradeoffs=dict(cleanerOneProAdvantages=["Documented duplicate/similar-photo categories and startup/app management fit users seeking those specific workflows (duplicates/startup/app-manager).", "Vendor minimum macOS 10.15 reaches earlier OS versions than BR's macOS 13 requirement; this is not a tested compatibility guarantee (compatibility/br-install)."],
                                          breathingRoomAdvantages=["Source-level activity/free-space history and developer-tool discovery suit investigating repeated growth; no unsupported absence claim about competitor (br-growth/br-dev).", "Free local core and optional hosted AI pricing are explicit; no currency-adjusted cheaper claim (br-price)."],
                                          tradeoffs=["BR preview is not Developer ID signed/notarized and requires Python 3.10+ for inventory/legacy scripts; physical Intel and distributed parity unverified.", "BR hosted AI sends relevant data and requires authentication/network; no offline-AI promise.", "Cleaner One Pro current version, exact cleanup controls, developer adapters and local/hosted boundaries are not verified.", "Competitor public image is link-only; price currency/locale/renewal terms need bounded wording or separate clarification.", "No measured speed, safety, savings, secure-erasure or matching-accuracy comparisons."]),
              draftingGate=dict(status="blocked", blockers=["visual-rights: clear republication rights for the real Cleaner One Pro app image or obtain an explicitly authorized alternative/policy decision. Official link fallback does not meet required on-page competitor image gate."],
                                noncriticalUnknownPolicy="Keep listed unknowns explicit and omit unsupported comparisons. Version unknown blocks only version-specific walkthroughs; pricing ambiguity blocks universal USD/renewal/cheaper assertions, not identity research.",
                                independentReview="pending; no score or publication approval awarded", siteChecks="Not applicable: no website records/assets edited; no build or deployment run."))
(ROOT / "research.json").write_text(json.dumps(packet, indent=2) + "\n")
print(f"Built research.json: {len(claims)} exact-excerpt claims, {len(sources)} sources, {len(visuals)} visuals; drafting blocked.")
