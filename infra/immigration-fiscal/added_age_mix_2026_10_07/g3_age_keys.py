#!/usr/bin/env python3
"""The engine's G3+ keys by five-year age band: how much of each allocation key the identified third-plus holds at
each age, on the account's own per-person key vectors.

The engine's G3+ member (generation_account_2026_09_24 model_G3plus.json and its corrected payload, per member) has
one amount per cell: the union cell times the G3+ share of the cell's key and allocation (build_models.py), plus the
G3+ part of the corrections. keys.py builds those shares from per-person vectors on the account's CPS ASEC 2025 frame.
This script rebuilds the same vectors with keys.py's own functions (imported read-only: frame.py, the CPS imputation
lane's common.py, keys.owner_property / meps_keys / school_keys) and sums the G3+ part of each by age band:
T[side][allocation][key][band] = sum over G3+ persons in the band of vector x weight (convention a).

Re-weighting the G3+ persons to another age mix pi' multiplies band b by pi'_b / pi_b, so a cell's G3+ amount moves
by f = sum_b (pi'_b / pi_b) T_b / sum_b T_b (price.cjs). At pi' = pi, f is 1 exactly. The corrections in a cell take
its key's age profile [ASSUMPTION]. Keys keys.py builds from parts:
  use (justice)                  per-head part by persons, custody and arrest parts by persons aged 18-64 (keys.py's
                                 rule for the US-born); use|arrest_per_adult the arrest part by adults 18+;
                                 use_raw_coding its per-head part by persons and the rest by persons aged 18-64;
  uninsured_use_*                the Medicaid key's profile for the cell's Medicaid part, uninsured person-years for
                                 the under-charge (model.json cells and keys.py's shares give the two parts);
  observed_liability_plus_...    the CPS liability plus the BEA gap on the high-AGI key, banded with keys.py's formula;
  external, none                 zero for every group.
Cells whose key is not one of keys.py's (the v4 and engine-only lines):
  housing_support (a receipt cell's key)  the spending housing_support vector;
  renter_contract_rent                    persons in cash-rent homes (v4_inputs.py tenant(): H_TENURE 2);
  school_reprice, college_rekey, lane_constants: school_operating, postsecondary, resident_population;
  roads_vmt_sl/fed                        persons aged 5+ [INFERENCE: miles less the earnings key; small lines];
  state_price_<line>                      the parent line's key in the case: use, health_other, population.
Production: the wage key.

Gates (exit 1, nothing written): the G3+ band shares are white_lines.json's g3plus structure (1e-6: that frame weights
MARSUPWT / 100, this one pwwgt0; price.cjs re-weights by pi' / white_lines' pi, so the control is exact); every key's band
sum is generation_keys.csv's G3plus total (1e-9 relative); the justice parts give keys.py's G3+ use share (1e-12).
Outputs: derived/g3_age_keys.json, derived/gates_keys.json
Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/added_age_mix_2026_10_07/g3_age_keys.py
"""
from __future__ import annotations

import json
import resource
import sys
from pathlib import Path

sys.dont_write_bytecode = True  # read-only imports from other lanes: write nothing beside them

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
OUT = HERE / "derived"
GEN = FISCAL / "generation_account_2026_09_24"
sys.path.insert(0, str(GEN))
import frame as F  # noqa: E402
import keys as K  # noqa: E402

C = F.C
ALLOC = ["personal", "shared"]
BANDS = list(range(0, 80, 5)) + [80]
G3 = 2
GATES: list[dict] = []


def gate(name: str, ok: bool, detail: str = "") -> None:
    GATES.append({"gate": name, "passed": bool(ok), "detail": detail})
    print(f"  {'PASS' if ok else 'FAIL'} {name}{' - ' + detail if detail else ''}", flush=True)


