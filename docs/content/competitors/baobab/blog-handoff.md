# Baobab Mac workflow article handoff

Task: `draft-blog-baobab` · drafted **2026-10-22** · **complete internal draft; publication review pending**.

## Owned files and exact hashes

| File | SHA-256 |
| --- | --- |
| `/Users/gabe/code/breathing-room/website/src/content/blog/baobab-mac-workflow.md` | `02503ed1f0bf0112d453b81d89aaaf319cb03c41dbeedc736f84597d728bca45` |
| `/Users/gabe/code/breathing-room/website/public/assets/blog/baobab/folder-review.svg` | `770623bc916bde21fddb1c1efea4c271d2040c74146b94641c26e9152da22a69` |
| `/Users/gabe/code/breathing-room/website/public/assets/blog/baobab/space-preview-2026-10-21.png` | `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a` |
| `/Users/gabe/code/breathing-room-app/docs/content/competitors/baobab/blog-skip.md` | `c8eda403a56de4e0463aec2f7c4bf9047bf04f13b785d364fd0a70ebde45aec4` |

Intended public path: `/blog/baobab-mac-workflow/`. The article is marked `status: review`, `published: false`, dated/updated October 22, 2026; author is Breathing Room team. Its 49-character title and 152-character description state a specific Mac folder-investigation task. Draft exclusion and rendering remain to be checked by the responsible site review process; no public preview is claimed.

## Intent and evidence

This is a concrete workflow article for someone carrying Baobab's folder-size investigation to a Mac: use a size view to choose a branch, understand its contents, classify originals versus reproducible outputs, verify recovery, then decide or stop. It is not an installation tutorial, a profile, an alternatives list, or a longer comparison matrix. The source packet, `docs/content/competitors/baobab/research.json` and `.md`, is sufficient for this bounded draft. The October 21 verification baseline and research were reused; no wholesale refetch was done.

The article uses claim-adjacent citations and distinguishes documented behavior from tests. It keeps the material source conflict explicit: GNOME’s listing presents its app in Linux/Flathub context, while Homebrew lists a macOS package and platform bottle keys. That supports package availability, not upstream Mac support guarantees or successful runtime parity. GNOME’s unversioned Trash help is not asserted to prove exact Homebrew Mac menus. GitLab HTTP 406, the older mirror metadata ending at 42.beta/2022, and Flathub’s navigation-shell-only response remain recorded research limitations; none is silently promoted to evidence. Unsupported or unknown Baobab monitoring, helper grouping, cache semantics, telemetry, Mac signing/runtime parity, exact paid-support terms, and remote-backend parity are omitted rather than turned into negative features.

Breathing Room is disclosed as the product we build. The article reuses `capabilities.md` and the identified preview release limits: source is not binary parity; Python 3.10+ is required for inventory; the identified preview is not Developer ID signed or notarized and lacks clean-machine/physical-Intel validation. Authenticated hosted AI and potential data transfer are disclosed. Different approval modes are not flattened into an unconditional “always asks” promise.

For replacement intent, the existing `alternatives-handoff.md` reports a separate Baobab alternatives draft and reviews existing packets for DaisyDisk, Disk Map, and DriveScape; it says these are job-relevant peers, not asserted AlternativeTo relationships. This task creates no second alternatives page and does not link hidden draft records. The separate head-to-head draft remains distinct. `blog-skip.md` consolidates verified Baobab/GNOME/package aliases under canonical `baobab`; no alias article is created.

## Visuals and interaction pass

Route B is used without copying competitor UI. The original `folder-review.svg` is a hand-authored decision sequence based on documented folder-size analysis and a review-before-removal workflow. It is an editorial diagram, not app UI, a Mac test, a scan, or a safety score. The caption links to GNOME’s official screenshot page. A second figure reuses the unmodified first-party Space browser preview. Its exact `screenshots.json` disclosure is retained; it is example data, not native behavior or measured results. The interaction pass is the non-executing inspect/identify/classify/recovery checklist; it performs no file access, uploads, deletion, or automatic file classification.

## Actual checks and blockers

- Reused packet and same-day capability/screenshot records; the copied preview PNG SHA-256 matches its retained source exactly.
- `xmllint --noout` passed on the authored SVG. This checks XML well-formedness, not visual usability.
- A Node standard-library-only structural check passed: frontmatter boundaries and required fields present, review/unpublished flags and current dates, sequential content headings/no body H1, both local image references with alt text, and no TODO/internal-link placeholders. It reported title/description lengths 49/152 and hashes above. This was not YAML/schema parsing.
- An attempted isolated import of the website's `yaml` dependency failed because `yaml` is not installed/resolvable in the existing website `node_modules`; Python PyYAML is also unavailable. No packages were installed. Do not count schema parsing as passed.
- No shared `pnpm check`, build, tests, or browser rendering were run, as prohibited by this job. No independent factual/rights/SEO score or responsive/light-dark review is claimed.

## Remaining review before publication

1. Independently compare article and asset hashes with the claim ledger and exact source passages; refresh volatile version/package facts if the October 21 evidence is older than 30 days at publication.
2. Render and inspect the draft through the responsible isolated review process at approximately 390/768/1440 px in light and dark themes. Confirm SVG text, long image/caption behavior, links and keyboard usability; review the first-party preview context and disclosure.
3. Run the authorized serialized website `pnpm check`, `pnpm build`, then `pnpm test`; inspect generated canonical/OG/Twitter/Article/Breadcrumb output and verify review/unpublished exclusion from routes, hubs, RSS and sitemap.
4. Require independent scorecard >=85/100 and zero evidence, visual, privacy, or technical blockers. Keep the record unpublished until approved. Draft completion is not publication or deployment.
