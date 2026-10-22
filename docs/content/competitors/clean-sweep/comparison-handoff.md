# Clean Sweep comparison draft handoff

Task: `draft-clean-sweep` · Drafted and checked: **2026-10-22 UTC**.

## Outcome and scope

Completed one search/reference comparison at `/Users/gabe/code/breathing-room/website/src/content/comparisons/clean-sweep.md`. Intended public path: `/comparisons/clean-sweep/`; **not a currently public article**. Frontmatter remains `status: review`, `published: false`, with current creation/update dates and Breathing Room team authorship.

This is an adjacent-product decision: Clean Sweep's documented personal-library tools versus Breathing Room's broader storage/activity investigation. It is not an alternatives list, neutral tool profile or deletion tutorial. No other page family was created. Canonical owner is `clean-sweep`; the Photo Cleaner and Phone Cleaner names share App Store ID 6449146108. No alias skip file is warranted for this canonical task, and no relationship to PowerMyMac is asserted.

Read PLAN, EDITORIAL including the October22 override, capabilities, screenshots, existing research JSON/Markdown, verification/batch-2.json, site schema/publishing rules and the MailKite contract. Loaded blog-write, blog-seo-check, blog-factcheck and browser-automation. No applicable AGENTS.md was found in either scoped tree or checked ancestors. Existing unrelated changes were preserved.

## Exact outputs and SHA-256

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `/Users/gabe/code/breathing-room/website/src/content/comparisons/clean-sweep.md` | 13011 | `0b200aaae7fde3d29630f5aee2f8347f24d508fb70a977e3359b2459328abf42` |
| `/Users/gabe/code/breathing-room/website/public/assets/comparisons/clean-sweep/choose-the-job.svg` | 2301 | `084023cefd3d9ce65dd579bedbc9d9bd996a032716cd172cad5564b2b12bea62` |
| `/Users/gabe/code/breathing-room/website/public/assets/comparisons/clean-sweep/space-preview-2026-10-21.png` | 587216 | `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a` |

This handoff is also an owned output: `/Users/gabe/code/breathing-room-app/docs/content/competitors/clean-sweep/comparison-handoff.md`. Its final hash is recorded in the job receipt diagnostic rather than creating a circular self-hash.

## Evidence reuse and claim review

No blanket refetch or new app test was needed. Research packet claim IDs C1–C3, C5–C7 and B1 underpin the page; C4's abbreviated version date was unnecessary and omitted. The baseline's iPhone-only platform summary was **not** adopted: the later research packet preserves the Mac compatibility detail and explicit vendor documentation.

Recomputed these retained file hashes; all match research.json and batch-2.json:

- `docs/content/.runtime/verification-2/clean-sweep-directory.json`: `727d6ac7eff77c9ff18e22138cc91c17e0fa9d529ce09279b0fe6b90531a4bf5`.
- `docs/content/.runtime/verification-2/clean-sweep-official.json`: `5757f8ed6fa051f8f75b24a78225de47a393c9e2ec20ee911a2002568cdff869`.
- `docs/content/.runtime/verification-2/clean-sweep-extra.json`: `03164ab4480dd85358c3f694b1b9f1607771c12309b4d0d25f06a44e50be39c0`.

All source retrieval/check dates remain **October 21**, not silently refreshed to the draft date. Read the retained homepage and store text and rechecked substantive store passages (whitespace-normalized): macOS 13.0/M1, contradictory phone-only and macOS-unverified labels, $3.99/month, $12.99/year, both $14.99/$19.99 lifetime entries, duplicate-contact merging, Data Not Collected and Apple's non-verification warning. Official docs excerpts for cross-device restoration and Family Sharing are retained in research.md; sharing remains qualified by the store's “some purchases” wording.

The matrix and prose explicitly preserve:

- Documented Mac availability, **not** a verified native Mac interface or installation; no Intel support inference for Clean Sweep.
- Both lifetime amounts; no guaranteed active offer, free quota, tax, trial or renewal claim for Clean Sweep.
- Local-data statements as vendor/developer declarations, not privacy audits.
- Unknown Clean Sweep approval/recovery/sync behavior, app-source licence, helper grouping, disk-growth and developer-cache features, never unsupported “No” cells.
- Breathing Room free local core versus paid advertised AI Care; authenticated hosted data boundary, source-versus-release limitation, Python prerequisite, non-notarized preview and incomplete clean-machine/physical-Intel QA.
- Exact-action approvals with the narrow optional automatic Ruff exception, and daily-care running-app constraint. No measured savings, benchmark or safety guarantee.

## Visual provenance: approved route B

