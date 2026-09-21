"""Military service among US-born men by first-reported ancestry, ACS 2024 PUMS.

A costly behavioural proxy for national attachment, to set beside the survey measures (giving,
volunteering, turnout) in the Indian-origin memo. Two tabulations through the Census tabulate
API, both US-born men: ages 18-49 at every education level, and ages 25-49 with a bachelor's
degree, because enlistment falls steeply with education and the groups differ in education.
`MIL`: 1 now on active duty, 2 active duty in the past, 3 reserve or guard training only,
4 never served. "Ever active duty" = 1 + 2. Reads CENSUS_API_KEY from the environment and never
prints it. No replicate weights are pulled: the standard error shown is a binomial approximation
on a 1% sample and understates the design-based one.
"""
import csv
import importlib.util
import json
import math
import re
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE, DERIVED = HERE / "_cache", HERE / "derived"
CARE = HERE.parent / "mr_leads_papers_2026_09_21" / "pull_acs_care.py"
MIN_POPULATION = 50_000
FRAME = "&col+MIL&row+ANC1P&NATIVITY=1&SEX=1"
QUERIES = {
    "men_18_49": f"{FRAME}&AGEP=18:49",
    "men_25_49_ba": f"{FRAME}&AGEP=25:49&SCHL=21:24",
    # narrow bands: the newer groups' US-born men are young, and "ever served" accumulates with age
    "men_25_34": f"{FRAME}&AGEP=25:34",
    "men_25_34_ba": f"{FRAME}&AGEP=25:34&SCHL=21:24",
}
SHOW = re.compile(r"asian indian|chinese|filipino|korean|vietnamese|japanese|pakistani|iranian|"
                  r"^mexican|cuban|puerto rican|^german|^irish|^english|^italian|^polish|"
                  r"^american$|african american|nigerian|^russian|lebanese|egyptian|^arab", re.I)


def load_care():
    spec = importlib.util.spec_from_file_location("pull_acs_care", CARE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.CACHE = CACHE
    return module


def ancestry_labels(year):
    target = CACHE / f"acs{year}_ANC1P_labels.json"
    if not target.exists():
        url = f"https://api.census.gov/data/{year}/acs/acs1/pums/variables/ANC1P.json"
        with urllib.request.urlopen(url, timeout=60) as response:
            target.write_text(response.read().decode())
    items = json.loads(target.read_text())["values"]["item"]
    return {code.lstrip("0") or "0": label for code, label in items.items()}


def main():
    CACHE.mkdir(exist_ok=True)
    DERIVED.mkdir(exist_ok=True)
    care = load_care()
    labels = ancestry_labels(care.YEAR)
    rows = []
    for tag, query in QUERIES.items():
        by_ancestry = {}
        for key, weight in care.cells(care.fetch(tag, query)).items():
            cell = dict(key)
            code = str(cell["ANC1P"]).lstrip("0") or "0"
            by_ancestry.setdefault(code, {}).setdefault(str(cell["MIL"]).lstrip("0"), 0.0)
            by_ancestry[code][str(cell["MIL"]).lstrip("0")] += weight
        print(f"  ✓ {tag}: {len(by_ancestry)} ancestries, {sum(sum(v.values()) for v in by_ancestry.values()):,.0f} men")
        for code, mil in by_ancestry.items():
            population = sum(mil.get(k, 0.0) for k in "1234")
            if population < MIN_POPULATION:
                continue
            ever = (mil.get("1", 0.0) + mil.get("2", 0.0)) / population
            rows.append({"year": care.YEAR, "universe": tag, "anc1p": code,
                         "ancestry": labels.get(code, "?"), "population": round(population),
                         "now_active_duty": mil.get("1", 0.0) / population,
                         "ever_active_duty": ever,
                         "reserve_training_only": mil.get("3", 0.0) / population,
                         "approx_se_ever": math.sqrt(max(ever * (1 - ever), 0) / (population / 100))})
    rows.sort(key=lambda r: (r["universe"], -r["ever_active_duty"]))
    with open(DERIVED / "military_service_by_ancestry.csv", "w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        for row in rows:
            writer.writerow({k: (f"{v:.5f}" if isinstance(v, float) else v) for k, v in row.items()})
    for tag in QUERIES:
        print(f"\n  [{tag}] US-born men, ancestries shown by name filter")
        print(f"  {'ancestry':28} {'men':>10} {'ever active':>11} {'±se':>6} {'now':>6}")
        for r in rows:
            if r["universe"] == tag and SHOW.search(r["ancestry"]):
                print(f"  {r['ancestry'][:28]:28} {r['population']:10,d} {r['ever_active_duty']:11.2%} "
                      f"{r['approx_se_ever']:6.2%} {r['now_active_duty']:6.2%}")
    leaked = [p.name for p in CACHE.glob("acs*.json") if re.search(r"key=", p.read_text())]
    assert not leaked, leaked


if __name__ == "__main__":
    sys.exit(main())
