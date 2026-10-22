# PureMac research packet

**Task:** `research-puremac` · **Research complete; not publication approval.**

PureMac is a relevant, distinct Mac-maintenance product. Keep `canonicalOwnerId: puremac`; do not skip it as a PowerMyMac alias. A bounded documentary draft can proceed using the claims in `research.json`. No installation, cleanup, benchmark, native test or browser interaction was performed.

## Evidence and identity

Reused `docs/content/verification/batch-2.json` and its original PureMac directory/repository captures from **2026-10-21**. Both original file SHA-256 values match the baseline. Those facts were not fetched again merely to change their check dates. Exact retrieval timestamps, URLs, retained excerpts and hashes are in `research.json` and `sources/*.meta.json`. The worker's local calendar date is October 22; acquisition timestamps are actual UTC clock values, not backdated editorial dates.

- Discovery: <https://alternativeto.net/software/puremac/about/>. The retained rendered about-page links directly to `momenbasel/PureMac#install`. The manifest records CleanMyMac and Mole seed edges; it does not supply a more-specific pagination position, so none is invented.
- Official repository: <https://github.com/momenbasel/PureMac>.
- Official homepage: <https://www.moamenbasel.com/PureMac/>, linked by the repository and linking back to it. Author: Moamen Basel; GitHub owner `momenbasel`.
- Verified alternate name: **PureMac Cleaner**, from homepage structured data. This is the same owner, not a second article candidate.
- PowerMyMac is a separate identity lead. The existing batch-2 record points its FoneDog URL to TechyCub Mac Cleaner, whereas PureMac's directory, homepage and source identify the independent PureMac repository. No evidence supports merging PureMac into PowerMyMac. No PowerMyMac files were changed or independently researched here.
- Fit: **direct overlap in Mac storage inspection and maintenance**, not identical feature sets. No Windows/Linux support is established or needed for this Mac intent.

## Material product facts

Each row below maps to exact proposed wording, source URL, supporting passage, original check date, evidence class and limitations in the JSON claim ledger.

| Dimension | Bounded finding | Claims |
| --- | --- | --- |
| Release | GitHub's latest stable release API returned **v3.1.0**, published **2026-10-08**, with DMG and ZIP assets. Not downloaded or executed. | `release` |
| Platform/version | Source config targets **macOS 13.0**, **arm64 + x86_64**, marketing version **3.1.0**, build **30**. Main-branch documentation is not certification of binary parity. | `platform` |
| Price/licence | Advertised **free**, no subscription, trial or account; MIT source licence. This is not a paid trial or zero-price introductory period. Preserve copyright and permission notice when redistributing repository material. | `free`, `license` |
| Distribution | Release author describes a universal Developer ID-signed, notarized and stapled app. This is a vendor release disclosure, not our signature inspection. Homebrew and release DMG installation are documented; no commands were run. | `signing`, `install` |
| Inspection | Space Explorer measures allocated folder space, supports drill-down/Finder reveal and reports inaccessible/skipped entries. Folder size is not a promise of space recovered. | `space` |
| Removal | User-level app, orphan and exact-duplicate removal use Trash. Category/dashboard cleanup, scheduled auto-clean, Trash emptying, Docker/Xcode runtime cleanup, administrator removal, local snapshots and CLI paths can permanently delete data. | `removal`, `permanent-source` |
| Approval | Manual destructive workflows require confirmation; scheduled auto-clean remains unattended once enabled. Do not write “asks before every deletion.” | `approvals` |
| Developer categories | Xcode, Homebrew, npm, Yarn classic, pnpm and Docker are documented. Some runtime/MCP items are opt-in; methods differ. A cache can have rebuild/download costs. | `developer` |
| Processes | Performance documents live CPU/memory and **helper grouping**. Do not claim this is unique to Breathing Room. Resident memory can overlap and CPU uses total Mac capacity. | `helpers` |
| Offline/network | Local scans/cleanup are documented offline; Homebrew updates and GitHub release checks use the network. No-telemetry wording is the author's policy assertion, not a network audit. | `offline` |
| Access | Full Disk Access affects coverage; without it some categories/container scans are incomplete. No permission was granted in this research. | `permissions` |
| Protection | Configuration audit, expressly **not antivirus or a malware scanner**. | `protection` |
| Recurring growth | Not verified. Scheduling cleanup does not by itself prove growth history or writer attribution. | JSON unknowns |

