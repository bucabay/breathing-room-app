# Breathing Room

A free, open-source macOS maintenance app. Understand storage, inspect app
activity, and review cleanup before approving changes.

## What is included

This repository contains the React/Tauri desktop app, native local tools,
cleanup scripts, and app tests. The marketing website, hosted AI/billing backend,
internal business documents, signing credentials, and private repository history
are not included.

Local storage views, inspection, manual cleanup, and CPU/memory monitoring do not
require an AI Care subscription. The optional hosted AI Care service is separate:
$5 USD/month or $50 USD/year. Open-source licensing does not grant free hosted
service access. AI requests can send questions and relevant inspection results
(including paths) to the configured service; local inspection/cleanup runs on
your Mac. The source currently defaults to the official hosted API origin in
src/agent-config.json. It contains no service credentials. A compatible service
origin can be configured with BREATHING_ROOM_API_URL.

## Development

Requires macOS 13+, Node.js 22.13+, pnpm, Rust, and Xcode Command Line Tools.

```sh
pnpm install
pnpm dev             # browser preview with example data
pnpm tauri dev       # native app; reads real local data
pnpm build
pnpm test
cargo test --manifest-path src-tauri/Cargo.toml
python3 -m unittest discover -s tests -p "*_test.py"
```

## Downloads and releases

Public signed installers have not been published yet. This source snapshot is
not a claim that a notarized release or automatic updates are available.
GitHub Releases will host official installers when release verification is done.

Use the Tauri CLI directly for a local build without the install wrapper:
```sh
pnpm exec tauri build --debug --bundles app
```

The pnpm tauri build wrapper installs and relaunches the app in /Applications.
Developer ID signing, notarization, and updater signing credentials must remain
outside this repository. The release helper requires an update endpoint and
public key in src-tauri/update-config.json plus signing credentials supplied
through the release environment. It does not configure notarization for you.

## License and attribution

Apache License 2.0; see LICENSE and NOTICE. Redistributors must comply with its
license and notice requirements, including preserving applicable attribution
notices, marking modified files, and supplying the license. An in-app credit is
not required. Seal-derived UI code retains its original MIT notice in
THIRD_PARTY_LICENSES/Seal-MIT.txt. Dependencies retain their own licenses.
The license does not grant trademark rights or imply official endorsement.
