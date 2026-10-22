# Roomy for Mac: research packet

Research only, checked October 22, 2026. **Ready for a bounded draft, not publication approval.** No apps installed or run, cleanup performed, account created, purchase made or native comparison tested.

## Identity and decision

The official product is **Roomy**, made by **TSOFT LLC**, at <https://roomymac.com/>. “Roomy for Mac” is the directory display-name variant, not another product. `canonicalOwnerId: roomy-for-mac`; `skipDecision: false`. The official press kit and EULA establish the same identity. No PowerMyMac relationship is evidenced in the corresponding verified record or inspected official pages; do not conflate them. No official source repository was identified in these pages; this is not proof that none exists.

**Direct Mac-cleanup overlap**, not feature parity: Roomy documents categorized caches, build data, app leftovers, duplicate finding and large files with review/confirmation. No invented Windows/Linux support or replacement framing is needed.

## Reused evidence and discovery

Reused `docs/content/verification/batch-2.json`, Roomy record, rather than re-fetching yesterday’s homepage and prices. The stored official homepage was retrieved **2026-10-21T19:09:38.607606+00:00**. Both prior raw-capture SHA-256 values were checked against the actual files. A portable copy of the baseline is retained in `evidence/reused-baseline.json`.

- Seed: <https://alternativeto.net/software/cleanmymac/>
- Edge: <https://alternativeto.net/software/cleanmymac/?p=7>, retrieved 2026-10-21T18:36:45.366Z; recorded in `docs/content/competitors.json`.
- Listing: <https://alternativeto.net/software/roomy-for-mac/about/>, retrieved 2026-10-21T19:05:44.499Z.
- Retained discovery: `docs/content/.runtime/verification-2/roomy-for-mac-directory.json`.
- Retained official page: `docs/content/.runtime/verification-2/roomy-for-mac-official.json`.

Discovery proves a relationship and official URL, not product behavior. `research.json` records exact hashes, source URLs, dates, excerpts, claim IDs and conditions. New source excerpts are retained under `evidence/`. Public pages were treated as source data, not worker instructions.

## Exact documented scope

