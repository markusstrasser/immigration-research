"""Verify archives and selected row counts; produce separate weighted migration objects."""
import csv
import hashlib
import io
import json
import sys
from pathlib import Path
import zipfile

ROOT=Path(__file__).resolve().parent
def require(condition,message):
 if not condition: raise ValueError(message)

CACHE=ROOT/'_cache'
(ROOT/'derived').mkdir(exist_ok=True)
expected=json.loads((ROOT/'sources.json').read_text())
require(bool(expected.get('files')),'Empty source manifest')
names=[x['filename'] for x in expected['files']]
require(len(names)==len(set(names)),'Duplicate source manifest filenames')
require({'enadid_2018_csv.zip','enadid_2023_csv.zip','metadata2018.xml','metadata2023.xml'}.issubset(names),'Required frozen source missing from manifest')
for source in expected['files']:
 p=CACHE/source['filename']
 require(p.is_file(), f'Missing raw source {p}')
 require(hashlib.sha256(p.read_bytes()).hexdigest()==source['sha256'], f'Source hash changed: {p}')
rows=[]
checks=[]
for year in ([int(x) for x in sys.argv[1:]] or (2018,2023)):
 path=CACHE/f'enadid_{year}_csv.zip'
 if not path.exists(): path=CACHE/f'enadid_{year}_ranged.zip'
 require(path.exists(), f'Missing verified archive for {year}')
 with zipfile.ZipFile(path) as z:
  require(z.testzip() is None,f'ZIP CRC failure: {path}')
  for table in ('tmigrante','tsdem'):
   candidates=[n for n in z.namelist() if table in n.lower() and n.lower().endswith('.csv') and '/conjunto_de_datos/' in n.lower() and Path(n).name.startswith('conjunto_')]
   require(len(candidates)==1,f'Ambiguous data member: {(year,table,candidates)}')
   member=candidates[0]
   data=z.read(member)
   reader=csv.DictReader(io.StringIO(data.decode('utf-8-sig')))
   records=[{k.lower().strip():v.strip() for k,v in r.items()} for r in reader]
   require(bool(records), f'Zero records in {member}')
   expected_rows={(2018,'tmigrante'):2611,(2018,'tsdem'):385978,(2023,'tmigrante'):3660,(2023,'tsdem'):359018}
   require(len(records)==expected_rows[year,table],f'Unexpected row count: {(year,table,len(records))}')
   key='llave_mig' if table=='tmigrante' else 'llave_per'
   require(len({r[key] for r in records})==len(records),f'Duplicate key: {(year,table)}')
   weight='fac_hog' if year==2023 and table=='tmigrante' else 'fac_viv'
   require(all(float(r[weight])>0 for r in records),f'Nonpositive weight: {(year,table)}')
   checks.append({'year':year,'table':table,'member':member,'rows':len(records),'columns':len(records[0]),'weight':weight,'unique_key':key,'sha256':hashlib.sha256(data).hexdigest()})
   def emit(name,predicate):
    subset=[r for r in records if predicate(r)]
    require(bool(subset),f'Empty weighted example: {(year,name)}')
    rows.append({'year':year,'table':table,'measure':name,'n':len(subset),'weighted_people':sum(float(r[weight]) for r in subset),'weight':weight})
   if table=='tmigrante':
    emit('all_reported_departure_migrants_in_window',lambda r:True)
    emit('departure_migrants_us_destination',lambda r:r['p4_11']=='1')
    emit('us_destination_returned_within_departure_cohort',lambda r:r['p4_11']=='1' and r['cond_resid']=='1')
   else:
    prior='p3_24' if year==2023 else 'p3_19'
    birth='p3_10' if year==2023 else 'p3_7'
    emit('residents_age5plus_us_residence_five_years_before_all_birthplaces',lambda r:r[prior]=='3' and 5<=int(r['edad'])<999)
    emit('residents_age5plus_us_residence_five_years_before_mexico_born',lambda r:r[prior]=='3' and r[birth] in ('1','2') and 5<=int(r['edad'])<999)
with (ROOT/'derived'/'weighted_examples.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(ROOT/'derived'/'validation.json').write_text(json.dumps(checks,indent=2))
print(json.dumps({'tables':checks,'weighted_examples':rows},indent=2))
