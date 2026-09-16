"""Combine the two residual lanes into one running balance without double counting.

The micro lane priced public higher-education appropriations to enrolled 18-24-year-olds; the
aggregate lane priced the same appropriations from SHEEO by state. Keep the aggregate lane's
version (state-specific) and drop the micro lane's `higher_ed_subsidy_nces` row.
Institutional care (ACS self-ID proxy) and the two per-capita conventions are reported as
separate lines, not folded into the headline.
"""
import csv, pathlib
HERE = pathlib.Path(__file__).resolve().parent
M = HERE.parent / "ledger_residual_micro_2026_09_16/residual_micro_by_generation.csv"
G = ["all_native", "all_second_gen", "mexican_second_gen", "mexican_third_plus_selfid", "mexico_born"]
micro = {(r["allocation"], r["group"], r["metric"]): float(r["difference_from_third_plus_nh_white"]) for r in csv.DictReader(open(M))}
agg = {(r["allocation"], r["group"], r["item"]): float(r["difference_from_third_plus_nh_white"] or 0) for r in csv.DictReader(open(HERE / "residual_agg_by_generation.csv"))}
# transfers/costs enter the balance with a negative sign; the micro CSV differences are already signed as balance effects
MICRO_ITEMS = ["edu_assistance_government", "aptc_measured", "uncompensated_care", "other_public_transfers"]
AGG_ITEMS = ["ccdf", "head_start", "higher_ed", "lifeline"]
out = []
for alloc in ["equal_all_members", "equal_adults_18plus"]:
    print(f"\n[{alloc}] difference from 3rd+ NH white, $ per adult 25-64")
    print(f"{'line':44}" + "".join(f"{g[:14]:>16}" for g in G))
    def row(label, vals):
        print(f"{label:44}" + "".join(f"{v:16,.0f}" for v in vals)); out.append((alloc, label, *vals))
    base = [micro[(alloc, g, "extended_balance")] for g in G]
    row("extended balance (§12)", base)
    run = base[:]
    # the micro lane's running balance is stored as after_<item> rows in this order; recover each item's
    # effect as the step from the previous row, then drop the higher-education step (kept from the agg lane)
    order = ["edu_assistance_government", "higher_ed_subsidy_nces", "aptc_measured", "uncompensated_care", "other_public_transfers"]
    prev = base[:]
    for it in order:
        cur = [micro[(alloc, g, "after_" + it)] for g in G]
        d = [c - q for c, q in zip(cur, prev)]; prev = cur
        if it == "higher_ed_subsidy_nces":
            continue
        row("  - " + it, d); run = [a + b for a, b in zip(run, d)]
    for it in AGG_ITEMS:
        d = [-agg[(alloc, g, it)] for g in G]
        row("  - " + it, d); run = [a + b for a, b in zip(run, d)]
    row("= combined residual balance", run)
    inst = [-micro[(alloc, g, "institutional_care_base")] for g in G]  # cost difference -> balance effect
    row("  institutional care, ACS self-ID proxy (base)", inst)
    row("= with institutional care", [a + b for a, b in zip(run, inst)])
    gs = [-agg[(alloc, g, "general_services")] for g in G]
    fp = [-agg[(alloc, g, "federal_public_goods")] for g in G]
    row("  local general services, per-capita convention", gs)
    row("  federal public goods, per-capita convention", fp)
    row("= with both per-capita conventions", [a + b + c + d for a, b, c, d in zip(run, inst, gs, fp)])
with open(HERE / "combined_residual_balance.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["allocation", "line", *G]); w.writerows(out)
