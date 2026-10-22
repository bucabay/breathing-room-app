# MacSweep comparison draft handoff

Task: `draft-macsweep`. Prepared **2026-10-22 UTC**. Outcome: **complete internal comparison draft**, not publication approval. Public path when approved: `/comparisons/macsweep/`. Frontmatter is `status: review`, `published: false`.

## Exact outputs and SHA-256

| File | SHA-256 |
| --- | --- |
| `/Users/gabe/code/breathing-room/website/src/content/comparisons/macsweep.md` | `c1ca9acdacdb3b012fb8542ce9e9f2950ca6d3804e05701da340b2d450798e04` |
| `/Users/gabe/code/breathing-room/website/public/assets/comparisons/macsweep/decision.svg` | `2135c0cc2c9aaccbd24184d3761571b0aa3cc940432ed6df518c2150ee061505` |
| `/Users/gabe/code/breathing-room/website/public/assets/comparisons/macsweep/space-preview-2026-10-21.png` | `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a` |

This handoff: `/Users/gabe/code/breathing-room-app/docs/content/competitors/macsweep/comparison-handoff.md`. Its hash is recorded in the receipt rather than self-referenced here. Receipt: `/Users/gabe/code/breathing-room-app/docs/content/.runtime/draft-macsweep.1792630777985218000.receipt.json`.

## Intent, evidence and policy decisions

- One search/reference head-to-head page, not a neutral tool profile, replacement roundup or workflow tutorial. It contains a fact matrix, concrete MacSweep strengths, bounded Breathing Room advantages, explicit unknowns, reasons not to use our preview, and a four-step decision aid. No alternative-products page was created or another queue job undertaken; the several-peer requirement belongs to that separate intent.
- Read PLAN, October22 EDITORIAL, capabilities, screenshots, research.json/.md, source-excerpts, baseline official snapshot, website schema/publishing contract and MailKite contract. Loaded blog-write, blog-seo-check, blog-factcheck and browser-automation. Comparison template adapted under the local editorial override: no automatic winner cells, benchmark quota, fabricated experience, forced code or FAQ.
- No AGENTS.md found in checked ancestors or the applicable app docs/marketing website trees. Existing unrelated website changes were inspected with `git status --short` and preserved.
- Canonical identity remains MacSweep at arkenage.com. Retained research establishes a distinct product and no verified alias; no skip file or duplicate canonical page warranted. Website/distribution source is not called desktop source, and its MIT README is not treated as the desktop licence or image clearance.
- Reused October21 evidence dates without freshening them. Source-adjacent citations refer to retained vendor documentation and first-party source/disclosures, not newly executed binary tests. No binaries downloaded or tested.
- The old image-only drafting restriction is superseded by October22 route B. Annual effective pricing remains unresolved: the prose explicitly explains the visible promotion versus June30 metadata expiry and declines a cheaper-product verdict. Unknown approval flow, runtime, licence, free module identities, Pro terms, grouping and recurring monitoring are not converted to negative claims.

### Claim crosswalk to retained research.json

| Draft location | Retained claims / supporting register |
| --- | --- |
| Identity and evidence note | M01; research identity/discovery; source-excerpts repository |
| OS / installation / licence rows and strengths | M02, M03, M10, M11, M12, BR01; capabilities preview/install register |
| Cleanup / developer rows and discussion | M04, M05, M06, M08, M12, BR02; capabilities Space, developer and approval rows |
| Activity / helper / recurring growth | M12 explicitly unknown; BR02; capabilities Apps/Activity and sampled-attribution limitations |
| Local / hosted / account boundary | M07, BR03; capabilities local-hosted and access register; no inference about Pro activation |
| Free / paid scope and annual-price conflict | M08, M09, BR03; source-excerpts English offer and failed purchase-page retrieval; capabilities pricing caveats |
| Interactive approvals, optional Ruff mode and daily runtime | BR02; capabilities approval exception sections 1–3 and daily-runtime row |
| Diagram and decision aid | Editorial synthesis of those supported scopes, not a product test, substitute UI or safety certification |

## Route-B visual provenance

1. **Original decision diagram**: `decision.svg`, 640 × 820, authored for this comparison on October22. Dark fixed background and light labels are self-contained. Captions name MacSweep's official English page and Breathing Room source/README. Claims: M04/M07/M08 and BR02/BR03. It contrasts reader jobs, not exclusive product feature sets; the caption explicitly says MacSweep monitoring is unknown. No competitor UI, logo, screenshot pixels or external embedded image was copied. This original editorial artwork may accompany the owner-requested draft; independent typography/mobile and claim review remains pending. SVG has title, description and image alt/caption. XML parsing is not a visual legibility approval.
2. **First-party Space illustration**: unedited byte-for-byte copy of `/Users/gabe/code/breathing-room-app/docs/content/assets/breathing-room/space-preview-2026-10-21.png`, manifest ID `current-space-browser-preview`; 2940 × 3468, capture `2026-10-21T19:06:45.416416+00:00`, source revision `54828ac3170b45861aee70861dd0b9c658ed7e51`. Source and output hash match above. Owner-requested first-party example-UI reuse basis from screenshots.json; no blanket image/trademark licence inferred. Original manifest privacy review says built-in example data only. The actual PNG was opened and read during this job: example-data banner, Space category view/tabs and floating composer visible. No crop or altered numbers. Caption identifies capture date/revision, example-only data and non-native/non-release-parity limits. Its full-page density/composer overlap needs independent contextual/mobile review before publication.
3. **MacSweep official image** remains link-only: `https://arkenage.com/img/screenshot-hero.png`, credited to Arkenage in prose. The existing packet retains its provenance and rights conflict. Not downloaded, copied, hotlinked as an image, redrawn or independently pixel-reviewed; no reuse permission or capture date invented. Route B does not require sending a permission request.

