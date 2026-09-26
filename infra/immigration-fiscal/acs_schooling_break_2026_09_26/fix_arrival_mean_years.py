"""Re-compute arrival_cohorts_2026_09_18/origin_relative.py's mean years at entry with the 2020 ACS
no-schooling step removed from its 2023 point (the only post-2019 survey in its IPUMS panel).

The lane maps harmonised EDUC to years {1: 2.5, 2: 6.5, 3: 9, ...} and has no entry for EDUC 0
("N/A or no schooling"), so no-schooling reports are dropped from the mean. The step therefore
removes people who would have been scored 2.5-9 years and raises the 2023 mean. Corrections:
  A  phi = 1 - share_2019 / share_2023 for no-schooling reports among the Mexico-born 20-64
     (return_vs_us_stayers_2026_09_26/derived/acs_no_schooling_break.csv), returned to the grades 1-8
     distribution of 2019's recent arrivals (0-5 years in the US, 25-54, IPUMS extract 3)
  B  flow rates of break_anatomy.py (fixed Mexico-born population) on the 2023 group's own EDUCD mix
Also shown, as an adjacent check rather than a break correction: EDUC 0 scored as 0 years in every
survey. A positive control re-computes the published series first. Since 2026-09-26 the lane scores
EDUC 0 at 0 (its YRS map gained the key after this lane found the drop), so the control reproduces
the "scored 0" rule; the dropped rule is kept below for the record.
Output: derived/arrival_mean_years_corrected.csv. Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/acs_schooling_break_2026_09_26/fix_arrival_mean_years.py
"""
import sys
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "infra/immigration-fiscal/build"))
import breakfix as B  # noqa: E402
import paths  # noqa: E402

LANE = ROOT / "infra/immigration-fiscal/arrival_cohorts_2026_09_18"
PUBLISHED = LANE / "derived/origin_relative_mean_years.csv"
BREAK_SERIES = ROOT / "infra/immigration-fiscal/return_vs_us_stayers_2026_09_26/derived/acs_no_schooling_break.csv"
EXTRACT3 = ROOT / "sources/immigration-fiscal/derived/ipums_usa/usa_00003_census1980-2000+acs2005-2024_mexborn.parquet"
YRS = {1: 2.5, 2: 6.5, 3: 9, 4: 10, 5: 11, 6: 12, 7: 13, 8: 14, 9: 15, 10: 16, 11: 18}  # the lane's map
EDUC_OF = {11: 1, 12: 1, 14: 1, 15: 1, 16: 1, 17: 1, 22: 2, 23: 2, 25: 2, 26: 2, 30: 3, 40: 4, 50: 5, 61: 6}
INEGI_GAIN_2000_2020 = 2.20  # the lane's INEGI 15+ series, 7.5 -> 9.7


def recent(d: pd.DataFrame, year: int) -> pd.DataFrame:
    g = d[d.YEAR == year]
    ysm = g.YEAR - g.YRIMMIG
    return g[(ysm >= 0) & (ysm <= 5)]


def mean_years(g: pd.DataFrame, none_years: float | None) -> float:
    y = g.EDUC.map(YRS)
    if none_years is not None:
        y = y.where(g.EDUC != 0, none_years)
    m = y.notna()
    return float(np.average(y[m], weights=g.PERWT[m]))


def corrected_2023(g: pd.DataFrame, phi: float, dest: dict, none_years: float | None) -> float:
    none = g.EDUCD.eq(2)
    base = g.copy()
    base["PERWT"] = base.PERWT.astype(float)
    base.loc[none, "PERWT"] *= (1 - phi)
    moved = []
    for code, s in dest.items():
        m = g[none].copy()
        m["EDUCD"], m["EDUC"] = code, EDUC_OF[code]
        m["PERWT"] = m.PERWT.astype(float) * phi * s
        moved.append(m)
    return mean_years(pd.concat([base] + moved, ignore_index=True), none_years)


def main() -> None:
    con = duckdb.connect(str(paths.microdata_duckdb_path()), read_only=True)
    d = con.execute("""SELECT YEAR, AGE, YRIMMIG, EDUC, EDUCD, PERWT FROM ipums_usa_borjas_panel
                       WHERE BPL = 200 AND AGE BETWEEN 25 AND 54 AND YRIMMIG > 0""").fetchdf()
    con.close()
    pub = pd.read_csv(PUBLISHED).set_index("survey_year")
    for y in pub.index:
        v = mean_years(recent(d, y), 0.0)
        B.gate(abs(v - pub.loc[y, "migrant_mean_years_at_entry"]) < 1e-9, f"[BLOCKED] control {y}: {v}")
    print("positive control passed: published mean years reproduced", flush=True)

    s = pd.read_csv(BREAK_SERIES).set_index("acs_year").no_schooling_share
    phi_a = float(1 - s[2019] / s[2023])
    x = pd.read_parquet(EXTRACT3, columns=["YEAR", "AGE", "YRIMMIG", "EDUCD", "PERWT"])
    x = x[(x.AGE.between(25, 54)) & (x.YRIMMIG > 0)]
    r19 = recent(x, 2019)
    dest_a = B.split_a(B.weights_by_code(r19.EDUCD.to_numpy(), r19.PERWT.to_numpy(float)), "educd")
    g23 = recent(d, 2023)
    B.gate(set(g23.EDUCD.unique()) - {0, 1, 999} <= set(range(2, 117)), "[BLOCKED] unexpected EDUCD")
    phi_b, dest_b = B.split_b(B.weights_by_code(g23.EDUCD.to_numpy(), g23.PERWT.to_numpy(float)),
                              B.flow_rates("mexico_born", "fixed"), "educd")
    w = g23.PERWT.to_numpy(float)
    none_share = float(w[g23.EDUCD.to_numpy() == 2].sum() / w.sum())

    rows = []
    for rule, ny in (("lane: EDUC 0 dropped", None), ("adjacent: EDUC 0 scored 0", 0.0)):
        series = {y: mean_years(recent(d, y), ny) for y in (1980, 1990, 2000, 2010)}
        for method, v23 in (("none", mean_years(g23, ny)), ("A", corrected_2023(g23, phi_a, dest_a, ny)),
                            ("B", corrected_2023(g23, phi_b, dest_b, ny))):
            rows.append({"scoring": rule, "method": method, **{f"mean_{y}": v for y, v in series.items()},
                         "mean_2023": v23, "gain_2000_2023": v23 - series[2000],
                         "minus_inegi_gain": v23 - series[2000] - INEGI_GAIN_2000_2020,
                         "phi": {"none": 0.0, "A": phi_a, "B": phi_b}[method], "none_share_2023": none_share,
                         "dest_mean_years": {"none": np.nan, "A": B.mean_years(dest_a, "educd"),
                                             "B": B.mean_years(dest_b, "educd")}[method]})
    R = pd.DataFrame(rows)
    R.to_csv(HERE / "derived" / "arrival_mean_years_corrected.csv", index=False, float_format="%.5f",
             lineterminator="\n")
    pd.set_option("display.width", 200)
    print(R.to_string(index=False, float_format=lambda v: f"{v:.4f}"))


if __name__ == "__main__":
    main()
