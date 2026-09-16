import os
import pandas as pd, numpy as np
D = os.path.dirname(os.path.abspath(__file__)); R = lambda f: pd.read_csv(os.path.join(D,'raw',f))
s4=R('strafna4_offence_origin_2008_2024.csv'); pop=R('folk1c_pop_origin_sex_age_2008_2024.csv')
pop['YEAR']=pop.TID.astype(str).str[:4].astype(int)
out=[]
def P(*a):
    s=' '.join(str(x) for x in a); print(s); out.append(s)
def ratio(offl,origins,y0,y1):
    c=s4[s4['OVERTRÆD'].isin(offl)&s4.TID.between(y0,y1)]; p=pop[(pop.KØN=='Total')&pop.YEAR.between(y0,y1)]
    num=c[c.IELAND.isin(origins)].INDHOLD.sum(); den=p[p.IELAND.isin(origins)].INDHOLD.sum()
    dn=c[c.IELAND=='Denmark'].INDHOLD.sum()/p[p.IELAND=='Denmark'].INDHOLD.sum()
    return (num/den)/dn, num
V=['Crimes of violence, total']
CH1={'Kuwait':10.1,'Somalia':9.8,'Lebanon':8.7,'Tunisia':8.4,'Jordan':6.5,'Uganda':5.65,'Iraq':4.9,
 'Morocco':4.85,'Algeria':4.7,'Ethiopia':4.2,'Syria':4.15,'Afghanistan':4.05,'Egypt':3.75,'Iran':3.5,
 'Turkey':3.35,'Kenya':3.3,'Ghana':3.2,'Myanmar':2.85,'Pakistan':2.55,'Tanzania':2.4,'Denmark':1.0,
 'Poland':1.2,'Sweden':0.6,'Germany':0.45,'USA':0.35,'Japan':0.2}
rows=[]
for c,cv in CH1.items():
    r,n=ratio(V,[c],2010,2022); rows.append((c,cv,round(r,2),int(n)))
t=pd.DataFrame(rows,columns=['origin','chart_ratio','my_ratio','persons'])
t['diff']=(t.my_ratio-t.chart_ratio).round(2)
t.to_csv(os.path.join(D,'chart1_comparison.csv'),index=False)
P("CHART 1 comparison (violent crime, 2010-2022, ratio to Danish origin)")
P(t.to_string(index=False))
P(f"max |diff| = {t['diff'].abs().max():.2f}; mean |rel err| = {(t['diff'].abs()/t.chart_ratio).mean()*100:.1f}%")

P("\nEX-YUGOSLAVIA variant test (2008-2024 ratios)")
VAR={'YU+YUFR+SerMon':['Yugoslavia','Yugoslavia, Federal Republic','Serbia and Montenegro'],
 '+Bosnia,Croatia,NMac':['Yugoslavia','Yugoslavia, Federal Republic','Serbia and Montenegro','Bosnia and Herzegovina','Croatia','Republic of North Macedonia'],
 'Yugoslavia only':['Yugoslavia']}
OFF={'blackmail':['Blackmail and usury '],'burglary':['Burglary (banks, shops, etc.)','Household burglary ','Burglary (uninhabited buildings)'],
 'fraud':['Fraud '],'shoplifting':['Shoplifting, etc.'],'theft':['Other theft ','Theft of other objects ','Theft from cars, boats, etc.','Theft of vehicle','Theft of mopeds ','Theft of bicycles ']}
CH={'blackmail':13,'burglary':5,'fraud':5,'shoplifting':7,'theft':5}
P(f"{'offence':<14}{'chart':>6}"+''.join(f"{k:>24}" for k in VAR))
errs={k:[] for k in VAR}
for o,cv in CH.items():
    row=f"{o:<14}{cv:>6}"
    for k,v in VAR.items():
        r,n=ratio(OFF[o],v,2008,2024); row+=f"{r:>18.1f}(n{int(n)})"[:24].rjust(24); errs[k].append(abs(r-cv)/cv)
    P(row)
P("mean |rel err|: "+", ".join(f"{k}={np.mean(v)*100:.0f}%" for k,v in errs.items()))
open(os.path.join(D,'analysis_log.txt'),'a').write('\n'.join(out)+'\n')
