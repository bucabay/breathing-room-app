# Blog draft handoff — 4DDiG Mac Cleaner / Tenorshare Cleamio

Prepared **2026-10-22** for task `draft-blog-4ddig-mac-cleaner`. This is a source-backed internal draft, not independent approval or publication. The historical `draftingAllowed:false` value in the research packet was solely the previous screenshot-rights gate; the October 22 editorial update permits drafting with route-B visuals. No competitor image was copied.

## Owned outputs and snapshot hashes

Marketing repository `/Users/gabe/code/breathing-room/website`:

| File | SHA-256 | Purpose |
|---|---|---|
| `src/content/blog/4ddig-mac-cleaner-mac-workflow.md` | `2d6fe1338fece11201fa625881f1f207e812a382f0294f7338fd2bb4ca3e1bfd` | Complete workflow article; `status: review`, `published: false`; public path when approved: `/blog/4ddig-mac-cleaner-mac-workflow/` |
| `public/assets/blog/4ddig-mac-cleaner/junk-review-flow.svg` | `895c90b81bb051accdfd365873b9d67f81672a59f5f2566e9894a4e8715c0223` | Original diagram of documented scan/review/cleanup sequence; explicitly not product UI or a test |
| `public/assets/blog/4ddig-mac-cleaner/review-checklist.svg` | `6cb5eba44ed48e6f82b431478b02b0ced4f569f83cbc9a17a91045e30192a84c` | Original owner/recovery/decision checklist; editorial aid, not Cleamio functionality |
| `public/assets/blog/4ddig-mac-cleaner/space-preview-2026-10-21.png` | `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a` | Unmodified first-party Space browser preview, reused from screenshot inventory; example data only, not native scan or measurement |

App repository `/Users/gabe/code/breathing-room-app`:

| File | SHA-256 | Purpose |
|---|---|---|
| `docs/content/competitors/4ddig-mac-cleaner/blog-skip.md` | `d23aa5467b671f81cdc7025d4b5604a9204fc748f7cff3761d9a58df91b5c5d7` | Prevents a second article for the verified Cleamio/current-destination alias; links the canonical workflow owner |

## Editorial and evidence decisions

- The concrete job is deciding what to inspect before Smart Cleanup, not a generic cleaner profile, head-to-head matrix, or replacement list. The article follows Tenorshare's guide sequence: Junk Files → Scan → review/choose → Smart Cleanup. It presents the decision questions as editorial guidance, not product controls.
- Identity, vendor claims and retained snippets are reused from `research.json`, `research.md`, `validation.json`, and `docs/content/verification/batch-1.json`; Breathing Room claims reuse `docs/content/capabilities.md` and `docs/content/screenshots.json`. Research retrieval was October 21, 2026; no needless refetch or app test was performed.
- **Source conflicts retained:** the Cleamio product page advertises a seven-day trial, while the purchase page lists promotional licence cards alongside a separately named 4DDiG File Repair trial and its renewal note. Cleamio trial billing, renewal amounts, and add-on default selection remain unknown. The article makes no price/trial recommendation. Cleamio's offline statement is explicitly attributed to the vendor and not generalized to AI data handling.
- Competitor screenshot rights remain uncleared under the retained terms evidence. Article links the official guide but uses original workflow/decision SVGs instead of copying or recreating the interface. The first-party image keeps its exact source and example-data disclosures; no crop or edit was made.
- Alternatives intent is already represented by `website/src/content/alternatives/4ddig-mac-cleaner.md` (not edited by this job). Its distinct replacement purpose is supported by retained product packets for CleanMyMac (broad maintenance), Mole (native app/CLI distinction), DaisyDisk (disk-map inspection), and AppCleaner (known-app removal). These are job-specific peers, not asserted direct substitutes in every dimension. No new alternatives page or duplicate was created.
- `blog-skip.md` maps the verified legacy 4DDiG URL/current Cleamio destination to this one canonical owner. Redirect evidence does not claim historical binary, feature, or licence equivalence.

## Checks actually performed

- Read the assigned editorial plan, October 22 editorial update, capability evidence register, screenshot inventory, retained research and validation records, relevant site schema/publishing instructions, existing workflow article pattern, and MailKite writing contract. No applicable AGENTS.md was found in the scoped trees.
- Python structural check passed: draft/review metadata and current date present; all three article figure references resolve to files; no unresolved internal-link placeholders; both SVGs contain accessible title/description wiring and complete SVG envelopes.
- `xmllint --noout` passed for both authored SVGs.
- SHA-256 of copied Space PNG matches screenshot inventory: `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a`.
- Node v25.0.0 and pnpm 12.14.0 are available. No shared site check/build/test or browser preview was run: this scheduled task explicitly forbids shared site builds, and the draft has no public preview route. A preliminary optional Python XML parser check could not run because the installed Python expat extension fails to load; the SVG XML check was then completed successfully with `xmllint`.
- The marketing working tree already contains unrelated changes and other workers' generated content. None of those files was edited or reverted by this job.

## Remaining review before publication

1. Independent factual/source-adjacent review of this exact article and current hashes; refresh mutable product/trial details before publication.
2. Independent visual/context review of both diagrams and the reused example-data preview; check the disclosure stays clear and layout remains legible on mobile, tablet and desktop, in light and dark themes.
3. Run the site's required `pnpm check`, `pnpm build`, then `pnpm test` in the serialized site-validation job; inspect generated metadata, canonical, schema, links, draft exclusion, and rendered assets. Do not publish until all independent evidence, visual, SEO and technical gates pass.

No queue/database state was changed. No purchase, account, message, cleanup, commit, push, deployment, or subagent activity occurred.
