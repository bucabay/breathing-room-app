# Comparison directory review — 2026-10-21

**Done locally. Zero public comparison records; no publication approval or deployment.**

## Changes and boundary

Website root: `/Users/gabe/code/breathing-room/website`.

- Enhanced `src/pages/comparisons/index.astro` without replacing the foundation layout, metadata, disclosure, or `publishedEntries('comparisons')` publication gate.
- Added `src/lib/comparison-directory.ts`: literal, case/Unicode-width/whitespace-normalized matching of all query words against published title + description only. No rankings, discovery feeds, API requests, storage, or manifest integration.
- Added `tests/comparison-directory.test.mjs`: four tests covering a 150-record synthetic DOM, matching edge cases, result/empty/reset behavior, focus restoration, zero-record enhancement, and built-page/schema consistency.
- Kept styles scoped to the directory and reused the existing palette, buttons, card grid and focus treatment. Search stacks on narrow screens; controls have at least 48px height.

The build still reports **0 published comparisons** with the review explanation and links to guides/tools. The search form stays hidden when no records exist. Directory-only discovery leads are not public records. No content record, competitor manifest, queue, worker/script, screenshot, foundation document, or other agent source file was edited. No new agents, install, commit, push, or deployment.

## Progressive enhancement and accessibility

Every eligible card and its destination link is rendered on the server. With JavaScript absent or failing, all published cards remain accessible; the inactive search form stays hidden, and nonempty directories have a `<noscript>` browser-Find explanation. Enhancement does not fetch or publish anything.

Search has an explicit label, named search landmark, help text and controlled-results reference. Counts use a polite atomic status region. No-match text gives recovery instructions; Reset clears the input, restores all cards and returns focus to search. Native search/reset controls and links remain keyboard-operable. Hidden cards are removed from layout and the accessibility tree, not merely faded. No custom keyboard trap or forced focus while typing.

## Automated validation

Ran in this job, with the existing foundation pnpm wrapper and Node 24.18.0 PATH prefix:

| Command | Final result | Evidence under `docs/content/.runtime/` |
| --- | --- | --- |
| `pnpm check` | 50 files; 0 errors, warnings or hints | `comparison-directory-check.log` |
| `pnpm build` | Exit 0; 25 static pages plus sitemap/RSS | `comparison-directory-build.log` |
| `pnpm test` | 44 passed; 0 failed/skipped/cancelled | `comparison-directory-test.log` |
| `git diff --check` | Exit 0 | Rechecked before handoff |

The first test run matched `data-comparison-card` inside bundled JavaScript rather than an actual article; narrowed the assertion to rendered articles. Also initialized the mock's focus flag to remove a type-check hint. Final logs above replace the intermediate failures. The existing isolated publication-build test still passes, including fail-closed draft/review/unapproved/future exclusions. No initial article was republished for testing.

## Actual browser verification

Loaded `browser-automation`; used the existing authorized Chrome DevTools profile on **127.0.0.1:9333**. Listed existing tab metadata only, then created owned background **page 31**, with explicit `pageId: 31` on every subsequent action. Used per-page `emulate`, never global window resizing. Closed only page 31 after verification.

Started this job's loopback-only Python preview on **127.0.0.1:48764**, serving a temporary copy of the built site outside the repository. `/comparisons/` was unchanged production HTML. `/fixture.html` contained 150 clearly synthetic cards inserted into that copy and the actual production bundled directory script. No fixture was added to `src/content`, `dist`, sitemap, or deployment output. Temporary preview path is recorded in `.runtime/comparison-directory-preview-path.txt`; stopped only this job's preview process when finished. Other workers' tabs and servers were untouched.

Observed and read back from the live DOM:

| Case | Result | Evidence prefix `comparison-directory-` |
| --- | --- | --- |
| Production empty page | 0 cards, correct count/review message; no dead search UI; production canonical retained | `empty-{390,768,1440}.json` |
| Fixture: `STORAGE fixture` | 75 of 150 visible, no empty message | `filter.json`, `filter-snapshot.txt` |
| Enter in search | Remained on fixture URL; no reload or submission | Filter snapshot and subsequent no-match URL |
| Fixture: `zz-no-matches-zz` | 0 of 150 visible; recovery text visible; cards compute to `display:none` | `no-match.json`, `no-match-snapshot.txt` |
| Tab from search | Reset focused, blue solid 3px outline | `keyboard.json` |
| Enter on Reset | 150 cards restored, query empty, focus back in search, reset disabled | `reset.json`, `reset-snapshot.txt` |
| Subsequent native Tab navigation | Fixture 0 link reachable | `card-keyboard.json` |
| Responsive fixture | Width equals scroll width at 390, 768, 1440; one card column on narrow, two on wider viewports | `fixture-{390,768,1440}.json` |
| Extra narrow/dark preference | 320px viewport/scroll width, 280px input; existing explicit light color scheme retained | `fixture-320-dark.json` |
| Console | No warnings or errors in the owned fixture tab | Tool result at handoff |

This is functional DOM/accessibility-tree and viewport-metric review, not screenshot review, screen-reader certification, physical-device testing or a newly implemented dark theme. JavaScript-disabled browser mode was not separately exercised; fallback behavior is covered by server-rendered markup/source and isolated handler tests. No screenshots were created or changed. The synthetic 150-card case demonstrates directory capacity, **not** 150 researched or published comparisons. Real records still require the separate editorial/evidence/publication gates.

Receipt: `docs/content/.runtime/comparison-directory.receipt.json` (`jobId: comparison-directory`, `status: done`).
