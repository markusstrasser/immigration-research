"""Step 3: the account's production term (engine terms P and F) attributed to the three generations.

The term comes from matched_benefits_2026_09_19: a two-skill CES economy with and without the union's
labor, where the union's efficiency units in skill cell s are its positive earnings (PEARNVAL or
WSAL_VAL) in that cell and f_s is its fraction of the cell. P (other residents' private after-tax
gain) and F (induced current receipts) are smooth functions of f = (f_low, f_high) that are zero at
f = 0. Within a cell the CES treats all workers as perfect substitutes, so a generation's labor differs
from another's only by its quantity in each cell.

Attribution (first order, stated as such): the Aumann-Shapley path integral along the proportional
removal path, P = sum_s f_s * integral_0^1 dP/df_s(t f) dt, splits P exactly across the two cells; each
cell's part goes to the generations in proportion to their share of the union's labor in that cell,
P_g = sum_s (L_gs / L_s) * AS_s. The same holds for F. This is an attribution, not a counterfactual:
removing one generation alone gives a different number, because P is not linear in f. Those stand-alone
removals, and the simple split by total labor income, are written beside it for comparison.
Gates (exit 1): the rebuilt composition equals skill_composition.csv; phi(f) reproduces model.json's P and
F in all 3,888 scenarios (1e-6 bn); the cell parts sum to phi(f) before the final closure (1e-6
relative); the generations sum to the union exactly.
Outputs: derived/production_by_generation.json. Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/generation_account_2026_09_24/production.py
"""
from __future__ import annotations

import importlib.util
import itertools
import json
import sys

import numpy as np
import pandas as pd

import frame as F

FAILS = []
NODES = 24  # Gauss-Legendre nodes on [0, 1]
STEP = 1e-5  # central-difference step in the cell fraction; above the 1e-12 fixed-point noise, below every t*f
TAX = [.384, .426]  # matched_benefits: transported marginal labor tax rates by skill
CAPITAL_TAX = .246


def gate(label, ok, detail=""):
    print(f"  {'✓' if ok else '✗'} {label}{' — ' + detail if detail else ''}", flush=True)
    if not ok:
        FAILS.append(label)


