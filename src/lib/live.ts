export interface AlertConfig { enabled: boolean; cpuEnabled: boolean; writesEnabled: boolean; cpuThreshold: number; writeMbPerSecond: number; sustainedSeconds: number; cooldownSeconds: number }
export const defaultAlerts: AlertConfig = { enabled:true, cpuEnabled:true, writesEnabled:true, cpuThreshold:100, writeMbPerSecond:50, sustainedSeconds:30, cooldownSeconds:300 };
export interface MonitorConfig { enabled: boolean; fileEvents: boolean; processIo: boolean; intervalSeconds: number; alerts: AlertConfig }
export interface Anomaly { id:number; kind:string; name:string; path:string; value:number; threshold:number; since:number; acknowledged:boolean }
export interface LiveStatus {
  appGroups?: import("./model").AppGroup[]; coreCount?: number; diskTimestamp?: number; cached?: boolean;
  anomalies?: Anomaly[]; topCpuApps?: {name:string;path:string;cpu:number}[];
  ready: boolean; timestamp?: number; totalBytes?: number; availableBytes?: number; freeChangeBytes?: number | null;
  cpuPercent?: number | null; processCount?: number; appCount?: number; readBytesPerSecond?: number | null;
  writeBytesPerSecond?: number | null; sampledIoProcesses?: number; monitorCpuPercent?: number;
  monitorMemoryBytes?: number | null; sampleMs?: number; config?: MonitorConfig;
  memoryUsedBytes?: number | null; memoryTotalBytes?: number | null;
  watching?: boolean; dropped?: number; watchError?: string; processError?: string; databaseError?: string; databasePath?: string; coverage?: string;
  minute?: { appsStarted: number; processesStarted: number; filesCreated: number; fileChanges: number; foldersCreated: number };
  history?: { timestamp: number; availableBytes: number; cpuPercent: number | null; memoryPercent?: number | null; writeBytesPerSecond: number }[];
  topWriters?: { name: string; path: string; bytesPerSecond: number }[];
}
export interface ActivityEntry {
  id: number; timestamp: number; kind: string; path: string; owner: string; workflow: string; attribution: string;
  pid: number | null; flags: number; sizeBytes: number | null; deltaBytes: number | null;
  readBytes: number; writeBytes: number; detail: string;
}
export interface ActivityGroup { owner: string; workflow: string; bytes: number; events: number; path: string }
export interface ActivityLog { events: ActivityEntry[]; growth: ActivityGroup[]; writers: ActivityGroup[]; diskHistory: { timestamp: number; totalBytes: number; availableBytes: number; cpuPercent: number | null }[]; storedEvents: number; retentionDays: number }
export const initialMonitorConfig: MonitorConfig = { enabled: true, fileEvents: true, processIo: true, intervalSeconds: 5, alerts:defaultAlerts };
export function demoLive(): LiveStatus {
  const saved = JSON.parse(localStorage.getItem("breathing-room-monitor-preview") ?? "null");
  const config = {...initialMonitorConfig,...saved,alerts:{...defaultAlerts,...saved?.alerts}};
  const timestamp = Math.floor(Date.now()/1000);
  return { ready: true, timestamp, config, watching: config.enabled, totalBytes: 512e9, availableBytes: 88.4e9,
    freeChangeBytes: -12e6, cpuPercent: config.enabled ? 18 : null, processCount: 412, appCount: 16,
    readBytesPerSecond: config.enabled && config.processIo ? 1.1e6 : null, writeBytesPerSecond: config.enabled && config.processIo ? 2.8e6 : null,
    sampledIoProcesses: 320, monitorCpuPercent: .6, monitorMemoryBytes: 45e6, memoryUsedBytes:config.enabled?10e9:null,memoryTotalBytes:config.enabled?16e9:null,sampleMs: 24, dropped: 0,
    minute: config.enabled ? { appsStarted: 2, processesStarted: 7, filesCreated: 12, fileChanges: 28, foldersCreated: 3 } : { appsStarted: 0, processesStarted: 0, filesCreated: 0, fileChanges: 0, foldersCreated: 0 },
    history: [10,18,12,15,30,22,38,18,24,16,18].map((cpuPercent,i)=>({timestamp:timestamp-(10-i)*5,availableBytes:88.4e9,cpuPercent,memoryPercent:[54,55,56,55,58,59,60,61,60,62,62.5][i],writeBytesPerSecond:(i%4+1)*1e6})),
    databasePath: "Desktop app · local activity.sqlite", topWriters: [{name:"Visual Studio Code",path:"/Applications/Visual Studio Code.app",bytesPerSecond:2e6}] };
}
export function demoLog(): ActivityLog {
  const timestamp=Math.floor(Date.now()/1000);
  const events: ActivityEntry[] = [
    { id: 7, timestamp, kind: "file_changed", path: "/Users/example/code/website/.next/cache/webpack/client.pack", owner: "Project tools", workflow: "code/website", attribution: "Path inference · writer unknown", pid: null, flags: 4096, sizeBytes: 230e6, deltaBytes: 25e6, readBytes: 0, writeBytes: 0, detail: "Observed allocated growth; not exact write throughput" },
    { id: 6, timestamp: timestamp-5, kind: "app_started", path: "/Applications/Figma.app", owner: "Figma", workflow: "Apps", attribution: "Observed bundle transition", pid: 1001, flags: 0, sizeBytes: null, deltaBytes: null, readBytes: 0, writeBytes: 0, detail: "New app observed in successful process snapshot" },
    { id: 5, timestamp: timestamp-6, kind: "folder_created", path: "/Users/example/code/website/.next/cache/images", owner: "Project tools", workflow: "code/website", attribution: "Path inference · writer unknown", pid: null, flags: 131328, sizeBytes: null, deltaBytes: null, readBytes: 0, writeBytes: 0, detail: "Folder creation notification" },
    { id: 4, timestamp: timestamp-10, kind: "process_io", path: "/Applications/Visual Studio Code.app", owner: "Visual Studio Code", workflow: "Process I/O", attribution: "Observed counter delta · not file attribution", pid: null, flags: 0, sizeBytes: null, deltaBytes: null, readBytes: 1e6, writeBytes: 4e6, detail: "Sampled read/write counters" },
    { id: 3, timestamp: timestamp-12, kind: "file_created", path: "/Users/example/Downloads/video-export.mov", owner: "Unattributed", workflow: "Downloads", attribution: "Path inference · writer unknown", pid: null, flags: 256, sizeBytes: 500e6, deltaBytes: 500e6, readBytes: 0, writeBytes: 0, detail: "Estimated zero baseline for newly observed creation" },
  ];
  return { events, diskHistory:[89.1,89,89,88.8,88.9,88.8,88.5,88.6,88.4].map((gb,i)=>({timestamp:timestamp-(8-i)*60,totalBytes:512e9,availableBytes:gb*1e9,cpuPercent:18})), growth: [{owner:"Project tools",workflow:"code/website",bytes:230e6,events:42,path:events[0].path},{owner:"Unattributed",workflow:"Downloads",bytes:500e6,events:1,path:events[4].path}],
    writers:[{owner:"Visual Studio Code",workflow:"Observed process I/O",bytes:80e6,events:12,path:"/Applications/Visual Studio Code.app"}], storedEvents: 1250, retentionDays: 7 };
}
