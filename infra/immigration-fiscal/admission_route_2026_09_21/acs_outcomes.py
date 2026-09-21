"""ACS 2024 outcomes by birthplace for foreign-born residents who entered in 2000 or later.

Units are the birthplaces with at least 100,000 foreign-born residents in the origin screen
(`high_skill_origin_screen_2026_09_21/derived/acs_origin_screen.csv`), UK components merged.
Outcomes as fixed in README.md: P1 Medicaid and P2 income of $100,000 or more among degree
holders aged 25-64; S1 Medicaid, S2 poverty, S3 employment at 25-64, all education levels.
Reads CENSUS_API_KEY from the environment and never prints it.
"""
import csv
import importlib.util
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE, DERIVED = HERE / "_cache", HERE / "derived"
SCREEN = HERE.parent / "high_skill_origin_screen_2026_09_21"
ENTERED = "&YOEP=2000:2024"
FRAME = "&col+NATIVITY&row+POBP"
QUERIES = {
    "pop": f"{FRAME}{ENTERED}",
    "medicaid": f"{FRAME}{ENTERED}&HINS4=1",
    "poverty_universe": f"{FRAME}{ENTERED}&POVPIP=0:501",
    "poor": f"{FRAME}{ENTERED}&POVPIP=0:99",
    "pop_25_64": f"{FRAME}{ENTERED}&AGEP=25:64",
    "employed_25_64": f"{FRAME}{ENTERED}&AGEP=25:64&ESR=1,2",
    "ba_25_64": f"{FRAME}{ENTERED}&AGEP=25:64&SCHL=21:24",
    "ba_medicaid_25_64": f"{FRAME}{ENTERED}&AGEP=25:64&SCHL=21:24&HINS4=1",
    "ba_income_100k_25_64": f"{FRAME}{ENTERED}&AGEP=25:64&SCHL=21:24&PINCP=100000:9999999",
    # exploratory, added after the pre-specified run: employment by sex
    "men_25_64": f"{FRAME}{ENTERED}&AGEP=25:64&SEX=1",
    "men_employed_25_64": f"{FRAME}{ENTERED}&AGEP=25:64&SEX=1&ESR=1,2",
    "women_25_64": f"{FRAME}{ENTERED}&AGEP=25:64&SEX=2",
    "women_employed_25_64": f"{FRAME}{ENTERED}&AGEP=25:64&SEX=2&ESR=1,2",
}
UK_LABEL = "United Kingdom"
UK_PARTS = re.compile(r"^(united kingdom|england|scotland|wales|northern ireland)", re.I)


def load_screen():
    spec = importlib.util.spec_from_file_location("acs_screen", SCREEN / "acs_screen.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.CACHE = CACHE  # cache this lane's pulls here, not beside the screen
    return module


def main():
    CACHE.mkdir(exist_ok=True)
    DERIVED.mkdir(exist_ok=True)
    screen = load_screen()
    care = screen.load_care()
    labels = screen.birthplace_labels(care.YEAR)
    units = {}
    for row in csv.DictReader(open(SCREEN / "derived" / "acs_origin_screen.csv")):
        name = UK_LABEL if UK_PARTS.match(row["birthplace"]) else row["birthplace"]
        units.setdefault(name, 0)
        units[name] += int(row["foreign_born_population"])

    def unit_of(code):
        label = labels.get(code, "?")
        return UK_LABEL if UK_PARTS.match(label) else label

    tables = {}
    for tag, query in QUERIES.items():
        by_unit = {}
        for code, weight in screen.foreign_born_by_birthplace(care, tag, query).items():
            by_unit[unit_of(code)] = by_unit.get(unit_of(code), 0.0) + weight
        tables[tag] = by_unit
        print(f"  ✓ {tag}: total {sum(by_unit.values()):,.0f}")

    def ratio(unit, top, bottom):
        denominator = tables[bottom].get(unit, 0.0)
        return tables[top].get(unit, 0.0) / denominator if denominator else float("nan")

    rows = []
    for unit, stock in sorted(units.items(), key=lambda kv: -kv[1]):
        rows.append({
            "year": care.YEAR, "birthplace": unit, "foreign_born_all_years": stock,
            "entered_2000_plus": round(tables["pop"].get(unit, 0.0)),
            "degree_holders_25_64": round(tables["ba_25_64"].get(unit, 0.0)),
            "degree_share_25_64": ratio(unit, "ba_25_64", "pop_25_64"),
            "p1_medicaid_degree_25_64": ratio(unit, "ba_medicaid_25_64", "ba_25_64"),
            "p2_income_100k_degree_25_64": ratio(unit, "ba_income_100k_25_64", "ba_25_64"),
            "s1_medicaid_all": ratio(unit, "medicaid", "pop"),
            "s2_poverty": ratio(unit, "poor", "poverty_universe"),
            "s3_employed_25_64": ratio(unit, "employed_25_64", "pop_25_64"),
            "x_employed_men_25_64": ratio(unit, "men_employed_25_64", "men_25_64"),
            "x_employed_women_25_64": ratio(unit, "women_employed_25_64", "women_25_64"),
        })
    with open(DERIVED / "acs_route_outcomes.csv", "w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        for row in rows:
            writer.writerow({k: (f"{v:.5f}" if isinstance(v, float) else v) for k, v in row.items()})
    print(f"  ✓ {len(rows)} units → derived/acs_route_outcomes.csv")
    leaked = [p.name for p in CACHE.glob("acs*.json") if re.search(r"key=", p.read_text())]
    assert not leaked, leaked


if __name__ == "__main__":
    sys.exit(main())
