# Techtool Pro research

**Research status: blocked for drafting.** Micromat's Techtool Pro is relevant but adjacent: its documented job is Mac hardware/volume diagnostics and repair, not simply finding disposable storage. Breathing Room is not a verified replacement for those diagnostic tools. The required competitor app-UI visual has an official URL but no established reproduction permission; a link does not pass the on-page image gate.

Job: `research-techtool`. Evidence checked October 21, 2026 UTC (the local scheduled date is October 22). No article, website record, queue state or shared verification file was changed. `research.json` contains the claim-level ledger, exact conditions, image manifest and downstream briefs. No hands-on product tests were performed.

## Identity and existing evidence reused

- Official name: **Techtool Pro**, advertised major version **21**, by **Micromat Inc.** Listing spelling “TechTool Pro” and version label “Techtool Pro 21” belong to the same record, `canonicalOwnerId: techtool`; `skipAsAlias: false`.
- Official homepage: <https://www.micromat.com/products/techtool-pro/>. The baseline followed `http://www.micromat.com/products/techtool-pro` to this HTTPS destination. Source repository and exact current patch/build are **not verified**.
- Existing `verification/batch-2.json#techtool` and original raw captures were read first. Identity, core function, Mac fit, version, licensing models and discovery were reused, not re-researched from scratch. The additional product DOM retrieval filled missing rendered prices and image references.
- Techtool Lite is **not an alias**. The existing official-source decision quotes: “Techtool Lite focuses on essential testing and maintenance. For volume repair, deeper diagnostics, external drive testing, and advanced tools, Techtool Pro gives you complete control.” Source: <https://www.micromat.com/products/techtool-lite/>; retained in `verification/alias-decisions.json`, reviewed October 21. Keep the Pro workflow diagnostic-specific rather than duplicating Lite's scope.
- Discovery: <https://alternativeto.net/software/techtool/about/>; reused capture October 21 at 19:06:24.984Z, official destination excerpt “Official Website / micromat.com/products/techtool-pro.” The shared manifest records a Mole edge from <https://alternativeto.net/software/mole/?p=5>, retrieved 18:37:15.718Z. Raw about-page capture SHA-256: `2896f86a123f50ffc242965c012c6820dbe4a6a071658ef3a03dff9fd86471d7`. Directory evidence establishes discovery, not features.
- **Decision:** relevant adjacent Mac product; do not skip as dead/irrelevant/alias. Do not create separate capitalization/version doorway pages. No unrelated PowerMyMac identity work was done.

## Documented claims and boundaries

The official product source was verified at 19:09:45.306448Z on October 21 and retained in `docs/content/.runtime/verification-2/techtool-official.json`. Its file hash is `34913ba0e6585c9e159947401c252aac5df92ce7d420db99287b3fe0b309b94c`. This is the file hash, not the embedded text hash. New rendered DOM evidence is retained in `official-dom.json`, retrieved 22:15:52.016Z, SHA-256 `8c0528c4bde571f5174d786b802fc6d0b6e6eeeacf71f88fdf46b57a05bd3b3d`.

