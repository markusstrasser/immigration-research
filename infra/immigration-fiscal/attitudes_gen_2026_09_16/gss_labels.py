import pyreadstat
p="raw/GSS_stata/gss7224_r3a.dta"
df,meta=pyreadstat.read_dta(p, metadataonly=True, encoding="latin1")
for v in ["born","parborn","hispanic","race","trust","eqwlth","helppoor","natfare","letin1","partyid","immcrime"]:
    k=meta.variable_to_label.get(v)
    print("==",v,"|",meta.column_names_to_labels.get(v))
    if k: 
        for kk,vv in list(meta.value_labels[k].items())[:15]: print("   ",kk,vv)
