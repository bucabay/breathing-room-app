# Plumby workflow blog handoff

Task: `draft-blog-plumby` · draft completed **2026-10-22** · not publication approval.

## Exact outputs

- Article record: `/Users/gabe/code/breathing-room/website/src/content/blog/plumby-mac-workflow.md`
- Intended public path: `/blog/plumby-mac-workflow/`; record remains `status: review`, `published: false`.
- Original route-B diagram: `/Users/gabe/code/breathing-room/website/public/assets/blog/plumby/update-storage-review.svg`
- Reused first-party example preview: `/Users/gabe/code/breathing-room/website/public/assets/blog/plumby/space-preview-2026-10-21.png`
- Visual provenance: `/Users/gabe/code/breathing-room/website/public/assets/blog/plumby/provenance.json`
- This handoff: `/Users/gabe/code/breathing-room-app/docs/content/competitors/plumby/blog-handoff.md`
- Runtime receipt: `/Users/gabe/code/breathing-room-app/docs/content/.runtime/draft-blog-plumby.1792668197148840000.receipt.json`

## Reader job and evidence boundary

The article teaches a bounded workflow: prepare to review Mac storage before a specific update, distinguish candidates from an update requirement, check ownership/recovery/removal method, and separately verify available space. It does not prescribe a universal storage threshold or direct a reader to delete backups. It differs from the Plumby tool profile and concise comparison matrix by centering a concrete, non-destructive decision process.

Reused `docs/content/competitors/plumby/research.json` claims P01/P02/P07/P08/P09/P11/P12 and the retained verification batch, plus `capabilities.md` B01/B02 and `screenshots.json`. The official homepage and `pricing.md` remain in direct conflict about whether an iPhone backup can be restored from Trash. The page quotes and attributes both claims, says the method is unresolved, and advises no action on that candidate until version-specific official evidence resolves it. It does not choose a convenient interpretation. Quick Plunge’s optional scheduled behavior is disclosed; no universal fresh-approval promise is made.

Apple storage guidance was reused from the same-day verified source record in `docs/content/roundups/top-10-mac-cleaners-2026/draft-handoff.md` (Apple page published October 16, retrieved October 22, 2026). Its general guidance is not represented as an update-specific requirement. Plumby claims are dated October 21; do not overwrite source dates with the article date.

The draft does not assert app installation, scanning, cleanup, update success, free-space recovery, speed, safety, complete coverage, backup restoration, or binary feature parity. It avoids unresolved Plumby pricing because no price is needed for this workflow. Breathing Room is disclosed as the publisher’s product only for the distinct owner/project-investigation option, with preview, Python, signing, validation, and hosted-data limitations.

## Visual and interaction pass

The lead visual is an original decision diagram, not a redraw of Plumby UI, screenshot, or scan result. Its diagram labels explicitly separate the documented product workflow from the unknown iPhone-backup method. The official Plumby homepage is linked adjacent to the figure; its Overview asset remains link-only because reuse permission and pixel provenance are not established.

The later Space PNG is byte-identical to the screenshot-library source (`current-space-browser-preview`). Retain the example-data banner; the article identifies the capture date and source commit, says it is not native/measured/Plumby UI, and notes composer overlap. The screenshot library’s inherited privacy review and owner-requested reuse basis are not independent page approval. Provenance JSON records both visuals.

Interaction pass: non-mutating decision diagram plus an actionable five-check review. No fake interface, scanner, delete button, calculator, app execution, or destructive demonstration.

## Alternatives and alias treatment

Plumby remains its own canonical product identity, not an alias; no `blog-skip.md` is warranted. This is not an alternatives page. The existing `alternatives-handoff.md` documents its separate replacement intent and peer evidence reused from CleanMyMac, AppCleaner, and DaisyDisk packets; this job did not invent AlternativeTo relationships or repeat that page. No additional alternatives record or exception is needed.

## Validation and remaining gates

Actual checks: Node v25 with the site's existing Astro Zod and YAML 2.9.1 dependencies validated the schema-equivalent frontmatter, current dates, source records, review/unpublished flags, lead visual, allowed internal link, asset presence, provenance JSON, title (56 characters), description (158), 1,351 whitespace-counted body words, and two figure elements: **PASS**. `xmllint --noout` and Python ElementTree parsed the SVG; Python parsed provenance JSON: **PASS**. Copied preview SHA-256 matched both screenshot registry and provenance: **PASS**. Placeholder scan (`TODO`, `TBD`, `placeholder`, `lorem`, unresolved internal-link marker): no matches. The first Node attempt using a bare `yaml` import failed because the package is not a website-root dependency; rerunning against the existing pnpm-store module path succeeded. No dependencies were installed. Shared `pnpm check`, `pnpm build`, `pnpm test`, public page fetches, browser/rendered checks, and independent review were not performed. Do not claim publication readiness or that the draft has a public preview route.

Final SHA-256 snapshot:

| Real file | SHA-256 |
| --- | --- |
| `/Users/gabe/code/breathing-room/website/src/content/blog/plumby-mac-workflow.md` | `24d2b130d6189f96b17fb0cd81a9eec12d744a6865574bbf36f054956f445a45` |
| `/Users/gabe/code/breathing-room/website/public/assets/blog/plumby/update-storage-review.svg` | `7a4fd7d89b5970b6d0bbccef43d2312160780c9aa2ace0549caa9d9a6663e43b` |
| `/Users/gabe/code/breathing-room/website/public/assets/blog/plumby/space-preview-2026-10-21.png` | `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a` |
| `/Users/gabe/code/breathing-room/website/public/assets/blog/plumby/provenance.json` | `91adfda2afead09fae1a4f993969f53a82a589da5cf5dddf41174a65c4ce3f8c` |

The handoff cannot contain its own stable hash without changing that hash; its final hash is recorded in the receipt.

Before publication, independently review the exact snapshot and the P08 conflict; assess diagram and screenshot legibility at narrow/tablet/desktop widths in both themes; inspect page metadata and draft exclusion in the authorized serialized site review; refresh volatile official claims as needed. Keep the iPhone-backup method explicitly unresolved unless consistent version-specific evidence is added. No minimum 85-point independent score is assigned here.

No source packet, queue/database, shared site schema/navigation/tests, other record, account, credential, installation, scan, cleanup, settings, message, purchase, commit, push, deployment, or unrelated work was changed.
