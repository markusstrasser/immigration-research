"""Ladder 263's white replacement with both sides on audit row 4's count, 39,712,493.

white_replacement_2026_09_28 prices the union on its rough keys at the published CPS weights and scales every white
slice to the engine meta's target_population, 40,896,574 (engine_lines.cjs:22, rekey_white.py:159,214). The state
version scales each region's white piece to that region's union persons on the same weights (state_white.py:141,148-149).
So both sides of every delta hold 40.90M people. Per-head lines are charged at the engine's corrected per-head share
on either side (rekey_white.py:202, pc_scale), so they cancel in the delta.

Here the lane's modules are imported read-only (their module-level builds read files and write nothing) and rerun on
the account's count: the CPS weights of audit row 4 (the engine's factors from combine_onbooks_lane.weight_arms), the
white slices scaled to 39,712,493, and the frame totals the keys divide by (key totals, CPS total, per-head scale,
the union's age structure, the white age factors) recomputed on the row-4 frame.

The accrual rows take each group's accrual per tax dollar from the white lane's derived/accrual_ratios.csv, except
the union's on row-4 weights, which white_accrual.py recomputes with the pension lane (the white group's ratios do
not move: row 4 reweights only Mexico-born people).

Gates (exit 1, nothing written): the published run reproduces the lane's rekey_summary.csv, accrual_beside.csv and
state_summary.csv (1e-3bn); white_accrual.py's published union ratios are the lane's (1e-6); recomputing the frame
totals on the published weights returns the module's own; the row-4 weights reproduce derived/frame_counts.csv's
row-4 union within 2 persons.

Writes derived/white_count.csv (figure, end, published_bn, row4_bn, move_bn, proportional_bn, published_per_member,
row4_per_member, note); proportional_bn is the published figure times 39,712,493 / 40,896,574.
Run from the repository root after frame_counts.py and white_accrual.py:
  OPENBLAS_NUM_THREADS=1 uv run --no-project --offline python3 infra/immigration-fiscal/population_basis_2026_09_29/white_count.py
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # read-only imports from other lanes: write nothing beside them

import ast  # noqa: E402
import csv  # noqa: E402
import importlib.util  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
WR = FISCAL / "white_replacement_2026_09_28"
OUT = HERE / "derived" / "white_count.csv"
FIELDS = ["figure", "end", "published_bn", "row4_bn", "move_bn", "proportional_bn", "published_per_member",
          "row4_per_member", "note"]
ENDS = ("low", "high")
FAILS: list[str] = []
sys.path.insert(0, str(FISCAL / "generation_account_2026_09_24"))
import frame as F  # noqa: E402  (puts the CPS lane on sys.path)
import combine_onbooks_lane as L  # noqa: E402


def gate(label, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'} {label}{' — ' + detail if detail else ''}", flush=True)
    if not ok:
        FAILS.append(label)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_csv(path):
    with path.open() as handle:
        return list(csv.DictReader(handle))


print("[white lane modules]", flush=True)
S = load("state_white", WR / "state_white.py")   # imports rekey_white (its module-level build) as S.R
R = S.R
ORIGINAL = {k: getattr(R, k) for k in ("KTOT", "CPS_TOTAL", "pc_scale", "NHW_POP", "NHW_CRIME", "NHW_OLD", "WUS_POP",
                                       "TARGET")}
ORIGINAL_PI = R.PI["union"].copy()
# accrual_white.py's constants, read without importing it (it imports the pension lane)
_tree = ast.parse((WR / "accrual_white.py").read_text())
_const = {t.targets[0].id: t.value for t in _tree.body if isinstance(t, ast.Assign) and isinstance(t.targets[0], ast.Name)}
STORED = {kw.arg: ast.literal_eval(kw.value) for kw in _const["STORED"].keywords}   # accrual_white.py:32,34-36
WHITE_REL_RATE = ast.literal_eval(_const["WHITE_REL_RATE"])
OASDI_PART = 0.124 / (0.124 + 0.029)   # accrual_white.py:143, statutory SE split


def set_weights(w, target):
    """The white lane's frame totals, recomputed on person weights w (rekey_white.py:121-122, 201-208)."""
    R.w = w
    R.KTOT = {k: float((w * v).sum()) for k, v in R.K.items()}
    R.CPS_TOTAL = float(w.sum())
    R.PI["union"] = R.structure(R.MASK["mex"], w, R.cage)
    R.pc_scale = R.eng_share["spending|general_public_services"] / (float(w[R.MASK["mex"]].sum()) / R.CPS_TOTAL)
    R.NHW_POP = float(w[R.MASK["wall"]].sum())
    R.NHW_CRIME = float((w * R.crime_c)[R.MASK["wall"]].sum())
    R.NHW_OLD = float((w * R.old_c)[R.MASK["wall"]].sum())
    R.WUS_POP = float(w[R.MASK["wus"]].sum())
    R.TARGET = target


