# /// script
# requires-python = ">=3.11"
# dependencies = ["duckdb", "numpy", "pandas"]
# ///
"""Fixed-population sensitivity for recent ACS entry cohorts, 2019 versus 2024.

These are synthetic balanced populations, not national means or causal effects.
Do not condition on education or origin: their composition remains in the result.
PERNP includes zero/negative earnings and is rolling prior-12-month income, which
can include pre-US earnings. YOEP records most recent entry, in integer years.

Native-First: pandas streams existing official ZIPs; NumPy accumulates cell
sufficient statistics. Reuse the parent reader and SDR formula; no database,
new acquisition, survey framework or shared API mutation is needed.
"""
from __future__ import annotations

import paths as _data_paths

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path

import numpy as np
import pandas as pd

import analyze_arrival_cohorts as parent
from analyze_arrival_cohorts import WEIGHTS, person_streams, sdr_estimate, sha256


FIELDS = ["AGEP", "SEX", "NATIVITY", "YOEP", "ESR", "RELSHIPP", "PERNP", "ADJINC"]
AGE_BANDS = ["25-34", "35-44", "45-54", "55-64"]
METRICS = ["employment_population", "mean_real_earnings_2024_dollars"]
ANCHORS = ["Total population", "Total males (SEX=1)", "Age 25-34"]
METHODS = {
    "recent_equal_duration": "Foreign-born CNI ages25-64, entry1-3: weight each duration 1/3",
    "recent_equal_age_sex_duration": "Foreign-born CNI ages25-64, entry1-3: weight each age x sex x duration cell 1/24",
    "native_equal_age_sex": "Native CNI ages25-64: weight each age x sex cell 1/8; period context only",
}


def balanced_replicates(sums: np.ndarray, sample_n: np.ndarray) -> np.ndarray:
    """Ratio within each cell, then fixed equal weighting for all 81 estimates."""
    if sums.ndim != 3 or sums.shape[1:] != (81, 3):
        raise ValueError("Expected cell x 81 weights x (denominator, employed, earnings)")
    if sample_n.shape != (len(sums),) or (sample_n <= 0).any():
        raise ValueError("Empty standardized population cell")
    if not np.isfinite(sums).all() or (sums[:, :, 0] <= 0).any():
        raise ValueError("Nonpositive/nonfinite full or replicate cell denominator")
    return (sums[:, :, 1:] / sums[:, :, :1]).mean(axis=0)


def accumulate_cells(sums, sample_n, codes, weights, values) -> None:
    for code in np.unique(codes):
        mask = codes == code
        sums[code] += weights[mask].T @ values[mask]
        sample_n[code] += int(mask.sum())


