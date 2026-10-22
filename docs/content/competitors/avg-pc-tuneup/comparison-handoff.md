# AVG PC TuneUp comparison draft handoff

Task: `draft-avg-pc-tuneup` · Draft review date: **2026-10-22** · **Draft complete; not publication-approved.**

## Exact owned outputs

Marketing root: `/Users/gabe/code/breathing-room/website`.

| File relative to marketing root | SHA-256 |
| --- | --- |
| `src/content/comparisons/avg-pc-tuneup.md` | `b6050f833a208ea9bab8aee8b7eb0f04e892ad7faf6314ce3457401788a6f6d0` |
| `public/assets/comparisons/avg-pc-tuneup/decision.svg` | `cf323e2cf158fd6aeb3d6e991971f3113d45a2586c2061efbe8813050fb5b58e` |
| `public/assets/comparisons/avg-pc-tuneup/space-preview-2026-10-21.png` | `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a` |

This handoff: `/Users/gabe/code/breathing-room-app/docs/content/competitors/avg-pc-tuneup/comparison-handoff.md`.
Receipt: `/Users/gabe/code/breathing-room-app/docs/content/.runtime/draft-avg-pc-tuneup.1792632816510097000.receipt.json`.

Intended eventual URL: `/comparisons/avg-pc-tuneup/`. The record is `status: review`, `published: false`; this is not a live article or public preview URL. Date and updated are October 22, not backdated to the research retrievals.

## Intent, identity and evidence reuse

Search/reference head-to-head intent: decide between Breathing Room and the Mac edition of AVG TuneUp. Not a neutral tool profile, alternatives roundup or migration tutorial. No other records were created. The packet confirms `avg-pc-tuneup` is the canonical owner; the PC/TuneUp/Premium names do not warrant a skip of this owner or another alias page. No PowerMyMac relationship is claimed.

Read PLAN, October22 EDITORIAL, capabilities, screenshots, research.json/.md, retained support excerpts, Mac marketing capture and baseline `verification/batch-2.json`. No applicable AGENTS.md found in either scoped tree or checked ancestors (including `/Users/gabe/code/breathing-room`). Loaded blog-write, blog-seo-check, blog-factcheck, browser-automation and the MailKite voice contract. User scope overrides generic builds, delegation, demo repositories and mandatory image-generation defaults.

Reused verified October 21 competitor/public-release/offer evidence rather than refetching it. Rechecked local README and RELEASE_NOTES on October 22. Verified the baseline directory/PC raw SHA-256 values against research.json. Baseline's no-card PC trial was not accepted as a universal fact: the richer packet preserves the contradictory FAQ. Existing research blockers remain unchanged as historical evidence; October22 expressly permits route-B drafting.

Claim review map:

| Article area | Retained research claim IDs and disposition |
| --- | --- |
| Identity and Windows boundary | `identity`, `windows-scope`; separate Mac edition, no Windows substitute claim |
| AVG strengths and matrix | `mac-cleanup`, `mac-duplicates`, `mac-photos`, `mac-apps-startup`, `mac-automatic-browser`, `mac-monitoring`, `mac-trash`; documented controls, not tested accuracy/safety |
| Access/licence/data | `mac-paid`, `personal-use`, `mac-local-hosted`; subscription, scan-only unactivated mode, commercial restriction and incomplete data-flow audit preserved |
| AVG compatibility/pricing | `mac-version-requirements`, `mac-os-conflict`, `mac-price-observed`, `trial-conflict`; omit numeric AVG buying recommendation, preserve conflicts, no old-OS or Mac-trial advice |
| Breathing Room | `br-preview`, `br-offer`, `br-workflow`, `br-approvals`; source/documentation evidence, not installed-binary certification |
| Unknown matrix cells | `unknown-specialties`; no unsupported negative feature cells or inferred parity |

All substantive feature rows have adjacent official/documented source links. Public numbers are confined to documented requirements, release identity and attributed Breathing Room price; no benchmarks, recovered-space totals or speed/safety claims. Main-branch source links are mutable and need version/delta review before publication. Affiliation is visible in the rendered description.

## Route-B visuals and interaction pass

