# Breathing Room content programme

## Outcome

Build a useful, searchable blog with **at least 100 individually researched posts**, a comparisons/alternatives directory, and working free tools. Reuse MailKite/SendHog's evidence-first editorial approach, adapted to Mac owners, developers, builders and creators—not email infrastructure readers.

Source repositories:
- Desktop app and programme: `/Users/gabe/code/breathing-room-app`.
- Marketing site: `/Users/gabe/code/breathing-room/website`.
- Reference implementations: `/Users/gabe/code/mailkite`, `/Users/gabe/code/sendhog`.
- Blog contract: `/Users/gabe/.agents/skills/blog/references/mailkite-dev-blog.md`.

## Ordered checklist

- [x] C01: Confirm the two published AlternativeTo relationships and save exact listing URLs, retrieval dates, and raw discovery provenance. Live listing confirms CleanMyMac and Mole; see sources.md.
- [ ] C02: Traversal and listing-URL deduplication complete: 19 pages, 113 CleanMyMac entries, 101 Mole entries, 150 competitor listing identities excluding ourselves. Official vendor-alias verification, direct/adjacent/platform classification and dead-product review remain per-item research. Never fabricate names to reach 100.
- [x] C03: Verify Breathing Room's documented/source capabilities, release and pricing boundaries; see capabilities.md. Native binary behavior is not claimed tested.
- [x] C04: Inspect MailKite/SendHog patterns; retain direct evidence-first voice, source ledgers and honest trade-offs. See reference-handoff.md and EDITORIAL.md.
- [x] C05: Build `/blog/`, `/comparisons/`, separate `/alternatives/`, and `/tools/` with individual content routes, navigation and indexable static HTML. Tools includes both free utilities and neutral tool profiles; draft visibility fails closed across all four families.
- [x] C06: Add validated content records, draft filtering, authorship, visible update dates, canonical URLs, Open Graph, Article/Breadcrumb schema, sitemap and RSS. Drafts must not leak into feeds/search. Initial check/build and 33 website tests pass; independently review before scaling.
- [x] C07: Capture a reusable current-source browser screenshot set: Space, Apps, Assistant plan review, Activity, Activity panel and Daily care, plus Home. Seven PNGs were opened and visually inspected. Example data is explicitly labeled; native menu-bar behavior and measurements remain unverified. See screenshots.json and screenshot-review.md.
- [x] C08: Materialize150 research chains with four individual page intents each (tool profile, comparison, alternatives, workflow blog), plus five roundups:605 nominal page targets and1371 execution jobs. Verified aliases/irrelevant products must be merged/skipped, not counted as distinct vendors or filler. Target >=100 real blog posts; report any verified shortfall rather than padding.
- [ ] C09: Complete a three-competitor pilot; test evidence, imagery, SEO, readability and cross-linking before scaling.
- [ ] C10: Process remaining competitors in relevance order, up to three independent jobs at once.
- [x] C11: Implement/test storage unit converter, headroom planner and cache/rebuild checklist. Actual browser keyboard/responsive checks completed; no filesystem deletion, sensitive uploads or fake measured savings.
- [ ] C12: Audit 100+ finished posts for broken links, duplicate intent, unsupported claims, missing images/alt text, mobile readability, schema and build correctness.
- [ ] C13: Assemble release-ready site and deployment checklist. No automatic production deploy or git push in scheduled jobs.
- [ ] C14: Refresh volatile pricing/availability at least every 30 days; change dateModified only after substantive review. Track indexed pages and qualified download clicks without promising rankings.

The machine queue is `queue.json`; live completion is recorded in the local SQLite database, not inferred from unchecked Markdown boxes. Run `python3 scripts/content-worker.py status` for the authoritative state. Append evidence to the appropriate checklist item when completed.

## Information architecture / search intent

| Surface | Intent | Content |
| --- | --- | --- |
| `/blog/<distinct-workflow-slug>/` | Help someone accomplish a real Mac task | One original post per competitor: an actual use case and evidence-based comparison, not a renamed template |
| `/comparisons/<competitor>/` | Breathing Room vs that product | Concise fact matrix, decision criteria, honest strengths/limitations and links to the deeper post |
| `/comparisons/` | Explore direct comparisons | Searchable Breathing Room-versus-product decision pages |
| `/alternatives/<competitor>/` | Replacement options | Several verified job-relevant options, not the head-to-head article repeated; document an exception if the intent cannot earn a useful page |
| `/tools/<competitor>/` | Understand a product | Neutral sourced identity/platform/scope/profile with official links and bounded unknowns |
| `/tools/storage-headroom/`, `/tools/storage-units/`, `/tools/cache-rebuild-checklist/` | Solve a small problem now | Working local-only utilities, separate from competitor profiles |

