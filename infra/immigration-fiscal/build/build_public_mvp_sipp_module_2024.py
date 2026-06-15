#!/usr/bin/env python3
"""Build SIPP 2024 working-age transition cells (98-cell target grid).

Spec: research/immigration-public-mvp-variable-dictionary-2026-04-11.md
"""
from __future__ import annotations

import csv
import io
import json
import zipfile
from pathlib import Path

from public_mvp_io import (
    PROTO,
    SIPP_SCHEMA,
    SIPP_ZIP,
    sipp_eeduc_bucket,
    sipp_working_age_band,
    weighted_mean,
    write_meta,
)

OUT = PROTO / "sipp_public_mvp_cells_2024.csv"
META = PROTO / "sipp_public_mvp_cells_2024.meta.json"

COLS = (
    "WPFINWGT",
    "TAGE",
    "EBORNUS",
    "ECITIZEN",
    "EEDUC",
    "TYRENTRY",
    "TPEARN",
    "TSNAP_AMT",
    "TTANF_AMT",
    "TSSI_AMT",
    "TPTOTINC",
)


def _load_indices() -> dict[str, int]:
    schema = json.loads(SIPP_SCHEMA.read_text())
    names = [r["name"] for r in schema]
    return {c: names.index(c) for c in COLS}


def _num(raw: str) -> float | None:
    raw = (raw or "").strip()
    if not raw:
        return None
    try:
        v = float(raw)
    except ValueError:
        return None
    return v if v >= 0 else None


def build() -> Path:
    PROTO.mkdir(parents=True, exist_ok=True)
    idx = _load_indices()
    cells: dict[tuple, dict] = {}
    n_rows = 0

    with zipfile.ZipFile(SIPP_ZIP) as zf:
        with zf.open("pu2024.csv") as fh:
            rdr = csv.reader(io.TextIOWrapper(fh, encoding="latin-1", newline=""), delimiter="|")
            for row in rdr:
                n_rows += 1
                if len(row) < max(idx.values()) + 1:
                    continue
                age = _num(row[idx["TAGE"]])
                wt = _num(row[idx["WPFINWGT"]])
                if age is None or wt is None or wt <= 0:
                    continue
                age_i = int(age)
                band = sipp_working_age_band(age_i)
                if band is None:
                    continue
                eb = row[idx["EBORNUS"]].strip()
                ec = row[idx["ECITIZEN"]].strip()
                ed = row[idx["EEDUC"]].strip()
                if not eb or not ed:
                    continue
                try:
                    ed_bucket = sipp_eeduc_bucket(int(float(ed)))
                except ValueError:
                    continue
                key = (band, eb, ed_bucket)
                c = cells.setdefault(
                    key,
                    {
                        "age_band": band,
                        "nativity_code": eb,
                        "nativity_label": "1 US-born" if eb == "1" else "2 foreign-born",
                        "citizenship_code": ec,
                        "education_bucket": ed_bucket,
                        "person_weight_sum": 0.0,
                        "person_month_rows": 0,
                        "sum_tpearn": 0.0,
                        "sum_tptotinc": 0.0,
                        "sum_tsnap": 0.0,
                        "sum_ttanf": 0.0,
                        "sum_tssi": 0.0,
                        "pos_tsnap_wt": 0.0,
                        "pos_ttanf_wt": 0.0,
                        "pos_tssi_wt": 0.0,
                        "recent_arrival_wt": 0.0,
                    },
                )
                c["person_weight_sum"] += wt
                c["person_month_rows"] += 1
                tpe = _num(row[idx["TPEARN"]])
                tpt = _num(row[idx["TPTOTINC"]])
                snap = _num(row[idx["TSNAP_AMT"]])
                tanf = _num(row[idx["TTANF_AMT"]])
                ssi = _num(row[idx["TSSI_AMT"]])
                yrentry = _num(row[idx["TYRENTRY"]])
                if tpe is not None:
                    c["sum_tpearn"] += tpe * wt
                if tpt is not None:
                    c["sum_tptotinc"] += tpt * wt
                if snap is not None:
                    c["sum_tsnap"] += snap * wt
                    if snap > 0:
                        c["pos_tsnap_wt"] += wt
                if tanf is not None:
                    c["sum_ttanf"] += tanf * wt
                    if tanf > 0:
                        c["pos_ttanf_wt"] += wt
                if ssi is not None:
                    c["sum_tssi"] += ssi * wt
                    if ssi > 0:
                        c["pos_tssi_wt"] += wt
                if yrentry is not None and yrentry >= 2014 and eb == "2":
                    c["recent_arrival_wt"] += wt

    rows = []
    for _, c in sorted(cells.items()):
        w = c["person_weight_sum"]
        rows.append(
            {
                "age_band": c["age_band"],
                "nativity_code": c["nativity_code"],
                "nativity_label": c["nativity_label"],
                "citizenship_code": c["citizenship_code"],
                "education_bucket": c["education_bucket"],
                "sipp_person_weight_sum": w,
                "person_month_rows": c["person_month_rows"],
                "mean_monthly_tpearn": weighted_mean(c["sum_tpearn"], w),
                "mean_monthly_tptotinc": weighted_mean(c["sum_tptotinc"], w),
                "mean_monthly_tsnap_amt": weighted_mean(c["sum_tsnap"], w),
                "mean_monthly_ttanf_amt": weighted_mean(c["sum_ttanf"], w),
                "mean_monthly_tssi_amt": weighted_mean(c["sum_tssi"], w),
                "share_positive_tsnap_pct": 100 * c["pos_tsnap_wt"] / w if w else None,
                "share_positive_ttanf_pct": 100 * c["pos_ttanf_wt"] / w if w else None,
                "share_positive_tssi_pct": 100 * c["pos_tssi_wt"] / w if w else None,
                "share_recent_arrival_foreign_pct": 100 * c["recent_arrival_wt"] / w
                if w and c["nativity_code"] == "2"
                else None,
            }
        )

    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    write_meta(
        META,
        {
            "builder": "build_public_mvp_sipp_module_2024.py",
            "source_zip": str(SIPP_ZIP),
            "person_month_rows_scanned": n_rows,
            "cells_written": len(rows),
            "target_cells": 98,
            "output_csv": str(OUT),
            "grid": "7 age bands × 2 nativity × 7 education buckets (working age 25-64)",
            "notes": "TPEARN/TPTOTINC are monthly; EBORNUS 2 = foreign-born inference.",
        },
    )
    print(f"Wrote {OUT} ({len(rows)} cells from {n_rows:,} person-month rows)")
    return OUT


if __name__ == "__main__":
    build()
