"""Regression: portable roots, preserved overrides, and no self-linking local layout."""
from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

INFRA = Path(__file__).resolve().parents[1]


class LocalDataLayout(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name).resolve() / 'relocated checkout'
        self.infra = self.repo / 'infra/immigration-fiscal'
        for relative in ('build/paths.py', 'acquire/lib.sh', 'acquire/config.env.example',
                         'scripts/link-data-layout.sh'):
            target = self.infra / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(INFRA / relative, target)
        spec = importlib.util.spec_from_file_location('relocated_paths', self.infra / 'build/paths.py')
        self.paths = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.paths)
        self.clean_env = {'PATH': os.environ['PATH'], 'HOME': str(self.repo / 'unused-home')}

    def shell(self, command, overrides=None):
        return subprocess.run(['bash', '-c', command], cwd=self.temp.name,
                              env=self.clean_env | (overrides or {}), text=True,
                              capture_output=True, check=False)

    def initialize(self, overrides=None):
        return self.shell('bash "$INFRA/scripts/link-data-layout.sh"',
                          {'INFRA': str(self.infra)} | (overrides or {}))

    def test_local_layout_is_repeatable_and_relative(self):
        for _ in range(2):
            result = self.initialize()
            self.assertEqual(result.returncode, 0, result.stderr)
        raw = self.repo / 'sources/immigration-fiscal/data'
        derived = raw.parent / 'derived'
        self.assertFalse(raw.is_symlink())
        self.assertFalse(derived.is_symlink())
        self.assertEqual(os.readlink(raw / 'derived'), '../derived')
        self.assertEqual((raw / 'derived').resolve(), derived)
        reused = self.repo / 'sources/reused-surveys'
        reused.mkdir()
        with mock.patch.dict(os.environ, self.clean_env, clear=True):
            self.assertEqual(self.paths.data_root(), raw)
            self.assertEqual(self.paths.derived_root(), derived)
            self.assertEqual(self.paths.corpus_root(), self.repo / 'sources/corpus')
            self.assertEqual(self.paths.reused_surveys_root(), reused)
            self.assertEqual(self.paths.microdata_duckdb_path(), derived / 'immigration_microdata.duckdb')

    def test_shell_and_python_preserve_explicit_overrides(self):
        values = {'PNY_DATA_ROOT': '/chosen/raw', 'DERIVED_ROOT': '/chosen/derived',
                  'CORPUS_ROOT': '/chosen/corpus', 'REUSED_SURVEYS_ROOT': '/chosen/surveys'}
        result = self.shell('source "$INFRA/acquire/lib.sh"; immigration_fiscal_load_config; '
                            'printf "%s\\n" "$PNY_DATA_ROOT" "$DERIVED_ROOT" "$CORPUS_ROOT" "$REUSED_SURVEYS_ROOT"',
                            values | {'INFRA': str(self.infra)})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.splitlines(), list(values.values()))
        with mock.patch.dict(os.environ, self.clean_env | values, clear=True):
            for function, key in ((self.paths.data_root, 'PNY_DATA_ROOT'),
                                  (self.paths.derived_root, 'DERIVED_ROOT'),
                                  (self.paths.corpus_root, 'CORPUS_ROOT'),
                                  (self.paths.reused_surveys_root, 'REUSED_SURVEYS_ROOT')):
                self.assertEqual(function(), Path(values[key]))

    def test_aliases_match_between_shell_and_python(self):
        values = {'IMMIGRATION_DATA_ROOT': '/alias/raw', 'IMMIGRATION_DERIVED_ROOT': '/alias/derived',
                  'IMMIGRATION_CORPUS_ROOT': '/alias/corpus'}
        result = self.shell('source "$INFRA/acquire/lib.sh"; immigration_fiscal_load_config; '
                            'printf "%s\\n" "$PNY_DATA_ROOT" "$DERIVED_ROOT" "$CORPUS_ROOT"',
                            values | {'INFRA': str(self.infra)})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.splitlines(), list(values.values()))
        with mock.patch.dict(os.environ, self.clean_env | values, clear=True):
            self.assertEqual(self.paths.data_root(), Path('/alias/raw'))
            self.assertEqual(self.paths.derived_root(), Path('/alias/derived'))
            self.assertEqual(self.paths.corpus_root(), Path('/alias/corpus'))

    def test_raw_only_override_keeps_existing_derived_tree_through_init(self):
        raw = self.repo / 'provided data'
        derived = raw / 'derived'
        derived.mkdir(parents=True)
        marker = derived / 'immigration_microdata.duckdb'
        marker.write_bytes(b'existing warehouse')
        for variable in ('PNY_DATA_ROOT', 'IMMIGRATION_DATA_ROOT'):
            with self.subTest(variable=variable):
                overrides = {variable: str(raw)}
                with mock.patch.dict(os.environ, self.clean_env | overrides, clear=True):
                    self.assertEqual(self.paths.derived_root(), derived)
                    self.assertEqual(self.paths.microdata_duckdb_path(), marker)
                shell = self.shell('source "$INFRA/acquire/lib.sh"; immigration_fiscal_load_config; '
                                   'printf "%s\\n" "$DERIVED_ROOT"',
                                   overrides | {'INFRA': str(self.infra)})
                self.assertEqual(shell.returncode, 0, shell.stderr)
                self.assertEqual(shell.stdout.strip(), str(derived))
                initialized = self.initialize(overrides)
                self.assertEqual(initialized.returncode, 0, initialized.stderr)
                self.assertEqual((self.repo / 'sources/immigration-fiscal/data').resolve(), raw)
                self.assertFalse(derived.is_symlink())
                self.assertEqual(marker.read_bytes(), b'existing warehouse')

    def test_itep_override_selects_exact_file_and_ignores_code_root(self):
        selected = self.repo / 'chosen itep.tsv'
        selected.parent.mkdir(parents=True, exist_ok=True)
        selected.write_text('selected source')
        env = self.clean_env | {'ITEP_TABLE_PATH': str(selected),
                                'IMMIGRATION_FISCAL_ROOT': '/unrelated/code',
                                'PNY_DATA_ROOT': '/different/raw'}
        with mock.patch.dict(os.environ, env, clear=True):
            self.assertEqual(self.paths.itep_table_path(), selected)
            self.assertEqual(self.paths.itep_table_path().read_text(), 'selected source')
        with mock.patch.dict(os.environ, self.clean_env | {'IMMIGRATION_FISCAL_ROOT': '/old/data-use'}, clear=True):
            self.assertEqual(self.paths.itep_table_path(),
                             self.repo / 'sources/immigration-fiscal/data/itep/itep_table_5.tsv')

    def test_conflicting_data_is_preserved(self):
        self.assertEqual(self.initialize().returncode, 0)
        marker = self.repo / 'sources/immigration-fiscal/data/keep.csv'
        marker.write_text('source bytes')
        result = self.initialize({'PNY_DATA_ROOT': str(self.repo / 'different-raw')})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('refusing to replace', result.stderr)
        self.assertEqual(marker.read_text(), 'source bytes')

    def test_missing_survey_root_is_reported(self):
        with mock.patch.dict(os.environ, self.clean_env, clear=True):
            with self.assertRaisesRegex(FileNotFoundError, 'REUSED_SURVEYS_ROOT'):
                self.paths.reused_surveys_root()

    def test_deferred_defaults_do_not_weaken_normal_root_checks(self):
        with mock.patch.dict(os.environ, self.clean_env, clear=True):
            for resolver, relative in ((self.paths.data_root, 'sources/immigration-fiscal/data'),
                                       (self.paths.derived_root, 'sources/immigration-fiscal/derived'),
                                       (self.paths.reused_surveys_root, 'sources/reused-surveys')):
                self.assertEqual(resolver(require_exists=False), self.repo / relative)
                with self.assertRaises(FileNotFoundError):
                    resolver()

    def ecls_command(self, *arguments):
        """Exercise the real parser/source check; pandas is unused before that check."""
        lane = self.infra / 'school_peer_checks_2026_09_20'
        lane.mkdir(exist_ok=True)
        for name in ('extract.py', 'sources.json'):
            shutil.copyfile(INFRA / lane.name / name, lane / name)
        modules = self.repo / 'test-modules'
        modules.mkdir(exist_ok=True)
        (modules / 'pandas.py').write_text('# Dataframe processing is outside this parser test.\n')
        return subprocess.run([sys.executable, str(lane / 'extract.py'), *arguments],
                              env=self.clean_env | {'PYTHONPATH': str(modules)},
                              text=True, capture_output=True, check=False)

    def test_cli_help_does_not_require_unused_default_source(self):
        result = self.ecls_command('--help')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('--source-dir', result.stdout)
        self.assertFalse((self.repo / 'sources').exists())

    def test_explicit_source_reaches_its_validation_without_default_root(self):
        source = self.repo / 'explicit source'
        source.mkdir()
        (source / 'ECLSK_Kto8_child_STATA.dct').write_text('deliberately wrong release')
        result = self.ecls_command('--source-dir', str(source), '--out', str(self.repo / 'output'))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Dictionary differs from verified release', result.stderr)
        self.assertNotIn('FileNotFoundError', result.stderr)
        self.assertFalse((self.repo / 'sources').exists())

    def test_selected_missing_default_file_still_fails_loud(self):
        result = self.ecls_command('--out', str(self.repo / 'output'))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('FileNotFoundError', result.stderr)
        self.assertIn('sources/reused-surveys/ecls_k/ECLSK_Kto8_child_STATA.dct', result.stderr)


if __name__ == '__main__':
    unittest.main()
