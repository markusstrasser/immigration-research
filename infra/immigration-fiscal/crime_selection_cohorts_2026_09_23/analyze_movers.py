#!/usr/bin/env python3
"""US-born men 18-40 living outside their state of birth ("movers") against those living in it
("stayers"), ACS 1-year 2019, 2023 and 2024 (IPUMS extract `acs_movers_lite`).

Institutional = GQ 3. Mover = BPL (state of birth, 1-56) != STATEFIP (state of residence).
Groups: all, non-Hispanic white, non-Hispanic Black, Hispanic (any race).
Gaps are movers minus stayers in percentage points, with stayers' rates applied at movers' single
years of age (and age x education). SEs: delete-a-group jackknife over 80 household groups
(SERIAL mod 80); the extract omits replicate weights to fit a constrained link, and
analyze_acs.py reports how this jackknife compares with the replicate-weight SE on the
Mexico-born file.

Placement bias: prisoners are counted where they are held. A share f of institutionalized
stayers held outside their birth state (federal placement, transfers) is counted as movers. The
`placement_f*` columns move f of stayers' institutional count to the movers' side and back out
what the gap would be without it (f = 0.04 and 0.08, illustrative, not measured).

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/crime_selection_cohorts_2026_09_23/analyze_movers.py
Out: derived/acs_movers.csv
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from analyze_census import cells, crude, rate_vec  # noqa: E402
from cohort_lib import educ3, standardized, summarize  # noqa: E402

CACHE = HERE / "_cache"
DERIVED = HERE / "derived"


def load() -> pd.DataFrame:
    cols = ["YEAR", "SERIAL", "PERWT", "GQ", "STATEFIP", "AGE", "SEX", "BPL", "HISPAN", "RACE", "EDUC"]
    df = pd.read_csv(CACHE / "ipums" / "acs_movers_lite.csv.gz", usecols=cols)
    if not (df.SEX.eq(1).all() and df.AGE.between(18, 40).all() and df.BPL.between(1, 56).all()):
        raise SystemExit("[FAILED] acs_movers_lite case selection did not hold")
    nh = df.HISPAN == 0
    df["sub"] = np.select([nh & (df.RACE == 1), nh & (df.RACE == 2), df.HISPAN.between(1, 4)],
                          ["nhw", "nhb", "hispanic"], "other")
    df["mover"] = np.where(df.BPL == df.STATEFIP, "stayer", "mover")
    df["educ3"] = educ3(df.EDUC)
    df["inst"] = (df.GQ == 3).astype(float)
    df["corr"] = 0.0
    df["jk"] = df.SERIAL % 80
    return df


def placement_gap(mv: pd.DataFrame, st: pd.DataFrame, f: float, strata: list[str]) -> float:
    """Age-standardized gap after returning a share f of movers' institutional count to stayers,
    where that share equals f of stayers' own institutional count (full-sample weights)."""
    i_st = st.i0.sum()
    shift = f * i_st / (1 - f)  # stayers held out of state, currently counted with movers
    mv = mv.copy()
    st = st.copy()
    mv["i0"] = mv.i0 * (1 - shift / mv.i0.sum())
    st["i0"] = st.i0 * (1 + shift / i_st)
    s = standardized(mv, st, strata)
    return float(s["observed"][0] - s["expected"][0])


def main() -> None:
    df = load()
    c = cells(df, ["YEAR", "sub", "mover", "AGE", "educ3"])
    rows = []
    for year in (2019, 2023, 2024):
        cy = c[c.YEAR == year]
        for g in ("all", "nhw", "nhb", "hispanic"):
            cg = cy if g == "all" else cy[cy["sub"] == g]
            mv, st = cg[cg.mover == "mover"], cg[cg.mover == "stayer"]
            rm, sem = crude(mv)
            rs, ses = crude(st)
            diff, diff_se = summarize(rate_vec(mv) - rate_vec(st), "jk")
            s_age = standardized(mv, st, ["AGE"])
            s_edu = standardized(mv, st, ["AGE", "educ3"])
            gap_age, gap_age_se = summarize(s_age["observed"] - s_age["expected"], "jk")
            gap_edu, gap_edu_se = summarize(s_edu["observed"] - s_edu["expected"], "jk")
            rows.append(dict(year=year, source="ACS 1-year", group=g, n_movers=int(mv.n.sum()),
                             n_stayers=int(st.n.sum()), mover_share=float(mv.w0.sum() / cg.w0.sum()),
                             movers_rate=rm, movers_rate_se=sem, stayers_rate=rs, stayers_rate_se=ses,
                             crude_gap_pp=100 * diff, crude_gap_pp_se=100 * diff_se,
                             age_std_gap_pp=100 * gap_age, age_std_gap_pp_se=100 * gap_age_se,
                             age_educ_std_gap_pp=100 * gap_edu, age_educ_std_gap_pp_se=100 * gap_edu_se,
                             placement_f04_age_gap_pp=100 * placement_gap(mv, st, 0.04, ["AGE"]),
                             placement_f08_age_gap_pp=100 * placement_gap(mv, st, 0.08, ["AGE"]),
                             placement_f04_age_educ_gap_pp=100 * placement_gap(mv, st, 0.04, ["AGE", "educ3"]),
                             placement_f08_age_educ_gap_pp=100 * placement_gap(mv, st, 0.08, ["AGE", "educ3"])))
        # all US-born men 18-40: the reference the cohort ratios in analyze_acs.py hold fixed
        us_rate, us_se = crude(cy)
        rows.append(dict(year=year, source="ACS 1-year", group="us_born_reference", movers_rate=np.nan,
                         stayers_rate=np.nan, n_movers=int(cy.n.sum()), n_stayers=0,
                         mover_share=np.nan, reference_rate=us_rate, reference_rate_se=us_se))
    out = pd.DataFrame(rows)
    out.to_csv(DERIVED / "acs_movers.csv", index=False, float_format="%.6g")
    print(out[["year", "group", "movers_rate", "stayers_rate", "age_std_gap_pp", "age_std_gap_pp_se",
               "age_educ_std_gap_pp", "placement_f04_age_educ_gap_pp", "placement_f08_age_educ_gap_pp"]
              ].to_string(index=False))


if __name__ == "__main__":
    main()
