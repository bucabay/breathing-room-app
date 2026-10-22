# Intego Washing Machine X9: research handoff

**Research blocked for drafting.** Sources checked October 21, 2026; this packet is not an article, a hands-on test or publication approval. `research.json` contains the claim ledger, exact URLs, excerpts, scope, timestamps, hashes and briefs. Work resumed after transport interruptions without refreshing the evidence date.

## Identity and fit

Canonical owner: **`intego-washing-machine`**. Official documentation names **Washing Machine X9**; the listing calls it Intego Mac Washing Machine / Mac Washing Machine. Its old homepage, `http://www.intego.com/mac-cleaner`, redirects to [SmartClean](https://www.intego.com/features/smartclean). That same-day redirect observation and listing snapshot were **reused from batch-1**, not fetched again.

Do **not** merge this identity into SmartClean solely from the redirect. The [official X9 manual](https://integosupport.zendesk.com/hc/en-us/articles/40945613333275-Washing-Machine-X9-User-Manual) still documents Washing Machine, and [current migration guidance](https://integosupport.zendesk.com/hc/en-us/articles/56127413762715-The-Get-Intego-ONE-Tile-Is-Missing-or-Won-t-Open-in-Your-Intego-X9-My-Account) separately lists standalone Washing Machine as ineligible for self-service migration to ONE. A new ONE subscription is required for that move. Mac Premium Bundle X9 has different eligibility; do not generalize.

**Alias skip decision:** retain the X9 identity; skip creating any additional SmartClean doorway draft from this job. Historical feature parity is not established. No official repository was established. No connection to PowerMyMac was established or presumed. This is not a verified dead-product exclusion: current documentation and release notes exist, although standalone new-purchase terms remain unknown.

Fit is direct overlap for **Mac storage cleanup**, adjacent for duplicate selection and Desktop/Dock organization. No Windows support is inferred from Intego's separate Windows antivirus navigation. Breathing Room is not established as a duplicate finder or Dock organizer.

## Verified facts and boundaries

All entries below are vendor documentation, not observed execution. Claim IDs map to source URLs and supporting passages in `research.json`.

| Dimension | Finding | Claim |
| --- | --- | --- |
| Version | Latest inspected [release-ledger](https://integosupport.zendesk.com/hc/en-us/articles/40945609280411-Washing-Machine-X9-Release-Notes) entry: **10.9.28**, March 24, 2026; vendor states Tahoe compatibility. No binary inspected. | `version` |
| Platform | Manual: macOS **10.13+**, 64-bit Mac processor, **1.5 GB** free disk. Not an architecture-specific runtime test. | `platform` |
| Reclaim | Caches, Downloads, Languages, Logs, Trash; Safe/Aggressive criteria, graph/list inspection, then Clean. Manual warns cleaned files cannot be recovered. The label “Safe” is not our guarantee. | `reclaim` |
| Duplicates | Actual-data comparison, scan locations, rules for which copies to keep, Finder reveal and Quick Look; separate preference can move duplicates to Trash. Do not apply that preference to all Reclaim deletion. | `duplicates` |
| Organization | Desktop, Dock and Smart Folders are separately documented jobs, not evidence of app uninstallation or measured storage recovery. | `organize` |
| Recurrence | Scan reminders default to every two weeks; monthly/three-monthly choices. Continuous growth monitoring and automatic cleanup are **not verified**, not “No.” | `reminders` |
| Trial/activation | Manual describes name/company and serial registration; **30-day trial excludes Clean and Tidy**. | `trial` |
| Updates | NetUpdate installed alongside the app. Signing/notarization, full permissions and runtime dependencies not verified. | `updates` |
| Data flows | Native-app documentation does not prove entirely offline operation. Manual exposes an anonymous usage-data Feedback toggle; no backend audit. | matrix |
| Developer caches/helper grouping | Not verified. Generic caches do not establish owning-tool adapters. | matrix |

### Pricing must not cross product generations

Current standalone **Washing Machine X9 price, licence duration, device count and new-sale availability are not verified** (`legacy-price`). AlternativeTo's perpetual $70–$90 range is not official current pricing and must not enter the comparison as fact.

The [current public buy page](https://www.intego.com/buynow), read in Chrome, instead displays **Intego ONE Advanced with SmartClean**: $90.99 for the first two years, automatically renewing at $129.99 every two years, with 1 Mac displayed. The $3.79/month figure is an equivalent display, **not monthly billing**. ISO currency, tax, geography and checkout totals were not independently established. This is separate context, never the X9 price (`one-offer`). No purchase or selector interaction occurred.

## Breathing Room evidence reused

Same-day `docs/content/capabilities.md` and `screenshots.json` were read, not re-researched needlessly. Preserve their original evidence classes and caveats:

- `0.1.0-preview.1`, macOS 13+, advertised universal installer; physical Intel and clean-machine runtime validation incomplete. Published disclosure: Apple Development signed, not Developer ID signed or notarized. Python 3.10+ prerequisite. [Release](https://github.com/bucabay/breathing-room-app/releases/tag/v0.1.0-preview.1).
- Source implements storage exploration, grouped CPU/memory sampling, activity observations and developer-cache discovery. Source presence is not binary parity or hands-on validation. Inferred ownership/sampled I/O is not forensic proof.
- Default reviewable cleanup, optional automatic verified Ruff-cache Trash mode, and exact saved approvals for daily care must not be flattened into “always asks before every deletion.” Daily care requires the app to remain running.
- Free local core; [advertised AI Care](https://breathing-room.chatic.ai/#pricing) $5 USD/month or $50 USD/year, renewal/tax conditions. Hosted assistance needs authentication/internet and can send relevant paths/process/storage data; [privacy policy](https://breathing-room.chatic.ai/privacy/). No unlimited allowance or successful checkout established. Website download registration differs from public GitHub release access.

These are packet-supported statements, not permission to claim faster, safer, risk-free, production-ready or measured space savings.

## Visual handoff: image gate blocked

### Competitor app UI — link only

- Source: [Washing Machine X9 manual](https://integosupport.zendesk.com/hc/en-us/articles/40945613333275-Washing-Machine-X9-User-Manual), Reclaim section.
- Public asset: https://integosupport.zendesk.com/hc/article_attachments/56239213980571 . Rendered page reports 2048 × 1343; observed October 21 at 20:44:31.618 UTC. Capture date, app build and photographer unknown.
- Caption: “Intego's Washing Machine X9 Reclaim illustration in its official manual; vendor-provided example, not our scan or measured savings.”
- Alt: “Official Washing Machine X9 Reclaim screen illustrating cleanup category selection.”
- **Reuse basis unresolved.** Official placement establishes provenance, not republication permission; manual footer says all rights reserved. No download, transformation, copied image hash or invented licence. `originalSha256` remains null because no original image file was downloaded. The official link is a research fallback, not satisfaction of the on-page image gate. Privacy and independent visual review pending.

### Selected Breathing Room preview

Use `docs/content/assets/breathing-room/space-preview-2026-10-21.png`, inventory ID `current-space-browser-preview`. Original SHA-256: `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a`; 2940 × 3468. Captured October 21 at 19:06:45.416416 UTC from source commit `54828ac3170b45861aee70861dd0b9c658ed7e51`, not a native build test.

**Required caption:** “Current-source Breathing Room Space browser preview, captured October 21, 2026. Example data only; not a native scan, measured activity or cleanup result.”

Alt: “Breathing Room Space browser preview with example-data banner, storage categories and illustrative file sizes.” App-owner-requested first-party capture, with third-party marks remaining their owners' marks. Opened and visually read the actual PNG; example-data banner is visible, and floating composer overlaps part of the category display. Keep disclosure visible, do not treat numbers as measurements, and require contextual mobile/theme legibility review. No new capture or asset edits performed.

## Distinct workflow article brief

**Proposed title:** Review duplicate copies before reclaiming space on a Mac  
**Proposed slug:** `review-duplicate-copies-before-reclaiming-mac-space`  
**Track:** search/reference. Primary job is deciding which copy to keep and separating that decision from cache cleanup and organization, not expanding a product matrix into filler.

Conclusion-first lead should distinguish content duplicates, rebuildable caches and organization. Then show a rights-cleared real app visual before long prose. Sections: choose the cleanup job; inspect duplicate locations and previews; verify deletion/Trash method; keep organization separate; investigate recurring growth when one-off cleanup does not explain the problem. Cite the manual next to each described step. Explain backups and rebuild/download costs without claiming a tested procedure.

**Interaction-pass handoff:** a non-destructive decision checklist: backup exists; original/copy locations understood; preview reviewed; method and recoverability understood; rebuild/download cost accepted. No filesystem controls, code demo or fabricated outcome. Include a later disclosed Space preview. No artificial FAQ, signup CTA or companion repo.

## Concise comparison brief

**Title:** Breathing Room vs Intego Washing Machine X9  
**Proposed comparison slug:** `intego-washing-machine`  
**Intent:** choose a documented duplicate/organization workflow versus a preview storage/process investigation workflow. Explain the SmartClean redirect immediately; do not write the page as if X9 and ONE are the same edition.

Use six compact rows: identity/version; platform/prerequisites; cleanup/approval; duplicates and organization; monitoring/recurrence with explicit unknowns; price/access with generation-specific caveats. Link to `/comparisons/` and the proposed deeper workflow article only when those routes are available; they were not verified live here. Disclose “Breathing Room, which we build” at any recommendation. Keep unpublished.

**Truthful strengths:** Washing Machine's documented actual-data duplicate comparisons, selection rules and organization cycles suit those jobs. Breathing Room's source-backed storage/process investigation and developer-cache methods may suit unexplained growth; that is editorial fit, not measured superiority.

**Trade-offs:** X9's Reclaim deletion warning and trial restrictions matter; current standalone purchase terms are unknown. Breathing Room's preview, signing, Python, hosted-data and untested runtime caveats matter. Neither product should be assigned undocumented missing features or guaranteed outcomes.

## Precise blockers and next action

1. **Competitor image rights:** retain link-only evidence until authorized licence/permission or an explicitly approved visual-policy decision. Do not contact anyone from this scheduled job. Required on-page image gate remains blocked.
2. **Legacy offer:** obtain a current public official standalone X9 offer with price/licence/device/availability conditions, or explicitly approve an existing-owner-only comparison that says those values remain unverified. ONE bundle prices cannot fill this gap.

Noncritical unknowns include official repository, screenshot capture/build, offline/data-flow details, architecture execution, helper grouping, developer adapters and exact original discovery pagination edge. Unknowns must remain visible. No independent review, rendered draft checks or score was awarded.

## Actual research checks

Read PLAN, EDITORIAL, capabilities and screenshot inventory; no applicable AGENTS.md found in app tree or checked ancestors. Reused batch-1 discovery/redirect evidence and verified retained-source hashes. Public manual and migration page fetched successfully. WebFetch pricing, release notes and Organize returned 403; pricing/release notes were subsequently read normally in owned Chrome tab **112**. No challenge bypass or cookie extraction. Only owned tab was inspected/navigated and closed; no browser recovery needed. Search snippets were leads, not release/version proof.

Four browser source extracts retained in `sources/`, with timestamps and hashes in JSON. No third-party image downloaded. Actual first-party PNG visually inspected and hash checked. Final structural/evidence validation is recorded in `validation.json` and the task receipt. No site changed, so site build/tests and draft browser QA are not claimed or run. No cleanup, accounts, purchases, messages, credentials, queue/database edits, other jobs, agents, commits, pushes or deployment.
