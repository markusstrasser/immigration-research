"""Does income push US-born white postgraduates rightward at all?

The matched-cell test in matched_white.py leaves one question open: the income leg is weak
because GSS top-codes family income at $158,425. This checks the DIRECTION of the income
gradient inside the white postgraduate group. If more income does not move whites rightward,
then no achievable income match would close the residual Indian American gap, and the
top-coding limitation is not load-bearing for the conclusion.

Run: uv run --no-project --with pandas --with pyreadstat python3 income_gradient.py
"""
import pathlib
import pandas as pd
import pyreadstat

DTA = ("/Users/alien/Projects/immigration-research/infra/immigration-fiscal/"
       "attitudes_gen_2026_09_16/raw/GSS_stata/gss7224_r3a.dta")
OUT = pathlib.Path(__file__).parent / "derived"

df, _ = pyreadstat.read_dta(
    DTA,
    usecols=["year", "race", "hispanic", "degree", "coninc", "srcbelt", "pres20",
             "partyid", "born", "wtssps", "wtssnrps"],
    encoding="latin1",
)
d = df[df["year"] >= 2021].copy()
d["wt"] = d["wtssps"].fillna(d["wtssnrps"])
d = d[d["wt"].notna()]
base = (d["race"] == 1) & (d["hispanic"] == 1) & (d["born"] == 1)

rows = []
for label, edu in [("BA or higher", d["degree"] >= 3), ("postgraduate", d["degree"] == 4)]:
    g = d[base & edu & d["pres20"].isin([1, 2]) & d["coninc"].notna()].copy()
    g["q"] = pd.qcut(g["coninc"], 4, labels=["Q1 lowest", "Q2", "Q3", "Q4 highest"])
    for q, s in g.groupby("q", observed=True):
        w = s["wt"]
        rows.append({
            "education": label,
            "income_quartile": str(q),
            "n": len(s),
            "median_coninc": round(s["coninc"].median()),
            "biden_two_party_pct": round(100 * (w * (s["pres20"] == 1)).sum() / w.sum(), 1),
        })

res = pd.DataFrame(rows)
print(res.to_string(index=False))
res.to_csv(OUT / "income_gradient_white.csv", index=False)
print("\nwrote", OUT / "income_gradient_white.csv")
