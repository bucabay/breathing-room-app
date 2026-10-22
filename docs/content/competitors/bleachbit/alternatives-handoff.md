# BleachBit alternatives page handoff

**Status:** complete textual draft; independent review and publication gates pending. The earlier `draftingAllowed:false` was retained as historical packet state; this draft relies on the packet's `ready-for-bounded-documentary-draft` decision and October 22 route-B policy.

## Owned outputs

- Marketing page: `/Users/gabe/code/breathing-room/website/src/content/alternatives/bleachbit.md` — public route `/alternatives/bleachbit/`.
- Original diagram: `/Users/gabe/code/breathing-room/website/public/assets/alternatives/bleachbit/choose-by-platform-and-job.svg` — source-backed editorial decision aid, not competitor UI.
- First-party image: `/Users/gabe/code/breathing-room/website/public/assets/alternatives/bleachbit/breathing-room-space-example.png` — unchanged copy of the October 21 current-source Space browser preview; example data only, not native scan or cleanup evidence.
- This handoff: `/Users/gabe/code/breathing-room-app/docs/content/competitors/bleachbit/alternatives-handoff.md`.
- Receipt: `/Users/gabe/code/breathing-room-app/docs/content/.runtime/draft-alternatives-bleachbit.1792663564375534000.receipt.json`.

## Editorial scope and evidence

The page separates the documented Windows/Linux packaged BleachBit path from experimental source-based Mac support. It names five task-bounded peers from retained verification/source packets: CleanMyLinux (Linux cleaner), Mac CleanUp Go (Mac terminal cleanup), CleanMyMac (Mac maintenance suite), DaisyDisk (Mac disk map), and AppCleaner (Mac app removal). This is editorial selection from verified peers, not an asserted AlternativeTo relationship graph or a head-to-head copy. Breathing Room is disclosed separately for a different Mac storage-investigation job.

BleachBit's FAQ/platform release conflict is preserved: the general download FAQ said 6.0.4, while Windows/Linux platform pages and the October 17 announcement supported 6.0.6 at packet check. The page uses the platform-specific release and documents Mac support as experimental. CleanMyLinux's beta label and unresolved distro/GLIBC compatibility are retained. No installs, tests, cleanup, price checkout, benchmarks, savings or erasure outcomes are claimed.

Route B is used: an original platform/task diagram plus a labeled first-party Space preview and an official screenshot-page link where relevant. The retained historical BleachBit screenshot has CC0 evidence but depicts v3.2 on Windows 10, not current Mac UI; it was intentionally not copied because the diagram better communicates the distinct platform decision. The screenshot reuse waiver is retained at `research.json` claim B06/visual record and `screenshots-page.json`.

## Hashes

SHA-256 at draft handoff:

- Alternatives page: `9630a65930483d2d286f261d229c131240e0c54077e29f5531fb441b4876b79a`
- Decision SVG: `c3c33331a6f1776aad79a8496a7e916af21b5f4373d7cf007c23aeca57709b5c`
- First-party PNG: `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a` (matches retained source; unchanged)

The handoff document and receipt are not included in those content/asset hashes. No asset was altered.

## Remaining review before publication

- Independently check factual citations against retained packets and refresh volatile versions/prices before publication (research checked October 21, 2026).
- Review SVG readability and both visuals in rendered mobile/tablet/desktop contexts and light/dark themes. Preserve the example-data disclosure; the original tall PNG may need a contextual presentation/crop with edit and hash provenance.
- Review all cited destinations, internal routes, frontmatter/schema/canonical metadata and draft exclusion in built output. The existing BleachBit comparison file and routes were not changed by this job.
- Run the website's `pnpm check`, `pnpm build`, and `pnpm test` in sequence, then inspect output and perform authorized responsive browser review. No shared site build or tests were run for this job.
- Independent content/evidence/visual/SEO review and required editorial scorecard are pending. Keep `status: review`, `published: false` until these gates pass.

No queue changes, shared website files, unrelated competitor records, commits, pushes or deployments were made.
