# Cleaner One Pro for Mac: research handoff

Checked **October 21, 2026** · Task `research-cleaner-one-pro-mac` · **Research only; drafting blocked; unpublished.**

## Decision

Keep this product as a **direct Mac storage-cleanup comparison**, canonical owner `cleaner-one-pro-mac`. Trend Micro's official support explicitly identifies **Trend Cleaner Pro** as a regional name: skip a separate article for that alias, not this canonical product. No verified PowerMyMac relationship exists in the corresponding baseline; this task does not modify or resolve unrelated PowerMyMac jobs.

**Blocking diagnostic:** a real official Cleaner One Pro app image was found and visually inspected, but no affirmative republication permission/licence was verified. Its status is **link-only**. Under `EDITORIAL.md`, that does not satisfy the required on-page competitor screenshot gate. Clear the rights or obtain a separately authorized alternative/policy decision before drafting. No permission request was sent and no competitor image was downloaded into the repository.

`research.json` is the detailed source/claim/visual ledger. It contains 26 supported claims, exact supporting excerpts, URLs, check dates, source hashes and explicit unknowns. Its blocked state is deliberate, not an incomplete-success claim.

## Reused discovery and identity

- Reused `docs/content/verification/batch-1.json`, record `cleaner-one-pro-mac`; corresponding baseline official snapshot hash verified. Batch 2 has no corresponding Cleaner One Pro record found in the checked index/search. No current baseline facts were needlessly fetched again from the general homepage.
- Discovery: <https://alternativeto.net/software/cleaner-one-pro-mac/about/>, retrieved `2026-10-21T19:05:48.182Z`. Raw directory snapshot and its actual SHA-256 are linked in the JSON.
- Existing CleanMyMac edge: <https://alternativeto.net/software/cleanmymac/?p=3>, retrieved `2026-10-21T18:36:26.872Z`; seed <https://alternativeto.net/software/cleanmymac/>. Directory evidence establishes discovery, not capabilities or all the listed platforms.
- Homepage: <https://cleanerone.trendmicro.com/>. Mac product: <https://cleanerone.trendmicro.com/cleaner-one-pro-for-mac/>. Publisher: Trend Micro Incorporated.
- Official repository: **not verified**; do not claim none exists. Exact applicable EULA: **not verified**. A commercial subscription is documented; the directory's proprietary label is directory evidence, not independently verified licence text.
- [Current support](https://helpcenter.trendmicro.com/en-us/article/TMKA-10020), visibly updated September 17, 2026: “In some countries, this software is called Trend Cleaner Pro.” Regional alias belongs to this canonical owner. Historical Trend Cleaner/Dr. Cleaner name continuity was not established.
- [Older edition comparison](https://cleanerone.trendmicro.com/blog/cleaner-one-apps-features/) distinguishes Lite, Cleaner One and Pro. Its Big Sur-era distribution/feature table is **not current edition-parity evidence**. Current installation support documents App Store and direct-download paths; do not silently substitute one edition's terms/features for another.

## Verified facts and boundaries

All facts below were checked October 21, 2026; IDs map to exact excerpts in `research.json`.

| Dimension | Evidence and wording boundary |
| --- | --- |
| Platform/version | Mac product specifies **macOS 10.15 and later**; purchase page adds **64-bit processor** (`compatibility`, `processor`). Current direct version/build, native Apple Silicon behavior, Rosetta, notarization and runtime dependencies: not verified. No binary downloaded/tested. |
| Storage workflow | Vendor documents Smart Scan, storage visualization, junk/large-file cleanup, duplicate files and similar photos (`scan`, `duplicates`). These are vendor-published capabilities, not our measured results or evidence every candidate is safe to delete. |
| Other tools | Startup-item management, app-file management, File Shredder and vulnerability scanning are advertised (`startup`, `app-manager`, `shredder`, `vulnerability`). Do not repeat faster/safer/irrecoverable-erasure claims as proven facts. |
| Controls | Official illustration shows selection and Remove controls; exact live approval, Trash, undo, auto-clean or restore behavior is not verified. An illustration is not a tested workflow. |
| Monitoring | The historical edition table includes Network and CPU monitor (`historical-monitor`). Current helper grouping, attribution and recurring-growth history are unknown, not “No.” |
| Developer caches | Named tool adapters/validation not verified. Generic junk cleaning does not prove npm/pnpm/Go support. |
| Local/hosted | Desktop installation documented; offline operation, telemetry, account/trial constraints and precise data flows not verified. No blanket privacy advantage asserted. |
| Platforms outside Mac | A separate Windows edition is officially linked in reused baseline. This packet compares the Mac edition; Breathing Room is not presented as a Windows app. Ignore unsupported directory tags for other platforms. |

### Pricing observation, not a universal offer

[Purchase page](https://cleanerone.trendmicro.com/cleaner-one-pro-buy/): **one-year subscription**, 1-device and 5-device choices (`annual`). HTML initially contained `...` price placeholders. The actual rendered public browser page at `2026-10-21T20:16:07.025Z` showed:

| Choice | Displayed price | Crossed-out reference | Displayed discount |
| --- | --- | --- | --- |
| 1 device, one year | $19.99 | $24.99 | 20% / $5.00 |
| 5 devices, one year | $29.99 | $59.99 | 50% / $30.00 |

Evidence: `sources/purchase-browser.txt` and `sources/purchase-observation.json` (`observed-prices`). Page language label was English (United States), but the observed Purchase Now URL contained `Locale=ru-ru`. **Do not infer ISO USD, regional eligibility, tax, checkout total, first-term conditions or renewal price** from this mismatch or from the crossed-out number. No purchase link was followed. Omit universal/cheaper pricing comparisons unless clarified independently.

[Official renewal guidance](https://cleanerone.trendmicro.com/blog/how-do-i-cancel-automatic-renewal-subscription-for-cleaner-one-pro/) documents auto-renew cancellation by purchase channel and access through the current billing period (`renewal`). No account, activation, cancellation or refund was tested. Free Download is not proof of free unlimited cleanup or a specific trial duration.

## Breathing Room comparison basis

Reuse today's `docs/content/capabilities.md`; targeted current README cross-checks matched preview, minimum OS, Python and price caveats. No native installation/cleanup test or new public-release certification was performed.

- **Free macOS maintenance preview**, macOS 13+, universal installer advertised; capability register identifies **0.1.0-preview.1** as an inspected published prerelease, not a certified newest version across every channel (`br-version`). Physical Intel and distributed binary feature parity remain unverified (`br-preview`, `br-install`). Apple Development signed, **not Developer ID signed or notarized**. Python **3.10+** is disclosed for inventory/legacy scripts. Do not suggest disabling Gatekeeper.
- Local storage/inspection and grouped process sampling are source implementations. Activity/free-space history and named developer-cache discovery are documented in inspected source (`br-growth`, `br-dev`); this does not prove complete attribution or installer runtime QA.
- Default interactive actions are reviewed, but an explicit automatic verified-Ruff-cache option exists. Daily care reuses exact saved approvals and needs the app running (`br-approvals`). Do not use an unconditional “never deletes without asking” promise.
- Hosted AI requires internet/authentication and can receive relevant inventory/tool output (`br-hosted`). Core local app is free; optional AI Care advertised **$5 USD/month or $50 USD/year** (`br-price`), renewals/tax/allowance caveats retained from capabilities. Do not turn profiles into paid tiers or claim unlimited/offline AI.
- Desktop source Apache-2.0 does not establish a licence for the hosted service or all screenshot/trademark assets.

## Visual handoff

### Competitor: real app UI, link-only

- Source page: <https://cleanerone.trendmicro.com/cleaner-one-pro-for-mac/>
- Exact asset: <https://cleanerone.trendmicro.com/images/en-us/clean-duplicate-on-mac.webp>
- App view: **Similar Photos**, visually inspected in owned Chrome page 80; 645 × 402 intrinsic pixels. Flower/landscape groups, selection boxes, All/Selected and Remove controls are visible. This is not merely a landing-page screenshot or logo.
- Browser observation time and dimensions: `sources/visual-observation.json`. Vendor capture date, product version, OS and capturer unknown. Vendor illustration, not our scan/test. Low resolution limits fine-detail readability.
- Reuse: **link-only, rights unresolved**. Product footer reserves copyright; public access is not a licence. Legal index inspected but no affirmative image reuse permission established. No original asset downloaded, so original/published paths and hashes are intentionally null, not invented. Retained page/observation evidence has hashes in `research.json`/`validation.json`.
- Proposed alt: “Cleaner One Pro Similar Photos view grouping flower and landscape images with selection controls and a Remove button.”
- Proposed caption: “Trend Micro's official Cleaner One Pro for Mac Similar Photos illustration; version and capture date not provided. Linked reference only, not our app test or measured cleanup result.” Credit Trend Micro beside any permitted future use.

### Breathing Room: selected current-source Space preview

- Existing asset: `docs/content/assets/breathing-room/space-preview-2026-10-21.png`; inventory ID `current-space-browser-preview`.
- Original SHA-256: `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a`; verified against actual bytes. 2940 × 3468. Capture `2026-10-21T19:06:45.416416+00:00`; source commit `54828ac3170b45861aee70861dd0b9c658ed7e51`.
- Opened and visually read the PNG in this job. Keep visible **“Interactive preview · example data”** and **“This browser preview uses example data. Actions never change your Mac.”** Source capture illustrates current-source UI at its capture commit, not current distributed native behavior.
- Caption: “Current-source Breathing Room Space browser preview, captured October 21, 2026. Example data only; not a native scan, measured activity or cleanup result.”
- Alt: “Breathing Room Space view rendered in a browser with illustrative example data.”
- App-owner-requested first-party UI basis retained from `screenshots.json`; no blanket third-party trademark licence. No new crop/resize, copy or published variant was made. Any later crop must preserve disclosure and record both hashes. Narrow-screen legibility needs draft-stage review; the floating composer overlaps part of the category diagram.

## Distinct workflow article brief

**Title:** Review similar photos before removing them from your Mac  
**Slug:** `review-similar-photos-before-removing-mac`  
**Track:** search/reference  
**Intent:** decide which visually similar photo candidates to retain, rather than treating all detected groups as disposable duplicates.

The lead distinguishes duplicate-file discovery from similar-photo review and says the article uses documented/vendor-illustrated behavior, not hands-on testing. Put the permitted official Similar Photos image immediately after the lead once rights are cleared. Continue with:

1. Explain the keep/review/stop decision without claiming any specific matching algorithm.
2. Inspect contents/provenance; stop where original/edit/library relationships are unclear. Do not invent a versioned click path, photo-library integration or deletion/restore method.
3. Separate selected sizes from actual available-space change; no fabricated recovery figures.
4. If the actual problem is storage growing again, introduce the source-level investigation alternative with a labeled Breathing Room Space preview and “Breathing Room, which we build” disclosure.
5. Choose based on photo-review versus repeated-growth intent, not a generic winner list.

**Interaction handoff:** a small local/no-upload keep/review/stop checklist: Have you verified the contents? Do you know which copy/edit matters? Is backup/recovery understood? Any uncertainty yields keep/review, never deletion authority. Research-stage specification only; no site widget implemented. Any Apple Photos/library/backup instructions require targeted official Apple evidence before inclusion.

Link contextually to `/comparisons/`, the product comparison and `/tools/` only where useful; verify actual destinations in drafting. Do not create a separate alias/alternatives doorway article. Earn length through decision value, not filler.

## Concise comparison brief

**Title:** Breathing Room vs Cleaner One Pro for Mac  
**Slug:** `cleaner-one-pro-mac`  
**Intent:** choose category/photo/startup cleaning versus a Mac preview focused on storage/activity investigation.

Lead with who each fits. Use a compact claim-linked matrix for platform, workflow, controls, activity, developer caches, local/hosted boundary, licence/pricing and installation. Unknown competitor cells remain “not verified.” Follow with preview/runtime and regional-offer caveats, when not to switch, then the deeper photo-review article. This is not the workflow article repeated at another URL.

### Honest advantages and trade-offs

- Cleaner One Pro is a plausible fit for its documented similar-photo/duplicate-file, startup and app-management workflows. Its published macOS minimum is earlier than Breathing Room's; actual compatibility was not tested. Do not imply Breathing Room has matching tools.
- Breathing Room's inspected source supports activity/free-space history and developer-tool discovery for repeated-growth questions. This is an editorial fit judgment, **not** proof Cleaner One Pro lacks those features, nor a performance/safety benchmark.
- Breathing Room carries non-notarized preview, Python, hosted AI, running-app and native QA limitations. Cleaner One Pro has unknown current version, approval/data-flow details and bounded pricing evidence. Neither measured savings nor a universal cheaper/faster/safer winner is supported.

## Validation and next gate

Retained official HTML/parsed excerpts and browser observations are read-only public source evidence; no accounts, cookies, hidden browser state, installers, purchases or destructive tests were accessed. Only this folder and the requested runtime receipt are written. No website, shared manifest, queue/database, PLAN or unrelated job is changed. No agents were spawned.

Run `python3 docs/content/competitors/cleaner-one-pro-mac/validate_packet.py` for retained hash/excerpt/reference/label checks. Actual outcomes are in `validation.json` and the receipt. Earlier builder schema-key and inline-whitespace assertion failures were corrected before the successful packet build; they were not app tests. No site check/build/test applies because no website file changed. No independent editorial score, rendered-article review or publication approval is claimed.

**Next authorized action:** resolve the competitor-image reuse gate without unapproved contact/signup or invented rights, then hand this packet to the separately assigned draft/review stages. Preserve noncritical unknowns or omit the affected claims.
