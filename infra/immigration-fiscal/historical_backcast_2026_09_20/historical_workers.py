"""Measure the available pension-worker split from preserved CPS inputs only.

Public-use 2019–2024 supplies positive wages and farm/self-employment income;
pooled IPUMS 2005–2024 supplies wages alone (a separate proxy sensitivity).
Legal/on-books status is not observed; its relative adjustment is held fixed.
The CPS labour-income identity is not an exact split of ACS total income.
"""
from __future__ import annotations

import argparse
import hashlib
import inspect
import json
import sys
import time
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np
import pandas as pd

import historical_use as h

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(HERE.parent / 'pension_accrual_2026_09_28'))
import pension_accrual as p


def rows_from_sums(sums, year, source, definition):
    rows = []
    npop, nworkers, nearnings = sums['national']
    for group, (pop, workers, earnings) in sums.items():
        if group == 'national':
            continue
        if min(pop, workers, earnings, npop, nworkers, nearnings) <= 0:
            raise ValueError('[BLOCKED] nonpositive worker-income denominator')
        worker_ratio = (workers / pop) / (nworkers / npop)
        earnings_ratio = (earnings / workers) / (nearnings / nworkers)
        income_ratio = (earnings / pop) / (nearnings / npop)
        if abs(worker_ratio * earnings_ratio - income_ratio) > 1e-12:
            raise ValueError('[BLOCKED] worker x earnings CPS labour identity')
        rows.append(dict(year=year, survey_year=year + 1, source=source, definition=definition, group=group,
                         group_population=pop, national_population=npop, group_workers=workers,
                         national_workers=nworkers, group_earnings=earnings, national_earnings=nearnings,
                         relative_workers_per_member=worker_ratio, relative_earnings_per_worker=earnings_ratio,
                         relative_labour_income_per_member=income_ratio))
    return rows


def public_split(module, sources):
    rows = []
    econ = p.L.Economy()
    if econ.base[2024 - p.L.Y0] != p.ss.ext.OASDI_CAP_2024:
        raise ValueError('[BLOCKED] primary contribution-base table differs from pension worker mapping in2024')
    fields = ['PH_SEQ', 'PPPOS', 'A_AGE', 'PRPERTYP', 'PRCITSHP', 'PENATVTY', 'PEFNTVTY', 'PEMNTVTY',
              'PRDTHSP', 'WSAL_VAL', 'SEMP_VAL', 'FRSE_VAL']
    for survey_year, (path, pin) in module.SOURCES.items():
        sources.append(h.verified_source(path, pin))
        sums = {definition: {g: np.zeros(3) for g in ('national', 'union', 'g1', 'g2', 'g3plus')}
                for definition in ('positive_wage_or_SE_age_lt65', 'positive_wage_or_SE_all_ages_oasdi')}
        with zipfile.ZipFile(path) as z:
            weights = pd.read_csv(z.open(f'asec_csv_repwgt_{survey_year}.csv'),
                                  usecols=['h_seq', 'PPPOS', 'pwwgt0']).rename(columns={'h_seq': 'PH_SEQ'})
            for chunk in pd.read_csv(z.open(f'pppub{survey_year % 100}.csv'), usecols=fields, chunksize=50_000):
                d = chunk.merge(weights, on=['PH_SEQ', 'PPPOS'], how='left', validate='one_to_one')
                if d.isna().any().any():
                    raise ValueError('[BLOCKED] missing public worker field/weight')
                civ, union = module.canonical_target(d)
                native = d.PRCITSHP.isin([1, 2, 3]).to_numpy()
                g1 = union & ~native
                g2 = union & native & (d.PEFNTVTY.eq(303) | d.PEMNTVTY.eq(303)).to_numpy()
                g3 = union & ~g1 & ~g2
                wage = d.WSAL_VAL.clip(lower=0).to_numpy(float)
                se = (d.SEMP_VAL.clip(lower=0) + d.FRSE_VAL.clip(lower=0)).to_numpy(float)
                all_workers = (wage > 0) | (se > 0)
                cap = econ.base[survey_year - 1 - p.L.Y0]
                if not np.isfinite(cap) or cap <= 0:
                    raise ValueError('[BLOCKED] missing pension-lane historical contribution base')
                # Same covered-earnings mapping as pension career_levels:
                # capped wages + 92.35% of positive SE; worker eligibility
                # matches Part A's age<65 positive-tax condition.
                earned = np.minimum(wage, cap) + p.ss.SECA_FACTOR * se
                w = d.pwwgt0.to_numpy(float)
                h.partition_gate(w, union, civ)
                for definition, aggregate in sums.items():
                    worker = all_workers & d.A_AGE.lt(65).to_numpy() if definition.endswith('lt65') else all_workers
                    for group, mask in dict(national=civ, union=union, g1=g1, g2=g2, g3plus=g3).items():
                        aggregate[group] += [w[mask].sum(), (w * worker)[mask].sum(), (w * earned * worker)[mask].sum()]
        for definition, aggregate in sums.items():
            rows += rows_from_sums(aggregate, survey_year - 1, str(path.relative_to(h.ROOT)), definition)
    return rows


