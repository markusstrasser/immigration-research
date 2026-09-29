"""The legal-status calibration arm, step 2b: the payroll-compliance item's ratios on each arm.

Candidate v4's item 6a (payroll_items "central", payroll_rule "proportional") moves each receipt line's group amount by
(r_cal_raw - 1), read from payroll_compliance_2026_09_28/derived/items.json, items.all.central. Those ratios are
status-keyed twice: the item is built on the imputed unauthorized (the paper flag, on published weights: off-books
slopes for the flagged in four industries, the taxes their off-books part leaves unpaid added back to consumption, and
the EITC the audit's rules deny), and its calibration factor c reads the case's status stacks
(row4+status_state_aware|central|<method> against |alone|). This script recomputes items.all.central's r_cal_raw with
the lane's own Frame, keys and share function (compliance.py, imported read-only), following main()'s code for that
item: each arm's movers (derived/movers.csv) move on the lane's paper flag by their change from the adopted flag
(clipped to [0, 1]; an arrival-tier mover the paper flag already counts legal stays legal), and the calibration reads
the arm's stacks (derived/stacks.json). A fractional flag theta takes 1 - theta of the person at full compliance and
theta at the flagged treatment: on-books scale (1 - theta) + theta x s, the four industries' (1 - theta) + theta x
(1 - slope), the EITC denied in proportion theta. The within-group ratio r_cal is not recomputed: the set reads r_raw's
calibrated form only.

Gate (stops with [BLOCKED] before anything is written): with the adopted flag and the case's stacks, every line and
allocation's r_cal_raw equals items.json's (1e-12).
Writes derived/payroll.json. Run from the repository root after calibrate.py:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/status_calibration_2026_09_30/payroll.py
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # read-only imports from other lanes: write nothing beside them

import json  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
OUT = HERE / "derived"
sys.path.insert(0, str(FISCAL / "payroll_compliance_2026_09_28"))

import compliance as pc  # noqa: E402

f = pc.f
ITEMS = pc.OUT / "items.json"


def blocked(msg: str):
    raise SystemExit(f"[BLOCKED] {msg}")


def main() -> None:
    stored = json.loads(ITEMS.read_text())["items"]["all"]["central"]
    if stored["row2_case"] != "central":
        blocked("items.all.central is not at row 2's central case")
    ob = pc.onbooks_shares()
    slopes = pc.gap_lane()
    ae = pc.alm_erard()
    d = pc.load()
    F = pc.Frame(d)
    W = F.W
    if not all(ok for _, ok, _ in pc.GATES):
        blocked("a payroll-lane input gate failed: " + "; ".join(n for n, ok, _ in pc.GATES if not ok))

    # main()'s keys and CBO group weights, as that script builds them.
    model = json.loads(f.MODEL.read_text())
    ref = model["receipts"]["reference"]
    national = {l["id"]: l["national_bn"] for l in model["receipts"]["lines"]}
    trans = pd.read_csv(pc.BENCH / "derived/cbo_translation.csv")
    part = {}
    for line, spec in pc.CBO_SPEC.items():
        r = trans.query("spec == @spec and line == @line")
        part[line] = float(r.national_bn.iloc[0]) / national[line]
    lines = {}
    for l in model["receipts"]["lines"]:
        key = l["cells"][ref]["shared"]["key"]
        if key in pc.KEYS:
            lines[l["id"]] = (key, pc.CBO_SPEC.get(l["id"]), part.get(l["id"], 0.0))
    no_cbo = {line: (key, None, 0.0) for line, (key, _, _) in lines.items()}
    K = {}  # the raw ratios read no CBO weight; shares() takes K only on lines with a spec
    t0 = {(l["id"], a): l["cells"][ref][a]["target_bn"] for l in model["receipts"]["lines"] for a in pc.ALLOCS}

    s_mex, s_oth = ob["central"]
    origin = np.where(F.mex, s_mex, s_oth)
    inf = np.isin(F.ind, [c for v in pc.INFORMAL.values() for c in v])
    us = (1 - np.clip(np.where(inf, ae["rho_informal"], ae["rho_formal"]), 0, 1)) * F.seinc  # se_us("central")
    other = F.unauth & ~F.latin & F.no_degree  # d_scale(s_oth, restricted=True): unchanged by any mover

    def ratios(theta: np.ndarray, stacks: dict) -> dict:
        """items.all.central's r_cal_raw per line and allocation with row 2 at theta (main()'s formulas)."""
        b = (1.0 - theta) + theta * origin                       # F.scale(*ob["central"])
        sc = b.copy()
        for sl in slopes.values():                                # c_scale("central", b)
            sc = np.where(F.ind == sl["code"], (1.0 - theta) + theta * (1 - sl["central"]), sc)
        sc = np.where(other, s_oth, sc)                           # d_scale(s_oth, True, .)
        denied = np.where(other, 1.0, theta)                      # F.unpaid's `flagged`, in proportion
        off = 1 - sc
        dres = (off * (d.FICA.to_numpy(float) + F.fedbc + F.st) - denied * d.EIT_CRED.to_numpy(float)
                - off * d.ACTC_CRD.to_numpy(float))
        base_raw = pc.shares(F, F.vectors(scale=b), K, no_cbo, W)
        sG = pc.shares(F, F.vectors(scale=np.where(F.target, 1.0, b)), K, no_cbo, W)
        sO = pc.shares(F, F.vectors(scale=np.where(F.target, b, 1.0)), K, no_cbo, W)
        pay = lambda k, c, line, a: stacks[f"{c}|{k}"]["receipts"].get(line, {}).get(a, 0.0)  # noqa: E731
        c = {}
        for line in lines:
            for a in pc.ALLOCS:
                k = (line, a)
                tc = t0[k] + np.mean([pay(m, "central", line, a) for m in pc.METHODS])
                rel_pkg = np.mean([pay(m, "alone", line, a) - pay(m, "central", line, a) for m in pc.METHODS]) / tc if tc else 0.0
                gG, gO = ((x[k][0] - base_raw[k][0]) / base_raw[k][0] for x in (sG, sO))
                c[k] = (rel_pkg - gO) / gG if abs(gG) > 1e-9 else None
        for a in pc.ALLOCS:
            wts = {u: base_raw[(u, a)][0] * national[u] * ((sG[(u, a)][0] - base_raw[(u, a)][0]) / base_raw[(u, a)][0])
                   for u in pc.UNPAID_LINES}
            c_unpaid = sum(c[(u, a)] * wts[u] for u in pc.UNPAID_LINES) / sum(wts.values())
            for line in lines:
                if c[(line, a)] is None:
                    c[(line, a)] = c_unpaid
        s_item = pc.shares(F, F.vectors(us=us, scale=sc, dres=dres), K, no_cbo, W)
        s_g = pc.shares(F, F.vectors(scale=np.where(F.target, sc, b), dres=dres * F.target), K, no_cbo, W)
        out = {}
        for line in lines:
            out[line] = {}
            for a in pc.ALLOCS:
                k = (line, a)
                r_raw = s_item[k][0] / base_raw[k][0]
                out[line][a] = float(r_raw + (c[k] - 1) * (s_g[k][0] / base_raw[k][0] - 1))
        return out

    cache = json.loads(pc.STACK_CACHE.read_text())
    alone = {f"alone|{m}": cache[f"row4+status_state_aware|alone|{m}"] for m in pc.METHODS}
    case = {f"central|{m}": cache[f"row4+status_state_aware|central|{m}"] for m in pc.METHODS}
    paper = F.row2.astype(float)
    got = ratios(paper, {**alone, **case})
    worst = max(abs(got[line][a] - stored["lines"][line][a]["r_cal_raw"]) for line in got for a in pc.ALLOCS)
    print(f"[gate] adopted flag and the case's stacks: r_cal_raw equals items.json on {len(got)} lines x 2 allocations, "
          f"largest difference {worst:.1e}", flush=True)
    if worst > 1e-12 or set(got) != set(stored["lines"]):
        blocked("the adopted flag does not reproduce items.all.central's r_cal_raw")

    arm_stacks = json.loads((OUT / "stacks.json").read_text())["stacks"]
    movers = pd.read_csv(OUT / "movers.csv")
    idx = pd.Series(np.arange(len(d)), index=pd.MultiIndex.from_arrays([d.PH_SEQ.to_numpy(), d.PPPOS.to_numpy()]))
    out = {}
    for arm in dict.fromkeys(pd.read_csv(OUT / "arms.csv").arm):
        mv = movers[movers.arm == arm]
        rows = idx.reindex(pd.MultiIndex.from_arrays([mv.PH_SEQ.to_numpy(), mv.PPPOS.to_numpy()])).to_numpy()
        if np.isnan(rows).any():
            blocked(f"{arm}: movers missing from the payroll lane's frame")
        rows = rows.astype(int)
        if not (F.latin[rows].all() and F.mex[rows].all()):
            blocked(f"{arm}: a mover who is not Mexico-born")
        theta = paper.copy()
        theta[rows] = np.clip(paper[rows] + (mv.theta.to_numpy() - mv.adopted.to_numpy()), 0.0, 1.0)
        st = {**alone, **{f"central|{m}": arm_stacks[arm][m] for m in pc.METHODS}}
        r = ratios(theta, st)
        out[arm] = {"r_cal_raw": r, "movers_on_paper_flag": float(np.abs(theta - paper)[rows] @ W[rows, 0]),
                    "largest_change": max(abs(r[line][a] - got[line][a]) for line in r for a in pc.ALLOCS)}
        print(f"[payroll] {arm}: flag moves {out[arm]['movers_on_paper_flag']:,.0f} persons on the paper flag "
              f"(published weights); largest ratio change {out[arm]['largest_change']:.2e}", flush=True)
    meta = {"source": str(ITEMS.relative_to(FISCAL)), "field": "items.all.central.lines.<line>.<allocation>.r_cal_raw",
            "gate_largest_difference": worst}
    (OUT / "payroll.json").write_text(json.dumps({"meta": meta, "arms": out}, indent=1, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
