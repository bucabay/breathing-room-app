# Research validation

Actual read-only Python checks passed:

- `research.json` parses; research and drafting gates are blocked; unresolved canonical owner is null.
- Every claim's source IDs resolve and each claim has a URL, excerpt and check date.
- Reused discovery snapshot, D1 snapshot and O0 access diagnostic hashes match the existing baseline records (three hash comparisons, two unique files).
- Selected Breathing Room PNG SHA-256 matches `screenshots.json`; PNG header confirms 2940 × 3468.
- Retained owned-tab snapshot contains `ERR_CERT_AUTHORITY_INVALID`; actual snapshot read after saving.
- Competitor asset URL remains null; no unknown screenshot URL invented.
- Selected PNG opened using image-capable read tool; browser-preview disclosure and chart/list inspected. No native test or fresh capture inferred.
- Chrome was reachable; only newly created tab 146 was navigated/read, then closed. No recovery launch required; no TLS bypass.

Artifact SHA-256 at validation:

| Path within this folder | SHA-256 |
| --- | --- |
| `research.json` | `7383107b25b63694afe63b6c809e413c095d57bb7df2caea7be4502b5c4d4c78` |
| `research.md` | `f58293d4b610739c6b982cf890a4735564612b4790a20baa195622632348b82e` |
| `evidence/official-access.txt` | `fae57fe11193209195973d7dcf80e576c8e74f95527f340603c39b38222e1efb` |

No site files changed; site check/build/tests are not applicable to this blocked research-only packet. No independent publication score/review claimed. Unrelated working changes were present before this task and left untouched.
