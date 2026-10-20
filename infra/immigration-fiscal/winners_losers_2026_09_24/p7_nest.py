"""Read-only literature-epsilon solves and Card split wage-bill sizing.

Reuse the authoritative nest and distribution adapters with isolated function
globals. No production source, grid, or case payload is modified.
"""
import types
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd


def scenario_solver(B, epsilons):
    scope = dict(B.row4_nest_rows.__globals__)
    scope["LANE_SCENARIOS"] = list(B.LANE_SCENARIOS) + [
        ("hs_or_less", 2.0, 1.0, epsilon) for epsilon in epsilons]
    return types.FunctionType(B.row4_nest_rows.__code__, scope,
                              B.row4_nest_rows.__name__, B.row4_nest_rows.__defaults__)


def low_skill_solve(nest, shares, tree, removed, sigma, labor_share, adjustment, elasticity=0.0):
    """Use the tree's finite epsilon only in cell 0; cell 1 is exactly linear.

    The existing equilibrium and Euler checks remain authoritative. A local
    function namespace changes only its two-branch aggregate, never the module.
    Above-HS wages can still change through complementarity across skill cells.
    """
    if len(tree.children) != 2 or tree.children != (0, 1):
        raise ValueError("Low-skill epsilon requires the two-branch nativity nest")

    def aggregate(node, quantities):
        total, gradients = nest.aggregate(node, quantities)
        total = total.copy()
        total[1] = (node.weights[:, 1] * quantities[:, 1]).sum(axis=0)
        for index in gradients:
            gradients[index] = np.broadcast_to(gradients[index], total.shape).copy()
            gradients[index][1] = node.weights[index, 1]
        return total, gradients

    scope = dict(nest.solve.__globals__, aggregate=aggregate)
    solve = types.FunctionType(nest.solve.__code__, scope, nest.solve.__name__, nest.solve.__defaults__)
    return solve(shares, tree, removed, sigma, labor_share, adjustment, elasticity)


def finite_row(B, d, template, row4_info, epsilon, require):
    """Rebuild the producer's row-4 calibration, then solve the scoped epsilon."""
    spec = importlib.util.spec_from_file_location("p8_epsilon_builder", B.NEST_DIR / "builder.py")
    builder = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(B.NEST_DIR))
    try:
        spec.loader.exec_module(builder)
    finally:
        sys.path.remove(str(B.NEST_DIR))
    weights = (d.pw_production if "pw_production" in d else d.pw).to_numpy(float).copy()
    outside = ~np.isin(d.st.to_numpy(), B.ROW4_EXCLUDED_STATES)
    for status, label in B.ROW4_STATUS.items():
        mask = d.PENATVTY.eq(B.MEXICO_BIRTHPLACE).to_numpy() & d.PRCITSHP.eq(status).to_numpy() & outside
        weights[mask] *= row4_info["factors"][label]
    native, target, civ = d.native.to_numpy(), d.target.to_numpy(), d.civ.to_numpy()
    branches = (civ & native & ~target, civ & native & target,
                civ & ~native & ~target, civ & ~native & target)
    cells = (d.A_HGA.between(31, 39).to_numpy(), d.A_HGA.between(40, 46).to_numpy())
    earn = np.maximum(d.PEARNVAL.to_numpy(float), 0)
    four = np.array([[(weights * earn * br * cell).sum() for cell in cells] for br in branches])[:, :, None]
    total = four.sum(axis=0)
    case = dict(shares=total / total.sum(axis=0), four_share=four / total[None, :, :])
    tree, removed, _, _ = builder.make_case(case, "A_by_nativity", epsilon)
    result = low_skill_solve(builder.nest, case["shares"], tree, removed, template.sigma,
                            template.labor_share, template.capital_adjustment)
    # A second branch ratio in the high cell would reveal an accidental finite
    # high-skill nest even when aggregate production totals still close.
    require(f"epsilon_{epsilon:g}_above_hs_perfect_substitutes",
            np.allclose(result["wage_without_over_with"][0, 1],
                        result["wage_without_over_with"][1, 1], rtol=0, atol=1e-12))
    tau = np.asarray(builder.TAU).reshape(2, 1)
    scale = total.sum(axis=0)[0] / .65 / 1e9
    private = ((1 - tau) * (result["labor_gain_by_branch"] - result["disutility_by_branch"])).sum(axis=1)
    row = template.copy()
    row["sigma_NI"] = epsilon
    for index, tag in enumerate(("native", "other_fb")):
        for cell in (0, 1):
            row[f"wage_pct_{tag}_cell{cell}"] = float(100 * (result["wage_without_over_with"][index, cell, 0] - 1))
    row["native_production_gain_bn"], row["other_immigrant_production_gain_bn"] = scale * private[:, 0]
    row["capital_gain_bn"] = float(scale * result["capital_gain"][0])
    row["capital_tax_gain_bn"] = row.capital_gain_bn * builder.CAPITAL_TAX
    row["capital_private_residual_bn"] = row.capital_gain_bn - row.capital_tax_gain_bn
    row["induced_current_receipts_bn"] = float(scale * (tau * result["labor_gain_by_branch"]).sum()) + row.capital_tax_gain_bn
    row["private_plus_receipts_bn"] = row.native_production_gain_bn + row.other_immigrant_production_gain_bn + row.capital_private_residual_bn + row.induced_current_receipts_bn
    return row


