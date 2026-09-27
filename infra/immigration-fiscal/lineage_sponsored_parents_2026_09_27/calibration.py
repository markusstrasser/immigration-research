#!/usr/bin/env python3
"""Calibrate E, the Mexican IR-5 parents admitted per naturalised Mexico-born citizen, and
p = E / m, the probability a naturalised founder petitions for their surviving parents.

Estimators (all parents per newly eligible citizen; steady-state flow ratios):
  equal_hazard  IR-5 parents a year / (Mexican naturalisations a year + US-born children of
                Mexico-born parents turning 21 a year). Treats naturalised and US-born
                petitioners as equally likely to petition.
  age_bound     IR-5 parents aged 55+ at admission / Mexican naturalisations: gives every parent
                admitted at 55+ to a naturalised petitioner and every parent under 55 to a US-born
                one. An upper bound for the naturalised channel if naturalised petitioners' parents
                are all 55+ (a founder naturalising at 30 or later has a parent of about 55+).
  stock_hazard  IR-5 parents a year / (naturalised Mexico-born adults + US-born adults 21+ with a
                Mexico-born parent), an annual hazard per eligible citizen, times the remaining
                life expectancy of a parent aged 59 (the L25 founder's parent at naturalisation).

Writes derived/calibration.csv and derived/calibration.json.
"""
from __future__ import annotations

import json
import re
import sys
from html import unescape

import numpy as np
import pandas as pd

import common as C

NAT_HTML = C.HERE / "_cache/nat_fy24.html"
NAT_URL = ("https://ohss.dhs.gov/topics/immigration/naturalizations/annual-flow-report/"
           "fy-24-naturalizations-flow-report")
# OHSS FY2024 Naturalizations Annual Flow Report, Table 2, Mexico row; parsed from the cached
# page below and checked against these values.
NAT_MEXICO = {2022: 128880, 2023: 111460, 2024: 107670}
NIS_MEX_55PLUS = None  # read from ir5_age_nis2003.csv
NAT_RATE = 0.619


def naturalisations() -> dict:
    t = NAT_HTML.read_text()
    t = re.sub(r"<script.*?</script>|<style.*?</style>", "", t, flags=re.S)
    t = re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", t)))
    m = re.search(r"Table 2\. Persons Naturalized by Country of Birth.*?Mexico ([\d,]+) [\d.]+% "
                  r"([\d,]+) [\d.]+% ([\d,]+) [\d.]+%", t)
    if not m:
        raise SystemExit("[BLOCKED] OHSS Table 2 Mexico row not found in the cached page")
    got = dict(zip((2022, 2023, 2024), (int(x.replace(",", "")) for x in m.groups())))
    if got != NAT_MEXICO:
        raise SystemExit(f"[BLOCKED] Table 2 Mexico row {got} != {NAT_MEXICO}")
    return got


