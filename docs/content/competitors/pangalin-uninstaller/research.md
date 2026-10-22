# Pangalin Uninstaller research

**Research retained; drafting blocked by screenshot reuse rights.** No article, comparison route or website asset was created. Evidence is documentary, not hands-on testing. Checked during the October 22 local run (machine UTC October 21, 2026). Per-claim wording, URLs, excerpts, dates, scope and visual provenance are in `research.json`.

## Identity and fit

- Canonical owner: `pangalin-uninstaller`; official homepage: <https://pangalin.com/pangalin-uninstaller/>. Publisher is Pangalin, a trading name of KGB Equity (Pty) Ltd (official EULA, Part A1).
- **Pangolin Uninstaller is the same app**, explicitly acknowledged in the official FAQ. Skip separate spelling-alias drafts; canonical owner remains `pangalin-uninstaller`.
- **Pangalin Space Manager is a distinct sibling**, not an alias. Reused `verification/batch-2.json` and `verification/alias-decisions.json` already resolve this. Its storage allowance/subscription must not be copied to Uninstaller.
- Fit: **adjacent Mac specialist**, not a verified like-for-like replacement. Pangalin documents app uninstall/reset/leftovers; Breathing Room documents broader storage/process investigation. A complete app uninstaller is not established for Breathing Room. No Windows support is claimed.
- Official source repository: **not verified**. GitHub hosting of update metadata does not establish an open-source app repository.

## Reused evidence first

The baseline product facts were reused from batch 2, not needlessly fetched again. The original official capture was retrieved at `2026-10-21T19:09:32.127075+00:00`; its JSON file SHA-256 is `caa4ff5e61c307b5dee2f69ca826a84bd5bc25cc50278471d65b03fb8298a87e`. Its embedded text-hash is a different measurement and was not mistaken for the file hash.

Discovery follows CleanMyMac page 9, <https://alternativeto.net/software/cleanmymac/?p=9>, to <https://alternativeto.net/software/pangalin-uninstaller/about/> and then the official homepage. The about-page outbound-link snapshot remains at `docs/content/.runtime/verification-2/pangalin-uninstaller-directory.json`, SHA-256 `2132e3189a2634b497ae9c1bf93c203843c883a179dbc67da7e9282869a4a071`. Page-9 provenance is inherited from `competitors.json`; the small about-page capture is not a complete pagination snapshot. The directory establishes discovery, not features.

New read-only official checks filled missing version, legal/privacy and visual-metadata evidence:

