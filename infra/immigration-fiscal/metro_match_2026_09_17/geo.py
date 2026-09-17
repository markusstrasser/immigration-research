"""Metro-group geography for the metro-matching lane.

CPS ASEC 2025 carries the CBSA code on the HOUSEHOLD record (hhpub25.csv:
GTCBSA, GTMETSTA), not on the person extract the upstream build keeps, so the
two columns are merged onto `d` by PH_SEQ exactly as extend_ledger.build merges
GESTFIPS. Nothing outside this lane is written.
"""
from pathlib import Path
import sys
import zipfile

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
STRESS = HERE.parent / "ledger_stress_2026_09_17"
sys.path.insert(0, str(STRESS))
import common  # noqa: E402

CA, TX = 6, 48
SW_IL = (4, 8, 17, 32, 35)

# (name, cbsa or None, state filter or None, metro flag) applied in order.
# metro flag: True = identified metro (GTCBSA > 0), False = GTCBSA == 0, None = any.
RULES = [
    ("los_angeles", 31080, None, None),
    ("riverside", 40140, None, None),
    ("san_diego", 41740, None, None),
    ("san_francisco", 41860, None, None),
    ("san_jose", 41940, None, None),
    ("ca_other_metro", None, (CA,), True),
    ("ca_nonmetro", None, (CA,), False),
    ("houston", 26420, None, None),
    ("dallas", 19100, None, None),
    ("san_antonio", 41700, None, None),
    ("austin", 12420, None, None),
    ("mcallen", 32580, None, None),
    ("el_paso", 21340, None, None),
    ("tx_other_metro", None, (TX,), True),
    ("tx_nonmetro", None, (TX,), False),
    ("chicago", 16980, None, None),
    ("phoenix", 38060, None, None),
    ("denver", 19740, None, None),
    ("las_vegas", 29820, None, None),
    ("swil_other_metro", None, SW_IL, True),
    ("swil_nonmetro", None, SW_IL, False),
    ("rest_metro", None, None, True),
    ("rest_nonmetro", None, None, False),
]
NAMES = [r[0] for r in RULES]

# Merge target when a group has a nonpositive cell in any replicate.
PARENT = {
    "los_angeles": "ca_other_metro", "riverside": "ca_other_metro",
    "san_diego": "ca_other_metro", "san_francisco": "ca_other_metro",
    "san_jose": "ca_other_metro", "ca_nonmetro": "ca_other_metro",
    "houston": "tx_other_metro", "dallas": "tx_other_metro",
    "san_antonio": "tx_other_metro", "austin": "tx_other_metro",
    "mcallen": "tx_other_metro", "el_paso": "tx_other_metro",
    "tx_nonmetro": "tx_other_metro",
    "chicago": "swil_other_metro", "phoenix": "swil_other_metro",
    "denver": "swil_other_metro", "las_vegas": "swil_other_metro",
    "swil_nonmetro": "swil_other_metro",
    "rest_nonmetro": "rest_metro",
    # Last-resort collapse of a whole state group onto itself is a no-op; these
    # roots have no parent and a failure there is reported, not merged away.
    "ca_other_metro": None, "tx_other_metro": None,
    "swil_other_metro": None, "rest_metro": None,
}


def attach(d):
    """Return (GTCBSA, GTMETSTA) aligned to d's rows."""
    with zipfile.ZipFile(common.CPS_ZIP) as z:
        hh = pd.read_csv(z.open("hhpub25.csv"),
                         usecols=["H_SEQ", "GTCBSA", "GTMETSTA", "GESTFIPS"])
    merged = d[["PH_SEQ"]].merge(hh, left_on="PH_SEQ", right_on="H_SEQ",
                                 how="left", validate="many_to_one")
    if merged.H_SEQ.isna().any():
        raise ValueError("Person record without a household record")
    if not np.array_equal(merged.GESTFIPS.to_numpy(), d.GESTFIPS.to_numpy()):
        raise ValueError("Household merge disagrees with the build's GESTFIPS")
    return merged.GTCBSA.to_numpy(dtype=int), merged.GTMETSTA.to_numpy(dtype=int)


