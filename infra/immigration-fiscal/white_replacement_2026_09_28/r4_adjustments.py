"""Round-4 own-record comparator additions, returned without mutating any cost.

Apply only to comparator scenarios (or differences between outside-lineage
blocks). The existing lineage bridge already carries its school pricing and row
8, including the added descendants' inherited share: adding this to the lineage
would double count them.

Audit row 8's original 2bn is declared at main_case_2026_09_24/package.cjs:333.
The identified union dump applies the current response's row-8 edit but none of
the descendants' own cells (engine_lines.cjs:98-108). Therefore its per-head
benchmark is 2 * current meta.responses.row8_factor / R.TARGET, not September
29's earlier factor and not a denominator including the added descendants.
"""
from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

import district_prices_oct15 as D

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
BLACK_CODES = {2, 6, 10, 11, 12, 16, 17, 18, 22, 23}


@lru_cache(maxsize=1)
def source_inputs():
    """Small, immutable source declarations and the built same-vintage table."""
    package = (FISCAL / "main_case_2026_09_24/package.cjs").read_text()
    rows = re.findall(r'row8:\s*\{[^}]*\bc:\s*([\d.]+)', package)
    D.require(len(rows) == 1 and float(rows[0]) == 2.0, "audit row 8's source constant changed")
    state = pd.read_csv(FISCAL / "gen_ledger_extension_2026_09_16/state_parameters.csv")
    prices = dict(zip(state.fips.astype(int), state.per_pupil_current_spending))
    school = json.loads((FISCAL / "school_cost_where_enrolled_2026_09_24/derived/within_district.json").read_text())
    factor = float(school["TCURELSCS"]["factor_all_districts"])
    return D.load(), prices, float(rows[0]), factor


# Modules and DataFrames are unhashable; cache only their immutable per-record
# construction by identity, holding references to prevent object-id recycling.
_FRAME_CACHE = {}


def frame_vectors(R, W, extra):
    """Reuse own-race, state, and probability arrays across scenario/replicate calls."""
    key = (id(R), id(W), id(extra), id(R.K["k12"]))
    if key in _FRAME_CACHE:
        return _FRAME_CACHE[key][3]
    stored, prices, constant, level_factor = source_inputs()
    state = np.asarray(W.STATE, dtype=int)
    n = len(state)
    D.require(len(extra) == n and len(R.K["k12"]) == n, "scenario rows do not align")
    hispanic = extra.PEHSPNON.eq(1).to_numpy()
    race = extra.PRDTRACE.to_numpy()
    # Use a child's own race, exactly as members_coverage_oct15.race_group.
    # NH Black-in-combination children take the NH Black-alone district proxy;
    # that race-universe approximation is explicit beside the measured prices.
    group = np.where(hispanic, "hispanic", np.where(race == 1, "nh_white",
                     np.where(np.isin(race, list(BLACK_CODES)), "black", "nh_other")))
    D.require(set(state) <= set(prices), "missing school price for a scenario state")
    cost = np.array([prices[int(s)] for s in state], float)
    D.require(np.isfinite(cost).all() and (cost > 0).all(), "invalid school state prices")
    probability = np.asarray(R.K["k12"], float) / cost
    D.require(np.isfinite(probability).all() and ((probability >= 0) & (probability <= 1)).all(),
              "K-12 exposure must be own October probability times state price")
    rate = D.per_pupil_rates(state, group, stored)
    vectors = dict(probability=probability, district_dollars=probability * rate,
                   # This is a size proxy if the lineage's school-level factor
                   # applied to this comparator, never an additional charge.
                   level_proxy_dollars=probability * (cost + rate) * (level_factor - 1),
                   other_pupils=probability * (group == "nh_other"),
                   black_multiracial_pupils=probability * (~hispanic & np.isin(race, list(BLACK_CODES - {2}))),
                   row8_constant_bn=constant)
    _FRAME_CACHE[key] = (R, W, extra, vectors, R.K["k12"])
    return vectors


def scenario_adjustments(R, W, extra, sc):
    """Return additive amounts on sc['cps_w']; leave the caller's cost unchanged.

    Raw observed and reweighted nonnegative weights both work. Row 8 uses the
    weights' actual total, gated to sc.population. The caller must form signed
    differences between blocks after calling this on each nonnegative block.
    """
    v = frame_vectors(R, W, extra)
    cw = np.asarray(sc["cps_w"], float)
    D.require(cw.shape == v["probability"].shape and np.isfinite(cw).all() and (cw >= 0).all(),
              "invalid scenario person weights")
    population = float(cw.sum())
    D.require(abs(population - float(sc["population"])) <= max(1e-5, population * 1e-12),
              "scenario population differs from its weighted persons")
    D.require(float(R.TARGET) > 0, "row 8 needs the identified union's positive count")
    factor = float(W.META["responses"]["row8_factor"])
    D.require(np.isfinite(factor) and factor > 0, "invalid current row-8 response factor")
    scale = school_price_scale(R, W)
    raw_district = float(cw @ v["district_dollars"] / 1e9)
    return dict(district_bn=raw_district * scale,
                district_raw_bn=raw_district, district_price_scale=scale,
                row8_bn=v["row8_constant_bn"] * factor * population / float(R.TARGET),
                pupil_count=float(cw @ v["probability"]),
                school_level_unmeasured_bn=float(cw @ v["level_proxy_dollars"] / 1e9) * scale,
                nh_other_unmeasured_pupils=float(cw @ v["other_pupils"]),
                black_multiracial_proxy_pupils=float(cw @ v["black_multiracial_pupils"]))


def school_price_scale(R, W):
    """Map literal F-33 district dollars onto the evaluator's charged BEA school pool.

    run29's school amount is national education_services * R.K12_PART times
    the scenario's share of full-frame school exposure. Its national denominator
    stays fixed when adding a group's own district differential. Read the actual
    principal national from the case dump; no source-summary fallback is allowed.
    """
    principals = []
    for basis in ("cash", "accrual"):
        for end in ("low", "high"):
            lines = [line for line in W.DUMP[basis][end]["lines"]
                     if line["side"] == "spending" and line["id"] == "education_services"]
            D.require(len(lines) == 1, f"principal education line is not unique: {basis}/{end}")
            principals.append(float(lines[0]["national_bn"]))
    national = principals[0]
    D.require(np.isfinite(principals).all() and national > 0 and
              all(abs(value - national) <= 1e-10 for value in principals),
              "education national differs across the principal sets/ends")
    fraction = float(R.K12_PART)
    D.require(np.isfinite(fraction) and 0 < fraction <= 1, "invalid evaluator K-12 fraction")
    w, exposure = np.asarray(R.w, float), np.asarray(R.K["k12"], float)
    D.require(w.shape == exposure.shape and np.isfinite(w).all() and (w >= 0).all(),
              "invalid national school exposure weights")
    denominator = float(w @ exposure) / 1e9
    D.require(np.isfinite(denominator) and denominator > 0, "empty national school dollar exposure")
    return national * fraction / denominator
