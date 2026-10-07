"""The pension accrual at scheduled benefits on the 2026 inputs, for engine_breaks_sept29.cjs --case oct07 (C1's
pension_scheduled item and C2's tally at scheduled benefits, both beside the case).

Main case v6 (main_case_2026_10_07, item pension_tr2026) values the accrual on the 2026 Trustees' separate-funds arm
at payable benefits, and its scheduled_benefits_arm stays on the 2025 reports (ratio_net 1.2406). The break script's
rule, scheduled less payable, would then mix the 2025 scheduled arm with the 2026 payable one. Here the scheduled arm
is rebuilt on the 2026 inputs the payable arm reads (TR 2026's new-issue rates, Note 2026.3's wage index, Table V.C1's
COLAs and contribution bases, the mortality decline, Medicare TR 2026's HI cost per beneficiary, the tax-on-benefits
share), with no payable cut: Note 2025.7 Table 1 (scheduled) times the lifetime model's k on the 2026 inputs over its
money's-worth ratio on Note 2025.7's basis at the 2025 economy (pension_tr2026.hybrid, as that lane builds the payable
arm); the benefit-tax timing on the 2026 inputs at scheduled benefits; Part A at scheduled benefits on the 2026 HI
costs and mortality. The union's relative benefit-tax rate is the pension lane's measured 0.523382 (2024 benefits).
Trust-fund separation does not enter: scheduled benefits are paid in full on either reading.

The code is the white lane's, imported by file and read-only: accrual_white.py's oasdi_ratio and part_a (whose union
reproduces the pension lane) and tr2026_path.py (pension_tr2026_2026_10_06's own functions, nothing written beside
them).

Gates ([BLOCKED], nothing written):
  - on the 2025 inputs the same code gives the case's scheduled-benefits arm (meta.pension_accrual
    .scheduled_benefits_arm.ratio_net, 1e-6) and the pension lane's scheduled Part A accrual (its summary.json
    scheduled_arm.decomposition.low.part_a_accrual_bn, 1e-6 relative), the file the payload's previous.oct05 pins;
  - on the 2026 inputs at payable benefits it gives the case's ratio_net and Part A accrual, the arm's union row of
    the 2026 lane's arms.csv (tr2026_path.case_check, and this run against that row, 5e-9).
Output: derived/scheduled_tr2026.json. Run from the repository root (under a minute):
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/break_conditions_2026_09_29/scheduled_tr2026.py
"""
from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True   # read-only imports from other lanes: write nothing beside them

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
REPO = FISCAL.parents[1]
WR = FISCAL / "white_replacement_2026_09_28"
CASE_PAYLOAD = FISCAL / "main_case_2026_10_07/derived/corrections.json"
PEN_FILE = FISCAL / "pension_accrual_2026_09_28/derived/summary.json"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


A = load("accrual_white", WR / "accrual_white.py")      # imports the pension lane (A.P)
TP = load("tr2026_path", WR / "tr2026_path.py")         # imports pension_tr2026 (TP.TR)
P, TR, G = A.P, TP.TR, A.G


def blocked(msg):
    raise SystemExit(f"[BLOCKED] {msg}")


def union_ratios(p, grids, taus, econ, scens, u_long, ctx):
    """The union's OASDI accrual per tax dollar, timing, net ratio and Part A accrual for each scenario (A's code)."""
    qq = p[p.union & (p.tax_oasdi > 0)].reset_index(drop=True)
    with ctx():
        o = A.oasdi_ratio(qq, grids, u_long, taus, scens=scens)
        a = {s: A.part_a(p[p.union].copy(), econ, u_long, s) for s in scens}
    rel = A.STORED["rel_union"]
    return {s: dict(per_tax_dollar=o[s]["ratio"], timing=o[s]["timing"],
                    ratio_net=o[s]["ratio"] * (1 - rel * o[s]["timing"]), part_a_bn=a[s]["accrual_bn"],
                    hi_tax_bn=a[s]["hi_tax_bn"]) for s in scens}


