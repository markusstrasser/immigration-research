"""Regression checks for overlap, accounting closure and fail-loud provenance."""
from pathlib import Path
import csv
import importlib.util
import json
import tempfile
import unittest

HERE = Path(__file__).resolve().parent


class AccountingTests(unittest.TestCase):
    def test_existing_freight_is_not_added_twice(self):
        summary = json.loads((HERE / "derived/summary.json").read_text())
        controls = [r for r in summary["rows"] if r["arm"] == "freight_demand_control"]
        self.assertEqual(len(controls), 4)
        for row in controls:
            self.assertAlmostEqual(row["change_bn"], 0, delta=1e-12)
            self.assertAlmostEqual(row["result_bn"], row["baseline_bn"], delta=1e-12)

    def test_every_reported_change_closes_to_its_parts(self):
        summary = json.loads((HERE / "derived/summary.json").read_text())
        with (HERE / "derived/line_changes.csv").open() as f:
            lines = list(csv.DictReader(f))
        for row in summary["rows"]:
            parts = [r for r in lines if all(r[k] == row[k] for k in ["arm", "frame", "end"])]
            self.assertEqual(len(parts), 2)
            values = [sum(float(r[k]) for k in ["police_delta_bn", "fire_delta_bn", "pos_capital_delta_bn", "highway_delta_bn"]) for r in parts]
            self.assertAlmostEqual(sum(values)/2, row["change_bn"], delta=1e-9)
            self.assertAlmostEqual(row["baseline_bn"]+row["change_bn"], row["result_bn"], delta=1e-9)
        for row in lines:
            self.assertAlmostEqual(float(row["new_safety_target_bn"])+float(row["new_safety_other_bn"]), float(row["safety_national_bn"]), delta=1e-9)

    def test_stale_source_stops_validation(self):
        spec = importlib.util.spec_from_file_location("lane_pins", HERE / "pins.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source.txt"
            source.write_text("changed primary bytes\n")
            with self.assertRaisesRegex(RuntimeError, "pinned source missing/stale"):
                module.validate({"sources": [{"path": str(source), "sha256": "0"*64}]})

    def test_no_false_full_lineage_sampling_error(self):
        summary = json.loads((HERE / "derived/summary.json").read_text())
        for row in summary["rows"]:
            if row["frame"] == "lineage":
                self.assertIsNone(row["conditional_union_key_se_bn"])

    def test_all_altered_lineage_freight_arms_are_labeled(self):
        summary = json.loads((HERE / "derived/summary.json").read_text())
        altered = {a["arm"] for a in summary["arms"] if a["freight"] is not None and a["arm"] != "freight_demand_control"}
        for row in summary["rows"]:
            if row["frame"] == "lineage" and row["arm"] in altered:
                self.assertIn("[DEGRADED]", row["freight_basis"])


if __name__ == "__main__":
    unittest.main()