| Claim IDs | Supported statement | Exact support and scope |
| --- | --- | --- |
| T01–T02 | Mac diagnostics and repair; advertised Apple Silicon/Intel support | [Product](https://www.micromat.com/products/techtool-pro/): “Techtool Pro provides complete Mac diagnostics, plus a host of troubleshooting and repair tools.” Requirements say “macOS 13.5 ‘Ventura’ through macOS 27 ‘Golden Gate’.” The upper OS name/version is **vendor wording only**, not independently checked Apple release identity or tested compatibility. |
| T06 | Memory, drive, fan/sensor, file and battery testing; selectable suites | Product headings and passage: “Use the built-in Full, Intermediate or Quick suites or make your own suite of tests.” No tests run and no universal hardware coverage inferred. |
| T07 | Volume testing/repair with important APFS qualifications | [APFS support](https://www.micromat.com/apfs-support-status-13/), fetched October 21: “can validate APFS volumes using the Volume Structures test and may potentially repair APFS structure errors using the Volume Rebuild tool.” It excludes APFS File/Volume Optimization and qualifies full structural rebuild. The support article does not identify an exact current patch. FAT32/ExFAT volume support does **not** establish Windows app support. |
| T08 | Problem-cache and system database maintenance | Product: “repair important system database files, clear out problem caches.” Exact-location approval, reversibility and npm/uv/pnpm adapters remain not verified, not absent. |
| T09 | Techtool Monitor has background health monitoring | Product: “protection doesn’t stop when you close the app”; drive SMART, volume usage/APFS snapshots, CPU frequency/power, battery/UPS and configurable email alerts are described. This is not evidence of per-app helper grouping or folder-writer attribution. No email settings were touched. |

These are documentary/vendor statements, not safety, speed or recovery benchmarks. The product page itself warns that data recovery may not work in all circumstances. Do not instruct repair, erasure, initialization or defragmentation from this research packet.

## Price and license conditions

**Verified model, unresolved final numeric quote.** [Official product](https://www.micromat.com/products/techtool-pro/) offers a one-computer one-time Standard purchase with **one year of updates**, or annual subscriptions. It says: “A new license can be purchased at the end of that year to continue receiving updates.” Do not equate perpetual use with lifetime updates. Extra licenses and business options exist in cart; no cart was opened.

The public rendered page, captured October 21 at 22:15:52.016Z, displayed:

| Offer | Observed display | Conditions |
| --- | --- | --- |
| Standard | `110,00 $` | One-time, one computer; updates for one year. |
| Subscription | `80,00 $` initially; `90,00 $` annually thereafter | One computer, renews annually. Page also says “10% off first year,” inconsistent with the displayed reduction. |
| Subscription Upgrade | `67,50 $` initially; `90,00 $` annually thereafter | Says “25% off first year” and “For non-subscription Techtool Pro users”; one computer. |

Currency code is not explicit in this localized display. **Do not silently call these USD, correct the discount, calculate a saving or promise a checkout total.** Omit numeric competitor prices from downstream content until clarified; model/update conditions can be used with citations. This does not by itself require abandoning the useful non-price comparison.

[Subscription expiry support](https://www.micromat.com/what-happens-when-techtool-subscription-ends/), fetched October 21, says that from **18.1.2**, single- and three-Mac licenses “continue to function once the subscription lapses”; updates stop and a resubscription reminder appears. Do not generalize to enterprise licenses. Product-page cancel-any-time footnote applies to one- and three-user licenses.

[Sales terms](https://www.micromat.com/terms-of-service/), fetched October 21: “Your use of Micromat-branded software is on the terms of the license in effect for the software at the time of purchase.” Applicable sales tax is based on shipping address. Installed EULA, signing/notarization, runtime prerequisites, activation, trial and offline requirements remain unknown. The directory's proprietary label is not an inspected EULA.

## Breathing Room comparison evidence

Reused `docs/content/capabilities.md` and `screenshots.json`, both reviewed October 21. No new installer, cleanup or hosted-service execution occurred. Claims B01–B04 retain original public URLs and register support in JSON:

- Identified release **0.1.0-preview.1**, macOS **13+**, advertised universal installer; physical Intel/clean-machine validation uncompleted. **Apple Development signed, not Developer ID signed or notarized**; Python **3.10+** prerequisite. Do not advise disabling protections.
- Free Apache-2.0 desktop/core local tools. Source supports category/owner/project/folder/large-file inventory, grouped sampled CPU/memory, activity and constrained cleanup. Source implementation is not proof of distributed binary parity. Permission limits, sampled ownership and inferred attribution apply.
- Ordinary cleanup requires reviewed actions; optional explicit automatic Ruff-cache mode is an exception that must be named. Daily care reuses exact saved approvals **while the app runs**, not blanket future deletion authority. Trash bytes are not immediate free-space recovery.
- Authenticated hosted AI needs internet and can send relevant paths/process/storage data to the service/Cloudflare Workers AI. Do not say entirely offline. AI Care advertised **$5 USD/month or $50 USD/year**, renewing with tax; exact allowances/enforcement not verified. Website account-gated download differs from public GitHub releases.

Comparison dimensions in JSON cover platform, licensing, local/hosted behavior, scan/cleanup model, approval, helper grouping, recurring growth, developer caches and runtime. Every cell maps to claim IDs. Unknown competitor functions remain **not verified**, never negative checkmarks.

## Required visuals and blocking gate

### Techtool Pro: official app-test image, link-only

- Source: <https://www.micromat.com/products/techtool-pro/>.
- Exact image reference: <https://www.micromat.com/wp-content/uploads/2025/09/volume-structures.png>, observed in the official public DOM `data-src`, beside the Mac Drive Testing content. An additional interface illustration reference is <https://www.micromat.com/wp-content/uploads/2025/11/ttp2105-interface-layers-1024x709.png>.
- No asset bytes downloaded, no original capture date known, no invented image hash or version. Lazy-load placeholders, box art and logos are not accepted as product UI evidence. Actual asset UI, version, legibility and privacy inspection are pending.
- Reuse basis: **link-only**, not cleared for reproduction. Official footer says “All Rights Reserved”; no express image license/permission was established from the checked sources. Public availability does not license reuse. Credit: Micromat / Techtool Pro.
- Proposed link caption: “Official Micromat Volume Structures illustration linked from the Techtool Pro page; not our test. Image version and capture date are unverified.”
- **Critical blocker:** obtain documented reuse permission/press license or an explicitly approved policy decision, then retrieve permitted public bytes, preserve hashes and inspect the real image. An attributed link is a research fallback, not satisfaction of the required on-page competitor screenshot. No permission request was sent or authorized.

### Breathing Room: selected existing current-source Space view

- `docs/content/assets/breathing-room/space-preview-2026-10-21.png` — 2940 × 3468; SHA-256 `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a`.
- Original capture: October 21, 19:06:45.416416Z; source commit `54828ac3170b45861aee70861dd0b9c658ed7e51`; browser source `http://127.0.0.1:1431/`. This was reused, not recaptured.
- Opened and visually read in this job. The “Interactive preview · example data” label and “This browser preview uses example data. Actions never change your Mac.” warning are visible. The composer obscures part of the chart; contextual rendering/crop remains a later review task, not an image rewrite here.
- **Required caption:** “Current-source Breathing Room Space browser preview, captured October 21, 2026. Example data only; not a native scan, measured activity or cleanup result.”
- **Alt:** “Breathing Room Space view rendered in a browser with illustrative example data.” Keep banner/caption; numbers are illustrative, not observed storage or savings. First-party app-owner capture basis is retained from screenshot library; no third-party trademark endorsement inferred. Independent target-page review is still required.

## Distinct workflow article brief

**Proposed title:** Low Mac storage or a damaged volume? Choose the right investigation  
**Proposed slug:** `techtool-mac-workflow`  
**Track:** Search/reference workflow. **Primary job:** separate capacity/growth investigation from volume-integrity/hardware diagnosis before choosing a tool.

Lead with the distinction, not a cleanup promise. Put an approved real product visual immediately after the lead. Explain capacity versus integrity, map questions to documented tests/storage views, preserve APFS limitations, and distinguish testing from potentially destructive repair/erase functions. A later labeled Space preview explains inventory and review, never measured savings. Include a single bounded, disclosed recommendation: “Breathing Room, which we build,” can fit attribution/cleanup questions; Techtool Pro's documented diagnostic scope is the stronger fit for hardware/volume questions. No claim that one fully replaces the other.

**Interaction handoff:** a non-executing three-way decision aid (capacity -> inventory/review; recurring growth -> activity with attribution caveats; integrity/hardware concern -> backup-aware diagnostics/support). It must neither diagnose failing hardware nor run a scan, repair or cleanup. No arbitrary commands/demo repository; this is not a hands-on repair tutorial. Link the concise comparison and existing hub only after the draft job verifies actual routes.

## Concise comparison brief

**Proposed title:** Breathing Room vs Techtool Pro: storage investigation or diagnostics  
**Route intent:** `/comparisons/techtool/`; adjacent-tool decision, not duplicated workflow prose.

Use a compact claim-linked matrix, one short strengths/trade-offs section per product, accurate preview/hosted/runtime and licensing caveats, two cleared real product views and a link to the deeper workflow. No separate alternatives doorway page. Unknown cells remain not verified. Omit unresolved numeric competitor prices; disclose affiliation at recommendation.

**Honest strengths:** Techtool documents memory/sensors/battery/volume tests, repair tools and background health monitoring. Breathing Room source documents storage ownership, grouped app activity and constrained cleanup relevant to capacity questions. **Trade-offs:** qualified APFS repair/recovery, commercial/update conditions and unknown competitor install/privacy details; Breathing Room preview maturity, Python requirement, source-versus-binary limits and hosted-AI boundary. No benchmarks, ranking, safety, speedup or savings claims exist.

## Validation and handoff

- Read PLAN, EDITORIAL, capabilities, screenshot inventory, applicable blog/browser skills and adapted MailKite contract before writing. No applicable AGENTS.md found in the app tree or checked ancestors.
- Original baseline/discovery and selected first-party PNG hashes were actually checked; no shared originals were changed.
- Direct public urllib retrieval returned HTTP 403. Owned Chrome tab **173** initially timed out at navigation, then loaded the intended Micromat URL/title; read-only DOM extraction succeeded. No browser recovery or profile change was needed. Existing tabs were only listed as metadata, never read/navigated. Owned tab closed after research.
- Three targeted official support/terms WebFetch reads completed. No account, purchase, cart, message, credential/cookie extraction, installation, native test, cleanup, commit, deployment or site edits.
- Local JSON/reference/hash checks are recorded in `validation.json`; no app/site build was appropriate for this research-only packet. No independent quality score or publication approval is claimed.
- **Next stage remains blocked:** permission and actual review for the competitor UI image are required before drafting. Exact patch/EULA/install/privacy details are noncritical unknowns only if omitted or explicitly labeled. Currency/discount conflict blocks numeric price claims, not the useful model-level distinction.
