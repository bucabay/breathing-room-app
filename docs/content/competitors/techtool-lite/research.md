# Techtool Lite research — blocked for drafting

Task: `research-techtool-lite`. Local editorial date: October 22, 2026; actual final UTC check: October 21, 2026, 22:14. Research only, not publication approval or hands-on testing.

## Decision

**Retain Techtool Lite as a distinct, adjacent Mac utility. Do not draft yet.** Its documented diagnostics answer a different question from storage accounting. `canonicalOwnerId: techtool-lite`; no alias skip. The official page explicitly distinguishes Lite from Techtool Pro (`techtool`), so this job does not own or duplicate Pro's repair-oriented content. No PowerMyMac relationship was established.

Two material gates remain:

1. **Competitor image rights:** a genuine vendor app UI image was found and visually inspected, but no republication permission was established. Keep it link-only; that does not pass the required on-page image gate. No competitor image was downloaded.
2. **Compatibility conflict:** the product page lists macOS 13.5–26; the official 21.1.1 release announcement says it adds macOS 27 compatibility. Do not silently broaden the supported range or certify either assertion as tested. Resolve the version-specific claim, or obtain independent approval for an attributed conflict disclosure without an OS recommendation.

## Reused verification and discovery

Read `docs/content/verification/batch-2.json` first and reused the current product identity, free offer, platform baseline and Lite/Pro distinction. The alias decision is also recorded in `verification/alias-decisions.json`. Actual retained official and directory file hashes match the baseline record. The raw official capture's embedded hash is not the file hash; the packet explicitly records the actual file digest.