def main():
    meta = json.loads(CASE_PAYLOAD.read_text())["meta"]
    pa = meta["pension_accrual"]
    TP.case_check(meta)
    prev = pa["previous"]["oct05"]["source"]
    if hashlib.sha256(PEN_FILE.read_bytes()).hexdigest() != prev["sha256"]:
        blocked(f"{PEN_FILE.relative_to(FISCAL)} is not the file the payload's previous.oct05 pins ({prev['commit']})")
    pen = json.loads(PEN_FILE.read_text())
    q = P.S.quotes()
    u_long = q["note151_eligible_share"]["value"]["end_of_projection"]
    p = P.frame()
    prelim = P.S.scaled_factors().preliminary.to_numpy()

    # The 2025 inputs: accrual_white.main's grids and timing (the pension lane's central).
    econ = P.L.Economy()
    P.GRID = [G, P.BASE]
    g25 = {s: P.model_grid(econ, prelim, P.payable_path(econ) if s == "payable" else None) for s in P.SCENARIOS}
    share = P.tob_share_path() * (1 + P.hi_over_oasdi_tob()) * P.obbba_factor()
    t25 = P.tob_timing(econ, prelim, share, runs=[(G, s) for s in P.SCENARIOS])
    r25 = union_ratios(p, g25, t25, econ, P.SCENARIOS, u_long, contextlib.nullcontext)
    want = pa["scheduled_benefits_arm"]["ratio_net"]
    if abs(r25["scheduled"]["ratio_net"] - want) > 1e-6:
        blocked(f"the 2025 scheduled ratio_net {r25['scheduled']['ratio_net']} is not the case's arm {want}")
    want = pen["scheduled_arm"]["decomposition"]["low"]["part_a_accrual_bn"]
    if abs(r25["scheduled"]["part_a_bn"] / want - 1) > 1e-6:
        blocked(f"the 2025 scheduled Part A accrual {r25['scheduled']['part_a_bn']} is not the pension lane's {want}")
    print(f"[gate] the 2025 inputs give the case's scheduled arm: ratio_net {r25['scheduled']['ratio_net']:.9f}, "
          f"Part A {r25['scheduled']['part_a_bn']:.6f}bn")

    # The 2026 inputs: the payable arm (tr2026_path.payable) and the same inputs at scheduled benefits.
    ea, gpay, tpay, paths = TP.payable(P, prelim)
    e25 = TR.L.Economy()
    den = TR.grid(e25, prelim, None, [G, TR.BASE])       # Note 2025.7's basis at scheduled benefits, the 2025 economy
    with TP.on_path(P, paths):
        gsch = TR.hybrid(TR.grid(ea, prelim, None, [G]), den)
        tsch = P.tob_timing(ea, prelim, TR.tob_share_tr2026(), runs=[(G, "scheduled")])
    r26 = union_ratios(p, {"payable": gpay, "scheduled": gsch}, {**tpay, **tsch}, ea, ("payable", "scheduled"), u_long,
                       lambda: TP.on_path(P, paths))
    row = TP.union_row()
    for k, col in (("per_tax_dollar", "per_tax_dollar"), ("timing", "timing"), ("part_a_bn", "part_a_bn"),
                   ("hi_tax_bn", "hi_tax_bn")):
        if abs(r26["payable"][k] - float(row[col])) > 5e-9 * max(1.0, abs(float(row[col]))):
            blocked(f"the 2026 payable {k} {r26['payable'][k]} is not {TP.ARM}'s union {col} {row[col]}")
    if abs(r26["payable"]["ratio_net"] - pa["ratio_net"]) > 5e-9 or abs(r26["payable"]["part_a_bn"] - pa["part_a_accrual_bn"]) > 5e-8:
        blocked("the 2026 payable run is not the case's ratio_net and Part A accrual")
    print(f"[gate] the 2026 payable run is the case's pension block (ratio_net {r26['payable']['ratio_net']:.9f}, "
          f"Part A {r26['payable']['part_a_bn']:.6f}bn)")
    out = dict(
        question="the pension accrual at scheduled benefits on the 2026 inputs the v6 case's payable arm reads",
        rule="Note 2025.7 Table 1 x k(2026 inputs, scheduled) / mwr(Note 2025.7's basis, 2025 economy, scheduled); "
             "timing at scheduled benefits on the 2026 inputs; Part A at scheduled benefits on the 2026 HI costs and "
             "mortality; net at the union's relative benefit-tax rate",
        relative_benefit_tax_rate_union=A.STORED["rel_union"],
        scheduled_2026=r26["scheduled"], payable_2026=r26["payable"], scheduled_2025=r25["scheduled"],
        payable_2025=r25["payable"],
        case=dict(ratio_net=pa["ratio_net"], part_a_accrual_bn=pa["part_a_accrual_bn"],
                  scheduled_benefits_arm_ratio_net=pa["scheduled_benefits_arm"]["ratio_net"]),
        inputs={str(f.relative_to(REPO)): hashlib.sha256(f.read_bytes()).hexdigest() for f in
                (CASE_PAYLOAD, PEN_FILE, TP.TR_LANE / "derived/arms.csv", WR / "accrual_white.py", WR / "tr2026_path.py")},
    )
    (HERE / "derived/scheduled_tr2026.json").write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    for k in ("scheduled_2025", "payable_2025", "payable_2026", "scheduled_2026"):
        v = out[k]
        print(f"{k}: per tax dollar {v['per_tax_dollar']:.6f}, timing {v['timing']:.6f}, net {v['ratio_net']:.6f}, "
              f"Part A {v['part_a_bn']:.4f}bn")


if __name__ == "__main__":
    main()
