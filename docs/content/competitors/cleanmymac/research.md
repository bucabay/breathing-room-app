# CleanMyMac research packet

Reviewed **October 21, 2026** · `research-cleanmymac` · **Blocked for drafting** · Not publication approval.

CleanMyMac is a relevant, direct Mac-cleanup competitor, not a product to skip. The workflow brief and comparison are distinct, but neither may advance while exact pricing conditions and the required competitor image remain blocked. No website, queue or other product records were changed.

## Identity and deduplication

- **Official product/vendor:** CleanMyMac, MacPaw. Homepage: <https://macpaw.com/cleanmymac>. `canonicalOwnerId: cleanmymac`.
- **Discovery:** <https://alternativeto.net/software/cleanmymac/about/>, retained directory extraction retrieved `2026-10-21T19:04:46.576Z`. Its official-link title identifies MacPaw. No new traversal was necessary. Extracted DOM JSON and hash are referenced in `research.json`; this is not retained original wire HTML.
- **Reused first:** `docs/content/verification/batch-1.json` and its original homepage/directory snapshots. `batch-2.json` was absent at intake. Identity, requirements, teaser and download availability were not needlessly re-fetched.
- **Historical alias:** CleanMyMac X is a previous major version of this family. MacPaw’s [purchase-options documentation](https://macpaw.com/support/cleanmymac/knowledgebase/purchase-options) distinguishes an X licence from an upgrade to the latest CleanMyMac. Skip a separate X replacement draft; preserve version differences.
- **PowerMyMac is not that alias:** the [official PowerMyMac page](https://www.imymac.com/powermymac/) names iMyMac, whereas CleanMyMac belongs to MacPaw. Keep PowerMyMac under the separately discovered `imymac--cleaner` identity; do not merge it or process its separate queue job here.
- **Repository/licence:** no official current CleanMyMac app source repository established. AlternativeTo labels it proprietary, but exact current 5.x EULA remains unverified. Generic `/eula` names older Classic/2/3 products and cannot settle current terms. A guessed `/legal/cleanmymac` returned 404. Do not invent a repo or reuse licence.
- **Fit:** direct storage/cleanup overlap, with broader documented maintenance tools than verified Breathing Room scope. This is a Mac decision, not a Windows-support claim.

## Material facts and boundaries

Claim IDs, source URLs, exact excerpts, check dates and states are in `research.json`. Full public HTML and extracted text for new evidence are under `sources/`, with hashes. Vendor documentation is not hands-on testing.

| Topic | Evidence-backed wording | Claim/source |
| --- | --- | --- |
| Platform | Homepage advertises macOS 11+, 320 MB and 1200×800 minimum display. Architecture-specific runtime not tested. | `c-platform`, reused homepage |
| Version | Homepage says 5.5.7 / July 22, 2026; [changelog](https://macpaw.com/cleanmymac/whats-new) documents **5.7.2 / October 15, 2026**. Say “latest documented changelog entry,” not “binary tested.” | `c-home-version` (stale label), `c-version` |
| Cleanup review | [Smart Care](https://macpaw.com/support/cleanmymac/knowledgebase/smart-care), updated October 15, describes Scan → review → Run. Tasks selected by default; skip tiles or use Review to adjust details. | `c-review`, `c-details` |
| Duplicates | Smart Care’s My Clutter step scans Downloads; do not extend that step’s scope to every folder. Other modules have separate capabilities. | `c-duplicates` |
| Developer caches | [Edition table](https://macpaw.com/support/cleanmymac/knowledgebase/missing-features), updated April 21, lists Xcode Junk. npm/pnpm/Ruff/CLI parity not established. | `c-xcode` |
| Monitoring | Same table lists CPU/RAM/storage monitors and alerts. Do not claim no monitoring. Helper grouping and recurring-path attribution remain unknown. | `c-monitoring` |
| Editions | MacPaw Store, App Store and Setapp differ. Do not pair direct-edition functions with another marketplace’s price. | `c-editions`; retained edition table |
| Signing | Homepage says “Notarized by Apple.” Vendor statement, not independent signature check. | `c-notarization` |

### Pricing: blocked, not extrapolated

Homepage says **“Starting at $3.33/month.”** It does not establish currency, payment frequency, device count, introductory period, tax or renewal price. Do not multiply by twelve and call the result an annual offer, or compare numerically against Breathing Room as if terms matched.

[Purchase options](https://macpaw.com/support/cleanmymac/knowledgebase/purchase-options), updated August 11, document monthly/annual automatically renewing subscriptions, one-time current-major purchase, and Setapp access. One-time purchase excludes future major-version upgrades. [Marketplace guidance](https://macpaw.com/support/cleanmymac/knowledgebase/editions) says price varies by devices, upgrade possibilities and country-specific taxes. A seven-day trial is documented there; actual trial payment/cancellation conditions were not verified.

The exact [store offer](https://macpaw.com/store/cleanmymac) returned **403** to WebFetch. An owned Chrome tab showed **“Our system wants to double check that you are human.”** `sources/store-browser.txt` retains the actual accessibility snapshot. Stopped at the gate, did not interact with the challenge, and closed only the owned tab. No checkout/account/payment created.

**Unblock:** permitted independent review must record currency, actual charge/billing interval, edition, device count, tax, promotion and renewal conditions. A teaser or search snippet is insufficient.

## Visual manifest

### CleanMyMac: official app UI identified, link-only

- Source: [official Smart Care instructions](https://macpaw.com/support/cleanmymac/knowledgebase/smart-care).
- Asset: <https://cms-assets-proxy.macpaw.com/cdn-cgi/image/format=auto,quality=90/f296b094-6321-4b20-b995-a16b07b456ae.webp>.
- Source HTML identifies **“Task details”**; other real app views include scan results and selected tasks. Not a logo or landing-page capture.
- Source-page retrieval: `2026-10-21T19:16:46.502761+00:00`. Vendor capture date, capturer, build, dimensions and image-byte hash unknown: asset **not downloaded**.
- Caption: “Official MacPaw Smart Care task-details illustration. Vendor-provided UI, not our test or measured cleanup result. Exact build and capture date unknown.”
- Alt: “Official CleanMyMac Smart Care task-details screenshot linked from MacPaw’s review-results instructions.” Credit: MacPaw, linked to source.
- **Reuse: link-only.** Public availability is not a licence. [Official press room](https://macpaw.com/press) offers <https://cdn3.macpaw.com/press/cmm-media-kit.zip>, but download returned **403**. No kit bytes or permission obtained. No support image silently substituted as licensed.
- **Image gate blocked:** link-only is research fallback, not completed on-page imagery. Obtain accessible authorized assets/terms, permission, or an explicitly approved policy decision; then preserve original hashes and inspect actual image. No permission request sent.

### Breathing Room: selected current-source Space preview

- Existing asset: `docs/content/assets/breathing-room/space-preview-2026-10-21.png`.
- Inventory ID `current-space-browser-preview`; captured `2026-10-21T19:06:45.416416+00:00`; source commit `54828ac3170b45861aee70861dd0b9c658ed7e51`; source `http://127.0.0.1:1431/`.
- SHA-256 `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a`; **2940×3468**. Recomputed from actual file; not copied/edited/republished.
- Required caption: **“Current-source Breathing Room Space browser preview, captured October 21, 2026. Example data only; not a native scan, measured activity or cleanup result.”**
- Alt: “Breathing Room Space view rendered in a browser with illustrative example data.”
- Reuse basis: owner-requested first-party UI capture; third-party marks retain their owners’ rights. No blanket image/trademark licence.
- Opened and read actual PNG in this run: example-data disclosures visible; floating assistant overlaps part of chart. Future contextual crop must retain disclosure and be reviewed at target widths. No crop created.
- Browser illustration is **not** native capture or distributed-release test. Independent target-page review remains pending.

## Breathing Room comparison guardrails

Reused same-day `capabilities.md`; independently reread README requirements/workflow/pricing, native version/macOS config and billing config. Identified version **0.1.0-preview.1**, macOS 13+, Python 3.10+ for inventory; physical Intel runtime untested. Preview is not notarized. Local inspection differs from hosted authenticated AI, which can send paths/tool data to the service. Do not promise offline AI.

Free core and optional **$5 USD/month or $50 USD/year AI Care** are advertised; legacy `appAmount` is not an app price. Source presence does not prove installer parity or production readiness. Paid quotas/enforcement remain unknown. Default approval, optional narrowly verified automatic Ruff cache Trash moves, and scheduled reuse of exact saved approvals are distinct. Never flatten these into “never deletes without asking.” Daily care needs app running.

Storage size, cleanup result, bytes moved to Trash and available-space change are different quantities. No measured cleanup/speed, detection rate, safety guarantee or privacy superiority established for either product.

## Distinct workflow article brief

**Track:** search/LLM reference. **Title:** “Review CleanMyMac Smart Care selections before running cleanup.” **Slug:** `review-cleanmymac-smart-care-selections`.

**Reader job:** understand multi-module default selections and decide which actions to run, rather than shop for an alternative. Documented checklist, not fictional hands-on tutorial.

1. After conclusion-led description, show official task-details UI once rights/access cleared.
2. Explain selection, tile skipping and Review; scanning is not executing Run.
3. Distinguish Downloads duplicate step from other modules; inspect each category.
4. Checklist: originals, rebuildable data, unknown app data, backup, permission, rebuild/download cost and exact action.
5. Use labelled Space preview to explain why category totals do not authorize deletion.
6. One bounded disclosed recommendation: “Breathing Room, which we build,” for investigation if preview/hosted/runtime limits acceptable; CleanMyMac for documented broader maintenance and appropriate edition.

**Interaction pass:** non-mutating review checklist; no deletion commands, compulsory demo repo, signup or invented results. Link `/comparisons/cleanmymac/` and `/comparisons/`. Add cache/rebuild tool only after route/behavior verified. About 900–1,400 words if earned. **Drafting not allowed yet.**

## Concise comparison brief

**Title:** “Breathing Room vs CleanMyMac: cleanup or investigation?” **Route:** `/comparisons/cleanmymac/`.

Short purchase/use decision with cited matrix: platform/runtime, scan/approval, storage, helpers/monitoring, recurring growth, developer caches, price/edition, local/hosted boundaries. Unknown means “not verified,” not negative checkmarks. Link workflow article instead of repeating its steps. No duplicate alternatives doorway page.

**Advantages/trade-offs (editorial judgments):**

- CleanMyMac documents broader maintenance including malware, app and duplicate workflows; one-time current-major and subscription choices. Editions and paid major upgrades matter. No effectiveness benchmark performed.
- Breathing Room’s source-visible project/app/storage investigation may suit context-first readers wanting free local core. Preview, Python, signing/notarization and hosted-AI caveats make it not a verified substitute for every module.
- Both document review controls and monitoring. Do not manufacture absence, superiority or savings to differentiate.

## Open questions and handoff

**Critical:** exact payable price and cleared accessible competitor screenshot. These block drafting. **Noncritical if qualified:** current exact EULA/repo, architecture/permissions, offline/privacy boundaries, helper grouping, recurring-path attribution and CLI caches. Changelog includes dated releases and an “in progress” section; directory CLI news and roadmap text do not prove shipped CLI capability.

No native app launch/install, cleanup, benchmark, credential/account access, purchase, message, commit, push or deploy. No site build necessary: site unchanged. Independent editorial/runtime/rendered review remains separate.

`validation.json` retains actual checks: source hashes, claim excerpts, selected image hash and packet structure. Receipt reports **blocked**, not completion based on prose alone.
