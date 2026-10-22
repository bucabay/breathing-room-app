# AmpleCapacity workflow blog handoff

Job: `draft-blog-amplecapacity` · prepared 2026-10-22 · internal review draft, not publication approval.

## Owned outputs and hashes

Marketing repository (`/Users/gabe/code/breathing-room/website`):

| File | SHA-256 | Purpose |
| --- | --- | --- |
| `src/content/blog/amplecapacity-mac-workflow.md` | `dfb6f22db4a1823a116fde63ca1c0b6dadb13b8fef8aa3bd207f1a222d134d73` | Complete review-state article; intended route `/blog/amplecapacity-mac-workflow/`. |
| `public/assets/blog/amplecapacity/recovery-vault-workflow.svg` | `ddcf4167a51e5b46d7c03bbc10f9aa31132f07f16fd5d4824635df5f6d1781d5` | Original editorial workflow diagram, not competitor UI or test output. |
| `public/assets/blog/amplecapacity/space-preview-2026-10-21.png` | `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a` | Unmodified copy of the retained first-party Space browser preview. |

The image matches `docs/content/screenshots.json` and `research.json`: captured from current source on October 21, 2026, example data only, not a native scan, measured activity, cleanup result, or proof of distributed-release parity. Its example-data banner is visible. The editorial SVG illustrates documented distinctions and is explicitly captioned as neither AmpleCapacity UI nor a test. Route B is used: retain the official AmpleCapacity results image as a link to its download page only; do not reproduce it because reuse permission, actual image bytes, privacy review, and provenance remain unresolved.

## Evidence reused and article boundaries

Reused, without repeating baseline fetches, `docs/content/verification/batch-1.json#amplecapacity`, the retained official homepage snapshot (`657c4a79ad9af82ecfaebf786b4d43fe5724666bec0cc8b1b193b2f056ecb4f7`), and `docs/content/competitors/amplecapacity/research.json` plus `research.md`. The official follow-up source pages and excerpts were retained October 21, 2026. Breathing Room boundaries come from same-day `docs/content/capabilities.md`; preview-image provenance comes from `docs/content/screenshots.json`.

The article teaches a concrete deadline workflow: distinguish candidate estimates, selected items, same-disk vault contents, and actual available space; then check backup, replaceability, and the applicable recovery window. The terms document seven days for ordinary vault moves and thirty days for Guardian-rule moves, but setup/execution and recovery guarantees were not tested. APFS estimates may read high. A vault move is not immediate free space or an independent backup. These are vendor-documented claims, not observations.

Preserved material unknowns/conflicts: AmpleCapacity exact version, minimum macOS, CPU support, and runtime requirements are unverified; vendor signing/notarization is attributed and no binary was inspected. Its privacy introduction says two network calls, its body lists three, and the policy discusses both offline activation and network validation. The article does not resolve call count or claim fully offline operation. Monitoring features are not discussed as absent. No install, scan, cleanup, purchase, account, message, benchmark, or binary inspection occurred.

Breathing Room is disclosed as built by us and explicitly bounded to the identified `0.1.0-preview.1` testing preview; source support is not binary parity. The draft retains macOS 13+, Python 3.10+ inventory prerequisite, non-Developer-ID/non-notarized disclosure, incomplete clean-machine and physical-Intel validation, and hosted AI authentication/network/data boundary. No savings, safety, speed, or parity claim is made.

## Intent separation and alternatives disposition

This `/blog/` page teaches a workflow, not the AmpleCapacity profile or head-to-head matrix. Existing separate records are `website/src/content/tool-profiles/amplecapacity.md`, `website/src/content/comparisons/amplecapacity.md`, and `website/src/content/alternatives/amplecapacity.md`; all are currently review/unpublished. The article links only to the live comparison and tools hubs plus the live storage headroom utility, not to those hidden review records.

No alias skip applies: the retained identity evidence does not verify an alias. No additional alternatives page was created. The existing alternatives record is already a distinct shortlist with job-relevant DaisyDisk (visual disk mapping), Mole CLI (developer-artifact maintenance), and CleanMyMac (broader care), supported there by retained official sources and explicitly not presented as AlternativeTo-verified relationships. Thus the alternatives intent is already covered in its own record; this workflow must not duplicate it. Confirm those peers' evidence/currentness independently before publication of that separate page.

## QA and remaining gates

- Article frontmatter uses the site's observed fields and remains `status: review`, `published: false`, dated 2026-10-22. No publication state or queue was changed.
- Source-adjacent links are included for material vendor claims. There are no fabricated statistics, app tests, FAQs/schema, benchmark claims, competitor screenshot copies, placeholder visuals, or links to unpublished records.
- Both visuals were read/inspected; the SVG is a real built artifact and the PNG's visible example-data banner was confirmed. The SVG still needs independent accessibility/legibility review in rendered site context; the PNG needs per-article crop/legibility review.
- **Not run by design:** shared website `pnpm check`, `pnpm build`, and `pnpm test`; no site build or shared tests were authorized for this scheduled drafting task. No rendered page, canonical/OG/schema output, draft-leak behavior, responsive browser layout, or light/dark rendering was validated.
- **Pending before publication:** independent factual and source-conflict review; verify current volatile details; review both assets and attribution/rights in the rendered page; validate metadata, static output, route, internal links and draft exclusion; perform required browser review at narrow/tablet/desktop and light/dark. No independent score awarded. The result is a complete textual draft, not a passed publication gate.
