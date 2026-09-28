"""CPS counts the social rows' lanes use, under the published weights and under audit row 4's weights.

The adopted fiscal case charges its lines for the row-4 union (39,712,493 people in a civilian frame of
335,543,722); the social rows' lanes read the published union (40,896,574 of 336,727,803). This script
tabulates, under both weight sets, every CPS count those lanes read: the union by age, the union and all
civilian residents of Hispanic origin, the civilian frame, and uninsured person-years.

Frame and weights are the account's own, imported read-only: `generation_account_2026_09_24/frame.py`
(the cached ASEC 2025 person frame and the canonical union) and
`cps_imputation_keys_2026_09_23/combine_onbooks_lane.py` `weight_arms`, arm "row4" (Mexico-born naturalized
and noncitizen persons outside CA+TX scaled to their ACS 2024 cells; no weight moves to anyone else). Only
the full-sample weight and replicate 1 are passed: every step of `weight_arms` acts column by column, and
it needs a second column for its replicate printout.

Gates (exit 1, nothing written): the published counts reproduce
crime_victim_cost_2026_09_23/derived/target_population_cps2025.csv (0.5 persons); the row-4 union, its 12+
and 18+ counts and the civilian frame reproduce main_case_decomposition_2026_09_29/derived/age_bins.csv
(1e-6 relative); uninsured person-years reproduce the same file's `extra|exposure_py` (1e-6 relative).
Writes derived/frame_counts.csv. Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project --offline python3 infra/immigration-fiscal/population_basis_2026_09_29/frame_counts.py
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # read-only imports from other lanes: write nothing beside them

import csv  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
sys.path.insert(0, str(FISCAL / "generation_account_2026_09_24"))
import frame as F  # noqa: E402  (puts the CPS lane on sys.path)
import combine_onbooks_lane as L  # noqa: E402

TARGET_POP = FISCAL / "crime_victim_cost_2026_09_23/derived/target_population_cps2025.csv"
AGE_BINS = FISCAL / "main_case_decomposition_2026_09_29/derived/age_bins.csv"
OUT = HERE / "derived" / "frame_counts.csv"
FAILS: list[str] = []


def gate(label, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'} {label}{' — ' + detail if detail else ''}", flush=True)
    if not ok:
        FAILS.append(label)


def main():
    print("[frame]", flush=True)
    d = F.load()
    civ, union, gens = F.masks(d)
    W = d[F.REPS[:2]].to_numpy(float)
    print("[row 4 weights]", flush=True)
    arms, info = L.weight_arms(d, W, L.acs_cells())
    weights = {"published": W[:, 0], "row4": arms["row4"][:, 0]}
    del arms

    age = d.A_AGE.to_numpy()
    hisp = d.PEHSPNON.eq(1).to_numpy()
    exposure = d.NOCOV_CYR.eq(3).to_numpy(float) + 0.5 * d.NOCOV_CYR.eq(2).to_numpy(float)
    ones = np.ones(len(d))
    ages = {"all": age >= 0, "0_11": age < 12, "12_17": (age >= 12) & (age < 18), "12_plus": age >= 12,
            "18_plus": age >= 18, "0_17": age < 18, "5_17": (age >= 5) & (age < 18)}
    masks = {"union": union, "union_hispanic": union & hisp, "mexico_born": gens["G1"],
             "cps_hispanic_civilian": civ & hisp, "cps_all_civilian": civ}
    rows = []
    for name, m in masks.items():
        for band, a in ages.items():
            v = {w: float(wv[m & a] @ ones[m & a]) for w, wv in weights.items()}
            rows.append(dict(count=f"{name}|{band}", **v))
    for name, m in (("union", union), ("cps_all_civilian", civ)):
        v = {w: float(wv[m] @ exposure[m]) for w, wv in weights.items()}
        rows.append(dict(count=f"{name}|uninsured_person_years", **v))
    got = {r["count"]: r for r in rows}

    print("[gates]", flush=True)
    tp = pd.read_csv(TARGET_POP).set_index("group")
    col = {"all": "all_ages", "0_11": "age_0_11", "12_17": "age_12_17", "12_plus": "age_12_plus", "18_plus": "age_18_plus"}
    worst = 0.0
    for group in ("union", "mexico_born", "cps_hispanic_civilian", "cps_all_civilian", "union_hispanic"):
        for band, c in col.items():
            worst = max(worst, abs(got[f"{group}|{band}"]["published"] - float(tp.loc[group, c])))
    gate("published counts reproduce target_population_cps2025.csv (5 groups x 5 age bands)", worst < 0.5,
         f"worst difference {worst:.3f} persons")
    ab = pd.read_csv(AGE_BINS)
    pop = ab[(ab.key == "extra|pop") & (ab.allocation == "both")]
    for w in weights:
        p = pop[pop.weights == w]
        for band, lo in (("all", 0), ("12_plus", 12), ("18_plus", 18)):
            want = float(p[p.bin >= lo].union.sum())
            gate(f"{w} union {band} reproduces age_bins.csv", abs(got[f"union|{band}"][w] / want - 1) < 1e-6,
                 f"{got[f'union|{band}'][w]:,.1f} vs {want:,.1f}")
        want = float(p.national.sum())
        gate(f"{w} civilian frame reproduces age_bins.csv", abs(got["cps_all_civilian|all"][w] / want - 1) < 1e-6,
             f"{got['cps_all_civilian|all'][w]:,.1f} vs {want:,.1f}")
        e = ab[(ab.key == "extra|exposure_py") & (ab.weights == w) & (ab.allocation == "personal")]
        for name, colname in (("union", "union"), ("cps_all_civilian", "national")):
            want = float(e[colname].sum())
            gate(f"{w} {name} uninsured person-years reproduce age_bins.csv",
                 abs(got[f"{name}|uninsured_person_years"][w] / want - 1) < 1e-6,
                 f"{got[f'{name}|uninsured_person_years'][w]:,.1f} vs {want:,.1f}")
    removed = {k: got[k]["published"] - got[k]["row4"] for k in ("union|all", "cps_all_civilian|all",
                                                                  "cps_hispanic_civilian|all", "mexico_born|all")}
    gate("row 4 removes the same people from the union, the civilian frame and the Mexico-born",
         max(abs(removed[k] - removed["union|all"]) for k in ("cps_all_civilian|all", "mexico_born|all")) < 0.5,
         f"{removed['union|all']:,.1f} persons")
    gate("row 4 moves no weight outside the union", abs(got["cps_all_civilian|all"]["published"] - got["union|all"]["published"]
                                                      - got["cps_all_civilian|all"]["row4"] + got["union|all"]["row4"]) < 0.5)
    print(f"  row-4 factors: naturalized {info['factor_natz']:.6f}, noncitizen {info['factor_noncit']:.6f}", flush=True)
    if FAILS:
        print(f"FAIL: {len(FAILS)} gate(s): {FAILS}")
        sys.exit(1)

    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", newline="") as handle:
        out = csv.writer(handle, lineterminator="\n")
        out.writerow(["count", "published", "row4", "ratio"])
        for r in rows:
            out.writerow([r["count"], f"{r['published']:.4f}", f"{r['row4']:.4f}", f"{r['row4'] / r['published']:.9f}"])
    for r in rows:
        print(f"  {r['count']:44s} {r['published']:>16,.1f} {r['row4']:>16,.1f} {r['row4'] / r['published']:.6f}")
    print(f"  wrote {len(rows)} counts -> {OUT.relative_to(FISCAL)}")


if __name__ == "__main__":
    main()
