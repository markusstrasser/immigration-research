"""Failure-path checks: a broken or timed-out trial must retain its evidence."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

import duckdb

from diagnose import worker as profile_worker
from trial import compatible, controls, run_worker, save, worker


class GuardTests(unittest.TestCase):
    def test_comparator_rejects_missing_rows_and_schema_type_change(self):
        controls()
        self.assertFalse(compatible([[1], [2]], [[1]]))
        self.assertFalse(compatible({"schema": [["n", "BIGINT"]]},
                                    {"schema": [["n", "DOUBLE"]]}))

    def test_failed_sql_is_recorded_and_cannot_return_success(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            db = path / "input.duckdb"
            with duckdb.connect(str(db)) as con:
                con.execute("CREATE TABLE source AS SELECT 42 AS n")
            before = db.read_bytes()
            manifest = path / "manifest.json"
            save(manifest, dict(cases=[dict(name="bad", db=str(db),
                sql="SELECT nonexistent FROM source", attach=[]),
                dict(name="good", db=str(db), sql="SELECT * FROM source", attach=[])]))
            out = path / "result.json"
            with self.assertRaises(SystemExit) as raised:
                worker(manifest, out, duckdb.__version__)
            self.assertEqual(raised.exception.code, 2)
            result = json.loads(out.read_text())
            self.assertIn("error", result["cases"][0])
            self.assertEqual(result["cases"][1]["executions"][0]["output"][0]["rows"], [[42]])
            self.assertEqual(db.read_bytes(), before)

    def test_timeout_and_nonzero_exit_keep_output(self):
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory) / "worker.json"
            with self.assertRaises(RuntimeError):
                run_worker([sys.executable, "-c", "import sys; "
                    "print('broken', file=sys.stderr, flush=True); sys.exit(2)"], out)
            self.assertIn("broken", out.with_suffix(".stderr").read_text())
            with self.assertRaises(RuntimeError):
                run_worker([sys.executable, "-c", "import time; "
                    "print('started', flush=True); time.sleep(10)"], out, timeout=0.5)
            self.assertIn("started", out.with_suffix(".stdout").read_text())

    def test_json_profile_can_be_written_on_baseline(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            manifest = path / "manifest.json"
            save(manifest, dict(cases=[dict(name="probe", db=None,
                                            sql="SELECT 42 AS n FROM range(2)")]))
            out = path / "profiles.json"
            profile_worker(manifest, out, "baseline", profile_only=True)
            result = json.loads(out.read_text())
            profile = json.loads(Path(result["cases"][0]["profile"]).read_text())
            self.assertEqual(profile["rows_returned"], 2)


if __name__ == "__main__":
    unittest.main()
