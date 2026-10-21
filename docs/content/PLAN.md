# Breathing Room content programme

## Outcome

Build a useful, searchable blog with **at least 100 individually researched posts**, a comparisons/alternatives directory, and working free tools. Reuse MailKite/SendHog's evidence-first editorial approach, adapted to Mac owners, developers, builders and creators—not email infrastructure readers.

Source repositories:
- Desktop app and programme: `/Users/gabe/code/breathing-room-app`.
- Marketing site: `/Users/gabe/code/breathing-room/website`.
- Reference implementations: `/Users/gabe/code/mailkite`, `/Users/gabe/code/sendhog`.
- Blog contract: `/Users/gabe/.agents/skills/blog/references/mailkite-dev-blog.md`.

## Ordered checklist

- [ ] C01: Confirm the two published AlternativeTo relationships and save exact listing URLs, retrieval dates, and raw discovery provenance.
- [ ] C02: Traverse both seeds' alternatives (including pagination), deduplicate products by canonical identity, classify direct/adjacent/irrelevant, and record excluded/dead products. Never fabricate names to reach 100.
- [ ] C03: Verify Breathing Room's current capabilities against app code, README, release and pricing pages; separate shipped, preview, planned and paid features.
- [ ] C04: Inspect MailKite/SendHog layout, content model, comparison tables, screenshot handling and SEO; record adaptation decisions.
- [x] C05: Build `/blog/`, combined `/comparisons/` comparisons/alternatives hub, `/tools/` and individual routes, navigation and indexable static HTML. Initial foundation completed locally; no deployment or browser QA yet.
- [x] C06: Add validated content records, draft filtering, authorship, visible update dates, canonical URLs, Open Graph, Article/Breadcrumb schema, sitemap and RSS. Drafts must not leak into feeds/search. Initial check/build and 33 website tests pass; independently review before scaling.
- [ ] C07: Capture a reusable current Breathing Room screenshot set: Space, Apps, Assistant plan review, Activity, menu bar and Daily care. Label example-data views; never present them as measured outcomes.
- [ ] C08: Create the deduplicated competitor manifest and queue one research → draft → review chain per eligible product. Target >=100 distinct competitors only if discovery supports it; otherwise explicitly report the shortfall and propose genuinely distinct workflow posts to reach >=100 total blog posts.
- [ ] C09: Complete a three-competitor pilot; test evidence, imagery, SEO, readability and cross-linking before scaling.
- [ ] C10: Process remaining competitors in relevance order, up to three independent jobs at once.
- [ ] C11: Implement and test free, local-only tools (storage unit converter, cleanup planning estimator with assumptions, cache/rebuild checklist); no filesystem deletion, sensitive uploads or fake measured savings.
- [ ] C12: Audit 100+ finished posts for broken links, duplicate intent, unsupported claims, missing images/alt text, mobile readability, schema and build correctness.
- [ ] C13: Assemble release-ready site and deployment checklist. No automatic production deploy or git push in scheduled jobs.
- [ ] C14: Refresh volatile pricing/availability at least every 30 days; change dateModified only after substantive review. Track indexed pages and qualified download clicks without promising rankings.

The machine queue is `queue.json`; live completion is recorded in the local SQLite database, not inferred from unchecked Markdown boxes. Run `python3 scripts/content-worker.py status` for the authoritative state. Append evidence to the appropriate checklist item when completed.

## Information architecture / search intent

| Surface | Intent | Content |
| --- | --- | --- |
| `/blog/<distinct-workflow-slug>/` | Help someone accomplish a real Mac task | One original post per competitor: an actual use case and evidence-based comparison, not a renamed template |
| `/comparisons/<competitor>/` | Breathing Room vs that product | Concise fact matrix, decision criteria, honest strengths/limitations and links to the deeper post |
| `/comparisons/` | Explore comparisons and alternatives | Combined hub initially; expand into filterable, linked catalogue grouped by job-to-be-done once products are verified |
| `/alternatives/<competitor>/` (optional future) | Replacement options | Create only if distinct from comparison intent; otherwise use one canonical comparison, not duplicate doorway pages |
| `/tools/<tool>/` | Solve a small problem now | Tested usable client-side utility, explanation, limitations and related guides |

## Per-competitor definition of done

1. Research packet: official product/docs/pricing/platform URLs, dated factual claims and the AlternativeTo discovery edge. A directory is discovery evidence, not proof a feature exists or is absent.
2. Compare macOS compatibility, licence, local vs hosted operation, scan/cleanup model, approval controls, process/helper grouping, recurring-growth monitoring, developer caches, pricing and installation caveats where relevant. Unknown is **not verified**, never “No”. Do not call an adjacent product a direct substitute.
3. Explain when Breathing Room fits and when the competitor is the better choice. Disclose “we build Breathing Room”. No “best”, performance, safety or savings claims without supporting evidence and conditions.
4. Two useful visual elements minimum: a real Breathing Room view and a competitor app screenshot from the official site/authoritative listing (not merely a landing page). Save source URL, asset URL, capture date, caption, alt text and reuse/permission notes. No fabricated app UIs, stock photos or invented hands-on testing. If reuse rights or access are unclear, mark blocked or link the official visual; do not quietly waive the image gate.
5. State preview/notarization, Python/runtime, sign-in/hosted-agent and feature/pricing limitations accurately. The app README is the starting evidence, not a perpetual source of current truth.
6. Write the conclusion first, then specifics. The description is the introduction; do not repeat it in the body. Plain language, short paragraphs, descriptive headings, no marketing filler. Length earned, typically 900–1,800 words for a substantive comparison post; do not pad.
7. One unique primary intent/title/meta, contextual internal links to hub/comparison/tool, source links next to claims, author and reviewed date. Use schema only for visible content; no fabricated reviews, stars or FAQ questions.
8. Load `blog-write`, `blog-seo-check` and `blog-factcheck` for drafting/QA as applicable, plus the MailKite contract. Adapt its software/code-demo requirements only to runnable tutorials—not arbitrary comparison articles. Run an interaction pass; a decision aid can be more useful than a forced code sample.
9. Review content quality (30), SEO (25), evidence (15), technical (15), citation readiness (15). Require >=85/100 and zero blocking evidence, screenshot, privacy or technical failures. A score is a documented review, not automatically awarded.
10. Build/test the changed site. Keep content draft until review passes. “Done” is not “deployed”. Record output paths and validation results in a job receipt.

## Scheduling and safety

LaunchAgent runs a dispatcher every **600 seconds** while this Mac is awake and the user is logged in. The dispatcher admits at most **three** independent OpenCode sessions; dependent stages wait for receipts. It does not promise one finished article every ten minutes. Long jobs continue rather than overlap. Each invocation times out after 45 minutes; failed/interrupted jobs become blocked, not silently retried forever.

Shared site foundation, manifest expansion and publication work are serialized through dependencies. Parallel competitor jobs own separate competitor directories/files; they must not edit shared navigation, index files, queue or other workers' output. Public browser automation must load its browser skill and use owned tabs. Do not run desktop cleanup or purchase subscriptions for research. No account creation, competitor sign-ins, credentials extraction, emails, pushes or deployments without separate authorization.

Controls and exact installation state are described in `AUTOMATION.md`. Runtime logs/receipts remain local under `.runtime/`. Infrastructure completion is checked separately from finished article count.
