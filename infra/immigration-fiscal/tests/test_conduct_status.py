"""Regression checks tied to primary-source definitions and observed replication cells."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "build"))
from build_status_crosswalk import CLASSES, status_class_for
from load_light_tx_crime import _melt, _melt_nat
from load_spi_citizenship import summarize_spi, matched_rates, DENOM_UNIVERSE


class ConductStatusTests(unittest.TestCase):
    def test_citizenship_does_not_identify_nativity(self):
        classes = {r[0]: r for r in CLASSES}
        citizen = status_class_for("BJS_SPI", "RV0004_1")
        self.assertEqual(classes[citizen][2:4], ("unknown", True))
        foreign = status_class_for("ACS_NATIVITY", "2")
        self.assertEqual(classes[foreign][2:4], ("foreign", None))
        legal = status_class_for("LIGHT_TXDPS", "LEGAL")
        self.assertIsNone(classes[legal][3])
        self.assertNotEqual(legal, status_class_for("LIGHT_TXDPS", "LEGAL_NONCIT"))

    def test_unrecognized_source_code_fails(self):
        with self.assertRaises(ValueError):
            status_class_for("BJS_SPI", "V0950_skip_or_1")

    def test_spi_official_missing_is_not_assigned_citizen(self):
        frame = pd.DataFrame({"RV0001": [18, 30, 45, 70], "RV0004": [1, 2, 8, -9], "V1585": [10., 20., 30., 40.]})
        result = summarize_spi(frame).set_index("citizenship_status")
        self.assertEqual(result.loc["us_citizen", "weighted_inmates"], 10)
        self.assertEqual(result.loc["ambiguous", "weighted_inmates"], 70)
        self.assertEqual(result.loc["us_citizen", "status_class"], "citizen_unknown_nativity")

    def test_prison_rate_rejects_wrong_year_and_universe(self):
        summary = summarize_spi(pd.DataFrame({"RV0001": [25, 30], "RV0004": [1, 2], "V1585": [100., 10.]}))
        denom = pd.DataFrame({"year": [2016, 2016], "geography": ["US", "US"],
                              "universe": [DENOM_UNIVERSE] * 2,
                              "citizenship_status": ["us_citizen", "noncitizen"],
                              "population": [100000., 10000.], "source": ["test fixture"] * 2})
        self.assertTrue(matched_rates(summary, denom)["per_100k_adults"].eq(100).all())
        with self.assertRaisesRegex(ValueError, "2016 denominator"):
            matched_rates(summary, denom.assign(year=2024))
        with self.assertRaisesRegex(ValueError, "institutional group quarters"):
            matched_rates(summary, denom.assign(universe="civilian noninstitutional residents"))

    def test_spi_age_universe_is_enforced(self):
        with self.assertRaisesRegex(ValueError, "at least 18"):
            summarize_spi(pd.DataFrame({"RV0001": [17], "RV0004": [1], "V1585": [100.]}))

    def test_actual_2018_violent_cell_does_not_subtract_naturalized_twice(self):
        # openICPSR124923: baseline legal population/count is split in CMS_nat.
        source = dict(year=2018, category=1, undocumented_immigrants_charge=1858,
                      citizen_charge=53837, immigrants_charge=5632, pop_undoc=1794800,
                      tot_citizen=23773820, tot_legal2_immi=3133224,
                      illegal2_immigrants_crime_rate=103.521286,
                      citizen_crime_rate=226.454986, immigrant_crime_rate=179.750946)
        split = dict(source, immigrants_charge=2468, tot_legal2_immi=1276552,
                     immigrant_crime_rate=193.333298, naturalized_charge=3164,
                     naturalized_citizen=1856672, naturalized_citizen_rate=170.412430)
        base = {r["status_class"]: r for r in _melt(pd.DataFrame([source]), "CMS")}
        nat = {r["status_class"]: r for r in _melt_nat(pd.DataFrame([split]))}
        for field in ["charge_count", "population", "crime_rate_per_100k"]:
            self.assertEqual(base["native_born"][field], nat["native_born"][field])
        for field in ["charge_count", "population"]:
            self.assertEqual(base["legal_immigrant_mixed_citizenship"][field],
                             nat["lpr_legal_noncitizen"][field] + nat["naturalized"][field])
        self.assertEqual(nat["native_born"]["charge_count"], 53837)
        self.assertEqual(nat["native_born"]["population"], 23773820)


class SpiCallerTests(unittest.TestCase):
    """Run the real shell caller; only external builders/config/runtime are stubs."""

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="spi caller ")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        for directory in ["build", "acquire", "bin", "derived/crime", "data"]:
            (self.root / directory).mkdir(parents=True)
        caller = Path(__file__).resolve().parents[1] / "build-context.sh"
        shutil.copy2(caller, self.root / "build-context.sh")
        (self.root / "acquire/lib.sh").write_text('''immigration_fiscal_load_config() {
  PNY_DATA_ROOT="$SPI_CALLER_TEST_ROOT/data"
  DERIVED_ROOT="$SPI_CALLER_TEST_ROOT/derived"
  DUCKDB_PATH="$SPI_CALLER_TEST_ROOT/context.duckdb"
  CORPUS_ROOT="$SPI_CALLER_TEST_ROOT/corpus"
}
''')
        runtime = self.root / "bin/uv"
        runtime.write_text('''#!/usr/bin/env bash
set -euo pipefail
while (( $# )); do
  if [[ "$1" == python || "$1" == python3 ]]; then
    shift
    exec "$SPI_CALLER_TEST_PYTHON" "$@"
  fi
  shift
done
echo "stub uv received no Python invocation" >&2
exit 97
''')
        runtime.chmod(0o755)
        builder = '''import json, os, pathlib, sys
root = pathlib.Path(os.environ["SPI_CALLER_TEST_ROOT"])
name = pathlib.Path(__file__).name
crime = pathlib.Path(os.environ["DERIVED_ROOT"]) / "crime"
exports = [crime / "spi_incarceration_rate.csv", crime / "spi_inmates_by_citizenship_2016.csv"]
event = {"builder": name, "args": sys.argv[1:],
         "denominator_present": "SPI_DENOMINATOR_CSV" in os.environ,
         "denominator": os.environ.get("SPI_DENOMINATOR_CSV"),
         "existing_spi_exports": [p.name for p in exports if p.exists()]}
with (root / "calls.jsonl").open("a") as stream:
    stream.write(json.dumps(event) + "\\n")
if name == "build_immigration_warehouse.py":
    pathlib.Path(os.environ["DUCKDB_PATH"]).write_text("stub rebuilt warehouse")
if name == "load_spi_citizenship.py":
    if sys.argv[1:] != ["--counts-only"]:
        print("stub SPI: explicitly supplied denominator rejected", file=sys.stderr)
        sys.exit(23)
    if os.environ.get("SPI_CALLER_TEST_FAIL_COUNTS") == "1":
        print("stub SPI: malformed present source", file=sys.stderr)
        sys.exit(24)
    exports[1].write_text("fresh counts")
'''
        for name in ["build_immigration_warehouse.py", "compose_scenario_ledger.py",
                     "build_status_crosswalk.py", "parse_scaap_awards.py",
                     "load_light_tx_crime.py", "load_spi_citizenship.py",
                     "build_crime_views.py", "build_immigrant_assimilation_profile.py",
                     "load_cps_second_gen.py"]:
            (self.root / "build" / name).write_text(builder)
        self.rate = self.root / "derived/crime/spi_incarceration_rate.csv"
        self.counts = self.root / "derived/crime/spi_inmates_by_citizenship_2016.csv"
        self.unrelated = self.root / "derived/crime/unrelated.csv"
        self.raw = self.root / "data/external/crime_frontier/spi/ICPSR_37692/DS0001/37692-0001-Data.dta"

    def run_caller(self, *, raw_present=False, supplied_denominator=None, fail_counts=False):
        for path in [self.rate, self.counts, self.unrelated]:
            path.write_text("stale fixture")
        if raw_present:
            self.raw.parent.mkdir(parents=True, exist_ok=True)
            self.raw.write_text("present source fixture; parsing is stubbed")
        env = dict(os.environ)
        env.pop("SPI_DENOMINATOR_CSV", None)
        env.update(SPI_CALLER_TEST_ROOT=str(self.root), SPI_CALLER_TEST_PYTHON=sys.executable,
                   PATH=str(self.root / "bin") + os.pathsep + env.get("PATH", ""),
                   SPI_CALLER_TEST_FAIL_COUNTS="1" if fail_counts else "0")
        if supplied_denominator is not None:
            env["SPI_DENOMINATOR_CSV"] = supplied_denominator
        result = subprocess.run(["bash", str(self.root / "build-context.sh")], env=env,
                                capture_output=True, text=True, timeout=20)
        calls = [json.loads(line) for line in (self.root / "calls.jsonl").read_text().splitlines()]
        self.assertEqual(calls[0]["builder"], "build_immigration_warehouse.py")
        self.assertEqual(self.unrelated.read_text(), "stale fixture")
        return result, calls

    def test_optional_absent_source_continues_and_withdraws_exports(self):
        result, calls = self.run_caller()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("[UNAVAILABLE] Optional SPI raw data not staged", result.stdout)
        self.assertNotIn("load_spi_citizenship.py", [call["builder"] for call in calls])
        self.assertEqual(calls[-1]["builder"], "load_cps_second_gen.py")
        self.assertFalse(self.rate.exists())
        self.assertFalse(self.counts.exists())

    def test_explicit_invalid_denominator_does_not_become_optional_skip(self):
        result, calls = self.run_caller(supplied_denominator=str(self.root / "missing.csv"))
        self.assertEqual(result.returncode, 23)
        self.assertEqual(calls[-1]["builder"], "load_spi_citizenship.py")
        self.assertEqual(calls[-1]["args"], [])
        self.assertTrue(calls[-1]["denominator_present"])
        self.assertEqual(calls[-1]["existing_spi_exports"], [])
        self.assertNotIn("[UNAVAILABLE]", result.stdout)

    def test_explicit_empty_denominator_does_not_become_counts_only(self):
        result, calls = self.run_caller(raw_present=True, supplied_denominator="")
        self.assertEqual(result.returncode, 23)
        self.assertEqual(calls[-1]["builder"], "load_spi_citizenship.py")
        self.assertEqual(calls[-1]["args"], [])
        self.assertEqual(calls[-1]["denominator"], "")
        self.assertEqual(calls[-1]["existing_spi_exports"], [])
        self.assertFalse(self.rate.exists())
        self.assertFalse(self.counts.exists())

    def test_present_optional_source_requests_counts_only(self):
        result, calls = self.run_caller(raw_present=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        spi = [call for call in calls if call["builder"] == "load_spi_citizenship.py"]
        self.assertEqual(len(spi), 1)
        self.assertEqual(spi[0]["args"], ["--counts-only"])
        self.assertEqual(spi[0]["existing_spi_exports"], [])
        self.assertFalse(spi[0]["denominator_present"])
        self.assertEqual(self.counts.read_text(), "fresh counts")
        self.assertFalse(self.rate.exists())
        self.assertEqual(calls[-1]["builder"], "load_cps_second_gen.py")

    def test_malformed_present_source_failure_is_not_suppressed(self):
        result, calls = self.run_caller(raw_present=True, fail_counts=True)
        self.assertEqual(result.returncode, 24)
        self.assertEqual(calls[-1]["builder"], "load_spi_citizenship.py")
        self.assertEqual(calls[-1]["args"], ["--counts-only"])
        self.assertFalse(self.rate.exists())
        self.assertFalse(self.counts.exists())


if __name__ == "__main__":
    unittest.main()
