"""Mexico-born level, CPS ASEC against ACS, every year both are held (2005-2025).

- CPS ASEC: IPUMS-CPS extract 1 (`cps_2ndgen.csv.gz`), ASECFLAG 1, weight ASECWT, Mexico-born =
  BPL 20000 and CITIZEN 4/5 (the audit's PENATVTY 303, PRCITSHP 4/5). 2014 carries two ASEC
  files (HFLAG 0 = 5/8, 1 = 3/8), each weighted to the whole population; the 5/8 file is used.
- ACS: IPUMS USA extract 3 (Mexico-born universe, ACS 2005-2024), weight PERWT, foreign-born =
  CITIZEN 2-5 (CITIZEN 1 is born abroad of American parents, native as in the CPS). GQ 3 is
  institutional group quarters, GQ 4 other group quarters, 1/2/5 households. The CPS universe is
  the civilian noninstitutional population, so the like-for-like ACS figure is households plus
  noninstitutional group quarters.

ASEC year t is interviewed February-April of t (midpoint about March 15); ACS year t averages
January-December of t (midpoint July 1). `acs_at_asec_m` interpolates ACS t-1 and t to March 15 of
t (weight 8.5/12 on t). Writes derived/annual_series.csv.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CPS = ROOT / "sources/immigration-fiscal/data/external/cps/cps_2ndgen.csv.gz"
ACS = ROOT / "sources/immigration-fiscal/derived/ipums_usa/usa_00003_census1980-2000+acs2005-2024_mexborn.parquet"


def cps_series() -> pd.DataFrame:
    c = pd.read_csv(CPS, usecols=["YEAR", "ASECFLAG", "HFLAG", "ASECWT", "BPL", "CITIZEN", "HISPAN"])
    c = c[c.ASECFLAG.eq(1) & c.YEAR.ge(2005)]
    c = c[~(c.YEAR.eq(2014) & c.HFLAG.eq(1))]
    fb = c.CITIZEN.isin([4, 5])
    mex = fb & c.BPL.eq(20000)
    g = lambda m: c.ASECWT[m].groupby(c.YEAR[m]).sum() / 1e6  # noqa: E731
    return pd.DataFrame({
        "cps_population_m": g(pd.Series(True, index=c.index)),
        "cps_hispanic_m": g(c.HISPAN.between(100, 612)),
        "cps_foreign_born_m": g(fb),
        "cps_mexborn_m": g(mex),
        "cps_mexborn_natz_m": g(mex & c.CITIZEN.eq(4)),
        "cps_mexborn_noncit_m": g(mex & c.CITIZEN.eq(5)),
        "cps_mexborn_n": c[mex].groupby("YEAR").size(),
    })


def acs_series() -> pd.DataFrame:
    a = pd.read_parquet(ACS, columns=["YEAR", "GQ", "PERWT", "BPL", "CITIZEN"])
    a = a[a.YEAR.ge(2005) & a.BPL.eq(200) & a.CITIZEN.isin([2, 3, 4, 5])]
    g = lambda m: a.PERWT[m].groupby(a.YEAR[m]).sum() / 1e6  # noqa: E731
    return pd.DataFrame({
        "acs_mexborn_all_m": g(pd.Series(True, index=a.index)),
        "acs_mexborn_hh_m": g(a.GQ.isin([1, 2, 5])),
        "acs_mexborn_noninst_m": g(a.GQ.isin([1, 2, 4, 5])),
        "acs_mexborn_inst_m": g(a.GQ.eq(3)),
        "acs_mexborn_natz_noninst_m": g(a.GQ.isin([1, 2, 4, 5]) & a.CITIZEN.eq(2)),
        "acs_mexborn_noncit_noninst_m": g(a.GQ.isin([1, 2, 4, 5]) & a.CITIZEN.isin([3, 4, 5])),
    })


def main() -> None:
    c, a = cps_series(), acs_series()
    t = c.join(a, how="outer")
    t.index.name = "year"
    prev = t.acs_mexborn_noninst_m.shift(1)
    t["acs_at_asec_m"] = prev + (8.5 / 12) * (t.acs_mexborn_noninst_m - prev)
    t["cps_over_acs_same_year"] = t.cps_mexborn_m / t.acs_mexborn_noninst_m
    t["cps_over_acs_prior_year"] = t.cps_mexborn_m / prev
    t["cps_over_acs_at_asec"] = t.cps_mexborn_m / t.acs_at_asec_m
    prev_noncit = t.acs_mexborn_noncit_noninst_m.shift(1)
    t["cps_over_acs_noncit_prior_year"] = t.cps_mexborn_noncit_m / prev_noncit
    t["cps_over_acs_natz_prior_year"] = t.cps_mexborn_natz_m / t.acs_mexborn_natz_noninst_m.shift(1)
    t = t.round(6)
    t.to_csv(HERE / "derived/annual_series.csv")
    with pd.option_context("display.width", 250, "display.max_columns", 30):
        print(t.to_string())


if __name__ == "__main__":
    main()
