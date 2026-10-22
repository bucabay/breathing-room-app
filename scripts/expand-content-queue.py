#!/usr/bin/env python3
"""Build evidence → individual page draft → independent review assignments."""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "docs/content"
ROUNDUPS = [
    ("top-10-mac-cleaners-2026", "Top 10 Mac cleaners in 2026: choose by workflow", "An overall editorial shortlist of ten documented Mac cleaner/storage options. Explain scope, criteria and who each fits; not a claimed benchmark ranking. Distinguish mature commercial suites, focused tools and our non-notarized preview."),
    ("free-mac-cleaners-2026", "7 free Mac cleanup options in 2026", "Free-core/free-CLI/built-in options: identify exactly what is free versus paid, limitations and whether an account is needed. Do not call a time-limited paid trial free or source-available code unrestricted open source."),
    ("mac-disk-space-analyzers-2026", "8 disk-space analyzers for Mac in 2026", "Visual disk inspection, physical versus logical size, protected locations and deliberate removal. Choose eight actual Mac-capable tools with verified sources; distinguish viewing from cleaning and native support from community builds."),
    ("mac-cleanup-tools-developers-2026", "7 Mac cleanup tools for developers in 2026", "Developer-specific job map: rebuildable caches, project artifacts, package-manager ownership, rebuild/download costs and recurring growth. Choose seven documented tools/workflows; no cleanup commands executed or fabricated developer experience."),
    ("open-source-mac-cleaners-2026", "7 open-source Mac maintenance tools in 2026", "Licence-first shortlist: verify actual repository licence and exact CLI/native scope for seven tools. Candidate sources include Breathing Room, Mole CLI, PureMac, App Eraser, Depflush, Dusty by Toprak and Mac Sai, only if current official evidence supports inclusion. Explain why Commons-Clause/source-available projects are not unrestricted open source. Do not conflate paid native Mole with its GPL CLI."),
]
KINDS = {
    "comparison": ("comparisons", "Breathing Room versus this single product: fact matrix, honest competitor strengths, our actual advantages, explicit unknowns and when not to choose us."),
    "tool": ("tool-profiles", "Neutral sourced tool profile: official identity/links, documented job, platform and licence/price conditions only where verified. No sales pitch or unsupported rankings. This is not a new calculator or a claim we built the competitor."),
    "alternatives": ("alternatives", "Several genuinely relevant replacements for this product's job, not just Breathing Room. Use verified peers from the retained source graph/packets; explain trade-offs and platform boundaries. Do not invent an AlternativeTo relationship or clone the head-to-head body."),
    "blog": ("blog", "Teach one concrete product-related Mac workflow with original decision value; no renamed template or duplication of the profile/comparison/alternatives page."),
}


def page_ids(slug, kind):
    # Preserve original comparison-stage IDs and all existing outcome history.
    suffix = slug if kind == "comparison" else f"{kind}-{slug}"
    return f"draft-{suffix}", f"review-{suffix}"


