#!/usr/bin/env python3
"""Questions 1 and 4 (counts): why US-born adults leave California, against other states' leavers
and movers into Texas, from the CPS ASEC main reason for moving (IPUMS WHYMOVE), 1999-2025.

Survey year t covers moves between March t-1 and March t. Standard errors: replicate weights from
2005; a design-factor-scaled household-cluster variance for 1999-2004 (lane_common.Var).

Writes derived/:
  reasons_ca_leavers.csv      reason shares, US-born adult California leavers, by window and variant
  ppic_crosscheck.csv         all adult California leavers in the 2010s, against PPIC's published shares
  reasons_compare.csv         the same for other states' leavers, movers into Texas, California to Texas
  reasons_ca_by_year.csv      California leavers year by year and by period
  reasons_ca_by_subgroup.csv  California leavers by race and ethnicity, education, income, age
  q4_counts.csv               neighborhood/crime movers per year, CPS level and ACS-scaled level
  income_weighted_shares.csv  share of leavers' and in-movers' household income in each reason group
  design_factor.json          the variance calibration used for 1999-2004

Run from the repository root after build_cps.py and check_census.py:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/movers_reasons_2026_09_24/reasons.py
"""
import json

import numpy as np
import pandas as pd

from lane_common import (ANOMALY_YEARS, BUILD, DERIVED, DETAIL, GROUPS, REP, STATES, Var, con, cpi_2024,
                         load_interstate, write_csv)

EXTRA = ["cheaper_housing", "better_housing", "own_home"]
OUTCOMES = GROUPS + EXTRA
WINDOWS = {"2005-2025": (2005, 2025), "1999-2025": (1999, 2025), "1999-2004": (1999, 2004),
           "1999-2005": (1999, 2005), "2006-2011": (2006, 2011), "2012-2015": (2012, 2015),
           "2016-2019": (2016, 2019), "2020-2025": (2020, 2025)}


def shares(d: pd.DataFrame, label: dict, years: int) -> list[dict]:
    rows = []
    for y in OUTCOMES:
        th, se, _, _ = Var.ratio(d, y)
        rows.append({**label, "reason": y, "share_pct": round(100 * th, 2), "se_pp": round(100 * se, 2),
                     "n": int(len(d)), "n_citing": int(d[y].sum()),
                     "weighted_persons_per_year": round(float(d.wt.sum()) / years)})
    return rows


def window(d: pd.DataFrame, w: str, exclude_anomaly=False) -> tuple[pd.DataFrame, int]:
    lo, hi = WINDOWS[w]
    sel = d.YEAR.between(lo, hi)
    if exclude_anomaly:
        sel &= ~d.YEAR.isin(ANOMALY_YEARS)
    yrs = sorted(d.loc[sel, "YEAR"].unique())
    return d[sel], len(yrs)


