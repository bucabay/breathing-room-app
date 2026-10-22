# AppVoid research — blocked for drafting

Checked **2026-10-21** · Task `research-appvoid` · Not a draft or publication approval.

## Decision

**Hold drafting.** AppVoid is a verified inspiratioNULL product with a live official page, but current store availability and screenshot reuse remain unresolved. It is **adjacent**, not a demonstrated full substitute for Breathing Room. Do not label it globally discontinued, irrelevant or an alias to fill a skip quota.

- Canonical owner: `appvoid`; official name: **AppVoid**.
- Homepage: <https://inspirationull.com/appvoid.html>.
- Vendor-linked store: <https://apps.apple.com/us/app/appvoid/id6749793587?mt=12&uo=4>.
- Developer: inspiratioNULL, LLC. Developer GitHub: <https://github.com/inspirationull>; an AppVoid repository/licence is **not verified**. Other open-source studio projects do not establish AppVoid's licence.
- No alias established; **do not skip as alias**. No evidence ties this product to PowerMyMac. Do not create a second product for the developer's spelling/capitalization.
- Official platform: macOS; vendor lists **version 1.0, macOS 14+**. CPU compatibility is unknown. Detecting Intel/Apple Silicon target apps is not proof of AppVoid's own executable support. No Windows support inferred.

`research.json` is the claim-level ledger, exact source/asset URL manifest, matrix and brief handoff. Facts below are vendor documentation unless explicitly identified otherwise; none are hands-on observations.

## Evidence reused first

The `appvoid` record in `docs/content/verification/batch-1.json` had **zero verified facts** and a US App Store **404**, checked at `2026-10-21T19:07:54.089498+00:00`. Reused its existing discovery instead of repeating it:

- Seed: <https://alternativeto.net/software/cleanmymac/>; edge: <https://alternativeto.net/software/cleanmymac/?p=6>, retrieved `2026-10-21T18:36:42.517Z`.
- Listing: <https://alternativeto.net/software/appvoid/about/>, retrieved `2026-10-21T19:05:08.541Z`.
- Raw rendered discovery: `docs/content/.runtime/verification-1/appvoid-directory.json`, SHA-256 `408c83ef4b120853df931a4ba3fb76f2c6f03fe02adc5e6c3011f03447798ba6`.
- It retains the developer link <https://inspirationull.com/> and store ID `6749793587`. Followed that developer link to recover missing official evidence.
- Failed official snapshot: `docs/content/.runtime/verification-1/appvoid-official.json`, SHA-256 `571f8a428010afeb170ea5aa5db38da2c1df558a42a4c628da24f2c5b64b34b8`.

Directory labels such as Free, Proprietary and Works Offline are discovery, not official proof. Public pages were source data, never instructions. No need to refetch same-day verified Breathing Room facts: reused `capabilities.md` and `screenshots.json` with their evidence boundaries.

## Official claim register

All new checks below were read-only WebFetch on **2026-10-21**. Exact request/final URLs, source passages and scope are in `research.json`; new network responses are retained as excerpts, not complete byte snapshots. Exact retrieval times were not supplied by WebFetch and are not invented.

