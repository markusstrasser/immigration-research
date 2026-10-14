"""Read-only literature-epsilon solves and Card split wage-bill sizing.

Reuse the authoritative nest and distribution adapters with isolated function
globals. No production source, grid, or case payload is modified.
"""
import types

import numpy as np
import pandas as pd


def scenario_solver(B, epsilons):
    scope = dict(B.row4_nest_rows.__globals__)
    scope["LANE_SCENARIOS"] = list(B.LANE_SCENARIOS) + [
        ("hs_or_less", 2.0, 1.0, epsilon) for epsilon in epsilons]
    return types.FunctionType(B.row4_nest_rows.__code__, scope,
                              B.row4_nest_rows.__name__, B.row4_nest_rows.__defaults__)


def transport_wage_delta(d, delta, old_weights, new_weights, require):
    """Keep each state/nativity/skill/signed epsilon change when payers thin."""
    other = d.other.to_numpy()
    groups = pd.MultiIndex.from_arrays([d.st, d.native, d.A_HGA.le(39), delta > 0])
    codes, _ = pd.factorize(groups)
    old = np.bincount(codes, weights=np.where(other, old_weights * delta, 0))
    new = np.bincount(codes, weights=np.where(other, new_weights * delta, 0))
    require("epsilon_delta_cells_have_recipient_mass", bool(np.all((old == 0) | (new != 0))))
    factors = np.divide(old, new, out=np.zeros_like(old), where=new != 0)
    out = np.where(other, delta * factors[codes], 0)
    delivered = np.bincount(codes, weights=new_weights * out)
    require("epsilon_delta_state_nativity_skill_sign_conserved",
            float(np.max(np.abs(delivered - old))) / 1e9 < 1e-9)
    return out


def card_bills(d, weights, group_weights, population, require):
    """Move half the some-college wage bill; not a Card efficiency-hours solve."""
    earn = np.maximum(d.PEARNVAL.to_numpy(float), 0)
    education = d.A_HGA.to_numpy()
    low = (education >= 31) & (education <= 39)
    some = (education >= 40) & (education <= 42)
    high = (education >= 40) & (education <= 46)
    rows = []
    masks = {"native_nonmember": d.other.to_numpy() & d.native.to_numpy(),
             "earlier_immigrant_nonmember": d.other.to_numpy() & ~d.native.to_numpy(),
             "group_us_born": d.target.to_numpy() & d.native.to_numpy(),
             "group_mexico_born": d.target.to_numpy() & ~d.native.to_numpy()}
    for branch, mask in masks.items():
        w = group_weights if branch.startswith("group_") else weights
        bills = [float(np.dot(w, earn * mask * cell) / 1e9) for cell in (low, some, high)]
        lo, sc, hi = bills
        transfer = sc / 2
        require(f"card_bill_conservation_{population}_{branch}",
                abs((lo + transfer) + (hi - transfer) - (lo + hi)) < 1e-9)
        rows.append(dict(population=population, branch=branch, hs_or_less_bn=lo,
                         some_college_bn=sc, above_hs_bn=hi, transfer_bn=transfer,
                         card_low_bn=lo + transfer, card_high_bn=hi - transfer,
                         low_bill_change_pct=100 * transfer / lo,
                         high_bill_change_pct=-100 * transfer / hi))
    national_low = sum(r["hs_or_less_bn"] for r in rows)
    national_high = sum(r["above_hs_bn"] for r in rows)
    card_low = sum(r["card_low_bn"] for r in rows)
    card_high = sum(r["card_high_bn"] for r in rows)
    for row in rows:
        row.update(low_skill_share_before=row["hs_or_less_bn"] / (row["hs_or_less_bn"] + row["above_hs_bn"]),
                   low_skill_share_card=row["card_low_bn"] / (row["card_low_bn"] + row["card_high_bn"]),
                   low_cell_branch_share_before=row["hs_or_less_bn"] / national_low,
                   low_cell_branch_share_card=row["card_low_bn"] / card_low,
                   high_cell_branch_share_before=row["above_hs_bn"] / national_high,
                   high_cell_branch_share_card=row["card_high_bn"] / card_high,
                   group_low_removal_share_before=sum(r["hs_or_less_bn"] for r in rows if r["branch"].startswith("group_")) / national_low,
                   group_low_removal_share_card=sum(r["card_low_bn"] for r in rows if r["branch"].startswith("group_")) / card_low,
                   group_high_removal_share_before=sum(r["above_hs_bn"] for r in rows if r["branch"].startswith("group_")) / national_high,
                   group_high_removal_share_card=sum(r["card_high_bn"] for r in rows if r["branch"].startswith("group_")) / card_high)
    return rows


