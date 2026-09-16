import json
d=json.load(open('raw_13je_2023.json'))
ids=d['id']; sizes=d['size']; val=d['value']; dim=d['dimension']
print(ids,sizes)
def cat(c):
    x=dim[c]['category']; return x['index'], x['label']
residx,reslab=cat('valtio_34_20220101'); nidx,nlab=cat('valtio_19_20190101'); cidx,clab=cat('contentscode')
st=[1]*len(sizes)
for i in range(len(sizes)-2,-1,-1): st[i]=st[i+1]*sizes[i+1]
def get(res,nat,cc):
    p=0*st[0]+residx[res]*st[1]+nidx[nat]*st[2]+0*st[3]+0*st[4]+cidx[cc]*st[5]
    return val[p]
out={}
for nat in nidx:
    out[nlab[nat]]={r:{c:get(r,nat,c) for c in cidx} for r in residx}
json.dump(out,open('je_parsed.json','w'),indent=1)
for k in ['TOTAL','Finland','FOREIGN COUNTRIES, TOTAL','Syria','Afghanistan','Iraq','Somalia','Iran','Sweden','Estonia','Ukraine','Russian Federation','Democratic Republic of the Congo']:
    if k in out: print(k, out[k])
