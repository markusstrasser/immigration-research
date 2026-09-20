from pathlib import Path
import json
import math
from collections import Counter
import pyreadstat
import pandas as pd

LANE = Path(__file__).resolve().parent
src = LANE / 'raw/masp_combined.dta'
data, meta = pyreadstat.read_dta(src)
children = data.loc[data['v3'].notna()]
results = {'raw_shape': list(data.shape), 'children': len(children),
           'family_count': int(children['id'].nunique()), 'unique_pair': not children[['v3', 'prefix']].duplicated().any(),
           'prefix': children['prefix'].value_counts().to_dict(),
           'identity_values': {f'v{k}': sorted(children[f'v{k}'].dropna().unique().tolist()) for k in range(12, 24)},
           'informant_labels': {k: meta.variable_value_labels.get(k) for k in ['v75_I','v87_I','v91_I']}}
rows = []
def country(x):
    return x if x in (1,2,3) else None
def reverse_country(x):
    return {1:2,2:1,3:3}.get(x)
for _, r in children.iterrows():
    mentions = [k for k in range(12,24) if r[f'v{k}'] in (1,2,3,4,5,6)]
    latin = any(k in range(14,21) for k in mentions)
    only_american = bool(mentions) and all(k in (12,13) for k in mentions)
    group = 'Any_Mexican_Latino_Spanish' if latin else ('Only_Anglo_American' if only_american else 'Other_or_unresolved')
    closest = (mentions[0]-11) if len(mentions)==1 and r.v24==2 else (r.v25 if r.v24==1 and r.v25 in range(1,11) else None)
    preferred = ('Anglo_or_American' if closest in (1,2) else 'Hispanic_Latino_Spanish' if closest in (3,4,9)
                 else 'Mexican_Chicano' if closest in (5,6,7,8) else 'Other_or_unresolved')
    own, p1, p2 = country(r.v75), country(r.v75_O2), country(r.c19)
    gps = [country(r.v87_O2),country(r.v91_O2),reverse_country(r.c28),reverse_country(r.c29)]
    if own == 2: generation='G1_Mexico'
    elif own == 3: generation='G1_other'
    elif own == 1 and (p1 in (2,3) or p2 in (2,3)): generation='G2'
    elif own == p1 == p2 == 1 and any(x in (2,3) for x in gps): generation='G3'
    elif own == p1 == p2 == 1 and all(x == 1 for x in gps): generation='G4plus'
    else: generation='Unresolved'
    benefits = [r.v338,r.v340,r.v341]
    any_benefit = 1 if 1 in benefits else (0 if all(x==2 for x in benefits) else None)
    rows.append({'any_mention_identity':group,'preferred_identity':preferred,'generation':generation,
                 'G3_MexGP':generation=='G3' and 2 in gps,
                 'G4_MexGreatGP':generation=='G4plus' and any(r[f'v{k}_O2']==1 for k in range(98,102)),
                 'ba_plus':int(r.v140 in (5,6,7)) if r.v140 in range(0,8) else None,
                 'income_under30k':int(r.v348 in range(1,8)) if r.v348 in range(1,22) else None,
                 'any_three_benefits':any_benefit,
                 'white_race_with_latin_mention':r.v51==1 and latin})
results['generations'] = dict(Counter(r['generation'] for r in rows))
results['G3_MexGP'] = sum(r['G3_MexGP'] for r in rows)
results['G4_MexGreatGP'] = sum(r['G4_MexGreatGP'] for r in rows)
results['white_race_with_latin_mention'] = sum(r['white_race_with_latin_mention'] for r in rows)
results['outcomes'] = []
for scheme in ('any_mention_identity','preferred_identity'):
    for name in ['All'] + sorted(set(r[scheme] for r in rows)):
        subgroup = [r for r in rows if name=='All' or r[scheme]==name]
        for outcome in ('ba_plus','income_under30k','any_three_benefits'):
            vals = [r[outcome] for r in subgroup if r[outcome] is not None]
            results['outcomes'].append({'scheme':scheme,'identity':name,'outcome':outcome,'n_total':len(subgroup),
                                        'n_valid':len(vals),'events':sum(vals),'estimate':sum(vals)/len(vals)*100})
export = pd.read_csv(LANE / 'derived/lineage-outcomes.csv')
checked = 0
for row in results['outcomes']:
    found = export[(export.scope == 'all_children') & (export['sample'] == 'endpoint')
                   & (export.scheme == row['scheme']) & (export.identity == row['identity'])
                   & (export.outcome == row['outcome'])]
    assert len(found) == 1, row
    for field in ('n_total', 'n_valid', 'events', 'estimate'):
        assert math.isclose(float(found.iloc[0][field]), row[field], abs_tol=1e-10), (row, field)
        checked += 1
primary = json.loads((LANE / 'derived/lineage-audit.json').read_text())
assert primary['parent_source'] == 'O2_only'
assert primary['generation_counts'] == results['generations']
assert primary['confirmed_mex_G3'] == results['G3_MexGP']
assert primary['confirmed_mex_G4_from_one_branch'] == results['G4_MexGreatGP']
assert checked == 108
(LANE / 'derived/verification.json').write_text(json.dumps(results,indent=2,default=lambda x:x.item()))
print(f'PASS: {checked} independent count/event/rate checks and principal generation counts')
