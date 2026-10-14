"""Check the age/credit-owner partition against principal published components."""
import importlib.util
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent


def module():
    spec = importlib.util.spec_from_file_location("direct_adult_test", HERE / "direct_adults_v8.py")
    out = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(out)
    return out


def test_direct_cell_preserves_generation_and_reports_credit_age_change():
    direct = module()
    for basis in ("set", "cash"):
        rows, receipt = direct.calculate(basis)
        assert len(rows) == 2
        assert all(g["pass"] and g["final_G2_a_gap_bn"] < 1e-9 for g in receipt["gates"])
        for row in rows:
            assert abs(row["g2_adults_direct_bn"] + row["g2_minors_direct_bn"] - row["g2_total_a_bn"]) < 1e-9
            assert abs(row["first_order_generic_adult_bn"] + row["credit_owner_age_correction_bn"]
                       + row["coverage_adult_cost_bn"] - row["g2_adults_direct_bn"]) < 1e-9


def test_credit_owner_age_export_collapses_to_source_generation_and_joint_se():
    p = json.loads((HERE / "derived/credit_replicates_oct15.json").read_text())
    old = json.loads((HERE / "derived/credit_routing.json").read_text())
    for conv in ("a", "b"):
        for gen in ("G1", "G2", "G3plus"):
            for scenario, values in p["mean_base_credit_net_cost_bn"][conv][gen].items():
                age = p["mean_base_credit_net_cost_bn"][conv + "_age"]
                combined = np.asarray(age[gen + "_adult"][scenario]) + age[gen + "_minor"][scenario]
                assert np.max(np.abs(combined - values)) < 1e-9
                assert abs(module().sdr(np.asarray(values)) - old["average_net_cost_se"][conv][gen][scenario]) < 1e-12
