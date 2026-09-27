"""Items 2 and 4 of BRIEF.md: the production grid on the account's row-4 weights, and public pay.

Item 2. The account reweights the Mexico-born outside California and Texas to ACS 2024 totals by citizenship
(naturalized x 0.856, noncitizens x 0.778; conceptual audit ffcce20 section C). The production model still uses the
unweighted CPS population. conceptual_audit_2026_09_27/probe_production.py recalibrates the reference cell on those
weights. This script rebuilds every one of model.json's 3,888 production cells the same way, because the sign
break-even ranges over 864 of them (main_case_2026_09_24/sign_reversal.cjs productions()):
  - the CES and the tax partition are matched_benefits_2026_09_19/model.py's, imported unchanged;
  - the cell grid, the scalar solve for P and F and the 161-column solve for the sampling SE follow
    matched_benefits_2026_09_19/builder.py and full_account_benefits_2026_09_20/builder.py (expand_ownership);
  - the row-4 factors are the probe's (ACS person file, Mexico-born, CIT 4 and 5, outside CA and TX, household
    population), applied per weight column, so each replicate is raked to the same ACS total.
Gates, before anything is written: on the published weights every cell's P, F and SE reproduces model.json; the
reference cell reproduces the audit memo's figures on both weights.

Item 4. The production model changes the wages of public workers, whose pay their employer does not recover. At the
case's production cell, the public employers' charge is each skill group's public payroll share of the incumbents'
earnings times the model's incumbent labor gain in that group: the part of P + F that public employers pay. Public
payroll is the longest job's wage and salary (ERN_VAL, ERN_SRCE 1) where that job is federal, state or local (LJCW 2-4,
CPS ASEC 2025, longest job last year); the base is the model's own, positive person earnings (PEARNVAL). Incumbents are
the civilian residents outside the group; the reweight moves none of them.

Writes derived/production_row4.json. Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/main_case_candidate_2026_09_28/production_row4.py
"""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import hashlib
import itertools
import json

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
F = ROOT / "infra/immigration-fiscal"
LANE = F / "cps_imputation_keys_2026_09_23"
sys.path.insert(0, str(LANE))
sys.path.insert(0, str(F / "matched_benefits_2026_09_19"))
import common as c  # noqa: E402
from model import equilibrium, fiscal_and_private  # noqa: E402

SOURCES = {
    "cps_lane_common": LANE / "common.py",
    "cps_lane_parquet": LANE / "_cache/asec25_lane.parquet",
    "production_model": F / "matched_benefits_2026_09_19/model.py",
    "acs_person_2024": F / "dataset_integrity_2026_09_23/_cache/acs_person_2024.parquet",
    "explorer_model": F / "assumption_explorer_2026_09_21/derived/model.json",
    "audit_probe": F / "conceptual_audit_2026_09_27/probe_production.py",
}
GDP_BN = 29298.0          # matched_benefits_2026_09_19/builder.py --gdp-billions default
TAX = [0.384, 0.426]      # builder.py: transported labor marginal rates by skill
CAPITAL_TAX = 0.246
CUT = {"hs_or_less": 39, "below_ba": 42}
PUBLIC_LJCW = {2: "federal", 3: "state", 4: "local"}
# The audit memo's figures (research/immigration-conceptual-audit-2026-09-27.md, section C): P+F cash / GDP.
MEMO = {"published": {"cash": 8.791, "gdp": 13.323}, "row4": {"cash": 7.683, "gdp": 11.680}}
ROUND = 9                 # model.json's rounding (assumption_explorer_2026_09_21/build_model.py ROUND)

GATES = []


def gate(name, ok, detail=""):
    GATES.append({"gate": name, "passed": bool(ok), "detail": detail})
    print(f"  {'PASS' if ok else 'FAIL'} {name}{' — ' + detail if detail else ''}", flush=True)


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def se(v):
    # builder.py summarize(): successive-difference replicate variance, 160 replicates
    return float(np.sqrt(4 / 160 * np.square(v[1:] - v[0]).sum()))


