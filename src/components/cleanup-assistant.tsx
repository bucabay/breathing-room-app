import { useEffect, useRef, useState } from "react";
import { ArrowLeft, ArrowRight, Bot, Check, ChevronDown, CircleHelp, FolderSearch, LoaderCircle, Send, Sparkles, X } from "lucide-react";
import { Button } from "./ui/button";
import { Dialog, DialogContent, DialogDescription, DialogTitle } from "./ui/dialog";
import { AuthProviderButtons } from "./auth-provider-buttons";
import { CleanupResults } from "./cleanup-results";
import { CleanupActionList } from "./cleanup-action-list";
import { ReviewStorage } from "./review-storage";
import { AssistantConversation } from "./assistant-conversation";
import { assistantHistory, type AssistantTurn } from "@/lib/assistant";
import { api, native } from "@/lib/api";
import type { AgentCleanupConnection, AgentCleanupRun, InventoryPage } from "@/lib/agent-cleanup";
import { pendingCleanupActions, defaultDiscoveryPolicy } from "@/lib/agent-cleanup";
import { reviewStorageLocations } from "@/lib/review-storage";
import { formatBytes, type AppGroup, type Page, type Profile } from "@/lib/model";

export function CleanupAssistant({ active, request, requestScope, requestDaily, requestedRunId, runReviewRequest, disabled: unsupported, operationRunning, onBusyChange, onFocusChange, navigate, onCompleted }: {
  active: boolean; request: number; requestScope: string; profiles: Profile[]; apps: AppGroup[]; disabled: boolean;
  operationRunning: boolean; onBusyChange: (title: string) => void; navigate: (page: Page) => void; onCompleted: (run:AgentCleanupRun,newCompletion:boolean) => void;
  onFocusChange: (focused: boolean) => void;
  requestDaily?:boolean;requestedRunId?:string;runReviewRequest?:number;
}) {
  const [input, setInput] = useState("Free up disk space. Clean reproducible caches and generated files; keep my personal files.");
  const [dockInput, setDockInput] = useState("");
  const [connection, setConnection] = useState<AgentCleanupConnection | null>(null);
  const [model, setModel] = useState("@cf/qwen/qwen3-30b-a3b-fp8");
  const [apiUrl, setApiUrl] = useState("");
  const [loginId, setLoginId] = useState("");
  const [authBusy, setAuthBusy] = useState(false);
  const [loginOpen, setLoginOpen] = useState(false);
  const loginPrompted = useRef(false);
  const restored = useRef(false);
  const generation = useRef(0);
  const [run, setRun] = useState<AgentCleanupRun | null>(null);
  const [runId, setRunId] = useState("");
  const [selected, setSelected] = useState<string[]>([]);
  const [starting, setStarting] = useState(false);
  const [conversing,setConversing]=useState(false);
  const [turns,setTurns]=useState<AssistantTurn[]>([]);
  const [automatic, setAutomatic] = useState(false);
  const [limits,setLimits]=useState(defaultDiscoveryPolicy);
  const [inventoryPage,setInventoryPage]=useState<InventoryPage|null>(null);
  const [inventoryCategory,setInventoryCategory]=useState("");
  const [inventoryBusy,setInventoryBusy]=useState(false);
  const [candidateDisplay,setCandidateDisplay]=useState(50);
  const [error, setError] = useState("");
  const [returning, setReturning] = useState(false);
  const [reviewRemaining, setReviewRemaining] = useState(false);
  const flowRoot = useRef<HTMLElement>(null);
  const previousRequest = useRef(request);
  const completed = useRef("");
  const liveRuns=useRef(new Set<string>());
  const reviewing = useRef("");
  const busy = starting || conversing || run?.status === "inspecting" || run?.status === "executing";
  const disabled = unsupported || (operationRunning && !busy);
  const loginRequired = !connection?.authenticated;
  const focused = starting || run != null;
  const showResults = !!run && run.outcomes.length > 0 && !busy && !reviewRemaining;
  const showPlan = !!run && (run.status === "review" || (run.status === "done" && reviewRemaining));
  const phase = showResults || run?.status === "executing" || (run?.status === "done" && !reviewRemaining) ? 2 : showPlan ? 1 : 0;
  const pending = run ? pendingCleanupActions(run) : [];
  const chosen = pending.filter(action => selected.includes(action.id));
  const estimated = chosen.reduce((sum, action) => sum + action.estimatedBytes, 0);
  const loadInventory=async(category=inventoryCategory,offset=0)=>{if(!run||inventoryBusy)return;const current=generation.current;setInventoryBusy(true);try{const page=await api.agentCleanupInventory(run.id,offset,category||undefined);if(current!==generation.current)return;setInventoryCategory(category);setInventoryPage(page);}catch(error){if(current===generation.current)setError(String(error));}finally{if(current===generation.current)setInventoryBusy(false);}};

  useEffect(() => { onBusyChange(busy ? conversing ? "Your agent is answering" : run?.status === "executing" ? "Your agent is cleaning approved locations" : "Your agent is inspecting the disk" : ""); }, [busy, conversing, run?.status, onBusyChange]);
  useEffect(()=>{setTurns([]);},[connection?.account?.subject]);
  useEffect(() => { onFocusChange(focused); }, [focused, onFocusChange]);
  useEffect(() => {
    if (active && focused) { window.scrollTo({ top: 0, behavior: "instant" }); flowRoot.current?.focus({ preventScroll: true }); }
  }, [active, focused, phase, showResults]);
  const checkConnection = async () => {
    setError("");
    try { const value = await api.agentCleanupConnection(); setConnection(value); setApiUrl(value.baseUrl || ""); setModel(value.defaultModel || value.models[0] || model); if (value.authenticated) setLoginOpen(false); }
    catch (e) { setError(String(e)); }
  };
  useEffect(() => { void checkConnection(); }, []);
  useEffect(() => {
    if (!active) { loginPrompted.current = false; return; }
    if (connection && !connection.authenticated && !loginPrompted.current) { loginPrompted.current = true; setLoginOpen(true); }
  }, [active, connection]);
  useEffect(() => {
    if (!active || restored.current) return;
    restored.current = true; const current = generation.current;
    void api.agentCleanupLatest().then(value => {
      if (!value || generation.current !== current) return;
      setRun(value); setRunId(value.id);
      if (["review","done"].includes(value.status)) { reviewing.current = value.id; setSelected(pendingCleanupActions(value).map(action => action.id)); }
    }).catch(() => {});
  }, [active]);
  useEffect(()=>{
    if(!requestedRunId)return;
    const current=++generation.current;restored.current=true;setStarting(false);setError("");setInventoryPage(null);setReviewRemaining(false);
    void api.agentCleanupState(requestedRunId).then(value=>{if(current!==generation.current)return;setRun(value);setRunId(value.id);reviewing.current=value.id;const pending=pendingCleanupActions(value);setReviewRemaining(value.status==="done"&&pending.length>0);setSelected(pending.map(action=>action.id));}).catch(error=>{if(current===generation.current)setError(String(error));});
  },[requestedRunId,runReviewRequest]);
  const signIn = async (provider: string) => {
    setLoginOpen(true); setError(""); setAuthBusy(true);
    try { const login = await api.agentAuthStart(provider); setLoginId(login.id); }
    catch (error) { setError(String(error)); setAuthBusy(false); }
  };
  useEffect(() => {
    if (!loginId) return;
    let live = true; let polling = false;
    const poll = async () => {
      if (polling) return; polling = true;
      try { const result = await api.agentAuthPoll(loginId); if (live && result.status === "succeeded") { setLoginId(""); setAuthBusy(false); await checkConnection(); } }
      catch (error) { if (live) { setError(String(error)); setLoginId(""); setAuthBusy(false); } }
      finally { polling = false; }
    };
    const timer = setInterval(() => void poll(), 2000); void poll();
    return () => { live = false; clearInterval(timer); };
  }, [loginId]);
  useEffect(() => {
    if (!runId) return;
    let live = true;
    const current = generation.current;
    const poll = async () => {
      try {
        const value = await api.agentCleanupState(runId);
        if (!live || generation.current !== current) return;
        setRun(value);
        if(value.status==="inspecting"||value.status==="executing")liveRuns.current.add(value.id);
        if (value.status === "review" && reviewing.current !== value.id) { reviewing.current = value.id; setSelected(value.actions.map(action => action.id)); }
        const completionKey = `${value.id}:${value.outcomes.length}`;
        if ((value.status === "done" || value.status === "cancelled") && !value.outcomes.some(outcome=>outcome.status==="running") && completed.current !== completionKey) { completed.current = completionKey; setSelected(pendingCleanupActions(value).map(action=>action.id)); onCompleted(value,liveRuns.current.delete(value.id)); }
      } catch (e) { if (live) setError(String(e)); }
    };
    void poll(); const timer = setInterval(() => void poll(), 1000);
    return () => { live = false; clearInterval(timer); };
  }, [runId]);
  const inspect = async (text = input, scope = "",daily=false) => {
    if (busy || disabled || !text.trim()) return;
    if (loginRequired) { setLoginOpen(true); navigate("assistant"); return; }
    if (!connection?.available) { setError(connection?.message || "The agent connection is unavailable."); return; }
    const current = ++generation.current;
    setStarting(true); setReviewRemaining(false); setError(""); setRun(null); setRunId(""); setSelected([]);setInventoryBusy(false);setInventoryPage(null);setInventoryCategory("");setCandidateDisplay(50); navigate("assistant");
    try { const id = await api.agentCleanupInspect(text.trim(), scope, model, automatic,limits,daily); if (generation.current !== current) { await api.agentCleanupCancel(id); return; } liveRuns.current.add(id);setRunId(id); const initial = await api.agentCleanupState(id); if(generation.current !== current) return; setRun(initial); if (initial.status === "review") { reviewing.current = id; setSelected(pendingCleanupActions(initial).map(action => action.id)); } }
    catch (e) { if(generation.current === current) setError(String(e)); }
    finally { if(generation.current === current) setStarting(false); }
  };
  const ask = async(text=input)=>{
    if(busy||disabled||!text.trim())return;
    if(loginRequired){setLoginOpen(true);navigate("assistant");return;}
    if(!connection?.available){setError(connection?.message||"The agent connection is unavailable.");return;}
    const current=++generation.current;restored.current=true;setConversing(true);setError("");navigate("assistant");
    try{
      const reply=await api.assistantMessage(text.trim(),assistantHistory(turns),automatic,limits);
      if(current!==generation.current){if(reply.runId)await api.agentCleanupCancel(reply.runId);return;}
      setTurns(old=>[...old.slice(-11),{id:crypto.randomUUID(),question:text.trim(),reply}]);setInput("");
      if(reply.runId){liveRuns.current.add(reply.runId);setReviewRemaining(false);setSelected([]);setInventoryPage(null);setInventoryCategory("");setCandidateDisplay(50);setRunId(reply.runId);const initial=await api.agentCleanupState(reply.runId);if(current!==generation.current)return;setRun(initial);if(initial.status==="review"){reviewing.current=initial.id;setSelected(pendingCleanupActions(initial).map(action=>action.id));}}
    }catch(error){if(current===generation.current)setError(String(error));}
    finally{if(current===generation.current)setConversing(false);}
  };
  useEffect(() => {
    if (request !== previousRequest.current && active && connection && !disabled && !busy) {
      previousRequest.current = request;
      const text = requestScope ? `Check this location and propose safe cleanup: ${requestScope}` : "Free up disk space. Verify reproducible caches and generated files, and keep personal files.";
      setInput(text); void inspect(text, requestScope,requestDaily);
    }
  }, [request, active, connection, disabled, busy,requestDaily]);
  const approve = async (ids = chosen.map(action=>action.id)) => {
    if (!run || !ids.length || busy) return;
    if (loginRequired) { setLoginOpen(true); return; }
    const current = generation.current;
    liveRuns.current.add(run.id);
    setReviewRemaining(false); setError(""); setRun({ ...run, status: "executing" });
    try { await api.agentCleanupApprove(run.id, ids); }
    catch (e) { if(generation.current === current) { setRun(run); setError(String(e)); } }
  };
  const stop = async () => { if (runId) { try { await api.agentCleanupCancel(runId); setRun(current => current ? { ...current, status: "cancelled" } : current); } catch(error) { setError(String(error)); } } };
  const backToAgent = async () => {
    if(returning) return;
    setReturning(true);
    try {
      if (busy && runId) await api.agentCleanupCancel(runId);
      generation.current += 1; restored.current = true;
      setRunId(""); setRun(null); setSelected([]); setStarting(false); setReviewRemaining(false); setError("");
      onBusyChange(""); onFocusChange(false); window.scrollTo({ top:0, behavior:"instant" });
    } catch (error) { setError(String(error)); }
    finally { setReturning(false); }
  };

  return <>
    {!active && !focused && <div className="assistant-dock"><form className="assistant-composer" onSubmit={e => { e.preventDefault(); setInput(dockInput); void ask(dockInput); setDockInput(""); }}>
      <button type="button" className="assistant-avatar" aria-label="Open Cleanup AI Assistant" onClick={() => navigate("assistant")}><Bot size={25}/></button>
      <input aria-label="Ask your Cleanup AI Assistant" placeholder={loginRequired ? "Sign in to use your agent…" : "Ask a question or investigate your Mac…"} value={dockInput} onChange={e => setDockInput(e.target.value)} disabled={!!busy || disabled || loginRequired}/>
      {loginRequired ? <button type="button" className="assistant-dock-login" onClick={() => { navigate("assistant"); setLoginOpen(true); }}>Sign in</button> : <button className="assistant-send" aria-label="Send AI assistant request" disabled={!dockInput.trim() || !!busy || disabled}><Send size={20}/></button>}
    </form></div>}
    {active && <section ref={flowRoot} tabIndex={-1} className={`agent-cleanup-page ${focused ? "agent-cleanup-focused" : ""}`} aria-label="Cleanup agent">
      {!focused && <header className="agent-cleanup-heading"><div><h1 id="cleanup-assistant-title">How can I help?</h1><p>Ask a question, investigate your Mac, or find space to free.</p></div><span className="agent-cleanup-mark"><Bot size={32}/></span></header>}
      {focused && <div className="cleanup-flow-navigation"><ol className="agent-cleanup-steps" aria-label="Cleanup progress">{["Inspect", "Review plan", "Clean"].map((label, index) => <li key={label} className={index === phase ? "current" : index < phase ? "complete" : ""} aria-current={index === phase ? "step" : undefined}><span>{index + 1}</span>{label}</li>)}</ol><Button variant="outline" className="cleanup-back-button" disabled={returning} onClick={()=>void backToAgent()}><ArrowLeft size={16}/>{returning ? "Stopping…" : "Back to agent"}</Button></div>}
      {showResults && run && <CleanupResults key={`${run.id}:${run.outcomes.length}`} run={run} preview={!native} onReviewRemaining={pending.length && run.status === "done" ? ()=>setReviewRemaining(true) : undefined}/>}
      {unsupported && <div className="cleanup-error">Agent cleanup is available in the development desktop app.</div>}
      <AssistantConversation turns={turns} focused={focused}/>
      {!focused && <form className="agent-cleanup-request" onSubmit={e => { e.preventDefault(); void ask(); }}>
        <label htmlFor="agent-cleanup-request">What would you like to know?</label>
        <textarea id="agent-cleanup-request" value={input} maxLength={2000} rows={3} onChange={e => setInput(e.target.value)} disabled={!!busy || loginRequired} aria-describedby={loginRequired ? "agent-login-required" : undefined} />
        <label className="agent-automatic-option"><input type="checkbox" checked={automatic} onChange={event=>setAutomatic(event.target.checked)} disabled={!!busy || loginRequired}/><span>Automatically move verified Ruff lint caches to Trash<small>Only owned, tagged project caches. Other cleanup methods need your approval.</small></span></label>
        <details className="agent-cleanup-settings"><summary>Discovery settings <ChevronDown size={16}/></summary><p>When you request disk investigation, agent exploration, known/app locations, recent files and general inventory run in parallel. Native-verified findings merge into one list. Personal files remain review-only.</p><label className="field-label">Maximum discovery turns<input type="number" min={1} max={32} value={limits.maxTurns} onChange={e=>setLimits({...limits,maxTurns:Number(e.target.value)})}/></label><label className="field-label">Maximum discovery tool calls<input type="number" min={1} max={192} value={limits.maxToolCalls} onChange={e=>setLimits({...limits,maxToolCalls:Number(e.target.value)})}/></label><p>Read-only terminal calls can run for up to two minutes each. The discovery session has a ten-minute reasoning limit. Reaching a limit means partial coverage, not a complete scan.</p></details>
        <div className="agent-cleanup-request-footer"><span><Check size={17}/>{loginRequired ? "Sign in required to use the agent" : automatic ? "Automatic lint-cache cleanup enabled for disk investigations" : "Nothing changes before your approval"}</span><Button className="big-button" disabled={!!busy || disabled || !input.trim() || !connection?.available || loginRequired}><Sparkles/>{conversing ? "Thinking…" : "Ask agent"}</Button></div>
      </form>}
      {loginRequired && !focused && <section className="agent-auth-panel" aria-label="Agent sign-in"><div><strong>Sign in to your cleanup agent</strong><p id="agent-login-required">Sign in is required before the agent can inspect your Mac or clean approved locations.</p><p>{authBusy ? "Complete sign-in in your browser. You’ll return to the app automatically." : connection?.message || "Checking the remote connection…"}</p></div><AuthProviderButtons disabled={authBusy || !connection?.authConfigured} onSelect={provider => void signIn(provider)} /><button type="button" className="text-button agent-login-open" onClick={() => setLoginOpen(true)}>{authBusy ? "View sign-in progress" : "Open sign-in"}</button></section>}
      {!focused && <details className="agent-cleanup-settings"><summary><span>Cloudflare Workers AI · {connection?.authenticated ? "signed in" : native ? "sign-in required" : "preview"}</span><ChevronDown size={16}/></summary><p>{connection?.message || "Checking your remote agent connection…"}</p><p>The model is configured by the API. Inspection and usage are saved locally in SQLite.</p><label className="field-label">API origin<input aria-label="Agent API origin" value={apiUrl} onChange={event => setApiUrl(event.target.value)} /></label><div className="agent-auth-actions"><Button variant="outline" onClick={async () => { try { await api.agentApiConfigure(apiUrl); await checkConnection(); } catch (error) { setError(String(error)); } }}>Save API origin</Button><Button variant="outline" onClick={() => void checkConnection()}>Check connection</Button>{native && connection?.authenticated && <Button variant="outline" onClick={async () => { try { await api.agentAuthLogout(); await checkConnection(); } catch (error) { setError(String(error)); } }}>Sign out</Button>}</div>{connection?.usage && <p>{connection.usage.requests} inference requests recorded in the local ledger{connection.usage.neuronEstimate != null ? ` · ${Math.round(connection.usage.neuronEstimate)} estimated Neurons` : ""}</p>}</details>}
      {(error || run?.error) && <div className="cleanup-error" role="alert"><CircleHelp size={20}/><span>{error || run?.error}</span></div>}
      {run?.status === "failed" && !run.approvedIds.length && <Button variant="outline" disabled={!connection?.authenticated || disabled} onClick={()=>void inspect(run.request,run.scope || "")}>Start a new inspection</Button>}
      {conversing && <div className="agent-cleanup-working" role="status"><LoaderCircle className="spin" size={24}/><div><strong>Your agent is answering</strong><p>Using the tools relevant to your question…</p></div></div>}
      {busy && !conversing && <div className="agent-cleanup-working" role="status"><LoaderCircle className="spin" size={24}/><div><strong>{run?.status === "executing" ? "Cleaning the locations you approved" : "Your agent is checking the disk"}</strong><p>{run?.activity[run.activity.length - 1] || "Inspecting actual locations and owning-app cleanup methods…"}</p></div><Button variant="outline" disabled={!runId} onClick={() => void stop()}><X/>Stop</Button></div>}
      {run && showPlan && <section className="agent-cleanup-plan" aria-labelledby="agent-plan-title">
        <div className="agent-cleanup-plan-heading"><div><h2 id="agent-plan-title">Ready for cleanup</h2><p>Verified cleanup methods. Choose locations, then approve.</p></div><span>{formatBytes(estimated)}<small>measured selected locations</small></span></div>
        {pending.length > 0 && <CleanupActionList actions={pending} selected={selected} onSelected={setSelected} onApprove={ids => void approve(ids)} disabled={disabled || loginRequired || !!busy}/>}
        {!pending.length ? <div className="empty-state"><FolderSearch size={28}/><p>{run.outcomes.length ? "All planned actions have been attempted." : "No supported cleanup actions in this plan. Manual inspection is separate below."}</p></div> : <div className="agent-cleanup-approval"><div><strong>{chosen.length} cleanup actions selected</strong><p>{loginRequired ? "Sign in required to use the agent" : "Prune may remove less than measured. Empty Trash separately to reclaim its space."}</p><small>Approvals remember the exact location and method for Daily care; revoke them there.</small></div><Button className="big-button" disabled={!chosen.length || disabled || loginRequired || !!busy} onClick={() => void approve()}><Check/>Approve selected cleanup<ArrowRight/></Button></div>}
      </section>}
      {run?.discovery && !showResults && <ReviewStorage key={run.id} items={reviewStorageLocations(run.discovery.reviewLocations || [], [...(run.discovery.inventory?.largest || []), ...(inventoryPage?.entries || [])])} onReveal={path => void api.reveal(path).catch(error => setError(String(error)))}/>}
      {run?.discovery && !showResults && <details className="cleanup-inspection-details"><summary>Inspection details <ChevronDown size={16}/></summary><p>{run.overview}</p>
      {run?.discovery?.inventory && !showResults && <details className="agent-cleanup-discovery"><summary>{run.discovery.inventory.filesInspected.toLocaleString()} files inventoried · {formatBytes(run.discovery.inventory.measuredBytes)} measured <ChevronDown size={16}/></summary><p>{run.discovery.inventory.partial?"Partial inventory":"Completed inventory"} · {run.discovery.inventory.pendingDirectories} queued directories · {run.discovery.inventory.inaccessible} inaccessible · {run.discovery.inventory.excluded} excluded. Metadata sizes are not guaranteed reclaimable space.</p><div className="agent-auth-actions">{run.discovery.inventory.categories.map(category=><Button key={category.name} variant="outline" disabled={inventoryBusy} onClick={()=>void loadInventory(category.name)}>{category.name} · {formatBytes(category.bytes)}</Button>)}</div><Button variant="outline" disabled={inventoryBusy} onClick={()=>void loadInventory("")}>Browse large files</Button><p>Large files, media and app-managed data are for review. They are not selected for deletion.</p><ul>{(inventoryPage?.entries||run.discovery.inventory.largest).map(item=><li key={item.path}><strong>{item.category} · {formatBytes(item.bytes)}</strong><code>{item.path}</code><span>{item.state} · review only</span><button className="text-button" onClick={()=>void api.reveal(item.path).catch(error=>setError(String(error)))}>Show in Finder</button></li>)}</ul>{inventoryPage&&<p>{inventoryPage.entries.length?`Showing ${inventoryPage.offset+1}–${inventoryPage.offset+inventoryPage.entries.length} of ${inventoryPage.totalEntries} large files in this view.`:"No files above 50 MiB in this inventory view."}</p>}{inventoryPage?.nextOffset!=null&&<Button variant="outline" disabled={inventoryBusy} onClick={()=>void loadInventory(inventoryCategory,inventoryPage.nextOffset!)}>Next page</Button>}</details>}
      {run?.discovery?.agent && !showResults && <details className="agent-cleanup-discovery"><summary>Agent discovery · {run.discovery.agent.status} <ChevronDown size={16}/></summary><p>{run.discovery.agent.reason}</p><p>{run.discovery.agent.toolCalls} tool calls · {run.discovery.agent.learnedRules} discovery rules saved for future scans. Learned rules do not grant cleanup authority.</p></details>}
      {run?.discovery && !showResults && <details className="agent-cleanup-discovery"><summary>{run.discovery.candidates.length} supported cleanup candidates · {run.actions.length} in this plan <ChevronDown size={16}/></summary><p>{run.discovery.coverage.join(" ")}</p><ul>{run.discovery.candidates.slice(0,candidateDisplay).map(action=><li key={action.id}><strong>{action.title}</strong><span>{formatBytes(action.estimatedBytes)}</span><code>{action.paths.join(", ")}</code></li>)}</ul>{candidateDisplay<run.discovery.candidates.length&&<Button variant="outline" onClick={()=>setCandidateDisplay(count=>count+50)}>Show more candidates ({run.discovery.candidates.length-candidateDisplay} remaining)</Button>}{run.discovery.manual.length>0&&<><h3>Owning-app review needed</h3>{run.discovery.manual.map((item,index)=><p key={index}><code>{item.path}</code><br/>{item.reason}</p>)}</>}{run.discovery.errors.map((error,index)=><p key={index}>{error}</p>)}</details>}
      </details>}
      {run && !busy && !showResults && !showPlan && <div className="cleanup-flow-empty"><CircleHelp size={40}/><h1>{run.status === "cancelled" ? "Cleanup stopped." : run.status === "failed" ? "Let’s try that again." : "This batch is complete."}</h1><p>Use Back to agent to start a fresh inspection.</p></div>}
      {run && <details className="agent-cleanup-activity"><summary>Agent activity <ChevronDown size={16}/></summary><ul>{run.activity.map((line, index) => <li key={index}>{line}</li>)}</ul></details>}
    </section>}
    <Dialog open={loginOpen && loginRequired} onOpenChange={setLoginOpen}><DialogContent className="room-dialog agent-login-dialog"><span className="agent-login-symbol"><Bot size={30}/></span><DialogTitle>Sign in to use your agent</DialogTitle><DialogDescription>Your agent stays disabled until you sign in. Continue securely in your browser with Google or GitHub.</DialogDescription>{authBusy && <div className="agent-login-progress" role="status"><LoaderCircle className="spin" size={20}/><div><strong>Waiting for browser sign-in…</strong><p>Sign in with your provider, then return to the app. This window closes automatically.</p></div></div>}<AuthProviderButtons disabled={authBusy || !connection?.authConfigured} onSelect={provider => void signIn(provider)} />{error && <div className="cleanup-error" role="alert">{error}</div>}{!connection?.authConfigured && <p className="metric-note">{connection?.message || "Checking the remote connection…"}</p>}<Button type="button" variant="outline" onClick={() => void checkConnection()}>Check connection</Button></DialogContent></Dialog>
  </>;
}
