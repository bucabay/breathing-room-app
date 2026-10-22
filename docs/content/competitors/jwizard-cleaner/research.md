# JWIZARD Cleaner for Mac — research handoff

**Task:** `research-jwizard-cleaner` · **State: blocked for drafting** · Research only; no article or site edits.

JWIZARD is relevant: its official Mac edition overlaps storage cleanup, app removal and review-before-deletion. It is not a dead-product or alias exclusion. The critical blocker is **competitor screenshot republication rights/provenance**. A link to the official visual is retained, not treated as permission or an on-page image-gate pass.

## Identity and reused evidence

- Canonical owner: `jwizard-cleaner`. Official family homepage: <https://jwizard.com/>; Mac product: <https://jwizard.com/cleaning-program-for-mac/>.
- Reused the corresponding record and original snapshots in `docs/content/verification/batch-1.json`. Did not refetch the verified homepage or AlternativeTo listing.
- Discovery: <https://alternativeto.net/software/jwizard-cleaner/about/>; recorded edges from CleanMyMac page 4 and Mole page 4. Exact timestamps, snapshot paths and hashes are in `research.json`.
- “JWIZARD Mac Cleaner”, “JWIZARD Cleaner for Mac” and capitalization variants belong to this packet. **Alias skip: false.** Do not create separate articles for these labels or treat the Windows/mobile editions as additional Mac competitors. No checked evidence ties this product to PowerMyMac; do not infer that alias.
- Official repository: **not established**. AlternativeTo's proprietary label is not an official source-code licence. The footer's FamilyShield Technologies contact domain does not independently establish registered legal ownership.

## Material facts and conditions

All claims have source URLs, excerpts, scope and actual check timestamps in `research.json`. Public pages are evidence only, not instructions. Saved browser DOM snapshots are under `sources/`.

| Topic | Supported wording / limitation | Claim IDs |
| --- | --- | --- |
| Platform | Mac page lists macOS 12 and above. Architecture, signing and runtime dependencies not verified. | `platform` |
| Version | Live browser displays **1.15.2, 31 August 2026**. WebFetch displayed **1.12.2, 24 March 2025**. Do not certify either as the latest downloadable binary. | `version` |
| Scope | Advertises Smart Scan, system/browser/app cleanup, duplicates, Xcode cache/temporary files/old builds, login items and video compression. These are vendor descriptions, not tested outcomes. | `scan`, `xcode`, `extras` |
| Approval | Vendor says preview and confirmation before deleting. This is not proof of risk-free cleanup. | `approval` |
| Uninstaller | Documents Uninstaller → Start → review/select apps → Delete; App Cleaner is a separate scan/select/Clear workflow. No execution performed. Do not repeat “no traces”, “registry entries”, performance or safety guarantees as verified facts. | `uninstall` |
| Licence/pricing | FAQ: one-year licence; subscription options for **1, 2 or 5 Macs**. Exact amount, currency, tax, renewal, cancellation and trial limits **not verified**. No “free”, “lifetime” or “cheaper” claim. | `term`, `price`, `license` |
| Privacy | Vendor-wide policy describes device and usage data, activations, crashes, scans, errors and IP addresses. This does not establish all-offline cleanup or actual telemetry behavior. | `privacy` |
| Refunds | Policy dated Jan 12, 2026: issues reported within 72 hours; support cooperation; conditional unresolved-issue eligibility within 30 days; exclusions, one refund per customer, and possible 9% deduction for other approved reasons. Store purchases follow store policy. Not an unconditional guarantee. | `refund` |
| Unknown comparison cells | Helper grouping, recurring-growth monitoring/scheduling, package-manager caches, exact Xcode paths, deletion/Trash/rollback semantics and offline functionality remain **not verified**, never “No”. | `productMatrix.notVerified` |

