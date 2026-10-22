# BackApp research: adjacent app-inventory workflow

Checked **2026-10-21** · Task `research-backapp` · **Drafting blocked; research only.**

## Decision

BackApp is a live native macOS app-inventory and snapshot comparison tool by **Markus Lind / li-nd**, with [official documentation](https://backapp.developer.pm/) and [repository](https://github.com/li-nd/BackApp). Canonical owner: **`backapp`**. Do not skip as an alias or dead product. Treat it as **adjacent**, not a substitute for a storage cleaner or running-process investigation tool. No Windows replacement framing is needed or supported.

**Blocking diagnostic:** the [install guide](https://backapp.developer.pm/install/) says macOS Tahoe or newer, and the [vendor tap](https://github.com/li-nd/homebrew-apps/blob/main/Casks/backapp.rb) uses `:tahoe`, but both current source and the [v1.0.0 tagged project](https://github.com/li-nd/BackApp/blob/v1.0.0/BackApp.xcodeproj/project.pbxproj) set `MACOSX_DEPLOYMENT_TARGET = 26.2` in Debug and Release. This is more specific than the docs/cask and leaves the compiled ZIP's exact minimum OS unresolved. Do not promise all Tahoe versions, Intel support or a universal binary. Need a release-specific official compatibility manifest or separately authorized read-only inspection of release Info.plist/Mach-O metadata. No executable was downloaded under this image-only download authorization.

The useful article is a migration **inventory checklist**, not “BackApp alternatives that clean your Mac.” Do not draft an installation recommendation around unresolved requirements.

## Reused discovery and identity evidence

Read `PLAN.md`, `EDITORIAL.md`, `capabilities.md`, `screenshots.json`, and the corresponding `verification/batch-1.json` record before edits. No applicable `AGENTS.md` was found in the app tree or checked ancestors. Loaded the blog and browser-automation skills and read the MailKite contract with Breathing Room's editorial adaptation. No delegation or browser interaction was needed.

- Discovery: [Mole alternatives, page 7](https://alternativeto.net/software/mole/?p=7), retrieved `2026-10-21T18:37:22.582Z`, retained `docs/content/.runtime/mole-7.json`.
- Product listing: [BackApp About](https://alternativeto.net/software/backapp/about/), retrieved `2026-10-21T19:05:15.321Z`, retained `docs/content/.runtime/verification-1/backapp-directory.json`.
- Baseline official homepage: retrieved `2026-10-21T19:07:55.916176+00:00`, retained `docs/content/.runtime/verification-1/backapp-official.json`. Reused its current name, function, macOS identification, MIT and official-release link; did **not** refetch homepage or directory.
- All raw discovery hashes, retrieval times, source references and claim IDs are in `research.json`. New retained public evidence, timestamps, final URLs and hashes are in `source-ledger.json` and `sources/`.

**Directory contamination:** its header describes app inventories, but “WHAT IS BACKAPP?” contains “NativePass is a native macOS client for the Unix password manager pass.” Do not import that password-manager description or its GPG/runtime claims. The official BackApp homepage and reciprocal repository README establish the app-inventory identity. NativePass is not established as a BackApp alias. Neither PowerMyMac nor any other duplicate identity was established by these sources; absence of evidence is not a global alias audit. “Backup your App / Get back your App” is a tagline, not another queue product.

## Claim-level findings

These are documented/source-level findings, **not hands-on tests**. `research.json` supplies proposed wording, excerpts, locators, dates, conditions and matrix mappings for every material statement.

| Claim | Finding and scope | Official support |
|---|---|---|
| B01 | BackApp lists installed Mac apps and creates/compares/shares snapshots. | Reused homepage; retained `sources/README.md`. |
| B02 | Normal discovery: `/Applications`, `~/Applications`; optional System filter includes `/System/Applications`, default off. Not a whole-disk guarantee. | [Usage: Installed Apps / Filters](https://backapp.developer.pm/usage/#installed-apps). |
| B03 | Named snapshots are local JSON. Comparison states: Same version, Not installed, Different version. Import/export supports a checklist across Macs; imported snapshot gets a new ID. Version ordering is conditional on comparability. | [Usage](https://backapp.developer.pm/usage/), snapshot and export/import sections. |
| B04 | The export schema is metadata, not a backup of app binaries, documents or settings. It includes device/app details that deserve review before sharing. | Retained `sources/Snapshot.swift`, lines 10–44, 68–75, 112–121; [pinned source](https://github.com/li-nd/BackApp/blob/ebf4502d32ebe5b801b00e86653a4dd2fb3ba201/BackApp/Models/Snapshot.swift). No restored-Mac experiment. |
| B05 | Docs say the app list works offline; optional App Store detail lookup uses network. Not a traffic/privacy audit. | [Install: Dependencies](https://backapp.developer.pm/install/#dependencies), [Usage: App detail](https://backapp.developer.pm/usage/#app-detail). |
| B06 | Homebrew vendor tap or GitHub ZIP; not Mac App Store distribution. Docs disclose ad-hoc signing and no notarization. | [Install](https://backapp.developer.pm/install/). No installation/signature test or protection-bypass advice. |
| B07 | GitHub latest stable metadata: **1.0.0**, tag **v1.0.0**, published **2026-08-24T20:11:23Z**; asset `BackApp-1.0.0-macos.zip`. Project marketing version separately says **1.0**. | [Release](https://github.com/li-nd/BackApp/releases/tag/v1.0.0), retained API and cask. Reported archive digest matches cask; archive bytes not downloaded or verified. |
| B08–09 | Docs/cask Tahoe; source deployment target **26.2**. Compiled minimum OS and architecture coverage **not verified**. | Retained install, cask, current and tagged project. **Drafting blocker.** |
| B10–11 | **MIT source and associated documentation**, with notice condition. Public release link; no verified commercial-plan amount, currency, billing period, trial or support terms. | [MIT licence](https://github.com/li-nd/BackApp/blob/main/LICENSE), README/install/release. Do not turn directory “Free” or the MIT grant into a perpetual $0 binary offer. |

Cleanup execution/approval controls, running-helper grouping, recurring storage growth and developer-cache cleanup in BackApp remain **not verified**, not “No.” These are not the documented inventory job. No superiority, savings, speed, safety or complete migration claim is supported.

### Breathing Room evidence and fair trade-offs

Reuse same-day `docs/content/capabilities.md`, with its source and public-page citations, rather than needlessly re-fetching current verified first-party claims:

- R01: source implements storage views, app/helper CPU/memory grouping and constrained reviewable cleanup. Source presence is not distributed-release feature parity. Ownership inference and overlapping RSS are qualified; no forensic proof or performance promise.
- R02: identified preview **0.1.0-preview.1**, advertised macOS **13+** universal; physical Intel/clean-machine validation incomplete. Published preview is Apple Development signed, **not Developer ID signed or notarized**. **Python 3.10+** required and not bundled. Do not recommend disabling system protections.
- R03: advertised free local core; optional AI Care **$5 USD/month / $50 USD/year**, renewing until cancelled, applicable checkout tax. Hosted AI requires network/authentication and may receive relevant paths, storage/process data, history and tool output. Usage allowance and payment activation were not tested. Website account gate is not the same as public GitHub download access.
- Default interactive actions use review; optional automatic Ruff Trash mode is a narrow explicit exception. Daily care uses exact saved approvals and requires the app to remain running. No blanket “never does anything without asking” or entirely-offline-AI claim.

**BackApp advantage:** directly documented app-set JSON snapshots and cross-Mac missing/version comparison; local inventory with optional online detail enrichment. **Trade-off:** inventory metadata is not a full backup, reinstall mechanism, licence migration or proof that app data works after migration.

**Breathing Room advantage for a different job:** source-level storage and live helper/resource investigation, plus bounded approved maintenance. **Trade-off:** preview/runtime/install limitations and hosted AI boundaries. It is not established as a BackApp inventory-export replacement. At a recommendation, say **“Breathing Room, which we build”**. Readers can reasonably use both, or neither if they need a full backup.

## Visual evidence and permitted reuse

Both actual PNGs were opened and read in this job, not approved merely from file metadata. No generated UI, stock photography, sign-in, cookies, hidden extraction or native app execution was used.

### Official BackApp comparison view

- Source page: https://backapp.developer.pm/usage/#compare-to-a-snapshot
- Official site asset: https://backapp.developer.pm/screenshots/4-snapshot-compare.png
- Downloaded exact pinned repository asset: https://raw.githubusercontent.com/li-nd/BackApp/ebf4502d32ebe5b801b00e86653a4dd2fb3ba201/docs/screenshots/4-snapshot-compare.png
- Original: `assets/snapshot-compare-original.png`, **1347 × 908**, retrieved `2026-10-21T20:02:33.366699+00:00`.
- SHA-256: `bccc25ed94e6163066d419db8ab943bd7d2f6846535aa181cd61f1ac641b6129`. No edits or published derivative.
- Reuse basis: repository's MIT grant explicitly includes associated documentation; full notice retained in `sources/LICENSE.txt`. Carry the full copyright/permission notice into any distributed site asset. Credit **© 2026 Markus Lind, MIT**. No third-party logo/trademark ownership or endorsement inferred.
- Caption: **BackApp's official snapshot-comparison screenshot, supplied in its documentation. Shows Same version and Not installed states; not our test or a measured migration result. © 2026 Markus Lind, MIT.**
- Alt: **BackApp snapshot comparison with installed-app version rows, missing-app indicators and source/status filters.**
- Capture date, version and OS unknown. Displayed snapshot date is not a capture timestamp. Vendor data includes some mismatched names/paths: do not present rows as audited actual installations. Only public app paths and generic device information visible, no exposed account credentials or personal home path found. Incidental marks remain their owners' marks.

### Selected Breathing Room view

Reuse `current-apps-browser-preview` from `screenshots.json`:

- `docs/content/assets/breathing-room/apps-preview-2026-10-21.png`, **2940 × 4440**.
- Original SHA-256: `6bacc46187202835a29e24458383056e9cd55197bd53b0df2592e68c03c741d3`.
- Inventory capture time: `2026-10-21T19:06:59.096850+00:00`; current-source commit `54828ac3170b45861aee70861dd0b9c658ed7e51`. Browser preview at `http://127.0.0.1:1431/`, not a new capture in this job.
- Caption: **Current-source Breathing Room Apps browser preview, captured October 21, 2026. Example data only; not a native scan, measured activity or cleanup result.**
- Alt: **Breathing Room Apps browser preview with visible example-data banner and illustrative grouped app/helper CPU and memory rows.**
- Keep **Interactive preview · example data** and **This browser preview uses example data. Actions never change your Mac.** visible. Source currentness does not certify binary/native behavior. First-party owner-requested capture basis; incidental third-party marks are not blanket-licensed.

Draft-stage images need target-page narrow-screen legibility and independent context/privacy review. The full-height Apps image should not be shrunk into unreadable text; any contextual crop must preserve disclosures, record edits and retain original plus derivative hashes. No website asset, image crop or published hash exists yet. MIT notice distribution is mandatory for the competitor image; research permission does not equal independent publication approval.

## Distinct workflow article brief

**Title:** Compare your installed Mac apps before and after a migration  
**Slug:** `compare-mac-app-inventories-before-after-migration`  
**Track:** Search/reference workflow. **Intent:** app/version checklist across Macs, not a storage-cleaner sales page or full-backup tutorial.

Lead with what a JSON inventory can and cannot tell you. Place the official comparison image after the lead, then:

1. Define app-folder discovery and optional system inclusion; scope is not every app/file on every volume.
2. Explain the documented named snapshot/export/import process without saying we ran it.
3. Interpret missing and different-version rows; a matching version is not proof of migrated documents, settings, licences or app health.
4. Review device/app metadata before sharing JSON; no upload widget.
5. Separate installed-app change from running-helper CPU/memory or storage growth, illustrated by the expressly labeled Breathing Room preview.
6. Offer a non-destructive decision checklist and link to `/comparisons/backapp/` and `/comparisons/` only when real draft routes are established by their owner.

**Interaction pass requirement:** a small static decision aid: app/version list → inventory; binaries/documents/settings → independent backup plan; helper activity/storage growth → maintenance investigation. No arbitrary runnable code, accounts, companion repository, scan or deletion is needed. Keep install advice blocked pending exact compiled OS evidence.

## Concise comparison brief

**Title:** Breathing Room vs BackApp: activity or app inventory?  
**Route intent:** `/comparisons/backapp/`, not a near-duplicate `/alternatives/` doorway.

Conclude first that the tools serve adjacent jobs. Disclose affiliation in the recommendation. Use a concise claim-linked matrix for job, JSON inventory, running helpers, storage/cleanup, local/network boundary, OS/version, licence/pricing and install caveats. Unknown BackApp cleanup/growth/helper/cache cells stay “not verified.” Preserve both products' limitations and both real product visuals. Link to the distinct migration workflow rather than expanding the same matrix into filler. No overall winner, cheaper/free-lifetime claim, invented testing, FAQ, rating or savings.

## Remaining gates and handoff

- **Critical:** release-specific compiled minimum macOS remains unresolved against source target 26.2. Receipt is **blocked**, not publication-ready or queue-complete.
- **Noncritical unknowns:** architecture coverage (omit support promises), commercial-plan terms (explicit unknown), vendor capture build/date (official illustration only), undocumented cleanup/helper/cache features (unknown), all hands-on results (not performed).
- **Later stages:** independently verify draft facts, licence notice transfer, image presentation and captions; then website check/build/tests and responsive/theme review only when site changes are authorized. No score or runtime QA claimed here.
- No shared files, marketing site, queue/database or other product directories edited; no signups, credentials, executable download, app installation, cleanup, messages, commits, pushes or deployment.

Actual structural validation and hashes are retained in `validation.json`; the required runtime receipt summarizes that result. This packet's retained-source checks are not native feature, signature, migration or website tests.
