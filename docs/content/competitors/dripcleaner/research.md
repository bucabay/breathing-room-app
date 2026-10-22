# DripCleaner research — drafting blocked

Checked **2026-10-21** · Job `research-dripcleaner` · Research only, not publication approval.

## Decision

DripCleaner is a relevant, directly overlapping **Mac cleanup** product offered by [getapps.cafe](https://getapps.cafe/app/dripcleaner). Keep `canonicalOwnerId: dripcleaner`. No alias, dead-product or irrelevance skip is justified by the checked evidence. No evidence links it to PowerMyMac; do not infer an alias from similar categories. An official source repository/upstream lineage is **not verified**.

**Drafting is blocked by competitor screenshot rights.** The official gallery identifies seven app screenshot assets, but [Terms §10](https://getapps.cafe/terms) reserves rights and offers no publication licence. The exact screenshot link is retained below, not downloaded. Public availability is not permission. Obtain separately verified rights before retrieval/publication; this job authorizes no outreach. Missing minimum-OS and other noncritical facts can remain explicit unknown cells rather than invented values.

## Evidence reused, not researched again

`verification/batch-1.json` and its complete retained official snapshot supply current product facts (2026-10-21 19:08:07 UTC). SHA-256 independently matched: `e08ea82bbafeddb37562def44e92f25f2cdd968a5e01a89f8fc9ff4f2921a108`.

Discovery: [CleanMyMac page 5](https://alternativeto.net/software/cleanmymac/?p=5), retained manifest edge at 18:36:40 UTC → [DripCleaner about page](https://alternativeto.net/software/dripcleaner/about/), captured 19:06:54 UTC → official homepage above. Retained about-page JSON hash: `413f121e61723b71f6bd94808ca512f3fa6a88125ab75f45b4be0993601122c2`. Exact paths, excerpts, conditions and per-claim IDs are in `research.json`; original snapshots remain in `docs/content/.runtime/verification-1/`.

New requests were limited to official terms (missing licence, trial and rights) and one product HTML retrieval (missing gallery asset URLs). No directory re-fetch or app testing. New source retrieval dates have day precision, not invented request timestamps.

## Claim summary and comparison boundaries

All DripCleaner capability statements below are **vendor-documented, not observed**; checked October 21, 2026. JSON claims D01–D12 retain exact excerpts and source URLs.

| Dimension | Evidence and conditions |
| --- | --- |
| Identity/platform/version | [Official page](https://getapps.cafe/app/dripcleaner): macOS cleaner; **v2.2.1**, updated August 2026. Windows x64/arm64 download labels also offered. No Windows parity test and no Breathing Room Windows substitute claim. D01–D02. |
| Exploration | Space Lens: “Pure exploration - nothing here is deletable.” A distinct reason to separate looking from deleting. D04. |
| Approval | Scan items have checkboxes; some categories preselect, personal files/apps stay unchecked according to vendor. Do not simplify into manual selection of everything. D03. |
| Cleanup methods | Vendor says “Safe items go to the Trash (reversible); permanent deletes always ask first.” Not a guarantee of recovery, safety or immediate free-space gain. D08. |
| Caches | User/browser/developer caches, logs and crash reports documented; DerivedData/build caches named. Exact adapters, cache versions and rebuild costs not verified. D05. |
| Originals | Large & Old Files documents ≥100 MB files in Downloads, Documents, Movies and Desktop, descending by size. MB convention unspecified; size is not disposal permission. D06. |
| Other tools | Uninstaller, Mail Attachments, Trash Bins and Extensions listed. Not proof of comprehensive residue removal or successful execution. D07. |
| Licence/activation | [Terms §8](https://getapps.cafe/terms): personal, non-transferable, revocable subscription licence tied to active plan. Product FAQ requires getapps.cafe sign-in to activate; no activation tested. D10. |
| Price | **US$19.99 once, one device** advertised. Solo Cup **US$3.99/month** for one device or **US$1.99/month paid annually**; Family Roast **US$7.99/month** for up to five devices or **US$3.99/month paid annually**. Membership includes menu apps. Do not call $1.99 a month-to-month offer. D09. |
| Billing conditions | Terms identify USD, automatic subscription renewal and applicable taxes. Seven-day membership trial needs valid payment method and converts automatically unless cancelled. No trial/checkout entered. General subscription terms do not establish one-off lifetime updates or transfer rights. D09–D10. |
| Unknowns | Minimum macOS, Intel/Apple Silicon, notarization, runtime prerequisites, permission identity, offline/telemetry behavior, helper grouping and recurring-growth monitoring **not verified**, not “No.” D11. |

The directory's “up to $5” purchase and “$10–$15” subscription conflict with the official offer. Use the official page, explicitly scoped to the review date; do not blend or average prices. Recheck volatile offer/availability within 30 days and before publication if stale.

Do not repeat the vendor's universal cache-safety, under-a-minute, gigabytes-in-two-clicks or unrecoverable zero-overwrite promises as findings. No savings, performance, security or destructive tests were performed (D12).

### Breathing Room side

Reuse same-day `capabilities.md` rather than claiming new live tests. Claims B01–B02 point to its official page/release/privacy register and source matrix:

- **Breathing Room, which we build**, is a free Apache-2.0 **macOS 13+ preview**, identified version `0.1.0-preview.1`. Universal installer advertised; physical Intel and clean-machine behavior untested. Apple Development signed, **not Developer ID signed or notarized**. Python **3.10+** is a disclosed prerequisite.
- Local inspection/storage and app/helper grouping are source implementations, not certified distributed-binary feature parity. Optional hosted AI requires internet/authentication and can send relevant paths/process/storage outputs. Advertised AI Care is **US$5/month or US$50/year**, not a $5 app purchase.
- Source daily care requires the app running and exact saved approvals. An explicitly enabled, narrowly constrained Ruff-cache mode is an exception to blanket per-action asking language. No native test or measured result is implied.

## Visual handoff

### Competitor: official link only — gate blocked

- Source: <https://getapps.cafe/app/dripcleaner>, gallery `app-screenshots-track` and SoftwareApplication `screenshot` metadata.
- App screenshot 1: <https://files.getapps.cafe/dripcleaner-getapps-cafe-9998ed798b40f12b.png>.
- Official HTML specifically labels it “DripCleaner screenshot 1”; unlike the separate JPG OG image, this is the gallery's designated app visual. Actual image contents, dimensions, version, capture time, privacy and legibility remain uninspected.
- Reuse: **link-only**, no permission established under terms §10. No image bytes retrieved; original/published hashes intentionally null, no invented provenance. Credit: DripCleaner / getapps.cafe. Descriptive final alt must follow permitted visual inspection; the JSON's generic gallery identification is not publication-ready alt.
- A link is an acceptable research fallback, **not** the required rendered competitor-app figure. Do not hotlink as a workaround.

### Breathing Room: selected existing current-source preview

Use `docs/content/assets/breathing-room/space-preview-2026-10-21.png`, inventory ID `current-space-browser-preview`, **2940 × 3468**. SHA-256 independently matches `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a`. Captured October 21 at 19:06:45 UTC from current-source browser render, commit `54828ac3170b45861aee70861dd0b9c658ed7e51`; not recaptured in this job.

**Required caption:** “Current-source Breathing Room Space browser preview, captured October 21, 2026. Example data only; not a native scan, measured activity or cleanup result.”

**Alt:** “Breathing Room Space view rendered in a browser with illustrative example data.” Keep the example-data banner. Existing inventory records first-party capture authorization and privacy inspection; target-page review, readable cropping, third-party marks and final asset hashes still need independent review. No website copies created.

## Distinct briefs — not drafts

### Workflow article

**Working title:** Review a Mac cleanup scan without treating every large file as junk  
**Proposed slug:** `dripcleaner-mac-workflow`  
**Track:** Search/reference. **Reader job:** distinguish exploration, preselected regenerable items and original files in a scan review.

Conclusion first: inspect categories before approval; a headline reclaimable size is neither permission nor a measured result. Place the cleared DripCleaner app image directly after the lead, then:

1. Start with exploration-only Space Lens (D04).
2. Inspect Overview preselection, not just its headline (D03).
3. Separate original large files from caches with a known rebuild source/cost (D05–D06). Large is not junk.
4. Identify Trash versus permanent deletion (D08); no secure-shredder tutorial or guarantee.
5. Explain that returning growth can call for monitoring rather than repeated scans. Introduce Breathing Room only here, with affiliation and preview/hosted/runtime limits (B01–B02).
6. Use the labeled Space preview as the second product view. Add a non-destructive checklist: original/cache; restoration/rebuild known; automatic preselection/deliberate choice; Trash/permanent. No filesystem operation or invented savings calculator.

Contextual link targets: `/comparisons/` and proposed `/comparisons/dripcleaner/`; verify counterpart existence during drafting. No arbitrary code demo, forced FAQ or word-count padding.

### Concise comparison

**Working title:** Breathing Room vs DripCleaner: cleanup review or ongoing investigation  
**Proposed route:** `/comparisons/dripcleaner/`  
**Intent:** purchase/workflow decision, not the workflow article repeated.

Use compact source-linked rows for version/platform, approval/deletion, exploration/caches, activity/helper monitoring (DripCleaner unknown), account/hosted boundary, exact billing conditions and installation caveats. Link to the distinct review workflow and comparison hub. Two product UI visuals still required; rights cannot be waived.

## Honest advantages and trade-offs

DripCleaner may fit a periodic category-based scan/review and exploration workflow, with a documented uninstaller and one-device purchase option. The offer is not evidence of lifetime updates. Account activation and subscription conditions matter; undocumented monitoring does not prove monitoring is absent.

Breathing Room's source implements app/helper context, activity history and optional AI investigation, potentially relevant when space returns after cleanup. Its preview/notarization, Python, hosted-data, paid-AI and app-running constraints can make it the wrong choice for someone seeking a validated production installer or entirely offline AI. No safety, speed or savings winner is established.

## Validation and precise unblock

Actual checks: read required programme/evidence files and applicable instruction locations; reused batch-1 facts; computed official/directory/first-party PNG hashes; read official terms and public product HTML for missing conditions/assets. No browser interaction, image downloads, signups, app launch, cleanup, account access or destructive tests. Research-only files mean no marketing build/test is applicable or claimed.

**Unblock:** establish an actual screenshot reuse licence/permission through separately authorized work, then retrieve the permitted original, hash it, inspect the real UI/privacy/version and write descriptive alt/caption with provenance. Until then `draftingAllowed: false`. Independent drafting/review and rendered QA are separate jobs; no queue/database or shared site files changed.
