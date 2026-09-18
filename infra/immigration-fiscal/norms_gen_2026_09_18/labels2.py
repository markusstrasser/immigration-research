import pyreadstat, json
P="raw/GSS_stata/gss7224_r3a.dta"
df,meta=pyreadstat.read_dta(P, metadataonly=True, encoding="latin1")
V=["conarmy","confed","conjudge","conlegis","conpress","consci","coneduc","conbus","confinan","conclerg","conmedic","conlabor","contv",
   "spkath","colath","libath","spkrac","spkmslm","colmslm","libmslm","spkhomo",
   "obey","courts","cappun","gunlaw","polhitok","polabuse","polmurdr","polescap","polattak","grass",
   "amcit","amcitizn","amancstr","amchrstn","amenglsh","amfeel","amgovt","amshamed","ambornin","amcult","amimp","amlived","amproud","amownway",
   "ethnofit","ethadapt","ethspkok","immassim","immcult","immlimit",
   "ethnic","eth1","hispanic","born","parborn","polviews","degree","educ","realinc","coninc","race"]
for v in V:
    k=meta.variable_to_label.get(v)
    print("==",v,"|",meta.column_names_to_labels.get(v))
    if k:
        for kk,vv in list(meta.value_labels[k].items())[:30]: print("    ",kk,"=",vv)
