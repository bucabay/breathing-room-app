# MacSweep workflow blog handoff

Job: `draft-blog-macsweep`, drafted October 22, 2026. This is an internal review draft, not publication approval.

## Owned outputs

- Marketing article: `/Users/gabe/code/breathing-room/website/src/content/blog/macsweep-mac-workflow.md`
- First-party preview visual: `/Users/gabe/code/breathing-room/website/public/assets/blog/macsweep/space-preview-2026-10-21.png`
- Original route-B workflow visual: `/Users/gabe/code/breathing-room/website/public/assets/blog/macsweep/developer-artifact-review.svg`

Article SHA-256: `493333954d655af818cabda8afed89a263964d5ab58a7043abfbaed26324c071`  
Preview SHA-256: `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a`  
Diagram SHA-256: `af2c7d9c95238b6f89e36b2cf6b5b15e1c9b42829f5675c3aea56fd438ef321f`

## Editorial decision and evidence

The article teaches a specific developer-artifact review workflow, distinct from the product profile, comparison, and alternatives intent. It reuses `docs/content/competitors/macsweep/research.json` and `.md`, the baseline verification cited there, `docs/content/capabilities.md`, and `docs/content/screenshots.json`; no broad research refresh was performed.

The old `draftingAllowed:false` is overridden only as permitted by the October 22 editorial update: its material blocker was competitor screenshot rights. Route B is used: an original decision diagram, clearly identified as editorial guidance and not product UI/test, plus a text link to MacSweep’s official product page. The app image candidate remains link-only; it was not downloaded or copied. The Breathing Room Space image is the existing current-source browser preview, with its example-data/native-test limitation in the caption. The article has no fake UI, unsupported negative feature cells, fabricated measurements, or purchase-price recommendation.

The packet’s conflicting locale scope is disclosed: Chinese and English official pages list developer artifacts differently. The article scopes the list to the English page. The advertised early-bird yearly price conflicts with expired structured validity and an unreadable purchase page; effective price remains unknown. Approval controls, runtime dependencies, desktop licence, installer execution, binary signing validation, and actual scan coverage remain unknown or vendor-claimed as stated. MacSweep is not treated as a verified alias. Existing alternatives handoff is not overwritten; this job does not create an alternatives page or skip exception.

## Validation and remaining gates

- SHA-256 recorded for all three output assets.
- Marketing `pnpm check` attempted with the specified Node path. **Failed before validating this draft** because unrelated `src/content/alternatives/amplecapacity.md` has `sources.*.checked` values parsed as objects rather than strings. No unrelated file was changed.
- Per the required check/build/test sequence, stop here: build and tests were not run because content collection validation is already blocked by that shared pre-existing record.
- Independent factual/visual review, rendered HTML metadata/link review, build/test, and narrow/tablet/desktop light/dark browser checks remain pending. Draft stays `status: review`, `published: false`.
- Pricing, release availability, platform and product claims require fresh pre-publication review. Competitor image rights remain uncleared and no image permission request was made.
- Public route intended: `/blog/macsweep-mac-workflow/`; no route/build verification was possible.

No shared files, queue/database state, navigation, schema, tests, or other jobs were edited. No app test, cleanup, browser session, account, purchase, commit, push, or deployment was performed.
