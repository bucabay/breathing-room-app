# SpaceBroom tool-profile handoff

Task: `draft-tool-spacebroom` · Drafted/reviewed at source level: **2026-10-22**.
Outcome: **complete internal textual draft with two original route-B diagrams**. Not publication approval. Record remains `status: review`, `published: false`.

## Outputs and exact snapshot

| File (absolute) | SHA-256 |
| --- | --- |
| `/Users/gabe/code/breathing-room/website/src/content/tool-profiles/spacebroom.md` | `bd04398b69aa35a98117326e78b21004a42bf6bdb872a39544535b3d84af2010` |
| `/Users/gabe/code/breathing-room/website/public/assets/tools/spacebroom/documented-workflow.svg` | `4ddab6ed4299be5023497a344298a88e7a8165e3abd2b76b6766e4d21ff5cca5` |
| `/Users/gabe/code/breathing-room/website/public/assets/tools/spacebroom/recovery-boundaries.svg` | `c88312e2ded4fb30b7140d64cf529b6dbec6967d996e55de0de88e20cccd8d8b` |

Canonical future public path: `/tools/spacebroom/` on `https://breathing-room.chatic.ai`. It is intentionally not a live published page. Existing `src/lib/content.ts` maps `tools` to `toolProfiles` and derives this path; the template derives canonical/social/schema metadata. No unsupported frontmatter fields or shared code changes were added. The title is 49 characters; description is 158. Body is approximately 884 whitespace-delimited words including figure captions and Markdown links, not a padding target.

## Intent, identity and evidence reuse

- Search/reference track, surfaces organic search and source-grounded answers: understand SpaceBroom's official identity, documented job, direct-edition access and licence conditions. Not a comparison, alternatives list, workflow tutorial, calculator, recommendation ranking or claim we built SpaceBroom.
- Read `PLAN.md`, October22 `EDITORIAL.md`, `capabilities.md`, `screenshots.json`, both existing research files, retained official baseline/excerpts, website publishing/schema/route contracts and the MailKite writing adaptation. Loaded `blog-write`, `blog-seo-check`, `blog-factcheck` and `browser-automation`. No applicable AGENTS.md was found in checked ancestors or scoped docs/src/public trees.
- Reused the existing batch-2-derived packet rather than refetching competitor sources. Source retrieval remains **October 21**, not relabeled as October 22. Four unique retained snapshot files with source-ledger hashes match their SHA-256 values, including official/discovery baselines, homepage HTML and additional excerpts.
- Existing identity evidence establishes SpaceBroom / DIGITALPASSION Ltd. and `canonicalOwnerId: spacebroom`, with no verified alias. No skip file or duplicate owner was justified.
- The old packet's screenshot-only drafting block is historical under the October22 policy. Packet files and their unknowns were preserved unchanged. Official identity and substantive claims support this draft; copying its UI remains unauthorized.
- No alternatives section was manufactured. Several-peer verification belongs to a separate alternatives intent, not this neutral tool-profile task. No draft comparison, blog or alternatives routes were linked.

## Claim-level drafting review

The retained homepage text was read in full during this job; the additional legal/policy excerpts and claim ledger were checked against the actual prose. These checks establish documentary support, not runtime behavior.

| Draft subject | Packet claims / sources | Treatment |
| --- | --- | --- |
| Identity and seller | SB-01/02; D1, S1, S3, S6 | Official identity linked; directory only discovery. |
| macOS and permission-limited access | SB-03/12; S1 | macOS 14+, vendor FAQ scope; no architecture or complete-coverage claim. |
| Folder exploration / cleanup categories | SB-08/09/10; S1 | Documented, not tested; duplicate exclusions not generalized to all cleanup. |
| Free scan, seven-day trial, direct EUR offer | SB-04/07; S1 | Dated offer, one Mac, VAT and post-trial paid cleanup retained. No trial or checkout attempted. |
| Renewal and one-time entitlement | SB-05/06; S3/S4 | Annual minimum/notice/pro-rata conditions, monthly boundary, version-1 entitlement and German precedence retained. Not all-version lifetime upgrades. |
| Trash / permanent operations / restore | SB-11; S1/S3/S4 | Broad homepage wording explicitly bounded by exceptions and destination/name conditions. No universal recovery promise. |
| Local/network and Store edition | SB-13/14; S5 | Attributed policy, not audit; Store availability/price unverified, no edition mixing. |
| Download/signing/version | SB-15/16; S1/S7 | Existing endpoint response not installation proof; signing remains attributed. Exact version, architecture/runtime unknown. |

Unresolved material claims were omitted or explicitly bounded: official source repository/licence classification, process/helper grouping, recurring-growth monitoring, exact binary version/architectures/runtime, App Store availability/price and tested safety/privacy/notarization. None is converted to a negative feature cell. No benchmarks, fabricated experience or performance/savings claims. The price and availability review must be refreshed within 30 days of the original checks and again before publication if overdue.

## Visual provenance and interaction pass