def recompute_lineage_row(row, bases, tau, private_delta, receipt_delta):
    """Solve descendant multipliers on this epsilon's wage bill, never its sibling.

    [ASSUMPTION] The case's first-order descendant P/F addition is held fixed
    beside the finite union solve. Only its allocation across branches/cells is
    recomputed; this is not a newly estimated descendant production effect.
    """
    tau = np.asarray(tau, float)
    labor = {(tag, cell): -row[f"wage_pct_{tag}_cell{cell}"] / 100 * bases[(tag, cell)]
             for tag in ("native", "other_fb") for cell in (0, 1)}
    wages = np.array([labor[("native", cell)] + labor[("other_fb", cell)] for cell in (0, 1)])
    private_before = row.native_production_gain_bn + row.other_immigrant_production_gain_bn + row.capital_private_residual_bn
    target = np.array([private_before + private_delta, row.induced_current_receipts_bn + receipt_delta])
    if row.capital_private_residual_bn == 0 and row.capital_tax_gain_bn == 0:
        kappa, lam = 1.0, np.linalg.solve(np.array([(1 - tau) * wages, tau * wages]), target)
    else:
        one, kappa = np.linalg.solve(np.array([[float((1 - tau) @ wages), row.capital_private_residual_bn],
                                               [float(tau @ wages), row.capital_tax_gain_bn]]), target)
        lam = np.array([one, one])
    new = row.copy()
    for tag in ("native", "other_fb"):
        for cell in (0, 1):
            new[f"wage_pct_{tag}_cell{cell}"] *= lam[cell]
    for tag, field in (("native", "native_production_gain_bn"), ("other_fb", "other_immigrant_production_gain_bn")):
        new[field] = sum((1 - tau[cell]) * lam[cell] * labor[(tag, cell)] for cell in (0, 1))
    for field in ("capital_gain_bn", "capital_tax_gain_bn", "capital_private_residual_bn"):
        new[field] *= kappa
    new["induced_current_receipts_bn"] = float(tau @ (lam * wages)) + new.capital_tax_gain_bn
    new["private_plus_receipts_bn"] = new.native_production_gain_bn + new.other_immigrant_production_gain_bn + new.capital_private_residual_bn + new.induced_current_receipts_bn
    return new, dict(sigma_NI=float(row.sigma_NI), lambda_cell0=float(lam[0]), lambda_cell1=float(lam[1]),
                     kappa=float(kappa), delta_P_bn=float(private_delta), delta_F_bn=float(receipt_delta),
                     max_abs_closure_bn=float(np.max(np.abs(np.array([
                         new.native_production_gain_bn + new.other_immigrant_production_gain_bn + new.capital_private_residual_bn,
                         new.induced_current_receipts_bn]) - target))))


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
    source_path = Path(__file__).resolve().parent / "inputs/p8_epsilon_sources.json"
    pin(source_path, wl)
    source_evidence = json.loads(source_path.read_text())
    # Parameters are the parent's requested sensitivity arms, with their exact
    # source populations recorded locally. Neither is estimated on this CPS.
    epsilons = (8.7, 17.9)
    prod = B.fiscal_totals(wl.CASE["case"])["adopted"]["production"]
    base = B.LATER_CASES[wl.CASE["case"]].grid_base
    for lane in (base, wl.CASE["lane"]):
        pin(wl.FISCAL / lane / "derived/corrections.json", wl)
    pin(wl.FISCAL / prod["grid"]["file"], wl)
    base_rows, info = B.row4_nest_rows(d, B.nest_rows(), prod, base)
    rows, lineage_info = B.lineage_rows(d, base_rows, base, wl.CASE["lane"])
    template = B.pick(base_rows, "hs_or_less", 2.0, 1.0, np.inf)
    numeric = [k for k in base_rows.columns if k.endswith("_bn") or k.startswith("wage_pct")]
    infinite_control = finite_row(B, d, template, info, np.inf, require)
    require("epsilon_calibration_infinite_reproduces_row4", all(
        abs(infinite_control[k] - template[k]) < 1e-9 for k in numeric))
    live = B.pick(rows, "hs_or_less", 2.0, 1.0, np.inf)
    private_delta = (live.native_production_gain_bn + live.other_immigrant_production_gain_bn + live.capital_private_residual_bn
                     - template.native_production_gain_bn - template.other_immigrant_production_gain_bn - template.capital_private_residual_bn)
    receipt_delta = live.induced_current_receipts_bn - template.induced_current_receipts_bn
    bases = {key: float(np.dot(d.pw.to_numpy(), values) / 1e9)
             for key, values in I["basis"]["hs_or_less"].items()}
    finite_lineage = []
    for epsilon in epsilons:
        row = finite_row(B, d, template, info, epsilon, require)
        row, metadata = recompute_lineage_row(row, bases, B.TAU, private_delta, receipt_delta)
        require(f"epsilon_{epsilon:g}_descendant_parts_close", metadata["max_abs_closure_bn"] < 1e-9)
        finite_lineage.append(metadata)
        rows = pd.concat([rows, pd.DataFrame([row])], ignore_index=True)
    lineage_info["finite_scenarios"] = finite_lineage
    lineage_info["finite_rule"] = "[ASSUMPTION] hold the case-minus-base descendant P/F addition fixed; solve its skill-cell multipliers anew on each finite low-skill epsilon wage bill; do not reuse infinite multipliers"
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
        epsilon_scope="[ASSUMPTION] finite literature epsilon in hs_or_less only; above_hs has exact infinite substitution. 8.7 transports Caiumi–Peri's no-HS-diploma estimate to hs_or_less; 17.9 transports Piyapromdee's low-skill, gender-specific metro estimate. Infinite remains central",
        source_evidence=source_evidence,
        receipt_incidence="delta induced labor receipts: national combined-tax key for a; equal persons for b; responding-programme receipts for c",
        card_status="builder has no Card split option; wage-bill reclassification only, no equilibrium/share-ahead estimate")
