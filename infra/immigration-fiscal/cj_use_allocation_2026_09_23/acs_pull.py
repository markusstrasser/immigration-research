"""ACS PUMS tabulations for the custody and scaling keys of the use-weighted justice allocation.

Institutional group-quarters residence (TYPEHUGQ=2) by Hispanic origin (HISP) x nativity, ages 18-64,
both sexes, plus all-age and 12+ population counts for the Hispanic -> Mexican-origin scaling.
Same construction as ../acs_institutional_2026_09_16/pull_and_compute.py, which covered men 18-39 only.
TYPEHUGQ=2 pools correctional, nursing, psychiatric and juvenile institutions and can include ICE
detention; public PUMS cannot split them.

Run from the repository root:
    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/cj_use_allocation_2026_09_23/acs_pull.py
Writes _cache/*.json (ignored), derived/acs_hisp_nativity_gq.csv and derived/acs2019_adults.csv.
Skips fetches already cached.
"""
import csv, json, os, pathlib, re, sys, urllib.request

HERE = pathlib.Path(__file__).resolve().parent
CACHE = HERE / "_cache"
DERIVED = HERE / "derived"
ENV = HERE.parent / "acquire" / "config.local.env"
PRODUCTS = {"acs1_2024": "https://api.census.gov/data/2024/acs/acs1/pums",
            "acs5_2024": "https://api.census.gov/data/2024/acs/acs5/pums"}
AGES = {"1864": "&AGEP=18:64", "12up": "&AGEP=12:99", "all": ""}


def key() -> str:
    k = os.environ.get("CENSUS_API_KEY", "")
    if not k:
        m = re.search(r"CENSUS_API_KEY=\"?([A-Za-z0-9]+)", ENV.read_text())
        k = m.group(1) if m else ""
    if not k:
        sys.exit("[BLOCKED] CENSUS_API_KEY missing")
    return k


def fetch(product: str, age: str) -> list:
    out = CACHE / f"acs_{product}_{age}.json"
    if not out.exists():
        k = key()
        url = (f"{PRODUCTS[product]}?tabulate=weight(PWGTP)&col+TYPEHUGQ&row+NATIVITY&row+HISP"
               f"{AGES[age]}&key={k}")
        try:
            body = urllib.request.urlopen(url, timeout=300).read()
        except Exception as e:  # never let the key reach a log
            sys.exit(f"[BLOCKED] fetch {product} {age}: {str(e).replace(k, '<KEY>')}")
        json.loads(body)
        CACHE.mkdir(exist_ok=True)
        out.write_bytes(body)
    return json.loads(out.read_text())


def fetch_b01001_2019() -> dict:
    """ACS 2019 1-year adults 18+: all residents (B01001) and Hispanic (B01001I), the FBI 2019 arrest year."""
    under18 = {"B01001": ["003", "004", "005", "006", "027", "028", "029", "030"],
               "B01001I": ["003", "004", "005", "006", "018", "019", "020", "021"]}
    res = {}
    for tbl, cells18 in under18.items():
        out = CACHE / f"acs1_2019_{tbl}.json"
        if not out.exists():
            k = key()
            names = ",".join([f"{tbl}_001E"] + [f"{tbl}_{c}E" for c in cells18])
            url = f"https://api.census.gov/data/2019/acs/acs1?get={names}&for=us:1&key={k}"
            try:
                body = urllib.request.urlopen(url, timeout=120).read()
            except Exception as e:
                sys.exit(f"[BLOCKED] fetch {tbl} 2019: {str(e).replace(k, '<KEY>')}")
            json.loads(body)
            out.write_bytes(body)
        hdr, row = json.loads(out.read_text())
        v = {h: float(x) for h, x in zip(hdr, row) if h.endswith("E")}
        res[tbl] = {"total": v[f"{tbl}_001E"], "adult18": v[f"{tbl}_001E"] - sum(v[f"{tbl}_{c}E"] for c in cells18)}
    return res


def cells(tab: list) -> dict:
    """(nativity, hisp) -> {'hh', 'inst', 'noninst', 'total'} weighted persons."""
    hdr = tab[0]
    col = {list(h.values())[0]: i for i, h in enumerate(hdr) if isinstance(h, dict)}
    res = {}
    for r in tab[1:]:
        nat, hisp = str(r[len(col)]), str(r[len(col) + 1])
        v = {"hh": r[col["1"]], "inst": r[col["2"]], "noninst": r[col["3"]]}
        v["total"] = v["hh"] + v["inst"] + v["noninst"]
        res[(nat, hisp)] = v
    return res


def main() -> None:
    DERIVED.mkdir(exist_ok=True)
    rows = []
    for product in PRODUCTS:
        for age in AGES:
            c = cells(fetch(product, age))
            for (nat, hisp), v in sorted(c.items()):
                rows.append({"product": product, "ages": age, "nativity": {"1": "native", "2": "foreign_born"}[nat],
                             "hisp": hisp, **{k: round(x) for k, x in v.items()}})
    path = DERIVED / "acs_hisp_nativity_gq.csv"
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {path.relative_to(HERE)} rows={len(rows)}")
    pop19 = fetch_b01001_2019()
    path = DERIVED / "acs2019_adults.csv"
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["table", "group", "total", "adult18"])
        for tbl, grp in (("B01001", "all"), ("B01001I", "hispanic")):
            w.writerow([tbl, grp, round(pop19[tbl]["total"]), round(pop19[tbl]["adult18"])])
    print(f"wrote {path.relative_to(HERE)}")


if __name__ == "__main__":
    main()
