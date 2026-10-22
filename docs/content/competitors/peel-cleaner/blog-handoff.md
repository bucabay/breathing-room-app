# Peel workflow blog handoff

**Job:** `draft-blog-peel-cleaner`  
**Draft:** `/Users/gabe/code/breathing-room/website/src/content/blog/peel-cleaner-mac-workflow.md`  
**Public route if approved:** `/blog/peel-cleaner-mac-workflow/`  
**Status:** complete textual draft; review only, not publication-approved.

## Intent and evidence

The article teaches a specific decision workflow: interpret why a file is associated with an app before moving app leftovers to Trash. It is not a profile, comparison matrix, alternatives list, or generic Mac cleaning guide. The source packet's historical `draftingAllowed:false` was solely tied to unresolved competitor screenshot reuse. The October 22 policy permits this source-backed draft using route B; no screenshot permission was inferred, requested, or bypassed.

Reused `research.json`, `research.md`, `validation.json`, version-pinned Peel README/GUIDE/privacy/release evidence, `capabilities.md`, and `screenshots.json`. Research validation reports 82/82 structural/hash checks passed. Source retrievals were October 21 UTC; they were not refreshed in this job. The article preserves the meaningful README/guide distinction: some confident app-only matches may be preselected, while shared and guessed matches wait for review. It also states that Trash/History recovery is conditional, has a 20,000-item history limit, and does not cover named irreversible exceptions. No installation, cleanup, native testing, network audit, or recovered-space measurement is claimed.

## Visual and interaction handoff

- Route B. The original SVG `/Users/gabe/code/breathing-room/website/public/assets/blog/peel-cleaner/leftover-review.svg` is a source-backed decision aid, explicitly not Peel UI. Its unknown branch says keep/investigate; it does not score or automate deletion.
- Reused the approved first-party example-data Space preview unchanged at `/Users/gabe/code/breathing-room/website/public/assets/blog/peel-cleaner/space-preview-2026-10-21.png`. It requires the visible example-data disclosure, the supplied caption, and review of its floating-assistant overlap. It is browser-rendered Breathing Room UI, not Peel UI, native behavior, or measured data.
- The actual Peel app screenshot was not downloaded or reproduced. It is linked from the article to the official version-pinned guide; capture details and screenshot-specific rights remain unknown.
- Interaction pass: implemented as a readable static decision aid, without file access, buttons, automation, or cleanup. Narrow-screen and theme review remains pending.

## Distinct peers and page scope

Existing research packets independently verify relevant Mac app-removal peers: FreeMacSoft's AppCleaner documents dropping an app, finding related files, and choosing a delete action (`docs/content/competitors/appcleaner/research.json`); Pearcleaner documents App Uninstall and Orphaned File Search, with its maintenance pause disclosed (`docs/content/competitors/pearcleaner/research.json`); Mole's packet documents a separate CLI/native maintenance product (`docs/content/competitors/mole/research.json`). CleanMyMac is a broader maintenance product with documented app-removal capability (`docs/content/competitors/cleanmymac/research.json`). These establish a real peer set, not a claim that each is interchangeable or has equivalent recovery controls.

No Peel alternatives page was created in this blog job. A genuinely useful comparison among removal workflows could be a separate assigned page, but would need its own verified, current decision criteria and review. The article links only to the existing `/comparisons/` hub and `/tools/` routes, not hidden draft records. The canonical product comparison currently exists only as `status: review`, `published: false` and is not linked as a public destination.

Alias decision: **Peel Cleaner** and official **Peel** identify the same product. No duplicate alias article was created. `blog-skip.md` records that resolution and links to the canonical owner/article.

## Exact outputs and pending review

- Article: `/Users/gabe/code/breathing-room/website/src/content/blog/peel-cleaner-mac-workflow.md` · SHA-256 `04494a6794f384058a3e153ed16afac807a95844b7c11e0380fa78cdc0ce7305`
- Decision aid: `/Users/gabe/code/breathing-room/website/public/assets/blog/peel-cleaner/leftover-review.svg` · SHA-256 `4aec067bb57bd90393a5a7e095806c1b68c7df372395b6e277a80bc58e13e941`
- Example-data image: `/Users/gabe/code/breathing-room/website/public/assets/blog/peel-cleaner/space-preview-2026-10-21.png` · SHA-256 `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a` (identical to the reviewed source asset)
- Alias skip record: `/Users/gabe/code/breathing-room-app/docs/content/competitors/peel-cleaner/blog-skip.md` · SHA-256 `2ad6a127371125184322470f5a3f441a9296497834a319344de72cac880fcc27`
- This handoff: `/Users/gabe/code/breathing-room-app/docs/content/competitors/peel-cleaner/blog-handoff.md`

Before publication: independently fact-check the draft against the retained claims; review both visual contexts, SVG accessibility, example banner/caption and mobile/light/dark rendering; recheck volatile release/pricing facts; run the site's required `pnpm check`, `pnpm build`, `pnpm test` in order and inspect generated metadata/routes/draft exclusion. These shared-site checks were not run because this scheduled task explicitly prohibits shared site builds. Local structural checks confirmed current draft status (`review`, `published: false`, `date: 2026-10-22`), 1,465-word article, the unchanged source-image hash/dimensions (2940 × 3468), SVG structure, and intended internal hub/tool links. The app's research check is not a website check or independent review. No score or publication approval is claimed.
