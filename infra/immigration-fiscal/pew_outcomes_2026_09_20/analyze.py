"""Historical Pew ancestry outcome audit; raw inputs remain read-only."""
from pathlib import Path
import hashlib
import json
import numpy as np
import pandas as pd
import pyreadstat

LANE = Path(__file__).resolve().parent
BASE = LANE.parent / 'new_datasets_2026_09_17/derived/pew'
OUT = LANE / 'derived'
OUT.mkdir(exist_ok=True)
SPECS = [
    ('Identifiers', 'Pew-Research-Center_2015-National-Survey-of-Latinos-Dataset', 'NSL2015_FOR RELEASE.sav', 'weights', 37.8, '5d4ef87d19dd93b1b1fd7f9661fa96dd526d62de1e0b933c0cd28df2ea808136'),
    ('Nonidentifiers', 'Pew-Research-Center_2016-Survey-of-Self-Identified-non-Hispanics-Dataset', 'NSL2015 Omnibus_FOR RELEASE.sav', 'OMNIWeight', 4.9, '74e0d106b94ced44123fcdec9fb7b11d953cec791e2bf8d61d7a65df7f16f293'),
]
frames, audit, rows = [], [], []
for source, folder, name, weight, mass, expected_hash in SPECS:
    p = BASE / folder / name
    actual_hash = hashlib.sha256(p.read_bytes()).hexdigest()
    assert actual_hash == expected_hash
    d, m = pyreadstat.read_sav(p, user_missing=True)
    assert m.variable_value_labels['q3_combo'][1] == 'Mexican'
    assert d[weight].gt(0).all() and np.isfinite(d[weight]).all()
    d['source'] = source
    d['weight'] = d[weight]
    # Normalize FULL source before origin selection. Published population masses
    # are historical external calibration, not a new estimate of prevalence.
    d['calibrated_weight'] = mass * d[weight] / d[weight].sum()
    age = d.age.where(d.age.between(18, 97))
    d['valid_age'] = age
    d['age_band'] = np.select([age.between(18,29), age.between(30,49), age.between(50,64), age.ge(65)], ['18-29','30-49','50-64','65+'], default='Unknown')
    for code, band in [(1,'18-29'),(2,'30-49'),(3,'50-64'),(4,'65+')]:
        d.loc[age.isna() & d.age2.eq(code), 'age_band'] = band
    own_parents = d.q4.eq(2) & d.q7.eq(2) & d.q8.eq(2)
    gps = d[['q8aa','q8ab','q8ba','q8bb']]
    d['generation'] = np.select([d.q4.isin([1,3]), d.q4.eq(2) & (d.q7.isin([1,3]) | d.q8.isin([1,3])), own_parents & gps.isin([1,3]).any(axis=1), own_parents & gps.eq(2).all(axis=1)], ['G1','G2','G3','G4plus'], default='Unresolved')
    d['ba_plus'] = d.educ.isin([6,7,8]).astype(float).where(d.educ.between(1,8))
    d['no_hs'] = d.educ.isin([1,2]).astype(float).where(d.educ.between(1,8))
    audit.append({'source':source,'source_n':len(d),'mexican_n':int(d.q3_combo.eq(1).sum()),'hash':actual_hash,'historical_calibration_millions':mass,'income_wording':m.column_names_to_labels['income'],'education_labels':m.variable_value_labels['educ'],'missing_income_n':int(d.loc[d.q3_combo.eq(1),'income'].isin([98,99]).sum())})
    frames.append(d.loc[d.q3_combo.eq(1)].copy())

all_d = pd.concat(frames, ignore_index=True)
for source in ['Identifiers','Nonidentifiers','Historical_calibrated_pool']:
    d = all_d if source == 'Historical_calibrated_pool' else all_d[all_d.source.eq(source)]
    weight = 'calibrated_weight' if source == 'Historical_calibrated_pool' else 'weight'
    groups = {'All_adults': np.ones(len(d),dtype=bool), 'US_born':d.q4.eq(2), 'US_born_25plus':d.q4.eq(2)&d.valid_age.ge(25),'US_born_USparents':d.q4.eq(2)&d.q7.eq(2)&d.q8.eq(2), 'G3':d.generation.eq('G3'),'G4plus':d.generation.eq('G4plus')}
    for group, mask in groups.items():
        z=d.loc[mask]
        # Income wording differs across surveys: do not pool these outcomes.
        for outcome in ['ba_plus','no_hs','valid_age']:
            v=z[outcome].notna()
            value=np.average(z.loc[v,outcome],weights=z.loc[v,weight]) if v.any() else np.nan
            rows.append({'source':source,'group':group,'outcome':outcome,'n_total':len(z),'n_valid':int(v.sum()),'n_missing':int((~v).sum()),'estimate':value if outcome=='valid_age' else 100*value,'weighted_missing_pct':100*z.loc[~v,weight].sum()/z[weight].sum() if len(z) else np.nan,'kish_n_valid':z.loc[v,weight].sum()**2/(z.loc[v,weight]**2).sum() if v.any() else 0,'nonidentifier_weight_pct':100*z.loc[z.source.eq('Nonidentifiers'),weight].sum()/z[weight].sum() if len(z) else np.nan})
        for band in ['18-29','30-49','50-64','65+','Unknown']:
            rows.append({'source':source,'group':group,'outcome':'age_'+band,'n_total':len(z),'n_valid':int(z.age_band.eq(band).sum()),'estimate':100*z.loc[z.age_band.eq(band),weight].sum()/z[weight].sum() if len(z) else np.nan})
result=pd.DataFrame(rows)
result.to_csv(OUT / 'outcomes.csv',index=False)
(OUT / 'audit.json').write_text(json.dumps(audit,indent=2))
assert len(all_d)==883
assert len(all_d[all_d.source.eq('Nonidentifiers')])==52
print(result[result.outcome.isin(['ba_plus','no_hs','valid_age'])].round(3).to_string(index=False))
