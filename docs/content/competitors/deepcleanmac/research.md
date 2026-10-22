# DeepCleanMac research — blocked for drafting

Checked October 21, 2026. Task: `research-deepcleanmac`. **Research and planning only; no article, site changes, installation or product test.** The machine-readable claim ledger, exact excerpts, retrieval timestamps and source hashes are in [`research.json`](research.json).

## Decision

DeepCleanMac is a live, relevant **direct Mac-cleanup competitor with different scope**, not a verified alias or a dead-product skip. Its official identity is **DeepCleanMac**, homepage <https://deepcleanmac.com/>. `canonicalOwnerId: deepcleanmac`; aliases: none verified; `skipSeparateDraft: false`. The listing and official site agree on identity (C01). No official repository or independently identified legal publisher was established; null is not proof that no repository exists.

Do not merge this product with similarly named DeepClean or with PowerMyMac. The latter's unresolved iMyMac/FoneDog/TechyCub relationship is a separate group in `docs/content/verification/alias-decisions.json`; this job does not resolve or edit that group's records.

**Do not draft yet.** Two precise blockers remain:

1. A real competitor Dashboard image is identified and visually inspected, but redistribution permission is unverified. The allowed link-only research fallback does not satisfy the required on-page app-image gate. Obtain a verified licence/permission and legible asset, or an explicitly authorized editorial policy decision. Do not send a permission request in this scheduled job.
2. Exact pricing needs reconciliation: the current homepage advertises **$5/year / $9 lifetime**, but the July 22 changelog announces **$9/year / $19 lifetime**. No promotion duration or actual payable amount was established. Independent approval of carefully attributed, dated homepage-offer-only wording is another possible resolution; do not silently present either source as the final transaction price.

## Reused evidence and discovery

First reused `docs/content/verification/batch-1.json`, record `deepcleanmac`, including its official snapshot checked **2026-10-21T19:08:01.448108+00:00**. Its retained SHA-256 is `76403e4f07576520a85bbfbcc1d5d15e77fa7e238f03df2f3924c761f2266018`.

- Discovery listing: <https://alternativeto.net/software/deepcleanmac/about/>, retained directory snapshot retrieved **2026-10-21T19:06:21.309Z**. Exact official-link excerpt: “Official Website / deepcleanmac.com”.
- Manifest edges: CleanMyMac page 6, <https://alternativeto.net/software/cleanmymac/?p=6>, retrieved 18:36:42.517Z; Mole page 6, <https://alternativeto.net/software/mole/?p=6>, retrieved 18:37:21.311Z, both October 21. These are inherited manifest provenance, not new traversal or new distinct-product proof.
- Reused same-day first-party `capabilities.md` and `screenshots.json`; no unnecessary refetch of their current facts.
- New official terms/privacy/changelog reads fill material gaps. Homepage and listing revisits were for image/repository-link discovery absent from the baseline, not a redundant general research pass.
- Direct Python public GETs returned **HTTP 403** for homepage, terms, privacy and changelog. WebFetch returned readable text; normal navigation in owned browser tab **89** retained public DOM snapshots. No challenge bypass, cookies, hidden endpoints or alternate profile. The owned tab was closed; existing tabs were not inspected or navigated.

Public content was treated as source data, not instructions. `PLAN.md`, `EDITORIAL.md`, capabilities and screenshots were read before editing; no applicable `AGENTS.md` was found in the app ancestor checks or the docs subtree.

## What the official sources support

All entries below are **documented vendor statements**, not observed app execution. Each C/B identifier resolves to source URL, excerpt, check date, scope and evidence class in `research.json`.

