import json, pandas as pd, numpy as np
P=print
DKC='https://api.statbank.dk/v1/data (POST, table=STRAFNA9)'
DKP='https://api.statbank.dk/v1/data (POST, table=FOLK1E)'
NLU='https://opendata.cbs.nl/ODataApi/odata/85658NED/TypedDataSet'
c=pd.read_csv('dk_crime_raw.csv'); p=pd.read_csv('dk_pop_raw.csv')
BAND={'15-29 years':'15-29','30-49 years':'30-49','50-79 years':'50-79'}
c['band']=c.ALDER.map(BAND); c['year']=c.TID.astype(int)
ctot=c[c.ALDER=='Age, total'].copy()
c=c.dropna(subset=['band'])
p['age']=p.ALDER.str.extract(r'(\d+)').astype(int)
p['band']=pd.cut(p.age,[14,29,49,79],labels=['15-29','30-49','50-79']).astype(str)
p['year']=p.TID.str[:4].astype(int); p['sex']=p['KØN']
pg=p.groupby(['HERKOMST','sex','band','year'],as_index=False).INDHOLD.sum().rename(columns={'INDHOLD':'pop'})
def add(dst,src,new):
    x=pg[pg.HERKOMST.isin(src)].groupby(['sex','band','year'],as_index=False)['pop'].sum(); x['HERKOMST']=new; return pd.concat([dst,x])
pg=add(pg,['Immigrants from western countries','Immigrants from non-western countries'],'Immigrants, total')
pg=add(pg,['Descendants from western countries','Descendants from non-western countries'],'Descendants, total')
PMAP={'Total':'Total','Persons of Danish origin':'Persons of Danish origin','Immigrants, total':'Immigrants, total',
 'Immigrants from western countries':'Immigrants from western countries','Immigrants from non-western countries':'Immigrants from non-western countries',
 'Descendants, total':'Descendants, total','Descendants from western countries':'Descendants from western countries','Descendants from non-western countries':'Descendants from non-western countries'}
c['sex']=c.KOEN
m=c.merge(pg,left_on=['HERKOMST','sex','band','year'],right_on=['HERKOMST','sex','band','year'],how='inner')
m=m.rename(columns={'INDHOLD':'count'})
P("DK merged band rows:",len(m),"| unmatched crime rows:",len(c)-len(m))
# both sexes
bs=m.groupby(['HERKOMST','band','year'],as_index=False)[['count','pop']].sum(); bs['sex']='Both sexes'
m=pd.concat([m[['HERKOMST','sex','band','year','count','pop']],bs],ignore_index=True)
m['rate']=m['count']/m['pop']*1e5
# 15-79 aggregate + direct standardisation (standard pop = HERKOMST 'Total', same sex)
agg=m.groupby(['HERKOMST','sex','year'],as_index=False)[['count','pop']].sum(); agg['band']='15-79'
agg['rate']=agg['count']/agg['pop']*1e5
std=m[m.HERKOMST=='Total'][['sex','band','year','pop']].rename(columns={'pop':'stdpop'})
z=m.merge(std,on=['sex','band','year'])
z['exp']=z['rate']*z['stdpop']
asr=z.groupby(['HERKOMST','sex','year'],as_index=False).apply(lambda g: pd.Series({'asr':g['exp'].sum()/g['stdpop'].sum()}),include_groups=False)
base=asr[asr.HERKOMST=='Total'][['sex','year','asr']].rename(columns={'asr':'base'})
asr=asr.merge(base,on=['sex','year']); asr['standardized_index']=asr.asr/asr.base*100
agg=agg.merge(asr[['HERKOMST','sex','year','standardized_index']],on=['HERKOMST','sex','year'],how='left')
dk=pd.concat([m.assign(standardized_index=np.nan),agg],ignore_index=True)
dk=pd.DataFrame({'country':'Denmark','table_id':'STRAFNA9 x FOLK1E','year':dk.year,'group':dk.HERKOMST,'sex':dk.sex,
 'age_band':dk.band,'count':dk['count'],'population':dk['pop'],'rate':dk.rate,'rate_unit':'per 100,000 population',
 'standardized_index':dk.standardized_index,'provisional':False,'source_url':DKC+' + '+DKP})
