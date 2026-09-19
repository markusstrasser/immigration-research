"""Regression: derived verification skipped every build/compose manifest row."""

import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
HEADER = "stage\trequired\trelpath\tmin_bytes\tscript\tnotes\n"


class VerifyDownloadsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for relative in ("scripts/verify-downloads.sh", "acquire/lib.sh",
                         "acquire/config.env.example"):
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, target)
        self.data = self.root / "data"
        self.derived = self.root / "outputs"
        self.data.mkdir()
        self.derived.mkdir()
        self.manifest = self.root / "DOWNLOAD_MANIFEST.tsv"
        self.manifest.write_text(
            HEADER
            + "1\trequired\traw.zip\t4\tacquire\ttest\n"
            + "2\toptional\textra.zip\t4\tacquire\ttest\n"
            + "3\trequired\tderived/built.csv\t4\tbuild\ttest\n"
            + "4\toptional\tcomposed.csv\t4\tcompose\ttest\n"
        )

    def run_tier(self, tier):
        return subprocess.run(
            ["bash", str(self.root / "scripts/verify-downloads.sh"), "--tier", tier],
            env={**os.environ, "IMMIGRATION_DATA_ROOT": str(self.data),
                 "IMMIGRATION_DERIVED_ROOT": str(self.derived)},
            capture_output=True, text=True, check=False,
        )

    def test_derived_requires_both_build_and_compose_outputs(self):
        missing = self.run_tier("derived")
        self.assertEqual(missing.returncode, 1, missing.stdout + missing.stderr)
        self.assertIn("checked 2", missing.stdout)
        self.assertIn("built.csv", missing.stdout)
        self.assertIn("composed.csv", missing.stdout)
        (self.derived / "built.csv").write_text("valid")
        (self.derived / "composed.csv").write_text("x")
        small = self.run_tier("derived")
        self.assertEqual(small.returncode, 1, small.stdout + small.stderr)
        self.assertIn("TOO_SMALL", small.stdout)
        (self.derived / "composed.csv").write_text("valid")
        complete = self.run_tier("derived")
        self.assertEqual(complete.returncode, 0, complete.stdout + complete.stderr)

    def test_raw_tiers_do_not_require_derived_outputs(self):
        (self.data / "raw.zip").write_text("valid")
        required = self.run_tier("required")
        self.assertEqual(required.returncode, 0, required.stdout + required.stderr)
        self.assertIn("checked 1", required.stdout)
        self.assertEqual(self.run_tier("optional").returncode, 1)
        (self.data / "extra.zip").write_text("valid")
        self.assertEqual(self.run_tier("optional").returncode, 0)

    def test_no_selected_rows_cannot_pass(self):
        self.manifest.write_text(HEADER + "1\trequired\traw.zip\t4\tacquire\ttest\n")
        self.assertNotEqual(self.run_tier("derived").returncode, 0)

    def test_invalid_tier_rejected_even_with_empty_manifest(self):
        self.manifest.write_text(HEADER)
        result = self.run_tier("typo")
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
