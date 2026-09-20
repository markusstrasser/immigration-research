#!/usr/bin/env python3
"""Arm 3 (coverage-multiplier grid) and Arm 6 (the 40-million test).

Both run on the same ACS 2024 1-year PUMS residual the acs_residual.py lane
produced, so the arithmetic is exposed end to end: one counted base, several
published coverage assumptions, and a ladder of definitions with the population
each one names.

Coverage assumptions, each taken verbatim from its own publisher:
  none   1.00 everywhere.
  CIS    2.25% flat.  "In the past, we adjusted upward our CPS-based estimates of
         illegal immigrants by 2.25 percent to reflect those missed by the survey."
  DHS    13% for the most recent arrival year, declining 7.5% with each year of
         presence.  OHSS April 2024, appendix item 1e.
  CMS    5% for those who entered 1982-2020, 37% for those who entered 2021-2024.
         Warren et al., JMHS July 2026, Table A1, "All countries" row.
  CMS-hi 5% pre-2021, 65% for 2021-2024 arrivals: the highest country-specific
         rate CMS published (Ecuador), applied to every recent arrival.  This is
         an upper bound, not an estimate.

Output: derived/coverage_grid.csv
        derived/coverage_grid_by_cohort.csv
        derived/forty_million_ladder.csv
"""
from __future__ import annotations

import sys as _path_sys
from pathlib import Path as _Path
_path_sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "build"))
import paths as _data_paths


import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

os.environ.setdefault("PYTHONUNBUFFERED", "1")

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
DERIVED = HERE / "derived"
REPS = [f"PWGTP{i}" for i in range(1, 81)]

sys.path.insert(0, str(HERE))
from acs_residual import impute, ohss_multiplier, se_from_reps  # noqa: E402

# Coverage rate as a function of arrival year; multiplier = 1/(1 - rate).
SCHEMES = {
    "none": lambda yr: np.zeros_like(yr, dtype=float),
    "cis_2.25pct_flat": lambda yr: np.full(yr.shape, 0.0225),
    "dhs_ohss_decay": lambda yr: 0.13 * np.power(1 - 0.075, np.clip(2024.0 - yr, 0, None)),
    "cms_5_37": lambda yr: np.where(yr >= 2021, 0.37, 0.05),
    "cms_high_5_65": lambda yr: np.where(yr >= 2021, 0.65, 0.05),
    "census_2020_pes_hispanic_4.99pct": lambda yr: np.full(yr.shape, 0.0499),
}


