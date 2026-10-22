# Noah workflow blog handoff

Task: `draft-blog-noah` · Draft written October 22, 2026 · **Draft complete; publication approval pending.**

## Owned output files and hashes

| Real output file | SHA-256 |
| --- | --- |
| `/Users/gabe/code/breathing-room/website/src/content/blog/noah-mac-workflow.md` | `325fb82eee00790413399bf5bbebf09d0635f29c5f7df02d171c44029d75ad14` |
| `/Users/gabe/code/breathing-room/website/public/assets/blog/noah/slow-mac-diagnostic-path.svg` | `c8c66337e860cd4add832f94aa7a8a28c951412dae55229b9bdf0b633c39800e` |
| `/Users/gabe/code/breathing-room/website/public/assets/blog/noah/space-preview-2026-10-21.png` | `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a` |

Intended route: `/blog/noah-mac-workflow/`. The article is `status: review`, `published: false`, dated October 22, 2026, by Breathing Room team. It teaches one workflow: separate low-space observation from process or broader software symptoms before selecting a diagnostic or approving a change. It is not the Noah profile, comparison matrix, or alternatives guide expanded into prose.

## Evidence and intent decisions

Read `PLAN.md`, October22 `EDITORIAL.md`, `capabilities.md`, `screenshots.json`, Noah `research.json`/`.md`, existing tool/comparison/alternatives handoffs, and the Noah entry in `verification/batch-2.json`. Loaded `blog-write`, `blog-seo-check`, `blog-factcheck`, and `browser-automation`; applied the Breathing Room editorial adaptation to the MailKite contract. No applicable AGENTS.md was found in the scoped app or marketing trees or checked ancestors.

Reused baseline Noah identity, advertised Mac requirements, approval model, free-first-conversation and managed offer evidence. Reused claim-level policy, terms, pinned Tinkerers README/licence, edition distinctions, and October 21 UTC retrieval records from the existing packet. The AlternativeTo URL `https://alternativeto.net/software/noah/about/` remains discovery provenance, not capability evidence; nothing was refetched. Sources in frontmatter preserve their actual October 21 checked dates.

The research packet's old `draftingAllowed:false` was solely tied to the former screenshot gate. October22 EDITORIAL permits source-backed internal drafting via route B; the research files were left unchanged. Noah's app GIF remains link-only because image-specific reuse rights, visual review, capture provenance, and managed-edition fidelity are unverified. The article accurately links its pinned official README demonstration without copying or hotlinking the GIF.

No aliases require a skip record. Noah is the canonical product; Tinkerers is a related BYOK edition, not a duplicate competitor. The separate Noah alternatives draft already documents three verified job-relevant peers from existing packets—CleanMyMac, DaisyDisk, and Mole CLI—for distinct storage jobs. This article links only the live alternatives/comparisons hubs and cache/rebuild utility, not that unpublished alternatives record. No separate alternatives exception or skip page is warranted.

## Visuals and interaction pass

- `slow-mac-diagnostic-path.svg` is an original, first-party editorial decision aid authored for this article. It separates storage, process, and broader symptoms, then distinguishes diagnosis from permission. It contains no competitor UI, logo, screenshot, invented measurement, or product-test claim. Caption and alt text identify its nature and limits. The SVG is 720 × 900 and uses a vertically stacked layout.
- `space-preview-2026-10-21.png` is an unchanged copy of screenshot-library asset `current-space-browser-preview`. Its output SHA-256 matches the retained original exactly. Library provenance: captured `2026-10-21T19:06:45.416416+00:00`, source commit `54828ac3170b45861aee70861dd0b9c658ed7e51`, 2940 × 3468. Existing library review is reused; this job did not freshly inspect the PNG. Caption/alt disclose that it is a browser preview with example data, not native behavior, measured storage, or Noah UI. Contextual article rendering remains unreviewed.
- Interaction pass: the useful reader decision is which evidence to gather before a remedy. The static diagram supplies this aid without filesystem access, a fake calculator, or destructive interaction.

## Claims and limitations preserved

- Noah's managed product is vendor-described as broader desktop support. Terms document automatic read-only diagnostics, explicit approval for destructive/system-modifying actions, and action logs; none is presented as a successful repair test or safety guarantee.
- The managed privacy policy requires email before the first answer, describes hosted conversation processing and repair-history retention without a fixed deletion schedule, and allows specific crash reports, system logs, or settings files to enter a conversation. These are published policy statements, not a backend audit; the homepage's broad “never opens your files” wording is not repeated without qualification.
- Tinkerers is distinguished as a separate AGPL-3.0, user-key edition with direct Anthropic requests and provider charges. Managed-product license, privacy, and command scope are not transferred to it.
- Noah helper grouping, continuous storage-growth monitoring, and managed developer-cache adapters remain **not verified**, not absent. Current managed binary version, some runtime details, Noah currency code/taxes/fair-use cap, and installer authenticity remain unresolved where not material to this workflow.
- Breathing Room is disclosed as our product and as a qualified preview. Source implementations are not represented as distributed-binary parity. macOS 13+, Python 3.10+ for inventory, non-Developer-ID/non-notarized release status, incomplete clean-machine/physical-Intel validation, hosted-AI data transfer, and daily-care runtime boundary are retained. No comparative savings, speed, or safety claim is made.

## Actual validation and checks

- `shasum -a 256` on all three outputs: **PASS**; screenshot-copy hash also matches its source file exactly.
- `/usr/bin/python3` structural check: **PASS**. The authored SVG parses as XML; draft/review fields, two figures, no TODO/internal-link placeholders, only existing hub/utility routes, required screenshot disclosures, matching source/copy hash, and no link to the unpublished Noah alternatives record were checked.
- Site-owned path check showed the article and its asset directory as new/untracked outputs only; no shared site files were edited by this task.
- Content schema attempt using Node imports of `yaml`/`astro/zod`: **not run**, exit 1 because the installed marketing `node_modules` does not expose the `yaml` package. Python PyYAML fallback: **not run**, module unavailable. No packages were installed. Frontmatter fields were authored to the inspected current `src/content.config.ts` contract, but parser/schema validation remains outstanding.
- No shared site check/build/test was run. No generated HTML, publication predicate, RSS/sitemap exclusion, browser viewport/theme review, or live link reachability is claimed. No fresh public research was needed or performed.
- The first identical structural-check attempt with Homebrew Python 3.14 failed before assertions because its `pyexpat` could not link `_XML_SetAllocTrackerActivationThreshold`; `/usr/bin/python3` rerun passed without changing the environment.
- No install, account, native app test, cleanup, purchase, message, credential access, settings change, commit, push, deployment, queue/database change, or subagent.

## Remaining independent review gates

1. Parse and validate the frontmatter with the responsible site check environment; retain `review` / `published: false` and verify draft exclusion in built routes, listings, RSS, and sitemap.
2. Independently verify claims and source conflicts against the retained evidence; refresh volatile offers/availability before publication. Keep the current managed installer version, unknown feature fields, and policy-vs-homepage privacy wording bounded unless new evidence resolves them.
3. Inspect both actual visuals in article context at narrow/tablet/desktop widths and light/dark themes. Preserve screenshot example-data disclosure and assess the original diagram's readability. The source visual library's PNG review is not a rendered article review.
4. Run the serialized site check/build/test and inspect generated canonical, dates, author, social metadata, schema, links, and page behavior through the authorized review process. No independent score or publication approval is awarded here.

The draft is complete for editorial review, not release-ready or deployed. Research records, shared site configuration/navigation/schema/tests, queue/database, and unrelated work remain unchanged.
