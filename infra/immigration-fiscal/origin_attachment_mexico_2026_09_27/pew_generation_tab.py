"""Weighted Pew NSL attachment items for Mexican-origin respondents by generation.

Reads the held Pew zips (dataset register PEW_NSL_*), writes derived/pew_attachment_by_generation.csv.
Generation: 1 = born outside US and PR; 2 = US-born, >=1 parent born outside US/PR; 3+ = US-born, both parents US-born.
Mexican = heritage code 1 ('Mexican (Mexico)'). Other Hispanic = any other known heritage.
"""
import csv, glob, os, tempfile, zipfile
import numpy as np, pyreadstat

RAW = "infra/immigration-fiscal/new_datasets_2026_09_17/raw"
OUT = os.path.join(os.path.dirname(__file__), "derived", "pew_attachment_by_generation.csv")
# file tag: (zip, heritage var, nativity self/mother/father, weight, [items])
SPECS = {
 "NSL2011": ("PHCNSL2011PubRelease.zip", "qn301", ("qn4","qn7","qn8"), "weight", ["qn59"]),
 "NSL2012": ("PHCNSL2012PublicRelease.zip", "qn3", ("qn4","qn7","qn8"), "weight", ["qn78","qn79","qn80"]),
 "REL2013": ("Pew-Research-Center-2013-U.S.-Latino-Religion-Survey.zip", "Q3REC", ("Q4","Q410","Q411"), "totalwt", ["Q111"]),
 "NSL2014": ("Pew-Research-Center_2014-National-Survey-of-Latinos-Dataset.zip", "q3", ("q4","q7","q8"), "weight", ["q50"]),
 "NSL2015": ("Pew-Research-Center_2015-National-Survey-of-Latinos-Dataset.zip", "q3_combo", ("q4","q7","q8"), "weights", ["q13","q16c","q46","q47","q27aa","q64","q59","q63"]),
 "NSL2016": ("Pew-Research-Center_2016-National-Survey-of-Latinos-Dataset.zip", "qn3", ("qn4","qn7","qn8"), "weights", ["qn29c"]),
 "NSL2018": ("Pew-Research-Center_2018-National-Survey-of-Latinos-Dataset.zip", "qn3", ("qn4","qn7","qn8"), "weight", ["qn21bd"]),
}

def load(zname):
    tmp = tempfile.mkdtemp()
    with zipfile.ZipFile(os.path.join(RAW, zname)) as z:
        z.extractall(tmp)
    sav = [f for f in glob.glob(tmp + "/**/*.sav", recursive=True) if "__MACOSX" not in f][0]
    return pyreadstat.read_sav(sav, encoding="latin1")

def generation(df, s, m, f):
    g = np.full(len(df), np.nan)
    g[df[s] == 3] = 1
    us = df[s] == 2
    abroad = (df[m] == 3) | (df[f] == 3) | (df[m] == 1) | (df[f] == 1)
    g[us & abroad] = 2
    g[us & (df[m] == 2) & (df[f] == 2)] = 3
    return g

rows = []
for tag, (zname, her, (s, m, f), w, items) in SPECS.items():
    df, meta = load(zname)
    df["gen"] = generation(df, s, m, f)
    df["grp"] = np.where(df[her] == 1, "Mexican", np.where(df[her].between(2, 97), "OtherHispanic", "unknown"))
    for item in items:
        vl = meta.value_labels.get(meta.variable_to_label.get(item), {})
        label = meta.column_names_to_labels[item]
        for grp in ("Mexican", "OtherHispanic"):
            for gen in (1, 2, 3):
                sub = df[(df.grp == grp) & (df.gen == gen) & df[item].notna() & (df[item] != 0)]
                n = len(sub); wt = sub[w].sum()
                for code, lab in vl.items():
                    if code == 0: continue
                    share = sub.loc[sub[item] == code, w].sum() / wt if wt else np.nan
                    rows.append([tag, item, label[:160], grp, {1:"1st",2:"2nd",3:"3rd+"}[gen], n, code, lab, round(share, 4)])
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", newline="") as fh:
    wr = csv.writer(fh, lineterminator="\n")
    wr.writerow(["survey","item","question","group","generation","n_unweighted","code","answer","weighted_share"])
    wr.writerows(rows)
print("wrote", OUT, len(rows))
