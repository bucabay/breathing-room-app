# Four page families — October22

Implemented distinct content collections and public routes:

- `src/content/tool-profiles/<id>.md` → `/tools/<id>/`: neutral factual product profile; existing three browser utilities remain separate.
- `src/content/comparisons/<id>.md` → `/comparisons/<id>/`: direct Breathing Room-versus-product decision.
- `src/content/alternatives/<id>.md` → `/alternatives/<id>/`: several verified job-relevant replacement options.
- `src/content/blog/<workflow>.md` → `/blog/<workflow>/`: distinct workflow article. Five user-requested roundup article jobs are highest-priority drafting assignments.

Hubs/navigation/footer/sitemap now cover all four. Shared canonical/social/Article/Breadcrumb metadata and the same fail-closed publication predicate apply to every family; RSS remains blog-only. No discovery-only records or placeholder competitor profiles were published to populate empty hubs.

Validation: `pnpm check` passed (51 Astro files, zero diagnostic errors/warnings/hints); `pnpm build` passed; **44 website tests passed**. The isolated publication-build test now creates positive/negative fixtures in all four collections and independently verifies route, index, sitemap and blog-only RSS inclusion/exclusion. Normal empty-collection notices are expected until writers create records, not content errors.

Browser: used owned background tab200 on an owned preview at48771; preserved unrelated user/worker tabs. Read actual new alternatives hub and tools directory at390px/light preference, checked canonical, one H1 and no horizontal overflow from live DOM. Captured and opened both actual mobile PNGs plus both1440px/dark-preference PNGs; the existing deliberate light-only palette remains readable (no separate dark theme claimed). Evidence: `.runtime/page-family-{alternatives,tools}-{mobile,desktop}.png` and matching mobile DOM JSON. Existing tool interaction/keyboard checks remain covered by the prior foundation browser QA; no authenticated/native behavior was tested here. No deployment/push/commit.

The October22 EDITORIAL update separates a research handoff/unpublished drafting from final publication. Restricted competitor images are not copied: permitted routeB uses an original documented-workflow visual plus attributed official image/guide links. Material unsupported claims, fake app UI and unreviewed publication remain prohibited.
