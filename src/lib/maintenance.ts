export interface MaintenanceActivity {
  title: string;
  page: string;
  blocksAgent?: boolean;
}

export function blocksAgent(activity: MaintenanceActivity | null | undefined): boolean {
  if (!activity) return false;
  if (activity.blocksAgent !== undefined) return activity.blocksAgent;
  // Compatibility with older native bundles and local preview progress.
  return !(activity.page === "space" && ["Refreshing disk map", "Mapping your whole disk"].includes(activity.title));
}

export function agentOperationBlocked(activity: MaintenanceActivity | null | undefined, scanBusy = false, actionBusy = false): boolean {
  // Check independent operations too: a visible map must not mask a mutation.
  return scanBusy || actionBusy || blocksAgent(activity);
}
