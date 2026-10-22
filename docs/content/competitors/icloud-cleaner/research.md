# iCloud Cleaner research: blocked, do not draft

Checked **2026-10-21** · Job `research-icloud-cleaner` · Research only, not publication approval.

## Decision

**Skip drafting pending evidence.** The directory-linked homepage, <https://icloudcleaner.com/>, returned HTTP 404 through WebFetch and displayed `404 page not found` in the owned browser tab at 20:42:21 UTC. The earlier batch-1 check also returned 404. This establishes an access failure, **not** that the product is permanently dead.

No operational official homepage, publisher, repository, current release, exact macOS requirements or current purchase terms were verified. `canonicalOwnerId: icloud-cleaner` is retained provisionally from the manifest. There is no verified alias or evidence connecting this listing to PowerMyMac. Do not merge it or create a renamed duplicate. This packet does not count as a finished distinct article.

## Reused discovery and verification

- Read `PLAN.md`, `EDITORIAL.md`, `capabilities.md`, `screenshots.json`, `AUTOMATION.md` and the applicable blog/browser skill instructions. No `AGENTS.md` found in the app tree or checked ancestors. No marketing-site files edited.
- First reused `docs/content/verification/batch-1.json`, record `icloud-cleaner`: `status: blocked`, `facts: []`, official-link failure and directory snapshot. There were no current verified product facts to re-fetch.
- Discovery edge: [Mole page 3](https://alternativeto.net/software/mole/?p=3), retrieved 2026-10-21T18:37:11.107Z → [iCloud Cleaner about listing](https://alternativeto.net/software/icloud-cleaner/about/), baseline retrieved 19:07:27.455Z → `https://icloudcleaner.com/`.
- Retained raw baseline: `docs/content/.runtime/verification-1/icloud-cleaner-directory.json`; SHA-256 `e1d16bc37cc47288e9e6c3bb5912970696fe7b0734cae9a0be991c7bbcf098ab`.
- Baseline official failure: `docs/content/.runtime/verification-1/icloud-cleaner-official.json`; SHA-256 `578ff38e5214b07a292d2faad69bcc275f30829fc5620cd50dde738e7e0e1925`.
- New browser records, with exact times, URLs and hashes in `research.json`: `sources/homepage-browser.json` and `sources/listing-visual-check.json`. Listing revisit filled the previously missing visual-asset evidence, rather than repeating capability verification.

## Claims and unknowns

The JSON claim ledger is authoritative for exact wording, excerpts, dates, evidence classes and conditions.

| Claim | Evidence | Treatment |
| --- | --- | --- |
| Listing points to icloudcleaner.com | S1/S4, “Official Website” | Verified directory destination only (C1). |
| Homepage currently fails | S2/S3, “404 page not found” | Verified observation, not discontinuation (C2). |
| Native Mac app scanning iCloud Drive, Desktop and Documents | S1 directory description | Official capability/platform claim not verified (C3). |
| One-time $4–$5 purchase | S1 directory price text | Not a current offer; currency, tax, devices, updates and licence terms unknown (C4). |

Official name, publisher, repository, version, minimum OS, architectures, licence terms, local/hosted operation, cleanup/approval controls, helper grouping, recurring-growth monitoring, developer-cache behavior, runtime and signing status remain **not verified**, never “No.” Do not repeat listing claims about notarization, encryption, safe deletion, ending iCloud payments or a 199.89 GB → 2.6 GB session as established facts. No app was installed or tested.

Provisional fit is **adjacent**, based only on directory-described iCloud-quota work. A Mac maintenance preview is not automatically an iCloud subscription migration replacement. No Windows/Linux support or Mac replacement behavior was invented. Search for the exact domain/product found only directory leads; a repository-focused search returned no results, which does not prove no repository exists. The secondary Automatool fetch produced no usable content.

## Visual evidence: blocked

The listing DOM exposes these candidates:

- [Make room for your iCloud data](https://img.alternativeto.net/s/618x394/avif/icloud-cleaner_674297_full.png)
- [Stop paying Apple for iCloud storage](https://img.alternativeto.net/s/618x394/avif/icloud-cleaner_200594_full.png)

Source page: <https://alternativeto.net/software/icloud-cleaner/about/>; inspected 2026-10-21T20:42:31.656Z. These are **link-only candidates**, not visually verified real app UI and not cleared assets. Capture date, app version, photographer and permission basis remain unknown. The separate image labeled `homepage` and the product icon do not satisfy the app-view requirement. No third-party image was downloaded; no original or publication hash is invented. Public access is not reuse permission. Required competitor screenshot gate remains blocked.

Selected first-party illustration: `current-space-browser-preview` from `docs/content/screenshots.json`, original `docs/content/assets/breathing-room/space-preview-2026-10-21.png`, 2940 × 3468. Original SHA-256 checked against manifest: `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a`. No copy, crop or new capture made.

**Required caption:** “Current-source Breathing Room Space browser preview, captured October 21, 2026. Example data only; not a native scan, measured activity or cleanup result.”

**Alt:** “Breathing Room Space view rendered in a browser with illustrative example data.” Preserve the example-data banner and browser-preview disclosure. Source commit `54828ac3170b45861aee70861dd0b9c658ed7e51`; first-party owner-requested UI capture, third-party marks not blanket-licensed. The screenshot-library job's visual review is reused, not claimed as a new visual inspection here. Publication-context privacy/rights/legibility review remains pending.

## Conditional workflow article brief

**Working title:** iCloud quota or Mac disk space? Identify the constraint before cleaning  
**Proposed slug:** `icloud-quota-versus-mac-disk-space-before-cleaning`  
**Track:** search/reference; not approved for drafting.

Distinct reader job: determine which storage constraint needs attention before choosing a tool, rather than expand a brand comparison into filler. Outline: identify the quota involved; confirm sync/download state and independent backups; distinguish project history, dependencies and photos; evaluate a tool's documented scope without promising plan savings. Obtain official Apple storage/sync/deletion documentation before writing procedural guidance. Do not treat `.git` or large personal files as disposable cache.

Interaction handoff: a local, non-mutating decision checklist asking which quota is full, where originals reside and whether there is a separate backup. No file access, upload, login, cleanup or settings change. Planned visuals: cleared competitor UI after the lead, explicitly labeled Breathing Room Space example later. A diagram cannot replace either required app view.

## Conditional concise comparison brief

**Working title:** Breathing Room vs iCloud Cleaner: verify the storage job first  
**Proposed route:** `/comparisons/icloud-cleaner/` — not created.

Compare the storage job, current version/platform, review model, local/hosted boundary, pricing conditions and installation caveats. Keep unsupported cells “not verified”; do not frame an unverified adjacent workflow as a direct substitute. Proposed contextual links to `/comparisons/` and the distinct workflow article require route validation later. No separate alternatives doorway.

## Truthful advantages and trade-offs

If later official evidence confirms the iCloud-focused workflow, its specificity may serve cloud-quota investigation; this is a conditional editorial judgment, not a recommendation to buy an unavailable offer.

Breathing Room, which we build, has documented preview implementations for Mac storage investigation and grouped app/process monitoring. Same-day `capabilities.md` evidence is reused; no native test or new service/pricing check was performed here. Identified release: `0.1.0-preview.1`, macOS 13+, advertised universal installer with physical Intel runtime untested, Apple Development signed but not Developer ID signed/notarized, Python 3.10+ prerequisite. Current-source screenshots do not establish distributed-binary parity.

Free local desktop capabilities are distinct from optional AI Care advertised at $5 USD/month or $50 USD/year, renewing with applicable tax. Hosted AI requires internet/authentication and may receive relevant paths/process/storage information; not entirely offline. Daily care needs the app running and exact saved approvals. Optional verified Ruff-cache automatic mode prevents an unconditional “never deletes without asking” promise. No iCloud migration equivalence, measured savings, safety or speed advantage established.

## Precise unblock requirements

1. Working official source identifying publisher/product and current availability, resolving any rename/alias before separate drafts.
2. Official current version, minimum macOS/architectures, licence/purchase conditions and documented workflow/approval behavior.
3. Real app-UI visual, source/capture provenance and explicit reusable rights or an approved policy decision. Link-only research fallback does not pass the on-page gate.
4. Apple primary evidence for any cloud-sync/backup procedural advice, then independent evidence and target-context visual review.

No site edits, queue mutations, signups, purchases, messages, credentials, cleanup, commits, pushes or deployments. Only owned research paths and the required receipt were written. Browser work used owned tab 111 and closed it; unrelated tabs were not inspected. Site builds are not applicable to this blocked research-only change.
