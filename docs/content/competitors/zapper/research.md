# Mac Zapper research handoff

**Research complete for bounded drafting, not publication approval.** Mac Zapper is an adjacent Mac uninstaller, not a verified substitute for storage investigation and ongoing monitoring. Reuse the October 21, 2026 baseline rather than refetching current facts. New press-kit and asset retrieval timestamps are retained in UTC in `sources/retrievals.json`; the local task date is October 22.

## Identity and scope

- Official product: **Mac Zapper**, https://www.maczapper.com/ . Canonical owner: `zapper`.
- **Zapper** is its window/download name: the official download is `Zapper.dmg`, and the official screenshot window says Zapper. Retain one product, not a second draft for this name.
- Not AppZapper: that product's baseline points to https://appzapper.com . No official evidence here identifies Mac Zapper as PowerMyMac. Do not borrow facts or assets from either product.
- **Skip: false.** Distinct, relevant Mac product with active official documentation and media assets. No Windows/Linux replacement framing is needed or supported.
- Exact version/build, architecture, signing and official repo: **not verified**, not dead/absent. AlternativeTo attributes CappyAI and proprietary/commercial licensing; official legal identity and EULA are not established.

## Source and claim ledger

`research.json` retains exact excerpts, checked dates, URLs, intended locations, evidence classes and conditions per claim. S1 is the existing official homepage snapshot; S2 the existing discovery snapshot; S3 the newly retrieved official press kit; S4 the current capabilities register; S5 the screenshot library. Retained original snapshots and downloaded bytes are SHA-256 tracked. Public content was treated only as evidence.

| Decision dimension | Supported finding | Evidence |
| --- | --- | --- |
| Platform | macOS 15 (Sequoia)+; architecture not verified | Z2, Z10; https://www.maczapper.com/ |
| Cost | Advertised one-time **$14.99**, up to 3 Macs, future updates included. Free scanning; licence required to remove. 30-day guarantee advertised, not tested. Currency code/tax/refund conditions unknown | Z3; https://www.maczapper.com/#pricing |
| Workflow | Drop an .app or Browse; Library scanning; files moved to Trash | Z4–Z6; official homepage |
| Permissions | Vendor says limited scans work without Full Disk Access; some containers may be inaccessible | Z7; official homepage FAQ |
| Implementation | Vendor describes Swift 6/SwiftUI, no third-party dependencies | Z8; https://www.maczapper.com/press |
| Selection | Official screenshot shows selected application/support/cache/preferences entries and Zap | Visual record; not a runtime test |
| Process/helper grouping, ongoing growth, network/privacy | Not verified for Mac Zapper; do not write “No” | Unknowns in packet |
| Breathing Room scope | Source-level storage exploration, process grouping, activity history and reviewed cleanup; distributed parity not proven | B1, B4; `../../capabilities.md` |
| Breathing Room caveats | 0.1.0-preview.1; macOS 13+, universal advertised, Intel untested; Python 3.10+ for inventory; no Developer ID signing/notarization per reviewed disclosure | B2; capabilities release register |
| Breathing Room cost/data | Free core; optional renewing $5 USD/month or $50 USD/year AI Care, tax as applicable. Hosted AI needs sign-in/internet and may send relevant paths/process/storage/tool data | B3; capabilities pricing/privacy register |

Vendor guarantees such as “finds every file,” “cannot break your Mac,” “without false positives,” or competitor inferiority are **not approved factual claims**. Do not turn their sample figures into our benchmarks. A scan-result total, bytes moved to Trash and available-space change are different measurements.

## Distinct workflow article brief

