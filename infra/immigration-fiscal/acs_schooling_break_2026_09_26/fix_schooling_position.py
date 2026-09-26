"""Re-run the exposed statistics of schooling_selection_position_2026_09_23 with the 2020 ACS
no-schooling step removed. The lane's own position.py is imported read-only (data, origin tables,
ridit and five-category code); nothing in that lane is written.

Exposed statistics (every ACS survey 2020 or later): the 2020-23 cohort's main row (2024 ACS),
the survey2020/2021/2023 rows, the acs2024_ref2020 row of Table 4, the 2024 column of the survivor
table, and the 2020-23 undercount rows.

Corrections (breakfix.py), applied separately by sex within each statistic's sample:
  A  phi from the lane's fixed set (arrived 1975-2009 at 20+, aged 25+, all records,
     derived/acs_break_2020.csv): phi_t = 1 - share_2019 / share_t; destination = the same
     cohort x sex's 2019 grades 1-8 distribution (the 2020-23 cohort borrows the 2015-19 cohort's)
  B  flow rates from the fixed Mexico-born population of break_anatomy.py
A positive control first re-computes every statistic uncorrected and requires the lane's
published CSVs to 5 decimals.
Output: derived/schooling_position_corrected.csv. Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/acs_schooling_break_2026_09_26/fix_schooling_position.py
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
LANE = HERE.parent / "schooling_selection_position_2026_09_23"
sys.path.insert(0, str(LANE))
sys.path.insert(0, str(HERE))
import position as P  # noqa: E402
import breakfix as B  # noqa: E402

OUT = HERE / "derived" / "schooling_position_corrected.csv"
BREAK = LANE / "derived" / "acs_break_2020.csv"
PUBLISHED = {"specs": LANE / "derived" / "position_all_specs.csv",
             "drift": LANE / "derived" / "survivor_drift.csv",
             "under": LANE / "derived" / "undercount_sensitivity.csv"}
KEEP = ["n", "wN", "ridit", "ridit_se", "q1", "q5", "position"] + [
    f"{p}_{c}" for c in P.FIVE for p in ("mig", "mex", "diff")] + [
    "diff_c1_none_primary_incomplete_se", "diff_c5_tertiary_se"]
TOL = 6e-6


def phi_a() -> dict:
    b = pd.read_csv(BREAK).set_index("acs_year").no_schooling_all
    return {int(y): float(1 - b[2019] / b[y]) for y in b.index if y >= 2020}


def dist_2019(d: pd.DataFrame, c0: int, sx: str, extra=None) -> dict:
    src = 2015 if c0 >= 2020 else c0
    g = P.cohort_rows(d, 2019, src, dict(P.COHORTS)[src])
    g = g[(g.arr_age >= 20) & (g.sex == sx)]
    if extra is not None:
        g = g[extra(g)]
    return B.weights_by_code(g.EDUCD.to_numpy(), g.PERWT.to_numpy(float))


def expand(g: pd.DataFrame, phi: float, dest: dict) -> pd.DataFrame:
    none = g.EDUCD.eq(2)
    keep = g.copy()
    keep["PERWT"] = keep.PERWT.astype(float)
    keep.loc[none, "PERWT"] = keep.loc[none, "PERWT"] * (1 - phi)
    parts, base = [keep], g[none]
    for code, s in dest.items():
        m = base.copy()
        m["EDUCD"] = code
        m["lo"], m["hi"] = P.EDUCD[code]
        m["PERWT"] = base.PERWT.astype(float) * phi * s
        parts.append(m)
    return pd.concat(parts, ignore_index=True)


def correct(g: pd.DataFrame, method: str, d: pd.DataFrame, c0: int, rates: dict, phis: dict, meta: list,
            extra=None) -> pd.DataFrame:
    if method == "none":
        return g
    years = set(g.YEAR.unique().tolist())
    B.gate(len(years) == 1 and min(years) >= 2020, f"[BLOCKED] correction asked for survey {years}")
    y = years.pop()
    parts = []
    for sx in ("H", "M"):
        gs = g[g.sex == sx]
        if method == "A":
            phi, dest = phis[y], B.split_a(dist_2019(d, c0, sx, extra), "educd")
        else:
            phi, dest = B.split_b(B.weights_by_code(gs.EDUCD.to_numpy(), gs.PERWT.to_numpy(float)), rates, "educd")
        w = gs.PERWT.to_numpy(float)
        meta.append({"cohort0": c0, "survey": y, "sex": sx, "method": method, "phi": phi,
                     "none_share": float(w[gs.EDUCD.to_numpy() == 2].sum() / w.sum()),
                     "moved_share": phi * float(w[gs.EDUCD.to_numpy() == 2].sum() / w.sum()),
                     "dest_mean_years": B.mean_years(dest, "educd"),
                     "dest_c1": sum(v for k, v in dest.items() if P.EDUCD[k][1] <= 5),
                     "dest_c2": sum(v for k, v in dest.items() if 6 <= P.EDUCD[k][0] <= 8),
                     "dest_c3": sum(v for k, v in dest.items() if P.EDUCD[k][0] >= 9)})
        parts.append(expand(gs, phi, dest))
    return pd.concat(parts, ignore_index=True)


def main() -> None:
    origin = P.Origin(LANE / "derived" / "origin_levels.csv")
    d = P.load_migrants()
    emp = P.empirical_splits(d)
    rates = B.flow_rates("mexico_born", "fixed")
    phis = phi_a()
    rows, meta, under = [], [], []

    def run(table, g, c0, survey, rule, method, extra=None):
        gc = correct(g, method, d, c0, rates, phis, meta, extra)
        for sx in ("P", "H", "M"):
            gg = gc if sx == "P" else gc[gc.sex == sx]
            r = P.summarize(gg, origin, emp, c0, rule)
            rows.append({"table": table, "cohort": f"{c0}-{dict(P.COHORTS)[c0]}", "survey": survey, "sex": sx,
                         "rule": rule, "method": method, **{k: r[k] for k in KEEP}})
        return gc

    for method in ("none", "A", "B"):
        for c0, survey, table in ((2020, 2024, "main"), (2015, 2020, "survey2020"), (2015, 2021, "survey2021"),
                                  (2020, 2023, "survey2023")):
            g = P.cohort_rows(d, survey, c0, dict(P.COHORTS)[c0])
            gc = run(table, g[g.arr_age >= 20], c0, survey, "nearest", method)
            if table == "main":
                for r in P.undercount(gc, origin, emp, c0):
                    under.append({"method": method, **r})
        for c0, c1 in P.COHORTS:
            g = P.cohort_rows(d, 2024, c0, c1)
            g = g[g.arr_age >= 20]
            run("acs2024_ref2020", g[2020 - g.BIRTHYR >= 20], c0, 2024, "2020", method,
                extra=lambda x: 2020 - x.BIRTHYR >= 20)
            run("survivor2024", g, c0, 2024, "nearest", method)
        print(f"method {method} done", flush=True)

    R = pd.DataFrame(rows)
    U = pd.DataFrame(under)
    # positive control: uncorrected statistics equal the lane's published outputs
    spec = pd.read_csv(PUBLISHED["specs"])
    for _, r in R[(R.method == "none") & (R.table != "survivor2024")].iterrows():
        name = r.table if r.table != "main" else "main"
        p = spec[(spec.spec == name) & (spec.cohort == r.cohort) & (spec.survey == r.survey) & (spec.sex == r.sex)]
        B.gate(len(p) == 1, f"[BLOCKED] no published row for {name} {r.cohort} {r.survey} {r.sex}")
        for k in ("ridit", "mig_c1_none_primary_incomplete", "mex_c1_none_primary_incomplete", "mig_c5_tertiary", "q1"):
            B.gate(abs(float(p.iloc[0][k]) - r[k]) <= TOL, f"[BLOCKED] control {name} {r.cohort} {r.sex} {k}: "
                   f"{r[k]:.6f} vs published {float(p.iloc[0][k]):.5f}")
    drift = pd.read_csv(PUBLISHED["drift"])
    for _, r in R[(R.method == "none") & (R.table == "survivor2024") & (R.sex == "P")].iterrows():
        p = drift[(drift.cohort == r.cohort) & (drift.survey == 2024)]
        B.gate(len(p) == 1 and abs(float(p.iloc[0].ridit) - r.ridit) <= TOL, f"[BLOCKED] drift control {r.cohort}")
    pu = pd.read_csv(PUBLISHED["under"])
    pu = pu[(pu.cohort == "2020-2023") & (pu.coding == "as coded")].set_index("k")
    for _, r in U[U.method == "none"].iterrows():
        B.gate(abs(float(pu.loc[r.k, "ridit"]) - r.ridit) <= TOL, f"[BLOCKED] undercount control k={r.k}")
    print("positive control passed: uncorrected statistics equal the published CSVs", flush=True)

    R.to_csv(OUT, index=False, float_format="%.5f", lineterminator="\n")
    U.to_csv(OUT.with_name("schooling_position_undercount_corrected.csv"), index=False, float_format="%.5f",
             lineterminator="\n")
    M = pd.DataFrame(meta).drop_duplicates()
    M.to_csv(OUT.with_name("schooling_position_correction_params.csv"), index=False, float_format="%.5f",
             lineterminator="\n")
    pd.set_option("display.width", 250)
    show = ["table", "cohort", "survey", "sex", "method", "ridit", "mig_c1_none_primary_incomplete",
            "mex_c1_none_primary_incomplete", "mig_c5_tertiary", "mex_c5_tertiary", "position"]
    print(R[R.table != "survivor2024"][show].to_string(index=False, float_format=lambda x: f"{x:.4f}"))


if __name__ == "__main__":
    main()
