# MangoDisk comparison draft handoff

Task: `draft-mangodisk`. Drafted/substantively reviewed October 22, 2026. **Complete internal textual draft; not publication approval.** Search/reference track, owned intent: Breathing Room versus MangoDisk only. No alternatives, neutral profile or workflow article was created. No AGENTS.md found in scoped trees or checked ancestors.

## Outputs and exact SHA-256

Marketing root: `/Users/gabe/code/breathing-room/website`.

| Real file, relative to marketing root | SHA-256 |
| --- | --- |
| `src/content/comparisons/mangodisk.md` | `8f33eb5f71b913f75d8b59f85c6acf086583276f046165b4c88aa0ec072978c4` |
| `public/assets/comparisons/mangodisk/decision.svg` | `e1abea9c7dfac227de42f99dad54b33d56f54ea596abbfad39144f351310c2a4` |
| `public/assets/comparisons/mangodisk/space-preview-2026-10-21.png` | `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a` |

Intended public path: `/comparisons/mangodisk/`; **not live**. Fields are `status: review`, `published: false`, date/updated `2026-10-22`, author Breathing Room team. Single source-backed comparison, roughly 1,185 whitespace tokens including Markdown links/markup; not a promised prose word count. Title 55 characters; description 161 characters (natural introduction retained rather than inserting a statistic or awkward truncation).

## Evidence reuse and claim audit

Read PLAN, October22 EDITORIAL update, capabilities and screenshot manifest; loaded blog-write, blog-seo-check, blog-factcheck and browser-automation; read MailKite contract with project adaptations. No browser needed or used; no profile recovery attempted. No subagents.

Reused `verification/batch-1.json` MangoDisk entry and both original retained snapshots; their actual SHA-256 values matched research.json:
- Directory: `910529d590f55abae7b4ed6193436885a6a74cf01152a19047c81ae442214385`, original retrieval October 21, 2026, 19:09:20.763Z.
- Homepage: `00d70322ed2fd21a11e80a8d5e1325d5eb78070d2d583067094d4d3925a561d5`, original retrieval October 21, 2026, 19:09:33.992906+00:00.

Read and preserved existing research files without edits. Research JSON hash: `dacf1d5c0a9c01a97aebd00a653687f490f928b052859efe6f17f8e71bd9932a`; research Markdown: `fa896c2fc7cbe291dde5cfb014f28c196af0f995e270ac155ecf07883be1eda2`. Capabilities hash: `cfc30c88a94cbaea9e01d4fb5bde253911442993cda90dcb283d48445f4d4613`; screenshots manifest: `d2a7a92350ba7e03edc8d80d171139e5f1cba470da5b3cbd531790de3aab974c`.

| Draft claims | Retained evidence | Treatment |
| --- | --- | --- |
| Free/no-account desktop, GPL | C01–C02 / S0,S1,S6 | Advertised desktop offer, not unlimited hosted AI or image licence |
| Release 1.2.0; macOS 12.5+, CLI and other platforms | C03–C04 / S1,S2,S4 | Documentation and metadata only; no binary/signature/platform tests |
| Developer caches and custom rules; scan/select/confirm | C05–C06 / S3 | Documented, not a fabricated cleanup walkthrough |
| Local scans/history, AI metadata, provider choice/cost, AI explanation not execution | C07–C08 / S5,S7 | Routing wording conflict explicitly preserved; allowance unknown |
| Permanent deletion and resource/storage breadth | C09–C10 / S1,S7 | Strengths retained; no unsupported negative monitoring/helper/scheduler cells |
| Breathing Room source workflows, price, licence and limitations | B01–B02 / capabilities.md | Source versus release distinction, Ruff exception, hosted data, paid service, runtime/signing and incomplete QA visible |

Source-adjacent matrix citations and 11 dated source entries retained; competitor official sources were not pointlessly refetched. Their original check dates remain October 21–22, not invented retrieval timestamps. No benchmarks, savings numbers, tests or absence claims invented. MangoDisk is distinct, with no verified alias; no skip record warranted. Peer alternatives research is outside this head-to-head job.

## Route B assets and provenance

