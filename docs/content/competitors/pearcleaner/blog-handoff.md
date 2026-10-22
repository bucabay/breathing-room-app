# Pearcleaner workflow article handoff

Task: `draft-blog-pearcleaner` · drafted October 22, 2026. Complete internal draft; **not publication approval**.

## Outcome

Created `/Users/gabe/code/breathing-room/website/src/content/blog/pearcleaner-mac-workflow.md`, intended route `/blog/pearcleaner-mac-workflow/`. The page is `status: review`, `published: false`, dated October 22, and uses the distinct workflow intent: decide between removing a known unwanted app and investigating storage that changes while an app stays. It does not expand the product profile or comparison matrix into a duplicate.

## Exact owned artifacts and SHA-256

| File | SHA-256 |
| --- | --- |
| `/Users/gabe/code/breathing-room/website/src/content/blog/pearcleaner-mac-workflow.md` | `ec6d2056647e55c0b81ecf1f14de1a45d657a40546c7bc21e3136fea7f37fd22` |
| `/Users/gabe/code/breathing-room/website/public/assets/blog/pearcleaner/removal-or-investigation.svg` | `3a083fc6d2a01b07705cabbe4dd90f2b46fdebd0985859ced79744f2e3a20fd4` |
| `/Users/gabe/code/breathing-room/website/public/assets/blog/pearcleaner/space-preview-2026-10-21.png` | `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a` |

The copied Space image hash matches the source asset and `screenshots.json`; it was copied byte-for-byte with no crop or edits. Receipt: `/Users/gabe/code/breathing-room-app/docs/content/.runtime/draft-blog-pearcleaner.1792668065966410000.receipt.json`.

## Evidence and editorial boundaries

- Reused `research.json`/`research.md`, verification batch records, `capabilities.md`, and `screenshots.json`. Existing source retrieval dates remain October 21; no redundant baseline fetch was performed. AlternativeTo is used for discovery only.
- Pearcleaner's uninstall, orphan-search, environment/manager feature list, release metadata, OS support statement, permission requirements, maintenance pause and qualified licence terms are presented as vendor documentation, not execution results. The retained release API reported 5.4.3 from November 26, 2025 with ARM/Intel assets; README compatibility statements are not runtime certification.
- Preserved the conflict between AlternativeTo's “Discontinued”/“Open Source” labels and the author's more qualified indefinite maintenance pause and Apache 2.0 with Commons Clause. Unknown privacy/network, account, signing, approval, per-file and recurring-growth details are not turned into negative claims.
- Breathing Room claims reuse the October 21 register: source-supported investigation scope; preview and Python limits; disclosed signing/notarization and physical Intel gaps; authenticated hosted-agent boundary; advertised optional AI Care price. Source implementation and published disclosures are not binary/backend tests.
- Route B used: original accessible SVG is an evidence-backed workflow decision diagram, explicitly not Pearcleaner UI or a test. The linked Pearcleaner screenshot remains unembedded because its reuse basis, depicted view/version, capture date, and privacy are unknown. The first-party Space preview retains the example-data/native-result caption and limitation.
- Interaction pass: diagram plus a non-executing, five-step decision checklist; no cleanup controls, file access, fabricated savings, or demo repo.
- No `/alternatives/pearcleaner/` skip file was needed: a separate alternatives page already exists at `website/src/content/alternatives/pearcleaner.md`, with a distinct replacement intent and multiple documented uninstall peers as recorded in `alternatives-handoff.md`. This workflow article is not a duplicate of that page.

## Checks actually performed

- **PASS:** Word count check reported 1,436 words; draft metadata inspection confirmed title, description, `status: review`, `published: false`, current date and author.
- **PASS:** No TODO/placeholder/internal-link markers or unsupported `best`/safety-superlative copy found by targeted grep.
- **PASS:** Exact PNG hash equals the source and inventory hash; source copy is byte-identical.
- **PASS:** Original SVG parsed with `/usr/bin/python3` `xml.etree.ElementTree`.
- **PASS:** Confirmed the canonical Pearcleaner comparison, distinct alternatives record and new workflow record exist as files.
- **NOT RUN:** `pnpm check`, shared `pnpm build`, and `pnpm test`, as this scheduled task forbids shared site builds/checks. No rendered HTML, browser viewport/theme inspection, link click test, or independent review is claimed.
- **Tool diagnostic:** Default Homebrew Python 3.14 could not load `pyexpat` due a system libexpat symbol mismatch; read-only SVG validation passed on the already-installed `/usr/bin/python3`, with no system changes. Node v25 is available at the requested path, but YAML dependency resolution from the website root failed (`Cannot find module 'yaml'`); no package installation was attempted.

## Remaining publication review

1. Independently fact-check the article and exact visual hashes against source passages; refresh material volatile details if publication occurs after the evidence window.
2. Independently inspect the SVG and full-height PNG in rendered mobile/tablet/desktop layouts and light/dark themes; preserve visible image disclosures and assess table/text overflow. No browser or rendered review has passed here.
3. Use the responsible site workflow for isolated draft rendering; verify metadata/schema and exclusion from routes, listings, RSS and sitemap. Keep the record unpublished until the publication gate and independent review pass.
4. Keep Pearcleaner UI screenshots link-only unless exact asset rights, visual content and privacy are independently cleared. Do not reclassify the packet's historical `draftingAllowed:false`; its image-rights blocker remains relevant to copying that image, not to this route-B draft.

No research packet, queue/database, shared site files, unrelated content, navigation, schemas or tests were changed. No accounts, purchases, messages, app installation, cleanup, commits, pushes or deployments occurred.
