#!/usr/bin/env python3
"""Sponsored-parent (IR-5) arms on the lineage lane's century account. Arms are preregistered
in RESULT.md. `verify.run_gates` must pass first; the script stops otherwise.

Run from the repo root (after calibration.py):
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 \
      infra/immigration-fiscal/lineage_sponsored_parents_2026_09_27/arms.py
"""
from __future__ import annotations

import csv
import json
import sys

import numpy as np

import common as C
import verify

RATES = (0.0, 0.03)
NAT_RATE = 0.619
GAP = 29              # parent-child age gap, the lineage lane's generation length
ADMIT_LAG = 1         # IR-5 admission one year after naturalisation
CENTRAL = {0.0: -1297150.0, 0.03: -514635.0}   # lineage lane central, rounded as quoted


def bar_years(ctx: C.Ctx, vec: np.ndarray, start: int) -> np.ndarray:
    """Five-year bar for a new LPR at ages start..start+4: federal medical, institutional and
    noncash programs removed, public care at the per-admission lane's central bar price
    (peak state coverage), scaled before 65."""
    out = vec.copy()
    for a in range(start, start + 5):
        out[a] -= ctx.lpr_bar[a]
        out[a] += -ctx.bar_price["central"] * (1.0 if a >= 65 else ctx.pre65_scale)
    return out


