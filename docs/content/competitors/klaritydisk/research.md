# Klarity Disk research: blocked before drafting

Task: `research-klaritydisk` · checked October 22, 2026 · research only.

**Klarity Disk is a relevant Mac storage-analysis competitor, not a dead product or a PowerMyMac alias. Do not draft yet:** its permitted official screenshot could not be downloaded, and official cleanup descriptions conflict. No article, comparison or website asset was created.

## Identity and reused discovery

Canonical owner: **`klaritydisk`**. **Klarity**, **KlarityDisk** and **KLARITY DISK** are names for Mukul Mehra's app at <https://www.klaritydisk.com/>, App Store ID **6758895498**. The directory links the homepage, the homepage/press page link that App Store ID, and Apple links back to the developer's domain. Skip separate drafts for those names; do not skip this canonical product. No public repository was established; do not invent a GitHub URL or claim none exists.

Classification: direct overlap for Mac storage investigation, adjacent to the broader maintenance/hosted-assistance workflow. It also documents RAM/process monitoring, so “only a disk map” is misleading. No Windows/Linux or cross-platform Breathing Room support is implied.

Reused `docs/content/verification/batch-1.json` record `klaritydisk` first. Its existing homepage retrieval was **2026-10-21T19:09:37.965667+00:00**; it already verified purpose, macOS floor and advertised price. No homepage or AlternativeTo refetch was needed. The missing baseline licence was resolved from official terms.

Discovery edge: Mole → <https://alternativeto.net/software/mole/?p=6> → <https://alternativeto.net/software/klaritydisk/about/>. Edge retrieved **2026-10-21T18:37:21.311Z**; directory about snapshot **2026-10-21T19:08:08.672Z**. Exact retained paths/hashes are in `research.json`. A directory edge is not proof of equivalent capabilities or a direct published Breathing Room relationship.

## Claim and source summary

Every row maps to the fuller per-claim excerpts, checked dates, qualifications and URLs in `research.json`.

