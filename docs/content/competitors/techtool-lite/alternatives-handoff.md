# Techtool Lite alternatives draft handoff

Task: `draft-alternatives-techtool-lite`. Editorial date: **2026-10-22**. Outcome: complete internal draft, **not publication approval**. Intended public path: `/alternatives/techtool-lite/`; draft gate remains `status: review`, `published: false`.

## Exact outputs and SHA-256

Marketing root: `/Users/gabe/code/breathing-room/website`.

| Actual file relative to marketing root | SHA-256 |
| --- | --- |
| `src/content/alternatives/techtool-lite.md` | `b2eca531d71fab071c553e16af53f8e427e4d4a8fe7718c6d7d9cce948b28522` |
| `public/assets/alternatives/techtool-lite/task-map.svg` | `9c25c70010f3443f391a5f5110fbe367cdf5f20631f7b4e0381755fbc7f05777` |
| `public/assets/alternatives/techtool-lite/space-preview-2026-10-21.png` | `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a` |

This handoff: `/Users/gabe/code/breathing-room-app/docs/content/competitors/techtool-lite/alternatives-handoff.md`. Receipt: `/Users/gabe/code/breathing-room-app/docs/content/.runtime/draft-alternatives-techtool-lite.1792654203661675000.receipt.json`. Receipt validation checks the handoff's actual file hash separately, avoiding a circular self-hash.

## Intent, selection and evidence

Search/reference replacement guide, not the existing head-to-head matrix or neutral tool profile. About 1,546 body tokens separated by whitespace (includes HTML/URLs; not a prose-only word count). Title 54 characters; description 154. The description supplies the lead, followed immediately by a task decision diagram. Four substantive choices, no rankings or manufactured feature negatives:

| Section | Retained support and boundaries |
| --- | --- |
| Lite baseline and reason to retain it | `research.json` / `research.md` in this directory; claims C1–C6. Free offer and documented diagnostics/maintenance, not verified runtime. |
| Techtool Pro | `docs/content/competitors/techtool/research.json`: T01, T03, T06–T08; Lite C1 for explicit sibling distinction and external-drive scope. T07 APFS qualifications stay attached. T04 numeric price/currency/discount conflict omitted, not resolved. |
| Cocktail | `docs/content/competitors/cocktail/research.json`: C01–C05, C07. Documented caches/database operations, Pilot, OS-specific editions, five-launch demo, native Apple Silicon still in development per vendor. Promotional prices, anticipated Apple policy and unsupported approval semantics omitted. |
| Sensei | `docs/content/competitors/disk-sensei/research.json`: S01–S07, S10, S15, S20–S22. Documented monitoring/maintenance; macOS 14+ explicitly scoped to vendor's August article and version 2.1.2, not current-binary certification. Store version-label conflict disclosed; numeric prices omitted. |
| Breathing Room | `capabilities.md`, Lite B1–B4, `screenshots.json`. One bounded affiliated recommendation for storage investigation, not hardware diagnostics. Source versus binary distinction, permissions/sampling, macOS/Python, signing/notarization, incomplete validation, free core/paid authenticated hosted AI, relevant data transfer, renewal/tax, Ruff exception and daily-care runtime retained. |
| Lite compatibility conflict | C3/C7: product page 13.5–26 versus release note claiming 27. Explicit disagreement; no combined range or installation recommendation. |

Read baseline `docs/content/verification/batch-2.json` for Lite, Pro and Sensei, including retained official-source captures; reused Cocktail's batch-1 capture through its packet. Actual four official capture hashes were recomputed and matched their registers. No broad refetch or new app testing. OnyX packet was inspected but excluded because it has zero verified substantive official facts; no search-index leads promoted to claims.

Discovery remains `https://alternativeto.net/software/techtool-lite/about/`, inherited via Mole page 3. Other peers come from the retained programme graph/packets; the article expressly does **not** assert a Techtool Lite AlternativeTo relationship for each. Lite is not a Pro alias: baseline and vendor explicitly distinguish them, so no skip file is warranted. No peer records were changed.

## Route-B visual provenance

