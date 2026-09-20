"""Reject staged error pages through the same functions used for acquisition."""

from pathlib import Path
import os
import subprocess
import tempfile
import unittest
import zipfile


ACQUIRE = Path(__file__).resolve().parents[1] / "acquire"
SCRIPTS = ("setup.sh", "setup-lifetime.sh", "setup-net-negative.sh",
           "setup-crime-frontier.sh", "setup-urban-housing.sh")


class AcquireValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.valid_zip = self.root / "valid.zip"
        with zipfile.ZipFile(self.valid_zip, "w") as archive:
            archive.writestr("data.csv", "x" * 30000)

    def validate(self, path, intended):
        return subprocess.run(
            ["bash", "-c", 'source "$1/validation.sh"; '
             'if immigration_fiscal_validate_file "$2" 1 "$3"; then exit 0; else exit 1; fi',
             "test", str(ACQUIRE), str(path), str(intended)],
            capture_output=True, text=True, check=False,
        )

    def test_format_checks_fail_in_conditional_and_preserve_input(self):
        for suffix in (".zip", ".xlsx", ".pdf", ".json"):
            for staged in (False, True):
                with self.subTest(suffix=suffix, staged=staged):
                    intended = self.root / ("bad" + suffix)
                    path = Path(str(intended) + (".part" if staged else ""))
                    payload = b"<html>blocked</html>" * 2000
                    path.write_bytes(payload)
                    result = self.validate(path, intended)
                    self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                    self.assertIn("INVALID", result.stderr)
                    self.assertEqual(path.read_bytes(), payload)

    def test_valid_formats_and_truncated_zip(self):
        for suffix, payload in ((".zip", self.valid_zip.read_bytes()),
                                (".xlsx", self.valid_zip.read_bytes()),
                                (".pdf", b"%PDF-1.4\n"), (".json", b'{"ok":true}')):
            path = self.root / ("payload" + suffix + ".part")
            path.write_bytes(payload)
            self.assertEqual(self.validate(path, path).returncode, 0)
        path = self.root / "truncated.zip.part"
        path.write_bytes(self.valid_zip.read_bytes()[:-30])
        self.assertEqual(self.validate(path, path).returncode, 1)

    def test_fetch_functions_reject_staged_html_and_accept_valid_zip(self):
        # Load only function definitions; no setup top-level code or network executes.
        command = '''
source "$1/validation.sh"
source <(sed -n '/^_validate_file()/,/^}/p; /^_fetch()/,/^}/p' "$1/$2")
_head_ok() { return 0; }
_log() { :; }; _ok() { :; }; _warn() { :; }; _fail() { :; }
curl() { while [[ "$1" != -o ]]; do shift; done; cp "$FIXTURE" "$2"; }
_fetch ignored "$3"
'''
        html = self.root / "blocked.html"
        html.write_text("<html>blocked</html>" * 2000)
        for script in SCRIPTS:
            for fixture in (html, self.valid_zip):
                with self.subTest(script=script, fixture=fixture.name):
                    dest = self.root / (script + fixture.name + ".zip")
                    result = subprocess.run(
                        ["bash", "-c", command, "test", str(ACQUIRE), script, str(dest)],
                        env={**os.environ, "FIXTURE": str(fixture)},
                        capture_output=True, text=True, check=False,
                    )
                    self.assertEqual(dest.exists(), fixture == self.valid_zip,
                                     result.stdout + result.stderr)
                    self.assertFalse(Path(str(dest) + ".part").exists())


if __name__ == "__main__":
    unittest.main()
