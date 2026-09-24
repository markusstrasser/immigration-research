"""QCEW 2014-2023 annual averages by county, private ownership, for restaurants and the grocery placebo.

BLS QCEW open-data industry slices (data.bls.gov/cew/data/api/{year}/a/industry/{code}.csv), which
carry every area for one industry; the slices start in 2014 (2012 and 2013 return 404), so the QCEW
panel has four pre-law years against CBP's six. Kept: county rows (agglvl 76 for 4-digit, 78 for 6-digit NAICS),
own_code 5 (private), disclosure code blank. Industries: 7225 restaurants and other eating places,
722511, 722513, 722330, 445110.

Gate: the county rows for 7225 must sum to within 2% of the national private 7225 row each year
(non-disclosed counties are the gap), and the national row must be present.

Writes _cache/qcew/*.csv (raw), _cache/qcew_county_panel.csv and derived/qcew_fetch_audit.json.
Run from the repository root.
"""
import csv
import json

from lib import BLS_HEADERS, CACHE, DERIVED, curl

YEARS = list(range(2014, 2024))  # API slices exist from 2014
CODES = ["7225", "722511", "722513", "722330", "445110"]


def slice_rows(year: int, code: str) -> list:
    out = CACHE / "qcew" / f"qcew_{year}_{code}.csv"
    if not out.exists():
        curl(f"https://data.bls.gov/cew/data/api/{year}/a/industry/{code}.csv", out, extra=BLS_HEADERS)
    with out.open() as fh:
        rows = list(csv.DictReader(fh))
    if not rows or "annual_avg_emplvl" not in rows[0] or rows[0]["industry_code"] != code:
        out.unlink()
        raise SystemExit(f"[FAILED] QCEW {year} {code}: bad body")
    return rows


def main() -> None:
    panel, audit = [], {}
    for y in YEARS:
        for c in CODES:
            rows = slice_rows(y, c)
            lvl = "76" if len(c) == 4 else "78"
            cty = [r for r in rows if r["own_code"] == "5" and r["agglvl_code"] == lvl]
            nat = [r for r in rows if r["area_fips"] == "US000" and r["own_code"] == "5"]
            shown = [r for r in cty if r["disclosure_code"] != "N"]
            emp_c = sum(float(r["annual_avg_emplvl"]) for r in shown)
            emp_n = float(nat[0]["annual_avg_emplvl"]) if nat else float("nan")
            audit[f"{y}_{c}"] = {"county_rows": len(cty), "disclosed": len(shown), "county_emp": emp_c,
                                 "national_emp": emp_n, "county_share_of_national": round(emp_c / emp_n, 4)}
            if c == "7225" and (not nat or abs(emp_c / emp_n - 1) > 0.02):
                raise SystemExit(f"[FAILED] QCEW {y} 7225: county sum {emp_c:.0f} vs national {emp_n:.0f}")
            for r in cty:
                panel.append({"year": y, "naics": c, "fips": r["area_fips"],
                              "disclosed": int(r["disclosure_code"] != "N"),
                              "estabs": int(r["annual_avg_estabs"]), "emp": int(r["annual_avg_emplvl"]),
                              "wages": int(r["total_annual_wages"])})
            print(f"  {y} {c}: {len(cty)} counties, {len(shown)} disclosed, county/national emp "
                  f"{audit[f'{y}_{c}']['county_share_of_national']}", flush=True)
    out = CACHE / "qcew_county_panel.csv"
    with out.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(panel[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(panel)
    DERIVED.mkdir(exist_ok=True)
    (DERIVED / "qcew_fetch_audit.json").write_text(json.dumps(audit, indent=1, sort_keys=True) + "\n")
    print(f"wrote {out} ({len(panel)} rows)")


if __name__ == "__main__":
    main()
