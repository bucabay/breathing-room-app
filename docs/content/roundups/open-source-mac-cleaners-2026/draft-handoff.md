# Draft handoff: seven open-source Mac maintenance tools

Task: `draft-roundup-open-source-mac-cleaners-2026`. Draft completed **October 22, 2026**, local timezone UTC+03. Actual validation timestamps are October 21 UTC; this is a timezone difference, not backdating. Author is the Breathing Room team; no human hands-on experience or independent review is implied.

## Outcome and ownership

- Article: `/Users/gabe/code/breathing-room/website/src/content/blog/open-source-mac-cleaners-2026.md`.
- Public assets: `/Users/gabe/code/breathing-room/website/public/assets/roundups/open-source-mac-cleaners-2026/`.
- This directory contains evidence copies, missing-licence retrievals, validation and this handoff. Only these owned paths and the requested receipt were written.
- Complete search/reference article, approximately **1,520 body words** by the retained script, seven comparison rows and seven individual selections. Order is not a ranking. `status: review`, `published: false`.
- Read PLAN.md, EDITORIAL.md including October22 update, AUTOMATION.md and the adapted MailKite contract. No applicable AGENTS.md was found in app/marketing trees or checked ancestors. Loaded blog-write, blog-factcheck, blog-seo-check and browser-automation. No agents spawned.
- Existing verification batches and all six candidate research packets were read first. Historical image-only blockers are preserved in those packets, not edited away; October22 route B authorizes this draft. No queue/database edits, shared build output, account, credentials, cleanup, native installation, deployment, commit, push or messages.

## Evidence map and per-claim support

`reused-evidence.json` preserves each original packet's claims, source ledger and dates, plus a hash of the original packet. It does not renew those checks. `sources.json` describes only missing official material retrieved for this job. `licence-checks.json` verifies actual retained licence text for all seven, rather than badges. Official URLs beside article claims are the reader-facing source trail; the IDs below join to the retained source packets.

All product capabilities below are **documented/source-inspected, not runtime-tested**. Selection reasoning and when-not-to-use advice are editorial judgments derived from those limits. No efficacy, savings, performance, security detection rates or awards are claimed.

