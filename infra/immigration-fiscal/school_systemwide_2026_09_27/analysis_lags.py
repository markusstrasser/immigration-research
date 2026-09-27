"""Cohort-lagged exposure (operator addendum, 2026-09-28): exposure builds up over the years a cohort
spends in school, so grade-8 scores are also related to the share when the same cohort was in grade 4
and to its average share over grades K–8, and grade-4 scores to the share at grades K–1.

For a NAEP wave in spring t the tested cohort was in grade g in fall t-1-(G-g), G = 4 or 8.
Shares:
  hisp   CCD Hispanic share of the cohort's own grade (race by grade exists from fall 1998, 34 states;
         45 in 2000, all later), and the all-grade CCD share (from 1995) as a complete proxy.
  el     NAEP-identified English learners in the same cohort at grade 4 (NAEP wave t-4), for grade 8;
         the all-grade CCD English-learner share in the K–1 years as a proxy for grade 4 (CCD counts
         have state gaps: 80 of 1,122 state-years in fall 1998–2019, CA in 2006, 2007 and 2010).
  imm    ACS children 6–17 with a foreign-born parent; ACS starts in 2006, so lags reach only the
         later waves.
Each slope is per 10 percentage points, with state-by-cell and cell-by-year FE, SEs clustered by
state; grade-8 cells (math, reading) and grade-4 cells are pooled separately, outcome in national
student SDs. Writes derived/lag_estimates.csv and derived/lag_coverage.csv.

Run from the repository root:
    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/school_systemwide_2026_09_27/analysis_lags.py
"""
import csv
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from analysis_naep import FIELDS, record, stack, write  # noqa: E402
from panel import ALL_YEARS, MAIN_YEARS, build  # noqa: E402
from stats_util import ols  # noqa: E402

OUT = HERE / "derived"


def grade_shares():
    g = pd.read_csv(HERE / "derived" / "state_grade_shares.csv")
    return {(r.state, r.fall_year, r.grade): r.hisp_share for r in g.itertuples()}


def all_grade(col):
    s = pd.read_csv(HERE / "derived" / "state_shares.csv")
    return {(r.state, r.fall_year): getattr(r, col) for r in s.itertuples() if pd.notna(getattr(r, col))}


def cohort_mean(lookup, state, years_grades):
    vals = [lookup.get(k) for k in years_grades(state)]
    return float(np.mean(vals)) if all(v is not None and np.isfinite(v) for v in vals) else np.nan


def add_measures(p):
    gs = grade_shares()
    hs = all_grade("hisp_share")
    els = all_grade("el_share_ccd")
    acs_imm = all_grade("imm_origin_share_617")
    rows = []
    for r in p.itertuples():
        t, G, s = r.year, r.grade, r.state
        f = t - 1  # fall of the tested school year
        rec = {"index": r.Index}
        rec["hisp_grade_now"] = gs.get((s, f, G), np.nan)
        # same cohort at each earlier grade g: fall f - (G - g)
        cohort = lambda st, gg: (st, f - (G - gg), gg)
        rec["hisp_k1"] = cohort_mean(gs, s, lambda st: [cohort(st, 0), cohort(st, 1)])
        rec["hisp_k_to_G"] = cohort_mean(gs, s, lambda st: [cohort(st, gg) for gg in range(0, G + 1)])
        rec["hisp_allgrade_k_to_G"] = cohort_mean(hs, s, lambda st: [(st, f - (G - gg)) for gg in range(0, G + 1)])
        rec["hisp_allgrade_k1"] = cohort_mean(hs, s, lambda st: [(st, f - G), (st, f - G + 1)])
        rec["el_ccd_k1"] = cohort_mean(els, s, lambda st: [(st, f - G), (st, f - G + 1)])
        if G == 8:
            rec["hisp_g4_lag"] = gs.get((s, f - 4, 4), np.nan)
            rec["hisp_allgrade_g4_lag"] = hs.get((s, f - 4), np.nan)
            rec["imm_g4_lag"] = acs_imm.get((s, t - 4), np.nan)
        else:
            rec["imm_k1"] = cohort_mean(acs_imm, s, lambda st: [(st, t - 5), (st, t - 4)])
        rows.append(rec)
    m = pd.DataFrame(rows).set_index("index")
    p = p.join(m)
    # the same cohort's NAEP-identified EL share in grade 4, four years earlier (same subject)
    g4 = p[p.grade == 4][["subject", "year", "state", "el_identified_pct_all"]].rename(
        columns={"el_identified_pct_all": "el_g4_lag"})
    g4["year"] = g4.year + 4
    p = p.merge(g4, on=["subject", "year", "state"], how="left")
    p.loc[p.grade == 4, "el_g4_lag"] = np.nan
    return p


