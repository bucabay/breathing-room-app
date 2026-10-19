import importlib.util
from pathlib import Path
import tempfile
import subprocess
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("space", Path(__file__).parents[1] / "scripts/cleanup/space.py")
s = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s)

class SpaceTest(unittest.TestCase):
    def test_volume_accounting_includes_system_volumes_without_double_counting(self):
        with tempfile.TemporaryDirectory() as temp:
            data = Path(temp)
            (data / "Users/user/Documents").mkdir(parents=True)
            (data / "Users/user/Documents/video.mov").write_bytes(b"fixture")
            du = "\n".join(f"{n}\t{data}{p}" for n, p in [(600, "/Users/user/Documents"), (600, "/Users/user"), (600, "/Users"), (600, "")]).encode()
            class Process:
                def communicate(self, timeout): return du, b""
            info = {"APFSContainerReference": "disk3", "DeviceIdentifier": "disk3s5"}
            apfs = {"Containers": [{"ContainerReference": "disk3", "CapacityCeiling": 1000*1024, "CapacityFree": 100*1024,
                    "Volumes": [{"DeviceIdentifier": "disk3s5", "Name": "Data", "CapacityInUse": 700*1024},
                                {"DeviceIdentifier": "disk3s1", "Name": "System", "CapacityInUse": 50*1024},
                                {"DeviceIdentifier": "disk3s2", "Name": "Preboot", "CapacityInUse": 50*1024}]}]}
            df = "Filesystem blocks used available capacity iused ifree use mounted\nsystem 1000 50 100 50% 0 0 0 /\ndata 1000 700 100 50% 0 0 0 /Data\n"
            def output(argv, **kwargs):
                if argv[0] == "/bin/df": return df
                raise AssertionError("disk metadata should use mocked disk_info")
            with patch.object(s, "DATA", data), patch.object(s, "sample_large_files", return_value=([], 0, False)), patch.object(s, "disk_info", side_effect=lambda argv: apfs if "apfs" in argv else info), patch.object(s.subprocess, "check_output", side_effect=output), patch.object(s.subprocess, "Popen", return_value=Process()):
                result = s.run()
            self.assertEqual(result["identifiedBytes"], 700*1024)
            self.assertEqual(result["unmappedBytes"], 200*1024)
            self.assertEqual(sum(g["bytes"] for g in result["groups"]), result["usedBytes"])
            self.assertAlmostEqual(result["coveragePercent"], 700/900*100)
            self.assertFalse(result["partial"])

    def test_blocked_large_file_worker_is_stopped_and_partial_findings_retained(self):
        class Worker:
            killed = False
            def communicate(self, **kwargs):
                if not self.killed:
                    raise subprocess.TimeoutExpired("fixture-worker", 15)
                return b'{"checked":1000}\n{"path":"/fixture/large.bin","bytes":200000000,"identity":"","removable":false}\n', None
            def kill(self): self.killed = True
        worker = Worker()
        with patch.object(s.subprocess, "Popen", return_value=worker):
            files, checked, timed_out = s.sample_large_files(["/fixture"])
        self.assertTrue(worker.killed)
        self.assertTrue(timed_out)
        self.assertEqual(checked, 1000)
        self.assertEqual(files[0]["bytes"], 200000000)

if __name__ == "__main__": unittest.main()