| Article claim / location | Evidence, locator and boundary |
| --- | --- |
| Definition section: Commons Clause is source-available, not unrestricted open source | `sources/commons-clause.txt`, official https://commonsclause.com/, “Is this Open Source?” explicitly says best not to call it open source. Terms exclude right to Sell; service scope is quoted/qualified, not a ban on all commerce. Original OSI URL returned 403; no claim relies on having read its blocked response. |
| MIT permits commercial redistribution with notice conditions | PureMac `sources/license.txt` and Dusty `assets/DUSTY-LICENSE.txt`: permission includes sell, notice retention. GPL and Apache/BSD descriptions read against corresponding actual texts in `licence-checks.json`; obligations are not waived. |
| Seven-count includes App Eraser conditionally, not under settled uniform terms | Official root GPL-3.0 is present; package `license: ISC` also present. Both are open-source families; do not infer a proprietary restriction or pretend the conflict resolved. No redistribution instructions given. Publication reviewer must specifically approve this qualified inclusion. |
| Table: Mole CLI GPL-3.0, native edition proprietary | Mole claims `cli-license`, `native-license`; pinned CLI LICENSE in existing packet; official README expressly says “separate proprietary app.” Native retail pricing not needed and omitted. |
| Table: Mole macOS 12+, Intel/Apple Silicon | Mole `cli-platform`, retained official README, documentary floor only. Not transferred from native macOS 14+ offer. |
| Mole section: CLI developer purge and activity-selection boundaries | Mole `cli-purge`, pinned README; no newest-stable CLI assertion. |
| Mole section: clean/purge/installer can permanently delete; default user Trash emptying | Mole `cli-delete`, official README warnings. No command executed, even help; earlier packet explains startup mutation risks. |
| Table: PureMac MIT | Retained actual licence and metadata in PureMac sources, source commit `1fbebb9840f2919a7d7fb71210c6ed37fe39f193`. |
| Table: PureMac desktop/CLI, macOS 13+ source floor | PureMac `platform`, `removal`, `permanent-source`; source target is not installed-binary parity. |
| PureMac section: allocated-space exploration and app/developer/configuration suite | PureMac `space`, `developer`, `protection`, `free`. Read repository over conflicting homepage promises. |
| PureMac section: Trash differs from category/Docker/snapshot/CLI deletion | PureMac `removal`, `permanent-source`, `approvals`; pinned CleaningEngine source corroborates permanent remove branch. No blanket Trash-only claim. |
| PureMac section: auto-clean unattended; protection not antivirus | PureMac `approvals`, `protection`. No claim of no monitoring or no helpers. |
| Table: App Eraser Electron desktop scope | App Eraser AE-01, AE-02, AE-10, package and official README. Development runtime not turned into a user prerequisite. |
| App Eraser: bundle-ID/name matching and checked candidates | AE-04, AE-05, AE-08; pinned `src/main/index.js` and `controller.js`. Matching is not ownership proof. |
| App Eraser: selected files confirmed for Trash | AE-05/08, controller confirmation wording. Not a successful removal observation. |
| App Eraser: release 1.0.0 in 2023; present compatibility/signing unknown | AE-03 release API and packet unknowns. Not labeled abandoned. No OS minimum or native architecture inferred. |
| Table: Depflush GPL source excludes name/icon | Depflush D03, README licence section, plus newly retained actual root GPL text. No image/trademark licence inferred. |
| Table: Depflush macOS 14+, Intel/Apple Silicon, native app | D01 and source README, documented requirements; no binary test. |
| Depflush: dormant dependencies vs Docker review | D04/D05 official homepage. Docker availability and dependency restoration are separate concerns. |
| Depflush: locally built images, stopped containers, orphan volumes unticked | D05 exact official passage. Not a certification that preselected registry objects are disposable. |
| Depflush: Docker running prerequisite | D05 official documentation. No Docker command run. |
| Depflush: Trash default, permanent optional | D06. Not all deletion reversible. |
| Depflush: not yet notarized | D09 vendor disclosure; no signature inspection or protection-bypass advice. |
| Table: Dusty MIT, Toprak identity, distinct from Dusty Storage | Dusty D1/D3, actual pinned MIT, retained batch alias decision. No Dusty Storage price/image imported. |
| Table: Dusty native app/CLI/Shortcuts, macOS 13+ | Dusty D2 and retained pinned README command-line/Shortcuts documentation. Version scope v2.1.0. |
| Dusty: item review, dry run, confirmation | D4, pinned README. Source documentation, not execution. |
| Dusty: manifest/activity-based stale-artifact rules | D6. Rules are not a guarantee of a successful rebuild. |
| Dusty: grouped memory and optional automation | D7–D9. No negative claims about competitor monitoring. |
| Dusty: tier “Safe” is not warranty; Undo and Trash limits | D12 and packet source-conflict boundary. No universal reversibility claim. |
| Table: Mac Sai BSD-3-Clause | Newly retained actual LICENSE, copyright Mac Sai Contributors; joins packet C2/S4. |
| Table/section: Mac Sai native suite, project junk, disk exploration | C1, C4–C8 and source architecture. Repository-internal MacClean naming not a different shortlist entry. |
| Mac Sai: adjacent markers and ignore-rule checks | C4/C5, official README; no tested folder-removal assertion. |
| Mac Sai: curated scanner explicitly not antivirus | C10. No detection accuracy/performance claim. |
| Mac Sai: Trash-first is not universal reversibility | C5/C6, documented shredder/Trash-emptying exceptions. |
| Mac Sai: v1.25.7 macOS 14+ | C3, release API/page checked October22 in original packet. No binary architecture guess. |
| Table: Breathing Room Apache-2.0 desktop only | Local LICENSE read in full and README 231–258; hosted backend not included, trademark rights excluded. No service entitlement inferred. |
| Breathing Room: storage/category/app/project, grouped process and sampled activity scope | Current local README 25–43, 74–118 and existing capabilities register. Scope is documented, not binary feature certification. |
| Breathing Room: daily care exact approvals while running | README 120–128; capability packet caveat preserves optional automatic verified-Ruff mode. Article does not promise asks before every action. |
| Breathing Room: preview, Apple Development signed, not Developer ID/notarized | Current README 15–18, 59–70; existing capabilities release evidence. No fresh signature audit claimed. |
| Breathing Room: macOS 13+, Python 3.10+ unbundled; Intel runtime incomplete | README 62–72; physical Intel not certified. Permissions can cause partial inventories. |
| Breathing Room: free local core, optional paid AI, authentication and off-device context | README 141–172, 231–236; no price or unverified quotas repeated. Hosted reasoning is not offline. |
| Breathing Room: GitHub downloads distinct from website registration | README 45–51, 152–157. No checkout/login used. |
| Final checklist: size does not establish deletion permission; restoration cost matters | Editorial synthesis of Mole purge, Depflush project/Docker, Dusty stale-artifact, PureMac removal and BR README review boundaries. No hypothetical calculations or guaranteed restoration. |
| `/tools/` is live | HTTP urllib returned 403; Chrome owned tab 219 loaded titled “Free Mac storage tools,” with actual calculator descriptions and links. Browser snapshot read. No draft cross-links used. |

