#!/usr/bin/env python3
"""Arm 2 (CPS half): reproduce the Borjas residual on CPS ASEC 2025.

Reuses infra/immigration-fiscal/status_impute_2026_09_16/impute_status.py
unchanged (imported, not copied).  That module is the repo's canonical
implementation of the Borjas (2017) rule list; ladder entry 85 rests on it.

Input : ~/research-data/immigration-fiscal/data/external/stage3/census/
        cps_asec_2025/asecpub25csv.zip   (read-only)
Output: derived/cps2025_residual_by_region.csv
        derived/cps2025_residual_by_yrsince.csv
        derived/cps2025_summary.json

Weights: MARSUPWT/100 is the full person weight.  The 160 ASEC replicate
weights give the Census Bureau's published successive-difference SE,
SE = sqrt(4/160 * sum_i (x_i - x)^2), the same formula
infra/immigration-fiscal/build/analyze_cps_fiscal_2025.py uses.
"""
from __future__ import annotations

import sys as _path_sys
from pathlib import Path as _Path
_path_sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "build"))
import paths as _data_paths


import json
import os
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

os.environ.setdefault("PYTHONUNBUFFERED", "1")

HERE = Path(__file__).resolve().parent
DERIVED = HERE / "derived"
IMPUTE_LANE = HERE.parent / "status_impute_2026_09_16"
sys.path.insert(0, str(IMPUTE_LANE))
from impute_status import impute  # noqa: E402

ZIP = (_data_paths.data_root(require_exists=False) / 'external/stage3/census/cps_asec_2025/asecpub25csv.zip')

PERSON = ["PH_SEQ", "PPPOS", "A_LINENO", "A_SPOUSE", "A_AGE", "PRPERTYP",
          "PRCITSHP", "PENATVTY", "PEINUSYR", "MARSUPWT", "SS_VAL", "SSI_VAL",
          "MCAID", "MCARE", "MIL", "CHAMPVA", "VET_YN", "PEAFEVER",
          "A_CLSWKR", "PEIOOCC"]
HOUSE = ["H_SEQ", "HPUBLIC", "HLORENT"]
REPS = [f"pwwgt{i}" for i in range(1, 161)]

# CPS ASEC PENATVTY country-of-birth recode, verified against this repo's own
# crosswalk (secgen_selectivity_2026_09_16/country_crosswalk.csv).
MEXICO = 303
# Region bands in the CPS PENATVTY recode.
REGIONS = [("Europe", 100, 199), ("Asia", 200, 299),
           ("North/Central America and Caribbean", 300, 359),
           ("South America", 360, 399), ("Africa", 400, 499),
           ("Oceania and at sea", 500, 599)]

# PEINUSYR bands -> midpoint year of entry, from the ASEC 2025 data dictionary
# (asec2025_ddl_pub_full.pdf).  Codes 1-6 are pre-1980 (see impute_status.py);
# from code 7 the bands are two-year, then annual at the end of the series.
PEINUSYR_LABEL = {
    1: "before 1950", 2: "1950-1959", 3: "1960-1964", 4: "1965-1969",
    5: "1970-1974", 6: "1975-1979", 7: "1980-1981", 8: "1982-1983",
    9: "1984-1985", 10: "1986-1987", 11: "1988-1989", 12: "1990-1991",
    13: "1992-1993", 14: "1994-1995", 15: "1996-1997", 16: "1998-1999",
    17: "2000-2001", 18: "2002-2003", 19: "2004-2005", 20: "2006-2007",
    21: "2008-2009", 22: "2010-2011", 23: "2012-2013", 24: "2014-2015",
    25: "2016-2017", 26: "2018-2019", 27: "2020-2021", 28: "2022-2025",
}


def se_from_reps(point: float, reps: np.ndarray) -> float:
    return float(np.sqrt(4.0 / 160.0 * np.square(reps - point).sum()))