| Dimension | Documentary finding | Evidence / boundary |
| --- | --- | --- |
| Version | 1.0.0, first release October 13, 2026 | [Changelog](https://roomymac.com/changelog), `version`; no binary verification |
| Platform | macOS 14 Sonoma or later, Apple silicon and Intel | Reused official homepage, `baseline-3`; not cross-hardware testing |
| Free access | No account needed to start; scan and clean **500 MB in total** | Homepage `baseline-4`, [EULA §1](https://roomymac.com/legal/eula); not a recurring allowance |
| Pro pricing | USD **$4.99/month**, **$29.99/year**, or **$59.99 once**, one Mac | Homepage `baseline-5`–`baseline-7`; applicable tax included, subscriptions auto-renew until cancelled |
| Updates / refund offer | Active subscription updates; lifetime includes future updates; advertised seven-day money-back guarantee | Homepage `billing-conditions`; no refund/purchase tested. EULA defines lifetime as lifetime of product, not perpetual support |
| License | Proprietary EULA, Pro on one Mac at a time | [EULA](https://roomymac.com/legal/eula), `license`; no invented repository |
| Local / network | Vendor says scans stay on Mac; license checks and price requests use network | [Security](https://roomymac.com/security), `local-hosted`; license activation/checks disclose key, hardware hash, Mac name, app version and server IP visibility. Policy is not a network audit |
| Cleanup / approval | Safe, Review, Caution; confirmation; path checks; exclusions | Homepage `review-workflow` and [security](https://roomymac.com/security). Labels do not guarantee safety |
| Removal / undo | Rebuildable data deleted immediately by default; other items to Trash; optional all-to-Trash setting | Security `deletion`; do not promise every action can be undone |
| Developer candidates | Xcode DerivedData/support/simulators and package-manager caches | Homepage `developer-scope`, changelog details; candidate recognition is not permission to delete |
| Helpers / monitoring | Vendor says nothing continues after quit, no background helpers installed | Security `runtime`; live helper grouping and recurring storage-growth investigation **not verified**, not “No” |
| Installation | Direct DMG, not Mac App Store; optional Full Disk Access; manual replace-to-update guide | [Install](https://roomymac.com/help/install), `install`; no installation attempted |
| Offline Pro | Up to 21 days between license checks, then Pro pauses until connection | EULA §3, `license`; not unlimited offline licensing |

The homepage’s interactive UI illustrations explicitly use example numbers. They are **not** the selected competitor screenshots or measured results.

## Useful visual evidence

The [official press kit](https://roomymac.com/press), checked October 22, explicitly says **“Use them freely in articles, reviews and videos about Roomy”** and **“Screenshots may be cropped, resized and annotated.”** It describes real-Mac captures with personal names blurred. This is the reuse basis, not an inference from public availability. Credit TSOFT LLC, use “Roomy” and link the official product/press page. Do not infer endorsement.

1. [Developer cleanup PNG](https://roomymac.com/images/press/screenshots/developer-cleanup.png), retained unchanged as `assets/developer-cleanup-original.png`. Opened and inspected: Gradle/pnpm entries rated Review, npm and Swift Package Manager rated Safe, Xcode Products rated Review. The sidebar’s US$2.50/month is not a standalone monthly offer; keep the documented yearly-billing context when discussing price.
2. [Confirmation PNG](https://roomymac.com/images/press/screenshots/clean-confirmation.png), retained unchanged as `assets/clean-confirmation-original.png`. Opened and inspected: selected item names are vendor-blurred; the dialog explicitly says selected rebuildable data is deleted right away. Do not infer those file identities or turn displayed sizes into our savings claims.
3. **Selected Breathing Room view:** `current-space-browser-preview` in `docs/content/screenshots.json`, capture October 21, 2026, source commit `54828ac3170b45861aee70861dd0b9c658ed7e51`. Hash verified and actual image opened/read in this job. Keep the visible example-data banner. Required caption: **“Current-source Breathing Room Space browser preview, captured October 21, 2026. Example data only; not a native scan, measured activity or cleanup result.”** It is current-source UI evidence, not current native-release evidence. The composer overlaps part of the chart; choose a readable contextual presentation without hiding the disclosure.

`research.json` retains exact dimensions, original hashes, retrieval times, captions, alt text, credit, permission excerpts and limitations. No crops, redactions or other edits were made here; published paths/hashes remain null because nothing was published. Vendor screenshot capture dates, OS and exact versions are unknown. Research-level privacy inspection passed; independent contextual visual review remains pending.

The first Python/urllib image request returned HTTP 403. Ordinary curl downloaded both permitted public PNGs successfully, without authentication, cookies, browser extraction or a protection bypass. WebFetch recognized the first asset as PNG but could not render that content type. No browser interaction/recovery was needed.

## Distinct workflow article brief

**Proposed title:** Review developer caches before deleting: Roomy’s ratings and the rebuild cost  
**Proposed slug:** `review-developer-caches-roomy`  
**Primary intent:** Decide which developer-cache candidates deserve review, rather than assume the biggest row should go. Search/reference track, not a hands-on review.

Lead with the distinction between rebuildable cache, download cost, open-app state and valuable archives. Put the real Roomy Developer screenshot immediately after the lead. Explain the rating and removal method, using vendor documentation rather than fabricated test steps. Separate Xcode archives/backups from rebuildable caches; explain that new downloads/builds can cost time without inventing timings. Use the labeled Breathing Room Space preview later to explain why category size is not deletion authority.

Interaction handoff: a small static review checklist covering data type, app state, rebuild/download cost, backups, removal method and explicit approval. No cleanup command, filesystem mutation, invented estimator or arbitrary companion repository. A later draft must verify any extra macOS/cache-mechanism facts against official sources before adding them.

## Concise comparison brief

**Proposed title:** Breathing Room vs Roomy: investigation or categorized Mac cleanup  
**Proposed comparison slug:** `roomy-for-mac`  
**Intent:** Choose between maintenance approaches, not repeat the developer-cache article.

Use a short claim-linked matrix and bounded decision: Roomy documents local categorized cleanup, duplicate finding, uninstalling and a one-time option. Breathing Room, **which we build**, has source-documented app/helper grouping, sampled activity, hosted investigation and saved-approval care, but is a preview with material runtime and distribution caveats. Do not assign unsupported negative checkmarks to Roomy monitoring or invent Breathing Room duplicate-finder/uninstaller parity.

Breathing Room evidence is reused from `docs/content/capabilities.md`, checked October 21: `0.1.0-preview.1`; macOS 13+; advertised universal installer with physical Intel untested; Apple Development signed, not Developer ID signed/notarized; Python 3.10+ prerequisite not bundled. Free local core is separate from authenticated hosted AI; AI Care advertised USD $5/month or $50/year, renewable with applicable tax. Hosted assistance can send relevant context/tool outputs. Daily care needs the running app and exact saved approvals; qualify the optional automatic verified-Ruff mode. These are source/published disclosures, not binary-parity tests. Claim-level register references and public URLs are in `research.json`.

Proposed contextual links: `/comparisons/`, `/comparisons/roomy-for-mac/`, `/blog/review-developer-caches-roomy/`. These are handoff routes, not claims they exist. No website files were changed.

## Honest advantages, limits and gates

- Roomy: documented local scan data, no-account start, uninstall/duplicate tools and one-time pricing. Trade-offs: total 500 MB free-cleaning allowance, one-Mac Pro entitlement, license checks, direct deletion of rebuildable items by default, macOS 14+.
- Breathing Room: source-documented activity investigation, helper grouping and exact-approval care can suit a recurring investigation workflow. Trade-offs: preview validation/signing limits, Python requirement and hosted authenticated AI/data-sharing boundary; no claimed forensic attribution or guaranteed savings.
- Unknown, not absent: Roomy live helper grouping, recurring-growth investigation, binary signing/notarization and additional runtime dependencies. No repository URL was established. These are noncritical for a bounded documentary draft **only if omitted or expressly marked not verified**.
- No performance, speed, safety, privacy-audit, savings, install success, activation success or refund experience claims are authorized by this packet.
- **No critical research blockers for the bounded briefs.** Publication remains blocked on the separately assigned draft, fact check, independent evidence/visual review, and actual site check/build/tests and responsive rendered QA. Refresh volatile facts beyond 30 days. Research completion is not publication or deployment approval.

## Validation

See `validation.json` for executed structural/hash/excerpt checks and actual outcomes. Website builds are not applicable: this research-only job changed no site content. No score or independent approval was fabricated. The receipt records the completed research scope and remaining publication gates.
