import type { AssistantTurn } from "@/lib/assistant";
import { sourceUrl } from "@/lib/assistant";

export function AssistantConversation({turns,focused=false}:{turns:AssistantTurn[];focused?:boolean}){
  if(!turns.length)return null;
  const visible=focused?turns.slice(-1):turns;
  return <section className="assistant-conversation" aria-label="Agent conversation" aria-live="polite" aria-relevant="additions">
    {visible.map(turn=><article key={turn.id} className="assistant-turn"><p className="assistant-question">{turn.question}</p><div className="assistant-answer">{turn.reply.answer}</div>
      {turn.reply.sources.length>0&&<ul className="assistant-sources" aria-label="Answer sources">{turn.reply.sources.flatMap(raw=>{const url=sourceUrl(raw);return url?[<li key={url}><a href={url} target="_blank" rel="noopener noreferrer">{new URL(url).hostname}</a></li>]:[];})}</ul>}
      {turn.reply.features.length>0&&<div className="assistant-features"><strong>I can also help with</strong><ul>{turn.reply.features.map(feature=><li key={feature}>{feature}</li>)}</ul></div>}
    </article>)}
  </section>;
}
