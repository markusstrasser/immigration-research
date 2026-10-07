#!/usr/bin/env python3
"""Round 2's income-tax move in its parts, from the CPS-dollar rule to the case's keys (the team lead's request of
2026-10-07), through this lane's library (rekey_sept29.py) at oct05 or oct07.

Each step changes one line's key; the cost is linear in the three income-tax lines (response 1, the accrual basis
subtracting a fixed tax on benefits), so the parts add up and do not depend on their order:
    cps         the CPS-dollar rule: each group charged the income tax it reports (rough keys: FEDTAX_AC split over the
                tax unit and floored at 0, `fit`; STATETAX_A the same way, `sit`; other personal tax on `fit`), the
                top tail the survey misses charged to no one
    (a)         the top tail spread in proportion to the same keys, line by line (federal, state, other personal);
                after (a) a group is at the cost_top_tail_proportional arm
    (b1)        federal: FEDTAX_AC -> FEDTAX_BC on the same tax-unit split. FEDTAX_AC is FEDTAX_BC less EIT_CRED and
                ACTC_CRD (CPS ASEC 2025 data dictionary), and the national line, NIPA table 3.4 line 3, records
                federal income tax before refundable credits: since BEA's 2015 annual revision the full value of
                refundable credits is a social benefit (the refundable_tax_credits line), "and estimates of personal
                current taxes paid to the federal government will be revised up by an equal amount to reflect the
                total tax liability of taxpayers" (McCulla and Smith, Survey of Current Business, June 2015). The
                rough key took the credits that offset liability out of a group's receipt key while the spending
                line charged them to it (45% of it keyed on EITC + ACTC): a double count, which (b1) ends
    (b2)        federal, then state: the tax-unit split -> the SPM unit's (the case's shared allocation), each key's
                concept unchanged (FEDTAX_BC; STATETAX_A floored at 0)
    (b3)        other personal tax: the federal key -> the state-liability key, as the case keys it
    (c)         federal: the IRS TY2023 and CBO 2022 raking on FEDTAX_BC (v4 item 3's key): the central
The figures: the rough union (the lineage on oct05/oct07), A1, A3 and the all-residents slice, each gap (union less
the slice), and Part F state by state (the union's pieces, the white pieces at the pieces' ages, the gap; per region
and summed), on both bases and ends. bins_<case> gives, per figure's slice, what the steps act on: its CPS dollars on
each key, the credits that offset its liability (FEDTAX_BC less FEDTAX_AC floored, on the tax-unit split: what the
CPS-dollar rule double counted, in CPS dollars), its shared FEDTAX_BC dollars in the top AGI bins, and its share of
each key.

Gates (exit 1, nothing written): the library's setup; FEDTAX_BC = FEDTAX_AC + EIT_CRED + ACTC_CRD on every record
(exact); the benchmark frame is the rough frame row for row; the SPM-unit split of FEDTAX_BC is the library's shared
federal_liability vector, and on the published weights the union's share is model.json's cell (1e-9); the national
raked vector is the library's; the cps, prop and central steps are run29's own 'cps', 'prop' and central runs (1e-9)
and rekey_summary_<case>.csv's cost_cps, cost_top_tail_proportional and cost (5e-5); the central state rows are
state_summary_<case>.csv's (5e-5); each part is minus the three lines' move times their responses (1e-9); Part F: each
white piece's share of the federal key is its records' sum of the one national raked vector over the frame's total
(1e-12), with its weights summing to its persons (1e-9 relative), so no state is raked or scaled on its own; the AGI
bins split each record's FEDTAX_BC as the raking does (their sum is the shared key, 1e-6).
Outputs: derived/income_tax_parts_<case>.csv, derived/income_tax_bins_<case>.csv. Run from the repository root after
rekey_sept29.py --case <case>:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/white_replacement_2026_09_28/income_tax_parts.py --case oct07
"""
from __future__ import annotations

import argparse
import contextlib
import csv
import importlib.util
import io
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True   # read-only imports: write nothing beside them

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

LANE = Path(__file__).resolve().parent
DER = LANE / "derived"
sys.path.insert(0, str(LANE))
import rekey_sept29 as W  # noqa: E402

