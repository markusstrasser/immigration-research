"""Pension-lane PIA responses for the back-cast's explicitly assumed income split.

Preserved public CPS supplies earnings-positive workers and earnings2019–2024,
under held legal/on-books adjustment. Earlier years hold relative workers/member
fixed and use ACS total income as the earnings proxy. Full-time medians and the
longer wages-only CPS extract are separately labelled sensitivities.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
PENSION = HERE.parent / "pension_accrual_2026_09_28"


@lru_cache(maxsize=1)
def pension_inputs():
    """Reuse the pension lane's cached frame, age-adjusted level and PIA formula."""
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(PENSION))
    import pension_accrual as p

    q = p.frame()
    q = q[q.union & (q.tax_oasdi > 0)].reset_index(drop=True)
    levels = np.clip(p.career_levels(q, "individual_age_adjusted"),
                     p.MODEL_LEVELS[0], p.MODEL_LEVELS[-1])
    births = np.clip(2024 - q.age.to_numpy(), p.BIRTHS[0], p.BIRTHS[-1]).astype(int)
    entries = np.where(q.mexico_born & q.arrival_age.notna(), q.arrival_age.fillna(21), 21)
    entries = np.array(p.ENTRIES)[np.clip(np.searchsorted(p.ENTRIES, np.maximum(entries, 21), side="right") - 1,
                                        0, len(p.ENTRIES) - 1)]
    econ = p.L.Economy()
    prelim = p.S.scaled_factors().preliminary.to_numpy()
    # Earnings/bend points share wage indexing. Normalise AIME by the first
    # bend point; this preserves each cohort's PIA elasticity exactly.
    x = np.empty(len(q))
    for i, (birth, level, entry) in enumerate(zip(births, levels, entries)):
        adj = level * p.L.LEVEL_ADJ["medium"] / p.MEDIUM_CAREER
        earnings = p.L.earnings_path(birth, adj, int(entry), prelim, econ)
        # The producer pays no retired-worker PIA without ten covered years.
        vested = int((earnings[:65] > 0).sum()) >= 10
        aime = p.L.top35((earnings * p.L.index_factors(birth, 60, econ))[:65]) / 420 if vested else 0.
        bp1 = 180 * econ.awi[birth + 60 - p.L.Y0] / econ.awi_1977
        x[i] = aime / bp1
    groups = {"union": np.ones(len(q), bool), "g1": q.mexico_born.to_numpy(),
              "g2": q.mexican_second_gen.to_numpy(), "g3plus": q.mexican_third_plus_selfid.to_numpy()}
    inputs = [PENSION / "pension_accrual.py", PENSION / "lifetime_model.py", PENSION / "sources.py",
              *PENSION.glob("_cache/stage_*.parquet"), PENSION / "reads/quotes.json",
              PENSION / "_cache/an2025-3.txt", PENSION / "_cache/tr2025.txt",
              p.ss.HERE / "ss_timing.py", p.ss.OUT / "cps_ss_stage.parquet",
              p.ONBOOKS_FILE, p.ENTRY_CODES, HERE / "inputs/acs_mexican_origin.csv", Path(__file__)]
    provenance = {}
    for path in inputs:
        with path.open("rb") as stream:
            provenance[str(path.relative_to(HERE.parents[2]))] = hashlib.file_digest(stream, "sha256").hexdigest()
    return p, econ, q, x, groups, provenance


def pia_normalized(x):
    p, econ, *_ = pension_inputs()
    # Invoke the producer's formula; use one real cohort's bend point as the
    # numeraire, rather than duplicate the statutory slopes in this consumer.
    birth = 1960
    bp1 = 180 * econ.awi[birth + 60 - p.L.Y0] / econ.awi_1977
    return p.L.pia_formula(np.asarray(x) * bp1, birth, econ) / bp1


