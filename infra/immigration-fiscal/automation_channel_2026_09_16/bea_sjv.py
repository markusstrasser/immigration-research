import pandas as pd, numpy as np
P="/Users/alien/Projects/immigration-research/infra/immigration-fiscal/automation_channel_2026_09_16/_cache/CAINC1_CA_1969_2024.csv"
US="/Users/alien/Projects/immigration-research/infra/immigration-fiscal/automation_channel_2026_09_16/_cache/CAINC1__ALL_AREAS_1969_2024.csv"
yrs=[str(y) for y in range(1969,2025)]
def load(p):
    d=pd.read_csv(p,dtype=str,low_memory=False,encoding="latin-1")
    d.columns=[c.strip() for c in d.columns]
    d['GeoFIPS']=d['GeoFIPS'].str.replace('"','').str.strip()
    d['GeoName']=d['GeoName'].str.replace('"','').str.strip()
    return d
ca=load(P); al=load(US)
SJV={'06019':'Fresno','06029':'Kern','06107':'Tulare','06031':'Kings','06047':'Merced','06039':'Madera','06099':'Stanislaus','06077':'San Joaquin'}
def num(d,fips,line):
    r=d[(d.GeoFIPS==fips)&(d.LineCode==str(line))]
    if r.empty: return None
    return pd.to_numeric(r.iloc[0][yrs].str.replace(',',''),errors='coerce')
# line1 personal income (thousands), line2 population, line3 per-capita income
inc=pd.DataFrame({n:num(ca,f,1) for f,n in SJV.items()})
pop=pd.DataFrame({n:num(ca,f,2) for f,n in SJV.items()})
sjv_pci=inc.sum(axis=1)*1000/pop.sum(axis=1)
us_pci=num(al,'00000',3); ca_pci=num(al,'06000',3)
out=pd.DataFrame({'SJV_pci':sjv_pci.round(0),'CA_pci':ca_pci,'US_pci':us_pci})
out['SJV/CA']=(sjv_pci/ca_pci).round(4); out['SJV/US']=(sjv_pci/us_pci).round(4)
out['SJV_pop']=pop.sum(axis=1).astype('Int64')
print(out.loc[[str(y) for y in [1969,1970,1975,1980,1985,1990,1995,2000,2005,2010,2015,2019,2020,2022,2023,2024]]].to_string())
print("\n--- per-county SJV/US ratio, 1970 vs 2024 ---")
for n in SJV.values():
    pci=(inc[n]*1000/pop[n])
    print(f"{n:12s} 1970 {pci['1970']/us_pci['1970']:.3f}  2024 {pci['2024']/us_pci['2024']:.3f}")
print("\nSJV population 1970 %d -> 2024 %d (x%.2f); CA x%.2f ; US x%.2f" % (
  pop.sum(axis=1)['1970'], pop.sum(axis=1)['2024'], pop.sum(axis=1)['2024']/pop.sum(axis=1)['1970'],
  float(num(al,'06000',2)['2024'])/float(num(al,'06000',2)['1970']),
  float(num(al,'00000',2)['2024'])/float(num(al,'00000',2)['1970'])))
