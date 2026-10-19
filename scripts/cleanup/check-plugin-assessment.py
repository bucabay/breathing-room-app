#!/usr/bin/env python3
"""Explicit live assessment of previously discovered metadata; never deletes data."""
import json
import cleanup as core
import plugins

home=core.home_dir()
path=core.store_dir(home).parent/"plugin-findings.json"
plan=json.loads(path.read_text())
if plan.get("catalogFingerprint")!=core.fingerprint(core.load_catalog(home)):
    raise SystemExit("Run plugin discovery first; the catalog changed.")
core.assess(plan,"Rank cleanup opportunities. Preserve unique recordings, profiles, source and mixed app data; explain regeneration/reinstallation impact through typed judgments.",home)
for candidate in plan["candidates"]:
    if not candidate.get("judgment"):candidate["executable"]=False
plan=core.save_plan(plan,home)
plugins.atomic(path,plan)
print(json.dumps({"mode":plan["mode"],"usage":plan.get("usage"),"assessed":[
    {"name":c["name"],"bytes":c["bytes"],"impact":c["impactLevel"],"executable":c["executable"],"judgment":c["judgment"]}
    for c in plan["candidates"] if c.get("judgment")
]},indent=2))