1. **Original decision diagram**, `choose-the-job.svg`, 540 × 760. Authored for this page on October 22 from C2/C3 and B1/documented desktop scope. It separates personal-library work, broader Mac investigation and the recovery/approval stop condition. It is expressly labeled a diagram, not competitor UI or a test. No copied third-party imagery, logos, fonts, external resources or generated app screen. Native SVG title/description, explicit image alt and source-adjacent caption included. Structured fixed dark palette with light text; narrow-screen legibility still needs rendered review. Original and final are the same file/hash; no capture date, product version or measured data applies.
2. **First-party Space browser preview**, copied byte-for-byte from `docs/content/assets/breathing-room/space-preview-2026-10-21.png`, screenshot ID `current-space-browser-preview`. Captured `2026-10-21T19:06:45.416416+00:00`, source commit `54828ac3170b45861aee70861dd0b9c658ed7e51`, local source URL `http://127.0.0.1:1431/`, 2940 × 3468. Original/published hash both `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a`. No edits/crop/redactions. Existing first-party app-owner-requested reuse and example-data privacy review are reused from screenshots.json, not a new independent approval. Third-party marks remain their owners' marks. Opened and read the actual PNG in this job: example-data banner remains visible, Space tabs visible, floating assistant overlaps part of chart. Caption discloses capture date, illustrative data, browser-only scope and no measured result. Not evidence of current distributed-release parity.
3. **Clean Sweep image is not reproduced or hotlinked.** Its rights remain link-only under the existing packet. The top figure instead provides an attributed text link to the official product illustration page and docs. No permission request, image download, screenshot UI assertion or reuse-rights claim was made. The historic packet's image-only drafting blocker is superseded for this internal draft by EDITORIAL's October22 route-B policy; research files remain unchanged.

## Actual validation outcomes

- **PASS**: isolated Node YAML parsing and schema-equivalent Zod validation using installed dependencies and the current schema's field/refinement rules. Dates, source URLs and checked-date format valid. The actual `src/lib/publication.ts` predicate returns false for this record. This is not a built-site leakage test.
- **PASS**: isolated installed Astro Markdown processor rendered the body in memory: 12,912 HTML bytes, six H2s, one fact table, two figures, no body H1. No shared build/cache/route fixture was created.
- **PASS**: both referenced image files exist and have nonempty descriptive alt text. XML parse validates SVG title/description and no external resources; PNG dimensions and source-copy hash match.
- **PASS**: title 52 characters; description 150 characters; seven frontmatter sources; approximately 1,369 whitespace-delimited body tokens including markup/table links. Natural title/description, no artificial statistic or power-word quota.
- **PASS, source-level only**: all four internal links have existing page sources: `/download/`, `/privacy/`, `/tools/cache-rebuild-checklist/`, `/comparisons/`. No links to hidden competitor/profile/workflow drafts. Known hubs/utilities only, not an assertion of new live HTTP testing.
- **PASS**: first body element is a useful figure; no public placeholder tokens; bounded marketing-language lint clear. Citations intentionally repeat beside table/prose claims, prioritising local evidence over generic link-dedup advice.
- **PASS**: baseline hash checks and substantive retained-store-text checks described above.
- Initial validation attempts were corrected, not concealed: the first Markdown assertion incorrectly expected seven H2s (there are six); a Python 3.14 XML check could not load system expat; system `/usr/bin/python3` succeeded. An initial exact-string source assertion missed nonbreaking spaces; whitespace-normalised source checks then passed. No package install or system change was used.

Commands used Node at `/Users/gabe/.nvm/versions/node/v25.0.0/bin/node` with `--experimental-strip-types --input-type=module` for in-memory YAML/Zod/render/publication checks, and `/usr/bin/python3` for XML, PNG, source-excerpt and hash checks. Results above are retained here; no separate unowned log or preview artifact is claimed.

## Interaction pass and remaining review gates

The highest-value interaction is classifying the target **before** authorising changes. Implemented a top decision diagram and final four-step non-destructive decision checklist. No forced code demo, upload, scanner, cleanup or savings calculator is needed for this comparison. The existing cache/rebuild checklist is the optional next step.

Drafting is complete; publication is **not approved**. Independent factual, visual, SEO and rendered-page review remains pending against the exact hashes above. No 85/100 pass is awarded: content quality, SEO, evidence, technical and citation-readiness scores must be independently assessed; unperformed technical/browser gates receive no verified credit.

Remaining items:

1. Arrange an isolated authorised review fixture without weakening the draft filter. Inspect both figures and the wide fact table at about 390/768/1440px in both themes, including caption legibility and image loading. The full-height first-party image may require a separately approved contextual crop after review; don't remove example-data disclosure.
2. Site owner runs serialized `pnpm check`, `pnpm build`, `pnpm test` and verifies canonical `/comparisons/clean-sweep/`, metadata, author/dates, Article/Breadcrumb schema and draft exclusion from routes, listings, RSS and sitemap. **Not run here**, per this job's shared-build prohibition. Isolated Markdown rendering is not a replacement for these checks.
3. Refresh volatile availability/pricing before publication when overdue (at least every 30 days). Preserve or resolve the store platform-label conflict; verify actual offer/device fit before any recommendation to install. Exact deletion/recovery/sync questions must be answered before adding procedural library-cleanup advice.
4. Independently review source-versus-binary boundaries and route-B visual context. Competitor image clearance is needed only if replacing the diagram route with copied competitor UI; the current draft contains none.

No browser session or native app was launched. No account, purchase, message, credential access, cleanup, subagent, shared nav/schema/test edit, queue/database update, commit, push or deployment occurred. Receipt completion means the owned comparison draft and handoff exist and passed the scoped checks, not that the page is published or release-ready.
