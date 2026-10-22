# Click&Clean — research handoff

**Task:** `research-clickandclean`  
**Reviewed:** 2026-10-22  
**State:** research complete; bounded source-backed drafting may proceed. This is not publication approval.

## Conclusion

Click&Clean is best treated as an **adjacent browser-privacy-data cleaner**, not a Mac system cleaner. Its official Chrome product page describes clearing selected browser data and lists macOS among the operating systems for the stated extension version. That is enough evidence for a carefully scoped draft explaining the distinction between browser data and general disk maintenance. It is not enough to recommend a current installation, assert present pricing/licence terms, or describe unverified privacy/data-flow behavior.

## Identity and discovery

- **Official name:** Click&Clean.
- **Official product page:** [Cleaner for Google Chrome | Click&Clean](https://www.hotcleaner.com/clickclean_chrome.html), published by/attributed to Mixesoft on the page. The company relationship was not separately investigated.
- **AlternativeTo discovery:** [Click&Clean about page](https://alternativeto.net/software/clickandclean/about/), retrieved 2026-10-21 19:07:35.090 UTC. Captured listing link: “Official Website hotcleaner.com/clickclean_chrome.html.” Retained raw capture: `docs/content/.runtime/verification-2/clickandclean-directory.json`, SHA-256 `369e6003f9f76fcab9d6b5dfe26778e79f0e848bb572096103d4bc19a2d355e8`.
- Discovery text called it a free browser extension for Chrome and Firefox and categorized it among system cleaners/duplicate finders. Those directory categories are not evidence of those capabilities. Do not characterize it as a filesystem cleaner on that basis.
- **Aliases:** none verified. Official page links to separate Firefox and Edge pages; do not treat these linked editions as feature-equivalent without checking them.
- **Fit:** Chrome browser-profile cleanup overlaps with a privacy/data-removal task, but is not the same job as freeing Mac disk space, inspecting app/process activity, or finding developer caches. Use this distinction to avoid a misleading direct-substitute comparison.

## Retained evidence

Official product page capture: retrieved 2026-10-21 19:10:01.895664 UTC; final URL unchanged; HTTP 200. Snapshot: `docs/content/.runtime/verification-2/clickandclean-official.json`, SHA-256 `755dd9704516118eb6936617e02f55cbeaccda58bac0601c01fb206a05819d80` (capture hash recorded in JSON: `116cde3416085c1e5016e73dfae7948c8b9486b496f0d7b114f6e34fd5f04880`). No fresh fetch or app test was performed for this handoff.

| Claim usable in a draft | Source excerpt and boundary |
| --- | --- |
| Product scope | Official page: “The Click&Clean web browser extension is a Private Data Cleaner for Google Chrome web browser.” Supports describing a browser cleaner, not a general Mac cleaner. |
| Documented browser-data options | Official page lists Low/Medium/High/Dev modes; time ranges; history, download history, cache, cookies, saved passwords/form data and browser storage categories. Vendor documentation only; not hands-on verified. |
| Export-before-delete statement | Vendor says users have an “option to save your browsing data to an HTML file before deleting that data.” Attribute this; export handling or recoverability was not tested. |
| Dated platform/version statement | Page says Chrome extension 9.8.1.0, released May 29, 2024, Chrome 115+, and OS list “Windows 11 / 10 / 8.1 / Mac OS X / Linux / Chrome OS.” This is a dated vendor statement, not proof of current compatibility or installation success. |
| Price/licence wording | Page labels that version “License: Freeware.” Do not turn this into an unqualified current price or legal licence claim. |
| Other browser links | Official page links to Firefox and Edge product pages. Their page contents, current status and feature parity were not checked. |

### Source-record conflict and unknowns

The baseline record in `docs/content/verification/batch-2.json` marks `license` and `availability` as unverified, but its facts also include `pricing: Freeware` with the official-page excerpt “License: Freeware.” This is an internal field-label/confidence inconsistency, not evidence that the source says two different things. Preserve both facts: the captured page used the word “Freeware” for version 9.8.1.0, while current legal licence, price and availability remain unverified. Avoid the claim or qualify it narrowly.

Other unknowns: current maintained version and Chrome compatibility; Firefox/Edge scope; data processing/local-versus-hosted behavior; exact confirmation and approval controls; helper/process grouping; recurring-growth monitoring; developer-cache discovery (the name “Dev mode” alone does not establish this); present price/legal licence; installation behavior; and whether the vendor's safety/security language has independent support. Unknown is not “No.” No installation, extension interaction, cleanup, or browser-data deletion test was performed.

## Capability matrix for draft use

| Dimension | Finding |
| --- | --- |
| macOS | The vendor page lists “Mac OS X” for Chrome extension 9.8.1.0. Current compatibility not verified. |
| Licence/price | Dated page says “Freeware”; current offer and legal licence unresolved. |
| Local/hosted | Not verified. Do not infer data handling from the fact it is a browser extension. |
| Scan/cleanup | Vendor documents selected browser-data categories and time ranges. General filesystem scanning/cleanup is not established. |
| Approval controls | Modes/categories are documented; exact confirmation flow unknown. |
| Helpers, growth, developer caches | Not verified. “Dev mode” is not proof of cache cleanup. |
| Runtime/install | Page's Chrome 115+ statement is tied to its 2024 version details; current requirements and install success unknown. Do not recommend installation pending refresh. |

Claim-level sources, exact excerpts, dates and qualification states are also recorded in `research.json`.

## Visual route

Use **route B** under the October 22 editorial policy. Existing first-party visual: `docs/content/assets/breathing-room/space-preview-2026-10-21.png` (`current-space-browser-preview`, SHA-256 `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a`). Retain its caption: “Current-source Breathing Room Space browser preview, captured October 21, 2026. Example data only; not a native scan, measured activity or cleanup result.” It is a browser preview, not a native test; publication-specific rights/context review remains due.

Do **not** copy Click&Clean imagery. Link to the vendor's [official screenshot page](https://www.hotcleaner.com/clickclean-chrome-screenshots.html), linked from its product page, with attribution; permission to reuse is unknown and no permission is implied. Add an original, accessible two-lane decision diagram: browser privacy task → choose browser/data category/time range → review scope → clear browser data; versus Mac storage task → inspect files/apps/process activity/developer caches → use a Mac-oriented tool. Label Click&Clean steps “vendor-documented, not independently tested.” The diagram must not imitate product UI or depict undocumented controls/results.

## Remaining publication gates (separate from research completion)

1. Refresh current product/version, Chrome/macOS compatibility, availability, price and legal licence; omit or narrowly qualify anything still unresolved.
2. Review official privacy/data-flow documentation before any local/hosted or privacy claim.
3. Do not recommend installation until current compatibility is verified. No app test was performed.
4. Inspect the first-party preview in its actual page context; preserve example-data disclosure and complete independent publication-specific rights/third-party-mark review.
5. Build and review the source-backed route-B diagram; ensure readable responsive layout, alt text, caption and adjacent attribution.
6. Independent factual/editorial/SEO/rendered-site/browser review and required site validation remain pending. Research completion does not authorize publication.

## Validation and retained files

- Reused baseline verification and raw captures rather than repeating completed research.
- Read `PLAN.md`, `EDITORIAL.md` October22 update, `capabilities.md`, `screenshots.json`, and the relevant verification records.
- No network refresh, app/extension testing, installation, image copying, purchases, account creation, messages, cleanup, publication review, commit, push, or deployment.
- Packet files: `docs/content/competitors/clickandclean/research.json` and `research.md`.
