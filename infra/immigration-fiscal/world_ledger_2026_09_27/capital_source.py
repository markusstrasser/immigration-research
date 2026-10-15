"""Shared item-6 numerical core; scratch module to port, with no I/O on import.

U.S.: job_capital.py shares(), parts_of(), record(); mining vectors zero.
Mexico: same callable, SAT corporate-gains ISR by SCIAN sector and ENIGH wage
shares. Inputs retain their currency; the caller applies the row's numeric PPP.
The group is an additional counterfactual workforce in Mexico, so its wages can
exceed the baseline industry's wages. Do not clamp that ratio to one.
"""
from __future__ import annotations

import math
from collections.abc import Mapping, Sequence


def source_taxes(
    wage_shares: Mapping[str, float],
    taxes_by_line: Mapping[str, Mapping[str, float]],
    responses: Mapping[str, Mapping[str, float]],
    excluded_industries: Sequence[str] = (),
    premise: str = "long_run_new_capital",
) -> dict:
    """Return sum_i wage_share_i * source_tax_i * response, both readings.

    Missing or nonfinite cells stop. Unknown premises stop. Zero row allowed
    explicitly for short-run or the beside output-mix/no-new-capital premise.
    This is the core for both countries; responses include corporate_labor.
    """
    if premise not in {"long_run_new_capital", "short_run_fixed_capital", "output_mix_no_new_capital"}:
        raise ValueError(f"[BLOCKED] unknown capital premise {premise}")
    if not taxes_by_line or set(responses) != set(taxes_by_line):
        raise ValueError("[BLOCKED] source-tax lines/responses mismatch")
    for industry, share in wage_shares.items():
        if not math.isfinite(share) or share < 0:
            raise ValueError(f"[BLOCKED] invalid wage share {industry}: {share}")
    excluded = set(excluded_industries)
    parts = {}
    totals = {reading: 0.0 for reading in ("low", "high")}
    for line, industry_taxes in taxes_by_line.items():
        if set(industry_taxes) != set(wage_shares):
            raise ValueError(f"[BLOCKED] missing or extra industry on {line}")
        if set(responses[line]) != set(totals):
            raise ValueError(f"[BLOCKED] missing reading on {line}")
        values = {}
        for industry, tax in industry_taxes.items():
            if not math.isfinite(tax) or tax < 0:
                raise ValueError(f"[BLOCKED] invalid source tax {line}/{industry}")
            values[industry] = wage_shares[industry] * tax if industry not in excluded else 0.0
        before = math.fsum(values.values())
        actual = {}
        for reading, response in responses[line].items():
            if not math.isfinite(response) or not 0 <= response <= 1:
                raise ValueError(f"[BLOCKED] invalid response {line}/{reading}")
            actual[reading] = before * response if premise == "long_run_new_capital" else 0.0
            totals[reading] += actual[reading]
        parts[line] = {"unresponded": before, "by_industry": values, "responded": actual}
    return {"premise": premise, "lines": parts, "total": totals}


def shares_from_wages(group: Mapping[str, float], national: Mapping[str, float]) -> dict:
    """Counterfactual group's wage bill over measured baseline industry wages.

    Caller must disclose baseline denominator; an augmented-denominator arm
    uses national+group and is a different premise, not a silent fallback.
    """
    if set(group) != set(national):
        raise ValueError("[BLOCKED] wage industry mismatch")
    out = {}
    for industry in national:
        n, g = national[industry], group[industry]
        if not math.isfinite(n) or not math.isfinite(g) or n < 0 or g < 0:
            raise ValueError(f"[BLOCKED] invalid wages {industry}")
        if n == 0 and g != 0:
            raise ValueError(f"[BLOCKED] group wages without national wage base {industry}")
        out[industry] = g / n if n else 0.0
    return out


