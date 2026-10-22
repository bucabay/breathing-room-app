# TrashPanda workflow blog handoff

Job: `draft-blog-trashpanda`  
Prepared: 2026-10-22  
State: complete textual draft; `status: review`, `published: false`. Not independent approval or publication clearance.

## Owned outputs and hashes

| File | SHA-256 |
| --- | --- |
| `/Users/gabe/code/breathing-room/website/src/content/blog/trashpanda-mac-workflow.md` | `51efd38c02bab66fee843d9acb714de0f662aa3b5dc70eadd04fffde5fbb6526` |
| `/Users/gabe/code/breathing-room/website/public/assets/blog/trashpanda/downloads-cache-triage.svg` | `beb364eb03bfb62feae434a2d900300ef1c2d41b8e751c1025da0bf916ec0971` |
| `/Users/gabe/code/breathing-room/website/public/assets/blog/trashpanda/keep-rebuild-investigate.svg` | `1a68ed307fae8902e20c476c6c00ae689eb7ffa5e67f2b71b4b5ba260897100b` |
| `/Users/gabe/code/breathing-room/website/public/assets/blog/trashpanda/space-preview-2026-10-21.png` | `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a` |
| `/Users/gabe/code/breathing-room/website/public/assets/blog/trashpanda/provenance.json` | `70a9bda1a70bf259a416a3ecf11048639d8e82190318a56dc610fcb8712c8f03` |

Public path: `/blog/trashpanda-mac-workflow/`.

## Editorial and evidence decisions

- Reused `docs/content/competitors/trashpanda/research.json` and `.md`, the verified TrashPanda baseline in `docs/content/verification/batch-2.json`, `capabilities.md`, and `screenshots.json`. Did not refetch established source records.
- The article teaches one distinct workflow: decide whether Downloads and developer-cache candidates should be kept, rebuilt at an understood cost, or investigated. It is not a renamed profile or comparison page.
- TrashPanda is a distinct canonical product, not an alias. Its official homepage documents Xcode/npm/Docker/Homebrew cache targets, a file-and-size preview, Trash and opt-in permanent deletion; these remain vendor claims, not app tests. The official image is link-only because rights are not established. It was not copied or redrawn.
- Preserved the version conflict: Downloads calls 4.1 latest stable and lists macOS 14+, while homepage/Updates foreground 4.0. The release notes disagree on the 4.0 month (August timeline, September anniversary heading). Intel notes are attributed as vendor history, not our test. Price is stated only as the dated advertised amount and unresolved terms remain explicit.
- Breathing Room claims retain preview, Python, notarization, runtime, hosted data and source-versus-binary limits. No guaranteed safety, savings, speed, monitoring absence or unverified feature claim is made.
- Top diagram and later checklist diagram are original editorial visuals, not product UI. The actual Space PNG was copied byte-for-byte; source and copy hashes match. Its caption/alt identify the October 21 browser preview and illustrative example data, not native measurement or product-test evidence. Provenance is in the asset directory.
- The interaction pass is the usable keep/rebuild/investigate review checklist; no filesystem access, automated deletion or score is implemented.
- Existing `alternatives-handoff.md` documents several source-verified, job-relevant peers (Mole, DaisyDisk, CleanMyMac and AppCleaner) and the separate alternatives page. No relationship to TrashPanda is implied and no duplicate/skip page was created.
- Internal links point to existing `/comparisons/` and `/tools/` hubs. Public official sources are linked adjacent to substantive claims and listed with actual check dates.

## Checks performed and pending review

- Passed Python static checks: frontmatter state, title 50 characters, description 152 characters, six H2 sections, three figures, referenced local asset existence, valid provenance JSON, and copied screenshot SHA-256 equality.
- Passed `/usr/bin/xmllint --noout` for both original SVGs.
- SHA-256 values above were calculated from the actual output files.
- Not run by design: shared site `pnpm check`, build or tests; this job must not run shared site builds. No rendered HTML, draft leakage, metadata/schema output, or browser light/dark/responsive review was performed.
- Pending independent review: evidence and source freshness; visual readability/captions/context at mobile, tablet and desktop in both themes; final rendered SEO/canonical/schema and draft exclusion; authorized shared-site check/build/test sequence. Keep unpublished until those gates pass.

No app installation, cleanup, account, purchase, message, permission request, commit, push, deployment, queue/database mutation, or unrelated file change was performed.
