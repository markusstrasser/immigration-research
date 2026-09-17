"""Shared setup for the ledger stress lane.

Rebuilds exactly the objects analyze.generate() builds (analyze.py lines ~183-210
in the dispatch numbering; lines 82-105 in the file) without running generate().
Nothing outside this lane directory is modified.
"""
from pathlib import Path
import argparse
import sys

import numpy as np

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
ROOT = HERE.parents[2]
SOURCE_LANE = FISCAL / "all_age_ledger_2026_09_17"
sys.path.insert(0, str(SOURCE_LANE))

import analyze  # noqa: E402
from analyze import ext, donor_model, read_meps  # noqa: E402
from estimator import account, contrast, standardized_gap, sufficient, sum_cells, summarize  # noqa: E402

TARGETS = analyze.TARGETS
REFERENCES = analyze.REFERENCES
COEFFICIENTS = analyze.COEFFICIENTS
COMPONENTS = analyze.COMPONENTS

CPS_ZIP = FISCAL / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip"
MEDICAL_ZIP = ROOT / "sources/immigration-fiscal/data/external/stage3/ahrq/meps_2024/h256dat.zip"
MEDICAL_SAS = MEDICAL_ZIP.with_name("h256su.txt")

# State groups for the within-state standard.
CA, TX = 6, 48
SW_IL = (4, 8, 17, 32, 35)
STATE_GROUP_NAMES = ["CA", "TX", "SW_IL", "rest"]


def setup():
    """Return every object the two stress tests need, built exactly as upstream."""
    state = ext.build(argparse.Namespace(cps_zip=CPS_ZIP))
    d = state["d"]
    weights = state["person_weights"]
    heads = d.loc[d.SPM_HEAD.eq(1)].sort_values("SPM_ID")
    head_weights = heads[ext.base.REPS].to_numpy()[state["index"]]
    civilian = (d.PRPERTYP.eq(2) | d.A_AGE.lt(15)).to_numpy()
    groups = {name: state["group"][name] & civilian for name in TARGETS[:3] + REFERENCES[:2]}
    member_count = sum(groups[name].astype(int) for name in TARGETS[:3])
    if member_count.max() > 1:
        raise ValueError("Target categories overlap")
    us = [57, 60, 66, 69, 73, 78]
    parents_us = d.PEFNTVTY.isin(us) & d.PEMNTVTY.isin(us)
    groups["native_two_us_parents"] = groups["all_native"] & parents_us.to_numpy()
    groups["other_natives"] = groups["all_native"] & (member_count == 0)
    bands = np.digitize(d.A_AGE, [18, 25, 35, 45, 55, 65, 75])
    shared, personal, renter = analyze.matrices(state)
    medical, anchors = read_meps(MEDICAL_ZIP, MEDICAL_SAS)
    exposure = ~(d.PUB.eq(0) & d.PRIV.eq(0)).to_numpy()
    if (d.loc[~exposure, "A_AGE"] > 0).any():
        raise ValueError("Post-reference-year exclusion contains noninfant")
    if (d.PENATVTY <= 0).any():
        raise ValueError("Unknown birthplace cannot select a medical donor")
    cells, codes, covariance = donor_model(medical, d, False)
    means = cells.mean_public_paid.to_numpy()
    health = np.eye(len(cells))[codes] * exposure[:, None]
    return dict(state=state, d=d, weights=weights, head_weights=head_weights,
                civilian=civilian, groups=groups, member_count=member_count,
                bands=bands, shared=shared, personal=personal, renter=renter,
                health=health, means=means, covariance=covariance,
                medical_anchors=anchors, exposure=exposure)


def state_codes(d):
    """0=CA, 1=TX, 2=SW_IL, 3=rest."""
    fips = d.GESTFIPS.to_numpy()
    out = np.full(len(fips), 3, dtype=int)
    out[np.isin(fips, SW_IL)] = 2
    out[fips == TX] = 1
    out[fips == CA] = 0
    return out


def audit_inputs():
    paths = [CPS_ZIP, MEDICAL_ZIP, MEDICAL_SAS, ext.HERE / "state_parameters.csv",
             Path(ext.__file__), Path(ext.base.__file__), SOURCE_LANE / "analyze.py",
             SOURCE_LANE / "estimator.py", SOURCE_LANE / "derived/estimates.csv",
             HERE / "common.py"]
    return [dict(path=str(p), sha256=ext.base.sha(p)) for p in paths]
