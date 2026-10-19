import type { CleanupLocation, CleanupPlan } from "./cleanup";

export function canClean(location: CleanupLocation) {
  return location.executable && location.complete && location.kind !== "review";
}

export function selectionSummary(plan: Pick<CleanupPlan, "candidates">, ids: string[]) {
  const selected = new Set(ids);
  const items = plan.candidates.filter(c => selected.has(c.id));
  const eligible = items.filter(canClean);
  const reviewOnly = items.filter(c => !canClean(c));
  return { items, eligible, reviewOnly, bytes: items.reduce((sum, c) => sum + c.bytes, 0),
    eligibleBytes: eligible.reduce((sum, c) => sum + c.bytes, 0), permanent: eligible.filter(c => c.kind === "tool").length,
    trash: eligible.filter(c => c.kind === "trash").length };
}

export function locationStatus(location: CleanupLocation) {
  if (canClean(location)) return { label: "Ready to clean", tone: "ready" };
  if (location.kind === "review") return { label: "Agent will find cleanup", tone: "review" };
  if (!location.complete) return { label: location.sizeComplete ? "Needs validation" : "Incomplete scan", tone: "review" };
  if (/recent|running|open in|activity/i.test(location.reason)) return { label: "Recently used", tone: "review" };
  return { label: "Agent will find cleanup", tone: "review" };
}
