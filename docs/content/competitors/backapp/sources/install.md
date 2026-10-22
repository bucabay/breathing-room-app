# Install

BackApp is a **macOS-only** SwiftUI app. It is not distributed via the Mac App Store.

You can install it with **Homebrew** or by **downloading a zip from GitHub Releases**.

## Homebrew

```bash
brew tap li-nd/apps
brew trust li-nd/apps
brew install --cask backapp
```

Tap: [li-nd/homebrew-apps](https://github.com/li-nd/homebrew-apps). Requires **macOS Tahoe** or newer (matches the app’s deployment target).

### Upgrade / uninstall

```bash
brew update
brew upgrade --cask backapp
brew uninstall --cask backapp
```

## GitHub Releases

1. Open [GitHub Releases](https://github.com/li-nd/BackApp/releases).
2. Download the latest macOS zip (for example `BackApp-x.y.z-macos.zip`).
3. Unzip and move `BackApp.app` to `/Applications` (or another folder you prefer).
4. Launch the app.

Use Releases if you prefer not to use Homebrew, or if you need a specific version.

## Notarization / Gatekeeper

Current BackApp builds are **ad-hoc signed and not notarized**. On first launch macOS may block the app — this applies to both Homebrew and Releases installs.

Workaround:

1. **System Settings → Privacy & Security → Open Anyway**, or  
2. Right-click the app in Finder → **Open** → confirm.

This project does **not** claim App Store or official Homebrew Cask compliance. Same policy as other apps in the [li-nd/homebrew-apps](https://github.com/li-nd/homebrew-apps) tap.

## Build from source

1. Clone the repository:
   ```bash
   git clone https://github.com/li-nd/BackApp.git
   cd BackApp
   ```
2. Open `BackApp.xcodeproj` in Xcode.
3. Select the **BackApp** scheme and a Mac destination.
4. Run (`⌘R`).

Requires a recent Xcode with a macOS SDK matching the project settings.

## Dependencies

BackApp has **no** Homebrew CLI prerequisites (no GPG, `pass`, etc.). Network is used only for App Store lookup on the app detail screen; the installed-apps list works offline.
