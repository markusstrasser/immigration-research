#!/usr/bin/env python3
"""Calendar-2024 person benefit allocation and SIPP 2025 survey uncertainty.

Native-First: stream the official ZIPs, reuse the owner/beneficiary allocator,
and evaluate weighted ratios with Census's 240 Fay-BRR replicates; no database.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import io
import json
import math
from pathlib import Path
import zipfile

import numpy as np
from public_mvp_io import (
    SIPP_BENEFIT_ALLOCATION, SIPP_NATIVITY_BASIS,
    iter_sipp_allocated_sample_units, SippPersonMonth,
)

REFERENCE_YEAR = 2024
REPLICATES = 240
FAY_FACTOR = 0.5
ENTRY_CODES = frozenset((1965,1971,1975,1979,1981,1985,1988,1990,1993,1995,
                         1997,1999,2000,2002,2004,2006,2009,2011,2013,2015,
                         2016,2017,2019,2021,2025))
METRICS = (
    'allocated_snap_usd', 'allocated_tanf_usd', 'individual_ssi_usd',
    'three_benefits_usd', 'person_earnings_usd', 'person_income_usd',
    'any_snap', 'any_tanf', 'any_ssi', 'any_three_benefits',
    'observed_months', 'in_frame_months', 'partial_frame_year',
    'zero_annual_earnings', 'negative_annual_earnings',
)


def annual_person(months: list[SippPersonMonth]) -> dict | None:
    """December sample, annual observed sums; no monthly annualization."""
    if len({row.month for row in months}) != len(months):
        raise ValueError('Duplicate person-month in annual calculation')
    december = next((row for row in months if row.month == 12), None)
    if december is None or not december.in_universe or december.weight <= 0:
        return None
    if december.age is None or not 25 <= december.age <= 64:
        return None
    if december.nativity not in (1,2):
        raise ValueError('Selected adult has unknown nativity')
    if december.nativity == 2 and december.entry_year not in ENTRY_CODES | {None}:
        raise ValueError(f'Invalid 2025 TYRENTRY code: {december.entry_year}')
    snap = sum(row.allocated_snap for row in months)
    tanf = sum(row.allocated_tanf for row in months)
    ssi = sum(row.ssi for row in months)
    earnings = sum(row.earnings for row in months)
    in_frame = sum(row.in_universe for row in months)
    return dict(
        sample_id=december.sample_id, person_number=december.person_number,
        weight=december.weight, nativity=december.nativity,
        entry_code=december.entry_year, age=december.age,
        allocated_snap_usd=snap, allocated_tanf_usd=tanf,
        individual_ssi_usd=ssi, three_benefits_usd=snap+tanf+ssi,
        person_earnings_usd=earnings, person_income_usd=sum(row.income for row in months),
        any_snap=float(any(row.snap_covered for row in months)),
        any_tanf=float(any(row.tanf_covered for row in months)),
        any_ssi=float(ssi>0), any_three_benefits=float(snap+tanf+ssi>0),
        observed_months=len(months), in_frame_months=in_frame,
        partial_frame_year=float(in_frame<12), zero_annual_earnings=float(earnings==0),
        negative_annual_earnings=float(earnings<0),
        out_of_frame_three_benefits_usd=sum(row.allocated_snap+row.allocated_tanf+row.ssi
                                          for row in months if not row.in_universe),
        out_of_frame_person_earnings_usd=sum(row.earnings for row in months if not row.in_universe),
    )


def domain_names(person: dict) -> tuple[str, ...]:
    base = 'native' if person['nativity']==1 else 'foreign_born'
    result = [base]
    if base == 'foreign_born':
        entry = person['entry_code']
        result.append('foreign_born_entry_unknown' if entry is None else
                      'foreign_born_entry_2022_25_code' if entry==2025 else
                      'foreign_born_entry_through_2021_code')
    if person['in_frame_months']==12:
        result.append(base+'_full_frame_year')
    return tuple(result)


def fay_se(point: np.ndarray | float, replicate_estimates: np.ndarray) -> np.ndarray:
    values = np.asarray(replicate_estimates, dtype=float)
    if values.shape[0] != REPLICATES or not np.isfinite(values).all():
        raise ValueError('Expected 240 finite replicate estimates')
    return np.sqrt(np.sum((values-point)**2, axis=0)/(REPLICATES*FAY_FACTOR**2))


def estimate_domain(values: np.ndarray, weights: np.ndarray, replicate_weights: np.ndarray) -> dict:
    if len(values)==0 or len(weights)!=len(values) or replicate_weights.shape!=(len(values),REPLICATES):
        raise ValueError('Empty or inconsistent domain arrays')
    denominators = replicate_weights.sum(axis=0)
    if weights.sum()<=0 or np.any(denominators<=0):
        raise ValueError('Nonpositive point or replicate domain denominator')
    point = (weights @ values)/weights.sum()
    replicates = (replicate_weights.T @ values)/denominators[:,None]
    se = fay_se(point,replicates)
    return dict(point=point,replicates=replicates,se=se,
                weighted_population=float(weights.sum()), population_replicates=denominators,
                population_se=float(fay_se(weights.sum(),denominators)))


def read_replicate_weights(schema: Path, archive_path: Path, people: list[dict]) -> tuple[np.ndarray,dict]:
    names = [entry['name'] for entry in json.loads(schema.read_text())]
    expected = ['SSUID','PNUM','SPANEL','SWAVE','MONTHCODE','REPWGT0']+[f'REPWGT{i}' for i in range(1,241)]
    if names != expected:
        raise ValueError('Unexpected SIPP 2025 replicate schema')
    selected = {(p['sample_id'],p['person_number']):i for i,p in enumerate(people)}
    if len(selected)!=len(people):
        raise ValueError('Duplicate selected annual person')
    result = np.full((len(people),REPLICATES),np.nan)
    seen = set()
    month_rows=december_rows=0
    with zipfile.ZipFile(archive_path) as archive:
        if archive.namelist()!=['rw2025.csv']:
            raise ValueError(f'Unexpected replicate ZIP members: {archive.namelist()}')
        with archive.open('rw2025.csv') as stream:
            reader=csv.reader(io.TextIOWrapper(stream,encoding='latin-1',newline=''),delimiter='|')
            for line,row in enumerate(reader,1):
                if line==1 and [field.upper() for field in row]==names:
                    continue
                if len(row)!=len(names):
                    raise ValueError(f'Replicate row {line} has unexpected width')
                month_rows+=1
                month=int(row[4])
                if not 1<=month<=12:
                    raise ValueError('Invalid replicate month')
                if month!=12:
                    continue
                december_rows+=1
                key=(row[0],int(row[1]))
                if key not in selected:
                    continue
                if key in seen:
                    raise ValueError(f'Duplicate selected December replicate key: {key}')
                seen.add(key)
                i=selected[key]
                if not math.isclose(float(row[5]),people[i]['weight'],abs_tol=1e-5,rel_tol=1e-10):
                    raise ValueError(f'REPWGT0 disagrees with December WPFINWGT: {key}')
                result[i]=np.asarray(row[6:],dtype=float)
    if len(seen)!=len(people) or not np.isfinite(result).all() or (result<0).any():
        raise ValueError(f'Missing or invalid December replicate weights: {len(seen)}/{len(people)}')
    return result,dict(replicate_person_month_rows=month_rows,replicate_december_rows=december_rows,
                       matched_selected_adults=len(seen))


def write_csv(path: Path, rows: list[dict]):
    with path.open('w',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def analyze(schema: Path, archive: Path, replicate_schema: Path, replicate_archive: Path, out: Path):
    people=[]
    audit=Counter()
    sample_programs=Counter()
    for sample in iter_sipp_allocated_sample_units(schema,archive):
        audit['sample_units']+=1
        audit['person_month_rows']+=len(sample)
        by_person=defaultdict(list)
        for row in sample:
            by_person[row.person_number].append(row)
            for program,amount in (('snap',row.allocated_snap),('tanf',row.allocated_tanf),('ssi',row.ssi)):
                sample_programs['all_people_'+program]+=amount
        for months in by_person.values():
            audit['distinct_people']+=1
            person=annual_person(months)
            if person is not None:
                people.append(person)
                for program,key in (('snap','allocated_snap_usd'),('tanf','allocated_tanf_usd'),('ssi','individual_ssi_usd')):
                    sample_programs['selected_adults_'+program]+=person[key]
    if not people:
        raise ValueError('No selected adults')
    print(f'Allocated {audit["person_month_rows"]:,} months; selected {len(people):,} adults',flush=True)
    reps,rep_audit=read_replicate_weights(replicate_schema,replicate_archive,people)
    values=np.asarray([[p[m] for m in METRICS] for p in people],dtype=float)
    weights=np.asarray([p['weight'] for p in people],dtype=float)
    domains=defaultdict(list)
    for i,person in enumerate(people):
        for group in domain_names(person):
            domains[group].append(i)
    estimates={}
    output=[]
    vectors={}
    for group,indices in sorted(domains.items()):
        index=np.asarray(indices)
        est=estimate_domain(values[index],weights[index],reps[index])
        est['nonzero']=np.count_nonzero(values[index],axis=0)
        estimates[group]=est
        vectors[group]=dict(zip(METRICS,est['replicates'].T.tolist()))
        for j,metric in enumerate(METRICS):
            point,se=float(est['point'][j]),float(est['se'][j])
            output.append(dict(group=group,reference_year=REFERENCE_YEAR,metric=metric,
                               unit='2024_USD_per_adult' if metric.endswith('_usd') else
                                    'months_per_adult' if metric.endswith('_months') else 'share_of_adults',
                               unweighted_adults=len(indices),weighted_adults=est['weighted_population'],
                               weighted_adults_se=est['population_se'],estimate=point,standard_error=se,
                               ci95_low=point-1.96*se,ci95_high=point+1.96*se,
                               nonzero_observations=int(est['nonzero'][j]),
                               zero_observation_warning=bool(est['nonzero'][j]==0)))
    contrasts=[]
    for left,right in (('foreign_born','native'),('foreign_born_entry_2022_25_code','native'),
                       ('foreign_born_entry_2022_25_code','foreign_born_entry_through_2021_code')):
        if left not in estimates or right not in estimates:
            continue
        a,b=estimates[left],estimates[right]
        gap=a['point']-b['point']
        se=fay_se(gap,a['replicates']-b['replicates'])
        for j,metric in enumerate(METRICS):
            contrasts.append(dict(left=left,right=right,metric=metric,
                                  unit='2024_USD_per_adult' if metric.endswith('_usd') else
                                       'months_per_adult' if metric.endswith('_months') else 'share_of_adults',
                                  difference=float(gap[j]),standard_error=float(se[j]),
                                  ci95_low=float(gap[j]-1.96*se[j]),ci95_high=float(gap[j]+1.96*se[j]),
                                  zero_observation_warning=bool(a['nonzero'][j]==0 or b['nonzero'][j]==0)))
    out.mkdir(parents=True,exist_ok=True)
    write_csv(out/'benefit_profiles_2024.csv',output)
    write_csv(out/'benefit_contrasts_2024.csv',contrasts)
    write_csv(out/'annual_person_allocations_2024.csv',people)
    (out/'replicate_estimates_2024.json').write_text(json.dumps(vectors)+'\n')
    for program in ('snap','tanf','ssi'):
        sample_programs['outside_selected_adults_'+program]=sample_programs['all_people_'+program]-sample_programs['selected_adults_'+program]
    hashes={}
    for name,path in (('microdata',archive),('schema',schema),('replicate_weights',replicate_archive),('replicate_schema',replicate_schema)):
        with path.open('rb') as handle:
            hashes[name]=dict(path=str(path),bytes=path.stat().st_size,sha256=hashlib.file_digest(handle,'sha256').hexdigest())
    (out/'manifest.json').write_text(json.dumps(dict(
        reference_year=REFERENCE_YEAR,source_year=2025,sources=hashes,
        selected_adults=len(people),audit=dict(audit),replicate_audit=rep_audit,
        unweighted_sample_benefits=dict(sample_programs),
        selected_out_of_frame_three_benefits_usd=sum(p['out_of_frame_three_benefits_usd'] for p in people),
        selected_out_of_frame_person_earnings_usd=sum(p['out_of_frame_person_earnings_usd'] for p in people),
        benefit_allocation=SIPP_BENEFIT_ALLOCATION,nativity=SIPP_NATIVITY_BASIS,
        weight_basis='December positive WPFINWGT once per person; age 25–64 and in frame in December; observed monthly sums, not annualized partial exposure',
        variance='240 Fay BRR replicate estimates; variance=sum((theta_r-theta)^2)/(240*0.5^2); full within-year contrast covariance; normal 95% intervals',
        broad_entry_definition='TYRENTRY=2025 is the pooled 2022–25 code, not a precise arrival year; TIMSTAT is not used as current status',
        limitations=['Direct SIPP survey estimates with an assumed equal-beneficiary allocation; no ACS matching.',
                     'SNAP/TANF/SSI only; neither full transfers nor net fiscal costs; amounts mix funding levels.',
                     'December survivors/residents; observed partial-year sums retained; full-frame subset is a selected sensitivity.',
                     'Reported earnings and income sum all observed months, including out-of-frame months; they are not an exclusively US earnings or taxable-income measure.',
                     'Replicate uncertainty excludes nonresponse bias, underreporting, imputation and allocation-model error.',
                     'Zero sample observations do not establish population zero; a zero BRR SE in that case is uninformative.']),indent=2)+'\n')
    print(json.dumps(dict(selected_adults=len(people),groups={k:len(v) for k,v in domains.items()},replicate_audit=rep_audit),indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--schema',type=Path,required=True)
    parser.add_argument('--zip',type=Path,required=True)
    parser.add_argument('--replicate-schema',type=Path,required=True)
    parser.add_argument('--replicate-zip',type=Path,required=True)
    parser.add_argument('--out-dir',type=Path,required=True)
    args=parser.parse_args()
    analyze(args.schema,args.zip,args.replicate_schema,args.replicate_zip,args.out_dir)
