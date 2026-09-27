"""Step 4: three re-keys that act on the tax and transfer keys, split exactly by generation.

1. CBO's income gradients (`external_benchmarks_2026_09_24/cbo_arm.py`, the 2022 bundle without
   Medicaid that `package.cjs` cboShifts uses). The lane writes the union's share of a key as
   s = sum_j pi_j theta_j over CBO-style income groups j (pi_j the group's share of the national key,
   theta_j the union's share inside the group) and moves only the gradient: s' = sum_j pi'_j theta_j.
   theta_j is the sum of the generations' own shares inside the group, so each generation's change is
   national x (pool fraction) x sum_j (pi'_j - pi_j) theta_jg: the brief's "by each generation's
   income position", exact.
2. Treasury OTA's EITC and child-credit shares (`ota_arm.py`, vs_audit_package_ssn_rule): the union's
   EITC and child-credit dollars inside the refundable key, after the SSN rule, are scaled by OTA's
   Hispanic share over the CPS's. A generation's change is the same ratios on its own dollars.
3. Audit row 1 (`dataset_integrity_2026_09_23/spending_credit_keys.py`, spending_mts_credits.json):
   premium tax credits, keyed by EITC+ACTC in the account, re-keyed by subsidized Marketplace persons
   (MRKS = 1). The change is PTC x pool fraction x (s_mrks - s_credits); a generation's part is its own
   s_mrks,g - s_credits,g. The package books the personal-key figure (-$14.23bn) at both allocations;
   each allocation's figure is split by that allocation's own credit key.

Generations enter as weights (F.assignments): convention (a) own generation; (b) minors in the
parents' generation, half to each when the parents' generations differ. The CBO lane's modules are
imported read-only; its frame.py is loaded first and this lane's by path under another name, so the
two modules called `frame` do not collide.
Gates (exit 1): the union's changes reproduce cbo_deltas.json all_but_medicaid|2022 and ota_deltas.json
vs_audit_package_ssn_rule (1e-9 bn) and the row-1 figure (to its 0.01 rounding); under each
convention the three generations add to the union (1e-12 bn, or exactly by construction for row 1).
Output: derived/external_by_generation.json. Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with openpyxl python3 infra/immigration-fiscal/generation_account_2026_09_24/external_split.py
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # read-only imports from other lanes: write nothing beside them

import importlib.util  # noqa: E402
import json  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

HERE = Path(__file__).resolve().parent
EXT = HERE.parent / "external_benchmarks_2026_09_24"
sys.path.insert(0, str(EXT))
import frame as xf  # noqa: E402  (the CBO lane's frame; cbo_arm and ota_arm bind to it)
import cbo_arm  # noqa: E402
import ota_arm  # noqa: E402

_spec = importlib.util.spec_from_file_location("generation_frame", HERE / "frame.py")
F = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(F)

YEAR = 2022
BUNDLE = f"all_but_medicaid|{YEAR}"
CENTRAL = {"individual_inc_tax": "individual_inc_tax_gross"}  # cbo_arm.main's central definitions
BUNDLE_CONCEPTS = ["individual_inc_tax", "payroll_taxes", "excise_taxes", "snap", "ssi", "other_transfers",
                   "social_security", "medicare"]
MTS = F.FISCAL / "dataset_integrity_2026_09_23/derived/spending_mts_credits.json"
PROBE_HF = 0.9900527  # spending_credit_keys.py's pool fraction
FAILS = []


def gate(label, ok, detail=""):
    print(f"  {'✓' if ok else '✗'} {label}{' — ' + detail if detail else ''}", flush=True)
    if not ok:
        FAILS.append(label)


def theta(v, w, civ, om, groups):
    """Generation weights' share of the key inside each income group (cbo_arm.decompose's theta)."""
    out = {}
    for j in xf.GROUPS:
        m = civ & (groups == j)
        gj = v[m] @ w[m]
        out[j] = ((v * om)[m] @ w[m]) / gj if gj != 0 else 0.0
    return out


def main():
    d = xf.load()
    civ, target = xf.masks(d)
    w = d.pwwgt0.to_numpy(float)
    hf = xf.household_fraction(d, civ)
    gd = F.load()
    gciv, gunion, gens = F.masks(gd)
    omega, _, _ = F.assignments(gd, gciv, gunion, gens)
    cols = {f"{conv}{j}": omega[conv][:, j] for conv in omega for j in range(len(F.GENS))}
    m = d[["PH_SEQ", "PPPOS"]].merge(gd[["PH_SEQ", "PPPOS"]].assign(**cols), on=["PH_SEQ", "PPPOS"], how="left",
                                     validate="one_to_one")
    om = {conv: {g: m[f"{conv}{j}"].fillna(0.0).to_numpy(float) for j, g in enumerate(F.GENS)} for conv in omega}
    for conv in om:
        total = sum(om[conv].values())
        gate(f"({conv}) generation weights partition the CBO lane's union",
             np.allclose(total[target], 1) and not total[~target].any())
    out = {"cbo": {}, "ota": {}, "row1": {}}

    # 1. CBO.
    g, _ = cbo_arm.groups(d)
    model = xf.model()
    lines = {x["id"]: x for x in model["receipts"]["lines"]}
    lines.update({x["id"]: x for x in model["spending"]["lines"]})
    rk, sk = xf.receipt_keys(d), xf.spending_keys(d)
    vec = {side: {a: (rk if side == "receipts" else sk)[a] for a in ["personal", "shared"]}
           for side in ["receipts", "spending"]}
    cbo = cbo_arm.cbo_shares(YEAR)
    stored = json.loads((EXT / "derived/cbo_deltas.json").read_text())[BUNDLE]
    worst_u, worst_sum = 0.0, 0.0
    for concept in BUNDLE_CONCEPTS:
        members = cbo_arm.CONCEPTS[concept]
        variant = CENTRAL.get(concept, concept)
        pis = {lid: cbo_arm.decompose(vec[side]["personal"][key], w, civ, target, g)[0]
               for (lid, key, side, part) in members}
        amounts = {lid: cbo_arm.national_amount(lines[lid], part) for (lid, key, side, part) in members}
        comp = {j: sum(amounts[x] * pis[x][j] for x in pis) / sum(amounts.values()) for j in xf.GROUPS}
        target_cbo = cbo_arm.cbo_detail(cbo, variant, comp["negative"])
        for (lid, key, side, part) in members:
            if lid not in cbo_arm.IN_MAIN_CASE:
                continue
            amount = cbo_arm.national_amount(lines[lid], part)
            scale = hf if side == "spending" else 1.0
            pi_point = pis[lid]
            pi_new = target_cbo if len(members) == 1 else cbo_arm.ratio_target(pi_point, comp, target_cbo)
            cell = out["cbo"].setdefault(lid, dict(side=side, key=key, concept=concept, union={}, a={}, b={}))
            for a in ["personal", "shared"]:
                v = vec[side][a][key]
                pi_r, th_r = cbo_arm.decompose(v, w, civ, target, g)
                new = {j: target_cbo[j] if len(members) == 1 else
                       (pi_new[j] / pi_point[j] * pi_r[j] if pi_point[j] else 0.0) for j in xf.GROUPS}
                union = float(amount * scale * sum((new[j] - pi_r[j]) * th_r[j] for j in xf.GROUPS))
                ref = stored["receipts"][lid][a] if side == "receipts" else stored["spending"][lid][key][a]
                worst_u = max(worst_u, abs(union - ref))
                cell["union"][a] = union
                for conv in om:
                    for gen in F.GENS:
                        th_g = theta(v, w, civ, om[conv][gen], g)
                        cell[conv].setdefault(gen, {})[a] = float(amount * scale * sum((new[j] - pi_r[j]) * th_g[j]
                                                                                       for j in xf.GROUPS))
                    worst_sum = max(worst_sum, abs(sum(cell[conv][x][a] for x in F.GENS) - union))
    gate(f"CBO: union changes reproduce cbo_deltas.json {BUNDLE}", worst_u < 1e-9, f"max |diff| {worst_u:.1e} bn")
    gate("CBO: the three generations add to the union under both conventions", worst_sum < 1e-12, f"{worst_sum:.1e} bn")
    missing = [x for x in list(stored["receipts"]) + list(stored["spending"]) if x not in out["cbo"]]
    gate("CBO: every line of the bundle is split", not missing, str(missing) if missing else "")

    # 2. OTA (ota_arm.main, spec vs_audit_package_ssn_rule).
    ratios = pd.read_csv(EXT / "derived/ota_shares.csv").set_index("item").ratio_ota_to_cps
    r_e, r_c = ratios["eitc_ssn_rule"], ratios["ctc_on_books_central"]
    un, latin = xf.status(d)
    unauth = un & latin
    eitc = np.where(unauth, 0.0, d.EIT_CRED.to_numpy(float))
    actc = np.where(unauth, d.ACTC_CRD.to_numpy(float) * ota_arm.ON_BOOKS["central"], d.ACTC_CRD.to_numpy(float))
    ids = d.SPM_ID.to_numpy()
    ota_stored = json.loads((EXT / "derived/ota_deltas.json").read_text())["vs_audit_package_ssn_rule"]
    ota_stored = ota_stored["spending"]["refundable_tax_credits"]["refundable_credits"]
    cell = out["ota"] = dict(line="refundable_tax_credits", key="refundable_credits", union={}, a={}, b={},
                             ratios=dict(eitc=r_e, ctc=r_c))
    worst_u, worst_sum = 0.0, 0.0
    for a in ["personal", "shared"]:
        e_v, c_v = (eitc, actc) if a == "personal" else (xf.unit_equal(eitc, ids), xf.unit_equal(actc, ids))
        total = (e_v + c_v)[civ] @ w[civ]

        def change(weight):
            return float(ota_arm.NON_PTC_BN * hf * ((r_e - 1) * ((e_v * weight)[civ] @ w[civ])
                                                    + (r_c - 1) * ((c_v * weight)[civ] @ w[civ])) / total)
        cell["union"][a] = change(target.astype(float))
        worst_u = max(worst_u, abs(cell["union"][a] - ota_stored[a]))
        for conv in om:
            for gen in F.GENS:
                cell[conv].setdefault(gen, {})[a] = change(om[conv][gen])
            worst_sum = max(worst_sum, abs(sum(cell[conv][x][a] for x in F.GENS) - cell["union"][a]))
    gate("OTA: union change reproduces ota_deltas.json vs_audit_package_ssn_rule", worst_u < 1e-9, f"{worst_u:.1e} bn")
    gate("OTA: the three generations add to the union under both conventions", worst_sum < 1e-12, f"{worst_sum:.1e} bn")

    # 3. Audit row 1: premium credits re-keyed by subsidized Marketplace persons.
    mts = json.loads(MTS.read_text())
    ptc = mts["lines"]["ptc"]["cy2024_bn"]
    booked = mts["ptc_effect_on_main_case_bn"]
    mrks = d.MRKS.eq(1).to_numpy(float)
    credits = {"personal": d.EIT_CRED.to_numpy(float) + d.ACTC_CRD.to_numpy(float)}
    credits["shared"] = xf.unit_equal(credits["personal"], ids)

    def share(v, weight):
        return float(((v * weight)[civ] @ w[civ]) / (v[civ] @ w[civ]))
    rebuilt = ptc * PROBE_HF * (share(mrks, target.astype(float)) - share(credits["personal"], target.astype(float)))
    gate("row 1: PTC x pool fraction x (Marketplace share - credit share) reproduces the booked figure",
         abs(rebuilt - booked) < 0.006, f"{rebuilt:.4f} vs {booked}")
    cell = out["row1"] = dict(line="refundable_tax_credits", key="refundable_credits", booked_bn=booked, ptc_bn=ptc,
                              union={}, a={}, b={}, weights={"a": {}, "b": {}})
    for a in ["personal", "shared"]:
        gap_u = share(mrks, target.astype(float)) - share(credits[a], target.astype(float))
        cell["union"][a] = booked
        for conv in om:
            for gen in F.GENS:
                wt = (share(mrks, om[conv][gen]) - share(credits[a], om[conv][gen])) / gap_u
                cell["weights"][conv].setdefault(gen, {})[a] = wt
                cell[conv].setdefault(gen, {})[a] = booked * wt
            ok = abs(sum(cell[conv][x][a] for x in F.GENS) - booked) < 1e-12
            gate(f"row 1 ({conv}, {a}): the three generations add to the booked figure", ok)
    out["meta"] = dict(source="external_benchmarks_2026_09_24 (cbo_arm.py, ota_arm.py); dataset_integrity_2026_09_23 "
                       "(spending_credit_keys.py, spending_mts_credits.json)", bundle=BUNDLE, household_fraction=hf,
                       layout="section -> union / a / b -> generation -> allocation, $bn of the group's target")
    (F.OUT / "external_by_generation.json").write_text(json.dumps(out, sort_keys=True, indent=1) + "\n")
    for lid, c in out["cbo"].items():
        print(f"  CBO {lid:30s} personal (a): union {c['union']['personal']:+.3f}; "
              + "; ".join(f"{x} {c['a'][x]['personal']:+.3f}" for x in F.GENS), flush=True)
    for name in ("ota", "row1"):
        c = out[name]
        for conv in ("a", "b"):
            print(f"  {name} ({conv}) personal: union {c['union']['personal']:+.3f}; "
                  + "; ".join(f"{x} {c[conv][x]['personal']:+.3f}" for x in F.GENS), flush=True)
    if FAILS:
        print(f"✗ {len(FAILS)} gate(s) failed: {FAILS}")
        sys.exit(1)
    print("  ✓ all external-check gates passed")


if __name__ == "__main__":
    main()