## Visual route, provenance and interaction pass

**Route B used throughout.** Competitor screenshots were not copied, downloaded or hotlinked. Each selection instead links its official README/image/guide with an honest example/version caveat. Those links are references, not reuse clearances. This avoids unresolved older image gates without rewriting the original packets.

### Visual 1: original decision workflow

- File: `selection-workflow.svg` in owned public assets; original authoring for this article on October22, no external image model/stock/competitor UI.
- Kind: original documented-workflow diagram, explicitly not app UI or a tested cleanup.
- Source basis: exact-edition licensing, seven documented tool jobs, owner/restoration/method/approval review from claims above. Categories are editorial selection aids, not exhaustive feature exclusions.
- Alt and caption supplied in article. Source citations are directly below/after the diagram in the table. At 600×1000 viewBox, the chain stacks vertically; opaque dark background gives stable contrast in either site theme.
- Browser served read-only from owned assets at `http://127.0.0.1:43891/selection-workflow.svg`; screenshot saved here as `diagram-browser-check.png`, opened and read. Labels fit without clipping at that actual browser viewport. This is not six-width/theme page QA.
- Interaction pass: implemented a non-mutating decision aid (licence → job → known owner/restoration/removal). A scanner, upload widget, forced calculator or cleanup command would not help this selection task and would imply evidence we do not have.

### Visual 2: first-party current-source preview

- Original: `docs/content/assets/breathing-room/space-preview-2026-10-21.png`, current-source library record `current-space-browser-preview`.
- Published draft copy: `breathing-room-space-preview.png` in owned assets. Bytes unchanged; original/copy SHA-256 `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a`. 2940×3468. No crop, label change or redaction.
- Original capture: `2026-10-21T19:06:45.416416+00:00`, source commit `54828ac3170b45861aee70861dd0b9c658ed7e51`, browser preview `http://127.0.0.1:1431/`. Not freshly recaptured; currentness explicitly scoped to recorded commit/date rather than installed binary.
- Opened and read actual PNG this job. Visible example-data banners, storage categories, folder-size rows; assistant overlaps part of chart. No private user paths observed. Full-resolution link supplied because the complete tall view may be small on phones.
- First-party owner-requested capture reuse basis inherited from `screenshots.json`; no blanket third-party mark rights/endorsement asserted. Per-page privacy/rights review still pending.
- Caption explicitly says example data, not native scan/activity/results; source capture date retained. No numerical example treated as measured storage or cleanup savings.

