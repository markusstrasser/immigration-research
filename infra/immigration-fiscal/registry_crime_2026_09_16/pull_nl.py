import json, requests, pandas as pd
S=requests.Session(); S.headers.update({'User-Agent':'research-agent/1.0'}); P=print
B='https://opendata.cbs.nl/ODataApi/odata/85658NED'
per="(Perioden eq '2023JJ00' or Perioden eq '2024JJ00' or Perioden eq '2025JJ00')"
sel="Geslacht,Leeftijd,Geboorteland,Herkomst,Opleiding,Huishoudensinkomen,Perioden,TotaalVerdachtenVanMisdrijven_1,TotaalVerdachtenVanMisdrijven_8"
flt=f"{per} and Opleiding eq 'T001143' and Huishoudensinkomen eq 'T001164'"
url=f"{B}/TypedDataSet?$format=json&$select={sel}&$filter={flt}"
rows=[]; u=url
while u:
    j=S.get(u, timeout=180).json(); rows+=j['value']; u=j.get('odata.nextLink') or j.get('@odata.nextLink')
    if u and not u.startswith('http'): u=B+'/'+u
P("NL filter A rows:", len(rows))
if len(rows)==0:
    flt=f"{per} and Opleiding eq 'T001143 ' and Huishoudensinkomen eq 'T001164 '"
    u=f"{B}/TypedDataSet?$format=json&$select={sel}&$filter={flt}"
    rows=[]
    while u:
        j=S.get(u, timeout=180).json(); rows+=j['value']; u=j.get('odata.nextLink')
        if u and not u.startswith('http'): u=B+'/'+u
    P("NL filter B rows:", len(rows))
df=pd.DataFrame(rows)
for c in ['Geslacht','Leeftijd','Geboorteland','Herkomst','Opleiding','Huishoudensinkomen','Perioden']:
    df[c]=df[c].astype(str).str.strip()
df.to_csv('nl_raw.csv',index=False)
P("cols:",list(df.columns)); P(df.head(3).to_string())
P("periods:",sorted(df.Perioden.unique()))
ti=S.get(f"{B}/TableInfos?$format=json",timeout=60).json()['value'][0]
open('nl_tableinfo.json','w').write(json.dumps(ti,ensure_ascii=False))
txt=(ti.get('ShortDescription') or '')
import re
P("--- provisional mentions ---")
for m in re.finditer(r'[^.]*[Vv]oorlopig[^.]*\.', txt): P("  ", m.group(0).strip()[:300])
open('nl_filter.txt','w').write(url)
