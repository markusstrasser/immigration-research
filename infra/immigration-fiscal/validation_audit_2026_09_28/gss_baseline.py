"""Compare the existing GSS temporal prediction with a frozen-distribution baseline.

Retrospective diagnostic of an auxiliary education model, not a fiscal back-test.
Reconstruct both predictions and observations from the published parent-link cells.
"""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path


LANE = Path(__file__).resolve().parent
ROOT = LANE.parents[2]
UPSTREAM = ROOT / "infra/immigration-fiscal/projection_backtest_2026_09_19"
CATEGORIES = ("below12", "exactly12", "above12")


def read_rows(path):
    with path.open(newline="") as stream:
        return list(csv.DictReader(stream))


def weighted_distribution(rows, weights=None):
    if weights is None:
        weights = [float(row["weight_sum"]) for row in rows]
    if not rows or not all(math.isfinite(w) and w > 0 for w in weights):
        raise ValueError("Missing cells or invalid weights")
    values = [sum(w * float(row[k]) for w, row in zip(weights, rows)) / sum(weights)
              for k in CATEGORIES]
    if not all(math.isfinite(v) and 0 <= v <= 1 for v in values):
        raise ValueError("Invalid probability")
    if not math.isclose(sum(values), 1, abs_tol=1e-10):
        raise ValueError("Distribution does not sum to one")
    return values


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=LANE / "derived")
    args = parser.parse_args()
    files = [UPSTREAM / "derived/gss_temporal_prediction.csv",
             UPSTREAM / "derived/gss_transition_cells.csv"]
    predictions, cells = [read_rows(path) for path in files]
    results, skipped = [], []
    for row in predictions:
        key = {k: row[k] for k in ("frame", "group")}
        if row["status"] == "insufficient_training_support":
            skipped.append({**key, "reason": row["status"]})
            continue
        matching = [c for c in cells if all(c[k] == v for k, v in key.items())]
        train = sorted((c for c in matching if c["period"] == "train_through_1996"),
                       key=lambda c: int(c["parent_edu"]))
        held = sorted((c for c in matching if c["period"] == "heldout_1998_2024"),
                      key=lambda c: int(c["parent_edu"]))
        if ([c["parent_edu"] for c in train] != ["0", "1", "2"] or
                [c["parent_edu"] for c in held] != ["0", "1", "2"] or
                any(int(c["respondent_n"]) < 30 for c in train) or
                not math.isclose(float(row["retained_parent_weight_share"]), 1)):
            raise ValueError(f"Unexpected support change: {key}")
        naive = weighted_distribution(train)
        model = weighted_distribution(train, [float(c["weight_sum"]) for c in held])
        observed = weighted_distribution(held)
        for category, predicted, actual in zip(CATEGORIES, model, observed):
            if not (math.isclose(predicted, float(row[f"{category}_predicted"]), abs_tol=1e-10)
                    and math.isclose(actual, float(row[f"{category}_observed"]), abs_tol=1e-10)):
                raise ValueError(f"Upstream cell/prediction mismatch: {key}, {category}")
        # 100 * total variation = 50 * sum of absolute probability differences.
        score = lambda estimate: 50 * sum(abs(a - b) for a, b in zip(observed, estimate))
        results.append({**key, "model_tv_pp": score(model), "naive_tv_pp": score(naive),
                        "model_above12_error_pp": 100 * (observed[2] - model[2]),
                        "naive_above12_error_pp": 100 * (observed[2] - naive[2]),
                        "training_respondents": int(float(row["training_respondents"])),
                        "heldout_respondents": int(float(row["heldout_respondents"]))})
    pins = files + [UPSTREAM / "cohorts.py", Path(__file__)]
    output = {
        "scope": "Retrospective GSS education diagnostic; not a fiscal forecast or prospective test.",
        "limitations": "Model conditions on later observed parent mix; parent-link weighted; no design intervals. All source frames retained; unsupported Mexican-origin rows skipped explicitly.",
        "input_sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in pins},
        "results": results, "skipped": skipped,
    }
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "gss_baseline.json").write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({"results": results, "skipped": skipped}, indent=2))


if __name__ == "__main__":
    main()
