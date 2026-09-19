"""Record existing source provenance; never overwrite or download raw data."""
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
audit=json.loads((HERE/'derived/audit.json').read_text())
links={
    'Section3All_xls.xlsx':('https://apps.bea.gov/national/Release/XLS/Survey/Section3All_xls.xlsx','https://www.bea.gov/resources/methodologies/nipa-handbook'),
    'asecpub25csv.zip':('https://www2.census.gov/programs-surveys/cps/datasets/2025/march/asecpub25csv.zip','https://www2.census.gov/programs-surveys/cps/datasets/2025/march/asec2025_ddl_pub_full.pdf'),
    'NST-EST2024-ALLDATA.csv':('https://www2.census.gov/programs-surveys/popest/datasets/2020-2024/state/totals/NST-EST2024-ALLDATA.csv','https://www.census.gov/programs-surveys/popest/technical-documentation/methodology.html'),
    'h256dat.zip':('https://meps.ahrq.gov/data_files/pufs/h256dat.zip','https://meps.ahrq.gov/data_files/pufs/h256doc.pdf'),
    'h256su.txt':('https://meps.ahrq.gov/data_stats/download_data/pufs/h256/h256su.txt','https://meps.ahrq.gov/data_files/pufs/h256doc.pdf'),
}
rows=[]
for filename,digest in audit['source_hashes'].items():
    path=Path(filename)
    if path.name in links:
        url,codebook=links[path.name]
        rows.append(dict(name=path.name,path=str(path),bytes=path.stat().st_size,sha256=digest,
            source_url=url,codebook_url=codebook,acquisition='Existing local primary source reused read-only; not redownloaded in this lane'))
output=HERE/'SOURCE_PINS.json'
if output.exists(): raise ValueError('Existing source pin contract must be reviewed, not overwritten')
output.write_text(json.dumps(dict(recorded='2026-09-20',sources=rows,raw_bytes=sum(r['bytes'] for r in rows)),indent=2)+'\n')
print(f'Pinned {len(rows)} existing sources; {sum(r["bytes"] for r in rows)} bytes')
