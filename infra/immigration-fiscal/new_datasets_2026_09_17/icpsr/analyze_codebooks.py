"""Analyze published codebook marginals only; never impersonate microdata."""
from pathlib import Path
import argparse
import csv
import json
import re

parser = argparse.ArgumentParser()
parser.add_argument('--docs-root', type=Path, default=Path(__file__).resolve().parents[1] / 'derived/icpsr')
args = parser.parse_args()
root = args.docs_root
rows = []

def table(study, variable):
    path = root / f'ICPSR_{study}/DS0001/{study}-0001-Codebook.txt'
    text = path.read_text()
    match = re.search(rf'(?m)^{re.escape(variable)}[ \t]+', text)
    if match is None:
        raise ValueError(f'{variable} not in {path}')
    stop = text.index('Based upon', match.end())
    section = text[match.start():stop]
    counts = {}
    for line in section.splitlines():
        fields = re.split(r'\s{2,}', line.strip())
        if len(fields) >= 3 and re.fullmatch(r'[0-9.]+(?: \(M\))?', fields[0]) and fields[-1].endswith('%'):
            code = fields[0].split()[0]
            count = int(fields[-2].replace(',', ''))
            counts[code] = count
            rows.append({'study': study, 'variable': variable, 'code': code,
                         'label': fields[1] if len(fields)>3 else '', 'n_unweighted': count,
                         'source_line': text[:match.start()].count('\n')+1,
                         'codebook': str(path)})
    if not counts:
        raise ValueError(f'No frequencies parsed for {variable}')
    return counts

ny_arrest = table('30302','ARRESTED')
ny_incarcer = table('30302','INCARCER')
ny_group = table('30302','GROUP')
ny_year = table('30302','YEAR')
lns_support = table('20862','INCSUPP')
lns_birth = table('20862','BORNUS')
lns_ethnic = table('20862','ETHNIC')
lns_parents = table('20862','PARBORN')
lns_grandparents = table('20862','GRANBORN')
assert sum(ny_arrest.values()) == sum(ny_incarcer.values()) == sum(ny_group.values()) == sum(ny_year.values()) == 3415
assert sum(lns_support.values()) == sum(lns_birth.values()) == sum(lns_ethnic.values()) == sum(lns_parents.values()) == sum(lns_grandparents.values()) == 8634

def bound(a,b,n):
    return {'intersection_n_lower': max(0,a+b-n), 'intersection_n_upper': min(a,b),
            'conditional_rate_lower': max(0,a+b-n)/a, 'conditional_rate_upper': min(a,b)/a}

n_support = lns_support['3']+lns_support['4']
result = {
    'analysis_type': 'published unweighted codebook marginals, no respondent microdata',
    'nyc_lifetime_arrest_valid_rate': ny_arrest['1']/(ny_arrest['1']+ny_arrest['2']),
    'nyc_lifetime_detention_valid_rate': ny_incarcer['1']/(ny_incarcer['1']+ny_incarcer['2']),
    'nyc_interview_year_counts': ny_year,
    'lns_income_support_all_sample_rate': n_support/8634,
    'lns_income_support_substantive_response_rate': n_support/(8634-lns_support['5']),
    'lns_income_support_bound_among_mexican_selfid': bound(lns_ethnic['2'],n_support,8634),
    'lns_income_support_bound_among_mainland_us_born': bound(lns_birth['1'],n_support,8634),
    'lns_mainland_us_born_both_us_parents_n_bounds': [max(0,lns_birth['1']+lns_parents['2']-8634),min(lns_birth['1'],lns_parents['2'])],
    'unidentified': ['generation-specific outcome rates','group contrasts','survey-weighted population rates','family/panel/cross-study record linkage']
}
with (root/'codebook_frequency_checks.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
(root/'codebook_analysis.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
