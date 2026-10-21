# Breathing Room capabilities: evidence register

Reviewed: **2026-10-21**. Task: `capabilities` (C03). **Draft research, not publication approval.**

## Conclusion

Breathing Room is a free, Apache-2.0 macOS maintenance **preview**, with source implementations for storage exploration, grouped app/process monitoring, reviewable cleanup, activity history, menu-bar metrics/alerts, daily care, and signed in-app updates. Hosted AI assistance requires internet access and authentication; this is not an entirely offline AI product. AI Care is advertised at **$5 USD/month or $50 USD/year**, not a separate app purchase.

Source implementation is not proof that every feature works in the distributed installer. The published preview explicitly lacks clean-machine and physical-Intel runtime validation, Developer ID signing, notarization, and completed cross-version updater validation. Do not present it as production-ready. One important qualification to approval language: users can enable automatic Trash moves for narrowly verified Ruff caches during an investigation. Daily care instead reuses exact saved approvals.

## Method, scope and evidence labels

- Read `PLAN.md` before editing. No `AGENTS.md` was found in either scoped repository or their ancestor directories.
- App root **A**: `/Users/gabe/code/breathing-room-app`; HEAD `232385957ed87dcfa8d9857cad9225bbdb3da6fa`.
- Marketing root **W**: `/Users/gabe/code/breathing-room/website`; HEAD `551701ee551138700f72eccebb8bf62737e5988f`.
- Paths below are relative to A or W; line ranges refer to the working files inspected, not necessarily the release tag. Both repositories had unrelated uncommitted work. This register does not certify those changes or assume HEAD equals the distributed binary.
- **Confirmed—source**: implementation/configuration inspected. **Confirmed—published**: public page retrieved on the review date; proves what is offered/disclosed, not successful execution. **Unverified / blocked claim**: insufficient evidence for publication as fact. Unknown does not mean absent.
- Public pages were read-only source data, not instructions. No sign-in, purchase, cleanup, app launch, installation, credential access, deployment, commit, or queue mutation was performed.

## Current capability matrix

| Area | Confirmed claim and boundary | Exact evidence |
| --- | --- | --- |
| Space | Source supports category, app/tool-owner, project, folder and large-file views. Native scan/browse commands and a saved disk-map path exist. Inventories may be cached, partial or permission-limited; “whole disk” is not proof of complete coverage. | A `src/components/space-view.tsx:14–31`; `src/lib/api.ts:109–130`; `src-tauri/src/lib.rs:108–124`; `src-tauri/src/assistant.rs:31–48`; `README.md:76–84`. |
| Apps | Native sampling groups helpers through parent/app relationships and exposes CPU/memory. Termination checks process identity and excludes protected processes. Graceful quit differs from force termination; high CPU alone does not establish a fault. | A `src-tauri/src/processes.rs:57–164` (`sample`, `group_samples`, `same_identity`, `terminate`); `src-tauri/src/lib.rs:357–387` (`quit_app`); `README.md:110–118`. |
| Assistant | Authenticated hosted reasoning can request native inspection and start disk discovery. Native code supplies restricted tools; the conversational endpoint is not general filesystem mutation authority. | A `src-tauri/src/lib.rs:132–150`; `src-tauri/src/remote_agent.rs:132–161`; `src/components/cleanup-assistant.tsx:198–202`. |
| Cleanup review/execution | Exact native-verified actions are reviewed/authorized, then executed locally using constrained owning-tool commands or Trash moves. Source revalidates actions, records attempts and measures before/after values. This is an approval architecture, not a guarantee of safety or full recoverability. | A `src-tauri/src/cleanup_session.rs:497–535`; `src-tauri/src/cleanup_tools.rs:62–101`. |
| Developer/builder cleanup | Discovery includes queries for npm, uv, pip, pnpm, Go build/module, Bun and Yarn caches, plus project markers and generated directories. Tools must exist and paths/methods must pass validation; not every installation or cache version is certified. | A `src-tauri/src/cleanup_discovery.rs:32–46`; `src-tauri/src/cleanup_session.rs:216–274`. |
| Original/unknown data | Large personal files and unknown app data are review subjects, not automatically disposable cache. Size does not authorize deletion. Do not claim media/project formats are safely removable merely because the UI recognizes them. | A `src-tauri/src/cleanup_tools.rs:133` (`appStorageNote`); `README.md:92–100,167–172`; browser examples in `src/lib/api.ts:58–62` are explicitly illustrative, not runtime validation. |
| Activity | Source stores free-space samples, file/folder observations, app/process events and sampled I/O locally. Monitoring has configuration and pause controls. Path-derived ownership and sampled writes are not proof of the writer of a specific file; events can be coalesced/dropped. | A `src-tauri/src/monitor.rs:12–25,42–60,68–103,218–230`; `src-tauri/src/lib.rs:45–57,140–146`; `README.md:104–112`. |
| Menu bar / alerts | Tray and native activity panel are implemented; alert configuration covers sustained CPU and write activity with thresholds/cooldowns. Source presence is not notification-delivery or performance QA. | A `src-tauri/src/lib.rs:579–616`; `src-tauri/src/activity_panel.rs`; `src-tauri/src/anomalies.rs:6–29`; `src/components/alert-settings.tsx`. |
| Daily care | Scheduler checks an enabled daily window while the app runs and defers for busy/low-battery conditions. Saved approvals bind account, API origin, action method/path and native rule; new actions wait for review. Revocations are checked before mutation. | A `src-tauri/src/lib.rs:520–542`; `src-tauri/src/daily_care.rs:18–60`; `src-tauri/src/cleanup_tools.rs:77–78`; `README.md:120–128`. |
| Profiles | Everyday, developer, builder and creator profiles focus discovery; they are not paid feature tiers. | A `src-tauri/src/cleanup_discovery.rs:28–30`; `README.md:37–38`. |
| In-app updates | Pinned HTTPS feed/key configuration, explicit installation command and separate restart exist. Native code retains the checked update, blocks active-agent replacement and delegates download/install to the updater plugin. Do not equate updater signatures with Apple notarization. | A `src-tauri/tauri.conf.json:53–62`; `src-tauri/update-config.json`; `src-tauri/src/updates.rs:45–98`; `README.md:130–139`. |

