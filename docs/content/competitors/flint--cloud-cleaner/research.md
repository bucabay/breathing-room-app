# Flint — research handoff

Checked **October 21, 2026**. Research only. **Blocked for drafting: competitor screenshot reuse and visual review unresolved.** No site, queue, app or account changes; no installs, cleanup, purchases or messages.

## Identity and fit

Canonical owner: `flint--cloud-cleaner`. Official homepage: https://oleksiimazurenko.dev/en/flint . Developer: Oleksii Mazurenko. “Flint,” “Flint - Cloud Cleaner” and “Flint: Local Cloud Cleaner” refer to the same identity: the retained AlternativeTo listing links the developer homepage and App Store ID `6760926077`, and that store listing links back. **Skip separate alias drafts, not this canonical product.** No evidence in this identity chain connects Flint with PowerMyMac; do not merge them by assumption.

Official direct-release repository: https://github.com/oleksiimazurenko/flint-releases . Its description is “Flint — Cloud Cleaner for macOS. Direct download releases (.dmg).” A source-code repository is **not verified**; API `license: null` is not itself a licence determination.

**Adjacent Mac product**, not an interchangeable general cleaner. Its documented task is inspecting local cloud-file copies and evicting those copies, with provider sync-state indicators. Breathing Room's broader storage/process/activity investigation is a different task. Neither documented cloud-copy eviction parity in Breathing Room nor general-cleanup parity in Flint was established. No Windows support or non-Mac replacement story invented. Product is not dead or irrelevant and is not skipped.

## Reused evidence and new checks

First reused the corresponding `docs/content/verification/batch-1.json` record, its official-page snapshot and directory snapshot. Those were checked the same day; identity and basic functionality did not need fresh verification. Discovery timestamp: **2026-10-21T19:07:11.031Z**; official snapshot timestamp: **2026-10-21T19:08:04.344309+00:00**. The directory's original traversal pagination is unknown in this corresponding record; no seed page invented.

New retrievals filled material gaps: developer terms/privacy, US App Store offer/compatibility/version, GitHub release and repository metadata, and homepage **image markup** missing from the inherited text snapshot. Exact URLs, excerpts, channel conditions, timestamps, retained files and hashes are in `research.json`, `sources/*.meta.json` and `validation.json`. Public pages were treated only as untrusted evidence.

## Claim-level findings

