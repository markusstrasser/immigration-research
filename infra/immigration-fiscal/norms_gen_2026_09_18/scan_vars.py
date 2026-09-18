import pyreadstat
P="raw/GSS_stata/gss7224_r3a.dta"
df,meta=pyreadstat.read_dta(P, metadataonly=True, encoding="latin1")
names=set(meta.column_names)
want = """year id ballot wtss wtssall wtssps wtssnrps wtsscomp vpsu vstrat sampcode sample
born parborn granborn hispanic ethnic eth1 eth2 eth3 race racecen1 racecen2 age educ degree sex polviews realinc coninc income rincome partyid
conarmy conbus conclerg coneduc confed confinan conjudge conlabor conlegis conmedic conpress consci contv
spkath colath libath spkrac colrac librac spkcom colcom libcom spkmil colmil libmil spkhomo colhomo libhomo spkmslm colmslm libmslm
tolerance obey thnkself workhard helpoth popular
courts cappun gunlaw polhitok polabuse polmurdr polescap polattak wiretap grass
eqwlth helppoor helpnot helpsick helpblk natfare natfarey natcity natcrime natheal
amcit amcitizn amgovt amancstr amborn amchrstn amcultr amenglsh amfeel amgovt1 amshamed ampride1 ampatrit amcitizn
letin1 letin1a immcrime immameco immassim immcult immjobs immecon
god attend reliten pray relig fund bible
trust fair helpful
spanking fepres fehome racdif1 racdif2 racdif3 racdif4
""".split()
have=[w for w in want if w in names]
miss=[w for w in want if w not in names]
print("HAVE:", " ".join(sorted(set(have))))
print()
print("MISSING:", " ".join(sorted(set(miss))))
print()
# fuzzy: anything starting with am / con / spk / col / lib / tol
import re
for pre in ["am","con","spk","col","lib","tol","pol","imm","eth","gran","nat"]:
    hits=sorted(n for n in names if n.startswith(pre))
    print(f"[{pre}*] ({len(hits)}):", " ".join(hits))
