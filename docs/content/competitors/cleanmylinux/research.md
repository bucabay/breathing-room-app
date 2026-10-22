# CleanMyLinux research handoff

**Research complete within the bounded Mac-transition intent. Not publication approval.** Task `research-cleanmylinux`. Actual new source retrievals occurred October 21, 2026 UTC (October 22 local scheduled date); exact timestamps and hashes are in `research.json` and `sources/manifest.json`.

## Decision and identity

CleanMyLinux is **Better Linux's Linux-specific desktop app**, not a native Mac alternative. Canonical owner ID: `cleanmylinux`. Official homepage: <https://www.cleanmylinux.com/>; repository: <https://github.com/Better-Linux/CleanMyLinux>. The site's repository links and repository's homepage link establish the identity. No alternate product alias was verified. **Do not skip as an alias**, and do not conflate it with CleanMyMac or PowerMyMac merely because the names resemble each other.

Classification: **adjacent, platform-specific**. Retain only a Linux-to-Mac replacement intent. Do not suggest Breathing Room runs on Linux or Windows, or CleanMyLinux runs on macOS or Windows. No evidence of death or irrelevance to this narrowly framed transition was found; no skip is recommended. Search demand for the proposed intent has not been measured. This is an editorial brief, not proof that a standalone page earns publication.

## Reused discovery and baseline evidence

Read `PLAN.md`, `EDITORIAL.md`, `capabilities.md`, `screenshots.json` and the MailKite contract before producing this packet. No applicable `AGENTS.md` was found in the app tree or checked ancestors. Blog and browser-automation skills were loaded; no live browser session was needed.

Reused `docs/content/verification/batch-2.json#cleanmylinux` rather than refetching its current homepage facts. Retained exact copies in `sources/baseline-record.json`, `sources/baseline-official.json` and `sources/baseline-directory.json`. The original official/directory capture byte hashes match the batch register. The official capture's embedded `sha256` is not its whole-file hash; the packet uses the batch's verified whole-file hash.

Discovery: <https://alternativeto.net/software/cleanmylinux/about/>, retrieved `2026-10-21T19:07:32.207Z`, from an owned baseline browser tab. Earlier listing traversal found it on CleanMyMac page 4 and Mole page 3; exact edge URLs/times are retained in `research.json`. The directory proves discovery and official destination, not capabilities or price. Its “Free” label is not used as an official commercial offer.

## Verified claims and boundaries

`research.json` holds the claim ledger: exact proposed wording, source URLs, excerpts/locators, actual check times, evidence class and conditions. Source bytes and SHA-256 values are retained. Key evidence:

| Topic | Evidence and permitted wording |
| --- | --- |
| Identity/platform | Baseline homepage: “designed exclusively for modern Linux desktops.” Its links identify Better-Linux/CleanMyLinux. Claims `identity`, `platform`. |
| App workflow | Pinned README Phase 2 documents app discovery, per-app usage analysis, uninstall and reset. Treat as current documentation, not beta-binary parity or hands-on results. Claim `apps`. |
| Updates/privileges | README documents APT, Pacman, DNF, Flatpak and Snap, an unprivileged GUI and PolicyKit for admin tasks. This is not evidence of exact-path cleanup approval or universal safety. Claims `updates`, `auth`. |
| Cleanup/roadmap | Homepage advertises cache/reset/update functions; README puts junk cleaner in Current Focus, disk analysis and monitoring in later phases. Do not flatten this into “all shipped” or “not supported.” Claims `scope`, `roadmap`. |
| Version/downloads | GitHub latest-release metadata returns **v1.0.0-beta.2**, published **2026-05-25T05:19:04Z**, with x86_64 RPM and amd64 DEB/AppImage assets. API `prerelease:false` does not erase the beta version name. No executable was downloaded or tested. Claims `version`, `downloads`. |
| Licence/price | MIT grants free-of-charge software/documentation permission with copyright and permission notices retained. Public release download URLs are verified. **No official commercial amount, billing, paid support, hosted offer or guarantee was verified.** Do not turn “premium” into a price, or the licence into a lifetime $0 service promise. Claims `license`, `pricing`. |
| Minimum Linux versions | **Unresolved:** README lists Ubuntu 22.04/Debian 12 and other minimums but warns binaries require GLIBC 2.39. Arch is marked untested. Do not recommend exact minimum distro versions. Claim `compatibility-conflict`. |