def line_amounts(rows):
    """Low-end line amounts as accrual_white.py reads them: national_bn (4 decimals) x share (6 decimals)."""
    out = {}
    for side, lid, nat, amt, _ in rows:
        out[lid] = float(f"{nat:.4f}") * float(f"{amt / nat:.6f}") if abs(nat) > 1e-6 else 0.0
    return out


def accrual_delta(amt, ratio, rel, part_a_share, receipt_per_ben):
    """accrual_white.py:141-153: accrual minus cash for Social Security and Part A."""
    se = amt["self_employment_oasdi_hi"]
    oasdi_tax = amt["employee_oasdi"] + amt["employer_oasdi"] + OASDI_PART * se
    hi_tax = amt["employee_hi"] + amt["employer_hi"] + (1 - OASDI_PART) * se
    ss_cash, pa_cash = amt["social_security"], part_a_share * amt["medicare"]
    acc_net = float(ratio["oasdi_per_tax_dollar"]) * (1 - rel * float(ratio["benefit_tax_timing"])) * oasdi_tax
    receipt = receipt_per_ben * rel * ss_cash
    pa_acc = float(ratio["part_a_per_hi_tax_dollar"]) * hi_tax
    return (acc_net - ss_cash + receipt) + (pa_acc - pa_cash)


def evaluate(part_a_share, union_ratio):
    """Every figure of the comparison on the current weights: {(figure, end): (bn, persons)}. union_ratio: the union's
    payable accrual per tax dollar row for these weights."""
    out = {}
    scen = {"union rough": R.scenario("mex"), "A1": R.scenario("w3"), "A3": R.scenario("w3", "union")}
    runs = {(k, end): R.run(sc, end) for k, sc in scen.items() for end in ENDS}
    white_ratio = {(r["group"], r["scenario"]): r for r in read_csv(WR / "derived" / "accrual_ratios.csv")}[
        ("third_plus_nh_white", "payable")]
    receipt_per_ben = STORED["receipt_low"] / (STORED["ss_cash_low"] * STORED["rel_union"])
    d = {}
    for k, ratio, rel in (("union rough", union_ratio, STORED["rel_union"]), ("A1", white_ratio, WHITE_REL_RATE),
                          ("A3", white_ratio, WHITE_REL_RATE)):
        d[k] = accrual_delta(line_amounts(runs[(k, "low")][1]), ratio, rel, part_a_share, receipt_per_ben)
    n = R.TARGET
    for end in ENDS:
        cost = {k: runs[(k, end)][0]["cost"] for k in scen}
        for k in scen:
            out[(f"cost: {k}", end)] = (cost[k], n)
            out[(f"cost on accrual: {k}", end)] = (cost[k] + d[k], n)
        out[("delta: A1, cash, white ages", end)] = (cost["union rough"] - cost["A1"], n)
        out[("delta: A3, cash, union ages", end)] = (cost["union rough"] - cost["A3"], n)
        out[("delta: A1, accrual (payable)", end)] = (cost["union rough"] + d["union rough"] - cost["A1"] - d["A1"], n)
        out[("delta: A1 against the engine's union", end)] = (R.case[end]["cost_bn"] - cost["A1"], n)
    # state_white.main without its writes: the union by region against local third-plus whites at its ages
    rough = {end: R.run(R.scenario("mex"), end)[0] for end in ENDS}
    pieces = {name: S.union_piece(m) for name, m in S.REGIONS.items()}
    pieces["Los Angeles metro"] = S.union_piece(S.LA)
    for end in ENDS:
        u = {name: S.priced(sc, end, sc["frac"]) for name, sc in pieces.items()}
        resid = rough[end]["cost"] - sum(u[x][0] for x in S.REGIONS)
        out[("state residual", end)] = (resid, n)
        tot = 0.0
        for name, sc in pieces.items():
            pop = sc["population"]
            uc = u[name][0] + resid * sc["frac"]["pc"]
            wmask = S.REGIONS.get(name, S.LA) if name != "rest of US" else np.ones(len(R.d), bool)
            pi_union = R.structure(S.UNION & S.REGIONS.get(name, S.LA), R.w, R.cage)
            cu = S.priced(S.white_piece(wmask, pop, pi_union), end)[0]
            out[(f"delta: local whites, {name}", end)] = (uc - cu, pop)
            if name in S.REGIONS:
                tot += uc - cu
        out[("delta: local whites, sum of CA, TX and rest", end)] = (tot, n)
    return out


