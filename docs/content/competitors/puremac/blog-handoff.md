# PureMac workflow blog handoff

Task `draft-blog-puremac` · prepared 2026-10-22 · **complete internal draft, not publication approval**.

## Owned outputs

- Article: `/Users/gabe/code/breathing-room/website/src/content/blog/puremac-mac-workflow.md`
- Intended public path: `/blog/puremac-mac-workflow/`; record remains `status: review`, `published: false`.
- Visual assets: `/Users/gabe/code/breathing-room/website/public/assets/blog/puremac/inspect-before-removal.svg`, `puremac-space-explorer.png`, `PureMac-MIT-LICENSE.txt`, `breathing-room-space-preview.png`, `provenance.json`.
- Article SHA-256: `2ddc58172b3b44eb61c9ad077f59d068bbb837144ea6c37d241a91ff8199ac81`.
- Visual route A: official PureMac Space Explorer screenshot with MIT notice and credit, plus first-party Breathing Room browser preview retaining its example-data limitations. Original decision diagram is explicitly editorial, not UI or test evidence.

| Asset | SHA-256 |
| --- | --- |
| `inspect-before-removal.svg` | `5a1341081f3d632a78a28443ddafd2d2c5db68e991c079d2160ead6aab4d42ca` |
| `puremac-space-explorer.png` | `739c0d02239cd73e69d67db79fb6f9a95da52aa0ce402a4ddb59889afe4c4ec1` |
| `PureMac-MIT-LICENSE.txt` | `88258dee1e1b9ced27bfbe7c40b3374ac1900adc82c427f71459a3d1e0976e2f` |
| `breathing-room-space-preview.png` | `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a` |
| `provenance.json` | `29c41fdfa72bcd3a4d467d060dc4880f92465a420fc3b6a6b92b0332ffc29ff7` |

## Editorial intent and evidence

The article teaches one distinct task: inspect allocated size in a chosen folder, account for access gaps, and separate that observation from any later deletion decision. This is not the PureMac product profile, the Breathing Room head-to-head comparison, or an alternatives list. It reuses `research.json` and `research.md`, including the homepage/repository conflict: blanket Trash-only/no-network claims are not repeated; action-specific repository descriptions and pinned source are used. It preserves unknown PureMac recurring-growth history and writer attribution as unknown.

Breathing Room is disclosed as “which we build”; preview, Python, signing, validation, hosted-context/authentication and example-data limits are stated. No app behavior, measurements, savings, screenshot capture details, blanket recovery, or unsupported negative feature claims are invented. No Alias skip is appropriate: PureMac Cleaner is the same canonical owner, not a second product. No separate alternatives skip is created; this job owns only the workflow page, and the existing alternatives handoff handles that distinct intent.

## Checks performed and outstanding

Read PLAN, EDITORIAL, capabilities, screenshots.json, AUTOMATION, applicable instructions search (no AGENTS.md found in the scoped repositories), PureMac research packet, and current website schema/examples. Loaded blog-write, blog-seo-check and browser-automation skills; applied the project editorial override. No browser work was necessary.

Actual local checks: Node v25 with the site's installed Astro-resolved YAML parser passed frontmatter parsing; confirmed review/unpublished state, current date/updated date, eight source records, title 46 characters, description 150 characters, one same-origin hub link, and all asset hashes against `provenance.json`. Article SHA-256 is recorded above. One initial checker attempt failed because `yaml` was not directly resolvable from the website root; it was rerun successfully using Astro's dependency resolution. Homebrew Python 3.14 XML parse failed due to its expat/system-library mismatch; the same SVG parse passed under existing `/usr/bin/python3`. Do not run shared `pnpm check`, build, or tests in this assigned job. Independent claim/SEO/rights review, rendered route/schema/draft-exclusion checks, shared site check/build/test, and responsive/theme screenshots remain required before publication. No independent score is awarded. Pricing is omitted; recheck release/version/availability within 30 days and before publication.

No shared nav/schema/tests/queue, other competitor record, purchases, accounts, messages, cleanup, commit, push, or deployment was performed. Queue state remains untouched.
