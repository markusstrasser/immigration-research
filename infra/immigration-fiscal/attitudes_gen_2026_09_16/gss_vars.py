import pyreadstat, sys
p="raw/GSS_stata/gss7224_r3a.dta"
df,meta=pyreadstat.read_dta(p, metadataonly=True, encoding="latin1")
names=meta.column_names
want=["year","id","ballot","wtss","wtssall","wtssps","wtssnrps","wtsscomp","vpsu","vstrat",
"born","parborn","granborn","hispanic","ethnic","race","racecen1","trust","eqwlth","helppoor",
"natfare","natfarey","letin1","letin1a","partyid","age","sex","polviews","immcrime","immameco"]
for w in want:
    print(w, "OK" if w in names else "MISSING")
print("n_vars",len(names))
