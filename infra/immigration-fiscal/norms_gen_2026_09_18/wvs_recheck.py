"""Independent recomputation of the WVS7 Mexico-vs-US anchors from the microdata,
written without reading the fetch agent's script, to check its reported numbers."""
import pandas as pd, numpy as np, sys
SRC = sys.argv[1]
COLS = ["B_COUNTRY_ALPHA","A_YEAR","W_WEIGHT","Q235","Q236","Q237","Q238","Q250",
        "Q69","Q70","Q71","Q73"]
head = pd.read_csv(SRC, nrows=0, low_memory=False).columns.tolist()
missing = [c for c in COLS if c not in head]
assert not missing, f"missing columns: {missing}"
d = pd.read_csv(SRC, usecols=COLS, low_memory=False)
d = d[d.B_COUNTRY_ALPHA.isin(["MEX","USA"])].copy()
for c in COLS:
    if c != "B_COUNTRY_ALPHA": d[c] = pd.to_numeric(d[c], errors="coerce")
print("rows:", d.groupby(["B_COUNTRY_ALPHA","A_YEAR"]).size().to_dict())
print("W_WEIGHT sum vs n:",
      {k: (round(float(g.W_WEIGHT.sum()),1), len(g)) for k,g in d.groupby("B_COUNTRY_ALPHA")})
def share(col, good, lo=1, hi=4):
    out={}
    for k,g in d.groupby("B_COUNTRY_ALPHA"):
        v=g[col]; m=v.between(lo,hi)              # valid responses only
        w=g.W_WEIGHT.where(m)
        out[k]=round(100*float((w*v.isin(good)).sum()/w.sum()),1)
    return out
REG=[("Q235","strong leader",[1,2],1,4),("Q238","democratic political system",[1,2],1,4),
     ("Q236","experts decide",[1,2],1,4),("Q237","army rule",[1,2],1,4),
     ("Q69","confidence police",[1,2],1,4),("Q70","confidence courts",[1,2],1,4),
     ("Q71","confidence government",[1,2],1,4),("Q73","confidence parliament",[1,2],1,4)]
REPORTED={"Q235":(71.6,38.1),"Q238":(75.8,85.0),"Q236":(76.2,52.6),"Q237":(45.5,20.9),
          "Q69":(21.3,68.8),"Q70":(22.5,57.8),"Q71":(17.4,33.7),"Q73":(14.6,15.1)}
bad=0
print(f"\n{'item':32s} {'MEX mine':>9s} {'MEX rep':>8s} {'USA mine':>9s} {'USA rep':>8s}")
for col,lab,good,lo,hi in REG:
    s=share(col,good,lo,hi); rm,ru=REPORTED[col]
    okm, oku = abs(s['MEX']-rm)<0.15, abs(s['USA']-ru)<0.15
    bad += (not okm)+(not oku)
    print(f"{lab:32s} {s['MEX']:9.1f} {rm:8.1f} {s['USA']:9.1f} {ru:8.1f}  {'ok' if okm and oku else 'MISMATCH'}")
# Q250, 1-10 importance of democracy
for k,g in d.groupby("B_COUNTRY_ALPHA"):
    v=g.Q250; m=v.between(1,10); w=g.W_WEIGHT.where(m)
    mean=float((w*v).sum()/w.sum()); hi3=100*float((w*v.ge(8)).sum()/w.sum())
    rep={"MEX":(8.30,72.0),"USA":(8.28,71.3)}[k]
    okm=abs(mean-rep[0])<0.015 and abs(hi3-rep[1])<0.15; bad += not okm
    print(f"{'importance of democracy '+k:32s} mean {mean:.2f} (rep {rep[0]}), 8-10 {hi3:.1f}% (rep {rep[1]}%)  {'ok' if okm else 'MISMATCH'}")
print("\nRECHECK:", "PASS" if bad==0 else f"{bad} MISMATCHES")
sys.exit(1 if bad else 0)
