import json, csv, os
RAW='/Users/alien/Projects/immigration-research/infra/immigration-fiscal/pueyo_repro_2026_09_16/germany/raw'
st=json.load(open(f'{RAW}/st0003.json'))
vv=st['variableValues']
d=json.load(open(f'{RAW}/d0003_staag.json'))['data'][0]
ids=d['id']; size=d['size']; dim=d['dimension']; val=d['value']
idx={k:dim[k]['category']['index'] for k in dim}
strides={}
s=1
for name,n in zip(reversed(ids),reversed(size)):
    strides[name]=s; s*=n
assert s==len(val), (s,len(val))
def get(**sel):
    p=0
    for name in ids:
        p+=idx[name][sel[name]]*strides[name]
    return val[p]
ages=sorted(idx['ALT102'])
age_m1839=[f'ALT{a:03d}' for a in range(18,40)]
rows=[]
for code in idx['STAAG6']:
    lab_de=vv[code]['label']['de']; lab_en=vv[code]['label']['en']
    def tot(ges,date):
        return sum(get(statistic='12521',DINSG='DG',content='BEV027$QMU',GES=ges,STAG=date,ALT102=a,STAAG6=code) for a in ages)
    t25=tot('%TOTAL%','2025-12-31')
    t24=tot('%TOTAL%','2024-12-31')
    m1839=sum(get(statistic='12521',DINSG='DG',content='BEV027$QMU',GES='GESM',STAG='2025-12-31',ALT102=a,STAAG6=code) for a in age_m1839)
    m_tot=tot('GESM','2025-12-31')
    rows.append(dict(staag6=code,name_de=lab_de,name_en=lab_en,pop_2025=int(t25),pop_2024=int(t24),
                     male_2025=int(m_tot),male_18_39_2025=int(m1839)))
rows.sort(key=lambda r:-r['pop_2025'])
out=f'{RAW}/../azr_nationality_2025.csv'
with open(out,'w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
tot25=sum(r['pop_2025'] for r in rows if r['staag6']!='%TOTAL%')
print('rows',len(rows))
print('%TOTAL% pop_2025',[r['pop_2025'] for r in rows if r['staag6']=='%TOTAL%'])
print('sum of listed nationalities 2025',tot25)
print('written',os.path.abspath(out))
