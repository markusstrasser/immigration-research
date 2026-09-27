"""Test 4: do NAEP exclusion rates move with the English-learner, Hispanic or immigrant share?

Outcomes (inclusion/derived/naep_inclusion.csv, from the NAEP technical appendices):
  el_excluded_pct_identified  excluded ELs as a percent of identified ELs (the exclusion policy margin)
  el_excluded_pct_all         excluded ELs as a percent of all pupils ("#" below 0.5 stored as 0)
  sd_excluded_pct_all         excluded pupils with disabilities, percent of all pupils
  sdel_excluded_pct_all       all excluded pupils, percent of all pupils
Also bounds how much exclusion could move the state means used in Test 2.

Writes derived/exclusion_estimates.csv and derived/exclusion_means.csv. Run from the repository root:
    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/school_systemwide_2026_09_27/analysis_exclusion.py
"""
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from analysis_naep import FIELDS, TREAT, record, stack, write  # noqa: E402
from panel import ALL_YEARS, MAIN_YEARS, build  # noqa: E402
from stats_util import ols  # noqa: E402

OUT = HERE / "derived"
OUTCOMES = ["el_excluded_pct_identified", "el_excluded_pct_all", "sd_excluded_pct_all", "sdel_excluded_pct_all"]


def main():
    p = build()
    rows = []
    for tkey in ("el", "hisp", "imm"):
        col = TREAT[tkey][0]
        yrs = [y for y in MAIN_YEARS if y >= (2007 if tkey == "imm" else 2003)]
        for outcome in OUTCOMES:
            for spec, years in (("twfe", yrs), ("twfe_with_2022_2024", [y for y in ALL_YEARS if y >= yrs[0]])):
                d = stack(p, years, "white")  # builds the FE keys; the outcome is set below
                res = ols(d, outcome, [col], fe=["cell_state", "cell_year"], cluster="state")
                record(rows, res, col, test="exclusion", spec=spec, treatment=tkey, outcome=outcome, cell="pooled",
                       units="percentage points", years=f"{min(years)}-{max(years)}",
                       note="state-by-cell and cell-by-year FE")
            d = stack(p, yrs, "white")
            res = ols(d, outcome, [col], fe=["cell_state", "cell_year", "region_cell_year"], cluster="state")
            record(rows, res, col, test="exclusion", spec="twfe_region_year", treatment=tkey, outcome=outcome,
                   cell="pooled", units="percentage points", years=f"{min(yrs)}-{max(yrs)}",
                   note="adds region-by-cell-by-year FE")
    # Does controlling for exclusion change the Test 2 white-pupil estimate?
    for tkey in ("el", "hisp"):
        col = TREAT[tkey][0]
        d = stack(p, MAIN_YEARS, "white")
        for ctrl in (["sd_excluded_pct_all"], ["sdel_excluded_pct_all"]):
            res = ols(d, "z", [col] + ctrl, fe=["cell_state", "cell_year"], cluster="state")
            record(rows, res, col, test="naep_exclusion_control", spec="twfe_ctrl_" + ctrl[0], treatment=tkey,
                   outcome="white", cell="pooled", units="SD", years="2003-2019",
                   note=f"Test 2 white-pupil TWFE with {ctrl[0]} as a control")
    write(OUT / "exclusion_estimates.csv", sorted(rows, key=lambda r: (r["test"], r["treatment"], r["outcome"], r["spec"])),
          FIELDS)
    # national-public trend and state spread of EL exclusion, by cell and year
    q = p[p.year.isin(ALL_YEARS)]
    m = q.groupby(["cell", "year"]).agg(
        el_identified_mean=("el_identified_pct_all", "mean"),
        el_excl_pct_identified_mean=("el_excluded_pct_identified", "mean"),
        el_excl_pct_identified_max=("el_excluded_pct_identified", "max"),
        sd_excl_pct_all_mean=("sd_excluded_pct_all", "mean"),
        sdel_excl_pct_all_mean=("sdel_excluded_pct_all", "mean"),
        n_states=("state", "nunique")).reset_index().round(3)
    m.to_csv(OUT / "exclusion_means.csv", index=False, lineterminator="\n")
    print(f"estimates={len(rows)}")


if __name__ == "__main__":
    main()
