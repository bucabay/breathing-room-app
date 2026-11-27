import type { RestartSpace } from "./model";

// A restart is the only supported way to release swap. Recommend it once swap
// in use (or the swap files macOS is holding) crosses this level.
export const SWAP_RESTART_THRESHOLD_BYTES = 2 * 1024 ** 3;

export function restartRecommended(data: RestartSpace | null): boolean {
  if (!data) return false;
  return (data.swap.usedBytes ?? 0) >= SWAP_RESTART_THRESHOLD_BYTES || data.swapFileBytes >= SWAP_RESTART_THRESHOLD_BYTES;
}
