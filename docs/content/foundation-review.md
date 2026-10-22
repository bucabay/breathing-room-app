# Foundation review — 2026-10-21

Task: `foundation-review`. **Infrastructure QA complete locally.** The browser follow-up on 2026-10-21 passes; see `foundation-browser-QA.md` and `.runtime/foundation-browser.receipt.json`. The earlier blocked run below is retained as history. Nothing was deployed, committed or pushed. This is not article publication approval.

## Scope and inspection

Read `PLAN.md`, `EDITORIAL.md`, `foundation-handoff.md`, the adapted MailKite contract and website publishing documentation. Loaded `blog-seo-check`, `browser-automation` and `wrangler` (the website check invokes local type generation). No applicable `AGENTS.md` was found in the parent paths, app documentation tree or website tree. No agents were spawned.

The website already had working static resource routes, a shared layout, two calculators, source records, authorship/dates, article/breadcrumb schema, canonical/social metadata, RSS, sitemap and footer navigation. These were extended, not replaced. `/comparisons/` remains the combined comparisons/alternatives hub. No `/compare/` routes or duplicate alternatives directory were created.

The marketing repository was clean at the initial status check. Unrelated app work, including `docs/content/screenshots.json`, was left untouched. Queue/database state and other jobs' files were not changed.

## Changes and findings

- Added `/tools/cache-rebuild-checklist/` in the existing resource styles. Six explicit questions track what remains unknown for one candidate location. Completion never authorizes deletion, predicts savings or assigns a safety score. Reset and no-JavaScript explanations are included. No paths, uploads, disk reads, deletion APIs, persistence or network requests were added.
- Retained the headroom planner and GB/GiB converter. The planner already discloses its formula, chosen-target assumption and distinction from measured savings. Added runtime rejection of unsupported conversion units.
- Added `src/lib/tools.ts` as the shared tool directory/sitemap registry; linked the checklist from the planner. Existing footer resource navigation was already sufficient and was preserved.
- Strengthened metadata validation: nonblank titles/descriptions/authors/source titles, HTTP(S) source URLs, valid ISO checked dates, and chronological updates. The shared publication gate also excludes future/invalid/reversed updates. These checks do not verify factual claims.
- Added breadcrumb schema for resource hubs and tools without duplicating article breadcrumbs. Existing article/static rendering and social metadata were preserved.
- **Retained both existing articles as `status: review`, `published: false`.** Only those two frontmatter fields changed; prose and dates were preserved. The workflow guide has no qualifying substantial visuals; the comparison has one earlier example-data preview, no required current/native and Apple UI visual pair, and no complete visual provenance/independent rendered review. Their material claims have not been independently reverified by this foundation job. Existing `published` flags were not sufficient evidence to pass the editorial gates.
- Empty hubs now explain review status. Removed public tool links into the hidden guide. The build has zero public articles and an intentionally empty blog RSS feed until review approval. No placeholder posts were published.

## Executed validation

Run in `/Users/gabe/code/breathing-room/website`, in the required order:

| Command/check | Actual result | Retained evidence (app-relative) |
| --- | --- | --- |
| `pnpm check` | Exit 0; Wrangler local types generated; Astro checked 48 files, 0 errors/warnings/hints | `docs/content/.runtime/foundation-review-check.log` |
| `pnpm build` | Exit 0; 25 static HTML pages built, plus sitemap/RSS | `docs/content/.runtime/foundation-review-build.log` |
| `pnpm test` | Exit 0; **40 passed, 0 failed**, no skips | `docs/content/.runtime/foundation-review-test.log` |
| `git diff --check` (marketing repository) | Exit 0 | Executed after final website edits |

The scheduled shell initially lacked Node/pnpm on PATH (`pnpm check` exited 127). Used the installed Node **24.18.0** and Corepack pnpm **12.14.0** through a job-local executable shim at `docs/content/.runtime/foundation-review-bin/pnpm`; no packages installed or computer settings changed. Reproduction PATH prefix: `/Users/gabe/code/breathing-room-app/docs/content/.runtime/foundation-review-bin:/Users/gabe/.nvm/versions/node/v24.18.0/bin`.

New tests exercise:

- An **isolated temporary Astro build**, not production fixtures: published positive controls and draft, review, unapproved, missing approval/status, future publication and future-update records in both collections. Assert route, hub, sitemap and RSS inclusion/exclusion independently.
- Rendered static article body, author, visible updated date, canonical, article OG type, parsed Article/BlogPosting and Breadcrumb JSON-LD. Script-closing strings and ampersands round-trip through escaped schema/RSS safely.
- Actual production exclusion of both unapproved foundation articles; no `/compare/` directory; resource links resolve; all HTML footers link resource hubs; directory tools match sitemap; no duplicate sitemap URLs.
- Arithmetic edge cases (zero/invalid/negative/nonfinite/overflow input, chosen targets, conversion round-trip and unsupported units), all checklist completion combinations relevant to missing/unknown/duplicate answers, and future/invalid/reversed update gates.
- Actual tool handler source executed with a small DOM adapter: calculation, stale-result invalidation, invalid input, checklist unchecking/completion caveat/reset. **This is not browser execution or accessibility approval.** No-JavaScript text/live regions and absence of upload/persistence/file APIs are source-checked.

The first expanded test run exposed two harness issues (fixture copy lacked the public parent billing config; VM Error constructors differed). Fixed the harness, then reran the required check/build/test sequence successfully. Temporary fixture copies and their `build.log` are retained; the latest exact path is recorded in the test log. They are outside the actual website content/dist tree. Node emits the expected experimental `stripTypeScriptTypes` warning; there are no failed tests.

## Historical browser blocker and remaining article gates

Two `chrome-devtools.list_pages` calls failed with:

> Could not connect to Chrome. Check if Chrome is running. Cause: Failed to fetch browser webSocket URL from http://127.0.0.1:9333/json/version: fetch failed

Stopped browser work after the permitted retry. No existing tabs were inspected, no tab was created and no alternate browser/profile was started. The following required checks remain **unperformed**, not inferred from source or tests:

- Actual tool use and keyboard navigation in a browser.
- Read screenshots at about 390, 768 and 1440 px, each in light and dark themes; verify text, captions, tables/overflow and focus controls.
- Independent article claim/provenance/visual review and itemized editorial scoring. No score or publication approval is awarded here; no source reachability check is represented as claim verification.

The authorized follow-up restored this gate using the already-running Chrome endpoint and an owned background tab. Both calculators and the checklist were exercised with native controls and keyboard activation; 36 responsive/preference screenshots were captured and read. Fresh check/build/test passed (40 tests). Details, limitations and current hashes are in `foundation-browser-QA.md`. Article research/visual jobs must still satisfy their separate gates before any publication flag is restored. No deployment is authorized by this report or receipt.

## Owned-file handoff

Website root: `/Users/gabe/code/breathing-room/website`. All 19 changed/added website paths and their current SHA-256 hashes are recorded in `docs/content/.runtime/foundation-review-website.sha256` (paths relative to `/Users/gabe/code/breathing-room`). They cover publishing docs, content config, the two review records, shared resource layout/publication/calculator/tool libraries, hubs/sitemap/planner/checklist, and three test files. Existing header/footer, homepage, worker, release/billing configuration and queue were not edited.

Historical app artifacts: this report; `docs/content/.runtime/foundation-review.receipt.json`; the original three check/build/test logs; the hash manifest; and the local pnpm shim. That original receipt remains `blocked` as an accurate record of its run. The current infrastructure outcome is `done` in `docs/content/.runtime/foundation-browser.receipt.json`; no queue/database state was changed by the browser follow-up.
