# AVG PC TuneUp research packet

**Research retained; drafting blocked by competitor-image reuse rights.** No article or website record was created. Canonical owner: `avg-pc-tuneup`. This is a Mac-replacement research intent, not a claim that Breathing Room runs on Windows.

Source checks used the observed UTC clock on **October 21, 2026**. The task environment says October 22; actual browser/shell timestamps are preserved rather than relabeled. See `research.json` for claim-level excerpts, URLs, scope, check dates, matrix, visual manifest and access failures.

## Identity, aliases and discovery

Reused `docs/content/verification/batch-2.json` and its two raw captures first. Their SHA-256 values match the files. No redundant AlternativeTo or PC-homepage request was made.

- Discovery: <https://alternativeto.net/software/avg-pc-tuneup/about/>; retrieved `2026-10-21T19:07:02.842Z`.
- Edge: Mole, page 2, <https://alternativeto.net/software/mole/?p=2>; retrieved `2026-10-21T18:37:09.298Z` (existing manifest provenance).
- Directory official link: `https://www.avg.com/avg-pctuneup`; cached final page: <https://www.avg.com/en-us/avg-pctuneup>.
- Official Windows name: **AVG TuneUp for PC**. Separate linked Mac edition: <https://www.avg.com/en-us/avg-tuneup-for-mac>. Support also calls that edition **AVG TuneUp Premium for Mac**.
- `canonicalOwnerId: avg-pc-tuneup`; retain this owner and **skip separate name-only alias drafts**. No evidence associates this record with PowerMyMac. Do not research/edit another queue job on that assumption.
- Classification: Windows-origin/platform-adjacent discovery, with direct storage-cleanup overlap through AVG's separate Mac edition. Not dead on current official offer/support evidence. No official source repository established; unknown is not proof none exists.

## Verified decision facts and limits

These are documentary findings, **not hands-on testing**. The full matrix in JSON maps every row to claims.

| Decision | AVG evidence | Breathing Room boundary |
| --- | --- | --- |
| Platform | PC page documents Windows; Mac has separate product/support instructions (`identity`, `windows-scope`). | macOS 13+ preview only; no Windows substitution (`br-preview`). |
| Cleanup review | Mac Clean clutter permits post-scan file selection; guide offers Select none (`mac-cleanup`). | Inspect location, method and rebuild/download cost; no safety guarantee (`br-workflow`). |
| Duplicates/photos | Identical-content duplicate detection; oldest/newest/manual selection; blurry/badly lit/similar photo analysis (`mac-duplicates`, `mac-photos`). | Comparable duplicate/photo tools not established; do not imply parity. |
| App/startup management | Mac uninstaller and applications/launch-agent/daemon startup list documented (`mac-apps-startup`). | Grouped app/helper CPU and memory observations are a different job, not a proven full uninstaller (`br-workflow`). |
| Automation | Configurable automatic browser scans, cookie allowlist and optional timed Trash deletion (`mac-automatic-browser`, `mac-trash`). | Daily care reuses exact approvals while app runs; optional automatic Ruff mode needs separate disclosure (`br-approvals`). |
| Monitoring | FAQ mentions System Monitor plus free-space/clutter alerts (`mac-monitoring`). | Activity observations/source support, not a complete audit trail. AVG history/helper-grouping equivalence unknown. |
| Developer caches | npm/pnpm/uv-specific adapters not verified. | Source includes tool-aware cache adapters; no cross-machine certification (`br-workflow`). |
| Access/privacy | Installed scanner; internet for activation/updates; account or code activation and app-usage sharing controls documented (`mac-local-hosted`). | Free local tools; hosted authenticated agent can send relevant paths/tool outputs. Not entirely offline AI (`br-offer`). |
| Paid access | Mac cleaning needs subscription; unactivated installation is scan-only (`mac-paid`). Sales page restricts personal/family, not commercial use (`personal-use`). | Free core, optional AI Care $5 USD/month or $50 USD/year; quota/entitlement behavior not independently tested. |

### Versions, OS conflict and installation