| Claim | Finding and boundary | Official evidence / excerpt |
| --- | --- | --- |
| F02–F03: workflow | Developer documents cloud-copy space inspection, eviction, sync states and a treemap across iCloud Drive, Google Drive, OneDrive and Dropbox. Not our runtime observation or guarantee of preservation. | [Homepage](https://oleksiimazurenko.dev/en/flint): “Removes local copies in one click. Files stay safe in the cloud, untouched.” |
| F04: selection | Listing documents batch selection/eviction and filters. Confirmation prompts, unsynced-file protections and rollback remain unverified. | [US App Store](https://apps.apple.com/us/app/id6760926077?mt=12): “Batch Operations — select multiple files and evict them all at once.” |
| F05: price | **Free download with in-app purchases; Lifetime Access $14.99 USD**, US storefront. Browser expanded the public “In-App Purchases” disclosure; retained before/after snapshots. No purchase initiated. Free limits, taxes, direct-build price and detailed lifetime entitlements unknown. | Same store URL; “Free · In‑App Purchases”; expanded “Lifetime Access” / “$14.99”; HTML offer currency `USD`. Directory $15 is a rounded discovery claim, not the exact official offer. |
| F06: App Store scope | **macOS 14.0+**, version **1.37.0**, October 21, 2026 entry. Architecture not verified. | Same store URL: “Requires macOS 14.0 or later.” / “Version 1.37.0”. |
| F07: direct channel | **v1.37.1**, published **2026-10-20T07:28:19Z**, with `Flint.dmg`. Not downloaded or installed. Do not silently conflate this channel with the store version. | [Official release API](https://api.github.com/repos/oleksiimazurenko/flint-releases/releases/latest), [versioned release](https://github.com/oleksiimazurenko/flint-releases/releases/tag/v1.37.1). |
| F09: licence | Personal, non-exclusive, non-transferable, revocable application-use licence on Macs owned/controlled by the user; subject to developer terms and Apple EULA. Not an open-source or image-reuse grant. | [Terms](https://oleksiimazurenko.dev/en/flint/terms), updated March 2026: “a personal, non-exclusive, non-transferable, revocable license”. |
| F10: local/hosted | Developer policy states local scanning/analysis/cleanup, no app account, analytics or telemetry. Attribute as policy; no network audit. Cloud-provider syncing is outside this assertion. | [Privacy](https://oleksiimazurenko.dev/en/flint/privacy), updated March 2026: “All file scanning, analysis, and cleanup operations are performed entirely on your device.” |
| F11: Breathing Room | Reuse same-day capabilities register: broad preview-source storage/process/activity and developer-cache work, not binary parity. Free local core; hosted AI requires authentication/internet; AI Care advertised $5 USD/month or $50 USD/year. | `docs/content/capabilities.md`, which retains current code and public-source citations, including [homepage](https://breathing-room.chatic.ai/) and [preview release](https://github.com/bucabay/breathing-room-app/releases/tag/v0.1.0-preview.1). |

All claims checked October 21, 2026. Refresh volatile offers/availability within 30 days and before publication if stale. No benchmark, savings figure, app test, independent privacy audit or quality score is claimed.

### Comparison guardrails

- Flint helper grouping, historical growth monitoring and developer-cache cleanup: **not verified**, not “No.” Sync-state reporting is not automatically a historical disk-growth monitor.
- Flint direct-build OS, CPU architecture, signing/notarization and runtime prerequisites: not verified. Store minimum OS must not silently cover the direct DMG.
- Breathing Room `0.1.0-preview.1`: macOS 13+, advertised universal installer, Python 3.10+ inventory prerequisite; release disclosure says Apple Development signed, not Developer ID signed/notarized. Physical Intel/clean-machine execution remains unverified.
- Breathing Room approvals are qualified: optional verified Ruff-cache automatic Trash mode exists; daily care uses saved exact approvals while the app runs. Do not promise unconditional approval before every action.
- Local size, files moved to Trash and newly available disk space are different quantities. Never portray example screenshot numbers as results.

## Visual manifest and blocker

### Flint: official app-image reference, link-only

- Source: https://oleksiimazurenko.dev/en/flint . Exact app asset: https://oleksiimazurenko.dev/flint-preview-1.webp . Other official markup references previews 2–4, but no extra visual coverage is inferred.
- Official alt description: “Flint — all cloud storages on one space map, with the space that can be freed.” HTML declares 2000 × 1255; not an independent dimension or content inspection.
- Source-page markup retrieved **2026-10-21T20:38:42.160161+00:00**; image retrieval/capture date, creator of capture, app version and original image hash **unknown**. Owned browser tab confirmed public image URLs; retained `sources/browser-homepage-visuals.json`.
- Footer says “© 2026 Oleksii Mazurenko. No rights reserved.” Application terms separately grant limited app use. No image-specific permission or explicit scope for the embedded app imagery was established. **Reuse: link-only, not cleared. No image downloaded or republished.** A public URL is not sufficient permission.
- Proposed caption: “Official Flint cloud-storage map preview supplied by the developer; version, capture date and example-versus-measured data not verified. Not our hands-on test.”
- Proposed alt: “Developer-supplied Flint preview described as a cloud-storage space map.” Revise after actual image inspection.

**B01, critical:** This link-only research fallback does not satisfy the required on-page competitor screenshot gate. An authorized licence/permission basis or explicit editorial policy decision is needed, followed by permitted original download/hash retention, visual/privacy inspection and contextual review. Do not send permission requests from this job or silently waive the gate.

### Breathing Room: selected current-source preview

Selected `current-space-browser-preview` from `docs/content/screenshots.json`, at `docs/content/assets/breathing-room/space-preview-2026-10-21.png`. Capture: **2026-10-21T19:06:45.416416+00:00**, current-source commit `54828ac3170b45861aee70861dd0b9c658ed7e51`, 2940 × 3468. Original SHA-256: `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a`.

Opened and read this actual PNG during this job: Space navigation, category chart/list and **Interactive preview · example data** plus browser-preview warning are visible. Assistant composer overlaps part of the chart. First-party app-owner-requested example UI reuse basis inherited; no blanket trademark licence inferred. Do not edit labels/numbers, remove disclosures or imply native behavior. No publication asset was created; independent article-context review remains pending.

Required caption: **“Current-source Breathing Room Space browser preview, captured October 21, 2026. Example data only; not a native scan, measured activity or cleanup result.”**

Alt: “Breathing Room Space browser preview with example storage categories and a visible example-data warning.” It illustrates broader investigation, not cloud-eviction support or measured results.

## Distinct workflow article brief

**Proposed title:** Local cloud copies or ordinary files? Plan a Mac space review before eviction  
**Proposed slug:** `review-local-cloud-copies-before-eviction`  
**Track:** Search/reference. **Intent:** understand whether cloud-copy eviction actually matches the storage problem before treating ordinary local files or caches the same way.

Lead with the bounded distinction, not “best cleaner” rankings. Place the cleared official Flint app visual immediately after the lead. Describe documented treemap/sync-state/filter/selection workflow without claiming to have used it. Add a preflight decision checklist: identify provider, establish sync completion and cloud-copy availability, decide which files are needed offline, stop if uncertain. This is editorial guidance, not a claim Flint enforces those safeguards. Provider-specific operating instructions require new official provider/Apple procedural sources before drafting; none are claimed verified here.

Use the labeled Breathing Room Space illustration later to show why a cloud-copy view and broader storage investigation answer different questions. One bounded recommendation: Flint for its documented cloud-file focus; Breathing Room, **which we build**, for broader preview-source investigation, with all preview/runtime/hosted-AI caveats. No equivalence claim for cloud eviction. Link `/comparisons/` and the proposed `/comparisons/flint--cloud-cleaner/`; these are planned targets, not verified existing routes.

**Interaction handoff:** A local decision checklist, not a forced code demo: cloud folder → sync state known → cloud copy available → offline need assessed. An uncertain answer means stop. No cleanup APIs, uploaded paths, invented savings calculator or live account access. This brief is not a draft or implemented interaction pass.

## Concise comparison brief

**Title:** Flint vs Breathing Room: cloud-copy eviction or broader Mac investigation?  
**Slug:** `flint--cloud-cleaner`. Answer who each fits, then use `research.json`'s claim-linked matrix for platform/channel, offer/licence, local/hosted boundary, cleanup model, controls and honestly unknown cells. Disclose “Breathing Room, which we build.” Link the deeper workflow and hub. Keep `draft`, unpublished, until visual gate and independent QA pass.

### Truthful advantages and trade-offs

- **Flint fit:** documented four-provider view, sync states, treemap and batch local-copy eviction (F02–F04). Its local-processing/no-account policy is relevant but not independently audited (F10).
- **Flint boundaries:** free download is not unlimited free eviction; lifetime entitlements/free limits/direct pricing unknown (F05). Store macOS 14+ is a constraint (F06). Neither wider maintenance parity nor guaranteed loss prevention is established.
- **Breathing Room fit:** source-documented wider storage, helper/process and activity investigation may fit questions outside cloud-copy storage (F11); do not upgrade this to tested release behavior.
- **Breathing Room boundaries:** preview/notarization/runtime limitations, Python prerequisite, hosted authenticated AI and optional AI Care pricing; cloud-copy eviction parity not established (F11).

## Handoff

Only this product folder and the required receipt are outputs. Research JSON, retained sources, browser disclosure snapshots, selected-preview hash and actual structural checks are retained. No website build is necessary or claimed: no site file changed. No independent publication review performed. **Blocked** means the scheduled drafting stage must not proceed solely on this packet.
