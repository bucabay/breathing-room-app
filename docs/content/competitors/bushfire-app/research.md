# Bushfire research handoff

Checked **2026-10-21** · `research-bushfire-app` · **Blocked for drafting**. No site content or assets were changed. This is evidence and a conditional brief, not a review or hands-on test.

## Decision and identity

Bushfire is an **adjacent Mac Safari privacy utility**, not a verified direct substitute for Breathing Room's storage and app/process investigation. Its official homepage is <https://bushfire-app.de/en/> and its reciprocal official repository is <https://github.com/ghostjuza/open-bushfire>. The repository's “Open Bushfire” community/name refers to this same product. `canonicalOwnerId: bushfire-app`; skip any separate Open Bushfire/open-bushfire draft. Do not skip this canonical record as an alias or declare the product dead merely because its latest GitHub release is old. No evidence connects it to PowerMyMac.

The current batch-1 verification record was reused **before** new retrievals. Batch-2 contains no Bushfire match. Homepage/directory facts were not needlessly fetched again. Exact source URLs, excerpts, dates, scopes, original snapshot paths/hashes and claim IDs are in `research.json`. Newly fetched pages have retained selected excerpts there, not invented raw snapshot hashes or exact retrieval timestamps.

## Material evidence

| Topic | Supported statement and limits |
| --- | --- |
| Function | Official README documents Safari cleanup when Safari quits, immediate menu-bar cleanup, category selection and pause. C4–C5; [README](https://github.com/ghostjuza/open-bushfire#readme). These are documented behaviors, not our tests. |
| Data categories | Includes cookies, cache, history and **downloads list**, among other categories. Downloads-list deletion must not become a claim that downloaded files are deleted. C5. |
| Price and licence | Current homepage says free including updates, no account/registration; donations confer no service contract. GPLv3; README says version 3 or later. C2–C3; [homepage](https://bushfire-app.de/en/), [licence](https://bushfire-app.de/en/license/). No paid plan or invented billing conditions. |
| Version | [GitHub latest-release API](https://api.github.com/repos/ghostjuza/open-bushfire/releases/latest) returned [`build-2022.235`](https://github.com/ghostjuza/open-bushfire/releases/tag/build-2022.235), published **2022-10-02T11:55:31Z**, with `Bushfire.dmg`. C7. Not proof of website-download equivalence, internal semantic version or binary compatibility. No installer downloaded. |
| Platform conflict | Homepage says **macOS 10.11+**; README Status says **10.11 to 12.x**; [support](https://bushfire-app.de/en/support/) discusses **macOS 15 Sequoia & newer**. C6. Modern macOS/Safari support and Intel/Apple Silicon architecture are not established. Never imply Windows support. |
| Access and sync | Vendor support says Library-folder access must be authorized and iCloud Safari sync can restore deleted data. C8. No settings changed; do not repeat advice about disabling protections or present vendor troubleshooting as a verified fix. |
| Local versus network | Local Safari cleanup is documented, but homepage discloses transmission of two counts (deleted objects and bytes) while elsewhere saying “no transfer of your data.” C9. Do not claim zero network/telemetry, guaranteed anonymity or audited privacy. |
| Deletion guarantees | Optional overwriting is documented, not proof of secure erasure on SSDs, complete deletion, recoverability or safety. No cleanup/savings/performance test performed. |
| Broader tools | Helper grouping, developer-cache adapters and recurring-growth monitoring for Bushfire: **not verified**, not “No.” |

## Two precise drafting blockers

1. **Compatibility:** obtain version-specific official release/maintainer evidence resolving the 10.11+/10.11–12.x/15+ mismatch before recommending current installation or replacement. Do not fill the conflict with guesswork or an old binary's age.
2. **Competitor image:** the official README links a real app-panel image, but image-specific reuse scope/compliance and actual pixel/privacy review remain pending. The link-only fallback is evidence, **not** a pass of the required on-page image gate. Resolve documented rights/compliance or get an explicitly authorized permission/policy decision before downloading/publishing it. No permission request was sent.

Network ambiguity restricts claims: omit blanket no-transfer/anonymity statements unless separately resolved. Noncritical unknowns such as helper grouping need not be researched into unsupported negative claims.

## Visual handoff

### Bushfire: link-only, not approved for republication

- Source: <https://github.com/ghostjuza/open-bushfire#readme>.
- Exact published image link: <https://github.com/ghostjuza/open-bushfire/raw/master/img/bushfire-panel.png>.
- Raw asset URL: <https://raw.githubusercontent.com/ghostjuza/open-bushfire/master/img/bushfire-panel.png>.
- Basis: official project supplies the panel screenshot. The software GPL alone has not been independently cleared as the complete image-reuse/compliance basis. Public access is not a licence.
- No image file was downloaded or published; original/published hashes, capture date, app version, dimensions and data origin remain null, rather than invented. A contents-API request returned an oversized response but was not used as a local image or clearance evidence.
- Proposed credit: Open Bushfire Community, official repository. Proposed caption: “Official Bushfire panel image linked by the project README. Capture date, app version and displayed-data origin are not verified; not our hands-on test.” Final alt text requires actual image inspection, not guessed controls.

### Breathing Room: selected current-source browser preview

Use `docs/content/assets/breathing-room/space-preview-2026-10-21.png`, from the current screenshot inventory. Original SHA-256 verified in this job:

`9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a`

2940 × 3468; captured 2026-10-21T19:06:45.416416+00:00 from source commit `54828ac3170b45861aee70861dd0b9c658ed7e51`. Opened and read the actual PNG: example-data warnings are visible; Space categories and storage figures are illustrative; floating assistant overlaps part of the view. No edit/crop or copy was made. Preserve banners in any later approved derivative and record original/published hashes.

**Required caption:** “Current-source Breathing Room Space browser preview, captured October 21, 2026. Example data only; not a native scan, measured activity or cleanup result.”

**Alt:** “Breathing Room Space browser preview showing illustrative storage categories with visible example-data warnings.” First-party owner-requested UI capture basis is recorded in `screenshots.json`; third-party marks and publication-context review remain bounded. It is not a native or distributed-release test.

## Conditional workflow brief

**Track:** search/reference. **Provisional slug:** `bushfire-app-mac-workflow`. **Title:** “Safari data on quit: what to check before using Bushfire”.

**Reader job:** distinguish Safari-session traces from a whole-Mac storage problem, then make a deliberate category/compatibility decision. This earns a different article from the concise product matrix, rather than expanding it into filler.

Lead with the two different jobs. Put the licensed, visually inspected official Bushfire panel immediately after the lead once cleared. Explain the documented on-quit/manual controls and category choices; distinguish downloads list from files. Resolve compatibility before any installation recommendation. Explain vendor iCloud/access caveats without changing settings or weakening protections. Later show the labeled Breathing Room Space view for the different storage-investigation task. No fabricated FAQ, benchmark, anonymity or secure-erasure promise.

**Interaction pass:** a non-executing decision checklist: Safari traces or general storage growth? Exact OS/Safari/version supported? Category loss understood? Sync caveat understood? It must not scan, delete, modify settings or infer compatibility. No arbitrary code/demo repo is needed.

## Conditional concise comparison brief

**Provisional path:** `/comparisons/bushfire-app/`. **Title:** “Bushfire vs Breathing Room: Safari cleanup or storage investigation?”

Disclose “Breathing Room, which we build,” at the bounded recommendation. Start with adjacent-tool fit, then a short claim-linked matrix covering platform/version, price/licence, local/hosted boundary, triggers/approval and caveats. Show both real product views only after clearance. Link to the deeper workflow rather than duplicate its prose. `/comparisons/` is the intended hub; counterpart routes are future handoffs, not claimed existing links. Verify all actual internal routes at drafting time.

**Bushfire advantages:** free, documented no-account Safari-on-quit/manual cleanup, category choices and pause, inspectable GPL source. **Trade-offs:** unresolved modern compatibility, access/sync caveats, no independently established zero-network/secure-erasure guarantee; broad Mac investigation features unknown.

**Breathing Room advantages:** source-level broader storage views and grouped app/process investigation for another job; free local core with optional AI Care. **Trade-offs:** current identified `0.1.0-preview.1`, macOS 13+, Python 3.10+ inventory prerequisite, Apple Development signed but not Developer ID signed/notarized, no clean-machine/physical-Intel validation. Hosted AI needs authentication/internet and may receive relevant paths/process/storage information. AI Care is advertised at $5 USD/month or $50 USD/year, renewing with applicable checkout tax; allowances/enforcement remain unverified. Daily care needs the app running and exact saved approvals; optional narrow automatic Ruff mode prevents blanket “always asks for every action” claims. These same-day facts reuse `capabilities.md`, not new runtime tests. Safari-on-quit parity is not established.

## Validation boundary

Research-only work: no app execution, installation, cleanup, account creation, credential read, settings changes, browser session, marketing edits, queue/database changes, commit, push or deployment. No subagents. `AGENTS.md` search found none in the app tree or checked ancestors. Blog/browser skills and the adapted editorial contract were read. JSON/path/hash/source-reference checks are recorded in the receipt; no site build is claimed or required for these research-only changes. Independent editorial, rights and rendered-page approval remain pending.
