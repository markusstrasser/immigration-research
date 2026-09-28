"""CPS ASEC 2025 cross-section of the NLSY97 birth cohort, against the NLSY97 panel at the nearest ages.

Ages 41-44 at the March 2025 interview approximate the 1980-84 births; earnings are for 2024. Reads the
account's ASEC 2025 frame through its own loader (generation_account_2026_09_24/frame.py, read-only; the
loader checks the source zip hash when it rebuilds its cache) and uses its US-area and Mexico codes.
All-origin Hispanic generations parallel the NLSY97 definition: G2 = US-born (incl. territories) with at
least one parent born outside the US areas; G3+ = US-born with both parents born in the US areas. The
account's own Mexican-origin masks (G2: a Mexico-born parent; G3+: Mexican-origin Hispanic with US-area
parents) are reported beside them. Reference: US-born non-Hispanic white-alone with US-area parents.
Standard errors: 160 successive-difference replicate weights, var = 4/160 * sum (replicate - full)^2.
Writes derived/cps_check.csv with the matching NLSY97 rows from derived/gaps.csv.
"""
import csv
import sys
from pathlib import Path

import numpy as np
import pandas as pd

LANE = Path(__file__).resolve().parent
sys.path.insert(0, str(LANE.parent / "generation_account_2026_09_24"))
import frame as F  # noqa: E402

d = F.load()
_, _, mex = F.masks(d)
adult = d.PRPERTYP.eq(2).to_numpy() & d.A_AGE.between(41, 44).to_numpy()
native = d.PRCITSHP.isin([1, 2, 3]).to_numpy()
mom_us, dad_us = d.PEMNTVTY.isin(F.US_AREAS).to_numpy(), d.PEFNTVTY.isin(F.US_AREAS).to_numpy()
hisp, nhw = d.PEHSPNON.eq(1).to_numpy(), (d.PEHSPNON.eq(2) & d.PRDTRACE.eq(1)).to_numpy()
groups = {"G3+ NH white": native & mom_us & dad_us & nhw,
          "G2 Hispanic": native & ~(mom_us & dad_us) & hisp,
          "G3+ Hispanic": native & mom_us & dad_us & hisp,
          "G2 Mexican (account frame)": mex["G2"], "G3+ Mexican (account frame)": mex["G3plus"]}
W = d[[f"pwwgt{i}" for i in range(161)]].to_numpy(float)
earn = d.PEARNVAL.clip(lower=0).to_numpy(float)
rows = []
for sx, sname in {1: "men", 2: "women"}.items():
    base = adult & d.A_SEX.eq(sx).to_numpy()
    sums = {g: (W[base & m].sum(0), (W[base & m] * earn[base & m, None]).sum(0),
                (W[base & m] * (earn[base & m, None] > 0)).sum(0), int((base & m).sum())) for g, m in groups.items()}
    rw, re, rp, _ = sums["G3+ NH white"]
    for g, (w, e, p, n) in sums.items():
        tot = np.log(e / w) - np.log(re / rw)
        emp = np.log(p / w) - np.log(rp / rw)
        se = lambda v: float(np.sqrt(4 / 160 * ((v[1:] - v[0]) ** 2).sum()))
        rows.append(dict(source="CPS ASEC 2025, income year 2024, ages 41-44", sex=sname, group=g, n_persons=n,
                         mean_earnings=e[0] / w[0], share_positive_earnings=p[0] / w[0],
                         gap_total=tot[0], se_total=se(tot), gap_employment=emp[0], se_employment=se(emp)))
gaps = pd.read_csv(LANE / "derived/gaps.csv")
levels = pd.read_csv(LANE / "derived/levels.csv")
for win in ["income year 2020 (ages 36-40)", "income year 2022 (ages 38-42)"]:
    for sname in ("men", "women"):
        for g in ["G3+ NH white", "G2 Hispanic", "G3+ Hispanic"]:
            lv = levels[levels.window.eq(win) & levels.sex.eq(sname) & levels.group.eq(g)].iloc[0]
            gp = gaps[gaps.window.eq(win) & gaps.sex.eq(sname) & gaps.group.eq(g) & gaps.arm.eq("raw")]
            pick = lambda k, c: float(gp[gp.stat.eq(k)][c].iloc[0]) if len(gp) else 0.0
            rows.append(dict(source=f"NLSY97 {win}", sex=sname, group=g, n_persons=int(lv.n_persons),
                             mean_earnings=float(lv.mean_earnings), share_positive_earnings=float(lv.share_positive_earnings),
                             gap_total=pick("total", "estimate"), se_total=pick("total", "se"),
                             gap_employment=pick("employment", "estimate"), se_employment=pick("employment", "se")))
cols = list(rows[0])
with open(LANE / "derived/cps_check.csv", "w", newline="") as fh:
    w = csv.writer(fh, lineterminator="\n")
    w.writerow(cols)
    for r in rows:
        w.writerow([f"{r[c]:.6g}" if isinstance(r[c], float) else r[c] for c in cols])
print(pd.DataFrame(rows).round(3).to_string())
