# CleanMyLinux alternatives page handoff

Task: `draft-alternatives-cleanmylinux`  
Public path: `/alternatives/cleanmylinux/`  
Article: `/Users/gabe/code/breathing-room/website/src/content/alternatives/cleanmylinux.md`

## Decision and scope

Created a distinct task-based alternatives draft rather than reusing the CleanMyLinux-versus-Breathing Room comparison body. It includes five documented candidates: BleachBit for Linux cleanup, Mac CleanUp Go for terminal cleanup on Mac, DaisyDisk for Mac disk mapping, AppCleaner for Mac app removal, and CleanMyMac for broader Mac maintenance. These are selected from retained official-source research packets, not represented as AlternativeTo relationships. The AlternativeTo CleanMyLinux about page remains discovery evidence only.

The page explicitly separates Linux from Mac, identifies CleanMyLinux's beta label and unresolved distro/GLIBC conflict, avoids installation recommendations, describes unknown commercial and behavior claims as unknown, and distinguishes Breathing Room's Mac storage-investigation use from a cleaner. Its pricing, preview, Python, hosted-data and signing limitations are stated from the retained same-day capability review.

## Owned outputs and hashes

SHA-256 values are recorded for each real file, not the asset directory:

| File | SHA-256 | Provenance |
| --- | --- | --- |
| `/Users/gabe/code/breathing-room/website/src/content/alternatives/cleanmylinux.md` | `4558dd6757c2b4c653d754944d50fd9c323754df4a78d1e9945e35eba91cb4c3` | Draft based on retained source packets. |
| `/Users/gabe/code/breathing-room/website/public/assets/alternatives/cleanmylinux/choose-by-platform-and-job.svg` | `71c8a1ff1cdf27412f1eb54120f26be7232a74024fe1f22eaf9daf27203fba73` | Original editorial decision diagram; not product UI. |
| `/Users/gabe/code/breathing-room/website/public/assets/alternatives/cleanmylinux/cleanmylinux-official-preview.png` | `91146332b2b472ee548644c36add50181379375f0c4be360488f99e7fa858104` | Copied unchanged from `docs/content/competitors/cleanmylinux/assets/cleanmylinux-official-preview.png`; published under packet's documented root-MIT image basis and full license notice retained in `sources/LICENSE`. |
| `/Users/gabe/code/breathing-room/website/public/assets/alternatives/cleanmylinux/breathing-room-space-example.png` | `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a` | Copied unchanged from `docs/content/assets/breathing-room/space-preview-2026-10-21.png`; example-data/native-measurement disclaimer retained. |

## Visual / interaction pass

Route B: original decision diagram plus a documented first-party example-data view; official CleanMyLinux UI is an attributed repository image, not a claim of a tested release. Diagram routes reader by platform and job, including explicit limits. No fake UI, screenshots were not edited, and no cleanup controls or calculations were added.

## Validation and pending review

- Reused the retained research and visual records; no redundant source refetch, install, test, cleanup or browser session was performed.
- Need run site `pnpm check`, `pnpm build`, then `pnpm test`, inspect generated HTML and draft exclusion, and perform authorized responsive light/dark browser review. These site-wide checks were not run by this scheduled worker.
- Independent source, image-rights, rendered visual, SEO and quality review remains pending; the draft is not publishable until those gates pass.
