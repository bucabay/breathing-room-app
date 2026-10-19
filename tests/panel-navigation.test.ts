import { test } from "node:test";
import assert from "node:assert/strict";
import { panelNavigationFromUrl, panelNavigationUrl, type PanelNavigation } from "../src/lib/panel-navigation.ts";

test("panel destinations preserve selected app, event and filter context",()=>{
  const destinations:PanelNavigation[]=[
    {page:"apps",search:"Visual Studio Code",appId:"/Applications/Visual Studio Code.app"},
    {page:"space"},
    {page:"activity",section:"writers",search:"Chrome"},
    {page:"activity",filter:"files",eventId:7,search:"/Users/test/Downloads/file & notes.txt",section:"feed"},
    {page:"activity",settings:true},
  ];
  for(const destination of destinations)assert.deepEqual(panelNavigationFromUrl(new URL(panelNavigationUrl(destination),"http://localhost").search),destination);
});
test("invalid routes, filters and event identities cannot be selected by a panel link",()=>{
  assert.equal(panelNavigationFromUrl("?page=unknown"),null);
  assert.deepEqual(panelNavigationFromUrl("?page=activity&filter=unknown&section=unknown&eventId=-1"),{page:"activity"});
  assert.deepEqual(panelNavigationFromUrl("?page=activity&eventId=3.5"),{page:"activity"});
});