def raw_codes(d):
    """0..22 metro-group code per record, first matching rule wins."""
    cbsa, _ = attach(d)
    fips = d.GESTFIPS.to_numpy()
    out = np.full(len(d), -1, dtype=int)
    for k, (_, code, states, metro) in enumerate(RULES):
        sel = out < 0
        if code is not None:
            sel &= cbsa == code
        if states is not None:
            sel &= np.isin(fips, states)
        if metro is True:
            sel &= cbsa > 0
        elif metro is False:
            sel &= cbsa == 0
        out[sel] = k
    if (out < 0).any():
        raise ValueError("Unassigned record")
    return out, cbsa


def state_group_of(name):
    for prefix, group in [("ca_", "CA"), ("tx_", "TX"), ("swil_", "SW_IL"), ("rest_", "rest")]:
        if name.startswith(prefix):
            return group
    return {"los_angeles": "CA", "riverside": "CA", "san_diego": "CA",
            "san_francisco": "CA", "san_jose": "CA", "houston": "TX", "dallas": "TX",
            "san_antonio": "TX", "austin": "TX", "mcallen": "TX", "el_paso": "TX",
            "chicago": "SW_IL", "phoenix": "SW_IL", "denver": "SW_IL",
            "las_vegas": "SW_IL"}[name]


def bands4(d):
    return np.digitize(d.A_AGE, [18, 45, 65])


def floors(groups, weights, cellcodes, count):
    """Minimum population over cells x all 161 weight vectors, per group."""
    out = {}
    for name, mask in groups.items():
        mask = np.asarray(mask)
        worst = np.inf
        for c in range(count):
            sel = mask & (cellcodes == c)
            n = weights[sel].sum(axis=0) if sel.any() else np.zeros(weights.shape[1])
            worst = min(worst, float(n.min()))
        out[name] = worst
    return out


RECORD_FLOOR = 5


def resolve_groups(raw, bands, groups, weights, key_groups, n_bands=4,
                   record_floor=RECORD_FLOOR):
    """Merge metro groups upward until every key group x cell is positive in all
    161 weight vectors AND carries at least `record_floor` sample records.
    Returns (labels, codes, merge_log)."""
    label = {k: NAMES[k] for k in range(len(NAMES))}
    merges = []
    for _ in range(len(NAMES) + 1):
        alive = sorted(set(label.values()), key=NAMES.index)
        idx = {name: i for i, name in enumerate(alive)}
        codes = np.array([idx[label[k]] for k in range(len(NAMES))])[raw]
        joint = codes * n_bands + bands
        bad = set()
        for g in key_groups:
            mask = np.asarray(groups[g])
            for a, name in enumerate(alive):
                for b in range(n_bands):
                    sel = mask & (joint == a * n_bands + b)
                    n = weights[sel].sum(axis=0) if sel.any() else np.zeros(weights.shape[1])
                    if float(n.min()) <= 0 or int(sel.sum()) < record_floor:
                        bad.add((name, g, b, int(sel.sum()), float(n.min())))
        if not bad:
            return alive, codes, merges
        progressed = False
        why = {}
        for name, g, b, rec, mn in bad:
            why.setdefault(name, []).append(f"{g} band{b}: {rec} records, min-161 population {mn:.0f}")
        for name in sorted(why, key=NAMES.index):
            parent = PARENT.get(name)
            if parent is None:
                continue
            target = parent
            while label[NAMES.index(target)] != target:
                target = label[NAMES.index(target)]
            for k, v in list(label.items()):
                if v == name:
                    label[k] = target
            merges.append(dict(merged=name, into=target, triggers=sorted(why[name]),
                               reason=("cell fails positivity in all 161 weight vectors "
                                       f"or the {record_floor}-record floor")))
            progressed = True
        if not progressed:
            raise ValueError(f"Cannot merge further; still sparse: {sorted(why)}")
    raise ValueError("Merge did not converge")
