# Clean Doctor workflow blog handoff

Task: `draft-blog-clean-doctor` · draft date **2026-10-22**.

## Outcome and ownership

Created one complete internal-review article for the canonical Clean Doctor owner: **“Clean Doctor on Mac: Sort Cache from Personal Data”**, intended path `/blog/clean-doctor-mac-workflow/`. The article teaches a distinct, non-destructive triage workflow: distinguish generated caches, apps intentionally being removed, personal originals, and unknown files; confirm purpose and recovery before an action. It is not an expanded profile, comparison matrix, or alternatives list. Current frontmatter is `status: review`, `published: false`.

Canonical identity is Apple app ID **855008026**. The same record is variously named Clean Doctor, Clean Doctor Pro, and AI Cleaner Max; no alias page is warranted. `blog-skip.md` records that decision. The existing alternatives draft separately uses documented peers DaisyDisk, AppCleaner, and CleanMyMac; this article only notes their distinct jobs and does not claim AlternativeTo relationships. No new alternatives page or alias page was created.

Only these requested outputs were authored, plus the copied preview image:

| Exact file | SHA-256 |
| --- | --- |
| `/Users/gabe/code/breathing-room/website/src/content/blog/clean-doctor-mac-workflow.md` | `16f50aa691b63376aefda6b8d1d6be23a2fbbd453b62d72c7a624c18b070f78a` |
| `/Users/gabe/code/breathing-room/website/public/assets/blog/clean-doctor/storage-triage.svg` | `00f47b345ad5f62c566043e3f0981841d4c093644a2575dfbc54abb77dab203b` |
| `/Users/gabe/code/breathing-room/website/public/assets/blog/clean-doctor/space-preview-2026-10-21.png` | `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a` |
| `/Users/gabe/code/breathing-room-app/docs/content/competitors/clean-doctor/blog-skip.md` | See final receipt (handoff self-hash also recorded there). |

This handoff is `/Users/gabe/code/breathing-room-app/docs/content/competitors/clean-doctor/blog-handoff.md`; its hash is recorded in the required receipt to avoid a self-referential value.

## Evidence and editorial choices

- Reused `research.json`, `research.md`, its retained source snapshots and hashes, `verification/batch-2.json`, `capabilities.md`, `screenshots.json`, and the peer-source work in `alternatives-handoff.md`. The existing research validator record reports **49/49** retained packet-integrity checks; it does not certify publication claims or visuals. No broad refetch was performed.
- Kept claims within the existing Clean Doctor ledger. The Mac listing advertises junk/cache cleanup, app removal, photo/video/contact/calendar tools, and a disk storage monitor. These remain vendor-described, not tested. Exact approval, Trash/recovery, hosted-versus-local AI, developer-cache adapters, and current support remain unknown. The directory's discontinued label is not resolved into either “dead” or “maintained.”
- Preserved the price disagreement: the US store snapshot lists Clean Doctor Pro at $24.99/year, $7.99/month, and $3.99/week; linked June 2020 terms say pricing starts at $7.99/week. Trial duration/eligibility, Mac entitlements, checkout totals, and current in-app quote remain unverified. No purchase or trial was attempted.
- Reused the documented Breathing Room limitations: preview 0.1.0-preview.1, macOS 13+, Python 3.10+ for inventory, not Developer ID signed/not notarized, incomplete clean-machine and physical Intel validation, and authenticated/internet-dependent hosted AI with relevant data transmission. Source implementation is not presented as runtime or distributed-binary proof. The optional automatic verified Ruff-cache Trash mode and exact saved daily approvals remain distinct; no blanket “always asks” claim is made.
- Primary claims link to source-adjacent Apple/vendor/project documents. Peer mentions use existing verified research retained for the alternatives work; they are not invented directory edges. Only the live `/comparisons/` and `/tools/` hubs are linked internally; hidden draft routes are not linked.

## Visuals and interaction pass

Route **B** is used because the official AI Cleaner Max screenshot is `link-only`: reuse rights are uncleared and the image bytes/UI were not inspected. The article links Apple's Mac listing and screenshot shelf but does not copy, hotlink, or describe unseen competitor UI.

1. `storage-triage.svg` is an original 720 × 720 decision aid authored for this article. It distinguishes four data classes and makes unknown purpose/recovery a stop condition. It is explicitly not competitor UI, a test, or a deletion instruction; title, description, HTML alt and caption are present.
2. `space-preview-2026-10-21.png` is a byte-identical copy of the existing first-party screenshot-library PNG; source and copied SHA-256 both equal `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a`. It is the October 21 current-source browser preview with example data, not a native scan, measured activity, cleanup result, or distributed-release parity. The source commit, capture date, disclosures, alt and caption are retained. No crop or image edit was made.

The top diagram is the interaction/decision pass. The article's worksheet implements the same non-destructive decision in prose; no fake scanner, app controls, calculator, filesystem interaction, or runnable demo was added.

## Validation performed

- Read `PLAN.md`, October22 `EDITORIAL.md`, `capabilities.md`, `screenshots.json`, Clean Doctor research/source records, retained verification, existing page records, and applicable site schema. No applicable `AGENTS.md` found in either scoped tree or checked ancestors.
- Ruby standard-library YAML parse: passed. Required frontmatter keys, source record shape/URLs, `status: review`, and `published: false` checked; title is 50 characters and description is 159 characters.
- Existing `/usr/bin/python3` XML parser: passed on the SVG root/title/description. Homebrew Python 3.14 XML parsing was unavailable due to the host's existing `pyexpat`/libexpat symbol mismatch; no system change was attempted.
- `sips` confirmed copied PNG dimensions **2940 × 3468**. `shasum -a 256` confirmed it is byte-identical to the source screenshot. SHA-256 recorded above for the SVG and article.
- Text review: 6 H2 sections, 2 figures/2 real asset paths, source-adjacent citations, only live internal hubs, no TODO/internal-link placeholders, no body H1, no fake FAQ/review/ranking/benchmark, and explicit no-test/source-conflict disclosures.
- Shared website `pnpm check`, `pnpm build`, and `pnpm test` were **not run**, as expressly forbidden for this job. The website's dependency resolver was not used. No rendered route, schema, draft exclusion, public link reachability, or light/dark/mobile browser appearance is claimed as checked.
- No app execution, installation, cleanup, account, purchase, message, credentials, browser recovery, commit, push, deployment, shared nav/schema/test/queue edit, or subagent use.

## Remaining review gates

Keep this draft unpublished. An independent reviewer must fact-check the exact article and asset hashes; refresh volatile listing/pricing/support details before publication and resolve no source conflict by assumption. Independently review route-B image context/reuse and actual rendered page at narrow/tablet/desktop sizes and both themes. Run the separately authorized serialized site check/build/test and inspect canonical/social/schema/draft exclusion; arrange an isolated review fixture without weakening publication gates. No score or publication approval is assigned here.
