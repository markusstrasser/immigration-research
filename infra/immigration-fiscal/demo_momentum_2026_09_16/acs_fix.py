import json,re,pathlib,urllib.request,csv,time
H=pathlib.Path(__file__).resolve().parent; C=H/"_cache"
KEY=re.search(r'CENSUS_API_KEY=(\S+)',open(H.parent/"acquire/config.local.env").read()).group(1).strip('"')
ST={"48":"Texas","06":"California","04":"Arizona","12":"Florida","*":"US"}
def get(url,tag):
    f=C/f"{tag}.json"
    if not f.exists(): f.write_bytes(urllib.request.urlopen(url+f"&key={KEY}",timeout=300).read()); time.sleep(1)
    return json.loads(f.read_text())
def hisp_tab(year,st,extra,tag):
    g="" if st=="*" else f"&for=state:{st}"
    u=f"https://api.census.gov/data/{year}/acs/acs1/pums?tabulate=weight(PWGTP)&row+HISP&AGEP=0:29{extra}{g}"
    t=get(u,tag); hdr=t[0]
    out={}
    for r in t[1:]:
        # last cols may be 'state'; row label is the HISP value column
        vals=[v for v in r if isinstance(v,str) and v.isdigit()]
        pass
    return t
rows=[]
for year in (2010,2023):
    for st,nm in ST.items():
        for lab,extra in (("all",""),("usborn","&NATIVITY=1")):
            t=hisp_tab(year,st,extra,f"h{year}_{st.replace('*','us')}_{lab}")
            hdr=t[0]
            # find index of HISP label column: tabulate returns cols for row categories
            print(year,nm,lab,json.dumps(t)[:400])
