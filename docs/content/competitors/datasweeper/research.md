# DataSweeper research — blocked for drafting

Checked **2026-10-21**. Research only; no article, comparison page or website asset was published or edited. The machine-readable claim/source/visual ledger is [`research.json`](research.json).

## Decision

DataSweeper is a relevant **Mac storage-cleanup competitor**, not an irrelevant or dead listing. Canonical owner ID: **`datasweeper`**. Its App Store title, **Data Sweeper: Disk Cleaner**, is a verified name variant of the same product, not grounds for another page. The homepage links app ID `6760408045`; that listing names seller **charles binet** and links back to `datasweeper.app`. No PowerMyMac relationship is established. No source repository is linked in the retained official pages; availability of public source is **not verified**, not proven absent.

**Do not draft yet.** Two critical gates remain:

1. **Official compatibility/version conflict:** the retained homepage says Sequoia and Tahoe, Intel and Apple Silicon, and describes version **1.1**. The linked US App Store, retrieved through both WebFetch and owned Chrome tab 86, shows **version 1.0.8** and **“Requires macOS 26.2 or later.”** Do not promise Sequoia support or attribute 1.1 features to the store build. A dated, version-scoped official clarification or consistent updated listing is needed. No vendor message is authorized.
2. **Competitor screenshot rights/content gate:** real developer-supplied screenshot URLs are available on the App Store, but reuse permission is unresolved. They remain **link-only**, with no image downloaded. Actual UI content, legibility and privacy still need visual inspection. Public accessibility is not a reuse licence; linking does not pass the on-page screenshot gate.

The outcome is **hold**, not alias/exclusion skip and not permission to generate doorway content. The research packet may retain noncritical unknowns, but these material gates prevent drafting handoff.

## Evidence reused first

