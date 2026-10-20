"""Validate live oct16 cells, including separately unlocated source parts.

Native-First: standard-library checks against principal JSON/CSV outputs.
Full precision closure is 1e-9bn; published six-decimal CSVs use 1e-5bn,
the historical four-decimal case-band oracle keeps 5.01e-5bn.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
ROOT = FISCAL.parents[1]
TOPS = ("G1", "G2", "G3plus")
LATE = ("G1_L50_50_64", "G1_L50_65p", "G1_L55_55_64", "G1_L55_65p")
REST = ("G1_Y_u50", "G1_Y_50_64", "G1_Y_65p")


def close(a, b, label, tolerance=1e-9):
    if not math.isfinite(a) or not math.isfinite(b) or abs(a - b) > tolerance:
        raise SystemExit(f"[BLOCKED] {label}: {a} vs {b}")


def main():
    which = sys.argv[sys.argv.index("--set") + 1] if "--set" in sys.argv else "oct16"
    if which != "oct16":
        raise SystemExit(f"[BLOCKED] live case is oct16; {which} outputs are frozen")
    snapshot = json.loads((HERE / "inputs/oct16_source_hashes.json").read_text())
    for rel, expected in snapshot["sha256"].items():
        p = ROOT / rel
        if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest() != expected:
            raise SystemExit(f"[BLOCKED] changed admitted oct16 input {rel}")
    bands = list(csv.DictReader((FISCAL / "main_case_2026_10_16/derived/main_case_bands.csv").open()))
    line = list(csv.DictReader((HERE / "derived/late_arrival_line_oct16.csv").open()))
    checks = 0
    for case in ("oct16", "oct16_cash"):
        gen = json.loads((FISCAL / f"generation_account_2026_09_24/derived/generation_summary_{case}.json").read_text())
        source_specs = json.loads((FISCAL / f"generation_account_2026_09_24/derived/generation_corrections_{case}.json").read_text())["payloads"]["a"]["G1"]["meta"]["v9_specs"]
        band = next(r for r in bands if r["profile"] == "long_run_non_school_full"
                    and r["variant"] == ("cash_set" if case.endswith("_cash") else "adopted"))
        for reading in ("central", "lower", "upper"):
            c = json.loads((HERE / f"_cache/cells_{case}_{reading}.json").read_text())
            if c["case"] != case or c["main"] != gen["lane"] or c["def"] != reading:
                raise SystemExit("[BLOCKED] cell/generation source identity")
            if (c["lo"] != gen["specifications"]["low_index"] or c["hi"] != gen["specifications"]["high_index"]
                    or c["low_spec"] != source_specs[c["lo"]] or c["high_spec"] != source_specs[c["hi"]]):
                raise SystemExit("[BLOCKED] found low/high specification differs from generation source")
            if "passthrough_source_tax" in c["v9"]["selected_items"]:
                raise SystemExit("[BLOCKED] beside item19 entered central")
            for conv in ("a", "b"):
                cells = c["conventions"][conv]
                names = [g for g in cells if g != "union"]
                close(sum(cells[g]["population"] for g in names), gen["union"]["population"], "population", 1e-6)
                for k, end in enumerate(("low", "high")):
                    total = sum(cells[g][end]["cost_bn"] for g in names)
                    close(total, gen["union"]["cost_bn"][k], "case/generation full precision")
                    close(total, float(band[f"cost_{end}_bn"]), "published band", 5.01e-5)
                    close(total, c["union_band_bn"][k], "cell union")
                    for G in TOPS:
                        fine = [g for g in names if g.startswith("G1_")] if G == "G1" else [G]
                        located = sum(cells[g][end]["cost_bn"] for g in fine)
                        unlocated = sum(cells[f"unlocated_{kind}_{G}"][end]["cost_bn"] for kind in ("coverage", "calibration"))
                        close(located + unlocated, gen["conventions"][conv][G]["cost_bn"][k], f"generation {G}")
                        for g in fine:
                            close(cells[g][end]["parts"]["coverage"], 0, "no located coverage")
                            close(cells[g][end]["parts"]["native_minor_calibration"], 0, "no unlocated calibration spread")
                            close(cells[g][end]["parts"]["coverage_tenure"], 0, "no unlocated tenure spread")
                    for g in names:
                        close(sum(cells[g][end]["parts"].values()), cells[g][end]["cost_bn"], f"programme {g}")
                    rows = {r["subgroup"]: float(r["bn"]) for r in line if r["case"] == case
                            and r["reading"] == reading and r["convention"] == conv
                            and r["spec"] == end and r["program"] == "total"}
                    close(rows["mexico_born"], sum(cells[g][end]["cost_bn"] for g in LATE + REST), "published identified G1", 1e-5)
                    close(rows["mexico_born_with_unlocated"], gen["conventions"][conv]["G1"]["cost_bn"][k], "published whole G1", 1e-5)
                    close(rows["union"], total, "published union", 1e-5)
                    checks += 1
    sys.path.insert(0, str(FISCAL / "scripts"))
    from memory_budget import require_within_budget
    physical = require_within_budget("late-arrival oct16 verification")
    print(f"PASS {checks} case/reading/convention/end contexts; full closure1e-9bn, CSV1e-5bn; physical {physical}bytes")


if __name__ == "__main__":
    main()
