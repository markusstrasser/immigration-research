"""ACS 2024 PUMS screen by birthplace: education against fiscal-exposure proxies.

Large-sample companion to `screen.py` (CPS dollars, thin samples). For every birthplace this
tabulates the foreign-born population, the share with a bachelor's degree at ages 25-64, and
proxies for the items that decide a fiscal balance: age structure, employment, poverty, SSI,
Medicaid, public assistance, Social Security receipt among the elderly, and high earners.
Proxies only: no dollars. Reads CENSUS_API_KEY from the environment and never prints it.
"""
import csv
import importlib.util
import json
import re
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE, DERIVED = HERE / "_cache", HERE / "derived"
CARE = HERE.parent / "mr_leads_papers_2026_09_21" / "pull_acs_care.py"
MIN_POPULATION = 100_000

# Every query is rows = birthplace, columns = nativity; only foreign-born cells are kept, so
# people born abroad to US parents are excluded.
FRAME = "&col+NATIVITY&row+POBP"
QUERIES = {
    "pop_all": FRAME,
    "pop_65_plus": f"{FRAME}&AGEP=65:99",
    "pop_25_64": f"{FRAME}&AGEP=25:64",
    "ba_25_64": f"{FRAME}&AGEP=25:64&SCHL=21:24",
    "employed_25_64": f"{FRAME}&AGEP=25:64&ESR=1,2",
    "income_100k_25_64": f"{FRAME}&AGEP=25:64&PINCP=100000:9999999",
    "poverty_universe": f"{FRAME}&POVPIP=0:501",
    "poor": f"{FRAME}&POVPIP=0:99",
    "ssi": f"{FRAME}&SSIP=1:99999",
    "public_assistance": f"{FRAME}&PAP=1:99999",
    "medicaid": f"{FRAME}&HINS4=1",
    "medicaid_65_plus": f"{FRAME}&HINS4=1&AGEP=65:99",
    "ssi_65_plus": f"{FRAME}&SSIP=1:99999&AGEP=65:99",
    "social_security_65_plus": f"{FRAME}&SSP=1:99999&AGEP=65:99",
}


def load_care():
    spec = importlib.util.spec_from_file_location("pull_acs_care", CARE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.CACHE = CACHE  # its fetch() caches beside this lane, not beside the care lane
    return module


def birthplace_labels(year):
    target = CACHE / f"acs{year}_POBP_labels.json"
    if not target.exists():
        url = f"https://api.census.gov/data/{year}/acs/acs1/pums/variables/POBP.json"
        with urllib.request.urlopen(url, timeout=60) as response:
            target.write_text(response.read().decode())
    items = json.loads(target.read_text())["values"]["item"]
    return {code.lstrip("0") or "0": label for code, label in items.items()}


def foreign_born_by_birthplace(care, tag, query):
    out = {}
    for key, weight in care.cells(care.fetch(tag, query)).items():
        cell = dict(key)
        if str(cell.get("NATIVITY")) == "2":
            code = str(cell["POBP"]).lstrip("0") or "0"
            out[code] = out.get(code, 0.0) + weight
    return out


def main():
    CACHE.mkdir(exist_ok=True)
    DERIVED.mkdir(exist_ok=True)
    care = load_care()
    labels = birthplace_labels(care.YEAR)
    tables = {}
    for tag, query in QUERIES.items():
        tables[tag] = foreign_born_by_birthplace(care, tag, query)
        print(f"  ✓ {tag}: {len(tables[tag])} birthplaces, total {sum(tables[tag].values()):,.0f}")

    def ratio(code, top, bottom):
        denominator = tables[bottom].get(code, 0.0)
        return tables[top].get(code, 0.0) / denominator if denominator else float("nan")

    rows = []
    for code, population in tables["pop_all"].items():
        if population < MIN_POPULATION:
            continue
        rows.append({
            "year": care.YEAR, "pobp": code, "birthplace": labels.get(code, "?"),
            "foreign_born_population": round(population),
            "ba_plus_share_25_64": ratio(code, "ba_25_64", "pop_25_64"),
            "share_65_plus": ratio(code, "pop_65_plus", "pop_all"),
            "employed_share_25_64": ratio(code, "employed_25_64", "pop_25_64"),
            "income_100k_share_25_64": ratio(code, "income_100k_25_64", "pop_25_64"),
            "poverty_rate": ratio(code, "poor", "poverty_universe"),
            "ssi_rate_all_ages": ratio(code, "ssi", "pop_all"),
            "public_assistance_rate": ratio(code, "public_assistance", "pop_all"),
            "medicaid_rate_all_ages": ratio(code, "medicaid", "pop_all"),
            "medicaid_rate_65_plus": ratio(code, "medicaid_65_plus", "pop_65_plus"),
            "ssi_rate_65_plus": ratio(code, "ssi_65_plus", "pop_65_plus"),
            "social_security_rate_65_plus": ratio(code, "social_security_65_plus", "pop_65_plus"),
        })
    rows.sort(key=lambda r: -r["ba_plus_share_25_64"])
    with open(DERIVED / "acs_origin_screen.csv", "w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        for row in rows:
            writer.writerow({k: (f"{v:.4f}" if isinstance(v, float) else v) for k, v in row.items()})
    print(f"\n  {len(rows)} birthplaces with at least {MIN_POPULATION:,} foreign-born residents")
    print(f"  {'birthplace':26} {'pop':>9} {'BA+':>6} {'65+':>6} {'emp':>6} {'100k+':>6} {'poor':>6} "
          f"{'Mcaid':>6} {'Mc65+':>6} {'SSI65+':>6} {'SS65+':>6}")
    for r in rows:
        print(f"  {r['birthplace'][:26]:26} {r['foreign_born_population']:9,d} {r['ba_plus_share_25_64']:6.1%} "
              f"{r['share_65_plus']:6.1%} {r['employed_share_25_64']:6.1%} {r['income_100k_share_25_64']:6.1%} "
              f"{r['poverty_rate']:6.1%} {r['medicaid_rate_all_ages']:6.1%} {r['medicaid_rate_65_plus']:6.1%} "
              f"{r['ssi_rate_65_plus']:6.1%} {r['social_security_rate_65_plus']:6.1%}")
    leaked = [p.name for p in CACHE.glob("acs*.json") if re.search(r"key=", p.read_text())]
    assert not leaked, leaked


if __name__ == "__main__":
    sys.exit(main())
