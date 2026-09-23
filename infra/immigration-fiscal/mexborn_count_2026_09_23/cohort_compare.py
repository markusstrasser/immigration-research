"""CPS ASEC against ACS for the Mexico-born by arrival cohort and age.

If the CPS excess sits in recent arrivals, it points to ACS undercoverage of new (often
unauthorized) migrants, the premise of the residual estimators. If it sits in long-settled cohorts
and at all ages, it points to CPS weighting: the CPS rakes to national Hispanic totals by age and
sex, so any Hispanic control mass its sample misses elsewhere lands on the Hispanics it reaches.

Pairs each ASEC year t with ACS t-1 (the audit's pairing). CPS: IPUMS-CPS extract 1, YRIMMIG
interval codes mapped by the first year of the interval label. ACS: IPUMS USA extract 3, single-year
YRIMMIG, households plus noninstitutional group quarters. Writes derived/cohort_compare.csv.
"""
from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CPS = ROOT / "sources/immigration-fiscal/data/external/cps/cps_2ndgen.csv.gz"
DDI = ROOT / "sources/immigration-fiscal/data/external/cps/cps_2ndgen.xml"
ACS = ROOT / "sources/immigration-fiscal/derived/ipums_usa/usa_00003_census1980-2000+acs2005-2024_mexborn.parquet"
PAIRS = [(2013, 2012), (2016, 2015), (2020, 2019), (2023, 2022), (2024, 2023), (2025, 2024)]
BINS = [(0, 1989, "before 1990"), (1990, 1999, "1990-1999"), (2000, 2009, "2000-2009"),
        (2010, 2019, "2010-2019"), (2020, 2100, "2020 or later")]
AGES = [(0, 24, "0-24"), (25, 44, "25-44"), (45, 64, "45-64"), (65, 200, "65+")]


def cps_first_year() -> dict[int, int]:
    x = DDI.read_text(encoding="utf-8")
    block = re.search(r'<var[^>]*name="YRIMMIG".*?</var>', x, re.S).group(0)
    out = {}
    for code, label in re.findall(r"<catValu>(.*?)</catValu>\s*<labl>(.*?)</labl>", block, re.S):
        yr = re.search(r"\d{4}", label)
        if yr:
            out[int(code)] = int(yr.group(0))
    return out


def label(year: pd.Series, bins: list) -> pd.Series:
    out = pd.Series(pd.NA, index=year.index, dtype="object")
    for lo, hi, lab in bins:
        out[year.between(lo, hi)] = lab
    return out


def main() -> None:
    first = cps_first_year()
    c = pd.read_csv(CPS, usecols=["YEAR", "ASECFLAG", "HFLAG", "ASECWT", "BPL", "CITIZEN", "YRIMMIG", "AGE"])
    c = c[c.ASECFLAG.eq(1) & c.BPL.eq(20000) & c.CITIZEN.isin([4, 5])]
    c = c[~(c.YEAR.eq(2014) & c.HFLAG.eq(1))]
    c["cohort"] = label(c.YRIMMIG.map(first), BINS)
    c["ageband"] = label(c.AGE, AGES)
    a = pd.read_parquet(ACS, columns=["YEAR", "GQ", "PERWT", "BPL", "CITIZEN", "YRIMMIG", "AGE"])
    a = a[a.YEAR.ge(2005) & a.BPL.eq(200) & a.CITIZEN.isin([2, 3, 4, 5]) & a.GQ.isin([1, 2, 4, 5])]
    a["cohort"] = label(a.YRIMMIG, BINS)
    a["ageband"] = label(a.AGE, AGES)
    rows = []
    for cy, ay in PAIRS:
        cc, aa = c[c.YEAR.eq(cy)], a[a.YEAR.eq(ay)]
        for dim in ["cohort", "ageband"]:
            cs = cc.groupby(dim).ASECWT.sum() / 1e6
            as_ = aa.groupby(dim).PERWT.sum() / 1e6
            for k in cs.index.union(as_.index):
                rows.append(dict(asec=cy, acs=ay, dim=dim, level=k, cps_m=cs.get(k, 0.0), acs_m=as_.get(k, 0.0)))
        rows.append(dict(asec=cy, acs=ay, dim="total", level="all", cps_m=cc.ASECWT.sum() / 1e6,
                         acs_m=aa.PERWT.sum() / 1e6))
    t = pd.DataFrame(rows)
    t["cps_minus_acs_m"] = t.cps_m - t.acs_m
    t["ratio"] = t.cps_m / t.acs_m
    t = t.round(6)
    t.to_csv(HERE / "derived/cohort_compare.csv", index=False)
    with pd.option_context("display.width", 200):
        print(t.to_string(index=False))


if __name__ == "__main__":
    main()