def build(wl, B, d, I, pin, require, check_total):
    nest_dir = wl.FISCAL / "production_nativity_nest_2026_09_22"
    for path in (nest_dir / "builder.py", nest_dir / "nest_model.py",
                 nest_dir / "derived/nest_scenarios.csv",
                 nest_dir / "derived/branch_composition.csv", nest_dir / "derived/audit.json",
                 wl.FISCAL / "distribution_weights_2026_09_23/distribute.py",
                 wl.FISCAL / "matched_benefits_2026_09_19/model.py"):
        pin(path, wl)
    # Parameters are the parent's requested arms, already present in the
    # production builder's published grid. No estimate is made on this CPS.
    epsilons = (8.7, 17.9)
    prod = B.fiscal_totals(wl.CASE["case"])["adopted"]["production"]
    base = B.LATER_CASES[wl.CASE["case"]].grid_base
    for lane in (base, wl.CASE["lane"]):
        pin(wl.FISCAL / lane / "derived/corrections.json", wl)
    pin(wl.FISCAL / prod["grid"]["file"], wl)
    rows, info = scenario_solver(B, epsilons)(d, B.nest_rows(), prod, base)
    rows, lineage_info = B.lineage_rows(d, rows, base, wl.CASE["lane"])
    factor = info["gdp_factor"]["row4"]
    basis = I["basis"]["hs_or_less"]
    w = d.pw.to_numpy()
    native = d.native.to_numpy()
    scenarios, detail = {}, []
    for epsilon in (np.inf, *epsilons):
        row = B.pick(rows, "hs_or_less", 2.0, 1.0, epsilon)
        name = "infinite" if np.isinf(epsilon) else f"eps{epsilon:g}"
        cash = B.wage_delta(basis, row, True)
        check_total(f"nest_private_{name}", cash, w,
                    row.native_production_gain_bn + row.other_immigrant_production_gain_bn)
        for is_native, field in ((True, "native_production_gain_bn"),
                                 (False, "other_immigrant_production_gain_bn")):
            check_total(f"nest_branch_{name}_{is_native}",
                        np.where(native == is_native, cash, 0), w, row[field])
        receipts = B.wage_receipts_bn(basis, row, w)
        require(f"nest_receipts_{name}", abs(receipts - row.induced_current_receipts_bn) < 1e-9)
        scales = {end: 1.0 if prod["ends"][end]["normalization"] == "cash" else factor
                  for end in ("low", "high")}
        wages = {end: cash * scale for end, scale in scales.items()}
        wages["central"] = (wages["low"] + wages["high"]) / 2
        delta_f = {end: row.induced_current_receipts_bn * scale -
                   I["account"].induced_current_receipts_bn * scale for end, scale in scales.items()}
        delta_f["central"] = (delta_f["low"] + delta_f["high"]) / 2
        if np.isinf(epsilon):
            require("nest_infinite_reproduces_live_row", all(
                abs(row[k] - I["account"][k]) < 1e-9 for k in rows.columns
                if k.endswith("_bn") or k.startswith("wage_pct")))
        else:
            live_cash = B.wage_delta(basis, I["account"], True)
            delta_wages = {end: (cash - live_cash) * scale for end,scale in scales.items()}
            delta_wages["central"] = (delta_wages["low"] + delta_wages["high"]) / 2
            scenarios[name] = dict(wages=wages, delta_wages=delta_wages, delta_f=delta_f)
        for level in wl.LEVELS:
            scale = (scales["low"] + scales["high"]) / 2 if level == "central" else scales[level]
            for tag, field in (("native", "native_production_gain_bn"),
                               ("earlier_immigrant", "other_immigrant_production_gain_bn")):
                detail.append(dict(epsilon="inf" if np.isinf(epsilon) else epsilon, level=level,
                    branch=tag, after_tax_wage_bn=row[field] * scale,
                    delta_vs_infinite_bn=(row[field] - I["account"][field]) * scale,
                    induced_receipts_bn=row.induced_current_receipts_bn * scale,
                    delta_receipts_bn=delta_f[level]))
    return scenarios, pd.DataFrame(detail), dict(row4=info, lineage=lineage_info,
        epsilon_scope="[ASSUMPTION] one common epsilon in both skill cells, as the existing nest; low-skill literature values transported",
        receipt_incidence="delta induced labor receipts: national combined-tax key for a; equal persons for b; responding-programme receipts for c",
        card_status="builder has no Card split option; wage-bill reclassification only, no equilibrium/share-ahead estimate")
