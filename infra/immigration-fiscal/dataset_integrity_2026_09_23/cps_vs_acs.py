"""CPS ASEC 2025 vs ACS 2024 1-year: Hispanic-origin detail and Mexico-born counts, household
population, by age band. Tests whether the CPS Mexican-origin count exceeds the ACS once the ACS
group-quarters population is removed. Reads the mexican_origin_population_total lane's cached
ACS subset (read-only) and the pinned CPS ZIP. Writes derived/cps_vs_acs_*.csv.
"""
from __future__ import annotations

import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
ACS = ROOT / "infra/immigration-fiscal/mexican_origin_population_total_2026_09_19/_cache/acs2024_ancestry_subset.parquet"
CPS = ROOT / "infra/immigration-fiscal/gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip"
BANDS = [0, 18, 25, 35, 45, 55, 65, 75, 200]
LABELS = ["0-17", "18-24", "25-34", "35-44", "45-54", "55-64", "65-74", "75+"]
# ACS HISP: 1 not Hispanic, 2 Mexican, 3 PR, 4 Cuban, 5 Dominican, 6-12 Central American,
# 13-23 South American, 24 Other Hispanic (Spaniard and other).
ACS_DETAIL = {"Mexican": [2], "Puerto Rican": [3], "Cuban": [4], "Dominican": [5],
              "Central American": list(range(6, 13)), "South American": list(range(13, 24)),
              "Other Hispanic": [24]}
CPS_DETAIL = {"Mexican": [1], "Puerto Rican": [2], "Cuban": [3], "Dominican": [4],
              "Central American": [5, 6], "South American": [7], "Other Hispanic": [8]}


def main() -> None:
    a = pd.read_parquet(ACS, columns=["SERIALNO", "PWGTP", "AGEP", "HISP", "POBP", "NATIVITY"])
    a["hh"] = ~a.SERIALNO.str.contains("GQ")
    with zipfile.ZipFile(CPS) as z:
        c = pd.read_csv(z.open("pppub25.csv"), usecols=["A_AGE", "PEHSPNON", "PRDTHSP", "PENATVTY",
                                                        "PRCITSHP", "PRPERTYP", "MARSUPWT"])
    c["w"] = c.MARSUPWT / 100
    rows = []
    for name in ACS_DETAIL:
        am = a.HISP.isin(ACS_DETAIL[name])
        cm = c.PRDTHSP.isin(CPS_DETAIL[name])
        rows.append(dict(origin=name, acs_all_m=a.PWGTP[am].sum() / 1e6,
                         acs_household_m=a.PWGTP[am & a.hh].sum() / 1e6,
                         cps_m=c.w[cm].sum() / 1e6))
    rows.append(dict(origin="All Hispanic", acs_all_m=a.PWGTP[a.HISP.gt(1)].sum() / 1e6,
                     acs_household_m=a.PWGTP[a.HISP.gt(1) & a.hh].sum() / 1e6,
                     cps_m=c.w[c.PEHSPNON.eq(1)].sum() / 1e6))
    rows.append(dict(origin="Mexico-born, foreign-born", acs_all_m=a.PWGTP[a.POBP.eq(303) & a.NATIVITY.eq(2)].sum() / 1e6,
                     acs_household_m=a.PWGTP[a.POBP.eq(303) & a.NATIVITY.eq(2) & a.hh].sum() / 1e6,
                     cps_m=c.w[c.PENATVTY.eq(303) & c.PRCITSHP.isin([4, 5])].sum() / 1e6))
    rows.append(dict(origin="Total population", acs_all_m=a.PWGTP.sum() / 1e6,
                     acs_household_m=a.PWGTP[a.hh].sum() / 1e6, cps_m=c.w.sum() / 1e6))
    t = pd.DataFrame(rows)
    t["cps_minus_acs_household_m"] = t.cps_m - t.acs_household_m
    t["cps_over_acs_household"] = t.cps_m / t.acs_household_m
    t.to_csv(HERE / "derived/cps_vs_acs_origin.csv", index=False)
    print(t.round(3).to_string())

    a["band"] = pd.cut(a.AGEP, BANDS, right=False, labels=LABELS)
    c["band"] = pd.cut(c.A_AGE, BANDS, right=False, labels=LABELS)
    rows = []
    for lab, am, cm in [("Mexican self-ID", a.HISP.eq(2), c.PRDTHSP.eq(1)),
                        ("Mexico-born FB", a.POBP.eq(303) & a.NATIVITY.eq(2), c.PENATVTY.eq(303) & c.PRCITSHP.isin([4, 5])),
                        ("Other Hispanic", a.HISP.gt(2), c.PRDTHSP.gt(1)),
                        ("Not Hispanic", a.HISP.eq(1), c.PEHSPNON.eq(2))]:
        ah = a[am & a.hh].groupby("band", observed=False).PWGTP.sum() / 1e6
        cc = c[cm].groupby("band", observed=False).w.sum() / 1e6
        for b in LABELS:
            rows.append(dict(group=lab, band=b, acs_household_m=ah[b], cps_m=cc[b],
                             ratio=cc[b] / ah[b]))
    t2 = pd.DataFrame(rows)
    t2.to_csv(HERE / "derived/cps_vs_acs_age.csv", index=False)
    print(t2.pivot(index="band", columns="group", values="ratio").round(3).to_string())


if __name__ == "__main__":
    main()
