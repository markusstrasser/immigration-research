"""County Business Patterns 2012-2023 by county for restaurants, mobile food and a grocery placebo.

Pulls ESTAB, EMP (mid-March) and PAYANN ($1,000) from the Census CBP API for every county, all
legal forms and all size classes, for:
  722    food services and drinking places (gate and context)
  7225   restaurants and other eating places
  722511 full-service restaurants
  722513 limited-service restaurants
  722330 mobile food services (licensed food trucks and carts that are employer establishments)
  445110 supermarkets and other grocery stores (placebo; stable code across NAICS 2012/2017/2022)

Gate: the API's US totals for NAICS 722 must match the published CBP US flat files within 0.5% for
establishments and employment in two years (2019, 2023).

Writes _cache/cbp/*.json (raw), _cache/cbp_county_panel.csv (tidy), derived/cbp_fetch_audit.json.
Run from the repository root:
  set -a; . infra/immigration-fiscal/acquire/config.local.env; set +a
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/vending_restaurants_2026_09_24/fetch_cbp.py
"""
import csv
import io
import json
import zipfile

from lib import CACHE, DERIVED, census_json, curl

YEARS = list(range(2012, 2024))
CODES = ["722", "7225", "722511", "722513", "722330", "445110"]
GATE_YEARS = [2019, 2023]
# minimum county rows expected per code; from 2017 CBP publishes fewer small-county cells
# (722513: 3,084 counties in 2016, 2,778 in 2017; 722330: 1,090 and 427; 445110: 3,169 and 2,421),
# so the floors sit below them
MIN_ROWS = {"722": 2900, "7225": 2900, "722511": 2500, "722513": 2500, "722330": 300, "445110": 2000}


def naics_var(year: int) -> str:
    return "NAICS2012" if year <= 2016 else "NAICS2017"


def pull(year: int, code: str, geo: str) -> list:
    nv = naics_var(year)
    url = (f"https://api.census.gov/data/{year}/cbp?get=ESTAB,EMP,PAYANN&for={geo}"
           f"&{nv}={code}&EMPSZES=001&LFO=001")
    tag = geo.split(":")[0].replace(" ", "")
    return census_json(url, CACHE / "cbp" / f"cbp_{year}_{code}_{tag}.json", need_cols=("ESTAB", "EMP", "PAYANN"))


def published_us(year: int) -> dict:
    """NAICS 722 row of the published US flat file (all legal forms, all sizes)."""
    yy = str(year)[2:]
    z = curl(f"https://www2.census.gov/programs-surveys/cbp/datasets/{year}/cbp{yy}us.zip",
             CACHE / "cbp" / f"cbp{yy}us.zip") if not (CACHE / "cbp" / f"cbp{yy}us.zip").exists() \
        else CACHE / "cbp" / f"cbp{yy}us.zip"
    zf = zipfile.ZipFile(z)
    name = [n for n in zf.namelist() if n.lower().endswith(".txt")][0]
    rdr = csv.DictReader(io.TextIOWrapper(zf.open(name), encoding="latin-1"))
    rdr.fieldnames = [f.strip().lower() for f in rdr.fieldnames]
    hits = []
    for r in rdr:
        naics = r["naics"].strip().strip("-/")
        lfo = r.get("lfo", "-").strip()
        size = (r.get("empszes") or r.get("empsize") or "001").strip()
        if naics == "722" and lfo in ("-", "001") and size == "001":
            hits.append(r)
    if len(hits) != 1:
        raise SystemExit(f"[FAILED] published US {year}: {len(hits)} rows for NAICS 722")
    est_col = "estab" if "estab" in hits[0] else "est"  # 2019 file names the column "est"
    return {"estab": int(hits[0][est_col]), "emp": int(hits[0]["emp"]), "file": name}


def main() -> None:
    rows, audit = [], {"counts": {}, "gate": {}}
    for y in YEARS:
        for c in CODES:
            data = pull(y, c, "county:*")
            head = data[0]
            ix = {k: head.index(k) for k in ("ESTAB", "EMP", "PAYANN", "state", "county")}
            body = data[1:]
            n999 = sum(1 for r in body if r[ix["county"]] == "999")
            audit["counts"][f"{y}_{c}"] = {"rows": len(body), "county_999_rows": n999}
            if len(body) < MIN_ROWS[c]:
                raise SystemExit(f"[FAILED] {y} {c}: only {len(body)} county rows")
            for r in body:
                rows.append({"year": y, "naics": c, "fips": r[ix["state"]] + r[ix["county"]],
                             "estab": int(r[ix["ESTAB"]]), "emp": int(r[ix["EMP"]]),
                             "payann": int(r[ix["PAYANN"]])})
            print(f"  {y} {c}: {len(body)} counties ({n999} statewide rows)", flush=True)
    # US totals and the gate
    for y in YEARS:
        us = pull(y, "722", "us:*")
        h = us[0]
        audit["counts"][f"{y}_722_us"] = {"estab": int(us[1][h.index("ESTAB")]), "emp": int(us[1][h.index("EMP")])}
    for y in GATE_YEARS:
        pub = published_us(y)
        api = audit["counts"][f"{y}_722_us"]
        # the county pull includes Puerto Rico (state 72); the published US file does not
        csum = [r for r in rows if r["year"] == y and r["naics"] == "722" and not r["fips"].startswith("72")]
        cty = {"estab": sum(r["estab"] for r in csum), "emp": sum(r["emp"] for r in csum)}
        g = {"published": pub, "api_us": api, "county_sum": cty}
        for k in ("estab", "emp"):
            g[f"api_vs_published_{k}_pct"] = round(100 * (api[k] / pub[k] - 1), 4)
            g[f"county_sum_vs_published_{k}_pct"] = round(100 * (cty[k] / pub[k] - 1), 4)
        g["pass"] = all(abs(g[f"{src}_vs_published_{k}_pct"]) <= 0.5
                        for k in ("estab", "emp") for src in ("api", "county_sum"))
        audit["gate"][str(y)] = g
        print(f"  gate {y}: {json.dumps(g)}")
        if not g["pass"]:
            raise SystemExit(f"[FAILED] gate {y}: US 722 (API or county sum) differs from published by more than 0.5%")
    out = CACHE / "cbp_county_panel.csv"
    with out.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    DERIVED.mkdir(exist_ok=True)
    (DERIVED / "cbp_fetch_audit.json").write_text(json.dumps(audit, indent=1, sort_keys=True) + "\n")
    print(f"wrote {out} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
