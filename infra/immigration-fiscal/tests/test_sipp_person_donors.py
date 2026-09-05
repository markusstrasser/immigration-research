"""Independent arithmetic fixtures run the actual SIPP builders and ACS joins.

Run: uv run --with duckdb,pandas python3 -m unittest discover -s infra/immigration-fiscal/tests
Native-First: standard-library unittest and temporary files; no test framework service.
"""
from __future__ import annotations

import csv
import ast
import io
import json
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile
from pathlib import Path

import duckdb

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "build"))
import build_federal_microsim_sipp_2024 as federal
import build_public_mvp_sipp_module_2024 as monthly
import build_public_mvp_sipp_meps_bridge_2024 as health_bridge
import build_country_fiscal_tensor as tensor
import compose_scenario_ledger as composer
from public_mvp_io import (
    SIPP_PERSON_MONTH_COLS, iter_sipp_allocated_sample_units, sipp_eeduc_bucket,
    nativity_group,
)


def person_rows(pnum=101, **changes):
    base = {
        "SSUID": "household", "PNUM": str(pnum), "MONTHCODE": "1", "RIN_UNIV": "1",
        "WPFINWGT": "1", "TAGE_EHC": "30", "EBORNUS": "2", "ENATCIT": "", "EEDUC": "39",
        "TYRENTRY": "2010", "TPEARN": "1000", "TPTOTINC": "1000",
        "RSNAP_MNYN": "2", "ESNAP_OWN": "", "ESNAP_CNT": "", "TSNAP_AMT": "",
        "RTANF_MNYN": "2", "ETANF_OWN": "", "TTANF_AMT": "",
        "RSSI_MNYN": "2", "TSSI_AMT": "",
        **{key: str(value) for key, value in changes.items()},
    }
    return [{**base, "MONTHCODE": str(month)} for month in range(1, 13)]


class SippPersonDonorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.schema = self.directory / "schema.json"
        self.archive = self.directory / "pu2024_csv.zip"
        self.schema.write_text(json.dumps([{"name": name} for name in SIPP_PERSON_MONTH_COLS]))

    def write_rows(self, rows):
        text = io.StringIO()
        writer = csv.writer(text, delimiter="|")
        writer.writerow(SIPP_PERSON_MONTH_COLS)
        for row in rows:
            writer.writerow([row[name] for name in SIPP_PERSON_MONTH_COLS])
        with zipfile.ZipFile(self.archive, "w") as archive:
            archive.writestr("pu2024.csv", text.getvalue())

    def build(self, rows):
        self.write_rows(rows)
        return federal.build_all_donor_cells(
            schema_path=self.schema, zip_path=self.archive, output_dir=self.directory,
        )

    def test_unknown_meps_birthplace_is_not_foreign_born(self):
        self.assertEqual(nativity_group("1"), "us_born")
        self.assertEqual(nativity_group("2"), "foreign_born")
        for code in ("-7", "-8", "", "-1"):
            self.assertEqual(nativity_group(code), "unknown")

    def test_official_education_codes_and_invalid_sentinels(self):
        expected = {
            **{code: "1_lt_hs" for code in range(31, 39)}, 39: "2_hs_ged",
            40: "3_some_college", 41: "3_some_college", 42: "4_associate",
            43: "5_bachelors", 44: "6_masters", 45: "7_professional_plus",
            46: "7_professional_plus",
        }
        for code, label in expected.items():
            with self.subTest(code=code):
                self.assertEqual(sipp_eeduc_bucket(code), label)
        for code in (-1, 0, 30, 47, 99, None, 31.5):
            with self.subTest(code=code), self.assertRaises(ValueError):
                sipp_eeduc_bucket(code)
        with self.assertRaises(ValueError):
            self.build(person_rows(EEDUC=-1))

    def test_birthright_citizens_born_abroad_are_native_donors(self):
        foreign, native = self.build(
            person_rows(101, ENATCIT=5) + person_rows(102, ENATCIT=4)
            + person_rows(103, ENATCIT=1) + person_rows(104, EBORNUS=1, ENATCIT=4)
        )
        self.assertEqual(sum(r['person_year_count'] for r in native), 3)
        self.assertEqual(sum(r['person_year_count'] for r in foreign), 1)

    def test_unmatched_health_cells_fail_without_exporting_partial_results(self):
        sipp = [{'age_band': '30-34', 'nativity_code': '2'}]
        meps = [{'age_band': '55-64', 'nativity_code': '2', 'nativity_group': 'foreign_born'}]
        with patch.object(health_bridge, 'PROTO', self.directory), patch.object(health_bridge, '_read_csv', side_effect=[sipp, meps]):
            with self.assertRaisesRegex(ValueError, 'Unmatched SIPP health'):
                health_bridge.build()

    def test_all_working_age_health_bridge_mappings(self):
        expected = {
            "25-29": "25-34", "30-34": "25-34", "35-39": "35-44",
            "40-44": "35-44", "45-49": "45-54", "50-54": "45-54",
            "55-59": "55-64", "60-64": "55-64", "55-64": "55-64",
        }
        for source, target in expected.items():
            with self.subTest(source=source):
                self.assertEqual(health_bridge._sipp_to_meps_age(source), target)
        for band in ("18-24", "30-39", "65-74", "invalid"):
            with self.subTest(source=band), self.assertRaises(ValueError):
                health_bridge._sipp_to_meps_age(band)

    def test_identical_adults_keep_person_units_through_actual_acs_join(self):
        rows, _ = self.build(person_rows(101, TPEARN=8000 / 12, TPTOTINC=8000 / 12)
                             + person_rows(102, TPEARN=8000 / 12, TPTOTINC=8000 / 12))
        self.assertAlmostEqual(rows[0]["employee_oasdi_hi_proxy_annual"], 612)
        self.assertEqual(rows[0]["person_year_count"], 2)
        con = duckdb.connect(":memory:")
        self.addCleanup(con.close)
        con.execute("""CREATE TABLE acs_person_raw AS SELECT * FROM (VALUES
            ('303','16','30','8000','1000000','1','2','01','1'),
            ('303','16','30','8000','1000000','1','2','01','1'))
            AS t(POBP,SCHL,AGEP,PINCP,ADJINC,PWGTP,NATIVITY,HISP,RAC1P)""")
        con.execute("CREATE TABLE pobp_dim AS SELECT '0303' AS pobp, 'Mexico' AS origin_label")
        federal.build_acs_recipient_cells(con)
        federal.load_federal_microsim_into_duckdb(con, rows)
        observed = con.execute("""SELECT SUM(weighted_adults),
            SUM(weighted_adults * payroll_less_allocated_benefits_proxy_annual)
            FROM acs_origin_person_payroll_transfer_microsim_2023""").fetchone()
        self.assertEqual(observed[0], 2)
        self.assertAlmostEqual(observed[1], 1224)

    def test_individual_education_age_income_and_row_order(self):
        source = person_rows(101, EEDUC=38, TAGE_EHC=30, TPEARN=1000, TPTOTINC=1000)
        source += person_rows(102, EEDUC=43, TAGE_EHC=50, TPEARN=6000, TPTOTINC=6000)
        forward, _ = self.build(source)
        backward, _ = self.build(list(reversed(source)))
        self.assertEqual(forward, backward)
        cells = {(row["education_bucket"], row["age_band"], row["income_band"]): row for row in forward}
        self.assertAlmostEqual(cells[("<HS", "25-34", "lt20k")]["employee_oasdi_hi_proxy_annual"], 918)
        self.assertAlmostEqual(cells[("other", "45-54", "40-75k")]["employee_oasdi_hi_proxy_annual"], 5508)

    def test_person_annual_cap_precedes_averaging_and_medicare_is_uncapped(self):
        source = person_rows(101, TPEARN=150000 / 12, TPTOTINC=150000 / 12)
        source += person_rows(102, TPEARN=500000 / 12, TPTOTINC=500000 / 12)
        rows, _ = self.build(source)
        self.assertEqual(len(rows), 1)
        # 150000*.0765 = 11475; 160200*.062 + 500000*.0145 = 17182.40.
        self.assertAlmostEqual(rows[0]["employee_oasdi_hi_proxy_annual"], 14328.70)

    def test_annual_sums_and_december_weights_not_monthly_annualization(self):
        first = person_rows(101, TPEARN=0, TPTOTINC=0, WPFINWGT=10)
        first[0].update(TPEARN="12000", TPTOTINC="12000")
        first[-1]["WPFINWGT"] = "1"
        second = person_rows(102, TPEARN=1500, TPTOTINC=1500, WPFINWGT=3)
        rows, _ = self.build(first + second)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["person_weight_sum"], 4)
        # Per-person 918 and 1377, with annual weights 1 and 3.
        self.assertAlmostEqual(rows[0]["employee_oasdi_hi_proxy_annual"], 1262.25)
        self.assertAlmostEqual(rows[0]["mean_annual_person_tptotinc"], 16500)

    def test_mixed_nativity_child_only_tanf_and_child_ssi_are_not_adult_costs(self):
        owner = person_rows(101, EBORNUS=1, RSNAP_MNYN=1, ESNAP_OWN=101,
                            ESNAP_CNT=3, TSNAP_AMT=300, ETANF_OWN=101, TTANF_AMT=600)
        migrant = person_rows(102, RSNAP_MNYN=1, ESNAP_OWN=101)
        child = person_rows(103, EBORNUS=1, TAGE_EHC=8, EEDUC="", TPEARN="", TPTOTINC=50,
                            RSNAP_MNYN=1, ESNAP_OWN=101, RTANF_MNYN=1,
                            ETANF_OWN=101, RSSI_MNYN=1, TSSI_AMT=50)
        foreign, native = self.build(owner + migrant + child)
        for rows in (foreign, native):
            self.assertEqual(len(rows), 1)
            self.assertAlmostEqual(rows[0]["allocated_snap_tanf_ssi_annual"], 1200)
            self.assertEqual(rows[0]["mean_annual_allocated_tanf"], 0)
            self.assertEqual(rows[0]["mean_annual_person_tssi"], 0)
        meta = json.loads((self.directory / "sipp_person_donor_cells_2024.meta.json").read_text())
        self.assertEqual(meta["unweighted_source_benefits_all_people"],
                         {"snap": 3600, "tanf": 7200, "ssi": 600})
        self.assertEqual(meta["unweighted_benefits_outside_adult_donor_universe"],
                         {"snap": 1200, "tanf": 7200, "ssi": 600})
        out = monthly.build(schema_path=self.schema, zip_path=self.archive, output_dir=self.directory)
        with out.open() as stream:
            month_rows = list(csv.DictReader(stream))
        self.assertEqual(len(month_rows), 2)
        self.assertNotIn("citizenship_code", month_rows[0])
        for row in month_rows:
            self.assertAlmostEqual(float(row["mean_monthly_allocated_snap"]), 100)
            self.assertEqual(float(row["mean_monthly_allocated_tanf"]), 0)

    def test_negative_personal_earnings_and_income_are_preserved(self):
        rows, _ = self.build(person_rows(TPEARN=-100, TPTOTINC=-50))
        self.assertEqual(rows[0]["mean_annual_person_tpearn"], -1200)
        self.assertEqual(rows[0]["mean_annual_person_tptotinc"], -600)
        self.assertEqual(rows[0]["employee_oasdi_hi_proxy_annual"], 0)

    def test_duplicate_month_missing_owner_and_wrong_snap_denominator_fail(self):
        variants = [
            person_rows() + [person_rows()[0]],
            person_rows(RSNAP_MNYN=1, ESNAP_OWN=102),
            person_rows(RSNAP_MNYN=1, ESNAP_OWN=101, ESNAP_CNT=2, TSNAP_AMT=300),
        ]
        for rows in variants:
            with self.subTest(rows=rows[0]), self.assertRaises(ValueError):
                self.build(rows)

    def test_missing_adult_income_is_not_silently_zero(self):
        with self.assertRaisesRegex(ValueError, "Missing in-universe SIPP adult income"):
            self.build(person_rows(TPTOTINC=""))

    def test_acs_inflation_adjustment_and_missing_income_are_not_top_bucket(self):
        con = duckdb.connect(":memory:")
        self.addCleanup(con.close)
        con.execute("""CREATE TABLE acs_person_raw AS SELECT * FROM (VALUES
            ('303','16','30','19000','1100000','1','2','01','1'),
            ('303',NULL,'30',NULL,'1000000','2','2','01','1'))
            AS t(POBP,SCHL,AGEP,PINCP,ADJINC,PWGTP,NATIVITY,HISP,RAC1P)""")
        con.execute("CREATE TABLE pobp_dim AS SELECT '0303' AS pobp, 'Mexico' AS origin_label")
        federal.build_acs_recipient_cells(con)
        rows = con.execute("SELECT education_bucket,income_band,weighted_adults FROM acs_origin_person_recipient_cells_2023 ORDER BY weighted_adults").fetchall()
        self.assertEqual(rows, [("HS / GED", "20-40k", 1), (None, None, 2)])

    def test_no_implicit_legacy_recipient_fallback(self):
        rows, _ = self.build(person_rows())
        con = duckdb.connect(":memory:")
        self.addCleanup(con.close)
        with self.assertRaisesRegex(ValueError, "Missing acs_origin_person_recipient_cells"):
            federal.load_federal_microsim_into_duckdb(con, rows)

    def test_unmatched_recipients_fail_before_exporting_partial_population(self):
        rows, _ = self.build(person_rows())
        con = duckdb.connect(":memory:")
        self.addCleanup(con.close)
        con.execute("""CREATE TABLE acs_origin_person_recipient_cells_2023 AS
            SELECT 'Mexico' AS origin_label, 'other' AS education_bucket,
                   '25-34' AS age_band, 'lt20k' AS income_band, 100 AS weighted_adults""")
        with self.assertRaisesRegex(ValueError, "Unmatched ACS recipients"):
            federal.load_federal_microsim_into_duckdb(con, rows)
        self.assertFalse(con.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_name='acs_origin_person_payroll_transfer_microsim_2023'").fetchone()[0])

    def test_benefit_units_and_monthly_coverage_changes_are_separate(self):
        owner = person_rows(101, RSNAP_MNYN=1, ESNAP_OWN=101, ESNAP_CNT=2, TSNAP_AMT=300)
        child = person_rows(102, TAGE_EHC=8, EEDUC="", TPEARN="", TPTOTINC="",
                            RSNAP_MNYN=1, ESNAP_OWN=101)
        other_unit = person_rows(103, EBORNUS=1, RSNAP_MNYN=1, ESNAP_OWN=103,
                                 ESNAP_CNT=1, TSNAP_AMT=90)
        for row in owner[6:]:
            row["ESNAP_CNT"] = "1"
        for row in child[6:]:
            row.update(RSNAP_MNYN="2", ESNAP_OWN="")
        foreign, native = self.build(owner + child + other_unit)
        self.assertEqual(foreign[0]["mean_annual_allocated_snap"], 2700)
        self.assertEqual(native[0]["mean_annual_allocated_snap"], 1080)

    def test_sipp_scenario_uses_each_nativity_own_donors(self):
        foreign, native = self.build(person_rows(101, TPEARN=1000, TPTOTINC=1000)
                                     + person_rows(102, EBORNUS=1, TPEARN=2000, TPTOTINC=2000))
        import pandas as pd
        database = self.directory / "donors.duckdb"
        con = duckdb.connect(str(database))
        for table, rows in (("sipp_person_donor_cells_2024", foreign),
                            ("sipp_person_donor_cells_usborn_2024", native)):
            con.register("input_rows", pd.DataFrame(rows))
            con.execute(f"CREATE TABLE {table} AS SELECT * FROM input_rows")
            con.unregister("input_rows")
        con.close()
        with patch.object(composer, "duckdb_path", return_value=database):
            values = composer._payroll_transfer_by_nativity_education()
        self.assertEqual(values[("2", "HS / GED")]["avg_payroll"], 918)
        self.assertEqual(values[("1", "HS / GED")]["avg_payroll"], 1836)

    def actual_tensor_sql(self, marker):
        source = Path(tensor.__file__).read_text()
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, (ast.Constant, ast.JoinedStr)):
                if marker not in (ast.get_source_segment(source, node) or ""):
                    continue
                try:
                    sql = eval(compile(ast.Expression(node), "tensor-sql", "eval"), vars(tensor))
                except NameError:
                    continue
                if isinstance(sql, str) and marker in sql:
                    return sql
        self.fail(f"Actual tensor SQL not found: {marker}")

    def test_eu_payroll_and_school_exclude_ambiguous_yugoslavia(self):
        con = duckdb.connect(":memory:")
        self.addCleanup(con.close)
        con.execute("ATTACH ':memory:' AS ctx")
        con.execute("""CREATE TABLE ctx.acs_origin_person_payroll_transfer_microsim_2023 AS
            SELECT origin_label, '<HS' AS education_bucket, weighted_adults,
                   100 AS payroll_less_allocated_benefits_proxy_annual,
                   110 AS employee_oasdi_hi_proxy_annual,
                   10 AS allocated_snap_tanf_ssi_annual, 1 AS donor_person_weight
            FROM (VALUES ('France',1),('Czechoslovakia',2),('Yugoslavia',1000))
                 AS t(origin_label,weighted_adults)""")
        self.assertEqual(con.execute(self.actual_tensor_sql("SELECT 'eu27_origin' AS population_group")).fetchone()[2], 3)
        con.execute("""CREATE TEMP TABLE _origin_school AS
            SELECT origin_label, weighted_adults AS weight_adults, 200 AS school_burden_per_adult
            FROM ctx.acs_origin_person_payroll_transfer_microsim_2023""")
        con.execute(self.actual_tensor_sql("CREATE TEMP TABLE _pop_school"))
        self.assertEqual(con.execute("SELECT weight_adults,school_per_adult FROM _pop_school WHERE population_group='eu27_origin'").fetchone(), (3, 200))

    def test_education_comparison_retains_actual_native_donor_result(self):
        con = duckdb.connect(":memory:")
        self.addCleanup(con.close)
        con.execute("ATTACH ':memory:' AS ctx")
        con.execute("""CREATE TABLE ctx.acs_nh_white_person_payroll_transfer_microsim_2023 AS
            SELECT '<HS' AS education_bucket, 20 AS weighted_adults,
                   400 AS payroll_less_allocated_benefits_proxy_annual, 1 AS donor_person_weight""")
        con.execute("""CREATE TABLE ctx.acs_origin_person_payroll_transfer_microsim_2023 AS
            SELECT '<HS' AS education_bucket, 10 AS weighted_adults,
                   900 AS payroll_less_allocated_benefits_proxy_annual, 1 AS donor_person_weight,
                   'Mexico' AS origin_label""")
        con.execute(self.actual_tensor_sql("CREATE TABLE education_matched_payroll_transfer"))
        row = con.execute("SELECT n_white,n_mex,payroll_transfer_white,payroll_transfer_mex FROM education_matched_payroll_transfer").fetchone()
        self.assertEqual(row, (20, 10, 400, 900))
        columns = {r[0] for r in con.execute("DESCRIBE education_matched_payroll_transfer").fetchall()}
        self.assertFalse(columns & {"fed_white_adj", "ratio_mex_to_white_adj", "cell_verdict"})

    def test_payroll_multiplier_keeps_transfers_fixed(self):
        con = duckdb.connect(":memory:")
        self.addCleanup(con.close)
        con.execute("""CREATE TEMP TABLE _pop_fed AS SELECT 'mexico_origin' AS population_group,
            '<HS' AS education_bucket, 10 AS weight_adults, 2000 AS payroll_per_adult,
            500 AS transfers_per_adult, 1500 AS fed_net_per_adult""")
        con.execute("""CREATE TABLE mechanical_payroll_multiplier_scenarios AS
            SELECT '<HS' AS education_bucket, .96 AS payroll_multiplier, 'fixture' AS scenario_id""")
        con.execute("""CREATE TABLE country_fiscal_tensor (
            population_group VARCHAR, education_bucket VARCHAR, fiscal_layer VARCHAR,
            effect_order INT, weight_adults DOUBLE, value_per_adult DOUBLE,
            value_total_usd DOUBLE, unit VARCHAR, source_ref VARCHAR, notes VARCHAR)""")
        con.execute(self.actual_tensor_sql("p.payroll_per_adult * g.payroll_multiplier"))
        row = con.execute("SELECT value_per_adult,value_total_usd,notes FROM country_fiscal_tensor").fetchone()
        self.assertEqual(row[:2], (1420, 14200))
        self.assertIn("not estimated GE", row[2])

    def test_rollup_preserves_alternative_scenarios_and_units(self):
        con = duckdb.connect(":memory:")
        self.addCleanup(con.close)
        con.execute("""CREATE TABLE country_fiscal_tensor (
            population_group VARCHAR, education_bucket VARCHAR, fiscal_layer VARCHAR,
            effect_order INT, weight_adults DOUBLE, value_per_adult DOUBLE,
            value_total_usd DOUBLE, unit VARCHAR, source_ref VARCHAR, notes VARCHAR)""")
        con.executemany("""INSERT INTO country_fiscal_tensor
            (population_group,education_bucket,fiscal_layer,effect_order,weight_adults,
             value_per_adult,value_total_usd,unit,source_ref,notes)
            VALUES (?,?,?,?,?,?,?,?,?,?)""", [
            ('cbo_surge_cohort',None,'state_local',3,None,None,9_200_000_000,'USD_total','direct','Alternative'),
            ('cbo_surge_cohort',None,'state_local',3,None,None,9_800_000_000,'USD_total','potential','Alternative'),
            ('mexico_origin','<HS','payroll_transfer_annual',2,10,1420,14200,'USD_per_adult_per_year','minus4pct','Alternative'),
            ('mexico_origin','<HS','payroll_transfer_annual',2,10,1540,15400,'USD_per_adult_per_year','plus2pct','Alternative'),
            ('unit_fixture','<HS','scope_fixture',1,1,10,10,'USD_2012','fixture','Different price units'),
            ('unit_fixture','<HS','scope_fixture',1,1,20,20,'USD_2023','fixture','Different price units'),
        ])
        con.execute(self.actual_tensor_sql("CREATE VIEW v_country_fiscal_rollup"))
        self.assertEqual(con.execute("SELECT COUNT(*) FROM v_country_fiscal_rollup").fetchone()[0], 6)
        self.assertEqual(con.execute("""SELECT scenario_id,weight_adults,value_total_usd
            FROM v_country_fiscal_rollup WHERE population_group='mexico_origin'
            ORDER BY scenario_id""").fetchall(), [('minus4pct',10,14200),('plus2pct',10,15400)])
        self.assertEqual(con.execute("""SELECT scenario_id,value_total_usd
            FROM v_country_fiscal_rollup WHERE population_group='cbo_surge_cohort'
            ORDER BY scenario_id""").fetchall(), [('direct',9_200_000_000),('potential',9_800_000_000)])

    def test_nas_annual_comparison_retains_units_without_false_match_verdict(self):
        con = duckdb.connect(":memory:")
        self.addCleanup(con.close)
        con.execute("ATTACH ':memory:' AS life")
        con.execute("ATTACH ':memory:' AS ctx")
        con.execute("""CREATE TABLE life.npv_education_benchmarks AS
            SELECT '<HS' AS acs_education_bucket, 10000 AS individual_npv_2012_usd,
                   'NAS 2017' AS study, 'baseline_public_goods' AS adjustment,
                   25 AS age_at_arrival, false AS includes_descendants""")
        con.execute("""CREATE TABLE ctx.acs_origin_person_payroll_transfer_microsim_2023 AS
            SELECT '<HS' AS education_bucket, 300 AS payroll_less_allocated_benefits_proxy_annual,
                   10 AS weighted_adults, 1 AS donor_person_weight""")
        con.execute(self.actual_tensor_sql("CREATE TABLE annual_npv_bridge_grid"))
        columns = {row[0] for row in con.execute("DESCRIBE annual_npv_bridge_grid").fetchall()}
        self.assertNotIn("annual_gap", columns)
        self.assertNotIn("bridge_verdict", columns)
        self.assertEqual(con.execute("SELECT DISTINCT nas_price_year,payroll_transfer_price_year,comparison_status FROM annual_npv_bridge_grid").fetchall(),
                         [(2012, 2023, "not_comparable_without_scope_and_price_alignment")])


if __name__ == "__main__":
    unittest.main()
