# Shiny workflow blog handoff

Task `draft-blog-shiny--mac-app` · Drafted 2026-10-22 · **Complete as an internal draft; publication review pending.**

## Owned outputs and SHA-256

| File | SHA-256 |
| --- | --- |
| `/Users/gabe/code/breathing-room/website/src/content/blog/shiny--mac-app-mac-workflow.md` | `1a4a9c00e16d5bc0aaad9b045383bd6ff83b762c9010cc908fd1606663572885` |
| `/Users/gabe/code/breathing-room/website/public/assets/blog/shiny--mac-app/memory-or-storage.svg` | `671878e264d83d77c83b1389319aeaaa4af48a62a8ec7b605fc480704b4e521f` |
| `/Users/gabe/code/breathing-room/website/public/assets/blog/shiny--mac-app/breathing-room-apps-example.png` | `6bacc46187202835a29e24458383056e9cd55197bd53b0df2592e68c03c741d3` |

Public path if independently approved: `/blog/shiny--mac-app-mac-workflow/`. The record is `status: review`, `published: false`, dated October 22, 2026. No route is available for this draft by design.

## Intent and evidence decisions

The article teaches a distinct diagnostic workflow: use Activity Monitor’s Memory Pressure, Cached Files and Swap Used to distinguish a memory concern from a full startup disk before considering Shiny’s documented Polish action. It is not a profile, a product-vs-product comparison, an alternatives list, or a generic cleaner template. It does not claim Shiny fixes disk fullness or that memory clearing improves speed.

Reused the October 21 verification baseline (`docs/content/verification/batch-2.json`), official and AlternativeTo snapshots, `research.json`/`.md`, `capabilities.md`, and `screenshots.json`. No refetch was performed. The official identity and material workflow claims are supported by retained primary sources. The homepage/terms disagreement about future major-version updates is explicitly preserved; no unqualified lifetime-major-updates claim appears. Unknown features remain out of the article. The prior alternatives handoff addresses job-relevant peers; this article does not manufacture a relationship to them or repeat that page.

## Visual and interaction record

- `memory-or-storage.svg` is a hand-authored, source-backed workflow diagram. It represents Apple’s memory diagnostic and the documented Shiny/storage decision, not Shiny UI, a test, or results. The official Shiny page/walkthrough is linked, not copied; reuse rights and actual screenshot provenance remain uncleared.
- `breathing-room-apps-example.png` is an unchanged copy of `docs/content/assets/breathing-room/apps-preview-2026-10-21.png`, inventory record `current-apps-browser-preview`. Capture: `2026-10-21T19:06:59.096850+00:00`, source commit `54828ac3170b45861aee70861dd0b9c658ed7e51`, 2940 × 4440. Copied asset hash matches inventory. Captured browser preview contains example data, not a native scan or measured result; captions retain that disclosure and note the floating assistant overlap. This is first-party preview evidence, not current binary proof.
- Interaction pass: the diagram and read-only diagnostic choices are the useful decision aid. No scanner, app control, upload, purchase, automation or deletion action is offered.

## Actual validation and remaining gates

- Ruby/Psych YAML parse and source-field/date/URL checks: **PASS**; `status: review` and `published: false`: **PASS**. Description length 158 characters; five cited sources; no TODO/TBD/internal-link placeholders; four H2 sections, two figures, approximately 1,155 body words.
- `/usr/bin/python3` ElementTree parse of the SVG: **PASS**; role and accessible title/description references present.
- SHA-256 of reused preview matches `screenshots.json` and existing alternatives-page copy: **PASS**.
- First attempted Node validation could not load `yaml` because website dependencies are not installed in this workspace. Ruby/Psych validation succeeded instead. No package installation was attempted.
- Shared `pnpm check`, `pnpm build`, `pnpm test`, live-link checks, isolated preview, and browser visual QA were **not run**; the task explicitly prohibits shared site builds. This is not publication or rendered-page approval.
- Independent factual/currentness and visual review remain pending. In particular, review the narrow-screen legibility of the tall preview and diagram; preserve example-data disclosure. Refresh volatile Shiny download, offer and terms claims before publication. Retain the Shiny update-entitlement conflict unless an authorized independent review resolves it. Check rendered canonical/social/schema and draft exclusion in a separately authorized site review.

No alternatives alias/skip record is warranted: the canonical owner is `shiny--mac-app` (not a verified alias), and the distinct alternatives work has its own existing handoff. No other competitor files, queue/database, shared navigation/schema/tests, or unrelated work were changed. No app test, browser session, install, cleanup, account, credential, purchase, message, commit, push or deployment was performed.
