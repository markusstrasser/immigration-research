import json, itertools
d=json.load(open('raw_13jg_grid.json'))
sizes=d['size']; val=d['value']; dim=d['dimension']
print('nvals',len(val),'expected',sizes[0]*sizes[1]*sizes[4])
tI=dim['timeperiod_y']['category']['index']; years=list(tI)
nI=dim['valtio_19_20190101']['category']['index']; nL=dim['valtio_19_20190101']['category']['label']
cI=dim['contentscode']['category']['index']
st=[1]*len(sizes)
for i in range(len(sizes)-2,-1,-1): st[i]=st[i+1]*sizes[i+1]
def g(y,n,c): return val[tI[y]*st[0]+nI[n]*st[1]+cI[c]*st[4]]
# derived population per year/nationality
def pop(y,n):
    a=g(y,n,'ep_lkm'); b=g(y,n,'ep_lkm_vaesto')
    if a and b: return a/b*10000
    a=g(y,n,'ep_lkm_nimike'); b=g(y,n,'ep_lkm_nimike_vaesto')
    if a and b: return a/b*10000
    return None
chart={'760':125.74,'180':101.60,'004':99.76,'368':85.54,'706':52.37,'364':38.35,'752':27.00,'233':12.02,'804':11.39,'246':8.12,'643':6.22}
res=[]
for ny in years:
    for py in years:
        for num in ['ep_lkm','ep_lkm_nimike','ep_lkm_tork']:
            devs=[]; ok=True
            for n,cv in chart.items():
                N=g(ny,n,num); P=pop(py,n)
                if N is None or P is None: ok=False; break
                devs.append(abs(N/P*10000-cv)/cv)
            if ok: res.append((sum(devs)/len(devs),ny,py,num))
res.sort()
for r in res[:8]: print(f'{r[0]:.4f}  num_year={r[1]} pop_year={r[2]} numerator={r[3]}')
best=res[0]
print()
print('BEST detail', best)
for n,cv in chart.items():
    N=g(best[1],n,best[3]); P=pop(best[2],n)
    print(f'  {nL[n]:<34} chart={cv:>7.2f} calc={N/P*1e4:>7.2f}  N={N} P={P:.0f}')
