# Click&Clean alternatives handoff

**Task:** `draft-alternatives-clickandclean`  
**Drafted:** 2026-10-22  
**State:** complete textual draft with original route-B diagram and first-party example preview; unpublished, independent review pending.

## Owned outputs and hashes

| File | SHA-256 | Purpose |
| --- | --- | --- |
| `/Users/gabe/code/breathing-room/website/src/content/alternatives/clickandclean.md` | `6254b2ab71d66d36a025715736552ba32dd8ad7e66af4defddee4f6481353929` | Complete alternatives guide; public path `/alternatives/clickandclean/`; `status: review`, `published: false`. |
| `/Users/gabe/code/breathing-room/website/public/assets/alternatives/clickandclean/browser-vs-mac-workflow.svg` | `be0ece3ff8315ffb31eb876595e2425bc38d7571229ca678cc412a8986eb8c8b` | Original accessible decision diagram; not product UI or test evidence. |
| `/Users/gabe/code/breathing-room/website/public/assets/alternatives/clickandclean/space-preview-2026-10-21.png` | `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a` | Reused first-party Space browser preview; example data, not native scan or measured result. |

## Evidence and choices

Reused the Click&Clean packet, baseline `verification/batch-2.json`, BleachBit and CCleaner research packets, `capabilities.md`, and `screenshots.json`; no broad refetch or app/extension test. Click&Clean is described as an adjacent browser-profile cleaner, not a general Mac cleaner. AlternativeTo is discovery provenance only and is not used to claim that it pairs Click&Clean with the alternatives.

Two replacements have retained source support for browser-data cleanup: CCleaner for Mac documents scheduled history/cookie/autofill removal, while BleachBit documents browser cleaners, cookie retention and a Preview/review workflow. The page keeps the meaningful platform limits: CCleaner's retained macOS requirements conflict; BleachBit offers packaged Windows/Linux releases and only experimental source-based Mac support. It intentionally does not pad the list with disk analyzers or app uninstallers.

The page preserves Click&Clean's source-record inconsistency: the official page labels v9.8.1.0 “Freeware,” while the baseline labels current licence and availability unverified and contains a pricing/licence field mismatch. Current price, legal licence, availability and compatibility remain unknown. Unknown processing location, confirmation behavior, current version and feature parity are not turned into negative claims. The official screenshot page is linked only; no competitor image is copied.

Visual route B is used: a new evidence-based task/platform diagram plus the first-party Space preview with its required example-data/native-limit caption. The diagram is not UI. The preview shows a different storage-investigation workflow, not Click&Clean behavior or a comparative test.

## Validation performed

Passed scoped Python structural check for review/unpublished frontmatter, no duplicate body H1, known internal destinations, explicit source conflicts/unknowns, and both referenced assets. `file` identified the SVG and 2940×3468 PNG; the copied preview SHA-256 matches the source screenshot inventory (`9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a`). Page length: 1,540 words. No shared marketing build/check/test, browser render, independent review, commit, push, deployment, purchase, account, message, cleanup, or queue/database change was performed. Do not imply publication approval.

## Remaining review before publication

1. Independently refresh Click&Clean current version, Chrome/macOS compatibility, availability, current price and legal licence; retain qualified wording or omit unresolved claims.
2. Review official privacy/data-flow evidence before making any local/hosted or privacy claim.
3. Independently inspect both visuals in page context; preserve first-party example-data disclosure and complete publication-specific image/third-party-mark review.
4. Review route-B diagram contrast, responsive legibility, title/description, citations and existing internal destinations.
5. Run the marketing site's required `pnpm check`, `pnpm build`, and `pnpm test` in order, inspect generated HTML/draft exclusion, and perform authorized visual/browser checks across required viewport and theme combinations. Keep unpublished until independent gates pass.
