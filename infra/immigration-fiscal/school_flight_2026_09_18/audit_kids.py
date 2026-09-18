"""Audit the kid cell files for duplicated-age responses.

The Census PUMS endpoint sometimes returns records outside the requested AGEP range, so a
recursive age split can return the same person several times. That inflates a state-year's
weighted total by an integer factor (California 2010 came back 13x, once per single year of
age). The check is within-state across years: a state's population aged 5-17 does not move
by more than a few percent a year, so a ratio to the state's cross-year median above 1.25
is a defect, not demography. Prints the bad state-years for re-fetching.
"""
import pathlib, sys
import pandas as pd

HERE = pathlib.Path(__file__).parent
CELLS = HERE / "_cache" / "kids"
rows = []
for f in sorted(CELLS.glob("kids_*.csv")):
    y, s = f.stem.split("_")[1:3]
    d = pd.read_csv(f)
    rows.append(dict(year=int(y), state=s,
                     total=float((d.pub + d.priv + d.noschool).sum()),
                     cells=len(d)))
t = pd.DataFrame(rows)
med = t.groupby("state").total.median().rename("med")
t = t.merge(med, on="state")
t["ratio"] = t.total / t.med
bad = t[(t.ratio > 1.25) | (t.ratio < 0.8)].sort_values("ratio", ascending=False)
print(f"{len(t)} state-years audited; {len(bad)} outside [0.80, 1.25] of the state median")
if len(bad):
    print(bad.to_string(index=False))
    print("\nREFETCH:", " ".join(f"{r.year}:{r.state}" for r in bad.itertuples()))
t.to_csv(HERE / "derived" / "kids_audit.csv", index=False)
sys.exit(1 if len(bad) else 0)