def foreign_parity_remainder(us_all_source: float, mexico_booked_source: float) -> dict:
    """Assumption stress on rest-of-world only; neither endpoint is measured.

    US input must include corporate_labor. Mexican corporate tax is already
    booked in full, so no second Mexican labour share is added or subtracted.
    This is a parity stress, not an empirical finite bound on third countries.
    """
    if any(not math.isfinite(x) or x < 0 for x in (us_all_source, mexico_booked_source)):
        raise ValueError("[BLOCKED] nonfinite/negative foreign parity input")
    return {"rest_of_world_low": 0.0,
            "rest_of_world_parity_high": max(us_all_source - mexico_booked_source, 0.0),
            "mexico_exceeds_us_parity": max(mexico_booked_source - us_all_source, 0.0),
            "us_basis": "all source receipts, including corporate_labor",
            "kind": "assumption stress; not an empirical finite bound"}


def project_industry_wages(cell_counts, wage_cells):
    """Project group industry wages from explicit matched demographic cells.

    cell_counts maps (sex, band, schooling) -> weighted people; a rearing
    projection passes schooling-transition weighted counts instead. wage_cells
    maps the same keys -> {industry: annual gross subordinate wages/person}.
    Missing positive-count cells stop: use the lane's existing explicit
    nearest-schooling rule upstream, not a hidden national fallback here.
    """
    industries = set().union(*(x.keys() for x in wage_cells.values()))
    out = {industry: 0.0 for industry in industries}
    for cell, count in cell_counts.items():
        if not math.isfinite(count) or count < 0:
            raise ValueError(f"[BLOCKED] invalid projected population {cell}")
        if count and cell not in wage_cells:
            raise ValueError(f"[BLOCKED] no ENIGH industry wage cell {cell}")
        for industry, wage in wage_cells.get(cell, {}).items():
            if not math.isfinite(wage) or wage < 0:
                raise ValueError(f"[BLOCKED] invalid projected industry wage {cell}/{industry}")
            out[industry] += count * wage
    return out


def mexico_corporate_source(group_wages, national_wages, corporate_tax,
                            residual_tax, *, residual_policy, premise="long_run_new_capital",
                            pool_sectors=()):
    """Mexico corporate ISR source row, in the inputs' money unit.

    Identified sector taxes use individual industry's wage shares. The small
    source's unclassified tax remainder needs explicit policy: 'pooled_private'
    or 'exclude_beside'. Pooling choices are visible, caller-owned assumptions.
    Do not infer industry's profits or tax from its own wage bill.
    """
    if residual_policy not in {"pooled_private", "exclude_beside"}:
        raise ValueError("[BLOCKED] declare unclassified corporate-tax policy")
    shares = shares_from_wages(group_wages, national_wages)
    if not set(corporate_tax).issubset(shares):
        raise ValueError("[BLOCKED] SAT sector lacks ENIGH wage key")
    private = [industry for industry in shares if industry not in {"93", "UNMAPPED"}]
    private_national = math.fsum(national_wages[k] for k in private)
    if private_national <= 0:
        raise ValueError("[BLOCKED] no national private wage base for residual corporate key")
    private_share = math.fsum(group_wages[k] for k in private) / private_national
    if pool_sectors:
        den = math.fsum(national_wages[k] for k in pool_sectors)
        if den <= 0:
            raise ValueError("[BLOCKED] empty explicit wage pool")
        pooled = math.fsum(group_wages[k] for k in pool_sectors) / den
        # Only the thin management-of-companies cell is re-keyed to this
        # pool. Other service industries retain their individual wage keys.
        if "55" not in pool_sectors:
            raise ValueError("[BLOCKED] thin management cell55 missing from declared pool")
        shares["55"] = pooled
    taxes = {industry: corporate_tax.get(industry, 0.0) for industry in shares}
    shares["RESIDUAL_POOLED"] = private_share
    taxes["RESIDUAL_POOLED"] = residual_tax if residual_policy == "pooled_private" else 0.0
    result = source_taxes(shares, {"corporate": taxes}, {"corporate": {"low": 1.0, "high": 0.37}},
                          ["21", "93"], premise=premise)
    result["residual_policy"] = residual_policy
    result["residual_attribution"] = "unclassified SAT corporate gains and auxiliar receipts; pooled private wages, explicit assumption"
    result["pool_sectors"] = list(pool_sectors)
    result["corporate_labor"] = "included in full corporate row; no separate added/subtracted labor share"
    result["government_sector93"] = "46million ISR gains observed, but government business-capital response0, same item scope as US; not an observed tax zero"
    return result
