import json, csv
d=json.load(open('raw_13jg_2023.json'))
ids=d['id']; sizes=d['size']; val=d['value']; dim=d['dimension']
def cat(c): 
    x=dim[c]['category']; return x['index'], x['label']
nidx,nlab=cat('valtio_19_20190101'); ridx,rlab=cat('rikokset_74_20211209'); cidx,clab=cat('contentscode')
# strides
st=[1]*len(sizes)
for i in range(len(sizes)-2,-1,-1): st[i]=st[i+1]*sizes[i+1]
def get(nat,ri,cc):
    pos = 0*st[0] + nidx[nat]*st[1] + ridx[ri]*st[2] + 0*st[3] + cidx[cc]*st[4]
    return val[pos]
rows=[]
for nat in nidx:
    r={'code':nat,'name':nlab[nat]}
    for ri,rn in (('231T241','sex'),('101T603','all')):
        for cc,cn in (('ep_lkm','events'),('ep_lkm_vaesto','events_p10k'),('ep_lkm_nimike','headings'),('ep_lkm_nimike_vaesto','headings_p10k'),('ep_lkm_tork','persons_agg'),('ep_lkm_tork_vaesto','persons_agg_p10k')):
            r[f'{rn}_{cn}']=get(nat,ri,cc)
    rows.append(r)
json.dump(rows,open('fi_parsed.json','w'),indent=1)
chart={'Syria':125.74,'Congo':101.60,'Afghanistan':99.76,'Iraq':85.54,'Somalia':52.37,'Iran':38.35,'Sweden':27.00,'Estonia':12.02,'Ukraine':11.39,'Finland':8.12,'Russia':6.22}
byname={r['name']:r for r in rows}
print(f"{'name':<28}{'chart':>8}{'evP10k':>10}{'hdgP10k':>10}{'aggP10k':>10}{'events':>8}{'hdgs':>8}{'pers':>7}")
for k,v in chart.items():
    cands=[n for n in byname if k.lower() in n.lower()]
    for n in cands:
        r=byname[n]
        print(f"{n:<28}{v:>8.2f}{str(r['sex_events_p10k']):>10}{str(r['sex_headings_p10k']):>10}{str(r['sex_persons_agg_p10k']):>10}{str(r['sex_events']):>8}{str(r['sex_headings']):>8}{str(r['sex_persons_agg']):>7}")
    if not cands: print(f"{k:<28}{v:>8.2f}  NOT FOUND")
print()
for k in ('TOTAL','Finland','FOREIGN COUNTRIES, TOTAL'):
    r=byname.get(k)
    if r: print(k, 'sex events', r['sex_events'], 'headings', r['sex_headings'], 'persons_agg', r['sex_persons_agg'], '| p10k', r['sex_events_p10k'], r['sex_headings_p10k'], r['sex_persons_agg_p10k'])
