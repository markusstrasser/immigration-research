#!/usr/bin/env python3
"""Gates for the selection-curve lane. Exit 0 = all PASS.

G1  CPS extract sha256 = manifest; Barro-Lee v3 and WIC v3 hashes pinned
G2  ladder 178: Mexican G2 no-HS gap +0.1184 recomputed with the V02 lane's estimator
G3  Indian ledger: India-born gap +10,732 raw and +10,488 top-1% excluded, recomputed from the dump
G4  reference mean percentile = 50 in every CPS and GSS spec (mid-rank construction)
G5  the main G1->G2 slopes in slopes.csv re-derive from origin_curve.csv
G6  curve_projection.csv observed rows equal origin_curve.csv; the PNG exists and is non-trivial

Run: OPENBLAS_NUM_THREADS=1 uv run --no-project --with duckdb --with pyarrow --with pyreadr \
       python3 infra/immigration-fiscal/selection_curve_2026_09_27/verify.py
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

LANE = Path(__file__).resolve().parent
sys.path.insert(0, str(LANE))
import cps_curve as cc  # noqa: E402
import load  # noqa: E402

DER = LANE / "derived"
fails = []


def check(name, ok, detail=""):
    print(f"  {'✓' if ok else '✗'} {name} {detail}")
    if not ok:
        fails.append(name)


def main() -> int:
    print("[G1] hashes")
    check("cps manifest", load.check_manifest() is not None)
    check("barro-lee v3", load.sha256_file(cc.BL_CSV) == cc.BL_SHA)
    check("wic v3", load.sha256_file(cc.WIC_RDS) == cc.WIC_SHA)

    print("[G2] ladder 178")
    df = load.load_frame()
    df["band"] = np.digitize(df.age, cc.AGE_EDGES) - 1
    g = cc.gate_ladder178(df)
    check("Mexican G2 no-HS gap", g["status"] == "PASS", f"{g['reproduced']:.4f} vs 0.1184")

    print("[G3] Indian ledger")
    r = subprocess.run([sys.executable, str(LANE / "ledger_tail.py")], capture_output=True, text=True)
    gate = json.loads((DER / "ledger_gate.json").read_text())
    check("ledger_tail exit 0", r.returncode == 0)
    check("India-born raw +10,732", abs(gate["raw"]["gap"] - 10732) < 1, f"{gate['raw']['gap']:.0f}")
    check("top-1% excluded +10,488", abs(gate["exclude_top1_income"]["gap"] - 10488) < 1,
          f"{gate['exclude_top1_income']['gap']:.0f}")

    print("[G4] reference means")
    a = json.loads((DER / "cps_audit.json").read_text())
    for k, v in a["reference_mean_pct"].items():
        check(f"CPS {k}", abs(v - 50) < 1e-6, f"{v:.6f}")
    for k, v in json.loads((DER / "gss_audit.json").read_text())["reference_mean_pct"].items():
        check(f"GSS {k}", abs(v - 50) < 1e-6, f"{v:.6f}")
    pdist = pd.read_csv(DER / "percentile_distribution.csv")
    w = pdist[pdist.group == "white_reference_G3plus"]
    check("task-1 white rows at 50", np.allclose(w.mean_pct, 50, atol=1e-6))

    print("[G5] slopes re-derive")
    o = pd.read_csv(DER / "origin_curve.csv")
    o = o[(o.spec == "all") & (o.n_g1 >= cc.MIN_G1)]
    s = pd.read_csv(DER / "slopes.csv").set_index("spec")
    for spec, x, y in (("G1->G2 education, main", "g1_p_edu", "g2_p_edu"),
                       ("G1->G2 earnings, main", "g1_p_earn", "g2_p_earn")):
        t = o.dropna(subset=[x, y])
        b = cc.wls(t[x].to_numpy(), t[y].to_numpy(), t.n_g2.to_numpy(float))
        check(spec, abs(b[1] - s.loc[spec, "slope"]) < 1e-4, f"{b[1]:.4f}")

    print("[G6] projection and figure")
    p = pd.read_csv(DER / "curve_projection.csv")
    for nm in ("India", "Mexico"):
        pr = p[(p.group == nm) & (p.outcome == "education")].iloc[0]
        orow = o[o.origin == nm].iloc[0]
        check(f"{nm} observed G1/G2", abs(pr.p_g1 - orow.g1_p_edu) < 0.01 and abs(pr.p_g2 - orow.g2_p_edu) < 0.01)
    png = DER / "selection_curve.png"
    check("selection_curve.png", png.exists() and png.stat().st_size > 50_000)

    print("[G7] arrival-age arms and nonlinearity test (audit 2026-09-27)")
    arms = pd.read_csv(DER / "selection_arms.csv")
    check("selection_arms: 3 arms x 2 Mexico x 5 models",
          len(arms) == 30 and set(arms.arm) == {"all_g1", "arrived_25plus", "arrived_under18"})
    aa = a["arrival_arms"]
    check("arms disjoint and partial", aa["share_arrived_25plus_weighted"] + aa["share_arrived_under18_weighted"] < 1)
    b = cc.yrimmig_bounds()
    check("YRIMMIG bounds parsed", b[1] == (1900, 1949) and b[62] == (2024, 2026) and all(lo <= hi for lo, hi in b.values()))
    nl = pd.read_csv(DER / "nonlinearity.csv")
    for _, r in nl.iterrows():
        check(f"nonlinearity {r.outcome} {r.mexico}: 10,000 draws, diff = below - above",
              r.draws_valid >= 9_900 and abs(r.difference - (r.slope_below - r.slope_above)) < 1e-4)
    row = nl[(nl.outcome == "education") & (nl.mexico == "with Mexico")].iloc[0]
    check("education point difference = audit 0.374", abs(row.difference - 0.374) < 0.002, f"{row.difference:.3f}")
    row = nl[(nl.outcome == "earnings") & (nl.mexico == "with Mexico")].iloc[0]
    check("earnings point difference = audit 0.466", abs(row.difference - 0.466) < 0.002, f"{row.difference:.3f}")

    print(f"\n{'ALL PASS' if not fails else 'FAIL: ' + ', '.join(fails)}")
    return 0 if not fails else 1


if __name__ == "__main__":
    raise SystemExit(main())
