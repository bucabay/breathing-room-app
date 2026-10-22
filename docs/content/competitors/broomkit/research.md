# Broomkit research: blocked before drafting

Checked **2026-10-21** · task `research-broomkit` · no publication approval.

## Decision

Broomkit is a relevant, live **direct Mac-cleanup comparison**, not a dead product or a verified alias of another cleaner. Its official homepage is <https://broomkit.com/>. The capitalization **BroomKit** on AlternativeTo describes the same product: retain `canonicalOwnerId: broomkit`, with **no alias skip** and no separate capitalization draft. The [official About page](https://broomkit.com/about/) identifies DPR Software Labs OPC Private Limited and developer Diljit PR, and explicitly says it is not a rebadged cleaner. No evidence connects it to PowerMyMac. No official source repository was identified in the checked pages; that is not proof none exists.

**Drafting is blocked by two specific gaps:**

1. **Post-trial entitlement conflict.** [Terms](https://broomkit.com/terms/) say “After that a valid licence is required to use the app.” The [licensing page](https://broomkit.com/refund-policy/) repeats that a licence is needed after three days, but also says “Scanning continues to work for free either way.” The retained homepage says both “Free to analyze forever” and “There is no reduced free tier after the trial.” About also describes permanent free scanning. Do not silently choose a favorable version. Obtain consistent, current version-specific official documentation or separately authorized non-destructive evidence before a free-versus-paid recommendation.
2. **Competitor screenshot rights.** A real app-image source and exact asset URL are identified below, but public access does not establish republication permission. Link-only is a research fallback, not satisfaction of the mandatory on-page screenshot gate. Need permission/licence evidence or an explicit policy decision. No permission request was sent and no competitor image was downloaded.

The full claim ledger, supporting excerpts, conditions, source dates, briefs and provenance are in [`research.json`](./research.json). Noncritical unknowns are retained rather than converted into negative comparison cells.

## Evidence reused first

Reused the corresponding `docs/content/verification/batch-1.json` record and its official/directory snapshots. The homepage snapshot is dated `2026-10-21T19:08:01.448223+00:00` and its SHA-256 was checked against the baseline. The AlternativeTo snapshot is dated `2026-10-21T19:05:21.862Z`; its hash is also retained in JSON. Discovery came from CleanMyMac page 8, <https://alternativeto.net/software/cleanmymac/?p=8>, via <https://alternativeto.net/software/broomkit/about/>. The directory's from-$34 offer is not used over the current official $9 offer.

New read-only official checks addressed missing material evidence: About, Terms, Licensing, Privacy, the public update JSON and homepage image/structured-data metadata. Exact request times were not emitted for the new WebFetch calls; the actual check date is retained without fabricated timestamps. The new metadata snapshot is [`home-visual-metadata.json`](./home-visual-metadata.json). It is source data, not editorial instructions or an image licence.

## What can be stated, with boundaries

| Dimension | Supported finding | Evidence / condition |
| --- | --- | --- |
| Version | Official feed identifies **0.6.0, build 9**, published **2026-09-12**. | [Update feed](https://broomkit.com/downloads/latest.json), C03. No binary downloaded or tested. |
| Platform | Vendor documents **macOS 14.0+**, Apple Silicon and Intel; Full Disk Access for the described scan. | [About](https://broomkit.com/about/), [Terms](https://broomkit.com/terms/), C02. No Windows/Linux support established or implied. |
| Licence / price | Proprietary use terms; advertised **USD $9 once**, lifetime, one concurrent Mac. Deactivate before transferring to another machine. | [Terms](https://broomkit.com/terms/), [Licensing](https://broomkit.com/refund-policy/), homepage `priceCurrency: USD`, C04/C14. Checkout, tax, regional totals and future major-version entitlement unverified. |
| Trial | All features advertised free for **three days**, once per Mac, no account/card. | Terms and update feed, C05. Post-trial free scope is blocked, C06. |
| Purchase caveats | Vendor says all sales final; duplicate-charge/undelivered-key errors have a billing-correction exception. | Licensing, C04. Not a legal assessment of mandatory rights. |
| Scan / cleanup | Documented home-folder scan, Disk Map, categories, individual path review and Trash-first moves. | [Homepage](https://broomkit.com/), C07. Not measured coverage, savings or guaranteed recovery. Emptying Trash ends the ordinary restore path. |
| Uninstaller | Vendor documents leftovers, deselection and Reset without uninstalling the app. | Homepage, C08. Reset concerns app data; do not call it disposable cache or promise perfect removal. |
| Monitoring | Advertises live memory, CPU, disk and battery, per-app Quit and alerts. | Homepage, C09. Helper grouping and historical/recurring-growth attribution are **not verified**, not absent. |
| Developer scope | Advertises package caches, simulators and nested dependency directories. | Homepage, C10. No benchmark or adapter-by-adapter execution evidence. |
| Local / network | Policy says scans stay local; activation sends licence key and machine identifier to Dodo Payments. Validated licence works offline **14 days** before rechecking; optional daily update check. | [Privacy](https://broomkit.com/privacy/), C11. Policy, not traffic audit. Website separately discloses Google Ads/Clarity; do not generalize app privacy to website. |
| Runtime / installation | Says no login item, launch agent or privileged helper; root tasks print commands instead. Advertises Developer ID signing and notarization. | Homepage/About, C12/C13. Vendor statements, not installer inspection; no commands executed. |

Do not repeat vendor claims that every cache is harmless to delete, totals equal recovered free space, or competitors necessarily miss directories. The vendor's 84.8 GB example concerns a particular reference machine, not our scan or an expected outcome. No hands-on use, cleanup, speed or safety measurements were performed here.

## Visual handoff

### Competitor: exact official app image, link-only

- Source: <https://broomkit.com/#demo>.
- Asset: <https://broomkit.com/demo/disk-map.jpg?v=021>.
- Homepage DOM identifies it as a Home-folder Disk Map treemap; natural dimensions reported **980 × 647**. Homepage describes demo screenshots as the real app, not mockups. Exact image build/OS/capture date remain unknown; asset query `v=021` is not a product version.
- Proposed alt: “Broomkit Disk Map treemap of the Home folder with safe-to-remove, needs-review and not-reclaimable categories.”
- Proposed caption: “Broomkit's official Disk Map screenshot. Vendor-supplied app view; figures are not our measurements or an expected cleanup result. Open the official demo for the image.” Credit DPR Software Labs OPC Private Limited.
- **Reuse: link-only; permission pending.** No downloaded original, hash, derivative or published asset exists. No blanket grant found in checked Terms/About links. Do not invent an original hash or silently hotlink it into an article. Independently inspect actual pixels/privacy after reuse is cleared.

### Breathing Room: selected current-source Space preview

- Reuse shared original `docs/content/assets/breathing-room/space-preview-2026-10-21.png`; do not edit the shared asset.
- Captured `2026-10-21T19:06:45.416416+00:00`, source commit `54828ac3170b45861aee70861dd0b9c658ed7e51`, browser URL `http://127.0.0.1:1431/`.
- SHA-256 checked: `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a`. Dimensions **2940 × 3468**.
- Required caption: **“Current-source Breathing Room Space browser preview, captured October 21, 2026. Example data only; not a native scan, measured activity or cleanup result.”**
- Alt: “Breathing Room Space view rendered in a browser with illustrative example data.” Keep the example-data banner visible. First-party owner-requested capture basis is recorded in `screenshots.json`; third-party marks remain their owners' marks.
- This job verified the existing file hash, not a new capture or new pixel-level review. Shared inventory visual/privacy review is retained; per-article legibility, context and any later crop need independent review and derivative hashes. No earlier screenshot is relabeled current.

## Distinct workflow article brief

**Proposed title:** Review a Mac cleanup list before emptying the Trash  
**Proposed slug:** `review-mac-cleanup-paths-before-emptying-trash`  
**Track:** search/reference. **Status:** blocked brief, not a draft.

Reader job: turn a disk map and candidate paths into a deliberate keep/remove/rebuild decision. This is not another generic System Data explanation or a renamed comparison matrix.

Outline:

1. Interpret a Disk Map without equating its total with recoverable free space.
2. Classify candidate paths: original data, known regenerable material, or unknown.
3. Keep app Reset/uninstallation decisions separate from cache cleanup; inspect retained data and backups.
4. Review Trash moves before choosing to empty it; explain the rollback boundary without claiming guaranteed recovery.
5. If growth returns, investigate the cause rather than repeating deletion.

Use C07–C12 and the current Breathing Room source register, not invented testing. Place a rights-cleared Broomkit Disk Map view after the lead, then the explicitly labeled Breathing Room Space preview later. Current rights status blocks that image plan.

**Interaction handoff:** a local-only decision checklist asking whether ownership is known, a backup exists, rebuild/download cost is understood and the app is closed where appropriate. Unknown personal data stays. No scanner, filesystem access, deletion, fake savings calculation or unnecessary code-demo repo. Link to `/comparisons/` and `/comparisons/broomkit/`; verify routes in the later site job. Earn the length; no artificial FAQ.

## Concise comparison brief

**Proposed route:** `/comparisons/broomkit/`  
**Title:** Breathing Room vs Broomkit: cleanup review and ongoing care.

Lead with the workflow choice and affiliation: **“Breathing Room, which we build”**. Follow with a compact sourced matrix for platform, licence/trial, maps and path review, app uninstaller, monitoring, developer material, local/hosted boundary and runtime requirements. Add bounded “when to choose each” sections and link to the distinct workflow article. No separate alternatives doorway page.

**Broomkit advantages:** documented integrated Disk Map/uninstaller/Reset and live performance displays; one-time one-Mac licence; local-scan policy and advertised Developer ID/notarization. These are attributed documented offerings, not proof of better speed or safety.

**Broomkit trade-offs:** macOS 14+, proprietary terms, fourteen-day offline licence recheck, all-sales-final policy and unresolved free tier. Recurring-growth investigation, helper aggregation and exact saved scheduled approvals remain unknown rather than absent.

**Breathing Room advantages:** inspectable Apache-2.0 desktop source and source implementations for helper grouping, activity history, tool-aware cleanup and exact saved daily approvals. Do not present source presence as distributed-release validation or claim it has a complete app uninstaller.

**Breathing Room trade-offs:** current identified `0.1.0-preview.1`, macOS 13+, Python 3.10+, Apple Development signed but not Developer ID signed/notarized; clean-machine and physical-Intel behavior unvalidated. Optional AI Care is USD $5/month or $50/year; hosted authenticated reasoning sends relevant context/tool outputs off-device, and daily care needs the app running. Local tools do not require AI Care. Explain the optional automatic Ruff-cache mode instead of promising unconditional per-action prompting. Current images are browser example data. Source: same-day `docs/content/capabilities.md`, BR01–BR03.

## Checks and handoff

- Read PLAN, EDITORIAL, capabilities and screenshots inventory before writing. No applicable `AGENTS.md` found in checked ancestors, repository root or docs subtree. The initial broad parent-tree discovery timed out; scoped checks completed instead.
- Loaded blog and browser-automation skills; read the MailKite contract under the Breathing Room adaptation. No agents spawned.
- Reused baseline records; checked official additional source content, not only reachability. Hash-checked existing discovery, homepage and selected preview originals.
- Public HTTP metadata request returned 403. Normal authorized Chrome worked in newly owned tab 66; public DOM supplied exact screenshot URLs and metadata. No credentials, browser cookies or private storage read. One extra read-only metadata expression failed to parse; the successful retained snapshot is the evidence.
- No competitor assets downloaded without permission. No accounts, messages, purchases, cleanup, installs, system changes, site edits, queue/database mutations, commits, pushes or deployments.
- Research JSON/schema/reference/hash checks are recorded in the job receipt after execution. No app/site build or runtime test is claimed for this research-only change. Drafting and independent editorial/rendered review remain blocked; no score or publication approval awarded.
