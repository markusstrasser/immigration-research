"""English ability and education of Mexico-born arrival cohorts, decomposed into cohort and duration.

Mexico-born person records pulled from the Census PUMS API, one call per survey year with the
predicate POBP=303 (Mexico), for ACS 1-year 2005-2021, plus the locally staged 2023 and 2024 files.
Only the Mexico-born are needed here, because English ability and attainment are within-group
statistics that take no native comparison.

  https://api.census.gov/data/<year>/acs/acs1/pums?get=PWGTP,AGEP,SEX,SCHL,ENG,YOEP,CIT,ESR,WAGP,WKHP&POBP=303

ENG: 1 very well, 2 well, 3 not well, 4 not at all; missing = speaks only English at home.
SCHL (2008+): <=15 less than HS, 16-17 HS/GED, 18-20 some college, >=21 BA+.
SCHL (2005-2007) used a 1-16 scale: 1-8 = grades through 11, 9 = HS graduate, 10-12 = some college
and associate's, 13 = bachelor's, 14-16 = graduate degrees. Handled separately.

With several survey years the same cohort is read at several durations, so cohort and duration
separate, which a single cross-section cannot do.

Outputs derived/english_*.csv, derived/edu_cohort_duration_*.csv
"""
import glob
import json
import os

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "_cache")
OUT = os.path.join(HERE, "derived")
os.makedirs(OUT, exist_ok=True)

N_STATES = 51  # 50 states + DC, the full PUMS state list

COH = [(0, 1979, "pre1980"), (1980, 1989, "1980-89"), (1990, 1999, "1990-99"),
       (2000, 2007, "2000-07"), (2008, 2014, "2008-14"), (2015, 2019, "2015-19"),
       (2020, 2021, "2020-21"), (2022, 2030, "2022-24")]


def cohort_of(y):
    if pd.isna(y):
        return None
    for lo, hi, lab in COH:
        if lo <= y <= hi:
            return lab
    return None


def edu4_modern(s):
    return np.where(s <= 15, "lths", np.where(s <= 17, "hs", np.where(s <= 20, "somecoll", "ba_plus")))


def edu4_old(s):
    # 2005-2007 SCHL: 9 = high school graduate, 10-12 some college/associate, 13 bachelor's, 14+ grad
    return np.where(s <= 8, "lths", np.where(s == 9, "hs", np.where(s <= 12, "somecoll", "ba_plus")))


def _finish(d, year):
    # the API echoes predicate variables as extra columns, so AGEP can appear twice
    d = d.loc[:, ~d.columns.duplicated()].copy()
    for c in d.columns:
        d[c] = pd.to_numeric(d[c], errors="coerce")
    d["YEAR"] = year
    d["edu4"] = edu4_old(d.SCHL) if year <= 2007 else edu4_modern(d.SCHL)
    return d


def load_api():
    """Whole-year pulls plus state-chunked pulls.

    A whole-year call for one birthplace is several megabytes and the Census API dropped the
    connection partway on most attempts, so the working pattern is one call per state with an
    AGEP=25:54 predicate: each response is small enough to complete.
    """
    frames = []
    for f in sorted(glob.glob(os.path.join(CACHE, "pums_api_*_mex.json"))):
        year = int(os.path.basename(f).split("_")[2])
        raw = json.load(open(f))
        frames.append(_finish(pd.DataFrame(raw[1:], columns=raw[0]), year))
    for dpath in sorted(glob.glob(os.path.join(CACHE, "states_*"))):
        year = int(os.path.basename(dpath).split("_")[1])
        files = sorted(glob.glob(os.path.join(dpath, "st_*.json")))
        # HARD GUARD: a partial state set is not a national sample. Four states dominated by
        # Arizona would look like a survey year and silently corrupt every cross-cohort
        # comparison, so a year short of all 51 state files is refused, not down-weighted.
        if len(files) < N_STATES:
            print(f"  SKIP state-chunked {year}: {len(files)}/{N_STATES} state files present, "
                  f"not a national sample")
            continue
        parts = []
        for f in files:
            raw = json.load(open(f))
            if len(raw) < 2:
                continue
            parts.append(pd.DataFrame(raw[1:], columns=raw[0]))
        d = pd.concat(parts, ignore_index=True)
        print(f"  state-chunked {year}: {len(files)} states, {len(d)} records")
        frames.append(_finish(d, year))
    return frames


def load_staged():
    frames = []
    for f in sorted(glob.glob(os.path.join(CACHE, "acs_*.parquet"))):
        d = pd.read_parquet(f)
        d = d[d.POBP == 303].copy()
        d["edu4"] = edu4_modern(d.SCHL)
        frames.append(d)
    return frames


