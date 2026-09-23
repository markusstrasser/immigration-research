"""Sum the Government Finance Database's administration columns to county areas, census years only.

The archive's 2.9 GB CSV is Deflate64-compressed, which Python's zipfile cannot read, so it is
streamed through `unzip -p` and never written to disk. Local units only (Type_Code 1-5), grouped
by the unit's own FIPS state and county. Amounts are thousands of dollars, as in the Census files.

Census-of-governments years only (1992-2022 every five years): the other years are samples.
Output: _cache/gfd_admin_county.csv (ignored). Diagnostics: row counts by Year4, parse failures.
"""
import csv
import io
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
ZIP = ROOT / "sources/immigration-fiscal/data/external/government_finance_database/gfd_entire.zip"
MEMBER = "The Government Finance Database_All Data.csv"
OUT = HERE / "_cache" / "gfd_admin_county.csv"
YEARS = {"1992", "1997", "2002", "2007", "2012", "2017", "2022"}
COLS = {  # lane label -> GFD column
    "e23": "Fin_Admin_Current_Exp", "e29": "Cen_Staff_Current_Exp", "e31": "Gen_Pub_Bldg_Current_Exp",
    "e25": "Judicial_Current_Exp",
    "d23": "Fin_Admin_Direct_Exp", "d29": "Cen_Staff_Direct_Exp", "d31": "Gen_Pub_Bldg_Total_Exp",
    "d25": "Judicial_Direct_Expend", "direct_general": "Direct_General_Expend",
}


def main():
    if not ZIP.exists():
        raise SystemExit(f"[BLOCKED] missing source {ZIP}")
    proc = subprocess.Popen(["unzip", "-p", str(ZIP), MEMBER], stdout=subprocess.PIPE)
    stream = io.TextIOWrapper(proc.stdout, encoding="latin-1", newline="")
    header = next(csv.reader([stream.readline()]))
    ix = {h.strip(): i for i, h in enumerate(header)}
    missing = [c for c in list(COLS.values()) + ["Year4", "Type_Code", "FIPS_Code_State", "FIPS_County"] if c not in ix]
    if missing:
        proc.kill()
        raise SystemExit(f"[BLOCKED] GFD columns missing: {missing}")
    iy, it, ist, ico = ix["Year4"], ix["Type_Code"], ix["FIPS_Code_State"], ix["FIPS_County"]
    width = len(header)
    years = Counter()
    bad = Counter()
    tot = defaultdict(lambda: defaultdict(float))
    types = defaultdict(Counter)
    for n, line in enumerate(stream, 1):
        head = line.split(",", 3)
        if len(head) < 4:
            bad["short"] += 1
            continue
        years[head[2]] += 1
        if head[2] not in YEARS:
            continue
        row = next(csv.reader([line]))
        if len(row) != width:
            bad["width"] += 1
            continue
        typ = row[it].strip()
        if typ not in ("1", "2", "3", "4", "5"):
            continue
        st, co = row[ist].strip(), row[ico].strip()
        if not (st.isdigit() and co.isdigit()):
            bad["nofips"] += 1
            continue
        key = (f"{int(st):02d}{int(co):03d}", head[2])
        types[key][typ] += 1
        for label, col in COLS.items():
            v = row[ix[col]].strip()
            if v:
                tot[key][label] += float(v)
        if n % 1_000_000 == 0:
            print(f"  {n:,} lines", flush=True)
    rc = proc.wait()
    if rc != 0:
        raise SystemExit(f"[BLOCKED] unzip exited {rc}")
    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["fips", "year", "n_units", "n_county_govt", "n_municipal", "n_township"] + list(COLS))
        for key in sorted(tot):
            t = types[key]
            w.writerow([key[0], key[1], sum(t.values()), t["1"], t["2"], t["3"]]
                       + [f"{tot[key].get(c, 0.0):.1f}" for c in COLS])
    print("rows by Year4:", dict(sorted(years.items())), flush=True)
    print("parse problems:", dict(bad), flush=True)
    print(f"[done] {OUT} {len(tot)} county-years", flush=True)
    if bad["width"]:
        raise SystemExit("[BLOCKED] rows with unexpected width; multi-line fields need a full csv reader")
    return 0


if __name__ == "__main__":
    sys.exit(main())