def analyze_year(year: int, source: Path, factor: float, inflation: dict, chunk_size: int) -> dict:
    fine = np.zeros((24, 81, 3))
    fine_n = np.zeros(24, dtype=np.int64)
    native = np.zeros((8, 81, 3))
    native_n = np.zeros(8, dtype=np.int64)
    calibration = np.zeros((81, 3))
    rows_read = 0
    negative_replicates = zero_replicates = 0
    earnings_counts = {"recent": {"zero": 0, "negative": 0}, "native": {"zero": 0, "negative": 0}}
    source_hash = sha256(source)
    with person_streams(source) as streams:
        for member, stream in streams:
            for frame in pd.read_csv(stream, usecols=FIELDS + WEIGHTS, dtype=float, chunksize=chunk_size):
                rows_read += len(frame)
                w = frame[WEIGHTS].to_numpy()
                if not np.isfinite(w).all() or (w[:, 0] <= 0).any():
                    raise ValueError("Invalid full weights or nonfinite replicate weights")
                negative_replicates += int((w[:, 1:] < 0).sum())
                zero_replicates += int((w[:, 1:] == 0).sum())
                if not frame.SEX.isin([1, 2]).all() or not frame.NATIVITY.isin([1, 2]).all():
                    raise ValueError("Unknown sex/nativity code")
                age = frame.AGEP.to_numpy()
                if not np.isfinite(age).all():
                    raise ValueError("Missing age")
                calibration += w.T @ np.column_stack((np.ones(len(frame)), frame.SEX.eq(1), frame.AGEP.between(25, 34)))
                adult = frame.AGEP.between(25, 64).to_numpy()
                required = ["ESR", "RELSHIPP", "PERNP", "ADJINC"]
                if not np.isfinite(frame.loc[adult, required].to_numpy()).all():
                    raise ValueError("Missing adult outcome, universe field or price adjustment")
                cni = adult & ~frame.ESR.isin([4, 5]).to_numpy() & ~frame.RELSHIPP.eq(37).to_numpy()
                if not frame.loc[cni, "ESR"].isin([1, 2, 3, 6]).all() or (frame.loc[cni, "ADJINC"] <= 0).any():
                    raise ValueError("Invalid civilian employment code or adjustment factor")
                duration = year - frame.YOEP.to_numpy()
                recent_mask = cni & frame.NATIVITY.eq(2).to_numpy() & (duration >= 1) & (duration <= 3)
                native_mask = cni & frame.NATIVITY.eq(1).to_numpy()
                for group, mask, sums, counts in [("recent", recent_mask, fine, fine_n), ("native", native_mask, native, native_n)]:
                    if not mask.any():
                        continue
                    block = frame.loc[mask]
                    age_cell = np.searchsorted([35, 45, 55], age[mask], side="right")
                    sex_cell = block.SEX.to_numpy(dtype=int) - 1
                    code = age_cell * 2 + sex_cell
                    if group == "recent":
                        durations = duration[mask]
                        if not np.equal(durations, durations.astype(int)).all():
                            raise ValueError("Recent entry-year codes are not individual integer years")
                        code = code * 3 + durations.astype(int) - 1
                    earnings = block.PERNP.to_numpy() * block.ADJINC.to_numpy() / 1_000_000 * factor
                    earnings_counts[group]["zero"] += int((earnings == 0).sum())
                    earnings_counts[group]["negative"] += int((earnings < 0).sum())
                    values = np.column_stack((np.ones(len(block)), block.ESR.isin([1, 2]), earnings))
                    accumulate_cells(sums, counts, code, w[mask], values)
                if rows_read % 500_000 < chunk_size:
                    print(f"{year} {member}: {rows_read:,} records", flush=True)

    official = inflation["calibration"][str(year)]
    if rows_read != official["official_national_person_records"]:
        raise ValueError(f"{year}: raw record count differs from official national PUMS count")
    checks = {}
    for i, name in enumerate(ANCHORS):
        result = sdr_estimate(calibration[:, i])
        expected = official["anchors"][name]
        estimate_delta = result["estimate"] - expected["estimate"]
        se_delta = result["acs_sdr_se"] - expected["sdr_se_published_rounded"]
        if abs(estimate_delta) > 0.01 or abs(se_delta) > 0.500001:
            raise ValueError(f"{year} {name}: official calibration failed: estimate delta={estimate_delta}, SE delta={se_delta}")
        checks[name] = result | {"expected": expected, "se_minus_published_rounded": se_delta, "passed": True, "full_and_80_replicates": calibration[:, i].tolist()}

    duration_sums = fine.reshape(4, 2, 3, 81, 3).sum(axis=(0, 1))
    duration_n = fine_n.reshape(4, 2, 3).sum(axis=(0, 1))
    grids = {"recent_equal_duration": (duration_sums, duration_n),
             "recent_equal_age_sex_duration": (fine, fine_n),
             "native_equal_age_sex": (native, native_n)}
    estimates, replicates, support = [], {}, {}
    for method, (sums, counts) in grids.items():
        balanced = balanced_replicates(sums, counts)
        support[method] = {"cell_count": len(counts), "fixed_cell_weight": 1 / len(counts),
                           "unweighted_n": int(counts.sum()), "min_unweighted_cell_n": int(counts.min()),
                           "max_unweighted_cell_n": int(counts.max()),
                           "min_full_cell_population": float(sums[:, 0, 0].min()),
                           "min_full_or_replicate_cell_denominator": float(sums[:, :, 0].min())}
        for i, metric in enumerate(METRICS):
            estimates.append({"survey_year": year, "method": method, "metric": metric} | sdr_estimate(balanced[:, i]))
            replicates[f"{method}/{metric}"] = balanced[:, i].tolist()
    cells = []
    for group, sums, counts in [("recent", fine, fine_n), ("native", native, native_n)]:
        for code in range(len(counts)):
            base = code // 3 if group == "recent" else code
            cells.append({"survey_year": year, "group": group, "age_band": AGE_BANDS[base // 2],
                          "sex": base % 2 + 1, "duration": code % 3 + 1 if group == "recent" else None,
                          "unweighted_n": int(counts[code]), "weighted_population": float(sums[code, 0, 0]),
                          "employment_population": float(sums[code, 0, 1] / sums[code, 0, 0]),
                          "mean_real_earnings_2024_dollars": float(sums[code, 0, 2] / sums[code, 0, 0])})
    return {"survey_year": year, "rows_read": rows_read, "source": {"path": str(source.resolve()), "bytes": source.stat().st_size, "sha256": source_hash},
            "real_dollar_factor": factor, "negative_replicate_weights_retained": negative_replicates,
            "zero_replicate_weights_retained": zero_replicates, "earnings_records_retained": earnings_counts,
            "calibration": checks, "support": support, "estimates": estimates, "replicates": replicates, "cells": cells,
            "cell_sufficient_statistics": {"axis_order": "age, sex, duration (recent only), replicate, statistic",
                "statistics": ["denominator", "employed_numerator", "real_earnings_numerator"],
                "recent_age4_sex2_duration3": fine.tolist(), "native_age4_sex2": native.tolist()}}


def self_test() -> None:
    sums = np.zeros((2, 81, 3))
    sums[:, :, 0] = np.array([10, 100])[:, None]
    sums[0, :, 1:] = [0, -100]
    sums[1, :, 1:] = [100, 3000]
    got = balanced_replicates(sums, np.array([2, 3]))
    np.testing.assert_allclose(got, np.tile([0.5, 10.0], (81, 1)))
    # Opposing cell perturbations cancel only if the whole estimate is replicated.
    sums[0, 1, 1] += 1
    sums[1, 1, 1] -= 10
    assert sdr_estimate(balanced_replicates(sums, np.array([2, 3]))[:, 0])["acs_sdr_se"] < 1e-12
    for invalid_counts, invalid_sums in [(np.array([0, 3]), sums), (np.array([2, 3]), sums.copy())]:
        if (invalid_counts > 0).all():
            invalid_sums[0, 80, 0] = 0
        try:
            balanced_replicates(invalid_sums, invalid_counts)
        except ValueError:
            pass
        else:
            raise AssertionError("Invalid cell did not fail")
    print("PASS: fixed-weight estimand, losses, whole-estimate covariance, empty/nonpositive-cell rejection")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--acs-2019", type=Path, default=_data_paths.data_root(require_exists=False) / 'external/acs_pums_2019_1yr/csv_pus.zip')
    parser.add_argument("--acs-2024", type=Path, default=_data_paths.data_root(require_exists=False) / 'external/acs_pums_2024_1yr/csv_pus.zip')
    parser.add_argument("--inflation", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--chunk-size", type=int, default=100_000)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    if not args.inflation or not args.out or args.chunk_size <= 0:
        parser.error("--inflation, --out and a positive --chunk-size are required")
    inflation = json.loads(args.inflation.read_text())
    if inflation["series"] != "R-CPI-U-RS all items annual average":
        raise ValueError("Expected the verified ACS R-CPI-U-RS source")
    dependency_hash = sha256(Path(parent.__file__))
    runs = [analyze_year(2019, args.acs_2019, float(inflation["factors"]["2019_to_2024"]["factor"]), inflation, args.chunk_size),
            analyze_year(2024, args.acs_2024, 1.0, inflation, args.chunk_size)]
    estimates = [row for run in runs for row in run["estimates"]]
    deltas = []
    for method in METHODS:
        for metric in METRICS:
            earlier, later = [next(x for x in run["estimates"] if x["method"] == method and x["metric"] == metric) for run in runs]
            point = later["estimate"] - earlier["estimate"]
            se = float(np.hypot(earlier["acs_sdr_se"], later["acs_sdr_se"]))
            deltas.append({"method": method, "metric": metric, "change_2024_minus_2019": point,
                           "se_cross_year_independence_approximation": se,
                           "ci95_low": point - 1.96 * se, "ci95_high": point + 1.96 * se})
    result = {"created_at_utc": datetime.now(timezone.utc).isoformat(),
              "status": "complete_with_official_calibration_passes", "methods": METHODS,
              "estimand": "Synthetic balanced cell populations; same fixed weights in 2019 and 2024; not actual national means or causal effects",
              "universe": "Civilian noninstitutional ages25-64: exclude ESR4/5 and RELSHIPP37. Recent = NATIVITY2 and survey year minus YOEP in1,2,3; native = NATIVITY1.",
              "employment_definition": "ESR1/2 as a share of every person in the selected population, not labor force only",
              "income_definition": "PERNP including zeros and losses, multiplied by ADJINC/1e6 and source-year R-CPI-U-RS factor to2024 dollars; rolling past12months",
              "uncertainty": "Whole standardized estimate computed for main and all80 replicate weights; SDR variance4/80. Between-year difference uses root-sum-squares and assumes cross-year independence approximately. Normal95% intervals omit nonsampling error.",
              "limits": ["YOEP most recent entry is not first arrival; integer durations do not align exact months", "Cross-sections differ in survival, coverage, selection and macro conditions", "Earnings can partly precede US arrival", "Synthetic equal cells give older/smaller cells more weight than actual populations", "Education and origin remain unconditioned; no attribution of their causal contribution"],
              "inflation_source": {"path": str(args.inflation.resolve()), "sha256": sha256(args.inflation)},
              "generator_sha256": sha256(Path(__file__)), "parent_helper_source_sha256_at_start": dependency_hash,
              "parent_helper_source_changed_during_run": sha256(Path(parent.__file__)) != dependency_hash,
              "runs": runs, "differences": deltas}
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "results.json").write_text(json.dumps(result, indent=2) + "\n")
    pd.DataFrame(estimates).to_csv(args.out / "estimates.csv", index=False)
    pd.DataFrame(deltas).to_csv(args.out / "differences.csv", index=False)
    pd.DataFrame([row for run in runs for row in run["cells"]]).to_csv(args.out / "cells.csv", index=False)
    lines = ["**Verdict:** The fixed-population sensitivity and independent official population/SDR calibrations completed. These are synthetic balanced populations, not national means or causal estimates.", "", "| Construction | Employment change, pp (95% CI) | Real mean earnings change, 2024 dollars (95% CI) |", "|---|---:|---:|"]
    for method in METHODS:
        employment, earnings = [next(x for x in deltas if x["method"] == method and x["metric"] == metric) for metric in METRICS]
        lines.append(f"| {method} | {100 * employment['change_2024_minus_2019']:.2f} ({100 * employment['ci95_low']:.2f}, {100 * employment['ci95_high']:.2f}) | {earnings['change_2024_minus_2019']:,.0f} ({earnings['ci95_low']:,.0f}, {earnings['ci95_high']:,.0f}) |")
    lines += ["", "Intervals use approximate cross-year independence; normal SDR sampling intervals omit nonsampling error. All 81 whole estimates and cell sufficient statistics are in results.json.", "", "Support and calibration:"]
    for run in runs:
        lines.append(f"- {run['survey_year']}: {run['rows_read']:,} national records; total population, males and ages25-34 match official point estimates and published SDR SEs within0.5; negative replicate weights retained: {run['negative_replicate_weights_retained']:,}.")
        for method, support in run["support"].items():
            lines.append(f"  - {method}: N={support['unweighted_n']:,}; smallest unweighted cell={support['min_unweighted_cell_n']:,}; all full/replicate cell denominators positive.")
    lines += ["", "Included: standardize_arrival_profiles.py; results.json, estimates.csv, differences.csv, cells.csv and this review. Skipped: parent generator edits, all databases, shared memos and commits (outside ownership).", "", "Interpretation limits: fixed weights change the target population; education/origin remain in the composition; rolling income can predate arrival; cross-sections do not identify policy effects or individual assimilation."]
    (args.out / "review.md").write_text("\n".join(lines) + "\n")
    print(json.dumps({"output": str(args.out), "differences": deltas, "support": {str(run["survey_year"]): run["support"] for run in runs}}, indent=2), flush=True)


if __name__ == "__main__":
    main()
