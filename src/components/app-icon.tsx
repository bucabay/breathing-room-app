import { useEffect, useState } from "react";
import { Code2, Command, MessageCircle, PanelsTopLeft, Terminal, Cpu } from "lucide-react";
import { api } from "@/lib/api";
import type { AppGroup } from "@/lib/model";
const cache = new Map<string, string | null>();
export function AppIcon({ app }: { app: AppGroup }) {
  const [icon, setIcon] = useState(cache.get(app.id));
  useEffect(() => {
    let live = true;
    if (cache.has(app.id)) { setIcon(cache.get(app.id)); return; }
    if (app.bundlePath) api.icon(app.id).then((data) => { cache.set(app.id, data); if (live) setIcon(data); });
    return () => { live = false; };
  }, [app.id, app.bundlePath]);
  if (icon) return <img className="app-icon native-icon" src={icon} alt="" />;
  const lower = app.name.toLowerCase();
  if (lower.includes("chrome")) return <span className="app-icon"><svg width="38" height="38" viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="20" r="19" fill="#e9bb3c" /><path d="M20 1A19 19 0 0 0 3.5 29.5L20 20h19A19 19 0 0 0 20 1" fill="#e7614b" /><path d="M3.5 10.5A19 19 0 0 0 20 39l9.5-16.5L20 20Z" fill="#39a575" /><circle cx="20" cy="20" r="8.5" fill="#4285db" stroke="white" strokeWidth="2" /></svg></span>;
  const Icon = lower.includes("code") || lower.includes("cursor") ? Code2 :
    lower.includes("slack") ? MessageCircle : lower.includes("terminal") ? Terminal : lower.includes("figma") ? PanelsTopLeft :
    lower.includes("system") || lower.includes("macos") ? Cpu : Command;
  const color = lower.includes("chrome") ? "orange" : lower.includes("code") ? "blue" : lower.includes("slack") ? "violet" : "mint";
  return <span className={`app-icon ${color}`}><Icon size={27} strokeWidth={1.7} /></span>;
}
