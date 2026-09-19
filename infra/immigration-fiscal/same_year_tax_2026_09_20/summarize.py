"""Compact derived results for independent checking; no calibration."""
from pathlib import Path
import json
import pandas as pd
from common import sha

p=Path(__file__).parent/'derived'
b=pd.read_csv(p/'irs_bands.csv').query('scope=="civilian" and metric in ["returns","agi","income_tax_after_nonrefundable"]')
b['bracket']=b.band.map(lambda x:'under_100k' if x<11 else '100k_to_200k' if x==11 else '200k_to_500k' if x==12 else '500k_plus')
out=b.groupby(['bracket','metric'],sort=False)[['estimate','irs_value']].sum().reset_index()
out['difference']=out.estimate-out.irs_value
out['raw_pct_difference']=100*(out.estimate/out.irs_value-1)
out.to_csv(p/'irs_bracket_summary.csv',index=False)
(p/'summary_audit.json').write_text(json.dumps({'sources':{f:sha(p/f) for f in ['irs_bands.csv','audit.json']},'implementation':sha(Path(__file__)),'output':sha(p/'irs_bracket_summary.csv')},indent=2)+'\n')
print(out.to_string(index=False))
a=json.loads((p/'audit.json').read_text())
print(json.dumps(a['return_construction'],indent=2))
c=pd.read_csv(p/'cps2023_components.csv').query('scope=="civilian" and region=="US"').pivot(index='group',columns='metric',values='estimate')
print(c[['population','gross_wages','wage_workers','federal_after_refundable','employer_payroll','fica_cps']].to_string())
print(pd.read_csv(p/'government_coverage_ceiling.csv').to_string(index=False))
