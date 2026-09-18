import pyreadstat
d,meta=pyreadstat.read_dta("raw/GSS_stata/gss7224_r3a.dta", metadataonly=True, encoding="latin1")
SKIP=set("dijmnprsuxyz")
for v in ["helppoor","helpnot","eqwlth","natfare","immcrime","letin1"]:
    k=meta.variable_to_label.get(v); print("==",v,"|",meta.column_names_to_labels.get(v))
    if k:
        for kk,vv in meta.value_labels[k].items():
            if str(kk) not in SKIP: print("   ",kk,"=",vv)
