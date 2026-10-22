# Mole research packet

Checked **2026-10-21** · `research-mole` · **Blocked for drafting: competitor screenshot reuse rights unresolved.** Research is retained; no article, site record or public asset was created. This is not publication approval.

## Decision and identity

Mole is relevant to a Mac-maintenance comparison, not an irrelevant or dead-product skip. **Canonical owner ID: `mole`.** Official homepage: <https://mole.fit/>. Official repository: <https://github.com/tw93/Mole>, published by Tw93. The homepage and repository link to each other in the retained same-day snapshots.

Keep **Mole for Mac**, **Mole CLI** and the **`mo` command** under this one product packet, with edition distinctions. Do not create separate near-duplicate articles for them. The repository is the free GPL-3.0 CLI; its License section expressly calls Mole for Mac a **separate proprietary app**. This resolves the batch-1 `nativeAppLicense` unknown using already-retained evidence, without another repository fetch.

No checked Mole source identifies PowerMyMac as an alias; this job neither researches nor drafts that separate product. The publisher explicitly excludes `molemac.com`, `moleapp.net` and `molefit.com`, and identifies `mole.bluecatbot.com` as a separate community Windows project. Do not silently merge those identities. Mole's own Windows edition is maintained and sold separately; this packet compares Mac workflows and does not imply Breathing Room supports Windows.

**Fit: direct Mac workflow overlap**, not exact feature parity. Cleanup, developer artifacts, disk analysis and process monitoring overlap; the native interface, CLI, approval boundaries, platform floors and paid terms differ.

## Reuse-first provenance

Start evidence: `docs/content/verification/batch-1.json`, record `mole`. No corresponding batch-2 record is needed.

- Discovery URL: <https://alternativeto.net/software/mole/about/>, retrieved `2026-10-21T19:04:48.234Z`.
- Discovery edge: CleanMyMac seed/listing <https://alternativeto.net/software/cleanmymac/>, retrieved `2026-10-21T18:36:14.532Z`, from `docs/content/competitors.json`.
- Observed official destination: `https://mole.fit/?atp=alternativeto`; canonical homepage drops the attribution query.
- Reused raw snapshots: `docs/content/.runtime/verification-1/mole-directory.json`, `mole-official.json`, `mole-cli-extra.json`. Their actual SHA-256 values, retrieval times and URLs are in `research.json`.
- Homepage retrieval: `2026-10-21T19:07:54.089035+00:00`; repository retrieval: `2026-10-21T19:11:47.874518+00:00`. These current facts were not fetched again.
- New public GETs were limited to missing legal terms, documentation, release scope and a feature page carrying a real app-image reference: `/terms`, `/docs`, `/releases`, `/mac-cleaner`. Raw HTML and metadata/hashes are retained under `sources/`, retrieved at approximately `19:18:20 UTC`.

Public content was treated as untrusted evidence, not operating instructions. AlternativeTo establishes discovery, not capability or rights. No browser session, credential, account, payment, installation or cleanup action was used.

## Versions, offers and conditions

