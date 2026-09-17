from pathlib import Path
import csv, hashlib, json

ROOT = Path(__file__).resolve().parent / '_cache/oi'
manifest = json.loads((ROOT/'manifest.json').read_text())
files = {r['name']:(ROOT/r['name'] if r['status'] != 'held_readonly_not_copied' else Path(r['local_path'])) for r in manifest}
checks = {}
for r in manifest:
    assert hashlib.sha256(files[r['name']].read_bytes()).hexdigest() == r['sha256'], r['name']
checks['source_hashes_match_manifest'] = True

def read(name):
    return list(csv.DictReader(files[name].open(encoding='utf-8-sig')))

country_a = read('race_table6a_parametric.csv')
country_b = read('race_table6b_nonpar.csv')
national = read('race_table1.csv')
natmom = read('race_table3_nativemom.csv')
assert len(country_a) == len({r['country'] for r in country_a})
assert {int(r['par_pctile']) for r in national} == set(range(1,101))
checks['table6a_rows'] = len(country_a)
checks['table6a_non_USA_countries'] = len(country_a)-1
checks['table6b_countries'] = sorted({r['country'] for r in country_b})
checks['table6b_rows'] = len(country_b)
checks['table1_native_mother_fields'] = [k for k in national[0] if 'nativemom' in k]
checks['table3_race_gender_rows'] = [(r['kid_race'],r['gender'],r['count']) for r in natmom]
checks['country_tables_have_only_income_outcomes'] = not any(
    word in k for row in (country_a[0],country_b[0]) for k in row
    for word in ('jail','marr','employ','crime','college','hs','trust'))
for name in ('changing_opportunity_primary.csv','changing_opportunity_secondary.csv'):
    data = read(name)
    assert sorted(int(r['cohort']) for r in data) == list(range(1978,1993))
    checks[name] = {'rows':len(data), 'columns':len(data[0]),
                    'country_or_nativity_fields':[k for k in data[0] if any(w in k.lower() for w in ('country','origin','native','birthplace'))]}

usa = next(r for r in country_a if r['country']=='USA')
national_by_p = {int(r['par_pctile']):r for r in national}
rows = []
for r in country_a:
    for outcome,sex in (('kir','M'),('kir','F'),('kfr','P')):
        for pct in (25,75):
            stem = f'{outcome}_{sex}_p{pct}'
            estimate = 100*float(r[stem])
            bench = 100*float(usa[stem])
            rows.append(dict(dataset_id='OI_RACE_T6A',country=r['country'],outcome=outcome,sex=sex,
                birth_cohort_start=1978,birth_cohort_end=1983,parent_income_percentile=pct,
                child_observation_years='2014-2015',unit='national_income_percentile',estimate=estimate,
                estimate_se=100*float(r[stem+'_se']),source_sample_count=r[f'n_{outcome}_{sex}'],
                count_scope='rounded_overall_country_outcome_sex_regression_sample_not_p25_cell',
                benchmark_id='OI_T6A_USA_PARENT_ORIGIN',benchmark_estimate=bench,
                same_table_difference=estimate-bench,
                native_white_mother_benchmark_estimate=(national_by_p[pct]['kfr_nativemom_white_pooled'] if outcome=='kfr' else ''),
                native_white_mother_comparability=('context_only_exact_percentile_bin_vs_parametric_prediction;parent_filter_differs' if outcome=='kfr' else 'unavailable_same_endpoint'),
                generation='parent_origin;exact_child_birthplace_filter_unverified',
                source_frame='paper_describes_citizen_or_authorized_child_and_parent_frame',
                established_native_g3plus_comparison='unavailable'))
with (ROOT/'candidate_country_comparisons.csv').open('w',newline='') as f:
    writer = csv.DictWriter(f,fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
checks['candidate_comparison_rows'] = len(rows)
checks['country_comparison_source'] = str(files['race_table6a_parametric.csv'])
(ROOT/'validation.json').write_text(json.dumps(checks,indent=2)+'\n')

schema = {
 'dataset_id':'Source table/version; never merge solely on an outcome label.',
 'country':'Released parent-origin label; not legal status, race, full ancestry or current residence.',
 'outcome':'kir=individual income rank; kfr=household income rank; preserve endpoint.',
 'sex':'M/F/P; pooled household outcomes are separate from sex-specific individual income.',
 'birth_cohort_start/end':'Inclusive child birth years; age-specific modern tables require separate records.',
 'parent_income_percentile':'National parent household income rank, not origin-specific rank.',
 'estimate/estimate_se':'Income percentiles, not dollars; null SE stays null.',
 'source_sample_count':'Disclosure-rounded relevant source count with count_scope; not weighted population.',
 'benchmark_id':'Explicit population and source estimand; USA-parent-origin is not established third-plus white.',
 'same_table_difference':'Descriptive country-minus-USA mean-rank gap only; no causal or fiscal meaning.',
 'native_white_mother_benchmark_estimate':'Household-only contextual native-mother series; do not treat as identical estimator.',
 'generation/source_frame':'Preserve own-birthplace uncertainty and paper-described authorized-family selection.',
 'established_native_g3plus_comparison':'Unavailable in these public OI tables; do not silently substitute.'
}
(ROOT/'candidate_schema.json').write_text(json.dumps(schema,indent=2)+'\n')
cards = ['# Staged dataset register candidates', '', 'Integration owner: root. No repository catalog edited.', '']
codebooks = {
 'race_table1.csv':'race_table1_codebook.pdf',
 'race_table3_nativemom.csv':'race_table3_codebook.pdf',
 'race_table5_income_crosswalk.csv':'race_table5_codebook.pdf',
 'changing_opportunity_primary.csv':'changing_opportunity_primary_codebook.pdf',
 'changing_opportunity_secondary.csv':'changing_opportunity_secondary_codebook.pdf',
 'race_table6a_parametric.csv':'race_table6a_codebook.pdf',
 'race_table6b_nonpar.csv':'race_table6b_codebook.pdf',
}
for name in ('race_table1.csv','race_table3_nativemom.csv','race_table5_income_crosswalk.csv',
             'changing_opportunity_primary.csv','changing_opportunity_secondary.csv',
             'race_table6a_parametric.csv','race_table6b_nonpar.csv'):
    m = next(r for r in manifest if r['name']==name)
    cb = next(r for r in manifest if r['name']==codebooks[name])
    cards.extend([f'### {name}', '**Source:** Opportunity Insights', '**Acquired/checked:** 2026-09-17',
        f"**Local path:** `{m['local_path']}`",f"**Official:** {m['source_url']}",
        f"**Codebook:** `{cb['local_path']}` | {cb['source_url']}",
        f"**Size:** {m['bytes']} bytes; {m['rows']} rows, {m['columns']} fields",
        '**Access:** Public download; no credential or payment used. Redistribution license not separately assessed.',
        '**Coverage and quirks:** See final memo and manifest field inventory; source labels do not establish third-plus ancestry.', ''])
(ROOT/'DATASET_CARDS.md').write_text('\n'.join(cards)+'\n')
print(json.dumps({k:v for k,v in checks.items() if k!='table3_race_gender_rows'},indent=2))
