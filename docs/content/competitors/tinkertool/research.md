# TinkerTool research — blocked for drafting

Review date: **October 22, 2026**. Actual source retrieval timestamps are October 21 UTC, retained without alteration. Research only; no article, site change, installation or hands-on product test.

## Decision

**TinkerTool is adjacent, not a direct storage-cleanup substitute.** It exposes personal preference settings already built into macOS. Keep canonical owner `tinkertool`. Treat “TinkerTool 11” and historical generations as this family, not separate doorway articles. **TinkerTool System is a distinct, complementary administrator tool**, not TinkerTool's paid tier. No evidence ties PowerMyMac to this identity; that example alias must not be imported.

**Drafting is blocked:** the official Finder screenshot page and asset URLs are established, but republication permission is not. Keep the competitor image link-only. Public availability is not a reuse licence. Resolve with explicit rights evidence or an independently authorized policy decision; do not email the vendor or silently waive the visual gate.

## Reused evidence and provenance

- First reused `docs/content/verification/batch-2.json` → `tinkertool`: identity, homepage, preference purpose, current-generation OS list and free download. The already-current homepage was **not re-fetched**.
- Official homepage: <http://www.bresink.com/osx/TinkerTool.html>. HTTPS equivalent: <https://www.bresink.com/osx/TinkerTool.html>. Publisher: Marcel Bresink Software-Systeme, corroborated by the official contact page. Official source repository: **not verified**, not “none exists.”
- Discovery: Mole seed <https://alternativeto.net/software/mole/>, page <https://alternativeto.net/software/mole/?p=2>, retained manifest edge dated `2026-10-21T18:37:09.298Z`; then <https://alternativeto.net/software/tinkertool/about/> → official homepage. The about-page capture is dated `2026-10-21T19:06:28.610Z`, SHA-256 `7888a6617f54f74c1514ceb0dc4a278d1eae6aff44ed4587e301da17e8535573`. Original pagination snapshot was not independently rehashed here. Directory “System Cleaner” categorization does not establish cleanup functionality.
- Official baseline capture: `docs/content/.runtime/verification-2/tinkertool-official.json`, retrieved `2026-10-21T19:09:47.888052+00:00`, actual file SHA-256 `ecb2c4e2dffeca53868678fc91ae4e62ba753c3864a27d6524efd960012487d1`. Its internal `sha256` property is not the file hash; preserve this distinction.
- Seven missing-detail official pages retained as unmodified HTML under `sources/`, with exact URLs, final URLs, UTC retrieval times and original-byte hashes in `sources/ledger.json`. Per-claim excerpts/check dates, intended locations, conditions and source IDs are in `research.json`. No public content was treated as instructions.

## Material facts and conditions

