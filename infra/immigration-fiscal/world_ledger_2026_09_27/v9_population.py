"""Source-owned minor calibration on the existing completed economic frame."""
import copy
import hashlib
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent


def calibrate_frame(original, payload, gate):
    from population_basis import completed_frame
    # Locate completion records using the historical source weights first.
    source = copy.deepcopy(payload)
    source["meta"].pop("population_v9")
    source["meta"]["coverage"]["counts_by_generation"] = dict(
        G1=0., G2=0., G3plus=source["meta"]["population_v8"]["coverage"])
    out = completed_frame(original, source, gate)
    from committed_inputs import checked_bytes
    relative = "infra/immigration-fiscal/count_composition_r5_2026_10_15/derived/native_person_factors.parquet"
    checked_bytes("WORKTREE_SHA256_OCT16", relative)
    file = HERE.parents[2] / relative
    factors = pd.read_parquet(file, columns=["PH_SEQ", "PPPOS", "central_member_factor"]).set_index(["PH_SEQ", "PPPOS"])
    joined = factors.reindex(pd.MultiIndex.from_frame(out[["PH_SEQ", "PPPOS"]])).central_member_factor
    gate("v9_factor_identity_join", bool(joined.notna().all()))
    mult = joined.to_numpy(float)
    gate("v9_minor_only", bool(np.all(mult[out.A_AGE.to_numpy() >= 18] == 1)))
    # The uniform G3+ proxy's latent mass is not an observed minor. Calibrate
    # actual reporting/completion records, holding synthetic descendants fixed.
    identified = out.pw_row4.to_numpy(float).copy()
    completed = out.completion_member.to_numpy(bool)
    identified[completed] = out.pwwgt0.to_numpy(float)[completed]
    latent = out.pw.to_numpy(float) - identified
    out["pw"] = identified * mult + latent
    counts = payload["meta"]["population_v9"]
    gate("v9_located_population", abs(float(out.pw[out.target].sum()) - counts["without_coverage"]) < 1e-3,
         actual=float(out.pw[out.target].sum()), expected=counts["without_coverage"])
    usb = out.PRCITSHP.isin([1, 2, 3]).to_numpy()
    parent = (out.PEFNTVTY.eq(303) | out.PEMNTVTY.eq(303)).to_numpy()
    target = out.target.to_numpy()
    masks = {"G1": target & ~usb, "G2": target & usb & parent, "G3+": target & usb & ~parent}
    coverage = payload["meta"]["coverage_tenure"]["coverage_counts_by_generation"]
    located = {g: float(out.pw[m].sum()) for g, m in masks.items()}
    missing = {g: coverage[g.replace("G3+", "G3plus")] for g in masks}
    full = {g: located[g] + missing[g] for g in masks}
    gate("v9_complete_population", abs(sum(full.values()) - counts["with_coverage"]) < 1e-3)
    out.attrs["population_oct15"].update(located_persons=located, unlocated_coverage_persons=missing,
        complete_denominator_persons=full, located_total=sum(located.values()), complete_total=counts["with_coverage"],
        case_located_total=counts["without_coverage"], calibration="source native_minor_calibration factor_source; fixed roster",
        calibration_applied_once=True)
    return out
