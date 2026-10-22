# AVG PC TuneUp workflow blog handoff

Task: `draft-blog-avg-pc-tuneup` · Draft date: **2026-10-22** · **Complete textual draft; not publication-approved.**

## Exact owned outputs

Marketing root: `/Users/gabe/code/breathing-room/website`.

| File | SHA-256 |
| --- | --- |
| `src/content/blog/avg-pc-tuneup-mac-workflow.md` | `bfe4392722fd2f2aa6c4ffca4b702a62693905fb48db838dbc7f84b9b9fb45c7` |
| `public/assets/blog/avg-pc-tuneup/duplicate-review.svg` | `11b22dd28d92751a77246db4a89730084ab5550c22457b619d27e382dbb9e3fb` |
| `public/assets/blog/avg-pc-tuneup/space-preview-2026-10-21.png` | `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a` |
| `docs/content/competitors/avg-pc-tuneup/blog-handoff.md` | See completion receipt. |

Intended route: `/blog/avg-pc-tuneup-mac-workflow/`. Content fields are `status: review`, `published: false`, and date/updated `2026-10-22`. Draft filtering means this is not a public route or publication approval.

## Intent and evidence reuse

This article teaches one task: how someone moving from AVG PC TuneUp on Windows can review apparent duplicate files on a Mac before removal. It distinguishes identical-content detection from keeper choice, ownership, independent recovery, similar-photo review and cache rebuild cost. It is not the AVG profile, comparison matrix, or alternatives roundup. Its conclusion-first advice is to treat a match as a clue and keep/investigate whenever ownership or restoration is uncertain.

Reused `docs/content/PLAN.md`, `EDITORIAL.md` October22 update, shared `docs/content/capabilities.md` and `docs/content/screenshots.json`, plus the existing `research.json`/`.md`, retained AVG source excerpts, validation record and verified baseline provenance. The two requested `capabilities.md` and `screenshots.json` paths did not exist inside the competitor subdirectory; their canonical shared records were read. Existing records report no applicable `AGENTS.md` in the scoped repositories/checked ancestors.

The retained research validator was run again and passed all 130 structural/source-excerpt checks. This reuses prior official-source verification; pages were not redundantly refetched. Core claim boundaries retained:

- AVG PC TuneUp is the Windows discovery identity; AVG has separately documented Mac instructions. Windows registry/Sleep Mode features are not represented as Mac features.
- AVG’s Mac guide documents identical-content duplicate detection and age-based/manual selection. No independent accuracy, safety, deletion, or recovery test is claimed.
- Similar-photo analysis is not treated as exact duplication. AVG support for package-manager caches is not verified, not presented as absent.
- Vendor Mac minimums conflict (PC footer 10.10, Mac marketing 10.12, dedicated 4.x requirements 10.13). The conflict is stated; no legacy OS installation recommendation is made.
- Trial evidence conflicts between PC marketing and Windows FAQ; it does not establish Mac trial terms. Purchase fine print, exact patch, installer signing/notarization, and runtime remain unverified. Numeric AVG prices were omitted.
- Breathing Room source-supported cache/owner investigation is narrowly described, with preview, Python, signing/notarization, runtime and hosted-service limitations. Source inspection is not binary or hands-on validation.
- AlternativeTo is cited only as discovery provenance, never as capability evidence or an endorsement relationship.

No alias skip was needed: `avg-pc-tuneup` is the canonical owner. This is not an alternatives page, so no new competitor relationship or alternatives exception was asserted; the separately owned alternatives draft already names verified peers and sources.

## Visuals and interaction pass

Route B was used under the October22 editorial policy; restricted AVG imagery was not copied or hotlinked.

1. `duplicate-review.svg` is a newly built, source-backed decision aid with SVG title/description, matching descriptive alt text, caption, and source/limitation disclosure. It guides the reader from a detected match through location/owner, keeper, and backup checks. It is not AVG UI, a test, or a delete action. SVG XML parsed successfully with Ruby REXML.
2. `space-preview-2026-10-21.png` is an unchanged first-party copy from `docs/content/assets/breathing-room/space-preview-2026-10-21.png`. Its SHA-256 matches the screenshot inventory (`9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a`). Capture time is `2026-10-21T19:06:45.416416+00:00`, source commit `54828ac3170b45861aee70861dd0b9c658ed7e51`, dimensions 2940×3468. The required caption says example data only, not a native scan, measured activity or cleanup result; composer/chart overlap is disclosed. No crop or edits were made.

The interaction pass is a non-interactive decision aid; a delete/run control would be inappropriate. The article links only to `/comparisons/`, the known live hub. It does not link to the unpublished comparison or alternatives records.

## Validation and remaining review

- `python3 docs/content/competitors/avg-pc-tuneup/validate.py`: **passed**, 130 checks, zero failures.
- Ruby standard-library YAML check: **passed** for frontmatter parse, draft fields, seven dated HTTPS sources, and required fields. Title is 54 characters; description is 159 characters.
- Local image references: **passed**, both referenced assets exist. SVG title/description and XML parse: **passed** with Ruby REXML. PNG copy hash matches retained source hash.
- Article structure: **passed**; 1,411 whitespace-delimited words, no body H1 (the renderer supplies the title), two figures, and no placeholder markers.
- `shasum -a 256`: **passed** for article and both assets; hashes are listed above.
- Initial Node YAML check did not run because `yaml` is not resolvable in the website workspace. Initial Python XML check could not run because local Python 3.14 `pyexpat` is incompatible with system libexpat; the SVG check passed with Ruby REXML instead. No dependency installation or system change was attempted.
- Not run: shared site `pnpm check/build/test` (prohibited by task), rendered HTML/canonical/schema/publication-leak checks, browser review at mobile/tablet/desktop and both themes, external live-link check, or independent claim/visual/SEO approval. No publication score is awarded.

Independent review must inspect this exact snapshot, confirm claim-adjacent source passages and the route-B visuals, validate the eventual rendered metadata and draft exclusion through the authorized serialized site process, and inspect responsive/theme legibility. Refresh volatile compatibility/offer facts before publication. Do not resolve the recorded OS/trial conflicts by assumption. Draft completion is not publication approval or deployment.

No other record, queue/database state, shared site file, build output, test fixture, navigation, schema, or unrelated work was changed. No account, purchase, message, credential, app installation, cleanup, settings change, commit, push, or deployment occurred.
