import numpy as np, pandas as pd
from norms_lib import *
d = load()
print("rows 2000+:", len(d), "| years:", sorted(d.year.unique()))
print("weight coverage:", round(d.w.notna().mean(), 4))
d, lab = assign_groups(d)
print("\ngroup n (all rows):")
for g in GROUP_ORDER:
    print(f"  {g:26s} {lab[g].sum():6d}")

items = CON + TOL_SPK + TOL_COL + TOL_LIB + LAW + ECON + IDENT
rows = []
for it in items:
    v = pd.to_numeric(d[it], errors="coerce")
    valid = v.notna().to_numpy()
    yrs = sorted(d.loc[valid, "year"].unique())
    rows.append(dict(item=it, n_total=int(valid.sum()),
                     years=f"{min(yrs)}-{max(yrs)}" if yrs else "none",
                     n_years=len(yrs),
                     n_mexG1=int((valid & lab["Mex G1"]).sum()),
                     n_mexG2=int((valid & lab["Mex G2"]).sum()),
                     n_mexG3=int((valid & lab["Mex G3+"]).sum()),
                     n_hispG1=int((valid & lab["Hisp G1"]).sum()),
                     n_hispG2=int((valid & lab["Hisp G2"]).sum()),
                     n_hispG3=int((valid & lab["Hisp G3+"]).sum()),
                     n_whiteG3=int((valid & lab["NHWhite G3+"]).sum())))
r = pd.DataFrame(rows)
pd.set_option("display.width", 250)
print("\n", r.to_string(index=False))
r.to_csv("derived/item_coverage.csv", index=False)
