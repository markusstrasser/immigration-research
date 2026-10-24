"""Reference for the independent-price check: what the r2 land lane charges in its five largest counties.

For each top-five county (r2 screen, high end, bound rates): the charge, its share, urban acres by price class, and the
acre-weighted FHFA 2024 as-is urban price per acre the lane applied before its class factors. Workers compare their
independent prices with `fhfa_urban_p24_per_acre`; `test.py` applies the pre-registered rule.

    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/land_price_check_2026_10_24/reference.py
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
R2 = HERE.parent / "land_price_rule_r2_2026_10_24"
sys.path.insert(0, str(R2))
import build  # noqa: E402

r1, d, h, coef, level, acs = build.prepare()
cfg = build.r2_cfgs(r1.FARM["us_share"])["central"]
ch = build.charges(d, cfg, build.rates()["bound"])
summary = json.loads((R2 / "derived" / "summary.json").read_text())
top5 = summary["screen"]["influence"]["top5"]
total = build.total(ch)
for i, end in enumerate(["low", "high"]):
    stored = summary["screen"]["influence"]["without_top5_bn"][i]
    left = float(ch[end][~d.county.isin(top5)].sum())
    if abs(left - stored) > 1e-9:
        raise ValueError(f"[BLOCKED] reference does not reproduce r2's drop-five residual at the {end} end")
rows = []
for c in top5:
    m = d.county.eq(c) & d.priced_rule
    ua = d.loc[m, "urban_acres"] * (1 - d.loc[m, "water_frac"])
    p = d.loc[m, "urban_p24"]
    by_class = d.loc[m].assign(ua=ua).groupby("class_r2").ua.sum().round(1).to_dict()
    rows.append(dict(county=c,
                     charge_low_bn=float(ch["low"][m].sum()), charge_high_bn=float(ch["high"][m].sum()),
                     share_high=float(ch["high"][m].sum()) / total[1],
                     urban_acres=float(ua.sum()), rural_acres=float(d.loc[m, "rural_acres"].sum()),
                     fhfa_urban_p24_per_acre=float(np.average(p.fillna(0), weights=ua)) if ua.sum() > 0 else float("nan"),
                     urban_acres_by_class=json.dumps(by_class, sort_keys=True)))
with open(HERE / "derived" / "reference_top5.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
(HERE / "derived" / "reference_total.json").write_text(json.dumps({"total_bn": total, "top5": top5}, indent=1) + "\n")
print(pd.DataFrame(rows).drop(columns="urban_acres_by_class").to_string())
