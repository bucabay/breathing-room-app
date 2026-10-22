# CCleaner Cloud (Agomo): research decision

**Complete research with an explicit skip. Do not draft standalone Mac-alternative pages.** CCleaner Cloud is documented Windows-fleet management, not a Mac cleaner. Its browser console being usable from other operating systems is not evidence of a Mac endpoint agent. This record does not count toward the distinct-article target. No marketing files or shared records changed.

Checked using the actual UTC clock on **2026-10-21**; current baseline evidence was retrieved earlier that day and reused without resetting its dates. `research.json` contains the claim ledger, exact excerpts, URLs, conditions and unknowns.

## Identity and aliases

- Official name/homepage: **CCleaner Cloud**, https://www.ccleanercloud.com/ (`C01`, inherited `S01`). Footer identifies Gen Digital Inc.
- Official company history verifies **Agomo → CCleaner Cloud**, September 2015 (`C07`, `S02`). Requested https://www.ccleaner.com/about; browser landed at https://www.ccleaner.com/ru-ru/about. Original Cyrillic text retained in `sources/official-history.json`; normalized excerpt and English translation in the claim ledger. WebFetch 403 and browser navigation timeout are recorded honestly; subsequent DOM inspection confirmed readable official history.
- `canonicalOwnerId: agomo`. **Skip separate Agomo/CCleaner Cloud drafts as aliases of one product.** CCleaner for Mac, CCleaner desktop and Cloud Drive Cleaner must not be conflated with this cloud-management product. No official repository established; no source licence assumed. No evidence ties this identity to PowerMyMac.

## Discovery and reused evidence

Reused `docs/content/verification/batch-2.json` and its existing raw captures first. Discovery: https://alternativeto.net/software/agomo/about/, retrieved 2026-10-21T19:07:19.971Z, linking the official homepage. The manifest records the Mole edge https://alternativeto.net/software/mole/?p=5 at 2026-10-21T18:37:15.718Z. Exact raw paths/hashes are in `research.json`. The directory supports discovery only.

The retained official homepage text from 2026-10-21T19:09:57.079271+00:00 documents these facts; no account, endpoint or cleanup was tested:

| Dimension | Evidence-backed finding |
| --- | --- |
| Fit | Adjacent Windows fleet-management service; excluded from a standalone Mac-replacement article (`C02–C04`). |
| Platform | “Currently, CCleaner Cloud supports only Windows OS.” Browser-console support across OSs is separate (`C03`). |
| Deployment | Install Cloud Agent on each managed computer; organize groups and perform tasks through cloud console (`C04`). |
| Audience | Vendor describes businesses managing more than five Windows PCs. This is positioning, not a verified minimum purchase or technical seat count (`C04`). |
| Cleanup | Vendor describes scheduled temp/cache/cookie deletion and Windows registry scan/repair (`C09`); no independent results or recommendation to execute registry changes. |
| Administration | Remote install/uninstall, hardware/software inventory, event logging, alerts and reports documented (`C08`), not tested. |
| Approval/helper/cache specifics | Exact approvals, rollback, process/helper grouping, specific developer caches and recurring folder-growth attribution **not verified**. Generic inventory/cache claims are insufficient. |
| Pricing | Monthly/annual per-PC subscription labels and 14-day no-credit-card trial advertised (`C05`). Exact numeric amount, currency, tax, minimum seats, renewal and plan limits unknown. Hidden/public-script price defaults are not verified displayed offers. |
| Requirements/version | **Conflicting** official minimums: “Windows 7 and later” versus “after Windows 10 or Server 2016” (`C06`). No current agent version established; do not treat CDN resource version as agent version. |
| Availability/licence | Public product offer and visual reachable; service, activation and download execution untested. Exact software licence terms/repository not established. |

The Windows minimum conflict does not change the Windows-only exclusion. It would block any installation guide or precise compatibility recommendation. No need to create an account or repeatedly re-fetch a current page to support this skip.

## Visual research and boundaries

**Official competitor app UI found and visually inspected:** https://s1.ccleanercloud.com/images/public/homepage/c3-home-mockup.png, linked by https://www.ccleanercloud.com/. Vendor-composed laptop mockup contains a CCleaner Cloud endpoint Summary: Windows system information, events, bandwidth and disk-space panels, not merely a landing-page screenshot. Original natural dimensions: 795 × 498. Source markup and metadata retained under `sources/`; inspected in owned browser tab 194, then closed. Unknown capture date, product version and author remain null.

