"""Post-hoc contrasts from analyze_cps_fiscal_2025.py replicate estimates: generation groups vs
third-plus non-Hispanic whites and vs all natives, with the published 160-replicate SDR variance
(4/160 x sum of squared replicate deviations), matching the generator's `summarize`.
Run: uv run --with pandas python3 fiscal_contrasts_by_generation.py <output_dir_of_generator>
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

out = Path(sys.argv[1])
reps = json.load(open(out / "replicate_estimates.json"))
acc = pd.read_csv(out / "accounts.csv")
METRICS = ["payroll", "federal_after_refundable", "state_after_credits", "modeled_tax_total",
           "selected_cash_total", "selected_noncash_total", "cash_tax_balance", "cash_noncash_tax_balance"]
GROUPS = ["all_native", "third_plus_nh_white", "all_third_plus", "all_second_gen",
          "mexican_second_gen", "mexican_third_plus_selfid", "mexico_born"]


def sdr(v):
    v = np.asarray(v, dtype=float)
    return float(v[0]), float(np.sqrt(4.0 / (len(v) - 1) * np.sum((v[1:] - v[0]) ** 2)))


for allocation, weighting in [("equal_all_members", "person"), ("equal_all_members", "resource_unit_head"),
                              ("equal_adults_18plus", "person")]:
    print(f"\n== allocation={allocation} weighting={weighting}; annual $ per adult 25-64 (SDR se) ==")
    hdr = f"{'metric':28s}" + "".join(f"{g[:22]:>24s}" for g in GROUPS)
    print(hdr)
    for m in METRICS:
        cells = []
        for g in GROUPS:
            key = f"{allocation}|{weighting}|{g}|{m}"
            if key in reps:
                e, se = sdr(reps[key]); cells.append(f"{e:>14,.0f} ({se:,.0f})")
            else:
                cells.append(f"{'n/a':>24s}")
        print(f"{m:28s}" + "".join(f"{c:>24s}" for c in cells))
    print("-- contrasts (group minus third_plus_nh_white; group minus all_native), cash_noncash_tax_balance and modeled_tax_total --")
    for g in ["mexican_second_gen", "mexican_third_plus_selfid", "all_second_gen", "all_third_plus", "mexico_born"]:
        for m in ["modeled_tax_total", "selected_cash_total", "selected_noncash_total", "cash_noncash_tax_balance"]:
            line = f"  {g:26s} {m:26s}"
            for ref in ["third_plus_nh_white", "all_native"]:
                a = f"{allocation}|{weighting}|{g}|{m}"; b = f"{allocation}|{weighting}|{ref}|{m}"
                if a in reps and b in reps:
                    e, se = sdr(np.array(reps[a]) - np.array(reps[b]))
                    line += f"   vs {ref[:12]}: {e:>9,.0f} ({se:,.0f})"
            print(line)
n = acc[(acc.allocation == "equal_all_members") & (acc.weighting == "person") & (acc.metric == "payroll")][["group", "n", "weighted_adults"]]
print("\n-- sample sizes (adults 25-64) --"); print(n.to_string(index=False))
own = acc[(acc.allocation == "own_person")].pivot(index="group", columns="metric", values="estimate")
print("\n-- own-person means: earnings, own payroll, Medicaid/means-tested coverage share, Medicare share --")
print(own.loc[[g for g in GROUPS if g in own.index]].to_string(float_format=lambda v: f"{v:,.3f}" if v < 2 else f"{v:,.0f}"))
