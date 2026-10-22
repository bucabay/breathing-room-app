# Independent review — Top 10 Mac cleaners in 2026

**Review outcome: BLOCKED — retain `status: review`, `published: false`.** No publication score is awarded: mandatory technical/rendered gates failed before the current production-layout article could be inspected. This review does not change the article or its assets.

## Snapshot reviewed

- Article: `/Users/gabe/code/breathing-room/website/src/content/blog/top-10-mac-cleaners-2026.md`
- Article SHA-256: `525d629e214cb298ed0b32f97983d99c92a57f43c213ddf2311e6c71ef73dd8d`
- Route-B diagram SHA-256: `a93d5869ca96e4cb1fbf828973aa64dce01c925275e02ed5288d0fd439b29ef5`
- First-party preview SHA-256: `7adbafc5c0641c4ad7776cc98847224d8e772d5a8ed5b18a3fa5a353e1c61761`
- Reviewed the existing owned research extract and draft handoff; factual claims remain tied to source excerpts and prior verification dates. No needlessly repeated vendor research was performed.

## Independent content/evidence findings

- **Count and intent:** Ten table rows match ten numbered selections. macOS itself is explicitly counted as an option; the list is grouped by workflow, not presented as a measured ranking. Mole CLI/native app are distinguished as editions within one slot, not double-counted. Breathing Room is disclosed as the publisher's own preview.
- **Evidence and boundaries:** Article claims are generally stated as vendor-documented behavior rather than hands-on results. The text avoids unsupported savings/performance/safety claims, preserves unknown deletion/recovery behaviors, and includes relevant removal, rebuild, compatibility, pricing and edition caveats. Retained packet records support the specific feature/license/price claims described in the handoff; the article does not claim current exact competitor prices.
- **Free/licensing distinctions:** Mole's free GPL-3.0 CLI is separated from the proprietary native app; Pearcleaner is correctly described as source-available under Apache 2.0 plus Commons Clause rather than unrestricted open source; AppCleaner is not mislabeled open source. Breathing Room's free local core and paid hosted AI are separated.
- **Disclosure and advice:** Affiliation appears before the comparison table. Preview signing/notarization, runtime, hosted AI/sign-in/data and download-account limitations are disclosed. The removal advice is cautious and does not recommend bypassing system protections.
- **Visuals:** Route B is an appropriate documented-workflow diagram plus an attributed official-source link strategy; no competitor screenshots are copied. Both article images have descriptive alt text and nearby captions. The first-party image is correctly qualified as a dated, example-data browser capture, not a native measurement or current installer proof. Existing packet records preserve provenance and hashes. Visual legibility and actual production rendering remain unverified in this review.
- **SEO/content pass:** The title and description match the workflow-selection intent; the lead distinguishes editorial shortlist from leaderboard, headings are sequential, and internal links are useful. This is a source-level review only; canonical, social metadata, schema, draft non-leakage and rendered layout cannot be independently certified without a successful site build.

## Blocking validation results

Ran from `/Users/gabe/code/breathing-room/website` with the specified Node PATH prefix:

1. `pnpm check` — **failed** during Astro content sync. `alternatives → amplecapacity` has `sources.*.checked` parsed as objects where the schema expects strings (`src/content/alternatives/amplecapacity.md`).
2. `pnpm build` — **failed** on the same content-schema error before generating a production site.
3. `pnpm test` — **43 passed, 1 failed, 44 total**. The failed isolated publication-build test hit the same AmpleCapacity schema error. Its output explicitly reports that the draft/review/future publication-filtering fixture could not build.
4. Consequently, production-layout HTML/metadata/draft-exclusion inspection and the required owned-browser preview at mobile/tablet/desktop in light/dark themes were **not completed**. Prior draft-fixture screenshots are explicitly not production-layout evidence and predate the final article wording/hash.

These failures occur in a different, pre-existing roundup/alternatives content entry, not the reviewed article. No unrelated content, navigation, tests or shared code was edited to work around them. Fix the schema/data mismatch through its owner, rerun the full check → build → tests sequence, then independently inspect the built publication surfaces and current article/assets in an owned local browser before reconsidering approval. Recheck volatile offers and Breathing Room release disclosures before publication.

**Decision:** hard blocker under `docs/content/EDITORIAL.md` (unperformed/failed required checks and absent current-snapshot production browser review). Do not publish or change queue state.