def main() -> None:
    c = con()
    cpi = cpi_2024(c)
    d = load_interstate(c, cpi)
    ua = d[d.usb & d.adult].copy()
    cal = Var.calibrate(ua)
    (DERIVED / "design_factor.json").write_text(json.dumps(cal, indent=2) + "\n")
    print(f"design factor for 1999-2004 SEs: {cal['design_factor']:.3f} (ratios {cal['ratios']})")

    ca = ua[ua.MIGSTA1 == 6]

    # --- Table 1: California leavers, windows and variants
    t1 = []
    for w in ("2005-2025", "1999-2025", "1999-2004"):
        dd, ny = window(ca, w)
        t1 += shares(dd, {"population": "US-born adults leaving California", "window": w, "variant": "all records"}, ny)
    dd, ny = window(ca, "2005-2025", exclude_anomaly=True)
    t1 += shares(dd, {"population": "US-born adults leaving California", "window": "2005-2025",
                      "variant": "excluding ASEC 2012-2015 (code anomaly)"}, ny)
    dd, ny = window(ca, "2005-2025")
    t1 += shares(dd[~dd.allocated], {"population": "US-born adults leaving California", "window": "2005-2025",
                                     "variant": "excluding allocated migration status or origin state"}, ny)
    dd, ny = window(ca, "2005-2025")
    dd = dd.copy()
    # detailed codes, main window
    for code, lab in DETAIL.items():
        dd["_c"] = (dd.WHYMOVE == code).astype(float)
        th, se, _, _ = Var.ratio(dd, "_c")
        t1.append({"population": "US-born adults leaving California", "window": "2005-2025",
                   "variant": "detailed code", "reason": f"{code:02d} {lab}", "share_pct": round(100 * th, 2),
                   "se_pp": round(100 * se, 2), "n": int(len(dd)), "n_citing": int(dd._c.sum()),
                   "weighted_persons_per_year": round(float(dd.wt.sum()) / ny)})
    write_csv(pd.DataFrame(t1), "reasons_ca_leavers.csv")

    # --- PPIC cross-check: adults of any nativity who left California in the 2010s. Johnson (PPIC
    # blog, 2021-05-06) reports jobs 49%, housing 23% and family 20% from the CPS for that population.
    tp = []
    for w, lo, hi in (("ASEC 2011-2020", 2011, 2020), ("ASEC 2010-2019", 2010, 2019)):
        dd = d[d.adult & (d.MIGSTA1 == 6) & d.YEAR.between(lo, hi)]
        tp += shares(dd, {"population": "adults of any nativity leaving California", "window": w}, dd.YEAR.nunique())
    write_csv(pd.DataFrame(tp), "ppic_crosscheck.csv")

    # --- Table 2: comparisons, 2005-2025 and 1999-2025
    pops = {"California leavers": ua.MIGSTA1 == 6}
    for s in (36, 17, 34, 25, 53, 48, 12, 4, 32, 35):
        pops[f"{STATES[s]} leavers"] = ua.MIGSTA1 == s
    pops["leavers of all other states"] = ua.MIGSTA1 != 6
    pops["movers into Texas, all origins"] = ua.STATEFIP == 48
    pops["movers into Texas from outside California"] = (ua.STATEFIP == 48) & (ua.MIGSTA1 != 6)
    pops["California to Texas"] = (ua.MIGSTA1 == 6) & (ua.STATEFIP == 48)
    pops["California to other states except Texas"] = (ua.MIGSTA1 == 6) & (ua.STATEFIP != 48)
    t2 = []
    for w in ("2005-2025", "1999-2025"):
        base, ny = window(ca, w)
        for name, sel in pops.items():
            dd, nyy = window(ua[sel], w)
            rows = shares(dd, {"population": f"US-born adults: {name}", "window": w}, nyy)
            for r in rows:
                if name != "California leavers" and not name.startswith("California to"):
                    df_, sed = Var.diff(base, dd, r["reason"])
                    r["ca_minus_this_pp"] = round(100 * df_, 2)
                    r["ca_minus_this_se_pp"] = round(100 * sed, 2)
            t2 += rows
    write_csv(pd.DataFrame(t2), "reasons_compare.csv")

    # --- Table 3: by year and by period
    t3 = []
    for y in sorted(ca.YEAR.unique()):
        dd = ca[ca.YEAR == y]
        for r in shares(dd, {"population": "US-born adults leaving California", "period": str(y)}, 1):
            r["se_method"] = "replicate" if y >= 2005 else f"cluster x design factor {Var.DESIGN_FACTOR:.2f}"
            r["note"] = ("NXTRES code anomaly" if y in ANOMALY_YEARS else
                         "pre-2006 migration imputation" if y <= 2005 else "")
            t3.append(r)
    for w in ("1999-2005", "2006-2011", "2012-2015", "2016-2019", "2020-2025"):
        dd, ny = window(ca, w)
        t3 += shares(dd, {"population": "US-born adults leaving California", "period": w}, ny)
        do, nyo = window(ua[ua.MIGSTA1 != 6], w)
        t3 += shares(do, {"population": "US-born adults leaving all other states", "period": w}, nyo)
    write_csv(pd.DataFrame(t3), "reasons_ca_by_year.csv")

    # --- Table 4: subgroups, 2005-2025, California against all other states' leavers
    t4 = []
    base, ny = window(ca, "2005-2025")
    other, nyo = window(ua[ua.MIGSTA1 != 6], "2005-2025")
    for dim in ("race_eth", "educ4", "inc_band", "age_band"):
        for lev in sorted(base[dim].dropna().unique()):
            b = base[base[dim] == lev]
            o = other[other[dim] == lev]
            if len(b) < 30:
                continue
            for y in ("neighborhood_crime", "housing", "cheaper_housing", "jobs", "family", "climate", "retirement"):
                th, se, _, _ = Var.ratio(b, y)
                tho, seo, _, _ = Var.ratio(o, y)
                df_, sed = Var.diff(b, o, y)
                t4.append({"dimension": dim, "level": lev, "reason": y, "ca_share_pct": round(100 * th, 2),
                           "ca_se_pp": round(100 * se, 2), "ca_n": len(b), "other_states_share_pct": round(100 * tho, 2),
                           "other_se_pp": round(100 * seo, 2), "other_n": len(o),
                           "ca_minus_other_pp": round(100 * df_, 2), "diff_se_pp": round(100 * sed, 2)})
    write_csv(pd.DataFrame(t4), "reasons_ca_by_subgroup.csv")

    # --- Q4 counts: neighborhood/crime movers per year, computed one year at a time.
    # ACS level: each year's CPS count times that year's ACS/CPS ratio for all California leavers
    # (ACS state-to-state tables, gate_movers_count.csv); in years without a published ACS pair
    # (ASEC 2005-2010, 2020, 2021, 2025) the mean ratio of the published years is used.
    cnt = pd.read_csv(DERIVED / "gate_movers_count.csv")
    scale = {r.asec_year: r.acs_mean_ca_out / r.cps_ca_out for r in cnt.itertuples()
             if not pd.isna(getattr(r, "acs_mean_ca_out", np.nan))}
    s_bar = float(np.mean(list(scale.values())))
    # at-risk population: US-born adults who lived in California a year earlier (CPS, weighted)
    at_risk = dict(c.execute(f"select YEAR, usborn_adult from read_parquet('{BUILD / 'state_cells.parquet'}') "
                             "where state = 6 and basis = 'year_ago'").fetchall())
    by_year = []
    for y in sorted(ca.YEAR.unique()):
        dd = ca[ca.YEAR == y]
        nb = dd[dd.neighborhood_crime == 1]
        p_, h_ = float(nb.wt.sum()), float(nb.drop_duplicates(["YEAR", "SERIAL"]).wth.sum())
        s_ = scale.get(y, s_bar)
        by_year.append({"asec_year": y, "all_leavers_cps": float(dd.wt.sum()), "persons_cps": p_, "households_cps": h_,
                        "acs_to_cps_scale_own": scale.get(y), "scale_used": s_,
                        "persons_acs_scaled": p_ * s_, "households_acs_scaled": h_ * s_,
                        "ca_usborn_adults_year_ago": at_risk[y], "persons_cps_per_1000": 1000 * p_ / at_risk[y],
                        "persons_acs_scaled_per_1000": 1000 * p_ * s_ / at_risk[y],
                        "all_leavers_cps_per_1000": 1000 * float(dd.wt.sum()) / at_risk[y]})
    by = pd.DataFrame(by_year)
    q4, means = [], []
    for w, lo, hi in (("2005-2025", 2005, 2025), ("2016-2025", 2016, 2025), ("2020-2025", 2020, 2025)):
        dd = ca[ca.YEAR.between(lo, hi)]
        ny = dd.YEAR.nunique()
        nb = dd[dd.neighborhood_crime == 1]
        per_year, se = Var.total(nb, ny)
        all_per_year, se_all = Var.total(dd, ny)
        yy = by[by.asec_year.between(lo, hi)]
        own = yy[yy.acs_to_cps_scale_own.notna()]
        if abs(yy.persons_cps.mean() - per_year) > 1:
            raise SystemExit(f"[FAILED] pooled per-year count differs from the mean of single years in {w}")
        q4.append({"window": w, "years": ny, "population": "US-born adults leaving California",
                   "all_leavers_per_year_cps": round(all_per_year), "all_leavers_se": round(se_all),
                   "nbhd_crime_persons_per_year_cps": round(per_year), "nbhd_crime_se": round(se),
                   "nbhd_crime_households_per_year_cps": round(yy.households_cps.mean()),
                   "acs_scale_mean_published_years": round(s_bar, 3), "years_with_own_acs_ratio": len(own),
                   "nbhd_crime_persons_per_year_acs_scaled": round(yy.persons_acs_scaled.mean()),
                   "nbhd_crime_households_per_year_acs_scaled": round(yy.households_acs_scaled.mean()),
                   "nbhd_crime_persons_per_year_acs_own_years_only": round(own.persons_acs_scaled.mean()) if len(own) else None,
                   "nbhd_crime_households_per_year_acs_own_years_only": round(own.households_acs_scaled.mean()) if len(own) else None,
                   "nbhd_crime_per_1000_cps": round(yy.persons_cps_per_1000.mean(), 3),
                   "nbhd_crime_per_1000_acs_scaled": round(yy.persons_acs_scaled_per_1000.mean(), 3),
                   "all_leavers_per_1000_cps": round(yy.all_leavers_cps_per_1000.mean(), 2)})
        means.append({"asec_year": f"mean {w}", **{c: yy[c].mean() for c in yy.columns if c != "asec_year"}})
    for name, sel in (("US-born adult interstate movers, all states", ua.index == ua.index),
                      ("US-born adults moving into California", ua.STATEFIP == 6)):
        dd = ua[sel & ua.YEAR.between(2005, 2025)]
        ny = dd.YEAR.nunique()
        nb = dd[dd.neighborhood_crime == 1]
        per_year, se = Var.total(nb, ny)
        q4.append({"window": "2005-2025", "years": ny, "population": name,
                   "all_leavers_per_year_cps": round(Var.total(dd, ny)[0]),
                   "nbhd_crime_persons_per_year_cps": round(per_year), "nbhd_crime_se": round(se),
                   "nbhd_crime_households_per_year_cps": round(float(nb.drop_duplicates(['YEAR', 'SERIAL']).wth.sum()) / ny)})
    write_csv(pd.DataFrame(q4), "q4_counts.csv")
    write_csv(pd.concat([by, pd.DataFrame(means)], ignore_index=True).round(3), "q4_counts_by_year.csv")

    # --- income-weighted reason shares (householders, all nativities): out of and into California.
    # A householder's person weight is the household weight, so weights and replicate weights are
    # both multiplied by household income (2024 dollars, in $100k units).
    iw = []
    hhd = d[(d.RELATE == 101) & d.YEAR.between(2005, 2025) & d.hhinc24.notna() & (d.hhinc24 > 0)].copy()
    for name, sel in (("householders leaving California", hhd.MIGSTA1 == 6),
                      ("householders moving into California", hhd.STATEFIP == 6),
                      ("householders California to Texas", (hhd.MIGSTA1 == 6) & (hhd.STATEFIP == 48)),
                      ("householders Texas to California", (hhd.MIGSTA1 == 48) & (hhd.STATEFIP == 6))):
        dd = hhd[sel].copy()
        mean_inc = float((dd.wt * dd.hhinc24).sum() / dd.wt.sum())
        f = (dd.hhinc24 / 1e5).to_numpy()
        dd["wt"] = dd.wt * f
        dd[REP] = dd[REP].to_numpy() * f[:, None]
        for y in ("neighborhood_crime", "housing", "jobs", "family", "retirement", "climate", "other"):
            th, se, _, _ = Var.ratio(dd, y)
            iw.append({"population": name, "reason": y, "income_weighted_share_pct": round(100 * th, 2),
                       "se_pp": round(100 * se, 2), "n_households": len(dd),
                       "mean_hhinc_2024usd": round(mean_inc)})
    write_csv(pd.DataFrame(iw), "income_weighted_shares.csv")

    main_nb = [r for r in t1 if r["window"] == "2005-2025" and r["variant"] == "all records"
               and r["reason"] == "neighborhood_crime"][0]
    print(f"CA US-born adult leavers 2005-2025: neighborhood/crime {main_nb['share_pct']}% "
          f"(SE {main_nb['se_pp']}), n={main_nb['n']}")


if __name__ == "__main__":
    main()
