"""Read-only pooled OFD+STL ratio covariance for item21's own donor cells.

Native-First: use the source Frame, ratio influences and stratified-PSU design.
"""
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
sys.path.insert(0, str(FISCAL/"spending_keys_r5_2026_10_15"))
sys.path.insert(0, str(FISCAL/"scripts"))
from health_ratios import Frame, cell_caps, estimate_rows, mean, ratio, verify_published
from memory_budget import require_within_budget


def build():
    from oct16_sampling import ROOT, digest, require
    source = FISCAL/"medical_ethnicity_pooled_2026_09_23"
    pool = source/"_cache/pooled.parquet"
    fr = Frame(pd.read_parquet(pool), 9., "defl_med", "STRA9624", "PSU9624")
    plain = estimate_rows(fr, "ofd_stl", "plain")
    verify_published(plain, pd.read_csv(source/"derived/ratios.csv"))
    cells, influences, expected = [], [], []
    y = fr.capped("ofd_stl", cell_caps(fr, "ofd_stl"))
    rows = estimate_rows(fr, "ofd_stl", "winsor_p995")
    for row in rows:
        band = ["0-17", "18-34", "35-49", "50-64", "65+"].index(row["band"])
        born = 1 if row["nativity"] == "us_born" else 2
        mask = fr.valid & (fr.tb == band) & (fr.born == born)
        est = ratio(mean(fr.design, y, fr.w, mask & fr.groups["mexican_origin"]), mean(fr.design, y, fr.w, mask))
        require(abs(est.value-row["ratio"]) < 1e-12 and abs(est.se(fr.design)-row["se"]) < 1e-12,
                "pooled OFD/STL ratio influence does not reproduce its own SE")
        cells.append({**row, "cell": row["band"]+"|"+row["nativity"]})
        influences.append(est.T)
        expected.append(row["se"]**2)
    covariance = np.zeros((10, 10))
    for i in range(10):
        for j in range(10):
            covariance[i, j] = (fr.design.var(influences[i]+influences[j])
                                 - fr.design.var(influences[i]-influences[j]))/4
    require(np.allclose(np.diag(covariance), expected, rtol=1e-12, atol=1e-12), "pooled covariance diagonal differs")
    require(np.linalg.eigvalsh(covariance).min() > -1e-10, "pooled covariance not PSD")
    paths = [pool, source/"pooled_ratios.py", source/"design.py", source/"derived/ratios.csv",
             FISCAL/"spending_keys_r5_2026_10_15/health_ratios.py", Path(__file__).resolve()]
    result = {"measure": "ofd_stl", "specification": "winsor_p995", "cells": cells,
        "covariance": covariance.tolist(),
        "rule": "own pooled2016–2024 ratio influences; PSU-stratified Taylor covariance retained across all10 cells; not sum of independent generation SEs",
        "gates": {"plain_primary_oracle": True, "ratio_and_own_se_1e_12": True, "diagonal_and_psd": True},
        "source_sha256": {str(p.relative_to(ROOT)): digest(p) for p in paths}}
    require_within_budget("item21 pooled ratio covariance")
    return result


if __name__ == "__main__":
    target = HERE/"derived/oct16/item21_pooled_covariance.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(build(), indent=2, allow_nan=False)+"\n")
    print("PASS item21 OFD+STL own pooled ratio SEs and full ten-cell covariance")