[Dedicated requirements](https://support.avg.com/SupportArticleView?l=en&urlName=avg-system-requirements) identify **AVG TuneUp 26.x for Windows** and **4.x for Mac**, not exact patch versions. Mac requirements list 64-bit Intel or Apple silicon (M1), 512 MB RAM (1 GB preferred), 750 MB free space, internet for download/activation/updates, and minimum 1024×768 display resolution. These are vendor requirements, not hardware or binary tests.

**Do not flatten the conflicting Mac footers:** the cached PC page says “MacOS 10.10 (Mavericks)” (including that inconsistent version/name pairing), the Mac sales page says 10.12 Sierra, and the dedicated 4.x list starts at 10.13 High Sierra. The latter is the more specific source, but old-OS install recommendations remain blocked pending clarification. The support page's newer “macOS 27 (Golden Gate)” wording and installation warning are vendor statements, not independent Apple/OS verification.

The [Mac installation section](https://support.avg.com/SupportArticleView?l=en&urlName=Install-AVG-TuneUp&option=mac) documents `avgtuneup.dmg`, licence acceptance, administrator authorization and a possible restart. No installer was downloaded, launched or inspected; signing/notarization and successful installation are unknown. No research step followed any vendor cleanup or system-setting instructions.

### Pricing and trial conditions

The US Mac marketing DOM at `2026-10-21T22:28:05.681Z` showed:

- 1 device: **$69.99**, described as **$5.83/month equivalent**; public purchase link identifies a 12-month SKU.
- 10 devices: **$34.99 promotion**, **$84.99/year renewal comparison**, described as **$2.92/month equivalent**; public link identifies a 12-month SKU.

These are locale-specific displayed dollar offers, **not month-to-month billing**, and not checkout verification. Single-device renewal, tax, complete initial-term/renewal and cancellation terms remain unverified. Clicking the public “Subscription details” text did not expose additional terms in the snapshot; no checkout link was followed. Do not claim cheapest or recommend a purchase from these partial conditions.

The cached PC landing page advertises seven days without a credit card. The [Windows FAQ](https://support.avg.com/SupportArticleView?l=en&urlName=avg-tuneup-faq) says a payment method is required and a paid subscription begins unless canceled. Different channels may explain this, but no reconciliation was established. **Neither statement proves Mac trial terms.** Keep the conflict explicit, or omit trial advice.

## Required visuals

### AVG: real app UI located, link-only pending rights

- Source: <https://www.avg.com/en-us/avg-tuneup-for-mac#mac>.
- Exact asset: <https://static2.avg.com/10005021/web/i/page/avg-tuneup-for-mac-v2/media-clutter-3.png>.
- DOM natural size: **664×351**. An owned-tab element screenshot was opened and read: a laptop illustration contains the real AVG TuneUp Premium dashboard with clutter, browser, duplicate, photo, uninstall and startup controls. The displayed **1.14 GB** is vendor illustrative content, not our result.
- Caption: “Official AVG TuneUp for Mac dashboard illustration. Vendor example figures, unknown version/capture date; not our test or measured cleanup. Image linked only pending reuse clearance.”
- Alt: “AVG TuneUp Premium Mac dashboard with clutter, browser, duplicate, photo, app-removal and startup-item tools inside a laptop illustration.”
- **Reuse basis is not established.** The footer reserves rights. No permission request sent; no third-party original downloaded or placed in the repository/site. Original/published hashes are honestly null. Tool inspection of rendered UI is not publication permission.
- Small/soft dashboard labels need target-layout review or a clearer rights-cleared official asset. Link fallback does **not** pass the on-page visual gate.

### Breathing Room: reuse the selected current-source preview

Selected `current-space-browser-preview` from `docs/content/screenshots.json`:

- Original: `docs/content/assets/breathing-room/space-preview-2026-10-21.png`.
- SHA-256: `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a` (verified this job).
- Capture: `2026-10-21T19:06:45.416416+00:00`; source commit `54828ac3170b45861aee70861dd0b9c658ed7e51`; **2940×3468**.
- Caption: **“Current-source Breathing Room Space browser preview, captured October 21, 2026. Example data only; not a native scan, measured activity or cleanup result.”**
- Alt: “Breathing Room Space browser preview with visible example-data warning, storage categories and app/tool/project exploration tabs.”

Opened and read the actual PNG again in this job. The example-data banner is visible; the assistant composer overlaps part of the chart. Retain the disclosure and independently verify the eventual layout. This is the library's current-source illustration, not a new capture, native measurement or proof of binary feature parity. First-party owner-requested reuse is documented; third-party marks stay their owners' marks. No shared asset was edited or copied into the site.

## Distinct workflow article brief

**Proposed title:** Moving from PC tune-up habits to Mac storage review  
**Proposed slug:** `from-pc-tuneup-to-mac-storage-review`  
**Track:** Search/reference. Primary reader: an AVG PC TuneUp user moving to Mac, choosing between duplicate/photo housekeeping and developer-cache investigation.

Lead with the platform boundary, not “a faster Mac.” A useful migration worksheet distinguishes intentional duplicate copies, similar photos, generated caches, owning tools, rebuild/download costs and automation permissions. AVG's Keep oldest/newest selectors provide a concrete reason to inspect locations rather than equating identical bytes with unwanted files. Breathing Room's source-supported owner/cache review is a different choice, not a substitute duplicate-finder claim.

Outline:

1. Carry over the maintenance goal, not Windows registry/Sleep Mode assumptions.
2. Separate identical files, similar photos and rebuildable caches.
3. Review duplicate locations before automatic oldest/newest selection.
4. Inspect app/tool ownership and rebuild cost before a cache approval.
5. Audit browser, Trash and exact-location automation separately.
6. Choose the documented Mac tool or explicitly accept preview limitations.

**Interaction handoff:** A non-destructive decision worksheet: Windows-only need → no Breathing Room replacement; personal duplicate/photo task → AVG's documented controls; business use → flag AVG's sales restriction; development-cache task → inspect owner/cost before considering the preview. No run/delete button or invented savings calculator. This is a proposed decision aid, not an implemented/tested artifact.

Place the disclosed Space preview after the lead and the cleared AVG dashboard later. Link `/comparisons/` and `/comparisons/avg-pc-tuneup/`; routes are proposals, not created or link-tested here. One bounded recommendation must say **“Breathing Room, which we build.”** No fabricated migration experience, benchmarks, FAQ or generic renamed template.

## Concise comparison brief

**Title:** AVG TuneUp and Breathing Room: choosing on Mac  
**Route:** `/comparisons/avg-pc-tuneup/` (proposal only).

Answer the Mac choice in a short matrix, preserving the Windows-origin discovery name. Favor AVG when its documented duplicate/photo/app/startup controls match a permitted personal-use task. Consider Breathing Room's free local storage/process core and tool-aware source workflow for ownership/rebuild-cost investigation only with all preview caveats. Do not equate the optional hosted subscription with an AVG licence or declare a universal price winner. Link the deeper migration worksheet instead of expanding the comparison into a duplicate article.

Truthful trade-offs:

- AVG has documented Mac review controls, browser automation, monitor/alerts and duplicate/photo handling. It must not be caricatured as lacking approvals or monitoring. Paid cleanup, use restrictions and incomplete price/trial conditions matter.
- Breathing Room has a free local core and inspectable source workflow, but remains a non-notarized **0.1.0-preview.1** preview with **Python 3.10+**, incomplete installation/Intel validation, hosted authentication/data boundaries and no established duplicate/photo parity. Daily care requires the app running; optional automatic Ruff mode is separate from ordinary review.

Current local README, release notes, native config, billing config and developer-cache source were checked against the October 21 capabilities register. Existing public release/pricing evidence was reused rather than fetched needlessly. Source implementation is not installed-binary validation.

## Blocking diagnostic and handoff

**Critical:** Obtain documented image reuse clearance or an explicit approved policy decision for the exact official AVG UI asset (or another authorized real capture). Only then download permissible original bytes, preserve hashes and provenance, and independently assess narrow-screen legibility/privacy. Do not silently hotlink to evade rights review.

**Claim-specific:** Resolve legacy OS conflicts before old-Mac installation advice. Resolve channel-specific trial and complete billing conditions before no-card, Mac-trial or numeric buying recommendations. They can otherwise remain explicit unknowns/omitted recommendations; image rights still block drafting.

No native test, cleanup, account creation, purchase, credentials read, messages, settings change, site build, commit, deployment, queue or database modification occurred. Only tab 190 was owned by this run. No independent approval or publication score is claimed. Structural/hash validation results are retained in `validation.json`; the attempt receipt records **blocked**, not article completion.
