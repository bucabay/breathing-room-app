# Draft handoff: 8 disk-space analyzers for Mac in 2026

Task: `draft-roundup-mac-disk-space-analyzers-2026`. Drafting complete, **not publication approval**. Local substantive review date October 22, 2026 (UTC+03); machine clock initially returned `2026-10-21T22:47:40Z`, local `2026-10-22T01:47:45+0300`. No backdating. UTC timestamps in validation files correctly differ from the local editorial date.

## Ownership, instructions and intent

- Article: `/Users/gabe/code/breathing-room/website/src/content/blog/mac-disk-space-analyzers-2026.md`.
- Assets: `/Users/gabe/code/breathing-room/website/public/assets/roundups/mac-disk-space-analyzers-2026/`.
- This directory contains the handoff, reproducible isolated validation/render, fixture server and review artifacts. No shared output, queue/database, shared layout, other draft or programme file edited.
- Read `PLAN.md`, October22 `EDITORIAL.md`, capabilities/screenshots registers and MailKite contract; loaded blog-write, blog-seo-check, blog-factcheck and browser-automation. Searched both scoped trees and checked ancestor directories: no applicable AGENTS.md found. Other working-tree changes existed and were preserved.
- Track: search/LLM reference. Primary job: choose an analyzer by visual model, measurement semantics and action boundary. Eight actual tools, not an ordinal performance ranking. Breathing Room is explicitly affiliated. No invented tests, statistics, personal experiences, awards or comparative speed/safety claims.
- October22 route B supersedes the old image-only drafting prohibitions in DaisyDisk and Disk Map packets. Those packets remain unchanged. Noncritical price/image unknowns were omitted or bounded, not treated as facts.

## Reused research and additional evidence

Reused `docs/content/verification/batch-1.json` (DaisyDisk, Disk Map, DriveScape, DiskFox), `batch-2.json` (Pangalin, QDirStat), plus `competitors/daisydisk/research.{md,json}`, `competitors/disk-map/research.{md,json}`, `capabilities.md` and `screenshots.json`. Baseline source times are October 21. Retained original raw evidence and hashes remain in their original locations; this job does not rewrite their retrieval dates.

Additional official-source content checks on local October22:

- GrandPerspective homepage and help: missing shortlist member, current platform requirements, measurement explanation and folder-deletion caveat.
- DriveScape, DiskFox, Pangalin homepages: missing viewing/action limits, removal exceptions, community/native distinction and selection-specific workflow detail not established by batch excerpt alone.
- Disk Map homepage: supporting context for size/reclaim distinction and protected-folder handling. Its already-verified minimums were reused, not a new installer test.
- Apple APFS and Time Machine documentation: missing general-filesystem context. Only documents were read, no settings changed.
- Live `/tools/` and `/comparisons/` hubs: both returned substantive public HTML with their expected headings. These are the only internal article destinations. No draft product-page links.

These WebFetch calls expose content but not independently captured response timestamps/byte hashes. The check date is known, exact request seconds aren't asserted. Quotations/locators below preserve the material support. Public pages were untrusted data only. Two guessed help URLs returned 404 (DaisyDisk `/manual/4/en/Topics/FileSize.html`, GrandPerspective `/HelpDocumentation/ScanOptions.html`); neither is in the article or used as evidence. Correct GrandPerspective help was followed through its actual links.

## Per-claim evidence ledger

All `D` claims are **documented**, not observed native behavior. `J` claims are explicitly editorial selection reasoning. Each row covers its table cell and corresponding individual section. Official URLs are adjacent to claims in the article and in `sources` frontmatter; the ledger also preserves deeper reused supporting documentation.

