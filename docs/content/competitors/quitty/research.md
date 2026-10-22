# Quitty research: drafting blocked

Quitty is relevant to Mac maintenance, but do not draft a replacement or comparison page yet. Its official homepage remains reachable; the officially linked repository and release API return **404**. A real official dashboard image URL is available, but image reuse permission is unresolved. Neither failure proves permanent discontinuation.

Task: `research-quitty`. Canonical owner: `quitty`. Research only; no site records, drafts or queue state changed. Checks retain actual UTC timestamps (October 21, 2026, around 22:00 UTC; October 22 local task date). The detailed source, claim, visual and brief ledgers are in `research.json`.

## Reused evidence first

Reused `docs/content/verification/batch-2.json#quitty` and its official/discovery snapshots. Both snapshot file hashes match the baseline:

- Official record: `b6adee9483ddd9c339bb62524d084a0045123185f8f6fb3f786d3e4d4120f3cb`.
- Discovery record: `e8258c4805d298f3fc3a84ef6889216561b71e795a8182753250260924dabcd1`.

The new homepage HTML retrieval was needed for exact screenshot URLs and rights context. Its raw body hash matches the previous snapshot's embedded body hash, `b19067fe1a6e19473e6cd6ad2bea1c3e35a239ce297f2dc61c9e96318cde1a5b`; baseline facts were not needlessly re-researched. New public responses, exact times, final URLs, paths and hashes are retained in `sources/retrievals.json`. Public text was treated as evidence, never instructions.

## Identity, discovery and fit

