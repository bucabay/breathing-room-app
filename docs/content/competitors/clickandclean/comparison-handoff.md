# Click&Clean comparison handoff

**Task:** `draft-clickandclean`  
**Drafted:** 2026-10-22  
**State:** complete textual draft; unpublished, independent review pending.

## Owned outputs and hashes

| File | SHA-256 | Purpose |
| --- | --- | --- |
| `/Users/gabe/code/breathing-room/website/src/content/comparisons/clickandclean.md` | `88383068ee3de53cf62d5d32058773cadcbc22d27ad83be0c10c5fd7c1e02a2d` | Complete comparison, public path `/comparisons/clickandclean/`; frontmatter remains `status: review`, `published: false`. |
| `/Users/gabe/code/breathing-room/website/public/assets/comparisons/clickandclean/decision.svg` | `4ff1e14b4c2cd5e5f89166f1c5c10023e66c8006c5438fb1c5292fb1c74f18a7` | Original accessible two-task diagram. Describes documented workflow, not Click&Clean UI or a test. |
| `/Users/gabe/code/breathing-room/website/public/assets/comparisons/clickandclean/space-preview-2026-10-21.png` | `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a` | Reused first-party current-source Space browser preview from screenshot inventory; example data, not native scan or measured result. |
| `docs/content/competitors/clickandclean/comparison-skip.md` | `1461e18bfe37603235385b53ce8ae6766e7885c641fbd7a417ebf76b5b09abf0` | Evidence-based exception for a separate alternatives page. |

## Evidence and choices

Reused `docs/content/competitors/clickandclean/research.json` / `.md`, `docs/content/verification/batch-2.json`, `docs/content/capabilities.md` and `docs/content/screenshots.json`; no refetch or extension/app test. The page calls Click&Clean an adjacent browser-data cleaner, cites its official Chrome page next to product claims, and uses AlternativeTo only for discovery. It preserves the internal “Freeware” versus unverified licence/availability conflict as a dated vendor label, not a current price/legal conclusion. Unknown processing location, approval flow, helper grouping, recurring monitoring, developer-cache behavior, current compatibility and install status are not asserted as absent.

Route B was used: original decision diagram, attributed official screenshot-page link only, and the first-party example-data preview. No Click&Clean image was copied. Alternative products were not presented as browser-cleaner replacements. The separate skip note records why peer packets for Mole, DaisyDisk and CleanMyMac demonstrate adjacent Mac-maintenance products, not a verified multi-option set for Click&Clean's browser-profile job.

## Validation performed

- Passed scoped Python structural check: frontmatter includes required title/description/source fields, review/unpublished gates and both referenced asset files exist; diagram starts with SVG markup.
- `file` confirmed decision diagram is SVG and preview is PNG, 2940×3468. Preview hash matches `current-space-browser-preview` in `screenshots.json`.
- Draft is 1,495 words. No shared site build, check, test, browser render, independent review or publication was performed. A first ad-hoc assertion expected two raw asset attributes but counted the same preview twice because it is both linked and shown; corrected integrity check passed using unique asset paths.

## Remaining review before publication

1. Independently refresh Click&Clean version, Chrome/macOS compatibility, availability, price and legal licence; retain qualified wording or omit unresolved claims.
2. Review official privacy/data-flow evidence before making any local/hosted or privacy claim.
3. Independently inspect the first-party preview in page context and resolve publication-specific image/third-party-mark rights review.
4. Review original diagram responsiveness/contrast/legibility and page SEO, citations, copy and any needed content links.
5. Run the marketing site's required `pnpm check`, `pnpm build`, `pnpm test` in that order, inspect built HTML/draft exclusion, and complete authorized visual/browser checks at required viewport/theme combinations. Keep the page unpublished until independent gates pass.
