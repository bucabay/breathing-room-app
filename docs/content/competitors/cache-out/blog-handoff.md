# Cache Out workflow article handoff

Task: `draft-blog-cache-out` · drafted 2026-10-22 · status remains `review`, `published: false`.

## Owned outputs

- Marketing article: `/Users/gabe/code/breathing-room/website/src/content/blog/cache-out-mac-workflow.md`
  - SHA-256: `bf6177decf20793de6aca598fb2c1f7d83fd31d2b66b10ab42a169d6e1ca397c`
  - Intended public route: `/blog/cache-out-mac-workflow/` (draft gate means no public route yet).
- Original decision diagram: `/Users/gabe/code/breathing-room/website/public/assets/blog/cache-out/browser-records-decision.svg`
  - SHA-256: `86ee1f2f5f29f9e3b1c3bcc3df611a0ea73a1bc45f6eb21a6972ea64de9eb015`
  - Route B visual: explicitly an editorial diagram of documented behavior, not Cache Out UI or a test.
- First-party example preview: `/Users/gabe/code/breathing-room/website/public/assets/blog/cache-out/space-preview-2026-10-21.png`
  - SHA-256: `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a` (matches the retained screenshot record).
  - Copied unchanged. The article caption preserves the example-data, browser-preview, non-native/non-measurement disclosures; per-article rights/context review is pending.

## Evidence and editorial boundaries

Reused `research.json` / `research.md`, `validation.json`, the existing baseline verification, `capabilities.md`, and `screenshots.json`; no broad refetch or app execution. The source packet verifies Cache Out identity, stated 1.5.3/macOS 26.2+ offer, documented data categories and profile selection, and the distinction between download-list entries and actual files. Text describes vendor documentation, not hands-on behavior.

The article retains the material conflict: Cache Out's changelog documents historical optional preview/confirmation and Move-to-Trash settings, while its terms state deletion is permanent. Current defaults and database/session recovery remain unknown; no undo promise is made. The official app image at `https://cacheout.app/assets/cacheout-window-140.webp` remains link-only because reuse rights, version and capture date are unknown. The route-B diagram supersedes the old screenshot-only drafting block under the October 22 editorial policy; it does not clear competitor-image rights.

One bounded product distinction names Breathing Room, which we build, and preserves the preview, Python, signing/notarization, runtime-validation and hosted-assistant limits from the capability register. No feature parity, savings, safety, compatibility test or comparative winner is claimed.

## Alternatives intent exception

Do not create `/alternatives/cache-out/` from the current evidence. Cache Out is documented for browser-record cleanup, while the retained CleanMyMac packet supports a broader Mac-maintenance suite and the Mole packet covers a distinct native/CLI maintenance family; those packets do not establish several job-relevant peers for Cache Out's specific browser-data task. Treating them as interchangeable replacements would manufacture the relationship the page is meant to verify. Reopen only if existing or later authorized packets establish multiple products with the same browser-record job and enough current evidence for a distinct replacement guide.

## Remaining review gates

- Independently verify claim-to-source alignment and current volatile version/platform statements before publication; no apps were installed and no browser data was cleared.
- Resolve or preserve the recovery uncertainty; do not claim Trash reversibility or current default from historical changelog text.
- Independently review diagram readability and preview context/rights, including visible example-data disclosure. No Cache Out image was copied; the official image remains an attributed link only.
- Run the marketing repository's required `pnpm check`, `pnpm build`, then `pnpm test` in the separately authorized validation stage; inspect rendered metadata/routes and mobile/tablet/desktop light/dark visuals. These shared checks were not run for this scoped draft job.
- Independent factual, visual, SEO and rendered review remains pending. Draft is not publication approval.

## Validation performed for this handoff

- Source packet validation already retained at `docs/content/competitors/cache-out/validation.json`: JSON/claim references and selected screenshot hash passed; not an article review.
- Recomputed SHA-256 for all three article/asset files after writing; values above are the observed results.
- Did not run shared site build/tests or browser review, change queue/database state, or edit shared site files.
