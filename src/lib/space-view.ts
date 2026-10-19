import type { Bucket, StorageView } from "./model";

export type SpaceTab = StorageView | "explore" | "large";
export const spaceTabs: { id: SpaceTab; name: string }[] = [
  { id: "category", name: "Categories" }, { id: "owner", name: "Apps & tools" },
  { id: "project", name: "Projects" }, { id: "explore", name: "Explore" }, { id: "large", name: "Large files" },
];
export const spaceColors = ["#8b5cf6", "#3b82f6", "#16a085", "#ef9855", "#ec6d98", "#719bb3", "#dcac33"];
export function spaceSlices(items: Bucket[], maximum = 6): (Bucket & { percent: number })[] {
  const measured = items.filter(item => Number.isFinite(item.bytes) && item.bytes > 0).sort((a, b) => b.bytes - a.bytes);
  const total = measured.reduce((sum, item) => sum + item.bytes, 0);
  const visible = measured.slice(0, maximum);
  const remainder = measured.slice(maximum);
  if (remainder.length === 1) visible.push(remainder[0]);
  else if (remainder.length) visible.push({ id: "space-other", name: "Other", bytes: remainder.reduce((sum, item) => sum + item.bytes, 0), files: remainder.reduce((sum, item) => sum + item.files, 0), color: "#a3aab6", groups: remainder.flatMap(item => item.groups) });
  return visible.map(item => ({ ...item, percent: item.bytes / total * 100 }));
}
