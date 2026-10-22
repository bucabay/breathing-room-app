# MacCleanse workflow article handoff

Task: `draft-blog-maccleanse` · Draft prepared **2026-10-22** · Intended public path: `/blog/maccleanse-mac-workflow/`.

**Complete textual draft, not publication approval.** The record remains `status: review`, `published: false`. No public route was enabled. It teaches one distinct job: separating saved scan scope, one-run results selection and recurring schedule. It does not duplicate the product profile or head-to-head matrix.

## Owned outputs and exact snapshots

| Real output file | SHA-256 |
| --- | --- |
| `/Users/gabe/code/breathing-room/website/src/content/blog/maccleanse-mac-workflow.md` | `433c96f11feeb5b00e7b1414de79f0b1b098223b4741e1d80ccb7ae5368ad985` |
| `/Users/gabe/code/breathing-room/website/public/assets/blog/maccleanse/results-preset-decision.svg` | `d0abcb9961a64ef77def70ef043a9c30e4d10107fa46ce4404399c507d725cdd` |
| `/Users/gabe/code/breathing-room/website/public/assets/blog/maccleanse/breathing-room-space.png` | `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a` |
| `/Users/gabe/code/breathing-room/website/public/assets/blog/maccleanse/provenance.json` | `44d49d95246d19d18689f9ea6cd16e6ca1056ed21dd53724cce1979622254ec6` |

## Evidence reused and conflicts preserved

- Reused the verified canonical identity, AlternativeTo discovery chain, official product snapshot and claims C01–C11 from `research.json` / `research.md`; reused `docs/content/verification/batch-1.json#maccleanse`, `capabilities.md`, and `screenshots.json`. No baseline re-fetch was needed.
- Core claim C06 is scoped to Koingo's **undated manual**: checking or unchecking a completed results list does not alter saved scan settings. The prose explains the decision principle; it does not invent current v15 controls or assert UI parity.
- C05 supports advertised daily/weekly/monthly scans. C07 remains explicitly conflicted: the manual's optional skip-to-erasing setting and unconditional prompt statement do not support a blanket approval promise. Current defaults and the setting's exact behavior remain unknown.
- C11 supports the caution that old or large does not mean disposable. No “safe cache,” permanent deletion, Trash/recovery, reclaimed-space, performance, or benchmark claim was added.
- Version-scoped macOS 11 minimum and broader vendor Apple Silicon wording remain vendor statements, not installation tests. Upper OS naming, current Intel binary, notarization/signing and runtime prerequisites remain unverified. Pricing and other nonessential unknowns are omitted.
- Breathing Room language reuses B01–B04 and the capability register: preview/non-notarized, Python 3.10+ for inventory, incomplete clean-machine/physical-Intel validation, source-versus-installer limits and authenticated hosted-data boundary. The opt-in Ruff automatic Trash exception is not flattened into “always asks”; daily approvals require the app to run. No feature parity is implied.

## Visual and interaction work

- Chose approved route B. The original top SVG separates three documented decisions and includes a review checkpoint. It is an editorial decision aid, not MacCleanse interface, a screenshot or a hands-on test.
- Reused the screenshot-library Space browser-preview PNG unchanged; hash matches the register. The image is first-party browser UI with illustrative example data, not a native scan, measurement or cleanup outcome. Its full disclosure is in the caption and asset manifest. Final responsive legibility is pending.
- Koingo's official Cleanup image remains an external text link only and is not reproduced. The legal page requires prior written consent; none was obtained or requested. No image bytes were downloaded.
- Interaction pass: plain-text, non-mutating five-question checklist distinguishes scope, current selection, future schedule, recovery and removal consequence. No filesystem access, settings write, cleanup command or fake mini-app.

## Actual validation

- Read `PLAN.md`, October22 `EDITORIAL.md`, `capabilities.md`, `screenshots.json`, existing MacCleanse research and relevant marketing content conventions. No applicable `AGENTS.md` was found in the scoped repository/ancestor chains.
- Loaded `blog-write`, `blog-seo-check`, `blog-factcheck` and `browser-automation`; applied Breathing Room's documented adaptation rather than irrelevant generic blog quotas.
- Read-only structural inspection: article has 95 lines, approximately 1,317 words, seven H2 headings, two local image references, no unresolved internal-link/TODO placeholder markers. Title is 52 characters; description is 157 characters. Draft publication fields are retained.
- `xmllint --noout public/assets/blog/maccleanse/results-preset-decision.svg`: passed (exit 0).
- `shasum -a 256` recorded exact hashes above; copied PNG hash exactly matches the existing screenshot register.
- No shared site checks/build/tests or browser preview were run: this scheduled task forbids shared builds and does not authorize shared site changes. No independent fact/visual/SEO/rendered review or score is claimed.

## Remaining review gates

1. Independently verify article claims against the retained Koingo manual/product passages, including the approval-language conflict and version-scoped platform statement; confirm citation adjacency and no unsupported inference.
2. Independently review the exact SVG and page at narrow/tablet/desktop widths and light/dark themes. The PNG is full height and may need a permitted contextual crop; preserve the visible example-data disclosure and record any crop/hash/provenance if changed.
3. Run serialized site `pnpm check`, `pnpm build`, then `pnpm test`; inspect built metadata, canonical/OG/Twitter/schema and confirm draft exclusion from routes, listings, feeds and sitemap. No build or leakage regression is inferred from source inspection.
4. Keep review/unpublished until independent evidence, asset, SEO and rendered-page review passes. Refresh volatile claims before release; this draft intentionally omits pricing.

No alternative/skip page was created: that is a separate intent and not required by this workflow article. No aliases were verified, so no blog-skip record is justified. No other research packet, queue state, database, nav/schema/tests or unrelated work was changed. No accounts, purchases, messages, credentials, cleanup, installation, settings change, subagents, commit, push or deployment occurred.
