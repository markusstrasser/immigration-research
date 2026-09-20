"""Calendar sensitivity restricted to units whose valid dates are all June30."""
from pathlib import Path
import json
import pandas as pd
ROOT=Path(__file__).parent / 'work'
df=pd.read_csv(ROOT/'scm-source-year-panel.csv',dtype={'ID':str,'FYEndDate':str})
dates=df.FYEndDate.str.zfill(4)
valid=dates.str.match(r'^(0[1-9]|1[012])([012][0-9]|3[01])$',na=False)
sets=df.assign(date=dates)[valid].groupby('ID').date.agg(set)
ids={u for u,s in sets.items() if s=={'0630'}}
if '105013001' not in ids:
    raise ValueError('Treated school district fails calendar restriction')
sub=df[df.ID.isin(ids)].copy()
sub.to_csv(ROOT/'scm-june-only-panel.csv',index=False)
review={'fiscal_year_mapping_verified':True,'explicit_survey_year_diagnostic':False,
        'analysis_calendar':'Year4 for June30 school fiscal years',
        'source':'Census2006 Classification Manual section3.2: survey Y includes fiscal endings July1(Y-1) to June30(Y)',
        'source_url':'https://www2.census.gov/programs-surveys/govs/about/2006_classification_manual.pdf',
        'restriction':'Include only units whose every valid source FYEndDate in1967-92 equals0630; no interpolation for units with any differing observed date',
        'remaining_assumption':'Unrecorded end dates do not conceal temporary fiscal-calendar changes; inference remains conditional on synthetic-control validity',
        'n_units':len(ids),'excluded_calendar_units':sorted(set(df.ID)-ids)}
(ROOT/'timing-review-june.json').write_text(json.dumps(review,indent=2)+'\n')
print('June30-only units',len(ids))
