"""Two measurement checks on the migrant side of position.py.

Allocation. Rendall & Parker (2014), citing Ibarraran & Lubotsky (2007), note that the Census
Bureau imputes education for as many as a fifth of Mexican-born respondents, using predictors that
do not include nativity. IPUMS extract #13 carries QEDUC for every record of extracts #3 and #12.
For each cohort's main survey this reports the weighted share whose education was edited or
allocated (QEDUC > 0) and the main statistics with those records dropped.

Instrument. In survivor_drift.csv every cohort observed in the 2000 census long form ranks higher
in the 2005 ACS and then stays nearly flat through 2024. The ACS 2000-2004 (extract #12) use the
same education categories as the long form and observe the same cohorts within 0-4 years of it,
so a gap already present in 2000-2004 points at the survey rather than at return migration or US
schooling acquired between 2000 and 2005.

ACS 2020 break. For a fixed set of people (arrived 1975-2009 at age 20+, aged 25+), the ACS share
reporting "no schooling completed" should not rise from one year to the next. acs_break_2020.csv
tabulates it by ACS year, for all records and for records whose education was not edited or
allocated.

  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/schooling_selection_position_2026_09_23/instrument_checks.py
"""
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import position as P  # noqa: E402

ACS0004 = HERE / "_cache" / "us_mexborn_acs0004.data.csv.gz"
QEDUC = HERE / "_cache" / "us_mexborn_qeduc.data.csv.gz"
KEY = ["SAMPLE", "SERIAL", "PERNUM"]
SHOW = ["n", "wN", "ridit", "ridit_se", "q1", "q5", "mig_c1_none_primary_incomplete", "mig_c3_lower_secondary",
        "mig_c4_upper_secondary", "mig_c5_tertiary", "diff_c1_none_primary_incomplete", "diff_c5_tertiary",
        "position"]
HS_DIPLOMA = [62, 63, 64]


def with_flags(d: pd.DataFrame, q: pd.DataFrame) -> pd.DataFrame:
    out = d.merge(q, on=KEY, how="left", validate="one_to_one")
    if out.QEDUC.isna().any():
        raise SystemExit(f"[FAILED] {int(out.QEDUC.isna().sum())} records have no QEDUC match")
    return out


def row(check: str, g: pd.DataFrame, origin, emp, c0: int, survey: str, sex: str, subset: str) -> dict:
    r = P.summarize(g, origin, emp, c0, "nearest")
    w = g.PERWT
    return {"check": check, "cohort": f"{c0}-{dict(P.COHORTS)[c0]}", "survey": survey, "sex": sex, "subset": subset,
            "edited_or_allocated_share": float(w[g.QEDUC > 0].sum() / w.sum()),
            "hs_diploma_share": float(w[g.EDUCD.isin(HS_DIPLOMA)].sum() / w.sum()),
            **{k: r[k] for k in SHOW}}


def both_subsets(check, g, origin, emp, c0, survey) -> list[dict]:
    out = []
    for sx in ("P", "H", "M"):
        gs = g if sx == "P" else g[g.sex == sx]
        out.append(row(check, gs, origin, emp, c0, survey, sx, "all records"))
        out.append(row(check, gs[gs.QEDUC == 0], origin, emp, c0, survey, sx, "education as reported"))
    return out


def main() -> None:
    origin = P.Origin(P.OUT / "origin_levels.csv")
    q = pd.read_csv(QEDUC, usecols=KEY + ["QEDUC"])
    d = with_flags(P.load_migrants(), q)
    emp = P.empirical_splits(d)
    rows = []
    for c0, c1 in P.COHORTS:
        s = P.MAIN_SURVEY[c0]
        g = P.cohort_rows(d, s, c0, c1)
        rows += both_subsets("allocation, main survey", g[g.arr_age >= 20], origin, emp, c0, str(s))

    acs = with_flags(P.load_migrants(ACS0004, all_samples=True), q)
    for c0, c1 in ((1985, 1989), (1990, 1994), (1995, 1999)):
        census = P.cohort_rows(d, 2000, c0, c1)
        rows += both_subsets("instrument", census[census.arr_age >= 20], origin, emp, c0, "census 2000 long form")
        a = acs[(acs.YRIMMIG >= c0) & (acs.YRIMMIG <= c1) & (acs.arr_age >= 20)]
        for label, sel in (("ACS 2000", a.SAMPLE == 200004), ("ACS 2001-2002", a.YEAR.isin([2001, 2002])),
                           ("ACS 2003-2004", a.YEAR.isin([2003, 2004])), ("ACS 2000-2004", a.YEAR <= 2004)):
            rows += both_subsets("instrument", a[sel], origin, emp, c0, label)
        a05 = P.cohort_rows(d, 2005, c0, c1)
        rows += both_subsets("instrument", a05[a05.arr_age >= 20], origin, emp, c0, "ACS 2005")

    out = pd.DataFrame(rows)
    out.to_csv(P.OUT / "instrument_checks.csv", index=False, float_format="%.5f")
    acs_break(d)
    pd.set_option("display.width", 250)
    show = ["check", "cohort", "survey", "sex", "subset", "n", "edited_or_allocated_share", "hs_diploma_share",
            "ridit", "ridit_se", "mig_c1_none_primary_incomplete", "mig_c5_tertiary", "position"]
    print(out[out.sex == "P"][show].to_string(index=False, float_format=lambda x: f"{x:.3f}"))


def acs_break(d: pd.DataFrame) -> None:
    g = d[(d.YEAR >= 2012) & (d.YRIMMIG >= 1975) & (d.YRIMMIG <= 2009) & (d.arr_age >= 20) & (d.AGE >= 25)]
    share = lambda x, m: float(x.PERWT[m].sum() / x.PERWT.sum())  # noqa: E731
    rows = []
    for y, x in g.groupby("YEAR"):
        r = x[x.QEDUC == 0]
        rows.append({"acs_year": y, "n": len(x), "edited_or_allocated_share": share(x, x.QEDUC > 0),
                     "no_schooling_all": share(x, x.EDUCD == 2), "no_schooling_as_reported": share(r, r.EDUCD == 2),
                     "grade6_as_reported": share(r, r.EDUCD == 23),
                     "grades_1_to_5_as_reported": share(r, r.EDUCD.isin([14, 15, 16, 17, 22])),
                     "hs_diploma_as_reported": share(r, r.EDUCD.isin(HS_DIPLOMA))})
    out = pd.DataFrame(rows)
    out.to_csv(P.OUT / "acs_break_2020.csv", index=False, float_format="%.5f")
    print(out.to_string(index=False, float_format=lambda v: f"{v:.3f}"))


if __name__ == "__main__":
    main()
