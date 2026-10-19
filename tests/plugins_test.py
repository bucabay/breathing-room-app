import copy
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

ROOT=Path(__file__).parents[1]/"scripts/cleanup"
sys.path.insert(0,str(ROOT))
import cleanup as core
import plugins

class PluginTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.home=Path(self.temp.name).resolve()
    def tearDown(self):self.temp.cleanup()
    def rule(self,id="test-cache"):
        rule=copy.deepcopy(core.RULES["cypress"])
        rule.update(id=id,patterns=["Library/Caches/Test"],kind="review",adapter="inspect-only.py",minAgeDays=0,
                    plugin={"handler":"paths","root":"home","timeoutSeconds":2,"maxItems":4})
        return rule
    def catalog(self,rules):
        catalog=copy.deepcopy(core.CATALOG);catalog["rules"]=rules;return catalog
    def fixture(self):
        path=self.home/"Library/Caches/Test";path.mkdir(parents=True);(path/"bytes").write_bytes(b"x"*8192);return path
    def test_catalog_has_100_distinct_plugin_areas(self):
        self.assertEqual(len(core.CATALOG["rules"]),100)
        self.assertEqual(len({r["id"] for r in core.CATALOG["rules"]}),100)
        for rule in core.CATALOG["rules"]:
            manifest=plugins.definition(rule)
            self.assertIn(manifest["handler"],plugins.REGISTRY)
            self.assertTrue(2<=manifest["timeoutSeconds"]<=20)
            self.assertTrue(1<=manifest["maxItems"]<=50)
        core.validate_catalog(core.CATALOG)
    def test_parallel_runner_preserves_success_and_absent_status(self):
        self.fixture();other=self.rule("absent");other["patterns"]=["Library/Caches/Absent"]
        result=plugins.run(self.home,self.catalog([self.rule(),other]),budget=10)
        self.assertEqual({p["status"] for p in result["plugins"]},{"complete","not-found"})
        self.assertEqual(len(result["candidates"]),1)
        self.assertGreater(result["candidates"][0]["bytes"],0)
    def test_unknown_handler_failure_does_not_hide_other_plugin(self):
        self.fixture();broken=self.rule("broken");broken["plugin"]["handler"]="unsupported"
        result=plugins.run(self.home,self.catalog([self.rule(),broken]),budget=10)
        self.assertEqual(len(result["candidates"]),1)
        self.assertIn("error",[p["status"] for p in result["plugins"]])
    def test_sizing_does_not_require_a_full_deletion_manifest(self):
        path=self.fixture();rule=self.rule();ctx=plugins.Context(self.home,rule,plugins.definition(rule),time.monotonic()+5,[])
        item=plugins.PathsPlugin().list(path,ctx)
        self.assertGreater(item["bytes"],0);self.assertTrue(item["sizeComplete"]);self.assertFalse(item["executable"])
    def test_overlap_is_explicit_and_parent_summary_is_not_hidden(self):
        parent={"path":"/Users/test/Library/App","pluginId":"app-support","bytes":1000}
        child={"path":"/Users/test/Library/App/Cache","pluginId":"cache","bytes":500}
        result=plugins.deduplicate([parent,child])
        self.assertEqual(len(result),2);self.assertTrue(all(r["overlaps"] for r in result))
    def test_cancel_stops_active_workers_and_preserves_progress(self):
        cancel=self.home/"cancel";progress=self.home/"progress.json"
        class Child:
            def __init__(self,*args,**kwargs):self.pid=99999;self.stdin=io.BytesIO();self.stopped=False
            def poll(self):return None
            def wait(self):self.stopped=True
        killed=[]
        timer=threading.Timer(.25,lambda:cancel.write_text("stop"));timer.start()
        try:
            with patch.object(plugins.subprocess,"Popen",Child),patch.object(plugins.os,"killpg",side_effect=lambda pid,sig:killed.append(pid)):
                result=plugins.run(self.home,self.catalog([self.rule()]),budget=10,progress=progress,cancel=cancel)
            self.assertTrue(result["cancelled"]);self.assertTrue(killed)
            self.assertFalse(json.loads(progress.read_text())["running"])
        finally:timer.join()
    def test_worker_timeout_is_reported_and_killed(self):
        class Child:
            def __init__(self,*args,**kwargs):self.pid=99999;self.stdin=io.BytesIO()
            def poll(self):return None
            def wait(self):pass
        with patch.object(plugins.subprocess,"Popen",Child),patch.object(plugins.os,"killpg") as kill:
            result=plugins.run(self.home,self.catalog([self.rule()]),budget=6)
            self.assertEqual(result["plugins"][0]["status"],"timeout");kill.assert_called()
    def test_cancel_token_interrupts_blocking_assessment(self):
        cancel=self.home/"assessment-cancel"
        timer=threading.Timer(.15,lambda:cancel.write_text("stop"));timer.start()
        start=time.monotonic()
        try:
            with self.assertRaises(core.DiscoveryStopped),core.cancellation_watch(cancel):time.sleep(3)
            self.assertLess(time.monotonic()-start,1)
        finally:timer.join()
    def test_plugin_interface_refuses_unknown_unapproved_delete(self):
        with self.assertRaises(ValueError):plugins.delete({"ruleId":"unknown","pluginId":"unknown"},self.home)
    def test_supported_plugin_delete_moves_only_selected_fixture_to_trash(self):
        path=self.home/"Library/Caches/Cypress";path.mkdir(parents=True);(path/"cache.bin").write_bytes(b"fixture"*1024)
        old=time.time()-40*86400;os.utime(path/"cache.bin",(old,old));os.utime(path,(old,old))
        rule=core.RULES["cypress"];ctx=plugins.Context(self.home,rule,plugins.definition(rule),time.monotonic()+10,[])
        item=plugins.PathsPlugin().list(path,ctx);self.assertTrue(item["executable"]);item["judgment"]={"model":"fixture"}
        with patch.object(core,"busy_check"):
            result=plugins.delete(item,self.home)
        self.assertIn("Trash",result);self.assertFalse(path.exists());self.assertEqual(len(list((self.home/".Trash").iterdir())),1)
    def test_simulator_plugin_refuses_booted_runtime_without_deleting(self):
        rule=core.RULES["simulator-runtimes"];ctx=plugins.Context(self.home,rule,plugins.definition(rule),time.monotonic()+20,[])
        uuid="8EAE4CCB-3D30-4D12-9381-D89ECF98451F"
        runtime={"identifier":uuid,"deletable":True,"state":"Ready","path":"/System/runtime.dmg","runtimeIdentifier":"iOS-test"}
        finding={"pluginId":"simulator-runtimes","judgment":{"purpose":"generated"},"runtimeUuid":uuid,"runtimeImagePath":runtime["path"],"runtimeIdentity":"iOS-test"}
        class Result:returncode=0;stdout=json.dumps({"devices":{"iOS-test":[{"state":"Booted"}]}}).encode()
        plugin=plugins.SimulatorPlugin()
        with patch.object(plugin,"discover",return_value=[runtime]),patch.object(plugins,"bounded_command",return_value=Result()) as command:
            with self.assertRaises(ValueError):plugin.delete(finding,ctx)
            self.assertEqual(command.call_count,1)

if __name__=="__main__":unittest.main()
