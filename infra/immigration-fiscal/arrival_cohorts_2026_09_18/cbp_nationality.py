"""Mexican-national share of CBP encounters, FY2022-FY2025 (and FY2021 if the fy21-fy24 file lands).

Source file: data/external/cbp/nationwide-encounters-fy22-fy25-aor.csv (CBP Nationwide Encounters,
https://www.cbp.gov/newsroom/stats/nationwide-encounters). Rows are counts of ENCOUNTERS, which are
events and not persons: under Title 42 a single person expelled and re-crossing is counted each
time, and those repeat crossings were concentrated among Mexican nationals, so the Mexican share of
encounters overstates the Mexican share of arriving persons, most severely in FY2021-FY2022.
"""
import os
import pandas as pd

SRC = "/Users/alien/research-data/immigration-fiscal/data/external/cbp/nationwide-encounters-fy22-fy25-aor.csv"
ALT = "/Users/alien/research-data/immigration-fiscal/data/external/cbp/nationwide-encounters-fy21-fy24-aor.csv"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "derived")

def load(p):
    d = pd.read_csv(p, on_bad_lines="skip", engine="python")
    d.columns = [c.strip() for c in d.columns]
    return d

frames = [load(SRC)]
if os.path.exists(ALT):
    a = load(ALT)
    a = a[a["Fiscal Year"] == 2021]
    if len(a):
        frames.append(a)
d = pd.concat(frames, ignore_index=True)
d["Encounter Count"] = pd.to_numeric(d["Encounter Count"], errors="coerce")
d = d.dropna(subset=["Encounter Count", "Fiscal Year"])
d["Fiscal Year"] = d["Fiscal Year"].astype(int)

rows = []
for scope, sub in [("nationwide", d),
                   ("southwest_land_border", d[d["Land Border Region"] == "Southwest Land Border"])]:
    for fy, g in sub.groupby("Fiscal Year"):
        tot = g["Encounter Count"].sum()
        mex = g.loc[g["Citizenship"].str.upper() == "MEXICO", "Encounter Count"].sum()
        t42 = g.loc[g["Title of Authority"] == "Title 42", "Encounter Count"].sum()
        mex42 = g.loc[(g["Citizenship"].str.upper() == "MEXICO") &
                      (g["Title of Authority"] == "Title 42"), "Encounter Count"].sum()
        rows.append({"scope": scope, "fiscal_year": fy, "total_encounters": int(tot),
                     "mexico_encounters": int(mex), "mexico_share": mex / tot,
                     "title42_encounters": int(t42), "title42_share": t42 / tot,
                     "mexico_title42": int(mex42),
                     "mexico_share_title8_only": (mex - mex42) / (tot - t42) if tot > t42 else float("nan")})
enc = pd.DataFrame(rows).sort_values(["scope", "fiscal_year"])
enc.to_csv(f"{OUT}/cbp_mexican_share_encounters.csv", index=False)
print(enc.to_string(index=False))

sw = d[d["Land Border Region"] == "Southwest Land Border"]
for fy in [2023, 2024]:
    g = sw[sw["Fiscal Year"] == fy]
    top = (g.groupby("Citizenship")["Encounter Count"].sum().sort_values(ascending=False).head(12))
    t = top.to_frame("encounters")
    t["share"] = t.encounters / g["Encounter Count"].sum()
    t.reset_index().assign(fiscal_year=fy).to_csv(
        f"{OUT}/cbp_top_nationalities_sw_fy{fy}.csv", index=False)
    print(f"\nFY{fy} Southwest land border, top nationalities:\n", t.to_string())