| Claim | Supported wording and boundary | Source |
| --- | --- | --- |
| K01 | One product, Mukul Mehra; names above resolve to the same Apple ID. | [Press](https://www.klaritydisk.com/press), [US App Store](https://apps.apple.com/us/app/klarity-disk/id6758895498), retained homepage |
| K02 | Current listed version **1.3.1**, vendor release date **October 2, 2026**; requires **macOS 14.6+**. Binary build/architectures not verified. | [Changelog](https://www.klaritydisk.com/changelog), Apple compatibility/version fields |
| K03 | US storefront **$6.99 USD**; vendor advertises one-time, no subscription/IAP. Terms limit entitlement to the purchased current version, not free future upgrades. Other storefronts/tax not verified. | Apple, press, [terms §10](https://www.klaritydisk.com/terms) |
| K04 | Restricted commercial/proprietary licence; personal/commercial use and multiple owned devices under same Apple ID. Not open-source rights. | Terms §§1–3, 9–10 |
| K05 | Documented treemap/icicle, age colouring, Large Files. Old/large does not mean disposable. | Retained homepage, Apple description |
| K06 | **Conflict:** newer notes describe Trash moves and confirmations; terms §5 says read-only and no moves/deletes. | Changelog 1.1/1.3/1.3.1, Apple What's New, terms |
| K07 | Vendor says local, no network/accounts/analytics; Apple privacy declaration is developer-reported. Not an independent privacy/network audit. | Retained homepage, press, Apple |
| K08 | RAM/process monitoring and menu-bar readout documented. Helper grouping and long-term growth attribution not verified. | Retained homepage, press, changelog |
| K09 | 1.3.1 notes describe hidden Library scanning and allocated space that excludes undownloaded iCloud files. Not an accuracy test. | Changelog and Apple What's New |
| K10 | Listed press-kit assets expressly permitted for editorial use. Not a blanket licence or endorsement. | Press: “no permission required for editorial use” |

New read-only source checks filled version/storefront/licence/rights gaps. Their webfetch responses do not expose exact retrieval timestamps; retained excerpts are in JSON, with a UTC window-end checkpoint rather than invented exact times. Machine checkpoint was **2026-10-21T21:22:33.805444+00:00**, despite the job's October 22 calendar. The press page's September 30 dateline precedes its stated October 2 release; release chronology is corroborated by changelog/Apple, not inferred from that dateline. Apple's prose says macOS 14+, but its stricter compatibility field and vendor agree on **14.6+**.

### Material conflict: preserve both sources

Terms, last updated February 2026:

> Klarity is a read-only disk analyzer — it only reads file metadata (names and sizes) and does not modify, move, or delete files.

Current 1.3.1 changelog and App Store notes:

> Klarity will not move folders your Mac depends on, such as Library or Keychains, to the Trash, and it asks twice before trashing app data, iCloud folders or files inside photo and video libraries.

The newer release notes are version-specific and support an attributed description, but do not erase contradictory legal text. Do not write an unqualified cleanup recommendation, promise “safe deletion,” or perform a cleanup test to force resolution. Needed: public version-specific clarification or corrected terms, followed by delta review. No contact message was sent.

## Required visuals

### Competitor app view: permission established, access blocked

- Source: <https://www.klaritydisk.com/press> → **Treemap view — the main disk map**.
- Exact asset: <https://www.klaritydisk.com/screenshot-treemap.png>.
- Reuse basis: “These are the same assets the site uses. Right-click and save whichever you need; no permission required for editorial use.” Credit **Klarity Disk / Mukul Mehra; official press-kit image**.
- One ordinary public GET via Python `urllib.request.urlopen` returned **HTTP Error 403: Forbidden**. No asset bytes were retained; no original hash, dimensions or invented capture date/version. No cookie or credential extraction, alternate profile or access-control bypass.
- The actual image has **not** been visually reviewed. Final alt text and factual pixel description remain pending. Link the official visual for research only; this does not satisfy the on-page image gate.

### Selected Breathing Room preview: reuse existing current-source inventory

`docs/content/assets/breathing-room/space-preview-2026-10-21.png`

- Library ID: `current-space-browser-preview` in `docs/content/screenshots.json`.
- Capture: **2026-10-21T19:06:45.416416+00:00**, browser preview at `http://127.0.0.1:1431/`, source commit `54828ac3170b45861aee70861dd0b9c658ed7e51`.
- Original SHA-256 rechecked: `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a`; **2940 × 3468** per library. No copy/edit or published hash claimed.
- Required caption: **Current-source Breathing Room Space browser preview, captured October 21, 2026. Example data only; not a native scan, measured activity or cleanup result.**
- Alt: **Breathing Room Space view rendered in a browser with illustrative example data.**
- Keep the example-data banner visible. Reuse basis is the owner-requested first-party capture, not blanket rights to third-party marks. Library privacy/visual review is reused; this worker does not claim a new native capture or article-context visual approval.

## Distinct workflow article brief

**Working title:** Use file age to investigate forgotten space on a Mac  
**Proposed slug:** `mac-storage-file-age-before-cleanup`  
**Track:** search/reference · conditional brief, not a draft.

Reader job: interpret large, old folders without turning age into deletion permission. Explain Klarity's documented age map and 1.3.1 allocated-size changes, then ownership, backups, project dependencies and rebuild/download costs. This is not the comparison table expanded into a doorway page.

Outline:

1. Lead with the decision: old and large identifies what to inspect, not what to remove. Place a verified competitor UI image immediately afterward.
2. Distinguish modification age, allocated space and cloud placeholders. Attribute 1.3.1 semantics; do not claim independent measurement.
3. Review ownership, originals versus generated data, backups and rebuild costs. No product-specific removal instructions until K06 is resolved.
4. Separate one-time mapping from recurring-growth investigation. Use the labeled Breathing Room Space browser example later, without suggesting native results.
5. Give bounded choices: Klarity's map, manual Finder review, or broader maintenance if preview/hosted-AI caveats are acceptable. Disclose “Breathing Room, which we build” in any recommendation.

Interaction handoff: a local decision checklist for known owner, backup, original/rebuildable status, offline availability and rebuild cost. Unknown means defer. No filesystem access, uploads or deletion. No arbitrary code-demo repository.

Proposed links: comparison hub, `/comparisons/klaritydisk/`; a relevant tool only after implementation/tests are confirmed. These are planned targets, not verified live routes.

## Concise comparison brief and truthful trade-offs

**Title:** Breathing Room vs Klarity Disk · **proposed comparison slug:** `klaritydisk`.

Choose based on the job, not a universal winner. Klarity documents age-coloured treemap/icicle exploration, RAM/process visibility and local-only operation. Breathing Room, which we build, has source implementations for broader investigation, grouped helpers, developer-cache discovery, history and daily care; these are not new distributed-binary or performance tests.

- **Klarity advantages:** focused map/age workflow; current US one-time $6.99 offer; vendor-described no-network operation; RAM/process/menu-bar tools acknowledged.
- **Klarity limits:** macOS 14.6+; future versions not included by terms; cleanup documentation conflict. Helper grouping, recurring growth and tool-specific cache cleanup remain **not verified**, not “No.”
- **Breathing Room advantages:** broader source-implemented investigation/history/approval scope in the current first-party evidence register, not a superiority benchmark.
- **Breathing Room limits:** `0.1.0-preview.1`, macOS 13+, Python 3.10+; Apple Development signed, **not Developer ID signed or notarized**. Clean-machine/physical-Intel runtime parity is not established. Hosted authenticated AI sends relevant context/tool outputs; advertised optional AI Care is **$5 USD/month or $50 USD/year**, not entirely offline AI. Daily care needs the app running and saved approvals. Optional automatic verified Ruff-cache mode prevents an unconditional “never deletes without asking” promise.

Reused Breathing Room evidence: `docs/content/capabilities.md`, reviewed October 21; it already contains source locators and public release/pricing/privacy checks. No needless refetch or stronger runtime claim. Recheck volatile offers within 30 days and before publication when stale.

Keep the eventual comparison concise: platform/version, licence/price/upgrade conditions, local/hosted boundary, map semantics, cleanup conflict, monitoring scope and runtime caveats. Link to the distinct workflow article and hub. No rankings, fabricated reviews, speed/savings claims, or duplicate alias pages.

## Gate and handoff

**Blocked**, not irrelevant: retain research; do not draft, publish or alter queue state.

1. **G01:** Get a publicly accessible permitted real competitor UI image, preserve bytes/hash/provenance and inspect it. Rights alone do not satisfy the visual gate.
2. **G02:** Resolve read-only terms versus current Trash notes before cleanup recommendations.

Noncritical unknowns include public repo, exact architecture/build, independent privacy/performance tests, unverified monitoring/cache features and non-US pricing. Do not invent these or turn them into negative claims. Independent editorial/rendered review remains pending; no score assigned. No site build is relevant because no website files changed.