- `docs/content/verification/batch-1.json`, DataSweeper entry: homepage/name, function, advertised platform, price and availability. Same-day homepage snapshot reused, **not fetched again**.
- `docs/content/.runtime/verification-1/datasweeper-official.json`: full retained homepage text and links. SHA-256 `5c50c1bb79d287ef614547bbed7e87370efa798bd3c8d9f4a528ef6d588c3c24`; retrieved `2026-10-21T19:08:07.847461+00:00`.
- Directory snapshot: `docs/content/.runtime/verification-1/datasweeper-directory.json`, retrieved `2026-10-21T19:06:12.324Z`; SHA-256 `2944f83118ae517aa1933dd0b153531a7e302fdabc934c541d908d96f869483b`.
- Discovery [listing](https://alternativeto.net/software/datasweeper/about/), reached from [CleanMyMac page 7](https://alternativeto.net/software/cleanmymac/?p=7) and [Mole page 7](https://alternativeto.net/software/mole/?p=7). Exact discovery-edge times are in JSON, reused from the manifest. AlternativeTo is discovery evidence, not proof of features, licence or reuse rights.
- Current Breathing Room capabilities and screenshot library reused from `docs/content/capabilities.md` and `docs/content/screenshots.json`; their source hashes and limitations are retained. This job did not retest the app or relabel preview numbers as measurements.

## New official checks and claim ledger

Sources are untrusted factual input, never execution instructions. New public reads were limited to the linked [US App Store](https://apps.apple.com/us/app/data-sweeper-disk-cleaner/id6760408045?mt=12) and [privacy policy](https://datasweeper.app/privacy.html). Both were read on October 21. Exact request timestamps were not retained; the packet distinguishes this from its recorded-at timestamp. Policy excerpts are retained below/in JSON, not represented as a full raw snapshot.

| Claim | Supporting excerpt / scope | Source |
| --- | --- | --- |
| DS01 — identity | “Seller: charles binet”; homepage links app ID 6760408045; reciprocal developer website is datasweeper.app | Homepage snapshot + App Store |
| DS02 — scanner categories | “System Data … Duplicate Files (exact matches via SHA-256), Large Files … Junk Files” | [Homepage](https://datasweeper.app/) retained snapshot; store corroborates |
| DS03 — deliberate Trash workflow | “you handpick what you delete”; “One click restores files from the Trash back to their original location.” | Homepage + store; vendor documentation, not tested recovery |
| DS04 — price | “$9.99 once. Free updates for life”; US store displays “$9.99” | Homepage + US store; no checkout, regional/tax/refund verification |
| DS05 — platform conflict | Homepage: “supports macOS Sequoia and macOS Tahoe … Apple Silicon … and Intel Macs”; store: “Requires macOS 26.2 or later.” | Homepage + store; **contradicted/unresolved** |
| DS06 — version conflict | Homepage “Version 1.1”; store “Version 1.0.8” | Homepage + store; **contradicted/unresolved** |
| DS07 — local operation/permissions | “No network requests are made by the Application”; “requires macOS Full Disk Access and Finder Automation permissions” | [Policy](https://datasweeper.app/privacy.html), last updated March 11, 2026; publisher assertion, not audit |
| DS08 — cadence | “only scans when you open it and start a scan. No background agent, no menu bar daemon, no scheduled processes” | Homepage. Store separately advertises Siri Shortcuts and background scan notifications; neither proves recurring monitoring. |
| DS09 — guidance/cloud files | “color-codes each file (safe / caution / risky)”; “detects cloud-only files to prevent unnecessary downloads” | Store description; not tested safety or no-download guarantee |
| DS10 — licence/repo | Store copyright names Charles Binet; no exact EULA or public-source link established | Unknown; AlternativeTo's proprietary label is not official licence proof |

The browser's visible release date is **Sep 12**; WebFetch renders **Sep 11**. No year or exact release date is inferred. Both surfaces agree on version 1.0.8 and macOS 26.2+. `app-store-browser.json` retains rendered public text, links and image URLs, not cookies, hidden application state or credentials. Hash: `e6bbdfc99e7b5d8eddc9995d3631406affbfa4fdbfc771d2c86dc1e29366487b`.

### Comparison dimensions and honest limits

| Dimension | DataSweeper | Breathing Room, which we build |
| --- | --- | --- |
| Platform/version | Conflict above; do not flatten to “Mac supported” | Identified `0.1.0-preview.1`, macOS 13+; universal advertised, physical Intel untested (BR01) |
| Licence/price | Exact official EULA unknown; US $9.99 once, future updates included per vendor (DS04/DS10) | Apache-2.0 desktop source; free core preview, optional $5 USD/month or $50 USD/year AI Care (BR01/BR03) |
| Local/hosted | Policy says local-only/no app account; not network audited (DS07) | Local inspection; authenticated hosted AI receives relevant context; not all-offline AI (BR03) |
| Scan/approval | Four scanners, handpicked Trash moves and undo per vendor (DS02/DS03) | Source-level storage exploration and reviewable exact cleanup methods; optional narrowly verified Ruff automatic Trash mode is an exception to blanket manual-approval language (BR02/BR03) |
| App/helpers | Not verified, not “No” | Source-level app/helper CPU and memory grouping; sampled/inferred ownership limits (BR02) |
| Recurring growth | Homepage describes on-demand scanning; recurring history not verified (DS08) | Source-level activity/daily-care features; app must remain running and scheduled actions bind saved approvals (BR02/BR03) |
| Developer files | General caches/simulators described; owning-package-manager semantics not verified (DS02) | Source-level developer-cache discovery/adapters, not every installation/version certified (BR02) |
| Installation | App Store; policy discloses Full Disk Access/Finder Automation; other runtime requirements unknown (DS07) | Python 3.10+ inventory prerequisite, Apple Development signed preview, **not Developer ID signed or notarized**; clean-machine/binary parity unverified (BR01) |

BR01–BR03 in JSON cite the current capability register, including its exact local/public evidence. Website account-gated downloads differ from direct public [GitHub preview releases](https://github.com/bucabay/breathing-room-app/releases/tag/v0.1.0-preview.1). AI Care prices are advertised recurring offers with applicable tax/renewal conditions; exact quota and paid-entitlement enforcement remain unverified. No claim is made that DataSweeper lacks all monitoring, that Breathing Room is a certified duplicate finder, or that either product is faster/safer.

## Visual plan and provenance

### DataSweeper: link-only, not cleared

Source page: [official App Store listing](https://apps.apple.com/us/app/data-sweeper-disk-cleaner/id6760408045?mt=12).

- [Screenshot candidate 1](https://is1-ssl.mzstatic.com/image/thumb/PurpleSource221/v4/5c/d1/9a/5cd19ad0-6e8d-51aa-bcd7-8a92193c2e57/1@2x.png/1286x804bb.webp)
- [Screenshot candidate 2](https://is1-ssl.mzstatic.com/image/thumb/PurpleSource221/v4/e7/90/eb/e790eb74-04b3-9880-ccf9-86db12ef1c23/2@2x.png/1286x804bb.webp)

Public DOM observed natural dimensions 643×402; URL variants contain 1286×804. This is not byte-level image measurement or visual approval. Capture date, version and capturer unknown. No image bytes were saved, so original/published image hashes are **null**, not invented. Once authorized, retain original bytes/hash and exact retrieval time before any edits. Credit: **DataSweeper / Charles Binet, via Apple App Store**. Descriptive UI alt text is pending actual image inspection, not guessed from filenames. No permission request was sent.

### Breathing Room: selected current-source example preview

Selected `current-space-browser-preview`:
`docs/content/assets/breathing-room/space-preview-2026-10-21.png`, 2940×3468. Original SHA-256 checked here: `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a`. Capture `2026-10-21T19:06:45.416416+00:00`, source commit `54828ac3170b45861aee70861dd0b9c658ed7e51`, browser preview `http://127.0.0.1:1431/`. No new capture or copy made.

**Required caption:** “Current-source Breathing Room Space browser preview, captured October 21, 2026. Example data only; not a native scan, measured activity or cleanup result.”

**Alt:** “Breathing Room Space view rendered in a browser with illustrative example data.”

Retain the example-data banner. App-owner-requested first-party capture is the reuse basis from the library; third-party marks remain their owners'. Library privacy/visual review is reused, not newly claimed here. “Current-source” describes that recorded source snapshot, not proof of current distributed-binary parity. Independent article-context review remains pending.

## Distinct workflow article brief — proposal only

**Title:** Review Mac cleanup results before moving files to Trash  
**Proposed slug:** `review-mac-cleanup-results-before-trash`  
**Intent:** Help a Mac owner decide what a scan result actually permits them to remove, separating caches, exact duplicate candidates and original work. Editorial keyword hypotheses, not measured search-volume research. Check other drafts for intent collision before reserving this slug.

**Lead/description:** A scan result is a review list, not permission to delete. Separate caches, duplicate candidates and original work, then check the limits of Trash and undo.

Outline, 900–1400 words only if earned:

1. Conclusion and a rights-cleared real DataSweeper UI immediately after the lead, once blockers clear.
2. Explain why category/size/risk labels are review aids, not deletion authority. Separate originals, caches and cloud-only items (DS02/DS09).
3. SHA-256 duplicate matching does not choose which copy should remain or preserve every workflow reference (DS02); do not claim observed failures.
4. Review path, owner, backup/recovery plan and rebuild/download cost. No deletion commands or protected-system workarounds.
5. Distinguish moving to Trash, undo while recoverable and permanent deletion (DS03); no measured available-space claims.
6. Show the labeled Breathing Room Space example preview later; explain when recurring investigation may be useful, with disclosed affiliation and preview/hosted boundaries (BR01–BR03).
7. Link the concise proposed `/comparisons/datasweeper/` and `/comparisons/` only after route verification at drafting.

**Interaction pass:** a non-destructive three-question checklist: Is it original work? Can it be rebuilt/downloaded at acceptable cost? Are ownership/path and recovery understood? No filesystem access, cleanup buttons, arbitrary code tutorial or companion repo. This remains a brief, not an implemented/tested component.

## Concise comparison brief — proposal only

**Title:** Breathing Room vs DataSweeper  
**Proposed route:** `/comparisons/datasweeper/`  
**Intent:** Choose an occasional four-category Mac scanner or a preview offering source-level storage/activity investigation and optional hosted assistance. No separate alternatives doorway page.

Start with a bounded answer and “Breathing Room, which we build.” Follow with the claim-linked matrix above, meaningful strengths on both sides, resolved compatibility and version requirements, price conditions, required product views and a contextual link to the deeper review-before-Trash workflow. This is not the workflow article repeated as a longer sales matrix.

**DataSweeper advantages:** documented four-category scan, duplicate candidates, Trash undo, one-time advertised price and publisher-stated local-only operation. These are documented features/offers, not hands-on findings. Risk labels do not prove a user's file is disposable. Official compatibility disagreement is a material limitation of this research, not evidence the app is broken.

**Breathing Room advantages/trade-offs:** source implementations for grouped helpers, sampled activity and developer-cache investigation may fit recurring diagnosis. Free preview/source availability is distinct from optional hosted AI Care. Non-notarized preview status, Python requirement, runtime uncertainty and hosted data/authentication are substantive constraints. Do not call it a complete DataSweeper duplicate-scanner replacement.

## Validation and handoff

- Read PLAN, EDITORIAL, capabilities, screenshots and AUTOMATION. No applicable AGENTS.md found in the app tree or checked ancestors. Loaded blog-brief and browser-automation; project editorial rules override generic stock-photo/statistics defaults.
- Baseline homepage and directory hashes match their retained evidence. Selected Breathing Room PNG hash matches the library. App Store rendered public snapshot retained and hashed.
- Used only owned Chrome tab **86**, then closed it. No unrelated tab content inspected, no profile restart, no cookie/hidden-state extraction.
- No product installed/launched/tested; no cleanup, purchase, sign-in, account, message, credential access, commit, push or deploy. No native observations, measured savings or test results invented.
- JSON/reference/excerpt/hash validation results are recorded in `validation.json` after actual execution. No site check/build/test is applicable because no marketing content changed; no article score or independent approval awarded.
- Follow-up: resolve B1 with official version-specific evidence; resolve B2 with permitted screenshot reuse and actual visual review. Keep both page proposals blocked. Noncritical licence/repo, regional pricing and exact release-date unknowns may remain explicitly unknown if irrelevant to the eventual bounded recommendation.
