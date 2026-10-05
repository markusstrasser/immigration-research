"""Gates for pension_legacy.py: the pinned 2024 BEA, Z.1 and Financial Report cells parse to the values the RESULT
records, the shares and weights are sane, and a rebuild reproduces derived/ byte for byte.

Run from the repository root (a worktree drops --no-project):
  uv run --no-project python3 -m pytest infra/immigration-fiscal/pension_legacy_2026_09_30/ -q
The inputs live in the ignored _cache/; without them the tests skip (fetch with `pension_legacy.py --fetch`).
"""
from __future__ import annotations

import csv
import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("pension_legacy", HERE / "pension_legacy.py")
pl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pl)

pytestmark = pytest.mark.skipif(not (HERE / "_cache/Section7All_xls.xlsx").exists(), reason="inputs not fetched (_cache/)")

# $bn, 2024, as published; the RESULT quotes these
BEA = {"domestic_interest_total": 1118.870, "domestic_interest_federal": 844.262, "domestic_interest_state_local": 274.608,
       "sl_imputed_interest": 162.963, "sl_plan_monetary_interest": 69.729, "sl_plan_dividends": 46.333,
       "sl_interest_accrued_on_entitlements": 442.066, "sl_actual_employer_contributions": 214.289,
       "sl_imputed_employer_contributions": -41.578, "fed_imputed_interest": 62.006, "fed_plan_monetary_interest": 89.071,
       "fed_plan_interest_total": 151.077, "fed_actual_employer_contributions": 250.510,
       "fed_imputed_employer_contributions": -144.348, "supp_state_local_retirement": 192.994,
       "defense_comp_civilian": 132.631, "defense_comp_military": 207.101, "nondefense_comp": 267.716}
Z1 = {(2023, "FL223073045.Q"): 3125.593, (2024, "FL223073045.Q"): 3005.859, (2023, "FL224190043.Q"): 8942.670,
      (2023, "FL343073045.Q"): 1163.664, (2024, "FL343073045.Q"): 961.965, (2023, "FL344190045.Q"): 3831.670,
      (2023, "FL343069245.Q"): 2639.431}


def recorded() -> dict[str, float]:
    return {r["item"]: float(r["value_bn"]) for r in csv.DictReader(open(HERE / "derived/measured_2024.csv"))}


def test_bea_cells_parse_to_recorded_values():
    m, extra = pl.measure_bea()
    rec = recorded()
    for k, want in BEA.items():
        assert m[k][0] == pytest.approx(want, abs=5e-7), k
        assert rec[k] == pytest.approx(want, abs=5e-7), k
    assert any("actuarial liabilities" in n for n in extra["notes"]["T3.3"])
    # the pension parts of the row the case holds at zero
    assert m["sl_imputed_interest"][0] + m["fed_imputed_interest"][0] + m["fed_plan_monetary_interest"][0] == pytest.approx(314.040, abs=5e-7)
    # normal cost sits in compensation: T7.8's state-local retirement = DB normal cost + DC contributions (T7.25 line 8, 20.283)
    assert BEA["sl_actual_employer_contributions"] + BEA["sl_imputed_employer_contributions"] + 20.283 == pytest.approx(BEA["supp_state_local_retirement"], abs=1e-9)
    # S&L plan interest accrued = monetary + dividends + imputed + implied funding from holding gains (T7.24 line 30, 163.041)
    assert 69.729 + 46.333 + 162.963 + 163.041 == pytest.approx(442.066, abs=1e-9)


def test_z1_and_financial_report_parse():
    z = pl.measure_z1()
    for (y, code), want in Z1.items():
        assert z[y][code] == pytest.approx(want, abs=5e-7), (y, code)
    fr = pl.measure_fr()
    assert fr["pension_interest_fy24"] == {"civilian": 75.3, "military": 75.7, "total": 151.0}
    assert fr["opeb_end_fy24"] == {"civilian": 443.1, "military": 1297.8, "total": 1740.9}
    assert fr["opeb_interest_fy24"] == {"civilian": 12.2, "military": 33.3, "total": 45.5}
    census = pl.measure_census_counts()
    assert census[2000] == pytest.approx(20.640711) and census[2010] == pytest.approx(31.798258)
    assert round(census[1990], 1) == 13.5


