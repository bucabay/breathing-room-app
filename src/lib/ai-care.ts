// Public Stripe Payment Link only. Never put Stripe API keys in the desktop app.
export type AiCareBillingStatus = { mode:"live"|"test";active:boolean;subscriptions?:{subscription:string;status:string;active:boolean;cancelAtPeriodEnd:boolean;periodEnd:number;priceId:string|null}[] };
export type CleanupQuota = { plan:"free"|"ai_care"; limit:number; used:number; remaining:number; period:string; resetsAt:number };
export const previewQuota: CleanupQuota = { plan:"free", limit:4, used:0, remaining:4, period:"", resetsAt:0 };
export function stripeCheckoutUrl(value: unknown): string | null {
  if (typeof value !== "string" || !value.trim()) return null;
  try {
    const url = new URL(value);
    if (url.protocol !== "https:" || !["buy.stripe.com", "checkout.stripe.com"].includes(url.hostname) || url.username || url.password || url.port || url.pathname === "/") return null;
    return url.href;
  } catch { return null; }
}
