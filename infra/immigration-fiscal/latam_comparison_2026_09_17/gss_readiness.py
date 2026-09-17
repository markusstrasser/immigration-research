from pathlib import Path
import json, re
import pyreadstat
p = Path('/Users/alien/Projects/immigration-research/infra/immigration-fiscal/attitudes_gen_2026_09_16/raw/GSS_stata/gss7224_r3a.dta')
_, m = pyreadstat.read_dta(str(p), metadataonly=True, encoding='latin1')
names = [n for n in m.column_names if re.search(r'ethnic|hispanic|born|trust', n)]
out = {'source': str(p), 'variables': {n:m.column_names_to_labels[n] for n in names}, 'value_labels': {n:m.value_labels.get(m.variable_to_label.get(n,''),{}) for n in names}}
cols = [n for n in ['year','ethnic','ethnic2','ethnic3','hispanic','hispanic_0022','born','parborn','granborn','trust'] if n in m.column_names]
d,_ = pyreadstat.read_dta(str(p), usecols=cols, encoding='latin1')
out['counts'] = {n:d[n].value_counts(dropna=False).to_dict() for n in cols if n != 'year'}
out['trust_by_ethnic'] = d.loc[d['trust'].isin([1,2,3])].groupby('ethnic').size().to_dict()
import pandas as pd
d['generation'] = 'unknown'
d.loc[d.born.eq(2), 'generation'] = 'G1'
d.loc[d.born.eq(1) & d.parborn.isin([1,2,4,6,8]), 'generation'] = 'G2'
d.loc[d.born.eq(1) & d.parborn.eq(0), 'generation'] = 'G3plus'
q = d.loc[d.trust.isin([1,2,3]) & d.hispanic_0022.notna()]
out['trust_hispanic0022_by_generation'] = q.groupby(['hispanic_0022','generation']).size().unstack(fill_value=0).to_dict(orient='index')
out['detailed_origin_trust_years'] = sorted(q.year.unique().tolist())
out['benchmark_counts'] = {
    'nonhisp_G3plus_TRUST': int((q.hispanic_0022.eq(1) & q.generation.eq('G3plus')).sum()),
    'nonhisp_USborn_bothparentsUS_allgrandparentsUS_TRUST': int((q.hispanic_0022.eq(1) & q.generation.eq('G3plus') & q.granborn.eq(0)).sum()),
}
destination = Path(__file__).resolve().parent / 'derived'
destination.mkdir(parents=True, exist_ok=True)
(destination/'gss-readiness.json').write_text(json.dumps(out,indent=2,default=str))
print(json.dumps({k:out[k] for k in ['detailed_origin_trust_years','benchmark_counts']},indent=2))