def main():
    parts = load_api() + load_staged()
    if not parts:
        raise SystemExit("no input files")
    keep = ["YEAR", "PWGTP", "AGEP", "SEX", "SCHL", "ENG", "YOEP", "CIT", "ESR", "WAGP",
            "WKHP", "edu4"]
    df = pd.concat([p[[c for c in keep if c in p.columns]] for p in parts], ignore_index=True)
    df = df[(df.AGEP >= 25) & (df.AGEP <= 54)].copy()
    df["cohort"] = df.YOEP.map(cohort_of)
    df["ysm"] = df.YEAR - df.YOEP
    df["sexlab"] = np.where(df.SEX == 1, "men", "women")
    df["eng_vw"] = np.where(df.ENG.isna(), 1.0, (df.ENG == 1).astype(float))
    df["eng_wellplus"] = np.where(df.ENG.isna(), 1.0, df.ENG.isin([1, 2]).astype(float))
    df["eng_notatall"] = np.where(df.ENG.isna(), 0.0, (df.ENG == 4).astype(float))
    print("years:", sorted(df.YEAR.unique()), "rows:", len(df))

    rows = []
    for (y, c), g in df[df.cohort.notna()].groupby(["YEAR", "cohort"]):
        if len(g) < 40:
            continue
        w = g.PWGTP.sum()
        r = {"survey_year": int(y), "cohort": c, "n": len(g),
             "mean_ysm": float(np.average(g.ysm, weights=g.PWGTP)),
             "mean_age": float(np.average(g.AGEP, weights=g.PWGTP)),
             "eng_very_well_or_only": float(np.average(g.eng_vw, weights=g.PWGTP)),
             "eng_well_plus": float(np.average(g.eng_wellplus, weights=g.PWGTP)),
             "eng_not_at_all": float(np.average(g.eng_notatall, weights=g.PWGTP))}
        for e in ["lths", "hs", "somecoll", "ba_plus"]:
            r[f"sh_{e}"] = float(g.loc[g.edu4 == e, "PWGTP"].sum() / w)
        rows.append(r)
    t = pd.DataFrame(rows).sort_values(["cohort", "survey_year"])
    t.to_csv(f"{OUT}/english_edu_cohort_by_survey_year.csv", index=False)

    # cohort x duration band: the decomposition a single cross-section cannot do
    df["ysm_band"] = pd.cut(df.ysm, [-1, 5, 10, 20, 100], labels=["0-5", "6-10", "11-20", "21+"])
    rows = []
    for (c, b), g in df[df.cohort.notna()].groupby(["cohort", "ysm_band"], observed=True):
        if len(g) < 40:
            continue
        w = g.PWGTP.sum()
        rows.append({"cohort": c, "ysm_band": str(b), "n": len(g),
                     "survey_years": str(sorted(g.YEAR.unique().tolist())),
                     "eng_very_well_or_only": float(np.average(g.eng_vw, weights=g.PWGTP)),
                     "eng_well_plus": float(np.average(g.eng_wellplus, weights=g.PWGTP)),
                     "eng_not_at_all": float(np.average(g.eng_notatall, weights=g.PWGTP)),
                     "sh_lths": float(g.loc[g.edu4 == "lths", "PWGTP"].sum() / w),
                     "sh_ba_plus": float(g.loc[g.edu4 == "ba_plus", "PWGTP"].sum() / w)})
    d = pd.DataFrame(rows)
    d.to_csv(f"{OUT}/english_edu_cohort_by_duration_band.csv", index=False)
    piv = d.pivot(index="cohort", columns="ysm_band", values="eng_very_well_or_only")
    piv.to_csv(f"{OUT}/english_cohort_x_duration_matrix.csv")
    print("\nEnglish 'very well or only English', cohort x duration:\n", piv.round(3).to_string())
    piv2 = d.pivot(index="cohort", columns="ysm_band", values="sh_lths")
    piv2.to_csv(f"{OUT}/edu_lths_cohort_x_duration_matrix.csv")
    print("\nShare less than high school, cohort x duration:\n", piv2.round(3).to_string())
    piv3 = d.pivot(index="cohort", columns="ysm_band", values="sh_ba_plus")
    piv3.to_csv(f"{OUT}/edu_baplus_cohort_x_duration_matrix.csv")
    print("\nShare BA+, cohort x duration:\n", piv3.round(3).to_string())
    print("\nper survey year:\n", t.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
