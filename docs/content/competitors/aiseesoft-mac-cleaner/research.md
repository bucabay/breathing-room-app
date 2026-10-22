# Aiseesoft Mac Cleaner: research handoff

Checked **2026-10-21** · Task `research-aiseesoft-mac-cleaner` · **Blocked for drafting; not publication approval.**

## Decision

Retain this as a distinct, directly relevant Mac-cleanup product. `canonicalOwnerId: aiseesoft-mac-cleaner`; **alias skip: false**. The official identity is [Aiseesoft Mac Cleaner](https://www.aiseesoft.com/mac-cleaner/), branded by Aiseesoft Studio. “Mac Cleaner” is its vendor-scoped short form, not a globally unique product alias. No inspected evidence connects it to PowerMyMac, iMyMac or TechyCub. Do not merge unrelated vendors based on generic cleaner terminology. No official source repository was identified; that is not proof none exists.

**Two gates prevent drafting:**

1. **Visual rights:** the official guide links real app-UI images, but no republication licence/permission is established. Link-only fallback does not pass the required on-page visual gate. No competitor image bytes were downloaded.
2. **Compatibility:** the retained homepage simultaneously says “Mac OS X 10.7 or higher,” “compatible with macOS Sequoia and before,” and lists “macOS 27 Golden Gate/…” in specifications. Do not silently reconcile these, endorse the unusual release label, or recommend installation on a specific OS until version-specific evidence resolves the conflict.

No article, site record, queue/database update, installation, native scan, cleanup, signup, message, checkout or deployment was performed. All product behavior below is documented, not hands-on tested.

## Reused evidence and discovery

Reused the corresponding **batch-1** record before new research; `baseline-reused.json` retains it. The same-day official homepage was **not re-fetched**. `sources.json` preserves its existing snapshot/hash and the directory snapshot/hash. New retained public HTML/text is restricted to the missing official guide and purchase terms.

- Discovery: <https://alternativeto.net/software/aiseesoft-mac-cleaner/about/>, retrieved `2026-10-21T19:04:53.433Z`.
- CleanMyMac edge: <https://alternativeto.net/software/cleanmymac/?p=3>, retrieved `2026-10-21T18:36:26.872Z`.
- Mole edge: <https://alternativeto.net/software/mole/?p=8>, retrieved `2026-10-21T18:37:24.218Z`.
- Existing official snapshot: `docs/content/.runtime/verification-1/aiseesoft-mac-cleaner-official.json`, retrieved `2026-10-21T19:08:09.581052+00:00`.
- Discovery is listing provenance, not feature proof. Exact new retrieval timestamps, final URLs and original SHA-256 values are in `sources.json` and `research.json`.

## Verified claims and boundaries

The machine packet contains **19 claim records**, each with source URL, supporting excerpt, check date/time, evidence class, intended location and scope. An exact app version was **not established**: the pages are unversioned, and no installer was downloaded. Do not invent a build number or equate the guide’s screenshots with the current binary.

| Topic | Documented finding | Claim/source |
| --- | --- | --- |
| Review workflow | Large & Old Files → Scan → View/Rescan → review/select → Clean. This describes deletion, not a guarantee of undo or recovery. | `workflow`, [official guide](https://www.aiseesoft.com/mac-cleaner/tutorial.html) |
| Filters | Guide lists `> 100 MB`, `5 MB to 100 MB`, `>1 Year`, `>30 days`. Old or large is not equivalent to unneeded. | `age-size-buckets`, guide |
| Breadth | Vendor advertises system/photo/email/iTunes cleanup, duplicates, similar photos and an uninstaller. Do not repeat antivirus efficacy or speed/savings promises. | `cleaner-categories`, `uninstaller`, [homepage](https://www.aiseesoft.com/mac-cleaner/) |
| Monitoring | CPU, memory and disk monitoring advertised. App/helper grouping, writer attribution and historical recurring-growth tools are **not verified**, not “No.” | `system-status`, homepage |
| Platform | Mac product; Intel/M-series requirements advertised, but supported OS range conflicts. Universal binary, signing and notarization unknown. | `platform-conflict`, `architecture` |
| Local/hosted | Guide describes an installed Mac scan workflow. Offline completeness, telemetry and activation/network requirements unknown. | `workflow`, `availability` |
| Developer-specific work | Developer-cache adapters, recurring growth and exact saved-approval mechanisms not established for Aiseesoft. | Explicit unknowns; no negative feature claims |

A generic Windows choice in the purchase page’s custom-licence form does **not** establish Windows support for this Mac product.

## Pricing and material purchase conditions

[Official purchase page](https://www.aiseesoft.com/purchase/mac-cleaner.html), retained under `sources/purchase.html` and `.txt`:

| Displayed offer | Device/term | Crossed-out comparison price |
| --- | --- | --- |
| `$9.98` | 1 month / 1 Mac | `$19.95` |
| `$27.00` | 1 year / 1 Mac | `$45.00` |
| `$48.00` | Lifetime / 1 Mac | `$80.00` |
| `$99.95` | Lifetime / 5 Macs | `$249.75` |

These are advertised promotional **dollar labels**, not confirmed final transaction totals. The cleaner price labels do not explicitly establish the currency code, tax, subsequent renewal price or cleaner auto-renewal mechanism. Do not turn a one-month licence into a verified recurring subscription, or infer future major-version entitlements from “Lifetime.” The directory calls the software proprietary; paid commercial licence offers are official, but an exact EULA/source-licence grant remains unverified.

**Material separate charge:** the purchase page says: “When you purchase Aiseesoft Mac Cleaner, you also gain 7-day free access to Aiseesoft Mac Blu-ray Player. After the trial, the subscription will automatically renew monthly with US$31.20. You have the option to cancel at any time before the renewal takes place.” This is a **bundled player**, not Mac Cleaner’s monthly price. Default selection, opt-out availability and actual checkout total were not tested. Any future price comparison must include this condition.

Refund footer: “We support 30-day refunds for lifetime licenses when there is a quality problem.” The homepage/guide have broader quality-problem language. Do not promise an unconditional refund across all plans. A public “Free Download” link is not evidence of unrestricted free cleaning; trial duration/quota remains unknown.

Refresh volatile terms by **2026-11-20**, and before publication if overdue. No purchase links were followed into checkout.

## Visual records

### Competitor: link-only, gate blocked

- Source: <https://www.aiseesoft.com/mac-cleaner/tutorial.html>, Step 4, “Review and Select Items.”
- Exact app-UI asset URL: <https://www.aiseesoft.com/images/mac-cleaner/clean-large-old-files.jpg>.
- The guide identifies this as the Large & Old Files selection view, not a landing-page image. The HTML’s asset reference is retained; image bytes were **not** downloaded or visually inspected.
- Capture date, version, dimensions, original image hash and current binary parity: unknown. The manifest deliberately leaves these null.
- Reuse: **link-only**. The official footer says “Copyright © 2026 Aiseesoft Studio. All rights reserved.” Public reachability does not supply permission. No fair-use conclusion or blanket licence is invented; no permission request sent.
- Proposed caption: “Aiseesoft’s official guide illustrates selecting large and old files before Clean. Vendor illustration; app version and capture date unknown.”
- Proposed alt: “Official Aiseesoft Mac Cleaner guide image of the Large & Old Files results and selection view.”
- Resolution: retain permission or an explicitly approved legal/policy reuse basis before acquisition; preserve original bytes/hash, inspect privacy/currentness and obtain independent contextual review.

### Breathing Room: selected current-source example preview

- Reuse `current-space-browser-preview` from `docs/content/screenshots.json`; do not copy or modify shared assets.
- Path: `docs/content/assets/breathing-room/space-preview-2026-10-21.png`.
- Original SHA-256: `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a`.
- Capture: `2026-10-21T19:06:45.416416+00:00`; source commit `54828ac3170b45861aee70861dd0b9c658ed7e51`; 2940 × 3468.
- **Actual PNG opened and read in this job.** It shows the Space category view, preview/example banners and floating assistant composer. Example storage/activity values are not measurements. Long full-page view needs responsive contextual review; no crop made here.
- Required caption: **“Current-source Breathing Room Space browser preview, captured October 21, 2026. Example data only; not a native scan, measured activity or cleanup result.”**
- Required alt: “Breathing Room Space view rendered in a browser with illustrative example data.”
- Keep visible “Interactive preview · example data” / browser-preview warning. Reuse basis: app-owner-requested first-party UI capture; marks remain their owners’ marks. Not a native scan or distributed-release parity certification.

## Distinct workflow article brief

**Track:** search/reference. **Working title:** “Review large and old Mac files without treating age as permission to delete.” **Slug:** `review-large-old-mac-files-aiseesoft`.

**Reader job:** turn Aiseesoft’s documented size/age buckets into a deliberate review queue. This is not a generic “best Mac cleaner” post or the comparison matrix expanded into filler. The description should answer first: filtering narrows inspection; it does not prove a file is disposable.

1. Put the official Large & Old Files UI immediately after the lead **only after rights clear**.
2. Explain the exact documented buckets and Scan → View → select sequence. Do not imply we executed it.
3. Review owner, sole-original status, backup and rebuild/download cost. Unknown candidates stay untouched. Do not label old projects or backups disposable merely because of age.
4. Distinguish a one-off inventory from the separate question “what keeps growing?” Use the qualified current-source Breathing Room Space preview as the later visual.
5. Give a single bounded recommendation with “Breathing Room, which we build,” and explain when Aiseesoft’s broader utility set better matches the task.

**Interaction pass handoff:** non-mutating keep/investigate checklist (known owner, backup verified, reproducibility, active project dependency). Any unknown leads to investigation, never automatic deletion. No app installation, arbitrary demo repo, fake scan, savings calculator or cleanup action is required. Link to `/comparisons/` and `/comparisons/aiseesoft-mac-cleaner/`; those are proposed links, not route-existence checks.

## Concise comparison brief

**Title:** “Breathing Room vs Aiseesoft Mac Cleaner.” **Slug:** `aiseesoft-mac-cleaner`. Intent: choose category-based cleanup versus owner/activity investigation, with honest preview and purchase caveats.

Use the machine packet’s sourced matrix: OS/version caveat; paid licence versus free core/paid AI; review controls; local/hosted boundary; monitoring; unknown developer-cache/history capabilities; installation caveats; broader utility differences. Every factual cell cites its claim. Link to the workflow article rather than duplicating its detailed review procedure. No separate alternatives doorway is justified.

### Truthful advantages and trade-offs

- **Aiseesoft:** its guide documents selectable size/age results, and its vendor page advertises duplicate/photo/uninstaller utilities. Those may suit a one-off broad utility workflow; completeness, results and current UI are not independently tested. Compatibility conflicts and the bundled-player renewal are material caveats.
- **Breathing Room, which we build:** the same-day `capabilities.md` register supports owner/project exploration, app/helper grouping, activity history and constrained cleanup approvals at the **source** level. Do not assert installer feature parity, superior safety, speed or recovered space.
- **Our limitations must accompany the recommendation:** `0.1.0-preview.1`, macOS 13+, Python 3.10+ prerequisite; published release says Apple Development signed, not Developer ID signed or notarized; physical Intel/clean-machine behavior unverified. Free local app; optional AI Care advertised at $5 USD/month or $50 USD/year, renewing with applicable tax. Hosted assistance needs authentication/internet and may send relevant path/process/storage information. Exact-location approval is not an unconditional “never deletes without asking” promise: optional verified Ruff-cache automatic Trash mode exists, while daily care uses exact remembered approvals and requires the app running.
- No equivalent complete uninstaller/duplicate-photo feature was established for Breathing Room. Unknown does not mean absent. Do not market it as a certified antivirus replacement.

## Validation and remaining work

`validate.py` checks source/text hashes, excerpt support, source/claim references, retained app-UI asset reference, selected preview hash/dimensions, identity/draft gates and owned-file inventory; actual outcomes are retained in `validation.json`. They do not constitute independent editorial review or native testing.

No site check/build/test is applicable: no marketing files changed. No score assigned; independent article review remains pending. Read-only research used no browser session, credentials or hidden cookie extraction. Relevant blog/browser skills were loaded; no agents spawned.

Legal/version URL probes `/company/terms-of-use.html`, `/company/license.html`, and `/mac-cleaner/reference.html` returned HTTP 404. The homepage’s actual tech-spec anchor was already retained. Exact EULA, version, trial limits and privacy/activation behavior remain explicit unknowns rather than invented facts. Research can retain those noncritical unknowns, but the image-rights gate still blocks drafting; exact compatibility must be resolved before installation recommendations.
