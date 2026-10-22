# MacPilot tool-profile handoff

Task: `draft-tool-macpilot` · Drafted: **2026-10-22** · Outcome: complete internal textual draft with two built visuals; **not publication approval**.

## Owned outputs and exact snapshot

| Real file | SHA-256 |
| --- | --- |
| `/Users/gabe/code/breathing-room/website/src/content/tool-profiles/macpilot.md` | `5604d2e0ad70c9e33e7f1e9c9d54f01f291458b5258e4526d490e7fcc8cbbc58` |
| `/Users/gabe/code/breathing-room/website/public/assets/tools/macpilot/documented-scope.svg` | `94ba29f7ad2441a0bd44d4bf338b36672194542918e31dcc39c8a77a6d56ab6d` |
| `/Users/gabe/code/breathing-room/website/public/assets/tools/macpilot/change-review.svg` | `274d2a36c7827e7a927bc801f6bfd43053bde71f451b3f195f4d758beee7afce` |

This handoff is `/Users/gabe/code/breathing-room-app/docs/content/competitors/macpilot/tool-handoff.md`; its hash is recorded in the receipt diagnostic to avoid a self-referential hash. Receipt: `/Users/gabe/code/breathing-room-app/docs/content/.runtime/draft-tool-macpilot.1792640927283589000.receipt.json`.

Intended public route: `/tools/macpilot/`. Current state: `status: review`, `published: false`, date/updated `2026-10-22`. It has no public article route until separately approved. No shared schema, navigation, tests, queue, research packet or other product files were changed.

## Intent, evidence and exclusions

Search/reference track: neutral product identity, documented scope and licence/platform conditions. This is not a calculator, hands-on review, comparison, replacement shortlist or claim that we built MacPilot. The description is the lead; the body starts with a substantive visual. Affiliation is explicit. The body has five H2 sections and approximately 782 whitespace-delimited words including captions/HTML attributes (not a prose-only count). Title: 51 characters; description: 158 characters.

Read PLAN.md, October22 EDITORIAL.md update, capabilities.md, screenshots.json, research.json/.md and the applicable site publishing/schema/rendering files. No applicable AGENTS.md was found in the two trees or checked ancestor locations. Loaded blog-write, blog-seo-check, blog-factcheck, browser-automation and the adapted MailKite contract. No browser session or subagent was used.

Reused `docs/content/verification/batch-1.json` MacPilot record, the existing research claim ledger and retained official-page text. Official snapshot SHA-256 `e8b1fc6660c2e4ff38400a599849086b0d6410d83d64559408e1f03d1653d64c` and directory snapshot SHA-256 `7378cf6e1b3296fa20408224856807e9678a15457a6b25bdef1dc6ab22428760` were recomputed and match. No sources were refetched or relabeled as freshly retrieved. Frontmatter checked dates remain October21; October22 is the substantive drafting date.

Claim-level self-check against research.json:

| Draft material | Supporting retained claims | Treatment |
| --- | --- | --- |
| Koingo identity; settings, file/disk information; QuickLook and Launch Services | C01, C04 / S1 | Vendor-documented, not observed |
| Save Points/reset scope | C05 / S1, S4 | Settings only; no deletion rollback promise |
| 18.0.1, macOS13 minimum, vendor-wide current-app architecture statement | C02 / S1 | Attributed; no binary/Intel compatibility test |
| Release-date/latest-OS conflict | C03 | Exact dates and uncorroborated OS target omitted; bounded conflict disclosed |
| Proprietary licence; source repository unknown | C06 / S2 | No claim that a repository cannot exist |
| Subscription/current-version/lifetime-update offers; demo and Unlock menu | C07, C08 / S1 | Amounts omitted; currency/annual total/tax/renewal/trial conditions unknown; no permanent free-tier assertion |
| Admin/SIP boundaries | C09 / S4 | No bypass instructions; legacy/request content not promoted to current features |
| Offline/data/approval/helper/growth unknowns | C10, C11 | Explicitly unknown, not negative feature cells |
| Website-image restrictions | C12 / S3 | No copied or hotlinked imagery |

The old packet's image-only drafting prohibition is superseded by October22 policy for internal drafting, not edited away. MacPilot remains its canonical owner; “MacPilot18” is version naming. No verified cross-product alias calls for a skip file. No alternatives article was attempted; no peer relationships or rankings were manufactured. Other records remain outside this job. Internal links are only `/tools/` and `/tools/cache-rebuild-checklist/`, both implemented routes; no links to unpublished comparison/workflow/profile records.

## Route-B visual provenance and interaction pass