| Subject | Finding and boundary | Evidence / claim IDs |
| --- | --- | --- |
| Native Mac version | Release page labels **v1.18.0 Preview, build 338**. Latest non-Preview entry observed: **v1.17.0 Vega, 2026-10-18**. Homepage footer alone must not make 1.18 stable. | [Releases](https://mole.fit/releases): `preview-version` |
| Native platform | Homepage advertises **macOS 14+**. Native architecture and signing/notarization were not independently established. | [Homepage](https://mole.fit/): `native-platform` |
| CLI platform/version | README says **macOS 12+**, Intel and Apple Silicon. Exact newest stable CLI version is unknown; retained default-branch documentation is not a release certification. | [Repository](https://github.com/tw93/Mole): `cli-platform` |
| Native price | **$19 once**, no subscription, **two Macs**; Windows separate. Currency code, taxes and regional checkout totals not established. No checkout opened. | [Pricing](https://mole.fit/#pricing): `native-price` |
| Licence | Native retail licence is non-exclusive, non-transferable and perpetual, with two same-platform concurrent activations and deactivation/reactivation allowed. CLI GPL does not cover the native app or website images. | [Terms](https://mole.fit/terms): `native-terms`; repository License section: `native-license`, `cli-license` |
| Trial/refund | Docs say scanning stays free; Clean, Software, Optimize and Analyze Trash actions each work twice without purchase. Homepage offers refund within 14 days with Payment ID; refunded key deactivates. Not tested. | [Docs](https://mole.fit/docs), homepage FAQ: `native-trial`, `refund` |
| Documentation scope | Docs explicitly warn that some features are in the Preview build and arrive with the next release. Qualify fine-grained behavior, or map it to a release before publication. | Docs opening: `docs-preview` |

Price and availability require review within 30 days and again before publication if stale. Do not convert `$` to a verified ISO currency or infer unlimited devices from “unlimited use.”

## Workflow and comparison matrix

The machine-readable claim ledger has **30 exact source excerpts**, source URLs, check dates, scope, intended location and evidence class (including three retry-investigation claims). `verified` means the quoted documentation/offer supports the bounded wording, **not** that we ran the app.

| Dimension | Mole evidence | Breathing Room evidence / limits |
| --- | --- | --- |
| Scan/cleanup | Native Clean lists categories, leftovers and System Data; backups, iCloud files, VMs and models appear under Manage Separately outside the cleanup total. CLI purge targets rebuildable project artifacts. `native-clean`, `cli-purge`. | Same-day capabilities register supports source storage/owner views, not full distributed-release parity. `breathing-preview`. |
| Approval/removal | Native caches permanently delete by default; Settings can use Trash. Analyze's context-menu move is immediate, unlike Clean's full-list review. CLI clean/purge/installer can permanently delete; clean empties user Trash by default unless protected. `native-delete`, `native-analyze`, `cli-delete`. | Source daily care binds exact saved approvals; interactive optional automatic Ruff-cache mode is a separate exception. No blanket “never deletes without asking” promise. `breathing-care`. |
| Developer costs | Native docs leave rebuild-cost caches/output unselected for review; CLI purge leaves recent or unverifiable-activity candidates unselected and documents permanent deletion. Do not copy CLI rules onto native Clean. `native-rebuild`, `cli-purge`. | Source adapters depend on installed owning tools and native validation; not every cache/tool version has runtime certification. See capabilities developer/builder row. |
| Local/hosted | Vendor says scans/cleanup and files/results stay local. Activation/update FAQ names network destinations; this is not a network-free-app or telemetry audit. `native-local`, `activation-network`. | Local inspection and execution; authenticated hosted AI can send relevant paths, process/storage information and tool outputs off-device. `breathing-caveats`; capabilities local/hosted register. |
| Process grouping | Published v1.15 notes describe grouping by app with combined CPU/memory and expandable details. `native-grouping`. | Source grouping exists, but inferred ownership is imperfect. Do **not** frame grouping as unique to Breathing Room. Capabilities Apps row. |
| Recurring growth/care | Clean feature page describes an on-demand workflow without scheduled reminders/background disk scanning. That is **not** absence of monitoring: v1.18 Preview describes growth since an older Analyze map, naming growing folders/files. `native-on-demand`, `native-growth-preview`. | Daily care uses saved approvals while app remains running; advertised within paid AI Care. Native execution/end-to-end entitlement not established. `breathing-care`, `breathing-price`. |

All Breathing Room evidence is reused from `docs/content/capabilities.md`, reviewed the same day, not re-scraped or newly runtime-tested. It identifies **0.1.0-preview.1**, macOS 13+, advertised universal installer with physical Intel untested, Python **3.10+**, Apple Development signing but **no Developer ID signing or notarization**. Free local core is distinct from optional authenticated hosted AI Care, advertised at **$5 USD/month or $50 USD/year**. Website download registration is distinct from public GitHub releases. Do not suppress these caveats or give instructions to bypass protections.

## Visual handoff and hard blocker

### Mole: official app UI reference, link-only

- Source page: <https://mole.fit/mac-cleaner>.
- Exact app asset: <https://mole.fit/img/en/clean.jpg>.
- The retained HTML identifies an actual Clean-tab image, not a landing-page screenshot or logo: alt text “Clean tab showing Earth and the space a scan found, with a button to review the results.” Declared size: **2584 × 1741**, not independently decoded dimensions. Responsive WebP references also exist.
- Vendor capture date, app version and capturer: **unknown**. No asset bytes were downloaded, so original/published hashes are **null**, not fabricated.
- Proposed credit: **Mole / Tw93; official Clean-tab visual**. Proposed caption: “Mole's official Clean-tab visual. Vendor illustration; version and capture date not supplied. No measured result from our testing.”
- Reuse basis: **link-only**. [Terms §3](https://mole.fit/terms) reserve ownership of content to Tw93; no screenshot licence/permission was found. Public visibility is not permission. The raw HTML is evidence of the source/asset reference, not visual approval.

**Precise drafting blocker:** permission/licence for this exact screenshot is unresolved. EDITORIAL requires an on-page competitor UI image, and its link-only research fallback explicitly does not waive that gate. The CLI retry below also remains unresolved. Obtain retained permission or a published licence covering a qualifying exact asset, then download only the permitted asset, preserve/hash original bytes, decode and inspect it, review privacy and prepare accessible placement. Do not send permission outreach from this scheduled job. No other competitor's assets or website records are owned here.

### Explicitly requested retry: CLI visual and non-mutating capture investigation

The retry reused the whole existing packet and batch-1 material facts. It did **not** request the reserved-rights native `clean.jpg` again. Only missing CLI visual-rights and execution-feasibility source data were retrieved. Source bodies, exact UTC retrieval timestamps, final URLs and SHA-256 values are retained under `sources/` and in `research.json`. All fetched scripts were treated as untrusted text, never executed.

Pinned official tree: **`84dc779dc651ff1f0509a2054b6e25b8fb5d2ac5`**, from <https://api.github.com/repos/tw93/Mole/git/trees/main?recursive=1>. This pins the inspected source; it does not certify the newest stable CLI release. The entrypoint contains `VERSION="1.62.0"`, a source constant only, not an installed-version observation.

**Official CLI asset candidate (link-only, not visually approved):**

- Source: <https://github.com/tw93/Mole/blob/84dc779dc651ff1f0509a2054b6e25b8fb5d2ac5/README.md>.
- Exact asset: <https://raw.githubusercontent.com/tw93/Mole/84dc779dc651ff1f0509a2054b6e25b8fb5d2ac5/docs/img/big-mole.png>.
- README excerpt: `<img src="./docs/img/big-mole.png" alt="Mole cleanup results" width="1000" />`. This establishes an official candidate reference, not independently verified image contents, measurements or capture provenance.
- Upstream Git blob SHA-1: `5b7e0bea82ad2d298a34fc44655634782b4e5b14`. This is **not** an original downloaded SHA-256. No image bytes were fetched; decoded dimensions, version, capture date, capturer, privacy, final alt text and original/published hashes remain unknown.
- Proposed credit: **Mole CLI / Tw93; official repository README visual**. If permitted and inspected, caption must distinguish publisher output from our tests and the free CLI from the paid native GUI.
- Licence evidence: the same README says “Mole is open source under GPL-3.0; see LICENSE” and calls Mole for Mac “a separate proprietary app.” The pinned [LICENSE](https://github.com/tw93/Mole/blob/84dc779dc651ff1f0509a2054b6e25b8fb5d2ac5/LICENSE) is GPL version 3. No image-specific licence scope/permission was identified in the inspected tree, README or LICENSE. Those documents establish the CLI code licence, **not sufficient explicit permission for this particular image under this job's gate**. This is unresolved, not a claim that permission is legally impossible or that the image is definitively excluded from GPL.

**Genuine non-mutating capture route:** `command -v mo` and `command -v mole` returned no path (shell exit 1); no installation search outside PATH or software installation was attempted. Inspected the pinned entrypoint plus `lib/core/common.sh`, `commands.sh`, `base.sh`, `help.sh` and `log.sh` as source data. The relevant startup chain is:

1. [Entrypoint](https://github.com/tw93/Mole/blob/84dc779dc651ff1f0509a2054b6e25b8fb5d2ac5/mole) sources `lib/core/common.sh`, then registers `trap cleanup_temp_files EXIT INT TERM`, **before** `main` dispatches `--help`.
2. [common.sh](https://github.com/tw93/Mole/blob/84dc779dc651ff1f0509a2054b6e25b8fb5d2ac5/lib/core/common.sh) lines 16–17 source `base.sh` and call `prepare_mole_tmpdir > /dev/null`. It also sources additional modules; the complete transitive execution closure was not audited.
3. [base.sh](https://github.com/tw93/Mole/blob/84dc779dc651ff1f0509a2054b6e25b8fb5d2ac5/lib/core/base.sh) lines 1297–1358 prepare/probe temporary roots and can call `prune_stale_mole_temp_files "$MOLE_RESOLVED_TMPDIR"`. Lines 1230–1262 restrict that deletion routine to dedicated Mole cache/temp roots, but it can remove stale files there. Lines 1417 onward implement exit cleanup. **Do not imply every help invocation deletes files**; the point is that a help flag alone does not establish a wholly non-mutating path.

Consequently this retry did not run even `--help`, install software, extract a help function into a fake terminal screenshot, stub application dependencies, or render README example output as though it were a genuine capture. No browser, cookie extraction or Chrome recovery was needed. No claim of hands-on testing or safe execution follows from source inspection.

**Exact evidence/decision needed to unblock:** either (a) a published image-specific licence or retained owner permission covering the pinned `docs/img/big-mole.png`, with reproduction scope and attribution/redistribution conditions, followed by permitted retrieval/hash/decode/privacy/visual review; or (b) an independently audited and explicitly authorized genuine no-install/no-cleanup CLI capture path, with output reuse rights established and version/OS/procedure/raw capture retained. This job does not authorize changing those constraints. The native Clean asset needs its own explicit clearance if chosen instead. No permission outreach was sent.

**CLI-only brief option:** keep canonical owner/slug `mole`, title **“Breathing Room vs Mole CLI: artifact review and removal choices.”** Scope Mole feature rows to retained CLI documentation; the native $19/two-Mac app is separately labeled context, not CLI pricing or a capability demonstrated by a CLI image. The workflow brief can narrow to CLI purge selection/rebuild/removal decisions, with native Clean only a bounded edition note. This is a future handoff, **not** a waiver of the competitor-image gate or a second doorway page. Drafting remains blocked.

### Breathing Room: selected current-source preview

- Reuse `current-space-browser-preview` from `docs/content/screenshots.json`.
- Existing asset: `docs/content/assets/breathing-room/space-preview-2026-10-21.png`; **2940 × 3468**; SHA-256 `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a`.
- Captured `2026-10-21T19:06:45.416416+00:00`, source commit `54828ac3170b45861aee70861dd0b9c658ed7e51`, browser `http://127.0.0.1:1431/`. This is current-source evidence as recorded, not a current native release capture.
- Caption must remain: **“Current-source Breathing Room Space browser preview, captured October 21, 2026. Example data only; not a native scan, measured activity or cleanup result.”**
- Alt: “Breathing Room Space view rendered in a browser with illustrative example data.”
- Basis: app-owner-requested first-party UI capture; no blanket rights to third-party marks inferred. Original remains shared and unchanged; no publication copy exists.
- Opened and read the actual PNG in this research job: example-data banner, categories and Projects & development row are visible; assistant composer overlaps part of the category view. Keep disclosure visible, and review readable contextual presentation rather than shrinking the whole tall image. No crop was made. Per-article responsive/theme/privacy review remains pending.

## Distinct workflow article brief

**Title:** Before purging Mac build artifacts: review rebuild cost, age and removal method  
**Slug:** `review-mac-build-artifacts-before-purging`  
**Track:** search/reference workflow, not a renamed comparison or untested executable tutorial.

**Reader job:** distinguish original project state, generated output, dependency downloads and caches before approving removal. Use the documented differences between CLI purge and native Clean to explain rebuild cost and permanent deletion versus Trash. Do not execute commands or claim tested recovery.

Lead with the decision boundary; put the official Mole app view immediately after the lead **only when rights are cleared**. Then cover:

1. Generated versus irreplaceable data; lockfiles do not by themselves guarantee an offline or identical rebuild.
2. CLI purge's documented selection/age boundaries and permanent deletion, scoped to retained README, not an invented stable version.
3. Native Clean's review-only defaults and Preview-specific additions; do not treat CLI and native app as identical.
4. Backup, active work, disk-access limitations, time/bandwidth and removal-destination checklist.
5. Current-source Breathing Room Space preview as the later figure, with full example-data/native limitation labels.
6. One bounded recommendation: **“Breathing Room, which we build”**, followed by its preview, Python, signing and hosted-service caveats. Mole's free inspectable CLI and native paid app remain valid choices.

**Interaction pass handoff:** a static decision checklist (original/generated, sources available, active project, offline rebuild, Trash/permanent) is more useful than a forced code sandbox. It must not pretend to scan files. Link to `/comparisons/mole/`, `/comparisons/` and a relevant existing tool only after the drafting worker confirms routes. Roughly 900–1500 words if earned; no invented FAQ or benchmark.

## Concise comparison brief

**Title:** Breathing Room vs Mole: native app, CLI and care workflows  
**Comparison slug:** `mole`.

Answer the choice first, disclose affiliation, separate the native $19/two-Mac offer from free GPL CLI, then use a compact source-adjacent matrix: platform, price/licence, approval/removal, developer costs, disk analysis, process grouping, growth/care and local/hosted boundary. Link to the deeper workflow rather than repeating it. Do not add another alternatives route without distinct intent.

**Mole advantages/trade-offs:** free inspectable terminal toolkit; proprietary native all-in-one update/uninstall/analyze/monitor UI with one-time licensing; existing grouping and Preview growth comparisons. Removal modes differ and can be permanent. No independently tested speed, safety or savings advantage established.

**Breathing Room fit/trade-offs:** source-implemented category/owner exploration, local history and exact-approval daily care may fit someone investigating repeat growth. It remains an unnotarized maintenance preview with Python prerequisite, unverified binary parity and optional paid hosted AI. Do not imply it is production-ready, entirely offline or an established full app-uninstaller replacement.

## Unknowns, validation and handoff

Noncritical unknowns are retained rather than represented as “No”: CLI newest stable version, native architecture/signing, currency/tax totals, telemetry beyond the vendor local-scan statement, and feature-by-feature stable/Preview parity. Omit or explicitly qualify those claims. The image-rights blocker is critical and **blocks drafting**, even though the research has useful briefs and verified claims.

- Retry: ran `python3 docs/content/competitors/mole/build-packet.py`: **PASS**, 30 claim excerpts match retained evidence, 17 source records assembled, retained source hashes checked and selected preview hash matched. Additional structural/hash checks are in `validation.json`.
- Actual selected Breathing Room PNG opened with image-capable reader; example labels and overlap inspected. Competitor image not downloaded or visually approved.
- Packet structural/hash validation is recorded in `validation.json`; no marketing build or native tests apply because neither website nor app implementation changed.
- No independent reviewer score assigned. No cleanup, settings changes, account creation, messages, purchases, commits, pushes, deployments or queue/database mutation.
- Owned outputs are confined to `docs/content/competitors/mole/` and the required job receipt. Resume drafting only after the precise visual permission/access gate is resolved.
