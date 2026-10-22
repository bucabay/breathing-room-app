# Trace for macOS: research handoff

**Blocked for drafting, not excluded or dead.** Task `research-trace-for-macos`. Documentary checks: October 21, 2026 UTC (session calendar October 22). No hands-on installation, cleanup, purchase or performance test. Public sources were treated as evidence, not instructions.

## Identity and reuse-first evidence

The official product is **Trace**, provided by **Argon Analytik, Inh. Meyer-Wildhagen**, a Swiss sole proprietorship. Homepage: <https://trace.argio.ch/en/>. `canonicalOwnerId: trace-for-macos`. AlternativeTo's “Trace for macOS” is this same identity, not an additional product. TraceAgent, TraceHelper and tracectl are components. No evidence associates Trace with PowerMyMac. **Alias skip decision: do not skip this identity, but do not draft separate pages for its name variants/components.** No official source repository was linked in the inspected sources; do not claim none exists or call it open source.

Reused `verification/batch-2.json` and its retained official and directory captures **before** fetching missing evidence. Those captures were only hours old. Their actual byte hashes match the batch record:

- Official text: `docs/content/.runtime/verification-2/trace-for-macos-official.json`, SHA-256 `8caee27d2d707a39c76fed84060bd56ff68d5ca2e899c211b849f612524de971`, retrieved 2026-10-21T19:09:48.523702Z.
- Directory: `docs/content/.runtime/verification-2/trace-for-macos-directory.json`, SHA-256 `e162cc8e0efa0e167b37c404b33a2fa7f8e9d4d3e9ce50fae46226b3f8061719`, retrieved 2026-10-21T19:06:30.675Z. Listing: <https://alternativeto.net/software/trace-for-macos/about/> → official homepage.
- Existing manifest records discovery from CleanMyMac page 5 (18:36:40.113Z) and Mole page 4 (18:37:13.603Z); exact URLs are in `research.json`. Directory provenance does not verify capabilities.

