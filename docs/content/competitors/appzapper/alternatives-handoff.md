# AppZapper alternatives draft handoff

Task: `draft-alternatives-appzapper` · Draft assembled/reviewed at source level: **2026-10-22**.

## Outcome and ownership

One complete search/reference alternatives record was created for the intended public path `/alternatives/appzapper/`. It remains `status: review`, `published: false`; that path is not claimed live. This is drafting completion, not publication approval. No shared build, navigation, schema, test, queue/database, research packet or other job record was changed. No subagents, accounts, messages, purchases, cleanup, credentials, commits, pushes or deployments.

Read PLAN.md, the October22 EDITORIAL.md update, capabilities.md, screenshots.json, the AppZapper JSON/Markdown research, relevant peer packets, verification summaries, site content contract/schema/route, and the MailKite writing contract. Loaded blog-write, blog-seo-check, blog-factcheck and browser-automation. No AGENTS.md was found in either scoped tree or the checked ancestors. Browser interaction was not used; no Chrome recovery or profile changes were needed.

The initial broad parent-directory AGENTS search timed out; scoped glob searches and explicit ancestor checks completed instead. No content was changed before the applicable instruction checks.

## Exact outputs and SHA-256

Marketing root: `/Users/gabe/code/breathing-room/website`.

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `/Users/gabe/code/breathing-room/website/src/content/alternatives/appzapper.md` | 13386 | `fcfb5541175619459dd4b4e5023f8677a8e6e472899958ce625ab724055d68fb` |
| `/Users/gabe/code/breathing-room/website/public/assets/alternatives/appzapper/replacement-decisions.svg` | 2129 | `db0707ac9e4b9c3be719c9287856a99c3bc36c29a6ba9e26ce56068b909d0af3` |
| `/Users/gabe/code/breathing-room/website/public/assets/alternatives/appzapper/space-preview-2026-10-21.png` | 587216 | `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a` |

This handoff and the required receipt are additional owned files; their hashes are recorded in the receipt after writing. No separate AppZapper 3000 page or alias skip file is appropriate: `appzapper` is already the canonical owner.

## Distinct intent and claim review

The reader is replacing an app-removal workflow, not choosing Breathing Room versus AppZapper. Four documented uninstallers are explained by the reason to switch: focused removal/older OS branches, broader app management, Apple-silicon/free offer with recovery conditions, and orphan search with maintenance/licence qualifications. Breathing Room is a later adjacent investigation option, explicitly affiliated, not counted as a full uninstaller replacement. No direct pairwise AlternativeTo relationships are asserted. No head-to-head body was copied.

Source checks retain their actual **2026-10-21** dates; October22 is the substantive drafting date, not a new retrieval date. Baseline verification and packets were reused without refetching product pages. Claim-level support was read, not inferred merely from reachability:

| Draft claims | Retained evidence |
| --- | --- |
| AppZapper identity, 3000 lineage, 1.0.1, macOS 15.6+, three zaps, associated files, machine-count one-time offers and USD basis | `research.json` AZ01–AZ04; S1–S3; original official snapshot and buy-page excerpts |
| AppCleaner workflow and all four overlapping download branches | `../appcleaner/research.json` ac-purpose, ac-workflow, ac-versions; ac-price bounds official price/licence uncertainty |
| Nektony bundle-ID/path review, app management, published OS range, two-day trial/Free limits, major-version licence | `../app-cleaner/research.json` C02–C05, C07; no price/currency inference used |
| Pangalin free offer, M1/macOS minimum, Intel exclusion, conditional Undo/permanent exceptions, permissions and shared-toolchain exclusion | `../pangalin-uninstaller/research.json` C02–C03, C07, C10, C14; Startup wording conflict retained under C13 |
| Pearcleaner uninstall/orphan search, OS table, maintenance pause, licence, permissions and Trash-triggered automation | `../pearcleaner/research.json` P01–P03, P05–P06, P08–P09 |
| Breathing Room source/binary distinction, preview/Python/signing/runtime limits, free core/renewing AI Care, hosted data and download boundaries | `../../capabilities.md`; AppZapper BR01–BR03; public release/homepage/privacy citations |

Unknown AppZapper recovery, signing, architecture, network behavior and licence details were not converted to feature absences. AppCleaner price/licence remains unverified despite the directory's free label. Pearcleaner's pause is neither active-maintenance assurance nor proof of abandonment. Nektony's future-looking OS range is attributed, not certified. Pangalin Startup confirmation conflict is explicitly bounded; exact instructions are omitted. No app tests, benchmarks, savings, image rights or screenshot UI were invented.

## Route B visual provenance

The older packet's `draftingAllowed:false` was solely an outdated competitor-screenshot gate. The October22 policy permits this internal draft using route B. Original packets and their blockers remain unchanged. No competitor image was downloaded, copied, embedded or hotlinked. AppZapper's official How it works section and peer official pages/README provide attributed links to vendor images/documentation.

