"""Cleanup tests operate only on temporary owned fixtures, never user data."""
import copy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time
import unittest
import io
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location("cleanup", Path(__file__).parents[1] / "scripts/cleanup/cleanup.py")
c = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(c)


class CleanupTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.home = Path(self.temp.name).resolve()
        def plan_batch(payload=None, status=False):
            if payload and payload.get("operation") == "cleanup-batch":
                return {"actions": [{"id": row["id"], "action": "method" if row["methods"] else "approval", "methodId": row["methods"][0]["id"] if row["methods"] else "", "detail": "Fixture bulk plan"} for row in payload["locations"]], "telemetry": {"requestCount": 1, "batchCount": 1}}
            raise ValueError("No real inference in fixture tests")
        self.ai_patch = patch.object(c, "agent_call", side_effect=plan_batch)
        self.ai_mock = self.ai_patch.start()
        self.original_tool_path = c.tool_path
        self.tool_patch = patch.object(c, "tool_path", side_effect=ValueError("Fixture tool unavailable"))
        self.tool_patch.start()

    def tearDown(self):
        self.tool_patch.stop()
        self.ai_patch.stop()
        self.temp.cleanup()

    def fixture(self, relative="Library/Caches/electron"):
        path = self.home / relative
        path.mkdir(parents=True)
        (path / "download.bin").write_bytes(b"a" * 8192)
        old = time.time() - 40 * 86400
        os.utime(path / "download.bin", (old, old))
        os.utime(path, (old, old))
        rule = c.RULES["electron"]
        snap = c.snapshot(path, self.home)
        return {"id": "item", "ruleId": "electron", "path": str(path), "kind": "trash", "adapter": "trash-selected.py",
                "executable": True, "digest": snap["digest"], "minAgeDays": rule["minAgeDays"]}

    def plan(self, item):
        return c.save_plan({"expiresAt": time.time() + 60, "catalogFingerprint": c.fingerprint(c.CATALOG), "candidates": [item]}, self.home)

    def test_profile_coverage_and_schema(self):
        self.assertEqual(c.validate_catalog(c.CATALOG), c.CATALOG)
        for p in c.CATALOG["profiles"]:
            self.assertGreaterEqual(len({r["type"] for r in c.CATALOG["rules"] if p in r["profiles"]}), 10)

    def test_segment_glob_never_crosses_with_single_star(self):
        self.assertTrue(c.matches("code/**/.pytest_cache", "code/a/b/.pytest_cache"))
        self.assertTrue(c.matches("code/**/.pytest_cache", "code/.pytest_cache"))
        self.assertFalse(c.matches("Library/Caches/*", "Library/Caches/app/original"))

    def test_specific_rule_beats_fuzzy_app_cache(self):
        self.assertEqual(c.rule_for(self.home / "Library/Caches/electron", self.home)["id"], "electron")

    def test_snapshot_blocks_credentials_and_symlinks(self):
        item = self.fixture()
        path = Path(item["path"])
        (path / ".env").write_text("fixture")
        self.assertTrue(c.snapshot(path, self.home)["blocked"])
        (path / ".env").unlink()
        (path / "link").symlink_to(self.home)
        self.assertTrue(c.snapshot(path, self.home)["blocked"])

    def test_partial_inventory_cannot_be_complete(self):
        item = self.fixture()
        self.assertFalse(c.snapshot(Path(item["path"]), self.home, seconds=-1)["complete"])

    def test_changed_location_does_not_move(self):
        item = self.fixture()
        (Path(item["path"]) / "new.txt").write_text("new")
        with patch.object(c, "busy_check"):
            with self.assertRaises(ValueError):
                c.execute_item(item, self.home)
        self.assertTrue(Path(item["path"]).exists())

    def test_current_plan_trash_and_replay_rejected(self):
        item = self.fixture()
        plan = self.plan(item)
        with patch.object(c, "busy_check"):
            result = c.execute_plan(plan["planId"], ["item"], self.home)
        self.assertTrue(result["results"][0]["ok"])
        self.assertFalse(Path(item["path"]).exists())
        self.assertEqual(len(list((self.home / ".Trash").iterdir())), 1)
        with self.assertRaises(OSError):
            c.execute_plan(plan["planId"], ["item"], self.home)

    def test_unknown_id_no_mutation(self):
        item = self.fixture()
        plan = self.plan(item)
        with self.assertRaises(ValueError):
            c.execute_plan(plan["planId"], ["arbitrary"], self.home)
        self.assertTrue(Path(item["path"]).exists())

    def test_manual_approval_promotes_exact_cache_to_trash_and_invalidates_old_plan(self):
        item = self.fixture()
        item.update(executable=False, complete=True, impactLevel=3, kind="review", judgment={"model": "fixture"})
        plan = self.plan(item)
        with patch.object(c, "busy_check"):
            updated = c.approve_location(plan["planId"], "item", self.home)
            self.assertTrue(updated["candidates"][0]["userApproved"])
            self.assertEqual(updated["candidates"][0]["kind"], "trash")
            self.assertFalse((c.store_dir(self.home) / (plan["planId"] + ".json")).exists())
            result = c.execute_plan(updated["planId"], ["item"], self.home)
        self.assertTrue(result["results"][0]["ok"])

    def test_manual_approval_rejects_protected_or_changed_inventory(self):
        item = self.fixture()
        item.update(executable=False, complete=True, impactLevel=5)
        plan = self.plan(item)
        with self.assertRaises(ValueError):
            c.approve_location(plan["planId"], "item", self.home)
        item["impactLevel"] = 3
        plan = self.plan(item)
        (Path(item["path"]) / "new-file").write_text("changed")
        with patch.object(c, "busy_check"), self.assertRaises(ValueError):
            c.approve_location(plan["planId"], "item", self.home)

    def test_generic_approval_accepts_exact_app_cache_but_not_whole_app_data(self):
        item = self.fixture("Library/Application Support/Adobe/Common/Media Cache")
        item.update(ruleId="adobe-media", executable=False, complete=True, impactLevel=3, kind="review")
        with patch.object(c, "busy_check"):
            c.validate_manual(item, self.home)
            root = {**item, "path": str(self.home / "Library/Application Support/Adobe")}
            with self.assertRaisesRegex(ValueError, "owning application's controls"):
                c.validate_manual(root, self.home)

    def test_expired_plan_no_mutation(self):
        item = self.fixture()
        plan = c.save_plan({"expiresAt": time.time() - 1, "candidates": [item]}, self.home)
        with self.assertRaises(ValueError):
            c.execute_plan(plan["planId"], ["item"], self.home)

    def test_review_runs_agent_then_returns_generic_approval_without_mutation(self):
        item = self.fixture()
        item.update(executable=False, complete=True, impactLevel=3, kind="review")
        plan = self.plan(item)
        with patch.object(c, "busy_check"):
            result = c.execute_plan(plan["planId"], ["item"], self.home, agent_model="openai/fixture")
        self.ai_mock.assert_called_once()
        self.assertEqual(result["results"][0]["status"], "approval")
        self.assertTrue(Path(item["path"]).exists())
        self.assertTrue((c.store_dir(self.home) / (result["pendingPlan"]["planId"] + ".json")).exists())

    def test_agent_cannot_execute_arbitrary_generated_shell_commands(self):
        item = self.fixture()
        item.update(kind="review", executable=False, complete=True, impactLevel=3)
        plan = self.plan(item)
        with patch.object(c, "busy_check"), patch.object(c, "agent_call", return_value={"actions": [{"id": "item", "action": "method", "methodId": "rm-anything", "detail": "unsupported"}]}), patch.object(c, "command") as command:
            result = c.execute_plan(plan["planId"], ["item"], self.home)
        self.assertFalse(result["results"][0]["ok"])
        command.assert_not_called()
        self.assertTrue(Path(item["path"]).exists())

    def test_typed_preserve_decision_does_not_offer_generic_trash(self):
        item = self.fixture()
        item.update(executable=False, complete=True, impactLevel=3, kind="review")
        plan = self.plan(item)
        with patch.object(c, "supported_agent_methods", return_value=[]), patch.object(c, "agent_call", return_value={"actions": [{"id": "item", "action": "preserve", "methodId": "", "detail": "Possible unique data"}]}):
            result = c.execute_plan(plan["planId"], ["item"], self.home)
        self.assertEqual(result["results"][0]["status"], "preserved")
        self.assertNotIn("pendingPlan", result)
        self.assertTrue(Path(item["path"]).exists())

    def test_agent_resolved_cargo_cleanup_runs_only_exact_target_argv(self):
        item = self.fixture("code/project/target")
        path = Path(item["path"])
        (path.parent / "Cargo.toml").write_text('[package]\nname="fixture"\nversion="0.1.0"\n')
        argv = ["cargo", "clean", "--manifest-path", str(path.parent / "Cargo.toml"), "--target-dir", str(path)]
        item.update(ruleId="rust-build", kind="review", executable=False, complete=True, impactLevel=3)
        plan = self.plan(item)
        with patch.object(c, "busy_check"), patch.object(c, "command") as command:
            result = c.execute_plan(plan["planId"], ["item"], self.home)
        self.assertIn("Owning-tool cleanup completed", result["results"][0]["detail"])
        command.assert_called_once_with(argv, 45)

    def test_large_recent_npm_cache_uses_owning_cli_without_a_full_manifest(self):
        item = self.fixture(".npm/_cacache")
        path = Path(item["path"])
        item.update(ruleId="npm", kind="tool", executable=False, complete=False, digest="", minAgeDays=30)
        def cache_path(rule, home):
            if rule["id"] == "npm": return path
            raise ValueError("Fixture tool unavailable")
        plan = self.plan(item)
        with patch.object(c, "tool_path", side_effect=cache_path), patch.object(c, "snapshot", side_effect=AssertionError("Owning CLI must not require a delete manifest")), patch.object(c, "busy_check", side_effect=AssertionError("Owning CLI handles cache concurrency")), patch.object(c, "command") as command:
            result = c.execute_plan(plan["planId"], ["item"], self.home)
        self.assertTrue(result["results"][0]["ok"])
        command.assert_called_once_with(["npm", "cache", "clean", "--force", "--cache", str(path.parent)], 45, env=None)

    def test_owning_cache_scope_is_pinned_again_before_mutation(self):
        item = self.fixture(".npm/_cacache")
        path = Path(item["path"])
        item.update(ruleId="npm", kind="tool", executable=False, complete=False)
        plan = self.plan(item)
        calls = [0]
        def scope(rule, home):
            if rule["id"] != "npm": return None
            calls[0] += 1
            return path if calls[0] == 1 else self.home / "other-cache"
        with patch.object(c, "tool_path", side_effect=scope), patch.object(c, "command") as command:
            result = c.execute_plan(plan["planId"], ["item"], self.home)
        command.assert_not_called()
        self.assertFalse(result["results"][0]["ok"])
        self.assertIn("scope changed", result["results"][0]["detail"])

    def test_mixed_selection_uses_one_bulk_plan_and_persists_all_followups(self):
        first = self.fixture()
        second = self.fixture("Library/Caches/other")
        second.update(id="second", kind="review", executable=False, complete=True, impactLevel=3)
        plan = c.save_plan({"expiresAt": time.time()+60, "catalogFingerprint": c.fingerprint(c.CATALOG), "candidates": [first, second]}, self.home)
        with patch.object(c, "busy_check"):
            result = c.execute_plan(plan["planId"], ["item", "second"], self.home)
        self.ai_mock.assert_called_once()
        self.assertEqual(len(self.ai_mock.call_args.args[0]["locations"]), 2)
        self.assertTrue(result["results"][0]["ok"])
        self.assertEqual(result["results"][1]["status"], "approval")
        self.assertEqual(result["followupPlan"]["candidates"][0]["id"], "second")
        self.assertEqual(json.loads((c.store_dir(self.home).parent / "cleanup-last-result.json").read_text())["results"], result["results"])

    def test_same_cache_command_is_not_run_twice_for_duplicate_locations(self):
        item = self.fixture(".npm/_cacache")
        path = Path(item["path"])
        item.update(ruleId="npm", kind="tool", executable=True)
        second = {**item, "id": "second"}
        plan = c.save_plan({"expiresAt": time.time()+60, "catalogFingerprint": c.fingerprint(c.CATALOG), "candidates": [item, second]}, self.home)
        with patch.object(c, "tool_path", side_effect=lambda rule, home: path if rule["id"] == "npm" else None), patch.object(c, "command") as command:
            result = c.execute_plan(plan["planId"], ["item", "second"], self.home)
        command.assert_called_once()
        self.assertEqual(result["results"][1]["status"], "covered")

    def test_individual_retry_refreshes_changed_cache_and_keeps_aggregate_results(self):
        item = self.fixture()
        plan = self.plan(item)
        (Path(item["path"]) / "recent.bin").write_text("new cache data")
        with patch.object(c, "busy_check"):
            initial = c.execute_plan(plan["planId"], ["item"], self.home)
            self.assertFalse(initial["results"][0]["ok"])
            retry = c.execute_plan(initial["followupPlan"]["planId"], ["item"], self.home)
        self.assertTrue(retry["results"][0]["ok"])
        self.assertEqual(len(retry["results"]), 1)
        self.assertEqual(retry["ai"]["requestCount"], 2)

    def test_approving_one_location_keeps_other_approval_plan_live(self):
        first = self.fixture()
        second = self.fixture("Library/Caches/other")
        second["id"] = "second"
        for item in (first, second): item.update(executable=False, complete=True, impactLevel=3, kind="review")
        plan = c.save_plan({"expiresAt": time.time()+60, "catalogFingerprint": c.fingerprint(c.CATALOG), "candidates": [first, second]}, self.home)
        with patch.object(c, "busy_check"):
            approved = c.approve_location(plan["planId"], "item", self.home)
            result = c.execute_plan(approved["planId"], ["item"], self.home)
            pending = result["pendingPlan"]
            self.assertEqual([i["id"] for i in pending["candidates"]], ["second"])
            approved = c.approve_location(pending["planId"], "second", self.home)
            self.assertTrue(c.execute_plan(approved["planId"], ["second"], self.home)["results"][0]["ok"])

    def test_git_tracked_cache_detected(self):
        item = self.fixture("code/project/.pytest_cache")
        project = self.home / "code/project"
        subprocess.run(["git", "init", "-q", str(project)], check=True)
        subprocess.run(["git", "-C", str(project), "add", ".pytest_cache"], check=True)
        self.assertTrue(c.tracked(Path(item["path"]), self.home))

    def test_remote_cannot_add_commands_or_expand_scope(self):
        for mutation in ("command", "scope", "age"):
            data = copy.deepcopy(c.CATALOG)
            rule = next(r for r in data["rules"] if r["id"] == "electron")
            if mutation == "command":
                rule["command"] = "rm -rf /"
            elif mutation == "scope":
                rule["patterns"] = ["Library/**"]
            else:
                rule["minAgeDays"] = 0
            with self.assertRaises(ValueError):
                c.validate_catalog(data, remote=True)

    def test_remote_can_add_review_only_heuristics(self):
        data = copy.deepcopy(c.CATALOG)
        rule = copy.deepcopy(next(r for r in data["rules"] if r["kind"] == "review"))
        rule.update(id="new-cache", type="new-cache", patterns=["Library/Caches/NewApp"])
        data["rules"].append(rule)
        self.assertEqual(c.validate_catalog(data, remote=True), data)
        rule.update(kind="trash", adapter="trash-selected.py")
        with self.assertRaises(ValueError):
            c.validate_catalog(data, remote=True)

    def test_catalog_fingerprint_change_invalidates_plan(self):
        item = self.fixture()
        plan = self.plan(item)
        newer = copy.deepcopy(c.CATALOG)
        newer["version"] += 1
        with patch.object(c, "load_catalog", return_value=newer):
            with self.assertRaises(ValueError):
                c.execute_plan(plan["planId"], ["item"], self.home)

    def test_custom_npm_location_is_queried_not_assumed(self):
        root = self.home / "custom/npm"
        (root / "_cacache").mkdir(parents=True)
        with patch.object(c, "command", return_value=str(root)), patch.object(c, "tool_path", side_effect=self.original_tool_path):
            self.assertEqual(c.tool_path(c.RULES["npm"], self.home), root / "_cacache")

    def test_remote_non_https_no_request(self):
        with patch.object(c.urllib.request, "build_opener") as opener:
            with self.assertRaises(ValueError):
                c.update_catalog("http://example.org/catalog.json", self.home)
            opener.assert_not_called()

    def test_remote_atomic_install_and_downgrade_rejection(self):
        data = copy.deepcopy(c.CATALOG)
        data["version"] += 1
        class Opener:
            def open(self, url, timeout):
                return io.BytesIO(json.dumps(data).encode())
        with patch.object(c.urllib.request, "build_opener", return_value=Opener()):
            result = c.update_catalog("https://example.org/catalog.json", self.home)
            self.assertEqual(result["version"], data["version"])
            self.assertEqual(c.load_catalog(self.home), data)
            with self.assertRaises(ValueError):
                c.update_catalog("https://example.org/catalog.json", self.home)
        self.assertEqual(c.load_catalog(self.home), data)

    def test_malformed_remote_keeps_valid_cache(self):
        data = copy.deepcopy(c.CATALOG)
        data["version"] += 1
        cache = c.store_dir(self.home).parent / "catalog.json"
        cache.write_text(json.dumps(data))
        broken = copy.deepcopy(data)
        broken["rules"][0]["kind"] = ["tool"]
        class Opener:
            def open(self, url, timeout):
                return io.BytesIO(json.dumps(broken).encode())
        with patch.object(c.urllib.request, "build_opener", return_value=Opener()):
            with self.assertRaises(ValueError):
                c.update_catalog("https://example.org/catalog.json", self.home)
        self.assertEqual(c.load_catalog(self.home), data)

    def test_jev_cannot_promote_unknown_to_executable(self):
        plan = {"candidates": [{"name": "Odd folder", "path": str(self.home / "Library/Caches/odd"), "bytes": 100,
                "evidence": "heuristic", "impact": "unknown", "executable": False, "complete": True, "reason": "unknown",
                "adapter": "inspect-only.py", "impactLevel": 4, "ruleId": "unknown", "judgment": None}]}
        response = {"model": "fixture", "answers": {
            "purpose_0": {"type": "choice", "choice": "cache", "confidence": 1},
            "relevant_0": {"type": "noul", "noul": 1}, "disposable_0": {"type": "noul", "noul": 1},
            "unique_0": {"type": "noul", "noul": 0}, "method_0": {"type": "noul", "noul": 1},
            "impact_0": {"type": "score", "score": 0}}}
        with patch.object(c, "jev_request", return_value=response):
            c.assess(plan, "Find caches", self.home)
        self.assertFalse(plan["candidates"][0]["executable"])
        self.assertEqual(plan["candidates"][0]["impactLevel"], 4)


if __name__ == "__main__":
    unittest.main()
