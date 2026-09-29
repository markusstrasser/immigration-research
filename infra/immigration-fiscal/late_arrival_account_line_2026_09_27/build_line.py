"""Task 2: the late-arrival line in the main case, by programme, from run_cells.cjs's outputs.

Reads _cache/cells_<case>_<reading>.json (cases sept27 and sept26_schools; readings central, lower, upper) and
writes derived/late_arrival_line.csv: one row per case, age-at-arrival reading, convention, band end,
subgroup and programme, with $bn a year and $ per member. A subgroup is a sum of frame.py's cells; the engine
is linear, so subgroup parts are sums of cell parts (run_cells.cjs gates that the cells add to the union).

Programmes are cost contributions to other US residents: a tax line enters negative (the group's taxes lower
the cost), a spending line positive, the production term negative; `total` is the cell's cost at that end.
`taxes_total` and `services_total` are sums of the lines above them, reported beside the total, never added
to it again.

--set sept29 reads cases sept29 (the main case adopted on 2026-09-29) and sept29_cash (its cash set) and writes
derived/late_arrival_line_sept29.csv, leaving the default file alone. Its per-person figures use the row-4
headcounts (the case's basis), and two more rows sit beside the total, never added to it: `sept27_total`, the same
persons' cost on the September 27 case at the same specification, and `change_from_sept27`.

Run from the repository root:
  uv run --no-project python3 infra/immigration-fiscal/late_arrival_account_line_2026_09_27/build_line.py [--set sept29]
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CASES = ["sept27", "sept26_schools"]
# Each set of cases and its file: the default two, and the v4 cases in a file of their own.
SETS = {"default": (CASES, "late_arrival_line.csv"), "sept29": (["sept29", "sept29_cash"], "late_arrival_line_sept29.csv")}
READINGS = ["central", "lower", "upper"]
SUBGROUPS = {
    "late50": ["G1_L50_50_64", "G1_L50_65p", "G1_L55_55_64", "G1_L55_65p"],
    "late50_65p": ["G1_L50_65p", "G1_L55_65p"],
    "late50_50_64": ["G1_L50_50_64", "G1_L55_55_64"],
    "late55": ["G1_L55_55_64", "G1_L55_65p"],
    "late55_65p": ["G1_L55_65p"],
    "younger_50p": ["G1_Y_50_64", "G1_Y_65p"],
    "younger_50_64": ["G1_Y_50_64"],
    "younger_65p": ["G1_Y_65p"],
    "younger_u50": ["G1_Y_u50"],
    "mexico_born_65p": ["G1_Y_65p", "G1_L50_65p", "G1_L55_65p"],
    "mexico_born": ["G1_Y_u50", "G1_Y_50_64", "G1_Y_65p", "G1_L50_50_64", "G1_L50_65p", "G1_L55_55_64", "G1_L55_65p"],
    "second_generation": ["G2"],
    "third_plus": ["G3plus"],
}
TAXES = ["taxes_income", "taxes_payroll", "taxes_consumption", "taxes_property", "taxes_other_receipts"]
SERVICES = ["education", "services_other"]


def main():
    which = sys.argv[sys.argv.index("--set") + 1] if "--set" in sys.argv else "default"
    if which not in SETS:
        sys.exit(f"--set must be one of {', '.join(SETS)}")
    cases, out_name = SETS[which]
    rows = []
    for case in cases:
        for reading in READINGS:
            f = HERE / "_cache" / f"cells_{case}_{reading}.json"
            if not f.exists():
                sys.exit(f"[BLOCKED] missing {f.name}: run run_split.sh and run_cells.cjs for it first")
            c = json.loads(f.read_text())
            if c["case"] != case or c["def"] != reading:
                sys.exit(f"[BLOCKED] {f.name} holds {c['case']} / {c['def']}")
            programs = c["programs"]
            for conv, cells in c["conventions"].items():
                groups = {**SUBGROUPS, "union": [g for g in cells if g != "union"]}
                for end in ("low", "high"):
                    spec = c["low_spec"] if end == "low" else c["high_spec"]
                    for name, members in groups.items():
                        pop = sum(cells[g]["population"] for g in members)
                        parts = {k: sum(cells[g][end]["parts"][k] for g in members) for k in programs}
                        total = sum(cells[g][end]["cost_bn"] for g in members)
                        if abs(sum(parts.values()) - total) > 1e-9:
                            sys.exit(f"[BLOCKED] parts do not add to the cost: {case} {reading} {conv} {end} {name}")
                        if name == "union" and abs(total - c["union_band_bn"][0 if end == "low" else 1]) > 1e-9:
                            sys.exit(f"[BLOCKED] cells do not add to the case: {case} {reading} {conv} {end}")
                        out = {**parts, "taxes_total": sum(parts[k] for k in TAXES),
                               "services_total": sum(parts[k] for k in SERVICES), "total": total}
                        if which == "sept29":
                            k = 0 if end == "low" else 1
                            out["sept27_total"] = sum(cells[g]["sept27_cost_bn"][k] for g in members)
                            out["change_from_sept27"] = total - out["sept27_total"]
                        for k, v in out.items():
                            rows.append(dict(case=case, reading=reading, convention=conv, spec=end,
                                             allocation=spec["allocation"], subgroup=name, program=k,
                                             bn=f"{v:.6f}", per_person_usd=f"{v * 1e9 / pop:.2f}",
                                             population=f"{pop:.1f}"))
    (HERE / "derived").mkdir(exist_ok=True)
    with (HERE / "derived" / out_name).open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(f"  ✓ wrote derived/{out_name} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
