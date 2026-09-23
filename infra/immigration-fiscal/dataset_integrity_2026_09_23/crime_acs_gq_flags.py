"""Crime family: ACS 2024 1-year allocation flags among institutional residents 18-64.

Tabulates, by TYPEHUGQ, the birthplace (FPOBP), citizenship (FCITP), age (FAGEP), sex (FSEXP),
Hispanic origin (FHISP) and year-of-entry (FYOEP) flags for Mexican-coded (HISP=02),
generic "Other Hispanic" (HISP=24) and non-Hispanic residents, crossed with NATIVITY.
Tests whether allocated birthplaces land on US-born (the 2000-census trap) in the custody key's
own file, and whether item flags are set at all in institutional records.
Run from the repo root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/dataset_integrity_2026_09_23/crime_acs_gq_flags.py
"""
import csv, json, os, pathlib, re, sys, urllib.request

HERE = pathlib.Path(__file__).resolve().parent
CACHE = HERE / "_cache"
ENV = HERE.parent / "acquire" / "config.local.env"
BASE = "https://api.census.gov/data/2024/acs/acs1/pums?tabulate=weight(PWGTP)&col+TYPEHUGQ&AGEP=18:64"
QUERIES = {f"crime_{flag}_{h}": f"{BASE}&row+{flag}&row+NATIVITY&HISP={h}"
           for flag in ("FPOBP", "FCITP", "FAGEP", "FSEXP", "FHISP", "FYOEP", "FRACP")
           for h in ("01", "02", "24")}


def key():
    m = re.search(r"CENSUS_API_KEY=\"?([A-Za-z0-9]+)", ENV.read_text())
    if not m:
        sys.exit("[BLOCKED] CENSUS_API_KEY missing")
    return m.group(1)


def get(name, url):
    out = CACHE / f"{name}.json"
    if not out.exists():
        k = key()
        try:
            body = urllib.request.urlopen(f"{url}&key={k}", timeout=300).read()
        except Exception as e:
            sys.exit(f"[BLOCKED] fetch {name}: {str(e).replace(k, '<KEY>')}")
        json.loads(body)
        CACHE.mkdir(exist_ok=True)
        out.write_bytes(body)
    return json.loads(out.read_text())


rows = []
for name, url in QUERIES.items():
    tab = get(name, url)
    hdr = tab[0]
    col = {list(h.values())[0]: i for i, h in enumerate(hdr) if isinstance(h, dict)}
    nrow = len(col)
    _, flag, h = name.split("_")
    for r in tab[1:]:
        fl, nat = str(r[nrow]), str(r[nrow + 1])
        for gq, lab in (("1", "hh"), ("2", "inst"), ("3", "noninst")):
            rows.append(dict(flag=flag, hisp=h, flag_value=fl, nativity=nat, gq=lab, weighted=round(r[col[gq]])))
out = HERE / "derived" / "crime_acs2024_gq_flags.csv"
out.parent.mkdir(exist_ok=True)
with open(out, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader(); w.writerows(rows)
print(f"wrote {out} rows={len(rows)}")
