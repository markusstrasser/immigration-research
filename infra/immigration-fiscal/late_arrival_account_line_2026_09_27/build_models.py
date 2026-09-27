"""Step 2: the explorer's model split into one model per generation.

Reads the executed model (assumption_explorer_2026_09_21/derived/model.json, built by build_model.py from
the receipt, spending, benefit and complete-account producers and the justice and uncompensated-care
lanes) and this lane's generation key shares (keys.py) and production attribution (production.py). Every
cell's target amount is split by its key's generation shares for that allocation; other_bn becomes
everyone outside the generation, so each model still conserves its national totals. P and F are the
production attribution. Nothing upstream is edited or re-run.
Gates (exit 1): summed line by line, cell by cell, the three models reproduce model.json's target amounts
(1e-9 bn) and its production arrays (1e-12 bn), under both conventions.
Outputs: derived/model_G1.json, model_G2.json, model_G3plus.json (convention a: own generation) and
derived/model_b_G1.json, model_b_G2.json, model_b_G3plus.json (convention b: minors with their parents).
Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/generation_account_2026_09_24/build_models.py
"""
from __future__ import annotations

import copy
import json
import sys

import numpy as np

import frame as F

MODEL = F.FISCAL / "assumption_explorer_2026_09_21/derived/model.json"
LABELS = {"G1": "Mexico-born (first generation)",
          "G2": "US-born with a Mexico-born parent (second generation)",
          "G3plus": "US-born of US-born parents, Mexican origin (third-plus generation)",
          # Late-arrival lane: the G1 cells (frame.py).
          **{g: f"Mexico-born, cell {g} (arrival class and current age; frame.py)" for g in F.G1_CELLS}}
CONVENTIONS = {"a": "each person in their own generation",
               "b": "minors in their parents' generation (National Academies 2017, pp. 387-388)"}


def split_cell(cell, s):
    target = cell["target_bn"] * s
    out = dict(cell)
    out["target_bn"] = target
    out["other_bn"] = cell["other_bn"] + cell["target_bn"] - target
    out["share"] = cell["share"] * s
    return out


def main():
    model = json.loads(MODEL.read_text())
    keys = json.loads((F.OUT / "generation_key_shares.json").read_text())
    shares, meta = keys["shares"], keys["meta"]
    production = json.loads((F.OUT / "production_by_generation.json").read_text())
    fails = []
    for conv in ("a", "b"):
        models = {g: copy.deepcopy(model) for g in F.GENS}
        for j, g in enumerate(F.GENS):
            mg = models[g]
            mg["meta"]["target"] = LABELS[g]
            mg["meta"]["generation"] = g
            mg["meta"]["convention"] = CONVENTIONS[conv]
            mg["meta"]["union_population"] = model["meta"]["target_population"]
            mg["meta"]["target_population"] = meta["population"][conv][j]
            mg["meta"]["split_by"] = "infra/immigration-fiscal/late_arrival_account_line_2026_09_27/build_models.py"
            for li, line in enumerate(model["receipts"]["lines"]):
                for sc, cells in line["cells"].items():
                    for a, cell in cells.items():
                        s = shares["receipt"][a][cell["key"]][conv][j]
                        mg["receipts"]["lines"][li]["cells"][sc][a] = split_cell(cell, s)
            for li, line in enumerate(model["spending"]["lines"]):
                for key, cells in line["keys"].items():
                    for a, cell in cells.items():
                        s = shares["spending"][a][key][conv][j]
                        mg["spending"]["lines"][li]["keys"][key][a] = split_cell(cell, s)
            series = production["series"][conv][g]
            mg["production"]["private_wtp_bn"] = series["P"]
            mg["production"]["induced_receipts_bn"] = series["F"]
            mg["production"]["sampling_se_bn"] = [None] * len(series["P"])
            mg["production"]["attribution"] = production["meta"]["method"]
        # Gates: line by line and cell by cell the generations add to the union.
        worst = 0.0
        for li, line in enumerate(model["receipts"]["lines"]):
            for sc, cells in line["cells"].items():
                for a, cell in cells.items():
                    total = sum(models[g]["receipts"]["lines"][li]["cells"][sc][a]["target_bn"] for g in F.GENS)
                    worst = max(worst, abs(total - cell["target_bn"]))
        for li, line in enumerate(model["spending"]["lines"]):
            for key, cells in line["keys"].items():
                for a, cell in cells.items():
                    total = sum(models[g]["spending"]["lines"][li]["keys"][key][a]["target_bn"] for g in F.GENS)
                    worst = max(worst, abs(total - cell["target_bn"]))
        ok = worst < 1e-9
        print(f"  {'✓' if ok else '✗'} ({conv}) every receipt and spending cell: generations sum to model.json — max |diff| {worst:.1e} bn")
        if not ok:
            fails.append(f"cells {conv}")
        for field in ("private_wtp_bn", "induced_receipts_bn"):
            total = np.sum([models[g]["production"][field] for g in F.GENS], axis=0)
            err = float(np.max(np.abs(total - np.array(model["production"][field]))))
            ok = err < 1e-12
            print(f"  {'✓' if ok else '✗'} ({conv}) production {field}: generations sum to model.json — {err:.1e} bn")
            if not ok:
                fails.append(f"production {field} {conv}")
        pops = sum(models[g]["meta"]["target_population"] for g in F.GENS)
        if abs(pops - model["meta"]["target_population"]) > 1e-3:
            fails.append(f"population {conv}")
        prefix = "model_" if conv == "a" else "model_b_"
        for g in F.GENS:
            (F.OUT / f"{prefix}{g}.json").write_text(json.dumps(models[g], sort_keys=True, separators=(",", ":")) + "\n")
    if fails:
        print(f"✗ gates failed: {fails}")
        sys.exit(1)
    print("  ✓ all model gates passed")


if __name__ == "__main__":
    main()
