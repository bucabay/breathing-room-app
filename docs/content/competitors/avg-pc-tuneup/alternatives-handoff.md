# AVG PC TuneUp alternatives draft handoff

Task: `draft-alternatives-avg-pc-tuneup` · Draft date: **2026-10-22** · **Complete draft; not publication-approved.**

## Exact owned outputs

Marketing root: `/Users/gabe/code/breathing-room/website`.

| File | SHA-256 |
| --- | --- |
| `src/content/alternatives/avg-pc-tuneup.md` | `fb39f77b298b8e8953468d6c5b56af9a8e1bf738298e4d0186b5ef74f750706f` |
| `public/assets/alternatives/avg-pc-tuneup/task-map.svg` | `10cb18bdbb55e7c9ace4ab1cf16513807c39bce43e716d4753d0607dfb185118` |
| `public/assets/alternatives/avg-pc-tuneup/space-preview-2026-10-21.png` | `9e3475d44a6387b2485dafe2e4284ca9d32fd9436d50b7f48906c044a5db743a` |
| `docs/content/competitors/avg-pc-tuneup/alternatives-handoff.md` | See receipt for current hash. |

Public route intended by the content schema: `/alternatives/avg-pc-tuneup/`. Record fields are `status: review`, `published: false`, and current `date`/`updated` of October 22, 2026. This is a draft, not an assertion that the route is live or independently reviewed.

## Intent and evidence

This is a replacement-options page for the maintenance jobs associated with AVG PC TuneUp, not an AlternativeTo relationship roundup and not a copy of the Breathing Room head-to-head body. It names AVG’s separately documented Mac edition, CleanMyMac for suite-style Mac maintenance, DaisyDisk for visual disk triage, BleachBit with an explicit experimental-Mac boundary, and Breathing Room only for a narrow preview-stage investigation use case. The retained CleanMyMac, DaisyDisk, BleachBit and AVG packets support these as distinct, relevant choices. No directory endorsement or pairing is asserted.

Reused `docs/content/PLAN.md`, `EDITORIAL.md` October22 route-B policy, `capabilities.md`, `screenshots.json`, `research.json`/`.md`, `verification/batch-2.json` provenance, and peer records `docs/content/competitors/{cleanmymac,daisydisk,bleachbit}/research.json`. No redundant product or directory fetch was made. No applicable AGENTS.md was found (corroborated by the existing capabilities/editorial records). Claim limits retained include AVG’s OS-minimum conflict, PC trial conflict (not transferable to Mac), incomplete purchase fine print, and no binary/runtime testing. Unknown product capabilities are not presented as absent.

## Visual route and provenance

- `task-map.svg` is an original, source-backed decision diagram. It is not competitor UI, a test, a ranking, or a feature parity matrix. Its text distinguishes Windows-only needs, Mac suite needs, disk-map exploration, and experimental BleachBit Mac support. Alt text and an explanatory caption are in the page. SVG XML parsing passed.
- `space-preview-2026-10-21.png` is an unchanged first-party copy from `docs/content/assets/breathing-room/space-preview-2026-10-21.png`; source and copy SHA-256 match. Keep the supplied caption/disclosure: example data only, not native scan/activity/cleanup evidence. Source manifest records capture `2026-10-21T19:06:45.416416+00:00`, commit `54828ac3170b45861aee70861dd0b9c658ed7e51`, and composer/chart overlap. No AVG competitor image was copied, downloaded or hotlinked because reuse permission is not established.

## Validation performed

- Structural Python checks passed: draft status/date/source count, two figures, no placeholder markers, and all local image references resolve. The body is approximately 1,876 whitespace-delimited words.
- Ruby REXML parsed `task-map.svg` successfully.
- `shasum -a 256` verified the three marketing outputs. The screenshot copy matches the shared source hash exactly.
- Attempted installed Node `yaml` parser check; it could not run because `yaml` is not installed/resolvable in the website workspace. No package installation was attempted. Python XML parsing also failed because this machine’s Python 3.14 `pyexpat` is incompatible with its system libexpat; equivalent SVG parsing passed using Ruby REXML.
- No shared site build/test, route render, browser/responsive/theme/keyboard review, external live-link fetch, or independent factual/visual/SEO approval was performed. No publication score is awarded. Per scope, no shared files, navigation/schema/tests, queue/database, or other job outputs were changed.

## Remaining independent review items

1. Validate exact article YAML/content against the current collection schema and review the produced route/canonical/metadata after the responsible serialized site check; this job did not run a site build.
2. Inspect the real rendered page at narrow/tablet/desktop widths and both themes. Confirm diagram labels, table behavior, screenshot legibility, caption/disclosure, links, and keyboard access. The screenshot is tall and its source capture has a composer overlapping part of the chart.
3. Independently verify every source-adjacent claim against the retained packets. Refresh volatile offer/availability details before publication; numeric AVG price/trial claims are deliberately omitted.
4. Confirm unpublished draft exclusion from all public outputs and require the programme’s independent review threshold before changing publication fields.

No apps were installed or tested; no cleanup, account, purchase, message, credential, computer-setting, commit, push, deployment, or queue/database action occurred.
