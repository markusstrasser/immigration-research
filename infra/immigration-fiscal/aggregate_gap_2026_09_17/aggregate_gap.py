"""All-ages aggregate of the annual partial ledger with public health, by origin-generation.
Reuses cps_generation_welfare_2026_09_16/lifecycle_ledger_by_generation.py's construction: per-band person-weighted
balance_after_health (taxes - cash - noncash - MEPS public medical), gap to 3rd+ NH white and to all natives,
times the band's weighted population. Prints per-group totals in $bn/yr. Run from cps_generation_welfare_2026_09_16/ (its sys.path imports):
uv run --with numpy --with pandas python3 ../aggregate_gap_2026_09_17/aggregate_gap.py <asecpub25csv.zip> <h256dat.zip> <h256su.txt>"""
import sys
from pathlib import Path
import numpy as np, pandas as pd
HERE = Path("/Users/alien/Projects/immigration-research/infra/immigration-fiscal")
sys.path.insert(0, str(HERE / "build")); sys.path.insert(0, str(HERE / "cps_generation_welfare_2026_09_16"))
from analyze_cps_fiscal_2025 import CASH, NONCASH, TAX, allocate, prepare
from meps_health_transport_2024 import donor_model, read_meps
from lifecycle_ledger_by_generation import BANDS, US_AREA, band_of
cps, mz, ms = map(Path, sys.argv[1:4])
d, heads, index, _ = prepare(cps)
n_units = len(heads); units = d.groupby("SPM_ID", sort=True)
totals = {k: units[v].sum().to_numpy(dtype=float) for k, v in (TAX | CASH).items()}
totals.update({k: heads[v].to_numpy(dtype=float) for k, v in NONCASH.items()})
eligible = np.ones(len(d), dtype=bool)
per = {k: allocate(v, index, eligible, n_units) for k, v in totals.items()}
tax = per["payroll"] + per["federal_after_refundable"] + per["state_after_credits"]
cash = sum(per[k] for k in CASH); noncash = sum(per[k] for k in NONCASH)
medical, _ = read_meps(mz, ms)
alive = ~(d.PUB.eq(0) & d.PRIV.eq(0)).to_numpy()
cells, codes, _ = donor_model(medical, d, False)
health = cells.mean_public_paid.to_numpy()[codes] * alive
bal_nohealth = tax - cash - noncash
bal = bal_nohealth - health
native = d.PRCITSHP.isin([1, 2, 3]); parents_us = d.PEFNTVTY.isin(US_AREA) & d.PEMNTVTY.isin(US_AREA)
parent_mex = d.PEFNTVTY.eq(303) | d.PEMNTVTY.eq(303)
groups = {"third_plus_nh_white": native & parents_us & d.PEHSPNON.eq(2) & d.PRDTRACE.eq(1), "all_native": native,
          "mexican_second_gen": native & parent_mex, "mexican_third_plus_selfid": native & parents_us & d.PRDTHSP.eq(1),
          "mexico_born": d.PRCITSHP.isin([4, 5]) & d.PENATVTY.eq(303)}
w = d.MARSUPWT.to_numpy(dtype=float) / 100.0  # MARSUPWT carries two implied decimals
band = d.A_AGE.map(band_of).to_numpy()
civ = d.PRPERTYP.eq(2).to_numpy() | d.A_AGE.lt(15).to_numpy()
def prof(mask, v):
    out = []
    for i in range(len(BANDS)):
        sel = mask & (band == i); ws = w[sel].sum(); out.append(((v[sel] * w[sel]).sum() / ws, ws))
    return out
P = {g: prof(m.to_numpy() & civ, bal) for g, m in groups.items()}
PN = {g: prof(m.to_numpy() & civ, bal_nohealth) for g, m in groups.items()}
print(f"{'group':28s}{'pop_all_ages_M':>15s}{'gap_vs_white_$bn':>18s}{'gap_vs_allnative_$bn':>22s}{'gap_vs_white_nohealth_$bn':>26s}{'pop_25_64_M':>12s}{'gap25_64_white_$bn':>20s}")
for g in ["mexico_born", "mexican_second_gen", "mexican_third_plus_selfid"]:
    pop = sum(n for _, n in P[g]); gw = sum((P[g][i][0] - P["third_plus_nh_white"][i][0]) * P[g][i][1] for i in range(len(BANDS)))
    ga = sum((P[g][i][0] - P["all_native"][i][0]) * P[g][i][1] for i in range(len(BANDS)))
    gnh = sum((PN[g][i][0] - PN["third_plus_nh_white"][i][0]) * PN[g][i][1] for i in range(len(BANDS)))
    pop2564 = sum(P[g][i][1] for i in (2, 3, 4, 5)); g2564 = sum((P[g][i][0] - P["third_plus_nh_white"][i][0]) * P[g][i][1] for i in (2, 3, 4, 5))
    print(f"{g:28s}{pop/1e6:15.2f}{gw/1e9:18.1f}{ga/1e9:22.1f}{gnh/1e9:26.1f}{pop2564/1e6:12.2f}{g2564/1e9:20.1f}")
print("\nper-band gap vs white after health ($/person/yr) and band population (M):")
for g in ["mexico_born", "mexican_second_gen", "mexican_third_plus_selfid"]:
    print(g, [(f"{BANDS[i][0]}-{BANDS[i][1]}", round(P[g][i][0] - P['third_plus_nh_white'][i][0]), round(P[g][i][1]/1e6, 2)) for i in range(len(BANDS))])
