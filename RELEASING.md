# Universal macOS preview releases

The first preview contains a fixed HTTPS feed and pinned updater public key.
Both `darwin-aarch64` and `darwin-x86_64` use the same universal `.app.tar.gz`.
The feed is on the public `main` branch at `updates/preview.json`, rather than
GitHub's `releases/latest` endpoint, which excludes prereleases.

1. Keep the updater private key safe in your OS keychain/secret manager. Supply
   `TAURI_SIGNING_PRIVATE_KEY` only through the build environment, never a committed
   file. The matching public key is in `src-tauri/update-config.json`. Do not
   regenerate the key between releases: existing installations trust the old key.
2. Update the version in `package.json`, `src-tauri/Cargo.toml`, Cargo lockfile,
   and `src-tauri/tauri.conf.json`; update `RELEASE_NOTES.md`.
3. Install matching Rust standard libraries for both `aarch64-apple-darwin` and
   `x86_64-apple-darwin`. Run the frontend, native, and Python tests.
4. Supply Apple signing credentials through the secure release environment.
   Run `pnpm desktop:release --target universal-apple-darwin --ci`. This uses the
   direct-distribution entitlements and does not install over your local app.
   The first preview is Apple Development signed and not notarized; do not
   describe it as Developer ID signed or notarized.
5. Verify the bundle signature and both Mach-O architectures. Check the bundled
   LICENSE, NOTICE, cleanup resources, and embedded update configuration.
6. Run `node scripts/prepare-release.mjs`. It stages the DMG, updater archive,
   version-bound signature, SHA-256 checksums, and a candidate `preview.json` in
   `build/releases/vVERSION/`. Cryptographically verify the archive against the
   pinned public key and check that a modified payload is rejected.
7. Commit the release source and push it. Create a GitHub prerelease for that
   exact source revision and upload all staged assets. Verify their public URLs.
8. **Only after the assets are publicly downloadable**, copy the staged
   `preview.json` to `updates/preview.json`, commit, and push. This promotes the
   release to installed preview users. Never announce an unavailable artifact.
9. Test the feed and an isolated previous installation (not your real working
   app): check, approval, download, signature verification, installation and
   restart. Test offline behavior, busy cleanup, and bad signatures. Do not claim
   cross-version installation was verified until this has actually been done.

Checks happen automatically, but installation and restart are explicit user
actions. The first public release can only establish the feed and signed artifact;
an upgrade from it to a newer public version is verified when that version exists.
Settings, approvals, and sessions live outside the app bundle; preserve their
formats or provide migrations. Changing the Apple signing identity later may
cause macOS privacy-permission prompts to recur.
