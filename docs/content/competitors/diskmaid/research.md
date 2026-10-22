# DiskMaid research — blocked for drafting

Checked **2026-10-21** · Task `research-diskmaid` · Research only, not a review or publication approval.

## Decision

DiskMaid is a **direct Mac cleanup/storage competitor**, not a dead product or a Windows utility needing a Mac-replacement angle. Keep `canonicalOwnerId: diskmaid`; do not skip it as an alias. Its official homepage is <https://nalarin.com/diskmaid>, linked to App Store ID **6758129723**, currently titled **DiskMaid: Clean Your Computer**, by **Nalarin** (seller **PT KERJA AKAL DIGITAL**). The store title is the same product, not another article. No official repository was established.

`MyMacMaid` occurs in legal-page paths and the store bundle identifier, but a historical product rename is **not verified**. Do not draft a separate MyMacMaid page on that clue. There is no DiskMaid/PowerMyMac alias evidence; the unrelated PowerMyMac issue was not investigated or merged.

**Drafting is blocked:** a real competitor screenshot URL is identified, but image reuse permission and pixel/privacy review are missing. The conflicting tracking disclosures also prohibit a blanket privacy recommendation. No website files changed.

## Existing evidence reused first

Reused the `diskmaid` record in `docs/content/verification/batch-1.json` and its retained official/directory snapshots from October 21. No repeat AlternativeTo fetch. Identity, homepage, Mac positioning and documented core features remain attributed to those same-day sources. The directory's “Free” tag and homepage's “Get DiskMaid Free” CTA do **not** establish free full functionality.

`research.json` contains the per-claim URL, exact supporting excerpt, check date, scope, evidence class and verification state; source snapshots have SHA-256 provenance. It also carries the reused discovery timestamp and exact listing <https://alternativeto.net/software/diskmaid/about/>. Original manifest edges are retained: CleanMyMac `?p=7` (2026-10-21T18:36:45.366Z) and Mole `?p=7` (2026-10-21T18:37:22.582Z); pagination was not invented or reconstructed.

## Missing material facts checked

