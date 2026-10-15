"""PES tenure transfer on the adopted coverage construction.

Native-First: import the existing coverage factors; parse the pinned primary PDF.
No independent benefit take-up or legal-status assumption enters this module.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

import numpy as np

sys.dont_write_bytecode = True
LANE = Path(__file__).resolve().parent
FISCAL = LANE.parent
sys.path.insert(0, str(FISCAL / "coverage_bound_2026_10_14"))
import coverage_bound as C
from source_tables import LABELS, load, parse_row


def require(ok, why):
    if not ok:
        raise ValueError("[BLOCKED] count composition: " + why)


def tenure_rates():
    folder = FISCAL / "coverage_bound_2026_10_14/inputs"
    source = folder / "pes_cross.pdf"
    pin = json.loads((folder / "pins.json").read_text())[source.name]["sha256"]
    require(hashlib.sha256(source.read_bytes()).hexdigest() == pin, "PES source hash")
    text = subprocess.run(["pdftotext", "-layout", str(source), "-"],
                          text=True, capture_output=True, check=True).stdout
    # Last occurrence is the full Hispanic tenure-by-age block in Table D.
    lines = text.splitlines()
    start = [i for i, line in enumerate(lines) if line.strip().startswith("Hispanic or Latino")][-1]
    out = {"all": parse_row(lines[start], "Hispanic or Latino")}
    for offset, tenure in ((1, "Owner"), (11, "Renter")):
        out[tenure.lower()] = {"all": parse_row(lines[start + offset], tenure)}
        for j, label in enumerate(LABELS, 1):
            out[tenure.lower()][label] = parse_row(lines[start + offset + j], label)
    require([out[k]["all"]["nce_pct"] for k in ("owner", "renter")] == [-2.18, -7.83]
            and out["all"]["nce_pct"] == -4.99, "PES tenure marginal controls")
    return out


def split_factors(data, rates, base):
    """Separate DA-under-five from the PES part of each current-age record."""
    total, _ = C.factors(data, rates, base)
    da = np.zeros_like(total)
    age, sex = data["age"], data["sex"]
    for shift, fraction in ((5, 1-C.BIRTH_OLDER_SHARE), (4, C.BIRTH_OLDER_SHARE)):
        old = age-shift
        for i in np.flatnonzero((old >= 0) & (old <= 4) & data["hispanic"]):
            arrival = data["arrival"][i]
            pre = (1.0 if arrival <= 26 else 1/8 if arrival == 27 else 0.0) if data["generation"][i] == 0 else 1.0
            da[i] += fraction*pre*C.rate_at(int(old[i]), int(sex[i]), rates, base)
    return total, da, total-da


def fixed_count_tenure(data, tenure, weights, rates, base, marginal=None):
    """Tilt PES-covered records by Table D marginal net-omission odds.

    Normalize inside exact current-age x sex x generation cells. This is a
    conditional transfer of the marginal tenure contrast, not multiplication
    of allegedly independent demographic and tenure marginal PES estimates.
    Signed cell totals and all DA-under-five contributions remain unchanged.
    """
    marginal = tenure_rates() if marginal is None else marginal
    total, da, pes = split_factors(data, rates, base)
    odds = {t: 1/(1+marginal[t]["all"]["nce_pct"]/100)-1 for t in ("owner", "renter")}
    require(set(np.unique(tenure)) <= {1, 2, 3}, "unmapped CPS tenure")
    tilt = np.where(tenure == 1, odds["owner"], odds["renter"])
    result = da.copy()
    cells = np.column_stack((data["age"], data["sex"], data["generation"]))
    diagnostics = []
    for age, sex, generation in np.unique(cells, axis=0):
        m = (cells == (age, sex, generation)).all(axis=1)
        target = float(weights[m] @ pes[m])
        denom = float(weights[m] @ (pes[m]*tilt[m]))
        require(abs(denom) > 1e-15 or abs(target) < 1e-12, "zero tenure support in nonzero PES cell")
        scale = target/denom if denom else 0.0
        require(scale >= 0, "tenure tilt reverses signed PES cell")
        result[m] += pes[m]*tilt[m]*scale
        before = float(weights[m] @ total[m])
        after = float(weights[m] @ result[m])
        require(abs(after-before) < 1e-7, "fixed age-sex-generation count closure")
        diagnostics.append(dict(age=int(age), sex=int(sex), generation=int(generation),
                                before_people=before, after_people=after,
                                owner_before=float(weights[m & (tenure == 1)] @ total[m & (tenure == 1)]),
                                owner_after=float(weights[m & (tenure == 1)] @ result[m & (tenure == 1)])))
    return result, diagnostics


def transfer_count_tenure(data, tenure, rates, base, cross=None):
    """Sensitivity: replace PES age-sex rate by its actual Table D tenure cell.

    Retains V2024 base absorption, birth/arrival mixture and DA under age five.
    Unlike the fixed-count arm, this signed net-coverage transfer changes counts.
    """
    cross = tenure_rates() if cross is None else cross
    _, da, _ = split_factors(data, rates, base)
    result = da.copy()
    for i, age in enumerate(data["age"]):
        if not data["hispanic"][i]:
            continue
        arrival = data["arrival"][i]
        pre = (1.0 if arrival <= 26 else 1/8 if arrival == 27 else 0.0) if data["generation"][i] == 0 else 1.0
        kind = "owner" if tenure[i] == 1 else "renter"
        for shift, fraction in ((5, 1-C.BIRTH_OLDER_SHARE), (4, C.BIRTH_OLDER_SHARE)):
            old = int(age-shift)
            if old <= 4:
                continue
            label, band = C.pes_label(old, int(data["sex"][i]))
            q = base[(*band, int(data["sex"][i]))]["base_over_census"]
            result[i] += fraction*pre*(1/((1+cross[kind][label]["nce_pct"]/100)*q)-1)
    return result