def main() -> int:
    ctx = C.Ctx()
    gates = verify.run_gates(ctx)
    gates.to_csv(C.HERE / "derived/gates.csv", index=False, lineterminator="\n")
    if not gates["pass"].all():
        print("[BLOCKED] verify gates failed")
        return 1
    cal = json.loads((C.HERE / "derived/calibration.json").read_text())
    E = cal["E_chosen"]
    # p = probability a naturalised citizen petitions for their surviving parents, calibrated as
    # E / m(60); a track's expected parents are p x m(a0), so older parents are fewer.
    P = {k: v / cal["m_living_parents_at_60"] for k, v in E.items()}
    res_share = cal["resident_share"]

    white = C.total_stream(ctx.white())
    rows = []

    def emit(arm, desc, mex_stream, base_stream, extra=None, **info):
        for r in RATES:
            m = C.disc(mex_stream, r)
            w = C.disc(white, r)
            b = C.disc(base_stream, r)
            g, gb = m - w, b - w
            rows.append({"arm": arm, "description": desc, "discount": r,
                         "mex_lineage": m, "white_lineage": w, "gap": g,
                         "gap_without_channel": gb, "channel": g - gb,
                         "channel_share_of_gap": (g - gb) / g if g else float("nan"),
                         "gap_vs_lineage_central": g - CENTRAL[r],
                         "gap_over_lineage_central": g / CENTRAL[r], **(extra or {}), **info})

    # ------------------------------------------------------------- comparators
    central = C.total_stream(ctx.mex())
    emit("ref_central", "lineage lane central: never legalised, pooled profile from 65",
         central, central)
    never = {}
    for regime in C.REGIMES:
        for case in C.CASES:
            s = C.total_stream(ctx.mex(**ctx.statutory(regime, case)))
            never[(regime, case)] = s
            emit(f"ref_never_{regime}_{case}",
                 f"never legalised, statutory bars plus priced care, {regime}, {case}", s, s)
    never26 = never[("rules_2026_new_enrollee", "central")]
    y10 = C.total_stream(ctx.mex(legalise_year=10))
    emit("ref_legal_y10", "lineage lane arm 2b: legalised at year 10 (age 35)", y10, y10)

    # --------------------------------------------------- arm 1: legalised by a US-born child
    def arm1(label, desc, vec):
        s = C.total_stream(ctx.mex(founder_vec=vec))
        emit(label, desc + " | channel vs never legalised, 2026 rules, central", s, never26)
        emit(label + "_vs_central", desc + " | channel vs lineage central (pooled from 65)", s, central)
        for (regime, case), n in never.items():
            emit(f"{label}_vs_never_{regime}_{case}",
                 f"{desc} | channel vs never legalised, {regime}, {case}", s, n)
        return s

    # child G2 born year 4 (founder 29), turns 21 in year 25: founder 50
    for lag in (0, 2):
        adj_age = 50 + lag
        v1a = ctx.founder_vec(legalise_year=adj_age - C.FOUNDER_AGE)
        arm1(f"1a_adjust_lag{lag}", f"founder adjusts to LPR at {adj_age}; pooled profile after", v1a)
        arm1(f"1a_bar_adjust_lag{lag}", f"founder adjusts at {adj_age}; five-year bar at "
             f"{adj_age}-{adj_age + 4}", bar_years(ctx, v1a, adj_age))
        back = adj_age + 10
        v1b = ctx.founder_vec(legalise_year=back - C.FOUNDER_AGE)
        v1b[adj_age:back] = 0.0
        arm1(f"1b_consular_lag{lag}", f"founder leaves at {adj_age}, ten-year bar, admitted at "
             f"{back}; pooled profile after", v1b)
        arm1(f"1b_bar_consular_lag{lag}", f"founder leaves at {adj_age}, admitted at {back}, "
             f"five-year bar at {back}-{back + 4}", bar_years(ctx, v1b, back))

    # ------------------------------------------------------ arm 2: founder sponsors parents
    tracks = {
        "L25": ("founder LPR on arrival (Mexico-born average), naturalises at 30",
                C.total_stream(ctx.mex(founder_status="mexico_born_average")), 30),
        "L10": ("founder legalised at year 10 (35), naturalises at 40",
                C.total_stream(ctx.mex(legalise_year=10)), 40),
        "L50": ("founder legalised at 50 by a US-born child (arm 1a), naturalises at 55",
                C.total_stream(ctx.mex(founder_vec=ctx.founder_vec(legalise_year=25))), 55),
    }

    def parent_vectors(a0):
        """Per-parent profile by pricing: new arrival (statutory, three cases) and eligibility
        change only (LPR minus unauthorized resident; three counterfactual variants)."""
        out = {}
        for case in C.CASES:
            out[f"new_{case}"] = C.PA.late_profile(ctx.mb, ctx.acs, a0, "statutory", case,
                                                   ctx.bar_price)
        lpr = C.late_components(ctx, a0, "statutory", "central")
        lpr_vec = C.to_vec(lpr)
        out["elig_central"] = lpr_vec - C.unauthorized_counterfactual(
            ctx, lpr, "rules_2026_new_enrollee", "central", bars_from=65)
        out["elig_bars_all_ages"] = lpr_vec - C.unauthorized_counterfactual(
            ctx, lpr, "rules_2026_new_enrollee", "central", bars_from=0)
        out["elig_peak_state"] = lpr_vec - C.unauthorized_counterfactual(
            ctx, lpr, "peak_state_coverage", "central", bars_from=65)
        return out

    def run_track(tname, a0):
        desc, base, nat_age = tracks[tname]
        t_nat = nat_age - C.FOUNDER_AGE
        t_adm = t_nat + ADMIT_LAG
        founder_age_adm = C.FOUNDER_AGE + t_adm
        m = ctx.living_parents(a0, gap=a0 - founder_age_adm)
        pv = parent_vectors(a0)
        streams = {k: ctx.parent_stream(v, a0, t_adm) for k, v in pv.items()}
        info = {"track": tname, "parent_age_at_admission": a0, "admission_year": t_adm,
                "living_parents_m": m}
        # per-parent values, for the record
        for k, s in streams.items():
            for r in RATES:
                rows.append({"arm": f"2_{tname}_a{a0}_per_parent_{k}",
                             "description": f"one parent, {k}, admitted at {a0} in year {t_adm}, "
                                            f"discounted to year 0", "discount": r,
                             "channel": C.disc(s, r), **info})
        emit(f"2_{tname}_a{a0}_p0", f"{desc}; p = 0", base, base, extra={"parents": 0.0}, **info)
        for pricing in ("new_central", "new_low", "new_high", "elig_central",
                        "elig_bars_all_ages", "elig_peak_state"):
            for plabel, n in (("p1", NAT_RATE * m), ("p1_given_naturalised", m)):
                emit(f"2_{tname}_a{a0}_{plabel}_{pricing}", f"{desc}; {plabel}; {pricing}",
                     base + n * streams[pricing], base, extra={"parents": n, "pricing": pricing},
                     **info)
            for ek in ("low", "central", "high"):
                n = NAT_RATE * P[ek] * m
                emit(f"2_{tname}_a{a0}_pcal_{ek}_{pricing}",
                     f"{desc}; calibrated E {ek} ({cal['E_rule'][ek]}); {pricing}",
                     base + n * streams[pricing], base,
                     extra={"parents": n, "pricing": pricing, "p": P[ek]}, **info)
        # calibrated, mixed new arrivals and already-resident parents
        for rk, rs in res_share.items():
            for ek in ("low", "central", "high"):
                n = NAT_RATE * P[ek] * m
                mix = (1 - rs) * streams["new_central"] + rs * streams["elig_central"]
                emit(f"2_{tname}_a{a0}_pcal_{ek}_mixed_res{rk}",
                     f"{desc}; calibrated E {ek}; resident share {rs:.2f}", base + n * mix, base,
                     extra={"parents": n, "pricing": f"mixed_resident_{rs:.2f}", "p": P[ek]},
                     **info)

    for a0 in (55, 60, 65):
        run_track("L25", a0)
    run_track("L10", 70)
    run_track("L50", 85)

    keys = []
    for r in rows:
        for k in r:
            if k not in keys:
                keys.append(k)
    with open(C.HERE / "derived/arms.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=keys, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()})
    audit = {"inputs_sha256": C.manifest(), "gates": {g: {"n": int(len(d)), "max_abs_diff":
                                                          float(d.abs_diff.max()),
                                                          "pass": bool(d["pass"].all())}
                                                      for g, d in gates.groupby("gate")},
             "calibration": cal, "naturalisation_rate": NAT_RATE, "parent_gap": GAP,
             "admission_lag_after_naturalisation": ADMIT_LAG,
             "lpr_bar_price_central": ctx.bar_price["central"], "pre65_scale": ctx.pre65_scale}
    (C.HERE / "derived/audit.json").write_text(json.dumps(audit, indent=1, sort_keys=True) + "\n")
    print(f"[written] arms.csv ({len(rows)} rows), audit.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
