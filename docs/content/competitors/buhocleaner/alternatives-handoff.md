# BuhoCleaner alternatives draft handoff

Task: `draft-alternatives-buhocleaner` · Drafted/reviewed for scope **2026-10-22**. **Draft complete; publication not approved.**

## Output and distinct intent

- Record: `/Users/gabe/code/breathing-room/website/src/content/alternatives/buhocleaner.md`
- Intended public path: `/alternatives/buhocleaner/`; deliberately not exposed while `status: review`, `published: false`.
- Search/reference replacement guide: choose which BuhoCleaner job to replace. CleanMyMac is the suite candidate; DaisyDisk covers disk-space triage; FreeMacSoft AppCleaner covers known-app removal; Breathing Room is a bounded preview-stage investigation option. Not the BuhoCleaner-versus-Breathing Room comparison body or the Flash Clean workflow article.
- Canonical identity is BuhoCleaner, Dr.Buho's distinct product, not a verified alias. No skip record is appropriate.
- Approximately 1,255 body tokens split on whitespace (including link/HTML attribute text, **not** a precise rendered word count); six H2 sections, seventeen dated source entries, two captioned figures. Title 56 characters; description 155 characters. The rendered description is the conclusion-first introduction; body starts with the decision diagram rather than repeating the lead.

## Evidence reused, not recreated

Read PLAN.md, the October22 EDITORIAL.md update, capabilities.md, screenshots.json, the MailKite contract, website content contract/schema/renderer and relevant blog-write, blog-seo-check, blog-factcheck and browser-automation skills. No AGENTS.md was found in the two scoped repositories or checked ancestor locations. No subagents used.

Reused `docs/content/verification/batch-1.json` and verified the retained official snapshot hashes for BuhoCleaner, CleanMyMac, DaisyDisk and AppCleaner. Reviewed each product's existing research.md and research.json claim ledger. No redundant official-source crawl or directory refetch was performed. Source checks remain **2026-10-21**; October22 is the substantive draft date, not a fabricated new retrieval date.

| Article claims | Retained support |
| --- | --- |
| BuhoCleaner toolbox, monitoring, Flash Clean review and Xcode categories | `buhocleaner/research.json` C3, C5, C6 |
| BuhoCleaner channel-specific offers cannot become a universal price | C8, C9 and their limitations; amounts intentionally omitted |
| CleanMyMac Smart Care controls, Downloads duplicate scope, Xcode/monitoring | `cleanmymac/research.json` c-review, c-details, c-duplicates, c-xcode, c-monitoring |
| CleanMyMac requirements, edition/purchase boundaries and source disagreement | c-platform, c-editions, c-purchase, c-renewal, c-one-time; c-home-version versus c-version; store gate retained in research.md |
| DaisyDisk map, permanent Collector removal, current advertised compatibility and purchase limits | `daisydisk/research.json` D2, D3, D5, D6; older guide/current-offer conflict preserved |
| AppCleaner focused workflow and overlapping OS download branches | `appcleaner/research.json` ac-purpose, ac-workflow, ac-versions; ac-price supports bounded licence/price uncertainty |
| Breathing Room investigation, preview/runtime/signing, local/hosted/paid boundaries and approval modes | capabilities.md; BuhoCleaner BR1/BR2; linked source, release, offer and privacy policy |

The page makes an editorial selection from the retained graph, **not** a new AlternativeTo edge or endorsement. BuhoCleaner was discovered through the retained CleanMyMac and Mole graph edges. Shared graph membership establishes a research pool, not an independently verified direct relationship between each pair. Official job evidence justifies the shortlist.

No hands-on app experience, recovered-space measurement, performance benchmark, blanket safety assertion or unsupported negative feature cell is used. BuhoCleaner recurring-growth, process grouping and hosted/offline boundaries remain unknown; none is asserted absent. Exact prices are omitted rather than promoting conflicting/channel-specific numbers or blocked store teasers. No install recommendation relies on BuhoCleaner's unusually broad OS wording. CleanMyMac version disagreement is explicit without claiming a current binary version; DaisyDisk's older-guide OS discrepancy and AppCleaner's overlapping download ranges remain bounded.

## Route-B visuals and interaction pass

1. **Top visual:** original `replacement-jobs.svg`, 480 × 680. Four vertically stacked job cards, with product roles and a material limit on each. This is a documented-role decision aid, not competitor UI, testing or a benchmark. Its source mapping and original-authorship basis are in provenance.json. SVG has a title/description, no scripts and no embedded third-party images. Opaque high-contrast colors avoid relying on inherited theme colors; actual light/dark responsive approval is pending.
2. **Later visual:** unmodified first-party `space-preview-2026-10-21.png`, 2940 × 3468. Opened and read the actual source PNG in this job. Example-data/no-Mac-change banners retained; floating composer overlap acknowledged. Published copy matches the shared manifest SHA-256 byte for byte. Caption says earlier source browser preview, example data, not a native scan, measured activity, cleanup result or installer parity. Full-size image link is included for labels. Owner-requested first-party capture basis and third-party marks caveat retained.
3. Official illustrated BuhoCleaner Flash Clean, DaisyDisk deletion and AppCleaner pages are linked at source. No restricted competitor artwork copied, hotlinked or redrawn. No permission request sent. The old packet's screenshot-only `draftingAllowed:false` is preserved as history; October22 route B permits this internal draft, not publication approval.