**Reuse: link-only.** Public accessibility is not a licence; official footer reserves rights and no permission was established. No competitor source image saved or republished; original/published image hashes remain null rather than invented. This does **not** pass an on-page screenshot gate. Caption and alt text are provided in JSON if an independently approved route later clears rights.

**Selected Breathing Room visual:** existing `current-space-browser-preview`, `docs/content/assets/breathing-room/space-preview-2026-10-21.png`, source commit `54828ac3170b45861aee70861dd0b9c658ed7e51`. Original SHA-256 `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a`. First-party capture/provenance reused from `screenshots.json`; no copy or edit made.

Required caption: **“Current-source Breathing Room Space browser preview, captured October 21, 2026. Example data only; not a native scan, measured activity or cleanup result.”** Keep the example banner visible. This is current-source browser illustration, not current-installer parity or native testing. Independent contextual visual/privacy review remains pending; original image rights do not clear every third-party mark.

## Planning-only briefs, suppressed by the skip

### Distinct workflow article

Provisional intent: **moving from a managed Windows PC to a Mac, distinguish fleet administration from personal storage investigation**. Provisional title: “Moving from a managed Windows PC to a Mac: separate fleet tools from local storage care”; slug `windows-fleet-tools-to-mac-storage-care`.

Structure: identify endpoint OS and owner/admin responsibility; distinguish console access from agent support; choose local Mac storage inspection only for a personal maintenance task; review ownership/backup/rebuild costs before considering removal; retain approved fleet-management tooling when administration is the actual need. A local decision checklist could branch by OS, fleet need and local inspection need, without data collection or executing cleanup.

**Not commissioned:** no supported distinct migration demand/workflow justifies a product-specific page here. Do not pad this outline into an Agomo doorway. If later reconsidered, use the selected preview immediately after the lead and a cleared competitor UI later; link-only is not a waiver. Any macOS-specific instructional claims need current primary sources before drafting.

### Concise comparison

Provisional title: “CCleaner Cloud and Breathing Room: Windows fleets versus one Mac”; comparison key `agomo`. Decision-first matrix: endpoint OS versus console OS; cloud console/agent versus local Mac preview/optional hosted AI; administration versus individual inspection; price conditions and unknowns; installation/runtime limitations. This is a scope distinction, not a winner ranking. Suppress standalone route; a future directory may classify the service as Windows fleet management without suggesting a Mac substitute.

## Truthful advantages and trade-offs

CCleaner Cloud's documented grouping, scheduling, inventory, reporting and remote software management suit Windows fleet administrators (`C02`, `C04`, `C08`). Those capabilities were not tested. Windows-only endpoints and a cloud/agent deployment are not a local Mac-cleanup workflow (`C03–C04`).

Breathing Room, **which we build**, may fit individual Mac storage investigation, but the current capability register describes **0.1.0-preview.1**, macOS 13+, Python 3.10+ for inventory, Apple Development signing without Developer ID/notarization, and no clean-machine/physical-Intel certification. Source implementation is not distributed-release validation. Free local tools and advertised optional AI Care ($5 USD/month or $50 USD/year) must remain distinct from authenticated hosted AI. Daily care requires the app running and saved exact approvals; optional constrained Ruff automatic mode prevents blanket “asks before every deletion” claims. See current `capabilities.md` (`BR01–BR02`) for exact code/public source citations and limitations. No Windows-fleet replacement, benchmark, security or savings claim is made.

## Handoff and validation

Research outcome is **done with skip**, not a draft approval. Alias exclusion and platform mismatch are supported; no critical evidence is needed to manufacture a page. If drafting is reconsidered, unresolved intent, competitor-image rights, any required exact pricing/Windows minimum, and independent review remain hard gates. Noncritical unknowns are explicit rather than negative feature claims.

No site build was appropriate: no site edits, published assets, drafts or executable tutorials were created. Validation results and retained source/artifact hashes are recorded in `validation.json`; the required runtime receipt summarizes them. Browser work used only newly created tab 194 and closed it. No cleanup, signup, message, purchase, credential access, computer-setting changes, queue mutation, commit, push, deployment or subagent occurred.
