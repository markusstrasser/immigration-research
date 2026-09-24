"""Positive controls for the crime-ratio direction lane.

    OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with numpy --with scikit-learn --with pytest \
        python3 -m pytest infra/immigration-fiscal/crime_ratio_direction_2026_09_24/ -q

1. The NIBRS lane's murder ratios (Hispanic ÷ NH white 2.30 central, 1.53 and 3.93 bounds) and
   robbery ratios (4.22, 2.36, 9.75) are reproduced from its staged cells before any new method.
2. The restaged victimisation rows conserve the lane's staged cells exactly.
3. The SHR design of the victim-cost lane (2024 P(offender Hispanic | victim group) x WONDER) gives
   its 2.7379 ratio.
4. The victim-cost lane's central ($28.92bn full, $4.50bn tangible) is reproduced through its own code.
5. The White-subtraction construction recovers a known overstatement on synthetic counts.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import nibrs_base as nb  # noqa: E402


def test_nibrs_lane_murder_and_robbery_ratios():
    r = nb.reproduce(("central", "alloc=b", "alloc=c"))
    got = {(x.spec, x.offence): x.RR_H_NHW for x in r.itertuples()}
    for key, published in nb.PUBLISHED.items():
        assert round(got[key], 2) == published, (key, got[key])
    pub = nb.published_rows().merge(r, on=["spec", "offence"], suffixes=("_pub", ""))
    assert (pub.RR_H_NHW - pub.RR_H_NHW_pub).abs().max() < 1e-6


def test_restage_conserves_staged_cells():
    import nibrs_impute as ni
    stages, _ = nb.load()
    ni.check_restage(ni.load_rows(), stages)          # raises SystemExit on any difference


def test_shr_victim_lane_ratio():
    import shr_impute as si
    df = si.load()
    won = pd.read_csv(si.VL / "derived/wonder_2024_homicide_victims.csv").set_index("group").deaths_not_stated_allocated
    won = won.reindex(si.G)
    pop = pd.read_csv(si.NCVS / "derived/cv_population_12plus.csv")
    pop = pop[pop.year.eq(2024)].set_index("group").population
    d = df[df.Year.eq(2024) & df.vic_eth.isin(si.G)]
    known = d[d.off_eth.isin(si.G)]
    pv = known.groupby("vic_eth").off_eth.value_counts(normalize=True).unstack(fill_value=0).reindex(index=si.G, columns=si.G)
    off = {o: float(sum(won[g] * pv.loc[g, o] for g in si.G)) for o in si.G}
    rr = (off["hispanic"] / pop["Hispanic"]) / (off["nh_white"] / pop["White"])
    assert abs(rr - 2.7379) < 5e-4


def test_victim_lane_central():
    import victim_cost_rerun as vcr
    vc = vcr.load_victim_lane()
    r = vcr.run(vc, vcr.setup(vc))
    assert abs(r["full"] / 1e9 - 28.9229) < 1e-3 and abs(r["tangible"] / 1e9 - 4.5014) < 1e-3


def test_white_subtraction_synthetic():
    import arm5_white_subtraction as a5
    c = pd.Series({"HW": 90.0, "HB": 10.0, "HO": 0.0, "HU": 0.0, "NHW": 100.0, "NHB": 0.0, "NHO": 0.0, "NHU": 0.0,
                   "UW": 0.0, "UB": 0.0, "UO": 0.0, "UU": 0.0})
    r = a5.construct(c)
    # White 190 - Hispanic 100 = 90 constructed NH white against 100 true: ratio overstated by 1/9
    assert r["nhw_route_b"] == pytest.approx(90.0) and r["over_route_b"] == pytest.approx(1 / 9)