Interaction pass: the highest-value choice is **which job needs replacing**. Implemented the top decision aid plus a non-executing closing checklist covering suite, map, uninstall, investigation and specific-feature verification. No JavaScript, filesystem access, invented scanner, cleanup buttons or forced code demo. Page is complete without executable interactions.

## Exact content/asset snapshot

All paths below are real files in the marketing website root `/Users/gabe/code/breathing-room/website`.

| File | SHA-256 |
| --- | --- |
| `src/content/alternatives/buhocleaner.md` | `e2afa5d897d06c81dfe96ee7dbc4c10aa02e18f272f1262e02fe88cf80b4e647` |
| `public/assets/alternatives/buhocleaner/replacement-jobs.svg` | `49706d0c6f516f4051228eef838aebbd3231d486af33f5ba86067bbd5ae9efb7` |
| `public/assets/alternatives/buhocleaner/space-preview-2026-10-21.png` | `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a` |
| `public/assets/alternatives/buhocleaner/provenance.json` | `05964ac0e85d13566fa8ef6b50408da08c795b6ded1bb19a9f34679215d87d7e` |

Read-only packet snapshots used: BuhoCleaner `15050cdc63026ad418a946b81fe31f7ec79f343526042ce225ba591b738aca85`; CleanMyMac `13720da6c11a13660e2652562703dd403a9117956f06ecb74d09342afffa3592`; DaisyDisk `d9fa3e5a422b0fbb2604886869c9bb11053153a35a28366eb1e9dfd2cfd90435`; AppCleaner `91abaab7c29691fca71fc1026eaf45e68b07bca5dd910ae8f16ed59d86e88499`. Each is the corresponding `docs/content/competitors/<id>/research.json` file in the app repository.

## Actual validation

- **PASS:** Python hashlib compared all four retained baseline official snapshots against batch-1 hashes. First-party PNG source/copy hash matches shared manifest.
- **PASS:** Node v25 using existing Astro-resolved YAML and Zod dependencies parsed the Markdown frontmatter and validated a schema equivalent to the current content schema. Confirmed `review`, `published:false`, current date/updated fields and actual `src/lib/publication.ts` `isPublished(data) === false`. This is a targeted source-level check, not an Astro collection build or a full draft-leak regression test.
- **PASS:** Same targeted Node check confirmed title/description lengths; two figures with real asset paths and alt text; top visual; six sequential H2s and no body H1; affiliation; no unresolved placeholder markers; seventeen external source URLs in the dated frontmatter; internal links limited to checked hubs.
- **PASS:** Python verified provenance JSON, PNG signature/dimensions/hash, accessible SVG title/description attributes and absence of script/embedded-image elements. `/usr/bin/xmllint --noout .../replacement-jobs.svg` exited 0.
- **Environment issue, recovered without installation/settings changes:** initial Python ElementTree XML parse failed because local pyexpat could not load `_XML_SetAllocTrackerActivationThreshold` from system libexpat. Used existing xmllint for real XML validation instead; did not claim the failed Python check passed.
- **Live links, October22 read-only WebFetch:** `/comparisons/` and `/tools/` returned substantive published hub text. `/alternatives/` and `/tools/cache-rebuild-checklist/` returned 404; both were removed from the draft. No links to unpublished competitor profiles/comparisons/workflow articles remain. Local route presence was not treated as live proof.
- **Retained-evidence fact-check:** checked substantive claims against the ledgers/excerpts above; this job did not refetch all mutable vendor pages or execute apps. All publication-specific freshness work remains independent review.
- **Not run by instruction:** shared `pnpm check`, `pnpm build`, `pnpm test`; no shared fixtures/nav/schema/tests/queue/database edits. No local preview server or browser session started, and no responsive page screenshots claimed. Browser skill loaded for applicable review requirements; no Chrome recovery was needed.

## Remaining review items — publication gates still pending

1. Independent claim-level factual/evidence review against this exact snapshot, including source conflicts and no unjustified scope expansion. Refresh volatile compatibility, availability and offer facts within 30 days and again before publication if stale.
2. Independent rendered review through an authorized isolated fixture: about 390/768/1440 px, light and dark themes. Inspect top diagram label fit, first-party preview readability/composer overlap, captions, full-size image link, heading hierarchy and keyboard navigation. SVG XML validity and source-PNG inspection are not rendered approval.
3. Site owner must run serialized check → build → test, inspect canonical `/alternatives/buhocleaner/`, author/dates, Article/Breadcrumb and social metadata, plus fail-closed routes/listings/RSS/sitemap behavior. Do not weaken publication filtering to preview the draft. A generic shared social card is not product evidence.
4. Independent itemized editorial score and zero blockers required before publication. **No passing score or independent approval awarded by this drafting worker.**

No purchases, accounts, messages, cleanup, credentials, computer-setting changes, commits, pushes or deployments. Unrelated working-tree content preserved. The required job receipt records completion of this internal draft only; it does not publish it or change queue state.