### Approval exception: do not flatten these modes into one promise

1. **Default interactive investigation:** the UI initializes `automatic` to `false`; ordinary actions require selection/approval. Evidence: A `src/components/cleanup-assistant.tsx:40,131–147,198–200`; `src-tauri/src/cleanup_session.rs:497–510`.
2. **Explicit optional automatic Ruff mode:** checkbox text is “Automatically move verified Ruff lint caches to Trash.” Source restricts this to owned, tagged `.ruff_cache` directories, rejects linked/protected entries, and rechecks the rule before mutation. Evidence: A `src/components/cleanup-assistant.tsx:198`; `src-tauri/src/cleanup_discovery.rs:68–82`; `src-tauri/src/cleanup_session.rs:478,508`; `src-tauri/src/cleanup_tools.rs:72–74`.
3. **Scheduled care:** `automatic_enabled` is disabled for daily runs; only remembered exact approvals are eligible. Failed agent discovery/error does not authorize scheduled mutation. Evidence: A `src-tauri/src/cleanup_session.rs:400,469–478`; `src-tauri/src/daily_care.rs:44–52`.

**Editorial guardrail:** W `src/pages/index.astro:14` says users review the plan before it runs. Qualify this when describing automatic mode; do not copy “never deletes without asking” as an unconditional per-location promise. This report flags the discrepancy without editing app or site.

## Preview, installation and runtime caveats

