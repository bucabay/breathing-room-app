# MacCare research — drafting blocked

Research date: 2026-10-22. Job: `research-maccare--mac-cleaner`. Research only; no article, installation, cleanup, purchase or publication. See `research.json` for claim-level excerpts, conditions and provenance.

## Identity and decision

**MacCare**, by Martin Wiederhold, is the product at https://www.getmaccare.com/. The AlternativeTo label is **MacCare - Mac Cleaner**. Canonical owner: `maccare--mac-cleaner`; retain as a distinct product, not an alias skip. There is no evidence connecting it to PowerMyMac. Do not merge on the basis of generic Mac-cleaner wording. The official homepage links MartinWiederhold's `maccare-releases` distribution repository. Its public release API confirms **v1.7.2**, published July 19, 2026; this is the homepage-linked version, not a claim that every release channel has been checked.

Fit: direct **Mac storage-cleanup** overlap, not identical maintenance coverage. Official requirements say macOS 14+, Intel and Apple Silicon. No Windows support is asserted. Exact software licence terms are unverified; AlternativeTo labels it proprietary, but the releases repository is not evidence of an open-source app licence.

## Reused evidence first

Reused the October 21 `batch-1.json` record and retained official/directory snapshots, rather than repeating verified feature/platform/pricing research. Discovery came from CleanMyMac alternatives page 7 at `https://alternativeto.net/software/cleanmymac/?p=7`, retrieved 2026-10-21T18:36:45.366Z. The exact product listing was retained at 19:08:37.316Z and official page at 19:09:32.409119+00:00. Owned copies and SHA-256 hashes are in the JSON ledger. The official HTML was additionally inspected only to resolve missing visual/rights/licence and currency evidence. Its “MACBOOK MOCKUP” / “ANIMATED APP SCREENS” are HTML/CSS, not native captures.

New evidence: official release metadata supplies version-specific automatic-cleanup boundaries; an owned browser tab exposed four real listing screenshot URLs. WebFetch of the listing returned HTTP 403; the ordinary browser loaded it without account interaction or challenge bypass. No cookies or hidden application state were read.

## Facts, conditions and limits

- Vendor documents eight scan categories, a TreeMap, app-remnant uninstaller, startup controls and a disk-space menu-bar indicator. These are vendor-documented features, not our execution results.
- Audio Producer Mode is documented for DAW-related plugins, presets, libraries and caches. Do not repeat “total protection,” “no other cleaner,” guaranteed safety, 20 GB recovery, speedups or two-minute results.
- Important approval distinction: homepage says safe files are cleaned instantly, then suggestions reviewed. v1.7.2 release notes restrict automatic Step 1 to caches, logs and build artifacts in the user's home folder; media/documents/music, Trash and Mail attachments are excluded from automatic cleanup. Step 2 asks Keep/Delete per item. These are release disclosures, not tested guarantees.
- Advertised Pro: **$29/year**, seven-day trial, cancel anytime; Lifetime: **$69 once**, advertised all features and future updates. Homepage structured offer identifies USD; currency of the lifetime checkout, taxes, device seats, refunds, renewal mechanics and post-trial limits are not independently verified. No payment flow was opened. Never convert the directory's rounded “$2/month” into a purchasable monthly plan or assert a permanent free tier.
- Apple notarization is a vendor assertion (also in v1.7.2 notes), not binary inspection. No installer downloaded. Network/activation needs, data collection, runtime dependencies, grouped process monitoring and recurring-growth diagnosis are not verified. Activity Log is not proof of process attribution.
- Release API reports installer size 3,075,995 bytes whereas homepage advertises 1.3 MB: omit installer-size recommendations until reconciled. This does not establish a malicious or broken installer.

## Visuals and blocker

Listing source: https://alternativeto.net/software/maccare--mac-cleaner/about/ . Cleanup screenshot asset: https://img.alternativeto.net/s/618x394/avif/maccare--mac-cleaner_321715_full.png . Listing describes it as “Cleanup view with color-coded risk classification per item (green = safe).” Preserve this as attributed listing metadata, not an independently verified safety label. Other dashboard/scanning/results asset URLs are in JSON. Product version and original capture date are unknown. No permission or licence for republication was established. **Link-only; no competitor image downloaded or republished.** The real screenshot requirement remains blocked pending documented reuse permission or explicit approved policy decision, plus visual/privacy inspection of the permitted original. Do not substitute a capture of the landing-page mockup.

