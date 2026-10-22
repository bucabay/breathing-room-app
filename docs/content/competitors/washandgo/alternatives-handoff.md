# WashAndGo alternatives draft handoff

**Task:** `draft-alternatives-washandgo`  
**Draft date:** 2026-10-22  
**State:** Internal review; not publication approval. No queue/database changes.

## Owned outputs

- Marketing page: `/Users/gabe/code/breathing-room/website/src/content/alternatives/washandgo.md`
- Original decision visual: `/Users/gabe/code/breathing-room/website/public/assets/alternatives/washandgo/mac-cleanup-decision.svg`
- Selected official press image: `/Users/gabe/code/breathing-room/website/public/assets/alternatives/washandgo/EN_CleaningOptions.PNG`
- First-party example UI: `/Users/gabe/code/breathing-room/website/public/assets/alternatives/washandgo/space-preview-2026-10-21.png`

## Intent and evidence

The page answers a distinct replacement need: choosing Mac tools for the job a former WashAndGo user wants to continue. WashAndGo's official offer identifies a Windows product; current Mac support remains unverified. The three candidates come from retained official evidence in the source graph: CleanMyMac for a broader maintenance routine, DaisyDisk for storage mapping, and AppCleaner for known-app removal. These are editorial task matches, not asserted AlternativeTo relationships. Breathing Room is disclosed as an affiliated, preview-stage, macOS-only option with significant runtime and hosted-service limits.

Research basis: `research.json`/`.md` in this directory for WashAndGo, `capabilities.md`, and retained packets for `cleanmymac`, `daisydisk`, and `appcleaner`. Conflicts remain bounded: Abelssoft's baseline showed €29.95 while a later regional rendering showed `$29.95`; no currency conversion/checkout conclusion is made. DaisyDisk current offer says macOS 10.13+ while an older edition guide says 10.10+; only the current advertised requirement is used, without binary compatibility inference. AppCleaner pricing/licence, exact removal semantics and recovery are explicitly not established. No competitor installation, cleanup, performance or savings test was performed.

Visual route: original authored decision diagram plus attributed link to WashAndGo's official press-supplied older options image. The retained image is the cleared, exact press-package item; version and capture date remain unknown. Breathing Room image is an unedited current-source browser capture with example data, not a native scan or measured result. No competitor UI was fabricated or redrawn.

## Integrity and open review

SHA-256 values are recorded in the job receipt. Remaining before publication: independent claim/intent and image-context review; refresh mutable offers/availability within 30 days and before publication; run site `pnpm check`, `pnpm build`, then `pnpm test`; inspect built metadata/draft exclusion; responsive light/dark visual and link review. No site build/tests or browser QA were run for this draft job. Do not change review status/published fields without the independent gate.
