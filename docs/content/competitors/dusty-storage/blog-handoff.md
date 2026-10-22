# Dusty Storage workflow blog handoff

Task: `draft-blog-dusty-storage` · drafted 2026-10-22 · status: **review, unpublished**

## Owned output

- Article: `/Users/gabe/code/breathing-room/website/src/content/blog/dusty-storage-mac-workflow.md`
- Public intent: `/blog/dusty-storage-mac-workflow/`
- Visuals: `/Users/gabe/code/breathing-room/website/public/assets/blog/dusty-storage/backup-decision.svg`, `offload-review.svg`, and `space-preview-2026-10-21.png`.
- SHA-256: article `cb3ad30ba95d7e68d74f5e4bab3871ef65f792ce892a70cd9475c453ba7b32ca`; backup decision SVG `b4cd37e9b8f8d5d6cb712c82efdb40145e30aff0671ea7d5740271066bc4221b`; offload review SVG `70f56dd48f4a1d51b0e94d7800d898e4cd52350ac40e1f93f73442764027bbe5`; Space PNG `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a`.

## Editorial decision

The article teaches a distinct preservation decision: whether and how to evaluate offloading a phone backup intended for future use. It is not a generic cleaner comparison, profile rewrite, or restore tutorial. It follows the source packet’s proposed workflow and explicitly leaves backup integrity, destination behavior, successful migration, and restore execution unverified. Dusty is domain-qualified; the AlternativeTo listing is used only as discovery provenance, and its subscription-price statement is explicitly contrasted with the retained official one-time offer.

Competitor UI remains link-only because the all-rights-reserved footer does not establish republication rights. Route B is used accurately: the two original SVGs are decision aids based on documented workflow, not Dusty UI or test output; the official feature guide is linked. The retained first-party Space preview is included with its example-data, browser-only, and non-native limitations. It does not imply backup functionality.

## Checks performed

- Read `PLAN.md`, October 22 `EDITORIAL.md`, `capabilities.md`, `screenshots.json`, the full Dusty research packet and validation record, existing Dusty comparison/profile records, site publishing contract/schema, and the applicable blog-write, SEO-check, factcheck, browser, and MailKite reference instructions. No applicable `AGENTS.md` found in either scoped repository.
- Reused the retained verification baseline, discovery record, alias decision, capabilities register and screenshot inventory; no redundant source refetch or browser visit was made.
- Confirmed the copied Space PNG SHA-256 matches the inventory’s original hash.
- Ran `shasum -a 256` for article and assets; hashes above are actual outputs.
- Checked inline external/internal references and source-adjacent citations by reading the complete article. Internal links point only to the existing comparisons hub and storage-headroom utility.
- Attempted Python XML parsing of the SVG assets; **not run successfully** because the installed Python 3.14 `pyexpat` failed to load the system expat symbol (`_XML_SetAllocTrackerActivationThreshold`). This is an environment limitation, not a successful SVG validation.
- No shared site check/build/test was run, as instructed. No browser rendering or viewport checks were run.

## Required before publication

1. Independently validate the article’s claim-to-source mapping and refresh volatile product availability/terms as needed; review the retained privacy-source conflict and ensure it remains represented accurately.
2. Validate both SVG files with a working XML/SVG parser and inspect readability, contrast, and responsive rendering. Verify the copied PNG renders and its disclosure is visible in context.
3. Run the site’s required `pnpm check`, build, and tests in the authorized review stage; inspect the rendered HTML, metadata, canonical, draft exclusion, and responsive browser output. Do not change this draft to published without independent approval.
4. Consider expanding only if authoritative Apple backup-management/restore sources and version-specific Dusty workflow evidence are separately verified; the current article intentionally does not give step-by-step migration instructions.

No competitor image was downloaded/copied, no permission request was sent, and no purchase, account, message, cleanup, install, commit, push, deployment, queue mutation, or shared navigation/schema/test edit was performed. Existing unrelated work was preserved.
