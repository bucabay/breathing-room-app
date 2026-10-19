import { defaultSettings, type SavedState, type StorageReport, type AppGroup } from "./model";
const gb = 1e9;
export const demoReport: StorageReport = {
  totalBytes: 512 * gb, availableBytes: 88.4 * gb, scannedBytes: 286.8 * gb, fileCount: 84100,
  partial: true, skipped: 3, scannedAt: Date.now() / 1000, roots: ["~/Downloads", "~/Projects", "~/Pictures"],
  warnings: ["Example data for the browser preview. Open the desktop app to scan your Mac."],
  largeFiles: [
    { path: "/Users/example/Movies/Brand film — final export.mp4", bytes: 8.4 * gb, identity: "preview-film", removable: true },
    { path: "/Users/example/Downloads/Design assets.zip", bytes: 2.1 * gb, identity: "preview-assets", removable: true },
  ],
  groups: [
    { id: "dev-site", name: "Projects", category: "development", owner: "Projects & tools", project: "Website", bytes: 34.8 * gb, files: 30000 },
    { id: "dev-api", name: "Projects", category: "development", owner: "Projects & tools", project: "API", bytes: 24 * gb, files: 12000 },
    { id: "npm", name: "npm", category: "development", owner: "npm", project: "", bytes: 6.2 * gb, files: 6000 },
    { id: "uv", name: "Python", category: "development", owner: "Python / uv", project: "", bytes: 4 * gb, files: 3000 },
    { id: "images", name: "Images", category: "images", owner: "Personal files", project: "", bytes: 82.4 * gb, files: 15000 },
    { id: "video", name: "Video", category: "video", owner: "Personal files", project: "", bytes: 54.8 * gb, files: 800 },
    { id: "chrome", name: "Google Chrome", category: "app-data", owner: "Google Chrome", project: "", bytes: 12.3 * gb, files: 6200 },
    { id: "slack", name: "Slack", category: "app-data", owner: "Slack", project: "", bytes: 3.8 * gb, files: 3000 },
    { id: "downloads", name: "Downloads", category: "downloads", owner: "Personal files", project: "", bytes: 21.6 * gb, files: 800 },
    { id: "documents", name: "Documents", category: "documents", owner: "Personal files", project: "", bytes: 19.7 * gb, files: 6200 },
    { id: "backups", name: "Backups", category: "backups", owner: "Device backups", project: "", bytes: 23.2 * gb, files: 1100 },
  ],
  candidates: [
    { id: "npm", name: "npm download cache", path: "~/.npm/_cacache", bytes: 6.2 * gb, description: "Downloaded packages, separate from your project dependencies. Downloads are recreated when needed.", method: "npm cache clean --force", executable: true },
    { id: "uv", name: "Unused Python cache", path: "~/.cache/uv", bytes: 4 * gb, description: "Uses uv's supported pruning. Measured cache size is not a promise of recovered space.", method: "uv cache prune", executable: true },
  ],
};
function demoApp(name: string, id: string, cpu: number, memory: number, count: number): AppGroup {
  return { id, name, bundlePath: `/Applications/${name}.app`, cpu, memoryBytes: memory * gb,
    metricsAvailable: true, canQuit: true, coverage: "Observed app processes",
    processes: Array.from({ length: count }, (_, n) => ({
      pid: 400 + count * 10 + n, parentPid: 1, uid: 501, cpu: cpu / count, memoryBytes: memory * gb / count,
      started: "Example", executable: `/Applications/${name}.app/Contents/MacOS/${name}`,
      name: n === 0 ? name : `${name} helper ${n}`, app: name, protected: false,
    })) };
}
export const demoApps = [demoApp("Google Chrome", "chrome", 34, 2.4, 12), demoApp("Visual Studio Code", "code", 18, 1.6, 8),
  demoApp("Figma", "figma", 7, 0.82, 4), demoApp("Slack", "slack", 3, 0.61, 5), demoApp("Terminal", "terminal", 2, 0.22, 3)];
export const demoState: SavedState = { settings: { ...defaultSettings, profiles: ["developer", "builder"] }, history: [], lastDailyDay: "" };
