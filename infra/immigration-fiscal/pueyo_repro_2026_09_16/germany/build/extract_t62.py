import openpyxl, csv, json
RAW='/Users/alien/Projects/immigration-research/infra/immigration-fiscal/pueyo_repro_2026_09_16/germany/raw'
wb=openpyxl.load_workbook(f'{RAW}/T62_bund_2025.xlsx',read_only=True,data_only=True)
ws=wb['T62 BKA']
rows=list(ws.iter_rows(values_only=True))
codes=rows[3]   # row 4: nationality key codes
names=rows[4]   # row 5: nationality names
KEYS={'------':'total_all','890000':'total_excl_imm','892000':'violent','100000':'sexual',
      '010000':'murder','020000':'manslaughter','892500':'homicide_all','725000':'imm_offences'}
out={}
for r in rows[5:]:
    k=str(r[0]).strip() if r[0] is not None else ''
    if k in KEYS:
        out[KEYS[k]]=r
cols=[]
for j in range(2,len(names)):
    nm=names[j]
    if nm is None: continue
    cols.append((j,str(codes[j]).strip() if codes[j] is not None else '',str(nm).strip()))
recs=[]
for j,code,nm in cols:
    rec={'bka_code':code,'bka_name':nm}
    for key,row in out.items():
        v=row[j]
        rec[key]=int(v) if isinstance(v,(int,float)) else (int(str(v)) if str(v).strip().isdigit() else None)
    recs.append(rec)
with open(f'{RAW}/../t62_suspects_2025.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(recs[0])); w.writeheader(); w.writerows(recs)
print('cols',len(recs))
for r in recs[:4]: print(r)
# checks
nd=[r for r in recs if r['bka_name'].startswith('Nichtdeutsche')]
print('nichtdeutsche row',nd)
tot=sum(r['total_all'] for r in recs if r['bka_code'] not in ('...','000','') and r['bka_name'] not in ('Tatverdächtige insgesamt','Nichtdeutsche insgesamt','Deutschland'))
print('sum of foreign nationality cols total_all',tot)
