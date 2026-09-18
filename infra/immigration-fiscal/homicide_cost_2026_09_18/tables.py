"""Memo-ready tables from the lane's derived CSVs, plus the SHR-to-WONDER coverage check."""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
OUT = HERE / "derived"
ETH = ["hispanic", "nh_white", "nh_black", "nh_other", "unknown"]
pd.set_option("display.width", 200)


def md(df, floatfmt="%.3f"):
    return df.to_string(float_format=lambda x: floatfmt % x)


def main() -> None:
    print("=" * 78)
    print("A1. Victim x offender ethnicity, SHR criminal homicide")
    for w in ["2019_2023", "2015_2023"]:
        m = pd.read_csv(OUT / f"shr_vic_off_matrix_{w}.csv")
        for uni in ["svso_cleared", "all_cleared"]:
            t = m[m.universe.eq(uni)].pivot(index="vic_eth", columns="off_eth", values="n")
            t = t.reindex(index=ETH, columns=ETH, fill_value=0)
            print(f"\n[{w} / {uni}] counts, rows = victim ethnicity, columns = offender")
            print(t.to_string())
            k = t.drop(index="unknown", columns="unknown")
            print(f"  ethnicity known on both sides: {int(k.to_numpy().sum()):,} of "
                  f"{int(t.to_numpy().sum()):,} ({k.to_numpy().sum()/t.to_numpy().sum():.3f})")
            print("  column shares (victim distribution of each offender group)")
            print(md((k / k.sum()).T))

    print("\n" + "=" * 78)
    print("A2. Ethnicity missingness and clearance, by year")
    print(md(pd.read_csv(OUT / "shr_missingness_by_year.csv", index_col=0)))

    print("\n" + "=" * 78)
    print("A3. Victim age distribution by victim ethnicity, 2019-2023 (all criminal victims)")
    v = pd.read_csv(OUT / "shr_vic_age_by_eth_2019_2023.csv", index_col=0)
    order = ["0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44",
             "45-49", "50-54", "55-59", "60-64", "65-69", "70-74", "75-79", "80-84", "85+",
             "unknown"]
    v = v.reindex(order).fillna(0)
    print(md(v / v.sum()))
    print("\nA4. Offender age distribution by offender ethnicity, 2019-2023 (cleared)")
    o = pd.read_csv(OUT / "shr_off_age_by_eth_2019_2023.csv", index_col=0).reindex(order).fillna(0)
    print(md(o / o.sum()))

    print("\n" + "=" * 78)
    print("A5. Relationship of victim to offender, by offender x victim ethnicity, 2019-2023")
    r = pd.read_csv(OUT / "shr_relationship_2019_2023.csv")
    r = r[r.off_eth.ne("unknown") & r.vic_eth.ne("unknown")]
    p = r.pivot_table(index=["off_eth", "vic_eth"], columns="rel", values="n",
                      aggfunc="sum", fill_value=0)
    print(md(p.div(p.sum(axis=1), axis=0)))
    print("\n  marginal by offender ethnicity")
    q = r.groupby(["off_eth", "rel"]).n.sum().unstack(fill_value=0)
    print(md(q.div(q.sum(axis=1), axis=0)))

    print("\nA6. Circumstance by offender ethnicity, 2019-2023")
    c = pd.read_csv(OUT / "shr_circumstance_2019_2023.csv")
    c = c[c.off_eth.ne("unknown")].pivot_table(index="off_eth", columns="circ", values="n",
                                               aggfunc="sum", fill_value=0)
    print(md(c.div(c.sum(axis=1), axis=0)))

    print("\nA7. Clearance by victim ethnicity")
    for w in ["2019_2023", "2015_2023"]:
        print(f"[{w}]")
        print(md(pd.read_csv(OUT / f"shr_clearance_by_vic_eth_{w}.csv", index_col=0)))

    print("\n" + "=" * 78)
    print("A8. SHR coverage against CDC WONDER, 2019-2023")
    wnd = pd.read_csv(OUT / "wonder_deaths_year_hispanic.csv")
    wnd = wnd[wnd.year.astype(str).str.strip().isin([str(y) for y in range(2019, 2024)])]
    tot_w = wnd.deaths.sum()
    shr_v = pd.read_csv(OUT / "shr_clearance_by_vic_eth_2019_2023.csv", index_col=0)
    tot_s = shr_v.victims.sum()
    print(f"  WONDER homicide deaths (GR113-127) 2019-2023           {tot_w:>10,.0f}")
    print(f"  SHR criminal-homicide victim records      {tot_s:>10,.0f}")
    print(f"  SHR coverage ratio                        {tot_s/tot_w:>10.3f}")
    wh = wnd[wnd.hispanic_origin.eq("Hispanic or Latino")].deaths.sum()
    wn = wnd[wnd.hispanic_origin.eq("Not Hispanic or Latino")].deaths.sum()
    print(f"  WONDER Hispanic {wh:,.0f}  non-Hispanic {wn:,.0f}  Hispanic share "
          f"{wh/(wh+wn):.4f}")
    shr_known = shr_v.drop(index="unknown")
    print(f"  SHR ethnicity-known victims Hispanic share "
          f"{shr_v.loc['hispanic','victims']/shr_known.victims.sum():.4f}")
    jb = pd.read_csv(OUT / "c1b_offender_composition.csv", index_col=0)
    print("\n  joint-imputed offender ethnicity composition (universe A, 2019-2023)")
    print(md(jb))

    print("\n" + "=" * 78)
    print("B1. Victim remaining lifetime fiscal balance, 2024 dollars per person")
    print(md(pd.read_csv(OUT / "victim_remaining_balance.csv"), "%.0f"))

    print("\nB2. Parent channel, CPS ASEC 2025, adults 18+ by group x sex x age band")
    c = pd.read_csv(OUT / "cps_parent_channel_by_age.csv")
    c = c[c.group.isin(["third_plus_nh_white", "mexican_observed_total", "all_hispanic"])
          & c.sex.ne("all")]
    print(md(c[["group", "sex", "band", "share_with_minor_child", "mean_kids",
                "mean_child_years", "mean_sole_child_years", "mean_years_to_16_max"]]))

    print("\nB3. Treasury cost per cleared homicide by offender ethnicity")
    res = pd.read_csv(OUT / "treasury_cost_per_homicide.csv")
    life = sorted(res.life_share.unique())[1]
    for acct in ["partial", "complete"]:
        for rate in [0.0, 0.03]:
            sub = res[(res.account.eq(acct)) & (res.rate.eq(rate))
                      & (res.life_share.eq(life)) & (res.foster_share.eq(0.0))]
            print(f"\n[{acct} account, rate {rate:.0%}, life share {life:.3f}]")
            print(md(sub[["off_eth", "mean_offender_age", "mean_victim_age",
                          "victim_balance", "child_cost", "offender_cost", "total"]], "%.0f"))
    print("\n[foster-care arm sensitivity, partial account, undiscounted]")
    f = res[(res.account.eq("partial")) & (res.rate.eq(0.0)) & (res.life_share.eq(life))]
    print(md(f.pivot_table(index="off_eth", columns="foster_share", values="total"), "%.0f"))

    print("\nB4. Against the social cost and the VSL")
    import json
    p = json.loads((OUT / "external_params.json").read_text())
    vsl = p["vsl_dot_2024"]["value"]
    sub = res[(res.account.eq("partial")) & (res.rate.eq(0.0)) & (res.life_share.eq(life))
              & (res.foster_share.eq(0.0))]
    t = sub[["off_eth", "total"]].copy()
    t["social_cost_mccollister"] = 13_087_784.0
    t["vsl_dot_2024"] = vsl
    t["treasury_share_of_social_cost"] = t.total / 13_087_784.0
    print(md(t, "%.0f"))


if __name__ == "__main__":
    main()