Official current-source README: <https://github.com/Better-Linux/CleanMyLinux/blob/02de64d1168e06820a4e280971b49175bdc31307/README.md>. Licence at the same commit: `LICENSE`. Release: <https://github.com/Better-Linux/CleanMyLinux/releases/tag/v1.0.0-beta.2>. Release metadata and current main documentation are distinct scopes. No feature was executed or benchmarked.

### Breathing Room cross-check

Reused same-day public release, pricing and privacy evidence in `capabilities.md`; reread current local README, native config, billing config and automatic-mode UI. Retained local source copies with hashes. Current config still identifies **0.1.0-preview.1**; source is not certification of the distributed binary.

- macOS **13+**, Apple Silicon/Intel universal advertised; physical Intel and clean-machine runtime validation remain unverified. Python **3.10+** is required for inventory/legacy scripts and is not bundled. Non-notarized preview; never advise disabling Gatekeeper.
- Free local core; advertised optional AI Care **$5 USD/month or $50 USD/year**, recurring until cancelled, applicable tax at checkout. No separate app purchase or unlimited-AI promise. Do not interpret legacy `appAmount` as a current purchase price.
- Hosted agent workflows require sign-in/internet and may send relevant paths, inventory/process data and tool outputs to the service. Not all-local AI. Website download has an account gate; public GitHub releases are separate.
- Ordinary review/approval is qualified by optional automatic verified Ruff-cache moves. Scheduled care reuses exact prior approvals and requires the app to remain running. File sizes, Trash moves and newly available space are different measurements.
- Space, grouped Apps and Activity are documented/source-level workflows, not new runtime observations. Sample I/O/ownership is not a forensic writer audit. No native test was performed.

## Visuals and rights

### CleanMyLinux Applications start screen

- Official source page: pinned README Preview section above.
- Original asset: <https://raw.githubusercontent.com/Better-Linux/CleanMyLinux/02de64d1168e06820a4e280971b49175bdc31307/public/image.png>.
- Download: `assets/cleanmylinux-official-preview.png`, **1194×797**, SHA-256 `91146332b2b472ee548644c36add50181379375f0c4be360488f99e7fa858104`. Exact retrieval time: `sources/visual-download.json`.
- Reuse basis: repository-associated README documentation image under root MIT licence; no separate image licence was found in the repository tree. Preserve the complete `sources/LICENSE` copyright and permission notice with reproduced documentation. Credit **CleanMyLinux / Better Linux, Copyright (c) 2026 Better Linux, MIT License**. No trademark endorsement inferred; independent publication review still required.
- Opened/read the actual PNG: Applications title, app-management description, Scan button, sidebar and settings; no scan results, account names or personal file data. This is app UI, not a landing page. Vendor capture date, OS and exact app version are unknown. Repository commit pins the asset, not the running app's version. Generic window controls do not establish Windows support.
- Caption: “CleanMyLinux official repository preview of the Applications screen. Vendor-provided image; app version, capture date and OS are not supplied. No scan or cleanup was performed for this article.”
- Alt: “CleanMyLinux Applications start screen with app-management description and a Scan button.”
- Original bytes preserved; no edits, crops or published derivative. Published path/hash are null because nothing was published.

### Breathing Room Space view

Selected `current-space-browser-preview` from `docs/content/screenshots.json`, source `docs/content/assets/breathing-room/space-preview-2026-10-21.png`. SHA-256 **9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a**, **2940×3468**. Recomputed hash matches. Opened/read actual PNG: both the example-data label and no-Mac-changes banner are visible. First-party owner-authorized capture; third-party marks are not endorsed. Source commit/capture timestamp and reuse basis are in `research.json`.

