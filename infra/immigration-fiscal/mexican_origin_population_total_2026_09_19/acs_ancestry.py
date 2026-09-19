#!/usr/bin/env python3
"""Arm 2 -- the ancestry definition of the Mexican-origin population.

ACS 2024 1-year PUMS, 3.42M person records, 80 replicate weights
(successive-difference variance factor 4/80).

ANC1P/ANC2P Mexican ancestry codes, from the 2024 PUMS data dictionary:
  210 Mexican, 211 Mexican American, 212 Mexicano, 213 Chicano,
  215 Mexican American Indian, 218 Mexican State, 219 Mexican Indian.
HISP = 02 is "Mexican"; 01 is "Not Spanish/Hispanic/Latino".
POBP = 303 is Mexico.
[SOURCE: ~/research-data/immigration-fiscal/data/external/acs_pums_dict/PUMS_Data_Dictionary_2024.csv]

Ancestry is a second SELF-REPORT, not an attrition correction: a person who has
stopped calling themselves Mexican on the Hispanic-origin question may equally
have stopped writing "Mexican" on the ancestry question.

Inputs : _cache/acs2024_ancestry_subset.parquet (from extract_acs.py)
Outputs: derived/arm2_ancestry_crosstab.csv
         derived/arm2_ancestry_totals.csv
         derived/arm2_ancestry_by_nativity.csv
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
DERIVED = HERE / "derived"

MEX_ANC = (210, 211, 212, 213, 215, 218, 219)
OTHER_HISP_ANC = (200, 221, 222, 223, 224, 225, 226, 227, 231, 232, 233, 234, 235,
                  236, 237, 238, 239, 249, 250, 251, 252, 261, 271, 275, 290, 291, 295)
MEXICO_POBP = 303
REP_N = 80
W0 = "PWGTP"
REPS = [f"PWGTP{i}" for i in range(1, REP_N + 1)]


def sdr_se(full: float, reps: np.ndarray) -> float:
    return float(np.sqrt(4.0 / REP_N * np.sum((reps - full) ** 2)))


def total(d: pd.DataFrame, mask: np.ndarray) -> tuple[float, float, int]:
    sub = d.loc[mask]
    full = float(sub[W0].sum())
    reps = sub[REPS].sum().to_numpy(dtype=float)
    return full, sdr_se(full, reps), int(mask.sum())


def main() -> int:
    DERIVED.mkdir(exist_ok=True)
    d = pd.read_parquet(CACHE / "acs2024_ancestry_subset.parquet")
    print(f"records: {len(d):,}", flush=True)

    a1 = d["ANC1P"].to_numpy()
    a2 = d["ANC2P"].to_numpy()
    mex_anc = np.isin(a1, MEX_ANC) | np.isin(a2, MEX_ANC)
    other_hisp_anc = (np.isin(a1, OTHER_HISP_ANC) | np.isin(a2, OTHER_HISP_ANC)) & ~mex_anc
    hisp = d["HISP"].to_numpy()
    mex_hisp = hisp == 2
    any_hisp = hisp != 1
    other_hisp = any_hisp & ~mex_hisp
    mex_born = (d["POBP"] == MEXICO_POBP).to_numpy()
    foreign = (d["NATIVITY"] == 2).to_numpy()
    anc_missing = (a1 >= 996) & (a2 >= 996)

    rows = []

    def add(label: str, mask: np.ndarray, note: str = "") -> None:
        t, se, n = total(d, mask)
        rows.append({"cell": label, "population": round(t, 1), "se": round(se, 1),
                     "unweighted_n": n, "note": note})
        print(f"  {label:<52} {t/1e6:8.3f}M  se {se/1e6:.3f}M  n={n:,}", flush=True)

    print("\nArm 2 -- ACS 2024 1-year PUMS, ancestry against Hispanic origin", flush=True)
    add("total population", np.ones(len(d), bool))
    add("Mexico-born (POBP=303)", mex_born)
    add("HISP = Mexican", mex_hisp)
    add("Mexican ancestry (ANC1P or ANC2P)", mex_anc)

    print("\n  cross-tab of the two self-reports", flush=True)
    add("Mexican ancestry AND HISP Mexican", mex_anc & mex_hisp)
    add("Mexican ancestry, HISP other Hispanic", mex_anc & other_hisp,
        "claims Mexican ancestry, reports a different Hispanic origin")
    add("Mexican ancestry, HISP NOT Hispanic", mex_anc & ~any_hisp,
        "ancestry without Hispanic origin -- the attrition-visible cell")
    add("HISP Mexican, NO Mexican ancestry", mex_hisp & ~mex_anc)
    add("HISP Mexican, no Mexican ancestry, other Hispanic ancestry",
        mex_hisp & ~mex_anc & other_hisp_anc)
    add("HISP Mexican, ancestry not reported", mex_hisp & anc_missing)

    print("\n  definition totals", flush=True)
    add("UNION ancestry-or-origin (Mexico-born | HISP Mex | Mex anc)",
        mex_born | mex_hisp | mex_anc)
    add("ancestry-only definition (Mexican ancestry | Mexico-born)", mex_anc | mex_born)
    add("origin-only definition (HISP Mexican | Mexico-born)", mex_hisp | mex_born)
    pd.DataFrame(rows).to_csv(DERIVED / "arm2_ancestry_crosstab.csv", index=False)

    # by nativity and by generation proxy
    nrows = []
    for nat_label, nat in (("foreign-born", foreign), ("US-born", ~foreign)):
        for lab, m in (("HISP Mexican", mex_hisp),
                       ("Mexican ancestry", mex_anc),
                       ("both", mex_anc & mex_hisp),
                       ("ancestry only, not Hispanic", mex_anc & ~any_hisp),
                       ("ancestry only, other Hispanic origin", mex_anc & other_hisp),
                       ("HISP Mexican without Mexican ancestry", mex_hisp & ~mex_anc),
                       ("union of the two", mex_hisp | mex_anc)):
            t, se, n = total(d, m & nat)
            nrows.append({"nativity": nat_label, "cell": lab,
                          "population": round(t, 1), "se": round(se, 1),
                          "unweighted_n": n})
            print(f"  {nat_label:<13} {lab:<42} {t/1e6:8.3f}M  se {se/1e6:.3f}M", flush=True)
    pd.DataFrame(nrows).to_csv(DERIVED / "arm2_ancestry_by_nativity.csv", index=False)

    # headline totals with the CPS union alongside
    t_union, se_union, _ = total(d, mex_born | mex_hisp | mex_anc)
    t_selfid, se_selfid, _ = total(d, mex_hisp | mex_born)
    t_anc, se_anc, _ = total(d, mex_anc)
    trows = [
        {"definition": "ACS self-identification (HISP Mexican or Mexico-born)",
         "population": round(t_selfid, 1), "se": round(se_selfid, 1)},
        {"definition": "ACS ancestry write-in (ANC1P/ANC2P Mexican)",
         "population": round(t_anc, 1), "se": round(se_anc, 1)},
        {"definition": "ACS union of both self-reports",
         "population": round(t_union, 1), "se": round(se_union, 1)},
        {"definition": "gain from adding the ancestry question",
         "population": round(t_union - t_selfid, 1), "se": None},
    ]
    pd.DataFrame(trows).to_csv(DERIVED / "arm2_ancestry_totals.csv", index=False)

    # Emeka & Vallejo 2011 (Social Science Research 40(6)) report that in the 2006
    # ACS, 6% of respondents with Latin American ancestry answered "no" to the
    # Hispanic-origin question.  Their PDF is paywalled and was NOT obtained, so
    # the 6% is [UNVERIFIED] -- taken from the Semantic Scholar abstract record,
    # not from the paper.  The same statistic rebuilt on ACS 2024:
    any_latin_anc = mex_anc | (np.isin(a1, OTHER_HISP_ANC) | np.isin(a2, OTHER_HISP_ANC))
    ev = []
    for lab, den, num in (
        ("all Latin American / Hispanic ancestry (Emeka-Vallejo analogue)",
         any_latin_anc, any_latin_anc & ~any_hisp),
        ("Mexican ancestry only", mex_anc, mex_anc & ~any_hisp),
    ):
        dt_, dse, dn = total(d, den)
        nt_, nse, nn = total(d, num)
        ev.append({"denominator": lab,
                   "with_ancestry": round(dt_, 1),
                   "answered_not_hispanic": round(nt_, 1),
                   "pct_not_hispanic_2024": round(100 * nt_ / dt_, 2),
                   "pct_not_hispanic_2006_emeka_vallejo": 6.0 if "all Latin" in lab else None,
                   "unweighted_n_denominator": dn})
        print(f"  {lab:<58} {100*nt_/dt_:5.2f}% answer 'not Hispanic'", flush=True)
    pd.DataFrame(ev).to_csv(DERIVED / "arm2_emeka_vallejo.csv", index=False)
    print(f"\n  ancestry adds {(t_union-t_selfid)/1e6:.3f}M over the ACS self-ID definition",
          flush=True)
    print("wrote derived/arm2_*.csv", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
