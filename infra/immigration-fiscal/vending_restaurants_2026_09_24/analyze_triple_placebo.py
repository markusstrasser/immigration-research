"""Placebo states for the triple difference (design a2).

The triple difference asks whether California counties with a higher Hispanic share changed after 2018
relative to the same Hispanic-share gradient in other states. Here each other state with at least 20
counties in the sample takes California's place (California dropped), and the same regression gives
that state's d_2019 and mean(d_2022, d_2023). California's rank among them is the permutation p-value:
(1 + number of placebo states with |d| >= |d_CA|) / (1 + number of placebo states).

Writes derived/triple_placebo.csv and derived/triple_placebo_summary.csv. Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with pyfixest python3 infra/immigration-fiscal/vending_restaurants_2026_09_24/analyze_triple_placebo.py
"""
import warnings

import pandas as pd
import pyfixest as pf

from analyze_county import CBP_YEARS, REF, balanced, load
from lib import DERIVED

warnings.filterwarnings("ignore")
OUTS = [("722511", "estab"), ("722511", "emp"), ("722513", "estab"), ("722513", "emp"), ("722330", "estab"),
        ("445110", "emp")]


def triple(d: pd.DataFrame, weight: str | None) -> tuple[float, float]:
    d = d.copy()
    names = []
    for k in CBP_YEARS:
        if k == REF:
            continue
        d[f"g{k}"] = d["x"] * (d["year"] == k)
        d[f"t{k}"] = d["x"] * d["tr"] * (d["year"] == k)
        names += [f"g{k}", f"t{k}"]
    m = pf.feols("y ~ " + " + ".join(names) + " | fips + state^year", data=d, weights=weight, vcov="hetero")
    b = m.coef()
    return float(b["t2019"]), float((b["t2022"] + b["t2023"]) / 2)


def main() -> None:
    cbp, _, ex = load()
    ex = ex.set_index("fips")
    rows = []
    for code, var in OUTS:
        base = balanced(cbp, code, var, CBP_YEARS).join(ex[["pop", "hisp_share"]], on="fips").dropna()
        base["state"] = base["fips"].str[:2]
        base["x"] = base["hisp_share"] * 10
        counts = base.drop_duplicates("fips")["state"].value_counts()
        states = sorted(s for s in counts[counts >= 20].index if s != "06")
        for wname in ("none", "pop"):
            w = "pop" if wname == "pop" else None
            d = base.copy()
            d["tr"] = (d["state"] == "06").astype(int)
            ca19, ca2223 = triple(d, w)
            rows.append({"naics": code, "var": var, "weight": wname, "state": "06", "d2019": ca19, "d2022_23": ca2223})
            for st in states:
                d = base[base["state"] != "06"].copy()
                d["tr"] = (d["state"] == st).astype(int)
                p19, p2223 = triple(d, w)
                rows.append({"naics": code, "var": var, "weight": wname, "state": st, "d2019": p19, "d2022_23": p2223})
            print(f"  {code} {var} {wname}: CA d2019 {ca19:+.4f}, d2022-23 {ca2223:+.4f}; {len(states)} placebo states",
                  flush=True)
    r = pd.DataFrame(rows)
    r.to_csv(DERIVED / "triple_placebo.csv", index=False, lineterminator="\n", float_format="%.6g")
    summ = []
    for (code, var, wname), g in r.groupby(["naics", "var", "weight"]):
        ca = g[g["state"] == "06"].iloc[0]
        pl = g[g["state"] != "06"]
        out = {"naics": code, "var": var, "weight": wname, "placebo_states": len(pl)}
        for stat in ("d2019", "d2022_23"):
            out[f"ca_{stat}"] = ca[stat]
            out[f"placebo_p10_{stat}"] = pl[stat].quantile(0.10)
            out[f"placebo_p90_{stat}"] = pl[stat].quantile(0.90)
            out[f"perm_p_{stat}"] = (1 + (pl[stat].abs() >= abs(ca[stat])).sum()) / (1 + len(pl))
        summ.append(out)
    pd.DataFrame(summ).to_csv(DERIVED / "triple_placebo_summary.csv", index=False, lineterminator="\n",
                              float_format="%.6g")
    print(pd.DataFrame(summ).round(4).to_string())


if __name__ == "__main__":
    main()
