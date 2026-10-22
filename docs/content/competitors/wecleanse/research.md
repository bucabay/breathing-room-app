# WeCleanse research: blocked, not a draft

Task: `research-wecleanse`. Checked at clock UTC **2026-10-21T22:22:38Z** (session-local date October 22). Owned output: this folder and the required receipt only.

## Decision

**Do not draft a workflow article or comparison yet.** Reused `verification/batch-2.json`’s WeCleanse record first. It contains no verified official product facts. The listed homepage failed TLS validation in the retained baseline; a new webfetch also failed. A second official-domain page found through search failed transport too. This is not proof the product is dead or irrelevant.

`canonicalOwnerId: wecleanse` preserves the existing manifest routing identity only. Official name, ownership, repository and aliases remain unverified. No alias skip is justified, and no connection to PowerMyMac is established. Hold rather than create a separate unsupported doorway page or merge unrelated products.

## Evidence retained and reused

The JSON packet has source/claim IDs, exact URLs, excerpts, timestamps and original hashes. Existing captures are referenced in place, not copied or altered:

- **S1 / C1:** [AlternativeTo about page](https://alternativeto.net/software/wecleanse/about/), retrieved `2026-10-21T19:06:42.203Z`; excerpt “Official Website / minicreo.com/wecleanse/”. Raw: `docs/content/.runtime/verification-2/wecleanse-directory.json`. SHA-256 `f82c600fce0d75b789a7e33cf00d1964df0be868503409d4e8962be1aced4af8`.
- Manifest discovery edge: CleanMyMac seed → `https://alternativeto.net/software/cleanmymac/?p=6`, retrieved `2026-10-21T18:36:42.517Z`. Directory text describes Free / Proprietary / Mac; these are discovery labels, not current official pricing, licence or compatibility evidence.
- **S2 / C2:** [Listed official homepage](https://www.minicreo.com/wecleanse/), retained fetch `2026-10-21T19:09:50.677437+00:00`: `CERTIFICATE_VERIFY_FAILED`, self-signed certificate. Raw: `docs/content/.runtime/verification-2/wecleanse-official.json`.
- **S3 / C2:** Baseline browser returned privacy error `NET::ERR_CERT_AUTHORITY_INVALID` at `2026-10-21T19:12:14.413Z`, not product content. Raw: `docs/content/.runtime/verification-2/wecleanse-browser.json`. This job did not repeat browser work or bypass warnings.
- **S4 / C2:** One current webfetch to the homepage: `Transport error (GET https://www.minicreo.com/wecleanse/)`. No content, excerpt or final destination established.
- **S5 / C2:** Search `WeCleanse site:minicreo.com` located [a MiniCreo cleaner article](https://www.minicreo.com/mac-cleaner/best-free-mac-cleaner.html). Fetch returned a transport error. The search snippet is a lead only, not official fact verification.

No already-current verified fact was re-fetched. Source update dates and exact product version are unknown. Check outcomes describe access from this worker, not global availability.

## Identity and fit gates

Directory evidence suggests possible direct Mac storage-cleanup overlap. **Classification remains not verified** until official product content can be read. There is no established Windows/Linux support and no reason to invent a non-Mac replacement angle. Current macOS minimum, architectures, release/version, installation/signing/runtime requirements, local/hosted model, cleanup selection/approval, licence and full price conditions are unknown. Helper grouping, recurring-growth monitoring and developer-cache scope are unknown, not absent.

## Visuals

### Competitor: blocked

Candidate source page: `https://www.minicreo.com/wecleanse/`. **Real app screenshot asset URL: unknown. Reuse basis: unknown/pending.** No competitor image was downloaded. No logo, webpage screenshot, generated UI or search thumbnail substitutes for app UI. A source link alone does not satisfy the image gate. Need an actual official/authoritative app UI asset, provenance, version/data labels, caption/alt and permitted reuse basis before embedding. Public access alone is not permission; no permission request was sent.

### Breathing Room: selected existing current-source Space preview

- Path: `docs/content/assets/breathing-room/space-preview-2026-10-21.png`.
- SHA-256: `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a`; 2940 × 3468.
- Original capture: `2026-10-21T19:06:45.416416+00:00`, source commit `54828ac3170b45861aee70861dd0b9c658ed7e51`, `http://127.0.0.1:1431/`.
- **Required caption:** “Current-source Breathing Room Space browser preview, captured October 21, 2026. Example data only; not a native scan, measured activity or cleanup result.”
- Alt: “Breathing Room Space view rendered in a browser with illustrative example data.”
- Reuse: first-party app-owner-requested capture per `screenshots.json`; third-party marks remain their owners’ marks. Page-specific independent review pending. No asset copied/published or edited.
- Opened and read the actual PNG in this job: visible interactive-preview and example-data disclosures; categories and navigation visible; floating composer overlaps chart content. Keep disclosures and review final narrow-screen legibility. Current-source designation is inherited from the capture review, not a fresh render or native release validation.

## Conditional workflow brief

**Title:** Investigate Mac System/Other storage before choosing a cleaner. **Reserved slug:** `wecleanse-mac-workflow`. Track: search/reference. Reader job: understand what occupies space before deciding whether anything is disposable; not “run WeCleanse and save X GB.”

1. Identify large categories without treating size as deletion permission.
2. Separate rebuildable caches from personal originals and backups; explain rebuild/download costs.
3. Verify any cleaner’s current compatibility, distribution and review controls before recommending it.
4. Choose inspection versus a documented cleanup workflow, with explicit uncertainty and backups.

Interaction handoff: a non-destructive decision checklist covering owner, backup, rebuild cost, exact location, method and approval. No arbitrary code demo or fabricated savings. Obtain official Apple support references for macOS instructions at drafting time. Without a verified WeCleanse-specific workflow, do not turn this general idea into a product-targeted doorway article.

## Conditional concise comparison brief

**Title:** Breathing Room vs WeCleanse: evidence and decision criteria. **Reserved comparison slug:** `wecleanse`. Intent: product choice, not repeated workflow prose. Use a short sourced matrix for availability/platforms, scan/review model, local/hosted boundary, app/helper investigation, recurring growth, developer caches, price and installation caveats. Unknown is “not verified,” never “No.” Link to the hub and counterpart only after checking routes. No separate alternatives page or winner claim.

WeCleanse strengths/trade-offs cannot yet be assessed from official evidence. Do not turn directory “free/lightweight” into a price or speed advantage. Breathing Room’s inspected source offers storage exploration, grouped monitoring and reviewable cleanup architecture; this is not binary parity, an independent benchmark or proof of superiority over WeCleanse.

Use “Breathing Room, which we build,” with any recommendation. Reuse the current `capabilities.md` baseline: `0.1.0-preview.1`, macOS 13+, advertised universal installer with untested physical Intel/clean-machine paths, Apple Development signed but not Developer ID signed/notarized, Python 3.10+ requirement. Free local tools differ from hosted authenticated AI; relevant tool context may leave the Mac. AI Care is advertised at $5 USD/month or $50 USD/year, renewing with applicable tax; no unlimited allowance established. Daily care requires the app running and exact saved approvals; narrow opt-in Ruff automation qualifies blanket approval language. These caveats can make another verified tool or built-in tools preferable; do not recommend installation as production-ready.

## Precise unblock requirements

1. Securely reachable official identity/product documentation or an authenticated official relocation announcement. Retain exact passages and dates; never disable certificate checking.
2. Establish current availability, platform/version, licence/price conditions and core scan/review workflow. Resolve any observed aliases with official evidence before separate drafting.
3. Identify real competitor app UI, exact asset URL and reuse evidence. Preserve original bytes/hash if download is permitted; otherwise keep blocked/link-only.

No product installed or tested; no cleanup, accounts, credential access, messages, purchases, browser recovery, site changes, commits, pushes, deployments or queue/database edits. No site build applies to this research-only change. Actual file/hash/schema checks are recorded in `validation.json`; independent publication review remains pending.