Selected first-party visual: `current-assistant-review-browser-preview`, captured October 21, from the existing screenshot library. Required caption: **Current-source Breathing Room Assistant plan review browser preview, captured October 21, 2026. Example data only; not a native scan, measured activity or cleanup result.** Keep its visible interactive-preview/no-inspection disclosure; this focused view hides the global banner. Hash verification and a fresh read of the actual PNG are recorded in validation; this is not current native testing or binary parity verification.

## Distinct workflow article brief (held, not drafted)

- Track: search/reference. Proposed title: **Review Mac cleanup without treating audio caches as disposable**.
- Proposed slug: `review-mac-cleanup-audio-project-caches`; primary intent: distinguish project originals, sample libraries, plugin state and rebuildable caches before approving maintenance on a music-production Mac.
- Lead direction: choose what must be preserved before choosing a cleaner. Audio Producer Mode is a documented MacCare option, not proof every DAW setup is protected.
- Outline: inventory originals and backups; distinguish regenerable cache from plugin/sample state; explain MacCare's documented two-phase model and v1.7.2 exclusions; contrast exact-path/method review in Breathing Room; leave uncertain items untouched; verify projects after any reader-authorized future maintenance without promising recovery.
- No tested DAW walkthrough, deletion commands or savings figures. Additional primary documentation is needed for any DAW-specific rebuild advice. Prefer a manual inventory/leave-untouched checklist over forced code.
- Interaction handoff: a non-executing decision aid asks “original or rebuildable?”, “backup verified?”, “owning application guidance available?”, “exact path/method understood?”; unknown answers mean stop, not permission to clean. No filesystem access, upload or auto-selection.
- Top visual: rights-cleared MacCare cleanup screenshot when available; later figure: labeled Breathing Room review example. Internal links planned, not verified existing routes: `/comparisons/`, `/comparisons/maccare--mac-cleaner/`, and a genuinely relevant future cache checklist only when available.

## Concise comparison brief (held)

Proposed title: **Breathing Room vs MacCare: review scope and audio-workflow boundaries**. Proposed route: `/comparisons/maccare--mac-cleaner/`. Answer the direct Mac-cleanup choice with a small claim-linked table: OS/version; documented scan/review model; audio-specific claims; monitoring scope; local/hosted boundary; price/trial; install caveats. Unknown cells read “not verified,” never “No.” Link the workflow article rather than expanding the table into duplicate prose.

**MacCare may fit** readers seeking the documented audio-focused exclusions, app-remnant removal or startup management, provided they verify suitability for their own setup. Those capabilities are not established as equivalent Breathing Room features. Trade-offs: MacCare's automatic safe-cleanup phase is not item-by-item approval for everything; actual protection and privacy behavior have not been tested here.

**Breathing Room, which we build, may fit** readers interested in source-visible exact-location/method cleanup review, developer-cache investigation and grouped CPU/memory/activity views. Evidence is the October 21 capabilities register, not new runtime testing. It is a macOS 13+ preview (`0.1.0-preview.1` identified), Apple Development signed but not Developer ID signed/notarized, requiring Python 3.10+ for inventory; physical Intel and clean-machine validation are incomplete. Free local inspection is distinct from authenticated internet/hosted AI and optional advertised AI Care ($5 USD/month or $50 USD/year). Hosted requests can include paths/process/storage data. Daily care requires the app running and saved exact approvals. Optional automatic verified Ruff-cache Trash mode prevents blanket “always asks for every action” wording. No certified equivalent DAW protection, general uninstaller or startup optimiser was established. No “safer,” “best,” or price-winner verdict.

## Handoff

**Do not draft yet:** competitor screenshot reuse/visual review is a critical unresolved gate. Licence terms, checkout conditions and optional feature details may remain explicitly unknown in a bounded packet; they cannot be turned into unsupported negative facts. Independent review and rendered site QA are future gates, not performed work. No website files, shared manifests, queue/database, PLAN or other competitor directories were changed by this job.