R, S = W.R, W.S
FAILS: list[str] = []
LINES = ("federal_income_tax", "state_local_income_tax", "other_personal_tax")
# The steps, cumulative: (part, the line it moves, every line's key after it). 'cps' is the CPS-dollar rule.
STEPS = [("cps", None, {"federal_income_tax": "cps", "state_local_income_tax": "cps", "other_personal_tax": "cps"})]
for part, lid, key in (("a_federal", "federal_income_tax", "fit"), ("a_state", "state_local_income_tax", "sit"),
                       ("a_other", "other_personal_tax", "fit"),
                       ("b1_federal_credits", "federal_income_tax", "fit_bc_tu"),
                       ("b2_federal_unit", "federal_income_tax", "fit_bc_spm"),
                       ("b2_state_unit", "state_local_income_tax", "sit_case"),
                       ("b3_other_key", "other_personal_tax", "sit_case"),
                       ("c_federal_raking", "federal_income_tax", "fit_case")):
    STEPS.append((part, lid, {**STEPS[-1][2], lid: key}))
PARTS = [p for p, _, _ in STEPS[1:]]
PROP_STEP = "a_other"     # after (a) every line is on its rough key in proportion: the cost_top_tail_proportional arm
MODES = None              # the step's keys while a step runs; None: the library's own rule
BASE_SHARE = R.line_share


def gate(label, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'} {label}{' — ' + detail if detail else ''}", flush=True)
    if not ok:
        FAILS.append(label)


def parts_line_share(sc, side, lid, top="cps"):
    """The library's line_share, with the three income-tax lines on the running step's keys."""
    if MODES is not None and side == "receipts" and lid in MODES:
        k = MODES[lid]
        if k == "cps":
            key, nat = R.TOP_TAIL[lid]
            return sc["cps_bn"][key] / R.NATIONAL[nat]
        return sc["share"][k]
    return BASE_SHARE(sc, side, lid, top)


@contextlib.contextmanager
def step_keys(keys):
    global MODES
    MODES = keys
    try:
        yield
    finally:
        MODES = None


def benchmark_frame():
    """The benchmark lane's frame (the library's source of FEDTAX_BC and AGI), gated to the rough frame's rows."""
    spec = importlib.util.spec_from_file_location("benchmark_frame", W.BENCH / "frame.py")
    bf = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bf)
    d = pd.read_parquet(bf.CACHE / "cps25_frame.parquet", columns=W.TAX_COLS)
    gate("the benchmark frame is the rough frame row for row (household, tax and SPM unit, FEDTAX_AC)",
         len(d) == len(R.d) and all(np.array_equal(d[c].to_numpy(), R.d[c].to_numpy())
                                    for c in ("PH_SEQ", "TAX_ID", "SPM_ID", "FEDTAX_AC", "STATETAX_A")))
    return bf, d


def add_keys(bf, d):
    """The steps' new keys on the rough frame's rows, added to the frame's keys and totals."""
    bc = W.TAX_K["_fedtax_bc"]
    gate("FEDTAX_BC = FEDTAX_AC + EIT_CRED + ACTC_CRD on every record (exact)",
         np.array_equal(bc, (R.d.FEDTAX_AC + R.d.EIT_CRED + R.d.ACTC_CRD).to_numpy(float)) and (bc >= 0).all())
    R.K["fit_bc_tu"] = np.maximum(R.split(bc, ["PH_SEQ", "TAX_ID"]), 0)
    R.K["fit_bc_spm"] = bf.unit_equal(bc, R.d.SPM_ID.to_numpy())
    gate("the national raked vector is the library's shared federal key", np.array_equal(R.K["fit_case"], W.TAX_K["fit_case_shared"]))
    civ, union = bf.masks(d)
    w0 = d.pwwgt0.to_numpy(float) * civ
    want = next(x for x in bf.model()["receipts"]["lines"] if x["id"] == "federal_income_tax")["cells"]["cbo_collective"]["shared"]["share"]
    got = float(w0[union] @ R.K["fit_bc_spm"][union] / (w0 @ R.K["fit_bc_spm"]))
    gate("the SPM-unit split of FEDTAX_BC gives the union model.json's federal_liability cell on the published weights (1e-9)",
         abs(got - want) < 1e-9, f"{got:.9f} vs {want:.9f}")
    for k in ("fit_bc_tu", "fit_bc_spm"):
        R.KTOT[k] = float((R.w * R.K[k]).sum())
    W.UNION_SC = R.scenario("mex")     # rebuilt with the new keys' shares