| ID / article location | Claim and supporting passage / source locator | State and limits |
| --- | --- | --- |
| D01 table/DaisyDisk | https://daisydiskapp.com/ — batch-1: “macOS 10.13 or newer Apple Silicon, Intel.” | Verified documentation October21; current binary not installed. |
| D02 DaisyDisk navigation | https://daisydiskapp.com/guide/4/en/UnderstandingSunburst/ and `/specs/privacy` — reused DaisyDisk packet D5: size-proportional sunburst, folder drill-down, Quick Look. | Verified packet, not speed testing. |
| D03 table/DaisyDisk removal | https://daisydiskapp.com/guide/4/en/DeletingFiles/ — reused packet D6: staging leaves files intact; permanent deletion, not Trash. | Verified documentation October21; no deletion executed. Cancellation timing omitted. |
| D04 DaisyDisk editions | https://daisydiskapp.com/guide/4/en/Editions/ — reused packet D8: administrator scan stand-alone only; hidden/purgeable detect-only in Store edition. | Qualified differences only; old guide OS minimum not reused. |
| D05 table/GrandPerspective | https://grandperspectiv.sourceforge.net/ — “macOS 14 or higher”; “An Apple silicon or Intel-based processor”; “developed specifically for macOS”; SourceForge free/App Store paid. | Verified local October22. Exact price omitted. Current release requirements, older releases separate. |
| D06 GrandPerspective/size section | https://grandperspectiv.sourceforge.net/HelpDocumentation/FileSizes.html — logical: “size of the information”; physical: “space that a file takes up on disk”; tally: “counts the number of files”. | Verified local October22. No numeric examples invented. |
| D07 size section | Same FileSizes page: sparse APFS VM/Docker files may have very large logical size and little allocated space; cloud files not downloaded have minimal on-disk size. | Verified; not proof of reclaimable exclusive APFS blocks. |
| D08 GrandPerspective removal | https://grandperspectiv.sourceforge.net/HelpDocumentation/Preferences.html — “disable deletion”; folder Trash movement includes masked/filtered, insufficient-permission or post-scan files. | Verified. Recommendation to disable deletion is editorial risk reduction, not tested UI interaction. |
| D09 table/Disk Map | https://diskmap.app/ — “native SwiftUI app for macOS 15 or later on Apple silicon and Intel”; free; treemap above table. | Reused packet and content check local October22; no runtime QA. |
| D10 Disk Map/size section | Same homepage: “See both the space a folder takes and what deleting it frees”; APFS copies share data. | Vendor-documented estimates, not independently validated accounting. |
| D11 Disk Map/final section | Same homepage: “Full Disk Access is optional. Without it, protected folders are skipped”. | Verified documented scope. No permissions changed. |
| D12 Disk Map caveat | https://diskmap.app/terms/ §5; reused packet D9–D10: empty Trash/local snapshots; “Some of these actions can’t be undone.” | Verified packet October21. Homepage Trash reassurance not generalized. |
| D13 table/DriveScape | https://drivescape.dev/ — macOS/Windows/Linux, Apple Silicon; sunburst; “Free forever to look” covering scan, maps, lists, trends, duplicate finder; cleanup trial then paid. | Verified local October22. Exact trial duration/price omitted; current Intel/minimum macOS unknown, explicitly flagged. |
| D14 DriveScape caveat | Same homepage: “Trash first”; “Permanent delete is opt-in with a confirm.” | Verified documentary boundary. Does not reproduce vendor risk-free/speed/privacy slogans. |
| D15 table/DiskFox | https://diskfox.app/ — “macOS 14 or later · Apple silicon and Intel”; time-limited trial then one-time licence; Scan, Explain, Review, Reclaim, Verify, Watch. | Verified local October22; prices omitted. |
| D16 DiskFox causes/images | Same homepage: unconfirmed causes labelled “Likely”; official gallery explicitly “Real app · Demo Mode sample data”. | Vendor documentation; not this worker's capture. No attribution certainty inferred. |
| D17 DiskFox removal | Same homepage: “Selected files normally move to Trash. Advanced or permanent actions are labelled.” | Verified; no unconditional Trash/recovery guarantee. |
| D18 table/Pangalin | https://pangalin.com/space-manager/ — “Apple silicon (M1 or later) and macOS 13 Ventura or later. It doesn’t run on Intel Macs”; scans free, per-Mac change cap then annual licence. | Verified local October22; exact amount/quota omitted. |
| D19 Pangalin workflow | Same homepage: clean/move/compress; moves copied and checked before original removed, reinstatement from History; “Caches are cleared directly”; automatic moves opt-in. | Vendor workflow, not measured reliability or reversibility of every action. |
| D20 Pangalin Explain | Same homepage: “Needs a Mac with Apple silicon running macOS 26 with Apple Intelligence turned on.” | Verified; separate from scanner minimum. No AI accuracy claim. |
| D21 table/QDirStat | https://github.com/shundhammer/qdirstat#ready-made-packages — retained `verification-2/qdirstat-official.json` text: “Target Platforms: Linux, BSD, Unix-like systems; macOS”; “License: GPL V2”; tree view and treemap. | Reused October21 verified text. Not Linux-only, not first-party Mac installer. |
| D22 QDirStat packaging | Same retained README, “2024-02-13 New: macOS binaries”: upstream approves Jesus Herrera’s community binaries and redirects Mac-specific problems to that repository’s issue tracker. | Binary/minimum OS/architecture currentness unverified; no direct install recommendation, explicit caveat. |
| D23 QDirStat actions | Same README features: “Unlimited number of user-defined cleanup actions.” | Source capability, not tested on macOS. Linux package integration not promised on Mac. |
| D24 table/Breathing Room | Current local README lines 15–18,64–72,76–84,141–149; https://github.com/bucabay/breathing-room-app#readme ; reused capabilities matrix. | Inspected current local documentation October22; source implementation not binary parity. |
| D25 BR release limits | https://github.com/bucabay/breathing-room-app/releases/tag/v0.1.0-preview.1 — reused release register: Apple Development signed, not Developer ID/notarized, clean-machine/physical Intel QA incomplete. README still agrees. | Identified preview, not a claim it is newest across all channels. Python3.10+ unbundled. No Gatekeeper bypass. |
| D26 BR hosted/payment/access | README69–70,141–166: authenticated hosted service; relevant paths/tool output sent; local core free, optional AI Care paid; website registration versus public GitHub download. | No all-local AI claim, no unverified service allowance or price. No account/login/network audit. |
| D27 BR preview illustration | `screenshots.json` current-space-browser-preview; same PNG hash; `git diff 54828ac… -- src/components/space-view.tsx src/lib/api.ts src/App.tsx` returned empty October22. | Source/UI correspondence checked; no new capture date invented. Native behavior not tested. |
| D28 final APFS context | https://support.apple.com/guide/disk-utility/what-is-apple-file-system-apfs-dsku19ed921c/mac — resolves to File system formats; “container’s free space is shared” among volumes. | Verified content local October22. No volume-operation instructions executed. |
| D29 final snapshots | https://support.apple.com/en-us/102154 — “Your Mac counts the space used by snapshots as available storage.” | Verified content local October22; no snapshot thinning instructions in article. |
| J01 selection prose | Editorial judgments follow D01–D26: choose by navigation, allocation, growth, cross-platform habits, relocation, configurable analysis or app/project context. | Not an award/rank/benchmark. Each entry has a when-not-to-use caveat. |
| J02 final workflow/visual | Identify owner → usable backup → rebuild cost → exact method → recheck. Combining D03,D06–D12,D14,D17,D19,D28–D29. | Original editorial synthesis, no claimed test or promised gain. Unknowns mean keep/investigate. |