| Dimension | DeepCleanMac evidence and boundary |
| --- | --- |
| Platform | Homepage says “macOS Sonoma (14.0) and later” on Apple Silicon and Intel (C02). No Windows/Linux claim or invented compatibility. |
| Version | Inspected [changelog](https://deepcleanmac.com/changelog) begins with **1.7.3, October 19, 2026** (C17). This identifies the newest listed entry, not the installed/downloaded binary. |
| Licence | [Terms](https://deepcleanmac.com/terms), updated April 13, grant non-exclusive, non-transferable paid use on **one Mac**; annual renews unless cancelled; lifetime includes future updates (C09–C10). Do not describe this as open source. |
| Price conditions | Homepage $5/year auto-renew, $9 lifetime one-time (C07–C08), both features advertised. Terms say **USD**, possible applicable taxes, payment through Polar, and a **14-day** refund request window (C11–C12). No purchase/refund/cancellation test. Historical discrepancy C21 remains explicit. |
| Download/free wording | Public `https://deepcleanmac.com/DeepCleanMac.dmg` link exists (C22). No binary retrieved. “Download Free” does not establish an unlimited free licence, trial duration, cleanup allowance or activation terms. |
| Review workflow | Homepage says “See exactly what will be cleaned … file sizes, locations, and types” (C03). No inference of universal guardrails, Trash-only deletion, undo, or guaranteed safety. |
| Suite | Updater for App Store/Homebrew/Sparkle (C04); advertised uninstaller, duplicate finder, resetter, shredder and disk treemap (C05). Do not repeat “zero leftovers” or SSD unrecoverability promises as verified outcomes. |
| Monitoring | CPU/memory/disk health dashboard documented (C06). Persistent growth history and process/helper ownership-grouping parity are **not verified**, not “No”. |
| Developer scope | Git-aware build-folder protections and cloud-only-folder exclusions are documented in 1.7.0/1.7.1 notes (C18–C19); 1.6.7 describes a double-counted-size fix and Poetry environment exclusion (C20). Do not imply current versions still have fixed historical defects. |
| Installation | 1.3.0 release note describes Full Disk Access detection and skipping protected paths (C23). Signing, notarization, runtime dependencies and exact download build are unknown. |
| Privacy/network | [Policy](https://deepcleanmac.com/privacy), updated April 13, discloses cleanup statistics “tied to your license key,” machine identifier/version, and IP-derived country/city analytics (C13–C15). It says cleaned filenames/paths are not collected (C16). These are policy assertions, not a traffic audit. Directory “No Tracking”/“Works Offline” tags cannot justify blanket privacy/offline claims. |

Reject unmeasured homepage averages and speed/safety claims: “15.4 GB”, “<30s”, “never” and “beyond recovery” are not our benchmarks. No screenshots establish savings, and no cleanup ran.

## Breathing Room comparison boundaries

Same-day source/published evidence reused from `docs/content/capabilities.md` (B01–B06):

- Free Apache-2.0 desktop **preview**, identified version **0.1.0-preview.1**, macOS **13+**, advertised universal Apple Silicon/Intel installer. Physical Intel and clean-machine behavior are not certified.
- Published preview is **Apple Development signed, not Developer ID signed or notarized**; Python **3.10+** is a disclosed prerequisite. Never advise bypassing system-wide protections.
- Local inspection and constrained cleanup are distinct from authenticated **hosted AI**. Do not describe AI as entirely offline. AI Care is advertised at **$5 USD/month or $50 USD/year**; free local tools do not require a separate app purchase. Paid enforcement/allowances are not newly verified here.
- Grouped helpers, sampled activity, developer-cache discovery and exact saved approvals are source-backed, not binary performance validation. Attribution is incomplete; sampled writes are not proof an app wrote a particular file.
- Daily care needs the app running and exact saved approvals. Explicit automatic Ruff-cache mode is a separate exception, so “never deletes without asking” is not an unconditional product promise.

Use <https://breathing-room.chatic.ai/>, its [privacy policy](https://breathing-room.chatic.ai/privacy/), [download disclosures](https://breathing-room.chatic.ai/download/) and the [identified release](https://github.com/bucabay/breathing-room-app/releases/tag/v0.1.0-preview.1) through the cited register. This job did not repeat installer, service, update or payment tests.

## Visual plan and rights gate

### Competitor: real app image, link-only

- Source page: <https://alternativeto.net/software/deepcleanmac/about/>
- Exact inspected asset: <https://img.alternativeto.net/s/618x394/avif/deepcleanmac_822195_full.jpg>
- Listing's corresponding fallback asset: `https://img.alternativeto.net/s/309x197/jpeg/deepcleanmac_822195_full.jpg`.
- Observed rendition: **618 × 394**; inspection timestamp retained in `sources/competitor-visual-inspection.json`.
- Visually read the actual browser-rendered image: Dashboard/System health overview, sidebar tools, health/disk/CPU/memory cards and lifetime-cleanup figures. It is an app UI image, not merely a logo or webpage. Small text is soft; do not silently enlarge it into a legibility claim.
- Version, capture date, actual capturer, OS, underlying data and privacy clearance unknown. No historical savings figures become factual claims.
- **Reuse: link-only, not cleared.** No explicit redistribution licence was established in checked material; public visibility is not permission. No original third-party image was saved to this repository or website, so original/published file hashes are null rather than invented. Browser diagnostic inspection is not a publication asset.
- Proposed alt: “DeepCleanMac Dashboard showing health, available disk space, CPU and memory cards, with cleanup tools in a sidebar.”
- Proposed caption: “DeepCleanMac Dashboard app image published on AlternativeTo. Version, capture date and underlying measurement conditions are unknown; not our test results.”
- Credit: DeepCleanMac via AlternativeTo; respective owners retain rights. Credit alone does not clear rights.

### First-party: selected current-source Space preview

Selected `current-space-browser-preview` from `screenshots.json`:

`docs/content/assets/breathing-room/space-preview-2026-10-21.png`

**2940 × 3468**, SHA-256 `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a`, captured **2026-10-21T19:06:45.416416+00:00**, source commit `54828ac3170b45861aee70861dd0b9c658ed7e51` at `http://127.0.0.1:1431/`. Existing file hash checked and actual PNG opened/read in this job; no recapture or modification.

Required caption: **“Current-source Breathing Room Space browser preview, captured October 21, 2026. Example data only; not a native scan, measured activity or cleanup result.”**

Alt: “Breathing Room Space view rendered in a browser with illustrative example data.” Keep both example-data disclosures visible. Do not use the legacy Home preview. This is current-source browser illustration, not proof of distributed native behavior. The floating assistant overlaps part of the chart; independent page-context/mobile review must choose a useful legible presentation without losing disclosure. Owner-requested first-party UI capture is the reuse basis; no blanket third-party trademark permission is inferred. No published copy or edits yet.

## Distinct workflow brief — not a draft

**Proposed title:** Review developer build folders before cleaning a Mac  
**Proposed slug:** `review-developer-build-folders-before-cleaning-mac`  
**Track/intent:** Search/reference; decide what to keep, rebuild or investigate in a development project before authorizing cleanup. No search-volume or ranking claim.

Lead with the decision: a generated-looking folder is not automatically disposable. Use DeepCleanMac's **dated** Git/build-folder, Poetry and size-accounting notes as concrete documented examples (C18–C20), not a fictional incident or hands-on tutorial.

Proposed sections:

1. Distinguish committed data, generated output, environments and unknown files.
2. Explain the versioned protection changes, including fail-closed checks, without alleging current defects.
3. Review owner, exact location, rebuild/download cost, backup and permissions before any action.
4. Explain that scan totals, bytes moved to Trash and newly available space are different. Do not add overlapping categories or promise reclaimed bytes.
5. Make one bounded recommendation: “Breathing Room, which we build,” can serve investigation/review for readers accepting preview/Python/hosted-AI constraints. It is not an equivalent full updater/uninstaller/duplicate suite.

Interaction handoff: a **non-destructive keep/rebuild/unknown checklist**, not runnable deletion code. Committed/unknown → keep; known generated output → verify owner/reproducibility/location and review. No scans, uploads, permission toggles or example savings calculator are needed. Primary visuals remain the cleared competitor app view and the labeled Space preview; a checklist cannot replace either image gate.

Link to `/comparisons/deepcleanmac/`, `/comparisons/` and a genuinely relevant `/tools/` resource after route verification. Check title/intent uniqueness again before drafting; no site route created here.

## Concise comparison brief — not a draft

**Proposed title:** Breathing Room vs DeepCleanMac: review workflow or utility suite?  
**Comparison slug:** `deepcleanmac`

Start with a bounded audience answer and affiliation disclosure. Follow with the compact sourced matrix in `research.json`: OS/version, licence/price conditions, local/hosted boundary, review controls, suite breadth, developer files, monitoring, runtime/signing caveats. Mark unsupported cells “not verified”. Link to the deeper workflow instead of expanding the matrix into a second interchangeable article. Do not create a separate alternatives doorway.

### Honest advantages and trade-offs

- **DeepCleanMac:** documented suite breadth may suit someone needing app updating, uninstalling, duplicates, reset or a disk treemap (C04–C05). Annual/lifetime single-Mac options are advertised, but exact payable amounts remain unresolved. Versioned notes document concrete protection work; none was tested here. Analytics/network disclosures and unknown deletion/undo behavior belong in the decision (C13–C20).
- **Breathing Room:** free core and inspectable desktop source, plus source-backed grouped activity and exact-approval investigation, may suit a developer (B01–B06). Counterweight: non-notarized preview, Python prerequisite, untested physical Intel, authenticated hosted AI and no verified full-suite parity.
- **Neither:** no proven performance/safety/savings winner, no guaranteed recovery, and no evidence authorizing automatic deletion of unknown project or personal data.

## Handoff and checks

`build-packet.py` builds only the owned JSON from retained evidence and asserts every quoted source excerpt exists. `validate-packet.py` checks source hashes, all claim citations, matrix references, current preview integrity, link-only competitor handling and blocked gates; actual results are retained in `validation.json`.

No marketing content/assets changed, so website check/build/test and responsive draft QA were **not run**. No independent editorial score or approval is claimed. Noncritical unknowns (repo/legal entity, trial allowance, exact binary/runtime/signing, historical capture details, helper grouping/history, deletion/undo model) remain explicit. Missing critical evidence means blocked, not invented; queue/database untouched.
