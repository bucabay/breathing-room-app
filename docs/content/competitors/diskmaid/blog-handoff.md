# DiskMaid workflow blog handoff

Task: `draft-blog-diskmaid` · Drafted 2026-10-22 · Status: review, unpublished.

## Owned outputs

- Marketing article: `/Users/gabe/code/breathing-room/website/src/content/blog/diskmaid-mac-workflow.md` (public path `/blog/diskmaid-mac-workflow/`).
- Route-B assets: `/Users/gabe/code/breathing-room/website/public/assets/blog/diskmaid/space-preview-2026-10-21.png`, `remnant-duplicate-review.svg`, and `provenance.json`.
- This handoff: `docs/content/competitors/diskmaid/blog-handoff.md`.

SHA-256 (actual files, calculated at handoff):

- Article: `0283696432c68802cea0f9561c5d80e0601a20991b8aafcae0dc3f410036f961`
- Preview PNG: `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a`
- Decision SVG: `394bd554066c8485f64d72abc3dfc1359d73bc103e72d70b5b7f481320aca725`
- Provenance JSON: `c7e5c99b1856695118665ce9f488582edf5b78c88bfc4aac12e56c79b02a724d`

## Evidence and editorial choices

Reused `research.json`, `research.md`, `docs/content/verification/batch-1.json`, `capabilities.md`, and `screenshots.json`; no competitor source was refetched. The supported workflow is the reader's retention decision about app remnants and exact duplicates. Vendor claims are attributed as documentation, not hands-on results. Matching bytes and app association are explicitly separated from ownership, current use, recovery, and rebuild cost.

The packet's old `draftingAllowed:false` is historical and solely reflects the unresolved DiskMaid screenshot rights/pixel gate. Drafting proceeds under October 22 route B: a current-source Breathing Room Space browser preview with the mandatory example-data/native limitation, plus an original documented-workflow decision SVG. No DiskMaid UI is copied or hotlinked. Asset detail and source/published hash are in `provenance.json`.

Material caveats retained: DiskMaid's US listing price/version/macOS requirement are dated October 21, 2026 evidence, not fresh checkout or install testing; official “no usage tracking” wording conflicts with App Store tracking-identifier disclosure and the privacy policy's device-identifier statement. No blanket privacy conclusion is made. DiskMaid deletion/undo semantics, architecture, exact cache adapters, native behavior, and measured savings remain unknown. Breathing Room preview, Python, notarization, hosted-data, daily runtime, and Ruff-mode qualifications are stated.

## Alternatives disposition

The marketing repository already contains `src/content/alternatives/diskmaid.md` in review/unpublished state. It names CleanMyMac, DaisyDisk, and Pearcleaner and frames alternatives by distinct jobs, so this job created no duplicate alternatives page or `blog-skip.md`. Existing source packets support relevant peer checks: SpaceBroom documents duplicates and app remnants (with vendor-specific exclusions); AppCleaner is a distinct app-removal utility; AppZapper documents the app-removal job. Their research records remain review-stage, so the existing alternatives page still needs independent claim/source and freshness review before publication. This is not a claim those products are equivalent or verified as DiskMaid replacements for every workflow.

## Interaction and review gates

Interaction pass: the non-scanning SVG is the useful decision aid; the article's five checks all lead unknown cases to “keep and investigate.” No file-system access, upload, automated deletion choice, or savings calculator was added.

Performed: read relevant policy, evidence and content-schema records; verified copied preview SHA-256 against the source packet; checked that article frontmatter uses the current content fields and review/unpublished gate; inspected article route as filename-derived and internal destination `/comparisons/` as the live hub. No site build, shared-site test, browser render, public-page verification, independent review, install, app test, cleanup, or deletion was performed, by scope. No quality score or publication approval is claimed.

Remaining before publication: independent claim-level fact/SEO review; visual review of SVG at narrow and desktop widths/light and dark themes; inspect rendered route, metadata, schema, links and draft leakage through the authorized site QA workflow; refresh volatile DiskMaid storefront/version and Breathing Room release/price facts; resolve whether stronger privacy statements are supportable. Current example preview and route-B diagram do not clear native/runtime QA or competitor-image rights. Keep `status: review`, `published: false` until all gates pass.
