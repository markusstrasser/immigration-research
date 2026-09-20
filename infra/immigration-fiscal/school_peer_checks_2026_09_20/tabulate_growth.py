"""Recalculate primary-report school counts; no causal attribution.

Run: UV_CACHE_DIR=/private/tmp/codex-uv-cache uv run --no-project python3 tabulate_growth.py
Inputs below are manually transcribed official tables, with URLs/locators.
Recent immigrant = age 3-21, born outside states/DC/PR, <=3 school years
in the United States. Category entries/exits are not a new-arrivals series.
"""
import csv
import hashlib
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent / 'derived' / 'state_growth'
OUT.mkdir(parents=True, exist_ok=True)
TEA = 'https://tea.texas.gov/data-reports/school-performance/accountability-research/enroll-2023-24-0.pdf'
CDE = 'https://www.cde.ca.gov/sp/ml/t3immdemgraphics.asp'
CA_ENROLL = 'https://www.cde.ca.gov/ds/ad/cefenrollmentcomp.asp'
CA_OLDER = 'https://www.cde.ca.gov/Sp/ps/cefprivinstr.asp'
STAFF = 'https://rptsvr1.tea.texas.gov/cgi/sas/broker?_debug=0&_program=perfrept.perfmast.sas&_service=marykay&ccyy={year}&id=S&lev=S&prgopt=reports%2Ftapr%2Fstaff.sas'

def write_csv(name, rows):
    fields = list(dict.fromkeys(k for r in rows for k in r))
    with (OUT / name).open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

# TX: report Tables 2 and 14, printed pp6/27; CA: Table I and enrollment.
raw = [
    ('TX','2013-14',5151925,72085,900476,None),
    ('TX','2018-19',5431910,107133,1055172,None),
    ('TX','2022-23',5518432,122504,1270533,None),
    ('TX','2023-24',5531236,158832,1345917,None),
    ('CA','2018-19',6186278,176976,None,None),
    ('CA','2019-20',6163001,177476,None,None),
    ('CA','2020-21',6002523,151920,None,None),
    ('CA','2021-22',5892240,144994,None,None),
    ('CA','2022-23',5852544,165293,None,None),
    ('CA','2023-24',5837690,189634,None,151491),
    ('CA','2024-25',5806221,236958,None,177570),
    ('CA','2025-26',5731260,228780,None,213313),
]
rows = [dict(state=s,school_year=y,total_enrollment=n,recent_immigrant_program=i,
             english_learner_or_emergent_bilingual=e,transitional_kindergarten=tk,
             residual_total_minus_recent_immigrant=n-i,
             immigrant_share_percent=100*i/n,
             total_source=TEA if s=='TX' else CA_ENROLL if y>='2023-24' else CA_OLDER,
             immigrant_source=TEA if s=='TX' else CDE)
        for s,y,n,i,e,tk in raw]
write_csv('enrollment_observed.csv',rows)
lookup={(r['state'],r['school_year']):r for r in rows}
comparisons=[('TX','2013-14','2023-24'),('TX','2018-19','2023-24'),
             ('TX','2022-23','2023-24'),('CA','2018-19','2024-25'),
             ('CA','2023-24','2024-25'),('CA','2024-25','2025-26')]
changes=[]
for s,y0,y1 in comparisons:
    a,b=lookup[(s,y0)],lookup[(s,y1)]
    for field in ['total_enrollment','recent_immigrant_program',
                  'residual_total_minus_recent_immigrant','english_learner_or_emergent_bilingual']:
        if a[field] is not None and b[field] is not None:
            changes.append(dict(state=s,start=y0,end=y1,measure=field,
                baseline=a[field],endpoint=b[field],change=b[field]-a[field],
                percent_change=100*(b[field]/a[field]-1)))
write_csv('enrollment_changes.csv',changes)

staff_values=[('2018-19',719502.5,358450.1,72848.5,21812.7,8268.8,74292.4,183830.1),
              ('2023-24',775882.5,374799.9,86026.7,25836.1,9488.3,88200.6,191530.9)]
staff=[]
for y,total,teach,supp,camp,cent,aides,aux in staff_values:
    n=lookup[('TX',y)]['total_enrollment']
    staff.append(dict(state='TX',school_year=y,total_staff_FTE=total,teacher_FTE=teach,
        professional_support_FTE=supp,campus_admin_FTE=camp,central_admin_FTE=cent,
        educational_aides_FTE=aides,auxiliary_staff_FTE=aux,
        calculated_pupils_per_teacher_FTE=n/teach,
        source=STAFF.format(year=2000+int(y[-2:]))))
write_csv('texas_staff.csv',staff)
staff_changes=[]
for k in ['total_staff_FTE','teacher_FTE','professional_support_FTE','campus_admin_FTE',
          'central_admin_FTE','educational_aides_FTE','auxiliary_staff_FTE',
          'calculated_pupils_per_teacher_FTE']:
    a,b=staff[0][k],staff[1][k]
    staff_changes.append(dict(measure=k,baseline=a,endpoint=b,change=b-a,percent_change=100*(b/a-1)))
write_csv('texas_staff_changes.csv',staff_changes)

# CDE Table II. Award-year funding uses previous fall's enrollment, public+
# private eligible pupils in funded LEAs. These are NOT total school costs.
grants=[('2018-19',115646,98.35,11373797),('2019-20',88423,100.42,8879426),
        ('2020-21',73318,110.95,8134632),('2021-22',22407,157.20,3522370),
        ('2022-23',24335,150.85,3670866),('2023-24',97738,126.05,12319877),
        ('2024-25',139513,125.90,17564695),('2025-26',187286,93.00,17417598)]
write_csv('california_title_iii_immigrant_grants.csv',[
    dict(funding_year=y,eligible_prior_fall_pupils=n,reported_dollars_per_pupil=p,
         total_nominal_dollars=d,source=CDE) for y,n,p,d in grants])

manifest = dict(retrieved='2026-09-20',method='Manual transcription of primary official tables, arithmetic by this script',
    source_urls=[TEA,CDE,CA_ENROLL,CA_OLDER,STAFF.format(year=2019),STAFF.format(year=2024)],
    local_files=[])
for p in sorted(OUT.iterdir()):
    if p.is_file() and p.name not in ['manifest.json','RESULT.md','run.log']:
        manifest['local_files'].append(dict(file=p.name,bytes=p.stat().st_size,
            sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
for r in changes:
    if r['measure'] in ['total_enrollment','recent_immigrant_program','residual_total_minus_recent_immigrant']:
        print(r)
print('Staff changes:',staff_changes)
