import test from "node:test";
import assert from "node:assert/strict";
import { assistantHistory, sourceUrl } from "../src/lib/assistant.ts";
import type { AssistantTurn } from "../src/lib/assistant.ts";
test("conversation history is bounded and retains question/answer order",()=>{
  const turns:AssistantTurn[]=Array.from({length:10},(_,index)=>({id:String(index),question:`Question ${index}`,reply:{answer:`Answer ${index}`,features:[],sources:[]}}));
  const history=assistantHistory(turns);assert.equal(history.length,8);assert.deepEqual(history[0],{role:"user",content:"Question 6"});assert.deepEqual(history.at(-1),{role:"assistant",content:"Answer 9"});
});
test("source links cannot execute scripts, disclose credentials or use local file URLs",()=>{
  for(const url of ["javascript:alert(1)","file:///Users/example/secret","http://example.org","https://user:pass@example.org/"])assert.equal(sourceUrl(url),null);
  assert.equal(sourceUrl("https://example.org/docs"),"https://example.org/docs");
});