## Actual validation and SEO review

All checks below were performed on October22. No shared build, generated website state or publication fixture was used.

- **PASS retained evidence hashes**: Python hashlib matched directory snapshot `e30ba2239727b94ac977c56068e23eccb48ee56fa5fbfbdaf7723e89de429e78`, official snapshot `d136dd9da80355cf90d5696dfa900b68fef19d85c12c2f20b69527324aadd5a0`, and source-excerpts `79ca914fe3a3e6de7136cf638cd779cc5d38170addda1b21c402278edde64abb` to research.json. PNG matched the retained screenshot record before copying.
- **PASS exact installed content schema and draft exclusion**: Node v25 with `/Users/gabe/.nvm/versions/node/v25.0.0/bin` prefixed to PATH parsed frontmatter using Astro's installed `@astrojs/internal-helpers/frontmatter`, evaluated the exact schema expression from `src/content.config.ts` with `astro/zod`, and invoked the real `src/lib/publication.ts` predicate. Schema accepted; review/unpublished record excluded; date/updated October22; all eight source entries accepted. No source schema was edited.
- **PASS source SEO/structure checks**: final title 53 characters, description 160; unique title and description against 63 other comparison records present at final check (concurrent workers may add records). Five H2s, one fact matrix, no body H1/heading-level skip, two figures, first body element is a figure, both image alts/captions present, no TODO/TBD/image/internal-link placeholders. Rough whitespace body count 1,355 including table/markup. The lead states the decision; body continues with affiliation/method rather than duplicating it. Repeated official URLs are intentionally retained as claim-adjacent citations, not SEO link stuffing.
- **PASS asset checks**: final `/usr/bin/python3` script parsed SVG XML, checked title/desc, no script/external-image elements, actual PNG header dimensions, image file existence, owned asset paths, matrix/heading counts, alts and only two internal hub destinations. Final hashes above were calculated from actual bytes.
- **PASS live hub checks**: WebFetch returned readable public `/comparisons/` and `/tools/` content on `https://breathing-room.chatic.ai/`. These are the only final internal destinations. A preliminary link to `/tools/cache-rebuild-checklist/` returned HTTP404 despite local implementation; it was removed. No hidden competitor/tool/workflow record is linked.
- **Not a new network fact-check**: material product facts were checked against the retained supported excerpts and capability register, as requested, not refetched wholesale. No benchmarks, copied competitor pixels, app execution or newly tested commercial terms claimed.

### Failed preliminary checks, retained honestly

- `python3 -c 'import yaml'` failed: PyYAML unavailable. No package installed; final parsing used Astro's installed parser.
- An optional in-memory Markdown-render attempt failed because this Astro installation cannot resolve `@astrojs/markdown-remark`. No HTML was generated and no rendering pass claimed.
- First structural script expected six sections; actual intended count is five. Corrected the check, not the article to satisfy an arbitrary quota.
- Homebrew Python3 XML parsing failed because pyexpat could not resolve `_XML_SetAllocTrackerActivationThreshold` in system libexpat. The same final XML/asset checks passed under existing `/usr/bin/python3`; no settings/installations changed.

## Remaining independent review gates

1. Independently check the exact draft/asset hashes, factual support, pricing conflict treatment and all caveats. Refresh volatile facts before release when necessary. The historical packet's annual-price blocker is not resolved; it is explicitly bounded in the draft, not used as a payable-price recommendation.
2. Arrange an isolated authorized review fixture through the site owner. This hidden review record has no public route. Do not flip publication flags merely to preview it.
3. Run the authorized site check/build/test sequence in a separately serialized site job. **Not run here** because the user forbids shared builds. Confirm canonical, H1, author/date, OG/Twitter, Article/Breadcrumb schema and exclusion from routes/feeds/sitemap on that built snapshot. Source-level schema/predicate checks are not an end-to-end rendering claim.
4. Inspect diagram, screenshot density, matrix overflow and captions at approximately390/768/1440px in light/dark themes, including keyboard/link checks. No page-browser session or screenshot of a rendered article was obtained in this drafting job. The browser skill was loaded; no Chrome recovery/profile action was needed.
5. Complete independent editorial scoring against Content30/SEO25/Evidence15/Technical15/Citation15, requiring85+ and zero blockers. No independent reviewer or numerical approval is fabricated here. These gates remain pending and keep the page unpublished; they do not prevent delivery of this complete source-backed draft.

No purchase/account/message, cleanup, credentials, system settings, commit/push/deployment, subagent, queue/database update, shared nav/schema/test change or other competitor output was performed.
