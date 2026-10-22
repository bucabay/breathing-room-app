# Quitty workflow blog handoff

Task: `draft-blog-quitty`. Drafting complete October 22, 2026; publication approval remains pending. Intended public path after independent approval: `/blog/quitty-mac-workflow/`. The article is a no-action workflow for inspecting a busy Mac app before choosing process termination; it is not the Quitty profile, head-to-head comparison, or alternatives guide.

## Owned outputs and hashes

Marketing root: `/Users/gabe/code/breathing-room/website`.

| File | SHA-256 |
| --- | --- |
| `src/content/blog/quitty-mac-workflow.md` | `a5a0e8cc447d7b4edd9269df82ff986082151c40d3a0c8dd85fcad4dd2a7f7f8` |
| `public/assets/blog/quitty/inspect-before-terminating.svg` | `fafec8f5dee75c8b5d61fa96971711418d1f80e7bbfd532c72c2828d2e8f7dd1` |
| `public/assets/blog/quitty/apps-preview-2026-10-21.png` | `6bacc46187202835a29e24458383056e9cd55197bd53b0df2592e68c03c741d3` |

The PNG is byte-identical to `docs/content/assets/breathing-room/apps-preview-2026-10-21.png`, retained as `current-apps-browser-preview` in `screenshots.json`. It was copied without crop or edit. Its capture is a current-source browser preview with example data, not a native scan or measured result. The SVG is original editorial artwork, not app UI; it contains a no-action review sequence and no app-specific interface imitation.

## Evidence carried forward and content boundaries

Read `PLAN.md`, the October22 update in `EDITORIAL.md`, `capabilities.md`, `screenshots.json`, Quitty `research.json/.md`, the existing comparison/tool/alternatives handoffs, the website publishing contract, schema and route patterns, and the blog authoring/SEO skill instructions. No applicable `AGENTS.md` was found under either scoped repository. No subagents, new research fetches, app tests or browser automation were used.

The old `draftingAllowed: false` is treated as the historical research hold under the October22 policy. Existing retained official identity and substantive descriptions support this bounded draft; the old blockers remain unresolved rather than being reframed as clearance. Reused research claims:

- Quitty identity/discovery and advertised scope: Q01–Q12. Its site describes a RAM booster that terminates processes, but the criteria, prompts, graceful/forced behavior, and results are unknown. This is vendor-described mechanism, not advice or a benchmark.
- Availability conflict: Q13–Q14. The official homepage remained reachable while its linked repository and release API returned 404 in the October 21 checks. No claim of discontinuation, current installer, binary OS/CPU support, or version is made.
- Offer/license/install: Q03–Q05 and Q15. Free/open-source is attributed advertising; specific license is not verified despite AlternativeTo's MIT label. Xcode 14+/macOS 14.6+ are source-build requirements only. Gatekeeper warning is attributed; no bypass instructions or binary inspection.
- Breathing Room: BR01–BR03 and `capabilities.md`. Grouped app/helper sampling is source-level evidence, not binary parity or complete attribution. Preview/runtime, signing/notarization, Python, hosted AI/data, and paid AI Care limits are stated. No product is called safe, faster, or a verified replacement.
- Alternative peers: the existing `alternatives-handoff.md` records packet-backed review of CleanMyMac, Mole, DaisyDisk, Pearcleaner and Breathing Room for a distinct replacement intent. This workflow post does not manufacture peer relationships or repeat that guide. Alias ledger shows no verified Quitty alias; therefore no `blog-skip.md` is warranted.

Source-adjacent citations are used throughout; the bottom notes preserve source names, URLs, and original check dates. The discovery listing is explicitly not treated as feature or license proof. No material uncertainty is filled with inference.

## Visual and interaction pass

- Top visual: original 720×900 SVG decision aid. Caption and alt identify it as editorial guidance, not Quitty UI or a test. Supports the process-inspection-versus-intervention distinction.
- Later visual: first-party Breathing Room Apps browser preview copied unchanged. The visible example-data and no-change banner remains present. Caption gives capture date, source commit, example-data/non-native limits, and composer overlap. UI buttons are present in the authentic source screenshot, but article text does not invite their use or claim native testing.
- Interaction: a four-step no-action checklist is the relevant decision aid. No widget, process controls, filesystem access, fabricated values, or executable cleanup instructions were added.

## Validation and pending gates

- **PASS:** read-only source-level Python assertions for review/false draft metadata, seven checked source records, workflow content, no placeholders, known internal route source files, and existence of each referenced asset. Title length 56 characters; description length 156 after final edit. Final SHA-256 values are listed above.
- **PASS:** `/usr/bin/python3` ElementTree parsed the SVG; accessible `<title>` and `<desc>` exist; no script element.
- **PASS:** opened and inspected the copied PNG; screenshot inventory digest equals the copied asset digest.
- **Attempted, unavailable:** Node/YAML parsing could not run because the marketing checkout has no installed `yaml`/`js-yaml` package; no package was installed. Source-level checks are not a full Astro schema validation.
- **Not run by instruction:** shared `pnpm check`, build and tests; no local preview or 390/768/1440 light/dark browser captures. No external pages were refetched. No independent score, rendered visual approval, live URL check, or publication approval is claimed.

Independent review should inspect exact source passages and final hashes; verify rendering, draft exclusion, canonical/social/schema metadata and routes in an authorized serialized site check; inspect the visuals responsively; and preserve all release, licensing, install, and feature-behavior unknowns. Do not publish unless the programme's independent evidence/visual/SEO gates pass.