1. `decision.svg`: original authored editorial decision aid, created for this task October 22. Not app UI, a redraw of competitor UI, screenshot, measurement or test. Text derives from C06/C08 and B02. On-page caption cites Deep Cleanup, AI guide and Breathing Room README. Accessible title/description, descriptive image alt, fixed pale background/dark text for theme-independent contrast; vertical layout. Actual narrow-screen legibility remains pending. No third-party imagery or copied screenshot elements. No vendor-image permission inferred.
2. `space-preview-2026-10-21.png`: byte-identical copy from app `docs/content/assets/breathing-room/space-preview-2026-10-21.png`, manifest ID `current-space-browser-preview`; 2940 × 3468, original capture `2026-10-21T19:06:45.416416+00:00`, source commit `54828ac3170b45861aee70861dd0b9c658ed7e51`. No edits. Original image opened/read in this task: example banner visible, categories/chart/list visible, floating composer overlaps chart as in original. Reuse basis: owner-requested first-party example UI capture, not blanket third-party marks clearance. Caption states source/browser/example scope and no native scan, activity measurement or cleanup result. Library privacy review says built-in example names/paths only; page-level independent review remains pending.

MangoDisk screenshot is **link-only**, through attributed official README, not downloaded, hotlinked or copied. External CDN rights remain unknown. October22 route B supersedes the old screenshot-only drafting prohibition without rewriting the research packet or granting permission. The page contains useful real/built visuals, not placeholders.

Interaction pass: implemented a read-only vertical decision diagram and end-of-page decision prompts (platform, AI role, outbound data); no scripts, filesystem access, deletion controls, or fake app demo. A forced code sample would add no value to this comparison.

## Actual validation and limitations

- Node v25 from authorized NVM path: parsed actual YAML through installed Astro dependency, validated supported fields with `astro/zod`, date ordering, 11 source URL/date records; **PASS**. Explicit review/false fields checked; this is not a generated-route exclusion test.
- Node file checks: two actual image assets with alt, top figure first, no TODO/TBD/image/internal-link placeholders, no body H1; **PASS**. One H1 is expected from shared layout; rendered H1 not checked.
- SHA-256: copied PNG matches manifest/original; both baseline snapshots match retained hashes; draft/asset hashes above computed from bytes; **PASS**.
- System `/usr/bin/python3`: SVG parsed as XML with accessible title/description; **PASS**. Earlier Homebrew Python XML attempt failed due to pyexpat/system libexpat symbol mismatch; no settings/packages changed, system Python successfully supplied this limited check.
- Attempted isolated Markdown renderer import through Astro: **FAILED**, `Cannot find module '@astrojs/markdown-remark'`. No HTML rendering success claimed. The subsequent frontmatter/asset checks passed independently.
- Read-only WebFetch: live `/comparisons/` and `/tools/` hubs returned real content. `/tools/cache-rebuild-checklist/` returned **404**, so it was deliberately omitted. Only verified live internal hubs are linked; no draft sibling links or self-link.
- Manual source-ledger review: quantitative installation/pricing/version claims map to C03/C04/B01 and capabilities; no unsupported statistical comparisons. Repeated official citations intentionally keep cells independently attributable rather than optimizing link deduplication at evidence's expense.
- Shared `pnpm check`, build and test **not run**, explicitly prohibited by this job. No native app tests or cleanup-capable commands run. No queues, shared nav/schema/tests, commits, pushes or deployment touched.

## Remaining independent review gates

Draft job complete; publication **blocked pending review**. No publication score awarded. A drafter self-score cannot substitute for the required independent ≥85/100 review.

1. Independently check current draft/asset hashes against source claims, especially hosted-AI wording conflict, pricing and source-to-release limits. Refresh volatile facts within 30 days and again if stale before publication.
2. Responsible serialized site job must run check/build/test and verify exclusion of review drafts from routes/listings/feed/sitemap. Do not weaken the publication gate for a preview.
3. Arrange isolated rendered review of this exact record: canonical `/comparisons/mangodisk/`, author/dates, Article/Breadcrumb and social metadata, body/table source links, accessibility and image loading. No renderer success inferred from schema checks.
4. Inspect actual screenshots in light/dark at approximately 390/768/1440 px: SVG text, long screenshot readability, captions, matrix overflow, link and keyboard behavior. If long image detail is insufficient, create an approved contextual crop retaining example disclosure or hand off a complementary first-party view; no fake UI.
5. Independent evidence/visual/SEO scorecard with zero blockers before any publication-field changes. Native runtime parity and signing remain unverified, not a task to solve by installing software here.
