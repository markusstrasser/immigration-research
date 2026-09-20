"""Reproduce SCAAP from PDF; adapted from existing analyze_conduct_denominators.py:87-109."""
from pathlib import Path
import argparse
import csv
import pdfplumber
from source_contract import require

def parse(pdf_path,output):
    rows=[]
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            for table in page.extract_tables():
                for row in table:
                    if not row or str(row[0]).strip()!='2024':
                        continue
                    require(len(row)==9,'SCAAP table column count changed')
                    year,state,name,application,*values=row
                    values=[float(v.replace(',','').replace('$','').strip()) for v in values]
                    rows.append([int(year),state,name,application,*values])
    require(bool(rows),'No SCAAP data rows extracted')
    require(len(rows)==len({r[3] for r in rows}),'Duplicate SCAAP applications')
    output.parent.mkdir(parents=True,exist_ok=True)
    with output.open('w',newline='') as f:
        writer=csv.writer(f,lineterminator='\n')
        writer.writerow(['fiscal_year','state','jurisdiction','application','salary_usd',
                         'total_days','confirmed_days','unknown_days','award_usd'])
        writer.writerows(rows)
    return len(rows)

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--root',type=Path,default=Path(__file__).resolve().parent)
    root=p.parse_args().root
    print(parse(root/'_cache/scaap_fy2024_awards.pdf',root/'derived/scaap_fy2024_awards.csv'))
