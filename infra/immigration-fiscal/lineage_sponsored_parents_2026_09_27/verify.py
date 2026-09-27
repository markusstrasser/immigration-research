#!/usr/bin/env python3
"""Gates that must pass before any sponsored-parent arm runs.

1. The lineage lane's stored sensitivity rows (central at 0% and 3%, Mexico-born-average founder,
   legalised at year 10, statutory bars and all twelve priced-care rows) are reproduced from its
   own functions to 1e-6 dollars.
2. Rebuilding the founder's stream from `founder_profile` leaves the central lineage unchanged.
3. `common.late_components` sums to `per_admission.late_profile` at every age tested.
4. A parent's stream placed on the lineage calendar reproduces the late-arrival lane's stored
   `per_admission.csv` common-total NPVs (stored rounded to $0.1).

Run from the repo root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 \
      infra/immigration-fiscal/lineage_sponsored_parents_2026_09_27/verify.py
"""
from __future__ import annotations

import sys

import numpy as np
import pandas as pd

import common as C

TOL = 1e-6


def lineage_rows(ctx: C.Ctx) -> list[dict]:
    stored = pd.read_csv(C.LINEAGE_DIR / "derived/sensitivities.csv")
    stored = stored.set_index("sensitivity")
    wl = ctx.white()
    specs = {C.CENTRAL_NAME: ({}, 0.0), "central at 3%": ({}, 0.03),
             "founder status: Mexico-born average": ({"founder_status": "mexico_born_average"}, 0.0),
             C.LEGAL_Y10: ({"legalise_year": 10}, 0.0),
             "senior rule: statutory bars from 65 (no cash transfers, public medical, institutional "
             "care or noncash aid; taxes and services kept)": (ctx.statutory(), 0.0)}
    for regime in C.REGIMES:
        for case in C.CASES:
            specs[f"senior rule: statutory bars plus priced care, {regime}, {case}"] = (
                ctx.statutory(regime, case), 0.0)
    out = []
    for name, (over, rate) in specs.items():
        s = stored.loc[name]
        ml = ctx.mex(**over)
        mine = {"mex_lineage_fiscal": C.disc(C.total_stream(ml), rate),
                "white_lineage_fiscal": C.disc(C.total_stream(wl), rate),
                "mex_founder_lifetime": C.disc(ml["G1"][1], rate)}
        mine["gap_lineage_fiscal"] = mine["mex_lineage_fiscal"] - mine["white_lineage_fiscal"]
        for k, v in mine.items():
            out.append({"gate": "lineage_row", "item": f"{name} | {k}", "stored": float(s[k]),
                        "mine": v, "abs_diff": abs(v - float(s[k])), "tol": TOL})
    return out


def founder_rebuild(ctx: C.Ctx) -> list[dict]:
    out = []
    for label, over in (("central", {}), ("legalised y10", {"legalise_year": 10}),
                        ("statutory 2026 central", ctx.statutory("rules_2026_new_enrollee", "central"))):
        a = C.disc(C.total_stream(ctx.mex(**over)), 0.0)
        b = C.disc(C.total_stream(ctx.mex(founder_vec=ctx.founder_vec(**over), **over)), 0.0)
        out.append({"gate": "founder_rebuild", "item": label, "stored": a, "mine": b,
                    "abs_diff": abs(a - b), "tol": TOL})
    return out


def late_rebuild(ctx: C.Ctx) -> list[dict]:
    out = []
    for a0 in (50, 55, 60, 65, 70, 84):
        for arm in ("statutory", "observed_late"):
            for case in C.CASES:
                ref = C.PA.late_profile(ctx.mb, ctx.acs, a0, arm, case, ctx.bar_price)
                mine = C.to_vec(C.late_components(ctx, a0, arm, case))
                d = float(np.abs(ref - mine).max())
                out.append({"gate": "late_components", "item": f"{a0}/{arm}/{case}",
                            "stored": float(ref.sum()), "mine": float(mine.sum()),
                            "abs_diff": d, "tol": TOL})
    return out


def per_admission_npv(ctx: C.Ctx) -> list[dict]:
    stored = pd.read_csv(C.LATE_DIR / "derived/per_admission.csv")
    out = []
    for a0 in (55, 60, 65):
        for case in C.CASES:
            vec = C.PA.late_profile(ctx.mb, ctx.acs, a0, "statutory", case, ctx.bar_price)
            f = ctx.parent_stream(vec, a0, 0)
            for rate in (0.0, 0.03):
                s = stored[(stored.arrival_age == a0) & (stored.arm == "statutory")
                           & (stored.case == case) & (stored.survival == "common_total")
                           & (stored.real_rate == rate)]
                assert len(s) == 1
                v = C.disc(f, rate)
                out.append({"gate": "per_admission_npv", "item": f"{a0}/statutory/{case}/{rate}",
                            "stored": float(s.npv_parent.iloc[0]), "mine": v,
                            "abs_diff": abs(v - float(s.npv_parent.iloc[0])), "tol": 0.051})
    return out


def run_gates(ctx: C.Ctx) -> pd.DataFrame:
    df = pd.DataFrame(lineage_rows(ctx) + founder_rebuild(ctx) + late_rebuild(ctx)
                      + per_admission_npv(ctx))
    df["pass"] = df.abs_diff <= df.tol
    return df


def main() -> int:
    ctx = C.Ctx()
    df = run_gates(ctx)
    df.to_csv(C.HERE / "derived/gates.csv", index=False, lineterminator="\n")
    for gate, g in df.groupby("gate", sort=False):
        print(f"[{'PASS' if g['pass'].all() else 'FAIL'}] {gate}: {len(g)} checks, "
              f"max |diff| {g.abs_diff.max():.3e}")
    if not df["pass"].all():
        print(df[~df["pass"]].to_string())
        print("[BLOCKED] gates failed; no arm may run")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
