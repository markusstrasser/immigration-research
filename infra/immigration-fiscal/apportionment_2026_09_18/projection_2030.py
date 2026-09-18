"""Rough 2030 apportionment arm from Census Vintage 2024 state estimates.

Three runs, all labelled ROUGH: (A) apportionment on the July 1, 2024 estimate as it stands;
(B) a straight-line 2020->2024 extrapolation to April 1, 2030; (C) the same 2030 projection with
the Mexican-origin population removed, holding each state's 2020 Mexican-origin population share
constant. No overseas-employee component is added (it is ~0.1% of the total and state-specific).
"""
from pathlib import Path
import pandas as pd

from hh import apportion, load_2020

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
DERIVED = HERE / "derived"

EXCLUDE = {"United States", "Northeast Region", "Midwest Region", "South Region", "West Region",
           "District of Columbia", "Puerto Rico"}


def vintage2024():
    d = pd.read_csv(CACHE / "NST-EST2024-ALLDATA.csv")
    d = d[(d.SUMLEV == 40) & (~d.NAME.isin(EXCLUDE))]
    return d[["NAME", "POPESTIMATE2020", "POPESTIMATE2024"]].rename(columns={"NAME": "state"}).reset_index(drop=True)


def seats_table(pops: dict, label: str) -> pd.DataFrame:
    s = apportion(pops)
    return pd.DataFrame([{"state": k, f"pop_{label}": pops[k], f"seats_{label}": s[k]} for k in pops])


if __name__ == "__main__":
    v = vintage2024()
    counts = pd.read_csv(DERIVED / "state_counts.csv", dtype={"state": str}).drop(columns=["state"]).rename(columns={"NAME": "state"})
    d20 = load_2020()
    base = d20.set_index("state")
    mex_share = (counts.set_index("state")["mex_origin_2020_dec"] / base["pop"]).rename("mex_share_2020")

    v = v.set_index("state")
    ann = (v["POPESTIMATE2024"] - v["POPESTIMATE2020"]) / 4.0
    v["pop_2030_lin"] = (v["POPESTIMATE2024"] + ann * 5.75).round().astype(int)  # Jul 2024 -> Apr 2030

    a = seats_table(dict(v["POPESTIMATE2024"]), "est2024").set_index("state")
    b = seats_table(dict(v["pop_2030_lin"]), "proj2030").set_index("state")
    cf = (v["pop_2030_lin"] * (1 - mex_share)).round().astype(int)
    c = seats_table(dict(cf), "proj2030_nomex").set_index("state")

    out = base[["pop", "seats"]].rename(columns={"pop": "pop_2020_app", "seats": "seats_2020_official"})
    out = out.join([a, b, c]).join(mex_share)
    out["delta_2030_vs_2020"] = out["seats_proj2030"] - out["seats_2020_official"]
    out["delta_nomex_vs_2030"] = out["seats_proj2030_nomex"] - out["seats_proj2030"]
    out = out.reset_index()
    out.to_csv(DERIVED / "projection_2030.csv", index=False)

    for col, lab in (("delta_2030_vs_2020", "2030 straight-line projection vs 2020 apportionment"),
                     ("delta_nomex_vs_2030", "2030 projection with Mexican-origin removed vs 2030 projection")):
        m = out[out[col] != 0]
        print(f"{lab}: {int(m[m[col] > 0][col].sum())} seats move")
        print("   gain:", "; ".join(f"{r.state} {int(r[out.columns.get_loc(col) + 1]):+d}"
                                    for r in m[m[col] > 0].itertuples()) or "-")
        print("   lose:", "; ".join(f"{r.state} {int(r[out.columns.get_loc(col) + 1]):+d}"
                                    for r in m[m[col] < 0].itertuples()) or "-")
    a2 = out[out["seats_est2024"] != out["seats_2020_official"]]
    print("If apportioned on the July 2024 estimate as it stands:",
          "; ".join(f"{r.state} {r.seats_est2024 - r.seats_2020_official:+d}" for r in a2.itertuples()) or "no change")
