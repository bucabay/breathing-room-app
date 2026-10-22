# RemoveMacAI research handoff

Research only. Task: `research-removemacai`. Local review date: October 22, 2026; retained retrieval timestamps are October 21 UTC. No article, website record, queue change or publication approval.

## Decision

**Keep as a distinct, adjacent Mac product.** Canonical owner ID: `removemacai`. The official homepage links to [omlahore/RemoveMacAI](https://github.com/omlahore/RemoveMacAI); the author is Om Lahore. The app and `removemacai` CLI are one product, not separate article candidates. The acknowledged upstream [pared](https://github.com/4evy/pared) is not established as a product alias. No evidence connects RemoveMacAI to PowerMyMac. Alias skip: **false**; no duplicate doorway draft.

RemoveMacAI documents Apple Intelligence disable/model removal, preference changes, background-item toggles and targeted storage cleanup. This overlaps Mac maintenance but is not the same job as investigating broad storage growth and grouped app activity. Breathing Room must not be pitched as a verified Apple Intelligence removal replacement.

## Evidence reused first

The `removemacai` record in `docs/content/verification/batch-2.json` already verifies the homepage identity, core purpose, free/open-source offer, MIT label and homepage's macOS 27/Apple silicon statement. Its raw official and directory captures remain referenced and SHA-256 checked. Neither page was re-fetched.

Discovery: [AlternativeTo about page](https://alternativeto.net/software/removemacai/about/), retrieved `2026-10-21T19:05:39.872Z`. Existing manifest records the Mole seed edge at `https://alternativeto.net/software/mole/?p=2`, retrieved `2026-10-21T18:37:09.298Z`. Directory evidence establishes discovery, not feature behavior. The about-page raw capture is retained; the original pagination response is not independently copied into this packet.

New official evidence fills release, workflow, screenshot and licence gaps. Raw files, final URLs, exact retrieval times and hashes are in `sources/ledger.json`; claim-level excerpts, conditions and checks are in `research.json`. These are documentary findings, not execution tests.

## Version and material caveats

- GitHub latest stable release metadata identifies **v1.1.4**, published **2026-10-18T19:49:49Z**, with an app ZIP and Darwin arm64 CLI archive. Binary contents, attestations, checksums and signatures were not independently tested. Metadata digests are not downloaded-file verification.
- [Tagged v1.1.4 README](https://github.com/omlahore/RemoveMacAI/blob/v1.1.4/README.md): Apple silicon, macOS 27; author says tested on 27.0 and requires 0.2.3+ on 27.0.1. It explicitly says 26 and earlier unsupported.
- **Documentation conflict:** retained `main` README says macOS 26 runs since 1.1.0 and macOS 15.1+ is in testing using 1.2.0-beta.1. Do not silently substitute branch claims for release support. The bounded brief uses macOS 27/Apple silicon only; older-OS installation recommendations remain unverified.
- Free/open-source is the verified software offer. No paid tier, renewal requirement or currency applies to that documented offer. Optional sponsorship is not a licence fee. The MIT grant and complete notices are retained.
- The README discloses the app is **not notarized**. No installation, Homebrew operation or remote-shell command was executed. Link installation documentation rather than reproduce untested commands or bypass system protections.

## Workflow findings and comparison dimensions

Each row maps to the named claim IDs in `research.json`, with exact source URLs/excerpts/check times.

| Dimension | Documentary finding | Claim IDs |
|---|---|---|
| Main job | Selectively disable Apple Intelligence and remove/block models; selected feature retention | `function` |
| Review | App review workflow; CLI apply/undo/background/clean ask; dry-run stops; `--yes` skips asking | `review` |
| Approval mechanism | Locked settings use a user-approved configuration profile; other preferences retain previous values in a journal | `profile` |
| Cleanup scope | Installers, wallpaper videos, iOS update files, Xcode data, simulators, app caches, local snapshots | `storage` |
| Reversibility | Files generally go to Trash; unavailable simulators and Time Machine snapshots are deleted immediately through simctl/tmutil | `trash-exceptions` |
| Space accounting | Model assets released through Apple's service may remain counted until macOS deletes files on its schedule | `timing` |
| Background items | Individual toggles for other apps' updaters/helpers, not evidence of grouped CPU/memory accounting | `background` |
| Local/hosted | Author says no runtime network requests or data collection; not independently audited; downloads use network | `local` |
| System protections | Author says SIP stays on and /System is not changed; protected built-in apps are not deleted | `sip` |
| Feature cost | Apple AI features and dependent Foundation Models/Shortcuts/Visual Intelligence/Calendar uses can stop working | `feature-loss` |
| Monitoring | Recurring-growth tracking and grouped-helper CPU/memory reporting **not verified**, not “No” | unknown cells |
| Runtime | Exact CLI/source-build dependencies not verified; do not invent Python requirements | unknown cells |

The homepage's broad undo/Trash wording is narrower in the README's specific deletion exceptions. Specific exceptions govern the brief. Never call every action reversible, safe or guaranteed to recover a number of gigabytes. Disabling an updater also deserves an editorial reminder that someone must remain responsible for updates; no performance/security outcome was tested.

## Breathing Room comparison basis

Reuse `docs/content/capabilities.md`, reviewed October 21, with its code/public-source locators and caveats. Do not upgrade source implementations into tested binary behavior:

- Free Apache-2.0 preview, identified release `0.1.0-preview.1`; advertised macOS 13+ universal installer, physical Intel runtime unvalidated, Python 3.10+ required for inventory, Apple Development signed but not Developer ID signed/notarized.
- Source implements category/owner/project/folder/large-file storage views, grouped app/process CPU and memory, activity history and constrained cleanup approvals. No verified Apple Intelligence model-removal capability.
- Default review, optional verified Ruff-cache automation and exact saved daily-care approvals are distinct modes. Scheduled care requires the app to remain running.
- Hosted AI needs internet/authentication and can transmit relevant paths/process/storage metadata. Do not call all AI offline. Optional AI Care is advertised at **$5 USD/month or $50 USD/year**, renewing until cancelled, with applicable tax at checkout; allowance/enforcement and purchase success remain unverified. Website download has an account gate; direct public releases are documented separately.

Claim IDs: `br-offer`, `br-caveats`, `br-tools`, `br-hosted`, `br-approval`. Where a recommendation appears, say **“Breathing Room, which we build.”**

## Visual evidence and reuse

### Real competitor app view

- Source: [v1.1.4 README](https://github.com/omlahore/RemoveMacAI/blob/v1.1.4/README.md).
- Exact asset: `https://raw.githubusercontent.com/omlahore/RemoveMacAI/v1.1.4/docs/screens/overview-light.webp`.
- Retained unmodified: `sources/overview-light-original.webp`, **2000 × 1400**, SHA-256 `05593d2f6111898bd25395ced7228c33df8a186882f261ece3f73962d050a32b`.
- Opened and visually read: actual app Overview, sidebar, AI status, storage estimate and presets. Not a homepage capture or generated UI. The vendor's visible 16.1 GB and “Safe by design” text are not our measurements or safety findings. Actual capture build/date/OS are unknown; tagged distribution does not establish capture version.
- Reuse basis: repository MIT licence explicitly includes associated documentation files; this is its README documentation asset. Retain **complete** copyright/permission/warranty notice in `sources/LICENSE.txt` with any later copied/published asset, plus credit. Third-party notices are retained conservatively. This does not license others' trademarks or imply endorsement. No separate screenshot restriction was found in inspected notices.
- Caption: “Official RemoveMacAI Overview image distributed with v1.1.4 documentation. Vendor illustration, not our test; the displayed 16.1 GB is not measured savings or a guarantee.”
- Alt: “RemoveMacAI Overview with Apple Intelligence status, background items, storage estimate and two reviewable presets.”

### Selected current-source Breathing Room preview

Reuse `current-space-browser-preview` from `screenshots.json`: `docs/content/assets/breathing-room/space-preview-2026-10-21.png`, captured `2026-10-21T19:06:45.416416+00:00`, source commit `54828ac3170b45861aee70861dd0b9c658ed7e51`, **2940 × 3468**, SHA-256 `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a`.

Opened and read again for this packet: visible interactive-preview/example-data notice and non-mutating-browser warning, storage categories and navigation. Existing first-party owner-requested capture basis applies; third-party marks remain their owners'. Do not relabel as a native scan, savings measurement or current binary proof. Keep the example-data notices visible.

Required caption: **“Current-source Breathing Room Space browser preview, captured October 21, 2026. Example data only; not a native scan, measured activity or cleanup result.”** Alt: “Breathing Room Space view rendered in a browser with illustrative example data.”

No image has been published or transformed. `publishedPath` and published hash remain null. Independent target-page legibility/rights/context review is a later gate, not inferred from image dimensions.

## Distinct workflow article brief

**Title:** Apple Intelligence models or ordinary clutter? Choose the cleanup scope first  
**Proposed slug:** `apple-intelligence-models-versus-mac-clutter`  
**Track:** search/reference. **Intent:** distinguish AI/configuration changes from unknown disk growth before choosing an intervention. No hands-on tutorial or claimed result.

Lead conclusion: RemoveMacAI addresses unwanted Apple Intelligence and selected macOS settings; broader disk growth needs a different investigation. Start with feature dependencies, OS support and cleanup reversibility, not a promised number of gigabytes.

Outline:
1. Identify AI-dependent features to keep before changing anything.
2. Separate configuration-profile changes from storage cleanup.
3. Bound v1.1.4 discussion to macOS 27/Apple silicon and disclose documentation conflict.
4. Review exact changes; separate ordinary Trash moves from immediate simctl/tmutil deletion.
5. Distinguish released model assets, Trash contents and available disk space without promising measurements.
6. For unknown growth, explain the wider-investigation job and make one bounded, disclosed Breathing Room recommendation with preview/runtime/hosted-AI caveats. Keeping current settings or using built-in settings is also a legitimate decision; do not invent an equivalent model-deletion procedure.

Interaction handoff: non-executing checklist for platform, features to retain, settings-vs-storage goal and acceptance of immediate deletion. No generated cleanup commands, calculator pretending to scan, signup or arbitrary demo repo. Place the official app image after the lead and the labeled Breathing Room Space preview at the broader-investigation section. Link `/comparisons/`, proposed `/comparisons/removemacai/`, and relevant `/tools/` only after route verification.

## Concise comparison brief

**Title:** Breathing Room vs RemoveMacAI: investigation or de-bloating?  
**Proposed comparison slug:** `removemacai`.

Use a short claim-linked matrix: job, macOS/architecture, licence/price, local/hosted boundary, review/undo exceptions, developer data, background controls versus resource monitoring, release/install caveats. Unknown cells remain “not verified.”

Decision: RemoveMacAI is the documented fit for selective Apple Intelligence/configuration changes on its conservatively supported platform. Breathing Room, which we build, serves broader storage/app-activity investigation but is a non-notarized preview with a Python prerequisite and optional paid hosted AI. They are adjacent, not interchangeable. Link the deeper workflow article; no separate alternatives doorway.

## Gate and honest unknowns

**Research complete for the bounded brief; drafting may proceed only within these conditions.** The OS documentation discrepancy is retained and resolved for this article by restricting scope, not by declaring the source conflict nonexistent. Unknown capture build/date, independent performance/privacy results, recurring-growth support and CLI build prerequisites are noncritical to this non-installation, non-benchmark brief. Any expansion to older-OS installation advice needs new evidence first.

No critical evidence blocker remains for that bounded draft. Neither page is publication-approved: draft/unpublished state, claim-adjacent citations, complete image notice/credit, independent fact/visual review, current pricing check when stale, and actual site/browser QA are still required. No score is awarded at research stage. No browser session, product installation, native test, cleanup, account access, message, purchase, commit, push or deployment occurred.

Validation outcomes are recorded in `validation.json` and the exact required runtime receipt. Site builds are inapplicable because no site files changed.
