import pyreadstat
P="raw/GSS_stata/gss7224_r3a.dta"
df,meta=pyreadstat.read_dta(P, metadataonly=True, encoding="latin1")
V=["spkath","colath","libath","spkrac","spkmslm","colmslm","libmslm","spkhomo",
   "obey","courts","cappun","gunlaw","polhitok","polabuse","polmurdr","polescap","polattak","grass",
   "amcit","amcitizn","amancstr","amchrstn","amenglsh","amfeel","amgovt","amshamed","ambornin","amcult","amimp","amlived","amproud","amownway",
   "ethnofit","ethadapt","ethspkok","immassim","immcult","immlimit",
   "eth1","hispanic","polviews","degree","coninc","race"]
SKIP={"d","i","j","m","n","p","r","s","u","x","y","z"}
for v in V:
    k=meta.variable_to_label.get(v)
    print("==",v,"|",meta.column_names_to_labels.get(v))
    if k:
        items=[(kk,vv) for kk,vv in meta.value_labels[k].items() if str(kk) not in SKIP]
        for kk,vv in items[:30]: print("    ",kk,"=",vv)