def expand():
    path = CONTENT / "queue.json"
    queue = json.loads(path.read_text())
    products = json.loads((CONTENT / "competitors.json").read_text())["competitors"]
    old = {job["id"]: job for job in queue["jobs"]}
    known_stages = {f"research-{p['id']}" for p in products}
    for p in products:
        for kind in KINDS:
            known_stages.update(page_ids(p["id"], kind))
    for slug, _, _ in ROUNDUPS:
        known_stages.update([f"draft-roundup-{slug}", f"review-roundup-{slug}"])
    base = [job for job in queue["jobs"] if job["id"] not in known_stages and job["id"] != "content-final-audit"]
    for number in (1, 2):
        name = f"verify-batch-{number}"
        if name not in {j["id"] for j in base}:
            base.append({"id": name, "dependsOn": ["sources", "editorial"], "task": f"Complete official-source baseline batch{number}, retaining all75 verified/partial/blocked outcomes with exact sources/excerpts/dates. Existing completed setup handoff must not be duplicated."})
    foundation_id = "page-family-foundation"
    if foundation_id not in {j["id"] for j in base}:
        base.append({"id": foundation_id, "dependsOn": ["foundation-review"], "resources": ["site-build"], "priority": 0, "task": "Validate the existing four page-family collections/routes: blog, comparisons, alternatives, toolProfiles (/tools/<id>/); separate hubs/navigation/sitemap and draft/future-date exclusion. Verify tools-directory profiles do not replace free utilities. Run check/build/tests and isolated publication fixtures for all four families. Read October22 EDITORIAL update: source-backed drafts may precede rights-safe final visuals; publication still requires independent review. Own shared infrastructure and docs/content/page-family-foundation.md only; do not overwrite workers' page records or publish placeholders."})
    for job in base:
        if job["id"] == "foundation-review":
            job["resources"] = ["site-build"]
    jobs = []
    for slug, title, brief in ROUNDUPS:
        packet = f"docs/content/roundups/{slug}"
        filename = f"/Users/gabe/code/breathing-room/website/src/content/blog/{slug}.md"
        jobs.append({"id": f"draft-roundup-{slug}", "phase": "draft", "priority": 1, "dependsOn": [foundation_id, "verify-batch-1", "verify-batch-2", "screenshot-library"], "task": f"Create the user-requested complete blog article '{title}' at {filename}, not an outline. {brief} Read EDITORIAL.md October22 update and adapted blog-write/MailKite contract. Reuse verified batch facts and competitor research packets; refresh only missing material evidence from official sources. Own only this article, {packet}/ and website/public/assets/roundups/{slug}/. Write approximately1000–1800 useful words if earned, a source-backed comparison/selection table, individual selection reasoning, explicit when-not-to-use caveats, affiliation disclosure and current Breathing Room preview/hosted/Python/notarization limits. No invented tests, personal stories, statistics, awards or rankings. The title's count must equal the actual supported shortlist; do not pad with unverified tools. Current date must be actual, never backdated. Use a labeled current first-party preview and a distinct original documented-workflow/decision visual; competitor images only if cleared, otherwise official-image links plus route-B visual. Two useful visuals, not fake app UI, not decorative stock. Cite official URLs beside claims and in frontmatter. Link only live hubs/tools or verified existing public pages; no broken cross-links to drafts. Keep status:review,published:false. Record per-claim evidence, image/provenance route and publication questions in {packet}/draft-handoff.md. No shared build output, shared site files, deployments, commits, pushes or more agents. Complete draft even when a noncritical price/image permission is unknown: omit/qualify the claim or use the approved visual fallback, never invent."})
        jobs.append({"id": f"review-roundup-{slug}", "phase": "review", "priority": 30, "dependsOn": [f"draft-roundup-{slug}"], "resources": ["site-build"], "task": f"Independently review the actual article at {filename} and {packet}/ evidence. Do not create another draft or self-award a score. Verify shortlist count/intent, source-supported statements, free/paid and OSS/source-available distinctions, disclosure, useful visuals under routeA/B, alt/captions, actual images and current dates. Use blog-factcheck/SEO checks, local owned browser preview and actual check/build/tests. Review >=85/100 and zero material blockers against hashes. Publish only this record if all gates pass; otherwise retain review state and precise blockers in {packet}/review.md. No shared tests/navigation edits, git push or deploy."})
    review_ids = []
    for index, product in enumerate(products):
        slug, name = product["id"], product["name"]
        folder = f"docs/content/competitors/{slug}"
        common = f"Read EDITORIAL.md October22 update, PLAN.md, capabilities.md and screenshots.json. Product {name} ({slug}), discovery {product['listingUrl']}. Reuse baseline verification and existing {folder}/research.json/.md, including honest source conflicts and unknowns. Never invent facts, app tests, image rights or screenshot UI. No purchases/accounts/messages, cleanup, commits, pushes, deployments or subagents. "
        research_id = f"research-{slug}"
        jobs.append({"id": research_id, "phase": "research", "productId": slug, "priority": 50, "dependsOn": ["sources", "editorial", "capabilities", "expand-queue", f"verify-batch-{1 if index < 75 else 2}"], "task": common + f"Finish the retained research handoff, not a publication review. Own only {folder}/. Establish official identity, aliases/platform fit and per-claim source URLs/excerpts/dates, verified capabilities and honest unknowns. Select existing first-party preview; record permitted competitor UI or an attributed official visual/guide link plus a route-B original workflow diagram specification. Missing image permission alone must NOT block the research handoff: do not copy restricted imagery. Conflicting price or runtime facts can be excluded or qualified in a narrow draft; do not recommend unverified installations. Record verified alias/exclusion skips instead of duplicate pages. Only missing identity/substantive official evidence blocks drafting. Complete research.json and research.md with a separate list of remaining publication gates. Old packets blocked solely by images are reusable under updated policy; do not repeat completed research."})
        for order, (kind, (collection, intent)) in enumerate(KINDS.items()):
            draft_id, review_id = page_ids(slug, kind)
            review_ids.append(review_id)
            record_slug = f"{slug}-mac-workflow" if kind == "blog" else slug
            filename = f"/Users/gabe/code/breathing-room/website/src/content/{collection}/{record_slug}.md"
            public_section = "tools" if kind == "tool" else collection
            jobs.append({"id": draft_id, "phase": "draft", "pageKind": kind, "productId": slug, "priority": 10 + order, "dependsOn": [research_id, foundation_id, "screenshot-library"], "allowEvidenceBackedResearch": True, "task": common + f"Create ONE complete {kind} page at {filename}; its public path is /{public_section}/{record_slug}/. Intent: {intent} Own only this record, {folder}/{kind}-handoff.md and website/public/assets/{public_section}/{slug}/. Existing research is sufficient for a draft when official identity and substantive claims are supported, even if the old packet says draftingAllowed:false solely due to screenshot rights. Do not await a permission request or refetch everything. Keep unresolved material claims out of prose or explicitly unknown; use approved routeB visuals where competitor UI cannot be copied. Do not publish placeholders, fake UI, unsupported negative feature cells, benchmarks, or four copies of the same content. Use natural SEO title/description, conclusion-first human prose, source-adjacent citations, clear affiliation and product limits. For alternatives, verify several job-relevant peers from existing packets rather than manufacturing relationships; if a distinct page cannot be justified, record an exception/skip with evidence. For verified aliases, write {folder}/{kind}-skip.md linking the canonical owner; no duplicate page. Link only live hubs/utilities and known public records. Internal drafts status:review,published:false; current dates, no backdating. Include useful actual/built visuals with alt/captions/provenance; routeB is legitimate and must be described accurately. A complete textual draft may leave asset work in the handoff for review, but no public broken placeholders. Load applicable blog-write/SEO skills, finish the article rather than an outline, and write the handoff with exact output/hash/remaining review items. Do not run shared site builds or edit shared nav/schema/tests/queue. Receipt artifacts must name real files, not directories."})
            jobs.append({"id": review_id, "phase": "review", "pageKind": kind, "productId": slug, "priority": 40, "dependsOn": [draft_id], "resources": ["site-build"], "task": common + f"Independent review of only {filename} and its {folder}/{kind}-handoff.md. If a verified alias/intent exclusion, validate and retain a skip note, not a fake page. Otherwise verify claims, prices/platform caveats, official identity, distinct intent versus sibling records, readable prose, affiliation, source links and permitted visual routeA or routeB. Missing rights to copy one vendor screenshot is not a blocker if the documented routeB alternative is useful, original, truthful and attributed. Never waive material factual/privacy/safety failures or reproduce restricted imagery. Inspect actual assets and local owned-browser rendering at mobile/desktop, use applicable factcheck/SEO skills, record an itemized >=85/100 zero-blocker review against hashes in {folder}/{kind}-review.md. Only then set this one record to published:true,status:published and run website check/build/tests under exclusive site-build resource. If any required validation fails, leave or restore only your own publication flags, retain prose and give an actionable blocker. Do not edit shared tests/navigation/schema/other pages, push or deploy."})
    audit_deps = review_ids + [f"review-roundup-{slug}" for slug, _, _ in ROUNDUPS]
    audit = {"id": "content-final-audit", "priority": 100, "dependsOn": audit_deps, "resources": ["site-build"], "task": "Audit all four competitor page families plus five roundups. Count actual unique published pages by family, drafts, aliases/exclusions and blockers; do not equate research rows with pages. Require >=100 real blog articles including five distinct user-requested roundups or report exact shortfall. Check sources, rights-safe visual route, intent/canonical collisions, internal links, publication dates/metadata/schema, all-family sitemap and blog-only RSS, draft exclusion, actual responsive rendering and check/build/tests. Write docs/content/final-audit.md with evidence and remaining decisions. No push/deploy/commit."}
    queue["jobs"] = sorted(base + jobs + [audit], key=lambda job: job.get("priority", 0))
    spec = importlib.util.spec_from_file_location("worker", ROOT / "scripts/content-worker.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.validate_queue(queue)
    temp = path.with_suffix(".pending.json")
    temp.write_text(json.dumps(queue, indent=2, ensure_ascii=False) + "\n")
    temp.replace(path)
    print(json.dumps({"products": len(products), "competitorPageTargets": len(products) * len(KINDS), "roundupTargets": len(ROUNDUPS), "totalJobs": len(queue["jobs"])}))


if __name__ == "__main__":
    expand()
