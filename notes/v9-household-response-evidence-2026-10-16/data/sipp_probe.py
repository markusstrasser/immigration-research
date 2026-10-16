"""Read-only feasibility counts, not an effect estimate or a final analytic sample."""
import json
import time
import zipfile
from pathlib import Path
import pandas as pd

OUT = Path(__file__).parent
ROOT = Path('sources/immigration-fiscal/data/external')
paths = {
    2023: ROOT / 'stage2/census/sipp/pu2023_csv.zip',
    2024: ROOT / 'stage3/census/sipp/pu2024_csv.zip',
    2025: ROOT / 'stage3/census/sipp_2025/pu2025_csv.zip',
}
schema = json.loads((OUT / 'sipp_probe_schema.json').read_text())
base = ['SSUID', 'PNUM', 'SPANEL', 'SWAVE', 'MONTHCODE', 'ERESIDENCEID', 'THHLDSTATUS',
        'TAGE_EHC', 'RMESR', 'TPEARN', 'WPFINWGT', 'RHNUMPER', 'RHNUMPERWT2',
        'EEHC_WHY', 'EMS_EHC', 'EPNSPOUS_EHC', 'EPNCOHAB_EHC', 'TMOVER',
        'EHISPAN', 'THISPAN', 'EBORNUS', 'TCBIRTH', 'AEHC_WHY', 'TMWKHRS', 'AMWKHRS']
