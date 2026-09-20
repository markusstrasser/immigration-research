"""Historical generation age comparators; no imputation or cross-source pooling."""
from pathlib import Path
import json
import hashlib
import re
import numpy as np
import pandas as pd
import pyreadstat

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / 'infra/immigration-fiscal/new_datasets_2026_09_17/derived'
OUT = Path(__file__).resolve().parent/'derived/historical'
OUT.mkdir(parents=True, exist_ok=True)
ORDER = ['G3', 'G4plus', 'Unresolved']
BANDS = ['18-24', '25-44', '45-64', '65+', 'Age_unresolved']
SPECS = [
    ('Pew2015_identifiers', 'Pew-Research-Center_2015-National-Survey-of-Latinos-Dataset', 'NSL2015_FOR RELEASE.sav', 'weights'),
    ('Pew2015_16_nonidentifiers', 'Pew-Research-Center_2016-Survey-of-Self-Identified-non-Hispanics-Dataset', 'NSL2015 Omnibus_FOR RELEASE.sav', 'OMNIWeight'),
]
HASHES = {'Pew2015_identifiers': '5d4ef87d19dd93b1b1fd7f9661fa96dd526d62de1e0b933c0cd28df2ea808136',
          'Pew2015_16_nonidentifiers': '74e0d106b94ced44123fcdec9fb7b11d953cec791e2bf8d61d7a65df7f16f293'}
manifest = {'sources': [], 'limitations': ['No cross-source pooling', 'No imputation', 'No design-correct standard errors claimed', 'Pew generic nativity treats Puerto Rico as foreign; origin q3_combo==1 excludes unspecified mixed origins']}
rows = []
audit_rows = []

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def summarize(d, source, scope, group='age_band'):
    groups = [('All', d)] + [(band, d[d[group].eq(band)]) for band in BANDS]
    for band, z in groups:
        denom = float(z.weight.sum())
        for generation in ORDER:
            v = z[z.generation.eq(generation)]
            rows.append({'source': source, 'scope': scope, 'age_band': band, 'generation': generation,
                         'n': len(v), 'denominator_n': len(z), 'weight_mass': float(v.weight.sum()),
                         'denominator_weight': denom, 'percent': 100*v.weight.sum()/denom if denom else None,
                         'kish_n_denominator': denom**2/z.weight.pow(2).sum() if denom else 0})
        assert len(z[z.generation.isin(ORDER)]) == len(z)

for source, folder, filename, weight in SPECS:
    path = BASE / 'pew' / folder / filename
    assert sha(path) == HASHES[source], 'Pew source hash changed'
    d, m = pyreadstat.read_sav(path, user_missing=True)
    assert d[weight].gt(0).all() and np.isfinite(d[weight]).all()
    assert m.variable_value_labels['q3_combo'][1] == 'Mexican'
    d['weight'] = d[weight]
    native_parents = d.q4.eq(2) & d.q7.eq(2) & d.q8.eq(2)
    gps = d[['q8aa', 'q8ab', 'q8ba', 'q8bb']]
    d['generation'] = np.select([gps.isin([1, 3]).any(axis=1), gps.eq(2).all(axis=1)], ORDER[:2], default=ORDER[2])
    age = d.age.where(d.age.between(18, 97))
    d['age_band'] = np.select([age.between(18,24), age.between(25,44), age.between(45,64), age.ge(65)], BANDS[:4], default=BANDS[4])
    # Only fallback intervals completely contained in a requested target band can resolve age.
    d.loc[age.isna() & d.age2.eq(3), 'age_band'] = '45-64'
    d.loc[age.isna() & d.age2.eq(4), 'age_band'] = '65+'
    mex = d.q3_combo.eq(1)
    target = d[mex & native_parents].copy()
    summarize(target, source, 'Mexican_reported_origin_native_two_native_parents')
    for origin, mask in [('Mexican', mex), ('Mixed_unspecified', d.q3_combo.eq(9)), ('Origin_unknown', d.q3_combo.isin([98,99]) | d.q3_combo.isna()), ('Other_origin', ~d.q3_combo.isin([1,9,98,99]) & d.q3_combo.notna())]:
        z=d[mask & native_parents]
        audit_rows.append({'source':source,'origin':origin,'all_origin_n':int(mask.sum()),'native_two_native_parents_n':len(z),'weight_mass_native_two_native_parents':float(z.weight.sum()),'exact_age_missing_n':int(z.age.isin([98,99]).sum()+z.age.isna().sum()),'requested_age_band_unresolved_n':int(z.age_band.eq('Age_unresolved').sum()),'sex_missing_n':int((~z.sex.isin([1,2])).sum())})
    candidates = [k for k in m.column_names if re.search(r'(^|_)(psu|strat|stratum|cluster|repw|brr|samp30|samp31)(_|$)', k, re.I) or re.search(r'weight|stratum|primary sampling|replicate', str(m.column_names_to_labels[k]), re.I)]
    selected = ['caseid','q3_combo','q4','q7','q8','q8aa','q8ab','q8ba','q8bb','age','age2','age_combo','sex',weight]+candidates
    metadata = {k:{'label':m.column_names_to_labels[k],'values':m.variable_value_labels.get(k),'observed_nonmissing_n':int(d[k].notna().sum())} for k in dict.fromkeys(selected) if k in d}
    manifest['sources'].append({'source':source,'path':str(path),'sha256':sha(path),'full_n':len(d),'target_n':len(target),'variables':metadata,'all_columns':list(m.column_names)})

