# MacSweep alternatives draft handoff

Task: `draft-alternatives-macsweep`. Draft review date: **2026-10-22**. Outcome: complete internal alternatives article, not publication approval. Intended public path: `/alternatives/macsweep/`; the record remains `status: review`, `published: false` and is not expected to have a live route.

## Owned outputs and SHA-256

| Actual file | SHA-256 |
| --- | --- |
| `/Users/gabe/code/breathing-room/website/src/content/alternatives/macsweep.md` | `ed5fab1f7170462e10ff147102c8e743344eea27df4a77f8c8b87e20aa30bdfc` |
| `/Users/gabe/code/breathing-room/website/public/assets/alternatives/macsweep/choose-replacement.svg` | `bd0321a61c1fb34bb25dac97395478188412b3c11e328328ad805a907eff0b82` |
| `/Users/gabe/code/breathing-room/website/public/assets/alternatives/macsweep/space-preview-2026-10-21.png` | `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a` |

This handoff and `docs/content/.runtime/draft-alternatives-macsweep.1792652084010291000.receipt.json` are the other owned outputs. The receipt identifies real files, not directories; no self-referential handoff hash is asserted here.

## Intent and evidence reuse

Search/reference comparison template, targeting owned search and extractable answers. This page answers which replacement fits the part of MacSweep a reader actually uses: terminal developer cleanup, visual file triage, app removal or broader investigation. It isn't the Breathing Room head-to-head expanded. Four options have different limits, not four nominally equivalent cleaners. No tests, rankings, measured savings, app experience or AlternativeTo MacSweep-to-peer relationship is claimed.

Read PLAN.md, the October22 EDITORIAL update, capabilities.md, screenshots.json, MacSweep research.json/.md, and the applicable peer packets. No AGENTS.md found in checked ancestors/app root, app docs subtree or marketing website subtree. The broad initial parent-directory search timed out; targeted scoped searches and explicit ancestor checks were used instead. Loaded blog-write, blog-seo-check, blog-factcheck, browser-automation and the MailKite contract. No browser interaction or subagents were needed.

Reused verification/batch-1.json records for MacSweep, Mole and DaisyDisk, plus batch-2.json for Pearcleaner. Seven retained official baseline snapshot hashes were recomputed and matched. Original October 21 retrieval dates remain unchanged. Claim-level details come from these retained files:

| Draft passage | Evidence mapping |
| --- | --- |
| MacSweep modules, developer artifacts and pricing uncertainty | `docs/content/competitors/macsweep/research.json`: M01, M04–M09, M12; `source-excerpts.json` and baseline official snapshot. No effective annual price asserted. |
| Mole CLI functions, GPL-3.0, macOS 12+, architectures and permanent/Trash distinctions | `docs/content/competitors/mole/research.json`: CLI licence/platform/deletion/purge claims; `sources/cli-README.md`, retained revision `84dc779dc651ff1f0509a2054b6e25b8fb5d2ac5`, especially lines 19–32, 63–70, 146–153. Native-app proprietary/paid/macOS 14+ boundary uses separate native claims. |
| DaisyDisk map, removal, OS, edition and licence boundaries | `docs/content/competitors/daisydisk/research.json`: D1–D8 and source excerpts. Current 10.13+ offer distinguished from older guide; dollar symbol is not relabeled USD; major-upgrade charges and restricted email-key trial retained. |
| Pearcleaner targeted uninstall/orphan search, pause, licence, permission and unknown controls | `docs/content/competitors/pearcleaner/research.json`: P01–P03, P05–P09, P11. Maintenance hold is prominently disclosed; source-available is not called unrestricted open source. |
| Breathing Room source behavior and limits | `docs/content/capabilities.md`; MacSweep BR01–BR03; Pearcleaner B01–B06. Preview, Python, signing, native-validation gaps, hosted data, recurring optional AI Care and Ruff approval exception remain explicit. |

MacSweep's canonical identity is supported; no verified alias requires a skip. Old screenshot-only drafting blockers are retained in research, not edited away. October22 route B authorizes this draft without copying competitor imagery. The annual-price conflict is not resolved: the article names the conflict without asserting an effective price or price superiority. Unknown confirmation, monitoring, licence and runtime facts are not negative feature cells.

## Route-B visual provenance and interaction pass

