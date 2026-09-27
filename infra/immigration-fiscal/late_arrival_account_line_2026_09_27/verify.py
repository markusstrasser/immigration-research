"""Re-derive the Mexico-born total from the late-arrival subgroup plus its complement and match it to the
generation lane's Mexico-born (G1) line for the same case, both conventions, both band ends (1e-6 bn).

Sources: this lane's _cache/cells_<case>_<reading>.json (full precision; every reading, since the readings
only move persons between G1 cells) and derived/late_arrival_line.csv (six decimals, checked to 1e-5); the
generation lane's derived/generation_summary.json (read-only), which holds one case, named in its `case`.
A case the generation lane has not run is reported [PENDING] and checked only against the case's published
band (main_case_bands.csv, row `adopted`, the nine cells summed). Exit 1 on any failure.
Run from the repository root:
  uv run --no-project python3 infra/immigration-fiscal/late_arrival_account_line_2026_09_27/verify.py
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
GEN = FISCAL / "generation_account_2026_09_24/derived/generation_summary.json"
MAIN = {"sept27": "main_case_long_run_2026_09_27", "sept26_schools": "main_case_schools_full_2026_09_26"}
LATE = ["G1_L50_50_64", "G1_L50_65p", "G1_L55_55_64", "G1_L55_65p"]
REST = ["G1_Y_u50", "G1_Y_50_64", "G1_Y_65p"]
fails = []


def check(label, ok, detail=""):
    print(f"  {'✓' if ok else '✗'} {label}{' — ' + detail if detail else ''}")
    if not ok:
        fails.append(label)


def main():
    gen = json.loads(GEN.read_text())
    line = list(csv.DictReader((HERE / "derived/late_arrival_line.csv").open()))
    for case in MAIN:
        band = next(r for r in csv.DictReader((FISCAL / MAIN[case] / "derived/main_case_bands.csv").open())
                    if r["variant"] == "adopted" and r["profile"] in ("long_run_non_school_full", "cbo_category_lag_non_school_full"))
        for reading in ("central", "lower", "upper"):
            c = json.loads((HERE / "_cache" / f"cells_{case}_{reading}.json").read_text())
            for conv in ("a", "b"):
                cells = c["conventions"][conv]
                for k, end in enumerate(("low", "high")):
                    late = sum(cells[g][end]["cost_bn"] for g in LATE)
                    rest = sum(cells[g][end]["cost_bn"] for g in REST)
                    union = sum(v[end]["cost_bn"] for g, v in cells.items() if g != "union")
                    tag = f"{case} {reading} ({conv}) {end}"
                    check(f"{tag}: the cells add to the case's band ({float(band['cost_low_bn' if k == 0 else 'cost_high_bn']):.4f})",
                          abs(union - float(band["cost_low_bn" if k == 0 else "cost_high_bn"])) < 5.01e-5, f"{union:.6f}")
                    if gen.get("case") == case:
                        ref = gen["conventions"][conv]["G1"]["cost_bn"][k]
                        same_spec = json.dumps(gen["low_spec" if k == 0 else "high_spec"], sort_keys=True) == \
                            json.dumps(c["low_spec" if k == 0 else "high_spec"], sort_keys=True)
                        check(f"{tag}: late + younger = the generation lane's G1 {ref:.6f}", same_spec and abs(late + rest - ref) < 1e-6,
                              f"late {late:.6f} + younger {rest:.6f}; |diff| {abs(late + rest - ref):.1e}")
                    elif reading == "central" and conv == "a" and end == "low":
                        print(f"  [PENDING] {case}: the generation lane holds case {gen.get('case')}, not {case}; "
                              "G1 checked against the case's band only")
                    rows = {r["subgroup"]: float(r["bn"]) for r in line if r["case"] == case and r["reading"] == reading
                            and r["convention"] == conv and r["spec"] == end and r["program"] == "total"}
                    check(f"{tag}: late_arrival_line.csv late50 + younger = mexico_born (1e-5)",
                          abs(rows["late50"] + rows["younger_50p"] + rows["younger_u50"] - rows["mexico_born"]) < 1e-5
                          and abs(rows["mexico_born"] - late - rest) < 1e-5)
    if fails:
        print(f"✗ {len(fails)} check(s) failed")
        sys.exit(1)
    print("  ✓ all checks passed")


if __name__ == "__main__":
    main()
