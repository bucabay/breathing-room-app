# MacCleanse research: blocked before drafting

**Task:** `research-maccleanse` · **Canonical owner:** `maccleanse` · **Publication:** not authorized.

MacCleanse is a relevant, direct Mac-maintenance comparison, not a verified alias or dead product. The research retains a distinct workflow brief, but **drafting is blocked on the competitor-image gate**. [Koingo's legal page](https://www.koingosw.com/legal.php) says: “The images from this site may not be reproduced in any form without the prior written consent of Koingo Software, Inc.” No consent was obtained or requested. No competitor image was downloaded.

The machine reported `2026-10-21T21:34:26.876877+00:00` during the session labeled October 22. Evidence dates preserve actual recorded UTC dates; baseline checks have not been relabeled as new retrievals.

## Identity, fit and discovery

- **Official product:** [MacCleanse, Koingo Software, Inc.](https://www.koingosw.com/products/maccleanse/). `MacCleanse 15` is a major-version label, not another product to count. `canonicalOwnerId: maccleanse`; `skipAsAlias: false` (C01).
- No official source repository established from inspected official material. Commercial proprietary licensing is supported by [Koingo's EULA](https://www.koingosw.com/enduserlicenseagreement.php), not merely AlternativeTo (C09).
- Direct overlap: storage cleanup, result review and recurring maintenance. App uninstall/leftovers, duplicates and history erasure are documented MacCleanse jobs, not assumed Breathing Room features (C04–C05).
- No PowerMyMac relationship established. A customer testimonial spelling “MacClean” is not proof of an official alias. No global alias queue record was changed.
- [AlternativeTo discovery](https://alternativeto.net/software/maccleanse/about/) was already captured at `2026-10-21T19:08:55.016Z`; exact official link, raw snapshot and hash are retained in `research.json`. Discovery edges: [CleanMyMac page 4](https://alternativeto.net/software/cleanmymac/?p=4) and [Mole page 5](https://alternativeto.net/software/mole/?p=5). Original page capture paths, UTC times and hashes are recorded, not re-fetched.
- This is a Mac comparison. The vendor's site-wide “Windows (when applicable)” language does not establish a Windows MacCleanse edition or Windows support for Breathing Room.

## Evidence retained and gaps closed

`research.json` is the per-claim source ledger: C01–C11 for MacCleanse, B01–B04 for Breathing Room, with exact URLs, excerpts, check dates, states, conditions and intended placements. Every factual matrix cell maps to claim IDs; unsourced cells explicitly say **not verified**.

Reused `docs/content/verification/batch-1.json#maccleanse` and the original official snapshot, SHA-256 `5706b9283caefe616c82fbb8b000f728181f1337fd3bbecc8303bbe0c7d3bba7`. No matching batch-2 record was found. The current baseline was not needlessly refreshed. New official checks were limited to the missing EULA, legal policy, manual and a targeted homepage-HTML request for screenshot links. New source excerpts are retained in the JSON; exact fetch seconds and raw HTML hashes were not recorded, rather than invented.

### Version/platform and offer boundaries

The retained [official page](https://www.koingosw.com/products/maccleanse/#versionhistory) lists **15.0, released August 29, 2026**, with a numeric **macOS 11 minimum** (C02). Its current-retail statement advertises Apple Silicon/64-bit compatibility and non-sandboxed retail apps (C03). These are vendor statements, not installation tests. Current Intel binary details, notarization and runtime prerequisites remain unverified.

The earlier record's “Optimized for macOS 26 Tahoe” excerpt belongs to **14.5**, not 15.0. Older tables also label macOS 11 as Ventura, while v15 notes call it Big Sur and make a macOS 27 “Golden Gate” assertion. Use the version-scoped numeric minimum; do not silently validate the vendor's Apple naming or infer an upper compatibility bound.

[Solo pricing](https://www.koingosw.com/products/maccleanse/#ordering), checked in the retained October 21 snapshot: **$29.95 this version only**, **$119 lifetime updates**, or advertised **$1.83 per month**; **one computer/user**, **five unique devices per year** (C08). Currency code, exact billed annual subscription amount, tax, renewal and trial duration are not established. Do not imply monthly billing, unrestricted devices or total-cost superiority. Hidden uninitialized `$0.00` order-modal values are not prices. No checkout was attempted.

### Review and scheduling are not unconditional approval guarantees

Koingo advertises reviewable scan details and daily/weekly/monthly scans (C05). Its [undated manual](https://www.koingosw.com/products/maccleanse/manual.php) explicitly says that checking/unchecking results **does not change saved scan settings** (C06). This is a useful documented distinction, not proof of current v15 click paths.

The same manual describes “Skip right to erasing...” and also says it will never remove files without prompting. This conflict blocks an unconditional “always asks first” claim (C07). Its “Words of Caution” section says large/old files are not automatically disposable (C11). Do not repeat blanket all-caches-safe, performance or guaranteed secure-erasure claims. No cleanup, benchmark or hands-on usage occurred.

## Comparison handoff

| Dimension | MacCleanse | Breathing Room, which we build |
| --- | --- | --- |
| Platform | 15.0, published macOS 11 minimum; precise upper compatibility unverified (C02–C03) | 0.1.0-preview.1, macOS 13+; physical Intel runtime untested (B01) |
| Scan/cleanup job | Vendor documents histories/cookies/caches, app leftovers, uninstalling and duplicates (C04) | Source-supported storage ownership/context, developer-cache discovery and activity/process views; not feature parity (B03) |
| Review | Results review documented; skip setting and conflicting manual wording require qualifications (C05–C07) | Exact approval architecture, with opt-in narrowly verified Ruff-cache automatic Trash exception (B04) |
| Recurrence | Daily/weekly/monthly scans and automatic cleanup advertised; growth history not verified (C05) | Activity implementation; saved exact daily approvals while app remains running (B03–B04) |
| Process/helper grouping | Not verified; login-item controls do not establish sampling | Source-supported sampled grouping, not forensic attribution (B03) |
| Pricing | Solo dollar-denominated offers above; billing/currency conditions unresolved (C08) | Free local core; optional AI Care $5 USD/month or $50 USD/year (B02) |
| Licensing/network | Commercial proprietary EULA; fully offline operation and product-specific telemetry not verified (C09) | Apache-2.0 desktop source; hosted AI separate, online and authenticated (B02–B03) |
| Installation | Retail non-sandboxed per vendor; signing/runtime details not verified (C03) | Non-notarized preview, Python 3.10+, partial inventories possible (B01) |

Breathing Room evidence reuses `docs/content/capabilities.md` and its public-page/release checks; local README requirements, `src-tauri/tauri.conf.json` version/minimum and billing amounts were cross-checked. This does not prove source-to-distributed-installer parity. Direct public GitHub downloads do not require the website account. Hosted assistant traffic is not entirely offline. Do not promise unlimited AI, production readiness, safety, speed or measured reclaimed space. Trash movement and increased available space are different measurements.

**MacCleanse advantages:** the documented histories/app-removal/duplicates suite, configurable presets and recurring scans; advertised non-subscription options. **Trade-offs:** current automation defaults and complete billing conditions are not verified; the manual's review language conflicts; image reuse requires consent.

**Breathing Room fit:** source-supported storage/process/activity context and developer-cache investigation, plus daily exact saved approvals. **Trade-offs:** preview/notarization/Python/Intel caveats, hosted AI data/authentication boundary and no established feature parity with MacCleanse's uninstall/duplicate/history functions. Unknown competitor features must never become negative checkmarks.

## Visual handoff: link-only is not a pass

### MacCleanse app image

- Source: [official product page](https://www.koingosw.com/products/maccleanse/).
- App-image URL: [Cleanup screenshot](https://www.koingosw.com/products/maccleanse/screenshots.carousel/full/1-cleanup.jpg); alternate [app uninstall screenshot](https://www.koingosw.com/products/maccleanse/screenshots.carousel/full/2-appsuninstall.jpg).
- These are actual screenshot links in official HTML, not generated UI or a landing-page capture. Pixels, depicted version, capture date, dimensions and data origin have **not** been reviewed.
- Reuse: **link-only**, due to the explicit [written-consent requirement](https://www.koingosw.com/legal.php). No download, crop, derivative or rehosting. Original/published hashes and local paths are null because no image bytes were retrieved.
- Proposed link caption: “Official MacCleanse Cleanup screenshot (external link). Vendor-supplied image; capture date, depicted version and data origin unverified. Not our hands-on test.”
- Required unblock: documented prior written consent or another independently authorized compliant image source, then permitted retrieval, original hash/provenance, actual pixel/privacy review and final publication hash. Do not send a permission request from this scheduled job or assume fair-use clearance.

### Selected Breathing Room view

Reuse `docs/content/assets/breathing-room/space-preview-2026-10-21.png`, **2940 × 3468**, current at captured source `54828ac3170b45861aee70861dd0b9c658ed7e51`. SHA-256 checked against the screenshot register: `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a`.

**Required caption:** “Current-source Breathing Room Space browser preview, captured October 21, 2026. Example data only; not a native scan, measured activity or cleanup result.”

**Alt:** “Breathing Room Space view rendered in a browser with illustrative example data.” Keep the visible example-data banner. First-party owner-requested capture; third-party marks remain their owners' marks. Prior library visual/privacy inspection is reused, not claimed as a fresh inspection. Final-page responsive legibility, crop suitability and independent review remain pending. No asset was copied or edited here.

## Distinct workflow article brief

**Title:** Keep a MacCleanse result selection separate from your saved cleanup preset  
**Slug:** `maccleanse-results-selection-versus-saved-presets`  
**Track/intent:** Search-reference explanation of one-run selections versus saved scope and future maintenance; not a renamed full comparison or an untested click-by-click tutorial.

Lead with the documented distinction (C06). Place a rights-cleared official Cleanup view immediately after the lead. Then explain three separate decisions: saved scan scope, this run's selected results and scheduled authority. Include the large/old-file caution (C11), the conflicting skip/prompt language (C07), and unknown v15 UI parity. Finish with a bounded comparison to Breathing Room's exact saved approvals, affiliation and preview/hosted caveats. Use the example-data Space view later, with its full caption.

**Interaction handoff:** a non-mutating three-column checklist for saved scope / one-run selection / scheduled authority. No cleanup code, filesystem access or settings writes. This research stage proposes the decision aid; it does not implement one or claim draft interaction QA.

Contextual planned links: `/comparisons/`, `/comparisons/maccleanse/`. No assumed tool route, invented keyword metrics, FAQs, savings anecdotes or companion repository.

## Concise comparison brief

**Title:** Breathing Room vs MacCleanse: saved approvals or a cleanup suite?  
**Route intent:** `/comparisons/maccleanse/` chooses between workflows, with the concise matrix above and the article link `/blog/maccleanse-results-selection-versus-saved-presets/`.

Lead with MacCleanse's documented history/app cleanup and presets, versus Breathing Room's source-supported storage/process investigation and saved approvals. Disclose “Breathing Room, which we build.” Include the competitor's strengths, pricing conditions, approval conflict and our preview/hosted/Python constraints. No total-cost, performance or safety winner. No separate duplicate alternatives doorway page.

## Gate and validation outcome

- Identity, discovery provenance and qualified source packet are established; this is not a dead/alias skip.
- **Drafting blocked:** no consent for the required competitor app visual; URL-only fallback and unreviewed pixels do not clear the gate.
- Noncritical unknowns may remain only if clearly marked or omitted: exact subscription currency/bill, trial length, runtime/signing, feature coverage and upper OS compatibility. Any stronger related claim needs fresh evidence first.
- No native test, browser workflow, cleanup, account, credential access, purchase, settings change, message, deployment, commit or queue mutation performed. Browser skill was loaded, but no browser interaction was needed.
- Structured validation results and artifact hashes are retained in `validation.json`. Website build/tests are not applicable because no site content changed. Independent draft/render review remains a separate stage; no score or publication approval is awarded here.
