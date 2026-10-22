# Kudu tool-profile handoff

Task: `draft-tool-kudu-cleaner` · Drafted/reviewed at source level: **2026-10-22 UTC**.

## Outcome and owned outputs

One complete neutral search/reference profile, approximately 916 body words, at the intended public path **`/tools/kudu-cleaner/`**. It is **not published**: `status: review`, `published: false`, `date` and `updated` both `2026-10-22`. This completes the assigned drafting stage, not the publication gate.

Website root: `/Users/gabe/code/breathing-room/website`.

| Exact output file (relative to website root) | SHA-256 |
| --- | --- |
| `src/content/tool-profiles/kudu-cleaner.md` | `c2e18fc77c9c1f4823b27e4987db96088b9938c177a6a61aae7b168c765ea72e` |
| `public/assets/tools/kudu-cleaner/desktop-cloud.svg` | `07bad616a58fe997e9d3fcd5ef21f4a1b3518b76431b67f8e839a6c1ac384ecb` |
| `public/assets/tools/kudu-cleaner/review-schedule.svg` | `0d1ac10566a51397b797a785b51c599b4e84f7c328dd04eced310a75ae988d9e` |

This handoff is `/Users/gabe/code/breathing-room-app/docs/content/competitors/kudu-cleaner/tool-handoff.md`. Its hash is recorded in the job receipt after writing; it cannot include a stable hash of itself.

## Instructions and retained evidence

Read `PLAN.md`, the controlling October22 update in `EDITORIAL.md`, `capabilities.md`, `screenshots.json`, `research.json`, `research.md`, `research-notes.json`, and the Kudu entry in `docs/content/verification/batch-1.json`. Checked ancestor instruction files and scoped docs/src/public AGENTS searches: none found. Loaded `blog-write`, `blog-seo-check`, `blog-factcheck`, `browser-automation` and the MailKite contract; applied the Breathing Room neutral-profile adaptation, not generic statistics/FAQ/demo-repository quotas.

Reused the October 21 evidence rather than refetching Kudu's entire source set. The homepage, AlternativeTo snapshot and retained MIT licence hashes match the packet. Source `checked` dates remain **October 21**, not the October 22 drafting date. No new native test, install, account, checkout, cleanup, recovery experiment or network audit is implied.

### Claim mapping and conflicts

| Profile section | Retained claim/source basis and boundary |
| --- | --- |
| Identity and job | K01; baseline homepage, reciprocal official repository identity. Kudu / kudu-cleaner are one canonical product owned by `kudu-cleaner`, not an alias of another record. |
| Platforms/download | K02; official Download page: 3.10.0 offered October 21, macOS 12+, Apple silicon/Intel; baseline Windows 10/11 and Linux. Offered packages are not independently tested binaries. |
| Desktop licence and Cloud | K03/K04/K09; retained MIT notice, Pricing and Safety. Desktop $0/no account differs from optional Cloud Basic $5 and Pro $9 USD/device/month base rates; volume thresholds/device-count conditions preserved. Taxes/refunds/discount totals unknown. Live monitoring is free; new recordings/AI require Pro. |
| Cleaner and schedules | K05/K07/K10; System Cleaner, Scheduler, Safety. Item review/exclusions/receipts differ from supported scheduled automatic application. Receipts are not file backups; Recovery Centre does not promise arbitrary deleted-file restoration. Ordinary cache and opt-in Privacy Traces differ. App-running condition retained. |
| Storage/process scope | K06/K08/K11; Storage History, Performance Monitor, baseline homepage. Local snapshots/growth alerts are free, with up-to-90-day/250 MB conditions. Exact Mac sensors, helper aggregation and per-rule developer-cache coverage remain unverified, not absent. |

Source tensions are explicitly bounded: “free forever” is not a free-Cloud promise; broad approval language does not override automatic scheduling; “local” is qualified by Safety's network/Cloud disclosures. Main-only custom-folder documentation is excluded from asserted release capabilities because release inclusion is unresolved. No unsupported negative feature cells, rankings, performance/savings claims or Windows-to-Mac feature transfer.

The page discloses that we build Breathing Room, not Kudu, and are not affiliated with Advent Development. It makes no Breathing Room capability or subscription recommendation, so it does not import preview screenshots or expand into a head-to-head sales page.

## Visual provenance and interaction pass

**Route B, neutral-profile decision-aid exception:** two original editorial diagrams, not copied/redrawn competitor UI. No screenshot permission is inferred or needed for these original compositions. Both were authored for this draft by the scheduled OpenCode worker on October 22, 2026. No competitor logos, screenshots, third-party image assets, real measurements or user data are embedded. These are documented-scope illustrations, not captures of either app and not benchmarks. The official System Cleaner guide is attributed and linked for the vendor's own illustration; that website image remains link-only.

| Asset | Provenance and supported claims | Published treatment |
| --- | --- | --- |
| `desktop-cloud.svg` | Original 480×650 SVG; K03/K04/K06/K07/K09; Pricing, Storage History, Scheduler, Safety excerpts in research-notes. | Top figure immediately after description-as-lead. Alt and caption distinguish free desktop from optional Cloud, identify documentation basis, and state not UI/test. |
| `review-schedule.svg` | Original 480×650 SVG; K05/K07/K10; System Cleaner, Scheduler and Safety excerpts. | Later figure distinguishes interactive review from scheduled automatic application and preserves receipts-not-backups boundary. Alt/caption provided. |

