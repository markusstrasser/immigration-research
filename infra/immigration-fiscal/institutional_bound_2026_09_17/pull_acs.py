#!/usr/bin/env python3
"""Pull ACS 2024 1-year PUMS tabulations (TYPEHUGQ x SEX) by age band for four groups.

Census API `tabulate` endpoint. One call per (group, age band): col+TYPEHUGQ, row+SEX,
filtered to the band and the group. Raw JSON cached under _cache/.
Out: derived/acs_cells.csv  (group, band, sex, typehugq, weighted_count)
"""
import csv, json, os, pathlib, re, sys, time, urllib.request

HERE = pathlib.Path(__file__).parent
CACHE = HERE / "_cache"; CACHE.mkdir(exist_ok=True)
(HERE / "derived").mkdir(exist_ok=True)
YEAR = "2024"

BANDS = [("0_17", "0:17"), ("18_24", "18:24"), ("25_34", "25:34"), ("35_44", "35:44"),
         ("45_54", "45:54"), ("55_64", "55:64"), ("65_74", "65:74"), ("75_99", "75:99")]
GROUPS = {
    "mexico_born":      "&POBP=303",
    "usborn_mexican":   "&NATIVITY=1&HISP=02",
    "native_nh_white":  "&NATIVITY=1&HISP=01&RAC1P=1",
    "all_natives":      "&NATIVITY=1",
}

def key():
    k = os.environ.get("CENSUS_API_KEY")
    if not k:
        m = re.search(r'CENSUS_API_KEY="?([A-Za-z0-9]+)',
                      (HERE.parent / "acquire/config.local.env").read_text())
        k = m.group(1)
    return k

K = key()

def get(name, extra):
    out = CACHE / f"{name}.json"
    if not out.exists():
        url = (f"https://api.census.gov/data/{YEAR}/acs/acs1/pums?tabulate=weight(PWGTP)"
               f"&col+TYPEHUGQ&row+SEX{extra}&key={K}")
        for attempt in range(4):
            try:
                out.write_bytes(urllib.request.urlopen(url, timeout=180).read()); break
            except Exception as e:
                print(f"  ! {name} attempt {attempt+1}: {e}")
                if attempt == 3: raise
                time.sleep(5)
        time.sleep(1)
    return json.loads(out.read_text())

def parse(d):
    """-> {(sex, typehugq): count}. Header: leading dicts are column (TYPEHUGQ) values."""
    hdr = d[0]
    tcols = {list(h.values())[0]: i for i, h in enumerate(hdr) if isinstance(h, dict)}
    nrowdims = len(hdr) - len(tcols)
    assert nrowdims == 1, f"expected 1 row dim, got {nrowdims}: {hdr}"
    out = {}
    for r in d[1:]:
        sex = str(r[len(tcols)])
        for gq, i in tcols.items():
            out[(sex, str(gq))] = r[i]
    return out

rows = []
for g, pred in GROUPS.items():
    for bname, brange in BANDS:
        print(f"[fetch] {g} {bname}")
        t = parse(get(f"{g}__{bname}", f"{pred}&AGEP={brange}"))
        for (sex, gq), n in sorted(t.items()):
            rows.append(dict(group=g, band=bname, sex=sex, typehugq=gq, weighted=n))

# Gate 1 replication call: exactly the 2026-09-16 lane's cell.
gate = parse(get("gate_usborn_mex_m18_39", "&NATIVITY=1&HISP=02&SEX=1&AGEP=18:39"))
gate_inst = sum(v for (s, gq), v in gate.items() if gq == "2")
print(f"[gate] fresh institutional count, US-born Mexican men 18-39, 2024 = {gate_inst}")

with open(HERE / "derived/acs_cells.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["group", "band", "sex", "typehugq", "weighted"])
    w.writeheader(); w.writerows(rows)
json.dump({"gate_fresh_institutional_usborn_mexican_men_18_39_2024": gate_inst},
          open(HERE / "derived/gate_raw.json", "w"), indent=1)
print(f"✓ wrote {len(rows)} cells")