# ---------- NL ----------
n=pd.read_csv('nl_raw.csv')
GES={'T001038':'Both sexes','3000':'Men','4000':'Women','9000':'Unknown'}
LFT={'10000':'Total','52020':'12-17','53103':'18-22','A052643':'23-44','53715':'45-64','80200':'65+','99999':'Other/unknown'}
GBL={'T001638':'Total','A051760':'Born in NL, both parents born in NL','A051777':'Born in NL, one parent born in NL',
 'A051778':'Born in NL, both parents born abroad (2nd gen)','A051736':'Born outside the Netherlands (1st gen)'}
HRK={'T001040':'Total','1012600':'Netherlands','H007933':'Europe (excluding the Netherlands)','H008766':'Turkiye','H008673':'Morocco',
 'H008751':'Suriname','H007119':'Dutch Caribbean','H008632':'Indonesia','2820717':'Outside Europe (excl. 5 largest origin countries)','2012659':'Unknown country of origin'}
n['sex']=n.Geslacht.astype(str).str.strip().map(GES); n['age_band']=n.Leeftijd.astype(str).str.strip().map(LFT)
n['gen']=n.Geboorteland.astype(str).str.strip().map(GBL); n['hrk']=n.Herkomst.astype(str).str.strip().map(HRK)
n['year']=n.Perioden.str[:4].astype(int)
n=n.rename(columns={'TotaalVerdachtenVanMisdrijven_1':'count','TotaalVerdachtenVanMisdrijven_8':'rate'})
n['population']=np.where(n['rate']>0, n['count']/n['rate']*1e4, np.nan)
nl=pd.DataFrame({'country':'Netherlands','table_id':'85656NED_absent|85658NED','year':n.year,
 'group':'herkomst='+n.hrk+' | geboorteland='+n.gen,'sex':n.sex,'age_band':n.age_band,'count':n['count'],
 'population':n.population,'rate':n['rate'],'rate_unit':'per 10,000 residents','standardized_index':np.nan,
 'provisional':n.year.isin([2024,2025]),'source_url':NLU})
nl['table_id']='85658NED'
out=pd.concat([dk,nl],ignore_index=True)
out.to_csv('registry_rates.csv',index=False)
P("\n=== VALIDATION ===")
P("rows: Denmark=%d Netherlands=%d Norway=0 TOTAL=%d"%( (out.country=='Denmark').sum(),(out.country=='Netherlands').sum(),len(out)))
v=out.dropna(subset=['count','population','rate']); v=v[(v.population>0)&(v['rate']>0)]
unit=np.where(v.country=='Denmark',1e5,1e4); rec=v['count']/v.population*unit
dev=(rec-v['rate']).abs()/v['rate']*100
P("rate recompute: n=%d max_dev=%.4f%% share>0.5%%=%d"%(len(v),dev.max(),(dev>0.5).sum()))
P("  Denmark max_dev=%.6f%% | Netherlands max_dev=%.4f%% (NL pop is DERIVED from count/rate -> tautological)"%(dev[v.country=='Denmark'].max(),dev[v.country=='Netherlands'].max()))
P("latest year: DK=%d (STRAFNA9 latestPeriod=2025) NL=%d (85658NED Period=2010-2025)"%(dk.year.max(),nl.year.max()))
P("DK crime 'Age, total' vs sum of 3 bands (2025, Total, Men): tot=%d bands=%d"%(
  ctot[(ctot.year==2025)&(ctot.HERKOMST=='Total')&(ctot.KOEN=='Men')].INDHOLD.sum(),
  c[(c.year==2025)&(c.HERKOMST=='Total')&(c.KOEN=='Men')].INDHOLD.sum()))
P("\n=== DK headline, 2025, age 15-79 ===")
h=out[(out.country=='Denmark')&(out.year==2025)&(out.age_band=='15-79')&(out.sex.isin(['Men','Both sexes']))]
P(h[['group','sex','count','population','rate','standardized_index']].round(1).to_string(index=False))
P("\n=== NL headline, 2025, all ages, by generation (herkomst Total) ===")
q=out[(out.country=='Netherlands')&(out.year==2025)&(out.age_band=='Total')&(out.sex.isin(['Men','Both sexes']))&(out.group.str.startswith('herkomst=Total'))]
P(q[['group','sex','count','population','rate']].round(1).to_string(index=False))
P("\n=== NL headline, 2025, all ages, by herkomst (geboorteland Total) ===")
q2=out[(out.country=='Netherlands')&(out.year==2025)&(out.age_band=='Total')&(out.sex.isin(['Men','Both sexes']))&(out.group.str.endswith('geboorteland=Total'))]
P(q2[['group','sex','count','population','rate']].round(1).to_string(index=False))
