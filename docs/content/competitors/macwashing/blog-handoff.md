# MacWashing workflow blog handoff

Task: `draft-blog-macwashing` · Draft date: **2026-10-22**. Drafting complete; publication approval remains pending.

## Owned outputs and exact hashes

| Real file | SHA-256 |
| --- | --- |
| `/Users/gabe/code/breathing-room/website/src/content/blog/macwashing-mac-workflow.md` | `8663ad0448956518692ff6d05fd4e27e68dba515da71e0fdc50429a9e1949608` |
| `/Users/gabe/code/breathing-room/website/public/assets/blog/macwashing/dependency-review.svg` | `1b5169a03ff8de166d7f945bca10a43d8185faf03344cabe0f261d008b2fd4e1` |
| `/Users/gabe/code/breathing-room/website/public/assets/blog/macwashing/breathing-room-space-preview-2026-10-21.png` | `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a` |

Public path intended: `/blog/macwashing-mac-workflow/`. Frontmatter is `status: review`, `published: false`, author `Breathing Room team`, with date and updated date October 22. It is not a public route while the draft gate remains closed. Research dates remain October 21; no evidence was backdated or refreshed by changing the article date.

## Intent, sources and alternatives decision

The article teaches one distinct task: decide whether a dependency folder in a project not opened for more than 90 days is understood and recoverable enough to consider cleanup. It uses MacWashing's documented project-age heuristic as the starting point, then adds decision value through project/environment records, local-only state, backup/rebuild access and cost, exact removal mode, and a keep/exclude outcome for unknowns. It is not a product profile, head-to-head matrix, generic cleaner roundup, package-manager tutorial, or claim that old dependencies are safe to delete.

Material MacWashing claims reuse `research.json` and `capabilities.md`: official homepage C09 establishes the named folder categories and 90-day heuristic; C07 and the retained Safety/homepage conflict establish that removal defaults must remain module-scoped and unresolved; C10 covers vendor-described scheduled cleanup; C02/C12 cover version/platform and requirements; C11 covers the vendor privacy policy. Breathing Room statements reuse BR01–BR03 and the reviewed capabilities register. The article separates source implementation and vendor policy from tested behavior, discloses affiliation, hosted AI, preview/notarization, Python and Intel/clean-machine limitations, and makes no performance, safety, coverage, or savings claim. No apps were installed or tested.

The existing alternatives record is justified; no `blog-skip.md` or duplicate alternatives page was created. Its existing `alternatives-handoff.md` retains verified, job-relevant peer evidence and official-source mapping for CleanMyMac (broader maintenance), AppCleaner (app removal), and DaisyDisk (disk mapping), alongside the MacWashing record. Those are distinct partial workflow replacements, not asserted AlternativeTo relationships or universal substitutes. The article does not manufacture peer claims or link to the unpublished alternatives/comparison records.

## Visual and interaction pass

- **`dependency-review.svg`** is a newly authored, original decision diagram: recoverability checks lead to keep/exclude when an answer is unknown. It has SVG title/description and descriptive Markdown alt/caption. It is editorial advice, not simulated application UI, a scanner, or a safety score. XML parsing passed; browser rendering/context review remains outstanding.
- **`breathing-room-space-preview-2026-10-21.png`** is a byte-identical copy of inventory asset `current-space-browser-preview`, captured from source commit `54828ac3170b45861aee70861dd0b9c658ed7e51`. The published hash matches the source inventory hash. Its caption and alt state example data and explicitly deny native scan, measured storage, cleanup result, MacWashing UI, and current-installer proof. The inventory describes visible example-data disclosure and records first-party reuse basis; article-context privacy/mark/legibility review remains pending.
- **Route B is deliberate.** The MacWashing official System Junk/Xcode image is linked through its official download page; it was not downloaded, visually inspected, copied, or hotlinked. Screenshot capture/version and redistribution permission remain unknown. The old research packet's screenshot-only drafting blocker is historical under October22 policy; rights are not waived or represented as cleared.
- The non-destructive keep/review/exclude sequence is the interaction pass. No fake scanner, cleanup action, code demo, or executable rebuild instructions were added.

## Actual validation and remaining gates

- Parsed the Markdown frontmatter with the already-installed YAML package and validated it against the marketing site's actual Zod schema expression: **PASS**. Required fields, eight dated HTTP(S) sources, and updated-date ordering passed.
- Imported the actual `src/lib/publication.ts` helper; it rejects this review/unpublished record at October 22: **PASS**.
- Checked title (50 characters), description (157), five H2s, two figures, three internal links and absence of TODO/TBD/internal-link placeholders. Internal links point only to the comparison hub and two existing tools; their source route files exist: **PASS**.
- Parsed the authored SVG as XML: **PASS** using `/usr/bin/python3`. Verified PNG signature, 2940 × 3468 dimensions and exact inventory SHA-256: **PASS**.
- `pnpm check`, shared site build and tests were **not run**, as directed. No local preview/browser screenshots were produced; the actual copied PNG was hash/dimension checked but not visually re-read in article context. A first optional validation attempt using the default Homebrew Python 3.14 failed because its `pyexpat` could not load a system libexpat symbol; the same XML check passed using existing `/usr/bin/python3`. An initial YAML lookup by the unlinked top-level package name also failed; validation then used the already-installed pnpm-store YAML module. No dependencies or system settings were changed.
- Before publication, independently fact-check the exact article/hash and evaluate visual/context rights, readability and responsive layout; refresh volatile product/release claims if needed; run the separately authorized serialized site checks/build/tests; inspect built metadata/schema and draft exclusion; and complete the independent ≥85/100 scorecard with zero blockers. No score or publication approval is awarded here.

No queue/database state, shared navigation/schema/tests, other content records, unrelated work, or source research packet was changed. No accounts, purchases, messages, cleanup, credential reads, deployments, commits, pushes, or subagents were used.