def agi_bins(d, bc):
    """Each person's shared FEDTAX_BC dollars by IRS AGI bin, as raked_vector bins them, and the bins' lower bounds."""
    labels, _ = W.irs_2023()
    lows = [int(re.match(r"\$([\d,]+) (?:under|or more)", lab).group(1).replace(",", "")) for lab in labels[1:]]
    edges = np.array(lows[1:], float)
    agi = d.AGI.to_numpy(float)
    b = np.where(agi <= 0, 0, np.searchsorted(edges, agi, side="right") + 1)
    codes, _ = pd.factorize(d.SPM_ID.to_numpy())
    size = np.bincount(codes).astype(float)
    m = np.zeros((len(d), 19))
    for k in range(19):
        m[:, k] = (np.bincount(codes, weights=bc * (b == k)) / size)[codes]
    gate("the AGI bins split each record's FEDTAX_BC as the raking does: their sum is the shared key (1e-6)",
         float(np.abs(m.sum(axis=1) - R.K["fit_bc_spm"]).max()) < 1e-6)
    return m, np.array([0.0] + lows, float)


def run_steps(scen):
    """Every figure's cost after each step, both bases and ends; the state rows' figures too."""
    cost, lines, state = {}, {}, {}
    for part, _, keys in STEPS:
        with step_keys(keys):
            for b in W.BASES:
                for end in W.ENDS:
                    for lab, sc in scen.items():
                        r, rows = W.run29(sc, end, b)[:2]
                        cost[(part, b, end, lab)] = r["cost"]
                        lines[(part, b, end, lab)] = {x[1]: x[3] * x[4] for x in rows if x[0] == "receipts" and x[1] in LINES}
                for b in W.BASES:
                    st, _ = W.state_rows(b)
                    for x in st:
                        state[(part, b, x["end"], x["region"])] = x
    return cost, lines, state


def gates_steps(scen, cost, lines, state):
    summary = pd.read_csv(DER / f"rekey_summary_{W.CASE}.csv")
    stsum = pd.read_csv(DER / f"state_summary_{W.CASE}.csv")
    linear = 0
    for b in W.BASES:
        for end in W.ENDS:
            for lab, sc in scen.items():
                own = {"cps": W.run29(sc, end, b, "cps")[0]["cost"], PROP_STEP: W.run29(sc, end, b, "prop")[0]["cost"],
                       "c_federal_raking": W.run29(sc, end, b)[0]["cost"]}
                row = summary.query("basis == @b and group == @lab and end == @end").iloc[0]
                files = {"cps": row.cost_cps, PROP_STEP: row.cost_top_tail_proportional, "c_federal_raking": row.cost}
                for part, col in (("cps", "cost_cps"), (PROP_STEP, "cost_top_tail_proportional"), ("c_federal_raking", "cost")):
                    got = cost[(part, b, end, lab)]
                    gate(f"{lab} {b} {end}: step {part} is run29's own run (1e-9) and rekey_summary's {col} (5e-5)",
                         abs(got - own[part]) < 1e-9 and abs(got - files[part]) < 5e-5, f"{got:.6f}")
                for i in range(1, len(STEPS)):
                    p0, p1 = STEPS[i - 1][0], STEPS[i][0]
                    move = sum(lines[(p1, b, end, lab)][x] - lines[(p0, b, end, lab)][x] for x in LINES)
                    d = cost[(p1, b, end, lab)] - cost[(p0, b, end, lab)]
                    linear += 1
                    if abs(d + move) >= 1e-9:
                        gate(f"{lab} {b} {end}: part {p1} is minus the three lines' move (1e-9)", False, f"{d:+.9f} vs {-move:+.9f}")
                        linear -= 1
            for x in stsum.query("basis == @b and end == @end").itertuples():
                got = state[("c_federal_raking", b, end, x.region)]
                gate(f"state {x.region} {b} {end}: the central's rows are state_summary's (5e-5)",
                     all(abs(float(got[c]) - getattr(x, c)) < 5e-5 for c in ("cost_union_bn", "cost_white_union_ages_bn",
                                                                              "delta_union_ages_bn")))
    n = len(W.BASES) * len(W.ENDS) * len(scen) * len(PARTS)
    gate(f"every part is minus its lines' move (1e-9; {linear} of {n})", linear == n)