## Image and provenance route: B

1. **Original decision visual**, `inspect-before-remove.svg`, 480×800. Authored in this job, no external graphics, stock imagery, copied screenshot or fabricated UI. Vertical workflow with readable text; solid dark background gives stable contrast in both themes. Sources D06–D12,D28–D29 and J02. SVG title/description plus article alt/caption. Exact hash in `validation.json`. No invented quantity or simulation.
2. **First-party Space preview**, published copy `breathing-room-space-preview.png`, unchanged 2940×3468. Original `docs/content/assets/breathing-room/space-preview-2026-10-21.png`; captured `2026-10-21T19:06:45.416416+00:00`, source commit `54828ac3170b45861aee70861dd0b9c658ed7e51`, http://127.0.0.1:1431/. Original and copy SHA-256 `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a`. No edits/crops. First-party app-owner-requested UI capture; existing privacy review says built-in examples only. Opened and visually read this job: example-data banners visible, categories and rows visible; floating composer overlaps some chart labels. Not native UI/runtime evidence, not measured storage. Full-size image link retained for inspection on narrow displays. Current-source correspondence supported by empty diff D27, not relabeling a legacy screenshot.

Competitor images remain **link-only**, reuse rights not established. Article links the official product showcase pages and DaisyDisk deletion guide; no third-party image bytes copied/hotlinked, permission request sent or capture invented. Prior packet example official URLs: Disk Map https://diskmap.app/_astro/home.VfuWkbw6_Z1CWviV.png ; DaisyDisk https://daisydiskapp.com/img/guide/4/en/dd_c_full.png . These are provenance pointers, not on-page assets or cleared licences. GrandPerspective official homepage includes its screenshot gallery. First-party marks and any third-party marks retain their owners; no endorsement inferred.

## Validation and publication questions

