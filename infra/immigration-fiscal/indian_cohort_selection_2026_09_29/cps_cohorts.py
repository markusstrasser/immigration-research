#!/usr/bin/env python3
"""India-born adults by arrival cohort on the IPUMS-CPS ASEC 1994-2025 (selection-curve frame).

Gate: the pooled 2015-2025 India G1 mean education percentile, age-standardised to the white
reference's age mix, must equal the selection-curve lane's 73.4831 (derived/percentile_distribution.csv).

Views (civilian adults 25-64). The stock view is age-standardised to the white reference's band
mix (the selection-curve rule); the fixed-duration views to the pooled India-born view's own band
mix. Shares (BA+, graduate) use the same standardised weights:
  stock_2015_2025   every cohort as observed in 2015-2025 (durations differ across cohorts)
  ysm_0_5, ysm_6_10 each cohort at a fixed 0-5 or 6-10 years since arrival, ages 25-54
  age_35_44_ysm_10_19  fixed age band and duration
CPS reports arrival in 2-4 year intervals; a person's arrival year is the interval midpoint.

Output: derived/cps_cohorts.csv, derived/gate.json (cps part).
Run from the repo root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with duckdb --with pyarrow python3 \
      infra/immigration-fiscal/indian_cohort_selection_2026_09_29/cps_cohorts.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402

cps_curve = C.cps_curve
GATE_EDU = 73.4831


def arrival_mid(df: pd.DataFrame) -> np.ndarray:
    b = cps_curve.yrimmig_bounds()
    lo = df.yrimmig.map(lambda c: b.get(int(c), (np.nan, np.nan))[0]).to_numpy(float)
    hi = df.yrimmig.map(lambda c: b.get(int(c), (np.nan, np.nan))[1]).to_numpy(float)
    lo = np.where(lo == 1900, hi - 5, lo)       # "1949 or earlier"
    return (lo + hi) / 2


def summarise(d: pd.DataFrame, m: np.ndarray, ref_share: pd.Series, view: str, cohort: str) -> dict:
    row = {"source": "CPS ASEC", "view": view, "cohort": cohort, "n": int(m.sum())}
    if m.sum() == 0:
        return row
    for var, ok in (("p_edu", "educ_ok"), ("p_earn", "earn_ok")):
        mm = m & d[ok].to_numpy() & np.isfinite(d[var].to_numpy())
        ws = cps_curve.std_weights(d, mm, ref_share)
        mean, se = cps_curve.wmean_se(d.loc[mm, var].to_numpy(), ws)
        row[f"{var}_mean"], row[f"{var}_se"] = mean, se
    mm = m & d.educ_ok.to_numpy()
    ws = cps_curve.std_weights(d, mm, ref_share)
    e = d.loc[mm, "educ"].to_numpy()
    row["ba_plus"] = float(ws[np.isin(e, list(C.BA_PLUS))].sum() / ws.sum())
    row["graduate"] = float(ws[np.isin(e, list(C.GRAD))].sum() / ws.sum())
    w = d.loc[m, "w"].to_numpy()
    row["citizen"] = float(w[np.isin(d.loc[m, "citizen"].to_numpy(), [3, 4])].sum() / w.sum())   # 3 born abroad of US parents, 4 naturalized
    row["mean_age"] = float(np.average(d.loc[m, "age"], weights=w))
    row["mean_years_since_arrival"] = float(np.average(d.loc[m, "ysm"], weights=w))
    return row


def main() -> int:
    df = C.cps_prepared()
    # --- gate: reproduce the selection-curve lane's India G1 education percentile ---
    win = (df.year >= 2015).to_numpy()
    d = df.loc[win]
    ref = d.ref.to_numpy()
    ref_share = d.loc[ref].groupby("band").w.sum() / d.loc[ref].w.sum()
    m = ((d.gen == 1) & (d.origin == C.INDIA_CPS) & d.educ_ok).to_numpy() & np.isfinite(d.p_edu.to_numpy())
    got, _ = cps_curve.wmean_se(d.loc[m, "p_edu"].to_numpy(), cps_curve.std_weights(d, m, ref_share))
    gate = {"india_g1_edu_2015_2025": got, "selection_curve": GATE_EDU,
            "status": "PASS" if abs(got - GATE_EDU) < 5e-4 else "FAIL"}
    print(json.dumps(gate))
    if gate["status"] != "PASS":
        raise SystemExit("[BLOCKED] gate failed")

    ind = df[(df.gen == 1) & (df.origin == C.INDIA_CPS)].copy()
    ind["arr"] = arrival_mid(ind)
    ind["ysm"] = ind.year - ind.arr
    ind["cohort"] = C.cohort_of(np.floor(ind.arr.to_numpy()))
    full = pd.concat([ind, df.loc[df.ref]], ignore_index=True)
    full["is_ind"] = full.gen.eq(1) & full.origin.eq(C.INDIA_CPS)

    views = {
        "stock_2015_2025": (full.year >= 2015),
        "stock_2015_2025_age25_54": (full.year >= 2015) & full.age.between(25, 54),
        "ysm_0_5_age25_54": full.ysm.between(0, 5.5) & full.age.between(25, 54),
        "ysm_6_10_age25_54": full.ysm.between(5.6, 10.5) & full.age.between(25, 54),
        "age35_44_ysm_10_19": full.ysm.between(10, 19.5) & full.age.between(35, 44),
    }
    rows = []
    for view, vm in views.items():
        if view.startswith("stock"):
            ymask = (full.year >= 2015).to_numpy()
        else:
            ymask = np.ones(len(full), bool)
        dd = full.loc[ymask]
        base = (dd.is_ind & vm.loc[dd.index]).to_numpy()
        if view == "stock_2015_2025":
            # the selection-curve definition: the white reference's age mix (the gate's rule)
            r = dd.ref.to_numpy()
        else:
            # fixed-duration views: the pooled India-born view's own age mix, so cohorts are
            # compared at one arrival-age structure without overweighting rare older arrivals
            r = base
        rs = dd.loc[r].groupby("band").w.sum() / dd.loc[r].w.sum()
        rows.append(summarise(dd, base, rs, view, "all"))
        for _, _, lab in C.COHORTS:
            rows.append(summarise(dd, base & (dd.cohort == lab).to_numpy(), rs, view, lab))
    C.write_csv(C.DER / "cps_cohorts.csv", [r for r in rows if r["n"] > 0])
    out = pd.DataFrame([r for r in rows if r["n"] > 0])
    print(out.round(3).to_string())
    g = json.loads((C.DER / "gate.json").read_text()) if (C.DER / "gate.json").exists() else {}
    g["cps"] = gate
    (C.DER / "gate.json").write_text(json.dumps(g, indent=1, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
