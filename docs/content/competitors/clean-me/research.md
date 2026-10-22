# Clean Me: research handoff

Checked **2026-10-21** · `research-clean-me` · research only, no article or publication approval.

## Decision

Keep canonical owner **`clean-me`**. Clean Me / Clean-Me / Clean me.app are spelling and bundle-name variants evidenced on the official homepage and its linked repository; skip separate drafts for those variants. There is no evidence here linking this identity to PowerMyMac, and no unrelated alias job was performed.

Official identity: [Kevin De Koninck's homepage](https://kevin-de-koninck.github.io/Clean-Me/) → [official repository](https://github.com/Kevin-De-Koninck/Clean-Me). This is a direct **storage analysis and selected-cleanup** overlap, not a proven substitute for every Breathing Room feature. It is already a Mac product; no invented Windows support or Mac-replacement rationale is needed.

The repository was archived **January 6, 2022**. Do not call it actively maintained, but do not call its downloads dead: the official latest-release API lists **v1.4.2**, published **July 19, 2020**, with `Clean.Me.app.zip`. Release documentation explicitly names **Catalina (10.15.x)**; inspected source sets deployment target `10.15`. Neither is proof of compatibility with every newer macOS or Apple Silicon. No binary was downloaded, installed or tested.

Research is complete for the narrow briefs below, with noncritical unknowns retained. Any expanded modern-installation recommendation is blocked pending runtime/architecture/signature evidence. Publication remains pending independent draft and visual review.

## Reused evidence and new checks

First reused the `clean-me` record in `docs/content/verification/batch-1.json` and its retained official, repository and directory snapshots. No matching batch-2 record was found. Identity, macOS purpose, archive status and baseline MIT licence were not needlessly fetched again. Reused today's `capabilities.md` and `screenshots.json` for Breathing Room; this is not a new native test or a new screenshot capture.

New targeted public reads addressed missing release scope, licence conditions, app screenshot provenance, source-path ambiguity and installation availability. `sources/acquisition.json` retains exact requested/final URLs, real retrieval timestamps, HTTP outcomes, paths, original byte counts and SHA-256. The source/claim ledgers in `research.json` carry excerpts, checked dates, conditions and intended locations. `validation.json` records actual local structural/hash checks, not inferred success.

Discovery: [Clean Me on AlternativeTo](https://alternativeto.net/software/clean-me/about/), retained at `docs/content/.runtime/verification-1/clean-me-directory.json`, retrieved `2026-10-21T19:05:44.710Z`. Prior rendered edges are CleanMyMac page 2 (`18:36:23.710Z`) and Mole page 4 (`18:37:13.603Z`). Their exact URLs and retained capture references are in the JSON. AlternativeTo's “Free” and “Discontinued” labels are discovery metadata, not our proof of pricing or binary availability.

## Facts usable with their boundaries

| Claim IDs | Supported wording / excerpt | Source |
| --- | --- | --- |
| CM01–02 | “A macOS system analyser and cleaner”; “archived ... Jan 6, 2022 ... read-only.” | [Homepage](https://kevin-de-koninck.github.io/Clean-Me/), [repository](https://github.com/Kevin-De-Koninck/Clean-Me) |
| CM03–04 | `v1.4.2`, published `2020-07-19T10:24:58Z`; “Supported macOS version: Catalina (10.15.x)”. Modern runtime/architecture unknown. | [Official release](https://github.com/Kevin-De-Koninck/Clean-Me/releases/tag/v1.4.2), retained API metadata |
| CM05 | MIT permission “free of charge,” with copyright/permission notice preserved. Public release asset is listed; no mandatory purchase established. Not a commercial-support or hosted-service entitlement. | [Pinned licence](https://raw.githubusercontent.com/Kevin-De-Koninck/Clean-Me/bb6f0e031db28c037b1c95a1fec296fe68e132f5/LICENSE) |
| CM06 | Author says analysis was the main purpose and “I do not recommend you to delete your cache files.” Attribute this, not a universal performance claim. | Homepage, retained official snapshot |
| CM07 | “If you do not provide the password ... skip those files ... requires root and display 0 MB.” Documented behavior, not our observation. | Homepage, How to use Clean Me |
| CM08–09 | Clean deletes selected topics; folder icons open corresponding folders. Author says only directory contents are cleaned, and iMessage attachments require Full Disk Access. No rollback or Trash-only promise. | Homepage, usage/security/access sections |
| CM10 | “Normally Clean Me should not request an internet connection.” Author statement, not a network/privacy audit. | Homepage, security section |
| CM11 | Source maps Xcode device logs and DerivedData; Archives is commented out in the `xcode` mapping. | [Pinned Paths.swift](https://raw.githubusercontent.com/Kevin-De-Koninck/Clean-Me/bb6f0e031db28c037b1c95a1fec296fe68e132f5/Clean%20Me/Paths.swift) |
| CM12 | Old README documents Homebrew, but the checked cask API returned **404**. Omit current Homebrew installation instructions; this does not prove every tap is unavailable. | [Checked cask API](https://formulae.brew.sh/api/cask/clean-me.json), retained 404 body |
| CM13 | Helper grouping, recurring-growth monitoring and modern package-manager adapters **not verified**, not “No.” | Limits of the inspected official documentation/source |

Pricing conditions: root MIT licence explicitly permits use free of charge with notice retention, and the official API lists a public release asset. No paid plan, currency amount, subscription, mandatory donation, trial condition or paid support offer was established for Clean Me. Do not invent a commercial pricing table from the directory's “Free” label. Archive status does not change the permission statement or promise maintained support.

No cleanup, permissions change, installation, password prompt, account, purchase, telemetry audit or performance comparison was attempted. Do not copy the old site's protection-bypass, password or access instructions into a recommendation.

## Required visuals

### Official Clean Me app UI

- Original: `assets/clean-me-official-original.png`; exact source and pinned asset URL in `research.json`.
- Source page: official repository README, not a landing-page capture. Actual PNG was opened and visually read: category toggles, folder icons, “Requires root,” Analyse and Clean are visible.
- SHA-256: `895711d46c31155cfa71462639a6a1c5d11b40e9a9e04b8f07039c08f3ab9598`. No edits or published derivative.
- Reuse basis: repository-associated documentation image under root **MIT License**; preserve `assets/Clean-Me-LICENSE.txt` with copied/distributed asset and credit **Clean Me screenshot © Kevin De Koninck, MIT License**. No endorsement or blanket trademark permission is inferred. Independent publication-context review still pending.
- Caption: **Historical Clean Me app screenshot from the official repository. Capture date, app build and macOS version are unknown; displayed sizes are vendor illustration, not our scan or recovered space. © Kevin De Koninck, MIT License.**
- Alt: **Clean Me category toggles, folder inspection icons, root-required labels and separate Analyse and Clean buttons in the official historical screenshot.**
- Important conflict: the screenshot says “Xcode DerivedData and Archives,” but the inspected source comments Archives out. Show the label as historical UI only; do not assert Archives removal or infer release behavior from the image. Screenshot sizes and toggle states are not our measurements or verified defaults.

### Breathing Room Space preview

Selected `current-space-browser-preview` from `screenshots.json`: `docs/content/assets/breathing-room/space-preview-2026-10-21.png`. Actual PNG reopened and inspected; the example-data banner is visible. Original hash: `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a`.

Required caption: **Current-source Breathing Room Space browser preview, captured October 21, 2026. Example data only; not a native scan, measured activity or cleanup result.**

Alt: **Breathing Room Space view in a browser with visible example-data warning and illustrative storage categories.**

Keep “Interactive preview · example data” and the browser-preview warning visible. This is current-source UI at the recorded capture commit, not distributed-binary parity. Composer overlaps part of the chart; draft layout/derivative work must retain disclosures, log edits/hashes and receive independent narrow-screen/theme review. This job did not copy or modify the shared first-party asset.

## Distinct workflow brief

**Title:** Clean Me shows 0 MB: check permissions before cleanup  
**Proposed slug:** `clean-me-zero-mb-permissions-before-cleanup`  
**Track:** search/reference, bounded legacy-tool workflow.

Reader job: distinguish an empty category from an unscanned protected category without treating permission grants as the default solution. Open with the documented 0 MB ambiguity and archive/Catalina boundary. Put the official app UI immediately after the lead. Continue with folder inspection, selected-topic cleanup boundaries, original files versus rebuildable data, and the author's cache warning. Avoid install commands or instructions that grant access merely to improve a screenshot.

Use the current-source Breathing Room Space illustration later to explain broader inspection as a bounded alternative, with “Breathing Room, which we build.” Do not manufacture a hands-on result. The interaction pass should produce a static decision aid: scanned or skipped → unknown size if skipped → inspect accessible contents → assess backup/rebuildability → leave unverified data untouched. No runnable demo repository or filesystem action is justified here.

Link contextually to `/comparisons/`, the proposed `/comparisons/clean-me/`, and only an actually verified cache/rebuild-checklist route. Route existence remains drafting QA, not an assertion that a tool already exists.

## Concise comparison brief

**Title:** Breathing Room vs Clean Me: scope and preview limits  
**Proposed comparison slug:** `clean-me`.

Answer product choice, not the same troubleshooting question again. Use a compact matrix: maintenance/platform/version, licence and conditional price, category analysis versus exploration, selection/approval and permission limits, documented local behavior versus optional hosted AI, developer path scope, and unknown Clean Me monitoring/process-grouping cells. Use the same two credited views with all caveats. Link to the deeper workflow; do not create a duplicate alternatives doorway.

Clean Me's supported advantages are MIT source, explicit folder/category inspection, and the author's useful restraint around cache removal. Its limits are archived maintenance, narrow documented compatibility and unverified modern runtime. Category selection can include valuable Downloads or attachments; size is not permission to delete them.

Breathing Room's source-implemented storage exploration, process/helper grouping and constrained approval records may better fit recurring investigation. Do not convert source presence into installer QA. Carry today's capability register conditions: **0.1.0-preview.1; macOS 13+; advertised universal installer with physical Intel/clean-machine validation incomplete; Apple Development signed, not Developer ID signed or notarized; Python 3.10+ for inventory/legacy scripts, not bundled**. Local tools are free; authenticated hosted AI uses relevant inspection data, and AI Care is advertised at **$5 USD/month or $50 USD/year**, renewing until cancelled with applicable tax at checkout. Exact quota and paid enforcement are unverified. Website download registration differs from public GitHub releases. Daily care requires the app running; optional verified Ruff automatic mode qualifies blanket approval language.

A reader unwilling to use either an archived tool or a non-notarized preview may prefer independently validated supported software or built-in inspection. No unsupported “best,” “safer,” speedup or recovered-space claim belongs in either brief.

## Handoff gates

- No critical evidence gap blocks these **bounded** briefs. Unknown modern compatibility, signature status, network behavior, screenshot capture version and binary feature parity are explicitly constrained, not filled in.
- Modern compatibility/installation claims, successful Homebrew commands, screenshot-based Archives behavior and measured-savings claims are blocked until specific new evidence exists.
- No draft exists and no independent score is awarded. Independent claim, licence-context and visual review, exact draft/derivative hashes, real internal links, site check/build/tests and responsive/theme inspection remain publication gates for the later jobs.
- No browser session was needed: relevant browser skill loaded, public HTTP/source reads and existing authorised local images sufficed. No Chrome recovery, cookie extraction or existing tab access occurred.
- Only this owned folder and the required receipt were written. No queue, shared register, website, unrelated product, commit, push or deployment changes.
