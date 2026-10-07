"""Shared setup for the ledger stress lane.

Rebuilds exactly the objects analyze.generate() builds (analyze.py lines ~183-210
in the dispatch numbering; lines 82-105 in the file) without running generate().
Nothing outside this lane directory is modified.

Since 2026-10-08 `income_tax_columns` also gives the white-reference ledger's item T
(`ledger_absolute_2026_09_17`): the income tax the survey misses, moved onto the main
case's income-tax keys, from that lane's own functions. Appended to the partial matrix
at coefficient 1 (`T_COEFFICIENTS`) it makes the `partial_plus_T` account.
"""
from pathlib import Path
import argparse
import sys

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
ROOT = HERE.parents[2]
SOURCE_LANE = FISCAL / "all_age_ledger_2026_09_17"
ABSOLUTE = FISCAL / "ledger_absolute_2026_09_17"
sys.path.insert(0, str(SOURCE_LANE))

import analyze  # noqa: E402
from analyze import ext, donor_model, read_meps  # noqa: E402
from estimator import account, contrast, standardized_gap, sufficient, sum_cells, summarize  # noqa: E402

sys.path.insert(0, str(ABSOLUTE))
import absolute_ledger as AL  # noqa: E402

TARGETS = analyze.TARGETS
REFERENCES = analyze.REFERENCES
COEFFICIENTS = analyze.COEFFICIENTS
COMPONENTS = analyze.COMPONENTS
T_ACCOUNT = "partial_plus_T"
T_COEFFICIENTS = np.append(COEFFICIENTS, 1.0)

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


def income_tax_columns(env):
    """Item T per record at both allocations, by matrix name, and the files to fingerprint.

    absolute_ledger.income_tax_keys joins the case's keys onto these records and refuses
    a different civilian universe or weights; income_tax_item gives the federal and state
    parts, with each SPM unit's dollars split equally over its members for "shared".
    """
    state, d, w, civilian = env["state"], env["d"], env["weights"][:, 0], env["civilian"]
    index, n_units = state["index"], state["n_units"]

    def unit_share(person_amounts):
        total = np.bincount(index, weights=np.asarray(person_amounts, dtype=float), minlength=n_units)
        return ext.allocate(total, index, np.ones(len(d), bool), n_units)

    keys = AL.income_tax_keys(d, civilian, w)
    columns = {}
    for name, personal in [("shared", False), ("personal", True)]:
        federal, state_part, _ = AL.income_tax_item(d, keys, civilian, w, personal, unit_share)
        columns[name] = federal + state_part
    inputs = [dict(path=str(p), sha256=ext.base.sha(p)) for p in [Path(AL.__file__), *keys["inputs"]]]
    return columns, inputs


def t_concentration(env, t_column, cells):
    """How much of each cell's item T its ten largest records and SPM units carry.

    cells maps a name to a record mask. Full weights; per person is over the cell's
    population. Returns one row per cell.
    """
    w, index = env["weights"][:, 0], env["state"]["index"]
    rows = []
    for name, mask in cells.items():
        m = np.asarray(mask)
        tw = t_column[m] * w[m]
        pop, total = float(w[m].sum()), float(tw.sum())
        top_records = float(np.sort(tw)[::-1][:10].sum())
        top_units = float(pd.Series(tw).groupby(index[m]).sum().nlargest(10).sum())
        rows.append(dict(cell=name, records=int(m.sum()), population=pop, t_total_bn=total / 1e9,
                         t_per_person=total / pop, top10_records_bn=top_records / 1e9,
                         top10_units_bn=top_units / 1e9, top10_units_share=top_units / total,
                         t_per_person_without_top10_units=(total - top_units) / pop))
    return pd.DataFrame(rows)


def t_gate(stats_base, stats_t, shares, means):
    """Item T on a one-geography, 8-band collapse at the shared allocation.

    For each target, T's move in the standardized gap against third-plus NH whites must
    equal the absolute lane's T row in its items_by_group.csv. Returns the residuals.
    """
    items = pd.read_csv(ABSOLUTE / "derived/items_by_group.csv").query("item == 'T' and arm == 'central'")
    residuals = {}
    for target in TARGETS:
        base, _ = standardized_gap(stats_base[target], stats_base[REFERENCES[0]], COEFFICIENTS, means, shares)
        with_t, _ = standardized_gap(stats_t[target], stats_t[REFERENCES[0]], T_COEFFICIENTS, means, shares)
        want = items[items.group.eq(target)].common_age_gap_per_person_vs_white
        if len(want) != 1:
            raise ValueError(f"Missing T anchor in the absolute lane: {target}")
        residuals[target] = float(abs(with_t[0] - base[0] - want.iloc[0]))
    if max(residuals.values()) > 1e-3:
        raise ValueError(f"Item T's column does not reproduce the absolute lane's T rows: {residuals}")
    return residuals


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
