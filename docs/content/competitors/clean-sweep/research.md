# Clean Sweep research: adjacent, drafting blocked

Clean Sweep is Indie Goodies' photo/video/contact cleaner, identified by App Store ID **6449146108**, not a PowerMyMac alias. It is **adjacent**, not a verified replacement for general Mac storage/activity investigation. Research reuses the current batch-2 records rather than repeating discovery. **No article, site record or publication approval was created.**

## Decision and canonical identity

- `canonicalOwnerId: clean-sweep`. Homepage: <https://indiegoodies.com/cleansweep>.
- The homepage title “Clean Sweep - Photo Cleaner” and store title “Clean Sweep - Phone Cleaner” refer to the same app through reciprocal links. Skip separate alias drafts. Do not merge with similarly named cleaners or PowerMyMac without evidence.
- Store seller: Khuong Pham; copyright Indie Goodies Lab. The homepage links the IndieGoodies GitHub organisation, **not an established app-source repository**. The screenshot-hosting repository is not product source.
- No dead-product exclusion: retained store version history lists 1.8.3, “Oct 12”; the latest entry does not print a year. No binary was installed.
- No platform-only exclusion: the baseline summary omitted a material Mac compatibility passage. It must not be repeated as proof of iPhone-only support.

## Reused evidence and platform conflict

Claim IDs, URLs, exact excerpts, timestamps and SHA-256 values are in `research.json`. Baseline source files were read and their **file hashes checked against batch-2**:

1. Discovery about page → official homepage: `clean-sweep-directory.json`, retrieved 2026-10-21T19:07:30.219Z. Existing manifest records discovery from Mole page 7, retrieved 18:37:22.582Z. This is an AlternativeTo relationship, not a capability endorsement.
2. Official homepage snapshot: `clean-sweep-official.json`, retrieved 19:10:00.293576 UTC. Supports similar photos/videos/contacts, lifetime offer and attributed local-data wording; excludes testimonial savings and safety assertions.
3. US App Store snapshot: `clean-sweep-extra.json`, retrieved 19:13:59.139457 UTC. Supports seller, listed requirements, version and IAP amounts. Store declarations are not hands-on tests.

All three are under `docs/content/.runtime/verification-2/`. The packet preserves existing dates, not a fresh “verified today” stamp. UTC shell clock returned October 21 while session calendar says October 22; new targeted checks are recorded with actual UTC date.

**Conflict:** The store headline says “Only for iPhone” and “Designed for iPhone. Not verified for macOS.” Its Compatibility section nevertheless says “Mac Requires macOS 13.0 or later and a Mac with Apple M1 chip or later.” New official documentation explicitly lists Mac availability. Editorial resolution: say **documented Mac availability with M1+/macOS 13+ listing requirements; native Mac interface and behavior untested**. Do not say iPhone-only, Intel-compatible, native Mac cleaner, or Windows-supported. Preserve the conflicting label rather than silently choosing the favorable one.

## New official source excerpts

Targeted check, UTC 2026-10-21, <https://docs.indiegoodies.com/cleansweep>:

> Remove similar photos, videos, and contacts
>
> Universal: Available on Mac, iPhone, and iPad. Buy on one device and restore purchases on other devices with the same iCloud account.
>
> Family Sharing: Lets you and other family members unlock the app.
>
> Last updated on October 12, 2026

This resolves whether the vendor documents a Mac offering, not the store's contradictory headline or operational compatibility. The store qualifies Family Sharing as applying to some purchases; do not promise all SKUs.

Targeted homepage HTML retrieval located this real `img` reference, not a logo or landing-page screenshot:

```text
alt="Clean Sweep"
src="https://raw.githubusercontent.com/khuong291/AppScreenshots/main/CleanSweep/Screenshot%202024-01-09%20at%2013.27.16.png"
```

<https://api.github.com/repos/khuong291/AppScreenshots/license> returned **404**. This establishes no permission; it is not proof a licence cannot exist elsewhere. No image bytes were downloaded. The filename is not proof of capture date, OS or version. No screenshot UI description or visual approval is invented.

## Pricing, platforms and honest unknowns

| Dimension | Documentary finding | Claim |
| --- | --- | --- |
| Scope | Similar photos/videos/screenshots; duplicate-contact merging | C2 |
| Platforms | Docs list Mac/iPhone/iPad; store requires iOS 16+, macOS 13+ and M1+, visionOS 1+; phone-only headline conflict retained | C3 |
| Version | US store lists 1.8.3, Oct 12; not installed | C4 |
| Download / IAP | Free with IAP; US listing Monthly $3.99, Yearly $12.99, Lifetime access $14.99 **and** $19.99 | C5 |
| Conditions | Lifetime advertised; cross-device restore with same iCloud account documented; Family Sharing qualified by store | C5, C7 |
| Data location | Vendor says local/no collection; store privacy declaration not independently verified by Apple or us | C6 |
| Source/licence | No app repository or licence verified; directory proprietary label is discovery, not official licence proof | Unknown |
| Approval/recovery | Exact selection/deletion/restore mechanics and sync effects not verified | Unknown |
| General maintenance | Helper grouping, developer caches, recurring disk growth not verified; do not mark “No” | Unknown |

