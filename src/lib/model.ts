export type Profile = "everyday" | "developer" | "builder" | "creator";
export type Page = "home" | "space" | "apps" | "daily" | "assistant" | "activity";
export type StorageView = "category" | "owner" | "project";
export interface Settings {
  profiles: Profile[]; enabled: boolean; hour: number; windowHours: number;
  minimumFreeGb: number; automaticCleanup: boolean; cleanupRules: string[]; scanPaths: string[];
  keepInMenuBar: boolean;
}
export interface StorageGroup {
  id: string; name: string; category: string; owner: string; project: string; bytes: number; files: number;
}
export interface Candidate {
  id: string; name: string; path: string; bytes: number; description: string; method: string; executable: boolean;
}
export interface LargeFile { path: string; bytes: number; identity: string; removable: boolean }
export interface Capabilities { sandboxed: boolean; cacheCommands: boolean; cloudAi: boolean }
export interface StorageReport {
  directories?: { path: string; name: string; parent: string; bytes: number; partial: boolean }[];
  usedBytes?: number; identifiedBytes?: number; unmappedBytes?: number; coveragePercent?: number; inventoryMethod?: string;
  totalBytes: number; availableBytes: number; scannedBytes: number; fileCount: number;
  partial: boolean; skipped: number; scannedAt: number; roots: string[];
  groups: StorageGroup[]; candidates: Candidate[]; warnings: string[];
  largeFiles: LargeFile[];
}
export interface Process {
  cpuAvailable?: boolean;
  pid: number; parentPid: number; uid: number; cpu: number; memoryBytes: number;
  started: string; executable: string; name: string; app: string; protected: boolean;
}
export interface AppGroup {
  cpuAvailable?: boolean;
  id: string; name: string; bundlePath: string | null; cpu: number; memoryBytes: number; processes: Process[];
  metricsAvailable: boolean; canQuit: boolean; coverage: string;
}
export interface CareEvent { id: string; timestamp: number; title: string; detail: string; recoveredBytes: number; kind: string }
export interface SavedState { settings: Settings; history: CareEvent[]; lastDailyDay: string }
export interface Bucket { id: string; name: string; bytes: number; files: number; color: string; groups: StorageGroup[] }
export const categories: Record<string, { name: string; color: string }> = {
  development: { name: "Development", color: "#8b5cf6" },
  images: { name: "Images", color: "#ef9855" },
  video: { name: "Video", color: "#ec6d98" },
  audio: { name: "Music & audio", color: "#dcac33" },
  documents: { name: "Documents", color: "#3b82f6" },
  downloads: { name: "Downloads", color: "#16a085" },
  apps: { name: "Applications", color: "#4b65d2" },
  "app-data": { name: "App data", color: "#4b65d2" },
  backups: { name: "Backups", color: "#719bb3" },
  system: { name: "macOS & system data", color: "#719bb3" },
  unmapped: { name: "Unmapped storage", color: "#a3aab6" },
};
export const defaultSettings: Settings = {
  profiles: ["everyday"], enabled: false, hour: 9, windowHours: 3, minimumFreeGb: 20,
  automaticCleanup: false, cleanupRules: [], scanPaths: [],
  keepInMenuBar: true,
};
export function formatBytes(bytes: number): string {
  if (!Number.isFinite(bytes) || bytes < 0) return "Unavailable";
  if (bytes >= 1e12) return `${(bytes / 1e12).toFixed(1)} TB`;
  if (bytes >= 1e9) return `${(bytes / 1e9).toFixed(1)} GB`;
  if (bytes >= 1e6) return `${Math.round(bytes / 1e6)} MB`;
  if (bytes >= 1e3) return `${Math.round(bytes / 1e3)} KB`;
  return `${bytes} B`;
}
export function buckets(groups: StorageGroup[], view: StorageView): Bucket[] {
  const map = new Map<string, Bucket>();
  for (const group of groups) {
    const id = view === "category" ? group.category : view === "owner" ? group.owner : group.project || "Outside projects";
    const existing = map.get(id) ?? {
      id, name: view === "category" ? categories[id]?.name ?? id : id,
      bytes: 0, files: 0, color: categories[group.category]?.color ?? "#719bb3", groups: [],
    };
    existing.bytes += group.bytes; existing.files += group.files; existing.groups.push(group); map.set(id, existing);
  }
  return [...map.values()].sort((a, b) => b.bytes - a.bytes);
}
export function profileBuckets(list: Bucket[], profiles: Profile[]): Bucket[] {
  // Default ordering remains by actual consumption. Profiles add relevant emphasis,
  // not imaginary storage estimates or hidden categories.
  return list.map((item) => ({ ...item, name: item.name === "Development" && profiles.includes("builder") ? "Projects & development" : item.name }));
}
export function profileFocus(groups: StorageGroup[], profiles: Profile[]): Bucket | undefined {
  const list = buckets(groups, "category");
  const focus = profiles.includes("developer") || profiles.includes("builder") ? ["development"] :
    profiles.includes("creator") ? ["images", "video", "audio"] : ["downloads", "app-data"];
  return list.find((item) => focus.includes(item.id)) ?? list[0];
}
export function dailyDue(settings: Settings, lastDay: string, date: Date): boolean {
  const day = `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`;
  const elapsed = (date.getHours() + 24 - settings.hour) % 24;
  return settings.enabled && lastDay !== day && elapsed < settings.windowHours;
}
export function localSummary(report: StorageReport | null, apps: AppGroup[]): string[] {
  const findings: string[] = [];
  if (report) {
    const largest = buckets(report.groups, "category")[0];
    if (largest) findings.push(`${largest.name} is the largest measured category at ${formatBytes(largest.bytes)}. Size alone does not make it disposable.`);
    if (report.candidates.length) findings.push(`${report.candidates.length} supported cache rules are available to review. Package downloads may be needed again.`);
    if (report.partial) findings.push("Some folders could not be fully scanned. The report covers measured files only.");
  }
  const top = [...apps].filter((a) => a.id !== "system" && a.metricsAvailable).sort((a, b) => b.memoryBytes - a.memoryBytes)[0];
  if (top) findings.push(`${top.name} has the largest sampled process-memory total. Shared memory may be counted more than once; this is not a leak diagnosis.`);
  return findings;
}