def oasdi_response(factor, group="union"):
    """Finite PIA response, fixed workers/career/benefit timing and payable path."""
    _, _, q, x, groups, _ = pension_inputs()
    mask = groups[group]
    weights = q.w.to_numpy()[mask] * q.onbooks.to_numpy()[mask]
    anchor = float(weights @ pia_normalized(x[mask]))
    if anchor <= 0 or not np.isfinite(factor).all():
        raise ValueError("[BLOCKED] pension transport lacks positive finite PIA inputs")
    return pd.Series([float(weights @ pia_normalized(x[mask] * f)) / anchor for f in factor], index=factor.index)


def income_paths(relative):
    """Available CPS worker split, earlier held coverage and proxy sensitivities."""
    acs = pd.read_csv(HERE / "inputs/acs_mexican_origin.csv").set_index("year").reindex(relative.index)
    male = acs.median_earnings_ftyr_male_mexican / acs.median_earnings_ftyr_male_total
    female = acs.median_earnings_ftyr_female_mexican / acs.median_earnings_ftyr_female_total
    median = np.sqrt(male * female).interpolate().bfill()
    median /= median[2024]
    if median.isna().any() or not median.gt(0).all():
        raise ValueError("[BLOCKED] incomplete median earnings proxy")
    paths = dict(covered_workers_per_member=pd.Series(1., index=relative.index),
                 unsplit_income_earnings_proxy=relative / relative[2024], median_earnings_proxy=median)
    profile_dir = Path(os.environ.get('BACKCAST_WORKER_PROFILE_DIR', HERE / 'derived/oct15'))
    profile_path, audit_path = profile_dir / 'worker_income.csv', profile_dir / 'worker_income_audit.json'
    if not profile_path.exists() or not audit_path.exists():
        raise ValueError('[BLOCKED] run historical_workers.py for the preserved CPS worker split')
    worker_audit = json.loads(audit_path.read_text())
    if not worker_audit.get('survey_year_is_income_year_plus_one') or hashlib.sha256(profile_path.read_bytes()).hexdigest() != worker_audit.get('output_sha256'):
        raise ValueError('[BLOCKED] worker profile year alignment/output receipt mismatch')
    for entry in worker_audit['sources']:
        source = HERE.parents[2] / entry['path']
        with source.open('rb') as stream:
            if hashlib.file_digest(stream, 'sha256').hexdigest() != entry['sha256']:
                raise ValueError('[BLOCKED] worker split source changed: ' + entry['path'])
    measured = pd.read_csv(profile_path)
    for group in ("union", "g1", "g2", "g3plus"):
        pub = measured[(measured.group == group) & measured.definition.eq('positive_wage_or_SE_age_lt65')].set_index('year')
        wage = measured[(measured.group == group) & measured.definition.eq('wage_only_age_lt65_IPUMS_all_ASEC')].set_index('year')
        pub_o = measured[(measured.group == group) & measured.definition.eq('positive_wage_or_SE_all_ages_oasdi')].set_index('year')
        wage_o = measured[(measured.group == group) & measured.definition.eq('wage_only_all_ages_oasdi_IPUMS_all_ASEC')].set_index('year')
        if any(set(v.index) != set(range(2019, 2025)) for v in (pub, pub_o)) or any(set(v.index) != set(relative.index) for v in (wage, wage_o)):
            raise ValueError('[BLOCKED] incomplete measured worker/income years')
        workers = pd.Series(1., index=relative.index)
        workers_o = pd.Series(1., index=relative.index)
        earnings = paths['unsplit_income_earnings_proxy'].copy()
        for year in pub.index:
            workers[year] = pub.loc[year, 'relative_workers_per_member'] / pub.loc[2024, 'relative_workers_per_member']
            workers_o[year] = pub_o.loc[year, 'relative_workers_per_member'] / pub_o.loc[2024, 'relative_workers_per_member']
            earnings[year] = pub_o.loc[year, 'relative_earnings_per_worker'] / pub_o.loc[2024, 'relative_earnings_per_worker']
        paths[f'covered_workers_per_member_{group}'] = workers
        paths[f'oasdi_workers_per_member_{group}'] = workers_o
        paths[f'central_earnings_per_worker_{group}'] = earnings
        paths[f'wage_only_workers_per_member_{group}'] = wage.relative_workers_per_member / wage.loc[2024, 'relative_workers_per_member']
        paths[f'wage_only_oasdi_workers_per_member_{group}'] = wage_o.relative_workers_per_member / wage_o.loc[2024, 'relative_workers_per_member']
        paths[f'wage_only_earnings_per_worker_{group}'] = wage_o.relative_earnings_per_worker / wage_o.loc[2024, 'relative_earnings_per_worker']
        paths[f'ACS_to_CPS_labour_residual_{group}'] = paths['unsplit_income_earnings_proxy'] / (workers_o * earnings)
        for label, values in [('central_earnings_per_worker', earnings), ('median_earnings_proxy', median),
                              ('wage_only_earnings_per_worker', paths[f'wage_only_earnings_per_worker_{group}'])]:
            paths[f"oasdi_{group}_{label}"] = oasdi_response(values, group)
    paths['covered_workers_per_member'] = paths['covered_workers_per_member_union']
    _, _, q, x, groups, provenance = pension_inputs()
    audit = {"inputs": provenance, "groups": {},
             "worker_rule": "CPS wage/positive-SE workers/member relative to national, normalized to2024; income2019–2024 uses surveys2020–2025; PartA age<65/OASDI all ages; fixed relative coverage before2019; legal/on-books adjustment held",
             "earnings_rule": "CPS mean covered-earnings mapping per worker2019–2024; unsplit ACS total-income proxy before2019; not an exact ACS decomposition",
             "median_rule": "geometric mean male/female relative full-time medians; pension-only sensitivity with central worker path",
             "wage_only_rule": "pooled IPUMS wage-positive workers/mean wages; PartA age<65 and OASDI all ages, all ASEC; missing SE and canonical civilian matching, beside only",
             "population_rule": "published CPS source weights estimate normalized relative rates; live fiscal population remains the case's own frame/count",
             "extension": "original pension union inputs transported to completed/coverage people; G3+ mapping used for added people",
             "benefit_rule": "finite own-PIA response; fixed careers, family/mortality/payability/benefit-tax timing; not full actuarial repricing"}
    audit['worker_split'] = worker_audit
    audit['worker_profile_sha256'] = hashlib.sha256(profile_path.read_bytes()).hexdigest()
    for group, mask in groups.items():
        factors = pd.Series([1 - 1e-5, 1., 1 + 1e-5])
        response = oasdi_response(factors, group)
        audit["groups"][group] = dict(pia_earnings_elasticity=float((response.iloc[2] - response.iloc[0]) / 2e-5),
                                     mean_aime_over_first_bend=float(np.average(x[mask], weights=q.w.to_numpy()[mask])),
                                     worker_sample_n=int(mask.sum()), vested_PIA_sample_n=int((x[mask] > 0).sum()))
    return paths, audit


def part_group(part, info):
    generation = {"G1": "g1", "G2": "g2", "G3plus": "g3plus", "G3+": "g3plus"}.get(info.get("generation"))
    return generation or ("g3plus" if part.startswith("v5_") or info.get("path") == "lineage" or
                           info.get("population_path") == "g3plus" else "union")


def part_factor(part, info, paths, proxy="central_earnings_per_worker"):
    if info["rule"] != "accrual":
        return paths['unsplit_income_earnings_proxy']
    group = part_group(part, info)
    worker_path = paths[f'wage_only_workers_per_member_{group}' if proxy == 'wage_only_earnings_per_worker'
                        else f'covered_workers_per_member_{group}']
    if info["contributions"] == "hi":
        return worker_path
    if info["contributions"] != "oasdi":
        raise ValueError(f"[BLOCKED] unknown pension contribution rule for {part}")
    worker_path = paths[f'wage_only_oasdi_workers_per_member_{group}' if proxy == 'wage_only_earnings_per_worker'
                        else f'oasdi_workers_per_member_{group}']
    return worker_path * paths[f"oasdi_{group}_{proxy}"]