Do not choose the lower lifetime amount as a guaranteed offer. Storefront amounts are not checkout tests; eligibility, tax, trial, renewal and free-use limits remain unknown. No customer reviews are used as proof of savings or purchase behavior.

## Breathing Room evidence and selected preview

Reused `docs/content/capabilities.md`, reviewed October 21: **0.1.0-preview.1**, macOS 13+, advertised universal installer but physical Intel/clean-machine validation pending; Apple Development signed, **not Developer ID signed or notarized**; **Python 3.10+** prerequisite. Source implementation does not prove release parity. Free local core; advertised AI Care **$5 USD/month or $50 USD/year**. Hosted AI needs authentication/internet and sends relevant inspection data; do not call the whole product offline. Exact approvals have a narrow optional automatic Ruff-cache exception; daily care reuses saved approvals while the app runs. No new native testing or savings measurement occurred.

Selected existing visual: `docs/content/assets/breathing-room/space-preview-2026-10-21.png`, ID `current-space-browser-preview`, source commit `54828ac3170b45861aee70861dd0b9c658ed7e51`. Original hash was rechecked and matches `screenshots.json`; no copying or edits. Existing library visual/privacy review reused, not independently re-awarded.

**Required caption:** “Current-source Breathing Room Space browser preview, captured October 21, 2026. Example data only; not a native scan, measured activity or cleanup result.”

**Alt:** “Breathing Room Space view rendered in a browser with illustrative example data.” Keep the example banner visible. This is current-source UI as of its captured commit, not a newly captured native release. Third-party marks retain their owners' rights; publication-context review remains pending.

Competitor visual is **link-only** at the exact official asset URL above. Capture/version/OS/data provenance and privacy review remain unknown. The on-page two-product visual gate **has not passed**.

## Conditional workflow brief, not a draft

**Title:** Separate photo-library duplicates from Mac disk growth before cleaning  
**Proposed slug:** `photo-library-duplicates-versus-mac-disk-growth`  
**Track/intent:** Search-reference decision workflow, not a renamed comparison or a tested deletion tutorial.

Lead with the distinction between media/contact organisation and broader disk/activity investigation. Identify where the reader's shortage actually occurs. Show the explicitly labelled Breathing Room Space preview after the lead. Explain Clean Sweep's documented media/contact scope without inventing a native Mac UI. Distinguish original files, rebuildable data and available space; never treat large size as deletion permission. End with a bounded decision and disclose “Breathing Room, which we build.”

**Interaction handoff:** A non-destructive decision checklist asks whether the problem is similar photos/videos/contacts or broader project/cache/app storage. No scanner, upload, cleanup or hypothetical savings presented as measurements. No code/demo repo needed. Obtain official approval/recovery/sync evidence before any step-by-step deletion instructions. Use the permission-cleared actual competitor UI as the second visual after review, not a generated substitute.

## Conditional concise comparison brief

**Title:** Clean Sweep and Breathing Room: different cleanup jobs  
**Proposed comparison ID:** `clean-sweep`; no route created.

Use a short matrix: documented library job, platform/phone-label caveat, vendor-local claims versus hosted AI, IAP versus free-core/paid-AI conditions, and preview/runtime limitations. Link the workflow article and hub only once real draft routes exist. Leave unverified features explicitly unknown.

**Truthful advantages/trade-offs:** Clean Sweep's documented specialised similar-media/contact tools and cross-device purchase restoration may suit library organisation. Breathing Room's documented storage/activity investigation addresses a different job, not superior photo deduplication. Its non-notarized preview, Python prerequisite and hosted-AI boundary are material trade-offs. Do not imply either tool replaces the other's unverified functions or is faster/safer. No unsupported Windows replacement intent is introduced.

## Blocking diagnostic and handoff

**Blocked: VISUAL-RIGHTS and VISUAL-REVIEW.** A real official app-image URL was located, but public hosting and a 404 licence endpoint do not establish reuse permission. Without permission or an explicitly approved policy decision, do not download/publish it, waive the image gate, or draft doorway content. After clearance, inspect the actual original and retain hash, dimensions, caption/alt, privacy and version/capture limits. No permission request was sent.

Other unknowns can remain qualified in an adjacent decision article. Any Mac-runtime, deletion/recovery or detailed price-offer recommendation requires additional scoped evidence. Independent evidence/rendered review remains pending; no score is awarded. Only this folder and the requested runtime receipt are owned outputs. No website, shared records, queue/database or unrelated work changed.
