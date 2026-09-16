import json
d=json.load(open('raw_13jg_allyears.json'))
sizes=d['size']; val=d['value']; dim=d['dimension']
tidx=dim['timeperiod_y']['category']['index']
nidx=dim['valtio_19_20190101']['category']['index']; nlab=dim['valtio_19_20190101']['category']['label']
cidx=dim['contentscode']['category']['index']
st=[1]*len(sizes)
for i in range(len(sizes)-2,-1,-1): st[i]=st[i+1]*sizes[i+1]
def g(y,n,c): return val[tidx[y]*st[0]+nidx[n]*st[1]+0*st[2]+0*st[3]+cidx[c]*st[4]]
chart={'760':125.74,'180':101.60,'004':99.76,'368':85.54,'706':52.37,'364':38.35,'752':27.00,'233':12.02,'804':11.39,'246':8.12,'643':6.22}
for c in ['ep_lkm_vaesto','ep_lkm_nimike_vaesto','ep_lkm_tork_vaesto']:
    print('===',c)
    best=[]
    for y in tidx:
        devs=[]; ok=True
        for n,cv in chart.items():
            v=g(y,n,c)
            if v is None: ok=False; break
            devs.append(abs(v-cv)/cv)
        if ok: best.append((sum(devs)/len(devs),y))
    best.sort()
    for s,y in best[:4]: print(f'  year {y} mean |rel dev| {s:.3f}')
    by=best[0][1]
    print('   best year detail:', by)
    for n,cv in chart.items(): print(f'     {nlab[n]:<32} chart={cv:>7.2f} statfin={g(by,n,c)}')
