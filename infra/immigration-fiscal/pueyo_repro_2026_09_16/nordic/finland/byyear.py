import json
d=json.load(open('raw_13jg_grid.json'))
sizes=d['size']; val=d['value']; dim=d['dimension']
tI=dim['timeperiod_y']['category']['index']; nI=dim['valtio_19_20190101']['category']['index']
nL=dim['valtio_19_20190101']['category']['label']; cI=dim['contentscode']['category']['index']
st=[1]*len(sizes)
for i in range(len(sizes)-2,-1,-1): st[i]=st[i+1]*sizes[i+1]
def g(y,n,c): return val[tI[y]*st[0]+nI[n]*st[1]+cI[c]*st[4]]
chart={'760':125.74,'180':101.60,'004':99.76,'368':85.54,'706':52.37,'364':38.35,'752':27.00,'233':12.02,'804':11.39,'246':8.12,'643':6.22}
print(f"{'nationality':<32}{'chart':>8}  best-matching year (ep_lkm_vaesto)   series 2015..2025")
for n,cv in chart.items():
    ser={y:g(y,n,'ep_lkm_vaesto') for y in tI}
    cand=[(abs(v-cv),y,v) for y,v in ser.items() if v is not None]
    cand.sort()
    s=' '.join(f"{y[-2:]}:{ser[y]}" for y in [str(x) for x in range(2015,2026)])
    print(f"{nL[n]:<32}{cv:>8.2f}  ->{cand[0][1]}={cand[0][2]}   {s}")
