#!/usr/bin/env python3
"""How much of the local-whites gap (Part F: the union less third-plus non-Hispanic whites state by state, at the union
pieces' ages) rests on a few households, on the case's income-tax keys (round 2), at oct05 or oct07 (the team lead's
request of 2026-10-07). Read-only on this lane's library (rekey_sept29.py) and income_tax_parts.py; writes one file.

Rows (derived/local_whites_fragility_<case>.csv, long: case, section, slice, measure, basis, end, value, unit):
  replicate_se         the local gap's and A1's white-side sampling error from the CPS ASEC's 160 successive-difference
                       replicate weights, SE = sqrt(4/160 sum (x_r - x_0)^2). Each white piece is rebuilt on a
                       replicate's weights as Part F builds it (reweighted within its age bands to the union piece's ages
                       and persons), A1 at its own ages; the union and its pieces, the keys and their national totals,
                       the raking and the MEPS weights are held at the central, as the Indian lane holds them. Also the
                       local gap less A1's, and each white piece's cost.
  leave_out            the local gap and A1's gap with the top 10 and top 20 households, or persons, dropped: ranked by
                       their records' contribution to the white side's central federal income tax (piece weight x the
                       raked key), each dropped record leaves every piece it is in, each Part F piece is rebuilt as Part
                       F builds it (the dropped weight goes to the other whites of the same age band) and A1 as the
                       library builds it (its own ages, scaled to its persons), and each is repriced on every line. A
                       stress test, not an interval: it always removes the largest contributors.
  personal_allocation  the local gap and A1's at the personal allocation of the case's income-tax keys, both sides (the
                       added people at the case lane's amounts), as the round-2 section prices A1 and A3 there.
  counts               per white piece (California, Texas, the rest of the US) and A1: sample records; households with a
                       member whose own AGI is at least $1M or $500k, the persons in those members' SPM units (who share
                       the unit's tax), their weighted share of the piece's persons and their share of its raked and of
                       its unraked (SPM split of FEDTAX_BC) federal tax; the top 10 and 20 records' share of the raked
                       federal tax, the households, minors and records with own AGI under $100k among the top 10; and
                       the share of the raked federal tax carried by persons under 18.

Gates (exit 1, nothing written): income_tax_parts.py's setup gates (the benchmark frame, FEDTAX_BC = FEDTAX_AC + EIT_CRED
+ ACTC_CRD, the national raked vector, the union's federal cell, the AGI bins); one national amount per income-tax line;
the rebuilt raking is the library's key (1e-12) with its pooled columns and top column; A1's gap is the parts file's
central (5e-5); each captured white piece reprices to state_summary (5e-5) and the local gap is its sum (2e-4: three
union pieces printed to 4 decimals); each slice's three-line and federal moves from its weights are the parts file's
(1e-3); the raking by column adds to the parts file's (c) (1e-3); the records' federal contributions add to each
piece's federal tax (1e-9); the replicate file covers the frame's rows and replicate 0 is the frame weight on third-plus
whites (0.0051). Positive controls: an empty drop set rebuilds every piece and A1 to their central costs (1e-9);
replicate 0 gives the central gaps within $0.05bn; the personal-allocation A1 gap is the additive figure from
income_tax_keys_<case>.csv (5e-4).
Run from the repository root after income_tax_parts.py --case <case> (--out-dir <dir> writes the file there instead):
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/white_replacement_2026_09_28/local_whites_fragility.py --case oct07
"""
from __future__ import annotations

import argparse
import contextlib
import csv
import io
import os
import sys
import zipfile
from pathlib import Path

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
sys.dont_write_bytecode = True   # read-only imports: write nothing beside them

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

LANE = Path(__file__).resolve().parent
DER = LANE / "derived"
sys.path.insert(0, str(LANE))
import income_tax_parts as P  # noqa: E402

W, R, S = P.W, P.R, P.S
FAILS: list[str] = []
N_REP = 160
REGIONS = list(S.REGIONS)          # California, Texas, rest of US
LOCAL = "local gap (California, Texas, rest of US)"
A1 = "A1 gap (third-plus non-Hispanic whites at their own ages)"
KS = (10, 20)


