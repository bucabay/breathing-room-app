# Purge research packet

**Research complete; not publication approval.** Job `research-purge`. Public evidence was checked on **2026-10-21 UTC** (the scheduled local date is October 22). No installation, cleanup, native test, account creation or website edit was performed. `research.json` is the claim/provenance ledger; unknown fields are not negative findings.

## Decision and identity

Proceed with a bounded Mac workflow draft and concise comparison. **Canonical owner: `purge`**. Official homepage: <https://purgemac.com/>. Official repository: <https://github.com/jithin-sabu/purge-app>, by Jithin Sabu. The directory, homepage and repository cross-link the same identity. “Purge for Mac” is descriptive naming of this product: **skip a separate alias draft**, not the product itself. No evidence connects this repository to PowerMyMac. Do not borrow facts from another Purge product or the macOS `purge` command.

Fit is **direct macOS storage-cleanup overlap**, not equivalence across every feature. Purge documents tool caches, project artifacts, app removal and optional schedules. Breathing Room’s source register additionally supports app/helper activity investigation; Purge’s equivalent process grouping and recurring-growth attribution are **not verified**, not “No.” No Windows or Linux support is claimed for either tool.

The GitHub latest-release API returned **v1.12.0**, published **2026-10-20T12:40:24Z**, neither draft nor prerelease, with DMG and checksum asset records. This establishes a public offer, not successful download/install or binary integrity. Architecture support and installer size remain unverified. The baseline homepage documents **macOS 13+**, a **free offer with no trial or paid tier**, and MIT licensing. No paid currency, billing period or checkout is applicable to that documented free offer; device limits were not established.

## Reused discovery and source provenance

Reused `docs/content/verification/batch-2.json`, record `purge`, before additional research. Did **not** refetch the current verified homepage or AlternativeTo page. Original about-page retrieval: **2026-10-21T19:05:29.670Z**, owned Chrome tab 16 in the prior job, not a tab operated here.

Discovery: <https://alternativeto.net/software/purge/about/> → <https://purgemac.com/> and the repository above. Manifest edges:

- CleanMyMac seed <https://alternativeto.net/software/cleanmymac/> via <https://alternativeto.net/software/cleanmymac/?p=10>, retrieved 2026-10-21T18:36:56.904Z.
- Mole seed <https://alternativeto.net/software/mole/> via <https://alternativeto.net/software/mole/?p=8>, retrieved 2026-10-21T18:37:24.218Z.

Retained original evidence and SHA-256 checks:

| Snapshot | SHA-256 |
| --- | --- |
| `docs/content/.runtime/verification-2/purge-directory.json` | `8bebe5d64614af39f4cf2506412d0c87f45bbd42bb00218bb8cc27c73ad1d102` |
| `docs/content/.runtime/verification-2/purge-official.json` | `01b0962aee8ba175ecf85661206097062da9e08176d37e64f196d45510ccde5a` |

New missing-material sources, retrieved about 21:58–21:59 UTC on October 21, are saved byte-for-byte under `sources/`, with exact URL, redirect destination, timestamp, HTTP status and SHA-256 in each `.meta.json`:

- **README:** <https://raw.githubusercontent.com/jithin-sabu/purge-app/v1.12.0/README.md> → `sources/readme-v1.12.0.txt`. Tagged documentation is the version scope, not current main-branch claims. Main README was also read as a discovery lead; claims use the retained tagged copy.
- **MIT notice:** <https://raw.githubusercontent.com/jithin-sabu/purge-app/v1.12.0/LICENSE> → `sources/license-v1.12.0.txt`.
- **Availability/release:** <https://api.github.com/repos/jithin-sabu/purge-app/releases/latest> → `sources/release-latest.json`; human release <https://github.com/jithin-sabu/purge-app/releases/tag/v1.12.0>.
- **Safety:** <https://purgemac.com/safety/> → `sources/safety.txt` (original HTML). Used to identify qualifications/conflicts, not as a guarantee of safety.
- **Breathing Room:** reused current `docs/content/capabilities.md` and `docs/content/screenshots.json`, both reviewed October 21. Their paths/hashes, public URLs and original-source locators remain in the JSON. This research does not re-certify their binary/runtime unknowns.

## Claim ledger and comparison boundaries

All entries below were checked October 21 UTC. Full proposed wording, per-claim URLs, exact excerpt, locator, conditions, reviewer and state are in `research.json`. Documentary verification is **not** observed behavior.

