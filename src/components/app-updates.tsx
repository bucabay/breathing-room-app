import { useCallback, useEffect, useRef, useState } from "react";
import { invoke } from "@tauri-apps/api/core";
import { listen } from "@tauri-apps/api/event";
import { Download, LoaderCircle, RefreshCw } from "lucide-react";
import { native } from "@/lib/api";
import { Button } from "./ui/button";
import { Dialog, DialogContent, DialogDescription, DialogTitle } from "./ui/dialog";
import { updateMessage, type UpdateCheck } from "@/lib/updates";

export function AppUpdates({ blocked, hidden }: { blocked: boolean; hidden: boolean }) {
  const [open, setOpen] = useState(false);
  const [result, setResult] = useState<UpdateCheck | null>(null);
  const [phase, setPhase] = useState<"idle" | "checking" | "installing" | "restarting">("idle");
  const [error, setError] = useState("");
  const [progress, setProgress] = useState<{ downloaded: number; total: number | null } | null>(null);
  const busy = useRef(false);
  const installed = useRef(false);
  const check = useCallback(async () => {
    if (busy.current || installed.current) return;
    busy.current = true; setPhase("checking"); setError("");
    try {
      const value = native ? await invoke<UpdateCheck>("check_app_update") : { configured: false, currentVersion: "Browser preview", version: null, notes: null, installed: false };
      installed.current = value.installed; setResult(value);
    } catch (error) { setError(`Could not check for updates. ${String(error)}`); }
    finally { busy.current = false; setPhase("idle"); }
  }, []);
  useEffect(() => {
    // One background check at startup, then every six hours; never auto-install.
    const startup = setTimeout(() => void check(), 15_000);
    const timer = setInterval(() => void check(), 6 * 60 * 60 * 1000);
    return () => { clearTimeout(startup); clearInterval(timer); };
  }, [check]);
  useEffect(() => {
    if (!native) return;
    const listener = listen<{ downloaded: number; total: number | null }>("app-update-progress", event => setProgress(event.payload));
    return () => { void listener.then(unlisten => unlisten()); };
  }, []);
  const install = async () => {
    if (busy.current || blocked || !result?.version || result.installed) return;
    busy.current = true; setPhase("installing"); setError(""); setProgress(null);
    try {
      await invoke("install_app_update", { version: result.version });
      installed.current = true; setResult({ ...result, installed: true });
    } catch (error) { setError(`Update not completed. ${String(error)}`); }
    finally { busy.current = false; setPhase("idle"); }
  };
  const restart = async () => {
    if (busy.current || blocked || !result?.installed) return;
    busy.current = true; setPhase("restarting"); setError("");
    try { await invoke("restart_after_update"); }
    catch (error) { setError(String(error)); busy.current = false; setPhase("idle"); }
  };
  return <>
    <button hidden={hidden} className="text-button app-updates-trigger" onClick={() => { setOpen(true); void check(); }}><RefreshCw size={14}/>{result?.installed ? "Restart to finish update" : result?.version ? `Update ${result.version} available` : "App updates"}</button>
    <Dialog open={open} onOpenChange={setOpen}><DialogContent className="room-dialog">
      <DialogTitle>{result?.installed ? "Ready for a fresh start." : "Keep Breathing Room up to date."}</DialogTitle>
      <DialogDescription>{updateMessage(result)}</DialogDescription>
      {result?.version && !result.installed && <p><strong>Version {result.version}</strong></p>}
      {result?.notes && <p className="app-update-notes">{result.notes}</p>}
      {phase === "checking" && <p role="status">Checking for updates…</p>}
      {phase === "installing" && <p role="status">Downloading and verifying the signed update{progress?.total ? ` · ${Math.min(100, Math.round(progress.downloaded / progress.total * 100))}%` : "…"}</p>}
      {error && <p role="alert" className="app-update-error">{error}</p>}
      {blocked && <p className="metric-note">Wait for your current storage check or cleanup to finish before installing or restarting.</p>}
      <div className="dialog-actions">
        {result?.installed ? <Button className="big-button" disabled={blocked || phase !== "idle"} onClick={() => void restart()}><RefreshCw size={16}/>Restart now</Button>
          : result?.version ? <Button className="big-button" disabled={blocked || phase !== "idle"} onClick={() => void install()}>{phase === "installing" ? <LoaderCircle className="spin" size={16}/> : <Download size={16}/>}Download and install</Button>
          : <Button variant="outline" className="big-button" disabled={phase !== "idle"} onClick={() => void check()}>Check for updates</Button>}
      </div>
      <p className="metric-note">Checks run automatically. Downloads and installation need your approval, and the app never restarts itself without asking.</p>
    </DialogContent></Dialog>
  </>;
}
