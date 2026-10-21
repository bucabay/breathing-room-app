# Initial website foundation — 2026-10-21

Implemented locally in `/Users/gabe/code/breathing-room/website`:

- `/blog/`: sourced Mac storage guide and RSS.
- `/comparisons/`: combined comparisons/alternatives hub and a built-in macOS tools comparison. **Use `/comparisons/`, not `/compare/`, for future queue outputs.** Named-competitor articles are not yet written.
- `/tools/`: functioning client-only headroom and GB/GiB calculators.
- Shared canonical/OG/Twitter metadata and Article/Breadcrumb schema.
- Fail-closed draft/review/future-date filtering across routes, listings, RSS and sitemap.
- Existing app screenshot clearly labeled earlier example-data/browser preview, not a current native scan.
- Footer links to resource hubs.

Key files: `src/content.config.ts`, `src/lib/{content,publication,calculators}.ts`, `src/layouts/ResourceLayout.astro`, `src/content/{blog,comparisons}/`, `src/pages/{blog,comparisons,tools}/`, `docs/content-publishing.md`, `tests/resources.test.mjs`.

Worker-reported checks: Astro check 0 errors/warnings/hints; build passed; 33 website tests passed. Browser QA blocked because Chrome endpoint at `127.0.0.1:9333` was unavailable on two attempts. Do not label browser checks complete. No deployment, commit or push.

The scheduled foundation-review job should inspect and finish this existing implementation, not start over or replace unrelated changes. The two working tools satisfy initial tool delivery, but full content/visual/independent-review gates remain required for competitor articles. Route schemas and publication frontmatter are documented in the website's `docs/content-publishing.md`.