Required caption: **“Current-source Breathing Room Space browser preview, captured October 21, 2026. Example data only; not a native scan, measured activity or cleanup result.”** Alt: “Breathing Room Space view rendered in a browser with illustrative example data.” Preserve visible disclosure labels. This is not current native or distributed-release evidence. The full-height image needs a readable contextual layout; any crop must retain disclosures and record new hashes. No shared image was changed or duplicated.

## Distinct workflow article brief

**Proposed title:** Moving from Linux app cleanup to Mac storage review  
**Slug:** `linux-app-cleanup-to-mac-storage-review`  
**Track:** search/reference; primary reader is a CleanMyLinux user moving to a Mac.

Conclusion: choose by OS and job. CleanMyLinux's Linux app/package workflow is not interchangeable with a Mac storage/process investigator. Open with that boundary and the official Applications visual, rather than a claim that one product wins.

1. Separate uninstalling a package, resetting an app's local state, discarding rebuildable cache and removing original work.
2. Explain which job the documented Linux workflow addresses, attributing claims to the README.
3. On the Mac, inventory before making changes; distinguish projects, app data and caches, including rebuild/download costs. No Linux cleanup commands copied to macOS.
4. Show the current-source Space example view, then explain partial inventory and measurement limits.
5. One bounded recommendation: “Breathing Room, which we build,” may fit Mac investigation, with preview/Python/hosted/paid boundaries; it is not a claimed replacement for Linux package updating or a verified full app uninstaller.

Interaction handoff: a non-destructive decision checklist **target OS → package management or storage investigation → original/rebuildable data → permissions, backup and rebuild cost → review**. No deletion controls, made-up recovered-space figures, forced demo repository or signup arc. Length is earned; do not pad to an article-count target.

## Concise comparison brief

**Proposed title:** CleanMyLinux vs Breathing Room: Linux and Mac roles  
**Comparison slug:** `cleanmylinux`

Short OS-first conclusion, then the claim-linked matrix in `research.json`: platforms, licence, local/hosted boundary, app scan/cleanup model, approvals, helper grouping, recurring growth, developer caches, pricing and installation caveats. Unknown competitor capabilities remain **not verified**, never negative checkmarks. Include both real product visuals and source credits, link the deeper transition article and `/comparisons/`, and verify all final routes before use. No additional alternatives doorway page.

Honest advantages: CleanMyLinux documents Linux-native app/package workflows across multiple formats and publishes MIT source/public beta assets. Breathing Room documents Mac storage/process/activity investigation with a free local core. Trade-offs: different platforms/jobs; beta/preview and source-vs-binary uncertainty; unresolved Linux compatibility minimums; Mac Python/notarization/hosted-AI and optional subscription constraints. No relative speed, safety, savings or price-superiority assertion is supported.

## Gates, unknowns and handoff

No critical evidence is missing **for the bounded transition brief**: identity/platform fit, source-level workflow, exact release metadata, qualified price/unknown terms and authentic reusable visual sources are retained. **Block any Linux installation guide or exact minimum-compatibility recommendation** until the distro/GLIBC contradiction is resolved with version-specific official evidence and permitted testing. Likewise block any proposed runtime, all-offline, stable-release, feature-parity or measured-savings assertion absent new evidence. Commercial terms, ARM, screenshot capture metadata and full network behavior remain noncritical unknowns because the brief does not rely on them.

Research completeness does not pass drafting/publication QA: independent fact/rights review, responsive/theme rendering, route checks and changed-site check/build/test remain later-stage requirements. No article or site record was edited. No browser cookies, credentials, signups, purchases, messages, cleanup, executable downloads, installs, commits, pushes or deployments occurred. Queue/database state was not changed.

Validation results are retained in `validation.json`. All owned artifacts are under this folder, apart from the required attempt-specific runtime receipt.
