# MacOSCleaner workflow blog handoff

**Job:** `draft-blog-macoscleaner` · **Draft date:** 2026-10-22 · **Status:** internal review only (`status: review`, `published: false`).

## Output

- Marketing article: `/Users/gabe/code/breathing-room/website/src/content/blog/macoscleaner-mac-workflow.md`
- Public route if independently approved and published: `/blog/macoscleaner-mac-workflow/`
- Original workflow visual: `/Users/gabe/code/breathing-room/website/public/assets/blog/macoscleaner/cache-review-decision.svg`
- First-party visual copy: `/Users/gabe/code/breathing-room/website/public/assets/blog/macoscleaner/space-preview-2026-10-21.png`

The article teaches a specific decision workflow for reviewing developer-cache candidates. It is not the neutral product profile or head-to-head comparison. It uses the retained MacOSCleaner evidence in `research.json` and `research.md`, plus the October 21 capabilities and screenshot records; no baseline was needlessly refetched. The old `draftingAllowed:false`/blocked state applied solely to the former screenshot gate. October 22 `EDITORIAL.md` explicitly authorizes source-backed internal drafting under route B.

## Evidence, visuals, and intent

- MacOSCleaner identity is AlexTkDev’s canonical `macoscleaner` project. “MacOS Cleaner” is a verified alias; no alias page was created. No alias skip record was necessary because this job owns the canonical article, not the separate alias workflow.
- The prose distinguishes vendor documentation from hands-on results, avoids the unsafe quarantine workaround, and keeps macOS 26+/Apple Silicon eligibility and direct-prune versus Trash distinctions prominent. Unknown release parity, signing, telemetry and recurring-growth behavior remain expressly bounded.
- Source conflict retained: AlternativeTo’s GPL label omits the Commons Clause described in the official README/licence. The article follows official project wording and avoids unqualified “open source” claims.
- Route B: the SVG is an original decision aid, not competitor UI or a test. The genuine official MacOSCleaner screenshot remains a link to its pinned README Demo section only: image-specific reuse rights and image inspection are unresolved, and no image bytes were copied or hotlinked.
- The unchanged Breathing Room Space browser capture is copied from `docs/content/assets/breathing-room/space-preview-2026-10-21.png`. Original SHA-256: `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a`; source commit `54828ac3170b45861aee70861dd0b9c658ed7e51`; capture `2026-10-21T19:06:45.416416+00:00`. Caption and alt identify example data and explicitly disclaim native scanning, measured activity, and cleanup results.
- Alternatives intent was checked against three existing packets rather than invented: CleanMyMac is direct cleanup overlap and documents Xcode Junk, but edition/price conditions remain unresolved (`cleanmymac/research.md`, checked October 21); Mole has separate CLI/native editions and CLI artifact cleanup, with distinct platform/version boundaries (`mole/research.md`, checked October 21); MacPilot is explicitly adjacent customization/maintenance rather than a direct storage-investigation substitute (`macpilot/research.md`, checked October 22). These support a future job-based candidate set, but not a distinct MacOSCleaner replacement page in this blog-only task: the peers are not established as interchangeable replacements, and no alternatives page was owned or created. Reassess under its own alternatives job using those retained packets and caveats.
- Internal links are limited to the live `/comparisons/` hub and implemented `/tools/cache-rebuild-checklist/` utility. No uncreated comparison or related blog slug is linked.

## Hashes and review gates

SHA-256: article `533bb9f2672ebeca7f94ebbb75d511a4f87f5f9ee8fa0c627cb994b70c7af770`; SVG `5c9a89d34edba9a73c811fd87010c9f51a16ab7c5d975bad85bbbf82dfbd75b5`; copied PNG `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a` (matches source byte-for-byte). Required independent factual/visual review, route rendering, `pnpm check`, `pnpm build`, `pnpm test`, built-output metadata/publication-gate inspection, and responsive browser review were not performed in this drafting task. Do not publish until those are complete. No shared build was run, as explicitly prohibited. The draft frontmatter remains unpublished and is not itself a public route.

Remaining review: assess the actual page and SVG on narrow/mobile, tablet and desktop in light/dark themes; confirm asset loading, accessibility and metadata; verify exact claim/source alignment and current product disclosures; inspect the copied preview/banner/caption in context; independently review score and blockers. Recheck volatile facts before publication. No license-based screenshot reuse grant is inferred.