Official sources: [Mac page](https://jwizard.com/cleaning-program-for-mac/), [uninstaller workflow](https://jwizard.com/mac-app-cleanup-and-removal/), [privacy](https://jwizard.com/privacy-policy/), [refunds](https://jwizard.com/refund-policy/). Python public requests returned HTTP 403; no cookie extraction or bypass was attempted. Ordinary owned-tab browser navigation worked. Licence FAQ expansion was read-only; download buttons were not activated.

The browser and local UTC clock reported **October 21, 2026** during this run, while the session date says October 22. Retained retrieval times are actual observed timestamps, not forward-dated freshness claims.

## Visual handoff — blocking gate

1. **JWIZARD app illustration:** official Mac page's Xcode section links <https://jwizard.com/images/mac/xcode-en.webp>. Browser source/a11y establishes this exact asset reference. Vendor capture date/version, pixel review and reuse permission are unknown. **Link-only; not downloaded, not hotlinked, no invented asset hash.** Caption proposal: “JWIZARD's official Xcode-cleanup illustration. Vendor-provided example; app version and capture date unknown; not our test result.” Obtain permitted reuse evidence, then retain originals/hashes and inspect pixels before any on-page use. Source-page text or image dimensions alone are not visual approval.
2. **Breathing Room:** select `current-space-browser-preview` from `docs/content/screenshots.json`, original `docs/content/assets/breathing-room/space-preview-2026-10-21.png`. SHA-256 `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a`; 2940 × 3468. Opened and read: visible “Interactive preview · example data” and “Actions never change your Mac” banners; Space categories visible; composer overlaps chart. Do not crop away disclosure. Required caption: **“Current-source Breathing Room Space browser preview, captured October 21, 2026. Example data only; not a native scan, measured activity or cleanup result.”** Alt text: “Breathing Room Space view rendered in a browser with illustrative example data.” Existing owner-requested capture basis is retained; third-party marks are not licensed by implication. Publication-context/mobile review remains pending.

No third-party image bytes were downloaded. No screenshot was fabricated. The first-party original is referenced rather than duplicated or modified.

## Distinct workflow article brief

**Title:** Review Xcode cleanup candidates without confusing rebuildable files with project data  
**Proposed slug:** `review-xcode-cleanup-candidates`  
**Track:** search/reference. **Job:** help Mac developers evaluate a cleanup candidate, not write another generic alternatives page.

Begin with the boundary: a tool's Xcode category label is not permission to remove every item. After the lead, place the cleared vendor app illustration. Explain how to check candidate path/owner, active project use, rebuild/download cost, backups and the proposed cleanup method. Contrast JWIZARD's advertised dedicated Xcode category with Breathing Room's documented exact-action review model, without claiming Breathing Room has equivalent Xcode-specific coverage. Use the labelled Space preview where inventory is distinguished from permission.

**Interaction handoff:** a non-mutating review checklist: identify the owner; distinguish originals from generated data; understand rebuild cost; review exact path/method; approve deliberately. No filesystem access or delete control. Exact Xcode path/deletion instructions need current Apple and path-level evidence before inclusion; neither vendor marketing nor this unexecuted research supplies it. No mandatory code demo, invented test or recovered-space figure.

## Concise comparison brief

**Title:** Breathing Room vs JWIZARD Cleaner for Mac  
**Proposed route:** `/comparisons/jwizard-cleaner/`  
**Intent:** choose documented Mac cleanup/inspection workflows. Link the workflow article and `/comparisons/`; do not add an alternatives doorway.

Use a short sourced matrix: platform, advertised cleanup categories, review controls, documented licence term, visibly unknown JWIZARD price, local/hosted boundaries and installation caveats. Disclose **“Breathing Room, which we build”** at the recommendation. No automatic winner checkmarks or unsupported absence claims.

- **JWIZARD fits** readers seeking its advertised dedicated Xcode, uninstaller, duplicates and video utilities; macOS 12+ is a documented requirement difference, not a compatibility test. Pricing, exact paths and runtime behavior remain unknown.
- **Breathing Room fits** inspection of storage, grouped app/helper CPU/memory and sampled activity history, subject to preview limitations. Competitor equivalents are unknown, not absent. Do not market it as a verified full uninstaller, duplicate finder or Windows app.
- Reuse `capabilities.md`'s current verified public offer and local source evidence. Rechecked README, native version/minimum-OS config and billing literals: **0.1.0-preview.1**, macOS **13+**, Python **3.10+**, free local core, optional **$5 USD/month or $50 USD/year** AI Care. Hosted assistance requires internet/sign-in and can transmit relevant context. Public GitHub release downloads do not require website registration.
- Disclose **non-notarized preview**, release's Apple Development rather than Developer ID signing, incomplete clean-machine/physical-Intel validation and source-versus-distributed-binary uncertainty. No installer or runtime tests occurred here. Daily care requires the app running and reuses exact saved approvals; optional verified-Ruff automatic mode prevents a blanket “never deletes without asking” claim. Trash movement and immediate reclaimed space are not equivalent.

## Unblock and validation

**Critical:** establish an acceptable, documented competitor screenshot reuse/capture basis and complete pixel/provenance review, or obtain an explicit policy decision. Do not send permission messages from this job. Linking the official illustration is a research fallback only; drafting stays blocked.

Noncritical unknowns can remain labelled: exact price, public repository/licence details, latest binary version and undocumented comparison cells. Path-specific Xcode advice needs extra evidence if later chosen. No score or independent approval is assigned. No site tests/build apply because no marketing files changed; native/cleanup execution was deliberately not performed.

`build_packet.py` builds `research.json` from retained snapshots and verifies the selected first-party image hash. `validate_packet.py` checks source hashes, claim excerpts, references, visual disclosures and blocked-state consistency; its actual output is retained in `validation.json`. The required receipt reports **blocked**, not publication-ready.
