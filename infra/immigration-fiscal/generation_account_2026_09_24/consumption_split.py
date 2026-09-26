"""Step 4b: the consumption key's correction (ladder 225, adopted 2026-09-26) split exactly by generation.

The consumption lane (`consumption_key_2026_09_24`, spec `both_corridor_net_h2`, the one the September 26
package adopts) replaces each person's consumption key, positive SPM resources over unit size, by
    c(unit) * max(resources - M(unit), 0) / size
with c consumption per resource dollar at the unit's income rank (CE 2024) and M the unit's remittance
outflow calibrated to Banxico's corridor less H-2 pay. Its CPS frame is this lane's frame person for
person (gate), so each generation's own key totals are computed directly, with convention (a) or (b)
weights from frame.assignments: G0_g on the old key, GS_g with saving only, GB_g with saving and
remittances. Only the national totals N0 and NB are shared.

The lane's edit on a line of national total T (consumption_key.py main) is linear in these totals:
    edit = T * (SA - phi * S0),   SA = (phi * GS - (GS - GB)) / NB,   S0 = G0 / N0
with phi the September 24 payload's stack factor on the consumption lines. Per generation this is
    edit_g = phi * R_g - A_g,     R_g = T * (GS_g / NB - G0_g / N0),   A_g = T * (GS_g - GB_g) / NB:
R_g is the saving part, a ratio correction the lane scales by phi, and A_g the corridor's outflow,
fixed in dollars and not scaled. The selective-excise line keeps its $99.964bn federal part at CBO's
income-group shares: there R_g also carries F * (adj * fed_B,g - fed_0,g), where fed_g is CBO's
excise share of each income group times generation g's share of the key inside that group (the
lane's theta, split by generation) and adj = SA / (phi * S) the lane's corridor adjustment.
run_generations.cjs scales R_g by each generation's own stack factor (the lane's rule for every
ratio-type correction), with the union's phi as the existing sensitivity. The cells with no main-case
weight (remaining production property in its consumption scenario, spending cells on the resources
key) take the union's edit times the generation's share of the change in the adopted-basis key share,
(SA_g - phi * S0_g) / (SA - phi * S0), which is exact for cells split by that share.

Modules of the consumption lane and its outside-checks dependency are imported read-only: the
outside-checks lane's frame.py is loaded first under its own name, this lane's by path under another,
so the two modules called `frame` do not collide, and no bytecode is written beside them.
Gates (exit 1): the two frames hold the same persons, weights and generation masks; the old key
reproduces the stored 8.104% share; phi equals the payload's; each generation sum reproduces the
lane's union totals (1e-12 relative) and key shares (key_specs.csv, 1e-12); the union's edits rebuilt
from the totals reproduce payloads.json cell by cell (1e-9 bn); the generations' edits at the union's
phi add to them (1e-9 bn); the CBO federal shares add to the lane's (1e-12).
Output: derived/consumption_key_by_generation.json. Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with openpyxl python3 infra/immigration-fiscal/generation_account_2026_09_24/consumption_split.py
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
CKL = HERE.parent / "consumption_key_2026_09_24"
sys.path.insert(0, str(EXT))
import frame as xf  # noqa: E402,F401  (the outside-checks lane's frame; the consumption lane's outside.py binds to it)

sys.path.insert(0, str(CKL))
import consumption_key as ck  # noqa: E402  (the consumption lane's driver, imported for its definitions)
import cps_frame  # noqa: E402
import fetch  # noqa: E402
import outside  # noqa: E402
import remittance  # noqa: E402
import saving  # noqa: E402

_spec = importlib.util.spec_from_file_location("generation_frame", HERE / "frame.py")
F = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(F)

SPEC = "both_corridor_net_h2"   # main_case_2026_09_26/package.cjs CENTRAL.ck
REMIT = "corridor_net_h2"
ALLOCS = ["personal", "shared"]
FAILS = []


def gate(label, ok, detail=""):
    print(f"  {'✓' if ok else '✗'} {label}{' — ' + detail if detail else ''}", flush=True)
    if not ok:
        FAILS.append(label)


def fed_by_generation(k, a, g_cbo, target, om):
    """CBO's excise shares times each generation's share of the key inside the income group (rep 0)."""
    civ, w = a["civilian"], a["weights"][:, 0]
    out = np.zeros(om.shape[1])
    for j in xf.GROUPS:
        m = civ & (g_cbo == j)
        gj = k[m] @ w[m]
        if gj != 0:
            out += target[j] * ((k * w)[m] @ om[m]) / gj
    return out


def main():
    print("[frames]", flush=True)
    a = cps_frame.frame()
    d = F.load()
    civ, union, gens = F.masks(d)
    omega, _, _ = F.assignments(d, civ, union, gens)
    pos = pd.Series(np.arange(len(d)), index=pd.MultiIndex.from_frame(d[["PH_SEQ", "PPPOS"]]))
    idx = pos.reindex(pd.MultiIndex.from_arrays([a["ph_seq"], a["pppos"]])).to_numpy()
    one_to_one = len(idx) == len(d) and not np.isnan(idx.astype(float)).any() and len(set(idx.tolist())) == len(d)
    gate("the consumption lane's frame is this lane's, person for person (PH_SEQ, PPPOS)", one_to_one, f"{len(idx)} persons")
    if not one_to_one:
        sys.exit("✗ frames do not align")
    idx = idx.astype(int)
    same = (np.array_equal(d[F.REPS].to_numpy(float)[idx], a["weights"]) and np.array_equal(civ[idx], a["civilian"])
            and np.array_equal(union[idx], a["target"]) and np.array_equal(gens["G1"][idx], a["mexico_born"] & a["civilian"])
            and np.array_equal(gens["G2"][idx], a["second_gen"] & a["civilian"])
            and np.array_equal(gens["G3plus"][idx], a["third_plus"] & a["civilian"]))
    gate("same 161 weights, civilian universe, union and generation masks", same)
    om = {c: omega[c][idx] for c in ("a", "b")}

    print("[union: the consumption lane's own computation]", flush=True)
    g1 = cps_frame.reproduce(a)
    gate("the old key reproduces the stored share", g1["ok"], f"{g1['reproduced']:.15f}")
    fr = ck.Frame(a)
    state = ck.adopted_state()
    phi = state["phi"]
    payloads = json.loads((CKL / "derived/payloads.json").read_text())
    gate("phi equals the payload's", abs(phi - payloads["meta"]["phi"]) < 1e-12, f"{phi:.12f}")
    gate("the payload composes with the September 24 corrections",
         payloads["meta"]["composes_with"] == "main_case_2026_09_24/derived/corrections.json")
    pub = saving.published_deciles()
    pumd = saving.pumd_ranked()
    c = saving.unit_factor(a, saving.ce_curve("consumption", 50, pumd, pub, within=True), "ratio")
    un = remittance.units(a)
    rspecs, _ = remittance.spec_flows(a, un, remittance.sender_rates(), fetch.cpi_annual())
    sp = rspecs[REMIT]
    if not sp["absolute"]:
        sys.exit("✗ the corridor is not an absolute flow")
    ones = np.ones(int(a["n_units"]))
    G0, N0, k0 = fr.totals_fixed(ones)
    GS, NS, kS = fr.totals_fixed(c)
    GB, NB, kB = fr.totals_remit(c, sp, un, "proportional")
    G0, N0, GS, GB, NB = (float(x[0]) for x in (G0, N0, GS, GB, NB))
    S0, S = G0 / N0, GB / NB
    SA = (phi * GS - (GS - GB)) / NB
    SA0 = phi * S0
    adj = SA / (phi * S)
    specs = pd.read_csv(CKL / "derived/key_specs.csv").set_index("spec")
    for name, share in [("raw", S0), ("saving_central", GS / float(NS[0])), (SPEC, S)]:
        gate(f"key share {name} reproduces key_specs.csv", abs(share - specs.loc[name, "key_share"]) < 1e-12,
             f"{100 * share:.6f}%")
    gate(f"adopted-basis share {SPEC} reproduces key_specs.csv", abs(SA - specs.loc[SPEC, "adopted_basis_share"]) < 1e-12,
         f"{100 * SA:.6f}%")
    g_cbo, cbo = outside.cbo_groups_for(a)
    f0 = outside.cbo_federal_share(k0, a, g_cbo, cbo)
    fB = outside.cbo_federal_share(kB, a, g_cbo, cbo)
    stored = pd.read_csv(ck.CBO_TRANSLATION).query("spec == 'excise_taxes|2022' and allocation == 'personal'")
    gate("the old key's CBO federal share is the outside-checks lane's", abs(float(f0["share_at_cbo"][0])
         - float(stored.reweighted_share.iloc[0])) < 1e-12, f"{100 * float(f0['share_at_cbo'][0]):.6f}%")
    fed0, fedB = float(f0["share_at_cbo"][0]), float(fB["share_at_cbo"][0])
    Fx = ck.FEDERAL_EXCISE_BN

    # The union's edits rebuilt from the totals, against the payload.
    lines = state["lines"]
    union_edit = {}
    for lid, ln in lines.items():
        if lid == "excise_selective_sales":
            union_edit[lid] = SA * (ln["national"] - Fx) + phi * fedB * adj * Fx - ln["adopted"]
        else:
            union_edit[lid] = SA * ln["national"] - ln["adopted"]
    ratio = SA / SA0
    rpp_edit = {al: (ratio - 1) * state["rpp"][al] for al in ALLOCS}
    sp_edit = {lid: {al: (ratio - 1) * cell["adopted"][al] for al in ALLOCS} for lid, cell in state["spending"].items()}
    worst, cells = 0.0, 0
    for e in payloads["specs"][SPEC]["edits"]:
        if e["side"] == "receipt" and e["line"] in union_edit:
            want = {al: union_edit[e["line"]] for al in ALLOCS}
        elif e["side"] == "receipt" and e["line"] == ck.RPP and e["scenario"] == ck.RPP_SCENARIO:
            want = rpp_edit
        elif e["side"] == "spending" and e["key"] == "resources" and e["line"] in sp_edit:
            want = sp_edit[e["line"]]
        else:
            sys.exit(f"✗ unexpected payload cell {e}")
        worst = max(worst, *(abs(e["by"][al] - want[al]) for al in ALLOCS))
        cells += 1
    gate(f"the union's edits rebuilt from the totals reproduce payloads.json {SPEC} ({cells} cells)", worst < 1e-9,
         f"max |diff| {worst:.1e} bn")

    print("[generations]", flush=True)
    w0 = a["weights"][:, 0]
    out = {"meta": dict(
        source="generation_account_2026_09_24/consumption_split.py", spec=SPEC,
        payload="consumption_key_2026_09_24/derived/payloads.json",
        composes_with="main_case_2026_09_24/derived/corrections.json", adopted_in="main_case_2026_09_26/package.cjs",
        rule=("edit_g = phi_g * R_g - A_g on the four consumption lines (R the saving part, scaled by the generation's own "
              "stack factor in run_generations.cjs; A the corridor's outflow, fixed in dollars); the other cells take the "
              "union's edit times change_fraction"),
        phi=phi, federal_excise_bn=Fx, adj=adj, national_key={"old": N0, "saving": float(NS[0]), "both": NB},
        lines={lid: dict(national_bn=ln["national"], adopted_bn=ln["adopted"]) for lid, ln in lines.items()}),
        "union": dict(key_share={"old": S0, "saving": GS / float(NS[0]), "both": S}, adopted_basis_share={"old": SA0, "both": SA},
                      fed_share_cbo={"old": fed0, "both": fedB}, edit_bn=union_edit, rpp_edit_bn=rpp_edit, spending_edit_bn=sp_edit)}
    lines_order = list(lines)
    for conv in ("a", "b"):
        o = om[conv]
        g0, gs, gb = ((k * w0) @ o for k in (k0, kS, kB))
        tot_ok = all(abs(x.sum() / y - 1) < 1e-12 for x, y in ((g0, G0), (gs, GS), (gb, GB)))
        gate(f"({conv}) the generations' key totals add to the union's (old, saving, both)", tot_ok)
        fed0_g = fed_by_generation(k0, a, g_cbo, f0["cbo"], o)
        fedB_g = fed_by_generation(kB, a, g_cbo, fB["cbo"], o)
        gate(f"({conv}) the generations' CBO federal shares add to the lane's", abs(fed0_g.sum() - fed0) < 1e-12
             and abs(fedB_g.sum() - fedB) < 1e-12)
        R, A = {}, {}
        for lid in lines_order:
            T = lines[lid]["national"]
            if lid == "excise_selective_sales":
                R[lid] = (T - Fx) * (gs / NB - g0 / N0) + Fx * (adj * fedB_g - fed0_g)
                A[lid] = (T - Fx) * (gs - gb) / NB
            else:
                R[lid] = T * (gs / NB - g0 / N0)
                A[lid] = T * (gs - gb) / NB
        worst = max(abs(float((phi * R[lid] - A[lid]).sum()) - union_edit[lid]) for lid in lines_order)
        gate(f"({conv}) at the union's phi the generations' edits add to the union's on the four lines", worst < 1e-9,
             f"max |diff| {worst:.1e} bn")
        sa_g = (phi * gs - (gs - gb)) / NB
        frac = (sa_g - phi * g0 / N0) / (SA - SA0)
        gate(f"({conv}) the change fractions add to one", abs(frac.sum() - 1) < 1e-12)
        out[conv] = {}
        for j, g in enumerate(F.GENS):
            out[conv][g] = dict(
                R_bn={lid: float(R[lid][j]) for lid in lines_order}, A_bn={lid: float(A[lid][j]) for lid in lines_order},
                edit_at_union_phi_bn={lid: float(phi * R[lid][j] - A[lid][j]) for lid in lines_order},
                change_fraction=float(frac[j]), old_key_share=float(g0[j] / G0),
                key_share={"old": float(g0[j] / N0), "saving": float(gs[j] / NS[0]), "both": float(gb[j] / NB)},
                adopted_basis_share={"old": float(phi * g0[j] / N0), "both": float(sa_g[j])},
                fed_share_cbo={"old": float(fed0_g[j]), "both": float(fedB_g[j])},
                saving_part_at_union_phi_bn=float(sum(phi * R[lid][j] for lid in lines_order)),
                remittance_part_bn=float(-sum(A[lid][j] for lid in lines_order)))
        print(f"  ({conv}) receipts change at the union's phi, $bn: " + ", ".join(
            f"{g} {out[conv][g]['saving_part_at_union_phi_bn']:+.3f} saving {out[conv][g]['remittance_part_bn']:+.3f} remittances"
            for g in F.GENS), flush=True)
    (F.OUT / "consumption_key_by_generation.json").write_text(json.dumps(out, indent=1) + "\n")
    print(f"  union: key share {100 * S0:.3f}% -> {100 * S:.3f}% (adopted basis {100 * SA0:.3f}% -> {100 * SA:.3f}%); "
          f"receipts {sum(union_edit.values()):+.3f}bn", flush=True)
    if FAILS:
        print(f"✗ {len(FAILS)} gate(s) failed: {FAILS}")
        sys.exit(1)
    print("  ✓ all consumption-key gates passed")


if __name__ == "__main__":
    main()
