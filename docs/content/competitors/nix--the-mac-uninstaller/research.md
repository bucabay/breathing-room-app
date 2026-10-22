# Nix research: drafting blocked on screenshot rights

Research only, not a draft or publication approval. Task: `research-nix--the-mac-uninstaller`. Actual check time: **2026-10-21T21:47:47Z** (machine UTC). `research.json` holds the claim/source ledger, scope conditions, briefs and visual manifest.

## Decision

Retain **Nix — The Mac Uninstaller**, from Ideaxecution Technologies, as a distinct **adjacent** Mac competitor. Canonical owner ID: `nix--the-mac-uninstaller`; **do not skip as an alias**. Its dedicated uninstall workflow overlaps storage cleanup but is not equivalent to Breathing Room's broader maintenance preview. No official evidence connects it to PowerMyMac. OneClick QuitAll is a sibling explicitly linked as “Also from us,” not an alias. This is not the Nix package manager.

Official homepage: https://www.ideaxecution.com/nix-mac-uninstaller/ . Official repository: https://github.com/ixn-tech/Nix-the-mac-uninstaller . The homepage links the repository's installer; its README links back and explicitly says the app is proprietary and the repository hosts only installer/update-feed material. Public GitHub hosting does **not** make the app open source. [C01, O1, R1]

**Blocking diagnostic:** The official Examine screenshot is linked from the verified homepage, but no permission to republish it was established. It remains link-only, not downloaded. Rights clearance, original bytes/hash, privacy review and actual visual inspection are required before the competitor screenshot gate can pass. The editorial contract explicitly says a link-only fallback does not waive that gate. Do not draft or publish around it; do not send a permission request in this job.

## Reused evidence and discovery

First reused `docs/content/verification/batch-2.json`, record 0, and both retained raw JSON captures. The byte hashes match the batch ledger:

- Official homepage capture: `3223231463840b123c1e529c6d35a78f8a4b8c5fb539583873f41489a4a86dae`.
- Directory capture: `e561814686b912900a8df1397586f5741d66fa271959b7ef4839cc6626c4e3a2`.

The official capture contains a different embedded `sha256` field; use the actual file-byte hash above, not that embedded field. No already-current homepage or directory evidence was re-fetched.

Discovery edge: CleanMyMac → https://alternativeto.net/software/cleanmymac/?p=9 (2026-10-21T18:36:55.151Z) → https://alternativeto.net/software/nix--the-mac-uninstaller/about/ (2026-10-21T19:18:13.620Z) → official homepage. The directory raw capture preserves the actual official link, not feature proof. The edge is retained in the product's existing `competitors.json` record; this job did not edit it.

