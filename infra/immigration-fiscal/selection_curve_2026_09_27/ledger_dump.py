#!/usr/bin/env python3
"""Per-person dump of the Indian ledger's 2025 partial fiscal net, for the tail-share task.

Imports `indian_ledger_2026_09_18/ledger_india.py` unchanged (which imports the upstream
`build/analyze_cps_fiscal_2025.py` and `gen_ledger_extension_2026_09_16/extend_ledger.py`) and
writes, for civilian adults 25-64, the person-level `extended_balance_after_health` under the
headline allocation (`equal_all_members`), earnings, weights and group masks. Nothing upstream is
written. Output: `_cache/ledger_persons.csv.gz` (ignored).

Run from the repo root:
  uv run --no-project --with "pandas>=2" --with "numpy>=2" python3 \
      infra/immigration-fiscal/selection_curve_2026_09_27/ledger_dump.py
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
INDIAN = HERE.parent / "indian_ledger_2026_09_18"
sys.path.insert(0, str(INDIAN))
sys.path.insert(0, str(HERE.parent / "cps_generation_welfare_2026_09_16"))

import ledger_india as li  # noqa: E402

for _f in ["A_SEX", "A_HGA"]:
    if _f not in li.base.PERSON:
        li.base.PERSON.append(_f)


def main() -> int:
    cps = li.resolve_cps(None)
    print(f"[dump] CPS {cps} sha256 {li.sha256(cps)}", flush=True)
    state = li.ext.build(argparse.Namespace(cps_zip=cps))
    d = state["d"]
    groups = li.build_groups(d)
    meps_zip = li._data_paths.data_root(require_exists=False) / "external/stage3/ahrq/meps_2024/h256dat.zip"
    meps_sas = li._data_paths.data_root(require_exists=False) / "external/stage3/ahrq/meps_2024/h256su.txt"
    health = li.health_person_means(d, meps_zip, meps_sas)
    per = li.per_person_metrics(state, "equal_all_members", health)

    age = d.A_AGE.to_numpy()
    civ = d.PRPERTYP.eq(2).to_numpy()
    use = civ & (age >= 25) & (age <= 64)
    resources = d.SPM_RESOURCES.to_numpy(dtype=float)
    w0 = d.MARSUPWT.to_numpy(dtype=float)
    order = np.argsort(resources[use], kind="stable")
    cum = np.cumsum(w0[use][order]) / w0[use].sum()
    thresh = float(resources[use][order][np.searchsorted(cum, 0.99)])

    out = pd.DataFrame({
        "age": age[use], "sex": d.A_SEX.to_numpy()[use], "a_hga": d.A_HGA.to_numpy()[use],
        "earnings": d.PEARNVAL.to_numpy(dtype=float)[use],
        "wsal": d.WSAL_VAL.to_numpy(dtype=float)[use],
        "spm_resources": resources[use],
        "top1_resources": (resources > thresh)[use].astype(int),
        "net": per["extended_balance_after_health"][use],
        "net_before_health": per["extended_balance_base"][use],
    })
    for g, m in groups.items():
        out[f"g_{g}"] = m[use].astype(int)
    reps = d[li.base.REPS].to_numpy()[use]
    for j in range(reps.shape[1]):
        out[f"w{j}"] = reps[:, j]
    dest = HERE / "_cache"
    dest.mkdir(exist_ok=True)
    out.to_csv(dest / "ledger_persons.csv.gz", index=False, float_format="%.4f")
    print(f"[dump] {len(out):,} adults 25-64, top-1% SPM threshold {thresh:,.0f}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