### Source conflict resolved without repeating the unsafe promise

The homepage's features, promise, comparison and FAQ say everything goes to Trash, and include blanket no-network wording. Those statements conflict with the repository's explicit current boundaries.

The retained README distinguishes Trash from permanent deletion and offline scans from networked updates. The source at pinned commit `1fbebb9840f2919a7d7fb71210c6ed37fe39f193`, `PureMac/Services/CleaningEngine.swift:165–209`, sends managed DerivedData to Trash but calls `fileManager.removeItem(at: itemURL)` in the alternative branch. This was **read, not executed**. It corroborates the permanent-delete caveat and rejects a universal recoverability claim.

Use the scoped repository descriptions. Do not use homepage “Trash-only,” “no network calls,” blanket safety, guaranteed recovery or universal pre-run approval claims. This conflict is resolved for that bounded comparison; it does not establish that every binary path has been audited. Do not copy PureMac's competitive checkmarks about other vendors as verified facts.

## Breathing Room comparison boundaries

Reuse `docs/content/capabilities.md`, checked October 21, rather than refetching its day-old verified public offer. Claims `br-preview` through `br-workflow` retain the distinction between implementation, advertised offer and runtime unknowns.

- Free Apache-2.0 Mac-maintenance **preview**, identified as `0.1.0-preview.1`, macOS 13+, universal installer advertised, Python **3.10+** prerequisite.
- Published preview is Apple Development signed, **not Developer ID signed or notarized**; clean-machine and physical Intel validation are incomplete. No assertion of production readiness or source-to-installer parity.
- Local core is advertised free. Optional AI Care: **$5 USD/month or $50 USD/year**, renews until cancelled, applicable tax at checkout. Exact hosted allowance and paid entitlement enforcement are not established.
- Hosted assistance requires authentication/internet; relevant paths/process/storage context may reach the service. Do not describe its AI as entirely offline. Website download registration and public GitHub releases are different flows.
- Source supports local activity history, grouped processes and saved exact approvals for daily care while the app runs. Optional interactive automatic mode for verified Ruff caches is an explicit exception to generic approval wording. No automatic deletion, schedule, permission or account setting was changed here.

## Real visual plan and provenance

### PureMac Space Explorer: official app UI, not a landing-page capture

- Source page: <https://github.com/momenbasel/PureMac/blob/1fbebb9840f2919a7d7fb71210c6ed37fe39f193/screenshots/space-explorer.png>.
- Original asset URL: <https://raw.githubusercontent.com/momenbasel/PureMac/1fbebb9840f2919a7d7fb71210c6ed37fe39f193/screenshots/space-explorer.png>.
- Original: `assets/space-explorer-original.png`, **2240 × 1480**, SHA-256 `739c0d02239cd73e69d67db79fb6f9a95da52aa0ce402a4ddb59889afe4c4ec1`.
- Opened and read the actual PNG. It shows Space Explorer, a sample `/tmp/PureMac Samples/Projects` folder, two design-asset files and allocated-space/access counters. The repository says its screenshots show the running Mac app and file tools use sample files/images. Capture date, OS and exact running-app version remain unknown; repository commit is not a fabricated app-build claim.
- Reuse basis: tracked documentation image in the MIT-licensed repository, whose licence explicitly covers software and associated documentation. Retain the full notice in `sources/image-license.txt` with any redistributed image; credit PureMac Contributors. This is not a blanket trademark licence or endorsement. No image modification was made.
- Caption: **PureMac Space Explorer, official running-app screenshot using sample files. Allocated-space figures are vendor sample data, not our measurements. Source: PureMac Contributors (MIT).**
- Alt: **PureMac Space Explorer showing two sample design-asset files, allocated folder size and skipped/inaccessible counters.**

### Selected Breathing Room view

Use `current-space-browser-preview` from `docs/content/screenshots.json`, not the legacy Home image. Original: `docs/content/assets/breathing-room/space-preview-2026-10-21.png`; SHA-256 `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a`. Hash checked and actual PNG opened in this job.

