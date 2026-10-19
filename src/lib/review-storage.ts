import type { InventoryItem, ReviewStorageLocation } from "./agent-cleanup";

export function reviewStorageLocations(locations: ReviewStorageLocation[], inventory: InventoryItem[]) {
  const result = [...locations];
  for (const item of inventory) {
    if (!item.severity || !item.recoverability || !item.warning || !item.owned || item.state !== "complete") continue;
    if (result.some(old => [old.path,...(old.aliases||[])].some(path=>item.path===path||item.path.startsWith(`${path}/`)||path.startsWith(`${item.path}/`)))) continue;
    result.push({ path: item.path, title: item.path.split("/").pop() || item.path, bytes: item.bytes,
      logicalBytes: item.logicalBytes, modifiedAt: item.modifiedAt, fileCount: 1, partial: false,
      severity: item.severity, recoverability: item.recoverability, warning: item.warning,
      reviewOnly: true, cleanupEligible: false, requiresSelection: true });
  }
  return result;
}

export function reviewStorageGroups(items: ReviewStorageLocation[]) {
  return {
    critical: items.filter(item => item.severity === "critical"),
    warning: items.filter(item => item.severity !== "critical"),
  };
}

// Review selection is deliberately separate from executable action IDs/approval.
export function selectedReviewLocations(items: ReviewStorageLocation[], paths: string[]) {
  return items.filter(item => paths.includes(item.path) && item.reviewOnly === true && item.cleanupEligible === false);
}
