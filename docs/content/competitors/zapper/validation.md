# Research validation

- Packet assembly: first attempt failed on an incorrect baseline collection key (`products`). Corrected to the actual `records` key; rerun completed successfully.
- Python structural validation **passed**: research JSON parsed; canonical owner and non-skip decision checked; five source snapshot SHA-256 values matched retained files; 15 claims had resolvable source references, URLs and dates; verified homepage excerpts matched the reused original text.
- Two visual records **passed** PNG signature, dimensions and original SHA-256 checks. Captions, alt text, reuse bases and unpublished paths were checked. Official press HTML contains both the screenshot asset reference and the journalist/blogger/content-creator provision.
- Reused official snapshot hash matches `batch-1.json`: `054c1708264cf3e287235be8bce36f29c18d01a86d029887613da40d0a00efed`.
- Actual image-capable reads completed for the original Mac Zapper scan-results PNG and the shared Breathing Room Space preview; visible contents and limitations are recorded in the packet. This is research inspection, not independent publication approval or runtime testing.
- Research JSON SHA-256: `18a12f734e8a971acc3b3098f6c06e38ea3699cf9cf33692e89b430a1d2a01c7`.
- Research Markdown SHA-256: `1766070362b6aa142920c325b7c9fe1d0c8947c25b0818ea9026a7de76995ac5`.
- No marketing content changed; site check/build/tests were not run and are not required for a research-only packet. No app installed, cleanup executed, browser/profile accessed, account created or external message sent. No queue/database, shared source register or unrelated competitor files changed by this job.

The owned `build-packet.py` can regenerate JSON from retained local sources without network access. It records a new assembly time; rerunning requires refreshing these packet hashes. Publication remains draft-only pending the separate drafting and independent review stages.