Required caption: **Current-source Breathing Room Space browser preview, captured October 21, 2026. Example data only; not a native scan, measured activity or cleanup result.** Alt: **Breathing Room Space view rendered in a browser with illustrative example data.** Retain the visible **Interactive preview · example data** banner. This is a first-party requested source-preview capture, not distributed native-release evidence. The floating composer overlaps part of the chart; decide responsive crop/context in drafting without hiding the disclosure. No crop or copied marketing asset exists yet.

These two original images meet research sourcing requirements. Published derivative paths/hashes remain null because nothing is published. Independent per-page responsive/theme, privacy, credit and legibility review is still required.

## Distinct workflow article brief

**Working title:** Inspect allocated folder space before choosing a Mac cleanup method  
**Proposed slug:** `inspect-folder-space-before-mac-cleanup`  
**Track:** search/reference · **Primary job:** distinguish inspection from removal before acting on a folder-size result.

Lead with the conclusion: inspect the chosen folder first; allocated bytes do not establish disposable data, recoverability or guaranteed free-space gains. Put the official sample-data Space Explorer image immediately after the lead.

1. Choose the folder and read allocated-space/skipped-access results using documented controls, not invented hands-on steps.
2. Separate original data, regenerable artifacts and unknown files. A large file or similar photo is not permission to delete it.
3. Choose the exact removal workflow: inspection alone, app/duplicate Trash workflow, category cleanup or scheduled cleanup. Explain the permanent-delete distinction and confirmations.
4. Check backup/rebuild costs and scope before any later action. Do not provide destructive runnable commands or promise benchmark outcomes.
5. Where recurring investigation is the actual reader need, explain Breathing Room's source-evidenced history/approval model with disclosure, preview/hosted caveats and the second real UI view. Do not assert PureMac lacks comparable features merely because not verified.

**Interaction handoff:** a non-mutating checklist with four branches (inspect / app-or-duplicate removal / category cleanup / unattended schedule). Show documented deletion method and approval boundaries beside each branch. No uploads, fake scanning or predicted savings. Implementation belongs to drafting, not this research job.

## Concise comparison brief

**Working title:** Breathing Room vs PureMac: reviewable care or a free native toolkit  
**Proposed route:** `/comparisons/puremac/` · **Intent:** product choice, not another copy of the workflow article.

Use six concise sourced rows: version/platform/runtime; local versus hosted; removal/approval boundaries; storage/process views; scheduling versus exact saved approvals; price/distribution caveats. Unknown cells say **not verified**. Link the workflow counterpart and `/comparisons/`; `/tools/` only where a relevant verified tool earns the link. Do not create a separate PureMac Cleaner or alternatives doorway page.

**PureMac advantages:** free MIT toolkit, documented uninstall/orphan/duplicate review and configuration checks, local offline scanning, stable universal release with vendor-disclosed Developer ID/notarization. Breathing Room has not established equivalence for all these tools. **Trade-offs:** heuristic matches need review, access limits affect coverage, scheduled/category paths may permanently delete, and our binary/runtime validation is absent.

**Breathing Room fit:** source-evidenced activity history and hosted investigation may help a reader pursuing recurring questions and scoped daily approvals. Say **“Breathing Room, which we build”** at the recommendation. **Trade-offs:** preview quality/signing limitations, Python prerequisite, hosted context/authentication and optional paid AI Care. No superiority, speed, safety or measured-savings claim is supported.

## Gates and honest unknowns

No critical research evidence is missing for the bounded briefs above. Binary tests, full main-to-release feature mapping, screenshot capture metadata and unlisted PureMac features remain unknown; omit unsupported claims rather than blocking unrelated verified statements. A draft that depends on those unknowns must stop and name the missing evidence.

Research completion is not an independent review score. Eventual content must remain draft/unpublished pending source-adjacent citations, proper credits/notice, changed-site check/build/tests and independent rendered review. No marketing/site record, queue/database or another competitor's files was edited. No browser recovery was needed; public HTTP sources and retained captures sufficed.

Validation results and exact artifact hashes are retained in `validation.json`; the job receipt records the actual checks. `build-packet.py` reproducibly checks retained source and image hashes plus supported excerpt presence before generating the JSON packet; it makes no network requests.
