# CleanMyMac workflow blog draft handoff

Task: `draft-blog-cleanmymac` · prepared **2026-10-22** · draft complete; independent publication review pending.

## Outcome and owned files

One complete search/reference workflow article was drafted for `/blog/cleanmymac-mac-workflow/`. It teaches a specific job: inspect CleanMyMac Smart Care's preselected tasks and decide what to run, skip, or investigate. It is not the product profile, head-to-head comparison, or alternatives page. The frontmatter remains `status: review`, `published: false`; this is not publication approval.

| Exact file | SHA-256 |
| --- | --- |
| `/Users/gabe/code/breathing-room/website/src/content/blog/cleanmymac-mac-workflow.md` | `a4ad165b8f989aedbc25c7ccf294871e5ad66a2389900e430917b8a02b5d25db` |
| `/Users/gabe/code/breathing-room/website/public/assets/blog/cleanmymac/smart-care-review.svg` | `0d368b75ac708bbe1c0c661b654ad79af5100926a4eae89384c828414ca7299a` |
| `/Users/gabe/code/breathing-room/website/public/assets/blog/cleanmymac/space-preview-2026-10-21.png` | `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a` |
| `docs/content/competitors/cleanmymac/blog-skip.md` | `e0780f1326f86452cfe65eda9db31dd210ffe92f9218107a2e3947cb062c45e7` |

This handoff's hash is not embedded recursively. Receipt is `/Users/gabe/code/breathing-room-app/docs/content/.runtime/draft-blog-cleanmymac.1792663787151173000.receipt.json`.

## Instructions and retained evidence

Read `PLAN.md`, the October22 update and full editorial rules in `EDITORIAL.md`, `capabilities.md`, `screenshots.json`, CleanMyMac `research.json`/`.md`, existing profile/comparison/alternatives records, website publishing contract/schema and the relevant `blog-write`, `blog-seo-check`, `blog-factcheck`, and `browser-automation` skills. No applicable `AGENTS.md` was found in either scoped tree. No subagents were used.

Reused the source packet and baseline verification instead of re-fetching sources. Official identity remains MacPaw CleanMyMac; discovery was `https://alternativeto.net/software/cleanmymac/about/`. The packet's old `draftingAllowed:false` is screenshot-rights history, not a bar to this internal route-B draft. MacPaw's Smart Care guide was retrieved October 21 and documents Scan → review → Run, initially selected tasks, skip/review controls, and five distinct task areas. The article distinguishes Cleanup, Protection, Performance, Applications, and My Clutter; it does not claim hands-on testing or generalize the Downloads duplicate scan to the whole disk.

Preserved conflicts and unknowns: the homepage snapshot calls 5.5.7 “latest” while the newer dated changelog entry is 5.7.2 (October 15); article attributes the conflict and does not infer installed version or marketplace parity. Exact CleanMyMac pricing conditions, current EULA, binary behavior, and screenshot reuse rights remain unknown. The article does not reproduce competitor UI, quote a numeric competitor price, assert unsupported feature absence, or claim savings, speed, safety, recovery, or malware-detection results. The documented guide's Smart Care image remains link-only in research; no asset was copied. The verified alias CleanMyMac X has a separate alias-only skip record; PowerMyMac remains distinct and outside this job.

## Visual and interaction pass

Route B is used accurately: the article starts with an original source-backed decision diagram, then includes a byte-identical copy of the existing first-party Space browser preview. The SVG is an editorial decision aid, not CleanMyMac UI, a screenshot, or a test. The PNG is the October 21, 2026 current-source browser capture with illustrative example data, not a native scan, measurement, cleanup result, or installer validation; the inventory's alt and full caption are retained. Source inventory SHA-256 matches the published copy. Rights/context/layout review remains pending.

Interaction pass: a non-mutating checklist asks about target/location, ownership/purpose, action and recovery path. It does not invoke the app, click Run, delete files, simulate a scan, or access a filesystem. Only known live internal links are used: `/comparisons/` and `/tools/storage-headroom/`; draft product pages are not linked as if public.

## Checks performed and pending gates

- **PASS:** article and visual source claims were cross-checked against the retained CleanMyMac research excerpts and same-day Breathing Room capability/screenshot records; source disagreement/unknowns above remain explicit.
- **PASS:** source schema fields follow `src/content.config.ts` (`title`, `description`, `status`, `published`, `date`, `author`, `sources`); October 22 is draft date, while source `checked` dates remain October 21.
- **PASS:** the SVG is authored without external image requests or app-like controls; the source PNG hash matches inventory and its caption/alt identify illustrative data and limitations.
- **NOT RUN:** shared website `pnpm check`, `pnpm build`, and `pnpm test`, prohibited by the scheduled task. No shared nav/schema/tests or queue files were changed.
- **PENDING:** isolated rendered-page fixture and independent browser inspection at mobile/tablet/desktop, light/dark, keyboard and visual legibility; built canonical/social/schema/link and draft-exclusion review; independent fact, image-context/rights and SEO review. The draft has no public preview route. No score or publication readiness is claimed.

No browser session was started; this task needed no live page interaction and existing retained sources were sufficient. No install, account, purchase, permission request, message, cleanup, commit, push, deployment, or queue/database mutation occurred. Existing unrelated work was preserved.
