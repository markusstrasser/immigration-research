#!/usr/bin/env python3
"""Gates for the late-arrival lane. Exit 1 on any failure.

1. ACS weighted Mexico-born (and India-born) totals within 1% of published B05006, each year.
2. Yearbook IR-5 totals equal the published all-country total each year (flow_gates.csv).
3. The ledger loaders run without [BLOCKED], and the pooled-profile arm reproduces the ledger's
   own survival NPV of the Mexico-born and white age vectors.
4. per_admission.csv has every arm, case, survival, rate and arrival age, all finite. No sign
   is asserted between statutory and observed_late: the priced floor can exceed observed care.

Run: OPENBLAS_NUM_THREADS=1 uv run --no-project python3 \
         infra/immigration-fiscal/late_arrival_tail_2026_09_27/verify.py
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = HERE / "derived"
results: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    results.append((name, bool(ok), detail))


def main() -> None:
    g = pd.read_csv(OUT / "acs_gate.csv")
    check("ACS vs B05006 within 1% (8 year-groups)",
          len(g) == 8 and (g.pct_diff.abs() < 1).all() and g.pass_within_1pct.all(),
          f"max |diff| {g.pct_diff.abs().max():.2f}%")
    f = pd.read_csv(OUT / "flow_gates.csv")
    check("IR-5 flow gates", f["pass"].all(), f"{int(f['pass'].sum())}/{len(f)}")
    tbl6 = f[f.gate.str.contains("Yearbook Table 6 Parents")]
    check("IR-5 Total = Yearbook Table 6 Parents, FY2005-2024", len(tbl6) == 20 and tbl6["pass"].all(),
          f"{len(tbl6)} years")

    spec = importlib.util.spec_from_file_location(
        "ledger_lifetime", ROOT / "infra/immigration-fiscal/ledger_absolute_2026_09_17/lifetime.py")
    lt = importlib.util.module_from_spec(spec)
    sys.modules["ledger_lifetime"] = lt
    spec.loader.exec_module(lt)
    try:
        profiles, _ = lt.load_age_profiles(ROOT)
        check("ledger loaders run without [BLOCKED]", True)
    except ValueError as e:
        check("ledger loaders run without [BLOCKED]", False, str(e))
        return
    tables = {k: lt.read_life_table(ROOT, k) for k in ("hispanic", "nh_white")}
    pa = pd.read_csv(OUT / "per_admission.csv")
    mb = lt.age_vector(profiles, "mexico_born")
    wh = lt.age_vector(profiles, "third_plus_nh_white")
    worst = 0.0
    for a0 in (45, 50, 55, 60, 65):
        for r in (0.0, 0.03):
            ref_p = lt.survival_npv(mb, tables["hispanic"], a0, r)[0]
            ref_w = lt.survival_npv(wh, tables["nh_white"], a0, r)[0]
            row = pa[(pa.arm == "pooled_profile") & (pa.survival == "group_specific")
                     & (pa.arrival_age == a0) & (pa.real_rate == r)]
            worst = max(worst, abs(row.npv_parent.iloc[0] - ref_p), abs(row.npv_white_same_age.iloc[0] - ref_w))
    check("pooled arm reproduces ledger survival NPVs (to $1)", worst < 1.0, f"max diff ${worst:.2f}")
    expect = 5 * (1 + 3 + 3 + 3) * 2 * 4
    check("per_admission.csv complete and finite",
          len(pa) == expect and np.isfinite(pa[["npv_parent", "npv_white_same_age"]]).all().all(),
          f"{len(pa)} rows, expected {expect}")
    fv = pd.read_csv(OUT / "flow_valuation.csv")
    check("flow valuation present", len(fv) > 0 and np.isfinite(fv.flow_npv_bn).all(), f"{len(fv)} rows")


if __name__ == "__main__":
    main()
    for name, ok, detail in results:
        print(f"  {'✓' if ok else '✗'} {name}{' — ' + detail if detail else ''}")
    bad = [r for r in results if not r[1]]
    print(f"{len(results) - len(bad)}/{len(results)} gates pass")
    sys.exit(1 if bad else 0)
