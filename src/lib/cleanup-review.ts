import type { AgentCleanupAction } from "./agent-cleanup";

export function cleanupSelection(actions: AgentCleanupAction[], selected: string[]) {
  const ids = new Set(selected);
  const chosen = actions.filter(action => ids.has(action.id));
  return {
    ids: chosen.map(action => action.id),
    all: actions.length > 0 && chosen.length === actions.length,
    partial: chosen.length > 0 && chosen.length < actions.length,
    bytes: chosen.reduce((sum, action) => sum + action.estimatedBytes, 0),
  };
}

export function toggleAllCleanup(actions: AgentCleanupAction[], checked: boolean) {
  return checked ? actions.map(action => action.id) : [];
}
