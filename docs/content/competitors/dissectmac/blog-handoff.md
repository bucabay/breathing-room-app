# DissectMac workflow blog handoff

Prepared **2026-10-22** for `draft-blog-dissectmac`. Draft remains `status: review`, `published: false`; no publication or independent review approval is implied.

## Owned outputs

- `/Users/gabe/code/breathing-room/website/src/content/blog/dissectmac-mac-workflow.md` — complete workflow article; public path if independently approved: `/blog/dissectmac-mac-workflow/`.
- `/Users/gabe/code/breathing-room/website/public/assets/blog/dissectmac/folder-triage.svg` — original SVG decision aid; not competitor UI.
- `/Users/gabe/code/breathing-room/website/public/assets/blog/dissectmac/breathing-room-space-preview-2026-10-21.png` — unchanged copy of the current-source first-party screenshot record. Example data only, not a native scan or measured result.
- This handoff.

## Scope and evidence

The article reuses `docs/content/competitors/dissectmac/research.json` and `.md`, existing verification records, `capabilities.md` and `screenshots.json`; no baseline facts were refetched. It treats DissectMac’s documented treemap, drill-down, search and developer filters as discovery aids only. The central decision rule is original editorial synthesis: establish ownership, activity, data type and recovery/rebuild cost before selecting a removal method. No cleanup commands, benchmarks, app tests or fabricated results are present.

The old `draftingAllowed:false` was solely tied to competitor image rights. October22 EDITORIAL route B allows this source-backed internal draft using a documented workflow diagram and attributed official image link, without copying the restricted screenshot. DissectMac official images remain link-only; no reuse rights are inferred. The page identifies its own SVG as editorial decision aid, not UI or safety certification.

Known conflicts/unknowns retained: DissectMac pricing says one-time while its privacy policy uses “subscription” language; billing cadence is unresolved. Pricing currency code, sale expiry and device allowance are unknown. Exact version/build, confirmation mechanics, runtime compatibility and independent privacy/network behavior remain unverified. Breathing Room statements remain source-level/preview-qualified, including Python, notarization and hosted-data caveats.

Alternatives intent was not duplicated here. Existing `src/content/alternatives/dissectmac.md` is a separate review draft based on retained evidence and evaluates DaisyDisk, Disk Map, AppCleaner and Breathing Room by distinct jobs; no skip/alias record is warranted for canonical DissectMac. This article links only the comparison hub and tools hub, not unpublished individual records.

## Asset and snapshot hashes

- Article `src/content/blog/dissectmac-mac-workflow.md`: `77ca8b1d57216446f7a88553474214449b172de6a2bb6b4f6e2cbc57aa55d814`
- Decision aid `public/assets/blog/dissectmac/folder-triage.svg`: `0e1593e566a24c38aa6e37141436cc7f90f67b69d4c4728b9a840db09857a1ee`
- Published Space preview copy: `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a`, matching its source file and screenshot-library record exactly.

## Remaining review items

1. Independently verify every claim against retained source passages and resolve/retain the pricing/privacy conflict; refresh volatile offer details before publication.
2. Inspect SVG appearance at mobile, tablet and desktop in light/dark modes; verify PNG crop/banner legibility, alt/captions, provenance and third-party marks.
3. Run the required marketing checks in sequence (`pnpm check`, `pnpm build`, `pnpm test`) and inspect generated draft exclusion, metadata/canonical/schema and links. No shared build was run in this job.
4. Conduct independent factual, SEO, accessibility and rendered-page review. Pending gates mean this is not publish-ready; no score is awarded.

## Validation recorded

Actual commands/results and final file hashes are recorded in the companion runtime receipt: `docs/content/.runtime/draft-blog-dissectmac.1792665682865657000.receipt.json`.