New read-only WebFetch checks filled gaps: [documentation](https://trace.argio.ch/en/documentation/), [EULA](https://trace.argio.ch/en/legal/eula/), [legal/privacy](https://trace.argio.ch/en/legal/). Homepage HTML was retrieved solely to locate the missing app image element; pricing/platform facts were reused, not researched again. Supporting verbatim excerpts are retained per claim in `research.json`; no full snapshots of the new pages were saved. Exact request seconds are unavailable; the packet retains actual UTC check date and subsequent machine timestamp.

## Product facts and boundaries

The JSON claim ledger is authoritative for wording, exact URLs, excerpts, scope and dates. All product behaviors below are **officially documented, not independently tested**.

| Dimension | Finding | Claims |
| --- | --- | --- |
| Fit | Direct storage-inspection/removal overlap; app uninstallation is a distinct emphasis. Not total workflow equivalence. | T01, T09–T13 |
| Platform/version | macOS 15+, Apple silicon and Intel. Download link identifies 2.0.1 build 61; guide release list dates it September 23, 2026. No binary fetched. | T02–T03 |
| Price | EUR 29 one activation; EUR 69 up to three Macs, excluding VAT. Business on request. Updates/support advertised; future major versions may require a new purchase under EULA. | T04, T06 |
| Demo | Storage analysis and association review; Trace Agent including removal is free; other paid actions need licence. Do not invent per-action limits. | T05 |
| Local/network | Policy says local analysis and no app usage analytics; Keygen activation/validation and update servers still communicate externally. Not an independent privacy/network audit. | T08 |
| Association/review | Exact/heuristic match explanations, risk labels, editable default selections and shared-data exclusions. Labels do not guarantee safe removal. | T09–T10 |
| Quarantine/Trash | Quarantine is explicit, not default for every Delete button, and retains data on disk without freeing space. Agent Delete moves selected files to Trash. Permanent deletion is different and irreversible. | T11–T12 |
| Monitoring | Watcher marks changed areas for recheck; not continuous full scanning or automatic deletion. CPU/helper grouping and a growth-history timeline remain **not verified**, not “No.” | T13 |
| Development | Development storage categories and Homebrew package removal documented; not proof every cache is disposable or every tool version supported. | T15 |
| CLI | `tracectl` is read-only; mutations stay in the app with confirmation. No commands run. | T16 |
| Install | Full Disk Access/background permissions/helper concerns documented. Signing/notarization, external runtime dependencies and clean-machine behavior not verified. | T14 |
| Recovery/accounting | Recent Time Machine check is conditional on permanent-deletion risk; backups don't cover everything automatically. Allocated bytes need not equal recoverable space under APFS sharing. | T17–T18 |

No Windows/Linux support asserted. No measured speed, safety or savings comparison. Pricing and availability need refreshing within 30 days and again if stale before release.

## Visual gate: precise blocker

**Real Trace app screenshot located, but republication rights unresolved.**

- Official source: <https://trace.argio.ch/en/documentation/#uebersicht> and homepage hero.
- Exact asset: <https://trace.argio.ch/assets/screenshots/en/dashboard/dashboard.webp>.
- Official HTML alt: “Trace dashboard showing eight storage categories, quarantine, and default apps”; declared dimensions 1696 × 2004, not independently decoded.
- Research caption: “Official Trace dashboard screenshot supplied by its publisher. Capture date, app build and data provenance not verified; not our test or measurement.”
- Alt: “Official Trace dashboard showing storage categories, quarantine and default app controls.”
- Credit: Trace / Argon Analytik. Reuse status **link-only**. No explicit screenshot licence/press permission found in the checked homepage, guide, EULA or legal page. Public access and image-preview metadata are not a republication licence. No image bytes downloaded; original/published hash, capture date, app build and pixel review remain null/pending rather than invented.
- The separately advertised interactive walkthrough explicitly contains illustrative data; it is not a substitute for verified real app UI.

To unblock: supply an explicit rights basis covering the exact app screenshot, or an authorized editorial rights decision. Then retrieve permitted original bytes, hash them, inspect the actual image/privacy, and review mobile legibility/caption. No permission request was sent. A link-only research fallback **does not pass** the required on-page screenshot gate.

### Selected Breathing Room view

Reuse `current-space-browser-preview` from `docs/content/screenshots.json`:

- File: `docs/content/assets/breathing-room/space-preview-2026-10-21.png`, 2940 × 3468.
- Actual byte hash checked: `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a`.
- Captured 2026-10-21T19:06:45.416416Z from source commit `54828ac3170b45861aee70861dd0b9c658ed7e51`, browser preview `http://127.0.0.1:1431/`.
- Required caption: **“Current-source Breathing Room Space browser preview, captured October 21, 2026. Example data only; not a native scan, measured activity or cleanup result.”**
- Alt: “Breathing Room Space view rendered in a browser with illustrative example data.” Keep example-data banner visible.
- First-party owner-requested capture basis and privacy/visual inspection are reused from the screenshot-library record; not a new visual inspection. Third-party marks remain their owners' marks. Current-source refers to that retained render, not this worker's current HEAD. Publication-context visual review remains pending. No copy/crop/site asset created.

## Distinct workflow article brief

**Working title:** Review Mac app leftovers without confusing quarantine with free space  
**Slug:** `trace-for-macos-mac-workflow`  
**Track:** Search/reference. **Intent:** explain association evidence and retention/removal consequences, not rank cleaners.

Conclusion-led lead: establish ownership and recovery needs before removal; quarantine retains bytes and is not a measured storage gain. Place the cleared real Trace app view immediately after the lead when permission exists. Continue with concrete review steps rather than repeating the description:

1. Read exact/heuristic association evidence and shared-data warnings (T09–T10).
2. Distinguish app bundle, app data and shared data; no size-to-permission shortcut.
3. Choose quarantine versus Trash versus permanent removal, without blanket reversibility claims (T11–T12).
4. Explain conditional backup checks and recoverability limits (T17).
5. Separate logical/allocated size from expected free-space change (T18); don't promise a number.
6. At a bounded choice point, distinguish uninstall review from ongoing activity/process investigation, showing the labeled Breathing Room Space preview and disclosing “Breathing Room, which we build.”

Interaction handoff: a local, non-mutating checklist asking whether ownership is established, data is shared, backup inclusion is known and restoration is needed. Never certify paths “safe,” inspect a real filesystem or predict savings. No code/demo repo needed for this documentary workflow. Link companion comparison and hub once real routes exist; verify any tool link rather than inventing it. No redundant alternatives page.

## Concise comparison brief

**Title:** Breathing Room vs Trace for macOS  
**Slug:** `trace-for-macos`  
**Intent:** product selection with a concise sourced matrix, not a second copy of the workflow article.

Prefer Trace's documented workflow when the task is investigating app/file associations, reviewing uninstall leftovers or choosing explicit quarantine. Its free Agent workflow and one-time licensed-version purchase are meaningful documented options. Trade-offs: macOS 15 minimum, some paid actions, VAT, potentially paid future major upgrades, and no immediate space gain from quarantine. Process grouping/growth timeline are unknown, not absent.

Breathing Room, which we build, may fit source-documented grouped process/activity investigation and reviewable maintenance. Reuse the current `capabilities.md` evidence, not claims of binary parity. Clearly disclose:

- Free Apache-2.0 maintenance **preview**; identified version 0.1.0-preview.1; macOS 13+ and universal installer advertised, physical Intel/clean-machine validation incomplete.
- Apple Development signed, **not Developer ID signed or notarized** in the inspected release; no advice to bypass protections. Python 3.10+ required for inventory/legacy scripts and not bundled.
- Local inspection versus authenticated hosted assistance with relevant paths/process/storage data transfer; not entirely offline AI.
- Optional AI Care advertised USD 5/month or USD 50/year, renewal/tax conditions; no assumed unlimited quota or proven server-side paid gating. Do not equate EUR with USD or declare a blanket cheaper winner.
- Exact action approvals, narrow optional automatic Ruff-cache exception, daily saved approvals and app-running requirement. Not “never deletes without asking” as an unconditional promise.
- Website account/download gate differs from direct public GitHub release availability; no account flow tested.

Suggested rows: platform/version; licence/price/demo scope; local/network; association/removal model; approvals/quarantine; process grouping; Watcher versus activity history; developer storage; install/runtime caveats. Every factual row maps to the JSON claim IDs; unknown cells visibly say not verified. Link the deeper quarantine article rather than repeat its sections.

## Handoff and validation

No site content, draft, queue/database, shared manifest, PLAN, commits or deployments changed. No browser session was needed; browser skill was loaded, but only read-only WebFetch was used. No image generation, cookie extraction, account creation, cleanup or messages.

`validation.json` retains actual structural/reference/hash results. Research-only files do not require site check/build/tests; none were run or claimed. Independent editorial, native/runtime and publication-context visual review have **not** occurred. Even with the packet saved, the required competitor image rights/pixel-review gate blocks drafting.