base += [f'{prefix}{i}' for prefix in ['ET2_LNO', 'TT2_AGE', 'ET2_WORK'] for i in range(1, 11)]
# Public schema has jobs 1-6 and a suppressed job-7 slot; no job-8 hours column.
base += [f'TJB{i}_MWKHRS' for i in range(1, 8)]
available = {v['name'] for v in schema}
wanted = [v for v in base if v in available]
result = {'description': __doc__, 'missing_requested': sorted(set(base)-available), 'files': {}}
persons = {}
for year, path in paths.items():
    start = time.monotonic()
    with zipfile.ZipFile(path) as z:
        member = next(n for n in z.namelist() if n.endswith('.csv'))
        with z.open(member) as f:
            cols = wanted if year == 2025 else ['SSUID', 'PNUM', 'SPANEL', 'SWAVE', 'MONTHCODE']
            d = pd.read_csv(f, sep='|', usecols=cols, dtype=str)
    assert not d.groupby('SSUID').SPANEL.nunique().gt(1).any(), 'SSUID crosses panels within file'
    persons[year] = set(zip(d.SPANEL, d.SSUID, d.PNUM))
    result['files'][year] = {'path': str(path), 'bytes': path.stat().st_size,
                            'rows': len(d), 'persons': len(persons[year]),
                            'panels': d.SPANEL.value_counts().to_dict(),
                            'seconds': round(time.monotonic()-start, 2)}
    if year != 2025:
        continue
    assert not d.duplicated(['SSUID', 'PNUM', 'MONTHCODE']).any(), 'duplicate person-month'
    for col in set(d.columns)-{'SSUID', 'PNUM', 'ERESIDENCEID'}:
        d[col] = pd.to_numeric(d[col], errors='raise')
    result['files'][year]['value_counts'] = {v:d[v].value_counts(dropna=False).to_dict()
        for v in ['THHLDSTATUS','RMESR','EEHC_WHY','RHNUMPERWT2']}
    d = d.sort_values(['SSUID', 'PNUM', 'MONTHCODE'])
    focal = d[d.TAGE_EHC.between(18,64)].copy()
    keys = ['SSUID','PNUM']
    prev = focal.groupby(keys).shift()
    adjacent = focal.MONTHCODE.eq(prev.MONTHCODE+1)
    samehome = focal.ERESIDENCEID.eq(prev.ERESIDENCEID) & adjacent
    type2_exit = pd.Series(False, index=focal.index)
    for i in range(1,11):
        type2_exit |= (prev[f'ET2_LNO{i}'].ge(60) & prev[f'TT2_AGE{i}'].ge(18)
                       & focal[f'ET2_LNO{i}'].isna() & samehome)
    result['type2_focal_departures'] = {
        'adult_focal_person_months': len(focal),
        'focal_person_months_with_adult_type2_exit': int(type2_exit.sum()),
        'focal_people_with_adult_type2_exit': int(focal.loc[type2_exit,keys].drop_duplicates().shape[0]),
        'both_months_employment_observed': int((type2_exit & focal.RMESR.between(1,8) & prev.RMESR.between(1,8)).sum()),
        'both_months_earnings_observed': int((type2_exit & focal.TPEARN.notna() & prev.TPEARN.notna()).sum()),
        'note': 'Focal ages 18-64 both months, unchanged residence, adjacent months within 2024; Type2 slot adult in prior month and missing next. Multiple focal adults can share one exit; not deduplicated household events. Missing slots require final codebook validation.'}
    # Tracked adult pair no longer co-resident next month, both still observed.
    result['missing_residence_adult_rows'] = int((d.TAGE_EHC.ge(18) & d.ERESIDENCEID.isna()).sum())
    adults = d[d.TAGE_EHC.ge(18) & d.ERESIDENCEID.notna()][['SSUID','PNUM','MONTHCODE','ERESIDENCEID']]
    pairs = adults.merge(adults,on=['SSUID','MONTHCODE','ERESIDENCEID'],suffixes=('_focal','_other'))
    pairs = pairs[pairs.PNUM_focal.ne(pairs.PNUM_other)].copy()
    pairs['NEXT_MONTH'] = pairs.MONTHCODE+1
    nxt = adults.rename(columns={'MONTHCODE':'NEXT_MONTH','ERESIDENCEID':'NEXT_HOME'})
    pairs = pairs.merge(nxt.rename(columns={'PNUM':'PNUM_focal','NEXT_HOME':'FOCAL_NEXT_HOME'}),on=['SSUID','PNUM_focal','NEXT_MONTH'])
    pairs = pairs.merge(nxt.rename(columns={'PNUM':'PNUM_other','NEXT_HOME':'OTHER_NEXT_HOME'}),on=['SSUID','PNUM_other','NEXT_MONTH'])
    events = pairs[pairs.FOCAL_NEXT_HOME.eq(pairs.ERESIDENCEID) & pairs.OTHER_NEXT_HOME.ne(pairs.ERESIDENCEID)]
    events = events.merge(focal[['SSUID','PNUM','MONTHCODE','RMESR','TPEARN']],left_on=['SSUID','PNUM_focal','NEXT_MONTH'],right_on=['SSUID','PNUM','MONTHCODE'])
    prior_work = d.set_index(['SSUID','PNUM','MONTHCODE']).RMESR
    events['PRIOR_RMESR'] = [prior_work.get((r.SSUID, r.PNUM_focal, r.NEXT_MONTH-1)) for r in events.itertuples()]
    work_observed = events.RMESR.between(1,8) & events.PRIOR_RMESR.between(1,8)
    assert events[['ERESIDENCEID','FOCAL_NEXT_HOME','OTHER_NEXT_HOME']].notna().all().all()
    result['tracked_adult_departures'] = {
        'focal_other_exit_transitions':len(events),
        'focal_person_exit_months':len(events[['SSUID','PNUM_focal','NEXT_MONTH']].drop_duplicates()),
        'departing_adult_months':len(events[['SSUID','PNUM_other','NEXT_MONTH']].drop_duplicates()),
        'focal_people':len(events[['SSUID','PNUM_focal']].drop_duplicates()),
        'focal_person_event_months_with_pre_post_employment':len(events.loc[work_observed,['SSUID','PNUM_focal','NEXT_MONTH']].drop_duplicates()),
        'note':'Adult person pairs co-resident in prior month and both observed next month, other moves and focal stays. Focal age18-64 post only. This is a descriptive candidate screen, not verified cause or clean event study.'}
    d.to_parquet(OUT / 'sipp2025_selected.parquet', index=False)
result['person_overlap'] = {f'{a}_{b}':len(persons[a]&persons[b]) for a,b in [(2023,2024),(2024,2025),(2023,2025)]}
result['person_overlap']['all3'] = len(persons[2023]&persons[2024]&persons[2025])
(OUT / 'sipp_probe.json').write_text(json.dumps(result, indent=2, default=str)+'\n')
print(json.dumps(result, indent=2, default=str))
