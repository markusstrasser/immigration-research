#!/usr/bin/env python3
"""Bridge SIPP transition cells to MEPS health-cost cells.

Spec: research/immigration-public-mvp-sipp-meps-bridge-2026-04-11.md
"""
from __future__ import annotations

import csv
from pathlib import Path

from public_mvp_io import PROTO, weighted_mean, write_meta

SIPP_IN = PROTO / "sipp_public_mvp_cells_2024.csv"
MEPS_IN = PROTO / "meps_health_cost_module_2023.csv"
BRIDGE_OUT = PROTO / "sipp_meps_bridge_cells_2024.csv"
EXPECTED_OUT = PROTO / "sipp_meps_expected_health_cost_cells_2024.csv"
META = PROTO / "sipp_meps_bridge_cells_2024.meta.json"


def _sipp_to_meps_age(age_band: str) -> str:
    """Map SIPP 5-year bands to MEPS 10-year bands for health-cost match."""
    start = int(age_band.split("-")[0])
    if start < 30:
        return "25-34"
    if start < 40:
        return "35-44"
    if start < 50:
        return "45-54"
    return "55-64"


def _read_csv(path: Path) -> list[dict]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def build() -> tuple[Path, Path]:
    PROTO.mkdir(parents=True, exist_ok=True)
    sipp_rows = _read_csv(SIPP_IN)
    meps_rows = _read_csv(MEPS_IN)

    meps_exact: dict[tuple, list[dict]] = {}
    meps_group: dict[tuple, list[dict]] = {}
    for m in meps_rows:
        key = (m["age_band"], m["nativity_code"])
        meps_exact.setdefault(key, []).append(m)
        gkey = (m["age_band"], m["nativity_group"])
        meps_group.setdefault(gkey, []).append(m)

    bridge_rows: list[dict] = []
    expected_rows: list[dict] = []
    matched_exact = matched_fallback = unmatched = 0

    for s in sipp_rows:
        meps_age = _sipp_to_meps_age(s["age_band"])
        nat = s["nativity_code"]
        match_kind = "exact"
        branches = meps_exact.get((meps_age, nat))
        if not branches:
            match_kind = "group_fallback"
            branches = meps_group.get(
                (meps_age, "us_born" if nat == "1" else "foreign_born")
            )
        if not branches:
            unmatched += 1
            continue
        if match_kind == "exact":
            matched_exact += 1
        else:
            matched_fallback += 1

        sipp_wt = float(s["sipp_person_weight_sum"])
        branch_wt_total = sum(float(b["person_weight_sum"]) for b in branches)
        cell_branches = []
        for b in branches:
            branch_share = float(b["person_weight_sum"]) / branch_wt_total if branch_wt_total else 0
            bridge_wt = sipp_wt * branch_share
            row = {
                "sipp_age_band": s["age_band"],
                "sipp_nativity_code": nat,
                "sipp_education_bucket": s["education_bucket"],
                "sipp_person_weight_sum": sipp_wt,
                "meps_age_band": b["age_band"],
                "meps_nativity_code": b["nativity_code"],
                "meps_insurance_group": b["insurance_group"],
                "match_kind": match_kind,
                "bridge_weight": bridge_wt,
                "mean_totexp23": b["mean_totexp23"],
                "mean_totslf23": b["mean_totslf23"],
                "mean_totmcr23": b["mean_totmcr23"],
                "mean_totmcd23": b["mean_totmcd23"],
                "mean_totprv23": b["mean_totprv23"],
                "mean_totstl23": b["mean_totstl23"],
            }
            bridge_rows.append(row)
            cell_branches.append(row)

        bw = sum(r["bridge_weight"] for r in cell_branches)
        expected_rows.append(
            {
                "sipp_age_band": s["age_band"],
                "sipp_nativity_code": nat,
                "sipp_education_bucket": s["education_bucket"],
                "sipp_person_weight_sum": sipp_wt,
                "match_kind": match_kind,
                "expected_mean_totexp23": weighted_mean(
                    sum(float(r["mean_totexp23"] or 0) * r["bridge_weight"] for r in cell_branches), bw
                ),
                "expected_mean_totmcd23": weighted_mean(
                    sum(float(r["mean_totmcd23"] or 0) * r["bridge_weight"] for r in cell_branches), bw
                ),
                "expected_mean_totprv23": weighted_mean(
                    sum(float(r["mean_totprv23"] or 0) * r["bridge_weight"] for r in cell_branches), bw
                ),
                "expected_mean_totslf23": weighted_mean(
                    sum(float(r["mean_totslf23"] or 0) * r["bridge_weight"] for r in cell_branches), bw
                ),
                "meps_branch_count": len(cell_branches),
            }
        )

    for path, rows in ((BRIDGE_OUT, bridge_rows), (EXPECTED_OUT, expected_rows)):
        with path.open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else [])
            w.writeheader()
            w.writerows(rows)

    write_meta(
        META,
        {
            "builder": "build_public_mvp_sipp_meps_bridge_2024.py",
            "sipp_rows_input": len(sipp_rows),
            "meps_rows_input": len(meps_rows),
            "sipp_rows_matched_exact": matched_exact,
            "sipp_rows_matched_group_fallback": matched_fallback,
            "sipp_rows_unmatched": unmatched,
            "bridge_rows_written": len(bridge_rows),
            "expected_rows_written": len(expected_rows),
            "outputs": [str(BRIDGE_OUT), str(EXPECTED_OUT)],
        },
    )
    print(
        f"Bridge: {len(bridge_rows)} rows, expected: {len(expected_rows)}, "
        f"exact={matched_exact} fallback={matched_fallback} unmatched={unmatched}"
    )
    return BRIDGE_OUT, EXPECTED_OUT


if __name__ == "__main__":
    build()