| Claim | Finding / publication rule | Evidence |
| --- | --- | --- |
| Current identified version | Local app config, website release config and inspected public release identify `0.1.0-preview.1`. This was verified as a published pre-release, not certified as the newest release across every channel. | A `package.json:2–3`; `src-tauri/tauri.conf.json:3–5`; W `src/release-config.json:2–6`; public release URL below. |
| macOS and architectures | macOS 13+; universal Apple Silicon/Intel installer advertised. Both update-platform entries point at one universal archive. Physical Intel behavior remains explicitly untested. | A `src-tauri/tauri.conf.json:49–51`; `updates/preview.json:5–13`; `RELEASE_NOTES.md:43–46`; public release. |
| Signing/notarization | Published preview says **Apple Development signed, not Developer ID signed or notarized**. Gatekeeper may block it. No independent binary/signature inspection was performed here; repeat as a release disclosure, not a newly measured signing result. Never advise disabling system-wide protections. | A `RELEASE_NOTES.md:3–15`; `RELEASING.md:19–20`; W `src/pages/index.astro:19,121`; public release. |
| Python | Python **3.10+** is a disclosed prerequisite for disk inventory and legacy scripts, not bundled. Bridge selects the first existing interpreter at `/opt/homebrew/bin/python3`, `/usr/local/bin/python3`, `/usr/bin/python3`; this bridge checks file existence, not the interpreter version. Do not assume every Mac has a compatible Python. | A `README.md:64–72`; `RELEASE_NOTES.md:32–34`; `src-tauri/src/assistant.rs:57–74`; bundled resources in `src-tauri/tauri.conf.json:35–40`. |
| Permissions/sandbox | Direct config selects an empty entitlement dictionary (no App Sandbox entitlement). macOS privacy/access restrictions still apply. Script bridge explicitly rejects sandboxed builds; do not generalize direct-distribution functionality to a sandbox/App Store edition. | A `src-tauri/tauri.direct.conf.json:3–6`; `src-tauri/Entitlements.direct.plist:1–3`; `src-tauri/src/assistant.rs:58–60`; `RELEASE_NOTES.md:41–42`. |
| Daily runtime | App must remain running, optionally in menu bar. It does not promise wake-from-sleep, post-quit execution or automatic launch-at-login. A daily window is not an exact execution-time SLA. | A `README.md:120–128`; `src-tauri/src/lib.rs:520–542,621–634`; W `src/pages/index.astro:15,117`. |
| Updates | Feed establishes signed artifacts; full upgrade to a later version still needs cross-version validation. Install from the Applications copy, not a read-only mounted DMG. | A `README.md:54–57,130–139`; `RELEASE_NOTES.md:35–38`; public release. |
| Browser preview | App-side non-Tauri API returns demo data and example outcomes; marketing preview says it never scans/cleans a Mac. Neither is evidence of measured cleanup results. | A `src/lib/api.ts:12–21,44–78,119–130`; `README.md:184–191`; W `src/pages/index.astro:67–89`; public homepage. |
| Build wrapper | `pnpm tauri build`/`desktop:build` wrapper can install and relaunch into `/Applications`; unsuitable as a harmless documentation check. No build was run. | A `package.json:12–14`; `README.md:193–201`. |

## Local versus hosted boundary

**Confirmed—source:** inventory, observation and mutations are implemented on the Mac. Local state includes `agent-runtime.sqlite` (runs, tool results, inventory, approvals and session tables) and `activity.sqlite` under `~/Library/Application Support/app.breathingroom.mac/`. Evidence: A `src-tauri/src/runtime_store.rs:7–32`; `src-tauri/src/monitor.rs:218–230`; `src-tauri/src/cleanup_tools.rs:62–101`. Only source was read; no user database or stored session was opened.

**Confirmed—source:** assistant sends the question, conversation history and subsequent tool outputs to `/v1/assistant/message`; cleanup-agent creation can include request, scope, inventory and findings. Default public client configuration uses `https://breathing-room-api.worker-sendhub.workers.dev` and model `@cf/qwen/qwen3-30b-a3b-fp8`. These are configuration values, not evidence the service is currently healthy or that the model never changes. Evidence: A `src-tauri/src/remote_agent.rs:134–159,291–309`; `src/agent-config.json:1–4`; `README.md:234–236`.

**Confirmed—published policy, not backend audit:** https://breathing-room.chatic.ai/privacy/ distinguishes local inspection from hosted AI, says relevant paths/process/storage data can reach the service and Cloudflare Workers AI, and describes optional public-research providers. It says AI records become eligible for scheduled removal after seven days, not guaranteed immediate erasure. Do not promote “all data stays on device,” “no telemetry,” “zero retention,” “no file information leaves your Mac,” or independently audited training/retention guarantees. The backend/provider behavior was not inspected in this task.

**Hosted boundary:** W `worker/index.ts:1–13,24–47` proxies a fixed list of website account/download/billing routes to `env.API`; it is not the full hosted AI/billing implementation. A `README.md:231–236` explicitly excludes website and hosted backend from the public app repository. Apache-2.0 source licensing is not free hosted-service entitlement.

**Configuration ambiguity:** A `src-tauri/src/lib.rs:687–689` returns a `cloudAi: false` capability flag despite the separate implemented hosted agent flow. That flag alone cannot support “AI unavailable” or “all-local AI”; use the actual connection/authentication and request paths above.