| ID | Supported wording / retained excerpt | Source and scope |
| --- | --- | --- |
| P01 | Official identity, “Purge on GitHub” links to `jithin-sabu/purge-app`. | Reused homepage links + directory; identity only. |
| P02 | “Yes. No license, no trial, no paid tier, nothing bundled in.” | Reused homepage free-offer answer; “no license” means no purchased licence, not absence of MIT terms. |
| P03 | “macOS 13+”. | Reused homepage platform line; no architecture inference. |
| P04 | `tag_name: v1.12.0`, `published_at: 2026-10-20T12:40:24Z`. | Release API; latest at retrieval only. |
| P05 | “Copyright (c) 2026 Jithin Sabu”; permission includes associated documentation. | Tagged LICENSE; retain full notice and warranty disclaimer. |
| P06 | “Purge does not use AI. Nothing you scan or clean is sent to an AI service.” | Tagged README Privacy; vendor describes local operation and update checks, not independently audited. |
| P07 | “Files and folders go to the Trash by default, and Purge never empties the Trash”. | README note/cleaning; simulators, runtimes and local snapshots are permanent exceptions; Apple Intelligence models use asset service, documented for macOS 27/Apple silicon. |
| P08 | “Nothing is removed until you review and confirm”. | README Large Files/duplicates; Clean Selected has confirmation. Not a promise about enabled automatic cleaning. |
| P09 | “Purge sends a local reminder and cleans safe items when you open the app”. | README Cleaning; weekly/monthly/three-month/custom intervals. Homepage says optional scheduling and deleted-app review are off by default. |
| P10 | “Developer projects: `node_modules`, Python virtual environments, Rust `target`”. | README Dev Tools; also Xcode/Homebrew/npm/pnpm. Active-project and stale-worktree rules documented, not tested. |
| P11 | “review a per-app sheet that lists every item with its path and size and a safety label”. | README App Uninstaller; optional off-by-default leftover watcher can operate when app is quit. Do not confuse watcher with schedule. |
| P12 | “Large Files and the app scans need Full Disk Access; without it only App Caches and Dev Tools scan”. | README Overview; qualified category boundary, not full scan without permission. |
| P13 | “Purge is notarized by Apple”. | README Installation, attributed only; no binary inspection. Homebrew/DMG and Sparkle documented. Xcode CLI optional for full simulator listing. Xcode 16/Node 18+ are source-build/icon prerequisites, not installed-app requirements. |
| P14 | “It is read only and moves nothing.” | v1.12.0 release, Everything else map; do not call all storage cleanup candidates. |
| P15 | “May be safe, but could cause inconvenience”. | README safety-label table. Vendor labels do not independently establish no data risk or rebuild cost. |
| B01 | “AI Care is advertised at $5 USD/month or $50 USD/year”. | Capabilities conclusion/pricing: free Apache-2.0 local app, optional hosted service; renewal/tax conditions apply. |
| B02 | “Path-derived ownership and sampled writes are not proof of the writer of a specific file”. | Capabilities Apps/Activity rows; grouping/history implementation, not a runtime benchmark. |
| B03 | “Apple Development signed, not Developer ID signed or notarized”. | Capabilities preview table: identified `0.1.0-preview.1`, macOS 13+, Python 3.10+ inventory dependency; physical Intel/clean-machine untested. |
| B04 | “relevant paths/process/storage data can reach the service and Cloudflare Workers AI”. | Capabilities hosted boundary; authentication/internet required for hosted AI. No entirely-offline-AI or blanket all-data-local claim. |
| B05 | “Automatically move verified Ruff lint caches to Trash”. | Capabilities approval exception; narrow optional interactive mode. Daily care instead reuses exact approvals while app runs. |

### Conflicts and honest unknowns

- Homepage generic “never deletes permanently” conflicts with its own explicit exceptions and tagged README. **Reject the generic claim**, use P07. Directory “nothing is ever lost” is discovery text, not usable product truth.
- README installation/requirements broadly request Full Disk Access, but Overview and homepage specify categories that work without it. Use P12; no permission behavior was tested.
- Safety-page generic “nothing is lost” is undermined by its detailed warnings (for example archives, simulator data and Docker volumes). Protected-category prose and listed explanation names also overlap. Do not generalize from either section to an absolute no-loss/never-touch guarantee. A rule-specific tutorial would require tagged implementation review before drafting that claim.
- Neither Trash movement nor category size demonstrates newly available disk blocks. No numbers in either screenshot are our test results. No cleanup was run.
- Purge architecture, binary notarization validation, actual installation, performance, runtime privacy audit and equivalent process/growth monitoring are noncritical unknowns **only because the brief omits or qualifies them**.
- Breathing Room current-source features do not establish distributed preview parity, production readiness, physical Intel support testing or successful paid service activation. Keep these caveats in the draft.

## Real visuals and reuse conditions

### Purge: official Overview app image

- Source page: <https://github.com/jithin-sabu/purge-app/blob/v1.12.0/README.md>, line 38.
- Exact original asset: <https://raw.githubusercontent.com/jithin-sabu/purge-app/v1.12.0/Assets/github-hero.png>.
- Downloaded **2026-10-21T21:59:13.769722+00:00** to `assets/github-hero-v1.12.0.original.png`, **1600 × 900**, **958018 bytes**.
- Original SHA-256: `9d7e5c45ba033e543ed8bb51d936873dfb5a7ce3460af8534e37498ddac387e7`.
- Opened and visually read with the image tool: a real Overview window is embedded in vendor hero artwork; visible category rows include App Caches, Dev Tools, Large Files, installed apps, leftovers and Everything else. The bottom of the window is cropped in the vendor original. No private account/path was visible. This is not merely a landing-page capture or logo.
- Reuse basis: root MIT licence covers repository software and associated documentation; this asset is embedded by the tagged README. **Retain `sources/license-v1.12.0.txt` in full** with published reuse, including Copyright (c) 2026 Jithin Sabu, permission notice and disclaimer. Do not imply endorsement or a separate licence to third-party marks. Caption adjacent credit is required in addition to the licence notice.
- Caption: **Official Purge Overview image supplied in its v1.12.0 repository. Vendor illustration, not our scan or measured cleanup result. Purge / Jithin Sabu, MIT licence.**
- Alt: **Purge Overview app window with App Caches, Dev Tools, Large Files, app removal and Everything else storage rows.**
- Vendor capture date, exact captured app build and OS are unknown; presence in tag is not proof of capture version. Promotional safety headline is vendor wording, not editorial endorsement. No edits or published copy were created; published hash remains null until a draft actually copies/transforms it.