1. **replacement-decisions.svg:** newly authored original editorial decision aid, 480 × 780, not app UI. It summarizes the four peer claims mapped above. Alt text describes the choices; caption states documentary selection, not testing/ranking. Fixed light background and dark text avoid theme-dependent contrast. Vertical layout limits wide flow shrinkage. Creation date October22; original and delivered bytes identical, hash above. Contains no user data, third-party logos or copied UI; independent visual/mobile inspection remains pending. No new legal claim about vendor screenshot rights is made.
2. **space-preview-2026-10-21.png:** unchanged copy of `docs/content/assets/breathing-room/space-preview-2026-10-21.png`; original and copied SHA-256 match the screenshot inventory and table above. 2940 × 3468. Capture `2026-10-21T19:06:45.416416+00:00`, source commit `54828ac3170b45861aee70861dd0b9c658ed7e51`, source `http://127.0.0.1:1431/`. First-party app-owner-requested example capture; privacy review inherited from inventory, third-party marks remain their owners'. Actual PNG opened with image-capable read during this job: example-data notices are visible; floating composer overlaps the chart. No crop/edits. Required example-data/non-native/no-measurement caption preserved. This represents the captured source, not a newly tested binary or a new capture.

Interaction pass: implemented the static selection diagram, differentiated decision table and final six-question checklist. No JavaScript, upload, scan, cleanup controls or arbitrary demo repository is needed. Completion of a checklist does not authorize deletion.

## Actual validation

- **PASS:** JSON parsing of all five packets; nine retained non-Markdown source snapshot hashes matched their packet values (AppZapper 3, AppCleaner 2, Nektony 1, Pangalin 1, Pearcleaner 2). This targeted check is not a claim that every inherited path/hash was revalidated.
- **PASS:** Node v25 command with existing Astro-resolved YAML/Zod parsed frontmatter and validated the same fields/refinement as `src/content.config.ts`: 12 source records, valid URLs/dates, nonempty metadata, ordered dates. Explicitly asserted review/unpublished/current drafting date.
- **PASS:** title 48 characters; description 158 characters; roughly 1,561 whitespace-separated body words including markup. H2 sections only; shared layout supplies H1. Description is not repeated as the opening paragraph. No placeholder/TODO/internal-link markers. Two images have meaningful alt text and existing local files. No source-only draft cross-links.
- **PASS:** existing `@astrojs/markdown-satteri` processor rendered the body in memory, returning code/metadata. This is Markdown parse/render validation, **not** a shared site build, route integration test or browser visual inspection.
- **PASS:** SVGO parsed/optimized the SVG in memory; original file was not rewritten. The preceding Python XML attempt failed because the installed Python expat extension could not resolve `_XML_SetAllocTrackerActivationThreshold`; this was an environment parser failure, not a successful XML check. Existing Node/SVGO supplied the successful fallback; no packages installed/settings changed.
- **PASS:** source PNG SHA-256 asserted before copying; output hashes/bytes computed from actual files.
- **PASS with corrected links:** read-only live checks returned substantive pages for `https://breathing-room.chatic.ai/comparisons/` and `/tools/`. `/alternatives/` and `/tools/cache-rebuild-checklist/` returned 404; those proposed links were removed. Only the two confirmed live internal hubs remain.
- **NOT RUN by task constraint:** shared `pnpm check`, `pnpm build`, `pnpm test`. No native app testing or cleanup execution. No browser-owned tab was opened and no responsive/theme or keyboard check is claimed.

## Remaining independent review gates

1. Independent claim/delta review against these exact hashes, including stale offers/availability before publication (within 30 days of source checks), future-looking Nektony OS wording and recovery limitations. If a material fact changes, revise and rehash before approval.
2. Authorized serialized check/build/test and draft-exclusion/route/schema review. Confirm the unpublished record stays out of routes, hubs, RSS and sitemap. Do not expose a draft by flipping publication fields.
3. Isolated rendered review at approximately 390, 768 and 1440 pixels, light/dark themes: diagram text, table overflow, full-height PNG readability, composer overlap, captions and keyboard links. If the large PNG is not useful at narrow widths, make a separately reviewed contextual crop preserving both example-data notices; do not fabricate UI.
4. Independent rights/privacy/context review of both visuals. Route B removes the need to copy uncleared competitor screenshots, not the visual-review requirement.
5. Itemized independent content/SEO/evidence/technical/citation scorecard, total at least 85/100 and no blocking failures. No self-awarded publication score or release-ready claim is made here. Canonical/OG/Twitter/Article/Breadcrumb output is pending rendered integration review.

The complete textual draft and two real assets are delivered. All publication gates above remain pending; the drafting receipt must not be treated as permission to publish or deploy.
