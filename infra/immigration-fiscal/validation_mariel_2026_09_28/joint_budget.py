"""Retrospective, accounting-coherent prediction of Dade school finances."""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import minimize

LANE = Path(__file__).resolve().parent
ROOT = LANE.parents[2]
TREATED = "105013001"
PRIMITIVES = ["Total_Rev_Own_Sources", "Total_Fed_IG_Revenue", "Total_State_IG_Revenue",
              "Tot_Local_IG_Rev", "Total_Current_Oper", "Total_Capital_Outlays",
              "Total_Interest_on_Debt"]
TOTALS = ["Total_Revenue", "Total_Expenditure", "Total_Taxes"]
SCORED = ["Total_Revenue", "Total_Expenditure", "Total_Current_Oper",
          "Total_Rev_Own_Sources", "Total_Fed_IG_Revenue", "Total_State_IG_Revenue"]
DERIVED = ["revenue_residual", "expenditure_residual", "balance"]
ALL = PRIMITIVES + TOTALS + DERIVED
YEARS = list(range(1970, 1991))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def solve(y, x):
    if not (np.isfinite(y).all() and np.isfinite(x).all() and x.shape[1] >= 2):
        raise ValueError("Invalid fit arrays")
    scale = max(np.linalg.norm(x, ord=2), np.linalg.norm(y), 1.0)
    x, y = x / scale, y / scale
    fit = minimize(lambda w: np.sum((x @ w - y)**2), np.full(x.shape[1], 1/x.shape[1]),
                   jac=lambda w: 2*x.T @ (x @ w - y), method="SLSQP",
                   bounds=[(0, 1)]*x.shape[1],
                   constraints={"type": "eq", "fun": lambda w: w.sum()-1,
                                "jac": lambda w: np.ones_like(w)},
                   options={"ftol": 1e-14, "maxiter": 10000})
    if not fit.success:
        raise RuntimeError(fit.message)
    w = fit.x
    if not (np.isfinite(w).all() and w.min() >= -1e-8 and abs(w.sum()-1) < 1e-8):
        raise ValueError("Invalid simplex solution")
    gradient = 2*x.T @ (x @ w-y)
    # For this convex problem, the simplex duality gap bounds suboptimality.
    if float(w @ gradient-gradient.min()) > 1e-7:
        raise RuntimeError("Optimizer did not reach a sufficiently accurate simplex optimum")
    return w


def load_panel(path):
    data = pd.read_csv(path, dtype={"ID": str})
    if data.duplicated(["ID", "fiscal_year"]).any():
        raise ValueError("Duplicate district-year")
    data = data[data.fiscal_year.isin(YEARS)].copy()
    data["revenue_residual"] = data.Total_Revenue-data[PRIMITIVES[:4]].sum(axis=1)
    data["expenditure_residual"] = data.Total_Expenditure-data[PRIMITIVES[4:]].sum(axis=1)
    data["balance"] = data.Total_Revenue-data.Total_Expenditure
    eligible = sorted(data.loc[data.donor_eligible.eq(1), "ID"].unique())
    if TREATED in eligible:
        raise ValueError("Treated district in donor pool")
    panels, dropped = {}, []
    for unit in [TREATED] + eligible:
        block = data[data.ID.eq(unit)].set_index("fiscal_year").reindex(YEARS)[ALL]
        if not np.isfinite(block.to_numpy()).all():
            dropped.append(unit)
        else:
            panels[unit] = block
    if TREATED not in panels or len(panels) < 20:
        raise ValueError("Insufficient complete support")
    return panels, dropped


def fit_weights(panels, target, donors, years, weighting):
    train = panels[target].loc[years]
    floor = .01*train.Total_Revenue.mean()
    if floor <= 0:
        raise ValueError("Invalid normalization level")
    scales = (train[PRIMITIVES].mean().clip(lower=floor) if weighting == "component_relative"
              else pd.Series(train.Total_Revenue.mean(), index=PRIMITIVES))
    y = (train[PRIMITIVES]/scales).to_numpy().ravel()
    x = np.column_stack([(panels[u].loc[years, PRIMITIVES]/scales).to_numpy().ravel()
                         for u in donors])
    return solve(y, x)


def predict(panels, target, donors, train, weighting):
    weights = fit_weights(panels, target, donors, train, weighting)
    prediction = panels[target]*0
    for unit, weight in zip(donors, weights):
        prediction += weight*panels[unit]
    verify_identities(prediction)
    return prediction, weights


def baseline(panels, target, donors, train):
    anchor = train[-1]
    growth = np.mean([panels[u].Total_Expenditure.to_numpy() /
                      panels[u].loc[anchor, "Total_Expenditure"] for u in donors], axis=0)
    if not np.isfinite(growth).all():
        raise ValueError("Invalid donor-growth baseline")
    out = pd.DataFrame(growth[:, None]*panels[target].loc[anchor].to_numpy(),
                       index=YEARS, columns=ALL)
    verify_identities(out)
    return out


def verify_identities(frame):
    equations = [frame.Total_Revenue-frame[PRIMITIVES[:4]].sum(axis=1)-frame.revenue_residual,
                 frame.Total_Expenditure-frame[PRIMITIVES[4:]].sum(axis=1)-frame.expenditure_residual,
                 frame.Total_Revenue-frame.Total_Expenditure-frame.balance]
    if any(np.max(np.abs(x)) > 1e-6 for x in equations):
        raise ValueError("Budget identity failure")