def capture_pieces():
    """Part F's white pieces at the union pieces' ages, as state_rows builds them on the central (one accrual pass)."""
    got = []
    real = S.white_piece

    def spy(mask, total, target_pi):
        sc = real(mask, total, target_pi)
        if target_pi is not None:
            got.append((mask, sc))
        return sc

    S.white_piece = spy
    try:
        W.state_rows("accrual")
    finally:
        S.white_piece = real
    pieces = {}
    for name in S.REGIONS:
        m = np.ones(len(R.d), bool) if name == "rest of US" else S.REGIONS[name]
        pieces[name] = next(sc for mask, sc in got if np.array_equal(mask, m))
    return pieces


def gates_pieces(pieces, scen):
    v = R.K["fit_case"]
    for name, sc in {**pieces, "A1_third_plus_nh_white": scen["A1_third_plus_nh_white"]}.items():
        cw = sc["cps_w"]
        share = float(cw @ v) / float(R.w @ v)
        gate(f"{name}: its federal key share is its records' sum of the one national raked vector over the frame's "
             f"total (1e-12), and its weights sum to its persons (1e-9 rel.)",
             abs(sc["share"]["fit_case"] - share) <= 1e-12 * share and abs(float(cw.sum()) - sc["population"]) <= 1e-9 * sc["population"],
             f"{share:.9f}, {sc['population']:,.0f} persons")


def bins_rows(scen, pieces, m, lows):
    out = []
    slices = {"mexican_origin_rough": scen["mexican_origin_rough"], "A1_third_plus_nh_white": scen["A1_third_plus_nh_white"],
              "A3_third_plus_nh_white_at_union_ages": scen["A3_third_plus_nh_white_at_union_ages"],
              "all_residents_slice": scen["all_residents_slice"],
              **{f"Part F whites at union ages: {n}": sc for n, sc in pieces.items()}}
    local = {"name": "sum", "cps_w": sum(sc["cps_w"] for sc in pieces.values()),
             "population": sum(sc["population"] for sc in pieces.values())}
    local["share"] = {k: float((local["cps_w"] * R.K[k]).sum() / R.KTOT[k]) for k in ("fit", "fit_bc_tu", "fit_bc_spm", "fit_case")}
    slices["Part F whites at union ages: sum of CA, TX and rest"] = local
    for lab, sc in slices.items():
        cw, pop = sc["cps_w"], sc["population"]
        by_bin = cw @ m
        tot = float(by_bin.sum())
        sh = sc["share"]
        out.append({"case": W.CASE, "slice": lab, "persons": f"{pop:.0f}",
                    "cps_fedtax_ac_tu_bn": f"{float(cw @ R.K['fit']) / 1e9:.4f}",
                    "cps_fedtax_bc_tu_bn": f"{float(cw @ R.K['fit_bc_tu']) / 1e9:.4f}",
                    "cps_offset_credits_bn": f"{float(cw @ (R.K['fit_bc_tu'] - R.K['fit'])) / 1e9:.4f}",
                    "cps_eitc_actc_bn": f"{float(cw @ R.K['ref']) / 1e9:.4f}",
                    "cps_fedtax_bc_spm_bn": f"{tot / 1e9:.4f}",
                    "bc_share_agi_200k_plus": f"{float(by_bin[lows >= 200_000].sum()) / tot:.6f}",
                    "bc_share_agi_500k_plus": f"{float(by_bin[lows >= 500_000].sum()) / tot:.6f}",
                    "bc_share_agi_1m_plus": f"{float(by_bin[lows >= 1_000_000].sum()) / tot:.6f}",
                    "share_fit": f"{sh['fit']:.9f}", "share_fit_bc_tu": f"{sh['fit_bc_tu']:.9f}",
                    "share_fit_bc_spm": f"{sh['fit_bc_spm']:.9f}", "share_fit_case": f"{sh['fit_case']:.9f}",
                    "raking_factor": f"{sh['fit_case'] / sh['fit_bc_spm']:.6f}"})
    return out


