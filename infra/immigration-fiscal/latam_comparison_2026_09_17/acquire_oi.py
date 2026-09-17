from pathlib import Path
import concurrent.futures, csv, datetime, hashlib, io, json, subprocess

ROOT = Path(__file__).resolve().parent / '_cache/oi'
ROOT.mkdir(parents=True, exist_ok=True)
BASE = 'https://opportunityinsights.org/wp-content/uploads/'
SOURCES = {
 'race_table1.csv': BASE+'2018/04/table_1.csv',
 'race_table1_codebook.pdf': BASE+'2018/04/table_1.pdf',
 'race_table3_nativemom.csv': BASE+'2018/04/table_3-2.csv',
 'race_table3_codebook.pdf': BASE+'2018/04/table_3.pdf',
 'race_table5_income_crosswalk.csv': BASE+'2018/04/table_5.csv',
 'race_table5_codebook.pdf': BASE+'2018/04/table_5.pdf',
 'race_table6a_codebook.pdf': BASE+'2019/08/Table6a.pdf',
 'race_table6b_codebook.pdf': BASE+'2019/08/Table6b.pdf',
 'changing_opportunity_primary.csv': BASE+'2024/07/Table_5_national_estimates_by_cohort_primary_outcomes.csv',
 'changing_opportunity_primary_codebook.pdf': BASE+'2024/07/ChangingOpportunity_Codebook_Table_5_National_Estimates_by_Cohort_Primary.pdf',
 'changing_opportunity_secondary.csv': BASE+'2024/07/Table_6_national_estimates_by_cohort_secondary_outcomes.csv',
 'changing_opportunity_secondary_codebook.pdf': BASE+'2024/07/ChangingOpportunity_Codebook_Table_6_National_Estimates_by_Cohort_Secondary.pdf',
 'official_data_library.html': 'https://opportunityinsights.org/data/',
}
HELD = {
 'race_table6a_parametric.csv': (BASE+'2019/08/race_table6a_parametric.csv', '/Users/alien/Projects/immigration-research/infra/immigration-fiscal/oi_origin_regression_2026_09_16/race_table6a_parametric.csv'),
 'race_table6b_nonpar.csv': (BASE+'2019/08/race_table6b_nonpar.csv', '/Users/alien/Projects/immigration-research/infra/immigration-fiscal/oi_origin_regression_2026_09_16/race_table6b_nonpar.csv'),
 'race_paper.pdf': (BASE+'2018/04/race_paper.pdf', '/Users/alien/Projects/immigration-research/infra/immigration-fiscal/oi_parental_income_2026_09_16/_cache/race_paper.pdf'),
}
LIMIT = 10_000_000
STAMP = datetime.datetime.now(datetime.timezone.utc).isoformat()

def metadata(name, url, path, status, headers=None):
    body = path.read_bytes()
    d = dict(name=name, source_url=url, local_path=str(path), status=status,
             bytes=len(body), sha256=hashlib.sha256(body).hexdigest(), checked_at=STAMP)
    if headers:
        d['http_headers'] = dict(headers)
    if name.endswith('.csv'):
        rows = list(csv.reader(io.StringIO(body.decode('utf-8-sig'))))
        if not rows or len(rows[0]) < 2 or '<html' in body[:200].decode(errors='ignore').lower():
            raise ValueError(f'{name}: not a tabular CSV')
        d.update(rows=len(rows)-1, columns=len(rows[0]), fields=rows[0])
    elif name.endswith('.pdf') and not body.startswith(b'%PDF'):
        raise ValueError(f'{name}: not a PDF')
    return d

def acquire(item):
    name, url = item
    dest = ROOT/name
    if dest.exists():
        return metadata(name, url, dest, 'already_staged')
    head = subprocess.run(['curl','-fsSIL','--max-time','30',url],check=True,capture_output=True)
    head_headers = dict(line.split(': ',1) for line in head.stdout.decode().splitlines() if ': ' in line)
    length = head_headers.get('content-length',head_headers.get('Content-Length'))
    if length and int(length) > LIMIT:
        raise ValueError(f'{name}: preflight exceeds 10 MB: {length}')
    body = subprocess.run(['curl','-fsSL','--max-time','40','--max-filesize',str(LIMIT),url],
                          check=True,capture_output=True).stdout
    if len(body) > LIMIT:
        raise ValueError(f'{name}: streaming size guard exceeded 10 MB')
    partial = dest.with_suffix(dest.suffix+'.part')
    partial.write_bytes(body)
    d = metadata(name, url, partial, 'acquired', head_headers)
    partial.replace(dest)
    d['local_path'] = str(dest)
    if name.endswith('.pdf'):
        subprocess.run(['pdftotext','-layout',str(dest),str(dest.with_suffix('.txt'))],check=True)
    return d

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
    pending = {pool.submit(acquire,item):item[0] for item in SOURCES.items()}
    records, errors = [], []
    for result in concurrent.futures.as_completed(pending):
        try:
            records.append(result.result())
        except Exception as exc:
            errors.append({'name':pending[result], 'error':str(exc)})
records += [metadata(name, url, Path(path), 'held_readonly_not_copied') for name,(url,path) in HELD.items()]
(ROOT/'manifest.json').write_text(json.dumps(records, indent=2)+'\n')
(ROOT/'errors.json').write_text(json.dumps(errors,indent=2)+'\n')
(ROOT/'ACQUIRED.md').write_text('# OI acquisition manifest\n\n'+ '\n'.join(
    f"{r['checked_at']} | {r['name']} | {r['status']} | {r['source_url']} | {r['bytes']} bytes | sha256:{r['sha256']} | {r['local_path']}"
    for r in records)+'\n')
for r in records:
    print(r['name'], r['status'], r['bytes'], f"rows={r.get('rows')} cols={r.get('columns')}")
print('New bytes:',sum(r['bytes'] for r in records if r['status']=='acquired'))
if errors:
    raise SystemExit(json.dumps(errors))
