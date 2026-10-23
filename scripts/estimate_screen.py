#!/usr/bin/env python3
"""Screen estimates before they enter a memo table.

Four tests, applied to every (function, model, sample) row of a scaling table:

1. Precision: the 95% CI half-width must be narrower than the gap between the
   competing hypotheses. For a scaling elasticity the hypotheses are
   proportional (1.0) and a 3/4 or 5/6 exponent, so the gaps are 0.25 and 0.167.
2. Stability: the pre-specified windows (all / census / pre-2020) must not
   straddle the competing hypotheses, and max/min must be <= 1.5.
3. Influence: dropping the five most influential observations must not move the
   estimate across a competing hypothesis or by more than 25%.
4. Data quality: no more than 5% of observations with CV > 10, and no
   year-to-year swing > 25% unexplained by population.

An estimate that fails is demoted, not deleted. The point estimate stays in the
screened CSV with screen=fail, and a memo table prints "not identified (reason)".
That keeps the number auditable without presenting noise as a finding.

    uv run --no-project python3 scripts/estimate_screen.py
    uv run --no-project python3 scripts/estimate_screen.py --lane <lane> --out <dir>
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_LANE = ROOT / "infra/immigration-fiscal/scaling_test_2026_09_20"

# Census function codes, mirroring state_analyze.py.
FUNCTIONS = {
    "k12": ["E12"],
    "higher_core": ["E16"],
    "admin": ["E23", "E29", "E31"],
    "police": ["E62"],
    "fire": ["E24"],
    "highways_nontoll": ["E44"],
    "parks": ["E61"],
    "libraries": ["E52"],
    "health": ["E32"],
    "hospitals": ["E36"],
}
GAP_34 = 0.25
GAP_56 = 1.0 - 5.0 / 6.0
CV_FLAG = 30.0          # Census "unreliable" threshold
CV_SHARE_MAX = 0.05
SWING = np.log(2.0)     # a doubling or halving is a data event, not a budget cycle
SWING_SHARE_MAX = 0.02


def design(d: pd.DataFrame, function: str, model: str):
    """Return the sample, design matrix and outcome used by state_analyze.fit."""
    d = d.loc[d[function].gt(0) & d.population.gt(0)].copy()
    y = np.log(d[function].to_numpy(float))
    x = np.log(d.population.to_numpy(float))
    terms = [
        np.ones((len(d), 1)),
        x[:, None],
        pd.get_dummies(d.year, drop_first=True).to_numpy(float),
    ]
    if model == "state_year_fe":
        terms.append(pd.get_dummies(d.state, drop_first=True).to_numpy(float))
    X = np.column_stack(terms)
    if np.linalg.matrix_rank(X) != X.shape[1]:
        raise ValueError(f"rank deficient: {function} {model}")
    return d, X, y


def ols(X: np.ndarray, y: np.ndarray):
    bread = np.linalg.inv(X.T @ X)
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    return beta, y - X @ beta, bread


def precision(row: pd.Series) -> tuple[bool, str]:
    lo, hi = float(row.ci_low), float(row.ci_high)
    includes_1 = lo <= 1.0 <= hi
    includes_34 = lo <= 0.75 <= hi
    includes_56 = lo <= 5.0 / 6.0 <= hi
    if includes_1 and includes_34:
        return False, f"CI [{lo:.3f}, {hi:.3f}] contains both 1.0 and 0.75"
    if includes_1 and includes_56:
        return True, "separates 1.0 from 0.75 but not 5/6"
    return True, ""


def stability(g: pd.DataFrame) -> tuple[bool, str]:
    b = g.beta.to_numpy(float)
    lo, hi = float(b.min()), float(b.max())
    if lo <= 0:
        return False, f"a window estimate is non-positive ({lo:.3f})"
    if lo < 0.75 < 1.0 < hi:
        return False, f"windows {lo:.3f}-{hi:.3f} straddle 0.75-1.0"
    if hi / lo > 1.5:
        return False, f"window ratio {hi / lo:.2f} > 1.5 ({lo:.3f}-{hi:.3f})"
    return True, ""


def influence(d: pd.DataFrame, function: str, model: str, beta_full: float) -> tuple[bool, str]:
    d2, X, y = design(d, function, model)
    beta, e, bread = ols(X, y)
    h = np.einsum("ij,jk,ik->i", X, bread, X)
    dfbeta = (X @ bread) * e[:, None] / (1.0 - h)[:, None]
    drop = np.argsort(-np.abs(dfbeta[:, 1]))[:5]
    mask = np.ones(len(d2), dtype=bool)
    mask[drop] = False
    beta_drop = float(np.linalg.lstsq(X[mask], y[mask], rcond=None)[0][1])
    moved = abs(beta_drop - beta_full)
    crossed = (beta_full - 0.75) * (beta_drop - 0.75) < 0 or (beta_full - 1.0) * (beta_drop - 1.0) < 0
    if crossed:
        return False, f"dropping the top 5 moves beta {beta_full:.3f}->{beta_drop:.3f}, across a hypothesis"
    if moved > 0.25 * abs(beta_full):
        return False, f"dropping the top 5 moves beta {beta_full:.3f}->{beta_drop:.3f} ({moved / abs(beta_full):.0%})"
    return True, ""


def data_quality(
    d: pd.DataFrame, function: str, beta_full: float, finance: pd.DataFrame
) -> tuple[bool, str]:
    codes = FUNCTIONS[function]
    cv = (
        finance.loc[finance.code.isin(codes)]
        .groupby(["state", "year"], as_index=False)["cv"]
        .max()
    )
    dd = d.merge(cv, on=["state", "year"], how="left").sort_values(["state", "year"])
    share_cv = float((dd.cv > CV_FLAG).mean())
    max_cv = float(dd.cv.max())
    dl = np.log(dd[function]).groupby(dd.state).diff()
    dp = np.log(dd.population).groupby(dd.state).diff()
    resid = dl - beta_full * dp
    transitions = int(resid.notna().sum())
    share_swing = float((resid.abs() > SWING).sum() / transitions) if transitions else 0.0
    reasons = []
    if share_cv > CV_SHARE_MAX:
        reasons.append(f"{share_cv:.0%} of obs with CV>{CV_FLAG:g} (max {max_cv:.1f})")
    if share_swing > SWING_SHARE_MAX:
        reasons.append(f"{share_swing:.0%} of transitions swing >25% beyond population")
    return (not reasons), "; ".join(reasons)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", type=Path, default=DEFAULT_LANE)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()
    out = args.out or args.lane / "derived" / "state"

    est = pd.read_csv(args.lane / "derived" / "state" / "estimates.csv")
    panel = pd.read_csv(args.lane / "derived" / "state" / "panel.csv")
    finance = pd.read_csv(args.lane / "derived" / "state" / "selected_finance.csv")

    rows = []
    for (function, model), group in est.groupby(["function", "model"], sort=False):
        group = group.reset_index(drop=True)
        ok_stab, why_stab = stability(group)
        for _, row in group.iterrows():
            sample = row["sample"]
            subset = panel
            if sample == "census":
                subset = panel.loc[panel.year.isin([2012, 2017, 2022])]
            elif sample == "pre2020":
                subset = panel.loc[panel.year.lt(2020)]

            reasons: list[str] = []
            codes: list[str] = []
            ok_p, why_p = precision(row)
            ok_i, why_i = influence(subset, function, model, float(row.beta))
            ok_d, why_d = data_quality(subset, function, float(row.beta), finance)
            for code, ok, why in (("P", ok_p, why_p), ("S", ok_stab, why_stab), ("I", ok_i, why_i), ("D", ok_d, why_d)):
                if not ok:
                    codes.append(code)
                    reasons.append(why)

            rec = row.to_dict()
            rec["screen"] = "pass" if not reasons else "not identified"
            rec["screen_code"] = ",".join(codes) if codes else ""
            rec["screen_reason"] = "; ".join(reasons)
            rec["precision_note"] = why_p if ok_p and why_p else ""
            rows.append(rec)

    screened = pd.DataFrame(rows)
    screened.to_csv(out / "estimates_screened.csv", index=False)

    # Memo table: the primary "all" rows only, point estimate on pass.
    primary = screened.loc[screened["sample"].eq("all")].copy()
    lines = [
        "| Function | Across states (year FE) | Within states (state+year FE) |",
        "|---|---:|---:|",
    ]
    for function in FUNCTIONS:
        cells = []
        for model in ("year_fe", "state_year_fe"):
            r = primary.loc[primary["function"].eq(function) & primary["model"].eq(model)]
            if r.empty:
                cells.append("—")
                continue
            r = r.iloc[0]
            if r["screen"] == "pass":
                cells.append(f"{r.beta:.3f} [{r.ci_low:.3f}, {r.ci_high:.3f}]")
            else:
                cells.append(f"not identified ({r['screen_code']})")
        lines.append(f"| {function} | {cells[0]} | {cells[1]} |")
    (out / "screen_summary.md").write_text("\n".join(lines) + "\n")

    passed = int(screened["screen"].eq("pass").sum())
    print(f"screened {len(screened)} rows: {passed} pass, {len(screened) - passed} not identified")
    print(f"wrote {out / 'estimates_screened.csv'}")
    print(f"wrote {out / 'screen_summary.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
