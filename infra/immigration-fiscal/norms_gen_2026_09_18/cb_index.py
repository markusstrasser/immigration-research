import re, sys, json
SRC={"2020":"../attitudes_gen_2026_09_16/cb_2020.txt","2024":"../attitudes_gen_2026_09_16/cb_2024.txt"}
out={}
for yr,p in SRC.items():
    txt=open(p, encoding="utf-8", errors="replace").read()
    lines=txt.split("\n")
    idx={}
    for i,l in enumerate(lines):
        m=re.match(r"^(V\d{6}x?)\s*(P(RE|OST)|SPS)?[:\s]*(.*)$", l.strip())
        if m:
            title=m.group(4).strip()
            # titles wrap onto the next line(s) in the extraction
            j=i+1
            while j<len(lines) and j<i+3 and lines[j].strip() and not re.match(r"^(V\d{6}|Question|Value|Universe|Survey|Response|Interviewer|Randomi|Note|CODEBOOK|PRE-|POST)", lines[j].strip()):
                title+=" "+lines[j].strip(); j+=1
            idx[m.group(1)]=title[:120]
    out[yr]=idx
    print(yr, len(idx), "variables indexed")
json.dump(out, open("derived/cb_index.json","w"), indent=0)
pats=sys.argv[1:]
for yr in out:
    print("#####", yr)
    for v,t in out[yr].items():
        if any(re.search(p, t, re.I) for p in pats):
            print(f"  {v}  {t}")