## Per-competitor definition of done

1. Research packet: official product/docs/pricing/platform URLs, dated factual claims and the AlternativeTo discovery edge. A directory is discovery evidence, not proof a feature exists or is absent.
2. Compare macOS compatibility, licence, local vs hosted operation, scan/cleanup model, approval controls, process/helper grouping, recurring-growth monitoring, developer caches, pricing and installation caveats where relevant. Unknown is **not verified**, never “No”. Do not call an adjacent product a direct substitute.
3. Explain when Breathing Room fits and when the competitor is the better choice. Disclose “we build Breathing Room”. No “best”, performance, safety or savings claims without supporting evidence and conditions.
4. Use useful real/built visuals under the October22 EDITORIAL routeA/B policy. Prefer a labeled Breathing Room view plus a permitted competitor app screenshot. If screenshot reuse is restricted/unclear, use an original source-backed workflow/decision diagram and an attributed official image/guide link instead; explicitly identify it as a diagram, never fake app UI. Keep captions, alt text, source/provenance and rights records. Missing screenshot permission does not prevent source-backed internal drafting or the approved fallback, but never permits copying restricted imagery.
5. State preview/notarization, Python/runtime, sign-in/hosted-agent and feature/pricing limitations accurately. The app README is the starting evidence, not a perpetual source of current truth.
6. Write the conclusion first, then specifics. The description is the introduction; do not repeat it in the body. Plain language, short paragraphs, descriptive headings, no marketing filler. Length earned, typically 900–1,800 words for a substantive comparison post; do not pad.
7. One unique primary intent/title/meta, contextual internal links to hub/comparison/tool, source links next to claims, author and reviewed date. Use schema only for visible content; no fabricated reviews, stars or FAQ questions.
8. Load `blog-write`, `blog-seo-check` and `blog-factcheck` for drafting/QA as applicable, plus the MailKite contract. Adapt its software/code-demo requirements only to runnable tutorials—not arbitrary comparison articles. Run an interaction pass; a decision aid can be more useful than a forced code sample.
9. Review content quality (30), SEO (25), evidence (15), technical (15), citation readiness (15). Require >=85/100 and zero blocking evidence, screenshot, privacy or technical failures. A score is a documented review, not automatically awarded.
10. Build/test the changed site. Keep content draft until review passes. “Done” is not “deployed”. Record output paths and validation results in a job receipt.

## Scheduling and safety

LaunchAgent runs a watchdog every **600 seconds** while this Mac is awake and the user is logged in. It maintains **three persistent worker slots**; each immediately claims its next ready comparison task after completion. Dependent stages wait for validated receipts. Shared site builds are serialized by a resource lock. It does not promise one finished article every ten minutes. CLI stream failures/45-minute timeouts quarantine the slot as uncertain until its terminal receipt is reconciled, rather than duplicating a potentially live server agent. Blocked jobs are not silently retried forever.

Shared site foundation, manifest expansion and publication work are serialized through dependencies. Parallel competitor jobs own separate competitor directories/files; they must not edit shared navigation, index files, queue or other workers' output. Public browser automation must load its browser skill and use owned tabs. Do not run desktop cleanup or purchase subscriptions for research. No account creation, competitor sign-ins, credentials extraction, emails, pushes or deployments without separate authorization.

Controls and exact installation state are described in `AUTOMATION.md`. Runtime logs/receipts remain local under `.runtime/`. Infrastructure completion is checked separately from finished article count.

## Five requested roundup articles

- [ ] Top10 Mac cleaners in2026: choose by workflow (`top-10-mac-cleaners-2026`).
- [ ] 7 free Mac cleanup options in2026 (`free-mac-cleaners-2026`).
- [ ] 8 disk-space analyzers for Mac in2026 (`mac-disk-space-analyzers-2026`).
- [ ] 7 Mac cleanup tools for developers in2026 (`mac-cleanup-tools-developers-2026`).
- [ ] 7 open-source Mac maintenance tools in2026 (`open-source-mac-cleaners-2026`).

These are distinct source-backed editorial shortlists, not invented benchmark rankings. Counts must match verified included options. Drafting is highest priority; independent claim/visual/rendered review precedes publication. Publication and deployment are separate states.