| Claim | Evidence and boundary |
| --- | --- |
| TT01: Personal macOS preference interface | Reused homepage: “access to additional preference settings Apple has built into macOS.” Documentation, not observed app behavior. |
| TT02: 11.71, build 260910, September 14, 2026 | [Download page](https://www.bresink.com/osx/0TinkerTool/download.php): version/build, date, 5.4 MB and “Notarized macOS Disk Image (DMG).” Vendor statements; no download, checksum/signature inspection or installation. |
| TT03: OS-specific generations | [Version overview](https://www.bresink.com/osx/TinkerToolOverview.html): current TinkerTool for macOS 26 Tahoe / 27 Golden Gate; TinkerTool 10 version 10.6 for macOS 13/14/15. These are vendor labels, not independent Apple release verification. Never describe current 11.71 as simply “macOS 13+.” CPU architecture unverified. |
| TT04: No-charge download, restricted redistribution | Download page: “You can download ... at no charge”; “Distributing the software without prior written permission is prohibited.” No currency, subscription interval or open-source licence inferred. Full EULA not established; software restrictions do not themselves settle screenshot rights. |
| TT05: Current-user scope/reset | Reused homepage: no administrative privileges needed; settings can reset to Apple defaults or prior state. Do not turn into guaranteed safety or file backup. |
| TT06: Separate from TinkerTool System | [Details](https://www.bresink.com/osx/0TinkerTool/details.html), distinction section: different audience and features; “they complement one another.” Do not borrow System's cleanup capabilities or licence prices. |
| TT07: Finder visibility and network preferences | Details table includes showing hidden/system files and disabling creation of hidden Finder `.DS_Store` files on network volumes. Neither establishes permission to delete hidden files or removal of existing `.DS_Store` files. |
| TT08: Permissions and persistent settings | [FAQ](https://www.bresink.com/osx/0TinkerTool/issues.html): protected Mail/Safari/Time Machine preferences can require Full Disk Access; changed preferences persist after app removal. Reset/log-out guidance is documented, not executed here. Do not prescribe broad permissions for a Finder-only task. |
| TT09: Preference export/import | Details: eligible settings can transfer between accounts/computers; third-party-dependent settings excluded from the stated transferable set. Not a full backup or migration test. |

The feature table varies even within macOS 26. The workflow must not promise every preference is available on every OS point release. The FAQ's opening “no known issues” is not evidence of no bugs; later FAQ sections document interactions and limitations.

## Breathing Room comparison basis

Reuse yesterday's `docs/content/capabilities.md` and its source/release/pricing citations, not fresh performance claims:

- **BR01:** identified `0.1.0-preview.1`, macOS 13+, universal installer advertised; physical Intel and clean-machine runtime unverified. Apple Development signed, **not Developer ID signed or notarized**. Python **3.10+** prerequisite for inventory/legacy scripts, not bundled. [Release](https://github.com/bucabay/breathing-room-app/releases/tag/v0.1.0-preview.1).
- **BR02:** source implementations for storage views, app/helper CPU-memory grouping, activity and constrained cleanup. Source is not binary parity. Default interactive review, optional verified Ruff-cache automatic Trash mode and exact saved daily approvals must not be flattened into “never deletes without asking.” Daily care needs the app running. Size, Trash movement and free-space changes differ.
- **BR03:** free local core and Apache-2.0 desktop source; optional advertised AI Care **$5 USD/month or $50 USD/year**, renewing until cancelled, applicable tax at checkout. [Pricing](https://breathing-room.chatic.ai/#pricing). Hosted AI needs internet/authentication and can receive paths/process/storage context; not entirely offline. [Privacy](https://breathing-room.chatic.ai/privacy/). Paid limits/enforcement and checkout success unverified. Website download account gate differs from public GitHub release access.

For TinkerTool, storage scanning, helper grouping, recurring-growth monitoring and developer-cache deletion are **not verified**, not negative checkmarks. Its documented preference task is sufficient to explain adjacent fit. Local preference editing does not establish no telemetry or no network requests. No Windows/Linux support invented.

## Required visual handoff

### Competitor: source established; rights blocked

- Source: <https://www.bresink.com/osx/0TinkerTool/screenshots.html>, retained HTML checked `2026-10-21T22:17:28.125866+00:00`.
- Real app-UI asset: <https://www.bresink.com/osx/0TinkerTool/Images-en/1-Finder@2x.jpg>; fallback <https://www.bresink.com/osx/0TinkerTool/Images-en/1-Finder.jpg>.
- Vendor caption: “Settings for the Finder (macOS 26.0).” Declared 1x display size 824 × 668; actual image bytes/dimensions, capture date and exact app version unknown.
- Proposed alt: “Vendor illustration of TinkerTool Finder preference controls on macOS 26.0.” Caption must state official vendor illustration, unknown capture/version and not our test.
- Credit: Marcel Bresink Software-Systeme. Reuse **link-only**. The [contact/rights page](https://www.bresink.com/info.html) discusses licensed third-party graphics, not a grant to republish product screenshots. Neither it nor the checked screenshot page establishes permission. **No image downloaded**, therefore original/published asset hashes are honestly null. No image visual approval claimed.

### Breathing Room: selected existing current-source preview

- Select `current-space-browser-preview` from `docs/content/screenshots.json`.
- Existing path: `docs/content/assets/breathing-room/space-preview-2026-10-21.png`; SHA-256 `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a`; 2940 × 3468. No copy, crop or site asset created.
- Captured `2026-10-21T19:06:45.416416+00:00`, source commit `54828ac3170b45861aee70861dd0b9c658ed7e51`, browser URL `http://127.0.0.1:1431/`. Current to that source snapshot, not proof of current distributed binary behavior.
- Required caption: **“Current-source Breathing Room Space browser preview, captured October 21, 2026. Example data only; not a native scan, measured activity or cleanup result.”**
- Alt: “Breathing Room Space view rendered in a browser with illustrative example data.” Keep the example-data banner visible. First-party owner-requested capture; third-party marks remain their owners' marks. Per-page crop, responsive legibility and independent review pending. Existing library visual review is reused, not claimed as a new review here.

## Distinct workflow brief

**Title:** Showing hidden files is not a Mac cleanup plan  
**Proposed slug:** `tinkertool-finder-preferences-versus-storage-cleanup`  
**Track:** Search/reference. **Intent:** distinguish visibility/network-folder preferences from disk-space investigation.

Lead with the distinction: TinkerTool changes personal Finder preferences; seeing hidden files does not make them disposable. After the lead, place the licensed official Finder visual once cleared. Then:

1. Choose the correct TinkerTool generation for the exact OS, not a generic minimum-version claim.
2. Separate showing files, preventing network `.DS_Store` creation and deleting existing data. Do not supply deletion commands or imply recovered space.
3. Explain recording/resetting changes and why app removal is not rollback.
4. When the real question is disk growth, discuss an inventory and qualified ownership/activity context. Introduce “Breathing Room, which we build” only here, with preview/runtime/hosted boundaries.
5. Include the labeled Space preview and a non-mutating decision checklist: appearance/visibility → preference tool; current usage → inventory; recurring growth → qualified activity investigation. No invented measurements, settings execution or forced code demo.

Link the concise comparison and `/comparisons/`; a relevant storage planning tool only if the drafting job verifies its route and usefulness. No compulsory FAQ, duplicate alternatives route or padded word-count target.

## Concise comparison brief

**Title:** TinkerTool vs Breathing Room: different Mac jobs  
**Route proposal:** `/comparisons/tinkertool/`  
**Intent:** choose the job, not a false replacement ranking.

Use the claim-linked matrix in `research.json`: purpose, exact OS/generation, price/licence, local/hosted boundary, scan/cleanup scope, controls, helper/growth/cache unknowns and installation caveats. Two properly sourced product views remain mandatory. Link the deeper workflow article; all eventual site records stay unpublished drafts pending independent review.

**TinkerTool advantages:** no-charge documented preference interface, current-user scope, reset and eligible export/import, vendor-described notarized DMG. **Trade-offs:** OS-dependent settings; permission caveats; preferences survive app removal; different job from storage analysis.

**Breathing Room advantage for the relevant intent:** source-documented storage/app/activity context, not a benchmark win. **Trade-offs:** preview, incomplete installer/runtime validation, signing/notarization and Python caveats, optional hosted authenticated AI with recurring paid care. It is not an established replacement for TinkerTool's hidden-preference interface.

## Validation and next gate

Research completion is not publication approval. Check JSON parsing, all saved-source hashes, claim source resolution and retained excerpts, baseline capture hashes and the selected preview hash. Record actual results in `validation.json` and the job receipt. No site check/build/tests are applicable because no site files changed. No native/browser execution, cleanup, sign-in, messages, credentials, purchases, commits, pushes or deployments.

**Precise unblock condition:** establish a reuse basis for a real TinkerTool app screenshot (or record an explicit authorized visual-policy decision), then have the downstream job visually inspect the actual asset and preserve bytes/hash/provenance before drafting. Noncritical unknowns can remain explicitly unknown. Independent editorial/browser QA is still a later stage, not awarded by this packet.
