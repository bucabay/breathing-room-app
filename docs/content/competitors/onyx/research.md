# OnyX research — blocked, not draft-ready

Task `research-onyx`. Research clock reading: **2026-10-21T21:53:15Z** (session calendar says October 22; actual clock retained). Owned outputs are this folder and the required attempt receipt only. No site content, queue or shared verification records changed.

## Decision

**Hold drafting.** The reused `verification/batch-2.json` OnyX record contains zero verified official product facts. The directory identifies an official destination, but direct retrieval still fails. Search-index text is useful for follow-up, not sufficient to verify versions, platforms, licensing, pricing or capabilities. Network failure does not establish that OnyX is dead.

`canonicalOwnerId: onyx` preserves the queue's stable identity provisionally. No alias has been verified, no separate alias draft is authorized, and no alias skip is justified. In particular, PowerMyMac is not established as an OnyX alias. Do not consolidate unrelated products based on names. Classification is **adjacent-provisional**: discovery suggests Mac maintenance/cache work with parameter controls, not proof of a complete substitute for Breathing Room's documented investigation workflow. No Windows support is asserted.

## Reused provenance and new checks

- Discovery: [OnyX about page](https://alternativeto.net/software/onyx/about/), previously read at `2026-10-21T19:05:08.963Z`. Exact excerpt: “Official Website\ntitanium-software.fr/en/onyx.html”. Raw record: `docs/content/.runtime/verification-2/onyx-directory.json`; SHA-256 `408ae76b2dd2b1ebe5afb35a497ece1b0f7ba06dbe14bf485eb6285fa8b7717c`.
- Reused traversal edge: [Mole page 2](https://alternativeto.net/software/mole/?p=2), recorded `2026-10-21T18:37:09.298Z`, from `competitors.json`. No unnecessary directory refetch.
- [Candidate official OnyX page](https://www.titanium-software.fr/en/onyx.html): WebFetch timed out with 45-second cap. Existing browser connection worked; owned tab **149**, created at `about:blank`, returned `net::ERR_TIMED_OUT` with a 40-second navigation cap. Accessibility snapshot read “This site can’t be reached”, “took too long to respond”, `ERR_TIMED_OUT`; final URL `chrome-error://chromewebdata/`. No successful source excerpt exists.
- Non-www `/en/onyx.html` and indexed extensionless `/en/onyx` also timed out with 35-/30-second caps. These were missing-evidence checks, not refreshed verified facts.
- [Official screenshot-page lead](https://www.titanium-software.fr/en/onyx_captures.html): search index identifies “OnyX Screenshots”, but direct WebFetch timed out with a 30-second cap. No individual image was obtained or inspected.
- Search query `site.titanium-software.fr/en/onyx.html OnyX version screenshot freeware` returned indexed feature/OS-specific version/free-use claims, and an official homepage/release-notes lead. These remain **unverified leads**. In particular, indexed version strings, macOS naming and signing/AI assertions must not silently become product facts. Packaging metadata is not the product's source repository.

`research.json` contains the claim-level ledger, exact source URLs/excerpts, evidence classes, unknown cells, conditional briefs and blocker resolutions. No installer, app or cleanup workflow was executed. No savings or performance results exist.

## What must be verified before drafting

1. Retrieve the official product page successfully, retaining text and a hash. Confirm official name/publisher, current homepage, any official repository and alias/component relationships. Distinguish unverified repo from no repository.
2. Record the exact OnyX release **for each claimed macOS version and processor**. Do not publish a single “macOS X+” compatibility rule from directory text. Indexed claims suggest per-major-version builds, but direct confirmation is still needed.
3. Verify current price/free-use terms, licence, donation conditions, installation/permissions/signing/runtime requirements, core maintenance scope and approvals. Unknown monitoring, developer cache and hosted-service fields remain **not verified**, never negative checkmarks.
4. Obtain an actual competitor app screenshot and permission basis. Source-page discovery does not meet the image gate.

No permission request, signup or purchase may be sent by this scheduled job. A future authorized rights decision is required if the public page does not provide usable terms.

## Visual handoff

### OnyX — blocked / link-only

Link to [the candidate official screenshot gallery](https://www.titanium-software.fr/en/onyx_captures.html). Actual app view, asset URL, image version, capture date, reuse licence, dimensions and original hash are unknown. No image downloaded; public visibility is not permission. No fabricated alt text or screenshot substituted. This is an acceptable research lead, **not an on-page visual-gate pass**.

### Breathing Room — selected existing current-source preview

Selected `current-space-browser-preview` from `screenshots.json`:

- File: `docs/content/assets/breathing-room/space-preview-2026-10-21.png` (shared existing asset; not copied or edited).
- SHA-256: `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a`; 2940 × 3468.
- Existing capture: `2026-10-21T19:06:45.416416+00:00`, source commit `54828ac3170b45861aee70861dd0b9c658ed7e51`, browser preview `http://127.0.0.1:1431/`.
- Caption: **Current-source Breathing Room Space browser preview, captured October 21, 2026. Example data only; not a native scan, measured activity or cleanup result.**
- Alt: “Breathing Room Space browser preview with example storage categories and a visible example-data banner.”
- Reuse basis: owner-requested first-party capture per inventory; no blanket third-party trademark licence inferred.
- Actual PNG opened in this job: example-data banners, categories and overlapping composer inspected. Keep disclosure visible. It is a source UI illustration, not distributed-installer or native testing. Any later crop must retain disclosure and get new edit/hash and responsive review.

## Conditional workflow brief — not article copy

**Title:** Before running Mac maintenance: match the utility to your macOS version  
**Proposed slug:** `match-onyx-version-before-mac-maintenance`  
**Track:** search/reference. **Intent:** select an OS-matched maintenance tool rather than run indiscriminate cleanup when storage grows.

Explain the version/processor check, how to read a verified official version table, the distinction between a targeted repair/parameter change and investigating storage growth, and why cache size is not permission to delete. Do not publish steps, menu labels or controls without version-specific evidence. No cleanup commands, fake hands-on narrative or guaranteed results.

Interaction handoff: a read-only checklist asking OS version, processor, intended task and confirmed official compatibility match. It should help readers stop when evidence is missing; no repair buttons. Place selected Breathing Room preview after the lead, and a rights-cleared OnyX app UI near the maintenance discussion when available. Link to `/comparisons/` and proposed `/comparisons/onyx/` only after those routes are confirmed by the draft owner. This article's distinct value is compatibility triage, not expanding a feature matrix into filler.

## Conditional concise comparison brief

**Title:** Breathing Room vs OnyX: storage investigation or targeted maintenance?  
**Proposed comparison slug:** `onyx`.

Use a concise sourced matrix: OS-specific compatibility, cost/licence, intended workflow, scan/cleanup model, approvals, grouped activity, recurring growth, developer caches and install/runtime conditions. Keep source links beside factual cells. If official evidence supports the candidate scope, OnyX may suit maintenance/parameter controls; Breathing Room may suit storage exploration and app activity investigation. Neither recommendation is approved while competitor evidence is blocked.

Disclose “Breathing Room, which we build” at its recommendation. Current `capabilities.md` evidence is reused, not live retested: free preview; macOS 13+ and Python 3.10+; preview installer lacks Developer ID/notarization and clean-machine/physical-Intel certification. Source implementations do not establish binary parity. Hosted AI requires authentication/internet and sends relevant context/tool output to a service. AI Care is advertised at $5 USD/month or $50 USD/year, renews, with applicable tax; free local capabilities are separate. Explain the optional automatic Ruff-cache exception rather than claiming unconditional per-location prompts. Daily care requires the app running and exact saved approvals.

## Honest advantages and trade-offs

- **OnyX candidate strength:** OS-specific system maintenance and parameter controls could address a different job. This is a research hypothesis awaiting official evidence, not a supported recommendation. Do not assert unverified free use, notarization, uninstaller behavior or feature absences.
- **Breathing Room documented source strength:** storage exploration, grouped helper sampling and constrained reviewable cleanup may help investigate, but sampled I/O cannot prove which process wrote a file. No speed, safety or space-recovered comparison was performed.
- **Breathing Room limitations:** preview installation/runtime caveats, hosted AI boundary, optional paid care and source-versus-release distinction must remain visible. Existing preview numbers are illustrative.

## Validation and handoff

No applicable `AGENTS.md` was found in the app tree or checked ancestors. Read `PLAN.md`, `EDITORIAL.md`, `capabilities.md`, `screenshots.json`, baseline OnyX record and browser/Blog contracts before creating owned files. No subagents used. Existing unrelated work preserved. JSON/path/hash checks are recorded in `validation.json` and the attempt receipt after execution. No site build is claimed or needed for research-only files; independent evidence, image-rights and editorial review remain pending. **Receipt status must remain blocked**, even though this diagnostic packet is complete.
