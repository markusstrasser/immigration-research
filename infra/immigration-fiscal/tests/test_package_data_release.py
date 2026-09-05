"""The observed --help regression must never invoke a release write.

Native-First: exercise argparse with a mocked builder, without staging data.
"""
from contextlib import redirect_stderr, redirect_stdout
import io
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "build"))
import package_data_release


class PackageArgumentTests(unittest.TestCase):
    def test_help_does_not_build(self):
        output = io.StringIO()
        with patch.object(package_data_release, "build") as build, redirect_stdout(output):
            with self.assertRaises(SystemExit) as stopped:
                package_data_release.main(["--help"])
        self.assertEqual(stopped.exception.code, 0)
        self.assertIn("usage:", output.getvalue())
        build.assert_not_called()

    def test_invalid_arguments_do_not_build(self):
        for arguments in (["../escape"], ["a/b"], [""], ["--unknown"], ["v1", "extra"]):
            with self.subTest(arguments=arguments):
                with patch.object(package_data_release, "build") as build, redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit) as stopped:
                        package_data_release.main(arguments)
                self.assertEqual(stopped.exception.code, 2)
                build.assert_not_called()

    def test_explicit_version_reaches_builder(self):
        with patch.object(package_data_release, "build") as build:
            package_data_release.main(["2026-09-05"])
        build.assert_called_once_with("2026-09-05")


if __name__ == "__main__":
    unittest.main()
