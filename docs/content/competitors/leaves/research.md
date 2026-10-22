# Leaves research: blocked before drafting

**Job:** `research-leaves`. Actual UTC check: 2026-10-21T21:24:10Z. Research only; no site content, publication approval or hands-on testing.

## Decision

Leaves is [patonw/leaves](https://github.com/patonw/leaves), a terminal disk-usage treemap, not an established full Mac-maintenance substitute. **Canonical owner: `leaves`. No alias skip.** The README calls WinDirStat/QDirStat inspirations, not aliases; there is no evidence connecting this identity to PowerMyMac. Public source/releases do not justify a dead-product label.

**Drafting is blocked:** the official README identifies a real competitor UI screenshot, but image-specific reuse rights are unresolved. Do not download or publish it under an assumed software-licence grant. A link is research evidence, not satisfaction of the on-page image requirement. Obtain licence evidence or a separately approved policy decision; then retrieve permitted original bytes, hash them, inspect pixels/privacy and complete provenance. No permission message was sent.

## Reused evidence and discovery

Read `PLAN.md`, `EDITORIAL.md`, `capabilities.md`, `screenshots.json`; no `AGENTS.md` found within the app tree or checked ancestors. Loaded blog/browser skills and the adapted MailKite contract. No browser session was needed.

First reused `verification/batch-1.json` and the retained official/directory snapshots. Identity, description and MPL-2.0 were already current and were not refetched. Discovery edge: [Mole page 4](https://alternativeto.net/software/mole/?p=4), retained retrieval 2026-10-21T18:37:13.603Z; [Leaves listing](https://alternativeto.net/software/leaves/about/) retrieved 19:08:14.503Z, linking the official repository. Directory tags are not platform proof.

Verified retained SHA-256:

- Official snapshot: `d89d94e1cb34ee4eaa58875857570de68fcb3879ccca81173f6d1bfc9e86f4b5`.
- Directory snapshot: `b13473b1b9fd9039151a6d8de7fd48402bf75d32d5cde472ded1e4ccf53cafca`.

`research.json` retains source excerpts, conditions, dates, URLs, claim IDs, matrix and visual records. New official sources were fetched only to fill missing availability/version/build/rights evidence. Retrieval times use the actual machine UTC date, not an invented next-day date.

## Verified facts and boundaries

| Dimension | Finding and evidence |
| --- | --- |
| Identity/function | **L1 / S1:** “Leaves is a disk usage analyzer inspired by WinDirStat and QDirStat.” Nested rectangles in a terminal, with approximate area. [README](https://github.com/patonw/leaves#description). |
| Version/availability | **L2 / S2:** newest of four returned [release records](https://api.github.com/repos/patonw/leaves/releases): `v0.2.0-cross`, published July 15, 2026, non-draft/non-prerelease. “A re-release of v0.2.0 cross-compiled to musl for static linking.” Assets target x86-64 Linux glibc/musl. [Release](https://github.com/patonw/leaves/releases/tag/v0.2.0-cross). Not downloaded/tested. |
| Platforms | **L7:** Mac, Windows and BSD runtime support not verified. Directory labels do not override Linux release assets. Do not claim impossible support either. Current [release workflow](https://raw.githubusercontent.com/patonw/leaves/main/.github/workflows/release.yml) builds Linux GNU/musl; [Nix package](https://raw.githubusercontent.com/patonw/leaves/main/package.nix) defaults to Linux-musl. |
| Price/licence | **L3:** public source/release assets, MPL-2.0. No checkout on inspected official surfaces. Exact commercial/support pricing not verified; do not promise lifetime free service/support. [Licence](https://raw.githubusercontent.com/patonw/leaves/main/LICENSE). |
| Install/runtime | **L6:** README requires Rust for a source build and documents Nix as an environment. [Cargo manifest](https://raw.githubusercontent.com/patonw/leaves/main/Cargo.toml): package `0.2.0`, Rust edition `2024`. Exact minimum Rust/OS and Mac architecture support not verified. No installation/build executed. |
| Scan model | **L5:** hidden/ignored entries excluded by default; `-A` disables automatic ignores. Symlinks not followed; hard links can be counted twice. “No attempt is made to detect hard links, so they will be double counted.” [README](https://github.com/patonw/leaves#links). Not equivalent to available or reclaimable disk space. |
| Remote fit | **L4:** README says it works over remote shells when a graphical desktop is unavailable/impractical; character-cell sizing is coarse. Documented, not tested here. |
| Other maintenance features | **L8:** cleanup/approval controls, helper grouping, recurring monitoring, cache cleanup adapters and network/privacy behavior not verified. Unknown is not “No.” |

### Breathing Room comparison boundary

Reuse current `capabilities.md` evidence (**B1/B2**), not screenshots as measurement: macOS 13+, identified `0.1.0-preview.1`, Python 3.10+, Apple Development signed but not Developer ID/notarized; clean-machine/physical Intel runtime not validated. Source implements storage views, grouped app/helper CPU/memory and reviewable cleanup, but source presence is not distributed-binary parity testing.

Core desktop app is advertised free; optional AI Care $5 USD/month or $50 USD/year, renewing, tax at checkout. Hosted AI needs authentication/internet and can receive relevant inventory/tool information. Do not promise entirely offline AI, unlimited service, safety, speed or savings. Default interactive approvals, optional verified Ruff auto-Trash and exact saved daily approvals must not be flattened into a universal “asks every time” claim. Daily care needs the app running. Public offer/release/privacy URLs remain in the JSON's BR1 source record.

## Visual handoff

1. **Leaves:** [official normal-mode UI image](https://github.com/patonw/leaves/blob/main/docs/images/normal-mode.png), linked from the README Layout section. Candidate public raw URL: `https://raw.githubusercontent.com/patonw/leaves/main/docs/images/normal-mode.png`. Not fetched; no local copy/hash/dimensions or pixel review claimed. Capture date/version/platform unknown. **Link-only, rights pending.** Software MPL-2.0 does not establish image-specific permission. Caption must identify official-source UI and unknown capture context, not our test.
2. **Breathing Room:** selected `current-space-browser-preview` from `screenshots.json`, at `docs/content/assets/breathing-room/space-preview-2026-10-21.png`, source commit `54828ac3170b45861aee70861dd0b9c658ed7e51`. SHA-256 `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a`; 2940 × 3468. Reuse in place, preserve example-data banner. Required caption: **“Current-source Breathing Room Space browser preview, captured October 21, 2026. Example data only; not a native scan, measured activity or cleanup result.”** First-party owner-requested capture; per-page visual/privacy and third-party-mark review remain pending. Current-source means captured commit, not current native-release evidence.

## Distinct workflow article brief

**Conditional title:** Why a terminal treemap and Mac storage totals can disagree  
**Slug:** `terminal-treemap-ignore-rules-remote-host-local-mac`  
**Intent:** Explain host scope, ignore rules and link counting before deciding what storage figure means. Not another generic “Leaves alternatives” doorway.

- Lead conclusion: a map of a selected directory/host is neither disposal permission nor a measure of local Mac reclaimable space.
- Show rights-cleared Leaves UI immediately after lead; explain the selected host/path.
- Explain hidden/gitignore exclusions, `-A`, hard links and coarse areas, citing L4/L5; no scan execution or fabricated output.
- Distinguish Linux-host inspection over SSH from local Mac maintenance. Breathing Room cannot be presented as replacing the remote-host job.
- Later show the labeled Space preview; discuss backup, rebuild/download cost and permissions before a separate cleanup decision.
- Interaction handoff: a static checklist, “Which host? Which directory? Which ignore rules? Which size metric?” No filesystem widget or forced runnable tutorial.
- Link hub, counterpart comparison and only a verified relevant tool route. Do not invent a tool URL.

## Concise comparison brief

**Title:** Leaves vs Breathing Room: terminal inspection or local Mac care?  
**Candidate comparison slug:** `leaves`.

Conclusion first, adjacent/platform-limited framing. Concise matrix: target host/platform, scan semantics, source licence/access, install requirements and documented maintenance scope. Unverified controls stay explicitly unknown. Link the deeper workflow rather than expanding the matrix into filler. Disclose “Breathing Room, which we build” at the one bounded recommendation.

**Choose Leaves** for its documented terminal/remote-shell treemap workflow; configurable exclusions and file-type/group views are useful without a desktop. Trade-offs: approximate areas, hard-link counting and no verified native Mac binary/runtime here.

**Consider Breathing Room** for documented local Mac storage/app investigation and approval architecture if its preview, runtime and hosted-service caveats fit. It is not a remote Linux terminal replacement. No measured superiority, guaranteed space recovery, security/privacy audit or unsupported negative competitor claims.

## Gates and actual validation

- Retained original official snapshot hash matches batch-1; directory hash calculated. No shared register modified.
- Six read-only official web fetches filled gaps: releases API, Cargo manifest, release workflow, licence, Nix package and flake. No README/directory refetch, binary/image download, browser/cookie extraction or account access.
- JSON structure, claim/source references, local evidence paths and selected preview hash checked in the retained validation log. Source-level checks are not native testing or independent editorial review.
- Site build/tests not run: no site files edited. No cleanup, signup, messages, purchases, commits, pushes, deployment, queue mutation or subagents.
- **Blocking:** competitor image reuse/access/provenance review. **Conditional:** native Mac recommendations need platform-specific evidence. Other feature/pricing unknowns can remain noncritical if honestly excluded from assertions.
- No article drafted, no score awarded; independent review remains pending.
