import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { Activity, ArrowUpRight, Bot, Check, ChevronDown, ChevronRight, CircleHelp, Clock3, Code2, FolderOpen,
  HardDrive, House, Image, Leaf, LoaderCircle, Moon, Play, RefreshCw, Search, Settings2,
  ShieldCheck, Sparkles, Square, Sun, Wind, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogDescription, DialogTitle } from "@/components/ui/dialog";
import { StorageRing, UsageBar } from "@/components/charts";
import { AppIcon } from "@/components/app-icon";
import { CleanupAssistant } from "@/components/cleanup-assistant";
import { TrashCleanupNotice } from "@/components/trash-cleanup-notice";
import { ApprovedLocationsPreview,ApprovedLocationsScreen } from "@/components/approved-locations";
import { AiCareCard } from "@/components/ai-care-card";
import { trashCompletion } from "@/lib/cleanup-results";
import { SpaceView } from "@/components/space-view";
import type { SpaceTab } from "@/lib/space-view";
import { LiveStatusBar } from "@/components/live-status";
import { ActivityPage } from "@/components/activity-page";
import { AppUpdates } from "@/components/app-updates";
import { api, native } from "@/lib/api";
import { buckets, defaultSettings, formatBytes, profileFocus,
   type Capabilities, type CareEvent, type Page, type Profile, type Settings,
  type StorageReport } from "@/lib/model";
import { useTheme } from "@/hooks/use-theme";
import { listen } from "@tauri-apps/api/event";
import { panelNavigationFromUrl, type PanelNavigation } from "@/lib/panel-navigation";
import { scrollPanelDestination } from "@/lib/panel-scroll";
import { agentOperationBlocked, blocksAgent } from "@/lib/maintenance";
import { useMetrics } from "@/hooks/use-metrics";
import { withCurrentDisk } from "@/lib/metrics-cache";
import { memoryUsage } from "@/lib/memory";
import type { DailyApproval,DailyNotification } from "@/lib/agent-cleanup";
import billingConfig from "@/billing-config.json";
import { stripeCheckoutUrl } from "@/lib/ai-care";

const aiCareCheckoutUrl = stripeCheckoutUrl(billingConfig.stripeSubscriptionUrl);
const aiCareAnnualUrl = stripeCheckoutUrl(billingConfig.stripeAnnualUrl);

const profiles: { id: Profile; name: string; description: string; icon: typeof House }[] = [
  { id: "everyday", name: "Everyday", description: "Downloads, media, and everyday apps", icon: House },
  { id: "developer", name: "Developer", description: "Projects, dependencies, and build tools", icon: Code2 },
  { id: "builder", name: "Builder", description: "Agent sessions, editors, and local tools", icon: Sparkles },
  { id: "creator", name: "Creator", description: "Photos, video, and creative work", icon: Image },
];
const nav: { id: Page; title: string; icon: typeof House }[] = [
  { id: "home", title: "Home", icon: House }, { id: "space", title: "Space", icon: HardDrive },
  { id: "apps", title: "Apps", icon: Square }, { id: "daily", title: "Daily care", icon: Leaf },
  { id: "assistant", title: "AI Assistant", icon: Bot },
  { id: "activity", title: "Activity", icon: Activity },
];
type Confirmation = { title: string; detail: string; action: string; destructive?: boolean; run: () => Promise<string> };

