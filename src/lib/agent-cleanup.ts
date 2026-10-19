export interface AgentCleanupAction {
  id: string; title: string; reason: string; impact: string; kind: "command" | "trash";
  paths: string[]; command: string[]; cwd?: string | null; estimatedBytes: number;
  mode?: "automatic" | "permission" | "command"; nativeRule?: string;
}
export interface AgentCleanupOutcome {
  id: string; ok: boolean; detail: string; status?: "running" | "success" | "failed" | "skipped";
  beforeBytes?: number | null; afterBytes?: number | null; removedBytes?: number | null;
  percentCleaned?: number | null; pendingTrashBytes?: number;
}
export interface DiscoveryPolicy { minimumLocations:number; minimumBytes:number; usefulLocationBytes:number; maxTurns:number; maxToolCalls:number }
export const defaultDiscoveryPolicy:DiscoveryPolicy={minimumLocations:4,minimumBytes:2*1024**3,usefulLocationBytes:64*1024**2,maxTurns:24,maxToolCalls:128};
export interface StorageRisk { severity: "warning" | "critical"; recoverability: "unknown" | "not-rebuildable"; warning: string }
export interface ReviewStorageLocation extends StorageRisk {
  aliases?:string[];
  path: string; title: string; bytes: number; logicalBytes: number; modifiedAt: number;
  fileCount: number; partial: boolean; reviewOnly: true; cleanupEligible: false; requiresSelection: true;
}
export interface InventoryItem extends Partial<StorageRisk> {path:string;kind:string;category:string;bytes:number;logicalBytes:number;modifiedAt:number;owned:boolean;state:string;reviewOnly:boolean}
export interface InventoryPage {entries:InventoryItem[];offset:number;nextOffset:number|null;totalEntries:number;note:string}
export interface InventorySummary {scanId:string;filesInspected:number;directoriesInspected:number;measuredBytes:number;logicalBytes:number;partial:boolean;pendingDirectories:number;inaccessible:number;excluded:number;categories:{name:string;bytes:number;files:number}[];largest:InventoryItem[];scannedAt:number}
export interface DiscoveryAssistance {triggered:boolean;reason:string;usefulLocations:number;measuredCandidateBytes:number;policy:DiscoveryPolicy;toolCalls:number;learnedRules:number;status:string}
export interface AgentCleanupRun {
  discoveryOptions?: { dailyCare?: boolean };
  id: string; status: "inspecting" | "review" | "executing" | "done" | "failed" | "cancelled";
  model: string; request: string; overview: string; actions: AgentCleanupAction[]; approvedIds: string[];
  scope?: string;
  activity: string[]; outcomes: AgentCleanupOutcome[];
  recoveredBytes: number; sessionId?: string | null; error?: string | null; updatedAt: number;
  schemaVersion?: number; automaticEnabled?: boolean; automaticIds?: string[];
  discovery?: { candidates: AgentCleanupAction[]; manual: {path: string; reason: string}[]; reviewLocations?: ReviewStorageLocation[]; coverage: string[]; errors: string[]; snapshotHash: string;inventory?:InventorySummary|null;agent?:DiscoveryAssistance|null;pendingSources?:string[];recentFindings?:unknown[] } | null;
  results?: {schemaVersion:number;success:number;failed:number;skipped:number;beforeBytes:number|null;removedBytes:number|null;percentCleaned:number|null;pendingTrashBytes:number;availableSpaceChange:number|null;items:AgentCleanupOutcome[]} | null;
}
export interface DailyApproval {key:string;action:AgentCleanupAction;approvedAt:number}
export interface DailyNotification {runId:string;title:string;body:string;pendingCount:number;status:string;seen:boolean;updatedAt:number;recoveredBytes:number;needsAttention?:boolean}
export function cleanupMode(action:AgentCleanupAction) { return action.mode || (action.kind === "command" ? "command" : "permission"); }
export function pendingCleanupActions(run:AgentCleanupRun) { return run.actions.filter(action => !run.outcomes.some(outcome => outcome.id === action.id)); }
export interface AgentCleanupConnection {
  available: boolean; models: string[]; defaultModel?: string; message: string; url?: string;
  reachable?: boolean; authenticated?: boolean; authConfigured?: boolean; baseUrl?: string;
  account?: { subject: string; name?: string | null; email?: string | null } | null;
  usage?: { requests: number; neuronEstimate?: number | null } | null;
}
