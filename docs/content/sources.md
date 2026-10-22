# AlternativeTo source discovery

## Live browser discovery completed — 2026-10-21

The approved browser profile was restored with the documented launcher from `/Users/gabe/code/indeed-apply/scripts/run_pipeline.py:39–49`, after confirming no listener existed on port 9333. The existing `~/.chrome-indeed-automation` profile was used; no new profile or job-application campaign was started. DevTools connected, and a new owned background tab was used. AlternativeTo showed the existing signed-in `bucabay` account; no login, contribution or account change was performed.

**Confirmed relationships:** [Breathing Room's own listing](https://alternativeto.net/software/breathing-room/about/) states “bucabay added Breathing Room as alternative to CleanMyMac and Mole.” Its [two-item alternatives page](https://alternativeto.net/software/breathing-room/) confirms both. The prior DaisyDisk candidate was incorrect as a seed; DaisyDisk does appear downstream in Mole's list.

| Confirmed seed | First page | Last page | Observed listing count |
| --- | --- | --- | --- |
| CleanMyMac | https://alternativeto.net/software/cleanmymac/ | https://alternativeto.net/software/cleanmymac/?p=10 | 113 |
| Mole | https://alternativeto.net/software/mole/ | https://alternativeto.net/software/mole/?p=9 | 101 |

Traversed all **19 pages** through observed next/pagination links in the rendered browser. Last pages had no next link. Deduplicated responsive duplicate cards and repeated products by exact listing URL: **151 identities including Breathing Room, 150 competitor listing identities after excluding our own product**. This is not a claim of 150 independent vendors, relevant Mac-native replacements, or publishable posts. Official-source verification, platform classification, screenshot permissions and vendor-alias review remain per-product research work. PowerMyMac / iMyMac - PowerMyMac is one suspected alias requiring review.

`competitors.json` now contains the full discovery manifest, page URLs, retrieval timestamps, raw-capture SHA-256 hashes, rendered product excerpts, all seed edges, and explicit publication-ineligible states. `CONTENT-CHECKLIST.md` lists all 150 research items. Raw captures remain local under `.runtime/`; `scripts/build-alternative-manifest.py` checks page completeness/counts and regenerates the records from those captures. No capability, price, licence or platform assertion is approved solely from directory text.

## Historical blocked attempt (superseded for browser access and seed discovery)

The following records preserve the earlier failure evidence. They do not describe current browser access or current discovery counts.

Retrieved: **2026-10-21**. Job: `sources`. Historical status: **blocked**. These are research records, not publishable comparison claims.

## Result

**0 of 2 published Breathing Room relationships confirmed; 0 verified eligible competitors.** The two placement URLs remain unknown. CleanMyMac and DaisyDisk are candidate seeds only, not confirmed placements. No complete alternatives page was retrieved. Four distinct names observed in current search snippets are retained separately in `competitors.json`; none is admitted to the eligible manifest. The verified count is 100 below the aspirational 100-product target, not proof that fewer than 100 relevant products exist.

## Local provenance

- Read `PLAN.md` and `research-handoff.md` in this directory before creating these outputs. The handoff explicitly says the two placements remain unresolved and identifies the two URLs below as candidates only.
- Searched both `/Users/gabe/code/breathing-room-app` and `/Users/gabe/code/breathing-room` for `AlternativeTo` / `alternativeto.net`. The marketing repository search returned no matches; the app matches were the plan, queue task description and handoff, not publication records. Search covered ordinary non-ignored files, not credentials, ignored build outputs or private browser data. Absence here does not establish that no placement exists.
- Read `/Users/gabe/code/breathing-room/docs/gtm-playbook.md`, especially lines 29–36: it names DaisyDisk, CleanMyMac and Mole as market alternatives, with official vendor links, but does not establish any AlternativeTo relationship.
- No `AGENTS.md` found in either scoped repository subtree or in their ancestor directories; none found in the marketing docs subtree.

## Public retrieval ledger

Every URL below was attempted with `webfetch` on **2026-10-21**. Every response was **HTTP 403**, with no listing content returned. Preserve URL spelling, trailing slash and query parameters as attempted; do not mistake these for verified canonical URLs.

| Exact URL | Role | Outcome |
| --- | --- | --- |
| https://alternativeto.net/software/cleanmymac | Candidate seed from handoff | 403 |
| https://alternativeto.net/software/daisydisk | Candidate seed from handoff | 403 |
| https://alternativeto.net/software/cleanmymac/?p=7 | Search-discovered pagination | 403 |
| https://alternativeto.net/software/cleanmymac/?p=8 | Search-discovered pagination | 403 |
| https://alternativeto.net/software/cleanmymac/?p=9 | Search-discovered pagination | 403 |
| https://alternativeto.net/software/daisydisk/?p=7 | Search-discovered pagination | 403 |
| https://alternativeto.net/software/daisydisk/?p=10 | Search-discovered pagination | 403 |
| https://alternativeto.net/software/daisydisk/?platform=mac | Search-discovered filtered listing | 403 |

Chrome DevTools `list_pages` failed twice (initial check plus one retry): `Could not connect to Chrome. Check if Chrome is running. Cause: Failed to fetch browser webSocket URL from http://127.0.0.1:9333/json/version: fetch failed`. No browser tab was created, inspected or changed. Browser work stopped; ordinary public search/fetch evidence above is explicitly distinguished from live browser verification. No challenge bypass or alternate browser profile was attempted.

## Search provenance (2026-10-21)

Queries and pertinent raw excerpts returned by public web search:

1. `site:alternativeto.net "Breathing Room" mac` — only an unrelated HelioPeak result; no placement confirmation.
2. `"Breathing Room" "AlternativeTo" cleaner` — unrelated results; no placement confirmation.
3. `site:alternativeto.net/software/ "breathingroom"` — unrelated HelioPeak, Actor AI Assistant and Weel ADHD Planner results; no placement confirmation. These are not competitors and are excluded from the manifest.
4. `site:alternativeto.net/software/cleanmymac/ "alternatives" "page"`:
   - `https://alternativeto.net/software/cleanmymac/?p=7`: “Is Disk Mop a good alternative to CleanMyMac? You are at page 7 of CleanMyMac ...”
   - `https://alternativeto.net/software/cleanmymac/?p=8`: “Is Glary Disk Cleaner a good alternative to CleanMyMac? You are at page 8 of ...”
   - `https://alternativeto.net/software/cleanmymac/?p=9`: “Is Glary Disk Cleaner a good alternative to CleanMyMac? You are at page 9 of CleanMyMac alternatives.”
   - `https://alternativeto.net/software/cleanmymac/?platform=windows`: “12 of 30 CleanMyMac ...” This is indexed text, not a verified total.
5. `site:alternativeto.net/software/daisydisk/ "alternatives" "page"`:
   - `https://alternativeto.net/software/daisydisk/?p=7`: “Is dut a good alternative to DaisyDisk? You are at page 7 of DaisyDisk alternatives.”
   - `https://alternativeto.net/software/daisydisk/?p=10`: “Go to first page of DaisyDisk alternatives · ❮1…910.”
   - `https://alternativeto.net/software/daisydisk/?platform=mac`: “Is OmniDiskSweeper a good alternative to DaisyDisk? 12 of 65 DaisyDisk ...”
   - Also surfaced `https://alternativeto.net/software/daisydisk/?platform=windows`, `https://alternativeto.net/software/daisydisk/?platform=linux` and `https://alternativeto.net/software/daisydisk/?license=free&platform=mac`; these were not fetched and do not establish additional edges here.

Search snippets can be stale, incomplete or inconsistent (Glary appears on two different page numbers). They are discovery hints, not live listing verification, capability evidence, canonical identity evidence or reliable totals. The search integration did not expose a shareable search-results URL; exact queries and returned source URLs are preserved instead. The handoff's older name list is not imported as freshly retrieved evidence.

## Pagination, deduplication and classification

Pagination traversal was **attempted but blocked**, not completed. Search exposed the numbered URLs recorded above; direct fetch of each returned 403. There was no readable first page or next-page control, so no reliable full chain, last page or exhaustion condition could be established. Gaps were not invented or marked traversed. A page-10 snippet does not prove a ten-page exhaustive set. Confirm the actual two seed URLs before expanding either candidate.

The eligible `competitors` array is empty. Four snippet-only leads are name-deduplicated separately: Disk Mop, Glary Disk Cleaner, dut and OmniDiskSweeper. Glary's two exact discovery edges are retained on one record. Their canonical product URLs and direct/adjacent/irrelevant classifications remain **unverified**. No product was labelled dead without evidence. Unrelated search hits are recorded above as exclusions, not as competitor products. Future eligible records must be merged by observed canonical product identity, retaining all seed/page edges and dates; do not count aliases, variants or repeated pages as distinct products.

## Blocking evidence and resume requirements

1. **Seed identity:** obtain the two exact public placement/relationship URLs or a marketing publication record that identifies them. Neither candidate may silently substitute for them.
2. **Access:** restore the approved Chrome endpoint or obtain readable public listing access without bypassing gates. A 403 is an access blocker, not evidence of absence.
3. **Enumeration:** from the confirmed seeds, traverse observed pagination until exhausted; retain each exact listing/edge URL and retrieval date, deduplicate by verified canonical identity, and document excluded/dead products with evidence.
4. **Eligibility:** verify platform/workflow relevance before assigning direct or adjacent status. Directory discovery alone is not proof of current product capabilities.

No drafts, queue state, website files, deployment or publication were changed. These source outputs do not authorize downstream publication or establish completion of C01/C02/C08.
