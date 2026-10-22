# App Eraser workflow blog — draft handoff

Task: `draft-blog-app-eraser` · Drafted **2026-10-22**. Drafting is complete; independent verification and publication approval are pending.

## Owned outputs

| File | SHA-256 | Purpose/state |
| --- | --- | --- |
| `/Users/gabe/code/breathing-room/website/src/content/blog/app-eraser-mac-workflow.md` | `ecc4b9402f1bf518bb3781ecfbd7d7ea73abfa0746bc68197e24f88b7ef32ad6` | Complete workflow draft for `/blog/app-eraser-mac-workflow/`; `status: review`, `published: false`, dated/updated October 22, author Breathing Room team. Not a live/published page. |
| `/Users/gabe/code/breathing-room/website/public/assets/blog/app-eraser/match-review.svg` | `e289db0450df104bb97a36bab8ad10eb2c451451486cf580931bb4c822086260` | Original route-B decision diagram; not competitor UI or a test. |
| `/Users/gabe/code/breathing-room/website/public/assets/blog/app-eraser/space-preview-2026-10-21.png` | `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a` | Unchanged first-party Space browser preview copied from app screenshot library; example data disclosed. |

This handoff owns the only other record in the app repository. Its final hash is recorded in the required receipt to avoid self-referential hashing.

## Intent and evidence boundary

The article teaches one concrete task: reviewing App Eraser’s filename/name and bundle-ID candidates before choosing what to remove. It is not a product profile, head-to-head comparison, or alternatives roundup. The canonical product is distinct and adjacent; no verified alias or skip applies. The old research packet’s `draftingAllowed:false` is preserved unchanged and reflected as historical research status: October 22 EDITORIAL.md explicitly allows a source-supported internal draft when that flag arose solely from unresolved screenshot rights. That does not clear the screenshot or license conflict.

Reused `docs/content/competitors/app-eraser/research.json` and `.md`, `validation.json`, `docs/content/verification/batch-1.json` through the retained App Eraser identity record, `capabilities.md`, and `screenshots.json`. Existing retained official snapshot/source evidence and the source validator report 30 structural/provenance checks passed. No unnecessary source refetch was done. Claim boundaries retained in the prose:

- Name/bundle-ID comparison is a heuristic, not ownership or disposability proof; source behavior is not asserted as verified release behavior.
- Inspected controller initializes candidate checkboxes checked, supports Finder reveal and confirmation, and attempts to quit the selected app; no app was run or removed.
- Search locations/permissions are not complete-coverage evidence. Modern OS compatibility, installer signing/notarization, privacy behavior and exact release/source parity remain unknown.
- GitHub/root GPL-3.0 declaration versus package ISC metadata remains an unresolved source conflict; neither is declared definitive.
- Breathing Room preview, Python, signing, Intel/clean-install, hosted-data and optional-price boundaries follow `capabilities.md`; no runtime or cleanup claims are made.
- App Eraser’s original screenshot remains link-only. It was not copied/downloaded; the page links to the official repository instead.

## Visual and interaction pass

`match-review.svg` is an original, vertically stacked decision diagram: match → identify path → assess ownership/purpose → pause if uncertain/shared → approve only a known action. It contains no copied pixels, vendor UI, simulated scanner, fake paths, deletion controls or results. Its accompanying alt/caption explicitly identify it as a diagram based on documented source, not an app screenshot or test.

The unchanged Space preview retains its captured-source provenance: October 21, 2026; source commit `54828ac3170b45861aee70861dd0b9c658ed7e51`; dimensions 2940×3468; original SHA-256 as above. The inherited screenshot register identifies it as a current-source browser preview with example data, not native behavior or measured results. No crop or image edits. Figure caption and alt text disclose scope and the overlapping assistant composer. Page-context mobile/light-dark visual review is still pending.

Interaction pass: implemented the non-executing choice flow in the SVG and a five-step prose checklist. No JavaScript, filesystem access, simulated results or destructive example.

## Validation actually performed

- Site content frontmatter parsed using installed Ruby/Psych: **passed**, current dates, review/unpublished flags, seven HTTPS sources, retained October 21 source-check dates.
- Final record structure/assets check: **passed**, title 58 characters, description 143 characters, two figures, no body H1 or unresolved placeholders, both asset paths exist.
- Original SVG parsed with `/usr/bin/python3` XML parser: **passed**, expected viewBox and accessible `<title>`/`<desc>`.
- Asset SHA-256: copied PNG matches source register hash; SVG and article hashes recorded above after finalization.
- First Node check attempted installed Node v25 but failed because `yaml` is not resolvable from the website package root. No packages were installed. A retry using the installed app/site Astro dependency path was not available (`node_modules/.pnpm` absent).
- Initial Homebrew Python XML check failed because its `pyexpat` could not load a system-library symbol; rerunning the same structural check with `/usr/bin/python3` passed. No environment changes were made.
- **Not run by design:** shared `pnpm check`, `pnpm build`, `pnpm test`, generated HTML/schema or draft-leakage checks, local preview, Chrome responsive/theme/keyboard review. The user explicitly prohibited shared site builds. No browser session was started; no app/browser runtime tests, account, cleanup, or external permission request.
- No independent fact/editorial score is claimed. Do not treat drafting or source validator passes as publication approval.

## Remaining review before publication

1. Independently check the exact article/assets against retained source records, especially default selection, Trash wording, source/release caveat, licensing conflict, compatibility unknowns and Breathing Room pricing/privacy/runtime boundaries.
2. Refresh volatile availability/pricing before publication if older than 30 days; preserve source check dates until actual re-verification.
3. Review the exact output hashes and rendered page; verify canonical/social/schema metadata and draft exclusion through the authorized site check/build/test workflow.
4. Inspect visuals and links at about 390/768/1440 px in light and dark themes, including mobile diagram readability, the Space preview disclosure/composer overlap, captions, keyboard links and image loading.
5. Require independent score >=85/100 with zero blocking evidence, visual, privacy or technical issues. Keep `review`/`false` until approved.

No queue/database, shared site infrastructure, other records, nav/schema/tests or unrelated files were changed. No commits, pushes, deployments, messages, purchases, accounts, credentials, cleanup, installation or destructive actions.