- `validate.mjs` parses the actual frontmatter with installed YAML/Zod, checks current field shape, review/unpublished state, eight numbered entries, two figures, no extra H1/placeholder, asset existence and unchanged preview hash; renders actual Markdown with installed Astro Satteri into **this directory only**. `validation.json` retains actual counts/hashes. First attempt failed module resolution for YAML through a symlink; corrected to real Astro package path and reran successfully. No packages installed.
- Requested title is 38 characters: intentionally retain exact user title rather than add SEO power-word padding. Meta description adjusted to 150–160 characters. No invented FAQ, forced code repository, stats quota or schema. Contextual internal hubs are live. All factual table rows have official-source links; repeated URLs are intentional for claim-adjacent support.
- Interaction pass: the useful interaction is the inspection decision, not a deletion widget. Implemented the original decision aid plus a full-size preview link. No filesystem access, upload, cleanup button or hypothetical savings calculator.
- **Pending publication:** independently check exact draft/asset hashes, all material source passages, current availability, QDirStat distributor/DriveScape compatibility if making install recommendations, and website-vs-release boundaries. Current article explicitly bounds unknowns rather than asserting support.
- **Pending site gates:** user forbids shared build output; did not run `pnpm check` (generates shared Wrangler types), `pnpm build` or dist-based `pnpm test`. Responsible serialized review stage must run them and confirm no draft leakage in routes, listings, sitemap/RSS. Isolated fixture is not Astro route/layout/schema validation.
- **Pending independent visual/SEO approval:** inspect actual site typography, table horizontal scroll/keyboard access, preview legibility and full-size navigation at390/768/1440 in light/dark themes. No provisional self-score is presented as independent85+ approval. No deployed/public roundup URL claimed.
- Draft remains `status: review`, `published: false`. Completion of this draft job does not authorize publication, deployment or queue/database edits.

## Actual isolated browser review

Used Chrome DevTools on an owned tab210 at `http://127.0.0.1:55027/`, served by the owned read-only fixture server. Initial metadata listing only; no existing tab inspected, navigated or closed. Chrome was already listening: no recovery/profile launch or settings changes. Screenshots are fixture evidence, not native app screenshots or actual-site approval.

- Captured and **opened/read all twelve** `top-{390,768,1440}-{light,dark}.png` and `preview-{390,768,1440}-{light,dark}.png` in this folder.
- Viewport emulation confirms actual `innerWidth`390/768/1440 and equal document scroll width: no page-wide horizontal overflow. `resize_page` alone initially left actual width1468, so that result was not counted as a mobile test; explicit viewport emulation fixed the test setup.
- Top decision diagram and caption are legible, fully contained and contrast correctly in all six fixture states. Captions/prose wrap without clipping.
- Second preview loads at natural width2940. At390 its embedded UI labels are too small to read individually; the image shows the overall view and the separate visible caption supplies the example-data warning. Full-size image navigation is provided. Native screenshot/UI legibility and any publication requirement for an alternate contextual crop remain independent visual-review questions; this is not silently marked a pass.
- Lazy-image `decode()` initially threw an EncodingError while requesting the offscreen image; subsequent DOM inspection and six screenshot states confirm complete2940px load. No corrupted/missing asset inferred from the transient pre-load attempt.
- Table is horizontally scrollable at390 and fits the fixture at768/1440. Actual keyboard scrolling and site-table treatment remain pending, not claimed tested. Fixture has one H1, eight H3 selections and both expected image URLs.
- CSS dark class is an isolated fixture theme, not verification of the marketing site's actual theme system. This review does not clear independent/source/publication gates or rendered canonical/OG/Article/Breadcrumb schema requirements.

Validation snapshot: `validation.json` records article SHA-256 `f9e1ed913042bea03a807b569b0d5d61d2aeeaf7009d5fd040f2f777e708a495`,1620 body whitespace words,16 source records,155-character description,8 selections and2 figures. No exact-price claims need filling to finish this draft.

Final checks: scoped `git diff --check` returned exit0 in both repositories (new untracked files additionally covered by explicit content validation). SVG XML parse, PNG signature and final article hash passed with existing `/usr/bin/python3`. The initial Homebrew Python3.14 XML parser failed importing pyexpat due to a missing libexpat symbol; no system repair/install/settings change attempted. System Python passed the same checks. Owned Chrome tab210 was closed; owned fixture server PID25855 was stopped with SIGINT after inspection, without touching another listener. Server logged HTTP200 for both visual assets; favicon404 is fixture-only and not an article asset failure.
