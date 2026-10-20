"""Export round6 U2 A2's source-line military mask bridge and basis-specific ordering.

Native-First: standard-library CSV/JSON from the validated live fine-cell run.
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SENIORS = {"earlier65p": ("G1_Y_65p",), "late50_65p": ("G1_L50_65p", "G1_L55_65p")}


def write(name, rows):
    with (HERE / "derived" / name).open("w", newline="") as fh:
        columns = list(dict.fromkeys(key for row in rows for key in row))
        writer = csv.DictWriter(fh, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main():
    military, posts, seniors = [], [], []
    for case in ("oct16", "oct16_cash"):
        for reading in ("central", "lower", "upper"):
            c = json.loads((HERE / f"_cache/cells_{case}_{reading}.json").read_text())
            for row in c["v9"]["item13_by_cell"]:
                implied = row["original_line_bn"] * row["fraction"] * (row["response"] - 1)
                if abs(implied - row["delta_bn"]) > 1e-9:
                    raise SystemExit("[BLOCKED] military original line × fraction × response does not close")
                if row["cell"].startswith("G1_"):
                    if abs(row["original_target_bn"] * row["inherited_response"] - row["original_line_bn"]) > 1e-9:
                        raise SystemExit("[BLOCKED] military responsive amount differs from its original assigned target × inherited response")
                    military.append(dict(case=case, reading=reading, **row))
            for row in c["v9"]["item_posts_by_cell"]:
                if row["item"] in ("coverage_tenure", "one_rate"):
                    posts.append(dict(case=case, reading=reading, **row))
            for conv in ("a", "b"):
                cells = c["conventions"][conv]
                for end in ("low", "high"):
                    groups = {}
                    for cell in (g for g in cells if g.startswith("G1_")):
                        original_parts = [r for r in c["v9"]["item13_by_cell"] if r["convention"] == conv
                                          and r["end"] == end and r["cell"] == cell]
                        implied = sum(r["delta_bn"] for r in original_parts)
                        if abs(implied - cells[cell][end]["parts"]["veterans_compensation"]) > 1e-9:
                            raise SystemExit("[BLOCKED] military source-line mask sum differs from priced cell")
                    for name, members in SENIORS.items():
                        n = sum(cells[g]["population"] for g in members)
                        cost = sum(cells[g][end]["cost_bn"] for g in members)
                        item13 = sum(cells[g][end]["parts"]["veterans_compensation"] for g in members)
                        item17 = sum(cells[g][end]["parts"]["coverage_tenure"] for g in members)
                        item20 = sum(cells[g][end]["parts"]["one_rate"] for g in members)
                        row = dict(case=case, reading=reading, convention=conv, end=end, subgroup=name,
                                   population=n, cost_bn=cost, per_member_usd=cost * 1e9 / n,
                                   military_delta_bn=item13, military_delta_per_member_usd=item13 * 1e9 / n,
                                   item17_delta_bn=item17, item20_delta_bn=item20,
                                   without_military_rule_per_member_usd=(cost - item13) * 1e9 / n,
                                   population_scope="identified roster; convention b includes assigned linked members; coverage/calibration unlocated")
                        groups[name] = row
                    difference = groups["late50_65p"]["per_member_usd"] - groups["earlier65p"]["per_member_usd"]
                    before = groups["late50_65p"]["without_military_rule_per_member_usd"] - groups["earlier65p"]["without_military_rule_per_member_usd"]
                    for row in groups.values():
                        seniors.append(dict(**row, late_minus_earlier_usd=difference,
                                            without_military_late_minus_earlier_usd=before))
    sys.path.insert(0, str(HERE.parent / "scripts"))
    from memory_budget import require_within_budget
    physical = require_within_budget("late-arrival military source diagnostics")
    write("item13_original_lines_oct16.csv", military)
    write("items17_20_oct16.csv", posts)
    write("senior_ordering_oct16.csv", seniors)
    print(f"PASS military{len(military)} rows,17/20{len(posts)},senior{len(seniors)}; physical {physical}bytes")


if __name__ == "__main__":
    main()
