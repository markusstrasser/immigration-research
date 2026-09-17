"""Reporting helpers shared by the two survey arms.

The estimators themselves (age bands, replicate cell totals, successive
difference variance, common-age and age-matched gaps) are imported from the
ACS earnings-replication lane's `common.py` so that the tax gaps and the
earnings gaps are computed by exactly the same code.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

import common as C

REFERENCE = "native_nh_white"


def cells_and_gaps(masks: dict[str, np.ndarray], band: np.ndarray,
                   weights: np.ndarray, values: dict[str, np.ndarray],
                   domain: str, denom: int, survey: str):
    cells = {k: C.cell_totals(m, band, weights, values) for k, m in masks.items()}
    n0 = cells[REFERENCE]["n"][:, 0]
    shares = n0 / n0.sum()
    rows, gaps = [], []
    for name, cell in cells.items():
        for b in range(C.NBANDS):
            row = dict(survey=survey, domain=domain, group=name, band=C.BAND_LABELS[b])
            pop, pop_se = C.sdr(cell["n"][b], denom)
            row.update(population=pop, population_se=pop_se)
            for key in values:
                e, s = C.sdr(C.safe_div(cell[key], cell["n"])[b], denom)
                row[f"mean_{key}"] = e
                row[f"mean_{key}_se"] = s
            rows.append(row)
        row = dict(survey=survey, domain=domain, group=name, band="all")
        pop, pop_se = C.sdr(cell["n"].sum(axis=0), denom)
        row.update(population=pop, population_se=pop_se)
        for key in values:
            e, s = C.sdr(C.crude_mean(cell, key), denom)
            row[f"mean_{key}"] = e
            row[f"mean_{key}_se"] = s
        rows.append(row)
    for name, cell in cells.items():
        if name == REFERENCE:
            continue
        for key in values:
            v = C.common_age_gap(cell, cells[REFERENCE], key, shares)
            e, s = C.sdr(v, denom)
            a = C.age_matched_total_gap(cell, cells[REFERENCE], key)
            ae, ase = C.sdr(a, denom)
            gaps.append(dict(survey=survey, domain=domain, group=name,
                             reference=REFERENCE, variable=key,
                             common_age_gap_per_person=e, common_age_gap_se=s,
                             common_age_ci_low=e - 1.96 * s,
                             common_age_ci_high=e + 1.96 * s,
                             age_matched_gap_bn=ae / 1e9,
                             age_matched_gap_bn_se=ase / 1e9))
    return rows, gaps


def anchor_table(person: dict[str, np.ndarray], masks: dict[str, np.ndarray],
                 domain_mask: np.ndarray, full_weight: np.ndarray,
                 union: list[str]) -> pd.DataFrame:
    """Full-weight group totals of every person-level series, plus ratios."""
    def one(name, sel):
        tot = {k: float((v[sel] * full_weight[sel]).sum()) for k, v in person.items()}
        rec = dict(group=name, population=float(full_weight[sel].sum()))
        rec.update({f"{k}_bn": v / 1e9 for k, v in tot.items()})
        cen = tot.get("FEDTAX_AC", 0.0)
        fic = tot.get("FICA", 0.0)
        rec["ratio_iitax"] = tot["iitax_full"] / cen if cen else np.nan
        rec["ratio_iitax_salt"] = tot.get("iitax_full_salt", np.nan) / cen if cen else np.nan
        rec["ratio_iitax_alloc_ref"] = (tot["iitax_full"] / tot["FEDTAX_AC_alloc"]
                                        if tot.get("FEDTAX_AC_alloc") else np.nan)
        rec["ratio_payroll"] = tot["payroll_full"] / fic if fic else np.nan
        return rec

    rows = [one(name, m & domain_mask) for name, m in masks.items()]
    u = np.zeros(len(domain_mask), dtype=bool)
    for name in union:
        u |= masks[name]
    rows.append(one("union_of_targets", u & domain_mask))
    return pd.DataFrame(rows)
