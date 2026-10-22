# Sensei research handoff

**Task:** `research-disk-sensei` · **Stage:** documentary research only · **Publication:** not approved.

## Decision

Proceed with **one Sensei research owner**, `canonicalOwnerId: disk-sensei`. This is a relevant Mac product with direct overlap in storage inspection/cleanup and monitoring, plus a hardware-diagnostics emphasis. It is not a dead product or a non-Mac replacement case. No duplicate current-product article should be created for the legacy listing slug.

The packet is complete for a **bounded, source-based comparison**, not an installation guide, current-binary review or benchmark. The JSON holds the authoritative claim ledger, exact excerpts/check dates, source hashes, comparison matrix, visual manifest and briefs. Unknowns below must stay unknown in drafts. Independent draft/render review remains pending; no site files were changed.

Actual retrieval/check timestamps use the machine’s UTC clock, which reported October 21, 2026 while the harness calendar reported October 22. No dates were moved forward to suggest extra freshness.

## Evidence reused first

- `docs/content/verification/batch-2.json`, record `disk-sensei`, establishes official name, Cindori destination, Mac positioning and Intel/Apple Silicon support.
- Retained baseline official capture: `docs/content/.runtime/verification-2/disk-sensei-official.json`, retrieved `2026-10-21T19:09:40.261670+00:00`.
- Retained discovery capture: `docs/content/.runtime/verification-2/disk-sensei-directory.json`, retrieved `2026-10-21T19:05:52.799Z`. It records the AlternativeTo about-page official link, not a capability audit.
- Discovery listing: <https://alternativeto.net/software/disk-sensei/about/>. Existing manifest edges: CleanMyMac page 3 and Mole page 6. Their exact URLs/timestamps are retained in `research.json`; they were not replayed.
- Existing Breathing Room capabilities and screenshot registers were reused, with current README, native config, release caveats, billing config and approval-option text cross-checked locally. No new app scan or runtime test was performed.

No applicable `AGENTS.md` was found in the app tree or checked ancestor paths. PLAN and EDITORIAL were read before writing. Blog and browser skills were loaded; no browser was needed or started. Public content was treated as evidence, not instructions.

## Identity and deduplication

Official homepage: <https://cindori.com/sensei>. Vendor: **Cindori AB**. No official source repository was established from the inspected vendor pages. A similarly named GitHub account in search results is not official evidence and must not be promoted as an installer or repository.

