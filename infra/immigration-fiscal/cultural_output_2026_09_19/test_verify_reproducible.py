"""A failed producer must never receive a stale-output reproducibility pass."""
from pathlib import Path
import os
import shutil
import subprocess
import tempfile
import unittest


class VerifyReproducibleTests(unittest.TestCase):
    def test_failed_snapshot_stops_before_producers_or_a_stale_pass(self):
        for failed_command in ("rm", "cp"):
            with self.subTest(command=failed_command), tempfile.TemporaryDirectory(prefix="cultural-snapshot-") as directory:
                root = Path(directory)
                lane = root / "lane"
                for relative in ("scripts", "logs", "derived", "_cache/osm"):
                    (lane / relative).mkdir(parents=True)
                (root / "acquire").mkdir()
                (root / "acquire/config.local.env").write_text("")
                (lane / "derived/control.csv").write_text("current\n")
                (lane / "_cache/osm/CA.json").write_text("{}\n")
                script = lane / "scripts/16_verify_reproducible.sh"
                shutil.copyfile(Path(__file__).parent / "scripts/16_verify_reproducible.sh", script)
                binary = root / "bin"
                binary.mkdir()
                (binary / failed_command).write_text("#!/bin/sh\nexit 19\n")
                (binary / failed_command).chmod(0o755)
                (binary / "uv").write_text("#!/bin/sh\ntouch producer-ran\nexit 0\n")
                (binary / "uv").chmod(0o755)
                result = subprocess.run(["bash", str(script)], text=True, capture_output=True,
                                        env={**os.environ, "PATH": f"{binary}{os.pathsep}{os.environ['PATH']}"})
                self.assertEqual(result.returncode, 19, result.stdout + result.stderr)
                self.assertFalse((lane / "producer-ran").exists())
                self.assertNotIn("REPRODUCIBLE:", result.stdout)
                self.assertFalse((lane / "derived/reproduction_check.txt").exists())

    def test_failed_producer_stops_before_comparing_old_outputs(self):
        with tempfile.TemporaryDirectory(prefix="cultural-verifier-") as directory:
            root = Path(directory)
            lane = root / "lane"
            for relative in ("scripts", "logs", "derived", "_cache/osm"):
                (lane / relative).mkdir(parents=True)
            (root / "acquire").mkdir()
            (root / "acquire/config.local.env").write_text("")
            (lane / "derived/control.csv").write_text("unchanged\n")
            (lane / "_cache/osm/CA.json").write_text("{}\n")
            script = lane / "scripts/16_verify_reproducible.sh"
            shutil.copyfile(Path(__file__).parent / "scripts/16_verify_reproducible.sh", script)
            binary = root / "bin"
            binary.mkdir()
            (binary / "uv").write_text("#!/bin/sh\nexit 17\n")
            (binary / "uv").chmod(0o755)
            result = subprocess.run(["bash", str(script)], text=True, capture_output=True,
                                    env={**os.environ, "PATH": f"{binary}{os.pathsep}{os.environ['PATH']}"})
            self.assertEqual(result.returncode, 17, result.stdout + result.stderr)
            self.assertIn("FAIL 01_build_pums_parquet", result.stdout)
            self.assertNotIn("REPRODUCIBLE:", result.stdout)
            self.assertFalse((lane / "derived/reproduction_check.txt").exists())


if __name__ == "__main__":
    unittest.main()
