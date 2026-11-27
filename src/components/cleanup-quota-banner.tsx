import { ArrowUpRight, Sparkles } from "lucide-react";
import { Button } from "./ui/button";
import type { CleanupQuota } from "@/lib/ai-care";

export function CleanupQuotaBanner({ quota, onOpen }: { quota: CleanupQuota; onOpen: () => void }) {
  const reset = quota.resetsAt ? new Date(quota.resetsAt * 1000).toLocaleDateString(undefined, { month: "short", day: "numeric" }) : "";
  const paid = quota.plan === "ai_care";
  return <section className="cleanup-quota-banner" role="alert" aria-live="polite" aria-label="Monthly cleanups used">
    <span className="cleanup-quota-icon"><Sparkles size={24} /></span>
    <div className="cleanup-quota-copy">
      <strong>{paid ? `You’ve used all ${quota.limit} AI Care cleanups this month.` : `You’ve used all ${quota.limit} free cleanups this month.`}</strong>
      <p>{paid
        ? `Your allowance resets${reset ? ` on ${reset}` : " next month"}. Daily care and reviewed plans resume with it.`
        : `AI Care includes 100 cleanups a month, daily care and new cleanup opportunities.${reset ? ` Your free allowance resets on ${reset}.` : ""}`}</p>
    </div>
    <Button className="big-button cleanup-quota-action" onClick={onOpen}>{paid ? "Manage AI Care" : "Get AI Care"}<ArrowUpRight size={17} /></Button>
  </section>;
}
