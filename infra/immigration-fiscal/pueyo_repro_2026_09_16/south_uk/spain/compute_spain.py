import json, csv
# --- prison stock, mean 2024, Administracion General del Estado (excl. Catalonia)
# Source: Informe General 2024, Instituciones Penitenciarias, Tabla 49 (p.70)
prison = {  # ISO2 : mean 2024 foreign prisoners
 'MA':3792,'CO':1480,'RO':1136,'DZ':974,'EC':440,'DO':386,'PE':346,'SN':309,'AL':286,'BR':262,
 'PT':228,'VE':227,'IT':211,'BG':200,'NG':194,'GB':178,'BO':174}
FOREIGN_PRISON_MEAN = 13850      # Tabla 44, mean 2024, AGE
SPANISH_PRISON_MEAN = 34630      # Tabla 44
TOTAL_PRISON_MEAN   = 48480      # Tabla 44
PRETRIAL_FOREIGN    = 4035
PRETRIAL_SPANISH    = 4138

d=json.load(open('eurostat_migr_pop1ctz_ES.json'))
cidx=d['dimension']['citizen']['category']['index']; clab=d['dimension']['citizen']['category']['label']
tidx=d['dimension']['time']['category']['index']; nt=len(tidx); val=d['value']
def pop(c,y):
    if c not in cidx: return None
    k=str(cidx[c]*nt+tidx[y]); return val.get(k)
def popmean(c):
    a,b=pop(c,'2024'),pop(c,'2025')
    return (a+b)/2 if a and b else (a or b)

tot=popmean('TOTAL'); nat=popmean('NAT')
# foreign = total - nationals
forg = tot-nat
rows=[]
for c,n in prison.items():
    p=popmean(c)
    if not p: continue
    rows.append(dict(iso=c,country=clab[c],prisoners_mean2024=n,
        pop_mean_2024_2025=round(p),
        prisoners_per_100k=round(100000*n/p,1)))
avg_for=100000*FOREIGN_PRISON_MEAN/forg
avg_sp =100000*SPANISH_PRISON_MEAN/nat
for r in rows:
    r['ratio_vs_avg_foreigner']=round(r['prisoners_per_100k']/avg_for,2)
    r['ratio_vs_spaniard']=round(r['prisoners_per_100k']/avg_sp,2)
    r['share_of_foreign_prisoners_pct']=round(100*r['prisoners_mean2024']/FOREIGN_PRISON_MEAN,2)
    r['share_of_total_prisoners_pct']=round(100*r['prisoners_mean2024']/TOTAL_PRISON_MEAN,2)
rows.sort(key=lambda r:-r['ratio_vs_avg_foreigner'])
with open('spain_prison_rates.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

print(f"Spain population 1Jan2024/2025 mean: total {tot:,.0f} nationals {nat:,.0f} foreigners {forg:,.0f} ({100*forg/tot:.1f}%)")
print(f"Avg foreigner prison rate (AGE): {avg_for:.1f}/100k ; Spanish nationals: {avg_sp:.1f}/100k ; foreigner/Spaniard = {avg_for/avg_sp:.2f}x")
print(f"Pretrial share: foreigners {100*PRETRIAL_FOREIGN/FOREIGN_PRISON_MEAN:.1f}%  Spaniards {100*PRETRIAL_SPANISH/SPANISH_PRISON_MEAN:.1f}%  ratio {(PRETRIAL_FOREIGN/FOREIGN_PRISON_MEAN)/(PRETRIAL_SPANISH/SPANISH_PRISON_MEAN):.2f}x")
print()
hdr=f"{'country':<22}{'prisoners':>10}{'pop':>12}{'per100k':>10}{'vsAvgFor':>10}{'vsSpan':>9}{'%foreign':>10}{'%total':>8}"
print(hdr)
for r in rows:
    print(f"{r['country']:<22}{r['prisoners_mean2024']:>10,}{r['pop_mean_2024_2025']:>12,}{r['prisoners_per_100k']:>10}{r['ratio_vs_avg_foreigner']:>10}{r['ratio_vs_spaniard']:>9}{r['share_of_foreign_prisoners_pct']:>10}{r['share_of_total_prisoners_pct']:>8}")

# --- Albania: INE Padron Continuo (table 03005) last published 1 Jan 2022; ECP/Eurostat do not break it out
print("\nAlbania (denominator not published by ECP/Eurostat; Padron Continuo table 03005 ends 1 Jan 2022)")
for p,lab in [(5022,'Padron 1 Jan 2022 (INE 03005)'),(7065,'extrapolated 1 Jan 2024 at the 2019-22 CAGR of 18.6%/yr'),(6688,'secondary INE-derived figure for 1 Jan 2025')]:
    r=100000*286/p
    print(f"  denom {p:>6,}  ({lab})  -> {r:7.0f}/100k = {r/avg_for:5.1f}x average foreigner, {r/avg_sp:5.1f}x Spanish national")
