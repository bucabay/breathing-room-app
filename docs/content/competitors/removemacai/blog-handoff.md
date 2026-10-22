# RemoveMacAI workflow blog handoff

Task: `draft-blog-removemacai` · Draft/review date: **2026-10-22** · Publication approval: **pending**.

## Outcome and ownership

- Complete article: `/Users/gabe/code/breathing-room/website/src/content/blog/removemacai-mac-workflow.md`
- Intended path: `/blog/removemacai-mac-workflow/`; frontmatter remains `status: review`, `published: false`.
- Reader job: distinguish a known Apple Intelligence/settings change from unexplained disk growth, then check feature dependencies, release scope, recovery boundaries and the measurement that matters. This is a workflow decision guide, not the profile, comparison matrix, alternatives list, installation tutorial or a tested cleanup procedure.
- Assets are individual files under `/Users/gabe/code/breathing-room/website/public/assets/blog/removemacai/`; hashes are below.
- No alias skip is warranted. The app and CLI are one canonical product; `pared` is acknowledged upstream, not a verified alias.
- A separate alternatives draft already exists at `/alternatives/removemacai/`. Its retained evidence identifies MacPilot (settings), Mole (cleanup) and Breathing Room (investigation) as job-relevant partial peers, not equivalent Apple Intelligence removers. This workflow post does not duplicate that selection page.

Read `PLAN.md`, October22 `EDITORIAL.md`, `capabilities.md`, `screenshots.json`, `AUTOMATION.md`, existing RemoveMacAI research JSON/Markdown and baseline verification. No applicable `AGENTS.md` was found in the scoped repositories or checked ancestors. Loaded `blog-write`, `blog-seo-check`, and `browser-automation`; applied project-specific editorial rules over generic blog defaults. Research was reused without refetching. No browser, product execution, subagents, purchase, account, message, cleanup, queue/database edit, shared build, commit, push or deployment was performed.

## Evidence and decisions

The retained packet's `draftGate.readyForBoundedDraft` is true with no critical blockers. The earlier screenshot-only `draftingAllowed:false` condition is superseded by October22 route B. This copy uses the official image only under the retained MIT documentation grant and includes the complete notice and third-party notices. AlternativeTo is discovery provenance only.

- **Identity/function:** baseline `docs/content/verification/batch-2.json#removemacai`; research claims `identity`, `function`. RemoveMacAI documents selective Apple Intelligence/model and setting controls; no hands-on execution is claimed.
- **Platform conflict:** claims `platform-release`, `platform-main`. v1.1.4 is bounded to documented Apple silicon/macOS 27; the separate main-branch README says macOS 26 runs and macOS 15.1+ is in testing. Older-OS release support remains unresolved.
- **Feature and background effects:** claims `feature-loss`, `background`. Named dependent features and individual updater/helper toggles are retained; no performance claim or grouped resource-monitoring inference.
- **Recovery and storage:** claims `review`, `profile`, `trash-exceptions`, `timing`. Ordinary cleanup generally uses Trash, but unavailable simulators and local Time Machine snapshots are immediately deleted. macOS model-file deletion timing is not a measured or guaranteed space recovery.
- **Breathing Room fit/limits:** `capabilities.md` and claims `br-tools`, `br-caveats`, `br-hosted`, `br-approval`. Affiliation, source/binary distinction, preview/Python/notarization/Intel limits, hosted AI authentication/internet/data boundary, and approval-mode distinctions are retained. It is not represented as an Apple Intelligence removal tool.

## Visuals and interaction

1. `removemacai-overview.webp` is the official v1.1.4 README Overview image after the rendered description. Its actual capture date/build/OS are unknown. Caption and alt text identify it as vendor illustration; the displayed 16.1 GB is not our measurement or a guarantee. Full MIT and third-party notices accompany the asset.
2. `choose-scope.svg` is an original, accessible decision diagram distinguishing documented workflow choices. It is not competitor UI, a scan or a test. Source claim IDs and limitations are in `provenance.json`.
3. `breathing-room-space.png` is the unmodified current-source browser preview from `screenshots.json`, captured 2026-10-21T19:06:45.416416Z, source commit `54828ac3170b45861aee70861dd0b9c658ed7e51`. Both caption and alt preserve that data is illustrative and not a native scan, measurement or cleanup result.