# (measure, grade, label, contemporaneous comparison column)
SPECS = [
    ("hisp_grade_now", 8, "Hispanic share of the tested grade, same year (grade-specific CCD)", None),
    ("hisp_g4_lag", 8, "Hispanic share of the same cohort in grade 4, 4 years earlier (CCD)", "hisp_grade_now"),
    ("hisp_allgrade_g4_lag", 8, "All-grade Hispanic share 4 years earlier (CCD)", "hisp_share"),
    ("hisp_k_to_G", 8, "Cohort's mean Hispanic share over grades K-8 (grade-specific CCD)", "hisp_grade_now"),
    ("hisp_allgrade_k_to_G", 8, "Mean all-grade Hispanic share over the cohort's K-8 years (CCD)", "hisp_share"),
    ("el_g4_lag", 8, "Same cohort's NAEP-identified EL share in grade 4, 4 years earlier", "el_identified_pct_all"),
    ("imm_g4_lag", 8, "ACS immigrant-origin share of children 6-17, 4 years earlier", "imm_origin_share_617"),
    ("hisp_grade_now", 4, "Hispanic share of the tested grade, same year (grade-specific CCD)", None),
    ("hisp_k1", 4, "Cohort's Hispanic share in grades K-1 (grade-specific CCD)", "hisp_grade_now"),
    ("hisp_allgrade_k1", 4, "All-grade Hispanic share in the cohort's K-1 years (CCD)", "hisp_share"),
    ("hisp_k_to_G", 4, "Cohort's mean Hispanic share over grades K-4 (grade-specific CCD)", "hisp_grade_now"),
    ("el_ccd_k1", 4, "All-grade CCD English-learner share in the cohort's K-1 years", "el_identified_pct_all"),
    ("imm_k1", 4, "ACS immigrant-origin share of children 6-17 in the cohort's K-1 years", "imm_origin_share_617"),
]


def main():
    p = add_measures(build())
    rows, cover = [], []
    for measure, G, label, contemp in SPECS:
        q = p[p.grade == G]
        for window, years in (("2003-2019", MAIN_YEARS), ("2003-2024", ALL_YEARS)):
            for outcome in ("white", "nonel", "white_nonel"):
                d = stack(q, years, outcome).dropna(subset=[measure, "z"])
                if d.year.nunique() < 3 or d.state.nunique() < 20:
                    continue
                res = ols(d, "z", [measure], fe=["cell_state", "cell_year"], cluster="state")
                record(rows, res, measure, test="naep_lag", spec=f"lag_g{G}_{window}", treatment=measure,
                       outcome=outcome, cell=f"grade{G}", units="SD",
                       years=f"{d.year.min()}-{d.year.max()}", note=label)
                if outcome == "white" and window == "2003-2019":
                    cover.append({"measure": measure, "grade": G, "label": label,
                                  "waves": " ".join(str(y) for y in sorted(d.year.unique())),
                                  "n_states_min_wave": int(d.groupby("year").state.nunique().min()),
                                  "n_obs": len(d)})
                    # same sample: contemporaneous share alone, then both together
                    if contemp:
                        dd = d.dropna(subset=[contemp])
                        r0 = ols(dd, "z", [contemp], fe=["cell_state", "cell_year"], cluster="state")
                        record(rows, r0, contemp, test="naep_lag", spec=f"lag_g{G}_same_sample_contemporaneous",
                               treatment=measure, outcome=outcome, cell=f"grade{G}", units="SD",
                               years=f"{dd.year.min()}-{dd.year.max()}",
                               note=f"contemporaneous {contemp} on the lag sample")
                        r2 = ols(dd, "z", [measure, contemp], fe=["cell_state", "cell_year"], cluster="state")
                        for nm, sp in ((measure, "horse_race_lag"), (contemp, "horse_race_contemporaneous")):
                            record(rows, r2, nm, test="naep_lag", spec=f"lag_g{G}_{sp}", treatment=measure,
                                   outcome=outcome, cell=f"grade{G}", units="SD",
                                   years=f"{dd.year.min()}-{dd.year.max()}", note=f"{measure} and {contemp} together")
    write(OUT / "lag_estimates.csv", sorted(rows, key=lambda r: (r["cell"], r["treatment"], r["outcome"], r["spec"])),
          FIELDS)
    with (OUT / "lag_coverage.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["measure", "grade", "label", "waves", "n_states_min_wave", "n_obs"],
                           lineterminator="\n")
        w.writeheader()
        w.writerows(cover)
    print(f"estimates={len(rows)} coverage rows={len(cover)}")


if __name__ == "__main__":
    main()
