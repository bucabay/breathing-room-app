import catalog from "../../scripts/cleanup/catalog.json";
import type { Profile } from "./model";

export interface CleanupJudgment {
  purpose: "cache" | "generated" | "personal" | "unknown"; confidence: number; relevance: number;
  disposable: number; uniqueData: number; methodSupported: number; impact: number; model: string;
}
export interface CleanupLocation {
  pluginId?: string; sizeBasis?: string; sizeComplete?: boolean; overlaps?: boolean; mountedBytes?: number;
  id: string; ruleId: string; name: string; type: string; category: string; profiles: Profile[]; path: string; bytes: number;
  files: number; complete: boolean; kind: "tool" | "trash" | "review"; adapter: string; executable: boolean;
  reason: string; description: string; impact: string; impactLevel: number; minAgeDays: number;
  source: string; evidence: string; patterns: string[]; judgment: CleanupJudgment | null; method?: string;
}
export interface CleanupPlan {
  cached?: boolean; cancelled?: boolean; plugins?: PluginResult[];
  planId: string; createdAt: number; expiresAt: number; catalogVersion: number;
  candidates: CleanupLocation[]; partial: boolean; warnings: string[]; mode: "offline" | "jev" | "clef" | "preview"; message: string;
}
export interface PluginResult { id:string; name:string; status:string; durationMs?:number; errors?:string[] }
export interface DiscoveryProgress { running:boolean; phase?:string; total:number; completed:number; active:string[]; plugins:PluginResult[]; candidates:CleanupLocation[]; elapsedSeconds?:number; cancelled?:boolean; catalogVersion?:number }
export interface AgentSettings { mode: "decision" | "platform" | "free" | "subscription" | "api"; model: string }
export interface AgentStatus { available: boolean; creditBalancesVerified: boolean; providers: { id: string; name: string; authentication: "decision" | "platform" | "subscription" | "api"; defaultModel: string; models: { id: string; name: string; mode: AgentSettings["mode"]; configured?: boolean; cleanupCompatible: boolean; status?: string; cost?: { input: number; output: number } }[] }[] }
export interface CleanupExecutionProgress { running: boolean; phase: string; total: number; completed: number }
export interface CleanupResult { message: string; recoveredBytes: number; runId?: string; completedAt?: number; pendingPlan?: CleanupPlan; followupPlan?: CleanupPlan; ai?: { requestCount: number; requestKind?: "sdk-prompts" | "provider-requests"; batchCount: number; completedBatches?: number; inputTokens?: number; outputTokens?: number; models?: string[]; failures?: string[] }; results: { id: string; path: string; ok: boolean; detail: string; method?: string; status?: "cleaned" | "covered" | "approval" | "manual" | "retry" | "preserved" | "blocked" }[] }
export const bundledCatalog = catalog;
export const impactLabels = ["", "Low impact", "Re-download / rebuild", "Significant disruption", "Possible data loss", "Protected / unsupported"];
export const profileNames: Record<Profile, string> = { everyday: "General users", developer: "Developers", builder: "Builders", creator: "Creators" };
export { selectionSummary } from "./cleanup-selection";
export function previewPlan(profiles: Profile[]): CleanupPlan {
  const now = Date.now() / 1000;
  const examples = ["npm", "uv", "node-gyp", "installers", "chrome-cache", "editor-cache", "next-cache", "adobe-media", "dependencies", "device-backups"];
  return { planId: "preview", createdAt: now, expiresAt: now + 1800, catalogVersion: catalog.version, partial: false,
    warnings: ["Fictional example locations and sizes. No files scanned, no Jev request made."], mode: "preview",
    message: "Example cleanup review. Choose locations to preview the selection flow; your Mac is never changed.",
    candidates: catalog.rules.filter(r => examples.includes(r.id) && (!profiles.length || r.profiles.some(p => profiles.includes(p as Profile)))).map((r, i) => ({
      ...r, profiles: r.profiles as Profile[], ruleId: r.id, id: `preview-${r.id}`, path: `/Users/example/${r.patterns[0].replace(/\*\*/g, "website").replace(/\*/g, "example")}`,
      bytes: (i + 1) * 240_000_000, files: 50 + i * 10, complete: true, kind: r.kind as CleanupLocation["kind"],
      executable: r.kind !== "review", reason: r.kind === "review" ? "Owning-app or project-specific inspection required." : "",
      evidence: "Example catalog match", judgment: null,
    })) };
}
