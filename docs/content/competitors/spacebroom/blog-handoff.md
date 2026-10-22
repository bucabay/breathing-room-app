# SpaceBroom workflow blog handoff

Drafted 2026-10-22 from the retained `research.json`/`research.md`, official baseline and claim excerpts, `capabilities.md`, and `screenshots.json`. The previous `draftingAllowed:false` was solely a screenshot-rights gate; the October 22 policy permits this internal source-backed draft with route B.

## Owned outputs and snapshot hashes

| File | SHA-256 | Role |
| --- | --- | --- |
| `/Users/gabe/code/breathing-room/website/src/content/blog/spacebroom-mac-workflow.md` | `0fb17c420bcaeb4c71c78f5f9fc9bb2601837a40249ff37d4bb9f87bf4bf0435` | Complete unpublished workflow article; `/blog/spacebroom-mac-workflow/` |
| `/Users/gabe/code/breathing-room/website/public/assets/blog/spacebroom/project-review.svg` | `70a732506382b3dd579392dca38099c1a0725bcc75b720a1d214e8674818b983` | Original vertical project-folder decision aid; not competitor UI |
| `/Users/gabe/code/breathing-room/website/public/assets/blog/spacebroom/space-preview-2026-10-21.png` | `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a` | Existing first-party Space browser preview, copied byte-identically from the source capture |

The lead SVG tells the reader how to classify a folder, establish recovery cost and distinguish investigation from an action decision. The later Space screenshot visibly labels example data. Its caption says it is a browser preview, not a native scan, measured result or proof of distributed-release parity. SpaceBroom's official Space Lens screenshot is linked only; its image bytes were not inspected and reuse permission was not established. This is the permitted route-B visual treatment, not a pending permission request.

## Evidence and editorial boundaries

- Uses the documented Space Lens folder-by-size navigation and developer categories as vendor-described behavior, not an app test. A large directory, `node_modules` label, duplicate match or category total is not treated as deletion permission.
- Resolves the broad “Trash first”/“nothing without your click” homepage language against the terms and FAQ: Trash only where possible, permanent-operation exceptions, and conditional restoration. No universal reversibility or safety promise.
- Reuses Breathing Room's source/release limits: preview `0.1.0-preview.1`, macOS 13+, Python 3.10+ for inventory, not Developer ID signed/not notarized per published disclosure, and incomplete clean-machine/physical-Intel validation. Hosted assistant context can leave the Mac; no entirely-offline claim.
- Says “Breathing Room, which we build.” Claims about SpaceBroom process/helper grouping, recurring-growth attribution, exact binary version/architecture and App Store availability are omitted or expressly left unverified. No pricing was needed for this workflow.
- Context links target the retained SpaceBroom comparison record and live `/comparisons/` and `/tools/` hubs. No alternatives page duplication or external competitor screenshot copy.

## Checks and pending review

Passed local structural checks: draft metadata/date, article section presence, local image targets, SVG structure/text, screenshot byte identity, and comparison target existence. SHA-256 values above were computed from the owned files; the screenshot hash matches the shared inventory.

The shared-site checks/build/test and rendered browser review were intentionally not run: this job explicitly forbids shared site builds. A first frontmatter-check attempt using PyYAML did not run because that module is unavailable; a separate dependency-free metadata check passed. A first SVG parser attempt could not run because this host's Python `pyexpat` import is broken; an independent structural/text and accessibility-attribute check passed. These are environment/tool limits, not successful render validation.

Still required before publication: responsible site workflow's `pnpm check`, `pnpm build`, then `pnpm test`; inspect generated canonical/schema/draft exclusion and links; independent factual/visual review against these exact hashes; authorized local browser review at mobile/tablet/desktop and light/dark; confirm narrow-screen visual legibility and both assets in rendered context. No score or publication approval is claimed. Draft stays `status: review`, `published: false`.
