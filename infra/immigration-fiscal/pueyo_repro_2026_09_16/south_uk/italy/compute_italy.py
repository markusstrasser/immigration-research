import csv, json, collections
YEAR='2023'
# codes present BOTH in the by-country file and the by-citizenship file, no parent/child double count
VIOLENT=['INTENHOM','ATTEMPHOM','INFANTHOM','MANSHOM','BLOWS','CULPINJU','MENACE','STALK',
         'KIDNAPP','RAPE','RAPEUN18','ROBBER','EXTORT']
SERIOUS=['INTENHOM','ATTEMPHOM','RAPE','RAPEUN18','ROBBER','KIDNAPP']

f2=[r for r in csv.DictReader(open('offenders_by_country_2022_2024.csv'))
    if r['DATA_TYPE']=='OFFEND' and r['TIME_PERIOD']==YEAR and r['OBS_VALUE']]
num=collections.defaultdict(lambda: collections.defaultdict(float))
for r in f2: num[r['COUNTRY_CITIZEN']][r['TYPE_CRIME']]+=float(r['OBS_VALUE'])

f1=[r for r in csv.DictReader(open('offenders_by_citizenship_2022_2024.csv'))
    if r['DATA_TYPE']=='OFFEND' and r['TIME_PERIOD']==YEAR and r['OBS_VALUE']]
cit=collections.defaultdict(lambda: collections.defaultdict(float))
for r in f1: cit[r['CITIZENSHIP']][r['TYPE_CRIME']]+=float(r['OBS_VALUE'])

pop=collections.defaultdict(dict)
for r in csv.DictReader(open('popstr_raw.csv')):
    if r['REF_AREA']=='IT' and r['SEX']=='9' and r['OBS_VALUE']:
        pop[r['CITIZENSHIP']][r['TIME_PERIOD']]=float(r['OBS_VALUE'])
def popmean(c):
    d=pop.get(c,{}); a,b=d.get('2023'),d.get('2024')
    return (a+b)/2 if a and b else (a or b)

es=json.load(open('eurostat_migr_pop1ctz_IT.json'))
ci=es['dimension']['citizen']['category']['index']; lab=es['dimension']['citizen']['category']['label']
ti=es['dimension']['time']['category']['index']; nt=len(ti); v=es['value']
ep=lambda c,y: v.get(str(ci[c]*nt+ti[y])) if c in ci else None
tot_pop=(ep('TOTAL','2023')+ep('TOTAL','2024'))/2
nat_pop=(ep('NAT','2023')+ep('NAT','2024'))/2
for_pop=tot_pop-nat_pop
R=lambda n,p: 100000*n/p

it_v=sum(cit['ITL'].get(k,0) for k in VIOLENT); it_s=sum(cit['ITL'].get(k,0) for k in SERIOUS)
fr_v=sum(cit['FRG'].get(k,0) for k in VIOLENT); fr_s=sum(cit['FRG'].get(k,0) for k in SERIOUS)
r_it_v, r_it_s = R(it_v,nat_pop), R(it_s,nat_pop)

ISMU=458000      # ISMU XXIX Rapporto: irregular foreign presence, Italy, 1 Jan 2023 (7.9% of total foreign presence)
NONRES=176000    # ISMU: 'regolari non residenti' - legally present, not on the population register
infl=1+ISMU/for_pop
infl2=1+(ISMU+NONRES)/for_pop

SKIP={'WORLD','999','X95','EU27_2020','EU28'}
out=[]
for c,cr in num.items():
    if c in SKIP: continue
    p=popmean(c)
    if not p or p<5000: continue
    nv=sum(cr.get(k,0) for k in VIOLENT); ns=sum(cr.get(k,0) for k in SERIOUS)
    out.append(dict(iso=c,country=lab.get(c,c),pop_mean_2023_2024=round(p),
        offenders_violent13=int(nv),offenders_serious6=int(ns),
        rate_violent_per100k=round(R(nv,p),1),rate_serious_per100k=round(R(ns,p),1),
        x_vs_italians_violent=round(R(nv,p)/r_it_v,1),
        x_vs_italians_serious=round(R(ns,p)/r_it_s,1),
        x_vs_italians_violent_ISMU_adj=round(R(nv,p)/r_it_v/infl,1),
        x_vs_italians_violent_allpresence_adj=round(R(nv,p)/r_it_v/infl2,1)))
out.sort(key=lambda r:-r['x_vs_italians_violent'])
with open('italy_violent_offender_rates_2023.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)

print(f"Italy {YEAR}: pop {tot_pop:,.0f}; Italian citizens {nat_pop:,.0f}; foreign residents {for_pop:,.0f} ({100*for_pop/tot_pop:.1f}%)")
print(f"Violent set (13 ISTAT offence codes): Italians {it_v:,.0f} -> {r_it_v:.1f}/100k | foreigners {fr_v:,.0f} -> {R(fr_v,for_pop):.1f}/100k = {R(fr_v,for_pop)/r_it_v:.2f}x")
print(f"Serious subset (6 codes):             Italians {it_s:,.0f} -> {r_it_s:.1f}/100k | foreigners {fr_s:,.0f} -> {R(fr_s,for_pop):.1f}/100k = {R(fr_s,for_pop)/r_it_s:.2f}x")
print(f"ISMU irregular presence {ISMU:,} -> foreign denominators x{infl:.3f}; every foreign ratio falls by {100*(1-1/infl):.1f}%")
print(f"+ regolari non residenti {NONRES:,} -> x{infl2:.3f}; ratios fall by {100*(1-1/infl2):.1f}%")
print()
CH={'TN':17.8,'DZ':17.1,'MA':11.8,'BA':10.9,'EG':10.2,'GM':9.6,'CI':7.3,'DO':6.4,'NG':6.4,'CO':5.8,'RS':5.7,'AF':5.5,'CU':5.3,'GN':5.2,'SN':5.2}
print(f"{'country':<24}{'pop':>11}{'offV':>7}{'/100k':>9}{'xITA':>7}{'xITA_ISMU':>11}{'xITA_allpres':>13}{'Pallesen':>10}")
for r in out[:20]:
    ch=CH.get(r['iso'],'')
    print(f"{r['country']:<24}{r['pop_mean_2023_2024']:>11,}{r['offenders_violent13']:>7}{r['rate_violent_per100k']:>9}{r['x_vs_italians_violent']:>7}{r['x_vs_italians_violent_ISMU_adj']:>11}{r['x_vs_italians_violent_allpresence_adj']:>13}{str(ch):>10}")
print("\n--- chart countries not in top 20 ---")
for iso,ch in CH.items():
    m=[r for r in out if r['iso']==iso]
    if m and m[0] not in out[:20]:
        r=m[0]; print(f"{r['country']:<24}{r['pop_mean_2023_2024']:>11,}{r['offenders_violent13']:>7}{r['rate_violent_per100k']:>9}{r['x_vs_italians_violent']:>7}{r['x_vs_italians_violent_ISMU_adj']:>11}{r['x_vs_italians_violent_allpresence_adj']:>13}{ch:>10}")
    elif not m: print(f"{iso:<24}{'(pop<5000 or missing)':>40}{ch:>10}")
