# Radix research packet

**Research complete; no article, site change or publication approval.** Job: `research-radix`. Canonical owner: `radix`. Actual public retrievals: October 21, 2026 UTC (October 22 local job date). Original baseline check times are preserved rather than relabeled.

## Decision

Radix is a relevant, distinct Mac storage product. Retain it as a **direct storage-workflow comparison**, not a claim that it substitutes for every Breathing Room feature. Do not skip this product or create an additional old-domain article.

- Official identity: **Radix**, Colin Kim, [tryradix.app](https://tryradix.app/).
- Official repository: [colinvkim/Radix](https://github.com/colinvkim/Radix).
- Former official domain: `radix.colinkim.dev` redirected to `tryradix.app` in the reused verification.
- `canonicalOwnerId: radix`; `skipSeparateDraft: false`. Consolidate the former/current homepage identities. Nothing checked establishes a PowerMyMac relationship; this job does not adjudicate that other product’s aliases. Do not confuse this analyzer with unrelated Radix UI tooling.
- **No critical research blocker** for the bounded documentation-led briefs below. Unknown runtime behavior and unverified features must remain unknown, not negative feature claims. Independent draft/visual approval remains pending.

## Discovery and source retention

First reused `docs/content/verification/batch-2.json`, record `radix`, including the official identity, macOS requirement and free offer. The homepage and AlternativeTo pages were **not re-fetched**. Missing licence, version, architecture, detailed workflow and image evidence were checked in the official repository and release API.

Discovery followed [Mole alternatives, page 4](https://alternativeto.net/software/mole/?p=4) to [Radix’s exact listing](https://alternativeto.net/software/radix/about/). The existing rendered listing was retrieved `2026-10-21T18:37:13.603Z`; about-page DOM was retrieved `2026-10-21T19:05:36.572Z`; the official homepage redirect was retrieved `2026-10-21T19:09:38.009021+00:00`.

The original baseline outer-file hashes were checked before copying their bytes into `sources/discovery-edge-reused.json`, `sources/discovery-reused.json` and `sources/homepage-reused.json`. The inner homepage JSON also contains a separate hash field; that is not substituted for the verification register’s outer-file SHA-256.

`research.json` is the detailed claim/source/visual ledger: every claim has wording, source ID, exact source URL where public, supporting passage, check time, scope, state and intended placement. Source snapshots and their hashes are retained under `sources/`; `sources/retrievals.json` records actual new HTTP retrievals and final URLs. Local first-party documents have app-relative paths and hashes rather than invented public source URLs.

### Primary evidence

| Source | Scope and supporting passage |
| --- | --- |
| [Official homepage](https://tryradix.app/) (reused) | “Scans and saved results stay local, with no account required.” “Open source and free forever.” Vendor statements, not network or future-price guarantees. |
| [Pinned official README](https://github.com/colinvkim/Radix/blob/e320bd6a02217a454fa39796387449211ffd4c01/README.md) | “Compare two scans to see which files and folders grew, shrank, appeared, or disappeared.” Documents sunburst/treemap views, Quick Look, Discard Pile, read-only `.radixscan` snapshots and permission limitations. |
| [Pinned MIT licence](https://github.com/colinvkim/Radix/blob/e320bd6a02217a454fa39796387449211ffd4c01/LICENSE) | Copyright 2026 Colin Kim; permission covers software and associated documentation files, conditional on retaining the notice. Full text retained in `sources/LICENSE.txt`. |
| [Latest-release API](https://api.github.com/repos/colinvkim/Radix/releases/latest), [v1.8.0 release](https://github.com/colinvkim/Radix/releases/tag/v1.8.0) | API returned non-draft, non-prerelease **v1.8.0**, published `2026-09-20T02:18:13Z`. Notes specify macOS 14.0+ universal Intel/Apple silicon download and discuss clone allocation, comparison and Discard Pile. No binary downloaded or installed. |
| `docs/content/capabilities.md`, current local `README.md`, `RELEASE_NOTES.md`, native/billing configs | Reused current public checks and rechecked local caveats, price, runtime and version. Source implementation, published disclosures and binary testing remain separate evidence classes. |

## Exact conditions and matrix handoff

Each row maps to the named claim IDs in `research.json`; cite those sources next to the eventual cells. A missing feature is **not verified**, never “No.”

| Dimension | Radix | Breathing Room | Claim IDs |
| --- | --- | --- | --- |
| Platform/version | macOS Sonoma **14+**. Latest API result **v1.8.0**, universal Intel/Apple silicon. | Documented **0.1.0-preview.1**, macOS **13+**, universal; physical Intel runtime untested. | `macos`, `release`, `br-preview` |
| Price/licence | Advertised free, no paid billing conditions documented; MIT source/documentation. “Free forever” is the vendor’s wording, not our guarantee. | Free core desktop source/app; Apache-2.0 app source. Optional **$5 USD/month or $50 USD/year** AI Care, recurring, applicable tax at checkout; allowances/enforcement unverified. | `free`, `license`, `br-price`, `br-license` |
| Local/hosted/account | Vendor says scans/results local, no account required. Not a zero-network audit. | Local inspection; hosted AI requires internet/sign-in and can transmit questions/tool output including paths. Website download registration differs from public GitHub access. | `local`, `br-runtime`, `br-hosted` |
| Storage model | Sunburst/treemap, file browser, filtering, Quick Look. | Category, app/tool, project, folder and large-file views; partial/cached inventories possible. | `maps`, `search`, `br-space` |
| Change over time | Compare two scans and save/reopen read-only `.radixscan` snapshots. | Sampled activity/history, with coalesced/missed events and inferred ownership limitations. Do not claim native `.radixscan` parity. | `compare`, `snapshots`, `br-activity` |
| Review/cleanup | Collect candidates in Discard Pile and review before choosing Trash moves. | Review exact locations/methods; optional narrowly validated Ruff-cache automatic mode qualifies blanket approval language. | `review`, `br-approval` |
| App/helper monitoring | Not verified. | Documented app/helper CPU and memory grouping; sampled activity is not proof of a particular writer. | `unknown-radix-monitoring`, `br-activity` |
| Recurring monitoring/care | Continuous monitoring not verified; scan comparison is documented. | Source/documented activity context and saved-approval daily care while app runs; not wake-after-quit execution. | `unknown-radix-monitoring`, `br-activity`, `br-daily` |
| Developer caches | Package-manager-specific adapters not verified. Generic folder inspection is not such an adapter. | Source register documents multiple cache discovery adapters, subject to tool availability and native validation. | `unknown-radix-dev`, `br-dev` |
| Install/runtime/coverage | Documented Homebrew cask or release download to Applications. Some folders may require Full Disk Access. Signing/notarization and independent runtime behavior not verified. | Unbundled **Python 3.10+**; permission-limited inventory; Apple Development signed, **not Developer ID signed or notarized** preview. | `install`, `permissions`, `unknown-radix-signing`, `br-runtime`, `br-preview` |

The Radix build-from-source requirement (Xcode 26 / Swift 6.2) must **not** be mislabeled an end-user dependency. Pinned main documentation is not proof every change ships in v1.8.0. Release notes independently substantiate the comparison/Discard Pile workflow and compatibility. No Mac, Windows or Linux runtime was tested here.

## Visuals and reuse

### Radix: official scan-comparison UI

- Source: [official README, Compare Scans Over Time](https://github.com/colinvkim/Radix/blob/e320bd6a02217a454fa39796387449211ffd4c01/README.md#compare-scans-over-time).
- [Exact immutable asset URL](https://raw.githubusercontent.com/colinvkim/Radix/e320bd6a02217a454fa39796387449211ffd4c01/docs/images/radix-scan-comparison.png).
- Original: `assets/radix-scan-comparison-original.png`; SHA-256 `81dc1eba56c260ca3d943adc01949e7e68635308657c343b56deda8b57a82fc4`. Original bytes retained; no edits or published copy.
- Downloaded `2026-10-21T22:02:19.198536+00:00`. Vendor capture time, app build and OS version are unknown; the repository commit is not the depicted binary version.
- Reuse basis: official repository documentation asset under the retained MIT licence covering associated documentation files, with no exception stated in the inspected README/LICENSE. **Distribute the full retained notice/disclaimer with the image and credit “Radix screenshot © 2026 Colin Kim, MIT License.”** This does not infer trademark endorsement or blanket rights to third-party marks.
- Actually opened and read: Storage Changes table, earlier/later scans and a prominent unreadable-locations warning. Public author username and Library paths are visible; no credentials or file contents identified. Publication privacy/context review is still required.
- Caption: “Official Radix scan-comparison screenshot, supplied in its repository documentation. Figures are vendor illustration, not our scan, a benchmark, or measured cleanup results. The visible warning notes unreadable locations; missing entries are not necessarily deleted.”
- Alt: “Radix Storage Changes window comparing earlier and later scans, with folder-level increases and decreases and a limited-coverage warning.”
- Keep that warning readable. Use a full-size link or carefully documented contextual crop during drafting; do not turn screenshot totals into claimed space savings.

### Breathing Room: selected current-source Space browser preview

- Reuse registry ID `current-space-browser-preview`, source `docs/content/assets/breathing-room/space-preview-2026-10-21.png`.
- SHA-256 `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a`; checked against actual bytes. No redundant download/copy.
- Captured `2026-10-21T19:06:45.416416+00:00`, source commit `54828ac3170b45861aee70861dd0b9c658ed7e51`, browser preview at `http://127.0.0.1:1431/`. No native capture or new browser run performed by this job.
- Required caption: “Current-source Breathing Room Space browser preview, captured October 21, 2026. Example data only; not a native scan, measured activity or cleanup result.”
- Required alt: “Breathing Room Space view rendered in a browser with illustrative example data.”
- Actually opened and read: both example-data disclosures are visible. Keep them. First-party owner-requested capture is the reuse basis; third-party app marks remain their owners’. “Current-source” means its recorded capture/commit, not newest binary parity.

Both images have full structured provenance, original hashes, review notes and limitations in `research.json`. Published paths/hashes remain null because no website asset has been created. They are research selections, not an independent visual/publication pass.

## Distinct workflow article brief

**Title:** Find what grew on your Mac with saved Radix scans  
**Proposed slug:** `compare-mac-storage-growth-with-radix-snapshots`  
**Track:** Search/reference workflow. **Intent:** investigate changed storage between comparable scans, not simply list large files or rank cleaners.

1. Lead with when a two-scan comparison answers the question. Immediately show the official Radix comparison view; disclose documentation-led guidance, not hands-on testing.
2. Define a baseline: chosen target, scan time, coverage and exclusions. Retain a completed `.radixscan` snapshot.
3. Compare a later scan and inspect grew/shrank/appeared/disappeared results. Check unreadable locations before treating missing entries as deletion.
4. Inspect a changed branch with search, filtering, Quick Look and Finder context. A folder’s size or growth does not establish its owner or disposability.
5. Review Discard Pile candidates; explain backups, rebuild/download costs, Trash versus available space, and the release’s APFS clone caveat. Do not perform cleanup for evidence.
6. Explain when Radix is sufficient. Only then introduce “Breathing Room, which we build,” for documented activity/helper context, with preview, Python, hosted-data and optional-price boundaries. Use the labeled Space preview as the second visual.

**Interaction handoff:** a read-only checklist: same target, comparable exclusions, unreadable locations, shared allocation, known ownership, rebuild cost? Unresolved answers mean investigate, not delete. No executable cleanup code, fake demo, arbitrary signup or invented FAQ. Link to `/comparisons/radix/` and the hub. Link a relevant tool only after its real route and function are verified by the drafting job.

## Concise comparison brief

**Title:** Breathing Room vs Radix: ongoing context or saved-scan comparison  
**Proposed route:** `/comparisons/radix/`  
**Intent:** choose between documented Mac storage workflows; not a second alternatives doorway.

Lead: Radix fits visual exploration and saved-scan comparisons. Breathing Room, which we build, adds documented app/helper and activity context, but remains a non-notarized preview and uses hosted AI for agent features. Follow with the compact sourced matrix, “when Radix is enough,” “when activity context helps,” runtime/privacy/price caveats, unknowns and a link to the distinct workflow article.

**Honest advantages:** Radix documents two map styles, portable read-only snapshots, no-account local scans, free availability and MIT source. Breathing Room documents broader activity/helper context and free local tools. **Trade-offs:** Radix needs macOS 14+, comparisons depend on coverage and are not process attribution; several ongoing-care features are not verified, not absent. Breathing Room has preview/signing/Python/Intel-validation constraints, hosted-data exposure and optional recurring AI Care. No winner, speed, safety or measured-savings claim is supported.

## Handoff gates and validation

- Research can proceed to bounded drafting; no critical missing identity, relevant workflow, price condition or visual-source/reuse evidence remains.
- Noncritical unknowns: Radix screenshot capture/version/OS, signing/notarization, independent runtime/network behavior, continuous/helper monitoring and developer-cache adapters; Breathing Room binary parity, clean-machine/Intel tests and exact hosted allowances.
- Do not silently promote those unknowns. Refresh volatile prices/availability within 30 days and before release if stale. Add precise evidence or remove the affected claim if a later draft needs it.
- Independent review, responsive light/dark image treatment, full licence-notice distribution, claim-adjacent citations and changed-site check/build/test belong to later owned stages. No score is awarded here.
- Actual validation results are retained in `validation.json`; the runtime receipt summarizes them. No site build or native test is claimed. No sign-in, settings change, cleanup, purchase, messages, commit, push, deployment or queue mutation occurred.
