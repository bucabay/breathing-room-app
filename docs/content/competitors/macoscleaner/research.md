# MacOSCleaner research handoff

**Research blocked for drafting: screenshot reuse not cleared.** Task `research-macoscleaner`; local review date October 22, 2026. Actual retrievals are October 21 UTC, retained in `sources/retrievals.json`. No article, site edit, installation or product test was performed.

## Identity and relevance

The corresponding `batch-1.json` record was reused first, including the official homepage and discovery evidence. MacOSCleaner is **Aleksandr (AlexTkDev)'s Mac utility**: [homepage](https://alextkdev.github.io/MacOSCleaner/), [repository](https://github.com/AlexTkDev/MacOSCleaner). The README also styles it **MacOS Cleaner**; the licence names both forms. `canonicalOwnerId: macoscleaner`; suppress a separate spaced-name draft. It is not established as PowerMyMac and must not be merged with that different vendor identity. No other queue job was researched or edited.

Classification: **direct overlap, with platform boundaries**. Storage analysis, cache cleanup and process views overlap; its documented uninstaller and duplicate finder are additional decision criteria, not verified Breathing Room equivalents. Retain this product; do not skip it as dead, irrelevant or another product's alias. Its spaced spelling is the alias to skip.

Discovery: [AlternativeTo listing](https://alternativeto.net/software/macoscleaner/about/), retrieved `2026-10-21T19:09:10.786Z`; retained in `docs/content/.runtime/verification-1/macoscleaner-directory.json`. Manifest edges came from CleanMyMac and Mole seed pages. Exact URLs, times and hashes are in `research.json`. AlternativeTo's GPL-only label is incomplete: the official project adds Commons Clause. Directory text is not product-capability proof.

## Evidence and conditions

Every proposed claim has an ID, exact excerpt, original check date, source IDs resolving to URLs, intended location and qualifications in `research.json`. New immutable README/licence snapshots and release/image-index metadata are retained under `sources/`, with actual times and SHA-256 hashes. Baseline homepage facts were **not fetched again**. Official documentation establishes what is documented, not what we measured.

| Dimension | MacOSCleaner | Breathing Room | Evidence |
|---|---|---|---|
| Platform | macOS **26.0+**, **Apple Silicon only**; Intel explicitly unsupported | Reviewed preview advertises macOS **13+**, universal; physical Intel untested | `platform`, `br-preview` |
| Version/access | Homepage advertises **2.3.0**; public GitHub release published October 1, 2026; DMG asset listed | Reviewed **0.1.0-preview.1** pre-release, not production-ready | `version`, `br-preview` |
| Pricing | Advertised free, donations optional; commercial licensing separate, amount unknown | Free local core; optional AI Care **$5 USD/month or $50 USD/year**, renews until cancelled, tax at checkout | `price`, `license`, `br-price-hosted` |
| Licence | Source-available **GPLv3 + Commons Clause**, not unqualified GPL/open source; branding restrictions | Apache-2.0 desktop source, not hosted-service entitlement | `license`; capabilities register lines 79–80 |
| Local/hosted | Vendor documents local scanning and FoundationModels explanations; optional GitHub launch update check | Local inspection/execution; authenticated hosted assistant can transmit relevant paths/process/storage data | `local-ai`, `br-price-hosted` |
| Cleanup method | Standard categories directly pruned after path validation; uninstaller/analyzer/duplicates/review-only categories use Trash | Constrained local owning-tool commands/Trash actions; exact approvals, with optional verified-Ruff automatic exception | `cleanup`, `review`, `br-workflow` |
| Developer work | Xcode, Docker, package managers and project artifacts documented; public builds use fallback catalogue | Source implements developer-cache discovery/owning-tool checks; not universally compatibility-tested | `developer`, `br-workflow` |
| Process views | CPU/memory and flat/grouped views documented; helper-accounting equivalence unknown | Source groups helpers and samples activity, not complete forensic attribution | `process`, `br-workflow` |
| Growth/daily care | Recurring storage-growth investigation **not verified**; history/intent names do not prove it | Source implements activity and exact-approval daily care while running; paid offer/hosted limits apply | `br-workflow`, `br-price-hosted` |
| Uninstaller/duplicates | Both documented, including SHA-256 duplicate verification | Equivalent dedicated capabilities **not verified**, not “No” | `extra-tools` |
| Installation | Vendor docs include Gatekeeper workaround; binary signing/notarization not inspected | Preview disclosed Apple Development signed, not Developer ID signed or notarized; Python **3.10+** not bundled for inventory | `install`, `br-preview` |

Primary new sources: [pinned README](https://raw.githubusercontent.com/AlexTkDev/MacOSCleaner/d834666d2279160b01bb24cc236eaa7aedc5d629/README.md), [pinned licence](https://raw.githubusercontent.com/AlexTkDev/MacOSCleaner/d834666d2279160b01bb24cc236eaa7aedc5d629/LICENSE), [release 2.3.0](https://github.com/AlexTkDev/MacOSCleaner/releases/tag/2.3.0). Breathing Room facts reuse yesterday's `docs/content/capabilities.md` evidence register rather than needlessly re-fetching verified offers.

### Do not turn these sources into stronger claims

- No hands-on scans, cleanup, duplicate-detection, recovery, signing or network tests. No saved-space, speed, safety, battery or zero-latency result is supported. Homepage animated zero counters are not actual category counts.
- “Local/on-device/no telemetry” is the vendor's documented architecture, not our privacy audit. Model/device/language availability remains qualified, not guaranteed on every supported Mac.
- Exact newest-release status, build/DMG catalogue parity, commercial licence price, device limits and precise permission requirements remain unknown. README branch documentation is not proof of released-binary feature parity.
- Installation instructions contain a quarantine-removal command. **Do not reproduce it as advice or execute it**. Keep security status unknown rather than claiming independent signing verification.
- Standard cleanup is documented as direct removal, so “everything goes to Trash” is false. Trash movement is not immediate available-space recovery. Cache/dependency size does not grant deletion permission.
- Breathing Room is a preview requiring Python for inventory; its hosted AI is not all-offline. Website download account requirements differ from direct GitHub releases. Optional automatic Ruff mode qualifies blanket approval language. Paid entitlement/allowances and distributed feature parity are not established.

## Visual handoff and precise blocker

### Competitor: official Smart Cleanup screenshot, link-only

The [official README Demo section](https://github.com/AlexTkDev/MacOSCleaner/blob/d834666d2279160b01bb24cc236eaa7aedc5d629/README.md#demo) embeds an actual app screenshot, not a landing-page image. [Original asset URL](https://raw.githubusercontent.com/AlexTkDev/MacOSCleaner/d834666d2279160b01bb24cc236eaa7aedc5d629/assets/screenshots/Cleanup_page_v2_3.png). GitHub metadata lists 2,161,300 bytes and blob SHA-1 `b4cb7c2b62315ab29d8d0d6e212bf8f22c519799`. **This is not a downloaded-image SHA-256.** Capture date, OS and actual image data provenance remain unknown; v2.3 is the vendor filename label.

Caption: “Official MacOSCleaner Smart Cleanup screenshot, labelled v2.3 by the vendor. Linked for reference; not our test or measured cleanup result.” Alt: “Official MacOSCleaner Smart Cleanup app screenshot (vendor-labelled v2.3).” Credit: MacOSCleaner / AlexTkDev.

**Reuse: link-only.** Public availability and the software licence do not establish an unambiguous screenshot-specific grant for this commercial comparison. Commons Clause and branding restrictions require an authorized rights decision. No competitor image bytes were downloaded, copied or hotlinked; no permission message was sent. Original/published paths and hashes remain null, honestly. Pixels, privacy and mobile legibility have not been reviewed.

**Drafting stays blocked under EDITORIAL.md lines 147–148.** Resolution: an authorized reviewer must establish image-specific permission/licence or approve a documented editorial reuse basis, then obtain original bytes, preserve SHA-256/provenance, inspect privacy and legibility, and record review. An attributed link is a research fallback, not a waiver of the two-product image gate.

### Breathing Room: selected current-source Space browser preview

Reuse `docs/content/assets/breathing-room/space-preview-2026-10-21.png`, SHA-256 `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a`, 2940 × 3468. Library capture: `2026-10-21T19:06:45.416416+00:00`, source commit `54828ac3170b45861aee70861dd0b9c658ed7e51`. No new capture, edit or site copy.

Required caption: **“Current-source Breathing Room Space browser preview, captured October 21, 2026. Example data only; not a native scan, measured activity or cleanup result.”**

Alt: “Breathing Room Space view rendered in a browser with illustrative example data.” Keep the example-data banner visible. The first-party owner-requested capture basis and library privacy inspection are inherited; third-party marks and publication-context review remain bounded. “Current-source” describes the library capture, not proof of a current native binary or latest working-tree render. Independent article-context review is still pending.

## Distinct workflow brief — blocked, not article copy

**Proposed title:** Review developer caches before using MacOSCleaner  
**Proposed slug:** `review-developer-caches-before-macoscleaner`  
**Track:** search/reference. **Reader job:** an Apple Silicon developer deciding whether a scanned path is regenerable, currently needed and suitable for the proposed removal method.

Lead with compatibility and the direct-removal/Trash distinction, not gigabytes promised. Explain this sequence:

1. Check OS/CPU eligibility before choosing the tool.
2. Identify owner and purpose of each candidate; distinguish original work, project dependencies and disposable cache.
3. Account for re-download/rebuild cost and active work; unknown ownership means stop, not delete.
4. Review risk badges and selected paths; treat local AI explanations as assistance, not permission or a guarantee.
5. Separate direct-pruned categories from Trash workflows and note public-build catalogue limits.
6. Discuss when recurring-growth investigation may warrant a different approach; disclose “Breathing Room, which we build,” with preview/Python/hosted-data caveats.
7. Record a baseline and recheck without claiming Trash bytes equal newly free space. No destructive tutorial or invented output.

**Interaction handoff:** non-executing decision checklist: owner known → regenerable → active work checked → backup/rebuild available → removal method understood. Any unknown stops the decision. No filesystem access, cleanup button or unsupported calculator. Place cleared official Cleanup screenshot after the lead; use labelled Breathing Room Space preview later. Link to comparison and `/comparisons/`; only link a cache/rebuild tool after its route and implementation are independently verified. Proposed routes are not live claims.

## Concise comparison brief — blocked, not page copy

**Title:** Breathing Room vs MacOSCleaner. **Proposed comparison slug:** `macoscleaner`.

Answer selection intent with compatibility, AI-network boundary and the short matrix above. MacOSCleaner may fit documented uninstaller/duplicate workflows and eligible on-device explanations. Breathing Room may fit sourced activity/growth investigation and reviewed care, but is a non-notarized preview with Python, hosted-data and paid-Care qualifications. Keep this selection page short and link the deeper cache-review workflow; do not expand the matrix into a renamed article or create a second alias doorway page.

Neither price nor documentation proves superiority. MacOSCleaner has meaningful documented tools beyond Breathing Room's verified scope. Conversely, MacOSCleaner recurring-growth parity is unknown, not absent. An older-OS Mac is outside MacOSCleaner's stated requirements; Breathing Room's advertised universal installer is not proof of tested physical Intel execution. No Windows support is implied for either product.

## Validation and boundaries

See `validation.json` for executed checks and outcomes. Required files and inherited source hashes are checked; new raw text/API snapshots retain hashes and actual HTTP retrieval metadata. Claim excerpts are checked against retained source text, not URL status alone. Image permission remains a hard blocker regardless of successful JSON/hash checks. No independent article score or publication approval is awarded.

Only this product directory and its requested receipt are outputs. Unrelated work, website, queue/database and shared files remain untouched. No browser session, account, credential access, cleanup, settings change, package installation, commit, push or deployment was needed. App/site builds are not applicable to this research-only change and were not run.