def load_model():
    spec = importlib.util.spec_from_file_location("matched_ces", F.FISCAL / "matched_benefits_2026_09_19/model.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def composition(d, civ, omega):
    """Positive earnings by skill cell: national, union, and by generation (per convention)."""
    w = d.pwwgt0.to_numpy(float)
    out = {}
    for proxy, split in itertools.product(("PEARNVAL", "WSAL_VAL"), ("hs_or_less", "below_ba")):
        earnings = np.maximum(d[proxy].to_numpy(float), 0)
        cut = 39 if split == "hs_or_less" else 42
        cells = [d.A_HGA.between(31, cut).to_numpy(), d.A_HGA.between(cut + 1, 46).to_numpy()]
        national = np.array([earnings[civ & c] @ w[civ & c] for c in cells])
        gens = {conv: np.array([F.totals(earnings * c, w, omega[conv]) for c in cells]) for conv in omega}
        out[(proxy, split)] = dict(national=national, gens=gens)
    return out


def phi(model, shares, fractions, sigma, labor_share, adjustment, elasticity, retention, excluded):
    """P and F per unit of scale for fraction arrays of shape (2, M)."""
    shares = np.repeat(shares[:, None], fractions.shape[1], axis=1)
    result = model.equilibrium(shares, fractions, sigma, labor_share, adjustment, elasticity)
    part = model.fiscal_and_private(result, TAX, CAPITAL_TAX, retention, excluded)
    return part["private_wtp"], part["current_receipts_gain"]


def main():
    model = load_model()
    d = F.load()
    civ, union, gens = F.masks(d)
    omega, _, _ = F.assignments(d, civ, union, gens)
    comp = composition(d, civ, omega)
    published = pd.read_csv(F.FISCAL / "matched_benefits_2026_09_19/derived/skill_composition.csv")
    worst = 0.0
    for (proxy, split), c in comp.items():
        for group, values in [("national", c["national"]), ("target", c["gens"]["a"].sum(axis=1))]:
            want = published.query("proxy == @proxy and split == @split and group == @group").sort_values("skill").estimate.to_numpy()
            worst = max(worst, float(np.max(np.abs(values / want - 1))))
    gate("union and national earnings by skill cell reproduce skill_composition.csv", worst < 1e-12, f"{worst:.1e}")

    m = json.loads((F.FISCAL / "assumption_explorer_2026_09_21/derived/model.json").read_text())
    dims = m["production"]["dims"]
    order = ["proxy", "split", "normalization", "labor_share", "sigma", "capital_adjustment",
             "labor_supply_elasticity", "capital_tax_retention", "excluded_capital_owner_share"]
    gdp = json.loads((F.FISCAL / "matched_benefits_2026_09_19/derived/audit.json").read_text())["gdp_billions"]
    x, wq = np.polynomial.legendre.leggauss(NODES)
    t, wq = (x + 1) / 2, wq / 2
    n = int(np.prod([len(dims[k]) for k in order]))
    out = {conv: {g: {"P": np.zeros(n), "F": np.zeros(n)} for g in F.GENS} for conv in omega}
    extra = {k: {g: {"P": np.zeros(n), "F": np.zeros(n)} for g in F.GENS}
             for k in ("standalone_a", "labor_income_share_a")}
    cell_parts = {"P": np.zeros((n, 2)), "F": np.zeros((n, 2))}
    worst_model, worst_closure = 0.0, 0.0
    for index, combo in enumerate(itertools.product(*[dims[k] for k in order])):
        s = dict(zip(order, combo))
        c = comp[(s["proxy"], s["split"])]
        national = c["national"]
        shares = national / national.sum()
        f = c["gens"]["a"].sum(axis=1) / national
        scale = (gdp * 1e9 if s["normalization"] == "gdp" else national.sum() / s["labor_share"]) / 1e9
        args = (s["sigma"], s["labor_share"], s["capital_adjustment"], s["labor_supply_elasticity"],
                s["capital_tax_retention"], s["excluded_capital_owner_share"])
        # Columns: phi(f); then for each node k and cell j, t_k f +/- STEP e_j.
        cols = [f]
        for tk in t:
            for j in range(2):
                e = np.zeros(2)
                e[j] = STEP
                cols += [tk * f + e, tk * f - e]
        # Stand-alone removals of each generation (convention a).
        for g in range(len(F.GENS)):
            cols.append(c["gens"]["a"][:, g] / national)
        P, Fv = phi(model, shares, np.column_stack(cols), *args)
        total = {"P": P[0] * scale, "F": Fv[0] * scale}
        stored = {"P": m["production"]["private_wtp_bn"][index], "F": m["production"]["induced_receipts_bn"][index]}
        for key in ("P", "F"):
            worst_model = max(worst_model, abs(total[key] - stored[key]))
        for key, vals in [("P", P), ("F", Fv)]:
            deriv = (vals[1:1 + 4 * NODES:2] - vals[2:2 + 4 * NODES:2]) / (2 * STEP)  # node-major, cell-minor
            deriv = deriv.reshape(NODES, 2)
            parts = f * (wq @ deriv) * scale
            worst_closure = max(worst_closure, abs(parts.sum() - total[key]) / max(abs(total[key]), 1.0))
            # Close exactly on the model's stored value (nine decimals): the residual (quadrature,
            # differencing and rounding) is spread in proportion to the parts.
            parts = parts * (stored[key] / parts.sum()) if parts.sum() else parts
            cell_parts[key][index] = parts
            for conv in omega:
                frac = c["gens"][conv] / c["gens"][conv].sum(axis=1, keepdims=True)  # cell x generation
                gpart = parts @ frac
                for g, gname in enumerate(F.GENS):
                    out[conv][gname][key][index] = gpart[g]
            for g, gname in enumerate(F.GENS):
                extra["standalone_a"][gname][key][index] = vals[1 + 4 * NODES + g] * scale
                labor = c["gens"]["a"][:, g].sum() / c["gens"]["a"].sum()
                extra["labor_income_share_a"][gname][key][index] = total[key] * labor
    gate("phi(f) reproduces model.json's P and F in every scenario", worst_model < 1e-6, f"max |diff| {worst_model:.1e} bn")
    gate("cell parts sum to phi(f) before closure", worst_closure < 1e-6,
         f"max residual {worst_closure:.1e} (relative, or bn where |phi| < 1)")
    for conv in omega:
        for key, source in [("P", "private_wtp_bn"), ("F", "induced_receipts_bn")]:
            s = sum(out[conv][g][key] for g in F.GENS)
            err = float(np.max(np.abs(s - np.array(m["production"][source]))))
            gate(f"({conv}) generations' {key} sum to the union in all {n} scenarios", err < 1e-12, f"{err:.1e}")
    ref = m["production"]["reference"]
    idx = {}
    for norm in dims["normalization"]:
        combo = [ref[k] if k != "normalization" else norm for k in order]
        idx[norm] = int(np.ravel_multi_index([dims[k].index(v) for k, v in zip(order, combo)], [len(dims[k]) for k in order]))
    summary = {}
    for norm, i in idx.items():
        summary[norm] = {
            "union": {"P": m["production"]["private_wtp_bn"][i], "F": m["production"]["induced_receipts_bn"][i]},
            "cells": {"P": cell_parts["P"][i].tolist(), "F": cell_parts["F"][i].tolist()},
            **{f"attribution_{conv}": {g: {k: out[conv][g][k][i] for k in ("P", "F")} for g in F.GENS} for conv in omega},
            **{name: {g: {k: extra[name][g][k][i] for k in ("P", "F")} for g in F.GENS} for name in extra}}
        print(f"  {norm}: union P+F {summary[norm]['union']['P'] + summary[norm]['union']['F']:.3f}; "
              + "; ".join(f"{g} {summary[norm]['attribution_a'][g]['P'] + summary[norm]['attribution_a'][g]['F']:.3f}"
                          f" (alone {summary[norm]['standalone_a'][g]['P'] + summary[norm]['standalone_a'][g]['F']:.3f})"
                          for g in F.GENS))
    labor = {f"{p}|{s}": {conv: (c["gens"][conv] / c["gens"][conv].sum(axis=1, keepdims=True)).tolist() for conv in omega}
             for (p, s), c in comp.items()}
    payload = dict(meta=dict(method="Aumann-Shapley along t*f, cells to generations by labor share", nodes=NODES,
                             step=STEP, reference_index=idx, labor_share_by_cell=labor,
                             closure_residual_max=worst_closure, model_reproduction_max_bn=worst_model),
                   reference=summary,
                   series={conv: {g: {k: out[conv][g][k].tolist() for k in ("P", "F")} for g in F.GENS} for conv in omega})
    (F.OUT / "production_by_generation.json").write_text(json.dumps(payload) + "\n")
    if FAILS:
        print(f"✗ {len(FAILS)} gate(s) failed: {FAILS}")
        sys.exit(1)
    print("  ✓ all production gates passed")


if __name__ == "__main__":
    main()