Reuse basis: newly authored editorial artwork for the requested site, with no copied vendor visual material. This is not a claim that vendor trademarks or site images have an MIT licence. Creation time is October 22; source-check date displayed in diagrams is October 21. No edits to vendor imagery, privacy redactions or purported capture metadata exist.

Interaction pass completed: the useful decision is understanding review versus automatic application, not simulating a scanner. The second diagram plus a non-executing owner/exclusions/backup/rebuild-cost checklist supplies that aid. No script, filesystem access, pretend scan, signup or cleanup button was introduced.

## Actual validation and outcomes

All commands below were scoped read-only checks, with no generated site files or shared build.

- **PASS, final snapshot:** Node v25 with PATH prefix `/Users/gabe/.nvm/versions/node/v25.0.0/bin`. Inline validator parsed YAML using the installed Astro dependency, evaluated the **actual current schema declaration** from `src/content.config.ts`, and parsed the record successfully. Required fields, source dates, review/unpublished state and current dates passed.
- **PASS:** imported the actual `src/lib/publication.ts` function; `isPublished(record)` returned **false**. This is a unit-level gate check, not an end-to-end feed/sitemap test.
- **PASS:** installed Astro Satteri Markdown processor rendered the final body **in memory**. Verified two figures, two images, two captions, six H2s, no body H1 (layout supplies it), first element is a figure, nonempty alt text, existing owned image files, and no TODO/TBD/link/image placeholders. This is not a full Astro layout build.
- **PASS:** 45-character title, 156-character description; title distinct from other current tool-profile titles. All 10 frontmatter source URLs match retained official evidence and retain `checked: 2026-10-21`. Every rendered external body link maps to the packet or the exact discovery URL.
- **PASS:** sole internal body link is `/tools/`. Read-only `curl -I --max-time 20 https://breathing-room.chatic.ai/tools/` returned HTTP 200; WebFetch GET confirmed the real tools hub with headroom and units utilities. No unpublished comparison/alternatives/profile peer link was added.
- **PASS:** retained homepage, directory and MIT licence SHA-256 comparisons against research.json. Final output hashes appear above.
- **PASS:** Chrome connected normally; metadata-only tab listing, fresh owned `about:blank` tab **436**, then only the two owned local SVGs. Checked real SVG DOM text bounding boxes: **13 text elements per diagram, none extending outside the 480-unit horizontal bounds**. Set display width 100%, max-width 480px and automatic height only in the browser to inspect proportional embedding. Opened/read the actual screenshots at **390×850**, desktop/Cloud diagram in light emulation and review/schedule diagram in dark emulation: labels readable, no clipping. Closed only tab 436. No existing tabs were inspected or navigated. No Chrome recovery/profile switch was needed. These tool-returned screenshots were not saved as file artifacts and are not a substitute for full-page visual approval.
- **PASS:** `xmllint --noout` on both exact SVG files exited **0**.
- **Initial validation error, corrected:** first inline Node check incorrectly expected seven H2s; actual content has six. Corrected the assertion, not the headings; final full validator passed, including the later source-adjacency text edit.
- **Environment failure, not repaired:** supplementary Python ElementTree parsing exited 1 because Homebrew Python's `pyexpat` could not load `_XML_SetAllocTrackerActivationThreshold` from system libexpat. No packages/settings were changed. XML validation was instead completed successfully with `xmllint` and actual Chrome SVG rendering.

## Remaining review gates

1. Independent factual and editorial review against the exact hashes above, including price freshness and mutable official documentation. No independent approval or 85+ score is claimed.
2. Full isolated page rendering through the responsible site reviewer; mobile/tablet/desktop, light/dark, captions, keyboard/link behavior and layout context still need review. The limited standalone diagram checks above do not satisfy that gate.
3. Serialized `pnpm check`, `pnpm build`, `pnpm test` and built HTML canonical/H1/author/date/social/schema checks; confirm exclusion from routes, hubs, sitemap and RSS end-to-end. **Not run because this job explicitly prohibits shared site builds.** Do not weaken the publication filter to preview this draft.
4. Refresh volatile prices/download offer within 30 days of October 21 and again before publication if stale; retain unverified binary/runtime/signing, sensor/helper, rule-level cache and checkout limits unless new evidence resolves them.

No textual or asset placeholders remain and no additional asset is required to complete this draft. The two diagrams still require independent contextual visual review. No numeric quality score is assigned by the drafter.

## Intent and ownership boundaries

This profile earns its distinct identity/platform/licence/documented-job intent. It is not a calculator, replacement shortlist, comparison or workflow tutorial. No alternatives list is included, so no peer relationship is manufactured. This does not complete, skip or change any separately assigned alternatives job. No `tool-skip.md` was written because the retained canonical identity explicitly says **do not skip**; verified aliases are handled in the one Kudu profile.

Only this handoff, the one tool record, its two owned SVG assets and the required job receipt were written. Existing research, shared navigation/schema/tests, other queue jobs and unrelated work were preserved. No queue/database mutation, subagents, credentials, messages, purchases/accounts, cleanup, commit, push or deployment.
