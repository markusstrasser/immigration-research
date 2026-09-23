"""Old (2010-based) against new (2020-based) CPS sample design, by rotation group.

BLS: "The introduction of the new CPS sample began in April 2025 and will be completed in July
2026 ... with one rotation group per month" (bls.gov/cps/methods/sample_redesign_2025.htm).
A household in month-in-sample (MIS) k during month t first entered at t-(k-1) for k <= 4 and at
t-k-7 for k >= 5 (4-8-4 rotation). It belongs to the new design if it first entered in April 2025
or later. ASEC 2025 (March 2025) is all old design; in July 2025 - March 2026 MIS 1-4 are new and
MIS 5-8 old; from July 2026 everything is new.

Rates are ratio estimates inside each group of rotation groups (weighted Mexico-born over weighted
population), so they do not depend on how the weighting splits the total across rotation groups.

Test: difference-in-differences of the MIS 1-4 minus MIS 5-8 rate, July 2025 - March 2026 (MIS 1-4
new, MIS 5-8 old) against January 2024 - March 2025 (both old). The pre-period months give the
null spread of the half-sample difference. Writes derived/rotation_by_month.csv and
derived/rotation_did.csv.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from monthly_series import BASIC, CA_TX, MONTHS, read_month

HERE = Path(__file__).resolve().parent
START_NEW = 2025 * 12 + 4  # April 2025 as a month index


def entry_index(t: int, mis: pd.Series) -> pd.Series:
    return np.where(mis.le(4), t - (mis - 1), t - mis - 7)


def group_rates(df: pd.DataFrame, mask: pd.Series) -> dict:
    d = df[mask]
    pop = d.w.sum()
    mex = d.PENATVTY.eq(303) & d.PRCITSHP.isin([4, 5])
    other = mex & ~d.GESTFIPS.isin(CA_TX)
    return dict(
        n=int(len(d)), n_mex=int(mex.sum()), pop_m=pop / 1e6,
        mex_rate=d.w[mex].sum() / pop, mex_other_rate=d.w[other].sum() / pop,
        mex_catx_rate=d.w[mex & d.GESTFIPS.isin(CA_TX)].sum() / pop,
        mex_noncit_rate=d.w[mex & d.PRCITSHP.eq(5)].sum() / pop,
        mex_share_hisp=d.w[mex].sum() / d.w[d.PEHSPNON.eq(1)].sum(),
        hisp_rate=d.w[d.PEHSPNON.eq(1)].sum() / pop,
    )


def main() -> None:
    rows = []
    files = sorted(BASIC.glob("*pub.zip"), key=lambda p: (int(p.name[3:5]), MONTHS.index(p.name[:3])))
    for path in files:
        df = read_month(path)
        df = df[df.w.gt(0)]
        year, month = int(df.HRYEAR4.iloc[0]), int(df.HRMONTH.iloc[0])
        t = year * 12 + month
        df["new"] = entry_index(t, df.HRMIS) >= START_NEW
        total_pop = df.w.sum()
        for lab, mask in [("all", df.w.gt(0)), ("mis1_4", df.HRMIS.le(4)), ("mis5_8", df.HRMIS.ge(5)),
                          ("new", df.new), ("old", ~df.new)]:
            if mask.sum() == 0:
                continue
            r = group_rates(df, mask)
            rows.append(dict(year=year, month=month, group=lab, **r,
                             mex_level_m=r["mex_rate"] * total_pop / 1e6,
                             mex_other_level_m=r["mex_other_rate"] * total_pop / 1e6))
        print(year, month, flush=True)
    t = pd.DataFrame(rows).round(6)
    t.to_csv(HERE / "derived/rotation_by_month.csv", index=False)

    wide = t.pivot_table(index=["year", "month"], columns="group",
                         values=["mex_rate", "mex_other_rate", "mex_catx_rate", "mex_noncit_rate", "mex_share_hisp"])
    ym = wide.index.get_level_values(0) * 12 + wide.index.get_level_values(1)
    pre = (ym >= 2024 * 12 + 1) & (ym <= 2025 * 12 + 3)
    split = (ym >= 2025 * 12 + 7) & (ym <= 2026 * 12 + 3)
    out = []
    for v in ["mex_rate", "mex_other_rate", "mex_catx_rate", "mex_noncit_rate", "mex_share_hisp"]:
        diff = wide[(v, "mis1_4")] - wide[(v, "mis5_8")]
        d_pre, d_split = diff[pre], diff[split]
        did = d_split.mean() - d_pre.mean()
        # null spread: SD of monthly half-sample differences in the all-old period, divided by the
        # square root of the months averaged (months overlap 75% in sample, so this is a floor)
        se = np.sqrt(d_pre.var(ddof=1) / len(d_pre) + d_split.var(ddof=1) / len(d_split))
        base = wide[(v, "all")][pre].mean()
        out.append(dict(variable=v, pre_months=int(pre.sum()), split_months=int(split.sum()),
                        diff_pre_mean=d_pre.mean(), diff_pre_sd=d_pre.std(ddof=1),
                        diff_split_mean=d_split.mean(), did=did, did_se_naive=se, did_z=did / se,
                        did_over_pre_level=did / base, pre_level=base))
    o = pd.DataFrame(out).round(6)
    o.to_csv(HERE / "derived/rotation_did.csv", index=False)
    with pd.option_context("display.width", 250, "display.max_columns", 30):
        print(o.to_string(index=False))


if __name__ == "__main__":
    main()
