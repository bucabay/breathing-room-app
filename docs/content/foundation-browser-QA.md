# Foundation browser QA — 2026-10-21

**Foundation infrastructure: done locally. Article publication: not approved.**

## Scope and environment

Read `PLAN.md`, `EDITORIAL.md`, `AUTOMATION.md`, `foundation-review.md` and the website's `docs/content-publishing.md`. Loaded `browser-automation`; also loaded `wrangler` for the existing check/type-generation workflow. Preserved all 19 pre-existing changed/new website files. No website source correction was needed after browser inspection. No competitors, screenshot library, queue or worker database were edited. No agents were spawned; no deployment, push or commit occurred.

Chrome DevTools connected to the authorized existing profile at `http://127.0.0.1:9333`. No Chrome launch/restart was needed. Listed existing tab metadata only, created background page **15**, and used only that page for inspection, navigation, input and screenshots. Closed page 15 at completion; other sessions' tabs were untouched.

The first attempted preview port, 4323, was already occupied: Python exited with `Address already in use`, and the owned tab showed another site's 404. Did not stop or alter that server. Started a separate loopback-only static preview with `python3 -m http.server 48763 --bind 127.0.0.1 --directory dist` in `/Users/gabe/code/breathing-room/website`. All recorded QA below uses **http://127.0.0.1:48763** and the fresh production `dist/`, not an Astro development overlay or deployed site. This does not test authenticated API/service-binding behavior.

## Fresh automated validation

Executed in website root, in order, all exit 0:

| Command | Actual result | App-relative retained log |
| --- | --- | --- |
| `pnpm check` | 48 files; 0 errors, warnings or hints; local Wrangler types generated | `docs/content/.runtime/foundation-browser-check.log` |
| `pnpm build` | 25 static HTML pages, sitemap and RSS | `docs/content/.runtime/foundation-browser-build.log` |
| `pnpm test` | **40 passed**, 0 failed/skipped/cancelled | `docs/content/.runtime/foundation-browser-test.log` |
| `git diff --check` | Exit 0 | Rechecked after QA; no website edits in this follow-up |

The initial check used PATH prefix `/Users/gabe/code/breathing-room-app/docs/content/.runtime/foundation-review-bin:/Users/gabe/.nvm/versions/node/v24.18.0/bin`; installed project scripts ran build/test. No install, remote Wrangler operation or settings change. The suite includes isolated publication fixtures, actual production review-record exclusion, rendered article metadata/schema, arithmetic edge cases and actual handler-source tests. Browser observations below supplement—not replace—those 40 tests.

## Actual tool and keyboard observations

Evidence JSON files are in `docs/content/.runtime/`, prefixed `foundation-browser-`:

| Interaction | Observed result | Evidence suffix |
| --- | --- | --- |
| Headroom: capacity 500 GB, available 20 GB, target 10%; Tab from last input, Enter on button | 4.0% available; 50.00 GB chosen target; 30.00 GB gap; explicit not-safe-to-delete warning | `headroom-valid.json` |
| Change available input after calculation | Previous result replaced by instruction to calculate again; stale output not retained | `headroom-stale.json` |
| Available 600 GB with capacity 500 GB, keyboard submit | Explicit capacity/available/percentage error, no misleading calculation | `headroom-invalid.json` |
| Converter: 1000 GB; Tab through select to button, Enter | 931.3226 GiB, same bytes explanation | `units-gb.json` |
| Converter: 1 GiB, native select then keyboard submit | 1.0737 GB = 1.0000 GiB | `units-gib.json` |
| Checklist: native focus, Space/Tab across six statements | All six checked; completion explicitly **not permission to delete** | `checklist-complete.json` |
| Space to uncheck last statement | Five checked; one remaining question named; pause/leave unchanged warning | `checklist-uncheck.json` |
| Tab to Reset, Enter | Zero checked; all six questions remain | `checklist-reset.json` |
| Tab/Enter on skip link, then Tab | URL `#main`; next keyboard stop is resource link “Mac guides”, bypassing global navigation | `skip-link.json`, `skip-next.json` |

The converter tool initially rejected the automation string `GiB` because it matches the displayed option label, not its HTML value. Resnapshotted and selected the actual label `GiB (binary gibibytes)` successfully. This was an automation invocation correction, not a website defect.

