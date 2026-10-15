"""One keyed lineage precedence rule shared by the producer and survivor adapter."""
import importlib.util
import json
from pathlib import Path

import numpy as np
import pandas as pd

FISCAL = Path(__file__).resolve().parent.parent
CASE = FISCAL / 'main_case_2026_10_15/derived/corrections.json'
SOURCE = FISCAL / 'mixed_unit_removal_2026_10_14/membership.py'


def lineage_membership_masks(d, civ, *, completion=None):
    """Return original union, completed reporters, latent/broad children and full lineage.

    Completion uses actual keyed case records, never a race or name proxy. Broad
    biological children are computed after completion, so completed parents count.
    Latent children are already priced in the case; outside children are its new
    block. All masks refer to observed records, not modeled added adults.
    """
    native = d.PRCITSHP.isin([1, 2, 3]).to_numpy()
    us = [57, 60, 66, 69, 73, 78]
    original = civ & ((d.PRCITSHP.isin([4, 5]) & d.PENATVTY.eq(303)).to_numpy()
        | (native & (d.PEFNTVTY.eq(303) | d.PEMNTVTY.eq(303)).to_numpy())
        | (native & d.PEFNTVTY.isin(us).to_numpy() & d.PEMNTVTY.isin(us).to_numpy()
           & d.PRDTHSP.eq(1).to_numpy()))
    if completion is None:
        completion = json.loads(CASE.read_text())['meta']['union_completion']['observed_records']
    reporters = np.zeros(len(d), bool)
    ids = [(r['PH_SEQ'], r['PPPOS']) for r in completion if r['central_reporter']]
    if ids:
        lookup = pd.Series(np.arange(len(d)), index=pd.MultiIndex.from_frame(d[['PH_SEQ', 'PPPOS']]))
        found = lookup.reindex(pd.MultiIndex.from_tuples(ids)).to_numpy(float)
        if not np.isfinite(found).all():
            raise SystemExit('[BLOCKED] lineage completion record missing from keyed frame')
        reporters[found.astype(int)] = True
        if np.any(reporters & ~civ):
            raise SystemExit('[BLOCKED] lineage completion contains noncivilian record')
    union = original | reporters
    spec = importlib.util.spec_from_file_location('comparator_membership_rule_source', SOURCE)
    mem = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mem)
    biological, _, _ = mem.biological_children(d, union, civ)
    latent = mem.latent_mask(d, union, civ)
    outside = biological & ~latent
    return {'original': original, 'reporters': reporters, 'union': union,
            'latent': latent, 'outside': outside, 'biological': biological,
            'all': union | biological}