| Topic | Finding and boundary | Evidence |
| --- | --- | --- |
| Version/platform | US App Store shows **1.6**, dated **June 1, 2026**, requiring **macOS 14.6+**. No installed/native test or exact Intel compatibility verification. | [Store](https://apps.apple.com/us/app/diskmaid-clean-your-computer/id6758129723), retained `sources/app-store.html`; `platform-version`. |
| Pricing | Free download, **Lifetime $19.99** displayed in the US storefront. Description: “All features described above requires one time purchase.” Do not call it a free fully functioning cleaner. Actual checkout, taxes, entitlement limits, regional price and refunds untested. | Store HTML Information → In-App Purchases and description; `price`. |
| Licence | Personal, non-exclusive, non-transferable licence on macOS; payments handled by Apple. No open-source licence established. Generic subscription wording in terms does not prove an active subscription SKU. | [Terms](https://nalarin.com/mymacmaid/terms), updated February 9, 2026; `license`. |
| Local scans | Vendor describes local scanning. Privacy policy says it collects a unique device-level identifier for licence management; do not turn local scans into no network traffic or no data collection. | [Privacy](https://nalarin.com/mymacmaid/privacy), updated February 9, 2026; `local-scan`. |
| Tracking conflict | Homepage says “No telemetry, no usage tracking”; store declares identifiers used to track users and identifiers not linked to identity. These are incompatible disclosures, not proof of actual network behavior either way. | Reused official snapshot plus store App Privacy; `privacy-conflict`. |

The ordinary HTTP retention attempt initially returned 403 at Apple; an ordinary retry succeeded. Terms/privacy were successfully read with WebFetch, but their subsequent urllib retention attempts and the image-locator homepage request returned 403. These failures are retained in `sources/manifest.json`; no anti-bot bypass, sign-in or hidden-cookie extraction occurred. Exact WebFetch retrieval clocks were not available; those sources use check date rather than invented timestamps.

## Documented workflow and honest matrix

Nalarin documents Smart Scan for caches/logs/Trash/browser data, large/old-file discovery with preview, exact-duplicate hashing, app-remnant removal and an Activity History/undo view. These are **vendor descriptions, not our tests**. Undo coverage, Trash semantics, protection against shared-data loss and safe-to-delete decisions remain unverified. Do not quote the website's example “24.7 GB Freed” as a result.

The App Store also explicitly advertises developer build files and package-manager caches. Do not say DiskMaid lacks developer cleanup. Exact adapters, paths, version support and rebuild costs remain unknown. Process/helper grouping and recurring-growth monitoring are **not verified**, not “No”; cleanup history does not establish either capability. SwiftUI, Apple Silicon optimization and sandboxing are vendor positioning, not independent performance or security certification.

Breathing Room evidence is reused from the same-day `capabilities.md`, including its release/source distinctions. Breathing Room, which we build, has source implementations for owner/project storage views, app/helper grouping, sampled activity, reviewable cleanup and exact saved daily-care approvals while running. Those are not proof of current distributed-binary parity. The optional automatic verified-Ruff-cache Trash mode prevents an unconditional “every cleanup always asks again” claim.

Preserve **0.1.0-preview.1**, **macOS 13+**, **Python 3.10+ inventory requirement**, the release's lack of Developer ID signing/notarization, physical-Intel/clean-machine testing limits and hosted assistance's authentication/internet/data boundary. Free local tools differ from optional AI Care advertised at **$5 USD/month or $50 USD/year**. No payment/entitlement test was performed. Do not recommend bypassing Gatekeeper.

## Visual handoff

1. **DiskMaid:** exact vendor-supplied screenshot asset URL is extracted from the retained App Store's `#product_media_mac_` public `source srcset`, saved in `research.json` → `visuals[0].assetUrl`. This is an app-screenshot locator, not a logo or guessed filename. No image was downloaded, copied, embedded or hotlinked: public availability grants no reuse licence. Vendor capture date, screenshot version, actual dimensions, pixel content and privacy review remain unknown. Link-only fallback does **not** satisfy the on-page gate. Proposed credit: “DiskMaid / Nalarin, via Apple App Store.” Caption/alt remain provisional until pixels are reviewed.
2. **Breathing Room:** selected `current-space-browser-preview`, `docs/content/assets/breathing-room/space-preview-2026-10-21.png`, SHA-256 `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a`. Opened and read the actual PNG; visible example-data and no-Mac-change disclosures retained. No edits or asset copies. Caption: **“Current-source Breathing Room Space browser preview, captured October 21, 2026. Example data only; not a native scan, measured activity or cleanup result.”** First-party capture basis and third-party mark limitations are inherited from `screenshots.json`. Source commit `54828ac3170b45861aee70861dd0b9c658ed7e51` is current-source illustration evidence, not release/native evidence.

To unblock the image gate: separately authorized work must establish reusable permission/licence or an explicit policy decision, then retrieve/hash the original image and review actual pixels/privacy/readability. This job must not send permission requests. Current-native evidence cannot be manufactured by relabeling the preview.

## Distinct workflow article brief

**Proposed title:** Review Mac app remnants without deleting shared files  
**Proposed slug:** `review-mac-app-remnants-and-duplicate-files`  
**Track/intent:** search/reference; a retention-first decision for files reported as app leftovers or duplicate content, not another generic cleaner ranking.

- Lead with the retention decision and backup boundary; place a cleared real product visual immediately after the lead.
- Explain that association with an app and identical file contents are different signals. Neither proves a copy is expendable.
- Review active apps/projects, shared or synced copies, originals, backup availability and rebuild/download cost before selecting anything.
- Use only documented DiskMaid preview/selection descriptions, with the purchase boundary; no invented click-path tutorial or undo guarantee.
- For uncertain ownership, explain an investigate/keep path. A bounded alternative can introduce Breathing Room's owner/project workflow with same-sentence affiliation and preview/hosted caveats, not a claimed equivalent duplicate finder.
- Distinguish displayed candidate bytes from bytes moved to Trash and actual available-space changes. No promised savings or speedup.

**Interaction handoff:** a non-scanning, local keep/investigate checklist. Any unknown about active use, original copy, shared/synced data, backup or rebuild cost yields “keep/investigate,” never “delete.” No filesystem access, uploads, fake measurements or mandatory signup. Link contextually to `/comparisons/` and the future `/comparisons/diskmaid/`; routes are proposals, not created pages.

## Concise comparison brief

**Breathing Room vs DiskMaid**, canonical proposed route `/comparisons/diskmaid/`. Use the claim-linked matrix in JSON: macOS, licence, scan/local-hosted boundary, approval controls, duplicates/remnants, developer caches, helper grouping, growth/history, purchase terms and installation caveats. Link to the workflow article rather than duplicating it or adding an alternatives doorway.

**DiskMaid fits:** readers wanting its documented Mac App Store cleanup, exact-duplicate and app-remnant workflow, accepting the purchase conditions and macOS requirement. No claim that its removal is complete, faster or safer.

**Breathing Room fits:** readers interested in its source-documented investigation/owner/project and app/helper workflow who accept preview/runtime limitations and optional hosted paid care. Do not present it as a certified duplicate-finder/uninstaller substitute, fully offline AI or production-ready binary.

**Remaining unknowns:** architecture/permissions, exact cache adapters, removal/undo semantics, free-tier limits, regional offers, repository availability, native performance and screenshots/rights. Noncritical unknowns can remain explicitly labelled; the visual blocker cannot be waived. Privacy claims must preserve the documented conflict unless resolved.

## Validation and scope

Packet assembly performs actual supporting-excerpt membership checks against retained official/App Store sources and verifies the selected Breathing Room image hash. Separate validation checks every retained source hash, claim/source links, receipt state and owned paths. See `validation.json` for actual results.

No competitor installation, cleanup, purchase, sign-in, messages, native scan, browser/profile manipulation, credential access, website change, site build, commit, push, deployment or queue/database mutation. No independent reviewer or publication score was invented. Only this competitor folder and the required runtime receipt are outputs.
