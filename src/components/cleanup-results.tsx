import { useState, type CSSProperties } from "react";
import { ArrowRight, Check, CheckCheck, ChevronDown, CircleCheck, CircleHelp, FolderCheck, PartyPopper, SkipForward, Trash2, TriangleAlert } from "lucide-react";
import type { AgentCleanupRun } from "@/lib/agent-cleanup";
import { cleanupResultSummary, type CleanupOutcomeGroup } from "@/lib/cleanup-results";
import { formatBytes } from "@/lib/model";
import { Button } from "./ui/button";

const groups = [
  { key: "cleaned", label: "Cleaned", icon: FolderCheck, empty: "No cleanup actions completed in this batch." },
  { key: "failed", label: "Failed", icon: TriangleAlert, empty: "No failures to review." },
  { key: "skipped", label: "Skipped", icon: SkipForward, empty: "No actions were skipped." },
] as const;

function Confetti() {
  return <div className="cleanup-confetti" aria-hidden="true">{Array.from({ length: 64 }, (_, index) => {
    const angle = (index * 137.5) * Math.PI / 180;
    const distance = 170 + (index % 9) * 32;
    const style = {
      "--confetti-x": `${Math.cos(angle) * distance}px`,
      "--confetti-y": `${Math.sin(angle) * distance - 80}px`,
      "--confetti-rotation": `${index * 57}deg`,
      "--confetti-color": ["#4977f5", "#24a982", "#a079ef", "#f7b948", "#eb779b"][index % 5],
      "--confetti-delay": `${(index % 7) * 30}ms`,
    } as CSSProperties;
    return <i key={index} style={style} />;
  })}</div>;
}

