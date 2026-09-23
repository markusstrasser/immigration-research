"""Native men 18-39: institutional share by Hispanic origin relative to native NH white alone,
by ACS year and pooled 2021-2024, raw and with the generic 'Other Hispanic' (HISP 24) excess
spread over named origins.

Excess = HISP-24 institutional residents above what HISP 24 would hold at the named-Hispanic
institutional rate; spread in proportion to each named origin's institutional count (the justice
lane's 'by institutional share' variant). Writes derived/acs_origin_inst_recode.csv.
Usage: acs_origin_inst_recode.py YEAR [YEAR ...]
"""
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
ORIGINS = {2: "Mexican", 3: "Puerto Rican", 5: "Dominican", 7: "Guatemalan", 8: "Honduran",
           11: "Salvadoran", 16: "Colombian", 24: "All other Hispanic"}


def cells(years):
    frames = []
    for y in years:
        d = pd.read_parquet(HERE / "_cache" / f"acs_person_{y}.parquet",
                            columns=["RELSHIPP", "AGEP", "SEX", "HISP", "RAC1P", "NATIVITY", "PWGTP"])
        d = d[d.NATIVITY.eq(1) & d.SEX.eq(1) & d.AGEP.between(18, 39)]
        d["inst"] = d.RELSHIPP.eq(37) * d.PWGTP
        d["grp"] = d.HISP.map(ORIGINS).fillna("other named Hispanic")
        d.loc[d.HISP.eq(1), "grp"] = "NH other race"
        d.loc[d.HISP.eq(1) & d.RAC1P.eq(1), "grp"] = "NH White"
        g = d.groupby("grp").agg(inst=("inst", "sum"), pop=("PWGTP", "sum")).reset_index()
        g["year"] = y
        frames.append(g)
    return pd.concat(frames)


def rates(g, label):
    g = g.set_index("grp")
    hisp = g.drop(index=["NH White", "NH other race"])
    named = hisp.drop(index="All other Hispanic")
    named_rate = named.inst.sum() / named["pop"].sum()
    excess = max(0.0, g.loc["All other Hispanic", "inst"] - named_rate * g.loc["All other Hispanic", "pop"])
    white = g.loc["NH White", "inst"] / g.loc["NH White", "pop"]
    out = []
    for o, r in hisp.iterrows():
        adj = r.inst if o == "All other Hispanic" else r.inst + excess * r.inst / named.inst.sum()
        if o == "All other Hispanic":
            adj = r.inst - excess
        out.append(dict(window=label, origin=o, inst=r.inst, pop=r["pop"], rate_pct=100 * r.inst / r["pop"],
                        ratio_to_white_raw=(r.inst / r["pop"]) / white,
                        ratio_to_white_hisp24_spread=(adj / r["pop"]) / white))
    out.append(dict(window=label, origin="NH White", inst=g.loc["NH White", "inst"], pop=g.loc["NH White", "pop"],
                    rate_pct=100 * white, ratio_to_white_raw=1.0, ratio_to_white_hisp24_spread=1.0))
    return out


if __name__ == "__main__":
    years = [int(y) for y in sys.argv[1:]]
    c = cells(years)
    rows = []
    for y in years:
        rows += rates(c[c.year.eq(y)].drop(columns="year"), str(y))
    pooled = [y for y in years if y >= 2021]
    rows += rates(c[c.year.isin(pooled)].groupby("grp")[["inst", "pop"]].sum().reset_index(),
                  f"pooled_{min(pooled)}_{max(pooled)}")
    r = pd.DataFrame(rows)
    r.to_csv(HERE / "derived" / "acs_origin_inst_recode.csv", index=False)
    pd.set_option("display.width", 200)
    print(r.pivot(index="origin", columns="window", values="ratio_to_white_raw").round(2).to_string())
    print(r.pivot(index="origin", columns="window", values="ratio_to_white_hisp24_spread").round(2).to_string())
