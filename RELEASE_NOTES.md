# Breathing Room 0.1.0-preview.2

**Preview build for testing and development. Not a production-ready release.**

## What's new

- **Monthly cleanup allowance.** Free accounts get 4 agent cleanups per calendar
  month. AI Care includes 100 cleanups per month. One cleanup is one new agent
  run; reviewing an existing plan, local scans, and approving saved actions do
  not spend another slot. The allowance resets on the 1st of each month.
- **Clear allowance prompts.** When the allowance is used up, a top banner explains
  the limit and remaining reset date, and the app offers AI Care. Local tools
  still work without a subscription.
- **Restart guidance for swap.** When swap in use (or swap files on disk) reaches
  2 GB, the Space view shows a visible recommendation to restart. macOS rebuilds
  swap and the sleep image at boot; Breathing Room never deletes them while macOS
  is using them.
- **Command-line diagnostics.** The same Rust package now offers a read-only CLI
  for storage scans, app/process summaries, and disk measurements. Run
  `breathing-room --help` for the available commands.
- **More reliable local inspection.** Additional restart-space measurement,
  process and inventory improvements, and a more resilient inference fallback
  chain for hosted AI Care.

## Download

- Universal installer for Apple Silicon and Intel Macs, macOS 13 or later.
- Free DMG installer; no separate app purchase.
- Apple Development signed, **not Developer ID signed or notarized**. macOS
  may block this build. We do not recommend disabling Gatekeeper or system-wide
  security protections.
- Verify the DMG against `SHA256SUMS.txt` before installing.
- Open the DMG, drag Breathing Room to Applications, eject the DMG, then launch
  the Applications copy. Run it from Applications so later in-app updates can
  replace the installed bundle rather than a read-only disk-image copy.

## What is included

- Storage views, app/process activity, CPU and memory monitoring.
- Reviewable local cleanup with explicit approval boundaries.
- Optional hosted AI Care at $5 USD/month or $50 USD/year. A subscription is not
  required for the local tools. AI requests may send questions and relevant tool
  results, including paths, to the configured hosted service.
- Apache-2.0 app source with a NOTICE and preserved Seal MIT attribution.
- Google, GitHub, and email sign-in. The website asks for a free account before
  starting its download; public GitHub downloads and in-app updates remain public.

## Known limitations

- Intended for testing and development; expect bugs. Back up important data and
  review every cleanup action before approving it.
- Python 3.10+ is required for disk inventory and legacy cleanup scripts; it is
  not bundled. Supported locations: `/opt/homebrew/bin/python3`,
  `/usr/local/bin/python3`, or `/usr/bin/python3`.
- In-app updates are configured with a pinned public key and HTTPS preview feed.
  Downloads, installation, and restart require your approval. Update signatures
  do not mean the app is Apple-notarized. This preview continues the existing
  feed; cross-version installation from the previous preview still needs a real
  installed upgrade test.
- Scheduled care requires the app to remain running, including in the menu bar.
  Busy or low-battery Macs may run later.
- The direct-distribution build is not App Sandbox restricted. macOS privacy
  permissions still apply; inaccessible locations can produce partial results.
- Build and automated tests were verified on the development Mac, not a separate
  clean-machine installation. No claim of clean-machine release validation.
- Both Mach-O architectures are included; Intel runtime behavior has not been
  tested on a physical Intel Mac.

Source is app-only; the website and hosted service implementation remain private.