def parts_rows(scen, cost, state):
    out = []

    def add(b, end, figure, series):
        row = {"case": W.CASE, "basis": b, "end": end, "figure": figure, "cps_bn": f"{series[0]:.4f}"}
        for i, part in enumerate(PARTS, start=1):
            row[f"{part}_bn"] = f"{series[i] - series[i - 1]:.4f}"
        row["prop_bn"] = f"{series[PARTS.index(PROP_STEP) + 1]:.4f}"
        row["central_bn"] = f"{series[-1]:.4f}"
        out.append(row)

    steps = [p for p, _, _ in STEPS]
    union = "mexican_origin_rough"
    for b in W.BASES:
        for end in W.ENDS:
            add(b, end, "union (rough)", [cost[(p, b, end, union)] for p in steps])
            for lab in ("A1_third_plus_nh_white", "A3_third_plus_nh_white_at_union_ages", "all_residents_slice"):
                add(b, end, lab, [cost[(p, b, end, lab)] for p in steps])
                add(b, end, f"gap: union less {lab}", [cost[(p, b, end, union)] - cost[(p, b, end, lab)] for p in steps])
            for region in (*S.REGIONS, "sum of CA, TX and rest"):
                st = [state[(p, b, end, region)] for p in steps]
                add(b, end, f"Part F union pieces: {region}", [float(x["cost_union_bn"]) for x in st])
                add(b, end, f"Part F whites at union ages: {region}", [float(x["cost_white_union_ages_bn"]) for x in st])
                add(b, end, f"Part F gap: {region}", [float(x["delta_union_ages_bn"]) for x in st])
    return out


def write(name, rows):
    with open(DER / name, "w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        wr.writeheader()
        wr.writerows(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", choices=W.TAX_CASES, required=True)
    case = ap.parse_args().case
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        W.use_case(case)
        W.setup()
    fails = [ln for ln in buf.getvalue().splitlines() if "FAIL" in ln]
    if fails or W.FAILS:
        print(buf.getvalue())
        raise SystemExit(f"[BLOCKED] the library's {case} setup failed: {fails[:3]}")
    print(f"the library's {case} setup: {buf.getvalue().count('PASS')} gates passed")
    R.line_share = parts_line_share
    bf, d = benchmark_frame()
    add_keys(bf, d)
    m, lows = agi_bins(d, W.TAX_K["_fedtax_bc"])
    if FAILS:
        raise SystemExit(f"[BLOCKED] {len(FAILS)} gate(s): {FAILS}")
    scen = {k: v for k, v in W.scenarios().items() if k in ("mexican_origin_rough", "A1_third_plus_nh_white",
                                                            "A3_third_plus_nh_white_at_union_ages", "all_residents_slice")}
    with contextlib.redirect_stdout(io.StringIO()):     # the state rows' own gates print; FAILS collects them
        cost, lines, state = run_steps(scen)
        pieces = capture_pieces()
    if W.FAILS:
        raise SystemExit(f"[BLOCKED] the library's gates failed in a step: {W.FAILS[:3]}")
    gates_steps(scen, cost, lines, state)
    gates_pieces(pieces, scen)
    if FAILS:
        print(f"FAIL: {len(FAILS)} gate(s): {FAILS}")
        sys.exit(1)
    parts = parts_rows(scen, cost, state)
    bins = bins_rows(scen, pieces, m, lows)
    write(f"income_tax_parts_{case}.csv", parts)
    write(f"income_tax_bins_{case}.csv", bins)
    print(f"[written] derived/income_tax_parts_{case}.csv ({len(parts)} rows), derived/income_tax_bins_{case}.csv ({len(bins)} rows)")
    show = pd.DataFrame(parts).query("basis == 'accrual' and figure in ['union (rough)', 'A1_third_plus_nh_white', "
                                     "'gap: union less A1_third_plus_nh_white', 'Part F whites at union ages: sum of CA, TX and rest', "
                                     "'Part F gap: sum of CA, TX and rest']")
    print(show.drop(columns=["case", "basis"]).to_string(index=False))


if __name__ == "__main__":
    main()