Discovery: [Mole seed](https://alternativeto.net/software/mole/) → [page 3](https://alternativeto.net/software/mole/?p=3), inherited edge retrieval `2026-10-21T18:37:11.107Z` → [Techtool Lite about page](https://alternativeto.net/software/techtool-lite/about/) → [Micromat product page](https://www.micromat.com/products/techtool-lite/). The retained about-page capture is `docs/content/.runtime/verification-2/techtool-lite-directory.json`, checked `2026-10-21T19:06:21.517Z`, SHA-256 `d82cb9bc8965d4d419625f637433544f24f05bb39c78cc046c6bf594b19dfe90`. The original paginated edge raw capture was not separately located; its provenance is inherited from `competitors.json`, not invented.

## Facts available for a future draft

Full claim-level excerpts, dates, URLs and conditions are in `research.json`. “Documented” below means vendor documentation, not successful execution.

| Claim | Exact evidence / scope |
| --- | --- |
| Identity and adjacent fit, C1 | [Micromat](https://www.micromat.com/products/techtool-lite/): “Techtool Lite focuses on essential testing and maintenance. For volume repair, deeper diagnostics, external drive testing, and advanced tools, Techtool Pro gives you complete control.” Baseline checked October 21 at 19:09 UTC. |
| Free offer, C2 | Same official page: “Techtool Lite, the free new utility from Micromat”. No Lite paid tier, expiry, seat allowance or commercial-use licence established. Free is not open source. |
| Platform baseline, C3 | Same page: “Apple Silicon and Intel-based Macs”; “macOS 13.5 ‘Ventura’ through macOS 26 ‘Tahoe’”. Do not present this as a definitive latest-version upper bound. |
| Internal-drive diagnostics, C4 | Same page: “including SMART health, partition map, and volume structures.” Testing is not proof of volume repair or complete drive coverage. |
| Maintenance, C5 | Same page: “reset system caches and rebuild important macOS databases”. No exact database list, approvals, developer-cache adapter support or performance result verified. |
| Other diagnostics, C6 | Same page documents memory and battery checks and viewing local-network devices/ports. Network monitoring is not evidence of app/helper CPU grouping or folder-growth attribution. |
| Current identified version and conflict, C7 | [Updates](https://www.micromat.com/support/updates/) links [21.1.1 announcement](https://www.micromat.com/techtool-lite-21-1-1-released/): “Version 21.1.1”, “Release Date: 10/9/2026”, “Added compatibility with macOS 27 ‘Golden Gate’”. Checked this run. Vendor-listed 19.0 MB is not a measured download size. |
| Licence limits | [General terms](https://www.micromat.com/terms-of-service/): the applicable licence accompanies installation and must be read. This is not the specific Lite EULA or an image licence. Official source repository not verified. |

The public product page exposes a DMG link ending `techtool_lite_21/ttl_2111_2808.dmg`; this is a link observation only. No binary download, install, activation, signature check or feature test was performed. Signing/notarization, permissions, helper installation, offline behavior, telemetry and detailed approval controls remain unknown, not negative claims.

## Selected visuals

### Competitor — official UI, link-only

- Source: https://www.micromat.com/products/techtool-lite/
- Asset: https://www.micromat.com/wp-content/uploads/2026/04/Techtool-Lite-Promo-2048x1418.png
- Alternate lazy-loaded asset: https://www.micromat.com/wp-content/uploads/2026/04/Techtool-Lite-Promo-1024x709.png
- URL inspected at `2026-10-21T22:14:05.439Z` in owned Chrome tab 172. Hero visually shows a genuine Tests sidebar and Mac hardware overview. It appears to show version 21.0.9 (2539), not current 21.1.1; confirm original before publication. Original capture date/OS unknown.
- **Caption:** Micromat's official Techtool Lite interface illustration; vendor example, not our hands-on test or the latest-version UI verification.
- **Alt:** Techtool Lite Tests overview showing a diagnostic sidebar and Mac hardware summary.
- Credit Micromat. All-rights-reserved footer and checked general terms do not establish republication rights. No permission request sent. No asset saved, edited or rehosted; original/published hashes intentionally null.
- The page's `cache-rebuild.png` and other feature thumbnails are icons, not acceptable competitor UI screenshots. Browser page captures were used only to inspect the source, not offered as replacement product imagery.

### Breathing Room — selected existing Space preview

- File: `docs/content/assets/breathing-room/space-preview-2026-10-21.png`, 2940 × 3468.
- SHA-256 rechecked: `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a`.
- Source render: `54828ac3170b45861aee70861dd0b9c658ed7e51`; captured `2026-10-21T19:06:45.416416+00:00` per `screenshots.json`. Opened and visually read again in this job.
- **Required caption:** Current-source Breathing Room Space browser preview, captured October 21, 2026. Example data only; not a native scan, measured activity or cleanup result.
- **Alt:** Breathing Room Space view rendered in a browser with illustrative example data.
- First-party app-owner-requested capture; keep both the example-data label and no-change warning. Do not infer blanket trademark rights. The floating assistant overlaps chart labels; future layout must preserve readable context. No copy or crop created here.
- This illustrates the recorded current-source preview, not the distributed native release or measured storage savings. Independent target-page visual review remains required.

## Distinct workflow brief

**Title:** Mac diagnostics or storage investigation? Choose the next check before resetting caches  
**Proposed slug:** `mac-diagnostics-before-cache-reset`  
**Primary intent:** Route a maintenance question to a useful investigation before applying a cache reset. This is a decision workflow, not a Pro repair guide or a database-reset tutorial.

Conclusion first: diagnostics and storage accounting answer different questions. State the symptom and backup boundary; distinguish internal-drive/memory/battery questions from database/service trouble and recurring storage growth. Explain the documented Lite diagnostic path without running it. Then explain the storage/activity investigation branch with bounded Breathing Room evidence. Avoid implying a cache reset fixes unexplained slowness or hardware failure.

Useful interaction: a non-destructive three-branch checklist (hardware health, database/service malfunction, storage growth). It chooses an investigation category, not a diagnosis or deletion command. No forced code demo. Place licensed competitor UI after the lead and the explicitly labeled Space preview later. Keep draft blocked until visual gate resolution.

## Concise comparison brief

**Title:** Breathing Room vs Techtool Lite: storage investigation or Mac diagnostics  
**Proposed comparison:** `/comparisons/techtool-lite/`

Lead: Techtool Lite documents essential diagnostics and system maintenance; Breathing Room, which we build, focuses on storage and activity investigation in a preview. Neither documented role establishes replacement coverage for the other.

Use a short sourced matrix: primary task, diagnostic versus storage views, cache scope, platform/version conflict, approvals/data-boundary unknowns, pricing and install caveats. Cross-link `/comparisons/` and the distinct workflow. Proposed links are not verified published routes; select a real relevant `/tools/` route later rather than fabricating one.

**Lite advantages:** documented internal-drive, memory and battery diagnostic scope; advertised free. **Boundaries:** Lite is explicitly distinguished from advanced Pro repair/external-drive tools; precise EULA, approvals and data behavior remain unknown.

**Breathing Room advantages for the storage branch:** source-supported owner/category views and grouped CPU/memory; reviewable maintenance architecture. **Trade-offs:** identified `0.1.0-preview.1`, macOS 13+, Python 3.10+ inventory prerequisite, Apple Development signed but not Developer ID signed/notarized, unvalidated clean-machine/physical Intel behavior. Free local core differs from optional authenticated hosted AI Care at $5 USD/month or $50 USD/year, renewing until cancelled with applicable tax. Relevant request/history/tool outputs can leave the Mac. Daily care requires the app running and saved approvals; optional verified Ruff automatic mode means no unconditional “never deletes without asking” promise. Reused `capabilities.md` evidence is source/published documentation, not binary parity certification.

Unknown competitor cells must remain “not verified,” including helper grouping, recurring folder growth and specific developer caches. No winner for speed, safety, savings or offline privacy. No Windows support or hardware repair capability invented for Breathing Room.

## Execution and handoff

Read PLAN, EDITORIAL, capabilities and screenshots; no applicable AGENTS.md found in checked ancestors/root/docs subtree. Loaded blog-factcheck and browser-automation. Preserved unrelated work and wrote only this product directory plus required receipt.

Python urllib returned HTTP 403 on the product page. Webfetch and the normal public Chrome page worked; no credentials/cookies extracted or access controls bypassed. New-tab navigation timed out but tab 172 existed and loaded; only this owned tab was inspected/scrolled and closed. No profile recovery, native tests, cleanup, signups, purchases, messages, agents, commits, pushes, deployments, website or queue changes.

`validation.json` records actual structural/evidence/hash checks. No site build was run because no site files changed. Drafting and independent review remain blocked; this packet does not award an editorial score or publish anything.
