"""Status arm conservation, alignment, and explicit non-additive rejection."""
import importlib.util
from pathlib import Path
import sys
from types import SimpleNamespace

import numpy as np
import pandas as pd
import pytest

spec = importlib.util.spec_from_file_location("status_keys_oct14_tested", Path(__file__).with_name("status_keys_oct14.py"))
S = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = S
spec.loader.exec_module(S)


def toy():
    w = np.array([2.0, 3.0, 5.0])
    raw = {key: np.array([10.0, 20.0, 30.0]) for key in set(S.LINE_KEYS.values())}
    rules = {key: value * np.array([0.4, 1.0, 1.0]) for key, value in raw.items()}
    return S.StatusKeys({"raw": S.normalized(raw, w), "rules_only": S.normalized(rules, w)},
                        w, np.array([True, False, False]), np.array([0.4, 0.7, 0.7]), {})


def test_partition_conserves_every_national_receipt():
    status = toy()
    for rule in ("raw", "rules_only"):
        for lid in S.LINE_KEYS:
            amount = 0.0
            for mask in (np.array([1, 0, 0]), np.array([0, 1, 1])):
                cw = status.weights * mask
                amount += status.receipt_amount({"cps_w": cw, "population": cw.sum()}, lid, 2573.0, rule)
            assert abs(amount - 2573) <= 1e-6


def test_unauthorized_earnings_fall_and_other_records_share_remainder():
    status = toy()
    first = {"cps_w": np.array([2.0, 0, 0]), "population": 2.0}
    lawful = {"cps_w": np.array([0, 3.0, 5.0]), "population": 8.0}
    assert status.receipt_amount(first, "employee_oasdi", 100) < status.receipt_amount(first, "employee_oasdi", 100, "raw")
    assert status.receipt_amount(lawful, "employee_oasdi", 100) > status.receipt_amount(lawful, "employee_oasdi", 100, "raw")


def test_ratio_method_rejected_instead_of_silent_summary_fallback():
    with pytest.raises(SystemExit, match="row13 ratio"):
        toy().shares({"cps_w": np.ones(3), "population": 3}, "b_matched_over_pooled")


def test_scenario_weight_conservation_is_required():
    with pytest.raises(SystemExit, match="population"):
        toy().shares({"cps_w": np.ones(3), "population": 10})


def test_source_alignment_accepts_reorder_and_rejects_duplicate_or_missing():
    ids = pd.DataFrame({"PH_SEQ": [10, 10, 20], "PPPOS": [1, 2, 1]})
    rough = ids.drop(columns="PPPOS").assign(SPM_ID=[1, 1, 2], A_AGE=[20, 21, 30], PRCITSHP=1,
                                             PENATVTY=57, FEDTAX_AC=[100, 200, 300], STATETAX_A=10)
    source = rough.assign(PPPOS=ids.PPPOS).iloc[[2, 0, 1]]
    assert S.align_source(source, ids, rough).FEDTAX_AC.tolist() == [100, 200, 300]
    with pytest.raises(SystemExit, match="incomplete"):
        S.align_source(source.iloc[:2], ids, rough)
    with pytest.raises(SystemExit, match="duplicate"):
        S.align_source(pd.concat([source, source.iloc[:1]]), ids, rough)


def test_invalid_key_does_not_normalize():
    with pytest.raises(SystemExit, match="invalid"):
        S.normalized({"wage": np.array([0.0, -1])}, np.ones(2))
    with pytest.raises(SystemExit, match="empty"):
        S.normalized({"wage": np.zeros(2)}, np.ones(2))


def test_engine_accrual_rates_close_to_post_edit_dumps():
    cash = {"employee_oasdi": 10, "employer_oasdi": 10, "employee_hi": 3, "employer_hi": 3,
            "self_employment_oasdi_hi": 4, "federal_income_tax": 30}
    accrual = {**cash, "federal_income_tax": 28}
    def lines(receipts, ss, medicare):
        return ([{"side": "receipts", "id": k, "amount_bn": v} for k, v in receipts.items()]
                + [{"side": "spending", "id": "social_security", "amount_bn": ss},
                   {"side": "spending", "id": "medicare", "amount_bn": medicare}])
    m = SimpleNamespace(DUMP={"cash": {"low": {"lines": lines(cash, 20, 10)}},
                              "accrual": {"low": {"lines": lines(accrual, 27, 16)}}},
                        SE_SHARE=0.8, PART_A_SHARE=0.4, REL_UNION=0.5)
    p = S.engine_accrual_rates(m, "low")
    assert p["net"] * (20 + 0.8*4) == pytest.approx(27)
    assert p["part_a"] * (6 + 0.2*4) + 0.6*10 == pytest.approx(16)
    assert p["per_rel_ben"] * 20 * 0.5 == pytest.approx(2)


def test_bracket_rake_preserves_receipts_in_unaffected_cells():
    w = np.array([2., 3., 5., 7.])
    base = np.array([.01, .02, .03, .04])
    adjusted = base * np.array([.4, 1., 1., 1.])
    cells = np.array(["low", "low", "high", "high"])
    result, rows = S.rerake_cells(base, adjusted, w, cells)
    assert np.array_equal(result[2:], base[2:])
    assert result[0] < base[0] and result[1] > base[1]
    assert all(abs(row["error_share"]) < 1e-12 for row in rows)
    assert w @ result == pytest.approx(w @ base, abs=1e-12)


def test_bracket_rake_rejects_lost_support():
    with pytest.raises(SystemExit, match="empty post-status bracket"):
        S.rerake_cells(np.ones(2), np.array([0., 1.]), np.ones(2), np.array(["a", "b"]))
