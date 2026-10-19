import type { LiveStatus } from "./live.ts";
import type { StorageReport } from "./model.ts";

export function createMetricsCache() {
  let snapshot: LiveStatus | null = null;
  let liveDisk = false;
  const listeners = new Set<() => void>();
  const publish = (next: LiveStatus) => { snapshot = next; for (const listener of listeners) listener(); return next; };
  return {
    getSnapshot: () => snapshot,
    subscribe: (listener: () => void) => { listeners.add(listener); return () => { listeners.delete(listener); }; },
    updateLive(next: LiveStatus) {
      // Slow requests must not roll a newer monitor sample back.
      if (snapshot?.timestamp != null && next.timestamp != null && next.timestamp < snapshot.timestamp) return snapshot;
      const merged = { ...snapshot, ...next };
      if (validDisk(next)) liveDisk = true;
      else if (snapshot && validDisk(snapshot)) {
        merged.totalBytes = snapshot.totalBytes; merged.availableBytes = snapshot.availableBytes;
        merged.diskTimestamp = snapshot.diskTimestamp; merged.ready = true;
      }
      if (snapshot?.diskTimestamp && next.diskTimestamp && next.diskTimestamp < snapshot.diskTimestamp) {
        merged.totalBytes = snapshot.totalBytes; merged.availableBytes = snapshot.availableBytes; merged.diskTimestamp = snapshot.diskTimestamp;
      }
      return publish(merged);
    },
    seedDisk(report: StorageReport) {
      if (liveDisk || !validDisk(report) || (snapshot?.diskTimestamp ?? 0) > report.scannedAt) return;
      publish({ ...snapshot, ready: true, totalBytes: report.totalBytes, availableBytes: report.availableBytes, diskTimestamp: report.scannedAt });
    },
  };
}

function validDisk(value: { totalBytes?: number; availableBytes?: number }): boolean {
  return Number.isFinite(value.totalBytes) && value.totalBytes! > 0 && Number.isFinite(value.availableBytes) && value.availableBytes! >= 0 && value.availableBytes! <= value.totalBytes!;
}

export function withCurrentDisk(report: StorageReport | null, metrics: LiveStatus | null): StorageReport | null {
  if (!report || !metrics || !validDisk(metrics)) return report;
  const totalBytes = metrics.totalBytes!, availableBytes = metrics.availableBytes!, usedBytes = totalBytes - availableBytes;
  const identified = report.identifiedBytes ?? report.scannedBytes;
  return { ...report, totalBytes, availableBytes, usedBytes,
    unmappedBytes: Math.max(0, usedBytes - identified), coveragePercent: usedBytes > 0 ? Math.min(100, identified / usedBytes * 100) : 0 };
}

export const metricsCache = createMetricsCache();
