# Content worker controls

## Operation

`scripts/content-worker.py` uses a local SQLite outcome ledger and an exclusive dispatcher lock. Every tick admits at most three dependency-ready jobs, each as a separate `opencode run` session. OpenCode's existing permission policy remains in force: this runner deliberately does **not** pass `--auto` or broaden tool permissions. A permission/authentication blocker must be resolved explicitly, not bypassed.

Receipts require matching job ID, `done` status, existing in-scope output files, and validation results. This detects missing output; it does not independently prove editorial truth. Article-review jobs must provide that separate gate. Blocked jobs require manual retry. In-progress dispatcher interruptions also block rather than duplicate work.

```sh
python3 scripts/content-worker.py validate
python3 scripts/content-worker.py tick --dry-run
python3 scripts/content-worker.py status
python3 scripts/content-worker.py pause
python3 scripts/content-worker.py resume
python3 scripts/content-worker.py retry sources
```

Queue definitions: `docs/content/queue.json`. Runtime ledger, logs and receipts: `docs/content/.runtime/` (gitignored). Keep task IDs stable when extending the queue. New jobs must have unique IDs and acyclic dependencies. A tick launches one batch, not an endless drain; the next timer handles newly ready work.

## macOS schedule

Label: `ai.chatic.breathing-room.content`.
LaunchAgent: `~/Library/LaunchAgents/ai.chatic.breathing-room.content.plist`.
Interval: 600 seconds. It runs only while the Mac is awake and the user is logged in; missed ticks do not imply cloud execution. No production deployment is scheduled.

Installation verified 2026-10-21 with `launchctl print`: loaded, interval 600 seconds, initially idle with zero runs. First batch will be admitted by the timer; this is not evidence an article job has completed. Python executable is `/opt/homebrew/opt/python@3.14/bin/python3.14`; update the plist if Homebrew removes that version. Queue validation and the three dispatcher tests passed at installation.

Subsequent first-run inspection: all three CLI invocations exited with provider transport failures (`WebSocket closed with code 1006`). The shared service continued and produced late receipts. After inspecting the artifacts and validating receipts, capabilities/editorial were recovered as done (research/policy only, not publication approval). Source discovery's receipt explicitly says blocked and remains blocked. Inspect shared-service sessions and late receipts before retrying a transport-failed job. Browser discovery is separately blocked by the unavailable Chrome DevTools endpoint at `http://127.0.0.1:9333/json/version` (two failed attempts). No AlternativeTo seed relationships have been verified by browser yet.

```sh
launchctl print gui/$(id -u)/ai.chatic.breathing-room.content
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/ai.chatic.breathing-room.content.plist
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.chatic.breathing-room.content.plist
```

`pause` stops new batches without interrupting active jobs; `resume` enables the next timer tick. `bootout` unloads scheduling and may terminate a running dispatcher; inspect its OpenCode sessions before retrying interrupted jobs (the shared service can outlive a CLI client). This worker does not deploy, push or commit changes. Review both repositories' diffs before any release.