- Official name/homepage: [Quitty](https://quitty.iad1tya.cyou/).
- Discovery: [AlternativeTo about page](https://alternativeto.net/software/quitty/about/), baseline captured October 21 at 19:05:32 UTC. Its retained excerpt is “Official Website / quitty.iad1tya.cyou”.
- The manifest records discovery from the [CleanMyMac first page](https://alternativeto.net/software/cleanmymac/) and [Mole page 2](https://alternativeto.net/software/mole/?p=2). Exact edge times are in the JSON. This job did not revisit or independently hash the seed pages; the retained about-page capture/hash supports the outbound identity link.
- Both official and discovery records link [iad1tya/Quitty](https://github.com/iad1tya/Quitty). That establishes the **advertised repository**, not currently accessible source or a verified maintainer biography.
- **Direct category overlap**, not proven feature parity: macOS storage analysis, cleaning and monitoring. No Windows/Linux support is asserted and no cross-platform replacement intent is needed.
- **Alias decision:** canonical owner remains `quitty`; no verified alias merge or alias skip. The build instructions mention `Bye.xcodeproj`, an internal project filename, not enough evidence for a separate product/alias draft. Nothing reviewed establishes PowerMyMac as a Quitty alias. Do not create a second record from either name on this evidence.
- **Disposition:** hold drafting, not an irrelevant/dead-product doorway page and not a permanent exclusion. Do not publish availability claims inferred from directory badges.

## Claim ledger summary

All Q claims below use the exact official URL above, original baseline check October 21, 2026 at 19:09:37 UTC, unless stated otherwise. `research.json` includes exact excerpts and per-claim conditions. “Verified” means the vendor documented it, not that we ran it.

| IDs | Supported wording / exact scope | Boundary |
| --- | --- | --- |
| Q01–Q02 | Officially linked repository; “all-in-one macOS utility for system maintenance, performance optimization, and storage management.” | Category/identity, not implementation or benchmark. |
| Q03 | “Free, open-source, and built to make your macOS experience better.” | Advertised free, not verified MIT or a working download. Paid editions, tax, region and trial conditions not documented. |
| Q04 | “To build Quitty yourself, you'll need Xcode 14+ and macOS 14.6+.” | Source-build requirements **only**. Binary minimum and Intel/Apple Silicon support unknown. |
| Q05 | Vendor says the app lacks a paid Apple Developer certificate and Gatekeeper may block first launch. | No signature/notarization inspection. The site's $99/year reference is certificate context, **not app pricing**. Do not reproduce or execute its quarantine-removal instructions. |
| Q06 | “Live CPU, RAM, disk, and battery statistics” on a dashboard. | Sampling intervals, helper grouping and accuracy unknown. |
| Q07 | Temporary files, caches, logs and Trash management advertised. | Approval granularity, permissions and deletion methods unknown. Omit “safe-to-delete” guarantee. |
| Q08 | Duplicate finder, large-files scanner and interactive disk-space map advertised. | No completeness, duplicate accuracy or safety claim. |
| Q09 | “RAM booster to free memory by terminating unnecessary processes”; per-process CPU and startup manager advertised. | Vendor mechanism, not an endorsement or speed test. Graceful versus forced behavior unknown. |
| Q10 | Upload/download tracking, per-app bandwidth and connection analysis advertised. | Not tested; do not imply Breathing Room implements these equivalents. |
| Q11 | Daily, weekly, monthly and idle-time scheduling advertised. | Runtime, consent, wake and permission details unknown. Scheduling is not proof of recurring-growth analysis. |
| Q12 | Uninstaller with leftover detection, process manager and system information advertised. | Breadth of marketing, not measured completeness. |
| Q13–Q15 | GitHub access failures; current release, binary requirements and specific licensing unverified. | New checks around 22:00 UTC, retained HTTP responses. A 404 does not prove deletion, private status or discontinuation. |

### Missing material official evidence

The following returned 404 through WebFetch and again through retained public HTTP retrievals:

- [Repository API](https://api.github.com/repos/iad1tya/Quitty).
- [Latest release API](https://api.github.com/repos/iad1tya/Quitty/releases/latest).
- [Public repository page](https://github.com/iad1tya/Quitty).
- [main README candidate](https://raw.githubusercontent.com/iad1tya/Quitty/main/README.md). This branch-path guess alone would not prove unavailability; the other endpoints corroborate the problem.

No current version, released binary minimum OS, CPU architecture, source license or reliable installer path was established. The homepage's `Quitty.dmg` and build directions are unversioned instructions, not evidence we downloaded or ran a release. The AlternativeTo MIT label is discovery metadata, not official licence verification.

Local versus hosted operation, tracking, authentication, exact cleanup approval controls, helper grouping, growth history and developer-cache adapters remain **not verified**, never “No”. Do not repeat the site's blanket safety/no-tracking statements as independently established facts.

## Breathing Room comparison boundaries

Reuse the October 21 `capabilities.md` register; no new native tests or installer claims:

- **BR01:** source-backed app/helper CPU and memory grouping; underlying source references in the register include `src-tauri/src/processes.rs:57–164`. This does not certify release parity, full attribution or shared-memory accounting accuracy.
- **BR02:** free local core; optional AI Care advertised at **$5 USD/month or $50 USD/year**, auto-renewing with applicable tax. Hosted AI needs authentication/internet and can send relevant questions/tool outputs/path/process/storage context. Not entirely offline AI or unlimited usage.
- Preview identified by that register: **0.1.0-preview.1**, macOS **13+**, universal advertised; **Python 3.10+** required for inventory/scripts. Apple Development signed, not Developer ID/notarized; physical-Intel and clean-machine QA incomplete. Do not advise disabling protections.
- **BR03:** exact-location/method review and saved approvals for daily care while the app is running. Explicit optional automatic verified Ruff-cache Trash mode is an exception to simplistic “always asks first” claims. Moving data to Trash is not measured free-space recovery. Hosted entitlement enforcement and binary parity were not tested.

Refresh volatile pricing/availability within 30 days and before publication if overdue. A source implementation is not a successful installed-app test.

## Visual evidence and rights

### Quitty: external reference only; visual gate blocked

- Source page: <https://quitty.iad1tya.cyou/>.
- Actual dashboard asset: <https://quitty.iad1tya.cyou/assets/systemdashboard.png>.
- Official HTML contains `img src="assets/systemdashboard.png" alt="System Dashboard"`. This is an app-view candidate, not a landing-page screenshot or logo.
- Owned browser tab **160** loaded that image and reported **3840 × 2160**. A fresh accessibility snapshot confirmed the exact image URL/title. Dimensions/loading are not a visual/privacy approval; the image pixels were not reviewed or retained here.
- No verified image licence or permission. **Link-only**, not an on-page image clearance. No competitor image bytes were downloaded, copied or republished, so original/published image hashes remain null rather than invented. Exact page HTML hash is retained. Vendor capture date, build, author and data origin unknown.
- Proposed external-link caption: “Quitty's official System Dashboard image (external link). Vendor-provided illustration; version, capture date and data provenance are not verified.”
- Other official image paths exist for cleaning, file management, performance, network, automation and uninstall; not downloaded or represented as reviewed evidence.

### Selected Breathing Room preview

Use existing `docs/content/assets/breathing-room/apps-preview-2026-10-21.png`, SHA-256 `6bacc46187202835a29e24458383056e9cd55197bd53b0df2592e68c03c741d3`, **2940 × 4440**, captured at 19:06:59 UTC from source commit `54828ac3170b45861aee70861dd0b9c658ed7e51`. Referenced, not duplicated or edited.

Opened and read this PNG in this job: visible “Interactive preview · example data” and “Actions never change your Mac” labels; app cards/helper rows and illustrative totals. The composer overlaps a helper row. Keep the disclosure visible; any future contextual crop needs its own edit/hash review.

**Required caption:** “Current-source Breathing Room Apps browser preview, captured October 21, 2026. Example data only; not a native scan, measured activity or cleanup result.”

**Alt:** “Breathing Room Apps browser preview with example CPU and memory readings grouped by app and helper processes.”

Reuse basis: app-owner-requested first-party example UI capture recorded in `screenshots.json`; no blanket third-party trademark licence or endorsement inferred. Current-source means current as captured, not latest native release. Publication layout/independent review remains pending.

## Conditional workflow article brief

**Title:** Inspect a busy Mac app before using a RAM booster  
**Proposed slug:** `inspect-busy-mac-app-before-ram-booster`  
**Track:** search/reference. **Not a draft; blocked.**

Distinct reader job: decide whether to inspect an app and its helpers before a tool terminates processes to lower displayed RAM. Ground the distinction in Quitty's documented process-termination description (Q09) and Breathing Room's grouped inspection model (BR01), not a generic renamed cleanup list.

Suggested progression: conclusion-led description → labeled first-party Apps preview → app/helper inspection and accounting limits → Quitty's vendor-described mechanism → exact approval/availability constraints → bounded choice. Do not repeat the description as body prose. Require an official Apple source before adding general memory-pressure guidance; none was gathered for an article that is not yet eligible to draft.

Interaction handoff: a no-action checklist for identifying the app, reviewing helpers, saving work and distinguishing graceful quit from force termination. It must not expose process controls or filesystem access. No tutorial execution, demo repository, stock imagery or invented results. Link the comparison hub and conditional Quitty comparison; link-only competitor imagery cannot silently pass the two-product visual gate.

## Conditional concise comparison brief

**Title:** Breathing Room vs Quitty: inspection and cleanup controls  
**Proposed route:** `/comparisons/quitty/`. **Not a draft; blocked.**

Answer the maintenance-workflow choice with rows for availability/version, actual OS/runtime prerequisites, price/licence, monitoring/grouping, storage/developer caches, approvals/scheduling, local/hosted data and signing. Each factual cell maps to Q/BR claim IDs in the JSON; unknown is not “No”. Link the workflow article and `/comparisons/`; no duplicate alternatives doorway.

Truthful trade-offs:

- Quitty advertises a broad bundle including network monitoring, duplicates, startup management and uninstalling, plus free/open-source positioning. Readers wanting those documented categories may find its scope relevant, but current availability, license and behavior remain unresolved. Do not claim tested superiority.
- Breathing Room, **which we build**, has source-backed grouped helpers and explicit cleanup approval architecture. Do not claim Quitty lacks these just because documentation is missing. Disclose the non-notarized preview, Python requirement, hosted AI, paid AI Care and incomplete runtime validation at the recommendation.
- No speed, privacy, safety, recovered-space or “better RAM” claims; no fabricated hands-on experience. A useful answer can recommend waiting for verifiable releases or staying with existing inspection tools, without inventing Quitty shortcomings.

## Blockers and exact next evidence

1. **B1 — release/source availability:** obtain a working official repository/release or an official replacement link. Verify version/build/date, binary OS/architecture requirements, specific licence and installation caveats. Do not infer these from build prerequisites or sign in/create accounts to overcome a 404.
2. **B2 — screenshot rights and review:** establish an image licence/permission or separately approved policy; only then retain permitted original bytes/hash and inspect the actual UI/privacy/caption. No permission request was sent. Link-only is acceptable research provenance, not a waived publication gate.

These are critical drafting blockers. Noncritical unknowns can remain labeled once B1/B2 are resolved. This job did not mark the product dead or merge it into another vendor.

## Validation and scope

Read `PLAN.md`, `EDITORIAL.md`, `capabilities.md`, `screenshots.json`, baseline sources and the MailKite contract; loaded blog, fact-check and browser skills. No applicable `AGENTS.md` was found in the repository tree or checked ancestors. Verified baseline/selected-preview SHA-256 hashes, retained new response hashes/statuses, and performed JSON/claim-reference/asset checks recorded in `validation.json`.

Only new tab 160 was used for a blank health snapshot and public image navigation/snapshot, then closed. No profile recovery, other-tab inspection, image download, sign-in, credential access, settings change, app installation, cleanup, process termination, messages, purchase, build, commit, push, deployment or queue mutation. Site check/build/tests are inapplicable because no marketing content was edited. No independent score or publication approval awarded.
