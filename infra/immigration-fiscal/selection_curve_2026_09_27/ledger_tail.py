#!/usr/bin/env python3
"""Task 1, fiscal side: how much of the Indian ledger's partial fiscal gap comes from the top tail.

Input: `_cache/ledger_persons.csv.gz` from `ledger_dump.py` (the Indian ledger's person-level
`extended_balance_after_health`, headline allocation `equal_all_members`, CPS ASEC 2025 public
file, 160 SDR replicates). Thresholds are the third-plus NH white reference's weighted p90/p95/p99
of own earnings (PEARNVAL) within the ledger's ten-year age bands.

Gate: the raw India-born gap reproduces the memo's +10,732 and the top-1% (SPM resources) arm
+10,488 before anything new is reported.

Run: uv run --no-project python3 infra/immigration-fiscal/selection_curve_2026_09_27/ledger_tail.py
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np
import pandas as pd

LANE = Path(__file__).resolve().parent
SRC = LANE / "_cache" / "ledger_persons.csv.gz"
OUT = LANE / "derived" / "tail_share_fiscal.csv"
BANDS = [(25, 34), (35, 44), (45, 54), (55, 64)]
GROUPS = ["india_born", "india_second_gen", "china_born", "mexico_born", "mexican_second_gen",
          "all_foreign_born"]
REF = "third_plus_nh_white"


def sdr(v: np.ndarray) -> tuple[float, float]:
    return float(v[0]), float(np.sqrt(4 / 160 * np.square(v[1:] - v[0]).sum()))


def wq(y, w, p):
    o = np.argsort(y, kind="stable")
    c = np.cumsum(w[o]) / w.sum()
    return float(y[o][min(np.searchsorted(c, p), len(y) - 1)])


def main() -> int:
    d = pd.read_csv(SRC)
    W = d[[f"w{j}" for j in range(161)]].to_numpy()
    net, earn, age = d.net.to_numpy(), d.earnings.to_numpy(), d.age.to_numpy()
    band = np.digitize(age, [35, 45, 55])
    ref = d[f"g_{REF}"].to_numpy() == 1

    def mean_reps(mask, y):
        ww = W[mask]
        return (ww * y[mask, None]).sum(0) / ww.sum(0)

    # gate
    gate = {}
    for arm, extra in (("raw", np.ones(len(d), bool)), ("exclude_top1_income", d.top1_resources.to_numpy() == 0)):
        g = (d["g_india_born"].to_numpy() == 1) & extra
        r = ref & extra
        est, se = sdr(mean_reps(g, net) - mean_reps(r, net))
        gate[arm] = {"gap": est, "se": se}
    gate["status"] = ("PASS" if abs(gate["raw"]["gap"] - 10732) < 1 and abs(gate["exclude_top1_income"]["gap"] - 10488) < 1
                      else "FAIL")
    print(json.dumps(gate, indent=1))
    if gate["status"] != "PASS":
        raise SystemExit("[BLOCKED] ledger gate failed")

    w0 = W[:, 0]
    thr = {}
    for q in (0.90, 0.95, 0.99):
        t = np.zeros(len(d))
        for b in range(4):
            m = ref & (band == b)
            t[band == b] = wq(earn[m], w0[m], q)
        thr[q] = t

    rows = []
    for g in GROUPS:
        gm = d[f"g_{g}"].to_numpy() == 1
        gap_reps = mean_reps(gm, net) - mean_reps(ref, net)
        gap, gap_se = sdr(gap_reps)
        for q, t in thr.items():
            above = earn > t
            # contribution of persons above the white threshold to the gap (sum decomposition)
            part = ((W[gm & above] * net[gm & above, None]).sum(0) / W[gm].sum(0)
                    - (W[ref & above] * net[ref & above, None]).sum(0) / W[ref].sum(0))
            p_est, p_se = sdr(part)
            share_est, share_se = sdr(part / gap_reps)
            below_gap, below_se = sdr(mean_reps(gm & ~above, net) - mean_reps(ref & ~above, net))
            rows.append({"group": g, "n": int(gm.sum()), "gap_net_after_health": gap, "gap_se": gap_se,
                         "white_earnings_threshold": f"p{int(q * 100)}",
                         "group_share_above": float(W[gm & above, 0].sum() / W[gm, 0].sum()),
                         "white_share_above": float(W[ref & above, 0].sum() / W[ref, 0].sum()),
                         "gap_from_persons_above": p_est, "gap_from_persons_above_se": p_se,
                         "share_of_gap_from_persons_above": share_est, "share_se": share_se,
                         "gap_excluding_persons_above": below_gap, "gap_excluding_se": below_se})
    OUT.parent.mkdir(exist_ok=True)
    with open(OUT, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: (f"{v:.6g}" if isinstance(v, float) else v) for k, v in r.items()})
    (LANE / "derived" / "ledger_gate.json").write_text(json.dumps(gate, indent=2) + "\n")
    for r in rows:
        print(f"{r['group']:<20} {r['white_earnings_threshold']}  gap {r['gap_net_after_health']:>8.0f}  "
              f"share above {r['group_share_above']:.3f} (white {r['white_share_above']:.3f})  "
              f"from above {r['gap_from_persons_above']:>8.0f} ({r['share_of_gap_from_persons_above']:.2f})  "
              f"excl above {r['gap_excluding_persons_above']:>8.0f} ({r['gap_excluding_se']:.0f})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