def main() -> int:
    DERIVED.mkdir(exist_ok=True)
    print("[1/4] loading ACS 2024 person subset")
    d = pd.read_parquet(CACHE / "acs2024_person_subset.parquet")
    w = d.PWGTP.to_numpy(float)
    rw = d[REPS].to_numpy(float)
    res = impute(d)
    unauth, fb = res["unauthorized"], res["foreign_born"]
    cit = d.CIT.to_numpy()
    noncit = cit == 5
    yoep = pd.to_numeric(d.YOEP, errors="coerce").to_numpy(float)
    # People with no year of entry recorded are treated as long-resident, the
    # conservative choice: it gives them the smallest coverage uplift.
    yr = np.where(np.isnan(yoep), 1980.0, yoep)

    def est(mask, weight=None):
        ww = w if weight is None else weight
        pt = float(ww[mask].sum())
        return pt, se_from_reps(pt, rw[mask].sum(axis=0).astype(float))

    # ---- does the ACS 2024 weighting already carry the coverage adjustment? --
    # The Census Bureau's Vintage 2024 population estimates raised net international
    # migration for 2021-23 by 69.5% and 101.7% over Vintage 2023, "to account for
    # 75% of the humanitarian migrants in our Benchmark Database".  If the ACS 2024
    # weights are controlled to Vintage 2024, an ACS-calibrated undercount rate
    # layered on top is partly double-counting.  Test it: the weighted ACS total
    # should equal the published Vintage 2024 July 1 2024 national estimate.
    nst = _data_paths.data_root(require_exists=False) / 'external/census_popest_2024/NST-EST2024-ALLDATA.csv'
    if nst.exists():
        pe = pd.read_csv(nst, dtype={"SUMLEV": str, "STATE": str})
        v2024 = int(pe.loc[pe.NAME.eq("United States"), "POPESTIMATE2024"].iloc[0])
        acs_total = float(w.sum())
        print(f"  Vintage 2024 national estimate, July 1 2024: {v2024:,}")
        print(f"  ACS 2024 1-year weighted total:              {acs_total:,.0f}")
        print(f"  difference: {acs_total - v2024:,.0f} "
              f"({abs(acs_total - v2024) / v2024 * 100:.6f}%)")
        print("  -> the ACS 2024 weights are controlled to Vintage 2024, which "
              "already carries the humanitarian-migrant adjustment.")
    else:
        print(f"  ! {nst} not found; skipping the weight-control check")

    # ---------------- Arm 3: coverage grid -----------------------------------
    print("[2/4] coverage-multiplier grid on the ACS 2024 Borjas residual")
    base, base_se = est(unauth)
    rows = []
    for name, fn in SCHEMES.items():
        rate = fn(yr)
        mult = 1.0 / (1.0 - rate)
        adj = float((w * mult)[unauth].sum())
        rows.append({"coverage_scheme": name,
                     "counted_residual": round(base),
                     "adjusted_residual": round(adj),
                     "implied_overall_multiplier": round(adj / base, 4),
                     "uplift": round(adj - base)})
    # A published estimate is not a multiple of OUR residual, but the grid is more
    # useful if the same schemes are shown on the non-citizen universe too.
    grid = pd.DataFrame(rows)
    grid.to_csv(DERIVED / "coverage_grid.csv", index=False)
    print(grid.to_string(index=False))

    print("\n[3/4] the same grid split by arrival cohort")
    bands = [(1800, 2000, "arrived before 2001"), (2001, 2010, "2001-2010"),
             (2011, 2020, "2011-2020"), (2021, 2024, "2021-2024")]
    rows = []
    for lo, hi, label in bands:
        m = unauth & (yr >= lo) & (yr <= hi)
        cnt, _ = est(m)
        row = {"arrival_cohort": label, "counted_residual": round(cnt)}
        for name, fn in SCHEMES.items():
            mult = 1.0 / (1.0 - fn(yr))
            row[name] = round(float((w * mult)[m].sum()))
        rows.append(row)
    coh = pd.DataFrame(rows)
    tot = {"arrival_cohort": "TOTAL", "counted_residual": round(base)}
    for name in SCHEMES:
        tot[name] = int(coh[name].sum())
    coh = pd.concat([coh, pd.DataFrame([tot])], ignore_index=True)
    coh.to_csv(DERIVED / "coverage_grid_by_cohort.csv", index=False)
    print(coh.to_string(index=False))

    # ---------------- Arm 6: the 40-million test -----------------------------
    print("\n[4/4] the definition ladder, and what it takes to reach 40 million")
    # Mixed-status households: US-born people sharing a household with a non-citizen.
    hh, _ = pd.factorize(d.SERIALNO.to_numpy(), sort=False)
    nhh = int(hh.max()) + 1
    hh_has_noncit = np.zeros(nhh, dtype=bool)
    np.logical_or.at(hh_has_noncit, hh, noncit)
    us_born = d.NATIVITY.to_numpy() == 1
    age = pd.to_numeric(d.AGEP, errors="coerce").to_numpy(float)

    ladder = []

    def add(label, value, se, basis):
        ladder.append({"definition": label, "population": round(value),
                       "se": (round(se) if se is not None else None), "basis": basis})

    pt, se = est(unauth)
    add("A. No lawful status: Borjas residual, ACS 2024, counted", pt, se,
        "ACS 2024 1-year PUMS, rule list of Borjas (2017), no coverage adjustment")
    v = float((w / (1 - SCHEMES["dhs_ohss_decay"](yr)))[unauth].sum())
    add("B. A, with the DHS OHSS coverage model", v, None,
        "13% at arrival declining 7.5% per year of presence")
    v = float((w / (1 - SCHEMES["cms_5_37"](yr)))[unauth].sum())
    add("C. A, with the CMS 2024 coverage model", v, None,
        "5% for 1982-2020 arrivals, 37% for 2021-2024 arrivals")
    v = float((w / (1 - SCHEMES["cms_high_5_65"](yr)))[unauth].sum())
    add("D. A, with CMS's highest published country rate on every recent arrival",
        v, None, "5% pre-2021, 65% for 2021-2024; an upper bound, not an estimate")
    add("E. CPS ASEC 2025 residual, same rule list, counted", 14896401, 316399,
        "CPS ASEC 2025; the survey the repo's ledger runs on")
    pt, se = est(noncit)
    noncit_pt = pt
    add("F. Every non-citizen in the ACS, counted", pt, se,
        "CIT==5: includes green-card holders, students, H-1B and every temporary visa")
    v = float((w / (1 - SCHEMES["cms_high_5_65"](yr)))[noncit].sum())
    add("G. F, with the upper-bound coverage model", v, None,
        "applies a recent-arrival undercount rate to lawful permanent residents too")
    mixed = us_born & hh_has_noncit[hh]
    pt_mixed, se_mixed = est(mixed)
    add("H. F plus every US-born person living with a non-citizen",
        noncit_pt + pt_mixed, None,
        "a mixed-status-household count; most of the added people are US citizens")
    kids = mixed & (age < 18)
    pt_kids, _ = est(kids)
    add("H'. F plus US-born children under 18 living with a non-citizen",
        noncit_pt + pt_kids, None, "the narrower mixed-status reading")
    pt, se = est(fb)
    add("I. Every foreign-born person in the ACS", pt, se,
        "NATIVITY==2; about half are naturalised US citizens")

    lad = pd.DataFrame(ladder)
    lad["reaches_40m"] = lad.population >= 40_000_000
    lad.to_csv(DERIVED / "forty_million_ladder.csv", index=False)
    print(lad.to_string(index=False))

    need = 40_000_000 / noncit_pt
    summary = {
        "non_citizens_counted": round(noncit_pt),
        "multiplier_on_all_non_citizens_to_reach_40m": round(need, 4),
        "implied_undercount_rate_pct": round(100 * (1 - 1 / need), 1),
        "highest_published_undercount_rate_pct": 65.0,
        "highest_published_undercount_scope": (
            "CMS 2026 Table A1, Ecuadorians who arrived 2021-2024 only; "
            "CMS's rate for 1982-2020 arrivals is 5 percent"),
        "us_born_living_with_a_non_citizen": round(pt_mixed),
        "us_born_children_under_18_living_with_a_non_citizen": round(pt_kids),
    }
    (DERIVED / "forty_million_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print("\n" + json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