### Breathing Room: current-source Space preview

- Selected record `current-space-browser-preview` from `screenshots.json`.
- Existing source: `docs/content/assets/breathing-room/space-preview-2026-10-21.png`; capture **2026-10-21T19:06:45.416416+00:00**, source commit `54828ac3170b45861aee70861dd0b9c658ed7e51`, browser URL `http://127.0.0.1:1431/`.
- **2940 × 3468**; hash matched: `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a`. Opened and read again in this research job; no new capture or server was started.
- Required caption: **Current-source Breathing Room Space browser preview, captured October 21, 2026. Example data only; not a native scan, measured activity or cleanup result.**
- Required visible labels: **Interactive preview · example data** and **This browser preview uses example data. Actions never change your Mac.** Preserve both if cropping; never relabel as native data. The composer overlaps part of the chart; review legibility in the actual draft layout.
- Alt: **Breathing Room Space view rendered in a browser with illustrative example data.**
- First-party app-owner-requested UI capture; preserve existing provenance and trademark limitations. No hosted asset URL applies to this local original; published destination/hash pending. Source-current at capture, not proof of current installer UI. No earlier/legacy preview substituted.

## Distinct workflow article brief

**Title:** Review stale developer artifacts before clearing Mac storage  
**Planned slug:** `purge-mac-workflow`  
**Track:** Search/reference; reader job is deciding whether a project artifact is reproducible, actively used, orphaned or original data, not finding the longest feature list.

Conclusion: review ownership and rebuild cost before selection. Purge documents stale-project and orphaned-worktree filters; age is not permission to discard work. Start with the official app visual after the lead, then:

1. Separate global tool caches, project output and original files (P10).
2. Explain documented activity/staleness/worktree exclusions without promising infallibility. Check uncommitted work and agent/terminal activity.
3. Ask whether dependencies can be downloaded/rebuilt, especially offline; do not equate a safety label with zero inconvenience (P15).
4. Separate Trash, permanent simulator/snapshot operations and actual available-space change (P07).
5. If storage repeatedly grows, consider investigation rather than repeating cleanup. Use the labeled Breathing Room Space view; disclose “Breathing Room, which we build,” with source/native/hosted limitations (B02–B05).

Interaction handoff: a non-mutating checklist—known owner, active use, original/reproducible, dependencies available, uncommitted work checked, Trash/permanent path understood. No scan button, delete command, invented savings or forced demo repository. Link the existing `/comparisons/` hub and the planned `/comparisons/purge/` counterpart only after checking actual draft links.

## Concise comparison brief

**Title:** Breathing Room vs Purge for Mac  
**Planned route:** `/comparisons/purge/`  
**Intent:** choose between documented local, non-AI cleaning and a preview combining storage, activity and hosted assistance. Use a concise sourced matrix rather than repeating the workflow article.

- **Choose Purge’s documented workflow** when free non-AI cleanup, app-removal review, developer artifacts and optional scheduling are the requirement (P02, P06, P09–P11). The vendor also documents notarization (P13); distinguish this statement from independently checking an installer.
- **Consider Breathing Room, which we build,** for source-backed app/helper CPU-memory grouping and activity investigation alongside storage (B02). Disclose non-notarized preview, Python requirement, authentication/hosted data boundary and optional AI price (B01, B03, B04). Do not promise production readiness or forensic attribution.
- **Fair trade-offs:** Purge has scheduling and cleanup history; do not invent their absence. Breathing Room’s full-uninstaller parity is not established. Purge’s process grouping/growth attribution remains unverified. Neither tool has been installed/tested here; no benchmark, guaranteed safety or space-recovered claim is supported.

## Handoff gates

Identity, Mac relevance, scoped documentary claims and two genuine product visuals are established for these bounded briefs. **No critical research blocker remains for that scope.** Research completeness does not approve publishing. Drafts must remain unpublished, preserve both visual disclosures/rights notices and receive independent claim/rendered-visual review. Changed-site checks/build/tests belong to the later authorized stage; none were run for this research-only packet.

The reproducible local validation is `python3 docs/content/competitors/purge/validate-packet.py`; its actual results are retained in `validation.json`. The assembly helper first encountered a baseline-key mismatch (`products` versus actual `records`), was corrected, and then succeeded; no source evidence was changed. No queue/database/shared-file state was updated.
