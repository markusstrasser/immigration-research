import json, csv, itertools
rows=[]
for iccs in ["ICCS0301","ICCS03011","ICCS03012"]:
    d=json.load(open(f"crim_off_cat_{iccs}.json"))
    geos=d['dimension']['geo']['category']['index']; glab=d['dimension']['geo']['category']['label']
    times=d['dimension']['time']['category']['index']
    nt=len(times); val=d['value']
    inv_g={v:k for k,v in geos.items()}; inv_t={v:k for k,v in times.items()}
    for gi,g in inv_g.items():
        for ti,t in inv_t.items():
            idx=gi*nt+ti
            v=val.get(str(idx))
            rows.append(dict(iccs=iccs,iccs_label=d['dimension']['iccs']['category']['label'][iccs],
                             geo=g,geo_label=glab[g],year=int(t),rate_per_100k=v))
with open("eurostat_sexual_violence_rates.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

# index 2014=100
out=[]
for iccs in ["ICCS0301","ICCS03011","ICCS03012"]:
    for g in sorted({r['geo'] for r in rows}):
        sub={r['year']:r['rate_per_100k'] for r in rows if r['iccs']==iccs and r['geo']==g}
        base=sub.get(2014)
        for y in range(2014,2025):
            v=sub.get(y)
            out.append(dict(iccs=iccs,geo=g,geo_label=[r['geo_label'] for r in rows if r['geo']==g][0],
                            year=y,rate=v,index_2014_100=(round(100*v/base,1) if (v is not None and base) else None))) 
with open("eurostat_index_2014_100.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)

print("=== ICCS0301 Sexual violence, index 2014=100 ===")
names={'FR':'France','DK':'Denmark','UKC-L':'England&Wales','ES':'Spain','IE':'Ireland','DE':'Germany','AT':'Austria','SE':'Sweden','NL':'Netherlands'}
hdr="geo        "+"".join(f"{y:>7}" for y in range(2014,2025)); print(hdr)
for g in ['FR','DK','UKC-L','ES','IE','DE','AT','SE','NL']:
    line=f"{names[g]:<11}"
    for y in range(2014,2025):
        r=[o for o in out if o['iccs']=='ICCS0301' and o['geo']==g and o['year']==y][0]
        line+=f"{(r['index_2014_100'] if r['index_2014_100'] is not None else '.'):>7}"
    print(line)
print()
print("=== ICCS0301 raw rate per 100k ===")
for g in ['FR','DK','UKC-L','ES','IE','DE','AT','SE','NL']:
    line=f"{names[g]:<11}"
    for y in range(2014,2025):
        r=[o for o in out if o['iccs']=='ICCS0301' and o['geo']==g and o['year']==y][0]
        line+=f"{(r['rate'] if r['rate'] is not None else '.'):>7}"
    print(line)
