from pypdf import PdfReader
import re,sys
paths={"2020":"raw/anes_timeseries_2020_csv_20220210/anes_timeseries_2020_userguidecodebook_20220210.pdf",
       "2024":"raw/anes_timeseries_2024_csv_20260519/anes_timeseries_2024_userguidecodebook_20260519.pdf"}
pats=[r"THERMOMETER.{0,80}", r"Hispanic", r"born in", r"parents", r"WEIGHT", r"stratum", r"cluster|PSU"]
for yr,p in paths.items():
    r=PdfReader(p); print("==",yr,"pages",len(r.pages))
    txt=[]
    for i,pg in enumerate(r.pages):
        t=pg.extract_text() or ""
        txt.append(t)
    full="\n".join(txt)
    open(f"cb_{yr}.txt","w").write(full)
    print("chars",len(full))
