"""Panel sanity checks and treatment-variation descriptives.

Prints, for the memo:
  1. national aggregates by year, checked against published Census figures
  2. the largest metros' Mexico-born share, checked for plausibility
  3. the cross-metro spread of the treatment change in each estimation window
"""
import pathlib
import pandas as pd

HERE = pathlib.Path(__file__).parent
D = HERE / "derived"
WINDOWS = [(2005, 2010), (2008, 2013), (2010, 2015), (2013, 2018), (2018, 2023),
           (2005, 2015), (2008, 2018), (2013, 2023)]


def main():
    p = pd.read_csv(D / "metro_year_panel.csv", dtype={"cbsa": str})
    t = (p.groupby(["cbsa", "cbsa_title", "year"], as_index=False)
           .agg(t_pop1864=("t_pop1864", "first"), t_mex1864=("t_mex1864", "first"),
                t_fb1864=("t_fb1864", "first"),
                pop1829=("pop1829", "sum"), emp1829=("emp1829", "sum"),
                pop1624=("pop1624", "sum"), emp1624=("emp1624", "sum")))
    t["mex_share"] = 100 * t.t_mex1864 / t.t_pop1864
    t["fb_share"] = 100 * t.t_fb1864 / t.t_pop1864
    t["epop1829"] = 100 * t.emp1829 / t.pop1829

    print("== metro-aggregate totals by year (millions, metros only) ==")
    g = t.groupby("year").agg(metros=("cbsa", "nunique"),
                              pop1864=("t_pop1864", "sum"),
                              mex=("t_mex1864", "sum"), fb=("t_fb1864", "sum"))
    g["mex_share_%"] = (100 * g.mex / g.pop1864).round(2)
    g["fb_share_%"] = (100 * g.fb / g.pop1864).round(2)
    for c in ("pop1864", "mex", "fb"):
        g[c] = (g[c] / 1e6).round(2)
    print(g.to_string())

    print("\n== ten largest metros, Mexico-born share of 18-64 ==")
    big = t[t.year == t.year.max()].nlargest(10, "t_pop1864")["cbsa"].tolist()
    piv = (t[t.cbsa.isin(big)]
           .pivot_table(index="cbsa_title", columns="year", values="mex_share"))
    keep = [y for y in (2005, 2010, 2015, 2019, 2023) if y in piv.columns]
    print(piv[keep].round(2).to_string())

    print("\n== cross-metro spread of the treatment change, by window ==")
    rows = []
    for (a, b) in WINDOWS:
        if a not in set(t.year) or b not in set(t.year):
            continue
        m = (t[t.year == a].merge(t[t.year == b], on="cbsa", suffixes=("_0", "_1")))
        m = m[m.pop1829_0 >= 50_000]
        if len(m) < 10:
            continue
        d = m.mex_share_1 - m.mex_share_0
        f = m.fb_share_1 - m.fb_share_0
        dy = m.epop1829_1 - m.epop1829_0
        rows.append(dict(window=f"{a}-{b}", n_metro=len(m),
                         mex_mean=d.mean(), mex_sd=d.std(), mex_p10=d.quantile(.1),
                         mex_p90=d.quantile(.9),
                         fb_mean=f.mean(), fb_sd=f.std(),
                         epop_mean=dy.mean(), epop_sd=dy.std()))
    print(pd.DataFrame(rows).round(3).to_string(index=False))


if __name__ == "__main__":
    main()