def main() -> int:
    DERIVED.mkdir(exist_ok=True)
    print(f"[1/5] reading {ZIP}")
    with zipfile.ZipFile(ZIP) as z:
        d = pd.read_csv(z.open("pppub25.csv"), usecols=PERSON)
        hh = pd.read_csv(z.open("hhpub25.csv"), usecols=HOUSE)
        r = pd.read_csv(z.open("asec_csv_repwgt_2025.csv"))
    print(f"  persons {len(d):,}  households {len(hh):,}  repwgt rows {len(r):,}")

    r = r.rename(columns={"h_seq": "PH_SEQ"})
    d = d.merge(r, on=["PH_SEQ", "PPPOS"], how="left", validate="one_to_one")
    if d[REPS].isna().any().any():
        raise ValueError("Incomplete person-replicate join")
    delta = float((d.MARSUPWT / 100 - d.pwwgt0).abs().max())
    if delta >= .01:
        raise ValueError(f"Full-weight merge validation failed: {delta}")
    print(f"  ✓ replicate join; max full-weight difference {delta:.6f}")

    print("[2/5] imputing status with the Borjas rule list (unmodified module)")
    res = impute(d, hh)
    fb, unauth = res["foreign_born"], res["unauthorized"]

    w = (d.MARSUPWT / 100).to_numpy(float)
    rw = d[REPS].to_numpy(float)

    def est(mask):
        pt = float(w[mask].sum())
        return pt, se_from_reps(pt, rw[mask].sum(axis=0).astype(float))

    tot, tot_se = est(unauth)
    fbt, fbt_se = est(fb)
    mex, mex_se = est(unauth & (d.PENATVTY.to_numpy() == MEXICO))
    print(f"  residual total {tot:,.0f} (se {tot_se:,.0f})")
    print(f"  residual Mexico-born {mex:,.0f} (se {mex_se:,.0f})")

    print("[3/5] region-of-birth table")
    pen = d.PENATVTY.to_numpy()
    rows = []
    for name, lo, hi in REGIONS:
        m = unauth & (pen >= lo) & (pen <= hi)
        if name == "North/Central America and Caribbean":
            mm = m & (pen == MEXICO)
            pt, se = est(mm)
            fpt, _ = est(fb & (pen == MEXICO))
            rows.append({"region_of_birth": "Mexico", "foreign_born": round(fpt),
                         "residual_unadjusted": round(pt), "se": round(se),
                         "share_of_foreign_born_pct": round(100 * pt / fpt, 1)})
            m = m & (pen != MEXICO)
            name = "Other North/Central America and Caribbean"
        pt, se = est(m)
        fpt, _ = est(fb & (pen >= lo) & (pen <= hi)
                     & ((pen != MEXICO) if name.startswith("Other North") else True))
        rows.append({"region_of_birth": name, "foreign_born": round(fpt),
                     "residual_unadjusted": round(pt), "se": round(se),
                     "share_of_foreign_born_pct": round(100 * pt / fpt, 1)})
    rows.append({"region_of_birth": "TOTAL", "foreign_born": round(fbt),
                 "residual_unadjusted": round(tot), "se": round(tot_se),
                 "share_of_foreign_born_pct": round(100 * tot / fbt, 1)})
    pd.DataFrame(rows).to_csv(DERIVED / "cps2025_residual_by_region.csv", index=False)
    print("  ✓ wrote cps2025_residual_by_region.csv")

    print("[4/5] arrival-cohort table")
    code = d.PEINUSYR.to_numpy()
    rows = []
    for c in sorted(PEINUSYR_LABEL):
        m = unauth & (code == c)
        if not m.any():
            continue
        pt, se = est(m)
        rows.append({"peinusyr_code": c, "arrival_window": PEINUSYR_LABEL[c],
                     "residual_unadjusted": round(pt), "se": round(se)})
    pd.DataFrame(rows).to_csv(DERIVED / "cps2025_residual_by_yrsince.csv", index=False)
    print("  ✓ wrote cps2025_residual_by_yrsince.csv")

    print("[5/5] summary")
    recent = unauth & (code >= 28)
    rec_pt, rec_se = est(recent)
    summary = {
        "cps_asec_2025_person_rows": int(len(d)),
        "weighted_total_population": round(float(w.sum())),
        "foreign_born": round(fbt), "foreign_born_se": round(fbt_se),
        "borjas_residual_unadjusted": round(tot), "borjas_residual_se": round(tot_se),
        "borjas_residual_mexico_born": round(mex), "borjas_residual_mexico_se": round(mex_se),
        "residual_arrived_2022_or_later": round(rec_pt),
        "residual_arrived_2022_or_later_se": round(rec_se),
        "max_full_weight_difference": delta,
    }
    (DERIVED / "cps2025_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
