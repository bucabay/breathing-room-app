# MacKeeper workflow blog handoff

Task: `draft-blog-mackeeper` · reviewed **2026-10-22**. Draft artifact complete for internal review; this is not independent approval or publication clearance.

## Outcome and ownership

Created one complete workflow article at `/Users/gabe/code/breathing-room/website/src/content/blog/mackeeper-mac-workflow.md`, intended route `/blog/mackeeper-mac-workflow/`. Frontmatter is `status: review`, `published: false`, dated and updated 2026-10-22. Its distinct reader task is separating a MacKeeper storage-cleanup decision from the separate need for security/privacy services. It does not repeat the product profile or the Breathing Room head-to-head matrix, and does not give unsupported removal steps.

Owned files only: that article, this handoff, and the three assets in `website/public/assets/blog/mackeeper/`. No research packet, shared site code, navigation, schema, tests, content queue or database was edited. Existing unrelated working-tree changes were left untouched. No alias skip applies: canonical product remains `mackeeper`, with no verified alias in its retained record.

## Evidence and conflicts retained

Read `PLAN.md`, `EDITORIAL.md` (including the October22 update), `capabilities.md`, `screenshots.json`, MacKeeper `research.md`/`.json`, existing verification, current marketing schema/publishing contract, and relevant blog-write/SEO/fact-check instructions and adapted MailKite contract. No applicable AGENTS.md was found in either scoped repository or checked ancestors. Existing baseline and targeted official-source findings were reused; no broad refetch or browser work was needed.

- MacKeeper identity and Clario Tech FZCO association: research `C1`, official sources `S1`/`S2`. The product is a broader maintenance/security/privacy suite, not interchangeable with a storage-only utility.
- Cleanup categories, reminders, similar-photo finding and app leftovers: `C6`/`C7`, `S2`/`S3`; treated as vendor-documented categories, not measured recovery, accuracy or completeness.
- Per-file controls, exclusions, confirmation, Trash/recovery semantics, unattended cleanup, helper grouping and package-manager cache adapters remain **not verified** (`C9`/`C10`). Article does not assert those features are absent or provide a click path.
- The requirements conflict remains explicit (`C2`/`C3`/`C15`): marketing identifies 7.8 (September 2026), macOS 10.15+ and 100 MB; the linked Help page describes versions 5/6, different OS scopes, Intel/M1-or-newer, 2 GB RAM and 113 MB. No invented unified 7.8 spec and no installation recommendation.
- Pricing remains only the attributed homepage headline “Starting at $10.95/month.” Currency code, bill total, device count, taxes, introductory duration and renewal total are unknown. EULA recurrence/cancellation language is qualified; no comparative cheaper claim.
- Breathing Room strengths and limitations reuse `capabilities.md`/research `BR1`: free local capabilities versus optional advertised hosted AI Care; identified preview, Python inventory requirement, signing/notarization and runtime limits; hosted assistant requires internet/authentication and may send relevant context. No binary parity, safety, speed or savings claim.
- Discovery source `https://alternativeto.net/software/mackeeper/about/` is retained only as discovery evidence; no feature assertions or invented AlternativeTo relationship derive from it.

The separate alternatives intent is supported by the already-created [`alternatives-handoff.md`](alternatives-handoff.md), which reports distinct, verified peers and packet citations (CleanMyMac, DaisyDisk and AppCleaner). This blog is not another alternatives list and invents no replacement relationship. The comparison draft is at the known public-source content path `website/src/content/comparisons/mackeeper.md`; it remains an unpublished review record. Contextual links in the article point only to live hubs/utilities (`/comparisons/`, `/tools/cache-rebuild-checklist/`), not unpublished product records.

## Visual and interaction pass

Route B. The top `suite-or-storage.svg` is an original source-backed task-selection aid. `change-boundary.svg` later separates a storage finding from an actual change decision. Both are editorial diagrams, not MacKeeper UI, screenshots, or test results. They include accessible title/description metadata and are vertically laid out. The official Safe Cleanup image reference is linked from the article’s caption/paragraph only; it was not downloaded, reproduced or hotlinked. Terms reserve rights; no permission request was sent and no reuse right is implied.

The third visual is an unchanged copy of the existing Breathing Room Space browser preview. Original and copy SHA-256: `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a`. It retains the screenshot inventory’s example-data, browser-only, non-native and non-measurement warnings. The existing capture has assistant overlap, which the caption discloses; it was not cropped. The diagram plus four-task checklist is the useful no-JavaScript interaction pass; no simulated cleanup, filesystem access or executable deletion workflow was added.

## Exact outputs and SHA-256

| File | SHA-256 |
| --- | --- |
| `/Users/gabe/code/breathing-room/website/src/content/blog/mackeeper-mac-workflow.md` | `662f0f4ed6e876f3fe158a84bdac89fe63ba6173cd670debe93fc939fd14e776` |
| `/Users/gabe/code/breathing-room/website/public/assets/blog/mackeeper/suite-or-storage.svg` | `8ff22c7a291a32039bb30d11ed84b99a52a3114ac190de08e0f161c910350e0d` |
| `/Users/gabe/code/breathing-room/website/public/assets/blog/mackeeper/change-boundary.svg` | `0a33b9825bf5573c9adbffd262ba6f4b71ec7153165b0d4f8bd55838dd5790ac` |
| `/Users/gabe/code/breathing-room/website/public/assets/blog/mackeeper/space-preview-2026-10-21.png` | `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a` |

## Actual validation and remaining gates

- **PASS:** Node 25 parsed the YAML and validated it against a direct equivalent of the current content schema (title, description, status, publication, dates, author, source shape and URL/date formats). Draft flags and date values were asserted.
- **PASS:** targeted structural assertions found six H2s, three nonempty image paths with alt text, and no placeholder or unresolved-link markers. Title length 55 characters; description length 158; approximate whitespace-split body length 1,324 words.
- **PASS:** `/usr/bin/python3` parsed both SVGs as XML. Existing screenshot copied byte-for-byte and hash matches the inventory.
- **PASS:** exact internal utility routes were confirmed in `src/lib/tools.ts` and `src/pages/tools/cache-rebuild-checklist.astro`; comparison hub is referenced as existing route. No unresolved internal-link placeholder remains.
- **Recovered check failure:** default Homebrew Python 3.14 XML parsing could not load `pyexpat` due to the existing system `libexpat` symbol mismatch. Retried using `/usr/bin/python3`; both SVG parses passed. No packages, settings or files were changed by that failure.
- **NOT RUN:** shared `pnpm check`, `pnpm build`, `pnpm test`; expressly excluded by the task. No browser/rendered review, isolated draft fixture, live link fetch, binary/app test, independent factual/visual review or score was performed. Existing screenshots are not this article’s rendered-page QA.

Before publication, independently inspect these exact hashes and claim mapping, verify volatile official facts, review diagram legibility and screenshot context at mobile/tablet/desktop in light/dark themes, then use the responsible isolated review/build/test workflow. Keep `review`/`false` until all independent evidence, visual, SEO and rendered gates pass. MacKeeper’s image rights, exact 7.8 requirements and detailed cleanup controls remain unresolved; route B avoids copying the image but does not resolve those factual unknowns. No publication or deployment is implied.
