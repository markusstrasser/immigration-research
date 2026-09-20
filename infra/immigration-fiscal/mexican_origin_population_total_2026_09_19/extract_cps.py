#!/usr/bin/env python3
"""Extract the CPS ASEC 2025 person columns this lane needs, plus replicate weights.

Input (read-only):
  ~/research-data/immigration-fiscal/data/external/stage3/census/cps_asec_2025/asecpub25csv.zip
    pppub25.csv               person records (income year 2024, interview Feb-Apr 2025)
    asec_csv_repwgt_2025.csv  full + 160 replicate person weights

Output: _cache/cps_asec2025_person_subset.parquet (gitignored)

Deterministic: rows are sorted by (PH_SEQ, A_LINENO) before writing.
"""
from __future__ import annotations

import sys as _path_sys
from pathlib import Path as _Path
_path_sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "build"))
import paths as _data_paths


import sys
import zipfile
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
ZIP = (_data_paths.data_root(require_exists=False) / 'external/stage3/census'
       / "cps_asec_2025/asecpub25csv.zip")

PERSON_COLS = [
    "PH_SEQ", "A_LINENO", "PPPOS", "PERRP", "PRPERTYP",
    "PEHSPNON", "PRDTHSP", "PRDTRACE",
    "PENATVTY", "PEMNTVTY", "PEFNTVTY", "PRCITSHP", "PEINUSYR",
    "PEPAR1", "PEPAR2", "PEPAR1TYP", "PEPAR2TYP",
    "A_AGE", "A_SEX", "A_HGA", "MARSUPWT", "PTOTVAL", "PEARNVAL",
]
REP_N = 160


def main() -> int:
    CACHE.mkdir(exist_ok=True)
    out = CACHE / "cps_asec2025_person_subset.parquet"
    if out.exists():
        print(f"cached: {out} ({out.stat().st_size/1e6:.1f} MB) — skipping", flush=True)
        return 0
    with zipfile.ZipFile(ZIP) as z:
        print("reading pppub25.csv", flush=True)
        with z.open("pppub25.csv") as fh:
            per = pd.read_csv(fh, usecols=PERSON_COLS, low_memory=False)
        print(f"  person rows: {len(per):,}", flush=True)
        print("reading asec_csv_repwgt_2025.csv", flush=True)
        rep_cols = ["h_seq", "PPPOS"] + [f"pwwgt{i}" for i in range(0, REP_N + 1)]
        with z.open("asec_csv_repwgt_2025.csv") as fh:
            rep = pd.read_csv(fh, usecols=rep_cols, low_memory=False)
        print(f"  repwgt rows: {len(rep):,}", flush=True)

    rep = rep.rename(columns={"h_seq": "PH_SEQ"})
    d = per.merge(rep, on=["PH_SEQ", "PPPOS"], how="inner", validate="one_to_one")
    if len(d) != len(per):
        raise SystemExit(f"merge lost rows: {len(per)} -> {len(d)}")

    # MARSUPWT carries two implied decimals in the public CSV; pwwgt0 is the same
    # full weight already scaled.  Verify the two agree before relying on pwwgt.
    ratio = (d["MARSUPWT"] / d["pwwgt0"]).replace([float("inf")], pd.NA).dropna()
    print(f"  MARSUPWT/pwwgt0: min={ratio.min():.4f} max={ratio.max():.4f} "
          f"median={ratio.median():.4f}", flush=True)

    d = d.sort_values(["PH_SEQ", "A_LINENO"], kind="mergesort").reset_index(drop=True)
    d.to_parquet(out, index=False, compression="zstd")
    print(f"wrote {out} ({out.stat().st_size/1e6:.1f} MB)", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
