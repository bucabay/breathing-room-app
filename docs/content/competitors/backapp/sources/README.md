<p align="center">
  <img src="docs/logo.png" alt="BackApp" width="160" />
</p>

<h1 align="center">BackApp</h1>

<p align="center">
  <strong>Backup your App / Get back your App</strong><br />
  List installed Mac apps, create snapshots, compare to your current machine, and share snapshot files.<br />
</p>

<p align="center">
  <a href="https://backapp.developer.pm/">Documentation</a> ·
  <a href="https://backapp.developer.pm/install/">Install</a> ·
  <a href="https://github.com/li-nd/BackApp/issues">Issues</a> ·
  <a href="#build">Build</a>
</p>

---

![Main window](docs/screenshots/1-main.png)

## Features

| | |
|---|---|
| **Browse** | Installed apps with categories, search, and source filters |
| **Snapshots** | Capture the current app set with name, device, and stats |
| **Compare** | Same version · not installed · different version |
| **Share** | Export / import snapshots as JSON |
| **Detail** | Local metadata + optional App Store lookup |
| **Keyboard** | `⌘N` create · `⌘⇧I`/`⌘⇧E` import/export · `⌘R` refresh · `⌘F` find |

## Install

```bash
brew tap li-nd/apps
brew trust li-nd/apps
brew install --cask backapp
```

Tap: [li-nd/homebrew-apps](https://github.com/li-nd/homebrew-apps). Or download a zip from [Releases](https://github.com/li-nd/BackApp/releases). Full notes: **[Install guide](https://backapp.developer.pm/install/)**.

> Builds are **not notarized** (ad-hoc signed). If macOS blocks the app: **System Settings → Privacy & Security → Open Anyway**, or right-click → **Open**.

## Screenshots

<p align="center">
  <img src="docs/screenshots/3-snapshot.png" alt="Create Snapshot" width="48%" />
  &nbsp;
  <img src="docs/screenshots/4-snapshot-compare.png" alt="Snapshot compare" width="48%" />
</p>
<p align="center">
  <img src="docs/screenshots/6-appstore-details.png" alt="App Store detail" width="48%" />
  &nbsp;
  <img src="docs/screenshots/5-app-detail.png" alt="App detail" width="48%" />
</p>

## Build

1. Open `BackApp.xcodeproj` in Xcode.
2. Select the **BackApp** scheme and run (`⌘R`).

## Documentation

Published site: **[backapp.developer.pm](https://backapp.developer.pm/)**

| Page | Topic |
|------|--------|
| [Install](https://backapp.developer.pm/install/) | Homebrew, Releases, build from source |
| [Usage](https://backapp.developer.pm/usage/) | Workflow and screenshots |
| [Troubleshooting](https://backapp.developer.pm/troubleshooting/) | Common issues |

### Preview docs locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-docs.txt
mkdocs serve
```

Pages deploy from `main` via [`.github/workflows/docs.yml`](.github/workflows/docs.yml) (enable GitHub Pages → GitHub Actions once).

## License

[MIT](LICENSE) © [Markus Lind](https://github.com/li-nd)
