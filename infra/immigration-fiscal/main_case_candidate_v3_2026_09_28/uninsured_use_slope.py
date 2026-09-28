"""Item 10's evidence re-read: the hospital use rate r that the CMS S-10 slope implies, in the published-figures back-test's
primary fit and in its region-controlled fit (backtest_published_2026_09_28, 340c8a6).

The back-test regressed each state's log ratio of its S-10 uncompensated-care share to the account's key share on the
group's share of the state's uninsured person-years g, weighted by the key share, with the 2023 expansion indicator. It
read the primary slope as a use rate through the key that r would produce, and it reported the region-controlled fit
(post hoc) as a slope only. This script reads both as use rates with the same map, from the lane's committed state
table: the key at r is the account's key times (1 - (1 - r) g), renormalized (the table's account_r07 column is this at
r = 0.7). The map holds the fit's own regressors, so the region fit is read through the region fit.

Gates: the table's r = 0.7 column is reproduced (1e-12 relative); both fits reproduce hcris_fits.csv's slope and
standard error (1e-9); the primary fit's implied r reproduces notes.csv (1e-6); the map reproduces the frozen r = 0.7
alternative slope within the lane's own tolerance (2e-3). The census regions are read from score.py's REGIONS literal
without running it. Writes derived/uninsured_use_slope.json; exit 1 and nothing written on a failed gate. Run from the
repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/main_case_candidate_v3_2026_09_28/uninsured_use_slope.py
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import ast  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
DERIVED = HERE / "derived"
BT = "backtest_published_2026_09_28"
STATES = f"{BT}/derived/hcris_s10_states.csv"
FITS = f"{BT}/derived/hcris_fits.csv"
NOTES = f"{BT}/derived/notes.csv"
SCORE = f"{BT}/score.py"
SOURCES = [STATES, FITS, NOTES, SCORE]
PRIMARY = "primary: weighted, expansion"
REGION_FIT = "post hoc: weighted, expansion, Census regions"
Z95 = 1.959963984540054  # score.py's
GATES: list[dict] = []


def gate(name, ok, detail=""):
    GATES.append({"gate": name, "passed": bool(ok), "detail": detail})
    print(f"  {'PASS' if ok else 'FAIL'} {name}{' — ' + detail if detail else ''}")


def sha256(rel):
    return hashlib.sha256((FISCAL / rel).read_bytes()).hexdigest()


def regions_literal():
    tree = ast.parse((FISCAL / SCORE).read_text())
    hits = [n.value for n in tree.body if isinstance(n, ast.Assign) and any(getattr(t, "id", None) == "REGIONS" for t in n.targets)]
    if len(hits) != 1:
        raise SystemExit(f"[BLOCKED] {SCORE}: {len(hits)} REGIONS assignments, not one")
    return ast.literal_eval(hits[0])


def wls_hc1(y, X, w):
    # score.py's wls_hc1: weighted least squares with HC1 standard errors.
    sw = np.sqrt(w)
    Xs, ys = X * sw[:, None], y * sw
    xtx_inv = np.linalg.inv(Xs.T @ Xs)
    beta = xtx_inv @ Xs.T @ ys
    e = ys - Xs @ beta
    n, k = Xs.shape
    cov = xtx_inv @ ((Xs * e[:, None] ** 2).T @ Xs) @ xtx_inv * n / (n - k)
    return beta, np.sqrt(np.diag(cov))


def main():
    before = {rel: sha256(rel) for rel in SOURCES}
    st = pd.read_csv(FISCAL / STATES)
    fits = pd.read_csv(FISCAL / FITS).set_index("fit")
    notes = pd.read_csv(FISCAL / NOTES)
    regions = regions_literal()
    g = st.group_share_of_uninsured.to_numpy()
    k1 = st.account_r1.to_numpy()
    y = np.log(st.s10_share.to_numpy() / k1)
    expansion = st.not_expanded_2023_kff.to_numpy(float)
    dummies = [st.state.isin(regions[r].split()).to_numpy(float) for r in ("Midwest", "South", "West")]
    design = {PRIMARY: np.column_stack([np.ones(len(st)), g, expansion]),
              REGION_FIT: np.column_stack([np.ones(len(st)), g, expansion, *dummies])}

    def key_at(r):
        k = k1 * (1 - (1 - r) * g)
        return k / k.sum()

    def implied_slope(r, X):
        return float(np.linalg.lstsq(X * np.sqrt(k1)[:, None], np.log(key_at(r) / k1) * np.sqrt(k1), rcond=None)[0][1])

    def implied_r(target, X):  # the implied slope rises with r; None outside (0.001, 1.5), the lane's bracket
        lo, hi = 1e-3, 1.5
        if not implied_slope(lo, X) <= target <= implied_slope(hi, X):
            return None
        for _ in range(80):
            mid = (lo + hi) / 2
            lo, hi = (lo, mid) if implied_slope(mid, X) > target else (mid, hi)
        return (lo + hi) / 2

    print("[gates: the back-test reproduced]")
    r07 = key_at(0.7)
    gate("the key at r = 0.7 is the table's account_r07 column (1e-12 relative)",
         np.allclose(r07, st.account_r07.to_numpy(), rtol=1e-12, atol=0), f"max rel diff {np.max(np.abs(r07 / st.account_r07.to_numpy() - 1)):.1e}")
    gate("census regions: 51 codes, each state of the table in exactly one", sorted(sum((v.split() for v in regions.values()), []))
         == sorted(st.state) and len(st) == 51, f"{len(st)} states")
    out = {}
    for name, X in design.items():
        beta, se = wls_hc1(y, X, k1)
        want = fits.loc[name]
        gate(f"{name}: slope and SE are hcris_fits.csv's (1e-9)", abs(beta[1] - want.slope) < 1e-9 and abs(se[1] - want.se) < 1e-9,
             f"{beta[1]:.4f} ({se[1]:.4f})")
        ci = [beta[1] - Z95 * se[1], beta[1] + Z95 * se[1]]
        out[name] = {"post_hoc": bool(want.post_hoc), "slope": beta[1], "se": se[1], "ci95": ci,
                     "slope_at_r07": implied_slope(0.7, X), "implied_r": implied_r(beta[1], X),
                     "implied_r_ci95": [implied_r(c, X) for c in ci]}
    prim = out[PRIMARY]
    lane_r = notes.loc[(notes.check == 3) & (notes.kind == "post-hoc explanation"), "value"]
    gate("the primary fit's implied r is notes.csv's (1e-6)", len(lane_r) == 1 and abs(prim["implied_r"] - float(lane_r.iloc[0])) < 1e-6,
         f"{prim['implied_r']:.4f}")
    alt = float(fits.loc[PRIMARY].alternative)
    gate("the map gives the frozen r = 0.7 alternative slope (the lane's tolerance, 2e-3)", abs(prim["slope_at_r07"] - alt) < 2e-3,
         f"{prim['slope_at_r07']:.5f} against {alt:.5f}")
    gate("the sources did not change during the run", before == {rel: sha256(rel) for rel in SOURCES})
    if not all(x["passed"] for x in GATES):
        raise SystemExit(f"[BLOCKED] {sum(not x['passed'] for x in GATES)} gate(s) failed; nothing written")

    DERIVED.mkdir(exist_ok=True)
    (DERIVED / "uninsured_use_slope.json").write_text(json.dumps({
        "meta": {"lane": "main_case_candidate_v3_2026_09_28", "item": "10",
                 "definition": ("use rate r implied by a fitted slope: the r whose key, account key x (1 - (1 - r) g) renormalized, "
                                "gives that slope in the same weighted regression with the same regressors; None outside (0.001, 1.5)"),
                 "sources": before},
        "fits": out, "gates": GATES}, indent=1) + "\n")
    reg = out[REGION_FIT]
    fmt = lambda v: "above 1.5" if v is None else f"{v:.2f}"  # noqa: E731
    print(f"\n  primary: slope {prim['slope']:.3f} -> r {prim['implied_r']:.2f} ({fmt(prim['implied_r_ci95'][0])}-{fmt(prim['implied_r_ci95'][1])})")
    print(f"  regions: slope {reg['slope']:.3f} (r = 0.7 gives {reg['slope_at_r07']:.3f}) -> r {fmt(reg['implied_r'])} "
          f"({fmt(reg['implied_r_ci95'][0])}-{fmt(reg['implied_r_ci95'][1])})")
    print(f"all {len(GATES)} gates passed; wrote derived/uninsured_use_slope.json")


if __name__ == "__main__":
    main()