The interaction pass is a non-executing five-question checklist (goal, dependent features, exact release/platform, operation/recovery, measurement). No generated removal commands, pretend scanner, form or destructive example. These visuals and the checklist are source-level checked only; independent rendered-context review remains pending.

## Exact output hashes (SHA-256)

| Real output file | SHA-256 |
| --- | --- |
| `/Users/gabe/code/breathing-room/website/src/content/blog/removemacai-mac-workflow.md` | `61eb6a27300b618371c2611fe8a41de604dd805054928aeb15cd9e1b234cfc07` |
| `/Users/gabe/code/breathing-room/website/public/assets/blog/removemacai/removemacai-overview.webp` | `05593d2f6111898bd25395ced7228c33df8a186882f261ece3f73962d050a32b` |
| `/Users/gabe/code/breathing-room/website/public/assets/blog/removemacai/breathing-room-space.png` | `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a` |
| `/Users/gabe/code/breathing-room/website/public/assets/blog/removemacai/choose-scope.svg` | `5567f9dce7d68302c8f1a60693904a3a561b27313cc92dd5a0eca38cc2b1fd9f` |
| `/Users/gabe/code/breathing-room/website/public/assets/blog/removemacai/LICENSE-RemoveMacAI.txt` | `5c6315bfce06cc3b3d6c2eb9b044782c99756261368a1b718a44f6ef495477e7` |
| `/Users/gabe/code/breathing-room/website/public/assets/blog/removemacai/THIRD-PARTY-NOTICES.md` | `dbfcf4ef90b16a6b2531fe3f45298e027b73d68f6dd2f5ff09ce47b82e126949` |
| `/Users/gabe/code/breathing-room/website/public/assets/blog/removemacai/provenance.json` | `a4ba8145b13cbd4c8505488bacf8f8fa9a275dfba1a1cc1a989d7de303ad3baa` |

## Validation and remaining review

- PASS: `shasum -a 256` run in the marketing repository for the article and all six asset files; official image, Space preview and both notices match retained source hashes.
- PASS: opened and visually inspected the actual official Overview image; reviewed the SVG source for labels, accessible title/description, dimensions and explicit non-UI framing.
- PASS: source inspection confirms current supported frontmatter fields, review/unpublished status, current date, sequential H2s, claim-adjacent official citations, concrete workflow, described uncertainties, internal links only to the established `/comparisons/` and `/tools/` hubs, and no fabricated FAQ/schema or metrics.
- PASS: `/usr/bin/python3` structural validation confirmed the draft gate/date, seven H2 sections and no body H1, all referenced local assets exist, SVG XML/accessibility labels/viewBox parse, and required vendor/example-data limitations remain present (about 1,551 body words).
- PASS after runtime selection: the Homebrew Python's XML parser import failed because its `pyexpat` could not load the system Expat symbol; rerunning the structural check with existing `/usr/bin/python3` passed. No environment changes were made.
- NOT RUN: shared `pnpm check`, `pnpm build`, `pnpm test`, preview/rendered HTML inspection and browser checks. This scheduled job must not run shared site builds. No independent reviewer or numeric score is claimed.

Before publication, independently verify exact claims and hashes; refresh volatile facts if stale; run the authorized serialized site check/build/tests and confirm draft exclusion; inspect canonical/social/schema output and assets; and review the page at about 390/768/1440 px in light and dark themes. Confirm diagram and screenshot readability, context, rights and captions. Draft completion is not publication approval or deployment.

Required receipt: `/Users/gabe/code/breathing-room-app/docs/content/.runtime/draft-blog-removemacai.1792668802108656000.receipt.json`.