def score(actual, predicted, train, test):
    floor = .01*actual.loc[train, "Total_Revenue"].mean()
    if not np.isfinite(floor) or floor <= 0:
        raise ValueError("Invalid scoring normalization level")
    scales = actual.loc[train, SCORED].mean().clip(lower=floor)
    error = predicted.loc[test]-actual.loc[test]
    joint = float(np.sqrt(np.mean((error[SCORED]/scales).to_numpy()**2))*100)
    rows = []
    for col in ALL:
        scale = max(abs(actual.loc[train, col].mean()), floor)
        rows.append({"outcome": col, "rmse_thousand_nominal": float(np.sqrt(np.mean(error[col]**2))),
                     "mean_prediction_minus_actual_thousand_nominal": float(error[col].mean()),
                     "normalized_rmse_pct": float(np.sqrt(np.mean(error[col]**2))/scale*100),
                     "normalizer_training_thousand_nominal": float(scale)})
    return joint, rows


def run_panel(path, out, label):
    panels, dropped = load_panel(path)
    donors = sorted(set(panels)-{TREATED})
    tests, annual, weights_out, placebo_rows = [], [], [], []
    for weighting in ["component_relative", "common_revenue_unit"]:
        for phase, train, test in [("pre_holdout", list(range(1970, 1977)), list(range(1977, 1980))),
                                   ("post_event", list(range(1970, 1980)), list(range(1981, 1991)))]:
            prediction, weights = predict(panels, TREATED, donors, train, weighting)
            largest = donors[int(np.argmax(weights))]
            leave, _ = predict(panels, TREATED, [u for u in donors if u != largest], train, weighting)
            for unit, weight in zip(donors, weights):
                weights_out.append({"panel": label, "weighting": weighting, "phase": phase,
                                    "donor": unit, "weight": float(weight)})
            alternatives = {"joint": prediction, "donor_growth": baseline(panels, TREATED, donors, train),
                            "drop_largest": leave}
            for method, pred in alternatives.items():
                joint, rows = score(panels[TREATED], pred, train, test)
                meta = {"panel": label, "weighting": weighting, "phase": phase,
                        "method": method, "joint_normalized_rmse_pct": joint,
                        "largest_donor": largest, "largest_weight": float(max(weights))}
                tests.extend([{**meta, **row} for row in rows])
                for year in YEARS:
                    for col in ALL:
                        actual, counter = float(panels[TREATED].loc[year, col]), float(pred.loc[year, col])
                        annual.append({**meta, "year": year, "outcome": col, "actual": actual,
                                       "counterfactual": counter, "actual_minus_counterfactual": actual-counter})
        train, test = list(range(1970, 1980)), list(range(1981, 1991))
        for target in [TREATED] + donors:
            controls = [u for u in donors if u != target]
            pred, _ = predict(panels, target, controls, train, weighting)
            error = pred.Total_Expenditure-panels[target].Total_Expenditure
            pre = float(np.sqrt(np.mean(error.loc[train]**2)))
            if pre <= 1e-8:
                raise ValueError("Undefined placebo RMSPE ratio")
            placebo_rows.append({"panel": label, "weighting": weighting, "target": target,
                                 "n_donors": len(controls), "pre_rmspe_thousand": pre,
                                 "post_pre_rmspe_ratio": float(np.sqrt(np.mean(error.loc[test]**2))/pre),
                                 "post_gap_over_training_expenditure_pct":
                                 float(-error.loc[test].mean()/panels[target].loc[train, "Total_Expenditure"].mean()*100)})
    for name, rows in [("scores", tests), ("annual", annual), ("weights", weights_out), ("placebos", placebo_rows)]:
        pd.DataFrame(rows).to_csv(out/f"{label}_{name}.csv", index=False, lineterminator="\n")
    return {"panel": label, "donors": len(donors), "dropped": dropped,
            "input_sha256": sha(path), "preholdout_scores": [r for r in tests
             if r["phase"] == "pre_holdout" and r["outcome"] == "Total_Expenditure"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=ROOT)
    parser.add_argument("--out-dir", type=Path, default=LANE/"derived")
    args = parser.parse_args()
    source = args.source_root/"infra/immigration-fiscal/causal_execution_2026_09_20/mariel/work"
    args.out_dir.mkdir(parents=True, exist_ok=True)
    summaries = [run_panel(source/name, args.out_dir, label) for label, name in
                 [("june30", "scm-june-only-panel.csv"), ("full_timing_diagnostic", "scm-source-year-panel.csv")]]
    summary = {"method": "Shared simplex weights across primitive budget lines; retrospective conditional donor-outcome prediction",
               "units": "Source levels in nominal thousands by fiscal year; annual series retained, no constant-price cumulative total",
               "source": "Pierson, Hand and Thompson (2015), doi:10.1371/journal.pone.0130119; pinned upstream S7",
               "script_sha256": sha(Path(__file__)), "design_sha256": sha(LANE/"Design.md"),
               "panels": summaries}
    (args.out_dir/"summary.json").write_text(json.dumps(summary, indent=2, allow_nan=False)+"\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
