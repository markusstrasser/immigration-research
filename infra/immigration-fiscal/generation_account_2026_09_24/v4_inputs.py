"""v4 case (sept29): the per-generation inputs of the September 29 main case's edits.

The case adopted on 2026-09-29 (candidate v4's set, main_case_2026_09_29) moves the production grid to the account's
row-4 weights (item 2), keys roads by driver miles and splits a tax on tenant-occupied housing out of the business
property line (item 5). Their generation splits need three measurements on the frame of the lane V4_LANE_DIR names
(this lane and its three generations by default; the late-arrival lane points it at itself, with LATE_DEF, for its
nine cells):
  production    the production term on the row-4 weights (main_case_candidate_2026_09_28/production_row4.py: the
                Mexico-born outside California and Texas raked to ACS 2024 totals by citizenship), attributed as
                production.py attributes model.json's grid: Aumann-Shapley along t*f, each skill cell's part to the
                generations by their share of the union's labor in it, closed on the stored row-4 value of each
                scenario;
  under5_share  each generation's persons under 5 over its persons, row-4 weights; the union's is the roads lane's
                (roads_mileage_key_2026_09_29/derived/inputs.json under5_share, gate), which ties the headcounts below
                to the roads key's definition;
  tenant_share  each generation's part of the group's share of contract rent (receipt_side_long_run_2026_09_28
                housing.json keys.rent_share, 0.114667): the group's rent in each state (states.csv group_rent)
                split by the generations' persons in homes rented for cash (H_TENURE 2) there, row-4 weights. Beside
                it (tenant_share_national) the same persons nationally, no state weights;
  headcount     persons, adults (18 and over) and persons aged 5 and over by generation on the row-4 weights: the
                case's per-member basis (the union's 39,712,493, main_case_candidate_v4_2026_09_29 package.cjs COUNT)
                and the driver-age persons the roads split uses (driver miles go to persons aged 5 and over at the
                union's miles per such person).
Both conventions: (a) own generation, (b) minors with their parents (frame.assignments).
Gates (exit 1, nothing written): the row-4 mask's records, CPS population and factors are production_row4.json's;
the reweight moves only union records among the civilian, and the union's row-4 headcount is the account's; phi(f)
on the row-4 weights reproduces production_row4.json's row-4 P and F in all 3,888 scenarios (1e-6 bn); the cell
parts sum to phi(f) before closure (1e-6 relative); the generations add to the stored row-4 grid in every scenario
(1e-12 bn); the union's under-5 share is the roads lane's (1e-9); the states' group rent over all rent rounds to
rent_share; each convention's tenant shares add to rent_share (1e-15).
Output: v4_inputs.json in the lane's frame.OUT (this lane: derived/; the late-arrival lane: _cache/split_<LATE_DEF>/).
Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/generation_account_2026_09_24/v4_inputs.py
  LATE_DEF=central V4_LANE_DIR=infra/immigration-fiscal/late_arrival_account_line_2026_09_27 OPENBLAS_NUM_THREADS=1 \
    uv run --no-project python3 infra/immigration-fiscal/generation_account_2026_09_24/v4_inputs.py
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # read-only imports from other lanes: write nothing beside them

import csv  # noqa: E402
import importlib.util  # noqa: E402
import itertools  # noqa: E402
import json  # noqa: E402
import os  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402

HERE = Path(__file__).resolve().parent
LANE = Path(os.environ.get("V4_LANE_DIR", str(HERE))).resolve()
_spec = importlib.util.spec_from_file_location("v4_lane_frame", LANE / "frame.py")
F = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(F)

FISCAL = F.FISCAL
ROW4 = FISCAL / "main_case_candidate_2026_09_28/derived/production_row4.json"
ROADS = FISCAL / "roads_mileage_key_2026_09_29/derived/inputs.json"
HOUSING = FISCAL / "receipt_side_long_run_2026_09_28/derived/housing.json"
STATES_CSV = FISCAL / "receipt_side_long_run_2026_09_28/derived/states.csv"
MODEL = FISCAL / "assumption_explorer_2026_09_21/derived/model.json"
MATCHED = FISCAL / "matched_benefits_2026_09_19"
NODES = 24  # production.py's Gauss-Legendre nodes and difference step
STEP = 1e-5
TAX = [.384, .426]
CAPITAL_TAX = .246
MEXICO = 303
ROW4_STATUS = {"naturalized": 4, "noncitizen": 5}  # PRCITSHP; production_row4.py's reweight
ROW4_OUTSIDE = [6, 48]  # GESTFIPS: California and Texas keep their weights
CASH_RENT = 2  # H_TENURE: rented for cash
STATES = {1: "AL", 2: "AK", 4: "AZ", 5: "AR", 6: "CA", 8: "CO", 9: "CT", 10: "DE", 11: "DC", 12: "FL",
          13: "GA", 15: "HI", 16: "ID", 17: "IL", 18: "IN", 19: "IA", 20: "KS", 21: "KY", 22: "LA",
          23: "ME", 24: "MD", 25: "MA", 26: "MI", 27: "MN", 28: "MS", 29: "MO", 30: "MT", 31: "NE",
          32: "NV", 33: "NH", 34: "NJ", 35: "NM", 36: "NY", 37: "NC", 38: "ND", 39: "OH", 40: "OK",
          41: "OR", 42: "PA", 44: "RI", 45: "SC", 46: "SD", 47: "TN", 48: "TX", 49: "UT", 50: "VT",
          51: "VA", 53: "WA", 54: "WV", 55: "WI", 56: "WY"}  # state_priced_services_2026_09_29/state_price.py
FAILS = []


def gate(label, ok, detail=""):
    print(f"  {'✓' if ok else '✗'} {label}{' — ' + detail if detail else ''}", flush=True)
    if not ok:
        FAILS.append(label)


def load_model():
    spec = importlib.util.spec_from_file_location("matched_ces", MATCHED / "model.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def phi(model, shares, fractions, sigma, labor_share, adjustment, elasticity, retention, excluded):
    """P and F per unit of scale for fraction arrays of shape (2, M) (production.py's phi)."""
    shares = np.repeat(shares[:, None], fractions.shape[1], axis=1)
    result = model.equilibrium(shares, fractions, sigma, labor_share, adjustment, elasticity)
    part = model.fiscal_and_private(result, TAX, CAPITAL_TAX, retention, excluded)
    return part["private_wtp"], part["current_receipts_gain"]


def row4_weights(d, civ, union, row4):
    """pwwgt0 with production_row4.py's reweight of the Mexico-born outside California and Texas."""
    w = d.pwwgt0.to_numpy(float)
    w4 = w.copy()
    moved = np.zeros(len(d), bool)
    outside = ~d.GESTFIPS.isin(ROW4_OUTSIDE).to_numpy()
    factors = {}
    for label, status in ROW4_STATUS.items():
        mask = d.PENATVTY.eq(MEXICO).to_numpy() & d.PRCITSHP.eq(status).to_numpy() & outside
        ref = row4["row4_factors"][label]
        cps = float(w[mask].sum())
        f0 = ref["acs_population"] / cps
        gate(f"row 4, {label}: records, CPS population and factor are production_row4.json's",
             int(mask.sum()) == ref["records"] and abs(cps - ref["cps_population"]) < 1e-6 and abs(f0 - ref["factor"]) < 1e-12,
             f"{int(mask.sum())} records, {cps:,.2f} -> {ref['acs_population']:,}, factor {f0:.12f}")
        w4[mask] *= f0
        moved |= mask
        factors[label] = {"records": int(mask.sum()), "cps_population": cps, "acs_population": ref["acs_population"], "factor": f0}
    gate("the reweight moves only union records among the civilian", not np.any(moved & civ & ~union))
    head = float(w4[union].sum())
    gate("the union's row-4 headcount is the account's (production_row4.json populations.row4)",
         abs(head - row4["populations"]["row4"]) < 1e-6, f"{head:,.6f}")
    return w4, factors


def composition(d, civ, omega, w):
    """Positive earnings by skill cell on weights w: national, and by generation (per convention); production.py's."""
    out = {}
    for proxy, split in itertools.product(("PEARNVAL", "WSAL_VAL"), ("hs_or_less", "below_ba")):
        earnings = np.maximum(d[proxy].to_numpy(float), 0)
        cut = 39 if split == "hs_or_less" else 42
        cells = [d.A_HGA.between(31, cut).to_numpy(), d.A_HGA.between(cut + 1, 46).to_numpy()]
        national = np.array([earnings[civ & c] @ w[civ & c] for c in cells])
        gens = {conv: np.array([F.totals(earnings * c, w, omega[conv]) for c in cells]) for conv in omega}
        out[(proxy, split)] = dict(national=national, gens=gens)
    return out


def production(d, civ, omega, w4, row4):
    model = load_model()
    comp = composition(d, civ, omega, w4)
    m = json.loads(MODEL.read_text())
    dims = m["production"]["dims"]
    order = ["proxy", "split", "normalization", "labor_share", "sigma", "capital_adjustment",
             "labor_supply_elasticity", "capital_tax_retention", "excluded_capital_owner_share"]
    gate("production_row4.json's grid has model.json's dimensions",
         all(row4["grid"]["dims"][k] == dims[k] for k in order) and len(row4["grid"]["dims"]) == len(order))
    stored = {"P": row4["grid"]["row4"]["private_wtp_bn"], "F": row4["grid"]["row4"]["induced_receipts_bn"]}
    gdp = json.loads((MATCHED / "derived/audit.json").read_text())["gdp_billions"]
    x, wq = np.polynomial.legendre.leggauss(NODES)
    t, wq = (x + 1) / 2, wq / 2
    n = int(np.prod([len(dims[k]) for k in order]))
    gate("3,888 stored scenarios", n == len(stored["P"]) == len(stored["F"]) == 3888, str(n))
    out = {conv: {g: {"P": np.zeros(n), "F": np.zeros(n)} for g in F.GENS} for conv in omega}
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
        cols = [f]
        for tk in t:
            for j in range(2):
                e = np.zeros(2)
                e[j] = STEP
                cols += [tk * f + e, tk * f - e]
        P, Fv = phi(model, shares, np.column_stack(cols), *args)
        total = {"P": P[0] * scale, "F": Fv[0] * scale}
        for key in ("P", "F"):
            worst_model = max(worst_model, abs(total[key] - stored[key][index]))
        for key, vals in [("P", P), ("F", Fv)]:
            deriv = ((vals[1:1 + 4 * NODES:2] - vals[2:2 + 4 * NODES:2]) / (2 * STEP)).reshape(NODES, 2)
            parts = f * (wq @ deriv) * scale
            worst_closure = max(worst_closure, abs(parts.sum() - total[key]) / max(abs(total[key]), 1.0))
            parts = parts * (stored[key][index] / parts.sum()) if parts.sum() else parts
            for conv in omega:
                frac = c["gens"][conv] / c["gens"][conv].sum(axis=1, keepdims=True)  # cell x generation
                gpart = parts @ frac
                for g, gname in enumerate(F.GENS):
                    out[conv][gname][key][index] = gpart[g]
    gate("phi(f) on the row-4 weights reproduces production_row4.json's row-4 P and F in every scenario", worst_model < 1e-6,
         f"max |diff| {worst_model:.1e} bn")
    gate("cell parts sum to phi(f) before closure", worst_closure < 1e-6, f"max residual {worst_closure:.1e}")
    for conv in omega:
        for key in ("P", "F"):
            err = float(np.max(np.abs(sum(out[conv][g][key] for g in F.GENS) - np.array(stored[key]))))
            gate(f"({conv}) the generations' {key} add to the stored row-4 grid in all {n} scenarios", err < 1e-12, f"{err:.1e}")
    ref = {}
    for norm, i in ((k, row4["reference"]["row4"][k]["index"]) for k in ("cash", "gdp")):
        ref[norm] = {"index": i, "union": stored["P"][i] + stored["F"][i],
                     **{conv: {g: out[conv][g]["P"][i] + out[conv][g]["F"][i] for g in F.GENS} for conv in omega}}
        print(f"  {norm} reference (index {i}): union P+F {ref[norm]['union']:.6f}; "
              + "; ".join(f"{g} {ref[norm]['a'][g]:.6f}" for g in F.GENS))
    labor = {f"{p}|{s}": {conv: (c["gens"][conv] / c["gens"][conv].sum(axis=1, keepdims=True)).tolist() for conv in omega}
             for (p, s), c in comp.items()}
    return {"reference_P_plus_F_bn": ref, "labor_share_by_cell": labor, "closure_residual_max": worst_closure,
            "row4_reproduction_max_bn": worst_model,
            "series": {conv: {g: {k: out[conv][g][k].tolist() for k in ("P", "F")} for g in F.GENS} for conv in omega}}


def under5(d, union, omega, w4):
    age = d.A_AGE.to_numpy()
    small = (age < 5).astype(float)
    u = float((small * union) @ w4 / (union.astype(float) @ w4))
    roads = json.loads(ROADS.read_text())["under5_share"]["group"]
    gate("the union's under-5 share on the row-4 weights is the roads lane's (inputs.json under5_share.group)",
         abs(u - roads) < 1e-9, f"{u:.12f} vs {roads:.12f}")
    out = {"union": u}
    for conv in omega:
        pop = F.totals(np.ones(len(d)), w4, omega[conv])
        out[conv] = {g: float(F.totals(small, w4, omega[conv])[j] / pop[j]) for j, g in enumerate(F.GENS)}
    return out


def headcount(d, union, omega, w4):
    """Persons, adults (18 and over) and persons aged 5 and over by generation on the row-4 weights: the case's
    per-member basis, and the roads split's driver-age persons."""
    age = d.A_AGE.to_numpy()
    adult, five = (age >= 18).astype(float), (age >= 5).astype(float)
    out = {"union": {"population": float(union.astype(float) @ w4), "adults": float((adult * union) @ w4),
                     "persons_5plus": float((five * union) @ w4)}}
    for conv in omega:
        pop, ad, p5 = (F.totals(v, w4, omega[conv]) for v in (np.ones(len(d)), adult, five))
        out[conv] = {g: {"population": float(pop[j]), "adults": float(ad[j]), "persons_5plus": float(p5[j])}
                     for j, g in enumerate(F.GENS)}
        gate(f"({conv}) the generations' row-4 persons, adults and persons aged 5+ add to the union's",
             all(abs(v.sum() - out["union"][k]) < 1e-6 for v, k in ((pop, "population"), (ad, "adults"), (p5, "persons_5plus"))),
             "; ".join(f"{g} {pop[j]:,.0f} ({ad[j]:,.0f} adults, {p5[j]:,.0f} aged 5+)" for j, g in enumerate(F.GENS)))
    return out


def tenant(d, omega, w4):
    share = json.loads(HOUSING.read_text())["keys"]["rent_share"]
    with STATES_CSV.open() as f:
        rows = {r["state"]: r for r in csv.DictReader(f)}
    gate("states.csv covers the 50 states and DC, as the FIPS map", sorted(rows) == sorted(STATES.values()), f"{len(rows)} rows")
    group = {s: float(r["group_rent"]) for s, r in rows.items()}
    every = {s: float(r["all_rent"]) for s, r in rows.items()}
    implied = sum(group.values()) / sum(every.values())
    gate("the states' group rent over all rent rounds to housing.json's rent_share", round(implied, 6) == share,
         f"{implied:.9f} -> {share}")
    rent = d.H_TENURE.eq(CASH_RENT).to_numpy().astype(float)
    st = d.GESTFIPS.to_numpy()
    out = {"rent_share": share, "rule": {}, "national": {}, "states_without_union_renters": {}}
    for conv in omega:
        national = F.totals(rent, w4, omega[conv])
        num = np.zeros(len(F.GENS))
        missing = []
        for fips, abbr in STATES.items():
            here = F.totals(rent * (st == fips), w4, omega[conv])
            if here.sum() > 0:
                num += group[abbr] * here / here.sum()
            else:
                num += group[abbr] * national / national.sum()
                missing.append(abbr)
        rule = share * num / sum(group.values())
        nat = share * national / national.sum()
        gate(f"({conv}) the generations' tenant shares add to rent_share, by state and nationally",
             abs(rule.sum() - share) < 1e-15 and abs(nat.sum() - share) < 1e-15,
             "; ".join(f"{g} {rule[j]:.6f} ({nat[j]:.6f})" for j, g in enumerate(F.GENS)))
        out["rule"][conv] = {g: float(rule[j]) for j, g in enumerate(F.GENS)}
        out["national"][conv] = {g: float(nat[j]) for j, g in enumerate(F.GENS)}
        out["states_without_union_renters"][conv] = missing
    return out


def main():
    print(f"[v4 inputs] frame {F.__file__}; generations {', '.join(F.GENS)}")
    row4 = json.loads(ROW4.read_text())
    d = F.load()
    civ, union, gens = F.masks(d)
    omega, _, _ = F.assignments(d, civ, union, gens)
    w4, factors = row4_weights(d, civ, union, row4)
    print("[production on the row-4 weights]")
    prod = production(d, civ, omega, w4, row4)
    print("[under-5 shares]")
    u5 = under5(d, union, omega, w4)
    print("  " + "; ".join(f"({c}) " + ", ".join(f"{g} {u5[c][g]:.4f}" for g in F.GENS) for c in omega))
    print("[tenant shares]")
    ten = tenant(d, omega, w4)
    print("[row-4 headcounts]")
    heads = headcount(d, union, omega, w4)
    if FAILS:
        print(f"✗ {len(FAILS)} gate(s) failed, nothing written: {FAILS}")
        sys.exit(1)
    payload = {"meta": {"source": "generation_account_2026_09_24/v4_inputs.py", "frame": str(Path(F.__file__).relative_to(F.ROOT)),
                        "generations": F.GENS, "row4_factors": factors,
                        "production": "Aumann-Shapley along t*f on the row-4 weights (production.py's method), closed on "
                                      "main_case_candidate_2026_09_28/derived/production_row4.json grid.row4",
                        "under5_share": "persons under 5 over persons, row-4 weights",
                        "tenant_share": "rent_share x the group's rent by state (states.csv) split by the generations' persons in "
                                        "cash-rent homes (H_TENURE 2) in the state, row-4 weights; national: the same persons, no "
                                        "state weights",
                        "headcount": "persons, adults (18 and over) and persons aged 5 and over by generation, row-4 weights"},
               "production": prod, "under5_share": u5, "tenant_share": ten, "headcount": heads}
    out = F.OUT / "v4_inputs.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload) + "\n")
    print(f"  wrote {out.relative_to(F.ROOT)}")
    print("  ✓ all v4 input gates passed")


if __name__ == "__main__":
    main()
