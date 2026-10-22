# AppZapper workflow blog handoff

Task: `draft-blog-appzapper` · **Draft complete; publication remains blocked pending independent review.** Prepared October 22, 2026.

## Owned output

Marketing root: `/Users/gabe/code/breathing-room/website`.

| Real file | SHA-256 |
| --- | --- |
| `/Users/gabe/code/breathing-room/website/src/content/blog/appzapper-mac-workflow.md` | `392cf8096d4ee4a7ab7b8e5f98814c75627e922b834eb40fc5ad697fa541a852` |
| `/Users/gabe/code/breathing-room/website/public/assets/blog/appzapper/uninstall-or-investigate.svg` | `44a1616b4135fd7248094790a559a15505d9c9e544e1b8eee4716c284fec10c9` |
| `/Users/gabe/code/breathing-room/website/public/assets/blog/appzapper/space-preview-2026-10-21.png` | `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a` |

This is the canonical `appzapper` workflow record; AppZapper 3000 is the same brand lineage, not a second article. No alias duplicate or extra blog-skip record was created. No queue/database state changed.

## Intent and evidence decisions

The article teaches one concrete decision workflow: distinguish removing a known unwanted app from investigating ongoing storage growth when the app must remain. It is not the AppZapper profile, comparison matrix, or alternatives list expanded into prose. It avoids deletion instructions and pauses on unclear purpose or recovery. It is a source-based guide, not a hands-on test.

Reused `research.json` / `research.md`, batch-1 verification, retained official snapshot, `capabilities.md`, and `screenshots.json`; no broad refetch or app test. The official identity and substantive claims are supported by AZ01–AZ06. Vendor-described drag/drop, associated-file search, one-click/Zap All, version 1.0.1, macOS 15.6+, and three-zap trial are attributed, not presented as tested completeness, safety, speed, or compatibility. The offer paragraph maps to AZ04 and retained buy-page excerpts: $18/1 Mac, $29/up to 5, $99/up to 25, with USD metadata. Checkout, tax, refund, activation, and upgrade rights remain unknown. The AlternativeTo snapshot is used for discovery only, not product capability evidence.

Breathing Room claims reuse BR01–BR04 and the capability register. The article distinguishes source implementation from release behavior; includes the preview, Python, signing, Intel/clean-machine, hosted-data, and paid-AI limitations; and does not claim full AppZapper parity. The $5/month and $50/year offer is dated October 21, 2026. No privacy audit, benchmark, recovered-space result, app execution, cleanup, or purchase is claimed. Existing source conflicts and unknowns remain in `research.json`; they were not edited or silently resolved.

The alternative-page question has already been handled separately: `alternatives-handoff.md` documents a distinct multi-option replacement intent and evidence for AppCleaner, Nektony App Cleaner & Uninstaller, Pangalin Uninstaller, and Pearcleaner, with caveats/conflicts retained and no fabricated AlternativeTo relationships. This workflow article does not repeat that page or link to an unverified relationship. Existing canonical `/comparisons/` and `/tools/` hubs are the only internal destinations used.

## Visuals and provenance

The first visual is an original vertical editorial SVG decision aid, not competitor UI. It reflects the documented-vs-investigated distinction and is explicitly captioned as neither a test nor permission to delete. It contains no AppZapper screenshot, copied logo, third-party UI, or invented measurement. Its visual/mobile and light/dark legibility review is still pending.

The second visual is an unchanged copy of the screenshot inventory asset `current-space-browser-preview`, source `docs/content/assets/breathing-room/space-preview-2026-10-21.png`, 2940×3468, capture `2026-10-21T19:06:45.416416+00:00`, source commit `54828ac3170b45861aee70861dd0b9c658ed7e51`. Source and published PNG SHA-256 match. It is a first-party browser preview with illustrative example data, not a native scan, measured activity, or current distributed-binary test. The inventory's first-party reuse basis/privacy review is reused; the caption and alt text disclose example data and the image’s floating-composer overlap. No crop or edits. Target-page visual review remains pending.

The AppZapper step-2 official image remains link-only; no bytes were downloaded, embedded, or hotlinked and no permission request was sent. Route B is the approved alternative. The article has a substantive original diagram plus an attributed official-site citation, not a bare-link visual workaround.

Interaction pass: the article includes a practical four-branch decision checklist and a visual decision aid. No JavaScript, scanner, upload, cleanup control, or fabricated UI was added.

## Validation actually performed

- `node --version`: Node v25.0.0 available. A targeted YAML import attempt did not run because the marketing project has no resolvable `yaml` package from the workspace root; no install was attempted. Standard-library Ruby YAML parsing and frontmatter assertions then **passed**: six HTTPS source records, current draft fields/date, nonempty author/title/description.
- `/usr/bin/python3` parsed the authored SVG as XML: **PASS**.
- `sha256sum` on original and copied Breathing Room PNG: **PASS**, identical hash `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a`.
- `wc -w` reports 1,476 whitespace-separated words including frontmatter/markup. Title length 59 characters; description 150 characters. Scan for TODO/PLACEHOLDER/INTERNAL-LINK/lorem tokens: **PASS**, none found.
- `git diff --check` on owned marketing paths: **PASS** (new untracked content is not covered by Git's diff check); working-tree status confirms only the intended article and asset directory were created in the marketing repository for this job.
- No shared website check/build/test, route rendering, browser preview, visual viewport/theme review, or independent fact-check was run. Shared builds are explicitly prohibited by the task. No claims of those gates passing.

## Remaining independent gates

1. Independently compare exact draft/asset hashes to the retained claim ledger; recheck mutable offer and availability before publication if stale (source check date October 21, 2026).
2. Review the article and both visuals in an isolated site rendering at about 390, 768, and 1440 px in light and dark themes; inspect captions, example-data notice, diagram text, keyboard links, and image overlap.
3. In the separately authorized site-review job, run check → build → tests and inspect rendered metadata/schema, canonical, body links, and draft exclusion from route/index/feed/sitemap. Do not flip review/unpublished fields to expose a preview.
4. Complete independent scorecard and claim/visual review. This handoff records drafting, not an 85-point publication pass or deployment.