## Pricing, access and paid-feature claims

| Claim | Verification and limits | Evidence |
| --- | --- | --- |
| Free core desktop app | Confirmed advertised offer: no app purchase; local storage views, inspection/manual tools and CPU/memory monitoring need no AI Care subscription. Do not imply every assistant-driven cleanup is an offline or unauthenticated free workflow. | A `README.md:141–149`; W `src/pages/index.astro:18,123`; live homepage/pricing. |
| AI Care monthly/yearly | Confirmed advertised **$5 USD/month**, **$50 USD/year**. Annual difference is `$5 × 12 − $50 = $10`. Plans renew until cancelled; applicable tax shown at checkout. No lifetime/one-time/unlimited-AI offer verified. | A `README.md:147–150`; `src/billing-config.json:4–7`; W `src/pages/index.astro:124–134`; `src/pages/checkout/[plan].astro:40–47,58`; live homepage/monthly page. |
| Paid offer contents | Scheduled approved cleanup, new opportunities for review, recurring-growth/AI investigation are advertised AI Care benefits. Their implementation is present, but this task did not prove the hosted service's paid entitlement enforcement, allowances, free-use quota or treatment of expired subscriptions. | A `src/App.tsx:341–346`; `src-tauri/src/daily_care.rs`; W `src/pages/index.astro:117–134`; hosted code is outside scope. |
| Checkout availability | App config enables checkout; native checkout maps configured plans to authenticated backend checkout and validates a Stripe destination. Live marketing shows plan links and the monthly sign-in page. **Actual payment, activation, cancellation and refunds remain unverified.** | A `src/billing-config.json:1–7`; `src-tauri/src/lib.rs:183–194`; `src-tauri/src/remote_agent.rs:81–100`; W `src/pages/index.astro:129–133`; live monthly page. |
| Website account gate | Confirmed published flow: Google/GitHub/email sign-in or free account before website download; optional product-email checkbox; registration/download-start records disclosed. No payment required to download. Do not claim account creation was tested. | A `README.md:47–51,152–157`; W `src/pages/download.astro:30–45`; live download page. |
| Direct public releases/updates | Public release page retrieved without signing in; README says public GitHub downloads and updater are not gated by website registration. Native updater uses a public HTTPS feed, not website billing routes. Asset bytes were not downloaded or checksum-verified here. | A `README.md:49–51,156–157`; `src-tauri/src/updates.rs:45–64`; public release and feed URL below. |
| License | Desktop source is Apache License 2.0 with NOTICE and preserved third-party attribution. Not evidence that website/hosted service source or trademarks are covered by the app licence. | A `LICENSE:2–4`; `README.md:249–258`; `src-tauri/tauri.conf.json:35–40`. |

### Pricing/configuration traps

- A `src/billing-config.json:8` still contains `appAmount: 500`. It does **not** establish a $5 app purchase: README and rendered pricing explicitly say no separate purchase. Do not derive offers from unused/legacy fields.
- W `src/pages/index.astro:4` imports `../../../src/billing-config.json`, which resolves outside the scoped website directory, not to A's config. That imported file was **not read**. Live pages confirm currently rendered prices/plan links; no assertion is made that the two repositories share a single configuration.
- Authentication is confirmed in native agent startup (`src-tauri/src/cleanup_session.rs:396–401`) and conversation (`src-tauri/src/remote_agent.rs:134–143`). Authentication is not proof of paid subscription gating. Describe advertised tiers separately from enforcement.

## Public URL retrieval register

All retrieved **2026-10-21** with read-only WebFetch. Page text is mutable; refresh pricing/availability within 30 days and before publication. No browser interaction was needed; relevant `blog-factcheck` and `browser-automation` skills were loaded.

