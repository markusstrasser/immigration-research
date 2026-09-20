#!/usr/bin/env python3
"""Native low-skilled workers' earnings base, for the offsetting wage channel.

Cortes (2008) finds a 10% increase in the low-skilled immigrant share of the labor
force reduces the wages of low-skilled NATIVES by 0.6% (and of low-skilled immigrants
by 8.0%).  Removing the Mexico-born low-skilled share therefore RAISES native
low-skilled wages under the same log-linear extrapolation, an offset to the consumer
loss.  This pass sizes the affected earnings base from ACS 2024.
"""
from __future__ import annotations

import sys as _path_sys
from pathlib import Path as _Path
_path_sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "build"))
import paths as _data_paths

import json, zipfile
from pathlib import Path
import numpy as np, pandas as pd

HERE = Path(__file__).resolve().parent
OUT = HERE / "derived"
DATA = _data_paths.data_root(require_exists=False) / 'external/acs_pums_2024_1yr'
COLS = ["PWGTP", "AGEP", "NATIVITY", "POBP", "SCHL", "ESR", "PERNP", "WAGP", "ADJINC", "SERIALNO"]


def main() -> None:
    parts = []
    with zipfile.ZipFile(DATA / "csv_pus.zip") as z:
        for name in sorted(n for n in z.namelist() if n.lower().endswith(".csv")):
            print(f"[read] {name}", flush=True)
            with z.open(name) as fh:
                for ch in pd.read_csv(fh, usecols=COLS, dtype={"SERIALNO": str},
                                      chunksize=500_000, low_memory=False):
                    parts.append(ch[(ch.AGEP >= 16) & ch.ESR.isin([1, 2])].copy())
    df = pd.concat(parts, ignore_index=True)
    adj = df.ADJINC / 1e6
    earn = df.PERNP.fillna(0) * adj
    w = df.PWGTP.to_numpy(float)
    native = (df.NATIVITY == 1).to_numpy()
    drop = (df.SCHL <= 15).to_numpy()
    noco = (df.SCHL <= 19).to_numpy()
    mex = (df.POBP == 303).to_numpy()
    rows = []
    for lab, m in {
        "native_dropout_employed": native & drop,
        "native_nocollege_employed": native & noco,
        "fb_dropout_employed": (~native) & drop,
        "mexborn_dropout_employed": (~native) & drop & mex,
        "mexborn_nocollege_employed": (~native) & noco & mex,
        "all_employed": np.ones(len(df), bool),
    }.items():
        rows.append(dict(group=lab, workers=float(w[m].sum()),
                         aggregate_earnings_bn=float((w[m] * earn.to_numpy()[m]).sum() / 1e9),
                         mean_earnings=float((w[m] * earn.to_numpy()[m]).sum() / w[m].sum())))
    out = pd.DataFrame(rows)
    out.to_csv(OUT / "native_lowskill_base.csv", index=False)
    print(out.to_string(index=False), flush=True)


if __name__ == "__main__":
    main()
