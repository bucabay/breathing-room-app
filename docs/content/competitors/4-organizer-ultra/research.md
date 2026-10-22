# 4-Organizer Ultra: research handoff

**Blocked for drafting: competitor screenshot rights (B01).** Identity and a conditional Mac-switcher intent are established. This is a research packet, not an article, publication approval or hands-on review. Checked October 21, 2026 UTC (October 22 local task date); exact per-source dates, excerpts and scope are in `research.json`.

## Identity, platform and deduplication

- Official product: **4-Organizer Ultra**, Ambeteco / American Best Technologies Company LLC. [Homepage](https://www.ambeteco.com/4-Organizer-Ultra/).
- `canonicalOwnerId: 4-organizer-ultra`; alias decision: **do not skip as alias**. Baseline aliases are empty. Official navigation treats Ultra, Nano, MyQuickMac Neo and MyQuickMac Lite as separate products, not interchangeable names. No PowerMyMac alias relationship is evidenced here.
- **Platform-adjacent, not a direct Mac substitute.** Official baseline says “Windows 11/10 x64.” A useful brief must serve someone moving to Mac, not imply Breathing Room runs on Windows or Ultra runs on Mac.
- Official [social page](https://www.ambeteco.com/social-media) links the [company GitHub organization](https://github.com/ambeteco). An official **product source repository is not verified**. Do not invent one or interpret the organization as product source availability.
- [Changelog](https://www.ambeteco.com/4-Organizer-Ultra/changelog/) leads with **5.2, Major Stable Release**, but is undated. This is a documented version, not a verified current MSI/Store build. Public [download page](https://www.ambeteco.com/4-Organizer-Ultra/download/) exposes an MSI link; installer bytes/signature and operation were not checked. No evidence warrants a dead-product skip.

## Reused discovery evidence

First reused `docs/content/verification/batch-2.json`, including its saved official response rather than refetching the homepage. Both raw file SHA-256 values were independently checked and match the batch ledger:

- About-page URL: <https://alternativeto.net/software/4-organizer-ultra/about/>; captured `2026-10-21T19:06:51.211Z`; raw `docs/content/.runtime/verification-2/4-organizer-ultra-directory.json`; SHA-256 `de8675e490a32f952646311540a678e74cb3aec90c3c97cd525b37ff9526d59f`.
- Official homepage captured `2026-10-21T19:09:51.260952+00:00`; raw `docs/content/.runtime/verification-2/4-organizer-ultra-official.json`; byte SHA-256 `108bf5dab07f2ef1194bd43a7b702fb7d05dd175d9a14c323368032f696f2123`. Its embedded hash is not the file-byte hash; use the independently verified ledger hash above.
- Discovery edge from `competitors.json`: CleanMyMac seed → <https://alternativeto.net/software/cleanmymac/?p=3>, captured `2026-10-21T18:36:26.872Z`. AlternativeTo proves discovery, not feature absence or comparative quality.

## Claim-ledger summary

Each C-ID maps to exact supporting excerpts and URLs in `research.json`. Documentary claims are not product tests.

| Claim | Supported wording and limits |
| --- | --- |
| C01–C02 | Windows 11/10 x64; top documented changelog version 5.2. Exact installed/downloaded build unknown. |
| C03 | [Pricing](https://www.ambeteco.com/4-Organizer-Ultra/pricing/) displays **USD $5.99/one month, $19.99/one year, $49.70/Forever**, one machine. Forever is a limited-time sale, not a perpetual quoted price. Geographic pricing and checkout tax may apply. The year link contains a 360-day parameter: do not assert 365 days or auto-renewal. |
| C04–C05 | [EULA](https://www.ambeteco.com/4-Organizer-Ultra/terms/) is proprietary, non-transferable personal-device licensing; business devices require a custom business licence. [Guide](https://www.ambeteco.com/article/4-Organizer-Ultra/quickstart) describes an Ambeteco activation account and active licence. No activation tested. |
| C06 | Guide documents sorting destination previews, folder selection and sorting rollbacks. Deep Scan offers per-file review with Auto-mode off, versus automatic deletion with it on. Sorting rollback is not deleted-file recovery; changed/missing files can be unavailable. |
| C07 | Auto Scan presets and Resource AI are documented background features. This does not establish recurring-growth attribution or process/helper grouping. |
| C08–C09 | EULA defines AI as a mixture of algorithms, neural networks and/or other technologies; discloses possible identifiers, paths and behavioral data collection. Exact network behavior unknown. Its test drive is explicitly “non-real, imaginary, artistic” and cannot support test or savings claims. |
| C10–C12 | Breathing Room capability register plus rechecked README/config support Mac storage investigation and grouped observations, not file-sorting parity. Preview and hosted-service caveats below are mandatory. |
| C13 | [Website terms](https://www.ambeteco.com/terms) reserve rights and prohibit republishing/copying artwork without permission. No permission established. |

**Conflict handling:** [Support](https://www.ambeteco.com/4-Organizer-Ultra/support/) claims file deletion is technically impossible, while guide/changelog describe Deep Scan deletion. Exclude the absolute safety promise; attribute actual documented modes and do not certify safety. Vendor “58% faster,” secure-erasure and other superiority claims are not our measurements.

## Product matrix and truthful trade-offs

Ultra has documented **file sorting**, destination previews, folder schemes, sorting rollbacks and configurable manual/automatic maintenance. Those are real decision advantages for a Windows file-organization workflow, not reasons to pretend all maintenance apps are equivalent. Forever licensing is an advertised option, subject to licence and sale conditions.

Breathing Room, **which we build**, is relevant to a Mac user who wants to explore categories, apps/tools, projects and large files, inspect grouped CPU/memory, or investigate sampled storage changes. Its documented cleanup architecture reviews locations/methods and can reuse saved exact daily approvals. Do not describe it as a general automatic file sorter or a Windows replacement. Unknown competitor helper grouping, developer-specific adapters and growth attribution remain **not verified**, never “No.”

Breathing Room limitations, reused from the current capability evidence and cross-checked locally:

- Identified release/source config: `0.1.0-preview.1`, macOS 13+, universal Apple Silicon/Intel advertised, physical Intel runtime untested. Preview is not notarized; no recommendation to disable protections.
- Python 3.10+ is required for disk inventory/legacy scripts and is not bundled. Permissions can yield partial inventory.
- Free local core; optional advertised AI Care **$5 USD/month or $50 USD/year**. Local inspection differs from authenticated hosted assistance, which can send relevant paths/process/storage information. No all-offline AI or unlimited-use promise; backend entitlements/allowances unverified.
- Daily care requires the app to remain running and saved exact approvals. Optional automatic verified Ruff-cache mode prevents unconditional “never deletes without asking” wording.
- Size, Trash movement and available-space change are different measurements. Sampled activity is not a complete audit or proof of a file's writer. Code/documentation is not binary/runtime parity.

## Visual manifest and blocking diagnostic

### Competitor: source links only, not cleared for publication

Owned browser tab 180 observed an actual official guide app-image URL and its natural dimensions:

- Source: <https://www.ambeteco.com/4-Organizer-Ultra/quickstart/>.
- Asset: <https://www.ambeteco.com/static/blog/quickstart/forg_ultra/ru/onboarding_welcome_landing.webp>, **1280 × 701**.
- View: onboarding/welcome, Russian locale. Browser followed the guide link to a Russian-localized page; no locale/account settings or cookies were read/changed. English factual guide text came from WebFetch.
- Vendor capture date/build/capturer: **unknown**. No file downloaded, hash generated, privacy/pixel review or editing claimed. This is not our app test.
- Caption/alt proposal: “Official 4-Organizer Ultra onboarding illustration from Ambeteco's quickstart guide, Russian locale. Vendor-provided app image, version/capture date unknown; not our hands-on test.” / “Official 4-Organizer Ultra onboarding image linked from the Russian quickstart guide.”
- Additional source candidate: download page's app-window slice <https://www.ambeteco.com/static/software/forg_ultra/download/1000.webp>, **1468 × 764**. This is a composite marketing slice, not approved as a useful standalone UI image.

**B01:** Official website terms say “Republish material from Ambeteco” and “Reproduce, duplicate or copy material from Ambeteco” under “You must not.” Public access is not a licence. Research keeps attributed links only; **no download, hotlink, public embed or reuse clearance**. Link fallback does not waive the required on-page competitor image gate.

**Unblock:** separately authorized reuse permission or an explicitly approved documented alternative policy basis, preferably for an English sorting/manual-review view. Then retain original bytes/hash, exact source, unknown capture/build labels, privacy review, caption/alt and independent visual review. This job may not send permission requests. Do not replace it with generated UI or a landing-page screenshot.

### Selected Breathing Room preview

Reuse `docs/content/assets/breathing-room/space-preview-2026-10-21.png` from `screenshots.json` (`current-space-browser-preview`), **2940 × 3468**, captured `2026-10-21T19:06:45.416416+00:00`, source commit `54828ac3170b45861aee70861dd0b9c658ed7e51`. Opened and inspected actual PNG this run; byte hash confirmed:

`9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a`

Required caption: **“Current-source Breathing Room Space browser preview, captured October 21, 2026. Example data only; not a native scan, measured activity or cleanup result.”**

Alt: “Breathing Room Space browser preview showing example storage categories, with its example-data banner visible.” Keep the warning visible. First-party owner-requested capture, not blanket rights to third-party marks. Source-current at capture, not a freshly tested native release. Floating assistant obscures some chart content: later contextual rendering must remain readable. No derivative or website copy created here.

## Conditional workflow article brief

**Title:** Moving from Windows to Mac: separate file sorting from cleanup  
**Slug:** `windows-to-mac-file-sorting-versus-cleanup`  
**Track:** search/reference. **Intent:** help a former Ultra user distinguish rearranging originals, removing selected disposable data and investigating recurring growth after changing platform.

1. Lead with the three different jobs; arranging files does not itself demonstrate reclaimed storage.
2. Inventory first and preserve backups/project/media relationships. Large does not mean disposable.
3. Explain documented Windows sorting preview, exclusions and rollback limits without a fictional Mac installation or first-person test.
4. On Mac, inspect categories and ownership before cleanup; explain size versus Trash versus free-space measurements.
5. Offer a non-mutating three-job decision checklist. Disclose Breathing Room affiliation once, with preview/Python/notarization/hosted-data limits and no sorting-parity claim.

Use the Space example-data image directly after the lead; add a permission-cleared real competitor sorting/review view later. Built-in Mac procedural alternatives require specific Apple sources before drafting those steps. No forced code demo, fake calculator savings or extra alternatives doorway page.

## Concise comparison brief

**Title:** 4-Organizer Ultra and Breathing Room: Windows care or Mac inspection?  
**Comparison slug:** `4-organizer-ultra`.

Platform-first conclusion, then a compact matrix: platform/version; sorting versus inspection; manual/automatic modes; account/hosted boundary; conditional personal/business pricing; install/runtime caveats. Link to the distinct workflow article and `/comparisons/` only after those routes are available. Do not expand the same matrix into a second article or claim route validation.

For a reader remaining on Windows who needs file sorting, Ultra's documented preview/rollback workflow is relevant. For a reader now using Mac who needs storage investigation, Breathing Room may fit, bounded by the preview caveats. There is no cross-platform head-to-head benchmark here.

## Unknowns and validation

Noncritical unknowns remain explicitly marked: current binary version/signature, dated release history, product repository, final regional checkout/renewal terms, exact AI/network behavior, helper grouping/developer adapters, and any performance/savings results. These need not become invented cells. The **critical** missing item is cleared competitor-app imagery, so drafting remains blocked.

Actual checks: read required programme files and relevant blog/browser contracts; no applicable `AGENTS.md` found in checked ancestor paths or docs tree. Reused baseline and verified its two file hashes. Retrieved only missing official evidence listed above. Browser used an owned tab without touching pre-existing tabs or restarting a profile. Selected PNG was opened and inspected, not inferred from its dimensions. JSON/schema/reference checks are retained in `validation.json` after execution.

No app installation, native test, cleanup, account, message, purchase, credential access, commit, push, deployment, queue change, website edit, site build or independent review was performed. No quality score is awarded by this research job.