**Route B, neutral-profile decision-aid variant** from October22 EDITORIAL §11. Both assets were authored as original SVGs in this task on October 22, 2026; 600 × 700 pixels/viewBox each. They contain original explanatory text, rectangles and arrows, not copied product artwork, logos, generated app UI, screenshots or scan data. No third-party image licence is inferred. Original and embedded asset bytes are identical (no transformations); hashes above identify both. No private data or user paths appear. Actual visual rendering/context approval is pending.

1. `documented-workflow.svg`: a vertical diagram of size-based navigation, deeper exploration and confirmed Space Lens Trash action. Supports SB-08; its “size alone” warning is editorial judgment, not an app safeguard. Source: `https://spacebroom.app/en/#space-lens`, S1 retained October 21. Alt and caption explicitly identify documented behavior, not UI or our test. The caption links the official section containing DIGITALPASSION's illustration without downloading, copying or hotlinking that image.
2. `recovery-boundaries.svg`: a later decision aid distinguishing Trash where possible, permanent exceptions and conditional history restoration. Supports SB-11 with S1/S3/S4, checked October 21. Caption links the official safety section and references terms §9. Alt/caption and in-image text reject a recovery guarantee or tested-safeguard interpretation.

Interaction pass completed at source level: the useful decision is whether the exact cleanup action is reversible, not an invented scan or deletion button. The second static visual and adjacent prose provide this aid without JavaScript, filesystem access, uploads or persisted inputs. No new calculator/island or executable demonstration is warranted. No Breathing Room screenshot is inserted into this neutral competitor profile; the neutral-profile decision-aid allowance avoids an irrelevant promotional comparison. Existing first-party screenshot records were read, not relabeled as native evidence or copied.

## Actual scoped validation

- Node v25.0.0 with the user-specified PATH: parsed YAML through Astro's existing YAML dependency and validated against the **actual existing Zod schema** extracted from `src/content.config.ts`. PASS: `review`, `false`, October22 date and source records accepted.
- Imported actual `src/lib/publication.ts`; `isPublished` rejects the record for both October22, 2026 and October22, 2027. PASS. This is a function-level draft-gate check, not a built sitemap/feed audit.
- Structural assertions: first body element is a figure; exactly two figures, two captions and two existing image files with descriptive alt text; six H2 sections, no body H1, no unresolved placeholders; six source records preserve October21 checks. PASS. Initial test erroneously expected seven H2s, failed, and passed after correcting the assertion to the actual six; no filler heading was added.
- Final description-length check: PASS, 158 characters. Original schema run reported 162; the description was shortened before final hashing. Title: 49 characters. No keyword/statistics/power-word/FAQ quota forced onto a neutral profile.
- `/usr/bin/python3` XML validation: both SVGs parse, expose role/title/description, declare 600 × 700 viewBoxes, have text anchor coordinates inside bounds, and contain no scripts, event attributes or embedded copied images. PASS. This does **not** prove text widths, responsive legibility or visual approval. Initial Homebrew `python3` XML parser failed on a missing `_XML_SetAllocTrackerActivationThreshold` symbol; rerun with the already installed system Python passed, without installs/settings changes.
- SHA-256 checks: PASS for four retained source snapshots and the three output files listed above. Canonical identity / no-verified-alias assertions: PASS.
- Read-only live WebFetch: `https://breathing-room.chatic.ai/tools/` returned the functional tools hub. Proposed `https://breathing-room.chatic.ai/tools/cache-rebuild-checklist/` returned **404**, so that link was omitted. The only internal body link is `/tools/`; no broken public placeholder or hidden draft links remain.
- Source-adjacent citations, lead/body progression, affiliation, edition boundaries and unsupported-negative/benchmark scan reviewed by the drafter. No independent score awarded. Generic blog statistics, H2 and internal-link quotas are inapplicable under the local editorial contract.

No shared check/build/test commands, no browser actions, no competitor source refresh, and no app execution were performed. `pnpm check` includes generated Wrangler types and is not represented as a read-only scoped check. No queue/database/shared nav/schema/test changes, agents, accounts, credentials, messages, purchases, cleanup, commits, pushes or deployments.

## Remaining review gates (publication blocked)

1. Independent factual review of the exact Markdown and assets above; confirm legal/update boundaries against retained source evidence and refresh volatile facts when needed. Rights for copied competitor UI remain unresolved, but this draft does not use it.
2. Independently inspect/render both SVGs and the whole page at approximately 390/768/1440 pixels in light and dark themes. Check text widths, contrast, reading order, captions and image sizing. No screenshots or responsive success are claimed here.
3. Responsible serialized site-review job must run the required site check/build/tests, inspect built canonical/social metadata, author/dates, Article/Breadcrumb schema, links and draft exclusions in routes/listings/RSS/sitemap. Those shared commands were explicitly prohibited for this drafting job.
4. Review current snapshot against all five editorial categories, require ≥85/100 and zero blockers; drafter has not assigned automatic points or waived independent approval. Keep review/unpublished until separate authorization.

The drafting task is complete; publication is not. The exact receipt is `docs/content/.runtime/draft-tool-spacebroom.1792642456228840000.receipt.json` in the app repository.