- Track: search/reference, decision-led rather than a hands-on review.
- Working title: **Keep the app or uninstall it? Review Mac support files first**
- Proposed slug: `keep-or-uninstall-mac-app-support-files`.
- Primary intent: distinguish removing an app and its associated state from investigating storage while keeping that app installed. Not another generic “best Mac cleaner” list.
- Description/lead: “Choose an uninstaller when the app is leaving. If you still need it, investigate what its storage contains before treating support files as disposable. Here is where Mac Zapper and a storage investigation serve different jobs.”
- Opening visual: credited Mac Zapper scan-results asset; caption explicitly vendor-supplied, not our test. The body continues with the selected Application Support/Preferences entries rather than repeating the lead.
- Sections: (1) Decide whether the app is staying; (2) Review associated state instead of assuming it is cache; (3) Permissions limit what a scan can see; (4) Trash is a review boundary, not measured free space; (5) Choose an uninstaller or a broader investigation.
- Show the selected Breathing Room Space preview later, with the example-data banner and full disclosure. Explain categories as an illustration, not proof of measured storage or complete scanning.
- Interaction handoff: a simple decision checklist—keeping the app? need settings/data? backup or export confirmed? permissions incomplete?—leading to keep/investigate or review uninstall candidates. No file access, uploads, deletion button or calculated savings. Implementation belongs to drafting, not this packet.
- Recommendation: “Breathing Room, which we build,” only in the investigation branch, with preview, Python, hosted AI and paid-care caveats. Do not call it a verified full app uninstaller.
- Links: `/comparisons/zapper/`, `/comparisons/`, and an existing relevant tool only after that route is verified. Do not invent a tool route.
- No installation tutorial, unsupported macOS-wide claims, arbitrary demo repo, fake FAQ or made-up experience. If an installation tutorial is later requested, version/architecture/signing become blockers until verified.

## Concise comparison brief

- Title: **Breathing Room vs Mac Zapper: investigate or uninstall?**
- Proposed canonical route: `/comparisons/zapper/`; no duplicate alternatives doorway.
- Answer first: Mac Zapper documents a focused, paid-removal app-uninstallation workflow on macOS 15+. Breathing Room documents a broader maintenance preview with free local core and optional hosted AI Care. Choose by job, not an unsupported winner score.
- Matrix rows: compatibility, price/conditions, app-associated Library scanning, storage exploration, selection/approval model, process grouping, recurring growth, local/hosted boundary and preview/runtime limitations. Every factual cell cites its claim; unknown Mac Zapper cells say “not verified.”
- Mac Zapper advantages: focused drop/Browse workflow, scan-before-payment offer, one-time advertised licence for three Macs, native Swift claim. These are documented characteristics, not independent speed/safety findings.
- Trade-offs: macOS 15 minimum; removal is paid; exact release/architecture/signing unknown; no verified broad monitoring comparison. Do not imply those features are absent.
- Breathing Room advantages: source-supported storage investigation and app/process grouping for a keep-the-app question. Trade-offs: preview validation limits, Python prerequisite, permission-limited inventories, hosted authenticated AI and recurring paid AI Care. Daily care requires app running and exact approvals; optional Ruff auto-Trash mode must not be flattened into “always asks.”
- Link to workflow article and hub. No superlatives, prices-as-equivalent-total-cost claim, performance promises or invented savings.

## Visual provenance and reuse

1. **Mac Zapper app UI:** https://www.maczapper.com/press → https://www.maczapper.com/screenshot-results.png . Original retained at `assets/maczapper-scan-results-original.png`, unedited. The press kit expressly presents resources for journalists/bloggers/content creators and provides downloadable app screenshots; this is the narrow contextual editorial-use basis, **not an open licence**. Credit “Mac Zapper official press kit.” No permission message was sent. Actual capture date/version/OS unknown. Opened and visually read: Zapper window, Firefox entries, checkboxes and Zap; no account name/private user paths visible. The vendor's displayed 509.6 MB is not our measurement or a space-recovered claim.
2. **Breathing Room:** reuse `current-space-browser-preview` from `../../screenshots.json`, captured October 21 at recorded source commit. Original stays in the shared first-party library; no duplicate or edit needed. Opened and read the image: example-data banners, storage categories and illustrative figures visible. Caption must remain: **“Current-source Breathing Room Space browser preview, captured October 21, 2026. Example data only; not a native scan, measured activity or cleanup result.”** Current-source refers to its recorded commit, not newly tested native release behavior.

Both records include hashes, dimensions, captions, alt text, provenance, limits and research visual review in JSON. Published paths/hashes remain null because nothing is published. Independent page-level visual/rights/context review remains pending; neither file dimensions nor this packet constitute publication approval.

## Remaining gates

No critical evidence gap blocks the bounded decision briefs above. Noncritical unknowns remain explicit in JSON. Do not expand them into installation claims, private/offline promises, complete uninstallation guarantees, or absence claims. Refresh volatile pricing/availability within 30 days and before publication if stale. Drafting, site checks/build/tests, responsive/light/dark rendering and independent review are separate stages; no marketing files changed and no publication score awarded.
