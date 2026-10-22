# Mint (DZG Studio): research handoff

**Blocked for drafting: competitor screenshot reuse is unresolved.** This is a distinct, relevant Mac product, not a dead listing or a verified alias of another competitor. No article or site content was created.

## Identity and fit

- Canonical owner: `mint-dzg-studio-`; official product **Mint**, publisher **DZG Studio LLC**. [Official terms](https://mintstorage.app/terms), section 15: “Mint is published by DZG Studio LLC.”
- Homepage: <https://mintstorage.app/>. Reused the October 21 batch-1 verification rather than repeating homepage/pricing/discovery fetches.
- App Store names “Mint: File Organizer & Cleaner” and “Mint: Disk Cleaner & Organizer” resolve to app ID `6762415711` with the same publisher. Keep one canonical packet; skip separate alias drafts. No evidence links Mint to PowerMyMac.
- Official download page links <https://github.com/dzg-studio/mint-releases/releases> and a `v1.1.1` DMG. This establishes a vendor-linked release repository, **not** an open-source repository or a tested download.
- Direct overlap: Mac disk exploration, cleanup and developer-cache review. Adjacent strengths: folder organization and identical-file storage optimization. Do not imply feature equivalence or Windows support.

## Evidence and edition boundaries

The machine-readable packet maps each claim to exact URLs, excerpts, retrieval times and retained source hashes. Source IDs below refer to `research.json`. New browser/system timestamps reported October 21 UTC despite the programme's October 22 date; the actual timestamps are preserved.

| Topic | Finding and boundary | Evidence |
| --- | --- | --- |
| Requirements | macOS 14+; publisher's download description names Apple silicon and Intel. No hardware testing. | C03 / S6; App Store also requires macOS 14.0+ |
| Observed versions | Download table: Direct **1.1.1**, Setapp **1.0.83**, App Store **1.0.84**, table dated October 18. App Store independently shows 1.0.84. | C03, C10 / S5–S6 |
| Licence | Proprietary, non-exclusive/non-transferable/revocable use licence; terms protect UI, code and related material. | C02 / S4 §8 |
| Direct free tier | Unlimited scans/memory release. From Direct 1.0.96, cleanup, Optimize, uninstall and organizing share **1 GB weekly**, Monday reset, including Auto Care; setup excluded. Current post-setup actions count from first run. | C04 / S3–S4 |
| Direct paid | **$39.99** first Mac, **$20** each additional Mac up to five; four **$9.99** payments for one-Mac Rent to Own, **$39.96 before tax**, then scheduled payments end. Includes Mint 1.x; later major upgrades may be optional separate purchases. Retained sources do not explicitly identify dollar currency code. | C05 / S3–S4 |
| Marketplaces | Separate terms. Observed App Store 1.0.84 describes unlimited manual organization and 1 GB cleanup, with paid Auto Care. Terms also describe 1.0.92 weekly allowances: do **not** assign those to the observed older listing. Regional IAP amounts/Setapp plan price unverified. | C10 / S4–S6 |
| Workflow | Four buckets: Optimizable, Safe to clean, Yours, Keep. “A scan only reads. Nothing changes until you press a button.” Vendor category names are not safety certification. | C06 / S2, S7 |
| Organization/growth | Vendor documents scheduled folder sorting while running and following storage changes over time. Do not claim Mint lacks monitoring. | C07 / S2 |
| Developer features | Edition table lists Xcode/Homebrew cleanup for Direct/Setapp, not App Store; CLI/MCP/Raycast for Direct only. | C08 / S6 |
| Privacy | Local analysis is documented, but terms also disclose version/edition-dependent usage analytics and some signals continuing with usage sharing off. No backend audit or blanket offline/privacy claim. | C09 / S4 |
| Installation | Vendor advertises notarization; no binary signature inspection performed. Direct download needs no account/card; restoring paid access uses purchase email. | C11 / S6 |
| Helper CPU/memory grouping | Mint: **not verified**, never “No.” Memory release does not prove grouping. | Matrix unknown |

### Breathing Room comparison limits

Reuse `docs/content/capabilities.md`, reviewed October 21, rather than re-fetching its current verified facts. It identifies **0.1.0-preview.1**, macOS **13+**, Python **3.10+**, a free Apache-2.0 desktop core, and advertised optional AI Care at **$5 USD/month or $50 USD/year**. Hosted AI requires authentication/internet and sends relevant tool context. The published preview is Apple Development signed, **not Developer ID signed or notarized**, and physical Intel/clean-machine validation remains incomplete.

Grouped helper activity, developer-cache discovery and approval mechanisms are **source implementations**, not certified distributed-binary tests. Saved exact Daily care approvals require the app to run. Preserve the optional narrow automatic Ruff-cache exception; do not promise every deletion always gets a new prompt. No measured savings, speed, safety or full writer-attribution claims.

## Visual handoff

1. **Mint candidate, link-only:** [App Store source](https://apps.apple.com/us/app/mint-disk-cleaner-organizer/id6762415711?mt=12). Exact image URL:

   <https://is1-ssl.mzstatic.com/image/thumb/PurpleSource211/v4/aa/93/7b/aa937b97-d99a-b203-ce92-dd6e79ab64a1/02-map.png/1286x804bb.webp>

   The listing DOM exposes this storage-map candidate. Capture date/version unknown; actual asset not downloaded or visually approved. No permitted reproduction basis established; terms §8 protects UI/materials and branding. **Do not hotlink or republish.** Public availability is not permission. A rights-cleared, opened/reviewed real UI image with provenance and original/published hashes is still required. The disk guide has HTML UI illustrations and no image elements; a guide-page screenshot would not resolve the real-app-image requirement.

2. **Selected Breathing Room view:** `docs/content/assets/breathing-room/space-preview-2026-10-21.png`, SHA-256 `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a` (actual file hash checked). Source capture commit `54828ac3170b45861aee70861dd0b9c658ed7e51`; 2940 × 3468. Reuse first-party inventory review; independent page-context review pending.

   Required caption: **“Current-source Breathing Room Space browser preview, captured October 21, 2026. Example data only; not a native scan, measured activity or cleanup result.”** Keep example banner visible. Alt: “Breathing Room Space view rendered in a browser with illustrative example data.” Current-source refers to that capture, not newly tested native UI.

## Distinct workflow article brief — blocked proposal

**Title:** Before cleaning an AI workspace: separate rebuildable files from session history  
**Proposed slug:** `review-ai-workspace-files-before-cleanup`  
**Intent:** Help Mac developers decide what needs review, not provide a deletion recipe or expand a comparison matrix into filler. Search/reference track.

Conclusion: old worktrees and agent context should not be treated as disposable solely because code is tracked in Git. Outline:

1. Identify ownership and active project/session context without running cleanup.
2. Explain Mint's four documented buckets as attributed classifications.
3. Separate build output, caches, worktrees and session history.
4. Check reproducibility, backup and exact action before any approval.
5. Choose folder/optimization tooling versus app-activity investigation by the reader's actual job.

Before concrete Git/session-loss mechanisms or executable advice, obtain relevant official tool documentation; current evidence supports Mint's attributed rationale only. Do not fabricate hands-on experience. Hand off a useful non-mutating checklist: owner known → in use → reproducible → backup → exact action understood. Unknown means stop/review. No filesystem access, arbitrary demo repository or claimed recovered bytes.

Place a cleared Mint screenshot after the lead; place the labeled Breathing Room Space example later beside its alternate investigation workflow. Link the comparisons hub, concise Mint comparison and a genuinely relevant tools page after checking actual routes at drafting time. Recommendation must say **“Breathing Room, which we build.”**

## Concise comparison brief — blocked proposal

**Title:** Breathing Room vs Mint: storage review or file organization?  
**Proposed route:** `/comparisons/mint-dzg-studio-/`

Start with the decision, then a short sourced edition/version matrix, strengths and installation/privacy caveats. Link the deeper workspace-review article instead of duplicating its steps.

- **Mint advantages:** documented organization templates, identical-file optimization, Direct CLI/MCP/Raycast and Direct/Setapp developer-cache workflows. Vendor advertises notarization, unlike Breathing Room's disclosed non-notarized preview; this is not our comparative binary test.
- **Breathing Room fit:** source-implemented grouped app/helper investigation and sampled activity, with explicit preview/hosted AI/runtime limits. Mint grouping is unknown, not absent. Avoid unsupported “cheaper,” “safer,” “faster” or “all offline” conclusions.
- **Trade-offs:** Mint has proprietary terms and edition/version-specific allowances. Breathing Room's code and example UI are not proof of native reliability, complete inventories or released feature parity. Neither packet supplies a storage-savings benchmark.

## Validation and precise unblock requirement

Reused three baseline snapshots and existing capability/screenshot registers. New public browser DOM snapshots retained under `sources/` for disk guide, terms, download editions and App Store. Ordinary Python HTTP retrieval returned 403; no bypass attempted. Existing Chrome worked; only owned tab 142 was read/navigated and then closed. No recovery, cookie extraction, installation, sign-in or cleanup.

Actual structural/hash/excerpt checks are retained in `validation.json`. No site changes, so no site build/tests or responsive publication review were run. Independent review and all publication gates remain pending.

**Blocker VISUAL-RIGHTS:** establish an authorized screenshot reuse basis, then inspect the real image and retain its provenance/hashes before drafting. No permission messages were sent. Noncritical unknowns (currency code, source repo, helper grouping, Setapp exact price) must remain unknown or be omitted; they must not become unsupported negative cells.
