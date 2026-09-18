"""Fetch one state-year of kid cells with a single-year-of-age split.

The standard puller halves the age range only after a failure; for the largest states a
single-year split keeps every response small enough that the Census API does not reset it.
Usage: python3 fetch_one_state_year.py YEAR STATEFIPS
"""
import csv, os, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import pull_kids as K

year, state = int(sys.argv[1]), sys.argv[2]
out = K.CELLS / f"kids_{year}_{state}.csv"
cols = ["PUMA", "SCH", "AGEP", "RAC1P", "HISP", "NATIVITY", "PWGTP"]
acc, total = {}, 0
for age in range(5, 18):
    hdr, rows = K.pums_split(year, state, cols, age, age, depth=9)
    ix = {c: i for i, c in enumerate(hdr)}
    total += len(rows)
    for r in rows:
        puma = str(r[ix["PUMA"]]).zfill(5)
        sch = K.num(r[ix["SCH"]]); a = K.num(r[ix["AGEP"]])
        g = K.group(K.num(r[ix["RAC1P"]]), K.num(r[ix["HISP"]]), K.num(r[ix["NATIVITY"]]))
        w = K.num(r[ix["PWGTP"]], 0)
        # Guard against the endpoint returning records outside the requested AGEP:
        # that is what inflated California 2010 by a factor of 13 (once per single year
        # of age) in the first pass.
        if g is None or sch is None or a is None or a != age:
            continue
        k = (puma, g, "elem" if a <= 12 else "sec")
        cell = acc.setdefault(k, [0, 0, 0])
        cell[0 if sch == 2 else 1 if sch == 3 else 2] += w
    print(f"  age {age}: {len(rows)} rows (cumulative {total})", flush=True)
tmp = out.with_suffix(f".{os.getpid()}.tmp")
with tmp.open("w", newline="") as f:
    w_ = csv.writer(f); w_.writerow(K.FIELDS)
    for (puma, g, lvl), (pub, priv, no) in sorted(acc.items()):
        w_.writerow([year, state, puma, g, lvl, pub, priv, no])
tmp.rename(out)
print(f"wrote {out} rows={total} cells={len(acc)}")
