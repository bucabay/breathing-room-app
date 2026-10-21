# Reference implementation findings

Inspected MailKite and SendHog source, 2026-10-21. Use source as inspiration, not a dependency on those deployments.

- SendHog standalone blog: `/Users/gabe/code/sendhog/blog/src/content.config.ts`, `src/pages/index.astro`, `src/pages/[...slug].astro`, `src/lib/seo.ts`, `src/styles/prose.css`, `tests/blog.test.mjs`, `scripts/check-site.mjs`.
- Extraction map: `/Users/gabe/code/sendhog/blog/docs/architecture.md`.
- Editorial: `/Users/gabe/code/sendhog/blog/.agents/skills/sendhog-blog/SKILL.md`, `.agents/skills/sendhog-blog-review/SKILL.md`, `docs/editorial-sources.md`, `docs/publication-review.md`.
- MailKite alternatives data and generated routes: `/Users/gabe/code/mailkite/web-monorepo/website/src/data/alternatives.ts`, `src/pages/alternatives/index.astro`, `src/pages/alternatives/[slug].astro`.
- MailKite tools: same website's `src/data/tools.ts`, `src/pages/tools/index.astro`, `src/pages/tools/[slug].astro`.
- Evidence-backed calculation model: `/Users/gabe/code/sendhog/website/src/lib/pricing-comparisons.ts` and `tests/pricing-comparisons.test.ts`.

Reuse typed records, honest strengths/trade-offs, explicit unknowns, source URLs and checked dates, readable article layout, real screenshot figures, related content, accessible search/filtering and an independent publication review.

Do not copy email-specific capabilities, brand/schema identities, fake zero-dollar Offers, unimplemented submission backends, historical backdating, or future-dated posts that bypass visibility checks. Reference routes filter `!draft` but do not reliably gate future dates; explicitly implement publication-time visibility if used.