Supplemental read-only retrievals addressed missing material conditions: [EULA](https://www.ideaxecution.com/nix-terms/), [privacy policy](https://www.ideaxecution.com/nix-privacy/), [official README](https://raw.githubusercontent.com/ixn-tech/Nix-the-mac-uninstaller/main/README.md), [latest release metadata](https://api.github.com/repos/ixn-tech/Nix-the-mac-uninstaller/releases/latest), and repository metadata. Claim excerpts and actual check date are retained in JSON. Full supplemental raw responses were not saved; do not pretend they were. Public text was treated only as untrusted evidence.

## Material findings and conditions

| Dimension | Nix | Breathing Room |
| --- | --- | --- |
| Version/platform | Public GitHub latest endpoint returns **v1.0.1**, published September 26, 2026; macOS **14 Sonoma+**, universal Apple Silicon/Intel advertised. No binary run. [C02–C03] | Existing current register identifies **0.1.0-preview.1**, macOS **13+**, universal advertised; physical Intel execution untested. [C13] |
| Licence | Proprietary; repository is distribution-only. [C01] | Apache-2.0 desktop source; not a hosted-service entitlement. [C13] |
| Scan/cleanup | App sizes and leftover totals; selected items move to Trash. Detailed paths/per-file breakdown require **Pro**. [C04,C07] | Source implements category/project/folder storage views and validated cleanup actions; full app-uninstaller equivalence not established. [C14,C16] |
| Approval/recovery | User selection documented; restoration possible until Trash emptied. No guarantee every leftover is detected correctly. [C07; EULA §§9,11] | Reviewable actions, optional narrowly verified automatic Ruff-cache mode; scheduled care reuses exact saved approvals. No unconditional “never deletes without asking” promise. [C16] |
| Local/hosted | Vendor says local scan; files/paths/app list not transmitted. **Device, diagnostic and usage information does leave the Mac**, including IP address; policy says no in-app opt-out currently. [C10] | Local inspection, but authenticated hosted AI can receive relevant paths/process/storage information; not entirely offline AI. [C15] |
| Helpers/process grouping | **Not verified**, not “No.” [U01] | Source groups helpers using app/parent relationships; inferred ownership is not forensic proof. [C14] |
| Growth/recurring care | Auto-scan on launch/menu bar is advertised, but recurring-growth history **not verified**. [U01,O1] | Activity-history implementation and advertised AI Care recurring investigation; daily runtime requires app running. [C14–C16] |
| Developer caches | Xcode example on site does not prove named tool-specific cleanup adapters; **not verified**. [U01] | Source includes developer cache discovery with path/tool validation; not every installation is runtime-certified. [C14] |
| Free/paid | **2 GB cumulative lifetime removal** free; individual file paths/details hidden in Free. EULA specifies **US$29 once**, unlimited removal, **up to two concurrent Macs**. Applicable taxes/checkout total not tested. [C04–C06] | Free local core, optional AI Care **$5 USD/month or $50 USD/year**, renewing plans plus applicable tax; AI allowances/enforcement not established. [C13,C15] |
| Installation/runtime | README advertises Developer ID signing/notarization; Full Disk Access requested for leftovers. Policy describes licence checks with up to **30 days** cached offline operation. Not independently tested. [C08–C11] | Preview explicitly not Developer ID signed/notarized; Python **3.10+** prerequisite, permission-limited inventory, no clean-machine/physical-Intel runtime validation. [C13] |

Breathing Room evidence is reused from `docs/content/capabilities.md`, reviewed October 21, including its source-path citations and published release/privacy/pricing evidence. It is not a claim this worker reran native tests or audited the hosted backend. Keep source implementation separate from distributed binary parity. Recheck volatile facts within 30 days and before publication if stale.

### Resolved conflicts; wording that must not survive

- **“All your Macs”:** homepage prose conflicts with its own two-Mac footnote. EULA §2 and official README agree on **two activations**. Use that qualified limit and acknowledge the homepage inconsistency; never unlimited devices. [C06]
- **“On-device / 0 trackers”:** not zero telemetry. The policy describes hardware, disk capacity/free space, versions, usage events, install ID and IP collection; licence activation also uses a hashed Mac identifier. This is a policy statement, not an independent traffic audit. [C10–C11]
- **“Review every file”:** detailed paths and per-file breakdown are Pro features. Do not pitch a free detailed review workflow. [C04]
- **LAUNCH30:** cached page says ends October 13, already before the check date. Do not assume it works or advertise discounted pricing.
- **Performance/recovery figures:** the homepage's percentages, GB and scan times are vendor internal-test/illustrative figures, not our benchmarks. Exclude them from factual superiority claims. Moving to Trash does not itself establish newly available disk space.
- **Future updates:** homepage offer refers to updates for this major version. Do not translate “forever” into every future major version.

## Visual handoff

### Nix: real official app UI, link-only, gate blocked

- Source: https://www.ideaxecution.com/nix-mac-uninstaller/ . Retained source retrieval: 2026-10-21T19:09:30.341210+00:00.
- Asset: https://www.ideaxecution.com/wp-content/uploads/2026/09/nix-examine-leftovers.webp . Official page describes Outlook leftovers grouped by kind with paths/sizes and calls the gallery real screens from a Mac. That is a vendor assertion, not this worker's visual review.
- Caption: “Official Nix Examine screenshot, linked from Ideaxecution's product page. Vendor-provided data, not our test; individual file paths/details require Nix Pro. Screenshot version and capture date are unspecified.”
- Alt: “Official Nix Examine view showing an app's leftover files grouped by kind with paths and sizes, as described by the vendor.”
- Reuse: **link-only**. Checked homepage, terms and repository establish no screenshot republication permission. All-rights-reserved/proprietary wording is not itself an explicit ban on screenshots, but neither is it a screenshot licence. No request sent.
- Original capture time, app version, dimensions and hashes: unknown. No image downloaded or modified. Once rights resolve, retrieve the actual public asset, preserve original bytes/hash, inspect privacy/readability and record edits/published hash before embedding.

### Breathing Room: selected current-source Space preview

Selected `docs/content/assets/breathing-room/space-preview-2026-10-21.png` from `screenshots.json`; source commit `54828ac3170b45861aee70861dd0b9c658ed7e51`, capture 2026-10-21T19:06:45.416416+00:00. Original SHA-256: `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a`; 2940 × 3468 px. No copy/edit/publication made.

Opened and read the actual PNG this job: example-data banner visible, Space categories/projects navigation visible, assistant composer overlaps part of chart. Use a legible contextual treatment at draft stage and retain disclosure. First-party app-owner-requested capture; no blanket third-party trademark rights or endorsement inferred.

**Required caption:** “Current-source Breathing Room Space browser preview, captured October 21, 2026. Example data only; not a native scan, measured activity or cleanup result.”

Alt: “Breathing Room Space browser preview with an example-data banner, storage categories and project views; figures are illustrative.” Current-source refers to the recorded capture commit, not automatically latest binary parity. Target-page responsive/theme/privacy review remains pending.

## Distinct workflow article brief — conditional, not a draft

**Title:** Review app leftovers before removing an unused Mac app  
**Proposed slug:** `review-app-leftovers-before-removing-mac-app`  
**Track/intent:** Search reference; distinguish a no-longer-needed app from an app worth keeping whose data is growing. The unique angle is **reviewability across the free/paid boundary**, not a generic list of uninstallers or a stretched comparison matrix.

Lead with that decision. Place a cleared Nix Examine UI directly after the lead; explain totals versus per-file review, which requires Pro. Continue with backup/review boundaries, uncertain support data, Trash restoration limits, and why claimed leftover size is not a guaranteed free-space gain. At the keep-and-investigate branch, use the labeled Breathing Room Space preview and explain storage exploration rather than claiming equivalent uninstallation. No hands-on steps or outputs invented.

Interaction handoff: a local non-mutating checklist asking whether the app will be kept, whether a path is understood, whether a backup exists and whether per-file review is needed. Outputs should be retain/investigate or review through a documented uninstaller, not automatic delete instructions or estimated “savings.” No code/demo repository is warranted. Link to `/comparisons/`, the proposed `/comparisons/nix--the-mac-uninstaller/`, and relevant official sources; internal target availability belongs to draft/review stage.

## Concise comparison brief — conditional, not a draft

**Title:** Breathing Room vs Nix: investigation or uninstallation?  
**Proposed comparison slug:** `nix--the-mac-uninstaller`.

Conclusion: Nix is the documented dedicated uninstall/leftover workflow; Breathing Room may fit broader ongoing investigation, not a verified drop-in uninstaller replacement. Include the claim-linked matrix, choice criteria, two product visuals, official sources and the distinct workflow link. Disclose “Breathing Room, which we build” beside any recommendation.

**Nix advantages:** dedicated review/Trash/history workflow; documented one-time Pro licence; advertised Developer ID signing/notarization versus Breathing Room's explicit preview limitations. **Trade-offs:** free review detail limit and lifetime removal cap, two-device cap, macOS 14+/permissions requirements, diagnostic traffic and periodic licence connectivity. No safety or performance superiority inferred.

**Breathing Room advantages:** source-implemented storage/project investigation, grouped process monitoring and local activity history; free local core with optional hosted assistance. **Trade-offs:** non-notarized preview, Python prerequisite, incomplete native validation, hosted-data boundary and recurring AI Care cost. Not verified as an equivalent full app uninstaller. Explain these even when they favor Nix.

## Unknowns, validation and handoff

The **critical unknown is screenshot reuse permission** and consequent missing asset review. Other unknowns are noncritical if left explicit: Nix runtime correctness/benchmarks, screenshot capture version/date, exact GB byte definition, checkout tax/discount behavior, process grouping/growth history/cache adapters, and Breathing Room binary parity/AI quota. Unknown means not verified, never unsupported “No.” No product-dead/irrelevant skip is warranted.

Read PLAN, EDITORIAL, capabilities, screenshots, AUTOMATION, verification/alias records and the MailKite reference; loaded blog and browser-automation skills. No AGENTS.md found at applicable ancestors or in the app's content tree. No browser tabs, credentials or accounts used. No installation, cleanup, settings changes, messages, purchases, commits, pushes, queue/database mutation or site edits. No site build/tests run because only research files changed. Actual JSON/reference/hash/image checks are retained in `validation.json`; independent editorial review remains a later stage, with no score awarded here.