1. **`task-map.svg`**, 600 × 680: original hand-authored editorial decision aid created for this alternatives intent on October 22. Maps four documented jobs to four options, with qualifications. No copied vendor image, logo, UI, invented screenshot or measurements. Dark opaque background/light text; vertical layout. Embedded SVG title/description plus article alt/caption. Source basis is the section claim mapping above. Caption identifies diagram, source date and absence of tests; attributed link to Micromat's official page/interface illustration is link-only. Original bytes and published bytes are the same file/hash.
2. **`space-preview-2026-10-21.png`**, 2940 × 3468: unchanged byte copy of `/Users/gabe/code/breathing-room-app/docs/content/assets/breathing-room/space-preview-2026-10-21.png`, matched to `screenshots.json#current-space-browser-preview`. Capture `2026-10-21T19:06:45.416416+00:00`, source commit `54828ac3170b45861aee70861dd0b9c658ed7e51`, local browser source `http://127.0.0.1:1431/`. First-party owner-requested capture; no blanket third-party trademark licence inferred. Opened/read actual PNG in this job: example banner and no-change warning retained; category chart partly obscured by real assistant composer. No edits, cropping or redactions. Caption accurately says example data, recorded source render, not native/release testing or savings. Reuse per shared first-party manifest; final page-context/privacy review pending.

Micromat/other competitor UI not copied or downloaded. Historical packet image blockers are preserved as research history, superseded for internal drafting by October22 route B, not reclassified as image permission. A new native capture is not claimed.

## Actual validation

- Read PLAN, October22 EDITORIAL update, capabilities, screenshots, both Lite research files, baseline and peer packets, website publishing/schema contract, and MailKite reference. Loaded blog-write, blog-seo-check, blog-factcheck and browser-automation. No AGENTS.md found in scoped trees or checked ancestors.
- `/usr/bin/python3` scoped assertions **passed**: review/unpublished fields; no body H1 (layout owns H1); first body element is a figure; exactly two figures; both asset paths are actual files; SVG parses as XML; no TODO/TBD/placeholder/internal-link markers; official-source hash matches for four products; PNG identity/hash matches original.
- Internal route-file checks **passed** for `src/pages/alternatives/index.astro`, `src/pages/comparisons/index.astro`, `src/pages/tools/cache-rebuild-checklist.astro`. Only these known hubs/utility are linked internally; no hidden peer comparison/tool/blog records linked. These are source-level checks, not new live HTTP checks.
- `/Users/gabe/.nvm/versions/node/v25.0.0/bin/node --input-type=module` **passed** scoped frontmatter validation using the actual schema expression read from `src/content.config.ts` and its `astro/zod` dependency: all 12 source entries accepted, real title/description/date/author fields valid, review/unpublished retained. No site output generated.
- Initial Python attempt reached SVG parsing then **failed** because Homebrew Python's `pyexpat` cannot resolve `_XML_SetAllocTrackerActivationThreshold` in system libexpat. No environment fixes attempted. Re-ran checks successfully with existing `/usr/bin/python3`. Asset copy had already completed; no second overwrite was attempted.
- Root module-resolution probe found yaml/gray-matter/markdown-remark not root-resolvable; used limited record-specific scalar extraction and actual Zod schema instead of installing dependencies. This does not certify full Markdown rendering.
- Manual claim pass checked section claims against retained excerpts, preserving source conflicts and unknowns; no new source retrieval date asserted. No benchmarks, measurements, fabricated experiences or unsupported negative table cells. Citations sit with relevant claims. No full live factcheck was claimed.
- Interaction pass implemented the task diagram and four-step non-executing decision checklist. No JavaScript, cleanup controls, uploads, sign-ins or irrelevant demo repository.

## Remaining independent review gates

1. Independent factual review of exact hashes above, including Lite compatibility conflict, Pro APFS qualification and Sensei version/store discrepancy. Do not certify unsupported platform ranges. Refresh volatile vendor offers within 30 days and before release; actual retained checks are October 21.
2. Shared `pnpm check`, `pnpm build`, `pnpm test` **not run**, as explicitly prohibited in this worker. Responsible serialized review job must run them and inspect draft exclusion from routes, listings, RSS and sitemap. Schema parsing alone is not a site build or leakage test.
3. No browser used in this drafting job; browser skill loaded, no Chrome recovery needed. Independent isolated rendered fixture needed at roughly 390/768/1440 px in both themes, with actual opened screenshots: inspect map labels, full-page PNG readability/banner, captions, keyboard/link behavior and overflow. Native screenshot and competitor image rights not invented. If the full PNG is too small on mobile, reviewer should request a documented contextual crop preserving disclosures, not relabel sample data.
4. Inspect eventual canonical `/alternatives/techtool-lite/`, H1, author/dates, OG/Twitter and Article/Breadcrumb schema through responsible fixture; route is intentionally absent publicly while unpublished. No frontmatter-only claim of SEO/render pass.
5. Independent itemized quality score remains pending; no numeric score or release-ready status awarded by drafter. No approval inferred from completion receipt.

No purchases/accounts/messages, app execution, cleanup, credentials, settings changes, subagents, shared navigation/schema/tests/queue edits, commits, pushes or deployments. Only this owned article, its asset files, this handoff and required receipt were written. Unrelated work and original research preserved.
