#!/usr/bin/env python3
"""Build MEPS HC-251 health-cost module (age × nativity × insurance cells).

Spec: research/immigration-public-mvp-meps-module-2026-04-11.md
"""
from __future__ import annotations

import csv
import zipfile
from collections import defaultdict
from pathlib import Path

from public_mvp_io import (
    MEPS_DAT_ZIP,
    MEPS_SU,
    PROTO,
    meps_age_band,
    meps_insurance_group,
    nativity_group,
    parse_meps_sas_fields,
    weighted_mean,
    write_meta,
)

OUT = PROTO / "meps_health_cost_module_2023.csv"
META = PROTO / "meps_health_cost_module_2023.meta.json"

NEED = (
    "AGE23X",
    "BORNUSA",
    "YRSINUS",
    "INSURC23",
    "PERWT23F",
    "TOTEXP23",
    "TOTSLF23",
    "TOTMCR23",
    "TOTMCD23",
    "TOTPRV23",
    "TOTSTL23",
)


def _num(raw: str) -> float | None:
    raw = raw.strip()
    if not raw:
        return None
    try:
        v = float(raw)
    except ValueError:
        return None
    return v if v >= 0 else None


def build() -> Path:
    PROTO.mkdir(parents=True, exist_ok=True)
    layout = parse_meps_sas_fields(MEPS_SU)
    for name in NEED:
        if name not in layout:
            raise SystemExit(f"missing {name} in {MEPS_SU}")

    def slice_field(line: str, name: str) -> str:
        start, width = layout[name]
        return line[start : start + width]

    cells: dict[tuple, dict] = {}
    yrs_counts: dict[tuple, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    n_rows = 0

    with zipfile.ZipFile(MEPS_DAT_ZIP) as zf:
        name = next(n for n in zf.namelist() if n.lower().endswith(".dat"))
        with zf.open(name) as fh:
            for raw in fh:
                line = raw.decode("latin-1", errors="replace")
                n_rows += 1
                age = _num(slice_field(line, "AGE23X"))
                wt = _num(slice_field(line, "PERWT23F"))
                if age is None or wt is None or wt <= 0:
                    continue
                age_i = int(age)
                born = slice_field(line, "BORNUSA").strip()
                ins = slice_field(line, "INSURC23").strip()
                if not born or not ins:
                    continue
                ins_i = int(float(ins))
                yrs = slice_field(line, "YRSINUS").strip()
                age_band = meps_age_band(age_i)
                nativity_code = born.lstrip("0") or born
                nativity_label = "1 YES" if nativity_code == "1" else "2 NO"
                ins_group = meps_insurance_group(ins_i, age_i)
                ins_label = {
                    1: "1 <65 ANY PRIVATE",
                    2: "2 <65 PUBLIC ONLY",
                    3: "3 <65 UNINSURED",
                }.get(ins_i, str(ins_i))
                key = (age_band, nativity_code, ins_group)
                c = cells.setdefault(
                    key,
                    {
                        "age_band": age_band,
                        "nativity_code": nativity_code,
                        "nativity_label": nativity_label,
                        "nativity_group": nativity_group(nativity_code),
                        "insurance_code": ins_i,
                        "insurance_label": ins_label,
                        "insurance_group": ins_group,
                        "person_weight_sum": 0.0,
                        "person_count": 0,
                        **{f"sum_{m}": 0.0 for m in ("totexp", "totslf", "totmcr", "totmcd", "totprv", "totstl")},
                        **{f"pos_{m}": 0.0 for m in ("totexp", "totslf", "totmcr", "totmcd", "totprv", "totstl")},
                    },
                )
                c["person_weight_sum"] += wt
                c["person_count"] += 1
                for field, short in (
                    ("TOTEXP23", "totexp"),
                    ("TOTSLF23", "totslf"),
                    ("TOTMCR23", "totmcr"),
                    ("TOTMCD23", "totmcd"),
                    ("TOTPRV23", "totprv"),
                    ("TOTSTL23", "totstl"),
                ):
                    val = _num(slice_field(line, field))
                    if val is None:
                        continue
                    c[f"sum_{short}"] += val * wt
                    if val > 0:
                        c[f"pos_{short}"] += wt
                if nativity_code == "2" and yrs:
                    yrs_counts[key][yrs] += wt

    rows = []
    for key, c in sorted(cells.items()):
        w = c["person_weight_sum"]
        top_yrs = ""
        if key in yrs_counts:
            top = sorted(yrs_counts[key].items(), key=lambda x: -x[1])[:3]
            top_yrs = ";".join(f"{code}:{mass:.0f}" for code, mass in top)
        rows.append(
            {
                **{k: c[k] for k in c if not k.startswith(("sum_", "pos_"))},
                "mean_totexp23": weighted_mean(c["sum_totexp"], w),
                "mean_totslf23": weighted_mean(c["sum_totslf"], w),
                "mean_totmcr23": weighted_mean(c["sum_totmcr"], w),
                "mean_totmcd23": weighted_mean(c["sum_totmcd"], w),
                "mean_totprv23": weighted_mean(c["sum_totprv"], w),
                "mean_totstl23": weighted_mean(c["sum_totstl"], w),
                "share_positive_totexp23_pct": 100 * c["pos_totexp"] / w if w else None,
                "share_positive_totmcd23_pct": 100 * c["pos_totmcd"] / w if w else None,
                "top_yrsinus_codes": top_yrs,
            }
        )

    cols = list(rows[0].keys()) if rows else []
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)

    write_meta(
        META,
        {
            "builder": "build_public_mvp_meps_module.py",
            "source_dat_zip": str(MEPS_DAT_ZIP),
            "source_setup": str(MEPS_SU),
            "rows_parsed": n_rows,
            "cells_written": len(rows),
            "output_csv": str(OUT),
            "notes": "Fixed-width parse via official h251su.txt; insurance_group collapses 65+ codes.",
        },
    )
    print(f"Wrote {OUT} ({len(rows)} cells from {n_rows:,} person rows)")
    return OUT


if __name__ == "__main__":
    build()