def test_shares_and_weights_are_sane():
    m, extra = pl.measure_bea()
    mix = pl.function_mixes(pl.measure_aspep(), m)
    for plan, d in mix.items():
        assert sum(d.values()) == pytest.approx(1.0, abs=1e-12), plan
        assert all(w >= 0 for w in d.values())
    assert 0.45 < mix["state_local"]["education_services"] < 0.55          # teachers dominate
    assert 0.15 < mix["state_local"]["public_order_safety"] < 0.20        # police, fire, courts, corrections
    share, response = pl.group_shares()
    for g in pl.GROUPS:
        for e in ("low", "high"):
            assert all(0 < s < 0.3 for s in share[g][e].values()), (g, e)
    assert response["low"]["defense"] == 0 and response["high"]["defense"] == 0
    assert share["mexican_origin"]["low"]["education_services"] == pytest.approx(0.157111, abs=5e-7)   # rekey_line_shares_sept29
    rel, _ = pl.headcount_path(extra["population"], pl.measure_census_counts())
    assert rel[2024] == 1.0 and all(0 < rel[y] <= 1.0 + 1e-12 for y in rel if y < 2024)
    factors, weights = pl.time_factors(rel, extra["population"], pl.measure_z1())
    for (plan, arm), w in weights.items():
        if arm.startswith("vintage"):
            assert min(w.values()) >= 0
        assert 0.3 < factors[plan][arm] < 1.0, (plan, arm)


def test_rebuild_reproduces_derived(tmp_path):
    run = subprocess.run([sys.executable, str(HERE / "pension_legacy.py"), "--out-dir", str(tmp_path)],
                         capture_output=True, text=True, env={**os.environ, "OPENBLAS_NUM_THREADS": "1"})
    assert run.returncode == 0, run.stderr[-2000:]
    names = sorted(p.name for p in (HERE / "derived").iterdir() if p.is_file())   # later cases sit in derived/<case>/
    assert sorted(p.name for p in tmp_path.iterdir()) == names
    assert [n for n in names if (tmp_path / n).read_bytes() != (HERE / "derived" / n).read_bytes()] == []
    for n in names:
        assert b"\r\n" not in (HERE / "derived" / n).read_bytes(), n


@pytest.mark.parametrize("corruption", ["published_count", "response", "nonfinite", "duplicate"])
def test_group_export_rejects_wrong_frame_or_line(corruption, monkeypatch, tmp_path):
    with pl.GROUP_LINES.open() as f:
        reader = csv.DictReader(f)
        fields, rows = reader.fieldnames, list(reader)
    group = "A1_third_plus_nh_white"
    target = next(r for r in rows if r["group"] == group and r["basis"] == "accrual"
                  and r["end"] == "low" and r["line"] == "education_services")
    if corruption == "published_count":
        population = next(r for r in rows if r["group"] == group and r["basis"] == "accrual"
                          and r["end"] == "low" and r["line"] == "population")
        population["amount_bn"] = "40900000"
    elif corruption == "response":
        target["response"] = "0"
    elif corruption == "nonfinite":
        target["amount_bn"] = "nan"
    else:
        rows.append(target.copy())
    path = tmp_path / "group_lines.csv"
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    monkeypatch.setattr(pl, "GROUP_LINES", path)
    with pytest.raises(ValueError, match=r"\[BLOCKED\]"):
        pl.group_shares()


def test_same_keys_pension_gap_uses_row4_and_differs_from_engine():
    share, _ = pl.group_shares()
    # Source anchors independently reconstructed from the current row-4 CPS/MEPS export.
    rows = list(csv.DictReader(open(HERE / "derived/summary.csv")))
    def interest(group, end):
        return float(next(r["interest_total_bn"] for r in rows
                          if r["arm"] == "adopted" and r["group"] == group and r["end"] == end))
    for end in ("low", "high"):
        assert share["A1_third_plus_nh_white"][end]["education_services"] < 0.103
        assert interest("mexican_origin_rough_minus_A1_white", end) == pytest.approx(
            interest("mexican_origin_rough", end) - interest("A1_third_plus_nh_white", end), abs=2e-6)
        assert interest("mexican_origin_minus_A1_white", end) > interest("mexican_origin_rough_minus_A1_white", end)
    assert interest("mexican_origin_rough_minus_A1_white", "low") == pytest.approx(4.8918, abs=0.0001)
    assert interest("mexican_origin_rough_minus_A1_white", "high") == pytest.approx(4.6828, abs=0.0001)
