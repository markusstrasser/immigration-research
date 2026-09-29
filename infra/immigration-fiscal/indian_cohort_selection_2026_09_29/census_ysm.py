#!/usr/bin/env python3
"""Entry quality of India-born arrival cohorts at fixed duration, 1980-2023 (IPUMS USA panel).

The CPS reference starts in 1994, so the 1965-1990 wave cannot be placed on the selection-curve
scale at arrival. This script uses the local IPUMS USA Borjas panel (1980, 1990, 2000 5% censuses;
ACS 2010 and 2023; `immigration_microdata.duckdb`, table `ipums_usa_borjas_panel`) and a second
reference that exists in every year (India is detailed BPLD 52100: the general BPL 521 also holds
Pakistan, Bangladesh, Sri Lanka, Myanmar and Bhutan): US-born white persons (BPL < 100, RACE 1; Hispanic origin is
not in the extract, and second-generation whites are included) of the same year and five-year age
band. For 2000, 2010 and 2023 the same people are also placed in the CPS G3+ NH white reference
(ASEC year = census/ACS year) to bridge the two scales. 1980 schooling is years completed, not
degrees: "BA+" there is 4+ years of college and "graduate" 5+ years.

Views: ages 25-54, arrived 0-5 years and 6-10 years before the survey (census intervals), age-
standardised to the view's India-born age mix pooled over the five surveys; `white_ba_plus` is the
reference's own 25-54 BA+ share for scale.
Output: derived/census_ysm.csv
Run from the repo root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with duckdb --with pyarrow python3 \
      infra/immigration-fiscal/indian_cohort_selection_2026_09_29/census_ysm.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402

DB = Path.home() / "research-data/immigration-fiscal/derived/immigration_microdata.duckdb"
# arrival windows (YRIMMIG codes as stored) for 0-5 and 6-10 years since arrival
WINDOWS = {1980: {"ysm_0_5": (1975, 1980, "1975-80"), "ysm_6_10": (1970, 1974, "1970-74")},
           1990: {"ysm_0_5": (1985, 1990, "1985-90"), "ysm_6_10": (1980, 1984, "1980-84")},
           2000: {"ysm_0_5": (1995, 2000, "1995-2000"), "ysm_6_10": (1990, 1994, "1990-94")},
           2010: {"ysm_0_5": (2005, 2010, "2005-10"), "ysm_6_10": (2000, 2004, "2000-04")},
           2023: {"ysm_0_5": (2018, 2023, "2018-23"), "ysm_6_10": (2013, 2017, "2013-17")}}


def main() -> int:
    con = duckdb.connect(str(DB), read_only=True)
    d = con.execute("""SELECT YEAR AS year, AGE AS age, BPL AS bpl, BPLD AS bpld, RACE AS race, YRIMMIG AS yrimmig,
                              EDUCD AS educd, PERWT AS w
                       FROM ipums_usa_borjas_panel
                       WHERE AGE BETWEEN 25 AND 54 AND (BPLD = 52100 OR (BPL < 100 AND RACE = 1))""").df()
    con.close()
    d["educ"] = d.educd.map(C.EDUCD_TO_EDUC)
    unmapped = d.loc[d.educ.isna() & (d.educd > 0), "educd"].unique()
    if len(unmapped):
        raise SystemExit(f"[BLOCKED] unmapped EDUCD codes {sorted(unmapped)}")
    d = d[d.educ.notna()].copy()
    d["band"] = C.band_of(d.age.to_numpy())
    d["ref"] = (d.bpl < 100) & (d.race == 1)
    d["p_edu_census"] = np.nan
    for (yr, b), g in d.groupby(["year", "band"]):
        r = g[g.ref]
        d.loc[g.index, "p_edu_census"] = C.cps_curve.midrank_pct(r.educ.to_numpy(float), r.w.to_numpy(),
                                                                 g.educ.to_numpy(float))
    cps = C.cps_prepared()
    ref = C.Reference(cps)
    bridge = d.year.isin([2000, 2010, 2023]).to_numpy()
    d["p_edu_cps"] = np.nan
    d.loc[bridge, "p_edu_cps"] = ref.pct("educ", d.year.to_numpy()[bridge], d.band.to_numpy()[bridge],
                                         d.educ.replace({91: 92}).to_numpy()[bridge])
    rows = []
    ind = (d.bpld == 52100).to_numpy()
    for yr, wins in WINDOWS.items():
        ry = d[(d.year == yr) & d.ref]
        rs_white = ry.groupby("band").w.sum() / ry.w.sum()
        for view, (lo, hi, lab) in wins.items():
            # age mix: the India-born arrivals of this view pooled over the five surveys
            pool = np.zeros(len(d), bool)
            for y2, w2 in WINDOWS.items():
                a, b, _ = w2[view]
                pool |= ind & (d.year == y2).to_numpy() & d.yrimmig.between(a, b).to_numpy()
            rs = d.loc[pool].groupby("band").w.sum() / d.loc[pool].w.sum()
            m = ((d.year == yr) & (d.bpld == 52100) & d.yrimmig.between(lo, hi)).to_numpy()
            ws = C.cps_curve.std_weights(d, m, rs)
            s = d.loc[m]
            row = {"survey_year": yr, "view": view, "arrival": lab, "n": int(m.sum())}
            row["p_edu_census_ref"], row["p_edu_census_ref_se"] = C.cps_curve.wmean_se(s.p_edu_census.to_numpy(), ws)
            if yr in (2000, 2010, 2023):
                row["p_edu_cps_ref"], row["p_edu_cps_ref_se"] = C.cps_curve.wmean_se(s.p_edu_cps.to_numpy(), ws)
            else:
                row["p_edu_cps_ref"], row["p_edu_cps_ref_se"] = float("nan"), float("nan")
            row["ba_plus"] = float(ws[s.educ.isin(C.BA_PLUS).to_numpy()].sum() / ws.sum())
            row["graduate"] = float(ws[s.educ.isin(C.GRAD).to_numpy()].sum() / ws.sum())
            wr = C.cps_curve.std_weights(d, ((d.year == yr) & d.ref).to_numpy(), rs_white)
            row["white_ba_plus"] = float(wr[ry.educ.isin(C.BA_PLUS).to_numpy()].sum() / wr.sum())
            rows.append(row)
    C.write_csv(C.DER / "census_ysm.csv", rows)
    print(pd.DataFrame(rows).round(3).to_string())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