export function CleanupResults({ run, preview, onReviewRemaining }: { run: AgentCleanupRun; preview: boolean; onReviewRemaining?: () => void }) {
  const summary = cleanupResultSummary(run);
  const [selected, setSelected] = useState<CleanupOutcomeGroup>(summary.groups.failed.length ? "failed" : "cleaned");
  const completed = summary.groups.cleaned.length;
  const total = run.outcomes.length;
  const stopped = run.status === "cancelled";
  const slices = summary.measured
    ? [{ value: summary.removed!, color: "var(--gain)" }, { value: summary.remaining!, color: "var(--ring-track)" }]
    : [{ value: completed, color: "var(--gain)" }, { value: summary.groups.failed.length, color: "var(--cleanup-failed)" }, { value: summary.groups.skipped.length, color: "var(--cleanup-skipped)" }];
  const sum = slices.reduce((sum, slice) => sum + slice.value, 0);
  let offset = 0;

  return <section className="cleanup-results-screen" aria-labelledby="cleanup-result-title">
    <header className="cleanup-result-hero" aria-live="polite">
      {completed > 0 && !stopped && <Confetti />}
      <div className={`cleanup-result-emblem ${completed ? "celebrate" : "neutral"}`} aria-hidden="true">{completed && !stopped ? <PartyPopper size={38} strokeWidth={1.6} /> : <CircleHelp size={38} strokeWidth={1.6} />}</div>
      <h1 id="cleanup-result-title"><span>{completed}</span> {completed === 1 ? "action" : "actions"} completed.</h1>
      <p>{stopped ? "Cleanup stopped. Here’s what finished before you stopped it." : completed ? "Congratulations! A little more breathing room." : "Let’s take a closer look at what needs attention."}{preview && <span className="cleanup-preview-note"> Example results · no Mac changes</span>}</p>
    </header>

    <div className="cleanup-result-overview">
      <figure className="cleanup-result-chart">
        <div className="cleanup-donut">
          <svg viewBox="0 0 220 220" role="img" aria-label={summary.measured ? `${summary.percent!.toFixed(1)} percent removed from measured cleanup locations` : `${completed} completed, ${summary.groups.failed.length} failed, ${summary.groups.skipped.length} skipped actions`}>
            <circle cx="110" cy="110" r="88" fill="none" stroke="var(--ring-track)" strokeWidth="19" />
            {slices.filter(slice => slice.value > 0).map((slice, index) => {
              const portion = sum ? slice.value / sum * 100 : 0;
              const start = offset; offset += portion;
              return <circle key={index} cx="110" cy="110" r="88" fill="none" stroke={slice.color} strokeWidth="19" pathLength="100" strokeDasharray={`${portion} ${100 - portion}`} strokeDashoffset={-start} transform="rotate(-90 110 110)" />;
            })}
          </svg>
          <div className="cleanup-donut-label"><strong>{summary.measured ? formatBytes(summary.removed!) : `${completed}/${total}`}</strong><span>{summary.measured ? "removed from locations" : "actions completed"}</span></div>
        </div>
        <figcaption>{summary.measured ? <><span><i className="cleanup-legend-cleaned" />{summary.percent!.toFixed(1)}% cleaned</span><span><i className="cleanup-legend-remaining" />{formatBytes(summary.remaining!)} remains</span></> : "Space measurements unavailable. This chart shows action outcomes."}</figcaption>
      </figure>
      <div className="cleanup-result-facts">
        <h2>{summary.measured ? "Space, accounted for." : "Every action, accounted for."}</h2>
        {summary.removed != null && <div><CheckCheck size={21} /><span>Removed from cleanup locations<strong>{formatBytes(summary.removed)}</strong></span></div>}
        {summary.pendingTrash != null && <div><Trash2 size={21} /><span>Waiting in Trash<strong>{formatBytes(summary.pendingTrash)}</strong></span></div>}
        {summary.spaceChange != null && <div><CircleCheck size={21} /><span>Available-space change · latest batch<strong>{summary.spaceChange < 0 ? "−" : "+"}{formatBytes(Math.abs(summary.spaceChange))}</strong></span></div>}
        <p>{summary.pendingTrash ? "Empty Trash to reclaim the space held there. " : ""}{summary.measured ? "Cleaned means removed from the source location. Available-space changes can include other disk activity." : "No space savings are claimed without before-and-after measurements."}</p>
        {onReviewRemaining && <Button variant="outline" onClick={onReviewRemaining}>Review remaining actions <ArrowRight size={16}/></Button>}
      </div>
    </div>

    <div className="cleanup-outcome-tabs" role="tablist" aria-label="Cleanup outcomes" onKeyDown={event=>{const index=groups.findIndex(group=>group.key===selected);const next=event.key==="ArrowRight"?(index+1)%3:event.key==="ArrowLeft"?(index+2)%3:event.key==="Home"?0:event.key==="End"?2:null;if(next==null)return;event.preventDefault();setSelected(groups[next].key);event.currentTarget.querySelector<HTMLButtonElement>(`#cleanup-tab-${groups[next].key}`)?.focus();}}>{groups.map(({ key, label, icon: Icon }) => <button key={key} id={`cleanup-tab-${key}`} role="tab" tabIndex={selected === key ? 0 : -1} aria-selected={selected === key} aria-controls="cleanup-outcome-panel" className={`cleanup-outcome-tab ${key} ${selected === key ? "selected" : ""}`} onClick={() => setSelected(key)}><Icon size={27} strokeWidth={1.7} /><span>{label}<strong>{summary.groups[key].length}</strong></span>{selected === key && <Check size={17}/>}</button>)}</div>
    <div id="cleanup-outcome-panel" role="tabpanel" aria-labelledby={`cleanup-tab-${selected}`} className={`cleanup-outcome-panel ${selected}`}>
      {summary.groups[selected].length ? <ul>{summary.groups[selected].map(outcome => {
        const action = run.actions.find(action => action.id === outcome.id);
        const Icon = selected === "cleaned" ? CircleCheck : selected === "failed" ? TriangleAlert : SkipForward;
        return <li key={outcome.id}><span className="cleanup-outcome-illustration"><Icon size={24} strokeWidth={1.6}/></span><div><strong>{action?.title || outcome.id}</strong><p>{outcome.status === "running" ? "Interrupted: the final outcome needs review. This action will not replay automatically." : outcome.detail}</p>{action?.paths.map(path => <code key={path}>{path}</code>)}</div><span className="cleanup-outcome-measure">{outcome.removedBytes != null ? formatBytes(outcome.removedBytes) : "—"}<small>{outcome.percentCleaned != null ? `${outcome.percentCleaned.toFixed(1)}% cleaned` : "Not measured"}</small></span></li>;
      })}</ul> : <div className="cleanup-outcome-empty">{selected === "failed" ? <CircleCheck size={32}/> : selected === "skipped" ? <SkipForward size={32}/> : <FolderCheck size={32}/>}<p>{groups.find(group => group.key === selected)?.empty}</p></div>}
    </div>
    {run.results && <details className="cleanup-results-data"><summary>Results JSON <ChevronDown size={15}/></summary><pre className="agent-results-json">{JSON.stringify(run.results, null, 2)}</pre></details>}
  </section>;
}
