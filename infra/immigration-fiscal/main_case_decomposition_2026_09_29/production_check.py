"""Checks the assumption that puts the production term (P + F) at zero for residents with national per-age earnings.

The engine's P and F come from the stationary two-skill CES model `matched_benefits_2026_09_19/model.py`
(`equilibrium`, `fiscal_and_private`), replayed by `full_account_benefits_2026_09_20/builder.py` into the 3,888
production scenarios. The case evaluates them at the explorer's reference (`assumption_explorer_2026_09_21/
build_model.py` REFERENCE: sigma 2, labor share 0.65, capital_adjustment 1, labor-supply elasticity 0; the package's
stateFor sets only the normalization). Removing the same fraction of both skills' labor there changes no wage and no
capital return: with adjustment 1 the domestic sector has constant returns in labor and capital together
(power = labor_share + adjustment x (1 - labor_share) = 1). This script runs the model on such a slice (the row-4
frame's union share, 0.118353), on the group's own skill fractions (positive control) and on the slice with capital
only partly adjusting (the assumption's failure case).

Gates (exit 1): the slice's private WTP, receipts gain and labor-market transfer saving are 0 within 1e-6bn at the
reference; the group's own fractions give a non-zero receipts gain; the slice with adjustment 0.5 gives a non-zero
private gain. Output: derived/production_check.json. Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/main_case_decomposition_2026_09_29/production_check.py
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # read-only import from another lane: write nothing beside it

import importlib.util  # noqa: E402
import json  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
UPSTREAM = FISCAL / "matched_benefits_2026_09_19"
SLICE = 39712493.3312 / 335543722.179  # the row-4 frame's union share (derived/summary.json frame)
REFERENCE = dict(sigma=2.0, labor_share=0.65, adjustment=1.0, elasticity=0.0)  # build_model.py REFERENCE
TAX_LABOR, TAX_CAPITAL, RETENTION = [.384, .426], .246, 1.0  # full_account_benefits builder.py expand_ownership
FAILS = []


def gate(label, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'} {label}{' — ' + detail if detail else ''}", flush=True)
    if not ok:
        FAILS.append(label)


def main():
    spec = importlib.util.spec_from_file_location("matched_stationary_model", UPSTREAM / "model.py")
    model = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(model)
    comp = pd.read_csv(UPSTREAM / "derived/skill_composition.csv")
    cells = comp[comp.proxy.eq("PEARNVAL") & comp.split.eq("hs_or_less")]
    incomes = cells.pivot(index="skill", columns="group", values="estimate").sort_index()
    shares = incomes.national.to_numpy() / incomes.national.sum()
    group = incomes.target.to_numpy() / incomes.national.to_numpy()
    scale = json.loads((UPSTREAM / "derived/audit.json").read_text())["gdp_billions"]  # $bn, normalization gdp

    def run(fractions, adjustment):
        r = model.equilibrium(shares, np.asarray(fractions, float), REFERENCE["sigma"], REFERENCE["labor_share"],
                              adjustment, REFERENCE["elasticity"])
        f = model.fiscal_and_private(r, TAX_LABOR, TAX_CAPITAL, RETENTION)
        return dict(private_wtp_bn=float(f["private_wtp"] * scale), receipts_gain_bn=float(f["current_receipts_gain"] * scale),
                    transfer_saving_bn=float(scale * np.dot([.038, .010], r["labor_gain"])),
                    wage_without_over_with=[float(x) for x in r["wage_without_over_with"]])

    out = {
        "slice_share": SLICE, "skill_shares": shares.tolist(), "group_fractions": group.tolist(),
        "reference": REFERENCE, "normalization": "gdp", "scale_bn": scale,
        "slice_at_reference": run([SLICE, SLICE], 1.0),
        "group_at_reference": run(group, 1.0),
        "slice_adjustment_0_5": run([SLICE, SLICE], 0.5),
        "slice_adjustment_0": run([SLICE, SLICE], 0.0),
    }
    s = out["slice_at_reference"]
    gate("a proportional slice at the reference moves no factor price (P, F and transfer saving 0 within 1e-6bn)",
         max(abs(s["private_wtp_bn"]), abs(s["receipts_gain_bn"]), abs(s["transfer_saving_bn"])) < 1e-6,
         f"P {s['private_wtp_bn']:.2e}, F {s['receipts_gain_bn']:.2e}, wages {s['wage_without_over_with']}")
    g = out["group_at_reference"]
    gate("positive control: the group's own skill fractions give a non-zero receipts gain", abs(g["receipts_gain_bn"]) > 1,
         f"P {g['private_wtp_bn']:.3f}, F {g['receipts_gain_bn']:.3f}bn")
    h = out["slice_adjustment_0_5"]
    gate("failure case: with capital half adjusting, the slice's private gain is non-zero", abs(h["private_wtp_bn"]) > 1,
         f"P {h['private_wtp_bn']:.2f}, F {h['receipts_gain_bn']:.2f}bn")
    (HERE / "derived").mkdir(exist_ok=True)
    (HERE / "derived/production_check.json").write_text(json.dumps(out, indent=1) + "\n")
    if FAILS:
        print(f"FAIL: {len(FAILS)} gate(s)")
        sys.exit(1)
    print("  all production gates passed")


if __name__ == "__main__":
    main()
