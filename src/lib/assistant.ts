export interface AssistantMessage { role:"user"|"assistant"; content:string }
export interface AssistantReply { answer:string; features:string[]; sources:string[]; runId?:string }
export interface AssistantTurn { id:string; question:string; reply:AssistantReply }
export function assistantHistory(turns:AssistantTurn[]):AssistantMessage[]{
  return turns.flatMap(turn=>[{role:"user" as const,content:turn.question},{role:"assistant" as const,content:turn.reply.answer}]).slice(-8).map(message=>({...message,content:message.content.slice(0,6000)}));
}
export function sourceUrl(raw:string):string|null{try{const url=new URL(raw);return url.protocol==="https:"&&!url.username&&!url.password?url.toString():null;}catch{return null;}}