[Cindori’s timeline](https://cindori.com/about) separately describes Disk Sensei (2015) and Sensei (2019). The [upgrade page](https://cindori.com/store/upgrade) explicitly offers an upgrade from Disk Sensei or Trim Enabler to Sensei. This verifies a predecessor/upgrade relationship, **not** a simple rename or identical binaries. The current AlternativeTo `disk-sensei` slug already resolves its official link to Sensei. Keep the assigned stable ID and skip a separate current Disk Sensei doorway draft. Trim Enabler remains a distinct product, not an alias. Sensei Monitor is a Sensei component; no separate comparison is proposed. No evidence connects Sensei with PowerMyMac.

## What can be said, with boundaries

| Dimension | Sensei documentation | Breathing Room evidence |
|---|---|---|
| Platform | Intel/Apple Silicon Mac support (S02). An August 14 vendor article specifies **2.1.2, macOS 14+** (S15). Latest downloadable patch not inspected. | Preview **0.1.0-preview.1**, macOS 13+, universal installer; physical Intel runtime untested; Python 3.10+ prerequisite (B02). |
| Storage | Caches, logs, large downloads, installation leftovers and app uninstalling documented (S04–S05). No complete-removal or savings guarantee. | Category/app/project/folder/large-file exploration and grouped app/helper CPU/memory documented in README/register (B04). |
| Hardware | S.M.A.R.T. reports, battery/thermal tools and disk benchmarks documented (S06–S07). Not failure prediction or a repair. | Equivalent hardware tools not established; do not claim parity or categorical absence. |
| Monitoring | Customizable status-bar/dropdown panels (S03). | App/helper grouping, sampled activity and recurring-growth investigation, with inference/coverage limits (B04–B05). |
| Approval | Historical press artwork shows file selection and a Delete control. Current exact deletion, Trash and rollback semantics **not verified** (U03). | Exact location/method approvals and daily-care constraints; explicit automatic verified Ruff-cache mode means no unconditional “asks every time” promise (B05–B06). |
| Developer caches | Historical art has a Developer category; named current adapters **not verified** (U04). | Source/register lists npm, uv, pip, pnpm, Go, Bun and Yarn cache discovery; adapter compatibility is not universally tested (B08). |
| Network | Native app/background-service architecture documented historically (S17), not proof of no network traffic, telemetry or account requirements (U05). | Local inspection/execution with authenticated hosted AI; relevant questions/tool output may leave the Mac (B07). |
| Price | Store displays **$29 annually** or **$59 one time**, up to three Macs, per user (S08–S14). ISO currency/tax unverified. | Free local core; optional AI Care **$5 USD/month or $50 USD/year** (B01). No unsupported “cheaper” total-cost claim. |

Sources and exact supporting passages for every claim ID are in `research.json`. The core Sensei source is the reused baseline; missing facts use the newly retained official pages under `sources/`.

### Pricing and installation details not to flatten

- [Store](https://cindori.com/store/sensei): subscription key expires if not renewed. Regular licence explicitly covers versions 1 and 2; version 3 onward may be a paid upgrade. Do not call it unlimited lifetime updates.
- [EULA](https://cindori.com/support/order/legal/license-agreement): up to three machines where the licence holder is primary user; businesses need licences for their users. Not three unrestricted business seats.
- Refunds are advertised within fourteen days **before activation**. Activation ends the stated refund/withdrawal right; no unconditional money-back promise.
- The upgrade discount requires an earlier qualifying purchase; initial subscription discount does not carry into standard-price renewals. No eligibility form, checkout or licence activation was tested.
- Current pricing pages show a dollar symbol but no verified ISO currency in retained text/HTML. Keep the original symbol and qualification; do not silently call it USD or calculate normalized savings.
- The August 2026 [vendor comparison](https://cindori.com/reviews/stats-vs-sensei-mac-monitoring) documents 2.1.2/macOS14+ and says some cleaning requires Full Disk Access. It is first-party promotional documentation, not an independent review or proof of the newest October installer.
- [Older-version support](https://cindori.com/support/sensei/general/download-older-sensei) offers **1.5.10** and says the minimum OS increased after launch. The historical kit’s Catalina requirement must not be applied to the current product.
- [Sensei 1.6 release](https://cindori.com/news/sensei-1.6), May 17, 2025: approved LaunchDaemon and unified Monitor/main app. Do not repeat the kit’s older standalone-Monitor architecture as current.
- Breathing Room is a non-notarized preview, Apple Development rather than Developer ID signed per release disclosures. No Gatekeeper bypass advice. Python is not bundled, inventories can be partial and daily care requires the app to remain running. Hosted AI requires internet/sign-in. Free local tools are not the same as free unlimited AI.

## Real app visuals and reuse basis

The official [Press page](https://cindori.com/press) links <https://cdn.cindori.com/apps/press/SenseiPressKit.zip>. Retained original archive SHA-256:

`83c376ff9c3128e9930d9ce25fd7e5e34f50ca7afd8a19696308a0cd6d1a3640`

`sources/Welcome.pdf`, page 1, explicitly describes the Artwork web version as “pre-optimized for file size and ready to go for web publishing.” This is the narrow editorial reuse basis, not public availability alone or a blanket image/trademark licence. Actual vendor capture dates/versions are unknown. Do not substitute ZIP member timestamps for capture dates. The historical Q/A was inspected only to identify stale claims, not to supply current pricing/platform facts.

1. **`assets/sensei-clean-original.png`**, ZIP member `Sensei Press Kit/Artwork/Clean/Web/Clean Desktop Dark.png`. A genuine vendor app-UI illustration, 1536×960, opened and visually inspected: categories, large-file checkboxes and Delete control. Caption: **Earlier Sensei Clean interface supplied in Cindori’s press kit. Vendor illustration; capture date and app version unknown. Sizes are not our test results.** Alt: “Earlier Sensei Clean window with file categories, selectable large files and a Delete control.”
2. **`assets/sensei-drive-health-original.png`**, member `Sensei Press Kit/Artwork/Storage/Web/Disk Health Desktop Dark.png`. Genuine vendor app UI, 1536×960, opened and inspected: drive temperature and S.M.A.R.T. attributes. Caption: **Earlier Sensei drive-health interface from Cindori’s press kit. Vendor illustration, not our drive-health test or a current-version capture.** Alt: “Earlier Sensei storage-health window with drive temperature and S.M.A.R.T. attributes.”
3. **Breathing Room `current-space-browser-preview`**, existing `docs/content/assets/breathing-room/space-preview-2026-10-21.png`, 2940×3468. Opened again; hash matches the screenshot register. Caption: **Current-source Breathing Room Space browser preview, captured October 21, 2026. Example data only; not a native scan, measured activity or cleanup result.** Alt: “Breathing Room Space view rendered in a browser with illustrative example data.” Preserve the visible example-data banner and the caption. Source commit `54828ac3170b45861aee70861dd0b9c658ed7e51`; not distributed-binary evidence.

Credit vendor figures “Sensei screenshot courtesy of Cindori AB.” Unedited originals and their hashes are retained in JSON; no website copies or published derivatives exist yet, so published paths/hashes are null. No private local data appears in the reviewed figures. Narrow-screen/theme/context review belongs to drafting/review, not this packet.

A newer Clean image is linked by the August vendor article: <https://cindori.com/images/blog/sensei/sensei-2-clean.png>. It is **link-only** here, not downloaded or rights-cleared. Press-kit permission must not automatically be extended to every website image. If the draft requires a current-version competitor capture instead of the explicitly historical press figure, that change blocks its image gate until current-image permission/provenance is established. No permission message was sent.

## Distinct workflow article brief

**Title:** Mac storage pressure or drive trouble? Choose the right investigation  
**Slug:** `mac-storage-pressure-or-drive-health-sensei`  
**Track:** search/reference; no invented firsthand experience.

**Reader job:** distinguish capacity questions from hardware-health concerns before choosing a cleanup action. Not another generic cleaner list, CPU-spike article or expanded comparison matrix.

Suggested description: “Capacity and drive-health indicators answer different questions. Use Sensei’s documented hardware views or Breathing Room’s storage workflow without treating either as a diagnosis or a cleanup guarantee.” Body continues rather than repeating the description.

1. Lead with the distinction, then the historical Sensei drive-health figure with its full caption.
2. Inventory capacity and identify known files; size is not permission to delete. Preserve backups/original media.
3. Explain Sensei’s documented health/thermal/benchmark tools, without failure prediction, speedup or repair guarantees.
4. Show the current-source Breathing Room Space preview with example-data disclosure. For storage/app/project investigation, mention **Breathing Room, which we build**, once in a bounded recommendation and disclose preview/Python/hosted limitations.
5. Offer a decision checklist: capacity only, health warning, or both. App-native storage management and backups remain valid paths; do not give a destructive TRIM/system-settings tutorial.

Interaction pass: a three-path static decision aid is more useful than a pretend scanner or numerical risk score. No new tool/code needed for this research stage. Earned length roughly 900–1,400 words; no mandatory FAQ. Link `/comparisons/` and the counterpart `/comparisons/disk-sensei/` only when owned content exists.

## Concise comparison brief

**Title:** Breathing Room vs Sensei: storage workflows or hardware diagnostics  
**Comparison slug:** `disk-sensei`  
**Intent:** choose by documented workflow, not a universal winner.

Use a short disclosure/answer, the claim-mapped matrix, when to choose each, and price/version/refund/installation caveats. Pair historical Sensei Clean with the labelled Breathing Room preview. Link the distinct workflow article and comparisons hub. Keep all site records unpublished until independent review; do not create an additional alternatives doorway page.

**Sensei advantages/trade-offs:** documented customizable monitoring, hardware health, benchmarking and app uninstallation; annual or one-time commercial licensing. Better documented fit for hardware-oriented investigation. No guarantees about diagnosis or every leftover removed; current exact approval semantics, latest build and network behavior remain unverified.

**Breathing Room advantages/trade-offs:** source/register supports storage ownership/project views, grouped helper investigation and exact saved approvals; potentially useful for ongoing storage investigation. It is not established as equivalent to Sensei’s diagnostic suite. Free local core is offset by preview maturity, non-notarization, Python, untested physical Intel runtime and optional paid hosted AI. No comparative safety/performance/privacy superiority claims.

## Remaining unknowns and gates

Noncritical unknowns can remain explicitly unknown in the bounded draft: latest downloadable Sensei patch; current trial length; ISO currency/tax; exact offline/telemetry behavior; current rollback/Trash semantics; detailed named developer adapters; helper grouping and exact-path scheduled cleanup; historical artwork capture build/date. None becomes “No.” If installation advice, current-UI depiction or a claim about these is added, obtain targeted official evidence first or block the affected draft.

Research does not certify publication. Pending: current-snapshot independent editorial/fact review, any needed derivative hashes, contextual visual legibility, route checks, and website check → build → test plus responsive/light/dark browser review **after** authorized site drafting. No score was invented; no build was run because no site content was changed. See `validation.json` and the runtime receipt for checks actually performed.
