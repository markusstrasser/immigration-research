"""Explicit source-year diagnostic until historical fiscal calendar is verified."""
from pathlib import Path
import json
import pandas as pd
ROOT=Path(__file__).parent / 'work'
df=pd.read_csv(ROOT/'schools-1967-1992-raw-selected.csv',dtype=str)
base=df[df.Year4.eq('1980') & (pd.to_numeric(df.Enrollment,errors='coerce')>50000)].copy()
# College names are explicit institutional types, not ethnic/name classification.
colleges={'55019061','55030031','55042701','145016801'}
spillovers={'105006001','105050001'}
treated='105013001'
exclusions=[]
for unit in base.itertuples():
    reason='community college' if unit.ID in colleges else 'south Florida spillover' if unit.ID in spillovers else 'treated' if unit.ID==treated else ''
    if reason: exclusions.append({'ID':unit.ID,'Name':unit.Name,'reason':reason})
eligible=set(base.ID)-colleges-spillovers-{treated}
selected=df[df.ID.isin(eligible|{treated})].copy()
selected['fiscal_year']=pd.to_numeric(selected.Year4)
selected['donor_eligible']=selected.ID.isin(eligible).astype(int)
selected.to_csv(ROOT/'scm-source-year-panel.csv',index=False)
published=selected[~selected.ID.eq('485017017')].copy()
published.to_csv(ROOT/'scm-published-pool-panel.csv',index=False)
exclusions.append({'ID':'485017017','Name':'SEATTLE SCH DIST 1','reason':'absent from published TableA1; excluded only in published-pool sensitivity, retained in independent main pool'})
(ROOT/'donor-exclusions.json').write_text(json.dumps(exclusions,indent=2)+'\n')
review={'fiscal_year_mapping_verified':False,'explicit_survey_year_diagnostic':True,
        'analysis_calendar':'GFD Year4, officially labeled four-digit survey year; stored fiscal_year column is provisional',
        'verified_anchor':'Miami1979 revenue493.310M and spending490.546M match StClair Table1 rounded values',
        'unresolved':'Unit-specific survey-to-fiscal realignment in author analysis not reproduced; do not call this exact published or definitive causal replication',
        'source_codebook':'official INDFID Historical Database User Guide, Variables rows123-124; YearofData DD means provided not imputed, BB blank, II imputed',
        'decision':'Run a transparently conditional reconstruction; preserve the unresolved calendar and compare with later verified alignment.'}
(ROOT/'timing-review.json').write_text(json.dumps(review,indent=2)+'\n')
print('candidates',len(eligible),'source-year rows',len(selected),'published pool candidates',len(eligible)-1)
