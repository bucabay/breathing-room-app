# Blog draft handoff: IUWEsoft Mac Cleaner Pro

**Task:** `draft-blog-mac-cleaner-pro`  
**Draft date:** 2026-10-22  
**Public path when independently approved:** `/blog/mac-cleaner-pro-mac-workflow/`  
**State:** `status: review`, `published: false`; no publication or rendered-page approval.

## Owned output and hashes

Marketing repository paths are absolute below.

| File | SHA-256 | Purpose |
|---|---|---|
| `/Users/gabe/code/breathing-room/website/src/content/blog/mac-cleaner-pro-mac-workflow.md` | `632193fd865b01ca7890c01634a5846bb0ba8c91f7b7524241631dc998a95a7d` | Complete search/reference workflow article; 1,474 words including metadata and sources. |
| `/Users/gabe/code/breathing-room/website/public/assets/blog/mac-cleaner-pro/goal-before-action.svg` | `857158b94925c4b0e8959fd14a5a4ab4d0562415ee61a47b7075d1d5d83609c3` | Original decision aid; explicitly not competitor UI or erasure guidance. |
| `/Users/gabe/code/breathing-room/website/public/assets/blog/mac-cleaner-pro/space-preview-2026-10-21.png` | `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a` | Unchanged first-party Space browser preview; matches `screenshots.json` source hash. |

## Scope and evidence handling

The article teaches a bounded per-file decision workflow: distinguish recovering storage, investigating recurring growth, and erasing sensitive data before selecting an action. It is not an expanded product comparison or alternatives roundup. IUWEsoft's target-selection/“Shred Now” copy is attributed to the official page, while the same-page “Start Analyze”/junk-cleanup conflict remains unresolved. It does not endorse irrecoverability or effectiveness, state a current price, or infer that an undocumented feature is absent. The vendor image URL is linked only; its contents and reuse rights remain unverified.

Breathing Room details reuse the October 21 capabilities register. Source implementation is not represented as tested installer behavior. The preview/runtime/signing, hosted-data, Python, and optional automatic Ruff-cache boundaries are preserved where relevant. The Space preview retains the example-data and non-native/non-measurement disclosures.

No competitor alternatives are asserted in this article. The already-existing alternatives draft uses retained research for Cleaner One Pro, CleanMyMac, and DaisyDisk as job-specific options, not as relationships inferred from the AlternativeTo listing. No alias-skip record applies: verification identifies IUWEsoft Mac Cleaner Pro as distinct from Nektony's MacCleaner Pro. The existing comparison and alternatives records are separate intents and were not edited by this job.

The October 22 route-B visual policy is followed: original documented-workflow diagram plus attributed official image link, alongside the labeled first-party Breathing Room view. The diagram makes no claim to depict competitor UI. Interaction pass: the five-step stop/go list and three-branch decision aid provide the reader-facing decision aid; no widget or runnable tutorial is needed for this non-executing workflow.

## Validation and remaining review

- Passed a local structural check for review/unpublished state, current dates, five H2 sections, source links, and referenced local assets/tool route.
- Passed `xmllint --noout` on `goal-before-action.svg`.
- Confirmed the copied PNG SHA-256 equals the retained source hash in `research.json` and `screenshots.json`.
- Attempted `PATH="/Users/gabe/.nvm/versions/node/v25.0.0/bin:$PATH" pnpm exec astro check` in the marketing site. **Blocked by an unrelated existing content-schema error** in `src/content/alternatives/amplecapacity.md`: multiple `sources[].checked` values parse as objects, while the schema requires strings. No unrelated file was edited.
- Did not run `pnpm build` or `pnpm test`, as this job explicitly prohibits shared site builds. No browser/rendered responsive review or independent editorial review was performed. Draft remains unpublished.

Review gates still open:

1. Resolve the unrelated Astro content error in its owning job, then run the required site check/build/test sequence under authorized scope.
2. Independently review exact copy against retained source excerpts; in particular, preserve the product identity/workflow conflict, pricing conflict, and unknown erasure efficacy.
3. Review both visuals in rendered mobile/tablet/desktop and light/dark views. Confirm diagram readability, image paths, visible example-data disclosure and route-B compliance.
4. Review the article's distinction from the existing `/comparisons/mac-cleaner-pro/` and `/alternatives/mac-cleaner-pro/` drafts before approving public release. Those destinations are not linked from this unpublished article; only live hubs and the verified storage planner are linked.
5. Refresh volatile product availability and claims before any publication; this draft is based on retained October 21 evidence, not a fresh vendor fetch.

No queue state/database changes, account creation, messages, purchases, cleanup, commits, pushes, deployments, or unrelated content edits were performed.
