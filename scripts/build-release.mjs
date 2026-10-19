// Builds signed updater archives without installing/relaunching the local app.
// Secrets are inherited from the release environment; never printed or saved.
import { spawnSync } from "node:child_process";
import { createRequire } from "node:module";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
const root = fileURLToPath(new URL("../", import.meta.url));
const config = JSON.parse(readFileSync(new URL("../src-tauri/update-config.json", import.meta.url), "utf8"));
if (!config.endpoint || !config.publicKey?.trim()) throw new Error("Configure src-tauri/update-config.json with the HTTPS feed and signing public key first.");
const endpoint = new URL(config.endpoint);
if (endpoint.protocol !== "https:" || endpoint.username || endpoint.password || endpoint.hash) throw new Error("The update feed must use HTTPS without embedded credentials.");
if (!process.env.TAURI_SIGNING_PRIVATE_KEY) throw new Error("Supply TAURI_SIGNING_PRIVATE_KEY from your secure release environment; do not commit it.");
const args = process.argv.slice(2);
if (args.some(arg => ["--debug", "--config", "-c", "--no-bundle", "--bundles", "-b"].includes(arg) || arg.startsWith("--config=") || arg.startsWith("--bundles="))) throw new Error("Release builds use fixed signing/bundling settings. Only pass target/compiler options.");
const require = createRequire(import.meta.url);
const cli = join(dirname(require.resolve("@tauri-apps/cli/package.json")), "tauri.js");
const override = { bundle: { createUpdaterArtifacts: true }, plugins: { updater: { pubkey: config.publicKey, requireSignedVersion: true } } };
const result = spawnSync(process.execPath, [cli, "build", "--bundles", "app,dmg", "--config", "src-tauri/tauri.direct.conf.json", "--config", JSON.stringify(override), ...args], { cwd: root, stdio: "inherit" });
if (result.error) throw result.error;
process.exit(result.status ?? 1);
