"""Join the source-owned native-minor calibration by explicit person identity."""
from pathlib import Path

import numpy as np
import pandas as pd

SOURCE = Path(__file__).resolve().parent.parent / "count_composition_r5_2026_10_15/derived/native_person_factors.parquet"


def observed_factors(d):
    """Return source factors in caller order; never match by row position.

    A subset of source people is allowed, but every caller identity must have
    exactly one non-null source identity and a finite, nonnegative factor.
    """
    source = pd.read_parquet(SOURCE, columns=["PH_SEQ", "PPPOS", "central_member_factor"])
    keys = ["PH_SEQ", "PPPOS"]
    if source[keys].isna().any().any() or d[keys].isna().any().any():
        raise ValueError("[BLOCKED] null calibration person identity")
    if source.duplicated(keys).any() or d.duplicated(keys).any():
        raise ValueError("[BLOCKED] duplicate calibration person identity")
    indexed = source.set_index(keys).central_member_factor
    values = indexed.reindex(pd.MultiIndex.from_frame(d[keys])).to_numpy(float)
    if not np.isfinite(values).all() or np.any(values < 0):
        raise ValueError("[BLOCKED] missing or invalid source calibration factor")
    return values
