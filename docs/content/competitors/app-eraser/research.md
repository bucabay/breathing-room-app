# App Eraser: research handoff

**Task:** `research-app-eraser` · **Checked:** October 21, 2026 · **Status: blocked for drafting.** No site content was created. This is research, not a review score or publication approval.

## Decision

Retain **App Eraser** as a distinct, **adjacent** Mac tool. Its official homepage and repository are [davunt/app-eraser](https://github.com/davunt/app-eraser). `canonicalOwnerId: app-eraser`; no verified alias requires skipping this entry. Neither the established owner nor the package identity supports conflating it with PowerMyMac. This is not an exhaustive assertion that aliases cannot exist.

App Eraser addresses unwanted applications and related-file candidates. Breathing Room addresses wider storage/activity investigation; a full app-uninstaller replacement was not established. Do not turn this into a generic cleaner-versus-cleaner doorway page. There is no Windows replacement premise or verified Windows support here.

**Critical diagnostic:** the README links a real official app-image file, but standalone reuse is not cleared. GitHub/root `LICENSE` say GPL-3.0 while `package.json` says ISC. The conflict must be disclosed rather than silently resolved. No competitor image was downloaded. A link-only source does **not** pass the required on-page image gate. Resolve licence/asset coverage or obtain an explicitly approved rights decision, then retrieve, hash and inspect the permitted original before drafting. No permission message is authorized.

## Evidence reused first

- `docs/content/verification/batch-1.json`, product `app-eraser`, already verifies the identity, Mac app-removal description, free offer and GitHub GPL label. Its status is partial, with availability missing. Batch-2 research was unnecessary once this corresponding current record was located.
- Existing official snapshot: `docs/content/.runtime/verification-1/app-eraser-official.json`, retrieved **2026-10-21T19:08:11.248136+00:00**, SHA-256 `f6c463ec08db4da0f7f2800d3ac2b389a782163865acabe212759dcf1cce7200`. Hash checked against retained bytes. Read the full README text in the snapshot; did not refetch the homepage.
- [AlternativeTo discovery](https://alternativeto.net/software/app-eraser/about/): existing snapshot retrieved **2026-10-21T19:04:59.358Z**, SHA-256 `a433be65dafc0f28ab10823f67cca985e9d511627bdb717a4060ab5fd894697f`. Official-link excerpt: “Official Website / github.com/davunt/app-eraser”. Directory labels and comments are discovery, not feature tests.
- Manifest edges: [CleanMyMac page 3](https://alternativeto.net/software/cleanmymac/?p=3), **18:36:26.872Z**, and [Mole page 2](https://alternativeto.net/software/mole/?p=2), **18:37:09.298Z**, October 21. These come from `docs/content/competitors.json`; no independent edge raw-file hash was established here.
- Reused current `capabilities.md` and `screenshots.json` instead of repeating their same-day verification. No shared register was edited.

## Missing facts checked against official sources

Exact URLs, excerpts, conditions and checked dates are in `research.json`. Every factual matrix entry references a claim ID; unknowns are not negative checkmarks. Reviewer for this packet is the scheduled research worker, not an independent approver.

| Claim | Evidence and boundary |
| --- | --- |
| **AE-01/02: identity and offer** | Official README: “App Eraser helps remove unwanted macOS applications and any related files that they leave behind.” Repository description: “Free and Open Source macOS app removal tool.” Free is the documented offer; no subscription/trial amount or conditions were verified. |
| **AE-03: release availability** | [Official latest-release API](https://api.github.com/repos/davunt/app-eraser/releases/latest) returned HTTP 200, tag **1.0.0**, published **2023-12-05T13:53:54Z**, not draft/prerelease. Listed asset: `App.Eraser-1.0.0-universal.dmg`, [release page](https://github.com/davunt/app-eraser/releases/tag/1.0.0). Metadata was read, not the binary. Do not call it abandoned merely because the release is old. |
| **AE-04: discovery mechanism** | README describes name/bundle-ID matching and threshold scoring. [Pinned implementation](https://github.com/davunt/app-eraser/blob/1b801bb3db4de54233d788e5f5866ce4f30f5da4/src/main/index.js) immediately accepts normalized bundle-ID matches and uses threshold matching for name variants. This is a relation heuristic, not proof of file ownership/disposability. |
| **AE-05/08: selection and approval** | [Controller](https://github.com/davunt/app-eraser/blob/1b801bb3db4de54233d788e5f5866ce4f30f5da4/src/main/controller.js): `checkbox.checked = true`, checked inputs determine selected paths, `shell.showItemInFolder(filePath)` reveals candidates, and confirmation says files “will be moved to trash”. The removal path attempts to quit the app first. These are source findings, not executed tests. |
| **AE-06/07: permissions and coverage** | README requires Finder Automation access for Trash moves and chosen Files and Folders permissions for discovery. [Configured locations](https://github.com/davunt/app-eraser/blob/1b801bb3db4de54233d788e5f5866ce4f30f5da4/utils/pathLocations.js) include Library support, caches, containers and preferences. Actual readable coverage is not established; the implementation processes successful directory reads. |
| **AE-09: licence conflict** | [Root licence](https://raw.githubusercontent.com/davunt/app-eraser/main/LICENSE): “GNU GENERAL PUBLIC LICENSE / Version 3, 29 June 2007”; GitHub labels GPL-3.0. [Package](https://raw.githubusercontent.com/davunt/app-eraser/main/package.json): `"license": "ISC"`. Conflict is verified; definitive uniform licensing is not. |
| **AE-10: runtime scope** | Package version **1.0.0**, author **David H**, app ID `com.apperaser.app`, Electron dependency **^22.2.0**, development Node pin **18.14.0**. These are development/source metadata, not user prerequisites or exact bundled runtime verification. No npm scripts were executed. |

The three pinned workflow responses are preserved in `sources/controller.json`, `sources/view.json` and `sources/locations.json`, with exact retrieval times and response-text SHA-256 values. `collect-evidence.py` only retrieves those public files; it never executes them. Earlier release/tree/licence/package responses were read in tool output; retained excerpts explicitly leave exact retrieval clock and full-response hashes unknown instead of inventing them.

### Honest unknowns

- Minimum supported macOS, current macOS compatibility and present binary signing/notarization were **not verified**. A universal filename is not proof of either architecture running correctly. A README section about unidentified-developer errors is not a current binary audit. Do not copy protection-bypass instructions.
- Source files were pinned to `1b801bb3db4de54233d788e5f5866ce4f30f5da4`; exact correspondence to tag 1.0.0 was not established. Describe source behavior as source behavior.
- Complete offline behavior, telemetry absence, registration requirements and data retention were **not verified**. The author's privacy rationale and AlternativeTo tags cannot establish those claims. Local file operations do not establish zero networking.
- Helper grouping, recurring-growth monitoring and package-manager cache cleanup were **not verified**. Searching app-related Library caches is not equivalent to cleanup through npm/pnpm/uv or other owning tools.
- No app installation, process quitting, file removal, measured savings, performance benchmark, account creation or signing check occurred. Do not claim that files in Trash equal newly available disk space; source general macOS explanations separately before drafting them as facts.

## Visual handoff

### Competitor: official source identified, gate blocked

- Source page: <https://github.com/davunt/app-eraser#readme>.
- README-linked image page: <https://github.com/davunt/app-eraser/blob/main/assets/img/appScreenshot.png>.
- Pinned original URL: <https://raw.githubusercontent.com/davunt/app-eraser/1b801bb3db4de54233d788e5f5866ce4f30f5da4/assets/img/appScreenshot.png>.
- Official repository tree identifies this as `assets/img/appScreenshot.png`, Git blob SHA-1 `ff270f764b2c704c7b9074d63c1f91a9d02a9acb`, listed size 549,160 bytes. That is **not** an original-file SHA-256.
- Reuse: **link-only**, pending licence conflict/asset coverage resolution. Public availability is not a licence. No invented fair-use clearance, screenshot capture date, dimensions, app version or UI description.
- Original bytes/hash and privacy/visual inspection remain pending because no download was authorized by established rights. After clearance, inspect the actual app view, preserve notices, record original/published hashes and only then write specific alt text. The current placeholder alt describes a link, not an approved embedded image.

### Breathing Room: selected existing current-source Space preview

Selected `current-space-browser-preview`, at `docs/content/assets/breathing-room/space-preview-2026-10-21.png` (**2940 × 3468**), captured **2026-10-21T19:06:45.416416+00:00**, source commit `54828ac3170b45861aee70861dd0b9c658ed7e51`.

SHA-256: `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a`. Reuse the original; no new copy or edits were made. First-party capture basis is inherited from `screenshots.json`; no endorsement or blanket trademark licence is inferred.

**Required caption:** “Current-source Breathing Room Space browser preview, captured October 21, 2026. Example data only; not a native scan, measured activity or cleanup result.”

**Alt:** “Breathing Room Space browser preview with visible example-data notices, category chart and folder-size list.”

Opened and read the actual image in this job. Both example-data notices are visible; the floating assistant overlaps the chart. Preserve the notices and review legibility in the eventual page context. This is neither an earlier legacy preview relabeled current nor native-release evidence. Currentness is scoped to its recorded capture/source commit.

## Distinct workflow article brief

**Proposed title:** Review App Eraser’s related-file matches before removing a Mac app  
**Proposed slug:** `review-app-eraser-related-file-matches`  
**Track:** search/reference. **Primary job:** distinguish a filename/bundle-ID candidate from a file the reader deliberately agrees to remove.

1. Conclusion in the description: App Eraser surfaces candidates; matching alone does not settle what should be removed. Put its cleared official app view directly after the lead, without repeating the introduction.
2. Explain name/bundle-ID matching and preselected candidates using AE-04/05. No fabricated scan or anecdote.
3. Non-executing checklist: save work, inspect candidates in Finder, keep uncertain/shared data, consider permission-limited coverage. Do not run removal or offer a blanket cache deletion recipe.
4. Discuss version/support uncertainty and the permission boundary, not security-bypass instructions.
5. Use the later example-data Space preview to explain a separate task: investigating storage unrelated to an app-removal decision.
6. One bounded recommendation: “Breathing Room, which we build,” with all preview/runtime/hosted/paid limitations. App Eraser may fit focused unwanted-app review better; Breathing Room is not a certified complete uninstaller.

**Interaction pass:** plan a static decision checklist for “known app-related / uncertain or shared / unrelated growth.” No fake scanner, filesystem access, deletion control, irrelevant code demo or hypothetical measured savings. Source additional Apple/vendor guidance before turning general uninstall/Trash semantics into factual instructions. No article draft or interactive implementation is authorized at this research stage.

## Concise comparison brief

**Proposed title:** Breathing Room vs App Eraser: investigation or app removal?  
**Proposed comparison slug:** `app-eraser`.

Answer the adjacent-tool decision, not which cleaner “wins”. Use a short claim-linked matrix for reader job, discovery method, review controls, release/OS evidence, licence conflict, cost and local/hosted boundary. Retain “not verified” where appropriate. Include both real app views only after rights/visual gates pass. Link to the workflow and `/comparisons/`; routes are proposed, not asserted live.

### Truthful advantages and trade-offs

- **App Eraser:** documented free, focused app-removal offer; inspectable matching and selected-file review. Candidates initialize checked; matching cannot guarantee disposability. Permissions, current runtime compatibility and licence ambiguity limit recommendations. No claims of total trace removal or superior safety.
- **Breathing Room:** broader storage and grouped process inspection in source; useful editorial fit for investigating growth rather than merely removing an app. **0.1.0-preview.1**, **macOS 13+**, **Python 3.10+**, advertised universal installer, but reviewed release is Apple Development signed, **not Developer ID signed/notarized**, and clean-machine/physical Intel validation is absent.
- Breathing Room's local core is advertised free. Hosted AI needs internet/authentication and can send relevant paths/process/storage information to the service. Optional AI Care is advertised at **$5 USD/month or $50 USD/year**, auto-renewing until cancelled, tax at checkout; exact allowances/entitlement enforcement remain unverified. Do not imply everything is offline, paid, unauthenticated or guaranteed private. Daily care needs the running app and exact saved approvals; optional verified Ruff-cache automatic mode prevents unconditional “always asks before every action” wording.
- Neither source inspection nor an example screenshot establishes successful cleanup, risk-free behavior, speedups, installer compatibility or measured savings. Source presence does not establish distributed binary feature parity.

## Gates and validation

**Drafting blocked:** competitor image rights/provenance/visual approval and licence conflict handling. Exact diagnostic/remedy is recorded in `research.json`. Other unknowns can remain explicit limitations; do not invent facts to fill a table. This is not a dead-product/alias skip.

Structural checks, actual outcomes and hashes are retained in `validation.json`. This packet has no independent editorial score or approval. No marketing files changed, so no site check/build/test or responsive browser QA was run. Those gates remain for separately authorized later work. Browser recovery was unnecessary because public read-only sources and existing visual evidence sufficed for this blocked research packet. No other queue job or shared state was changed.
