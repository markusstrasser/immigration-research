"""Under-30 composition by state, ACS 1-year PUMS tabulate, 2010 vs 2023, + B01001 validation."""
import json, os, re, pathlib, urllib.request, csv, time
H=pathlib.Path(__file__).resolve().parent; C=H/"_cache"; C.mkdir(exist_ok=True)
KEY=re.search(r'CENSUS_API_KEY=(\S+)',open(H.parent/"acquire/config.local.env").read()).group(1).strip('"')
ST={"48":"Texas","06":"California","04":"Arizona","12":"Florida","*":"US"}
def get(url,tag):
    f=C/f"{tag}.json"
    if not f.exists():
        f.write_bytes(urllib.request.urlopen(url+f"&key={KEY}",timeout=300).read()); time.sleep(1)
    return json.loads(f.read_text())
def pums(year,st,pred,tag):
    base=f"https://api.census.gov/data/{year}/acs/acs1/pums?tabulate=weight(PWGTP)&row+SEX&AGEP=0:29"
    g="" if st=="*" else f"&for=state:{st}"
    return get(base+"&"+pred+g,tag)
def total(tab):
    hdr=tab[0]; n=len(hdr)
    s=0
    for r in tab[1:]:
        for i,v in enumerate(r):
            if isinstance(v,(int,float)) and i<n-1: s+=v
            elif isinstance(v,str) and v.isdigit() and hdr[i] not in ("state",) and i<n-1: s+=int(v)
    return s
GROUPS={"Hispanic Mexican":"HISP=02","Other Hispanic":"HISP=03:24","NH white":"HISP=01&RAC1P=1",
        "NH Black":"HISP=01&RAC1P=2","NH Asian":"HISP=01&RAC1P=6"}
rows=[]
for year in (2010,2023):
    for st,nm in ST.items():
        tot=None
        vals={}
        for g,pred in GROUPS.items():
            try: t=total(pums(year,st,pred,f"p{year}_{st.replace('*','us')}_{g.replace(' ','_')}"))
            except Exception as e: t=None; print("FAIL",year,nm,g,e)
            vals[g]=t
        # all under 30
        try: tot=total(pums(year,st,"NATIVITY=1:2",f"p{year}_{st.replace('*','us')}_all"))
        except Exception as e: print("FAIL total",year,nm,e)
        # hispanic US-born
        try: hus=total(pums(year,st,"HISP=02:24&NATIVITY=1",f"p{year}_{st.replace('*','us')}_hisp_usborn"))
        except Exception as e: hus=None; print("FAIL hisp-usborn",year,nm,e)
        for g,v in list(vals.items())+[("Hispanic US-born",hus)]:
            rows.append([year,nm,g,v,tot,None if (v is None or not tot) else round(100*v/tot,2)])
with open(H/"acs_under30.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["year","geo","group","pop_under30","total_under30","pct"]); w.writerows(rows)
for r in rows: print(r)
