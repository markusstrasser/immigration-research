"""Consistency of the person-level accrual arm's committed outputs (derived/sept29/): the comparison file repeats
the flat and person arms' shares, and the model record carries the payload's pension figures."""
import json
from pathlib import Path

import numpy as np
import pandas as pd

D = Path(__file__).resolve().parent / "derived/sept29"
KEY = ["convention", "end", "breakdown", "cell"]


def arms():
    a = pd.read_csv(D / "person_accrual_arms.csv")
    return a.set_index(["arm", *KEY])


def test_arms_repeat_the_flat_and_person_files():
    a = arms()
    for arm, name in (("flat", "net_positive_shares.csv"), ("person", "net_positive_shares_person_accrual.csv")):
        f = pd.read_csv(D / name).query("convention in ['A', 'B']").set_index(KEY)
        sub = a.loc[arm].reindex(f.index)
        if arm == "flat":   # the flat file has no case-flag rows; the arms file adds them
            assert set(a.loc[arm].index) - set(f.index) == {k for k in a.loc[arm].index if k[2] == "head_status_case_flag"}
        assert np.allclose(sub.share_members_net_positive, f.share_members_net_positive, atol=1e-6)
        assert np.allclose(sub.se, f.se, atol=1e-6)
        assert (sub.records == f.records).all()


def test_flat_arm_is_its_own_baseline():
    flat = arms().loc["flat"]
    assert (flat.diff_vs_flat.abs() < 1e-12).all() and (flat.se_diff.abs() < 1e-12).all()


def test_model_record_carries_the_payload():
    m = json.loads((D / "person_accrual_model.json").read_text())
    assert m["gates_passed"] and m["pension_commit"] == "9ea1beb"
    u = m["oasdi"]["union"]
    net = u["per_tax_dollar_gross"] * (1 - u["future_share_own_rate"])
    assert abs(net - m["payload"]["ratio_net"]) < 1e-12
    assert abs(m["part_a_bn"]["union"] - m["payload"]["part_a_accrual_bn"]) < 1e-6
    assert abs(sum(m["part_a_bn"][g] for g in ("G1", "G2", "G3plus")) - m["part_a_bn"]["union"]) < 1e-9
