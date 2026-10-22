# 4-Organizer Ultra workflow blog handoff

**Draft status:** review, unpublished. Created October 22, 2026. This is a complete source-backed article draft, not publication approval or a hands-on product review.

## Owned outputs and hashes

| File | SHA-256 | Purpose |
| --- | --- | --- |
| `/Users/gabe/code/breathing-room/website/src/content/blog/4-organizer-ultra-mac-workflow.md` | `d9dda703a4e8b527d5c853ba38d625eb95b8d5a0c909cbc041e1011eb9396cd4` | 1,425-word workflow page; public path if approved: `/blog/4-organizer-ultra-mac-workflow/`. `status: review`, `published: false`. |
| `/Users/gabe/code/breathing-room/website/public/assets/blog/4-organizer-ultra/migration-workflow.svg` | `2003f4fbe25518626a5a8999c027a9eeb5adca2f3b4a59daa69a5326f58fea00` | Original accessible workflow diagram, not either product UI or a test. |
| `/Users/gabe/code/breathing-room/website/public/assets/blog/4-organizer-ultra/space-preview-2026-10-21.png` | `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a` | Unmodified first-party Space browser preview copied from the reviewed alternatives asset. Visible example-data disclosure is preserved; not a native scan or result. |

## Evidence and editorial decisions

- Reused `research.json` / `research.md`, `capabilities.md`, and `screenshots.json`; no unnecessary product refetch or repeat research. The old screenshot-only `draftingAllowed:false` did not prevent this draft under the October 22 route-B policy.
- The article teaches a platform-switch workflow: preserve/organize originals, investigate Mac storage separately, and make narrowly scoped cleanup decisions. It does not repeat the comparison matrix or present Ultra as a Mac app.
- Official sources describe Ultra for Windows 11/10 x64, destination previews and sorting rollback. Rollback limitations are included; sorting rollback is not represented as deleted-file recovery.
- Ambeteco support's absolute claim that deletion is technically impossible conflicts with the guide/changelog describing Deep Scan deletion. The draft explicitly identifies this conflict and omits the absolute safety promise.
- Route B visuals: an original workflow diagram plus a first-party Breathing Room browser preview with its example-data/native limitations. No competitor image was copied or hotlinked; the official Quickstart is linked and accurately described.
- Breathing Room affiliation and preview limitations are explicit, including Python 3.10+, non-notarized preview, hosted-assistance data boundary, and absence of file-sorting parity. No test, benchmark, savings, or cleanup outcome is claimed.
- Internal links are restricted to the existing `/comparisons/` hub and `/tools/storage-headroom/` utility. The separately owned alternatives handoff already documents verified peers; no alternatives exception is needed for this distinct workflow article.

## Checks performed

- Node 25 static assertions passed: required frontmatter fields, review/unpublished state, source-conflict disclosure, referenced-asset existence, SVG root/closure and accessible title/description labeling. Article word count: 1,425.
- `xmllint --noout` passed on `migration-workflow.svg`.
- SHA-256 recorded for all three exact output files; the copied PNG hash matches `screenshots.json` and existing alternatives asset provenance.
- An initial Python XML parse was attempted but could not run because Python 3.14's `pyexpat` failed to load against the system libexpat. The independent `xmllint` check passed; the Python failure is not represented as a validation pass.
- No marketing site check/build/test or browser rendering was run. This task does not authorize a shared site build; those validations belong to the serialized site-validation/review stage.

## Required independent review before publication

1. Independently check claim wording against the retained sources and refresh current/version-sensitive claims before release.
2. Inspect both visuals in page context for legibility, captions, alt text, visible example-data notice, and route-B provenance.
3. Run the separately authorized marketing-site `pnpm check`, `pnpm build`, then `pnpm test`; inspect generated metadata, links, draft exclusion, and asset loading.
4. Perform responsive light/dark browser review at mobile, tablet, and desktop widths; no visual browser approval is claimed here.
5. Keep `status: review` and `published: false` until factual, visual, SEO, technical, and independent review gates pass.

No queue/database change, app installation, account, purchase, message, cleanup, commit, push, or deployment was performed.