## Validation actually performed

1. Ran `python3 .../collect-gaps.py`: first run retained five public source bodies but failed on OSI 403 before global metadata write. Script amended to preserve cached bodies without pretending exact acquisition instants survived. Second run completed manifest, retaining five hashes and explicit OSI error. No verification was inferred from status alone: licence bodies, package metadata and relevant Commons Clause prose were read.
2. Inspected seven actual retained licence texts; asserted their identifying text; confirmed App Eraser package ISC conflict. Saved `licence-checks.json` and original source/claim references in `reused-evidence.json`.
3. Ran `PATH=/Users/gabe/.nvm/versions/node/v25.0.0/bin:$PATH node docs/content/roundups/open-source-mac-cleaners-2026/validate.mjs`. First run exposed a validator bug splitting Markdown table separators as frontmatter; corrected parser to anchored delimiters. Final run **passed**: actual current site Zod schema/YAML, draft flags/date, exact seven rows, ten H2s/no body H1, two visuals, file existence, source-preview hash, permitted internal link and no placeholder links. Output/hashes in `validation.json`.
4. Title 43 characters; description 157 characters. No fabricated FAQ/review schema, statistical quotas, power-word stuffing or search-volume claim. Frontmatter has official source URLs with actual original check dates. Description is the lead; body opens with the workflow visual rather than repeating it.
5. Source/preview image opened; SVG actually browser-rendered, screenshot saved and opened. Only owned browser tab 219 used; no pre-existing tab interaction or Chrome recovery. Live tools hub verified with browser content after HTTP-client 403.
6. No shared `pnpm check`, `pnpm build`, `pnpm test`, `dist/`, `.astro/` or generated types touched. User specifically prohibits shared build output. Static checks do not replace that separately serialized work or certify built draft exclusion.
7. Scoped `git diff --check -- ...` returned exit 0 in both repositories; since these are new files, also directly checked owned Markdown/JS/Python lines for trailing whitespace. SVG XML and 600×1000 viewBox parsed successfully using `/usr/bin/python3`. Initial Homebrew Python XML check failed because its `pyexpat` references a missing system libexpat symbol; system Python passed without package installation or settings changes. Owned browser tab 219 closed after inspection. The read-only asset server started for the SVG check uses localhost port 43891; no existing listener was stopped.

## Publication questions and pending gates

- **Independent evidence approval:** review the exact snapshot, especially qualified App Eraser inclusion. Does the root GPL plus disclosed ISC conflict warrant this editorial count? Resolve with maintainer only if a reviewer requires uniform redistribution terms; no permission request/message was sent.
- **Release compatibility:** current App Eraser OS/signing remain unknown. No install recommendation certifies it. Verify before any stronger installation guidance; do not infer discontinuation from release age.
- **Visual currentness:** approve the source-preview scope/date or arrange a new authorized first-party capture. Do not relabel this as current native binary evidence. Check the tall image and table at 390/768/1440 widths in both themes; potentially require a rights-safe crop preserving example banners.
- **Independent rendered review:** canonical/OG/Twitter/Article/Breadcrumb output, responsive text/table/image behavior, keyboard/link checks and built draft exclusion are not checked here. Shared check → build → tests must be run by the authorized serialized review job without exposing this draft publicly.
- **Source freshness:** most documentary packets date October21; missing licence checks date October22. Refresh volatile release/platform facts within 30 days or before publication if stale. Hosted allowance, price totals, compatibility, complete network behavior and source-to-binary parity are not invented.
- No independent score awarded. A self-score cannot override these gates. Draft completion is not publication approval, release-ready status or deployment.

Final artifact hashes and static results are in `validation.json`. The required receipt reports **done for the unpublished drafting task only**.
