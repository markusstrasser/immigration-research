import json,pathlib,csv,urllib.request,re,time
H=pathlib.Path(__file__).resolve().parent; C=H/"_cache"
KEY=re.search(r'CENSUS_API_KEY=(\S+)',open(H.parent/"acquire/config.local.env").read()).group(1).strip('"')
ST={"48":"Texas","06":"California","04":"Arizona","12":"Florida","*":"US"}
def tab(y,st,lab):
    d={k:v for v,k in json.loads((C/f"h{y}_{st.replace('*','us')}_{lab}.json").read_text())[1:]}
    return {k:int(v) for k,v in d.items()}
def racetab(y,st,pred,tag):
    f=C/f"p{y}_{st.replace('*','us')}_{tag}.json"
    t=json.loads(f.read_text()); return sum(int(r[0]) for r in t[1:])
rows=[]
for y in (2010,2023):
    for st,nm in ST.items():
        a=tab(y,st,"all"); u=tab(y,st,"usborn")
        tot=sum(a.values()); nh=a["01"]; mex=a["02"]; oth=tot-nh-mex
        hisp_us=sum(v for k,v in u.items() if k!="01")
        nhw=racetab(y,st,"","NH_white"); nhb=racetab(y,st,"","NH_Black"); nha=racetab(y,st,"","NH_Asian")
        for g,v in [("Hispanic Mexican",mex),("Other Hispanic",oth),("NH white",nhw),("NH Black",nhb),
                    ("NH Asian",nha),("Hispanic US-born (any origin)",hisp_us),("All Hispanic",tot-nh)]:
            rows.append([y,nm,g,v,tot,round(100*v/tot,2)])
w=csv.writer(open(H/"acs_under30.csv","w",newline="")); w.writerow(["year","geo","group","pop_under30","total_under30","pct"]); w.writerows(rows)
import collections
print(f"{'geo':12}{'group':30}{'2010%':>8}{'2023%':>8}{'delta':>8}")
d={(r[0],r[1],r[2]):r[5] for r in rows}
for st,nm in ST.items():
    for g in ["Hispanic Mexican","Other Hispanic","All Hispanic","NH white","NH Black","NH Asian","Hispanic US-born (any origin)"]:
        print(f"{nm:12}{g:30}{d[(2010,nm,g)]:8.2f}{d[(2023,nm,g)]:8.2f}{d[(2023,nm,g)]-d[(2010,nm,g)]:+8.2f}")
# GATE (a): TX under-30 total vs B01001 2023 acs1
u=f"https://api.census.gov/data/2023/acs/acs1?get=group(B01001)&for=state:48&key={KEY}"
f=C/"b01001_tx_2023.json"
if not f.exists(): f.write_bytes(urllib.request.urlopen(u,timeout=180).read())
b=json.loads(f.read_text()); hdr=b[0]; row=b[1]
M=["B01001_003E","B01001_004E","B01001_005E","B01001_006E","B01001_007E","B01001_008E","B01001_009E","B01001_010E","B01001_011E"]
F=[f"B01001_{n:03d}E" for n in range(27,36)]
tot_b=sum(int(row[hdr.index(c)]) for c in M+F)
tx=[r for r in rows if r[0]==2023 and r[1]=="Texas"][0][4]
print(f"\nGATE(a) TX under-30: PUMS={tx:,} B01001={tot_b:,} diff={100*(tx-tot_b)/tot_b:+.2f}%  -> {'PASS' if abs(tx-tot_b)/tot_b<0.01 else 'FAIL'}")
