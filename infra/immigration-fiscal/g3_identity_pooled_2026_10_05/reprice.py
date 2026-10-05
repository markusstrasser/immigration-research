#!/usr/bin/env python3
"""Reprice the identity-loss rows of notes/immigration-dataset-loose-ends-2026-09-30.md by the measured rule.

Rule (carryover_identity_2026_09_27 §2): attriters lost at the G3 rate close c of the identifiers'
gap; later losses close none, so they cost what identified G3+ members cost. c comes from this lane's
pooled estimate. The average resident's cost stands in for the white end, as in the note.
Inputs are the note's: counts (ladder 158), $2,581 / $3,847 per average resident (ladder 269 shared
part), $7,724 / $9,771 per identified G3+ member (generation_results_sept29.csv, convention b),
case $371.4 / $434.8bn on 39.71M (ladder 270 v4).
"""
import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent
c = float(next(r for r in csv.DictReader(open(HERE / "derived/corrected_step.csv"))
               if r["label"] == "pooled_1994_2026_dedup" and r["links"] == "all")["c"])
AVG = (2581, 3847)
G3ID = (7724, 9771)
CASE = (371.4, 434.8)
POP = 39.712493
G3RATE = 0.80  # third-generation attriters, the floor row
ROWS = [("third-plus attriters, floor", 0.80), ("third-plus attriters, central", 1.81),
        ("lineage, identity loss past G3, low", 3.03), ("lineage, identity loss past G3, high", 5.33)]

out = []
for label, n in ROWS:
    rec = {"row": label, "added_m": n, "c": round(c, 4)}
    for i, band in enumerate(("low", "high")):
        g3 = G3ID[i] - c * (G3ID[i] - AVG[i])
        early, later = min(n, G3RATE), max(0.0, n - G3RATE)
        added = (early * g3 + later * G3ID[i]) / 1e3
        rec[f"added_bn_{band}"] = round(added, 2)
        rec[f"excess_over_avg_bn_{band}"] = round(added - n * AVG[i] / 1e3, 2)
        rec[f"per_member_{band}"] = round((CASE[i] + added) / (POP + n) * 1e3)
        rec[f"note_avg_cost_bn_{band}"] = round(n * AVG[i] / 1e3, 2)
    out.append(rec)

with open(HERE / "derived/attriter_pricing.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0]), lineterminator="\n")
    w.writeheader(); w.writerows(out)
for r in out:
    print(r)
