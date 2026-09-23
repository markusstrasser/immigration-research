"""Shared estimators for the arrival-cohort and mover lanes.

Every estimate is computed on 81 weight columns: column 0 is the full-sample weight, 1-80 are
replicates. ACS replicates are the Census Bureau's successive-difference weights (variance
4/80 * sum of squared deviations from the full-sample estimate). Census 1980-2000 replicates are a
delete-a-group jackknife over 80 household groups (variance 79/80 * sum of squared deviations).
A reference population supplied with the main weight only is held fixed across replicates, and
the SE then covers the other side's sampling error alone; README states where that applies.
"""
import numpy as np
import pandas as pd

R = 80
BINS = [("0-5", 0, 5), ("6-10", 6, 10), ("11-15", 11, 15)]


def ysm_bin(ysm: pd.Series) -> pd.Series:
    out = pd.Series(pd.NA, index=ysm.index, dtype="object")
    for label, lo, hi in BINS:
        out[(ysm >= lo) & (ysm <= hi)] = label
    return out


def educ3(educ: pd.Series) -> pd.Series:
    """IPUMS EDUC: <=5 fewer than 12 years; 6 grade 12 (diploma, GED or 12th grade without one); 7+ college."""
    return pd.Series(np.select([educ <= 5, educ == 6], ["lt12", "g12"], "col"), index=educ.index)


def variance(theta: np.ndarray, kind: str) -> float:
    """theta[0] full sample, theta[1:] replicates."""
    reps = theta[1:]
    if kind == "sdr":
        return 4.0 / R * float(np.sum((reps - theta[0]) ** 2))
    if kind == "jk":
        return (R - 1) / R * float(np.sum((reps - reps.mean()) ** 2))
    raise ValueError(kind)


def wcols(prefix: str) -> list[str]:
    return [f"{prefix}{k}" for k in range(R + 1)]


def aggregate(df: pd.DataFrame, keys: list[str], weights: np.ndarray, inst: np.ndarray,
              extra: dict | None = None) -> pd.DataFrame:
    """Sum weights (n x 81) and inst-weighted weights over keys. extra: {name: 0/1 array} adds more numerators."""
    cols = {f"w{k}": weights[:, k] for k in range(R + 1)}
    cols.update({f"i{k}": weights[:, k] * inst for k in range(R + 1)})
    for name, flag in (extra or {}).items():
        cols.update({f"{name}{k}": weights[:, k] * flag for k in range(R + 1)})
    frame = pd.concat([df[keys].reset_index(drop=True), pd.DataFrame(cols)], axis=1)
    frame["n"] = 1
    frame["n_inst"] = inst.astype(int)
    return frame.groupby(keys, dropna=False, observed=True).sum().reset_index()


def rate(cells: pd.DataFrame, num: str = "i") -> np.ndarray:
    w = cells[wcols("w")].to_numpy().sum(axis=0)
    i = cells[wcols(num)].to_numpy().sum(axis=0)
    return i / w


def standardized(target: pd.DataFrame, ref: pd.DataFrame, strata: list[str], num: str = "i") -> dict:
    """Indirect standardization: observed target rate over the rate the reference would have at the
    target's own distribution across strata (e.g. single years of age). Returns 81-vectors."""
    t = target.groupby(strata)[wcols("w") + wcols(num)].sum()
    r = ref.groupby(strata)[wcols("w") + wcols(num)].sum()
    t = t.join(r, rsuffix="_ref", how="left")
    tw = t[wcols("w")].to_numpy()
    ti = t[wcols(num)].to_numpy()
    rw = t[[f"{c}_ref" for c in wcols("w")]].to_numpy()
    ri = t[[f"{c}_ref" for c in wcols(num)]].to_numpy()
    if np.isnan(rw).any():
        missing = t.index[np.isnan(rw[:, 0])].tolist()
        raise ValueError(f"reference has no cases in strata {missing[:5]}")
    ref_rate = np.divide(ri, rw, out=np.zeros_like(ri), where=rw > 0)
    observed = ti.sum(axis=0) / tw.sum(axis=0)
    expected = (tw * ref_rate).sum(axis=0) / tw.sum(axis=0)
    return {"observed": observed, "expected": expected, "ratio": observed / expected}


def summarize(vec: np.ndarray, kind: str) -> tuple[float, float]:
    return float(vec[0]), float(np.sqrt(variance(vec, kind)))