def gate(label, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'} {label}{' — ' + detail if detail else ''}", flush=True)
    if not ok:
        FAILS.append(label)


def stop():
    if FAILS:
        print(f"FAIL: {len(FAILS)} gate(s): {FAILS}")
        sys.exit(1)


def setup(case):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        W.use_case(case)
        W.setup()
    if W.FAILS or "FAIL" in buf.getvalue():
        raise SystemExit(f"[BLOCKED] the library's {case} setup failed")
    print(f"the library's {case} setup: {buf.getvalue().count('PASS')} gates passed", flush=True)
    R.line_share = P.parts_line_share          # MODES stays None: the library's own (central) rule
    bf, d = P.benchmark_frame()
    P.add_keys(bf, d)
    P.agi_bins(d, W.TAX_K["_fedtax_bc"])
    if P.FAILS:
        print(f"FAIL: {P.FAILS}")
        sys.exit(1)
    return bf, d


def capture():
    """Part F's white pieces at the union pieces' ages (mask, persons, target ages, scenario), as state_rows builds them
    on the central, and the state rows on both bases."""
    got = []
    real = S.white_piece

    def spy(mask, total, target_pi):
        sc = real(mask, total, target_pi)
        if target_pi is not None:
            got.append((np.asarray(mask).copy(), float(total), np.asarray(target_pi).copy(), sc))
        return sc

    S.white_piece = spy
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            st = {b: W.state_rows(b)[0] for b in W.BASES}
    finally:
        S.white_piece = real
    if W.FAILS:
        raise SystemExit(f"[BLOCKED] the library's state gates: {W.FAILS[:3]}")
    pieces = {}
    for name in REGIONS:
        m = np.ones(len(R.d), bool) if name == "rest of US" else S.REGIONS[name]
        mask, total, pi, sc = next(x for x in got if np.array_equal(x[0], m))
        pieces[name] = dict(mask=mask, total=total, pi=pi, sc=sc)
    rows = {(b, x["end"], x["region"]): x for b in W.BASES for x in st[b]}
    return rows, pieces


def price(sc):
    return {(b, end): W.priced29(sc, end, b, W.UNION_SC)[0] for b in W.BASES for end in W.ENDS}


def raking(bf, d):
    """The keys' shared raked_vector run (tax_key_heldout_2026_09_28/keys.py, the library's TK), returning each person's
    pooled columns' dollars and raked parts (gated to the library's vector)."""
    TK = W.TK
    civ, _ = bf.masks(d)
    w0 = d.pwwgt0.to_numpy(float) * civ
    labels, irs = TK.irs_2023()
    edges, lows = TK.bin_edges(labels)
    cbo = TK.cbo_shares()
    g = TK.cbo_groups(d)
    cols = TK._pool14(irs)
    m14 = TK._pool14(TK.bin_dollars(d, d.FEDTAX_BC.to_numpy(float), "shared", edges).T).T
    pos = [j for j in cbo if cbo[j] > 0]
    tb = np.stack([m14[civ & (g == j)].T @ w0[civ & (g == j)] for j in pos])
    rows = np.array([cbo[j] for j in pos])
    r = rows[:, None] * tb / tb.sum(axis=1, keepdims=True)
    for _ in range(20000):
        r *= cols[None, :] / r.sum(axis=0)[None, :]
        r *= (rows / r.sum(axis=1))[:, None]
        if max(np.abs(r.sum(axis=0) - cols).max(), np.abs(r.sum(axis=1) - rows).max()) < 1e-12:
            break
    ratio = np.divide(r, tb, out=np.zeros_like(r), where=tb > 0)
    vcol = np.zeros_like(m14)
    for i, j in enumerate(pos):
        mj = civ & (g == j)
        vcol[mj] = m14[mj] * ratio[i][None, :]
    v = vcol.sum(axis=1)
    gate("the rebuilt raking is the library's shared federal key (1e-12 relative)",
         np.allclose(v, R.K["fit_case"], rtol=1e-12, atol=0), f"max |d| {np.abs(v - R.K['fit_case']).max():.3e}")
    gate("the pooled columns' unraked dollars are the library's SPM split of FEDTAX_BC (1e-6)",
         float(np.abs(m14.sum(axis=1) - R.K["fit_bc_spm"]).max()) < 1e-6)
    gate("the pooled top column starts at $1,000,000", lows[13] == 1_000_000, f"{lows[13]:,}")
    return dict(m14=m14, vcol=vcol)


def national_lines():
    out = {}
    for b in W.BASES:
        for end in W.ENDS:
            for ln in W.DUMP[b][end]["lines"]:
                if ln["side"] == "receipts" and ln["id"] in P.LINES:
                    out.setdefault(ln["id"], set()).add(round(ln["national_bn"], 9))
    gate("each income-tax line has one national amount in every dump", all(len(v) == 1 for v in out.values()),
         str({k: sorted(v) for k, v in out.items()}))
    return {k: next(iter(v)) for k, v in out.items()}


def tax_amounts(cw, cps_bn, NAT):
    """A slice's three income-tax lines ($bn) under the CPS-dollar rule and the central keys, from its weights."""
    K, T = R.K, R.KTOT
    nat_f = R.NATIONAL["receipts|federal_income_tax"]
    nat_s = R.NATIONAL["receipts|state_local_income_tax"]
    cps = {"federal_income_tax": NAT["federal_income_tax"] * cps_bn["fit"] / nat_f,
           "state_local_income_tax": NAT["state_local_income_tax"] * cps_bn["sit"] / nat_s,
           "other_personal_tax": NAT["other_personal_tax"] * cps_bn["fit"] / nat_f}
    cen = {"federal_income_tax": NAT["federal_income_tax"] * float(cw @ K["fit_case"]) / T["fit_case"],
           "state_local_income_tax": NAT["state_local_income_tax"] * float(cw @ K["sit_case"]) / T["sit_case"],
           "other_personal_tax": NAT["other_personal_tax"] * float(cw @ K["sit_case"]) / T["sit_case"]}
    return cps, cen


def a1_rebuilt(a1, keep):
    """A1 as R.scenario('w3') builds it (own ages, scaled to its persons) on the third-plus whites in `keep`."""
    m = R.MASK["w3"] & keep
    cw = R.w * m * (a1["population"] / float(R.w[m].sum()))
    return R.keyed("w3", cw, a1["population"], a1["ages"], a1["meps_w"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", choices=W.TAX_CASES, required=True)
    ap.add_argument("--out-dir", type=Path, default=DER, help="where the file goes (default derived/)")
    args = ap.parse_args()
    case = args.case
    bf, d = setup(case)
    rows, pieces = capture()
    NAT = national_lines()
    L = NAT["federal_income_tax"]
    K, T = R.K, R.KTOT
    v = K["fit_case"]
    rk = raking(bf, d)
    stop()
    out = []

    def add(section, slc, measure, value, unit, basis="", end=""):
        if unit == "bn" or unit == "pct":
            txt = f"{value:.4f}"
        elif unit == "share":
            txt = f"{value:.6f}"
        else:
            txt = f"{int(value)}"
        out.append({"case": case, "section": section, "slice": slc, "measure": measure, "basis": basis, "end": end,
                    "value": txt, "unit": unit})

    # ---------------------------------------------------------------- the central, reproduced
    scen = W.scenarios()
    a1, a3 = scen["A1_third_plus_nh_white"], scen["A3_third_plus_nh_white_at_union_ages"]
    parts = pd.read_csv(DER / f"income_tax_parts_{case}.csv")
    union_rough = {(b, end): W.run29(W.UNION_SC, end, b)[0]["cost"] for b in W.BASES for end in W.ENDS}
    a1_cost0 = {(b, end): W.run29(a1, end, b)[0]["cost"] for b in W.BASES for end in W.ENDS}
    a1_gap0 = {k: union_rough[k] - a1_cost0[k] for k in union_rough}
    for (b, end), got in a1_gap0.items():
        want = float(parts[(parts.basis == b) & (parts.end == end)
                           & (parts.figure == "gap: union less A1_third_plus_nh_white")].central_bn.iloc[0])
        gate(f"A1 gap {b} {end}: the rough union less A1 is the parts file's central (5e-5)", abs(got - want) < 5e-5, f"{got:.4f}")
    base_cost = {name: price(p["sc"]) for name, p in pieces.items()}
    for name in REGIONS:
        for (b, end), c in base_cost[name].items():
            want = float(rows[(b, end, name)]["cost_white_union_ages_bn"])
            gate(f"{name} {b} {end}: the captured white piece reprices to state_summary's cost (5e-5)", abs(c - want) < 5e-5,
                 f"{c:.4f}")
    uc = {(b, end): sum(float(rows[(b, end, n)]["cost_union_bn"]) for n in REGIONS) for b in W.BASES for end in W.ENDS}
    gap0 = {k: uc[k] - sum(base_cost[n][k] for n in REGIONS) for k in uc}
    for k, g0 in gap0.items():
        want = float(rows[(k[0], k[1], "sum of CA, TX and rest")]["delta_union_ages_bn"])
        gate(f"local gap {k[0]} {k[1]}: the union pieces less the white pieces is state_summary's sum (2e-4)",
             abs(g0 - want) < 2e-4, f"{g0:.4f}")
    acc = parts[(parts.basis == "accrual") & (parts.end == "low")]
    pcols = [c for c in acc.columns if c.endswith("_bn") and c not in ("cps_bn", "prop_bn", "central_bn")]
    fed_parts = ["a_federal_bn", "b1_federal_credits_bn", "b2_federal_unit_bn", "c_federal_raking_bn"]
    slices = {**{n: (f"Part F whites at union ages: {n}", [pieces[n]["sc"]]) for n in REGIONS},
              "sum": ("Part F whites at union ages: sum of CA, TX and rest", [pieces[n]["sc"] for n in REGIONS]),
              "A1": ("A1_third_plus_nh_white", [a1]), "A3": ("A3_third_plus_nh_white_at_union_ages", [a3])}
    for lab, (fig, scs) in slices.items():
        pr = acc[acc.figure == fig].iloc[0]
        both = [tax_amounts(sc["cps_w"], sc["cps_bn"], NAT) for sc in scs]
        cps = {k: sum(x[0][k] for x in both) for k in P.LINES}
        cen = {k: sum(x[1][k] for x in both) for k in P.LINES}
        fmove = cen["federal_income_tax"] - cps["federal_income_tax"]
        gate(f"{lab}: the federal move from the weights is the parts file's four federal parts (1e-3)",
             abs(fmove + float(sum(pr[c] for c in fed_parts))) < 1e-3, f"{fmove:.4f}")
        tot = sum(cen.values()) - sum(cps.values())
        gate(f"{lab}: the three lines' move from the weights is the parts file's total (1e-3)",
             abs(tot + float(sum(pr[c] for c in pcols))) < 1e-3, f"{tot:.4f}")
    Kv, Ks = T["fit_case"], T["fit_bc_spm"]
    for name in REGIONS:
        cw = pieces[name]["sc"]["cps_w"]
        unr, rak = L * (cw @ rk["m14"]) / Ks, L * (cw @ rk["vcol"]) / Kv
        pr = acc[acc.figure == f"Part F whites at union ages: {name}"].iloc[0]
        gate(f"{name}: the columns' raking parts add to the parts file's (c) (1e-3)",
             abs((rak.sum() - unr.sum()) + float(pr.c_federal_raking_bn)) < 1e-3, f"{rak.sum() - unr.sum():.4f}")
    stop()

    # ---------------------------------------------------------------- counts
    agi = d.AGI.to_numpy(float)
    spm = d.SPM_ID.to_numpy()
    hh = d.PH_SEQ.to_numpy()
    age = R.d.A_AGE.to_numpy()
    s = K["fit_bc_spm"]
    unit_top = {thr: pd.Series(agi >= thr).groupby(spm).transform("max").to_numpy() for thr in (500_000, 1_000_000)}
    contrib = {}
    for name, sc in [*((n, pieces[n]["sc"]) for n in REGIONS), ("A1", a1)]:
        slc = f"whites at union ages: {name}" if name != "A1" else "A1: third-plus non-Hispanic whites at their own ages"
        cw = sc["cps_w"]
        c = L * cw * v / Kv
        contrib[name] = c
        fed = float(c.sum())
        gate(f"{name}: the records' federal contributions add to its federal tax (1e-9 rel.)",
             abs(fed - L * sc["share"]["fit_case"]) < 1e-9 * fed, f"{fed:.4f}")
        inn = cw > 0
        unr = L * cw * s / Ks
        add("counts", slc, "sample records", int(inn.sum()), "records")
        add("counts", slc, "raked federal income tax", fed, "bn")
        for thr, lab in ((1_000_000, "$1M"), (500_000, "$500k")):
            own = inn & (agi >= thr)
            unit = inn & unit_top[thr]
            add("counts", slc, f"households with a member whose own AGI is at least {lab}", pd.unique(hh[own]).size, "households")
            add("counts", slc, f"persons in those members' SPM units (AGI at least {lab})", int(unit.sum()), "records")
            add("counts", slc, f"weighted share of persons in those units (AGI at least {lab})", float(cw[unit].sum() / cw.sum()), "share")
            add("counts", slc, f"share of raked federal tax from those units (AGI at least {lab})", float(c[unit].sum() / fed), "share")
            add("counts", slc, f"share of unraked federal tax from those units (AGI at least {lab})", float(unr[unit].sum() / unr.sum()), "share")
        order = np.argsort(-c)
        for k in KS:
            add("counts", slc, f"share of raked federal tax from the top {k} records", float(c[order[:k]].sum() / fed), "share")
        top = order[:10]
        add("counts", slc, "households among the top 10 records", pd.unique(hh[top]).size, "households")
        add("counts", slc, "minors (under 18) among the top 10 records", int((age[top] < 18).sum()), "records")
        add("counts", slc, "records with own AGI under $100k among the top 10 records", int((agi[top] < 100_000).sum()), "records")
        add("counts", slc, "share of raked federal tax carried by persons under 18", float(c[age < 18].sum() / fed), "share")
    stop()

    # ---------------------------------------------------------------- leave-out
    for name, p in pieces.items():
        rebuilt = price(S.white_piece(p["mask"], p["total"], p["pi"]))
        gate(f"control: {name}'s piece rebuilt with nothing dropped is its central cost (1e-9)",
             all(abs(rebuilt[k] - base_cost[name][k]) < 1e-9 for k in rebuilt))
    a1_same = a1_rebuilt(a1, np.ones(len(v), bool))
    gate("control: A1 rebuilt with nothing dropped is its central cost (1e-9)",
         all(abs(W.run29(a1_same, end, b)[0]["cost"] - a1_cost0[(b, end)]) < 1e-9 for (b, end) in a1_cost0))
    stop()
    local_c = sum(contrib[n] for n in REGIONS)
    local_in = sum(pieces[n]["sc"]["cps_w"] for n in REGIONS) > 0
    for slc, cvec, inside in ((LOCAL, local_c, local_in), (A1, contrib["A1"], a1["cps_w"] > 0)):
        by_hh = pd.Series(cvec).groupby(hh).sum().sort_values(ascending=False, kind="mergesort")
        for k in KS:
            for kind in ("households", "persons"):
                if kind == "households":
                    drop = np.isin(hh, by_hh.index[:k].to_numpy())
                else:
                    drop = np.zeros(len(v), bool)
                    drop[np.argsort(-cvec, kind="mergesort")[:k]] = True
                what = f"top {k} {kind}"
                add("leave_out", slc, f"persons dropped: {what}", int((drop & inside).sum()), "records")
                add("leave_out", slc, f"share of the white side's raked federal tax dropped: {what}",
                    float(cvec[drop].sum() / cvec.sum()), "share")
                if slc == LOCAL:
                    new = {n: price(S.white_piece(p["mask"] & ~drop, p["total"], p["pi"])) for n, p in pieces.items()}
                    gaps = {kk: uc[kk] - sum(new[n][kk] for n in REGIONS) for kk in uc}
                    base = gap0
                else:
                    sc = a1_rebuilt(a1, ~drop)
                    gaps = {(b, end): union_rough[(b, end)] - W.run29(sc, end, b)[0]["cost"] for (b, end) in union_rough}
                    base = a1_gap0
                for (b, end), gnew in gaps.items():
                    add("leave_out", slc, f"gap without the {what}", gnew, "bn", b, end)
                    add("leave_out", slc, f"change without the {what}", gnew - base[(b, end)], "bn", b, end)
                    add("leave_out", slc, f"change without the {what}, % of the gap", 100 * (gnew - base[(b, end)]) / base[(b, end)], "pct", b, end)

    # ---------------------------------------------------------------- personal allocation
    personal = {k: f"{x}_personal" for k, x in W.CASE_TAX_KEY.items()}
    with W.patched(vars(W), CASE_TAX_KEY=personal), contextlib.redirect_stdout(io.StringIO()):
        st_p = {b: W.state_rows(b)[0] for b in W.BASES}
        a1_gap_p = {(b, end): W.run29(W.UNION_SC, end, b)[0]["cost"] - W.run29(a1, end, b)[0]["cost"]
                    for b in W.BASES for end in W.ENDS}
    if W.FAILS:
        raise SystemExit(f"[BLOCKED] the library's gates under the personal keys: {W.FAILS[:3]}")
    keys = pd.read_csv(DER / f"income_tax_keys_{case}.csv")
    dk = (keys.amount_personal_bn - keys.amount_shared_bn).groupby(keys.group).sum()
    add_p = {k: a1_gap0[k] - dk["mexican_origin_rough"] + dk["A1_third_plus_nh_white"] for k in a1_gap0}
    gate("control: A1's gap at the personal allocation is the additive figure from income_tax_keys (5e-4)",
         all(abs(a1_gap_p[k] - add_p[k]) < 5e-4 for k in a1_gap_p),
         ", ".join(f"{a1_gap_p[k]:.4f}" for k in sorted(a1_gap_p)))
    for b in W.BASES:
        for x in st_p[b]:
            if x["region"] in (*REGIONS, "sum of CA, TX and rest"):
                slc = LOCAL if x["region"] == "sum of CA, TX and rest" else f"local gap: {x['region']}"
                add("personal_allocation", slc, "gap at the shared allocation (the central)",
                    float(rows[(b, x["end"], x["region"])]["delta_union_ages_bn"]), "bn", b, x["end"])
                add("personal_allocation", slc, "gap at the personal allocation", float(x["delta_union_ages_bn"]), "bn", b, x["end"])
    for (b, end), g in a1_gap_p.items():
        add("personal_allocation", A1, "gap at the shared allocation (the central)", a1_gap0[(b, end)], "bn", b, end)
        add("personal_allocation", A1, "gap at the personal allocation", g, "bn", b, end)

    # ---------------------------------------------------------------- replicate SE
    with zipfile.ZipFile(R.ZIP) as z:
        pos_ = pd.read_csv(z.open("pppub25.csv"), usecols=["PH_SEQ", "PPPOS"])
        rep = pd.read_csv(z.open("asec_csv_repwgt_2025.csv"))
    rep = rep.rename(columns={"h_seq": "PH_SEQ"})
    mm = pos_.merge(rep, on=["PH_SEQ", "PPPOS"], how="left", validate="one_to_one")
    rcols = [f"pwwgt{i}" for i in range(N_REP + 1)]
    gate("every CPS person has replicate weights", not mm[rcols].isna().any().any())
    gate("the replicate file's rows are the rough frame's", np.array_equal(mm.PH_SEQ.to_numpy(), R.d.PH_SEQ.to_numpy()))
    rw = mm[rcols].to_numpy(float) * R.civ.astype(float)[:, None]
    del rep, mm
    w3 = R.MASK["w3"]
    gate("replicate weight 0 is the frame weight on third-plus whites (0.0051: MARSUPWT is rounded to hundredths)",
         float(np.abs(rw[w3, 0] - R.w[w3]).max()) < 0.0051)
    stop()
    reps = []
    for r in range(N_REP + 1):
        wr = rw[:, r]
        costs = {}
        for name, p in pieces.items():
            cw = R.reweight(R.MASK["w3"] & p["mask"], wr, R.cage, p["pi"], p["total"])
            costs[name] = price(R.keyed("w3", cw, p["total"], "piece", p["sc"]["meps_w"]))
        cwa = wr * w3 * (a1["population"] / float(wr[w3].sum()))
        sca = R.keyed("w3", cwa, a1["population"], a1["ages"], a1["meps_w"])
        for (b, end) in uc:
            reps.append({"r": r, "basis": b, "end": end,
                         "local": uc[(b, end)] - sum(costs[n][(b, end)] for n in REGIONS),
                         "a1": union_rough[(b, end)] - W.run29(sca, end, b)[0]["cost"],
                         **{n: costs[n][(b, end)] for n in REGIONS}})
    rp = pd.DataFrame(reps)
    for (b, end), x in rp.groupby(["basis", "end"], sort=False):
        x = x.sort_values("r")
        gate(f"control: replicate 0 gives the central local and A1 gaps within $0.05bn ({b} {end})",
             abs(x.local.iloc[0] - gap0[(b, end)]) < 0.05 and abs(x.a1.iloc[0] - a1_gap0[(b, end)]) < 0.05)
        se = {col: float(np.sqrt(4 / N_REP * ((x[col].to_numpy()[1:] - x[col].iloc[0]) ** 2).sum()))
              for col in ("local", "a1", *REGIONS)}
        diff = (x.local - x.a1).to_numpy()
        add("replicate_se", LOCAL, "central", gap0[(b, end)], "bn", b, end)
        add("replicate_se", LOCAL, "replicate 0", float(x.local.iloc[0]), "bn", b, end)
        add("replicate_se", LOCAL, "standard error", se["local"], "bn", b, end)
        add("replicate_se", A1, "central", a1_gap0[(b, end)], "bn", b, end)
        add("replicate_se", A1, "replicate 0", float(x.a1.iloc[0]), "bn", b, end)
        add("replicate_se", A1, "standard error", se["a1"], "bn", b, end)
        add("replicate_se", "local gap less A1 gap", "central", gap0[(b, end)] - a1_gap0[(b, end)], "bn", b, end)
        add("replicate_se", "local gap less A1 gap", "standard error",
            float(np.sqrt(4 / N_REP * ((diff[1:] - diff[0]) ** 2).sum())), "bn", b, end)
        for n in REGIONS:
            add("replicate_se", f"white piece at union ages: {n}", "standard error of its cost", se[n], "bn", b, end)
    stop()

    order = {"counts": 0, "leave_out": 1, "personal_allocation": 2, "replicate_se": 3}
    out.sort(key=lambda x: order[x["section"]])           # stable: each section keeps its build order
    path = args.out_dir / f"local_whites_fragility_{case}.csv"
    with open(path, "w", newline="") as f:
        wr_ = csv.DictWriter(f, fieldnames=list(out[0]), lineterminator="\n")
        wr_.writeheader()
        wr_.writerows(out)
    print(f"[written] {path} ({len(out)} rows)")
    show = pd.DataFrame(out)
    pick = show[(show.basis.isin(["", "accrual"])) & (show.end.isin(["", "low"]))]
    with pd.option_context("display.width", 250, "display.max_colwidth", 90, "display.max_rows", 400):
        print(pick.drop(columns=["case", "basis", "end"]).to_string(index=False))


if __name__ == "__main__":
    main()
