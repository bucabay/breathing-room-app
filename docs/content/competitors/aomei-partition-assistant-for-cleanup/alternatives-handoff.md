# Alternatives draft handoff — AOMEI PartitionAssistant Cleanup

Prepared: 2026-10-22. Status: internal review draft; not publication approval.

## Owned outputs and SHA-256

Marketing repository (`/Users/gabe/code/breathing-room/website`):

| File | SHA-256 |
| --- | --- |
| `src/content/alternatives/aomei-partition-assistant-for-cleanup.md` | `6491db92ce1a64d484ce6ca43c668e93aa1bb27a8c743de154fe24d759dcee94` |
| `public/assets/alternatives/aomei-partition-assistant-for-cleanup/choose-by-job.svg` | `1de65b08ef8c61a22b379fe78f8113ef3e1559322375b5d0528b3ac07b495c17` |
| `public/assets/alternatives/aomei-partition-assistant-for-cleanup/breathing-room-space-preview-2026-10-21.png` | `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a` |

App repository:

| File | SHA-256 |
| --- | --- |
| `docs/content/competitors/aomei-partition-assistant-for-cleanup/alternatives-handoff.md` | recorded in receipt after final write |

## Evidence and distinctions

- Reused `docs/content/verification/batch-2.json` plus retained AOMEI packet `research.json`, `research.md`, and `validation.json`; did not redo baseline research. AlternativeTo is cited only for the canonical product's discovery/official destination, not as proof of peer relationships.
- Mole, DaisyDisk, and Pangalin Space Manager were selected because retained official-source packets verify distinct Mac cleanup, disk-analysis, and storage-relocation jobs. Their source packets are `docs/content/competitors/mole/research.json`, `daisydisk/research.json`, and `space-manager/research.json`.
- AOMEI is treated as Windows-oriented; no Mac edition was established. The Professional $49.95 three-year/lifetime conflict is explicitly excluded from recommendation prose. Free quotas and removal/undo semantics remain unknown.
- Breathing Room is disclosed as the publisher's product and described as a limited Mac preview. Hosted AI, runtime, Python and release-validation caveats are retained.
- Visual policy: Route B. The original SVG is a labeled editorial decision aid, not competitor UI. The first-party Space browser preview is copied byte-for-byte from the reviewed screenshot library and must keep the example-data banner/disclosure. Its original capture timestamp, commit, and hash are in `docs/content/screenshots.json`. Official competitor screenshot links may be added only as ordinary source links; no screenshot bytes were copied.

## Checks performed

- Read PLAN.md, October22 EDITORIAL.md, capabilities.md, screenshots.json, available retained verification and source packets, existing alternative-page conventions and publishing documentation.
- Confirmed the draft metadata stays `status: review`, `published: false`, dated October 22, 2026; description/lead, sources and real internal hub/tool routes are present.
- Verified local visual assets exist; copied screenshot SHA-256 matches the retained original (`9e3475d4…a5db743a`). SVG is original and self-contained.
- No app/product execution, browser capture, screenshot-permission request, competitor image download, site check/build/test, queue/database change, commit, push or deployment was performed. Shared site build/test intentionally not run under the task boundary.

## Pending independent review (blocking publication)

1. Validate Markdown/frontmatter against the site content schema; run the site's authorized `pnpm check`, `pnpm build`, then `pnpm test` in the correct order in a separately permitted validation stage.
2. Inspect built page metadata/canonical/schema/draft exclusion and all asset routes. Test the rendered article at mobile/tablet/desktop in light and dark themes; visually inspect the decision diagram and screenshot banner/crop.
3. Independently fact-check source-adjacent product claims and current volatile availability/pricing before publication. Keep AOMEI's duration conflict and all packet unknowns unresolved unless new evidence is retained.
4. Confirm all linked public routes remain live and review readability/SEO/content quality. No independent score or approval is claimed here.

Public route if later approved: `/alternatives/aomei-partition-assistant-for-cleanup/`.
