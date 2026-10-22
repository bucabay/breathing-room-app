# Dusty Storage tool-profile handoff

Task: `draft-tool-dusty-storage` · Draft review: **2026-10-22** · Source checks retained from **2026-10-21**.

## Outcome and ownership

Completed one neutral, search/reference tool profile, not a comparison, replacement roundup, calculator or claim that Breathing Room built Dusty. Target route: `/tools/dusty-storage/`; canonical on eventual publication: `https://breathing-room.chatic.ai/tools/dusty-storage/`. **This route is not published or currently claimed live.** Frontmatter remains `status: review`, `published: false`, with date/updated October 22, 2026. No shared files or research packets were edited.

Read PLAN.md, the October22 EDITORIAL.md update, capabilities.md, screenshots.json, both Dusty Storage research files, the retained alias decision, the current collection schema/publication filter/route, and applicable blog-write, blog-seo-check, blog-factcheck and browser-automation instructions. No AGENTS.md was found in either scoped repository or applicable ancestors. Applied the Breathing Room editorial adaptation over generic blog quotas. No new source retrieval, browser session, app test, download, account, permission request or image copying was necessary.

## Exact outputs / SHA-256

| File | SHA-256 |
| --- | --- |
| `/Users/gabe/code/breathing-room/website/src/content/tool-profiles/dusty-storage.md` | `b542056ca7cf7375cf2c1d53851867e57a0c15f5015cc8f163ab345c126de822` |
| `/Users/gabe/code/breathing-room/website/public/assets/tools/dusty-storage/documented-jobs.svg` | `2fdb81fcd082fd4bd3471f2c14c792696815ec70dd7c2030f02ccf306b9ee8a7` |
| `/Users/gabe/code/breathing-room/website/public/assets/tools/dusty-storage/review-boundaries.svg` | `0f129ade06217de4c7940e24a5dc8720443e8fe3ab5bae39d4fcdd53193fec60` |

This handoff's hash is retained in the task receipt rather than attempting a self-referential hash. Receipt: `/Users/gabe/code/breathing-room-app/docs/content/.runtime/draft-tool-dusty-storage.1792639504621279000.receipt.json`.

## Identity and source adjudication

`research.json` C1 and `verification/alias-decisions.json` establish a distinct dustystorage.com offering, not an alias of the MIT-licensed toprak.sh Dusty. The alias record's `canonicalId` field must be read with its `status: distinct-products` and explicit decision; it does not authorize a merge. No tool-skip.md is warranted.

Reused the existing packet, not its obsolete image-only drafting prohibition. October22 EDITORIAL explicitly permits this draft stage and original route-B decision aids for neutral profiles. Historical blockers in research.json/.md are preserved unchanged.

| Draft material | Retained support | Treatment |
| --- | --- | --- |
| Identity and platform | C1–C2, S1/S7 | Domain-qualified; advertised macOS 13+, Apple Silicon/Intel, not tested compatibility. |
| Version | C3, S6 | v2.5.1 label at original source-check date; no release date or binary parity inferred. |
| Price, trial, licence | C4–C6, S3/S5 | Displayed dollar symbol; one-time device limits; 24-hour cleaning trial; v2.x update boundary; no invented ISO currency, tax, checkout total or future-major entitlement. |
| Documented jobs | C7–C8, S2/S6 | Disk map, backup offload/restore, uninstallation and named developer artifacts are documented, not tested. No safe-deletion or complete-removal guarantee. |
| Removal | C9, S5 | Trash by default; Dusty cannot recover emptied Trash; backup/rebuild cautions. |
| AI/privacy | C10–C11, S1/S3/S4/S5 | Metadata-transfer disclosures and daily managed quota preserved; contradictory blanket privacy wording explicitly identified. BYOK is not free/unlimited service. |
| Trial identifier | S6 v2.5.0 excerpt | Server-backed hardware UUID validation attributed; retention/implementation unknown. |
| Unknowns | C12 rejected; C13/C14 not verified | No blanket no-transmission, verified notarization, open-source, monitoring-absence or runtime-parity claims. |

Directory subscription pricing is not adopted over the retained official one-time offers. Family “perpetual updates” versus terms' v2.x wording remains explicitly unresolved; no v3+ promise. Conflicting stale-download thresholds and named AI-model availability are omitted. Affiliation is explicit without a Breathing Room recommendation or comparative feature pitch.

Peer packets for DaisyDisk and FreeMacSoft AppCleaner were inspected: respectively documented disk-map exploration (D5) and app-removal workflow (ac-purpose/ac-workflow). These are task-specific peers, not evidence of complete Dusty replacements or vendor relationships. This job owns a factual tool profile, not the separate alternatives intent; no alternatives section, ranking, new peer record, skip of another queue job or draft-only internal peer link was manufactured.

## Route-B visual provenance and interaction pass

