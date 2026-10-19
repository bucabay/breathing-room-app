import { useEffect, useSyncExternalStore } from "react";
import { listen } from "@tauri-apps/api/event";
import { native } from "@/lib/api";
import { metricsCache } from "@/lib/metrics-cache";
import type { LiveStatus } from "@/lib/live";

export function useMetrics() {
  const metrics = useSyncExternalStore(metricsCache.subscribe, metricsCache.getSnapshot);
  useEffect(() => {
    if (!native) return;
    let live = true;
    const listener = listen<LiveStatus>("metrics-updated", event => { if (live) metricsCache.updateLive(event.payload); });
    return () => { live = false; void listener.then(unlisten => unlisten()); };
  }, []);
  return metrics;
}
