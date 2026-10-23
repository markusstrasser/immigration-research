"""Gates and positive controls for the school-capital-where-enrolled lane (reads derived/, plus raw F-33 for one district).

1. Every build gate passed, and the national calibration ratio against BEA's $2,723.9bn is printed and within 5%.
2. Chain coverage: at least 0.98 of FY1992-2024 real construction sits in IDs present in FY2024 (the threshold: the
   unchained 1-2% are merged or closed districts, and moving them within their state shifts R_K by under 0.001,
   the realloc variant).
3. R_K finite and in a plausible band for every concept and arm.
4. Arms ordered as expected, or explained: under the FY2000 start arm b >= arm a; under the FY1992 start arm b < arm a
   only because the measured FY1992-1999 vintages put the group below national (relative < 1), which arm b extends
   back to older vintages.
5. Hand check, none of the lane's code: Los Angeles Unified's FY1992-2024 structures stock, rebuilt from the raw F-33
   F12 column with the price and rate in summary.json/national_flows.csv, equals top_group_districts.csv.
6. Every derived CSV is LF-only; the headline in summary.json equals its dollars.csv row.

    uv run --no-project python3 -m pytest infra/immigration-fiscal/school_capital_where_enrolled_2026_10_24/test_lane.py -q
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
OUT = HERE / "derived"
FISCAL = HERE.parent
S = json.loads((OUT / "summary.json").read_text())
MAIN = "mexican_district_share"


def test_all_build_gates_pass():
    g = pd.read_csv(OUT / "gates.csv")
    assert len(g) >= 20
    assert g["pass"].all(), g[~g["pass"]].to_string()
    assert S["gates_failed"] == []


def test_national_calibration_printed_and_close():
    for key in ("calibration", "calibration_fy2000_start"):
        c = S[key]
        print(f"{key}: F-33 PIM / BEA same vintages {c['post_start_structures_f33_over_bea_same_vintages']:.4f}; "
              f"total / BEA ${c['bea_k12_total_bn']:,.1f}bn {c['total_capital_f33_proportional_over_bea']:.4f}")
        assert abs(c["bea_k12_total_bn"] - 2723.9195) < 1e-3
        assert 0.95 <= c["post_start_structures_f33_over_bea_same_vintages"] <= 1.05
        assert 0.95 <= c["total_capital_f33_proportional_over_bea"] <= 1.05


def test_chain_coverage():
    ch = S["chain"]
    assert ch["chained_share_real_f12"] >= 0.98
    assert ch["chained_share_structures_stock_2024"] >= 0.98
    assert ch["chained_share_real_f12_before_2000"] >= 0.97
    assert S["coverage"]["group_pupils"] >= 0.85
    # moving unchained flows within their state barely moves R_K: the threshold is not doing the work
    r = S["R_K_mexican_district_share"]
    for arm in ("a", "b"):
        assert abs(r[f"structures_{arm}"]["C_district"] - r[f"structures_{arm}_realloc"]["C_district"]) < 0.002


def test_r_k_finite():
    for block in ("R_K_mexican_district_share", "R_K_mexican_district_share_fy2000_start"):
        for concept, fams in S[block].items():
            for fam, v in fams.items():
                assert np.isfinite(v) and 0.5 < v < 2.0, (block, concept, fam, v)
    rk = pd.read_csv(OUT / "r_k_by_concept.csv")
    assert rk.R.notna().all() and np.isfinite(rk.R).all()


def test_arms_ordered_or_explained():
    ao = S["arm_order"]
    assert ao["FY2000"]["b_ge_a"]
    v = ao["vintages_FY1992_1999"]
    if not ao["FY1992"]["b_ge_a"]:
        # the measured 1992-1999 vintages sit below national; arm b's FY1992-1996 intensity carries that back
        assert v["relative_C"] < 1.0
        assert ao["FY1992"]["pre_relative_arm_b"] < ao["FY1992"]["pre_relative_arm_a"] < 1.0
    # the measured relative of the 1992-1999 vintages lies below what the FY2000-start arm a assumed for them
    assert v["relative_C"] < ao["FY2000"]["pre_relative_arm_a"]


def test_hand_check_los_angeles_structures():
    lausd = "0622710"
    nat = pd.read_csv(OUT / "national_flows.csv").set_index("year")
    ds = S["rates"]["structures"]
    pre = HERE / "_cache" / "f33_pre2000"
    f33 = FISCAL / "school_dilution_2026_09_24" / "_cache" / "f33"
    total = 0.0
    for y in range(1992, 2025):
        if y < 2000:
            fn = pre / ("elsec99_xls.csv" if y == 1999 else f"elsec{y % 100:02d}.txt")
        else:
            fn = f33 / (f"elsec{y % 100:02d}_xlsx.csv" if y == 2022 else f"elsec{y % 100:02d}.txt")
        d = pd.read_csv(fn, dtype=str, index_col=False, encoding="latin-1", keep_default_na=False,
                        usecols=lambda c: c in {"NCESID", "F12"})
        f12 = pd.to_numeric(d.loc[d.NCESID.str.strip() == lausd, "F12"], errors="coerce").fillna(0).clip(lower=0).sum() * 1000
        price = nat.structures_price_fy[2024] / nat.structures_price_fy[y]
        total += f12 * price * (1 - ds) ** (2024 - y) * (1 - ds / 2)
    top = pd.read_csv(OUT / "top_group_districts.csv", dtype={"id": str}).set_index("id")
    assert abs(total / 1e9 - top.loc[lausd, "fy1992_2024_structures_bn"]) < 1e-5


def test_lf_only_and_headline_consistent():
    for f in OUT.glob("*.csv"):
        assert b"\r\n" not in f.read_bytes(), f
    d = pd.read_csv(OUT / "dollars.csv")
    for arm in ("a", "b"):
        row = d[(d.variant == "primary") & (d.pre_start_arm == arm) & (d.weighting == MAIN) & (d.factor == "key_consistent_A")]
        assert len(row) == 1
        h = S["headline_key_consistent_A"][arm]
        assert abs(row.delta_low_bn.iloc[0] - h["delta_low_bn"]) < 1e-5
        assert abs(row.delta_high_bn.iloc[0] - h["delta_high_bn"]) < 1e-5
        # the factor is the capital relative over the current-spending relative the case's key already embeds
        rk = S["R_K_mexican_district_share"][f"structures_{arm}"]["A_account_state_mix"]
        assert abs(h["F_structures"] - rk / S["r_embedded_account"]) < 1e-9
    band = S["case_band_bn"]
    assert abs(band[0] - 368.03) < 0.01 and abs(band[1] - 436.56) < 0.01