def main():
    pins = {k: sha(p) for k, p in SOURCES.items()}
    cols = ["PRPERTYP", "A_AGE", "PRCITSHP", "PENATVTY", "PEFNTVTY", "PEMNTVTY", "PRDTHSP", "A_HGA", "GESTFIPS",
            "WSAL_VAL", "SEMP_VAL", "FRSE_VAL", "PEARNVAL", "LJCW", "ERN_VAL", "ERN_SRCE"] + c.REPS
    d = pd.read_parquet(SOURCES["cps_lane_parquet"], columns=cols)
    civ, target = c.masks(d)
    W = d[c.REPS].to_numpy(float)
    print("[gates: the probe's frame]")
    gate("the group is the account's 40.9m (common.TARGET_POP)", abs(W[target, 0].sum() - c.TARGET_POP) < 0.01,
         f"{W[target, 0].sum():,.2f}")
    pearn = d.PEARNVAL.to_numpy(float)
    gate("PEARNVAL is WSAL_VAL + SEMP_VAL + FRSE_VAL on every record",
         np.array_equal(pearn, (d.WSAL_VAL + d.SEMP_VAL + d.FRSE_VAL).to_numpy(float)))

    # Row-4 factors: the probe's, per weight column.
    acs = pd.read_parquet(SOURCES["acs_person_2024"], columns=["ST", "RELSHIPP", "POBP", "CIT", "PWGTP"])
    acs = acs[acs.RELSHIPP.ne(37) & acs.POBP.eq(303) & acs.CIT.isin([4, 5]) & ~acs.ST.isin([6, 48])]
    W4 = W.copy()
    factors, reweighted = {}, np.zeros(len(d), bool)
    for status, label in [(4, "naturalized"), (5, "noncitizen")]:
        mask = (d.PENATVTY.eq(303) & d.PRCITSHP.eq(status) & ~d.GESTFIPS.isin([6, 48])).to_numpy()
        desired = float(acs.loc[acs.CIT.eq(status), "PWGTP"].sum())
        f = desired / W[mask].sum(axis=0)
        W4[mask] *= f
        reweighted |= mask
        factors[label] = {"records": int(mask.sum()), "cps_population": float(W[mask, 0].sum()),
                          "acs_population": desired, "factor": float(f[0]),
                          "replicate_factor_range": [float(f[1:].min()), float(f[1:].max())]}
    gate("the reweight moves only the group's records (civilian records outside the group keep their weights)",
         not np.any(reweighted & civ & ~target))
    gate("row-4 factors are the audit's 0.856 / 0.778 (conceptual audit section C)",
         round(factors["naturalized"]["factor"], 3) == 0.856 and round(factors["noncitizen"]["factor"], 3) == 0.778,
         f"{factors['naturalized']['factor']:.6f} / {factors['noncitizen']['factor']:.6f}")

    # Skill earnings by proxy and split: national (civilian) and group, 2 x 161, on both weights.
    earn = {"PEARNVAL": np.maximum(pearn, 0), "WSAL_VAL": np.maximum(d.WSAL_VAL.to_numpy(float), 0)}
    hga = d.A_HGA
    totals = {}
    for proxy, split in itertools.product(("PEARNVAL", "WSAL_VAL"), ("hs_or_less", "below_ba")):
        e = earn[proxy]
        if not hga[(e > 0) & civ].between(31, 46).all():
            raise SystemExit("[BLOCKED] a positive earner has missing or reserved education (builder.py check)")
        cut = CUT[split]
        skill = [hga.between(31, cut).to_numpy(), hga.between(cut + 1, 46).to_numpy()]
        for name, w in (("published", W), ("row4", W4)):
            totals[(proxy, split, name)] = {
                "national": np.array([(e * cell * civ) @ w for cell in skill]),
                "target": np.array([(e * cell * target) @ w for cell in skill]),
            }

    model = json.loads(SOURCES["explorer_model"].read_text())
    prod = model["production"]
    dims = prod["dims"]
    order = ["proxy", "split", "normalization", "labor_share", "sigma", "capital_adjustment",
             "labor_supply_elasticity", "capital_tax_retention", "excluded_capital_owner_share"]
    gate("model.json's production dims are the builder's grid, in engine order",
         list(dims) == order or sorted(dims) == sorted(order), json.dumps({k: dims[k] for k in order}))

    def solve(t, normalization, s, sigma, adjustment, elasticity, point_only):
        nat, tgt = (t["national"][:, :1], t["target"][:, :1]) if point_only else (t["national"], t["target"])
        shares, fractions = nat / nat.sum(axis=0), tgt / nat
        scale = np.full(nat.shape[1], GDP_BN * 1e9) if normalization == "gdp" else nat.sum(axis=0) / s
        return equilibrium(shares, fractions, sigma, s, adjustment, elasticity), scale

    grids = {"published": {"P": [], "F": [], "SE": []}, "row4": {"P": [], "F": [], "SE": []}}
    cache = {}
    for cell in itertools.product(*[dims[k] for k in order]):
        proxy, split, normalization, s, sigma, adjustment, elasticity, retention, excluded = cell
        for name in ("published", "row4"):
            t = totals[(proxy, split, name)]
            key = (proxy, split, name, normalization, s, sigma, adjustment, elasticity)
            if key not in cache:
                cache[key] = (solve(t, normalization, s, sigma, adjustment, elasticity, True),
                              solve(t, normalization, s, sigma, adjustment, elasticity, False))
            (r1, sc1), (r161, sc161) = cache[key]
            # P and F: the scalar solve on the point totals (full_account_benefits expand_ownership).
            part = fiscal_and_private(r1, TAX, CAPITAL_TAX, retention, excluded)
            grids[name]["P"].append(float(part["private_wtp"][0] * sc1[0] / 1e9))
            grids[name]["F"].append(float(part["current_receipts_gain"][0] * sc1[0] / 1e9))
            # SE: the 161-column solve, core ownership only (builder.py; the expansion keeps no SE otherwise).
            if excluded == 0:
                p161 = fiscal_and_private(r161, TAX, CAPITAL_TAX, retention)
                grids[name]["SE"].append(se(p161["private_plus_receipts"] * sc161 / 1e9))
            else:
                grids[name]["SE"].append(None)

    print("[gates: the published grid reproduces model.json]")
    n = len(prod["private_wtp_bn"])
    gate("3,888 cells", n == 3888 and len(grids["published"]["P"]) == n, str(n))
    dP = max(abs(a - b) for a, b in zip(grids["published"]["P"], prod["private_wtp_bn"]))
    dF = max(abs(a - b) for a, b in zip(grids["published"]["F"], prod["induced_receipts_bn"]))
    gate("private P, every cell (model.json rounds to 1e-9)", dP < 2e-9, f"max |diff| {dP:.2e} bn")
    gate("induced receipts F, every cell", dF < 2e-9, f"max |diff| {dF:.2e} bn")
    pairs = [(a, b) for a, b in zip(grids["published"]["SE"], prod["sampling_se_bn"])]
    gate("sampling SE present exactly where model.json has one", all((a is None) == (b is None) for a, b in pairs))
    dS = max(abs(a - b) for a, b in pairs if a is not None and b is not None)
    gate("sampling SE, every core-ownership cell", dS < 2e-9, f"max |diff| {dS:.2e} bn")

    def index(**v):
        i = 0
        for k in order:
            i = i * len(dims[k]) + [j for j, x in enumerate(dims[k]) if x == v[k] or
                                    (isinstance(x, float) and abs(x - v[k]) < 1e-9)][0]
        return i

    ref = dict(model["production"]["reference"])
    reference = {}
    for name in ("published", "row4"):
        reference[name] = {}
        for normalization in ("cash", "gdp"):
            i = index(**dict(ref, normalization=normalization))
            P, Fi = grids[name]["P"][i], grids[name]["F"][i]
            reference[name][normalization] = {"index": i, "P_bn": P, "F_bn": Fi, "P_plus_F_bn": P + Fi,
                                              "sampling_se_bn": grids[name]["SE"][i]}
    print("[gates: the reference cell reproduces the audit memo]")
    for name in ("published", "row4"):
        for normalization in ("cash", "gdp"):
            v = reference[name][normalization]["P_plus_F_bn"]
            gate(f"{name} {normalization} P+F is the memo's {MEMO[name][normalization]}",
                 abs(v - MEMO[name][normalization]) < 5e-4, f"{v:.6f}")
    change = {k: reference["published"][k]["P_plus_F_bn"] - reference["row4"][k]["P_plus_F_bn"] for k in ("cash", "gdp")}
    gate("the cost rises by the memo's $1.107bn (cash) / $1.643bn (GDP)",
         abs(change["cash"] - 1.107) < 1e-3 and abs(change["gdp"] - 1.643) < 1e-3,
         f"{change['cash']:.6f} / {change['gdp']:.6f}")

    # ------------------------------------------------------------------------------------------------------------
    # Item 4: public pay at the case's production cell.
    incumbents = civ & ~target
    ern, src, ljcw = d.ERN_VAL.to_numpy(float), d.ERN_SRCE.to_numpy(), d.LJCW.to_numpy()
    public = np.isin(ljcw, list(PUBLIC_LJCW)) & (src == 1)
    cut = CUT[ref["split"]]
    skill = [hga.between(31, cut).to_numpy(), hga.between(cut + 1, 46).to_numpy()]
    w0 = W[:, 0]
    base = np.array([(earn["PEARNVAL"] * cell * incumbents) @ w0 for cell in skill])
    t_pub = totals[(ref["proxy"], ref["split"], "published")]
    gate("the incumbents' earnings base is the model's national less the group's",
         np.allclose(base, t_pub["national"][:, 0] - t_pub["target"][:, 0], rtol=1e-12))
    pay = {level: np.array([(np.maximum(ern, 0) * cell * incumbents * public * (ljcw == code)) @ w0 for cell in skill])
           for code, level in PUBLIC_LJCW.items()}
    payroll = sum(pay.values())
    pi = payroll / base
    gate("public payroll is inside the base in each skill group", bool(np.all((pi > 0) & (pi < 1))),
         f"shares {pi[0]:.4f} / {pi[1]:.4f}")
    public_pay = {"definition": {
        "charge": "sum over the two skill groups of (public payroll / incumbent earnings) x the model's incumbent labor gain "
                  "(labor_gain = pay with the group - pay without it); positive raises the group's cost",
        "public_payroll": "ERN_VAL (longest job's earnings) with ERN_SRCE 1 (wage and salary) and LJCW 2-4 (federal, state, "
                          "local), civilian residents outside the group, CPS ASEC 2025 person weight",
        "base": "the production model's own incumbent earnings: max(PEARNVAL, 0) in the skill group, civilian residents "
                "outside the group",
        "cell": {k: ref[k] for k in ("proxy", "split", "labor_share", "sigma", "capital_adjustment",
                                     "labor_supply_elasticity", "capital_tax_retention", "excluded_capital_owner_share")},
        "response": "1: public employers pay the wage change on an unchanged public workforce and output (adversarial audit 61b4eac section 1)"},
        "skill_groups": ["high school or less", "more than high school"],
        "incumbent_earnings_bn": (base / 1e9).tolist(),
        "public_payroll_bn": {level: (v / 1e9).tolist() for level, v in pay.items()},
        "public_share_of_incumbent_earnings": pi.tolist()}
    for name in ("published", "row4"):
        t = totals[(ref["proxy"], ref["split"], name)]
        public_pay[name] = {}
        for normalization in ("cash", "gdp"):
            (r1, sc1), _ = cache[(ref["proxy"], ref["split"], name, normalization, ref["labor_share"], ref["sigma"],
                                  ref["capital_adjustment"], ref["labor_supply_elasticity"])]
            gain = r1["labor_gain"][:, 0] * sc1[0] / 1e9
            by_skill = pi * gain
            by_level = {level: float(np.sum(pay[code_level] / base * gain))
                        for code_level, level in ((lv, lv) for lv in PUBLIC_LJCW.values())}
            public_pay[name][normalization] = {
                "wage_without_over_with": r1["wage_without_over_with"][:, 0].tolist(),
                "incumbent_labor_gain_bn": gain.tolist(), "charge_by_skill_bn": by_skill.tolist(),
                "charge_by_level_bn": by_level, "charge_bn": float(by_skill.sum())}
        gate(f"{name}: the charge by level sums to the charge",
             all(abs(sum(public_pay[name][k]["charge_by_level_bn"].values()) - public_pay[name][k]["charge_bn"]) < 1e-9
                 for k in ("cash", "gdp")))

    gate("sources unchanged during the run", all(sha(p) == pins[k] for k, p in SOURCES.items()))
    if not all(g["passed"] for g in GATES):
        raise SystemExit(f"[BLOCKED] {sum(not g['passed'] for g in GATES)} gate(s) failed; nothing written")
    r9 = lambda xs: [None if x is None else round(x, ROUND) for x in xs]
    out = {
        "meta": {
            "item": "BRIEF.md items 2 and 4 (main_case_candidate_2026_09_28, case sept28_candidate)",
            "population": "CPS ASEC 2025 civilian Mexican-origin observable union (common.masks)",
            "weights": {"published": "CPS person weight (pwwgt0) and its 160 replicates",
                        "row4": "the same, with the Mexico-born outside California and Texas raked by citizenship to ACS 2024 "
                                "household-population totals, column by column (conceptual_audit_2026_09_27/probe_production.py)"},
            "grid": "every model.json production cell; P and F from the scalar solve, SE from the 161-column solve "
                    "(full_account_benefits_2026_09_20 expand_ownership; matched_benefits_2026_09_19/builder.py)",
            "no_national_reraking": "national skill totals include the reweighted records; nothing else is re-raked (as the probe)",
            "source_sha256": {k: pins[k] for k in SOURCES},
            "source_paths": {k: str(p.relative_to(ROOT)) for k, p in SOURCES.items()},
        },
        "populations": {"published": float(W[target, 0].sum()), "row4": float(W4[target, 0].sum())},
        "row4_factors": factors,
        "reference": reference,
        "cost_change_at_reference_bn": change,
        "grid": {"dims": {k: dims[k] for k in order},
                 "published": {"private_wtp_bn": r9(grids["published"]["P"]), "induced_receipts_bn": r9(grids["published"]["F"]),
                               "sampling_se_bn": r9(grids["published"]["SE"])},
                 "row4": {"private_wtp_bn": r9(grids["row4"]["P"]), "induced_receipts_bn": r9(grids["row4"]["F"]),
                          "sampling_se_bn": r9(grids["row4"]["SE"])}},
        "public_pay": public_pay,
        "gates": GATES,
    }
    dest = HERE / "derived" / "production_row4.json"
    dest.parent.mkdir(exist_ok=True)
    dest.write_text(json.dumps(out, indent=1) + "\n")
    print(f"\n  reference P+F: GDP {reference['published']['gdp']['P_plus_F_bn']:.6f} -> {reference['row4']['gdp']['P_plus_F_bn']:.6f}; "
          f"cash {reference['published']['cash']['P_plus_F_bn']:.6f} -> {reference['row4']['cash']['P_plus_F_bn']:.6f}")
    for name in ("published", "row4"):
        print(f"  public pay ({name}): GDP {public_pay[name]['gdp']['charge_bn']:+.4f}bn, cash {public_pay[name]['cash']['charge_bn']:+.4f}bn")
    print(f"all {len(GATES)} gates passed; wrote {dest.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