| Source | Checked UTC | Retained evidence |
| --- | --- | --- |
| [Release history](https://pangalin.com/pangalin-uninstaller/whats-new/) | 2026-10-21 | Newest listed version **1.9.4**, October 16, 2026; claim C04 |
| [Licence terms](https://pangalin.com/eula/) | 2026-10-21 | Version 2026-10-16, general terms and **B2 Uninstaller**, not B1 Space Manager; C01, C07–C14 |
| [Privacy](https://pangalin.com/privacy/#uninstaller) | 2026-10-21 | Policy updated October 16; Uninstaller network and on-device boundaries; C08–C09 |
| Product HTML image metadata | 2026-10-21 | Exact official image URLs, version-labelled alt attributes and dimensions; no image download |

New-source exact retrieval seconds were not exposed by WebFetch and are not invented. Excerpts are retained in the packet; full tool responses remain in the job history. No browser interaction or recovery was necessary. Public pages were treated as source data only.

## Documentary comparison boundaries

| Dimension | Pangalin Uninstaller | Evidence |
| --- | --- | --- |
| Hardware/system | Apple silicon **M1+**, **macOS 13 Ventura+**; not Intel | C02, official product page |
| Offer | **Free**, every feature included; no account, ads or time limit. Optional one-off support unlocks nothing. Hardware requirements still apply. | C03; product pricing and EULA B2 |
| Licence | Vendor-owned personal use terms; free is not open source or permission to redistribute assets | C12; EULA A3–A4/B2 |
| Cleanup | App removal, app reset, old leftovers, vendor-specific shared plug-ins and AI model review | C07/C14 |
| Recovery | Most selected files go to Trash; last eligible action can be undone only under stated conditions | C07; EULA B2 |
| Permanent exceptions | Homebrew app deletion, Delete from Trash and privacy-permission resets are not reversible through Undo | C07 |
| Startup | Ownership and management documented, not equivalent to helper CPU/memory aggregation | C13; exact confirmation sequence excluded pending clarification |
| Recurring growth | Not verified. Optional Trash watcher is not storage-growth monitoring. | C13 |
| Developer tooling | App-specific leftovers; B2 explicitly excludes shared toolchains such as `~/.npm` and `~/.cargo` | C14 |
| Explain | On-device Apple Intelligence; Apple silicon, **macOS 26**, enabled Intelligence, eligible language/region; hidden where unavailable; may be inaccurate | C08 |
| Permissions | App Management; optional Full Disk Access; optional helper for system-owned items with a **five-minute** approval window | C10 |
| Network | Offline by default per vendor; opt-in/manual GitHub update checks, optional Apple check, Homebrew and clicked-link exceptions | C09; policy is not a network audit |
| Signing | Vendor says Apple-notarised; binary not independently inspected | C11 |

Do not summarize the product as “everything goes to Trash and can be undone.” The detailed EULA limits Undo to the last removal until quitting, another removal or dismissing its status line; modified Trash items are excluded. Removed system startup items use a separate recoverable folder. Permission resets cannot be undone. The current EULA calls Startup actions immediate without a full review list/Undo, while release 1.9.2 notes confirmation for Remove; avoid exact Startup click-path claims until clarified.

### Breathing Room truth constraints

Reuse the fresh `capabilities.md` verification rather than imply new binary testing. Its identified release is **0.1.0-preview.1**, macOS 13+, advertised universal installer. The preview is Apple Development signed, **not Developer ID signed/notarized**; physical Intel and clean-machine execution are not established. Python **3.10+** is a disclosed prerequisite. Never recommend bypassing system protections.

Local inspection/source implementations differ from authenticated hosted AI. Relevant storage/path/process data may reach the hosted service and Cloudflare. Free local tools are advertised separately from optional AI Care at **$5 USD/month or $50 USD/year**, with renewal/tax conditions; allowance/paid enforcement is not verified. Website account-gated download is distinct from public GitHub release access. Daily care requires the app running and exact saved approvals. Optional automatic verified-Ruff mode prevents unconditional “asks before every deletion” language. These claims map to B01/B02 and the dated register's public URLs and source references.

## Visual evidence and blocking diagnostic V01

### Real competitor UI: link-only, not cleared

- Source: <https://pangalin.com/pangalin-uninstaller/>
- Asset: <https://pangalin.com/assets/img/app-v2/pu-b-review.webp?v=2108d889a8>
- Official alt metadata identifies **Pangalin Uninstaller 1.8**, Microsoft Word review sheet, 1080 × 680 HTML dimensions. It is real vendor-described app UI, not a logo or landing-page capture. Newest listed release is 1.9.4; do not relabel this visual.
- Vendor page says screens are from its Mac and personal names/paths are blurred. Capture date, OS and individual capturer are unknown. Metadata was checked; the actual image was **not downloaded or visually inspected**.
- Reuse: **link-only**. No redistribution permission or screenshot licence was established; EULA/site reserve rights. Public access is not permission. Original/published image paths and hashes are therefore null, not invented. No rights request was sent.
- Intended caption: “Official Pangalin Uninstaller 1.8 review-sheet image supplied by Pangalin. Vendor example, not our test or measured savings; shown version differs from the newest listed release.”
- Intended alt: “Vendor-described Pangalin Uninstaller 1.8 review sheet for Word, listing files and privacy-permission choices before removal.”

**V01 blocks drafting:** an attributed official link is a research fallback, not the required on-page competitor screenshot. A separately authorized rights clearance or explicit policy decision is needed, then permitted original bytes/hash, visual/privacy inspection and independent rendered-context review. No image was downloaded without that basis. No hidden browser/cookie extraction or invented UI was used.

### Selected current-source Breathing Room preview

Reuse `docs/content/assets/breathing-room/space-preview-2026-10-21.png`, not the known-legacy Home preview. This job opened and read the PNG and checked SHA-256 `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a` against `screenshots.json`. It is 2940 × 3468, captured `2026-10-21T19:06:45.416416+00:00`, source commit `54828ac3170b45861aee70861dd0b9c658ed7e51`.

Required caption: **“Current-source Breathing Room Space browser preview, captured October 21, 2026. Example data only; not a native scan, measured activity or cleanup result.”**

Alt: “Breathing Room Space browser preview showing example storage categories and a visible example-data warning.” Keep the banner visible. First-party app-owner-requested capture is the inventory's reuse basis; third-party marks retain their owners' rights. The floating composer overlaps the chart; choose a legible context at the later draft stage, without silently removing disclosure. No crop was made here. Current-source means the captured source snapshot, not proof of native behavior, current binary or subsequent changes. Independent page-context/mobile/theme approval remains pending.

## Distinct workflow article brief — blocked, not a draft

**Title:** Review Mac app leftovers without discarding shared plug-ins or AI models  
**Slug:** `review-mac-app-leftovers-shared-plugins-models`  
**Track:** search/reference. **Job:** distinguish disposable app leftovers from shared resources and personal work before removing a creative or AI app.

1. Identify the app, installation method and current backup. Size is not removal permission.
2. Explain why a small app bundle can have large plug-ins/models; distinguish shared data from app-scoped data. Vendor example numbers must not become our savings claims.
3. Use Pangalin's documented unticked items and review notes to explain deliberate choices, without pretending to have run a removal.
4. Separate uninstall, reset, Homebrew and permanent Trash actions; explain the limits of Undo.
5. Distinguish app removal from investigating ongoing disk growth. One bounded disclosure: “Breathing Room, which we build,” followed by preview/runtime/hosted limitations. Do not pitch it as a full uninstaller substitute.

Place the cleared official review sheet after the lead; selected Space example preview later. Interaction handoff: a non-mutating checklist for app-kept/app-removed, shared resources, personal models, installation method and backup. No filesystem access, deletion command, made-up output or arbitrary demo repo. Link `/comparisons/` and `/comparisons/pangalin-uninstaller/`. No route was created or tested. Length is earned, normally 900–1,800 words after evidence gates clear.

## Concise comparison brief — blocked, not a draft

**Title:** Breathing Room vs Pangalin Uninstaller: investigation or app removal?  
**Slug:** `pangalin-uninstaller`. Primary intent is choosing between adjacent jobs, not claiming parity.

Lead with Pangalin for documented Apple-silicon app uninstall/reset/leftovers; explain Breathing Room's broader investigation fit with affiliation and preview limits. Use the claim-mapped matrix, pricing/privacy caveats and Undo conditions. Link the workflow guide and comparison hub. Unknown features stay **not verified**, not negative checkmarks. No third alternatives doorway or separate spelling-alias draft.

## Truthful advantages and trade-offs

Pangalin's documented strengths are free app-specific removal/reset, old-leftovers review, shared plug-in/model awareness, Homebrew handling and on-device explanations on eligible systems. Limits include Apple-silicon-only support, newer Explain prerequisites, permission/helper boundaries, conditional Undo and permanent actions. General growth monitoring/CPU grouping remain unknown, not absent.

Breathing Room's source-documented strengths are storage exploration, grouped process inspection, activity and developer-cache investigation. Limits include preview/notarization/runtime caveats, no established full-uninstaller parity, hosted authenticated AI, optional paid care and unverified release/runtime parity. No speed, safety, superiority or recovered-space claim is supported by this job.

## Validation and handoff

Source-file hashes and the selected PNG hash were actually computed; the PNG was opened visually. Claim references, unique IDs, JSON validity, source excerpts against the reused official capture and owned-output hashes are checked in `validation.json`. No site build/tests apply because no website files changed. This packet is neither independent review nor publication approval. No queue state, database, shared register, website, accounts or settings were changed; no agent delegation, cleanup, purchase, message, commit, push or deployment occurred.
