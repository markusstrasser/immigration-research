#!/usr/bin/env python3
"""Van Hook & Bachmeier's fourth-plus identification rate as arms of the population machinery, on the account's frame.

Arms (effective fourth-plus identification rate p4, the population lane's DT_4TH_PLUS_ID slot; every arm is flat, held
for G5+ like arm b, because VHB's sample reaches great-grandchildren only, except the compounding row beside):
  vhb_i_relative     p3 x (G4+ / G3)_VHB = 0.8881 x 51.0 / 74.2: VHB's step from the third generation onto the
                     account's measured third-generation rate; equivalent to assuming VHB's shortfall against the CPS at
                     G3 carries unchanged to G4.
  vhb_ii_g1norm      (G4+ / G1)_VHB = 51.0 / 86.8: VHB's first generation taken as full identification (the account's G1
                     is birthplace); implies a G3 rate of 0.855 against the measured 0.888.
  vhb_ii_g2norm      (G4+ / G2)_VHB = 51.0 / 83.8: normalising on VHB's second generation (VHB's G3 / G2, 0.885, is near
                     p3, the claim the brief asks to test).
  vhb_iii_hispanic   p3 x (G4+ / G3)_VHB on "identify as Hispanic", 82.8 / 84.6: exit from any Hispanic identity, not
                     the account's construct (the account counts Mexican-origin reports), beside only.
  vhb_iv_cal_cps     VHB's G3 -> G4 log step scaled by k = ln(p3 / G1_CPS) / ln(G3_VHB / G1_VHB): today's CPS loss from
                     the first generation to the third over VHB's, both G1-normalised (G1_CPS adults 20+, benchmark.py).
  vhb_iv_cal_dt      the same step scaled by k = ln(p3_2025) / ln(p3_DT 1994-2006): the CPS third-generation rate today
                     over Duncan and Trejo's era, on the same design (arm3_dt_table8_replication.csv).
  vhb_v_compound     VHB's step compounded each generation past G4, rho 0.5 (identity_loss_propagation p_eff): beside
                     only, since VHB observe no fifth generation.

Each arm runs mexican_origin_population_total_2026_09_19/bounds_coverage_fiscal.py main() through
identity_loss_propagation_2026_09_27/propagate.py run_population (imported; its cache directory pointed here), the
added persons split by the population lane's arm-5 generation split, exactly as propagate.py builds
population_arms.csv. Positive controls: arms a, b and c (rho 0.5) rerun here equal the stored population_arms.csv rows.

Then main_case_lineage_2026_10_05/population.py main() (imported, module paths pointed here) moves every arm to the
account's frame (factor 0.997189) and writes population.json with arms floor, a, b, c and the VHB arms; a gate checks
floor, a, b and c equal that lane's population.json. Arms b, vhb_i_relative and vhb_iv_cal_cps are added again as
`<arm>_later_c3`, the same persons with every one priced as a G3-rate attriter (later losses closing C3 of the gap).

Outputs: derived/arms_vhb.csv, derived/population_arms.csv, derived/population.json, derived/population_arms_account.csv,
         derived/gates_population.json, derived/gates_arms.json
Run from the repository root after benchmark.py:
    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/vhb_fourth_plus_2026_10_07/arms.py
"""
from __future__ import annotations

import csv
import importlib.util
import json
import math
import sys
from pathlib import Path

sys.dont_write_bytecode = True  # read-only imports from other lanes: write nothing beside them

import pandas as pd  # noqa: E402

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
OUT = HERE / "derived"
CACHE = HERE / "_cache"
PROP_DIR = FISCAL / "identity_loss_propagation_2026_09_27"
LIN5_DIR = FISCAL / "main_case_lineage_2026_10_05"
DT_TABLE = FISCAL / "mexican_origin_population_total_2026_09_19/derived/arm3_dt_table8_replication.csv"
RHO = 0.5
LATER_C3 = ("b", "vhb_i_relative", "vhb_iv_cal_cps")   # arms also priced with later losses closing C3 (sensitivity)
GATES: list[dict] = []


