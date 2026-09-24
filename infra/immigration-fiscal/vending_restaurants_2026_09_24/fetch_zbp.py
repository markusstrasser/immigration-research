"""ZIP Code Business Patterns 2012-2023 for Los Angeles County ZIPs: establishments by size class.

ZIP-level CBP publishes establishment counts by employment-size class for detailed NAICS, but no
employment or payroll below the all-industry total, so the ZIP outcomes are establishment counts and
a size-class employment index (count x class midpoint). 2012-2018 come from the zbp endpoint
(for=zipcode:*), 2019-2023 from the cbp endpoint (for=zip code:*).

Los Angeles County ZIPs are the 2010 ZCTAs with at least half their population in county 06037
(Census 2010 ZCTA-to-county relationship file).

Writes _cache/zbp/*.json, _cache/zcta_county_rel_10.txt and _cache/zbp_la_panel.csv, and
derived/zbp_fetch_audit.json. Run from the repository root with CENSUS_API_KEY set.
"""
import csv
import json

from lib import CACHE, DERIVED, census_json, curl

YEARS = list(range(2012, 2024))
CODES = ["722", "722511", "722513", "722330", "445110"]
REL_URL = "https://www2.census.gov/geo/docs/maps-data/data/rel/zcta_county_rel_10.txt"
# employment-size class midpoints; 2012-2016 code 212 is 1-4 employees, 2017+ code 210 is <5
MID = {"210": 2.5, "212": 2.5, "220": 7, "230": 14.5, "241": 34.5, "242": 74.5, "251": 174.5,
       "252": 374.5, "254": 749.5, "260": 1500}


def la_zips() -> set:
    rel = CACHE / "zcta_county_rel_10.txt"
    if not rel.exists():
        curl(REL_URL, rel)
    out = set()
    with rel.open() as fh:
        for r in csv.DictReader(fh):
            if r["STATE"] == "06" and r["COUNTY"] == "037" and float(r["ZPOPPCT"]) >= 50:
                out.add(r["ZCTA5"])
    if not 250 <= len(out) <= 320:
        raise SystemExit(f"[FAILED] LA County ZCTA count {len(out)}")
    return out


def pull(year: int, code: str, zips: set, tag: str = "la") -> list:
    """National ZIP rows when a national file is cached (2012-2017 were pulled that way); otherwise the
    LA ZIPs in chunks of 60, which is far faster than a national pull for 2017+ vintages."""
    if year <= 2018:
        nv = "NAICS2012" if year <= 2016 else "NAICS2017"
        base = f"https://api.census.gov/data/{year}/zbp?get=ESTAB,EMPSZES&{nv}={code}&for=zipcode:"
    else:
        base = f"https://api.census.gov/data/{year}/cbp?get=ESTAB,EMPSZES&NAICS2017={code}&for=zip%20code:"
    nat = CACHE / "zbp" / f"zbp_{year}_{code}.json"
    if nat.exists():
        return census_json(base + "*", nat, need_cols=("ESTAB", "EMPSZES"))
    zs, rows = sorted(zips), []
    for i in range(0, len(zs), 60):
        part = census_json(base + ",".join(zs[i:i + 60]), CACHE / "zbp" / f"zbp_{year}_{code}_{tag}{i // 60}.json",
                           need_cols=("ESTAB", "EMPSZES"))
        rows = rows + (part[1:] if rows else part)
    if not rows:
        raise SystemExit(f"[FAILED] {year} {code}: no {tag} ZIP returned any row")
    return rows


def main() -> None:
    zips = la_zips()
    rows, audit = [], {"la_zctas": len(zips), "counts": {}}
    for y in YEARS:
        for c in CODES:
            data = pull(y, c, zips)
            h = data[0]
            iz = h.index("zip code")
            ie, isz = h.index("ESTAB"), h.index("EMPSZES")
            per = {}
            for r in data[1:]:
                z = r[iz]
                if z not in zips:
                    continue
                d = per.setdefault(z, {"estab": 0, "emp_index": 0.0, "classes": 0})
                if r[isz] == "001":
                    d["estab"] = int(r[ie])
                elif r[isz] in MID:
                    d["emp_index"] += MID[r[isz]] * int(r[ie])
                    d["classes"] += int(r[ie])
            nat = sum(int(r[ie]) for r in data[1:] if r[isz] == "001")  # national only when pulled nationally
            audit["counts"][f"{y}_{c}"] = {"zip_rows_pulled": sum(1 for r in data[1:] if r[isz] == "001"),
                                           "estab_pulled": nat, "la_zips_present": len(per),
                                           "la_estab": sum(d["estab"] for d in per.values())}
            bad = [z for z, d in per.items() if d["classes"] and d["classes"] != d["estab"]]
            if bad:
                audit["counts"][f"{y}_{c}"]["size_class_mismatch_zips"] = len(bad)
            for z, d in per.items():
                rows.append({"year": y, "naics": c, "zip": z, "estab": d["estab"],
                             "emp_index": round(d["emp_index"], 1)})
            print(f"  {y} {c}: {len(per)} LA ZIPs, {audit['counts'][f'{y}_{c}']['la_estab']} establishments "
                  f"(pulled {nat})", flush=True)
    out = CACHE / "zbp_la_panel.csv"
    with out.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    DERIVED.mkdir(exist_ok=True)
    (DERIVED / "zbp_fetch_audit.json").write_text(json.dumps(audit, indent=1, sort_keys=True) + "\n")
    print(f"wrote {out} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
