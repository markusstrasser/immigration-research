# /// script
# requires-python = ">=3.11"
# dependencies = ["duckdb", "numpy", "pandas"]
# ///
"""Descriptive ACS wages by nativity and disjoint ethnicity/race partitions.

Native-First: stream existing Census ZIPs and reuse the established ACS ratio,
SDR and archive helpers. No regression, status imputation or database access.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import json
from pathlib import Path

import numpy as np
import pandas as pd

from analyze_arrival_cohorts import person_streams, ratios, sdr_estimate, sha256, WEIGHTS

FIELDS = ['AGEP','SEX','NATIVITY','POBP','HISP','RAC1P','RACBLK','SCHL','ESR',
          'RELSHIPP','WAGP','PERNP','ADJINC']
CATEGORIES = ('hispanic_any_race','nonhisp_black','nonhisp_white_alone',
              'nonhisp_asian_alone','nonhisp_other_multiracial')
COLUMNS = ('adults','employed','positive_wage','wages','earnings','employed_wages',
           'employed_earnings','positive_wages','zero_earnings','negative_earnings',
           'age','male','ba_plus')
METRICS = {
    'employment_population': ('employed','adults','share'),
    'wages_all_adults': ('wages','adults','2024_USD'),
    'earnings_all_adults': ('earnings','adults','2024_USD'),
    'wages_currently_employed': ('employed_wages','employed','2024_USD'),
    'earnings_currently_employed': ('employed_earnings','employed','2024_USD'),
    'wages_positive_wage_recipients': ('positive_wages','positive_wage','2024_USD'),
    'positive_wage_share': ('positive_wage','adults','share'),
    'zero_earnings_share': ('zero_earnings','adults','share'),
    'negative_earnings_share': ('negative_earnings','adults','share'),
    'mean_age': ('age','adults','years'),
    'male_share': ('male','adults','share'),
    'ba_plus_share': ('ba_plus','adults','share'),
}


def race_codes(frame: pd.DataFrame, black_any_race: bool = False) -> np.ndarray:
    """Hispanic takes precedence; each person belongs to one of five groups."""
    if not (frame.HISP.between(1,24)&frame.RAC1P.between(1,9)&frame.RACBLK.isin([0,1])).all():
        raise ValueError('Invalid ethnicity/race code')
    if ((frame.RAC1P.eq(2)&frame.RACBLK.ne(1)) |
            (frame.RACBLK.eq(1)&~frame.RAC1P.isin([2,9]))).any():
        raise ValueError('Inconsistent Black-alone/combination codes')
    result = np.full(len(frame),4)
    result[frame.RAC1P.eq(6)] = 3
    result[frame.RAC1P.eq(1)] = 2
    result[frame.RACBLK.eq(1) if black_any_race else frame.RAC1P.eq(2)] = 1
    result[frame.HISP.ne(1)] = 0
    return result


def selected_frame(frame: pd.DataFrame) -> pd.DataFrame:
    adult = frame.AGEP.between(25,64)
    if frame.loc[adult,FIELDS].isna().any().any():
        raise ValueError('Missing adult outcome or classification; no zero substitution')
    if not (frame.loc[adult,'ESR'].isin([1,2,3,4,5]) | frame.loc[adult,'ESR'].eq(6)).all():
        raise ValueError('Invalid adult employment code')
    if not frame.loc[adult,'RELSHIPP'].between(20,38).all():
        raise ValueError('Invalid household/group-quarter relationship code')
    return frame.loc[adult & frame.RELSHIPP.ne(37) & ~frame.ESR.isin([4,5])].copy()


def group_masks(frame: pd.DataFrame) -> dict:
    if not frame.NATIVITY.isin([1,2]).all():
        raise ValueError('Invalid nativity code')
    groups = {}
    for nativity, code in [('native',1),('foreign_born',2)]:
        member = frame.NATIVITY.eq(code).to_numpy()
        groups[('aggregate',nativity,'all')] = member
        for partition, broad in [('black_alone',False),('black_any_race',True)]:
            race = race_codes(frame,broad)
            for j, category in enumerate(CATEGORIES):
                groups[(partition,nativity,category)] = member & (race==j)
        for label, mask in [('black_alone_any_ethnicity',frame.RAC1P.eq(2)),
                            ('black_any_race_any_ethnicity',frame.RACBLK.eq(1))]:
            groups[('overlap_sensitivity',nativity,label)] = member & mask.to_numpy()
    groups[('aggregate','foreign_born','mexico_born')] = (frame.NATIVITY.eq(2)&frame.POBP.eq(303)).to_numpy()
    return groups


def outcome_matrix(frame: pd.DataFrame, to_2024: float) -> np.ndarray:
    adjustment = frame.ADJINC.to_numpy()/1_000_000*to_2024
    if (adjustment<=0).any() or (frame.WAGP<0).any():
        raise ValueError('Invalid adjustment or negative wage/salary amount')
    wages = frame.WAGP.to_numpy()*adjustment
    earnings = frame.PERNP.to_numpy()*adjustment
    employed = frame.ESR.isin([1,2]).to_numpy()
    positive = wages>0
    return np.column_stack((np.ones(len(frame)),employed,positive,wages,earnings,
        wages*employed,earnings*employed,wages*positive,earnings==0,earnings<0,
        frame.AGEP,frame.SEX.eq(1),frame.SCHL.ge(21)))


def add_chunk(frame: pd.DataFrame, factor: float, sums: dict, counts: dict):
    selected = selected_frame(frame)
    if selected.empty:
        return
    if not selected.SCHL.between(1,24).all() or not selected.SEX.isin([1,2]).all():
        raise ValueError('Invalid education or sex code')
    values = outcome_matrix(selected,factor)
    weight = selected[WEIGHTS].to_numpy()
    for key, mask in group_masks(selected).items():
        if mask.any():
            sums[key] += weight[mask].T @ values[mask]
            counts[key] += np.count_nonzero(values[mask,:3],axis=0)


def check_partitions(sums: dict):
    for nativity in ('native','foreign_born'):
        for partition in ('black_alone','black_any_race'):
            total = sum(sums[(partition,nativity,category)] for category in CATEGORIES)
            if not np.allclose(total,sums[('aggregate',nativity,'all')],rtol=1e-10,atol=1e-5):
                raise ValueError('Ethnicity/race partition fails weighted conservation')


def write_estimates(year: int, sums: dict, counts: dict, output: Path) -> dict:
    check_partitions(sums)
    rows, vectors = [], {}
    for group, aggregate in sorted(sums.items()):
        for metric,(numerator,denominator,unit) in METRICS.items():
            den = aggregate[:,COLUMNS.index(denominator)]
            vector = ratios(aggregate[:,COLUMNS.index(numerator)],den)
            key = '|'.join((*group,metric))
            vectors[key] = vector.tolist()
            rows.append(dict(year=year,partition=group[0],nativity=group[1],race_ethnicity=group[2],
                metric=metric,unit=unit,unweighted_adults=int(counts[group][0]),
                unweighted_denominator=int(counts[group][COLUMNS.index(denominator)]),
                weighted_adults=float(aggregate[0,0]),weighted_denominator=float(den[0]),**sdr_estimate(vector)))
    pd.DataFrame(rows).to_csv(output/f'wage_profiles_{year}.csv',index=False)
    (output/f'wage_replicates_{year}.json').write_text(json.dumps(vectors)+'\n')
    sufficient = {'|'.join(k):v.tolist() for k,v in sums.items()}
    (output/f'wage_sufficient_statistics_{year}.json').write_text(json.dumps(dict(columns=COLUMNS,groups=sufficient))+'\n')
    pairs = [
        (('black_alone','native','nonhisp_black'),('black_alone','native','nonhisp_white_alone')),
        (('black_alone','foreign_born','nonhisp_black'),('black_alone','native','nonhisp_black')),
        (('aggregate','foreign_born','mexico_born'),('aggregate','native','all')),
        (('black_alone','native','nonhisp_black'),('aggregate','foreign_born','mexico_born')),
        (('black_any_race','native','nonhisp_black'),('black_alone','native','nonhisp_black')),
    ]
    contrasts = []
    for left,right in pairs:
        for metric,(_,_,unit) in METRICS.items():
            a,b = (np.array(vectors['|'.join((*group,metric))]) for group in (left,right))
            contrasts.append(dict(year=year,left='|'.join(left),right='|'.join(right),metric=metric,unit=unit,
                                  **sdr_estimate(a-b)))
    pd.DataFrame(contrasts).to_csv(output/f'wage_contrasts_{year}.csv',index=False)
    return vectors


def run_year(year: int, path: Path, calibration: dict, output: Path) -> dict:
    factor = calibration['factors']['2019_to_2024']['factor'] if year==2019 else 1.0
    if not np.isfinite(factor) or factor<=0:
        raise ValueError('Invalid common-dollar conversion')
    sums = defaultdict(lambda: np.zeros((81,len(COLUMNS))))
    counts = defaultdict(lambda: np.zeros(3,dtype=int))
    anchors = {name:np.zeros(81) for name in ('Total population','Total males (SEX=1)','Age 25-34')}
    rows_read = negative_replicates = 0
    with person_streams(path) as streams:
        for name,stream in streams:
            for frame in pd.read_csv(stream,usecols=FIELDS+WEIGHTS,dtype=float,chunksize=100_000):
                rows_read += len(frame)
                weight = frame[WEIGHTS].to_numpy()
                if not np.isfinite(weight).all() or (weight[:,0]<=0).any():
                    raise ValueError('Invalid person weight')
                negative_replicates += int((weight[:,1:]<0).sum())
                anchors['Total population'] += weight.sum(axis=0)
                anchors['Total males (SEX=1)'] += weight[frame.SEX.eq(1)].sum(axis=0)
                anchors['Age 25-34'] += weight[frame.AGEP.between(25,34)].sum(axis=0)
                expected_adj = {2019:1010145,2024:1015250}[year]
                if not frame.ADJINC.eq(expected_adj).all():
                    raise ValueError(f'Unexpected {year} ADJINC; verify new dictionary/data vintage')
                add_chunk(frame,factor,sums,counts)
            print(f'{year}: {name} complete; {rows_read:,} source records',flush=True)
    official = calibration['calibration'][str(year)]
    if rows_read != official['official_national_person_records']:
        raise ValueError('National source row count differs from official calibration')
    checked = {}
    for name,values in anchors.items():
        estimate = sdr_estimate(values)
        target = official['anchors'][name]
        if estimate['estimate']!=target['estimate'] or abs(estimate['acs_sdr_se']-target['sdr_se_published_rounded'])>.5:
            raise ValueError(f'Official full/replicate anchor failed: {name}')
        checked[name] = estimate
    vectors = write_estimates(year,sums,counts,output)
    manifest = dict(year=year,source_path=str(path),source_sha256=sha256(path),source_bytes=path.stat().st_size,
        raw_person_rows=rows_read,negative_replicates_retained=negative_replicates,anchors=checked,
        to_2024_dollars=factor,unit='All amounts in 2024 dollars; rolling past12months, not hourly or calendar-year wages',
        population='Civilian noninstitutional adults25–64; 50states+DC; noninstitutional group quarters retained',
        partitions='Hispanic any race first; non-Hispanic Black, White alone, Asian alone, other/multiracial. Black-alone and Black-any-race are separately exhaustive partitions.',
        overlap='All-native, all-FB, Mexico-born and any-ethnicity Black sensitivity rows overlap partitions; never sum them together.',
        estimands='All-adult wage/earnings means include zeros and earnings losses. Currently employed means ESR1/2 at interview, retaining zero wages among self-employed. Positive-wage means condition on WAGP>0 during rolling12months.',
        variance='80 SDR whole-estimate replicates, 4/80; within-year differences preserve covariance; normal95% sampling intervals only',
        limits=['No causal race coefficient, policy effect or within-person wage change.',
                'Age, sex, education, weeks/hours, occupational and migration composition are not standardized.',
                'Earnings include self-employment; wages exclude it. Current employment and income reference windows differ.',
                'Race question/processing changed in2020; between-year category composition is not fixed.',
                'Nonresponse, coverage, income reporting/topcoding and classification uncertainty are not in sampling intervals.'])
    (output/f'wage_manifest_{year}.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(f'{year}: {len(vectors)} profiles; three official calibration anchors passed',flush=True)
    return vectors


def write_changes(before: dict, after: dict, output: Path):
    if before.keys()!=after.keys():
        raise ValueError('Yearly profile coverage differs')
    rows = []
    for key in before:
        b,a = sdr_estimate(np.array(before[key])),sdr_estimate(np.array(after[key]))
        delta = a['estimate']-b['estimate']
        se = float(np.hypot(a['acs_sdr_se'],b['acs_sdr_se']))
        partition,nativity,race,metric = key.split('|')
        rows.append(dict(partition=partition,nativity=nativity,race_ethnicity=race,metric=metric,
            unit=METRICS[metric][2],estimate_2019=b['estimate'],estimate_2024=a['estimate'],
            difference_2024_minus_2019=delta,se_assuming_cross_year_independence=se,
            ci95_low=delta-1.96*se,ci95_high=delta+1.96*se))
    pd.DataFrame(rows).to_csv(output/'wage_changes_2019_2024.csv',index=False)


if __name__=='__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--acs-2024',required=True,type=Path)
    parser.add_argument('--acs-2019',type=Path)
    parser.add_argument('--inflation',required=True,type=Path)
    parser.add_argument('--output',required=True,type=Path)
    args = parser.parse_args()
    calibration = json.loads(args.inflation.read_text())
    args.output.mkdir(parents=True,exist_ok=True)
    after = run_year(2024,args.acs_2024,calibration,args.output)
    if args.acs_2019 is not None:
        before = run_year(2019,args.acs_2019,calibration,args.output)
        write_changes(before,after,args.output)
    (args.output/'wage_sources.json').write_text(json.dumps(dict(inflation_path=str(args.inflation),
        inflation_sha256=sha256(args.inflation),inflation_selected_vintage=calibration['selected_vintage'],
        dictionary_2019='https://www2.census.gov/programs-surveys/acs/tech_docs/pums/data_dict/PUMS_Data_Dictionary_2019.pdf',
        dictionary_2024='https://www2.census.gov/programs-surveys/acs/tech_docs/pums/data_dict/PUMS_Data_Dictionary_2024.pdf'),indent=2)+'\n')
