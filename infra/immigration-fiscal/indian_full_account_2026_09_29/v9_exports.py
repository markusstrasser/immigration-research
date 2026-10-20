"""Full-precision own-key v9 changes and Indian-minus-white annual cost gaps."""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path

ITEMS = {"13", "14", "15", "18", "20", "21"}
TOLERANCE = 1e-9


def records(results):
    """Check the source-typed changes before publishing their gap decomposition."""
    items, gaps = [], []
    for (basis, group, end), (row, _, _) in results.items():
        if not group.startswith(("indian_origin", "india_born", "A1_")):
            continue
        changes = row["v9_items"]
        parts = row["v9_service_parts"]
        if set(changes) != ITEMS or not all(math.isfinite(value) for value in changes.values()):
            raise SystemExit(f"[BLOCKED] {group}: incomplete own-key v9 item map")
        for item in sorted(ITEMS, key=int):
            amount = sum(part["delta_bn"] for part in parts if str(part["item"]) == item)
            if abs(amount - changes[item]) > TOLERANCE:
                raise SystemExit(f"[BLOCKED] {group}: typed item{item} parts do not close")
        if abs(row["cost"] - row["v9_before_cost_bn"] - sum(changes.values())) > TOLERANCE:
            raise SystemExit(f"[BLOCKED] {group}: own-key v9 before/after does not close")
        college = {part["kind"] for part in parts if str(part["item"]) == "15"}
        if not {"college_operating", "college_capital"} <= college:
            raise SystemExit(f"[BLOCKED] {group}: college operating/capital must be priced jointly")
        for part in parts:
            items.append(dict(case="oct16", basis=basis, group=group, end=end,
                              units="USD_bn_per_year", **part))
        if group.startswith("A1_"):
            continue
        white = results[basis, "A1_third_plus_nh_white", end][0]
        scale = row["population"] / white["population"]
        before = row["v9_before_cost_bn"] - scale * white["v9_before_cost_bn"]
        after = row["cost"] - scale * white["cost"]
        contributions = {item: changes[item] - scale * white["v9_items"][item]
                         for item in sorted(ITEMS, key=int)}
        if abs(after - before - sum(contributions.values())) > TOLERANCE:
            raise SystemExit(f"[BLOCKED] {group}: Indian-minus-white v9 gap does not close")
        gaps.append(dict(case="oct16", basis=basis, group=group, end=end,
                         units="USD_bn_per_year", population=row["population"],
                         white_population=white["population"], white_scale=scale,
                         before_bn=before, after_bn=after, change_bn=after-before,
                         change_by_item_bn=contributions,
                         scope="own fiscal evaluator, v8 policies versus v9 on the same own keys/counts; comparator item11 separate",
                         indian_item11="unmeasured, sign and size unidentified",
                         calibration_and_PES="Mexican-specific16/17 not transferred"))
    if not items or not gaps:
        raise SystemExit("[BLOCKED] no Indian own-key v9 evidence to export")
    return dict(case="oct16", tolerance_bn=TOLERANCE, item_parts=items,
                indian_minus_white_gap=gaps,
                college_rule="net operating and capital together; tuition and Pell retain their existing rules",
                mortality="whole-population tables for both evaluator references",
                units="USD_bn_per_year; modeled income-year2024 annual account")


def write(out: Path, results):
    evidence = records(results)
    (out / "v9_own_key_changes.json").write_text(json.dumps(evidence, indent=2) + "\n")
    rows = evidence["item_parts"]
    fields = list(dict.fromkeys(key for row in rows for key in row))
    with (out / "v9_own_key_parts.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