def main() -> int:
    ctx = C.Ctx()
    nat = naturalisations()
    flow = pd.read_csv(C.LATE_DIR / "derived/ir5_flow.csv")
    mx = flow[flow.country == "mexico"].set_index("fy")
    nis = pd.read_csv(C.LATE_DIR / "derived/ir5_age_nis2003.csv").set_index("group")
    nis55 = float(nis.loc["mexico", "age_55plus"])
    bound2005 = float(mx.loc[2005, "ir5_55plus_upper_bound_share"])  # NIS-era profile bound
    share55 = {y: (float(mx.loc[y, "ir5_55plus_upper_bound_share"]) * nis55 / bound2005,
                   float(mx.loc[y, "ir5_55plus_upper_bound_share"])) for y in mx.index}
    nat_adults = pd.read_csv(C.FISCAL / "origin_attachment_mexico_2026_09_27/derived/"
                                        "naturalization_share_2024.csv").set_index("country")
    nat_stock = float(nat_adults.loc["Mexico", "acs2024_naturalized_adults"])
    comp = ctx.comps
    pop = (comp[(comp.allocation == "personal") & (comp.account == "expanded")
                & (comp.group == "mexican_second_gen")].groupby("band").population.first())
    g2_turn21 = float(pop.loc[1]) / 7.0                       # band 18-24, one single year
    g2_21plus = float(pop.loc[1]) * 4.0 / 7.0 + float(pop.loc[2:].sum())
    tab = ctx.tables["total"]
    e59 = float(tab.Lx.to_numpy()[59:].sum() / tab.lx.iloc[59])

    windows = {"low": (list(range(2015, 2025)), [2022, 2023, 2024]),
               "central": ([2022, 2023, 2024], [2022, 2023, 2024]),
               "high": ([2024], [2024])}
    rows = []
    for label, (fys, nys) in windows.items():
        ir5 = float(np.mean([mx.loc[y, "ir5_parents"] for y in fys]))
        naturalised = float(np.mean([nat[y] for y in nys]))
        s55_c = float(np.mean([share55[y][0] for y in fys]))
        s55_u = float(np.mean([share55[y][1] for y in fys]))
        est = {"equal_hazard": ir5 / (naturalised + g2_turn21),
               "age_bound_nis_ratio": ir5 * s55_c / naturalised,
               "age_bound_ceiling": ir5 * s55_u / naturalised,
               "stock_hazard_x_e59": ir5 / (nat_stock + g2_21plus) * e59}
        for name, e in est.items():
            rows.append({"window": label, "ir5_fy": f"{fys[0]}-{fys[-1]}",
                         "ir5_parents_per_year": ir5,
                         "naturalisations_fy": f"{nys[0]}-{nys[-1]}",
                         "naturalisations_per_year": naturalised,
                         "g2_turning_21_per_year": g2_turn21, "naturalised_adults_2024": nat_stock,
                         "g2_adults_21plus": g2_21plus, "share_55plus_nis_ratio": s55_c,
                         "share_55plus_ceiling": s55_u, "e59_total_table": e59,
                         "estimator": name, "E_parents_per_naturalised": e})
    df = pd.DataFrame(rows)
    m60 = ctx.living_parents(60)
    df["m_living_parents_at_60"] = m60
    df["p_petition"] = df.E_parents_per_naturalised / m60
    df["parents_per_founder_lpr"] = NAT_RATE * df.E_parents_per_naturalised
    df.to_csv(C.HERE / "derived/calibration.csv", index=False, lineterminator="\n")
    pick = {"central": ("central", "equal_hazard"), "low": ("low", "equal_hazard"),
            "high": ("high", "age_bound_ceiling")}
    chosen = {k: float(df[(df.window == w) & (df.estimator == e)].E_parents_per_naturalised.iloc[0])
              for k, (w, e) in pick.items()}
    meta = {"naturalisation_rate": NAT_RATE, "nat_source": NAT_URL, "nat_mexico": nat,
            "nat_html_sha256": C.sha256(NAT_HTML), "E_chosen": chosen,
            "E_rule": {k: f"{w}/{e}" for k, (w, e) in pick.items()},
            "m_living_parents_at_60": m60,
            "resident_share": {"low": float(nis.loc["mexico", "share_adjusting"]),
                               "high": None}}
    adj = pd.read_csv(C.LATE_DIR / "derived/mexico_ir_new_vs_adjust.csv").set_index("fy")
    meta["resident_share"]["high"] = float(adj.loc[2024, "mexico_ir_adjustments"]
                                           / (adj.loc[2024, "mexico_ir_adjustments"]
                                              + adj.loc[2024, "mexico_ir_new_arrivals"]))
    (C.HERE / "derived/calibration.json").write_text(json.dumps(meta, indent=1, sort_keys=True) + "\n")
    print(df[["window", "estimator", "ir5_parents_per_year", "naturalisations_per_year",
              "E_parents_per_naturalised", "p_petition", "parents_per_founder_lpr"]].to_string())
    print(json.dumps(meta, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