def main():
    # Positive controls: the published run reproduces the lane's outputs.
    print("[published weights]", flush=True)
    w_pub = R.w.copy()
    set_weights(w_pub, ORIGINAL["TARGET"])
    same = all(abs(getattr(R, k) - v) <= 1e-9 * abs(v) for k, v in ORIGINAL.items() if k != "KTOT") and all(
        abs(R.KTOT[k] - v) <= 1e-9 * abs(v) for k, v in ORIGINAL["KTOT"].items()) and np.allclose(R.PI["union"], ORIGINAL_PI)
    gate("frame totals recomputed on the published weights equal the module's own", same)
    beside = {(r["group"], r["scenario"], r["end"]): r for r in read_csv(WR / "derived" / "accrual_beside.csv")}
    rough_low = R.run(R.scenario("mex"), "low")[1]
    part_a_share = float(beside[("mexican_origin_rough", "payable", "low")]["part_a_cash_bn"]) / line_amounts(rough_low)["medicare"]
    lane_ratio = {(r["group"], r["scenario"]): r for r in read_csv(WR / "derived" / "accrual_ratios.csv")}
    mine = {(r["weights"], r["scenario"]): r for r in read_csv(HERE / "derived" / "white_accrual_ratios.csv")
            if r["group"] == "union"}
    for k in ("oasdi_per_tax_dollar", "benefit_tax_timing", "part_a_per_hi_tax_dollar"):
        gate(f"white_accrual.py's published union ratio is the lane's: {k}",
             abs(float(mine[("published", "payable")][k]) - float(lane_ratio[("union", "payable")][k])) < 1e-6)
    pub = evaluate(part_a_share, lane_ratio[("union", "payable")])
    summary = {(r["group"], r["end"]): r for r in read_csv(WR / "derived" / "rekey_summary.csv")}
    state = {(r["region"], r["end"]): r for r in read_csv(WR / "derived" / "state_summary.csv")}
    lab = {"union rough": "mexican_origin_rough", "A1": "A1_third_plus_nh_white", "A3": "A3_third_plus_nh_white_at_union_ages"}
    for end in ENDS:
        for k, g in lab.items():
            got, want = pub[(f"cost: {k}", end)][0], float(summary[(g, end)]["cost"])
            gate(f"rekey_summary cost reproduces: {k} {end}", abs(got - want) < 1e-3, f"{got:.4f} vs {want:.4f}")
            got, want = pub[(f"cost on accrual: {k}", end)][0], float(beside[(g, "payable", end)]["cost_accrual_bn"])
            gate(f"accrual_beside cost reproduces: {k} {end}", abs(got - want) < 1e-3, f"{got:.4f} vs {want:.4f}")
        for name in list(S.REGIONS) + ["Los Angeles metro", "sum of CA, TX and rest"]:
            got, want = pub[(f"delta: local whites, {name}", end)][0], float(state[(name, end)]["delta_union_ages_bn"])
            gate(f"state_summary delta reproduces: {name} {end}", abs(got - want) < 1e-3, f"{got:.4f} vs {want:.4f}")

    # Audit row 4's weights: the engine's factors applied to the white lane's CPS persons.
    print("[row 4 weights]", flush=True)
    d = F.load()
    civ, union, gens = F.masks(d)
    W = d[F.REPS[:2]].to_numpy(float)
    arms, info = L.weight_arms(d, W, L.acs_cells())
    n4_frame = float(arms["row4"][union, 0].sum())
    del arms, d, W
    counts = {r["count"]: r for r in read_csv(HERE / "derived" / "frame_counts.csv")}
    n_pub, n4 = float(counts["union|all"]["published"]), float(counts["union|all"]["row4"])
    gate("the engine's row-4 union reproduces frame_counts.csv", abs(n4_frame - n4) < 1e-3, f"{n4_frame:,.2f}")
    outside = R.d.PENATVTY.eq(303).to_numpy() & ~np.isin(S.st, L.CA_TX)
    w4 = w_pub.copy()
    w4[outside & R.d.PRCITSHP.eq(4).to_numpy()] *= info["factor_natz"]
    w4[outside & R.d.PRCITSHP.eq(5).to_numpy()] *= info["factor_noncit"]
    mex = R.MASK["mex"]
    removed_here, removed_frame = float(w_pub[mex].sum() - w4[mex].sum()), n_pub - n4
    gate("row 4 removes the same people from the white lane's union", abs(removed_here - removed_frame) < 2,
         f"{removed_here:,.1f} vs {removed_frame:,.1f}")
    gate("the white lane's row-4 union matches the account's count", abs(float(w4[mex].sum()) - n4) < 2,
         f"{float(w4[mex].sum()):,.1f} vs {n4:,.1f}")
    if FAILS:
        print(f"FAIL: {len(FAILS)} gate(s): {FAILS}")
        sys.exit(1)

    set_weights(w4, n4)
    row4 = evaluate(part_a_share, mine[("row4", "payable")])
    ratio = n4 / n_pub
    rows = []
    notes = {"delta: A1, accrual (payable)": "the union's accrual per tax dollar on row-4 weights (white_accrual.py)",
             "delta: A1 against the engine's union": "the engine's $321.8/387.4bn is on 39.71M already; only the white slice moves",
             "state residual": "rough union less its region pieces, spread by persons (the lane's gate: under $1bn)"}
    for (fig, end), (v, pop) in pub.items():
        v4, pop4 = row4[(fig, end)]
        rows.append(dict(figure=fig, end=end, published_bn=v, row4_bn=v4, move_bn=v4 - v, proportional_bn=v * ratio,
                         published_per_member=v * 1e9 / pop, row4_per_member=v4 * 1e9 / pop4, note=notes.get(fig, "")))
    OUT.parent.mkdir(exist_ok=True)
    fmt = lambda v: f"{v:.4f}" if isinstance(v, float) else v  # noqa: E731
    with OUT.open("w", newline="") as handle:
        out = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        out.writeheader()
        for r in rows:
            out.writerow({k: fmt(r[k]) for k in FIELDS})
    for r in rows:
        print(f"  {r['figure'][:46]:46s} {r['end']:4s} {r['published_bn']:9.3f} -> {r['row4_bn']:9.3f} "
              f"({r['move_bn']:+7.3f}; proportional {r['proportional_bn']:9.3f}) per member "
              f"{r['published_per_member']:8.0f} -> {r['row4_per_member']:8.0f}")
    print(f"  wrote {len(rows)} rows -> {OUT.relative_to(FISCAL)}")


if __name__ == "__main__":
    main()