function App() {
  const [panelDestination,setPanelDestination]=useState(()=>panelNavigationFromUrl(window.location.search));
  const [panelRequest,setPanelRequest]=useState(0);
  const [page, setPage] = useState<Page>(panelDestination?.page??"home");
  const [cleanupRequest, setCleanupRequest] = useState(0);
  const [cleanupScope, setCleanupScope] = useState("");
  const [cleanupDaily,setCleanupDaily]=useState(false);
  const [requestedRunId,setRequestedRunId]=useState("");
  const [runReviewRequest,setRunReviewRequest]=useState(0);
  const [dailyApprovals,setDailyApprovals]=useState<DailyApproval[]>([]);
  const [approvalsOpen,setApprovalsOpen]=useState(false);
  useEffect(()=>{if(page!=="daily")setApprovalsOpen(false);},[page]);
  const [dailyNotifications,setDailyNotifications]=useState<DailyNotification[]>([]);
  const [nativeActivity, setNativeActivity] = useState<Awaited<ReturnType<typeof api.activity>>>(null);
  const [assistantBusy, setAssistantBusy] = useState("");
  const [assistantFocused, setAssistantFocused] = useState(false);
  const cleanupFocused = page === "assistant" && assistantFocused;
  const [clock, setClock] = useState(Date.now());
  const liveStatus = useMetrics();
  const memory = memoryUsage(liveStatus);
  const [metricsCollapsed, setMetricsCollapsed] = useState(false);
  const [collapsedOperation, setCollapsedOperation] = useState<string | null>(null);
  const reviewWithAi = (scope = "") => { setCleanupDaily(false);setRequestedRunId("");setCleanupScope(scope); setPage("assistant"); if (!agentBlocked && !assistantBusy) setCleanupRequest(n => n + 1); };
  const [volumeBusy, setVolumeBusy] = useState(false);
  const volumeRequested = useRef(false);
  const [overviewReport, setReport] = useState<StorageReport | null>(null);
  const [volumeReport, setVolumeReport] = useState<StorageReport | null>(null);
  const [volumeCacheReady, setVolumeCacheReady] = useState(false);
  const report = useMemo(()=>withCurrentDisk(page === "space" ? volumeReport ?? overviewReport : overviewReport ?? volumeReport,liveStatus),[page,volumeReport,overviewReport,liveStatus]);
  const apps = liveStatus?.appGroups ?? [];
  const [settings, setSettings] = useState<Settings>(structuredClone(defaultSettings));
  const [savedSettings, setSavedSettings] = useState<Settings>(structuredClone(defaultSettings));
  const [history, setHistory] = useState<CareEvent[]>([]);
  const [capabilities, setCapabilities] = useState<Capabilities>({ sandboxed: false, cacheCommands: !native, cloudAi: false });
  const [scanBusy, setScanBusy] = useState(false);
  const [actionBusy, setActionBusy] = useState(false);
  const [appsBusy, setAppsBusy] = useState(false);
  const [search, setSearch] = useState(panelDestination?.page==="apps"?panelDestination.search??"":"");
  const [sort, setSort] = useState<"memory" | "cpu">(panelDestination?.page==="apps"?"cpu":"memory");
  const [expanded, setExpanded] = useState<string | null>(panelDestination?.appId??null);
  const [view, setView] = useState<SpaceTab>("category");
  const [selectedBucket, setSelectedBucket] = useState<string | null>(null);
  const [profileOpen, setProfileOpen] = useState(false);
  const [aiOpen, setAiOpen] = useState(false);
  const [aiCareActive,setAiCareActive]=useState<boolean|null>(null);
  useEffect(()=>{
    if(!aiOpen||!native)return;
    let stopped=false,busy=false;setAiCareActive(null);
    const check=async()=>{if(busy)return;busy=true;try{const status=await api.aiCareBillingStatus();if(!stopped)setAiCareActive(status.mode==="live"&&status.active);}catch{if(!stopped)setAiCareActive(null);}finally{busy=false;}};
    void check();const timer=setInterval(()=>void check(),10000);
    return()=>{stopped=true;clearInterval(timer);};
  },[aiOpen]);
  const [confirmation, setConfirmation] = useState<Confirmation | null>(null);
  const [toast, setToast] = useState<{ message: string; error: boolean } | null>(null);
  const [trashNotice,setTrashNotice]=useState<{key:string;bytes:number|null}|null>(null);
  const toastTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const appRefresh = useRef(false);
  const scanInFlight = useRef(false);
  const { theme, toggleTheme } = useTheme();
  const notify = useCallback((message: string, error = false) => {
    if (toastTimer.current) clearTimeout(toastTimer.current);
    setToast({ message, error }); toastTimer.current = setTimeout(() => setToast(null), 8000);
  }, []);
  const loadState = useCallback(async () => {
    const state = await api.state(); setHistory(state.history); return state;
  }, []);
  const refreshDaily=useCallback(()=>{void api.dailyNotifications().then(setDailyNotifications).catch(()=>{});void api.dailyApprovals().then(setDailyApprovals).catch(()=>{});},[]);
  useEffect(()=>{refreshDaily();const timer=setInterval(refreshDaily,5000);return()=>clearInterval(timer);},[refreshDaily]);
  const reviewDaily=useCallback((id:string)=>{if(assistantBusy){notify("Your agent is still running. Review these findings after it finishes.");return;}setRequestedRunId(id);setRunReviewRequest(n=>n+1);setPage("assistant");void api.markDailyNotificationSeen(id).then(refreshDaily).catch(error=>notify(String(error),true));},[assistantBusy,refreshDaily,notify]);
  useEffect(()=>{if(!native)return;const listener=listen<DailyNotification>("daily-care-updated",()=>refreshDaily());return()=>{void listener.then(unlisten=>unlisten());};},[refreshDaily]);
  useEffect(()=>{if(!native)return;const listener=listen<string>("daily-care-review",event=>{if(event.payload)reviewDaily(event.payload);else setPage("daily");});return()=>{void listener.then(unlisten=>unlisten());};},[reviewDaily]);
  const refreshApps = useCallback(async () => {
    if (appRefresh.current) return;
    appRefresh.current = true; setAppsBusy(true);
    try { await api.apps(); } catch (e) { notify(String(e), true); }
    finally { appRefresh.current = false; setAppsBusy(false); }
  }, [notify]);
  const scan = useCallback(async () => {
    if (scanInFlight.current) return;
    scanInFlight.current = true;
    setScanBusy(true);
    try { setReport(await api.scan()); } catch (e) { notify(String(e), true); }
    finally { scanInFlight.current = false; setScanBusy(false); }
  }, [notify]);
  const refreshLive = useCallback(() => {
    void api.live().catch(() => {});
  }, []);
  useEffect(()=>{
    if(!native)return;
    const listener=listen<PanelNavigation>("navigate-main",event=>{
      const destination=event.payload;
      setPanelDestination(destination);setPanelRequest(n=>n+1);
      setPage(destination.page);setSelectedBucket(null);refreshLive();
      if(destination.page==="apps") {setSearch(destination.search??"");setSort("cpu");setExpanded(destination.appId??null);void refreshApps();}
    });
    return()=>{void listener.then(unlisten=>unlisten());};
  },[refreshLive,refreshApps]);
  useEffect(()=>{
    if(!panelDestination || page!==panelDestination.page || page==="activity")return;
    return scrollPanelDestination(page==="apps"&&panelDestination.appId?()=>document.getElementById(`app-group-${panelDestination.appId}`):undefined);
  },[page,panelDestination,panelRequest,apps.some(app=>app.id===panelDestination?.appId)]);
  useEffect(() => {
    refreshLive();
    const timer = setInterval(refreshLive, 3000);
    return () => clearInterval(timer);
  }, [refreshLive]);
  useEffect(() => {
    let live = true;
    const refresh = () => {
      setClock(Date.now());
      void api.activity().then(activity => { if (live) setNativeActivity(activity); }).catch(() => {});
    };
    refresh();
    const timer = setInterval(refresh, 1000);
    return () => { live = false; clearInterval(timer); };
  }, []);
  const maintenanceActivity = nativeActivity ?? (volumeBusy ? {
    title: volumeReport ? "Refreshing disk map" : "Mapping your whole disk", detail: volumeReport ? "Updating saved storage results in the background" : "df, du and APFS accounting · may take up to three minutes", page: "space" as Page, startedAt: 0, blocksAgent: false,
  } : scanBusy ? { title: "Checking storage", detail: "Reading accessible folders and file sizes", page: "space" as Page, startedAt: 0 }
    : assistantBusy ? { title: assistantBusy, detail: "Your cleanup assistant is working", page: "assistant" as Page, startedAt: 0 }
      : actionBusy ? { title: "Applying your selected action", detail: "Please wait for this action to complete", page, startedAt: 0 } : null);
  const agentBlocked = agentOperationBlocked(nativeActivity, scanBusy, actionBusy);
  const dailyNotice=dailyNotifications.find(n=>!n.seen&&(n.pendingCount>0||n.needsAttention));
  const operationKey = maintenanceActivity ? `${maintenanceActivity.page}:${maintenanceActivity.title}:${maintenanceActivity.startedAt}` : null;
  const operationCollapsed = (operationKey !== null && collapsedOperation === operationKey) || (page === "assistant" && maintenanceActivity?.page === "assistant") || maintenanceActivity?.title === "Refreshing disk map";
  useEffect(() => { if (!operationKey) setCollapsedOperation(null); }, [operationKey]);
  const scanVolume = useCallback(async () => {
    if (scanInFlight.current) return;
    volumeRequested.current = true;
    scanInFlight.current = true; setVolumeBusy(true);
    try {
      const cached = await api.cachedVolume().catch(() => null);
      if (cached) setVolumeReport(current => current && current.scannedAt >= cached.scannedAt ? current : cached);
      setVolumeReport(await api.scanVolume());
    }
    catch (e) { notify(String(e), true); }
    finally { scanInFlight.current = false; setVolumeBusy(false); }
  }, [notify]);
  useEffect(() => {
    if (page === "space" && volumeCacheReady && !scanBusy && !volumeBusy && !nativeActivity && !volumeRequested.current) {
      void scanVolume();
    }
  }, [page, volumeCacheReady, scanBusy, volumeBusy, scanVolume, nativeActivity]);
  useEffect(() => {
    let live = true;
    void api.cachedVolume().then(cached => {
      if (live && cached) setVolumeReport(current => current && current.scannedAt >= cached.scannedAt ? current : cached);
    }).catch(() => {}).finally(() => { if (live) setVolumeCacheReady(true); });
    return () => { live = false; };
  }, []);
  useEffect(() => {
    let live = true;
    api.state().then((state) => {
      if (live) { setSettings(state.settings); setSavedSettings(state.settings); setHistory(state.history); }
    }).catch((e) => notify(String(e), true));
    api.capabilities().then((caps) => { if (live) setCapabilities(caps); }).catch((e) => notify(String(e), true));
    void scan(); void refreshApps();
    return () => { live = false; if (toastTimer.current) clearTimeout(toastTimer.current); };
  }, [notify, scan, refreshApps]);
  useEffect(() => {
    const timer = setInterval(() => {
      if (document.visibilityState === "visible") { void refreshApps(); void loadState().catch(() => {}); }
    }, 15000);
    return () => clearInterval(timer);
  }, [refreshApps, loadState]);
  const categoryGroups = useMemo(() => buckets(report?.groups ?? [], "category"), [report]);
  const filteredApps = useMemo(() => apps.filter((app) => app.name.toLowerCase().includes(search.toLowerCase()))
    .sort((a, b) => sort === "cpu" ? b.cpu - a.cpu : b.memoryBytes - a.memoryBytes), [apps, search, sort]);
  const appMetricMaximums = useMemo(() => filteredApps.reduce((maximums, app) => app.metricsAvailable ? {
    memory: Math.max(maximums.memory, app.memoryBytes), cpu: Math.max(maximums.cpu, app.cpu),
  } : maximums, { memory: 1, cpu: 1 }), [filteredApps]);
  const largest = profileFocus(report?.groups ?? [], settings.profiles);
  const largestApp = [...apps].filter((a) => a.id !== "system" && a.metricsAvailable).sort((a, b) => b.memoryBytes - a.memoryBytes)[0];
  const metricsRestricted = apps.length > 0 && !apps.some((app) => app.metricsAvailable);
  const recovered = history.reduce((sum, e) => sum + e.recoveredBytes, 0);
  const dirty = JSON.stringify(settings) !== JSON.stringify(savedSettings);
  const save = async () => {
    setActionBusy(true);
    try { await api.settings(settings); setSavedSettings(structuredClone(settings)); notify(native ? "Preferences saved." : "Preview preferences saved in this browser."); }
    catch (e) { notify(String(e), true); } finally { setActionBusy(false); }
  };
  const execute = async () => {
    if (!confirmation) return;
    setActionBusy(true);
    try {
      const message = await confirmation.run(); setConfirmation(null); notify(message);
      await loadState(); await refreshApps();
      if (page === "space") await scan();
    } catch (e) { notify(String(e), true); } finally { setActionBusy(false); }
  };
  const runCare = () => {setCleanupDaily(true);setRequestedRunId("");setCleanupScope("");setPage("assistant");setCleanupRequest(n=>n+1);};
  const profileLabel = settings.profiles.length === 1 ? profiles.find((p) => p.id === settings.profiles[0])?.name : `${settings.profiles.length} profiles`;
  const chooseFolder = async () => {
    try {
      const path = await api.chooseFolder();
      if (path) setSettings((current) => ({ ...current, scanPaths: [...new Set([...current.scanPaths, path])] }));
      else if (!native) notify("The native folder picker is available in the desktop app.");
    } catch (e) { notify(String(e), true); }
  };

  return <div className={`app-shell ${cleanupFocused ? "cleanup-flow-shell" : ""}`}>
    {!cleanupFocused && <aside className="sidebar">
      <button className="wordmark" onClick={() => setPage("home")} aria-label="Breathing Room home"><span className="brand-symbol"><Wind size={27} /></span><span>breathing<br />room<span className="wordmark-dot">.</span></span></button>
      <span className="sidebar-caption">A little room. A better day.</span>
      <nav aria-label="Main navigation">{nav.map(({ id, title, icon: Icon }) => <button key={id} className={`nav-item ${page === id ? "active" : ""}`} aria-label={title} aria-current={page === id ? "page" : undefined} onClick={() => { setPage(id); setSelectedBucket(null); }}><Icon size={20} /><span>{title}</span>{id === "daily" && savedSettings.enabled && <span className="live-dot" />}</button>)}</nav>
      <div className="sidebar-bottom">
        <button className="profile-button" onClick={() => setProfileOpen(true)}><Settings2 size={19} /><span>{profileLabel}<small>Make it yours</small></span><ChevronRight size={16} /></button>
        <AiCareCard placement="sidebar" onOpen={()=>setAiOpen(true)}/>
        <div className="sidebar-footer"><span>Made for your Mac</span><button className="icon-button" aria-label={`Switch to ${theme === "light" ? "dark" : "light"} theme`} onClick={toggleTheme}>{theme === "light" ? <Moon size={18} /> : <Sun size={18} />}</button></div>
      </div>
    </aside>}
    <main className="main-content">
      {!cleanupFocused && <><header className="topbar"><span><span className={`status-dot ${native ? "" : "demo-dot"}`} />{native ? "Your Mac · live local data" : "Interactive preview · example data"}</span><button className="text-button" onClick={() => setAiOpen(true)}><Sparkles size={16} />AI care</button></header>
      {!native && <div className="preview-banner"><CircleHelp size={16} /><span>This browser preview uses example data. Actions never change your Mac.</span></div>}</>}
      {(!cleanupFocused||trashNotice) && <div className="status-dock">
        <div className="status-dock-row">
          {!cleanupFocused && maintenanceActivity && operationCollapsed && <button className="compact-operation" title={maintenanceActivity.detail} onClick={() => setCollapsedOperation(null)} aria-label={`Expand running operation: ${maintenanceActivity.title}`} aria-expanded={false} aria-controls="expanded-operation"><LoaderCircle className="spin" size={15}/><span role="status">{maintenanceActivity.title}</span><ChevronDown size={14}/></button>}
          {!cleanupFocused && (metricsCollapsed || page === "assistant") && <LiveStatusBar status={liveStatus} navigate={setPage} compact onExpand={() => setMetricsCollapsed(false)}/>}
        </div>
        {!cleanupFocused && !metricsCollapsed && page !== "assistant" && <div id="expanded-metrics" className="expanded-metrics"><LiveStatusBar status={liveStatus} navigate={setPage}/><button className="icon-button metrics-collapse" onClick={() => setMetricsCollapsed(true)} aria-label="Collapse metrics" aria-expanded={true} aria-controls="expanded-metrics"><X size={14}/><span className="metrics-collapse-tooltip" role="tooltip">Collapse metrics</span></button></div>}
        {!cleanupFocused && maintenanceActivity && !operationCollapsed && <div id="expanded-operation" className="global-maintenance" role="status" aria-live="polite"><span className="global-maintenance-icon"><LoaderCircle className="spin" size={23} /></span><div><strong>{maintenanceActivity.title}</strong><p>{maintenanceActivity.detail}</p><small>{blocksAgent(maintenanceActivity) ? "Other maintenance waits until this operation finishes" : "Your agent is available while the disk map updates"}{maintenanceActivity.startedAt ? ` · running for ${Math.max(0, Math.floor((clock / 1000 - maintenanceActivity.startedAt) / 60))}m ${Math.max(0, Math.floor(clock / 1000 - maintenanceActivity.startedAt) % 60)}s` : ""}</small></div>{nativeActivity?.cancellable&&<button className="text-button" onClick={()=>void api.cleanupStop().catch(e=>notify(String(e),true))}>Stop discovery <X size={15}/></button>}<button className="text-button" onClick={() => setPage(maintenanceActivity.page)}>View operation <ChevronRight size={16}/></button><button className="icon-button" title="Dismiss to status bar" aria-label="Dismiss operation notification to status bar" onClick={() => setCollapsedOperation(operationKey)}><X size={16}/></button></div>}
        {trashNotice&&<TrashCleanupNotice key={trashNotice.key} bytes={trashNotice.bytes} preview={!native} onOpen={()=>void api.openTrash().catch(error=>notify(String(error),true))} onDismiss={()=>setTrashNotice(null)}/>}
      </div>}
      {page === "home" && <>
          <div className="page-heading"><div><h1>Room to do your thing.</h1><p>Your space, your apps, a little less clutter.</p></div><Button className="big-button assistant-clean-button" onClick={() => reviewWithAi()} disabled={agentBlocked || !!assistantBusy || capabilities.sandboxed}><Sparkles />Clean up my Mac</Button></div>
        <section className="overview-grid" aria-label="Mac overview">
          <div className="space-panel panel"><div className="panel-heading"><h2>A little breathing room</h2><HardDrive size={20} /></div>
            {report ? <div className="space-visual"><StorageRing total={report.totalBytes} available={report.availableBytes} buckets={categoryGroups} /><div className="ring-legend">{categoryGroups.slice(0, 4).map((item) => <button key={item.id} onClick={() => { setView("category"); setPage("space"); setSelectedBucket(item.id); }}><i style={{ background: item.color }} /><span>{item.name}</span><strong>{formatBytes(item.bytes)}</strong></button>)}<span className="legend-note">{report.partial ? "Measured folders · partial coverage" : "Measured folders"}</span></div></div> : <div className="scan-placeholder"><LoaderCircle className="spin" size={35} /><p>Finding what takes up space…</p></div>}
            <Button className="big-button panel-action" onClick={() => setPage("space")}>Find more space <ArrowUpRight /></Button>
          </div>
          <div className="activity-panel panel"><div className="panel-heading"><h2>{metricsRestricted ? "Your running apps" : "Know your busy apps"}</h2><Square size={20} /></div><p className="panel-intro">{metricsRestricted ? "App names and icons are available. Detailed metrics are restricted in this build." : "Recognizable apps. Observed helpers, together."}</p>
            <div className="top-apps">{apps.filter((a) => a.id !== "system").slice(0, 3).map((app, i) => <button className="top-app" key={app.id} onClick={() => { setPage("apps"); setExpanded(app.id); }}><AppIcon app={app} /><div><div className="top-app-title"><strong>{app.name}</strong><span>{app.metricsAvailable ? formatBytes(app.memoryBytes) : "Not available"}</span></div>{app.metricsAvailable && <UsageBar value={app.memoryBytes} maximum={largestApp?.memoryBytes ?? 1} color={["#3b82f6", "#8b5cf6", "#16a085"][i]} />}<small>{app.metricsAvailable ? `${app.processes.length} processes grouped` : app.coverage}</small></div></button>)}</div>
            <p className="metric-note">Sampled memory totals may include shared memory. CPU peaks alone don’t mean an app is stuck.</p>
            <Button variant="secondary" className="big-button panel-action" onClick={() => setPage("apps")}>Manage my apps <ArrowUpRight /></Button>
          </div>
        </section>
        <section className="care-strip"><span className="care-symbol"><Leaf size={25} /></span><div><h3>A quiet daily check.</h3><p>{savedSettings.enabled ? `Daily, ${savedSettings.hour}:00–${(savedSettings.hour + savedSettings.windowHours) % 24}:00, while the app is running.` : "Choose a daily window. We’ll check when your Mac has a quiet moment."}</p></div><Button variant="outline" className="big-button" onClick={() => setPage("daily")}>{savedSettings.enabled ? "View daily care" : "Set up daily care"}<ChevronRight /></Button></section>
        <div className="section-heading"><h2>Worth a closer look</h2><span>Facts first. You stay in control.</span></div>
        <section className="finding-grid"><Finding icon={<FolderOpen />} color="violet" title={largest?.name ?? "Your storage"} detail={largest ? `${formatBytes(largest.bytes)} measured in a category relevant to your profiles. Explore before deciding what to remove.` : "Run a scan to see your largest storage groups."} action="Explore space" onClick={() => { setPage("space"); setView("category"); setSelectedBucket(largest?.id ?? null); }} />
          <Finding icon={<ShieldCheck />} color="mint" title="Clear the right things" detail="Your agent checks the disk and proposes safe cleanup. Review its plan before anything changes." action="Ask your agent" onClick={() => reviewWithAi()} />
          <AiCareCard onOpen={()=>setAiOpen(true)}/></section>
        {history.length > 0 && <History events={history.slice(0, 3)} recovered={recovered} />}
      </>}
      {page === "space" && <>
        <div className="page-heading"><div><h1>Find your breathing room.</h1><p>Your whole disk, from big folders to individual files.</p>{volumeReport && <p className="space-cache-status">{volumeBusy ? "Refreshing in background · " : ""}Last updated {new Date(volumeReport.scannedAt * 1000).toLocaleString(undefined, { month: "short", day: "numeric", hour: "numeric", minute: "2-digit" })}</p>}</div><div className="space-heading-actions"><Button variant="outline" className="big-button" disabled={actionBusy || volumeBusy || scanBusy} onClick={scanVolume}>{volumeBusy ? <LoaderCircle className="spin" /> : <RefreshCw />}{volumeBusy ? volumeReport ? "Refreshing…" : "Scanning…" : "Scan disk"}</Button><Button className="big-button" onClick={() => reviewWithAi()} disabled={capabilities.sandboxed}><Sparkles />Cleanup my Mac</Button></div></div>
        {volumeBusy && !volumeReport && <div className="cleanup-progress" role="status"><LoaderCircle className="spin" /><span>Mapping the Data volume with df and du… Large disks may take up to three minutes.</span></div>}
        {liveStatus?.totalBytes!=null&&liveStatus.availableBytes!=null&&<p className="metric-note">Current disk: {formatBytes(liveStatus.availableBytes)} free of {formatBytes(liveStatus.totalBytes)} · {Math.round((1-liveStatus.availableBytes/liveStatus.totalBytes)*100)}% used. Folder sizes below are from the saved disk map.</p>}
        <SpaceView report={report} profiles={settings.profiles} view={view} onViewChange={setView} selected={selectedBucket} onSelect={setSelectedBucket} onReview={reviewWithAi} />
      </>}
      {page === "apps" && <>
        <div className="page-heading"><div><h1>Your apps, together.</h1><p>One app. All its helpers. Easy to understand.</p></div><Button variant="outline" className="big-button" onClick={refreshApps} disabled={appsBusy}>{appsBusy ? <LoaderCircle className="spin" /> : <RefreshCw />}Refresh apps</Button></div>
        <div className="apps-toolbar"><label className="search-field"><Search size={20} /><input value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Find an app or background tool" aria-label="Search apps" /></label><div className="segmented"><button className={sort === "memory" ? "selected" : ""} aria-pressed={sort === "memory"} onClick={() => setSort("memory")}>Memory</button><button className={sort === "cpu" ? "selected" : ""} aria-pressed={sort === "cpu"} onClick={() => setSort("cpu")}>CPU</button></div></div>
        <p className="metric-note">System CPU: {liveStatus?.cpuPercent!=null?`${liveStatus.cpuPercent.toFixed(0)}%`:"Unavailable"} · normalized across all cores. App CPU below uses the same sample, with 100% representing one core.</p>
        <p className="metric-note">System RAM: {memory?`${formatBytes(memory.used)} of ${formatBytes(memory.total)} used (${memory.percent.toFixed(0)}%)`:"Unavailable"}. Physical-use estimate includes non-purgeable app memory, wired memory and compression; app RSS totals below can overlap.</p>
        <p className="metric-note">{metricsRestricted ? "This sandbox build shows available app metadata. Detailed resource metrics, hidden helpers, and individual process actions are unavailable." : "CPU is per-core and may exceed 100%. Memory is summed process RSS and can include shared pages. Unattributed tools remain separate."}</p>
        <div className="app-list">{filteredApps.map((app) => {
          const protectedGroup = app.processes.every((p) => p.protected);
          const quitUnavailable = app.bundlePath ? !app.canQuit : protectedGroup;
          return <div id={`app-group-${app.id}`} className="app-card panel" key={app.id}><div className="app-card-main"><AppIcon app={app} /><button className="app-card-title" aria-expanded={expanded === app.id} onClick={() => setExpanded(expanded === app.id ? null : app.id)}><strong>{app.name}</strong><span>{app.metricsAvailable ? `${app.processes.length} processes ${app.bundlePath ? "grouped by app" : "· background"}` : app.coverage}<ChevronDown size={14} /></span></button><div className="app-metrics">
            <div className={`app-usage ${sort === "memory" ? "sorted-metric" : ""}`}><small>Memory</small><strong>{app.metricsAvailable ? formatBytes(app.memoryBytes) : "Unavailable"}</strong>{app.metricsAvailable && <UsageBar value={app.memoryBytes} maximum={appMetricMaximums.memory} color="#3b82f6"/>}</div>
            <div className={`app-usage ${sort === "cpu" ? "sorted-metric" : ""}`}><small>CPU</small><strong>{app.metricsAvailable&&app.cpuAvailable!==false ? `${app.cpu.toFixed(1)}%` : "Unavailable"}</strong>{app.metricsAvailable&&app.cpuAvailable!==false && <UsageBar value={app.cpu} maximum={appMetricMaximums.cpu} color="#8b5cf6"/>}</div>
          </div><Button variant="outline" className="big-button quit-button" disabled={quitUnavailable || actionBusy} onClick={() => setConfirmation({ title: app.bundlePath ? `Quit ${app.name}?` : `End ${app.name}?`, detail: app.bundlePath ? "Ask the app to quit gracefully. It may ask you to save work. Its helpers usually exit with it." : "Send a termination signal to the selected background group. This is not a graceful application quit.", action: app.bundlePath ? "Quit app" : "End group", run: () => app.bundlePath ? api.quit(app) : api.endGroup(app, false) })}>{quitUnavailable ? "Protected" : app.bundlePath ? "Quit app" : "End group"}</Button></div>
            {expanded === app.id && <div className="process-details"><div className="process-header"><span>Inside {app.name}</span><button className="danger-link" disabled={protectedGroup || actionBusy} onClick={() => setConfirmation({ title: `Force quit ${app.name} group?`, detail: "Immediately stop the verified, eligible members in this group. Unsaved work may be lost. Protected, changed, or exited processes are skipped and reported.", action: "Force quit group", destructive: true, run: () => api.endGroup(app, true) })}>Force quit group</button></div>{app.processes.map((process) => <div className="process-row" key={process.pid}><span><strong>{process.name}</strong><small>PID {process.pid}</small></span><span>{app.metricsAvailable ? formatBytes(process.memoryBytes) : "Unavailable"}</span><span>{app.metricsAvailable&&app.cpuAvailable!==false&&process.cpuAvailable!==false ? `${process.cpu.toFixed(1)}% CPU` : "Unavailable"}</span><button disabled={process.protected || actionBusy} onClick={() => setConfirmation({ title: `End ${process.name}?`, detail: `Send a termination signal to PID ${process.pid}. Its identity will be checked again before acting. The app may restart this helper.`, action: "End process", run: () => api.end(process, false) })}>{process.protected ? "Protected" : "End process"}</button></div>)}</div>}</div>;
        })}{filteredApps.length === 0 && <div className="panel empty-state">{appsBusy ? "Reading running apps…" : "No apps match your search."}</div>}</div>
      </>}
      {page === "daily" && approvalsOpen && <ApprovedLocationsScreen approvals={dailyApprovals} onBack={()=>{setApprovalsOpen(false);requestAnimationFrame(()=>document.getElementById("daily-approvals-view-all")?.focus());}} onRevoke={async key=>{await api.revokeDailyApproval(key);setDailyApprovals(current=>current.filter(approval=>approval.key!==key));refreshDaily();}} onError={error=>notify(String(error),true)}/>}
      {page === "daily" && !approvalsOpen && <>
        <div className="page-heading"><div><h1>Daily cleanup</h1><p>Choose when to check your Mac and clean approved locations.</p></div><Button className="big-button" onClick={save} disabled={actionBusy || !dirty}>{actionBusy ? <LoaderCircle className="spin" /> : <Check />}{dirty ? "Save preferences" : "Preferences saved"}</Button></div>
        <div className="daily-hero panel"><span className="daily-illustration"><Clock3 size={65} strokeWidth={1.2} /></span><div><h2>{settings.enabled ? "Daily cleanup is on." : "Schedule daily cleanup."}</h2><p>Your agent checks for cleanup opportunities each day at your chosen time. It cleans only the exact locations and methods you previously approved. New locations wait for your review.</p><label className="toggle-row"><input type="checkbox" checked={settings.enabled} disabled={capabilities.sandboxed} onChange={(e) => setSettings({ ...settings, enabled: e.target.checked })} /><span>Enable daily cleanup</span></label><label className="toggle-row background-toggle"><input type="checkbox" checked={settings.keepInMenuBar} onChange={(e) => setSettings({ ...settings, keepInMenuBar: e.target.checked })} /><span>Keep running in the menu bar when I close the window</span></label><p className="metric-note">Sign in to use AI care. Runs while Breathing Room is open, including in the menu bar. Busy or low-battery Macs may run later. Quitting the app stops scheduled checks; launch-at-login is not enabled.</p></div></div>
        <div className="settings-grid"><section className="settings-panel panel"><h2><Clock3 size={22} />A good moment</h2><label className="field-label">Start time<select value={settings.hour} onChange={(e) => setSettings({ ...settings, hour: Number(e.target.value) })}>{Array.from({ length: 24 }, (_, h) => <option key={h} value={h}>{String(h).padStart(2, "0")}:00</option>)}</select></label><label className="field-label">Give it a window<select value={settings.windowHours} onChange={(e) => setSettings({ ...settings, windowHours: Number(e.target.value) })}>{[1, 2, 3, 4, 6].map((h) => <option key={h} value={h}>{h} {h === 1 ? "hour" : "hours"}</option>)}</select></label><p className="metric-note">No waking your Mac. No overlapping runs. Opt into menu-bar operation to keep care running after closing the window. Quitting the app stops it.</p></section>
          <ApprovedLocationsPreview approvals={dailyApprovals} onViewAll={()=>setApprovalsOpen(true)} onRevoke={async key=>{await api.revokeDailyApproval(key);setDailyApprovals(current=>current.filter(approval=>approval.key!==key));refreshDaily();}} onError={error=>notify(String(error),true)}/></div>
        <section className="settings-panel panel folders-panel"><h2><FolderOpen size={22} />Where to look</h2><Button variant="outline" className="big-button folder-picker" onClick={chooseFolder}><FolderOpen />Choose a folder</Button><label className="field-label">Home-folder paths, one per line<textarea rows={3} value={settings.scanPaths.join("\n")} onChange={(e) => setSettings({ ...settings, scanPaths: e.target.value.split("\n").filter((p) => p.trim()).map((p) => p.trim()) })} placeholder={native ? "/Users/you/Projects\n/Users/you/Downloads" : "Example: /Users/you/Projects"} /></label><p className="metric-note">Use the folder picker to grant access. Grants are stored as security-scoped bookmarks for later scans. Leave blank for accessible common home folders; symlink descendants are not followed.</p></section>
        <div className="care-strip"><span className="care-symbol"><Play size={25} /></span><div><h3>Want to check right now?</h3><p>Starts the same agent as the Assistant, with saved-approval cleanup enabled. Uses the same AI allowance.</p></div><Button className="big-button" disabled={agentBlocked || !!assistantBusy || dirty || capabilities.sandboxed} onClick={runCare}><Play />Run agent care</Button></div>
        {dailyNotifications.filter(n=>n.pendingCount>0||n.needsAttention).map(n=><section className="settings-panel panel" key={n.runId}><h2>{n.title}</h2><p>{n.body}</p><Button variant="outline" disabled={!!assistantBusy} onClick={()=>reviewDaily(n.runId)}>Review agent findings</Button></section>)}
        <History events={history} recovered={recovered} />
      </>}
      {page === "activity" && <ActivityPage status={liveStatus} onRefresh={refreshLive} onReview={reviewWithAi} navigation={panelDestination?.page==="activity"?panelDestination:undefined} navigationRequest={panelRequest}/>}
      {!cleanupFocused&&dailyNotice&&<section className="global-maintenance" role="status"><span className="global-maintenance-icon"><Leaf size={23}/></span><div><strong>{dailyNotice.title}</strong><p>{dailyNotice.body}</p></div><Button variant="outline" disabled={!!assistantBusy} onClick={()=>reviewDaily(dailyNotice.runId)}>Review findings</Button><button className="icon-button" aria-label="Dismiss daily care notification" onClick={()=>void api.markDailyNotificationSeen(dailyNotice.runId).then(refreshDaily)}><X size={16}/></button></section>}
      <CleanupAssistant active={page === "assistant"} request={cleanupRequest} requestScope={cleanupScope} requestDaily={cleanupDaily} requestedRunId={requestedRunId} runReviewRequest={runReviewRequest} profiles={settings.profiles} apps={apps} disabled={capabilities.sandboxed} operationRunning={agentBlocked} onBusyChange={setAssistantBusy} onFocusChange={setAssistantFocused} navigate={setPage} onCompleted={(run,isNew)=>{const moved=trashCompletion(run);if(isNew&&moved)setTrashNotice({key:`${run.id}:${run.outcomes.length}`,bytes:moved.bytes});volumeRequested.current=false;refreshDaily();void loadState();void scan();}} />
      <footer className="main-footer" hidden={cleanupFocused}><span><ShieldCheck size={15} />Local measurements. Clear choices.</span><AppUpdates hidden={cleanupFocused} blocked={scanBusy || volumeBusy || actionBusy || !!assistantBusy || !!nativeActivity}/></footer>
    </main>
    <Dialog open={profileOpen} onOpenChange={setProfileOpen}><DialogContent className="room-dialog"><DialogTitle>Make yourself at home.</DialogTitle><DialogDescription>Choose how you use your Mac. Mix profiles; every feature stays included.</DialogDescription><div className="profile-options">{profiles.map(({ id, name, description, icon: Icon }) => <button key={id} className={settings.profiles.includes(id) ? "chosen" : ""} aria-pressed={settings.profiles.includes(id)} onClick={() => setSettings((current) => ({ ...current, profiles: current.profiles.includes(id) ? current.profiles.length > 1 ? current.profiles.filter((p) => p !== id) : current.profiles : [...current.profiles, id] }))}><Icon size={26} /><span><strong>{name}</strong><small>{description}</small></span>{settings.profiles.includes(id) && <Check size={21} />}</button>)}</div><Button className="big-button" disabled={actionBusy} onClick={async () => { await save(); }}>Save profiles</Button><button className="text-button" onClick={() => setProfileOpen(false)}>Back to my Mac</button></DialogContent></Dialog>
    <Dialog open={aiOpen} onOpenChange={setAiOpen}><DialogContent className="room-dialog ai-dialog"><div className="ai-care-eyebrow"><Sparkles size={20} aria-hidden="true"/>AI Care</div><DialogTitle>Automatic daily cleanup</DialogTitle><DialogDescription className="ai-care-intro">Instead of starting every cleanup yourself, let AI care check your Mac each day. It remembers what you’ve approved and asks you to review anything new.</DialogDescription>
      <ul className="ai-care-benefits">
        <li><Clock3 size={20}/><div><strong>No need to remember to run cleanup</strong><p>Daily care checks at your chosen time and cleans only the locations you’ve already approved.</p></div></li>
        <li><Search size={20}/><div><strong>Find new cleanup opportunities</strong><p>Looks for temporary app files and other cleanup opportunities as you use your Mac. New locations wait for your approval.</p></div></li>
        <li><Activity size={20}/><div><strong>See where disk space is going</strong><p>Recent file changes and disk activity help your agent identify folders that may be filling up again, so you know what needs attention.</p></div></li>
      </ul>
      <p className="metric-note ai-care-schedule-note">Runs while Breathing Room is open, including in the menu bar. Busy or low-battery Macs may run later.</p>
      {aiCareActive?<p className="ai-care-active" role="status">Your AI Care subscription is active.</p>:<div className="ai-care-plan-options" aria-label="Subscribe to AI care">
        <Button className="big-button ai-care-subscribe" disabled={!billingConfig.liveCheckoutEnabled||!aiCareCheckoutUrl} onClick={()=>{if(aiCareCheckoutUrl)void api.openAiCareCheckout(aiCareCheckoutUrl).catch(error=>notify(String(error),true));}}>Monthly · $5 <ArrowUpRight size={17}/></Button>
        <Button className="big-button ai-care-subscribe" disabled={!billingConfig.liveCheckoutEnabled||!aiCareAnnualUrl} onClick={()=>{if(aiCareAnnualUrl)void api.openAiCareCheckout(aiCareAnnualUrl).catch(error=>notify(String(error),true));}}>Yearly · $50 <ArrowUpRight size={17}/></Button>
      </div>}
      <button type="button" className="text-button" disabled={!billingConfig.liveCheckoutEnabled} onClick={()=>void api.openAiCarePortal().catch(error=>notify(String(error),true))}>Manage subscription <ArrowUpRight size={14}/></button>
      <p className="metric-note">USD. Renews until cancelled. Yearly saves $10 compared with 12 monthly payments. Tax is shown at checkout. {billingConfig.liveCheckoutEnabled?"Use your Breathing Room account for secure Stripe checkout.":"Checkout is being connected; subscriptions are not available to purchase yet."} Local tools work without a subscription.</p>
    </DialogContent></Dialog>
    <Dialog open={confirmation !== null} onOpenChange={(open) => { if (!open && !actionBusy) setConfirmation(null); }}><DialogContent className="room-dialog"><DialogTitle>{confirmation?.title}</DialogTitle><DialogDescription>{confirmation?.detail}</DialogDescription>{!native && <div className="activation-note">Browser preview only. Nothing will be changed.</div>}<div className="dialog-actions"><Button variant="outline" className="big-button" disabled={actionBusy} onClick={() => setConfirmation(null)}>Cancel</Button><Button variant={confirmation?.destructive ? "destructive" : "default"} className="big-button" disabled={actionBusy} onClick={execute}>{actionBusy && <LoaderCircle className="spin" />}{actionBusy ? "Working…" : confirmation?.action}</Button></div></DialogContent></Dialog>
    {toast && <div className={`toast ${toast.error ? "error" : ""}`} role={toast.error ? "alert" : "status"}>{toast.error ? <CircleHelp size={20} /> : <Check size={20} />}<span>{toast.message}</span><button aria-label="Dismiss message" onClick={() => setToast(null)}><X size={18} /></button></div>}
  </div>;
}

function Finding({ icon, color, title, detail, action, onClick }: { icon: React.ReactNode; color: string; title: string; detail: string; action: string; onClick: () => void }) {
  return <article className="finding panel"><span className={`finding-icon ${color}`}>{icon}</span><h3>{title}</h3><p>{detail}</p><button onClick={onClick}>{action}<ArrowUpRight size={17} /></button></article>;
}
function History({ events, recovered }: { events: CareEvent[]; recovered: number }) {
  return <section className="history-section"><div className="section-heading"><h2>A little progress</h2><span>{formatBytes(recovered)} measured gains in history</span></div><div className="panel history-list">{events.length ? events.map((event) => <div className="history-row" key={event.id}><span className="history-check"><Check size={18} /></span><div><strong>{event.title}</strong><p>{event.detail}</p><small>{new Date(event.timestamp * 1000).toLocaleString()}</small></div>{event.recoveredBytes > 0 && <strong className="gain">+{formatBytes(event.recoveredBytes)}</strong>}</div>) : <div className="empty-state"><Clock3 size={27} /><h3>Your next check starts the story.</h3><p>Completed maintenance and measured results will appear here.</p></div>}</div></section>;
}
export default App;
