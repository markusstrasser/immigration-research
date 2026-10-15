"""Lane-owned OFD+STL ethnic translation for item 21.

The pooled producer publishes plain OFD+STL, but its WINSOR_MEASURES omits
OFD+STL. This module explicitly extends that producer's cell-specific 99.5th
percentile construction without modifying it. It imports the producer's Frame,
weighted quantile and survey-design estimators and reads its pooled frame.
No producer, cache or derived output is written.
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import importlib.util
import math
from pathlib import Path

import numpy as np
import pandas as pd

LANE = Path(__file__).resolve().parent
SOURCE = LANE.parent / "medical_ethnicity_pooled_2026_09_23"
POOL = SOURCE / "_cache/pooled.parquet"
RATIOS = SOURCE / "derived/ratios.csv"

_spec = importlib.util.spec_from_file_location("item21_pooled_ratios", SOURCE / "pooled_ratios.py")
if _spec is None or _spec.loader is None:
    raise RuntimeError("[BLOCKED] cannot load the pooled ratio producer")
_producer = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_producer)
Frame = _producer.Frame
weighted_quantile = _producer.weighted_quantile
mean = _producer.mean
ratio = _producer.ratio


def cell_caps(fr: Frame, measure: str, q: float = 0.995) -> dict:
    """Producer set_caps construction, explicitly extended to OFD+STL.

Quantiles include zero-spending donors. A zero cap leaves the cell uncapped,
as Frame.capped does; it does not turn a sparse positive tail into zero use.
An empty transport cell is an error rather than an alternate-cell fallback.
"""
    caps = {}
    for band in range(5):
        for born in (1, 2):
            mask = fr.valid & (fr.tb == band) & (fr.born == born)
            if not mask.any():
                raise ValueError(f"[BLOCKED] empty pooled transport cell: {measure}, {band}, {born}")
            cap = weighted_quantile(fr.y[measure][mask], fr.w[mask], q)
            if not np.isfinite(cap) or cap < 0:
                raise ValueError(f"[BLOCKED] invalid pooled cap: {measure}, {band}, {born}: {cap}")
            caps[(measure, band, born)] = float(cap)
    return caps


def estimate_rows(fr: Frame, measure: str, spec: str) -> list[dict]:
    """The ten age-by-nativity Mexican-origin/all-donor mean ratios and SEs."""
    if spec not in ("plain", "winsor_p995"):
        raise ValueError(f"[BLOCKED] unsupported pooled specification: {spec}")
    caps = cell_caps(fr, measure) if spec == "winsor_p995" else None
    y = fr.y[measure] if caps is None else fr.capped(measure, caps)
    rows = []
    for band, label in enumerate(_producer.TRANSPORT_LABELS):
        for nativity, born in (("us_born", 1), ("foreign_born", 2)):
            mask = fr.valid & (fr.tb == band) & (fr.born == born)
            num_mask = mask & fr.groups["mexican_origin"]
            num = mean(fr.design, y, fr.w, num_mask)
            den = mean(fr.design, y, fr.w, mask)
            est = ratio(num, den)
            se = est.se(fr.design)
            if not (math.isfinite(est.value) and math.isfinite(se)):
                raise ValueError(f"[BLOCKED] undefined pooled ratio/SE: {measure}, {spec}, {label}, {nativity}")
            rows.append({
                "sample": "pooled_2016_2024", "spec": spec, "scheme": "transport",
                "band": label, "nativity": nativity,
                "comparison": "mexican_origin/all_donors", "measure": measure,
                "ratio": float(est.value), "se": float(se),
                "n_num": int(num.n), "n_den": int(den.n),
                "n_positive_num": int((num_mask & (y > 0)).sum()),
                "n_positive_den": int((mask & (y > 0)).sum()),
                "mean_num": float(num.value), "mean_den": float(den.value),
                "cap_p995": None if caps is None else caps[(measure, band, born)],
            })
    return rows


def verify_published(rows: list[dict], published: pd.DataFrame) -> dict:
    """Fail closed on a plain-OFD+STL or winsor-other-public mismatch."""
    worst_ratio, worst_se = 0.0, 0.0
    for row in rows:
        match = published[
            (published["sample"] == row["sample"])
            & (published.spec == row["spec"])
            & (published.scheme == "transport")
            & (published.band == row["band"])
            & (published.nativity == row["nativity"])
            & (published.comparison == row["comparison"])
            & (published.measure == row["measure"])
        ]
        if len(match) != 1:
            raise ValueError(f"[BLOCKED] pooled oracle has {len(match)} rows for {row}")
        old = match.iloc[0]
        for field in ("ratio", "se", "n_num", "n_den"):
            if not math.isclose(row[field], float(old[field]), rel_tol=1e-12, abs_tol=1e-12):
                raise ValueError(f"[BLOCKED] pooled oracle mismatch in {field}: {row} versus {old[field]}")
        worst_ratio = max(worst_ratio, abs(row["ratio"] - float(old["ratio"])))
        worst_se = max(worst_se, abs(row["se"] - float(old["se"])))
    return {"checked": len(rows), "max_abs_ratio_error": worst_ratio, "max_abs_se_error": worst_se}


def build_ratios() -> list[dict]:
    """Return 20 JSON-safe OFD+STL rows; validate source oracles first.

PERWT/9, medical CPI to 2024 dollars, and pooled STRA9624/PSU9624
Taylor-linearization covariance all come from the producer's live Frame.
The 10 existing plain OFD+STL rows and 10 existing winsor other_public rows
must reproduce; there is no fallback to another measure or specification.
"""
    fr = Frame(pd.read_parquet(POOL), 9.0, "defl_med", "STRA9624", "PSU9624")
    plain = estimate_rows(fr, "ofd_stl", "plain")
    published = pd.read_csv(RATIOS)
    verify_published(plain, published)
    verify_published(estimate_rows(fr, "other_public", "winsor_p995"), published)
    return plain + estimate_rows(fr, "ofd_stl", "winsor_p995")


if __name__ == "__main__":
    import json

    print(json.dumps(build_ratios(), indent=2, allow_nan=False))