def main() -> None:
    d = F.load()
    civ, union, gens = F.masks(d)
    omega, _, _ = F.assignments(d, civ, union, gens)
    w = d["pwwgt0"].to_numpy(float)
    d = d.drop(columns=[c for c in F.REPS if c != "pwwgt0"])
    age = d.A_AGE.to_numpy()
    band = np.minimum(age // 5 * 5, 80)
    wg = w * omega["a"][:, G3]
    onehot = np.stack([(band == b) for b in BANDS], axis=1).astype(float) * wg[:, None]

    def banded(v):
        return (np.asarray(v, float) @ onehot)

    pop = banded(np.ones(len(d)))
    pi = pop / pop.sum()
    wl = json.loads((FISCAL / "main_case_lineage_2026_10_05/derived/white_lines.json").read_text())["meta"]["age_structures"]["g3plus"]
    # The white lane's frame weights are MARSUPWT / 100, the account's pwwgt0 (frame.py checks them within 0.01).
    gate("the G3+ band shares on the account's frame are white_lines.json's g3plus structure (1e-6: the two weights)",
         max(abs(a - b) for a, b in zip(pi, wl)) < 1e-6, f"max |diff| {max(abs(a - b) for a, b in zip(pi, wl)):.1e}")

    index = C.spm_index(d)
    T = {"receipt": {a: {} for a in ALLOC}, "spending": {a: {} for a in ALLOC}}
    rkeys = C.receipt_keys(d, index)
    owner, params = K.owner_property(d)
    for a in ALLOC:
        for key, v in rkeys[a].items():
            T["receipt"][a][key] = banded(v)
        T["receipt"][a]["resident_population"] = pop.copy()
        T["receipt"][a]["modeled_owner_property"] = banded(owner)
    skeys = C.spending_vectors(d, index)
    medical, _, _, _ = K.meps_keys(d)
    edu = K.school_keys(d, civ, params)
    for a in ALLOC:
        for key, v in {**skeys[a], **medical}.items():
            T["spending"][a][key] = banded(v)
        T["spending"][a]["school_operating"] = banded(edu[a]["school"])
        T["spending"][a]["postsecondary"] = banded(edu[a]["P"])
        T["spending"][a]["education_mix"] = banded(edu[a]["school"] + edu[a]["P"])

    gk = pd.read_csv(GEN / "derived/generation_keys.csv")
    gk = gk[gk.convention == "a"].set_index(["side", "allocation", "key"]).G3plus
    worst, n = 0.0, 0
    for side in T:
        for a in ALLOC:
            for key, t in T[side][a].items():
                want = float(gk[(side, a, key)])
                worst = max(worst, abs(t.sum() - want) / max(abs(want), 1.0))
                n += 1
    gate(f"{n} keys: the band sums are generation_keys.csv's G3plus totals (1e-9 relative)", worst < 1e-9, f"{worst:.1e}")

    shares = json.loads((GEN / "derived/generation_key_shares.json").read_text())
    up = {k: np.asarray(v, float) for k, v in shares["meta"]["use_parts"]["a"].items()}
    n1864 = banded(((age >= 18) & (age <= 64)).astype(float))
    adults = banded((age >= 18).astype(float))
    prof = lambda x: x / x.sum()  # noqa: E731
    use = up["per_head"][G3] * prof(pop) + (up["custody"][G3] + up["arrest_like_custody"][G3]) * prof(n1864)
    alt = up["per_head"][G3] * prof(pop) + up["custody"][G3] * prof(n1864) + up["arrest_per_adult"][G3] * prof(adults)
    central = up["per_head"] + up["custody"] + up["arrest_like_custody"] + up["ice_interior"]
    gate("the justice parts give keys.py's G3+ use share (1e-12)",
         abs(use.sum() / central.sum() - shares["shares"]["spending"]["personal"]["use"]["a"][G3]) < 1e-12)
    split = pd.read_csv(FISCAL / "cj_use_allocation_2026_09_23/derived/central_split.csv").set_index("component")
    model = json.loads((FISCAL / "assumption_explorer_2026_09_21/derived/model.json").read_text())
    lines = {l["id"]: l for l in model["spending"]["lines"]}
    pop_part = up["per_head"][G3] / (up["per_head"].sum()) * split.per_head_bn.sum()
    for a in ALLOC:
        T["spending"][a]["use"] = use
        T["spending"][a]["use|arrest_per_adult"] = alt
        raw_g3 = (lines["public_order_safety"]["keys"]["use_raw_coding"][a]["target_bn"]
                  * shares["shares"]["spending"][a]["use_raw_coding"]["a"][G3])
        T["spending"][a]["use_raw_coding"] = pop_part * prof(pop) + (raw_g3 - pop_part) * prof(n1864)
    # Uninsured use: the cell's Medicaid part on the Medicaid key's profile, the under-charge on uninsured person-years.
    exposure = d.NOCOV_CYR.eq(3).to_numpy(float) + 0.5 * d.NOCOV_CYR.eq(2).to_numpy(float)
    unins = banded(exposure)
    med_line = lines["medicaid_and_chip_other_medical"]["keys"]
    for a in ALLOC:
        med_g3 = med_line["medicaid"][a]["target_bn"] * shares["shares"]["spending"][a]["medicaid"]["a"][G3]
        for key in [k for k in med_line if k.startswith("uninsured_use")]:
            cell_g3 = med_line[key][a]["target_bn"] * shares["shares"]["spending"][a][key]["a"][G3]
            T["spending"][a][key] = med_g3 * prof(T["spending"][a]["medicaid"]) + (cell_g3 - med_g3) * prof(unins)
    # The federal-gap arm, banded with keys.py's formula.
    cats = pd.read_csv(FISCAL / "full_account_receipts_2026_09_20/derived/category_allocations.csv")
    gap = cats.query("scenario_id == 'federal_gap_high_agi' and category == 'federal_income_tax'").set_index("allocation")
    tax = pd.read_csv(FISCAL / "admin_tax_checks_2026_09_19/derived/group_components.csv")
    for a in ALLOC:
        fb, hi = rkeys[a]["federal_liability"], rkeys[a]["federal_high_agi"]
        nat_fb = float(tax.query("allocation == @a and group == 'national_civilian' and metric == "
                                 "'federal_before_refundable'").value.iloc[0]) / 1e9
        hi_nat = float(hi[civ] @ w[civ])
        T["receipt"][a]["observed_liability_plus_positive_gap_high_agi"] = (
            banded(fb) / 1e9 + (gap.loc[a, "national_bn"] - nat_fb) * banded(hi) / hi_nat)
        share = T["receipt"][a]["observed_liability_plus_positive_gap_high_agi"].sum()
        gate(f"the federal-gap arm ({a}) banded sums to keys.py's G3+ cell share of the arm (1e-9 relative)",
             abs(share / gap.loc[a, "target_bn"] - shares["shares"]["receipt"][a]["observed_liability_plus_positive_gap_high_agi"]["a"][G3]) < 1e-9,
             f"{share:.6f}bn")
    # Keys outside keys.py (the v4 and engine-only lines).
    rent = banded(d.H_TENURE.eq(2).to_numpy(float))
    five = banded((age >= 5).astype(float))
    for a in ALLOC:
        T["receipt"][a]["none"] = np.zeros(len(BANDS))       # keys.py: zero for every generation
        T["spending"][a]["external"] = np.zeros(len(BANDS))
        T["receipt"][a]["housing_support"] = T["spending"][a]["housing_support"]
        T["receipt"][a]["renter_contract_rent"] = rent
    extra = {"school_reprice": "school_operating", "college_rekey": "postsecondary", "lane_constants": "population",
             "state_price_public_order_safety": "use", "state_price_health_services": "health_other",
             "state_price_recreation_culture": "population"}
    line_keys = {lid: {a: T["spending"][a][k] for a in ALLOC} for lid, k in extra.items()}
    for lid in ("roads_vmt_sl", "roads_vmt_fed"):
        line_keys[lid] = {a: five for a in ALLOC}
    production = T["receipt"]["personal"]["wage"]

    if not all(g["passed"] for g in GATES):
        raise SystemExit(f"[BLOCKED] {sum(not g['passed'] for g in GATES)} gate(s) failed; nothing written")
    tolist = lambda x: [float(v) for v in x]  # noqa: E731
    out = {"meta": {"source": "added_age_mix_2026_10_07/g3_age_keys.py", "bands": BANDS, "pi": tolist(pi),
                    "population": float(pop.sum()), "convention": "a",
                    "line_keys_rule": {**extra, "roads_vmt_sl": "persons 5+", "roads_vmt_fed": "persons 5+"},
                    "production": "receipt wage key (personal)"},
           "keys": {s: {a: {k: tolist(v) for k, v in T[s][a].items()} for a in ALLOC} for s in T},
           "line_keys": {lid: {a: tolist(v) for a, v in x.items()} for lid, x in line_keys.items()},
           "production": tolist(production)}
    OUT.mkdir(exist_ok=True)
    (OUT / "g3_age_keys.json").write_text(json.dumps(out) + "\n")
    (OUT / "gates_keys.json").write_text(json.dumps({"gates": GATES}, indent=1) + "\n")
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2**30
    print(f"  wrote {sum(len(T[s][a]) for s in T for a in ALLOC)} key profiles, {len(line_keys)} line keys; peak RSS {peak:.2f} GiB")


if __name__ == "__main__":
    main()