Both SVGs were originally authored for this draft on October 22, 2026 by the scheduled Breathing Room content worker. Each is 720 × 740 with a vertical layout, explicit title/description, accessible page alt text and visible caption. Neither contains vendor pixels, logos, private data, copied UI, external assets, scripts, measurements or invented screenshots. Original bytes are the published-asset bytes; no crop, screenshot alteration or raster derivative exists. Rights basis: original editorial diagrams under the user's route-B authorization, not an inferred competitor-image licence. Publication-context and independent visual approval remain pending.

- `documented-jobs.svg`: maps C7/C8's distinct documented jobs: explore sizes, preserve phone backups, review removal candidates. Source: `https://dustystorage.com/features.html` (S2; checked October 21). Placed immediately after the rendered description. Caption links the official feature guide/disk-map illustration, **link-only**, credited to Dusty. No official image was downloaded or hotlinked.
- `review-boundaries.svg`: maps AI metadata sharing (C10), preservation versus removal (C7 plus explicitly editorial precautions), and default Trash/final recovery limits (C9). Sources: homepage S1, privacy S4, terms S5; original dates retained. Appears later at the recovery decision. Caption calls it an editorial decision aid, not a tested sequence.

Interaction pass completed in source: the useful aid is a non-executing decision checklist. Readers assess sharing, preservation and recovery requirements; unknown recovery needs mean pause. No interactive filesystem control, upload or forced calculator would help this profile. Neutral-profile policy permits these original aids rather than an unrelated first-party preview. Existing Breathing Room screenshots were read in the manifest but not copied or used to imply competitor behavior.

## Actual validation

Run from `/Users/gabe/code/breathing-room/website`; commands were inline, read-only scripts, not new shared test files. Output retained here and in the receipt; no separate log file is claimed.

1. Node v25.0.0 inline assertions using `astro/zod`, YAML resolved from Astro's existing dependency tree, and the **exact schema expression read from current src/content.config.ts**: **PASS**. Parsed all frontmatter; status/published/date/updated correct; seven source records have original October 21 checks. No unsupported schema fields were added.
2. Imported current `src/lib/publication.ts`: **PASS**, `isPublished` returns false for this record on October 22. Read source confirms `content.ts` maps tools to toolProfiles and the dynamic route only includes publishedEntries. This is source-level exclusion verification, not a new build/feed-leakage test.
3. Title **49** characters and description **155**: **PASS**. Primary product identity and limits are natural, without a ranking/power-word/statistics quota. Approximately **983** body whitespace tokens, including HTML attributes; not an exact prose word count. No body H1 (layout supplies it), placeholder markers or duplicate opening. Two figures, captions and nonempty descriptive alt texts present.
4. Local assets and internal routes: **PASS**. Both SVG files exist; `/tools/`, `/tools/storage-units/` and `/tools/storage-headroom/` have actual source route files. No draft-only comparison/blog/peer route is linked. This is source-route validation, not a fresh production HTTP check.
5. Source reuse and hashes: **PASS**. Seven source URLs match the retained research ledger. Discovery snapshot SHA-256 matches `72a071f3a796ee8808cb22620c59bf071dd31cd1dedbfae9a747c29d3bb9a681`; retained official snapshot matches `b6bd5178f65df610dad2e8046e16cf132f258d0c42d722fc0bb4492a0f44296b`. New file hashes are listed above. Source-adjacent assertions were manually cross-checked to the claim ledger; no live fetch is represented as newly performed.
6. Initial Python ElementTree XML check: **FAILED due to environment**, missing `_XML_SetAllocTrackerActivationThreshold` in the installed Python/expat linkage. No packages or settings changed. Replaced it with `/usr/bin/xmllint --noout` on both exact SVG files: **PASS**, exit 0. Additional Node assertions: **PASS**, vertical viewBoxes, role/title/description and absence of scripts or external image/href assets.

## Remaining independent review / publication gates

This drafting job is complete, **not publication approval**. No score is awarded for unperformed checks.

1. Independent factual/editorial review of the exact hashes and source excerpts, including source conflicts, quotas, updates and price scope. Refresh volatile facts within 30 days and again before publication if stale; do not silently change source-check dates.
2. Review actual rendered output, canonical/H1/social metadata/Article and Breadcrumb schema, draft exclusion from routes/listings/RSS/sitemap and internal HTTP destinations. The expected canonical follows inspected routing, not a rendered-page verification.
3. Independently inspect both diagrams and captions at approximately 390/768/1440 px in both themes for legibility, text fit, contrast and source-link usability. XML and dimensions alone do not establish visual approval. Browser work was not performed in this job.
4. A separately authorized serialized site job must run `pnpm check`, then `pnpm build`, then `pnpm test` and retain results. **None ran here**, per explicit prohibition on shared builds and shared edits; no shared nav/schema/tests/queue changes were made.
5. Complete the five-category editorial scorecard against this snapshot and require the programme's threshold with zero publication blockers. This drafter's checks are not independent approval.

No commits, pushes, deployments, purchases, messages, cleanup, app installation, credential reads, computer-setting changes, subagents or queue/database mutations were performed. Unrelated working-tree changes were preserved.
