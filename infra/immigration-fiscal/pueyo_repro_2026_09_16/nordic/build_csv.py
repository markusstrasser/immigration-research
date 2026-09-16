import json, csv, re, openpyxl
HDR=['country','origin','offence','unit','numerator','denominator','rate','ratio_to_native','standardized','period','source_table','chart_value']
rows=[]

# ---------------- FINLAND ----------------
fi=json.load(open('finland/fi_parsed.json')); byname={r['name']:r for r in fi}
chart_fi={'Syria':125.74,'Democratic Republic of the Congo':101.60,'Afghanistan':99.76,'Iraq':85.54,'Somalia':52.37,
 'Iran':38.35,'Sweden':27.00,'Estonia':12.02,'Ukraine':11.39,'Finland':8.12,'Russia':6.22}
nat=byname['Finland']['sex_events_p10k']; small=0; named=0
for r in fi:
    N=r['sex_events']; rate=r['sex_events_p10k']
    if N is None or not rate: continue
    pop=N/rate*10000
    if r['code'] not in ('SSS','ULK','EUR','AFR','ASI','AME','OSE','X','991'):
        named+=1
        if N<20: small+=1
    rows.append(['Finland',r['name'],'Sexual offences (Criminal Code ch.20, code 231T241)',
        'suspects (by number of events) per 10,000 resident citizens of that nationality',
        N,round(pop),round(rate,2),round(rate/nat,2),'no','2023','StatFin rpk 13jg, contentscode ep_lkm / ep_lkm_vaesto',
        chart_fi.get(r['name'],'')])
FI=(small,named)

# ---------------- SWEDEN ----------------
def num(s): return float(s.replace(' ','').replace(' ','').replace(',','.'))
sw=[]
for ln in open('sweden/b6_raw.txt',encoding='utf-8').read().split('\n')[:70]:
    if not ln.strip(): continue
    p=re.split(r'\s{2,}', ln.strip())
    if len(p)<6: continue
    try: vals=[num(x) for x in p[-5:]]
    except ValueError: continue
    sw.append((re.sub(r'^därav\s+','',p[0]).strip(), *vals))
chart_sw={'Afghanistan':5.1,'Nordafrika':4.6,'Somalia':4.5,'Eritrea':4.0,'Irak':3.9,'Libanon':3.8,'Syrien':3.8,
 'Colombia':3.5,'Iran':3.0,'Chile':2.8,'Etiopien':2.8,'Turkiet':2.7,'Ryssland':2.55,'Polen':2.4,'Vietnam':2.25,
 'Pakistan':2.25,'Rumänien':2.15,'Bosnien-Hercegovina':1.85,'Thailand':1.8,'Filippinerna':1.6,'Ungern':1.55,
 'Indien':1.4,'Island':1.4,'Grekland':1.25,'USA':1.2,'Danmark':1.15,'Norge':1.1,
 'Storbritannien och Nordirland':1.1,'Inrikesfödda med två inrikesfödda föräldrar':1.0,'Finland':1.0,'Kina':1.0,'Tyskland':0.9}
for name,ninn,nsus,ntot,pct,ori in sw:
    rows.append(['Sweden',name,'Any offence — registered as suspect at least once 2015-2017 (age 15+, registered 31-12-2014)',
        'share of group suspected (%)',int(nsus),int(ntot),pct,ori,'no','2015-2017',
        'Bra 2021:9 Tabellbilaga 1, Table B6','' if name not in chart_sw else chart_sw[name]])
SW={n:(a,b,c,d,e) for n,a,b,c,d,e in sw}

# ---------------- NORWAY ----------------
wb=openpyxl.load_workbook('norway/ssb_tab2_siktelser_per1000.xlsx',data_only=True)
ws=wb['Tab2 Siktelser, menn 15-24 år']; wp=wb['Befolkningstall, menn 15-24 år']; ws2=wb['Tab2 Siktelser (bosted)']
chart_no={'ØVRIGE BOSATTE':32,'Pakistan':111,'Syria':136,'Russland':140,'Afghanistan':160,'Eritrea':241,
 'Irak':288,'Etiopia':289,'Somalia':483}
cnt={}; 
for r in range(8,48):
    v=ws.cell(r,1).value
    if isinstance(v,str): cnt.setdefault(v.strip(),r)
pop={}
for r in range(5,47):
    v=wp.cell(r,1).value
    if isinstance(v,str): pop.setdefault(v.strip(),r)
natY=ws.cell(89,25).value
for r in range(84,124):
    a=ws.cell(r,1).value
    if not isinstance(a,str): continue
    a=a.strip(); y=ws.cell(r,25).value
    if y is None: continue
    N=ws.cell(cnt[a],25).value if a in cnt else ''
    P=wp.cell(pop[a],7).value if a in pop else ''
    rows.append(['Norway',a,'Charges (siktelser) for violence and abuse — vold og mishandling',
        'charges per 1,000 mean-annual population; MEN 15-24 RESIDENT IN OSLO; 4-year cumulative 2020-2023',
        N,P,round(y,2),round(y/natY,2),'no','2020-2023',
        'SSB 2024-12-09 "Tab 2-Siktelser (bosted).xlsx", sheet "Tab2 Siktelser, menn 15-24 ar", col Y (BOSTED OSLO)',
        chart_no.get(a,'')])
natH=ws2.cell(153,8).value
for r in range(148,246):
    a=ws2.cell(r,1).value
    if not isinstance(a,str): continue
    h=ws2.cell(r,8).value
    if h is None: continue
    rows.append(['Norway',a.strip(),'Charges (siktelser) for violence and abuse — vold og mishandling',
        'charges per 1,000 mean-annual population; ALL AGES, WHOLE COUNTRY; 4-year cumulative 2020-2023',
        '','',round(h,2),round(h/natH,2),'no','2020-2023',
        'SSB 2024-12-09 "Tab 2-Siktelser (bosted).xlsx", sheet "Tab2 Siktelser (bosted)", col H','' ])
natHm=ws.cell(89,8).value
for r in range(84,124):
    a=ws.cell(r,1).value
    if not isinstance(a,str): continue
    h=ws.cell(r,8).value
    if h is None: continue
    rows.append(['Norway',a.strip(),'Charges (siktelser) for violence and abuse — vold og mishandling',
        'charges per 1,000 mean-annual population; MEN 15-24, WHOLE COUNTRY; 4-year cumulative 2020-2023',
        '','',round(h,2),round(h/natHm,2),'no','2020-2023',
        'SSB 2024-12-09 "Tab 2-Siktelser (bosted).xlsx", sheet "Tab2 Siktelser, menn 15-24 ar", col H','' ])

with open('nordic_tidy.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(HDR); w.writerows(rows)
print('rows',len(rows))
print('FI: nationalities with <20 sexual-offence suspects 2023:',FI[0],'of',FI[1],'named nationalities with nonzero suspects')
for k,v in chart_fi.items():
    b=byname[k]; print(f'  FI {k:<34} chart={v:>7.2f} statfin2023={b["sex_events_p10k"]} N={b["sex_events"]}')
print('SW rows parsed:',len(sw))
print('SW ratios:', {k:SW[k][4] for k in ['Afghanistan','Nordafrika','Somalia','Eritrea','Irak','Libanon','Syrien','Colombia'] if k in SW})
print('NO check:', {a:(ws.cell(r,25).value) for a,r in [('Somalia',116),('Etiopia',115),('Irak',119)]})
