import { Sparkles } from "lucide-react";
import { Button } from "./ui/button";

export function PluginFindings({ onReview }: { onReview: (scope?: string) => void }) {
  return <section className="panel agent-space-invitation"><div><h2>Let your agent find room.</h2><p>It checks actual locations and owning-app methods, then shows a plan for your approval.</p></div><Button className="big-button" onClick={() => onReview()}><Sparkles/>Find space to free</Button></section>;
}
