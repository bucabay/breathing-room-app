import test from "node:test";
import assert from "node:assert/strict";
import { agentOperationBlocked, blocksAgent } from "../src/lib/maintenance.ts";

test("disk map refresh and first mapping never gate the agent", () => {
  for (const title of ["Refreshing disk map", "Mapping your whole disk"]) {
    assert.equal(blocksAgent({title,page:"space"}), false);
    assert.equal(agentOperationBlocked({title,page:"space",blocksAgent:false}), false);
  }
});
test("background mapping cannot hide another blocking maintenance action", () => {
  const map={title:"Refreshing disk map",page:"space",blocksAgent:false};
  assert.equal(agentOperationBlocked(map,false,true),true);
  assert.equal(agentOperationBlocked(map,true,false),true);
  assert.equal(blocksAgent({title:"Cleaning cache",page:"assistant"}),true);
  assert.equal(blocksAgent({title:"Refreshing disk map",page:"space",blocksAgent:true}),true);
  assert.equal(agentOperationBlocked(null),false);
});
