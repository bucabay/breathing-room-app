# Content worker controls

## Operation

`scripts/content-worker.py` maintains **three persistent worker slots**, each holding an exclusive slot lock. The LaunchAgent is now a **600-second watchdog**: it starts only missing slots, rather than waiting for a whole three-job batch to finish. Each worker atomically claims one dependency-ready job, runs a separate `opencode run` session, records its outcome, and immediately takes the next ready item. Idle slots check for newly ready work every ten seconds. No more than three managed agent attempts run concurrently.

Every scheduled worker invocation explicitly pins `--model openai/gpt-6-luna` (full GPT Luna, not Fast); do not rely on a mutable OpenCode default. OpenCode's existing permission policy remains in force: this runner deliberately does **not** pass `--auto` or broaden tool permissions. A permission/authentication blocker must be resolved explicitly, not bypassed. During handoff, `slot-N-external.json` reserves a slot for an already-running setup agent. Its actual completion notification, outputs and receipt are reconciled before that reservation is removed. Reserved slots do not launch another model agent, so two live setup agents plus one scheduled agent are still three, not five. Reservations never expire merely because a timeout passed.

Attempt-specific receipts require matching job ID, `done` status, existing in-scope output files, and validation results. This detects missing output; it does not independently prove editorial truth. Article-review jobs must provide that separate gate. Blocked jobs require manual retry. A disconnected CLI can leave the shared-service agent alive: the attempt becomes `uncertain` and holds its worker slot until its actual terminal receipt arrives. Late receipts are reconciled automatically; transport failure never authorizes a duplicate attempt. A restarted slot also reconciles its prior attempt before claiming new work.

All shared site builds/reviews use the `site-build` resource, atomically exclusive across workers. Research/draft jobs own separate packet/record/asset paths and do not write shared navigation, indexes, schema, queue or build output. The expanded queue has **1371 jobs**:150 research handoffs; separate draft/review assignments for each product's tool profile, head-to-head comparison, alternatives guide and workflow blog; five roundup draft/review pairs; foundation/baseline/directory work; and final audit. Nominal page targets:600 competitor-intent pages plus five roundups, minus any evidence-backed alias/exclusion exceptions. Alias/exclusion notes do not count as finished pages.

The coordinator runs every600seconds, preserves original blocked outcomes in an append-only SQLite transition history, and admits retained research packets to **unpublished drafting only** when official identity, documented function and platform facts have source excerpts. This fixes the former bottleneck where missing screenshot permission stopped every draft. Original packets and unknowns remain untouched. An attributed official image/guide link plus an original sourced workflow diagram is the approved rights-safe visual alternative; restricted screenshots are never copied. Independent review still gates publication.

Five user-requested roundups have drafting priority1; per-product comparison/profile/alternatives/workflow drafting follows, then independent review and remaining research. Drafting no longer waits behind a pilot image-permission deadlock. Each product reuses its completed75-product baseline batch and retained research. Unknown identity/substantive facts remain blocked, not invented. `PROGRESS.md` and `.runtime/progress.json` distinguish research outcomes, written files, approved flags, active assignments and remaining blockers; approved local flags are not a production-deployment report.

```sh
python3 scripts/content-worker.py validate
python3 scripts/content-worker.py tick --dry-run
python3 scripts/content-worker.py status
python3 scripts/content-worker.py status --all-jobs
python3 scripts/content-worker.py pause
python3 scripts/content-worker.py resume
python3 scripts/content-worker.py retry sources
```

Queue definitions: `docs/content/queue.json`; reproducible expansion: `scripts/expand-content-queue.py`. Runtime ledger, slot locks, attempt metadata, logs and receipts: `docs/content/.runtime/` (gitignored). Keep task IDs stable when extending the queue. New jobs must have unique IDs and acyclic dependencies. Queue expansion is atomic so live readers never see a partially written manifest.

## macOS schedule

Label: `ai.chatic.breathing-room.content`.
LaunchAgent: `~/Library/LaunchAgents/ai.chatic.breathing-room.content.plist`.
Interval: 600 seconds. It runs only while the Mac is awake and the user is logged in; missed ticks do not imply cloud execution. No production deployment is scheduled.

Installation verified 2026-10-21 with `launchctl print`: loaded, interval 600 seconds, initially idle with zero runs. First batch will be admitted by the timer; this is not evidence an article job has completed. Python executable is `/opt/homebrew/opt/python@3.14/bin/python3.14`; update the plist if Homebrew removes that version. Queue validation and the three dispatcher tests passed at installation.

Historical first-run issue: CLI streams failed with `WebSocket closed with code 1006`, but shared-service agents later produced receipts. Capabilities/editorial were recovered after validation. Browser access has since been restored, both true seeds confirmed (CleanMyMac and Mole), and 19 pages yielded 150 competitor listing identities. The current persistent-slot implementation handles late receipts without blind retries. Current captures and official-source verification remain distinct from discovery or article publication approval.

```sh
launchctl print gui/$(id -u)/ai.chatic.breathing-room.content
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/ai.chatic.breathing-room.content.plist
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.chatic.breathing-room.content.plist
```

`pause` stops new claims without interrupting active jobs; persistent slots stay alive and wait. `resume` lets existing slots claim again immediately; run `tick` to start missing slots without waiting for the watchdog. `bootout` unloads only the watchdog, **not detached worker slots**: pause first if you want all new work stopped. Never kill/retry an attempt without checking its shared-service session and terminal receipt. This worker does not deploy, push or commit changes. Review both repositories' diffs before any release. Slots may be idle when dependencies, evidence or authentication block work; the watchdog maintains three slot processes, not fake useful activity or an unlimited article-production guarantee.

## Authorized browser recovery

User explicitly authorized starting the existing automation profile on 2026-10-21. Source: `/Users/gabe/code/indeed-apply/AGENTS.md:79–83` and `scripts/run_pipeline.py:39–49`. Check `lsof -nP -iTCP:9333 -sTCP:LISTEN` first. Only if no listener exists, start the **same existing profile**, not everyday Chrome or a new profile:

```sh
/usr/bin/open -na 'Google Chrome' --args --remote-debugging-port=9333 --user-data-dir=/Users/gabe/.chrome-indeed-automation --no-first-run --no-default-browser-check about:blank
```

Allow startup to complete, then verify with Chrome DevTools `list_pages`. Never kill an existing listener, read/reuse unrelated tabs, or restart job-application workers. Create owned background tabs for research and close only those tabs. Stop at login/challenge gates. This recovery restored browser access and enabled full source discovery; the historical outage above no longer blocks the source job.
