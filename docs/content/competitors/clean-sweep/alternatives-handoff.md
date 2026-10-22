# Clean Sweep alternatives draft handoff

Task: `draft-alternatives-clean-sweep` · drafted October 22, 2026.

## Outcome and ownership

Created one internal alternatives page at `/Users/gabe/code/breathing-room/website/src/content/alternatives/clean-sweep.md`, intended route `/alternatives/clean-sweep/`. Frontmatter is `status: review`, `published: false`, with current dates. The article has a distinct replacement-selection intent: compare tools by personal photo/contact library work versus broader Mac cleanup or storage investigation. It does not repeat the Clean Sweep head-to-head comparison and does not claim AlternativeTo recommends the named peers.

Owned visual files are `website/public/assets/alternatives/clean-sweep/choose-by-job.svg` and `space-preview-2026-10-21.png`. No other files or queue state are owned or changed.

## Evidence and alternatives selection

Reused Clean Sweep `research.json`/`research.md`, the comparison handoff, `capabilities.md`, and the retained verification graph. No discovery refetch or app test was performed. The canonical identity remains Indie Goodies Clean Sweep, App Store ID 6449146108; “Photo Cleaner” and “Phone Cleaner” are listing-name variants, not separate products. Clean Sweep remains adjacent rather than a verified general-Mac-maintenance replacement.

The listed options have independent product-packet support for their stated jobs:

- **Tenorshare Cleamio** (owner `4ddig-mac-cleaner`; official destination under that retained listing identity): official product material advertises similar photos, duplicates and other Mac maintenance; retained purchase evidence documents limited free similar-photo/duplicate deletion. No runtime or matching-quality claim.
- **Cleaner One Pro**: retained official Mac product page advertises similar-looking photos alongside broader storage/maintenance functions. No assertion about parity, feature availability across editions, or effectiveness.
- **CleanMyMac**: retained official page and source packet support broader Mac suite/duplicate scope. It is not presented as verified contact-merging equivalent or as a direct AlternativeTo pairing.
- **Breathing Room** is included only as an affiliated, different-job option for storage/activity investigation, with release, Python, notarization and hosted-AI boundaries. It is explicitly not a media/contact replacement.

Clean Sweep claims preserve the retained conflict: official documentation lists Mac/iPhone/iPad, while the captured US store page says “Only for iPhone” and “Not verified for macOS” but also lists macOS 13+ with M1+. The page calls this documented availability, not tested Mac UI/runtime. Pricing reports both US lifetime amounts and does not choose an active offer. Vendor-local and App Store privacy statements are attributed, not described as an audit. Recovery, synced-library effects, exact free limits, Intel support and deletion mechanics remain unknown and are not converted into feature-absence claims.

## Visual route and provenance

Route B is used. `choose-by-job.svg` is an original editorial decision diagram, not Clean Sweep UI, a recreation, test result or benchmark. It has an accessible title/description and local-only vector content. The Clean Sweep official screenshot is not copied or hotlinked: the existing packet says the image is link-only, its actual view/provenance are unreviewed and reuse permission was not established. The page links to official product documentation instead.

The first-party PNG is copied byte-for-byte from `docs/content/assets/breathing-room/space-preview-2026-10-21.png`; SHA-256 matches the existing `screenshots.json` record. Its caption and alt retain the example-data and browser-only disclosure. Existing visual/privacy review is reused, not newly awarded. It is not native runtime evidence or proof of distributed-release parity.

## Outputs and hashes

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `/Users/gabe/code/breathing-room/website/src/content/alternatives/clean-sweep.md` | 11103 | `1ad4a5d5e00d6aedb2e89a8b31ef1e6eb777d11e528aacbf859850add213c314` |
| `/Users/gabe/code/breathing-room/website/public/assets/alternatives/clean-sweep/choose-by-job.svg` | 2414 | `af16e9cad8b4844396ed0a011da5dac9b3caff9c301ff8ade6f600942572da73` |
| `/Users/gabe/code/breathing-room/website/public/assets/alternatives/clean-sweep/space-preview-2026-10-21.png` | 587216 | `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a` |

## Checks performed and pending review

- **PASS:** focused Python structural check using `/usr/bin/python3`: draft metadata/status/date, seven H2s, affiliation disclosure, local referenced assets, SVG XML, accessible title/description and no external SVG resources.
- **PASS:** `shasum -a 256` verified the PNG copy equals the retained source hash and `screenshots.json` hash. `file` reports SVG and 2940×3468 RGB PNG.
- A first attempt with Homebrew Python 3.14 could not load its `pyexpat` against the system expat library. Re-ran the successful structural check with `/usr/bin/python3`; no packages or system configuration changed.
- Shared `pnpm check`, site build, test suite, rendered HTML inspection, and browser responsive/theme checks were **not run**: this scheduled task explicitly prohibits shared site builds. Independent factual/visual/SEO/rendered review remains pending; this draft is not publication approval and receives no editorial score.
- Interactivity pass: the useful decision aid is the non-executing choose-by-job diagram plus the four-step check list. No scanner, upload, cleanup, savings calculator or code sample is warranted.

Before publication, independently verify source-specific claims and current offers/platform labels; inspect the rendered page at narrow/tablet/desktop widths and both themes; check image/caption legibility, canonical/schema/social output, links and draft exclusion. Refresh volatile offers within 30 days. Do not change status/published fields until those gates pass.