family_path=BASE/'nlsy_family/family_analysis_rows.csv'
base_path=BASE/'nlsy/full_selected_data.csv'
assert sha(family_path)=='8372ae35fe32bd97d8a17ca40d11f6c9b158cb32f1499c7e2f5fb5df13e837a6'
assert sha(base_path)=='8e684c96d86bc97af92d65b9ea8c58438f5a54a535ed97988dc582b66b8d59d6'
family=pd.read_csv(family_path)
base=pd.read_csv(base_path)
assert family.R0000100.is_unique and base.R0000100.is_unique
d=family.merge(base[['R0000100','R0536402','R0536300','U6365400']],on='R0000100',how='left',validate='one_to_one',indicator=True)
assert d._merge.eq('both').all()
assert np.allclose(d.weight,d.U6365400/100)
assert d.sex.eq(d.R0536300.map({1:'Men',2:'Women'})).all()
target=d[d.identity.eq('Mexican_Chicano_self_ID')&d.weight.gt(0)&d.own_us.eq(1)&d.mother_us.eq(1)&d.father_us.eq(1)].copy()
assert target.R0536402.between(1980,1984).all()
target['generation']=target.linked_exact.map({'G3_USborn_USparents_foreign_grandparent':'G3','G4plus_USborn_USparents_all_four_USgrandparents':'G4plus','USborn_USparents_grandparents_unresolved':'Unresolved'})
assert target.generation.notna().all()
target['age_band']='25-44'
summarize(target,'NLSY97_R21_retained_1980_1984','Mexican_Chicano_ID_native_two_native_biological_parents')
cohort_rows=[]
for by,z in target.groupby('R0536402'):
    for generation in ORDER:
        v=z[z.generation.eq(generation)]
        cohort_rows.append({'birth_year':int(by),'generation':generation,'n':len(v),'denominator_n':len(z),'weight_mass':float(v.weight.sum()),'denominator_weight':float(z.weight.sum()),'percent':100*v.weight.sum()/z.weight.sum()})
pd.DataFrame(cohort_rows).to_csv(OUT/'nlsy_birth_cohort.csv',index=False)
audit_rows.append({'source':'NLSY97_R21_retained_1980_1984','origin':'Mexican_Chicano_ID','all_origin_n':int((d.identity.eq('Mexican_Chicano_self_ID')&d.weight.gt(0)).sum()),'native_two_native_parents_n':len(target),'weight_mass_native_two_native_parents':float(target.weight.sum()),'exact_age_missing_n':0,'requested_age_band_unresolved_n':0,'sex_missing_n':int(target.sex.isna().sum())})
audit_rows.append({'source':'NLSY97_R21_retained_1980_1984','origin':'Self_ID_unobserved','all_origin_n':int((d.identity.eq('Self_ID_unobserved')&d.weight.gt(0)).sum()),'native_two_native_parents_n':int((d.identity.eq('Self_ID_unobserved')&d.weight.gt(0)&d.own_us.eq(1)&d.mother_us.eq(1)&d.father_us.eq(1)).sum())})
manifest['sources'].append({'source':'NLSY97_R21_retained_1980_1984','family_path':str(family_path),'family_sha256':sha(family_path),'base_path':str(base_path),'base_sha256':sha(base_path),'target_n':len(target),'target_birth_years':sorted(target.R0536402.unique().tolist()),'design_fields_in_base':[k for k in base if re.search(r'psu|strat|replic|weight',k,re.I)],'weight':'U6365400/100 round21','birth_year':'R0536402','sex':'R0536300','family_and_base_join':'unique R0000100, all match, sex and weight agree','age_note':'All births1980-84 are25-44 during2016-24; approximate GSS birthyear=year-age has birthday boundary uncertainty. This is not cross-sectional age evidence.'})
pd.DataFrame(rows).to_csv(OUT/'generation_age_comparators.csv',index=False)
pd.DataFrame(audit_rows).to_csv(OUT/'ancestry_age_audit.csv',index=False)
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2))
print(pd.DataFrame(rows).query('denominator_n>0')[['source','age_band','generation','n','denominator_n','percent']].round(3).to_string(index=False))
print(pd.DataFrame(audit_rows).to_string(index=False))
