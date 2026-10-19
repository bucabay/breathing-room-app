import type { LiveStatus } from "./live.ts";

export function memoryUsage(status: LiveStatus | null) {
  const used = status?.memoryUsedBytes, total = status?.memoryTotalBytes;
  if (used == null || total == null || !Number.isFinite(used) || !Number.isFinite(total) || total <= 0 || used < 0 || used > total) return null;
  return { used, total, percent: used / total * 100 };
}

export function memoryTrend(status: LiveStatus | null): number[] {
  return (status?.history ?? []).flatMap(sample => {
    const value = sample.memoryPercent;
    return value != null && Number.isFinite(value) && value >= 0 && value <= 100 ? [value] : [];
  });
}
