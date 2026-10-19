import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { stripeCheckoutUrl } from "../src/lib/ai-care.ts";

test("AI care checkout accepts only real HTTPS Stripe-hosted links",()=>{
  assert.equal(stripeCheckoutUrl("https://buy.stripe.com/fixture"),"https://buy.stripe.com/fixture");
  assert.equal(stripeCheckoutUrl("https://checkout.stripe.com/c/pay/fixture"),"https://checkout.stripe.com/c/pay/fixture");
  for(const url of [null,"","javascript:alert(1)","http://buy.stripe.com/fixture","https://buy.stripe.com.evil.test/fixture","https://user:password@buy.stripe.com/fixture","https://buy.stripe.com:8443/fixture","https://buy.stripe.com/"])assert.equal(stripeCheckoutUrl(url),null);
});
test("AI care explains three concrete benefits over manual cleanup without overstating automation",()=>{
  const app=readFileSync(new URL("../src/App.tsx",import.meta.url),"utf8");
  const modal=app.slice(app.indexOf('<Dialog open={aiOpen}'),app.indexOf('<Dialog open={confirmation'));
  assert.match(modal,/<DialogTitle>Automatic daily cleanup<\/DialogTitle>/);
  assert.doesNotMatch(modal,/Automatic daily cleanup, at a time you choose/);
  for(const benefit of ["No need to remember to run cleanup","Find new cleanup opportunities","See where disk space is going"])assert.ok(modal.includes(benefit));
  const benefits=modal.slice(modal.indexOf('<ul className="ai-care-benefits">'),modal.indexOf('</ul>'));
  assert.equal((benefits.match(/<li>/g)||[]).length,3);
  for(const constraint of ["already approved","New locations wait for your approval","while Breathing Room is open","may run later"])assert.ok(modal.includes(constraint));
  assert.doesNotMatch(modal,/Care with a little context|usual scan misses|runs even when|guaranteed/);
});
test("AI care modal sells only AI care, not another app purchase or local findings",()=>{
  const app=readFileSync(new URL("../src/App.tsx",import.meta.url),"utf8");
  const modal=app.slice(app.indexOf('<Dialog open={aiOpen}'),app.indexOf('<Dialog open={!!confirmation}'));
  assert.ok(modal.includes("Subscribe to AI care"));assert.ok(modal.includes("Daily care"));
  for(const old of ["Your local findings","Buy the app once","One-time purchase","Proposed monthly plan","introductory AI credit"])assert.equal(modal.includes(old),false);
});
test("AI care has larger readable copy without changing typography in other dialogs",()=>{
  const css=readFileSync(new URL("../src/index.css",import.meta.url),"utf8");
  assert.match(css,/\.room-dialog\.ai-dialog\s*\{[^}]*580px/);
  assert.match(css,/\.ai-dialog \.ai-care-intro\s*\{[^}]*font-size:15px/);
  assert.match(css,/\.ai-care-benefits strong\s*\{[^}]*font-size:\s*15px/);
  assert.match(css,/\.ai-care-benefits p\s*\{[^}]*font-size:\s*14px/);
  assert.match(css,/\.ai-dialog \.ai-care-schedule-note\s*\{[^}]*font-size:13px/);
});
test("AI care offers the approved monthly and yearly subscriptions, never the app purchase",()=>{
  const app=readFileSync(new URL("../src/App.tsx",import.meta.url),"utf8");
  const modal=app.slice(app.indexOf('<Dialog open={aiOpen}'),app.indexOf('<Dialog open={!!confirmation}'));
  assert.match(modal,/Monthly · \$5/);assert.match(modal,/Yearly · \$50/);assert.match(modal,/liveCheckoutEnabled/);
  const native=readFileSync(new URL("../src-tauri/src/lib.rs",import.meta.url),"utf8");
  assert.match(native,/remote_agent::billing_checkout\(plan\)/);
});