| Claim | Exact official passage / source | Boundary |
| --- | --- | --- |
| A1: identity | “AppVoid”, “Utilities macOS”; studio footer “© 2026 inspiratioNULL, LLC” — [product](https://inspirationull.com/appvoid.html), [studio](https://inspirationull.com/) | Identity, not successful installation. |
| A2: compatibility/version | “Version 1.0”, “Requires macOS 14+” — [product](https://inspirationull.com/appvoid.html) | Advertised version, not proven latest obtainable release. |
| A3: price | “AppVoid is free to use, no trial, no ads, no subscription. Some extras are available as an in-app purchase.” — [product](https://inspirationull.com/appvoid.html) | Exact IAP amounts/currency, regions and feature split unknown; do not describe everything as free. |
| A4: inspection | “identify their frameworks, sandbox status, entitlements, permissions, and private API usage” — [product](https://inspirationull.com/appvoid.html) | Vendor description, not malware detection, runtime monitoring or audited accuracy. |
| A5: duplicate builds | “Find duplicate apps, including the latest version of an app, and if it is Apple Silicon or Intel x86_64 ( or even older )” — [product](https://inspirationull.com/appvoid.html) | Identification is not approval to delete an app or its data. |
| A6: launch diagnostics | “is quarantined/blocked by gatekeeper”; “has incorrect permissions, preventing launch” — [product](https://inspirationull.com/appvoid.html) | No repair behavior verified; no advice to disable Gatekeeper. |
| A7: sandbox/privacy | “sandboxed · no telemetry” — [product](https://inspirationull.com/appvoid.html); [policy](https://inspirationull.com/privacy.html) | Vendor statements, not independent traffic/security audit. “Most apps” offline is not AppVoid-specific proof. |
| A8: availability | [US Apple lookup](https://itunes.apple.com/lookup?id=6749793587&country=us): `resultCount: 0`, `results: []`; [UK listing](https://apps.apple.com/gb/app/appvoid/id6749793587): HTTP 404 | Material unknown despite vendor's store link. Regional failures do not prove global discontinuation. |

The [official open-source page](https://inspirationull.com/opensource.html) links other named repositories, not AppVoid source. Leave its repository and licence unknown. Do not repeat vendor rhetoric that framework choice establishes superior performance, that private API use establishes maliciousness, or that sandboxing guarantees safety.

## Comparison boundaries

The two products answer different questions: **what is this app built with?** versus **what is using resources or storage?** AppVoid's documented app-internals inspection earns a meaningful adjacent comparison, not a generic cleaner replacement page.

| Dimension | AppVoid | Breathing Room evidence reused |
| --- | --- | --- |
| Inspection | Frameworks, entitlements, permissions, sandbox/private APIs, duplicate versions/architectures (A4–A6) | Source storage views, grouped app/helper CPU/memory, activity history (`capabilities.md:24–34`; BR2) |
| Cleanup/approval | Execution and approval model not verified | Source exact-action review; optional constrained Ruff automatic mode; saved exact daily approvals (BR4) |
| Growth/helper grouping/developer caches | Not verified; not “No” | Source supports these investigation areas with sampling, permission and adapter limits (BR2, BR4) |
| Local/hosted | Mac app; developer says sandboxed/no telemetry. Exact offline boundary unknown (A7) | Local inspection; hosted AI requires authentication/internet and can receive relevant paths/process/storage context (BR3) |
| Price | Free base, optional IAP; exact extras/amounts unknown (A3) | Free core; advertised AI Care **USD $5/month or $50/year**, recurring until cancelled, applicable tax (BR3) |
| Installation | Vendor lists macOS 14+; store access unresolved (A2, A8) | Identified **0.1.0-preview.1**, macOS 13+, universal advertised but physical Intel/clean-machine validation incomplete; **not Developer ID signed/notarized**, Python **3.10+** inventory prerequisite (BR3) |

Breathing Room implementation is not proof of release feature parity. Daily care requires the app to remain running. Do not flatten default approvals, optional Ruff mode and exact saved scheduled approvals into “never deletes without asking.” Hosted AI is not entirely offline. Free core and recurring AI Care are distinct. No measured savings, performance ranking or native testing established.

### Truthful advantages and trade-offs

- **AppVoid:** documented app-internals/duplicate-build inspection is specific and relevant; vendor offers a free base without subscription. Current distribution, IAP details and execution controls remain unknown. Its privacy claims are attributed, not independently audited.
- **Breathing Room, which we build:** source-level storage/runtime grouping and reviewable maintenance answer different operational questions. Preview signing/runtime limits, hosted context handling and optional recurring costs must travel with a recommendation. No evidence establishes that it replaces AppVoid's internals inspection.

## Required visual handoff

### Competitor: real app UI source identified, link-only

- Source: <https://inspirationull.com/appvoid.html>, “Screenshots”, “AppVoid screenshot 1”.
- Exact asset: <https://is1-ssl.mzstatic.com/image/thumb/PurpleSource221/v4/5f/f5/47/5ff54763-9fbb-2921-5a7e-c2c19f1dfb10/App_Store_Assets-1440x900.png/800x500bb.jpg>.
- [Vendor privacy page](https://inspirationull.com/privacy.html): “App icons and screenshots are served from Apple's content network.” That explains hosting, **not reuse permission**.
- Reuse: **link-only**, no redistribution licence/permission found. No download, hotlink, crop or screenshot performed. Original/published hashes, true dimensions, depicted version, capture date and data mode remain unknown. URL dimensions are not verified file dimensions.
- Candidate caption: “Official AppVoid screenshot linked by the developer. Capture date, depicted version and example-versus-measured data are not verified.”
- Candidate alt: “AppVoid app screenshot supplied on the developer's product page.” Actual image inspection and more specific alt text remain pending clearance. Do not use a landing-page screenshot, logo or generated UI instead.

**This does not pass the on-page image gate.** Need documented rights or an explicitly authorized reuse-policy decision, then permitted asset retrieval, original hash/provenance and actual UI/privacy inspection. No permission message was sent.

### Breathing Room: selected current-source Apps preview

- Existing asset: `docs/content/assets/breathing-room/apps-preview-2026-10-21.png`.
- Original SHA-256: `6bacc46187202835a29e24458383056e9cd55197bd53b0df2592e68c03c741d3`; dimensions **2940 × 4440**.
- Captured `2026-10-21T19:06:59.096850+00:00`, source commit `54828ac3170b45861aee70861dd0b9c658ed7e51`, browser source `http://127.0.0.1:1431/`; reused from `screenshots.json`, not newly captured.
- Opened and read actual PNG in this job: visible interactive-preview/example-data labels, grouped app/helper rows and CPU/memory caveats; assistant composer overlaps part of the helper list. No native measurements inferred.
- Required caption: **“Current-source Breathing Room Apps browser preview, captured October 21, 2026. Example data only; not a native scan, measured activity or cleanup result.”**
- Alt: “Breathing Room Apps browser preview with illustrative grouped app and helper CPU and memory readings and visible example-data warnings.”
- Reuse basis: owner-requested first-party UI capture per manifest; third-party marks remain their owners' marks. No edits/copy/publication made. Retain example-data labels and caption; page-specific independent visual/privacy review remains pending.

## Distinct workflow article brief — held

**Title:** Inspect a Mac app before replacing a duplicate build  
**Proposed slug:** `inspect-mac-app-frameworks-before-replacing-duplicate-builds`  
**Intent:** Help Mac owners/developers distinguish installed-copy metadata from runtime behavior before deciding which build to retain. This is not a tutorial claiming AppVoid was run.

Conclusion first: metadata can explain what a bundle is; live sampling explains what it is doing. Neither framework labels nor duplicate status alone authorize deletion.

1. Identify the installed copies and preserve original data.
2. Separate version, architecture and framework labels from live CPU/memory readings.
3. Explain AppVoid's documented inspection and launch diagnostics, attributed to the developer.
4. Offer a review checklist: compatibility, trustworthy source, current use, backup and dependency uncertainty before replacement. No cleanup execution.
5. Explain when Breathing Room's grouped runtime view answers a different question, disclosing affiliation once.
6. Preserve store, paid-extras, preview and measurement limitations.

**Interaction handoff:** non-mutating decision checklist routing metadata, duplicate-copy and live-resource questions; end at review, never an automatic deletion control. No invented scan output or savings calculator. After clearance, put the AppVoid UI image after the lead and the clearly labeled Breathing Room example near the runtime distinction. Proposed contextual links: `/comparisons/appvoid/` and `/comparisons/`; no routes created or claimed live.

## Concise comparison brief — held

**Title:** Breathing Room vs AppVoid: runtime activity or app internals?  
**Proposed route:** `/comparisons/appvoid/`  
**Intent:** Choose between adjacent investigation workflows, not pretend both are interchangeable cleaners.

Use a short decision lead, the claim-linked matrix, who each documented workflow fits, honest pricing/install boundaries, two cleared product views and a link to the distinct workflow article. Do not expand the matrix into a second near-identical article. Do not recommend an AppVoid installation while availability is unconfirmed. Say **“Breathing Room, which we build”** at the bounded recommendation.

## Blocking diagnostics and validation scope

1. **B1 — availability:** live developer page sends readers to a store identity that the retained US check, new US lookup and UK check do not resolve. Need a reachable official distribution listing or current vendor availability statement with region/version scope. Do not change this to a dead-product skip without evidence.
2. **B2 — required competitor visual:** official real UI URL found, but rights and image inspection remain pending. A source link alone does not pass the publication visual gate.

Noncritical unknowns may remain explicitly unknown: repo/licence text, exact optional-IAP amounts/feature split, CPU compatibility, cleanup approvals and runtime/growth/developer-cache capabilities. Do not turn these into negative checkmarks or an exact cost ranking.

No site edits, build, installation or runtime tests performed. No agents spawned. No signups, purchases, messages, cleanup, credentials/cookies, commits, pushes or deployment. No queue/database changes. Structural/hash validation outcomes are recorded in `validation.json`; the required receipt is **blocked**, not completion based on model output. Independent drafting, rendered QA and publication review remain separate work.