Both SVGs were authored for this task on October22, 2026. They are original editorial diagrams, **not app UI, screenshots, app tests, measured data or reproductions of vendor artwork**. Both are 520×570, vertically stacked task cards with opaque high-contrast colours, accessible title/description and adjacent page alt/caption. No logos, competitor image bytes, scripts or external embedded resources are present. Independent rendering/legibility review remains pending; XML validation is not visual approval.

- `documented-scope.svg`: supports C01/C04; groups settings, targeted maintenance and information. Exact basis: Koingo MacPilot product page, https://www.koingosw.com/products/macpilot/, retrieved October21, 2026. Card grouping and “size isn't deletion authority” are editorial organization/caution, not app controls. Caption attributes the official screenshot-gallery page without copying its restricted images.
- `change-review.svg`: informed by C02/C05/C09 and the editorial safety contract. Exact bases: the product page above and https://www.koingosw.com/products/macpilot/manual.php, checked October21, 2026. This is a reader checklist, not a verified app confirmation sequence. No claim about app-specific safeguards is inferred.

Reuse basis: original text/shapes authored in owned files for the requested page, with no third-party visual material. No blanket licence over Koingo assets is claimed. Provenance/privacy self-check: only generic documented task labels, no local files, private inventory or user data. Neutral-profile exception permits these decision aids without an irrelevant first-party app screenshot. The inventory's Breathing Room preview images were reviewed as provenance records but not copied; adding one here would unnecessarily turn the neutral profile into a comparison. No native-capture claim is made.

Interaction pass completed inline: the useful decision is separating settings from rebuild/removal and establishing support/recovery before acting. Implemented as the second static diagram plus a link to the existing non-scanning checklist. No new calculator, JavaScript, forced tutorial or account flow is warranted.

## Actual validation

- **PASS:** Node25 ad-hoc checks used installed `astro/zod` with the current schema field rules, YAML parsing, and the installed Astro Satteri Markdown processor. Frontmatter parses; date ordering passes; two figures, five H2s, zero body H1s; top visual present; both image references exist with nonempty alt; no TODO/TBD/internal-link placeholders or scripts. Markdown rendered to 6,868 bytes of HTML in memory, not a full site page.
- **PASS:** Imported actual `src/lib/publication.ts`; this record is excluded at both October22 and December1 dates. This unit check is not built-site leakage verification.
- **PASS:** Both internal hrefs correspond to inspected implemented routes. External citations were mapped to retained sources rather than live reachability checks.
- **PASS:** `/usr/bin/python3` parsed both SVGs as XML, checked viewBox/title/description, and found no embedded image/script elements. Recomputed all output hashes and both retained snapshot hashes.
- Earlier check attempts: legacy `@astrojs/markdown-remark` resolution failed because this installed Astro uses Satteri; switched to the installed processor without modifying dependencies. First render assertion mistakenly expected six H2s; corrected the assertion to the actual five and reran successfully. Homebrew Python XML parsing failed due to a pyexpat/libexpat symbol mismatch; the system Python XML check then passed. No environment/package changes were made.
- **NOT RUN (explicit job boundary):** shared `pnpm check`, `pnpm build`, `pnpm test`. No claims about current dist/, generated metadata, public links, sitemap/RSS or full-site regressions are made.
- **NOT RUN:** browser screenshots, responsive/theme review or native app/competitor testing. No screenshot UI, measured outcomes or app recovery were invented.

## Remaining independent review / release gates

1. Independently check prose and both diagrams against the retained official claim sources and exact hashes above. Review the age/legacy scope of the manual. Refresh volatile offer/platform statements within30 days and before publication if stale. Do not resolve conflicts by choosing convenient dates or guessing currency.
2. Arrange an isolated review fixture through the site owner; review at approximately390,768 and1440px in light/dark themes. Inspect text fit, both visuals, captions, links and keyboard navigation. There are no screenshots or browser approval artifacts from this job.
3. In a separately authorized serialized site job, run check→build→tests and inspect rendered canonical `/tools/macpilot/`, one layout H1, authorship/date/social metadata, Article/Breadcrumb schema and draft exclusion from routes/listings/RSS/sitemap. Do not publish a real fixture merely to preview it.
4. Independent itemized editorial score (content30/SEO25/evidence15/technical15/citation15) must reach85/100 with zero blockers. No score or reviewer approval is awarded by this drafting worker; technical/browser and independent-review gates remain pending.

The drafting task is done, but publication remains blocked on independent review and site/render checks. Missing optional prices, latest-OS targets and screenshot permission do not justify inventing claims or copying imagery. No purchase, account creation, message, credential access, cleanup, commit, push, deployment, shared build or queue/database mutation occurred.
