# Smart Cleaner AI workflow article handoff

Task: `draft-blog-smart-cleaner-ai-disk-clean`  
Drafted: 2026-10-22 (task date; source retrievals remain October 21 UTC)  
State: internal review draft; **not publication-approved**.

## Owned outputs

| File | Purpose | SHA-256 |
| --- | --- | --- |
| `/Users/gabe/code/breathing-room/website/src/content/blog/smart-cleaner-ai-disk-clean-mac-workflow.md` | Complete workflow article; public slug if approved: `/blog/smart-cleaner-ai-disk-clean-mac-workflow/` | `ddc307a41124c6a0107be303620d4ae804ee8849348777722c47cbe147bbd1af` |
| `/Users/gabe/code/breathing-room/website/public/assets/blog/smart-cleaner-ai-disk-clean/review-before-removal.svg` | Original source-backed decision aid; not product UI | `276da77900def6ac6fcbd700e85fa5ea655da072ae78ad70c6fb61deb642057a` |
| `/Users/gabe/code/breathing-room/website/public/assets/blog/smart-cleaner-ai-disk-clean/space-preview-2026-10-21.png` | Unchanged first-party Space browser preview copied from the screenshot library | `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a` |

The PNG hash matches `docs/content/assets/breathing-room/space-preview-2026-10-21.png` and the `screenshots.json` record `current-space-browser-preview`. Its required caption and example-data/native-test limitations are preserved. The SVG is an original editorial decision aid grounded in the documented duplicate, Xcode DerivedData, review, and Trash workflow; it is explicitly not a screenshot, app UI, test, safety score, or deletion instruction. These are route-B visuals. No Smart Cleaner AI image was copied, downloaded, hotlinked, or used as a visual.

## Evidence and editorial decisions

- Reused the retained product `research.json` / `research.md`, `validation.json`, baseline snapshot hashes, `capabilities.md`, and `screenshots.json`. No redundant broad refetch was done. AlternativeTo is cited only as discovery in the research packet, not as feature proof.
- The article teaches candidate-by-candidate review of exact duplicates and Xcode DerivedData, then distinguishes a scan from permission, Trash movement from recovered free space, and one-off cleanup from recurring-growth investigation. It is not a profile, comparison matrix, or hands-on walkthrough.
- Preserved the official conflict: the vendor page says app removal requires Pro; the US App Store description says app uninstalling is free. Article makes no claim about which tier is correct. Exact IAP amounts, version-date year, license/EULA, repository, completeness, and unverified monitoring/helper capabilities remain unknown or omitted.
- Disclosed the Breathing Room affiliation and the preview, Python, notarization/validation, hosted-AI/data, and daily-care limitations from the existing capability record. No performance, safety, savings, or product test claim is made.
- Only live internal hubs `/comparisons/` and `/tools/` are linked. Hidden review-state profile/comparison/alternative records are not linked.

## Alternatives and aliases

No second aliases are warranted: `Smart Cleaner AI`, `Smart Cleaner AI: Disk Clean`, and `Smart Cleaner AI - Disk Clean` resolve to the same store ID 6764714299 in the retained packet. No `blog-skip.md` was created because this canonical owner is the one requested and is not an alias of another product.

The marketing site already contains a separate review-state alternatives record at `/Users/gabe/code/breathing-room/website/src/content/alternatives/smart-cleaner-ai-disk-clean.md`. It is outside this task's ownership and was not edited. Its three job-relevant peers are grounded in existing research packets: Nektony's MacCleaner Pro (`docs/content/competitors/maccleaner-pro/research.md`), DaisyDisk (`.../daisydisk/research.md`), and FreeMacSoft AppCleaner (`.../appcleaner/research.md`). Those packets distinguish a broader cleanup suite, visual disk-map workflow, and known-app removal respectively; none is presented as a universal substitute. The existing alternatives record is therefore not duplicated and no alternatives exception/skip is needed.

## Validation and remaining review

Actual checks completed:

- Read task-required plan/editorial, capabilities, screenshot inventory, site publishing contract, source packet, and relevant blog-writing, SEO-check, fact-check, and browser-automation skill guidance. No applicable `AGENTS.md` was found in the checked scoped trees/ancestors.
- Confirmed draft frontmatter (`status: review`, `published: false`), date, author, title/description/source entries, target filename/slug, visual references, hub-only internal links, omitted restricted image URL, explicit uninstall conflict, and no-test disclosure with a read-only structural script; all checks passed.
- `xmllint --noout` on `review-before-removal.svg`: passed.
- Compared the copied PNG SHA-256 to the research/screenshot inventory record: exact match.
- Article length: 1,845 words including source ledger.

Not run by design: shared website `pnpm check`, build, tests, preview, or browser visual QA, per the task's prohibition on shared site builds and this job's scope. Independent factual, responsive/rendered visual, SEO, and publication review remain pending. The older image-rights-only `draftingAllowed:false` gate was not treated as a prohibition on this internal draft; competitor-image rights remain respected. Do not publish until required independent review and site checks are completed.
