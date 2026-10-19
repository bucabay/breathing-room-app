import { invoke, isTauri } from "@tauri-apps/api/core";
import { demoApps, demoReport, demoState } from "./demo";
import type { AppGroup, Capabilities, LargeFile, Process, SavedState, Settings, StorageReport } from "./model";
import type { Profile } from "./model";
import { bundledCatalog, previewPlan, type CleanupPlan, type CleanupResult, type DiscoveryProgress } from "./cleanup";
import { demoLive, demoLog, type LiveStatus, type ActivityLog, type MonitorConfig } from "./live";
import type { AgentCleanupConnection, AgentCleanupRun, DiscoveryPolicy, InventoryPage, DailyApproval, DailyNotification } from "./agent-cleanup";
import { metricsCache } from "./metrics-cache";
import { stripeCheckoutUrl, type AiCareBillingStatus } from "./ai-care";
import billingConfig from "../billing-config.json";
import type { AssistantMessage, AssistantReply } from "./assistant";
export const native = isTauri();
const wait = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));
let previewDiscoveryCancelled = false;
let previewAgentRun: AgentCleanupRun | null = null;
export const api = {
  async openTrash():Promise<void>{if(native)await invoke("open_trash");},
  async assistantMessage(message:string,history:AssistantMessage[],automatic=false,limits?:DiscoveryPolicy):Promise<AssistantReply>{
    if(native)return invoke("assistant_message",{message,history,automatic,limits});
    await wait(250);
    return {answer:"This is an interactive preview, so I haven't inspected your Mac or fetched live information. In the desktop app, ask a general question, inspect memory or CPU, or ask me to investigate disk space. For live weather, include your city.",features:["Discover disk usage and recent space consumers","Inspect memory, CPU and recorded activity","Review large personal and app files without deleting them","Research the web and current weather","Clean native-verified locations with your approval"],sources:[]};
  },
  async openAiCareCheckout(value: string): Promise<void> {
    const url = stripeCheckoutUrl(value);
    if (!url) throw new Error("AI care checkout is not configured.");
    if (native) await invoke("open_ai_care_checkout", {url});
    else {
      const plan=url===billingConfig.stripeSubscriptionUrl?"monthly":url===billingConfig.stripeAnnualUrl?"annual":null;
      if(!plan)throw new Error("Choose a configured AI care plan.");
      window.open(`https://breathing-room-api.worker-sendhub.workers.dev/billing/start?plan=${plan}`, "_blank", "noopener,noreferrer");
    }
  },
  async aiCareBillingStatus():Promise<AiCareBillingStatus>{return native?invoke("ai_care_billing_status"):{mode:"live",active:false};},
  async openAiCarePortal():Promise<void>{if(native)await invoke("open_ai_care_portal");else window.open("https://breathing-room-api.worker-sendhub.workers.dev/billing/start?plan=manage","_blank","noopener,noreferrer");},
  async agentCleanupConnection(): Promise<AgentCleanupConnection> {
    return native ? invoke("agent_cleanup_connection") : { available: true, reachable: true, authenticated: true, authConfigured: true, models: ["@cf/qwen/qwen3-30b-a3b-fp8"], defaultModel: "@cf/qwen/qwen3-30b-a3b-fp8", baseUrl: "https://example.workers.dev", message: "Interactive preview · no agent request or Mac changes" };
  },
  async agentAuthStart(provider: string): Promise<{id:string;expiresAt:number}> { return invoke("agent_auth_start", {provider}); },
  async agentAuthPoll(id: string): Promise<{status:string}> { return invoke("agent_auth_poll", {id}); },
  async agentAuthLogout(): Promise<void> { await invoke("agent_auth_logout"); },
  async agentApiConfigure(url: string): Promise<void> { if(native) await invoke("agent_api_configure", {url}); },
  async agentCleanupLatest(): Promise<AgentCleanupRun|null> { return native ? invoke("agent_cleanup_latest") : previewAgentRun ? structuredClone(previewAgentRun) : null; },
  async agentCleanupResume(id: string): Promise<void> { if(native) await invoke("agent_cleanup_resume", {id}); },
  async agentCleanupInspect(request: string, scope: string, model: string, automatic = false, limits?:DiscoveryPolicy,daily=false): Promise<string> {
    if (native) return invoke("agent_cleanup_inspect", { request, scope, model, automatic, limits,daily });
    await wait(400);
    previewAgentRun = { id: "preview-agent", status: "review", model, request, overview: "I found reproducible package caches and generated build files. Packages can download again; build files can be regenerated.", approvedIds: [], activity: ["Checked available disk space", "Measured cache locations", "Verified owning-app cleanup commands"], outcomes: [], recoveredBytes: 0, updatedAt: Date.now()/1000,
      actions: [
        { id: "npm", title: "npm download cache", kind: "command", reason: "Downloaded packages can be fetched again.", impact: "Future installs may download packages again.", paths: ["/Users/example/.npm/_cacache"], command: ["npm", "cache", "clean", "--force", "--cache", "/Users/example/.npm"], estimatedBytes: 1800000000 },
        { id: "uv", title: "Unused Python packages", kind: "command", reason: "The owning tool can prune unused downloads.", impact: "Some packages may need to download again.", paths: ["/Users/example/.cache/uv"], command: ["uv", "cache", "prune"], estimatedBytes: 900000000 },
        { id: "build", title: "Generated website build", kind: "trash", reason: "Generated build output can be recreated from the project.", impact: "Move to Trash; regenerate with a build.", paths: ["/Users/example/code/website/.next"], command: [], estimatedBytes: 240000000 },
        { id: "ruff", title: "Ruff analysis cache", kind: "trash", mode:"automatic", nativeRule:"owned-tagged-ruff-cache-v1", reason:"Owned, tagged lint cache verified by the native app.",impact:"Regenerates on the next lint run. Trash must be emptied to reclaim space.",paths:["/Users/example/code/website/.ruff_cache"],command:[],estimatedBytes:2000000 },
      ] };
    previewAgentRun.discoveryOptions={dailyCare:daily};
    if (daily)previewAgentRun.overview="Daily care used the same agent inspection. These new example locations need your approval; no cleanup was performed.";
    if (scope) previewAgentRun.overview += ` Requested focus: ${scope}.`;
    previewAgentRun.discovery={candidates:structuredClone(previewAgentRun.actions),manual:[],coverage:["Preview inventory only; no actual disk was inspected."],errors:[],snapshotHash:"preview",inventory:{scanId:"preview-agent",filesInspected:7400,directoriesInspected:520,measuredBytes:18e9,logicalBytes:19e9,partial:true,pendingDirectories:12,inaccessible:2,excluded:4,categories:[{name:"downloads",bytes:8e9,files:100},{name:"media",bytes:7e9,files:60},{name:"caches",bytes:3e9,files:7240}],largest:[{path:"/Users/example/Downloads/old-installer.dmg",kind:"file",category:"downloads",bytes:2e9,logicalBytes:2e9,modifiedAt:1,owned:true,state:"complete",reviewOnly:true}],scannedAt:Date.now()/1000}};
    previewAgentRun.discovery.reviewLocations=[
      {path:"/Users/example/Movies/Launch/Session.screenstudio",title:"Screen recording project",bytes:3.2e9,logicalBytes:3.2e9,modifiedAt:1,fileCount:42,partial:false,severity:"critical",recoverability:"not-rebuildable",warning:"Original source footage and edits cannot be rebuilt by Breathing Room. Verify a separate usable backup before removal in the owning app.",reviewOnly:true,cleanupEligible:false,requiresSelection:true},
      {path:"/Users/example/Documents/Film.fcpbundle",title:"Video editing library",bytes:2.4e9,logicalBytes:2.4e9,modifiedAt:1,fileCount:150,partial:false,severity:"critical",recoverability:"not-rebuildable",warning:"This library may contain unique source clips and editable timelines. An exported video does not preserve the full project.",reviewOnly:true,cleanupEligible:false,requiresSelection:true},
      {path:"/Users/example/Library/Application Support/ExampleEditor/projects",title:"Local application data",bytes:780e6,logicalBytes:780e6,modifiedAt:1,fileCount:680,partial:true,severity:"warning",recoverability:"unknown",warning:"Rebuildability and backup status are unverified. Review this location in its owning app; it is not an approved cleanup method.",reviewOnly:true,cleanupEligible:false,requiresSelection:true},
    ];
    return previewAgentRun.id;
  },
  async agentCleanupInventory(id:string,offset=0,category?:string):Promise<InventoryPage>{if(native)return invoke("agent_cleanup_inventory",{id,offset,category});const entries=(previewAgentRun?.discovery?.inventory?.largest||[]).filter(item=>!category||item.category===category);return {entries:entries.slice(offset,offset+50),offset,nextOffset:null,totalEntries:entries.length,note:"Example inventory; no Mac files were inspected."};},
  async agentCleanupState(id: string): Promise<AgentCleanupRun> {
    if (native) return invoke("agent_cleanup_state", { id });
    if (!previewAgentRun || previewAgentRun.id !== id) throw new Error("No preview session");
    return structuredClone(previewAgentRun);
  },
  async agentCleanupApprove(id: string, ids: string[]): Promise<void> {
    if (native) return invoke("agent_cleanup_approve", { id, ids });
    if (!previewAgentRun || previewAgentRun.id !== id || !ids.length) throw new Error("Choose actions from the review plan");
    if(ids.some(id=>previewAgentRun!.outcomes.some(outcome=>outcome.id===id)||!previewAgentRun!.actions.some(action=>action.id===id)))throw new Error("Choose unattempted actions");
    await wait(400); previewAgentRun.approvedIds.push(...ids); previewAgentRun.status = "done";
    previewAgentRun.outcomes.push(...ids.map(id => {const action=previewAgentRun!.actions.find(action=>action.id===id)!;const percent=id==="uv"?60:100;const removed=action.estimatedBytes*percent/100;return { id, ok: true, status:"success" as const, detail: "Example result only. No files were changed.",beforeBytes:action.estimatedBytes,afterBytes:action.estimatedBytes-removed,removedBytes:removed,percentCleaned:percent,pendingTrashBytes:action.kind==="trash"?removed:0 };}));
    const before=previewAgentRun.outcomes.reduce((sum,item)=>sum+(item.beforeBytes||0),0),removed=previewAgentRun.outcomes.reduce((sum,item)=>sum+(item.removedBytes||0),0),trash=previewAgentRun.outcomes.reduce((sum,item)=>sum+(item.pendingTrashBytes||0),0);
    previewAgentRun.results={schemaVersion:2,success:previewAgentRun.outcomes.length,failed:0,skipped:0,beforeBytes:before,removedBytes:removed,percentCleaned:before?removed/before*100:null,pendingTrashBytes:trash,availableSpaceChange:null,items:structuredClone(previewAgentRun.outcomes)};
  },
  async agentCleanupCancel(id: string): Promise<void> { if (native) await invoke("agent_cleanup_cancel", { id }); else if (previewAgentRun) previewAgentRun.status = "cancelled"; },
  async cleanupProgress():Promise<DiscoveryProgress|null>{return native?invoke("cleanup_progress"):null;},
  async cleanupFindings():Promise<CleanupPlan|null>{
    if(native)return invoke("cleanup_findings");
    const plan=previewPlan([]);plan.cached=true;plan.candidates=plan.candidates.map(c=>({...c,executable:false}));return plan;
  },
  async cleanupStop():Promise<void>{if(native)await invoke("cleanup_stop");else previewDiscoveryCancelled=true;},
  async live(): Promise<LiveStatus> {
    let snapshot:LiveStatus;
    if(native)snapshot=await invoke("live_status");
    else{
      const demo=demoLive();const groups=structuredClone(demoApps).map(group=>({...group,cpuAvailable:demo.config?.enabled??true}));
      snapshot={...demo,appGroups:groups,coreCount:8,appCount:groups.length,processCount:groups.reduce((total,group)=>total+group.processes.length,0),cpuPercent:demo.config?.enabled?groups.reduce((total,group)=>total+group.cpu,0)/8:null,topCpuApps:demo.config?.enabled?[...groups].sort((a,b)=>b.cpu-a.cpu).slice(0,5).map(group=>({name:group.name,path:group.bundlePath||group.id,cpu:group.cpu})):[]};
    }
    return metricsCache.updateLive(snapshot);
  },
  async activityLog(filter: string, search: string, before = 0): Promise<ActivityLog> {
    if (native) return invoke("activity_log", { filter, search, before });
    const log = demoLog();
    log.events=log.events.filter(e=>(!before||e.id<before)&&(!search||`${e.path} ${e.owner} ${e.workflow}`.toLowerCase().includes(search.toLowerCase())) && (filter==="all" || (filter==="processes" ? e.kind.startsWith("process")||e.kind==="app_started" : !e.kind.startsWith("process")&&e.kind!=="app_started")));
    return log;
  },
  async configureMonitor(config: MonitorConfig): Promise<void> {
    if (native) return invoke("configure_monitor", { config });
    localStorage.setItem("breathing-room-monitor-preview", JSON.stringify(config));
  },
  async activity(): Promise<{ title: string; detail: string; page: "space" | "assistant" | "daily"; startedAt: number; cancellable?:boolean; blocksAgent?:boolean } | null> {
    return native ? invoke("get_activity") : null;
  },
  async browseStorage(path: string): Promise<{ path: string; entries: { path: string; name: string; directory: boolean; symlink: boolean; bytes: number; logicalBytes: number }[]; partial: boolean }> {
    return native ? invoke("browse_storage", { path }) : { path, partial: false, entries: [{ path: `${path}/example.zip`, name: "example.zip", directory: false, symlink: false, bytes: 240000000, logicalBytes: 240000000 }] };
  },
  async cachedVolume(): Promise<StorageReport | null> {
    if (native) { const report=await invoke<StorageReport|null>("cached_volume");if(report)metricsCache.seedDisk(report);return report; }
    try {
      const cached = JSON.parse(localStorage.getItem("breathing-room-disk-map-preview") || "null");
      return cached?.version === 1 && Array.isArray(cached.report?.directories) && Array.isArray(cached.report?.groups) && cached.report.scannedAt > 0 ? cached.report : null;
    } catch { return null; }
  },
  async scanVolume(): Promise<StorageReport> {
    if (native) { const report=await invoke<StorageReport>("scan_volume");metricsCache.seedDisk(report);await this.live().catch(()=>{});return report; }
    await wait(800);
    const report = structuredClone(demoReport);
    report.scannedAt = Math.floor(Date.now() / 1000);
    const used = report.totalBytes - report.availableBytes;
    report.usedBytes = used; report.identifiedBytes = report.scannedBytes;
    report.unmappedBytes = Math.max(0, used - report.scannedBytes);
    report.coveragePercent = report.scannedBytes / used * 100;
    report.directories = report.groups.map(g => ({ path: `/Users/example/${g.id}`, name: g.name, parent: "/", bytes: g.bytes, partial: false }));
    try { localStorage.setItem("breathing-room-disk-map-preview", JSON.stringify({ version: 1, report })); } catch { /* Preview storage can be unavailable. */ }
    return report;
  },
  async cleanupDiscover(prompt: string, scope: string, profiles: Profile[], jev: boolean): Promise<CleanupPlan> {
    if (native) return invoke("cleanup_discover", { prompt, scope, profiles, jev });
    previewDiscoveryCancelled=false;
    await wait(500);
    if(previewDiscoveryCancelled){const plan=previewPlan(profiles);plan.cancelled=true;plan.candidates=plan.candidates.map(c=>({...c,executable:false}));plan.message="Preview discovery stopped. No files changed.";return plan;}
    if (jev) {
      const plan = await this.cleanupAssess("preview", prompt);
      if(previewDiscoveryCancelled){plan.cancelled=true;plan.candidates=plan.candidates.map(c=>({...c,executable:false}));plan.message="Preview discovery stopped. No files changed.";}
      if (profiles.length) plan.candidates = plan.candidates.filter(c => c.profiles.some(p => profiles.includes(p)));
      if (scope) {
        plan.candidates = [{ ...plan.candidates[0], path: scope, name: scope.split("/").pop() || scope }];
      }
      return plan;
    }
    return previewPlan(profiles);
  },
  async cleanupAssess(planId: string, prompt: string): Promise<CleanupPlan> {
    if (native) return invoke("cleanup_assess", { planId, prompt });
    await wait(400); const plan = previewPlan([]);
    plan.message = "Illustrative JEV AI badges only. Browser preview makes no AI request.";
    plan.candidates = plan.candidates.map(c => ({ ...c, judgment: { purpose: c.kind === "review" ? "unknown" : "cache", confidence: .9, relevance: .95,
      disposable: c.kind === "review" ? .4 : .94, uniqueData: c.kind === "review" ? .6 : .03, methodSupported: c.kind === "review" ? .2 : .96, impact: c.impactLevel, model: "Illustrative preview" } }));
    return plan;
  },
  async cleanupExecute(planId: string, ids: string[], agent?: import("./cleanup").AgentSettings): Promise<CleanupResult> {
    if (native) return invoke("cleanup_execute", { planId, ids, agentMode: agent?.mode, agentModel: agent?.model });
    return { message: "Preview complete. No files were removed and no cache was cleaned.", recoveredBytes: 0,
      results: ids.map(id => ({ id, path: "Example location", ok: true, detail: "Preview only — no mutation." })) };
  },
  async cleanupApprove(planId: string, id: string): Promise<CleanupPlan> {
    return invoke("cleanup_approve", { planId, id });
  },
  async cleanupAgentStatus(): Promise<import("./cleanup").AgentStatus> {
    return native ? invoke("cleanup_agent_status") : { available: false, creditBalancesVerified: false, providers: [] };
  },
  async cleanupLastResult(): Promise<CleanupResult | null> { return native ? invoke("cleanup_last_result") : null; },
  async cleanupExecutionProgress(): Promise<import("./cleanup").CleanupExecutionProgress | null> { return native ? invoke("cleanup_execution_progress") : null; },
  async cleanupCatalog(): Promise<typeof bundledCatalog> { return native ? invoke("cleanup_catalog") : bundledCatalog; },
  async cleanupUpdate(url: string): Promise<{ message: string; version: number; rules: number }> {
    if (!native) throw new Error("Remote catalog updates are available in the development desktop app. Preview never fetches a catalog.");
    return invoke("cleanup_update_catalog", { url });
  },
  async capabilities(): Promise<Capabilities> { return native ? invoke("get_capabilities") : { sandboxed: false, cacheCommands: true, cloudAi: false }; },
  async state(): Promise<SavedState> {
    if (native) return invoke("get_state");
    try {
      const state = JSON.parse(localStorage.getItem("breathing-room-demo") ?? "null") ?? structuredClone(demoState);
      state.settings.keepInMenuBar ??= true; return state;
    }
    catch { return structuredClone(demoState); }
  },
  async scan(): Promise<StorageReport> {
    if (native) return invoke("scan_storage");
    await wait(700); return structuredClone(demoReport);
  },
  async apps(): Promise<AppGroup[]> {
    if(native){
      const groups=await invoke<AppGroup[]>("list_apps");
      const snapshot=await invoke<LiveStatus>("live_status");
      const cached=metricsCache.updateLive({...snapshot,appGroups:snapshot.appGroups??groups});
      return cached.appGroups??groups;
    }
    const snapshot=await this.live();return snapshot.appGroups??[];
  },
  async settings(settings: Settings) {
    if (native) return invoke<void>("save_settings", { settings });
    const state = await this.state(); state.settings = settings; localStorage.setItem("breathing-room-demo", JSON.stringify(state));
  },
  async cancel() { if (native) await invoke("cancel_scan"); },
  async chooseFolder(): Promise<string | null> { return native ? invoke("choose_folder") : null; },
  async trash(file: LargeFile): Promise<string> { return native ? invoke("trash_file", { file }) : "Preview only. No file was moved to Trash."; },
  async clean(id: string): Promise<string> {
    if (!native) return "Preview only. No files were changed. Open the desktop app to clean a cache.";
    return invoke("clean_cache", { id });
  },
  async end(process: Process, force: boolean): Promise<string> {
    if (!native) return "Preview only. No process was stopped.";
    return invoke("end_process", { process, force });
  },
  async endGroup(group: AppGroup, force: boolean): Promise<string> {
    if (!native) return "Preview only. No process was stopped.";
    return invoke("end_group", { id: group.id, members: group.processes, force });
  },
  async quit(group: AppGroup): Promise<string> {
    if (!native) return "Preview only. No app was closed.";
    return invoke("quit_app", { id: group.id });
  },
  async dailyApprovals():Promise<DailyApproval[]>{return native?invoke("daily_approvals"):[];},
  async revokeDailyApproval(key:string):Promise<void>{if(native)await invoke("revoke_daily_approval",{key});},
  async dailyNotifications():Promise<DailyNotification[]>{return native?invoke("daily_notifications"):[];},
  async markDailyNotificationSeen(id:string):Promise<void>{if(native)await invoke("mark_daily_notification_seen",{id});},
  async reveal(path: string): Promise<void> { if (native) await invoke("reveal_path", { path }); },
  async icon(id: string): Promise<string | null> { if (!native) return null; try { return await invoke("app_icon", { id }); } catch { return null; } },
};