| Exact URL | Actual result / evidence |
| --- | --- |
| https://breathing-room.chatic.ai/ | Retrieved rendered marketing text: free preview, sample-data warning, daily runtime constraints, $5 monthly/$50 annual plans, $10 annual saving, renewal/tax disclosure and checkout links. Pricing section: https://breathing-room.chatic.ai/#pricing . |
| https://breathing-room.chatic.ai/download/ | Retrieved preview version/requirements, free-account gate, Python warning, three provider options, optional unchecked email preference and download measurement disclosure. No sign-in attempted. |
| https://breathing-room.chatic.ai/checkout/monthly/ | Retrieved $5 USD/month offer and sign-in gate; no Stripe checkout session or purchase attempted. |
| https://breathing-room.chatic.ai/privacy/ | Retrieved policy effective October 20, 2026, local/hosted boundary, provider disclosures and qualified seven-day retention language. Policy statements are not runtime audits. |
| https://github.com/bucabay/breathing-room-app/releases/tag/v0.1.0-preview.1 | Retrieved public “Pre-release” page and release caveats, including no clean-machine/physical-Intel validation. Page links tag to commit `e0cb8c7dbdb437ab931fe03d0e0264edc7afac89`, distinct from inspected local HEAD. Assets section reports seven assets but its listing was dynamically loading; no binary validation inferred. |

Additional exact configured URLs, **not independently fetched in this task**:

- Updater: https://raw.githubusercontent.com/bucabay/breathing-room-app/main/updates/preview.json — A `src-tauri/tauri.conf.json:59`.
- Universal update archive: https://github.com/bucabay/breathing-room-app/releases/download/v0.1.0-preview.1/Breathing-Room_0.1.0-preview.1_universal.app.tar.gz — A `updates/preview.json:7,11`.
- Annual sign-in/offer: https://breathing-room.chatic.ai/checkout/annual/ — W `src/pages/index.astro:124–129`, route implementation `src/pages/checkout/[plan].astro:8–15,43–44`.

## Unverified claims / publication blockers

These are **blocked claims**, not reasons to invent facts or to mark every implemented feature absent:

1. **Production readiness, current binary feature parity, clean-machine installation, physical Intel execution:** published release explicitly limits validation; local HEAD differs from tagged release. Need independent installer/runtime QA and version-specific feature mapping.
2. **Developer ID/notarization now complete:** contradicted by inspected preview disclosures; requires new release and actual signature/notarization evidence.
3. **Successful end-to-end upgrade:** first preview establishes the feed; needs two-version upgrade testing, including failure/offline/busy cases. No updater install was attempted.
4. **Guaranteed savings, performance/speedup, risk-free cleanup or complete attribution:** no benchmark or hands-on measurement gathered. Sample figures such as 12.4 GB and advertised 14.5 MB installer size are not independently measured results. Trash movement is not immediate free-space recovery (`README.md:97–100`; `cleanup_tools.rs:92–100`).
5. **All assistant features work offline or without an account:** contradicted by native authentication/network paths. Conversely, do not claim a subscription is required for every local tool.
6. **Exact AI allowance, unlimited use, trial terms or server-side paid gating:** not established by scoped code/public offer. Backend review and permitted account-level testing required; no credentials/accounts accessed here.
7. **Seven-day guaranteed deletion, no data sharing/training, security certification:** policy/provider assertions are not independently established by the desktop source. Require separate backend/provider verification.
8. **Guaranteed Python availability or all cleanup adapters compatible on every Mac:** bridge/path rules and catalogue are not cross-machine compatibility tests.

No planned-only feature was promoted to confirmed implementation. No roadmap delivery date, Windows/Linux support, malware removal, full app uninstaller or certified duplicate-finder capability was established in this review; do not infer either support or definitive absence without targeted evidence.

## Validation performed

- Read-only source/configuration cross-checks and five public page retrievals above completed; evidence separates local implementation, public offer and runtime unknowns.
- Attempted `node --experimental-strip-types --test tests/readme.test.mjs tests/release-config.test.mjs tests/daily-care.test.ts tests/ai-care.test.ts tests/updates.test.ts`: **not run**, exit 127 (`zsh:1: command not found: node`). Common `/opt/homebrew/bin/node` and `/usr/local/bin/node` locations were absent. No runtime was installed or settings changed.
- Read-only Python structural checks **passed**: 108 cited file/range references exist; version `0.1.0-preview.1` matches app/native config/local feed/website; updater key/feed match; both architecture entries use the same archive; USD prices and $10 annual arithmetic match; direct entitlement configuration and marketing price literals match. These do not substitute for the unavailable Node suite or native/runtime QA.
- No app/site build or native tests run; avoided build-wrapper installation side effects and any cleanup-capable execution. Draft remains subject to independent editorial/runtime verification. Only this report and the required runtime receipt are owned outputs; queue/PLAN state is unchanged.
