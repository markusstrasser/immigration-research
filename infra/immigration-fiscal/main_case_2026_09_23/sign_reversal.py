"""Sign-reversal figures of the complete account under the adopted main case.

The September 20 account's "What can reverse the sign?" table holds defense and general
government fixed (public_goods_response 0) and pairs the ordinary service response with private
capital adjustment (0, 0.5, 1). This script reproduces those published rows from the executed
welfare scenarios, then applies the three adopted changes as linear shifts:

- general government responds at g (0.59 or 0.84) on its assigned 48.29bn, whatever the
  ordinary service response;
- the under-charged part of uncompensated care (U) moves onto Medicaid, a transfer that
  responds fully in every row;
- the justice key moves J onto public order and safety, a service line, so it scales with the
  ordinary service response s.

Adopted welfare(s) = published welfare(s) - g*GG - U - s*J. The service break-even solves
welfare(s) = 0: s* = (s0*S - g*GG - U) / (S + J), where s0 is the published root and S the
assigned service pool. The least adverse end pairs g=0.59 with U low; the most adverse end pairs
g=0.84 with U high. Run: uv run --no-project python3 sign_reversal.py
"""
import json
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
ACCOUNT = HERE.parent / "full_account_2026_09_20" / "derived"

failures = 0


def gate(label, ok, detail=""):
    global failures
    print(f"  {'✓' if ok else '✗'} {label}{' — ' + detail if detail else ''}")
    failures += not ok


w = pd.read_csv(ACCOUNT / "welfare_scenarios.csv")
pools = pd.read_csv(ACCOUNT / "response_pools.csv")
published = json.loads((ACCOUNT / "headline_summary.json").read_text())
inputs = json.loads((HERE / "derived" / "inputs.json").read_text())

GG = inputs["general_government_target_bn"]
G_LO, G_HI = inputs["general_government_response"]["low"], inputs["general_government_response"]["high"]
U_LO, U_HI = inputs["uncompensated_inside_bn"]["equal_low"], inputs["uncompensated_inside_bn"]["equal_high"]
J = inputs["justice_change_bn"]["central"]

base = w.query("excluded_capital_owner_share == 0 and public_goods_response == 0 and fiscal_weight == 1")
rows = []
print("\n[capacity path]")
for s, grp in base.groupby("service_response"):
    lo, hi = grp.welfare_bn.min(), grp.welfare_bn.max()
    want = published["core_capacity_path"][str(s)]
    gate(f"published row s={s}", abs(lo - want["min"]) < 1e-9 and abs(hi - want["max"]) < 1e-9,
         f"{lo:.2f} to {hi:.2f}")
    rows.append(dict(measure="capacity_path_welfare_bn", service_response=s,
                     published_low=lo, published_high=hi,
                     adopted_low=lo - G_HI * GG - U_HI - s * J, adopted_high=hi - G_LO * GG - U_LO - s * J))

print("\n[service break-even, preferred keys, capital fully adjusted]")
core = base.query("service_response == 1 and receipt_scenario == 'cbo_collective' "
                  "and spending_scenario == 'complete_preferred_F_per_capita'")
core = core.merge(pools[["receipt_scenario", "spending_scenario", "allocation", "services_bn"]],
                  on=["receipt_scenario", "spending_scenario", "allocation"], validate="many_to_one")
numerator = core.break_even_service_response_beta1 * core.services_bn
core = core.assign(least=(numerator - G_LO * GG - U_LO) / (core.services_bn + J),
                   most=(numerator - G_HI * GG - U_HI) / (core.services_bn + J))
for allocation, grp in core.groupby("allocation"):
    lo, hi = grp.break_even_service_response_beta1.min(), grp.break_even_service_response_beta1.max()
    want = published["preferred_service_roots"][allocation]
    gate(f"published root {allocation}", abs(lo - want["min"]) < 1e-9 and abs(hi - want["max"]) < 1e-9,
         f"{lo:.3f} to {hi:.3f}")
    rows.append(dict(measure=f"service_break_even_{allocation}", service_response=None,
                     published_low=lo, published_high=hi, adopted_low=grp.most.min(), adopted_high=grp.least.max()))

# Identity check on one row: the shifted welfare at the adopted root is zero.
r = core.iloc[0]
s_star = r.least
welfare_at_root = (r.break_even_service_response_beta1 - s_star) * r.services_bn - G_LO * GG - U_LO - s_star * J
gate("adopted welfare is zero at the adopted root", abs(welfare_at_root) < 1e-9, f"{welfare_at_root:.2e}")

out = pd.DataFrame(rows)
out.to_csv(HERE / "derived" / "sign_reversal.csv", index=False, float_format="%.4f")
print("\n" + out.to_string(index=False))
if failures:
    sys.exit(f"FAIL: {failures} gate(s)")
print("all gates passed")
