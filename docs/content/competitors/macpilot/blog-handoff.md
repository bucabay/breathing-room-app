# MacPilot workflow blog handoff

Task: `draft-blog-macpilot`. Draft created October 22, 2026 using the retained October 21 evidence packet; no broad refetch was done. The prior research packet's `draftingAllowed:false` was based solely on the old screenshot gate. October22 EDITORIAL permits a source-backed internal draft with route B, so the article uses an original symptom-routing diagram and a link-only official MacPilot image. No permission request was sent and no restricted competitor image was copied.

## Owned outputs

- Article: `/Users/gabe/code/breathing-room/website/src/content/blog/macpilot-mac-workflow.md`
- Diagram: `/Users/gabe/code/breathing-room/website/public/assets/blog/macpilot/symptom-routing.svg`
- First-party example illustration: `/Users/gabe/code/breathing-room/website/public/assets/blog/macpilot/space-preview-2026-10-21.png`
- This handoff.

Public path: `/blog/macpilot-mac-workflow/`. Status is `review`, `published: false`; the draft must remain unpublished.

## Intent and evidence

The article teaches symptom triage—settings behavior vs one targeted maintenance problem vs unexplained disk growth. It is not a tool profile, comparison matrix, or alternatives list. MacPilot identity and substantive product claims are supported by the retained official product page/manual/EULA. It preserves the product page's conflicting August 19/August 31 release dates, omits exact release-date and latest-OS-target claims, and avoids unneeded volatile pricing. It states unknown cleanup approval granularity and feature areas as unknown rather than “No.”

The first visual is an original, accessible SVG decision aid based on documented behavior, not MacPilot UI or a tested workflow. The official Maintenance screenshot remains link-only because Koingo requires prior written consent; its contents, version, capture date and permission were not verified. The second visual is the October 21 first-party Space browser preview copied byte-for-byte from the screenshot library. Its caption discloses example data, source commit, and that it is not a native scan, measurement, cleanup result, or release-binary proof. Route-B visual review is still pending for the article context.

Only `/comparisons/` and `/tools/` hubs are linked internally; no claim is made that the draft comparison is a live destination. No separate alternatives article was requested or created. Existing evidence classifies MacPilot as adjacent, and the distinct replacement page should be skipped unless further retained evidence demonstrates several job-relevant alternatives; do not manufacture relationships.

## Checks and remaining review

- Confirmed frontmatter conforms to the marketing site's documented content schema and draft gate by reading `src/content.config.ts` and `docs/content-publishing.md`.
- Confirmed the article slug is unique in the blog collection at drafting time and canonical comparison record exists, but linked only live hubs.
- Confirmed the copied PNG matches the source SHA-256 recorded in `screenshots.json` (see receipt validation).
- Did not run `pnpm check`, build, tests, shared-site builds, browser preview, or responsive/theme checks because the job explicitly prohibits shared site builds and has no authorized isolated review fixture. No publication or independent review is claimed.
- Independent fact/visual/SEO/rendered review, site checks, route rendering, six-context browser review and publication approval remain pending. Recheck volatile claims before publication. Review SVG accessibility and mobile legibility in rendered context.
- The article contains no code execution or cleanup instructions; no app tests, installs, account activity, purchases, messages, or cleanup occurred.

## Exact output hashes

- Article SHA-256: `c199ac20db4173a57c652da5cf37162f522fe270bb15e9e4d6bced58890e72ee`
- Diagram SHA-256: `1e81eb9f415ff81e79cf87bf041e6b0986cb6e0605ae3ad6b69d146b8e7d5198`
- Copied Space preview SHA-256: `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a` (matches source library)

Any later edits require updating these hashes and repeating relevant review.