def gate(name: str, ok: bool, detail: str = "") -> None:
    GATES.append({"gate": name, "passed": bool(ok), "detail": detail})
    print(f"  {'✓' if ok else '✗'} {name}{' - ' + detail if detail else ''}", flush=True)


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def rows(path: Path) -> list[dict]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    OUT.mkdir(exist_ok=True)
    CACHE.mkdir(exist_ok=True)
    print("[inputs]", flush=True)
    PR = load("identity_loss_propagate", PROP_DIR / "propagate.py")
    PR.CACHE = CACHE                         # run_population writes _cache/pop_<tag>/ here, never upstream
    vhb = {r["generation"]: r for r in rows(OUT / "vhb_table_2_1.csv")}
    mex = {g: float(r["pct_id_mexican"]) / 100 for g, r in vhb.items()}
    hisp = {g: float(r["pct_id_hispanic"]) / 100 for g, r in vhb.items()}
    bench = {(r["ages"], r["generation"]): r for r in rows(OUT / "cps_benchmark.csv")}
    g1_cps = float(bench[("20+", "G1 (Mexico-born, any citizenship)")]["id_mexican"])
    dt = {r["cell"]: r for r in rows(DT_TABLE)}
    p3_dt = float(dt["3rd gen, all"]["pct_identified_mexican_DT_1994_2006"]) / 100
    p3_2025_dt = float(dt["3rd gen, all"]["pct_identified_mexican_2025"]) / 100

    lo = PR.losses()
    p3 = PR.pop_p3()
    S = PR.schedules(p3, lo)
    gate("p3 is the population lane's 0.888111 (6 decimals)", abs(p3 - 0.888111) < 5e-7, f"{p3:.10f}")
    gate("the DT replication's 2025 third-generation rate is p3 (two decimals, its print)",
         abs(p3_2025_dt - round(p3 * 100, 2) / 100) < 1e-12, f"{p3_2025_dt} vs {p3:.6f}")
    step = mex["G4+"] / mex["G3"]
    k_cps = math.log(p3 / g1_cps) / math.log(mex["G3"] / mex["G1"])
    k_dt = math.log(p3) / math.log(p3_dt)
    vhb_step = {"kind": "compound", "step": 1.0 - step, "label": "VHB step compounded"}
    arms = {
        "vhb_i_relative": (p3 * step, "p3 x (G4+/G3)_VHB, Mexican"),
        "vhb_ii_g1norm": (mex["G4+"] / mex["G1"], "(G4+/G1)_VHB, Mexican"),
        "vhb_ii_g2norm": (mex["G4+"] / mex["G2"], "(G4+/G2)_VHB, Mexican"),
        "vhb_iii_hispanic": (p3 * hisp["G4+"] / hisp["G3"], "p3 x (G4+/G3)_VHB, Hispanic (not the account's construct)"),
        "vhb_iv_cal_cps": (p3 * step ** k_cps, f"p3 x (G4+/G3)_VHB ^ k, k = {k_cps:.6f} (CPS vs VHB, G1 to G3)"),
        "vhb_iv_cal_dt": (p3 * step ** k_dt, f"p3 x (G4+/G3)_VHB ^ k, k = {k_dt:.6f} (CPS 2025 vs DT 1994-2006, G3)"),
        "vhb_v_compound": (PR.p_eff(vhb_step, p3, RHO), "VHB step compounded past G4, rho 0.5 (beside)"),
    }
    gate("arm (i) is 0.8881 x 0.687 = 0.610 (3 decimals)", abs(arms["vhb_i_relative"][0] - 0.610) < 5e-4,
         f"{arms['vhb_i_relative'][0]:.6f}; VHB G4+/G3 {step:.6f}")
    gate("arm b's relative step is 0.880 (1 - the G3+ parents' 0.1204 loss)", abs(1 - lo["mex_mex_G3plus"] - 0.8796) < 1e-4,
         f"{1 - lo['mex_mex_G3plus']:.6f}")
    gate("calibration exponents lie in (0, 1): VHB's step is steeper than today's on both comparisons",
         0 < k_cps < 1 and 0 < k_dt < 1, f"k_cps {k_cps:.4f}, k_dt {k_dt:.4f}")

    # ---- population: positive controls on the stored arms, then the VHB arms
    stored = rows(PROP_DIR / "derived/population_arms.csv")
    cols = list(stored[0])
    ref = PR.run_population("reproduce", None)
    b0 = pd.read_csv(ref / "arm3_correction_bounds.csv")

    def arm5_rows(f: pd.DataFrame, g: pd.DataFrame, assumption: str):  # copy of propagate.main()'s arm5_rows
        gs = g[(g.population_assumption == assumption) & g.c3_source.str.endswith(PR.CENTRAL)]
        if len(gs) != 1:
            raise SystemExit(f"[BLOCKED] arm 5 central split row not unique for {assumption}")
        dtr = f[(f.population_assumption == assumption) & f.attriter_characteristics.str.startswith(PR.DT_ROW)]
        sp = f[(f.population_assumption == assumption) & f.attriter_characteristics.str.startswith(PR.SPLIT_ROW)
               & f.attriter_characteristics.str.contains(f"({gs.iloc[0].c3_source})", regex=False)]
        if not len(dtr) == len(sp) == 1:
            raise SystemExit(f"[BLOCKED] arm 5 rows not unique for {assumption}")
        return dtr.iloc[0], sp.iloc[0], gs.iloc[0]

    def run(key: str, rho: float, pe: float) -> dict:
        d = PR.run_population(f"{key}_rho{rho}", pe)
        bb = pd.read_csv(d / "arm3_correction_bounds.csv")
        for i in (0, 1, 3):
            if not bb.iloc[i].equals(b0.iloc[i]):
                raise SystemExit(f"[BLOCKED] substitution leaked into bound row {i}")
        b_row = bb.iloc[2]
        if abs(b_row.fourth_plus_identification_rate - round(pe, 4)) > 1e-12:
            raise SystemExit("[BLOCKED] substituted rate not carried")
        f5, s5, g5 = arm5_rows(pd.read_csv(d / "arm5_fiscal_implication.csv"),
                               pd.read_csv(d / "arm5_generation_split.csv"), b_row.assumption)
        union, corr = float(b_row.corrected_union), float(b_row.corrected_third_plus)
        return {"arm": key, "rho": rho, "p_eff_fourth_plus": pe,
                "corrected_third_plus_M": corr / 1e6, "union_M": union / 1e6, "union_pes_M": union * PR.PES / 1e6,
                "added_M": float(b_row.added) / 1e6,
                "hidden_share_of_third_plus": float(b_row.added) / corr,
                "hidden_share_of_union": float(b_row.added) / union,
                "gap_per_person_after": float(f5.gap_per_person_after),
                "aggregate_gap_bn_after": float(f5.aggregate_gap_bn_after),
                "g3_rate_attriters_M": float(g5.g3_rate_attriters) / 1e6,
                "later_loss_attriters_M": float(g5.later_loss_attriters) / 1e6,
                "gap_per_person_after_split": float(s5.gap_per_person_after),
                "aggregate_gap_bn_after_split": float(s5.aggregate_gap_bn_after)}

    fmt = lambda v: repr(float(v)) if isinstance(v, float) else str(v)  # noqa: E731  (propagate.py's writer)
    print("[population: positive controls]", flush=True)
    for key, rho in (("b_one_step", 0.5), ("c_compound", 0.5)):
        rec = run(f"control_{key}", rho, PR.p_eff(S[key], p3, rho))
        want = next(r for r in stored if r["arm"] == key and float(r["rho"]) == rho)
        diffs = [c for c in cols if c != "arm" and fmt(rec[c]) != want[c]]
        gate(f"rerun of arm {key} (rho {rho}) equals population_arms.csv in every column, as written", not diffs,
             f"added {rec['added_M']:.7f}M; differing columns {diffs}")
    want_a = next(r for r in stored if r["arm"] == "a_current")
    gate("arm a's stored p4 is p3 (its row is the bound's measured-rate row)", float(want_a["p_eff_fourth_plus"]) == p3)

    print("[population: VHB arms]", flush=True)
    recs = []
    for key, (pe, _) in arms.items():
        rec = run(key, RHO, pe)
        recs.append(rec)
        print(f"  {key:<18} p4 {pe:.6f}  added {rec['added_M']:.4f}M  (G3 rate {rec['g3_rate_attriters_M']:.4f}M, "
              f"later {rec['later_loss_attriters_M']:.4f}M)", flush=True)
    with (OUT / "population_arms.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        w.writerows(stored)
        w.writerows({c: fmt(r[c]) for c in cols} for r in recs)
    with (OUT / "arms_vhb.csv").open("w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["arm", "p4_effective", "relative_step_from_p3", "rule"])
        w.writerow(["b_one_step (v5 central)", repr(PR.p_eff(S["b_one_step"], p3, RHO)), repr(1 - lo["mex_mex_G3plus"]),
                    "p3 x (1 - 0.1204), held for G5+"])
        for key, (pe, rule) in arms.items():
            w.writerow([key, repr(pe), repr(pe / p3), rule])
        w.writerow(["k_cps", repr(k_cps), "", f"ln(p3 / G1_CPS {g1_cps}) / ln(G3_VHB / G1_VHB)"])
        w.writerow(["k_dt", repr(k_dt), "", f"ln(p3) / ln(p3_DT {p3_dt})"])

    # ---- account frame: main_case_lineage_2026_10_05/population.py main(), pointed here
    print("[account frame: main_case_lineage population.py]", flush=True)
    POPM = load("main_case_lineage_population", LIN5_DIR / "population.py")
    POPM.ARMS = OUT / "population_arms.csv"
    POPM.OUT = OUT
    POPM.PRICED = {**POPM.PRICED, **{k: (k, RHO) for k in arms}}
    argv, sys.argv = sys.argv, [str(LIN5_DIR / "population.py")]
    try:
        POPM.main()
    finally:
        sys.argv = argv
    mine = json.loads((OUT / "population.json").read_text())
    theirs = json.loads((LIN5_DIR / "derived/population.json").read_text())
    for k in ("floor", "a", "b", "c"):
        gate(f"account-frame arm {k} equals main_case_lineage population.json exactly", mine["arms"][k] == theirs["arms"][k],
             f"added {mine['arms'][k]['added']:,.1f}")
    gate("population.json meta and C3 equal the lineage lane's", mine["meta"] == theirs["meta"] and mine["c3"] == theirs["c3"]
         and mine["fractional_ancestry"] == theirs["fractional_ancestry"])
    gate("arm b on the account's frame is 3,039,719.6", f"{mine['arms']['b']['added']:.1f}" == "3039719.6")
    # Sensitivity: later losses close C3 of the gap as G3-rate attriters do (v5 prices them as identified G3+ members).
    # VHB's arms move most added persons into that class, and VHB find non-identification rises with schooling.
    for k in LATER_C3:
        a = mine["arms"][k]
        mine["arms"][f"{k}_later_c3"] = {**a, "g3_rate": a["added"], "later": 0.0,
                                         "rule": f"arm {k}'s persons, every one priced at (1 - C3) G3+ + C3 W"}
    (OUT / "population.json").write_text(json.dumps(mine, indent=1) + "\n")
    (OUT / "gates_arms.json").write_text(json.dumps({"gates": GATES}, indent=1) + "\n")
    if not all(g["passed"] for g in GATES):
        raise SystemExit(f"[BLOCKED] {sum(not g['passed'] for g in GATES)} gate(s) failed")
    print("[arms on the account's frame]")
    for k, a in mine["arms"].items():
        print(f"  {k:<18} added {a['added'] / 1e6:.4f}M  G3 rate {a['g3_rate'] / 1e6:.4f}M  later {a['later'] / 1e6:.4f}M  "
              f"lineage {a['population'] / 1e6:.4f}M")


if __name__ == "__main__":
    main()
