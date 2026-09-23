#!/usr/bin/env python3
"""Check the census jackknife SEs against a stratified design-based SE.

analyze_census.py uses a delete-a-group jackknife over 80 random household groups (SERIAL mod 80).
In these IPUMS samples CLUSTER is the household (CLUSTER = YEAR * 1e9 + SERIAL * 10 + 1), so the
jackknife treats the household as the primary sampling unit but ignores STRATA. This script
computes the Taylor-linearized SE of the same crude rates (ratio estimator, with-replacement
sampling of clusters within strata) for Mexico-born men 18-40 by years-in-US bin, and the ratio of
the two SEs.

Run from the repository root (after analyze_census.py):
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/crime_selection_cohorts_2026_09_23/census_se_check.py
Out: derived/census_se_check.csv
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from analyze_census import classify, load  # noqa: E402

DERIVED = HERE / "derived"


def taylor_se(year_df: pd.DataFrame, domain: pd.Series) -> tuple[float, float]:
    """Domain rate = sum(w*y*d)/sum(w*d); linearized residual z = w*d*(y - rate)/sum(w*d), zero
    outside the domain, summed per cluster; variance = sum over strata of n_h/(n_h-1) * sum over
    the stratum's clusters of (z_hc - mean_h)^2, every cluster of the year counted."""
    w, y, d = year_df.PERWT.to_numpy(float), year_df["inst"].to_numpy(float), domain.to_numpy(float)
    wd = w * d
    rate = (wd * y).sum() / wd.sum()
    z = pd.DataFrame({"h": year_df.STRATA.to_numpy(), "c": year_df.CLUSTER.to_numpy(),
                      "z": wd * (y - rate) / wd.sum()})
    zc = z.groupby(["h", "c"]).z.sum().reset_index()
    g = zc.groupby("h").z
    n = g.transform("size")
    dev = (zc.z - g.transform("mean")) ** 2 * n / (n - 1).where(n > 1)
    return rate, float(np.sqrt(dev.fillna(0).sum()))


def main() -> None:
    df = pd.read_csv(HERE / "_cache" / "ipums" / "census.csv.gz", usecols=["YEAR", "SERIAL", "PERNUM", "STRATA", "CLUSTER"])
    base = classify(load())
    base = base.merge(df, on=["YEAR", "SERIAL", "PERNUM"])
    if not (base.CLUSTER == base.YEAR * 10**9 + base.SERIAL * 10 + 1).all():
        print("  ! CLUSTER is not the household in every record; the jackknife PSU assumption is off")
    jk = pd.read_csv(DERIVED / "census_cohort_rates.csv")
    jk = jk[(jk.group == "mexico_born") & (jk.outcome == "institutional")].set_index(["year", "ysm"])
    rows = []
    for year in (1980, 1990, 2000):
        yd = base[base.YEAR == year]
        for ysm in ("0-5", "6-10", "11-15", "all"):
            dom = (yd["pop"] == "mex") & ((yd.ysm == ysm) if ysm != "all" else True)
            rate, se = taylor_se(yd, dom)
            j = jk.loc[(year, ysm)]
            rows.append(dict(year=year, ysm=ysm, rate=rate, se_taylor_stratified=se, se_jackknife=j.rate_se,
                             jackknife_over_taylor=j.rate_se / se))
    out = pd.DataFrame(rows)
    out.to_csv(DERIVED / "census_se_check.csv", index=False, float_format="%.6g")
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
