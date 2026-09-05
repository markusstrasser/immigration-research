"""Regression checks for source-series preservation and flow direction."""
from __future__ import annotations

import json
import io
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

import duckdb

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "build"))
import build_lifetime_evidence_warehouse as evidence


class RemittanceSeriesTests(unittest.TestCase):
    def test_annual_benchmark_cannot_enter_npv_or_wrong_price_year(self):
        with duckdb.connect() as con:
            evidence._seed_npv_benchmarks(con)
            value = con.execute("SELECT individual_npv_2012_usd FROM npv_education_benchmarks WHERE study='Colas-Sachs 2024'").fetchone()[0]
            self.assertIsNone(value)
            self.assertEqual(con.execute("SELECT annual_effect_usd,price_year FROM annual_effect_benchmarks").fetchone(), (750.0, 2017))

    def fixture(self, root: Path, country: str, value: float, indicator: str) -> None:
        folder = root / "worldbank"
        folder.mkdir(exist_ok=True)
        (folder / f"{country}_worker_remittances_bx_trf_pwkr_cd_dt.json").write_text(
            json.dumps([{}, [{"date": "2023", "value": value,
                             "indicator": {"id": indicator}}]])
        )

    def test_both_countries_survive_and_are_receipts(self):
        with tempfile.TemporaryDirectory() as folder, duckdb.connect() as con:
            root = Path(folder)
            self.fixture(root, "mexico", 66.2e9, "BX.TRF.PWKR.CD.DT")
            self.fixture(root, "usa", 7.4e9, "BX.TRF.PWKR.CD.DT")
            with patch.object(evidence, "LT", root):
                evidence._load_remittances(con)
            self.assertEqual(con.sql(
                "SELECT country, value_usd, flow_direction FROM remittance_series ORDER BY country"
            ).fetchall(), [("Mexico", 66.2e9, "received"), ("USA", 7.4e9, "received")])

    def test_changed_indicator_cannot_silently_change_flow_direction(self):
        with tempfile.TemporaryDirectory() as folder, duckdb.connect() as con:
            root = Path(folder)
            self.fixture(root, "usa", 80e9, "BM.TRF.PWKR.CD.DT")
            with patch.object(evidence, "LT", root), self.assertRaisesRegex(ValueError, "indicator"):
                evidence._load_remittances(con)


class StructuredLayerAuthorityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.context = self.root / "context.duckdb"
        self.derived = self.root / "current-derived"
        self.archive = self.root / "external-lifetime"
        self.stderr = io.StringIO()
        for patcher in (
            patch.object(evidence, "duckdb_path", return_value=self.context),
            patch.object(evidence, "DERIVED", self.derived),
            patch.object(evidence, "LT", self.archive),
            patch.object(evidence.sys, "stderr", self.stderr),
        ):
            patcher.start()
            self.addCleanup(patcher.stop)

    def make_context(self, omitted=None):
        # Independent national fixture: all 50 states, DC and the four territory
        # keys observed in the actual source. State-name nulls are permissible.
        keys = "01 02 04 05 06 08 09 10 11 12 13 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 44 45 46 47 48 49 50 51 53 54 55 56 60 66 72 78".split()
        with duckdb.connect(str(self.context)) as source:
            for table in evidence.CONTEXT_OWNED_TABLES:
                if table == omitted:
                    continue
                if table == "state_stage5_context_2023":
                    source.execute("""CREATE TABLE state_stage5_context_2023 (
                        state_fips VARCHAR, state_name VARCHAR, lep_count_reported BIGINT,
                        el_school_year VARCHAR, current_only_column BIGINT)""")
                    source.executemany("INSERT INTO state_stage5_context_2023 VALUES (?,NULL,27702,'2018-2019',2026)", [(key,) for key in keys])
                else:
                    source.execute(f"CREATE TABLE {table} AS SELECT 2026::BIGINT AS canonical_value")

    def write_csv(self, path, body):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body)

    def test_shared_tables_ignore_poisoned_current_and_archived_csvs(self):
        self.make_context()
        relatives = {
            "school_finance_county_2023":"stage2",
            "chas_county_housing_stress_2018_2022":"stage2",
            "irs_migration_county_2022_2023":"stage2",
            "puma_county_area_xwalk_2023":"stage2",
            "state_stage5_context_2023":"stage5",
            "receiver_city_migrant_costs":"stage5",
            "acs_foreign_born_education_bucket_totals_2023":"stage3_proto",
        }
        for table, folder in relatives.items():
            for base in (self.derived, self.archive / "derived"):
                self.write_csv(base / folder / f"{table}.csv", "poisoned_old_value\n-999\n")
        with duckdb.connect() as con:
            evidence._load_structured_layers(con)
            self.assertEqual(con.execute("SELECT COUNT(*),COUNT(DISTINCT state_fips),MIN(lep_count_reported),MIN(current_only_column) FROM state_stage5_context_2023").fetchone(), (55,55,27702,2026))
            self.assertEqual(con.execute("SELECT DISTINCT el_school_year FROM state_stage5_context_2023").fetchall(), [('2018-2019',)])
            for table in relatives.keys() - {"state_stage5_context_2023"}:
                self.assertEqual(con.execute(f"SELECT * FROM {table}").fetchall(), [(2026,)])
            self.assertEqual(con.execute("SELECT COUNT(*) FROM duckdb_databases() WHERE database_name='_lifetime_context'").fetchone()[0], 0)

    def test_missing_context_fails_before_changing_existing_lifetime_table(self):
        self.write_csv(self.archive / "derived/stage5/state_stage5_context_2023.csv", "poisoned\n1\n")
        with duckdb.connect() as con:
            con.execute("CREATE TABLE school_finance_county_2023 AS SELECT 42 AS keep_value")
            with self.assertRaisesRegex(FileNotFoundError, "canonical context"):
                evidence._load_structured_layers(con)
            self.assertEqual(con.execute("SELECT * FROM school_finance_county_2023").fetchall(), [(42,)])

    def test_missing_shared_table_fails_before_any_shared_copy(self):
        self.make_context(omitted="receiver_city_migrant_costs")
        with duckdb.connect() as con:
            con.execute("CREATE TABLE school_finance_county_2023 AS SELECT 42 AS keep_value")
            with self.assertRaisesRegex(ValueError, "receiver_city_migrant_costs"):
                evidence._load_structured_layers(con)
            self.assertEqual(con.execute("SELECT * FROM school_finance_county_2023").fetchall(), [(42,)])

    def test_full_builder_propagates_required_context_failure(self):
        catalog = [{"source_id":"fixture", "rel_path":"external/lifetime/fixture.csv",
                    "category":"fixture", "file_name":"fixture.csv", "ext":"csv",
                    "bytes":1, "min_bytes_expected":1, "acquire_script":"fixture",
                    "notes":"fixture", "exists":True}]
        with patch.object(evidence, "DUCKDB_PATH", self.root / "lifetime.duckdb"), \
             patch.object(evidence, "_manifest_lifetime_rows", return_value=catalog), \
             patch.object(evidence, "_scan_orphans", return_value=[]), \
             patch.object(evidence, "_load_mining_artifacts", side_effect=AssertionError("Required context failure was swallowed")):
            with self.assertRaisesRegex(FileNotFoundError, "canonical context"):
                evidence.build()

    def test_invalid_state_keys_fail_before_copy(self):
        for mutation in (
            "UPDATE state_stage5_context_2023 SET state_fips=NULL WHERE state_fips='60'",
            "UPDATE state_stage5_context_2023 SET state_fips='01' WHERE state_fips='60'",
            "DELETE FROM state_stage5_context_2023 WHERE state_fips='01'",
            "UPDATE state_stage5_context_2023 SET state_fips='99' WHERE state_fips='60'",
        ):
            with self.subTest(mutation=mutation):
                self.context.unlink(missing_ok=True)
                self.make_context()
                with duckdb.connect(str(self.context)) as source:
                    source.execute(mutation)
                with duckdb.connect() as con:
                    with self.assertRaisesRegex(ValueError, "state context"):
                        evidence._load_structured_layers(con)
                    self.assertEqual(con.execute("SELECT COUNT(*) FROM information_schema.tables").fetchone()[0], 0)

    def test_absent_optional_generated_file_never_loads_archived_substitute(self):
        self.make_context()
        self.write_csv(self.archive / "derived/stage3_proto/sipp_public_mvp_cells_2024.csv", "version\n-999\n")
        with duckdb.connect() as con:
            con.execute("CREATE TABLE sipp_public_mvp_cells_2024 AS SELECT 42 AS version")
            evidence._load_structured_layers(con)
            self.assertEqual(con.execute("SELECT * FROM sipp_public_mvp_cells_2024").fetchall(), [(42,)])
        self.assertIn("Optional source unavailable; sipp_public_mvp_cells_2024 unchanged", self.stderr.getvalue())

    def test_declared_generated_and_raw_sources_remain_available(self):
        self.make_context()
        self.write_csv(self.derived / "stage3_proto/sipp_public_mvp_cells_2024.csv", "version\n2026\n")
        self.write_csv(self.archive / "derived/stage3_proto/sipp_public_mvp_cells_2024.csv", "version\n-999\n")
        self.write_csv(self.archive / "ssa/ssa_period_life_table_2023.csv", "age,ex\n0,77.4\n")
        with duckdb.connect() as con:
            evidence._load_structured_layers(con)
            self.assertEqual(con.execute("SELECT * FROM sipp_public_mvp_cells_2024").fetchall(), [(2026,)])
            self.assertEqual(con.execute("SELECT * FROM ssa_period_life_table_2023").fetchall(), [(0,77.4)])


if __name__ == "__main__":
    unittest.main()
