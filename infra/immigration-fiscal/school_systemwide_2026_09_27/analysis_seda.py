"""Test 6 (optional in the brief): SEDA 6.0 NAEP-linked district scores for white pupils against the
district's Hispanic and English-learner shares, within districts, 2009–2019.

SEDA's cohort scale (cs) places each state's test results on the NAEP scale state-year by state-year,
so a district mean on it is absolute across years; within a state it follows the state test. Two
fixed-effect structures separate the two sources of variation:
  district + year FE        within-district change, statewide shifts included (a system can show);
  district + state×year FE  within-state change only, the structure of the peer-effect designs.
The gap between the two is the statewide component.

Inputs (downloaded without an account from the Stanford Digital Repository, SEDA 6.0,
https://purl.stanford.edu/xh833nn4025, into _cache/seda/):
  seda_geodist_annualsub_cs_6.0.csv  district × year × subgroup means, pooled over grades 3–8
  seda_cov_geodist_annual_6.0.csv    district × year covariates (CCD shares, ACS SES)
Writes derived/seda_estimates.csv. Run from the repository root:
    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/school_systemwide_2026_09_27/analysis_seda.py
"""
import sys
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from analysis_naep import FIELDS, record, write  # noqa: E402
from stats_util import ols_absorb  # noqa: E402

SEDA = HERE / "_cache" / "seda"
OUT = HERE / "derived"
# byte sizes served by stacks.stanford.edu (Content-Range, 2026-09-28): a first download of the
# achievement file stopped at 140.8 MB with curl exit 0, so completeness is checked, not assumed
EXPECTED_BYTES = {"seda_geodist_annualsub_cs_6.0.csv": 375_620_429, "seda_cov_geodist_annual_6.0.csv": 78_616_725}


def check_inputs():
    for name, size in EXPECTED_BYTES.items():
        got = (SEDA / name).stat().st_size if (SEDA / name).exists() else 0
        if got != size:
            sys.exit(f"[BLOCKED] {name}: {got} bytes, expected {size}; resume with curl -C -")


def load():
    con = duckdb.connect()
    ach = con.execute(f"""
        SELECT sedalea, year, stateabb, subgroup,
               cs_mn_avg_mth_ol AS mth, cs_mn_avg_rla_ol AS rla,
               tot_asmts_mth AS n_mth, tot_asmts_rla AS n_rla
        FROM read_csv_auto('{SEDA / "seda_geodist_annualsub_cs_6.0.csv"}', all_varchar=false)
        WHERE subgroup IN ('wht', 'all') AND gap = 0 AND multi_comp = 0
    """).df()
    cov = con.execute(f"""
        SELECT sedalea, year, perhsp, perell, perwht, totenrl, seswht
        FROM read_csv_auto('{SEDA / "seda_cov_geodist_annual_6.0.csv"}')
    """).df()
    # long in subject
    parts = []
    for subj in ("mth", "rla"):
        a = ach[["sedalea", "year", "stateabb", "subgroup", subj, "n_" + subj]].rename(
            columns={subj: "score", "n_" + subj: "n_tests"})
        a["subject"] = subj
        parts.append(a)
    d = pd.concat(parts).merge(cov, on=["sedalea", "year"], how="inner")
    d = d.dropna(subset=["score", "perhsp"])
    d["hisp_pp"] = 100 * d.perhsp
    # CCD English-learner counts have reporting gaps recorded as zero: a zero in a district whose
    # median share over 2009–2019 is at least 2% is treated as missing
    med = d.groupby("sedalea").perell.transform("median")
    d["el_pp"] = np.where((d.perell == 0) & (med >= 0.02), np.nan, 100 * d.perell)
    d["dist_subj"] = d.sedalea.astype(str) + "|" + d.subject
    d["subj_year"] = d.subject + "|" + d.year.astype(str)
    d["state_subj_year"] = d.stateabb + "|" + d.subj_year
    return d


def main():
    check_inputs()
    d = load()
    rows = []
    for group in ("wht", "all"):
        g = d[d.subgroup == group]
        for tcol, tkey in (("hisp_pp", "hisp_district"), ("el_pp", "el_district")):
            for spec, absorb, extra, weight, note in [
                ("district_year_fe", ["dist_subj", "subj_year"], [], None,
                 "district and year FE: statewide shifts included"),
                ("district_stateyear_fe", ["dist_subj", "state_subj_year"], [], None,
                 "district and state-by-year FE: within-state variation only"),
                ("district_year_fe_ses", ["dist_subj", "subj_year"], ["seswht"], None,
                 "adds white families' SES composite (ACS)"),
                ("district_year_fe_weighted", ["dist_subj", "subj_year"], [], "n_tests",
                 "weighted by the subgroup's number of tests"),
                ("district_stateyear_fe_weighted", ["dist_subj", "state_subj_year"], [], "n_tests",
                 "weighted, within-state only"),
            ]:
                res = ols_absorb(g, "score", [tcol] + extra, absorb=absorb, cluster="stateabb", weight=weight)
                record(rows, res, tcol, test="seda", spec=spec, treatment=tkey,
                       outcome="white" if group == "wht" else "all", cell="math+rla", units="SD (SEDA cs)",
                       years=f"{int(g.year.min())}-{int(g.year.max())}", note=note + "; SEs clustered by state")
                if spec in ("district_year_fe", "district_stateyear_fe"):
                    r2 = ols_absorb(g, "score", [tcol], absorb=absorb, cluster="sedalea", weight=weight)
                    record(rows, r2, tcol, test="seda", spec=spec + "_cl_district", treatment=tkey,
                           outcome="white" if group == "wht" else "all", cell="math+rla", units="SD (SEDA cs)",
                           years=f"{int(g.year.min())}-{int(g.year.max())}", note=note + "; SEs clustered by district")
            # pre-trend check: next year's district share, current share held
            q = g.sort_values(["dist_subj", "year"]).copy()
            nxt = q.groupby("dist_subj")[tcol].shift(-1)
            q["lead"] = np.where(q.groupby("dist_subj").year.shift(-1) == q.year + 1, nxt, np.nan)
            q = q.dropna(subset=["lead", tcol])
            for spec, absorb in (("district_year_fe_lead", ["dist_subj", "subj_year"]),
                                 ("district_stateyear_fe_lead", ["dist_subj", "state_subj_year"])):
                res = ols_absorb(q, "score", [tcol, "lead"], absorb=absorb, cluster="stateabb")
                for nm, sp, nt in (("lead", spec, "next year's district share, current share held"),
                                   (tcol, spec + "_current", "current share, next year's share held")):
                    record(rows, res, nm, test="seda", spec=sp, treatment=tkey,
                           outcome="white" if group == "wht" else "all", cell="math+rla", units="SD (SEDA cs)",
                           years=f"{int(q.year.min())}-{int(q.year.max())}", note=nt + "; SEs clustered by state")
    write(OUT / "seda_estimates.csv", sorted(rows, key=lambda r: (r["outcome"], r["treatment"], r["spec"])), FIELDS)
    w = d[d.subgroup == "wht"]
    print(f"estimates={len(rows)}; white district-subject-years={len(w)}, districts={w.sedalea.nunique()}, "
          f"states={w.stateabb.nunique()}")


if __name__ == "__main__":
    main()
