"""Check the pooled linearized standard errors with a PSU bootstrap.

Rao-Wu (n_h - 1) rescaling bootstrap over the HC-036 PSUs within strata: draw
n_h - 1 PSUs with replacement in each stratum, multiply weights by
count x n_h / (n_h - 1), recompute. Persons who appear in two or more years share
a PSU, so the bootstrap carries the between-year correlation the same way the
linearization does. Three quantities are checked: the 65+ public ratio, the
complete account's Medicaid-line change (winsorized at p99.5) and the ledger's
medical + M change (plain). The script stops if any bootstrap SE differs from
its linearized SE by more than 25%.

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 \
      infra/immigration-fiscal/medical_ethnicity_pooled_2026_09_23/validate_se.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

LANE = Path(__file__).resolve().parent
sys.path.insert(0, str(LANE))
from pooled_ratios import CACHE, DERIVED, TRANSPORT_LABELS, Frame  # noqa: E402

REPS = 1000
SEED = 20260923
NAT = {1: "us_born", 2: "foreign_born"}


def _ok(msg):
    print(f"  ✓ {msg}", flush=True)


def fail(msg):
    print(f"  ✗ [BLOCKED] {msg}", file=sys.stderr, flush=True)
    raise SystemExit(2)


def main():
    pool = pd.read_parquet(CACHE / "pooled.parquet")
    fr = Frame(pool, 9.0, "defl_med", "STRA9624", "PSU9624")
    des = fr.design
    caps = {}
    wc = pd.read_csv(DERIVED / "winsor_caps.csv")
    for _, r in wc.iterrows():
        caps[(r.measure, TRANSPORT_LABELS.index(r.band), 1 if r.nativity == "us_born" else 2)] = r.cap_p995
    y_pub = fr.y["public"]
    y_mcd_w = fr.capped("medicaid", caps)
    y_mcd = fr.y["medicaid"]
    y_mcr = fr.y["medicare"]
    mex = fr.groups["mexican_origin"]
    cell = np.where(fr.valid, fr.tb * 2 + (fr.born - 1), -1).astype(np.int64)   # 10 transport cells
    old = fr.valid & (fr.age >= 65)

    cells = pd.read_csv(DERIVED / "cps_cells.csv")
    params = json.loads((LANE.parent / "ledger_absolute_2026_09_17/params/params.json").read_text())["meps_coverage"]
    r_mcd = params["nhea_to_meps_ratio_medicaid"]["value"]
    r_mcr = params["nhea_to_meps_ratio_medicare"]["value"]
    order = [(b, n) for b in range(5) for n in (1, 2)]
    cw = cells.set_index(["band", "nativity"])
    led_med = np.array([cw.loc[(TRANSPORT_LABELS[b], NAT[n]), "ledger_medical_cost"] for b, n in order])
    led_mcd = np.array([cw.loc[(TRANSPORT_LABELS[b], NAT[n]), "union_exposed"] *
                        cw.loc[(TRANSPORT_LABELS[b], NAT[n]), "meps2024_medicaid"] * (r_mcd - 1) for b, n in order])
    led_mcr = np.array([cw.loc[(TRANSPORT_LABELS[b], NAT[n]), "union_exposed"] *
                        cw.loc[(TRANSPORT_LABELS[b], NAT[n]), "meps2024_medicare"] * (r_mcr - 1) for b, n in order])
    key_mcd = np.array([cw.loc[(TRANSPORT_LABELS[b], NAT[n]), "key_medicaid"] for b, n in order])
    ta = pd.read_csv(DERIVED / "translation_account.csv")
    line_bn = float(ta[(ta.spec == "winsor_p995") & (ta.line == "medicaid_and_chip_other_medical")].account_target_bn.iloc[0])

    def stats(w):
        def cell_ratio(y):
            keep = cell >= 0
            num = np.bincount(cell[keep & mex], weights=(w * y)[keep & mex], minlength=10)
            numw = np.bincount(cell[keep & mex], weights=w[keep & mex], minlength=10)
            den = np.bincount(cell[keep], weights=(w * y)[keep], minlength=10)
            denw = np.bincount(cell[keep], weights=w[keep], minlength=10)
            return (num / numw) / (den / denw)
        def dsum(a, r):
            # cells the account gives no dollars (e.g. Medicare for foreign-born children) drop
            # out, as in translate.py; their ratio can be 0/0 in a replicate
            live = a != 0
            return float((a[live] * (r[live] - 1)).sum())
        r65 = ((w * y_pub)[old & mex].sum() / w[old & mex].sum()) / ((w * y_pub)[old].sum() / w[old].sum())
        acc = line_bn * dsum(key_mcd / key_mcd.sum(), cell_ratio(y_mcd_w))
        led = (dsum(led_med, cell_ratio(y_pub)) + dsum(led_mcd, cell_ratio(y_mcd))
               + dsum(led_mcr, cell_ratio(y_mcr))) / 1e9
        return np.array([r65, acc, led])

    point = stats(fr.w)
    rng = np.random.default_rng(SEED)
    groups = [np.where(des.stratum_of_psu == h)[0] for h in range(len(des.strata))]
    out = np.empty((REPS, 3))
    for b in range(REPS):
        lam = np.zeros(des.n_psu)
        for idx in groups:
            nh = len(idx)
            counts = np.bincount(rng.integers(0, nh, size=nh - 1), minlength=nh)
            lam[idx] = counts * nh / (nh - 1)
        rec = np.where(des.psu_index >= 0, lam[np.maximum(des.psu_index, 0)], 0.0)
        out[b] = stats(fr.w * rec)
        if (b + 1) % 200 == 0:
            print(f"  [{b + 1}/{REPS}] bootstrap replicates", flush=True)
    if not np.isfinite(out).all():
        fail(f"{int((~np.isfinite(out)).any(axis=1).sum())} bootstrap replicates are not finite")
    boot = out.std(axis=0, ddof=1)

    rt = pd.read_csv(DERIVED / "ratios.csv")
    lin65 = rt[(rt["sample"] == "pooled_2016_2024") & (rt.spec == "plain") & (rt.scheme == "age_domain")
               & (rt.band == "65plus") & (rt.nativity == "both") & (rt.comparison == "mexican_origin/all_donors")
               & (rt.measure == "public")].iloc[0]
    tl = pd.read_csv(DERIVED / "translation_ledger.csv")
    lin_led = tl[(tl.spec == "plain") & (tl.age_group == "all ages") & (tl.nativity == "both")
                 & (tl.component == "medical+M")].iloc[0]
    lin_acc = ta[(ta.spec == "winsor_p995") & (ta.line == "medicaid_and_chip_other_medical")].iloc[0]
    checks = [("65+ public ratio, plain", point[0], lin65.ratio, lin65.se, boot[0]),
              ("account Medicaid line change $bn, winsor p99.5", point[1], lin_acc.delta_bn, lin_acc.se_bn, boot[1]),
              ("ledger medical+M change $bn, plain", point[2], lin_led.delta_cost_bn, lin_led.se_bn, boot[2])]
    res = []
    for name, pt, lin_pt, lin_se, bse in checks:
        if abs(pt - lin_pt) > 1e-6 * max(1.0, abs(lin_pt)):
            fail(f"{name}: bootstrap point {pt} != published {lin_pt}")
        rel = abs(bse - lin_se) / lin_se
        res.append(dict(quantity=name, estimate=lin_pt, linearized_se=lin_se, bootstrap_se=bse,
                        relative_difference=rel, replicates=REPS, seed=SEED))
        _ok(f"{name}: {lin_pt:.3f}, linearized SE {lin_se:.3f}, bootstrap SE {bse:.3f} ({rel:.1%} apart)")
        if rel > 0.25:
            fail(f"{name}: linearized and bootstrap SEs differ by {rel:.1%}")
    pd.DataFrame(res).to_csv(DERIVED / "se_validation.csv", index=False)
    _ok("se_validation.csv written")


if __name__ == "__main__":
    main()
