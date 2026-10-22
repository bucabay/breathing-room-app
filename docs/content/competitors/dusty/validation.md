# Research validation — 2026-10-21

Executed read-only Python structural/provenance checks; exit **0**:

- Six downloaded source/asset byte hashes match `sources/retrievals.json`.
- Three hashed source-register paths (official homepage snapshot, capabilities register and screenshot register), plus retained directory snapshot, match recorded SHA-256 values. Ten evidence hash checks total; visual originals additionally checked below.
- All **19 claims** resolve source IDs; retained supporting excerpts matched after whitespace normalization. Release `tag_name` parsed as `v2.1.0` rather than relying on serialization whitespace.
- All **8 matrix rows** map each product's cells to existing claim IDs.
- Both selected PNG originals match SHA-256 and PNG-header dimensions: Dusty **3800 × 1504**, Breathing Room Space **2940 × 3468**. Caption, alt and reuse-basis fields present.
- Actual image-capable reads completed for both PNGs, not just file existence checks. Dusty official app panels and Breathing Room example-data banner were inspected. Independent publication/crop review remains pending.
- `canonicalOwnerId` is `dusty`; alias skip is false; distinct Dusty Storage decision retained. Unknowns remain explicitly noncritical/not-verified; no critical evidence blocker for the bounded draft.
- App package version cross-check: `0.1.0-preview.1`. README install, pricing, local/hosted and workflow conditions agree with the reused capabilities evidence for this packet.

Packet hashes at completion:

| File | SHA-256 |
| --- | --- |
| `research.json` | `4302a8e807d2c5fee7c62ad6c33bb5a346b47bbe08dd209205c4aafdebaf63dc` |
| `research.md` | `c36d9b1c3ff5f0c0b793daa94dfb528249fddc159a9fc286d4690b976ee6b990` |
| `sources/retrievals.json` | `141f9fad2e26da47b7f628efa2851b59ec22da18631f93ba45e25ee3929bd101` |

No app/native tests, cleanup, installation, external scripts or site build executed. No browser session used. No website/queue/database changes made. This is research validation, not a safety audit, benchmark, independent article review or publication approval.