def wage_only_split(sources):
    sources.append(h.verified_source(h.POOLED, h.POOLED_PIN))
    ddi = h.POOLED.with_suffix('').with_suffix('.xml')
    variable = next(v for v in ET.parse(ddi).getroot().iter() if v.attrib.get('name') == 'INCWAGE')
    coding = ''.join(v.text or '' for v in variable.iter() if v.tag.split('}')[-1] == 'codInstr')
    if '99999999 = N.I.U.' not in coding or '99999998 = Missing (1962-1966 only)' not in coding:
        raise ValueError('[BLOCKED] pooled wage sentinel declaration changed')
    fields = [*h.COLS, 'INCWAGE']
    sums = {definition: {year: {g: np.zeros(3) for g in ('national', 'union', 'g1', 'g2', 'g3plus')} for year in h.YEARS}
            for definition in ('wage_only_age_lt65_IPUMS_all_ASEC', 'wage_only_all_ages_oasdi_IPUMS_all_ASEC')}
    for chunk in pd.read_csv(h.POOLED, usecols=fields, chunksize=100_000):
        d = chunk[chunk.ASECFLAG.eq(1) & chunk.YEAR.between(2006, 2025)]
        if d[fields].isna().any().any():
            raise ValueError('[BLOCKED] missing pooled wage proxy field')
        native = d.BPL.lt(15000)
        g1 = d.BPL.eq(20000)
        g2 = native & (d.MBPL.eq(20000) | d.FBPL.eq(20000))
        g3 = native & d.MBPL.lt(15000) & d.FBPL.lt(15000) & d.HISPAN.isin(h.MEX_HISPAN)
        masks = dict(national=np.ones(len(d), bool), union=(g1 | g2 | g3).to_numpy(),
                     g1=g1.to_numpy(), g2=g2.to_numpy(), g3plus=g3.to_numpy())
        w = d.ASECWT.to_numpy(float) * np.where(d.YEAR.eq(2014), 0.5, 1.)
        # DDI codInstr: 99999999 NIU, 99999998 missing only 1962–1966.
        wage = d.INCWAGE.where(~d.INCWAGE.isin([99999998, 99999999]), 0).clip(lower=0).to_numpy(float)
        for definition, aggregate in sums.items():
            worker = (wage > 0) & d.AGE.lt(65).to_numpy() if 'lt65' in definition else wage > 0
            for year in d.YEAR.unique():
                in_year = d.YEAR.eq(year).to_numpy()
                for group, mask in masks.items():
                    take = mask & in_year
                    aggregate[int(year) - 1][group] += [w[take].sum(), (w * worker)[take].sum(), (w * wage * worker)[take].sum()]
    return [row for definition, aggregate in sums.items() for year, values in aggregate.items()
            for row in rows_from_sums(values, year, str(h.POOLED.relative_to(h.ROOT)), definition)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out-dir', type=Path, default=HERE / 'derived/oct15')
    args = parser.parse_args()
    started = time.perf_counter()
    sources = []
    module = h.pandemic_module()
    public_started = time.perf_counter()
    rows = public_split(module, sources)
    public_seconds = time.perf_counter() - public_started
    pooled_started = time.perf_counter()
    rows += wage_only_split(sources)
    pooled_seconds = time.perf_counter() - pooled_started
    table = pd.DataFrame(rows).sort_values(['definition', 'group', 'year'])
    if len(table) != 208 or table.duplicated(['definition', 'group', 'year']).any():
        raise ValueError('[BLOCKED] incomplete historical worker grid')
    for path in (Path(__file__), Path(h.__file__), h.POOLED.with_suffix('').with_suffix('.xml'),
                 Path(inspect.getsourcefile(module.canonical_target)), Path(p.__file__), Path(p.L.__file__),
                 Path(p.S.__file__), Path(p.ss.__file__), Path(p.ss.ext.__file__),
                 p.CACHE / 'tr2025.txt', p.S.QUOTES):
        with path.open('rb') as stream:
            sources.append(dict(path=str(path.relative_to(h.ROOT)), sha256=hashlib.file_digest(stream, 'sha256').hexdigest()))
    sys.path.insert(0, str(HERE.parent / 'scripts'))
    from memory_budget import require_within_budget
    footprint = require_within_budget('historical worker extraction')
    args.out_dir.mkdir(parents=True, exist_ok=True)
    table.to_csv(args.out_dir / 'worker_income.csv', index=False, lineterminator='\n', float_format='%.15g')
    audit = dict(sources=sources, survey_year_is_income_year_plus_one=True,
                 worker_definition='positive wage or positive farm/self-employment; PartA age<65, OASDI all positive-tax ages',
                 age_rule='reported ASEC survey age matches original pension producer; exact prior-year work-spell age not observed',
                 legal_rule='on-books/legal coverage relative adjustment held fixed; CPS does not observe covered records',
                 income_boundary='CPS earned-income split; not exact ACS total income decomposition',
                 available_public_years=list(range(2019, 2025)), wage_only_years=h.YEARS,
                 historical_cap='pension lane Economy.base; earnings mapping matches career_levels',
                 pooled_NIU_source='asec_pooled.xml INCWAGE codInstr 99999999 and 99999998',
                 output_sha256=hashlib.sha256((args.out_dir / 'worker_income.csv').read_bytes()).hexdigest())
    (args.out_dir / 'worker_income_audit.json').write_text(json.dumps(audit, indent=2) + '\n')
    print(f'worker extraction {len(table)} rows; public_seconds={public_seconds:.3f}; pooled_seconds={pooled_seconds:.3f}; '
          f'seconds={time.perf_counter()-started:.3f}; physical_footprint={footprint}')


if __name__ == '__main__':
    main()