All tool results were read back from the live DOM. Checklist focus outline was blue, solid 3px; calculator keyboard focus was visibly outlined in the captured result. The headroom positive/stale rerun used 390px and dark preference; initial interactions used the default desktop viewport. The six-layout matrix below covers rendering independently, not a claim that every arithmetic case was repeated in every viewport. Native required/min/max validation and formulas are additionally covered by the automated suite. No cleanup, uploads, filesystem access or account actions were performed. Browser no-JavaScript mode and screen-reader announcements were not separately exercised; static fallback/live-region markup is covered by source/build tests, not claimed as assistive-technology certification.

## Captured and read responsive matrix

For **each** route below: viewport **390×1000**, **768×1000**, **1440×1000**, DPR 1, with both `prefers-color-scheme: light` and `dark`. These are viewport emulations, not physical iPhone/iPad tests or touch/virtual-keyboard tests.

| Route | Screenshot filename prefix | Visual result |
| --- | --- | --- |
| `/blog/` | `blog` | Review-state empty message, useful links, headings and footer fit |
| `/comparisons/` | `comparisons` | Affiliation/review disclosure readable; no hidden article card |
| `/tools/` | `tools` | Three tool cards stack on narrow view; two columns at wider sizes; links readable |
| `/tools/storage-headroom/` | `storage-headroom` | Labels, input boundaries, formula, status and caveats readable; single-column narrow form |
| `/tools/storage-units/` | `storage-units` | Select label/option text and formula fit; limitations readable |
| `/tools/cache-rebuild-checklist/` | `cache-rebuild-checklist` | Long checkbox labels wrap without clipping; legend, reset, status and caveats fit |

**36 full-page PNGs were captured and explicitly opened/read**, at `docs/content/.runtime/foundation-browser/<prefix>-<390|768|1440>-<light|dark>.png`. Each has a sibling `.json` recording actual width, document scroll width, requested preference, canonical and schema; tool records also include social metadata. All 36 have document scroll width equal to viewport width: no horizontal page overflow. Titles, body text, fieldsets and footer do not overlap in the unscrolled matrix. The mobile header intentionally hides “How it works” but retains other navigation/actions. No public article table/caption/required visual pair exists to inspect because both articles correctly remain unpublished; their visual gate is **not** satisfied by these tool/hub captures.

**Theme limitation:** the existing website explicitly sets `color-scheme: light` in `src/styles/breathing-room.css`; it has no separate dark palette. Dark-preference screenshots therefore correctly remain light, with readable text and controls. Matching light/dark PNGs can be byte-identical. This is verified compatibility under both preferences, **not** a claim of an implemented dark theme. No unrequested visual redesign was introduced.

Extra read screenshots: `foundation-browser/headroom-keyboard-result.png` (valid result and visible button focus) and `foundation-browser/skip-link-viewport.png`. The former is a full-page capture taken while the native control had scrolled into view; Chrome composites the fixed header partway down that full-page image. It is not a separate initial-layout screenshot. The viewport capture confirms the fixed header remains at its intended top position. Do not interpret full-page fixed-layer compositing as new page layout or a current-native app screenshot.

## Metadata, routes and editorial boundary

Browser DOM shows production canonicals under the configured **https://breathing-room.chatic.ai/** origin, not loopback. Tools have a single H1, matching title/description and OG/Twitter metadata, social image/alt, WebApplication schema and three-level BreadcrumbList. Hubs have BreadcrumbList; current tool schema describes JavaScript requirements and free access, not measured savings. Parsed schema and browser records are retained alongside screenshots. Public Article/BlogPosting author/review/date behavior is tested using isolated synthetic articles in the automated build suite—not falsely attributed to unpublished initial articles.

Both initial Markdown records are still `status: review`, `published: false`; production routes, hubs, sitemap and RSS exclude them. Empty RSS is intentional. No claim re-verification, current-native image provenance/rights clearance, independent article score or publication approval was performed. Article gates remain pending exactly as described in `foundation-review.md`. Infrastructure can finish without overriding those gates.

## Snapshot hashes and receipt

Current website source/build SHA-256 manifest: `docs/content/.runtime/foundation-browser-website.sha256` (absolute paths, current source/config/tests/docs plus built artifacts). Evidence SHA-256 manifest: `docs/content/.runtime/foundation-browser-evidence.sha256` (all screenshots/DOM records, logs and QA documents). These hashes describe the actual local snapshot; any later edit needs relevant delta review.

Machine-readable outcome: `docs/content/.runtime/foundation-browser.receipt.json`, `jobId: foundation-review`, `status: done`. The old `foundation-review.receipt.json` remains unchanged as historical evidence of the earlier browser outage. This follow-up does not itself mutate worker outcome state; the parent dispatcher may ingest its completion evidence through the authorized workflow.
