#!/usr/bin/env python3
"""Independent, descriptive F-33 school spending reconstruction.

No production estimator, parser or derived estimate is imported. Original files
are verified against fixed hashes and the existing source manifest. Run from the
main checkout with uv run --no-project --with scipy --with xlrd python3 PATH
--data-root MAIN_REPO --out-dir OUTPUT. Dollar amounts in files are thousands;
the factor 1000 cancels from every log slope. State intercepts absorb common
state price levels (cross section) or changes (long differences), including a
common inflation adjustment. They do NOT absorb district-specific price changes.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import t


BASE = Path("infra/immigration-fiscal/school_dilution_2026_09_24")
PINS = {
    "elsec00.txt": "75c2641e339890b50732c570692274b36c97b76371ae8ed61e181b3ea2d9d1d5",
    "elsec10.txt": "5bebf41c59ddb0f8ddc4e00070abbcb522237fec1c9febac9078d8e3fc841896",
    "elsec19.txt": "0d3fe071e52fa01d40b5dddaabfe0e07c997a593b740d9c35b3c240a137ddb09",
    "elsec10_sttables.xls": "147511becbc8e968986f3df6db88f6afe19175076040025ded0c3d0f4d6be7cf",
    "elsec19_sumtables.xls": "96807e7c1cb6b6390439f92310fc82d04df8be7e1a55d1b4c6a135ed431e76fc",
    "school15doc.pdf": "824553b59165613a1a4909084ee7dc9b8969228596d6dd1db8010421c0e0f9c8",
}
NUMERIC = ("V33", "TCURELSC", "TCURINST", "TCURSSVC", "TCUROTH")
FIELDS = ("NCESID", "IDCENSUS", "SCHLEV", "YRDATA", *NUMERIC)
STATE_FIPS = {
    "01", "02", "04", "05", "06", "08", "09", "10", "11", "12", "13",
    "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25",
    "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36",
    "37", "38", "39", "40", "41", "42", "44", "45", "46", "47", "48",
    "49", "50", "51", "53", "54", "55", "56",
}
METHOD = {
    "purpose": "Descriptive audit of the association behind the school-response assumption; not a causal estimate of group removal.",
    "declared_before_regressions": True,
    "inputs": "Original Census F-33 2000, 2010 and 2019 CSVs; official Table 8 workbooks; original documentation.",
    "selection": "Each year: SCHLEV 01/02/03, unique valid seven-digit NCESID, 50 states excluding DC, own-year V33 >= 100, positive TCURELSC and TCURINST. Every YRDATA must match its file.",
    "models": "2019 log spending on log enrollment with state intercepts; matched-ID 2000-2019, 2000-2010, 2010-2019 log differences with state intercepts.",
    "weights": "Equal district weight and baseline pupil weight; current pupils for cross section. WLS weights are normalized to mean one with no effect on slope or CR1 covariance.",
    "sensitivities": "Separate growth and shrinkage regressions (each with its own state intercepts) in every long difference; 2000-2019 stable SCHLEV and IDCENSUS, abs(dlog enrollment) <= log(2), and both restrictions. No outcome-tail trimming.",
    "california_sensitivity": "After the initial raw estimates, an additional source-driven check excludes California for the 2000-2019 pupil-weighted current/instruction regressions only. Census school19doc.doc Appendix B says over 900 California charters were reclassified out of governmental-system coverage in FY2019, producing substantial per-pupil finance and enrollment changes. This addition is post-result, not preregistered. It does not replace the full sample.",
    "california_source": "https://www2.census.gov/programs-surveys/school-finances/tables/2019/secondary-education-finance/school19doc.doc",
    "outcomes": "TCURELSC (current spending) and TCURINST (instruction). Instruction is an input-composition check, not an educational-quality outcome.",
    "inference": "State-cluster sandwich CR1: G/(G-1)*(N-1)/(N-(G+1)); t intervals with G-1 df. These are model-based regression uncertainty, not F-33 sampling variance or causal-identification uncertainty.",
    "inflation": "Nominal dollars: common state-level price levels or changes are absorbed by the state intercepts. No claim that district-specific inflation is removed.",
    "validation": "Verify raw source hashes and unique IDs; identity TCURELSC=TCURINST+TCURSSVC+TCUROTH; compare all positive-enrollment-unit pp to original Table 8 without calibration. Published pp exclude spending for students outside reported enrollment, so mismatch is reported, not silently adjusted.",
    "limits": "Matched IDs do not establish stable district geography; survival, migration, funding rules, prices and service mix remain confounders. Baseline pupil weights are not population-removal weights. Results do not identify school quality, a finite removal response or national equilibrium effects.",
}


def dump_json(path: Path, obj: object) -> None:
    path.write_text(json.dumps(obj, indent=2, sort_keys=True, allow_nan=False) + "\n")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_sources(root: Path) -> dict:
    lane = root / BASE
    manifest_path = lane / "derived/sources_f33.json"
    manifest = json.loads(manifest_path.read_text())
    records = {item["file"]: item for item in manifest}
    selected = []
    for name, pin in PINS.items():
        item = records[name]
        path = lane / "_cache/f33" / name
        actual = sha256(path)
        if item["sha256"] != pin or actual != pin:
            raise ValueError(f"[BLOCKED] source hash mismatch: {name}")
        selected.append({**item, "checked_sha256": actual})
    text_path = lane / "_cache/f33/school15doc.txt"
    return {
        "manifest_path": str(BASE / "derived/sources_f33.json"),
        "manifest_sha256": sha256(manifest_path),
        "fixed_manifest_subset": selected,
        "documentation_text": {
            "file": "school15doc.txt", "sha256": sha256(text_path),
            "note": "Local text extraction; original PDF independently hash-pinned above.",
        },
    }


def parse_raw(path: Path, year: int) -> tuple[pd.DataFrame, dict]:
    """Name-based CSV parsing preserves zeros; only trailing empty cells allowed."""
    parsed = []
    blank_trailer_rows = 0
    flag_counts: dict[str, int] = {}
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        missing = set(FIELDS) - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"[BLOCKED] missing columns {sorted(missing)}")
        for line_number, row in enumerate(reader, 2):
            trailer = row.pop(None, [])
            if any(value.strip() for value in trailer):
                raise ValueError(f"[BLOCKED] unexpected extra data at {path}:{line_number}")
            blank_trailer_rows += bool(trailer)
            if any(row.get(key) is None for key in FIELDS):
                raise ValueError(f"[BLOCKED] truncated data at {path}:{line_number}")
            unit = {key: row[key].strip() for key in FIELDS}
            if unit["YRDATA"] != f"{year % 100:02d}":
                raise ValueError(f"[BLOCKED] stale YRDATA at {path}:{line_number}")
            for key in NUMERIC:
                unit[key] = float(unit[key])
                if not math.isfinite(unit[key]):
                    raise ValueError(f"[BLOCKED] nonfinite {key} at {path}:{line_number}")
            if "FL_V33" in row:
                flag = row["FL_V33"].strip()
                flag_counts[flag] = flag_counts.get(flag, 0) + 1
            parsed.append(unit)
    frame = pd.DataFrame(parsed)
    valid = frame.NCESID.str.fullmatch(r"[0-9]{7}")
    if frame.loc[valid, "NCESID"].duplicated().any():
        raise ValueError(f"[BLOCKED] duplicate valid NCESID in {year}")
    frame["state"] = frame.NCESID.str[:2]
    if not frame.loc[valid, "state"].isin(STATE_FIPS).all():
        raise ValueError(f"[BLOCKED] unrecognized NCES state in {year}")
    residual = frame.TCURELSC - frame.TCURINST - frame.TCURSSVC - frame.TCUROTH
    if residual.abs().max() > 2:
        raise ValueError(f"[BLOCKED] material component identity discrepancy in {year}")
    coverage = {
        "year": year, "raw_rows": len(frame), "trailing_blank_rows": blank_trailer_rows,
        "valid_unique_nces_ids": int(valid.sum()), "invalid_nces_ids": int((~valid).sum()),
        "component_identity_max_abs_thousand_dollars": float(residual.abs().max()),
        "component_identity_nonzero_rows": int(residual.ne(0).sum()),
        "enrollment_flag_counts": flag_counts or {"not_in_this_file": len(frame)},
        "all_positive_enrollment_rows": int(frame.V33.gt(0).sum()),
        "all_positive_enrollment_pupils": float(frame.loc[frame.V33.gt(0), "V33"].sum()),
    }
    return frame, coverage


def analysis_sample(frame: pd.DataFrame) -> tuple[pd.DataFrame, list[dict]]:
    sample = frame.copy()
    checks = [
        ("direct_public_level_01_02_03", sample.SCHLEV.isin(["01", "02", "03"])),
        ("valid_seven_digit_nces_id", sample.NCESID.str.fullmatch(r"[0-9]{7}")),
        ("exclude_dc", sample.state.ne("11")),
        ("own_year_enrollment_at_least_100", sample.V33.ge(100)),
        ("positive_current_and_instruction", sample.TCURELSC.gt(0) & sample.TCURINST.gt(0)),
    ]
    keep = pd.Series(True, index=sample.index)
    flow = []
    for label, condition in checks:
        keep &= condition
        flow.append({"filter": label, "remaining_rows": int(keep.sum()),
                     "remaining_pupils": float(sample.loc[keep, "V33"].sum())})
    return sample.loc[keep].copy(), flow


def fit_state_fe(y: np.ndarray, x: np.ndarray, weights: np.ndarray,
                 state: np.ndarray) -> dict:
    """Weighted state demeaning and cluster sandwich, implemented independently."""
    y, x, weights = [np.asarray(a, dtype=float) for a in (y, x, weights)]
    state = np.asarray(state)
    if not (len(y) == len(x) == len(weights) == len(state)):
        raise ValueError("length mismatch")
    if not all(np.isfinite(a).all() for a in (y, x, weights)) or (weights <= 0).any():
        raise ValueError("nonfinite observations or nonpositive weights")
    weights = weights / weights.mean()
    groups = np.unique(state)
    n, g = len(y), len(groups)
    parameters = g + 1
    if g < 2 or n <= parameters:
        raise ValueError("insufficient independent groups or residual degrees of freedom")
    xd, yd = x.copy(), y.copy()
    for group in groups:
        mask = state == group
        xd[mask] -= np.average(x[mask], weights=weights[mask])
        yd[mask] -= np.average(y[mask], weights=weights[mask])
    bread = float(np.sum(weights * xd**2))
    if bread <= np.finfo(float).eps:
        raise ValueError("no within-state enrollment variation")
    beta = float(np.sum(weights * xd * yd) / bread)
    residual = yd - beta * xd
    scores = np.array([np.sum(weights[state == group] * xd[state == group] *
                              residual[state == group]) for group in groups])
    correction = g / (g - 1) * (n - 1) / (n - parameters)
    variance = float(correction * np.sum(scores**2) / bread**2)
    se = math.sqrt(max(variance, 0.0))
    critical = float(t.ppf(0.975, g - 1))
    return {
        "n": n, "states": g, "parameters": parameters, "beta": beta,
        "state_cluster_cr1_se": se, "ci95_low": beta - critical * se,
        "ci95_high": beta + critical * se, "t_df": g - 1,
        "cr1_correction": correction,
    }


def extract_benchmarks(frame: pd.DataFrame, workbook: Path, year: int) -> dict:
    table = pd.read_excel(workbook, sheet_name="8", header=None)
    rows = table[table[0].astype(str).str.strip().str.startswith("United States")]
    if len(rows) != 1:
        raise ValueError(f"[BLOCKED] ambiguous Table 8 national row: {workbook}")
    row = rows.iloc[0]
    positive = frame.loc[frame.V33.gt(0)]
    enrollment = float(positive.V33.sum())
    results = []
    for field, column in [("TCURELSC", 2), ("TCURINST", 5)]:
        raw_pp = float(positive[field].sum() * 1000 / enrollment)
        published = float(row[column])
        results.append({
            "field": field, "raw_positive_enrollment_pp": raw_pp,
            "published_table8_pp": published, "difference_dollars": raw_pp - published,
            "difference_percent": (raw_pp / published - 1) * 100,
            "excel_cell": f"{'C' if column == 2 else 'F'}{rows.index[0] + 1}",
        })
    notes = [str(value).strip() for value in table[0]
             if isinstance(value, str) and len(value) > 100]
    return {
        "year": year, "workbook": workbook.name, "sheet": "8", "results": results,
        "table_notes": notes,
        "status": "Uncalibrated comparison; raw amounts and published pp use different exclusions/adjustments. Neither exact equality nor complete reconciliation is claimed.",
    }


def estimate_all(samples: dict[int, pd.DataFrame]) -> tuple[list[dict], list[dict]]:
    estimates, panels = [], []

    def estimate(frame: pd.DataFrame, design: str, period: str, subset: str,
                 x: np.ndarray, outcome_values: dict, pupil_weights: np.ndarray,
                 pupil_only: bool = False):
        for weight_name, weights in [("equal_district", np.ones(len(frame))),
                                     ("baseline_pupil" if design == "long_difference" else
                                      "current_pupil", pupil_weights)]:
            if pupil_only and weight_name == "equal_district":
                continue
            for outcome, y in outcome_values.items():
                estimates.append({"design": design, "period": period, "subset": subset,
                                  "weight": weight_name, "outcome": outcome,
                                  "pupils_at_weight_year": float(pupil_weights.sum()),
                                  **fit_state_fe(y, x, weights, frame.state.to_numpy())})

    current = samples[2019]
    estimate(current, "cross_section", "2019", "all", np.log(current.V33.to_numpy()),
             {k: np.log(current[k].to_numpy()) for k in ("TCURELSC", "TCURINST")},
             current.V33.to_numpy())
    for start, end in [(2000, 2019), (2000, 2010), (2010, 2019)]:
        matched = samples[start].merge(samples[end], on="NCESID", suffixes=("_start", "_end"),
                                       validate="one_to_one")
        if not matched.state_start.eq(matched.state_end).all():
            raise ValueError("[BLOCKED] matched NCES ID changed state")
        matched["state"] = matched.state_start
        matched["dx"] = np.log(matched.V33_end / matched.V33_start)
        stable = matched.SCHLEV_start.eq(matched.SCHLEV_end) & matched.IDCENSUS_start.eq(matched.IDCENSUS_end)
        bounded = matched.dx.abs().le(math.log(2))
        masks = {"all": pd.Series(True, index=matched.index), "growing": matched.dx.gt(0),
                 "shrinking": matched.dx.lt(0)}
        if (start, end) == (2000, 2019):
            masks.update(stable_level_and_census_id=stable, enrollment_within_factor_two=bounded,
                         stable_and_within_factor_two=stable & bounded,
                         exclude_california_documented_2019_reporting_break=matched.state.ne("06"))
        panels.append({
            "period": f"{start}-{end}", "matched_districts": len(matched),
            "baseline_sample_districts": len(samples[start]), "end_sample_districts": len(samples[end]),
            "baseline_pupils_matched": float(matched.V33_start.sum()),
            "end_pupils_matched": float(matched.V33_end.sum()),
            "baseline_sample_pupil_share_matched": float(matched.V33_start.sum() / samples[start].V33.sum()),
            "end_sample_pupil_share_matched": float(matched.V33_end.sum() / samples[end].V33.sum()),
            "stable_level_and_census_id_districts": int(stable.sum()),
            "unchanged_enrollment_districts": int(matched.dx.eq(0).sum()),
        })
        for label, mask in masks.items():
            part = matched.loc[mask]
            estimate(part, "long_difference", f"{start}-{end}", label, part.dx.to_numpy(),
                     {k: np.log((part[k + "_end"] / part[k + "_start"]).to_numpy())
                      for k in ("TCURELSC", "TCURINST")}, part.V33_start.to_numpy(),
                     pupil_only=label.startswith("exclude_california"))
    return estimates, panels


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    # Materialize the declared method before source loading or any regression.
    dump_json(args.out_dir / "raw_method.json", METHOD)
    receipt = verify_sources(args.data_root)
    cache = args.data_root / BASE / "_cache/f33"
    samples, coverage, benchmarks = {}, [], []
    for year in [2000, 2010, 2019]:
        raw, info = parse_raw(cache / f"elsec{year % 100:02d}.txt", year)
        sample, flow = analysis_sample(raw)
        samples[year] = sample
        coverage.append({**info, "filter_flow": flow})
        if year in (2010, 2019):
            name = "elsec10_sttables.xls" if year == 2010 else "elsec19_sumtables.xls"
            benchmarks.append(extract_benchmarks(raw, cache / name, year))
    estimates, panels = estimate_all(samples)
    with (args.out_dir / "raw_estimates.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(estimates[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(estimates)
    dump_json(args.out_dir / "raw_coverage.json", {"years": coverage, "panels": panels})
    dump_json(args.out_dir / "raw_benchmarks.json", benchmarks)
    receipt["script_sha256"] = sha256(Path(__file__))
    receipt["outputs_sha256"] = {name: sha256(args.out_dir / name) for name in
                                  ["raw_method.json", "raw_estimates.csv", "raw_coverage.json", "raw_benchmarks.json"]}
    dump_json(args.out_dir / "raw_sources.json", receipt)
    print(f"Wrote {len(estimates)} descriptive specifications to {args.out_dir}")
    for row in estimates:
        if row["outcome"] == "TCURELSC" and row["subset"] == "all":
            print(f"{row['design']} {row['period']} {row['weight']}: "
                  f"{row['beta']:.6f} [{row['ci95_low']:.6f}, {row['ci95_high']:.6f}], n={row['n']}")


if __name__ == "__main__":
    main()
