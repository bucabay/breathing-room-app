# AppCleaner workflow article handoff

Task: `draft-blog-appcleaner` · prepared 2026-10-22. This is a draft handoff, not independent evidence approval or publication authorization.

## Owned outputs

- Article: `/Users/gabe/code/breathing-room/website/src/content/blog/appcleaner-mac-workflow.md`
- Route if independently approved and published: `/blog/appcleaner-mac-workflow/`
- Original decision visual: `/Users/gabe/code/breathing-room/website/public/assets/blog/appcleaner/removal-or-investigation.svg`
- First-party source preview copy: `/Users/gabe/code/breathing-room/website/public/assets/blog/appcleaner/space-preview-2026-10-21.png`

The article is `status: review`, `published: false`, date 2026-10-22. The workflow intent is choosing between removing a known unwanted app and investigating storage growth while retaining an app. It is not a second product profile or comparison matrix.

## Evidence applied

Reused `research.json` / `research.md`, the baseline in `docs/content/verification/batch-1.json`, `capabilities.md`, and `screenshots.json`; no redundant product crawl was performed. AppCleaner is FreeMacSoft’s distinct adjacent app-uninstaller. The official source describes drop app → find related files → click delete; this remains attributed vendor documentation, not a hands-on result. The version ranges are reproduced as the official page lists them, including overlap. AlternativeTo’s “Free” and “Proprietary” labels are attributed; exact price and full licence conditions remain unknown. Official repository, architecture, signing/notarization, runtime, permissions, privacy/network behavior, file-selection granularity, Trash/recovery, and completeness remain unverified and are not converted to negative claims.

The old `draftingAllowed:false` and blocked status reflected the earlier image-rights rule, not unknown identity or lack of substantive evidence. October 22 `EDITORIAL.md` permits a source-backed draft with route B: first-party labeled preview plus original documented-workflow diagram and attributed official image link. The AppCleaner screenshot URL is not copied or embedded because its page reserves all rights and its content/version were not visually inspected.

The Space PNG is reused unchanged from the record at `docs/content/assets/breathing-room/space-preview-2026-10-21.png`, SHA-256 `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a`, source commit `54828ac3170b45861aee70861dd0b9c658ed7e51`. It is an example-data browser preview, not a native scan or measured result. The original caption and visible disclosure are retained; the known floating-composer overlap is disclosed.

Breathing Room claims reuse the October 21 capabilities register. Preview, Python 3.10+ for inventory, no Developer ID signing/notarization, incomplete clean-machine/physical-Intel validation, hosted AI authentication/data transfer, and advertised renewing AI Care pricing are stated with scope. No installer/runtime, subscription, or payment was tested.

## Separate alternatives intent

No `/alternatives/appcleaner/` page was created in this job. A distinct replacement intent appears supportable from existing packets rather than requiring filler: the verified `appzapper` packet describes AppZapper 3000’s adjacent app-removal workflow and retains its own conditions; the `mole` packet verifies app-uninstallation context across distinct CLI/native editions. Any alternatives page should compare the actual removal jobs, edition/platform/licence boundaries, current terms, and source/visual blockers before drafting. AppCleaner has no verified aliases in its packet, so no alias `blog-skip.md` applies. No route beyond the live `/comparisons/` and `/tools/` hubs was assumed.

## Visual provenance and hashes

- Decision diagram is original SVG authored for this article from the cited workflow and capability boundaries; it does not depict either product UI. Rights/provenance: article authorship; independent visual/readability review pending.
- Article SHA-256: `0fa4840dbe2803c0e319639c2829140da6ddbf74cacba986653af2c114b6c5ba`.
- Decision SVG SHA-256: `9ca8f5a5a4f4d4988b41518b3201ab78bbe1e1e6aefd1a9ca177bf13b37f79ea`.
- PNG copy SHA-256: `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a` (matches the shared inventory).

## Remaining review before any publication

1. Independent claim and source review against the exact article and asset hashes; resolve any changed official facts, especially version availability and offers, before publication.
2. Confirm rendered canonical/metadata/schema and draft exclusion; run website `pnpm check`, `pnpm build`, then `pnpm test` in order, retaining outputs. No shared build was run by this drafting worker.
3. Inspect rendered page and both visuals at mobile/tablet/desktop and light/dark themes. Verify the example-data banner stays legible, image loads, captions/alt are appropriate, and no layout issue is hidden by source-only review.
4. Record itemized independent score and require at least 85/100 with zero blockers. Current review score is intentionally unassigned; no browser or rendered review is claimed.

No queue/database, shared navigation/schema/tests, other competitor record, or unowned article was changed. No accounts, messages, purchases, cleanup, commits, pushes, deployments, or subagents were used.
