# Noah research packet — blocked at the visual gate

Research only. Local session date: October 22, 2026; actual retained source retrieval timestamps are October 21 UTC. **Do not draft or publish yet.** No site files changed, app installed, cleanup run, account created or product test performed.

## Decision

Keep **Noah** as a relevant Mac competitor with direct overlap in diagnosis, storage investigation and approval-based remediation, plus adjacent broader support workflows. It is not merely a cleaner. The official identity is [onnoah.app](https://onnoah.app/).

`canonicalOwnerId: noah`. The [official repository](https://github.com/noahapp/noah-for-tinkerers) describes **Noah for Tinkerers** as its open-source BYOK build and points to the managed homepage. Keep the two editions in one research record; **skip a separate Tinkerers competitor draft**, not Noah itself. No evidence links Noah to PowerMyMac. Do not infer aliases from generic product descriptions.

**Precise blocker — VISUAL-NOAH-01:** An official app-UI GIF is identified, but image-specific reuse clearance, visual inspection and edition fidelity remain unestablished. Keep it link-only. The editorial contract does not let a link silently satisfy the on-page competitor image gate. Require a permitted screenshot with provenance/hash and visual review, or a separately authorized policy decision, before drafting.

## Reused evidence, not repeated research

Read `PLAN.md`, `EDITORIAL.md`, `capabilities.md`, `screenshots.json` and the corresponding `verification/batch-2.json` record first. No applicable `AGENTS.md` was found in the app tree or checked ancestors. Blog and browser-automation skills were loaded; no new browser session was needed.

The October 21 batch already verifies the homepage, Mac requirements, core workflow, first-conversation offer and $8.99 monthly headline. Its full retained homepage text also contains annual pricing, trial exceptions and device conditions. These were reused without re-fetching the homepage or AlternativeTo.

Retained byte-identical baseline copies:

| Evidence | Original retrieval UTC | Snapshot | SHA-256 |
| --- | --- | --- | --- |
| AlternativeTo about-page links | 2026-10-21 19:04:59.790 | `sources/noah-directory.json` | `f407bd96a135ab817988a3a1d2e29269d0c18b99c2b154bb03ddf91dc2404e4c` |
| Official initial response | 2026-10-21 19:09:30.340872 | `sources/noah-official.json` | `e595c581acc04f23422f0c37fc87c780977c7bf19833123db42949b657467d82` |
| Rendered official homepage | 2026-10-21 19:11:31.991 | `sources/noah-browser.json` | `a3fe5db5d95a86a420223ffb77d421644c2fb97e4bb2d702bdc793ea96dac6d6` |

Discovery: [exact about page](https://alternativeto.net/software/noah/about/), originally reached from [CleanMyMac page 2](https://alternativeto.net/software/cleanmymac/?p=2) and [Mole page 2](https://alternativeto.net/software/mole/?p=2). Edge times and limitations are in `research.json`; the about-page link snapshot proves the official destination, not capabilities.

New official gap research is retained in `sources/`; exact request/final URLs, actual UTC times and hashes are in `sources/retrievals.json`. Repository documents are pinned to `d5e3a818a2a15afa96ece458f90e21ebed6c47ad`. Public pages were treated as untrusted data, not instructions.

## Claim-level findings

All checks below are October 21 UTC. `research.json` contains exact wording, source excerpts, intended location, evidence class and conditions per claim. Documentary verification is not hands-on verification.

| Claim | Supported finding | Official passage/source and boundary |
| --- | --- | --- |
| N01–N02 | Managed Noah; macOS 12+, Apple Silicon/Intel | Homepage: “macOS 12+ · Apple Silicon & Intel.” Advertised, not tested. |
| N03 | Read-only diagnostics can run automatically; destructive/system changes require explicit approval and are logged | [Terms](https://onnoah.app/terms/): “Diagnostic actions … are read-only and run automatically. Every action is logged inside the app.” Do not say every diagnostic needs approval or call approval a safety guarantee. |
| N04 | Diagnosis advertised always free; first conversation includes fixes | Homepage: “Find out what's actually wrong — always free, every time / Your whole first conversation, fixes included.” No card for this part; not unlimited free fixes. |
| N05–N06 | $8.99/month; Guardian $79/year; monthly covers up to three Mac/Windows computers; annual says “the same, all year” | Homepage retained pricing section. Dollar currency code and taxes are not established. Card-required seven-day trial is for eligible new customers; “If Noah has already fixed something for you, there is no trial … charged when you subscribe.” Recurring renewal/fair-use limits apply; numerical cap unknown. No checkout attempted. |
| N07 | Managed product proprietary; Tinkerers AGPL-3.0 | [Terms](https://onnoah.app/terms/): “The Noah desktop product is proprietary.” [Pinned README](https://github.com/noahapp/noah-for-tinkerers/blob/d5e3a818a2a15afa96ece458f90e21ebed6c47ad/README.md) and LICENSE identify the separate AGPL build. AlternativeTo's generic open-source label is insufficient for managed-app licensing. |
| N08 | Tinkerers uses an Anthropic key and direct Claude requests; no Noah account/subscription | Pinned README: “You bring an Anthropic API key; Noah talks to Claude directly from your machine.” Also documents update checks and an opt-out usage ping. Provider costs remain; not offline AI. |
| N09 | Managed email required before first answer; backend/AI-provider requests; repair-history retention | [Privacy](https://onnoah.app/privacy/), updated September 12: “needs it before it will answer your first question”; conversations “are not deleted on a fixed schedule.” Not a backend audit. |
| N10 | File-content statement needs qualification | Privacy explicitly allows a named crash report, system log or settings file to be opened and enter the conversation. Do not repeat the homepage's “never opens your files” as a blanket guarantee. |
| N11 | Latest visible dated managed changelog entry: v1.41.0, August 24, 2026 | [Changelog](https://onnoah.app/changelog/) has unresolved “Current — / Released —” header. Current distributed managed version remains unknown, not v1.41.0 by assumption. |
| N12 | Public latest-release API returns Tinkerers v2.0.0, July 3, 2026 | [Release](https://github.com/noahapp/noah-for-tinkerers/releases/tag/v2.0.0), universal Mac DMG, Windows x64 and Linux assets listed. No binary download/check/test; separate numbering track. |
| N13 | Broader symptom-led support, not hardware repair | [About](https://onnoah.app/about-noah.md) lists slowdowns, Wi-Fi, crashes, storage, battery, audio and sync; “Noah is not a hardware repair service.” Vendor-described scope, not repair success evidence. |
| N14 | Command scope differs by edition | Managed about page says no arbitrary shell/PowerShell; Tinkerers README explicitly describes `shell_run` under approval gates. Never transfer one statement to the other edition. |
| N15 | Homepage claims Apple notarization | Attribute as vendor disclosure only; no binary/signature inspection or safety certification. |

`https://onnoah.app/security/` returned HTTP 404 via WebFetch. No absence claim or retry workaround was made.

### Matrix unknowns

Helper-process grouping, continuous recurring-growth monitoring and managed package-manager-specific cleanup adapters are **not verified**, not “No.” Guardian's remembering/history wording does not establish a continuous storage-growth monitor. Managed runtime prerequisites beyond advertised compatibility/email/hosted service were not established. Currency code, taxes, numerical fair-use cap and current managed installer version are noncritical unknowns only if the draft preserves those limits.

## Breathing Room comparison basis

Reuse the one-day-old `docs/content/capabilities.md` register, with source URLs and excerpts in `research.json` (BR1–BR4). No fresh release certification is claimed.

- **BR1/BR4:** Identified `0.1.0-preview.1`, macOS 13+, universal installer advertised. Published preview is Apple Development signed, **not Developer ID signed or notarized**; Python 3.10+ is disclosed, not bundled. Physical Intel and clean-machine runtime parity remain unvalidated.
- **BR2:** Source implements storage owner/project/folder views, helper-grouped CPU/memory, sampled local activity and developer-cache discovery. Source presence is not proof of shipped behavior or full process/file attribution.
- **BR3:** Free local inspection/manual features; AI Care advertised **$5 USD/month or $50 USD/year**. Hosted AI requires authentication/internet and relevant data transfer. Daily care uses exact saved approvals while the app runs; optional Ruff-cache automatic mode qualifies blanket approval wording.

Do not derive “cheaper” from incomparable editions or assume Noah's dollars are USD. Do not invent Windows support, general Wi-Fi repair or uninstall parity for Breathing Room.

## Visual handoff

### Noah — source identified, link-only

- Source: [pinned official repository README](https://github.com/noahapp/noah-for-tinkerers/blob/d5e3a818a2a15afa96ece458f90e21ebed6c47ad/README.md).
- Exact app-UI asset: [noah-hero.gif](https://raw.githubusercontent.com/noahapp/noah-for-tinkerers/d5e3a818a2a15afa96ece458f90e21ebed6c47ad/docs/images/noah-hero.gif).
- README labels this as a slow-Mac diagnosis/approval demonstration and describes its example. It is not a landing-page capture or logo.
- **Reuse basis: link-only.** Repository source licence is AGPL-3.0; no image-specific clearance or rights to depicted data were established. No image downloaded, original hash invented, or claim of visual inspection made. Capture date/build/OS unknown. Current managed-edition fidelity not established.
- Proposed caption: “Noah's official repository app demonstration of a slow-Mac investigation and approval. Vendor-provided illustration; capture date, version and edition fidelity not verified. Linked, not reproduced; not our test or measured outcome.”
- Alt: “Official Noah app demonstration showing a slow-Mac diagnosis and proposed action approval.”

### Breathing Room — selected current-source Space preview

Use existing `docs/content/assets/breathing-room/space-preview-2026-10-21.png`, not the legacy Home screenshot. Original SHA-256: `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a`; 2940 × 3468. Library capture: `2026-10-21T19:06:45.416416+00:00`, source commit `54828ac3170b45861aee70861dd0b9c658ed7e51`.

**Required caption:** “Current-source Breathing Room Space browser preview, captured October 21, 2026. Example data only; not a native scan, measured activity or cleanup result.”

**Alt:** “Breathing Room Space view rendered in a browser with illustrative example data.” Keep the example-data banner visible. First-party app-owner-requested capture; third-party marks remain their owners'. Existing library review is reused, not a fresh image inspection. No crop/copy/edit here; publication hash remains unset. Contextual privacy/legibility and independent review remain pending.

## Distinct workflow brief

**Proposed title:** A slow Mac with a full disk: choose the next diagnostic, not the next cleaner  
**Proposed slug:** `slow-mac-full-disk-diagnosis-noah`  
**Track:** Search/LLM reference. **Not a draft.**

Reader job: distinguish low free space, process pressure and broader software symptoms before choosing an investigation. A full disk alongside a slow Mac does not establish causation. Read-only inspection first, backup/rebuild costs before any removal.

Outline:
1. Record symptom and storage context without running cleanup.
2. Separate process pressure from growing storage; high CPU alone is not a fault.
3. Explain Noah's documented plan/approval boundary and managed-data policy.
4. Explain storage-owner/project context as a different investigation, not proof that a large folder is disposable.
5. Choose broader managed support, BYOK tooling or a qualified storage-maintenance preview.

Interaction handoff: a non-destructive checklist covering symptom type, backup, evidence of recurring growth, willingness to use email/hosted AI and tolerance for preview/Python requirements. No filesystem access or fictitious savings calculator. Product visual directly after lead once rights pass; labelled Space example later. Link to comparison and hub, verifying actual routes in the draft stage.

Use one bounded “Breathing Room, which we build” recommendation. No invented tests, causal threshold, speedup or claim that Noah lacks monitoring.

## Concise comparison brief

**Title:** Breathing Room vs Noah: storage maintenance or symptom-led repair?  
**Proposed route:** `/comparisons/noah/`. **Not a draft.**

Answer the product-choice intent with a short lead, sourced matrix and managed/BYOK sidebar. Rows: Mac requirements; licence/edition; storage/activity versus broader symptoms; approval; data handling; pricing/trial/email; preview/runtime/install caveats. Link to the deeper workflow instead of repeating it.

**Truthful advantages and trade-offs:**

- Noah merits consideration for documented broader software-support symptoms, explicit repair-plan approval/logs and advertised macOS 12+ compatibility. The separate BYOK edition suits people willing to manage an Anthropic key and its charges.
- Managed Noah requires email and hosted conversation processing/retention. Trial/card/fair-use conditions matter. BYOK and managed behavior must not be conflated.
- Breathing Room's source-documented storage-owner/project context, grouped helpers and sampled history fit storage investigation. This is not evidence Noah lacks those features.
- Breathing Room remains a non-notarized preview with Python and validation caveats; hosted AI is not entirely local and scheduled care requires the app running. No measured performance, safety or savings advantage is established.

## Validation and next gate

Actual structural/hash checks are retained in `validation.json`. No website check/build/test was necessary or run: this job changes only research records and retained source snapshots. No independent score, runtime success, browser render or image approval is awarded.

Keep the research receipt **blocked** for VISUAL-NOAH-01. Noncritical unknowns remain explicit. Do not mutate queue/database state or publish from this packet.