1. `decision.svg`: original worker-authored editorial decision aid, 640×690. Three vertically stacked choices distinguish Windows, Mac duplicates/photos and Mac owner/cache investigation. Not a competitor screenshot, fake UI, measured test or ranking. Sources: packet `identity`, `windows-scope`, `mac-duplicates`, `mac-photos`, `br-workflow`, `br-preview`. No third-party image bytes or logos used. Caption identifies documentary basis and source date. Explicit SVG title/description, HTML alt and caption supplied. Opaque light background is intentional for contrast in either site theme; actual responsive/themed rendering is pending.
2. `space-preview-2026-10-21.png`: byte-identical copy of first-party `docs/content/assets/breathing-room/space-preview-2026-10-21.png`, 2940×3468. Opened and read the original PNG in this job. Example-data warnings remain visible; no crop/redaction/number alteration. Library capture time `2026-10-21T19:06:45.416416+00:00`, source commit `54828ac3170b45861aee70861dd0b9c658ed7e51`. Captured by screenshot-library job, browser preview, not native measurement or distributed-release proof. Original and copy hash match. Reuse basis: first-party owner-requested capture per screenshots.json; no blanket third-party trademark licence inferred. Existing library privacy review found built-in example names/paths only. Caption discloses composer overlap and UI/measurement limits. Independent contextual rights/privacy/currentness review remains pending.

AVG illustration remains **link-only** at `https://www.avg.com/en-us/avg-tuneup-for-mac`; original rights-unclear image was not copied, downloaded or hotlinked. Route B supersedes the old screenshot-only drafting blocker, not the rights restriction. Official Mac guide is linked beside claims.

Interaction pass completed as a static decision aid: the highest-value choice is platform → actual maintenance job, implemented in the top SVG and explained in text. No scripts, deletion controls, settings changes or external submissions. A calculator or forced code sample would not improve this head-to-head decision. Page has a second substantive first-party figure later.

## Actual validation and outcomes

- `/usr/bin/python3` targeted structural/hash checks: **passed** baseline directory and PC source hashes, screenshot hash/copy equality, draft fields/date, two figures, no body H1, no public placeholder markers, all local image references resolve, SVG XML parsing.
- Initial `python3` attempt failed at SVG parsing due to local Python 3.14 `pyexpat`/system libexpat symbol mismatch. No system fix attempted. The same checks passed with existing `/usr/bin/python3`; screenshot copying had completed before the initial parse failure, and its bytes were subsequently verified.
- `/Users/gabe/.nvm/versions/node/v25.0.0/bin/node --experimental-strip-types --input-type=module`: **passed** YAML parsing using installed Astro dependency; validation against the exact schema expression read from current `src/content.config.ts`; actual `isPublished` excludes this record; ten dated source entries; title 48 characters, description 154 characters.
- `shasum -a 256` confirmed the final article and both assets listed above.
- Read-only live link check: `https://breathing-room.chatic.ai/comparisons/` returned substantive hub text. `https://breathing-room.chatic.ai/tools/cache-rebuild-checklist/` returned **404**; omitted from the article despite local utility source existing. Only internal body link is the verified live hub. No links to proposed/hidden competitor records or workflow drafts.
- SEO/source pass: conclusion-first description; distinct title/slug; sequential H2s; disclosure; source-adjacent matrix; dated source ledger; explicit unknowns and non-fit conditions. Repeated official URLs are intentional for cell-level evidence, not removed to satisfy generic deduplication lint. No invented FAQ, review, Offer or rating markup added. Shared layout adds a branded title suffix; assess final truncation in rendered review.
- **Not run:** shared `pnpm check/build/test`, site fixture build, native tests, browser article rendering, responsive/theme/keyboard QA or independent review. Shared builds and subagents were expressly forbidden. No Chrome session was needed for reused evidence. Source-level schema/publication checks do not establish final built HTML correctness or actual draft leakage across every output.

## Remaining review gates

1. Independently review this exact article/asset snapshot, claim-adjacent sources and route-B context. Do not inherit the research worker's approval or assign a publication score from file existence. No numeric quality score is awarded here; technical/rendered categories have unperformed checks.
2. Through the responsible site/review job, create an isolated local draft fixture without weakening real publication filtering. Run serialized site checks/build/tests and verify canonical `/comparisons/avg-pc-tuneup/`, single H1, author/date, OG/Twitter, Article/Breadcrumb schema and exclusion from public routes/listings/feed/sitemap while unpublished.
3. Open and inspect actual rendered output at approximately 390/768/1440 px in both themes. Check SVG labels, full screenshot legibility, table overflow, captions, disclosure and keyboard access. The full-height screenshot may need a contextual crop that retains the example-data warning; no crop is claimed here.
4. Refresh volatile facts within 30 days and before release when stale. Resolve OS/trial/billing questions only if adding affected advice; current draft explicitly withholds it. AVG installer signing, patch version, complete licence/privacy details and runtime behavior remain unverified. Breathing Room release/source parity, hosted quota/enforcement and native/Intel/clean-machine behavior remain unverified.
5. Final independent score must meet the programme threshold with zero blockers before changing publication fields. Draft completion is not publication approval, deployment or a claim the intended public article currently exists.

No purchases, accounts, messages, credentials, cleanup, app launches, commits, pushes, deployments, shared navigation/schema/tests, queue/database edits or other workers' files were involved.