1. **`choose-replacement.svg`**, 480 × 790: original worker-authored stacked editorial decision diagram, created for this page from the claim mapping above. No competitor pixels, logos, app chrome or generated fake UI. It illustrates task fit, platform boundaries and documented removal/maintenance limits, not observed app behavior. On-page alt and caption identify its nature and limitations. Dark fixed background/light text; actual responsive/theme inspection is pending. Credit: Breathing Room editorial. Original and final SVG bytes are the file hashed above; no external imagery licence is inferred. No private data.
2. **`space-preview-2026-10-21.png`**, 2940 × 3468: unchanged copy of `docs/content/assets/breathing-room/space-preview-2026-10-21.png`; original and copied hashes match the screenshot manifest. Actual pixels opened and read in this task: visible Interactive preview/example-data banner, example storage chart/category list, and overlapping composer. Capture date `2026-10-21T19:06:45.416416+00:00`, source revision `54828ac3170b45861aee70861dd0b9c658ed7e51`. First-party app-owner-requested capture; third-party marks retain their ownership, with no endorsement or blanket trademark licence inferred. No edits/crop/redactions. Manifest privacy review says built-in example data only. On-page caption preserves the full disclosure, not native measurements or latest-release parity. A full-size asset link is provided; narrow-screen readability still needs independent review.

MacSweep's actual interface remains an attributed text link to the official English page. Its screenshot isn't downloaded, embedded, hotlinked, redrawn or assumed MIT-licensed. Link-only rights status remains unchanged.

Interaction pass completed inline: the task-selection diagram and closing exact-target/method/retained-data/backup/rebuild-cost checklist supply a non-mutating decision aid. No forced code sample, scan, cleanup button, savings calculator or filesystem access is appropriate for this intent.

## Actual validation results

- **PASS:** final `/usr/bin/python3` structural checks: review/unpublished flags; October22 date and updated; top figure; two figures with alt/captions; no duplicate Markdown H1 or skipped heading levels; no TODO/citation/internal-link placeholders; all referenced local assets exist; SVG parses as XML.
- **PASS:** seven official baseline snapshot SHA-256 checks; copied first-party PNG matches manifest SHA-256. Final three output hashes recorded above.
- **PASS:** Node v25.0.0 parsed frontmatter using Astro's installed YAML dependency and validated it against a mirrored current `src/content.config.ts` Zod schema: 16 valid sources, date ordering and draft flags. Title 53 characters; description 156. The check does not invoke Astro's content loader or prove route exclusion at runtime.
- **PASS (source-level SEO/evidence):** title and replacement intent are specific; description is not repeated in the body; sequential H2s, adjacent official citations, disclosed affiliation and bounded peer recommendations. No artificial FAQ/review schema or unsupported statistics. Peer facts checked against retained ledgers, not a fresh full web crawl. Natural language takes precedence over generic power-word/statistics quotas.
- **PASS:** live WebFetch reads of `https://breathing-room.chatic.ai/comparisons/` and `/tools/` returned the actual hub bodies. These are the only internal prose links. `/alternatives/` and `/tools/cache-rebuild-checklist/` returned 404 and were omitted. Draft competitor records are not linked as public routes.
- **FAILED attempt, recovered:** default Homebrew Python's XML parser failed to load `pyexpat` due to a macOS libexpat symbol mismatch. The same structural/XML/hash checks passed with `/usr/bin/python3`; no runtime installation or settings changes.
- **PARTIAL attempt:** Node YAML/schema validation passed, then optional isolated Markdown rendering failed because `@astrojs/markdown-remark` wasn't resolvable from installed Astro. No rendered HTML or visual pass is claimed. No packages installed.
- **NOT RUN, as instructed:** shared `pnpm check`, build and tests, shared route/schema/nav edits, browser preview, publication or deployment. No queue/database state changed. No purchases, accounts, messages, credentials, cleanup, commits, pushes or subagents.

## Remaining independent review gates

The drafting job is complete; publication is **not approved**. No numerical quality score or independent sign-off is awarded by the drafter.

1. Independent factual/editorial review of this exact article/assets, including reasonable replacement relevance, all price/licence/platform boundaries and the retained source conflicts. Refresh volatile source offers within 30 days and before publication if stale; don't silently resolve MacSweep's annual promotion.
2. Serialized site owner must run check → build → tests and inspect canonical `/alternatives/macsweep/`, author/update dates, Article/Breadcrumb/social metadata and fail-closed draft exclusion from routes, listings, feeds and sitemap. No draft should become public merely to obtain a preview.
3. Arrange an isolated authorized review fixture. Inspect the actual page at about 390/768/1440 px in light/dark themes: diagram label fit, caption contrast, full PNG detail and full-size link accessibility. If the tall example preview is unreadable, produce an appropriately documented contextual crop that preserves its disclosure, or arrange a better permitted capture; do not relabel this capture or fabricate UI.
4. Complete publication-specific visual/privacy/rights context review and independent >=85/100 itemized editorial score with zero blockers. Any changes require new hashes and relevant delta checks.

Unrelated work in both repositories was preserved. Only the requested record, its asset files, this handoff and the designated receipt were written.
