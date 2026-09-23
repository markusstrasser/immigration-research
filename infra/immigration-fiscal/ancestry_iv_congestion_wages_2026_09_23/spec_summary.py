"""Every IV specification computed, summarised per outcome and treatment: how many rows, the range
of coefficients, and how many exclude zero (Wald at 5%; and the Anderson-Rubin set where one was
computed). Reads derived/estimates_commute.csv, estimates_wages.csv and estimates_pretrend.csv;
writes derived/spec_summary.csv. Rows with a first-stage F below 10 are counted separately, since
their Wald intervals are not valid.

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 \
    infra/immigration-fiscal/ancestry_iv_congestion_wages_2026_09_23/spec_summary.py
"""
import numpy as np
import pandas as pd

from common import DERIVED


def first_stage_f(est: pd.DataFrame) -> pd.Series:
    """First-stage F for each IV row: the row 'first stage on <instrument>' with the same keys (for a
    two-instrument set, the joint F that menu() stores on its 'coefficient on' rows)."""
    keys = [c for c in ("design", "endpoint", "outcome", "x", "controls") if c in est.columns]
    fs = est[est.estimator.str.startswith("first stage on ")]
    inst = (fs.estimator.str.replace("first stage on ", "", regex=False)
            .str.replace(r", coefficient on .*$", "", regex=True))
    fs = fs.assign(inst=inst).drop_duplicates(keys + ["inst"])[keys + ["inst", "F"]]
    iv = est[est.estimator.str.startswith("IV with ")]
    inst = (iv.estimator.str.replace("IV with ", "", regex=False)
            .str.replace(" + baseline level", "", regex=False))
    j = iv.assign(inst=inst).reset_index().merge(fs, on=keys + ["inst"], how="left", suffixes=("", "_fs"))
    return j.set_index("index")["F_fs"]


def summarise(est: pd.DataFrame, family: str) -> pd.DataFrame:
    iv = est[est.estimator.str.startswith("IV with ") & ~est.estimator.str.contains("two endogenous")].copy()
    iv["fs_F"] = first_stage_f(est)
    iv["t"] = iv.coef / iv.se
    iv["strong"] = iv.fs_F >= 10
    iv["arm"] = np.where(iv.estimator.str.endswith("+ baseline level"), "baseline-level control", "long difference")
    rows = []
    for (outcome, x, arm), g in iv.groupby(["outcome", "x", "arm"], sort=False):
        s = g[g.strong]
        ar = s[s.ar_kind.eq("bounded")]
        rows.append({"family": family, "outcome": outcome, "x": x, "arm": arm, "iv_rows": len(g), "strong_rows": len(s),
                     "coef_min_strong": s.coef.min() if len(s) else np.nan,
                     "coef_max_strong": s.coef.max() if len(s) else np.nan,
                     "wald_negative_strong": int((s.t < -1.96).sum()), "wald_positive_strong": int((s.t > 1.96).sum()),
                     "ar_rows_strong": len(ar), "ar_excludes_zero_negative": int((ar.ar_hi < 0).sum()),
                     "ar_excludes_zero_positive": int((ar.ar_lo > 0).sum()),
                     "weak_rows": int((~g.strong).sum())})
    return pd.DataFrame(rows)


def main():
    c = pd.read_csv(DERIVED / "estimates_commute.csv")
    w = pd.read_csv(DERIVED / "estimates_wages.csv")
    p = pd.read_csv(DERIVED / "estimates_pretrend.csv")
    out = pd.concat([summarise(c, "commute"), summarise(w, "wages"), summarise(p, "pre-trend")], ignore_index=True)
    out.to_csv(DERIVED / "spec_summary.csv", index=False)
    with pd.option_context("display.width", 250, "display.max_rows", 400, "display.max_colwidth", 48):
        print(out.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
