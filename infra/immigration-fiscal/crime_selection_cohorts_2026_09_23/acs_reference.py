#!/usr/bin/env python3
"""US-born reference rates for ACS 2006-2024 by single year of age x education, from the Census API
tabulate endpoint (main weight PWGTP; aggregates only).

The endpoint cannot tabulate by age in years whose metadata give AGEP as a range, so each age is
one predicate call. Groups: all US-born men (CIT 1), US-born non-Hispanic white men (HISP 01,
RAC1P 1), US-born Mexican-origin men (HISP 02). Columns are parsed by header because the column
order of TYPEHUGQ differs from TYPE.

Run from the repository root:
  set -a; . infra/immigration-fiscal/acquire/config.local.env; set +a
  uv run --no-project python3 infra/immigration-fiscal/crime_selection_cohorts_2026_09_23/acs_reference.py
Out: _cache/api/ref_*.json (raw) and _cache/acs_reference.csv (year, group, age, educ3, pop, inst)
"""
import csv
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import census_api as ca  # noqa: E402

YEARS = [y for y in range(2006, 2025) if y != 2020]
AGES = range(18, 41)
GROUPS = {"all": "CIT=1", "nhw": "CIT=1&HISP=01&RAC1P=1", "mex": "CIT=1&HISP=02"}


def gq(year: int) -> str:
    return "TYPE" if year <= 2019 else "TYPEHUGQ"


def educ3(year: int, schl: int) -> str | None:
    """Map SCHL to the IPUMS EDUC grouping: fewer than 12 years / grade 12 (diploma, GED or none) / college."""
    if schl == 0:
        return None
    if year <= 2007:  # 16-category scheme: 7 = 11th grade, 8 = 12th no diploma, 9 = HS graduate
        return "lt12" if schl <= 7 else "g12" if schl <= 9 else "col"
    return "lt12" if schl <= 14 else "g12" if schl <= 17 else "col"


def parse(data: list) -> list[tuple[int, float, float]]:
    """Return (SCHL, all persons, institutional persons) from a tabulate response."""
    hdr = data[0]
    col = {list(h.values())[0]: i for i, h in enumerate(hdr) if isinstance(h, dict)}
    out = []
    for row in data[1:]:
        total = sum(row[i] for i in col.values())
        out.append((int(row[-1]), float(total), float(row[col["2"]])))
    return out


def main() -> None:
    os.environ.setdefault("PYTHONUNBUFFERED", "1")
    jobs = [(y, a, g) for y in YEARS for a in AGES for g in GROUPS]

    def run(job):
        y, a, g = job
        path = f"{y}/acs/acs1/pums?tabulate=weight(PWGTP)&col+{gq(y)}&row+SCHL&SEX=1&AGEP={a}&{GROUPS[g]}"
        return job, parse(ca.get(path, f"ref_{y}_{g}_{a}.json"))

    rows = []
    with ThreadPoolExecutor(6) as ex:
        for i, ((y, a, g), cells) in enumerate(ex.map(run, jobs), 1):
            agg = {}
            for schl, pop, inst in cells:
                e = educ3(y, schl)
                if e is None:
                    continue
                p, n = agg.get(e, (0.0, 0.0))
                agg[e] = (p + pop, n + inst)
            rows += [dict(year=y, group=g, age=a, educ3=e, pop=p, inst=n) for e, (p, n) in sorted(agg.items())]
            if i % 100 == 0 or i == len(jobs):
                print(f"  [{i}/{len(jobs)}] {y} {g} age {a}")
    out = HERE / "_cache" / "acs_reference.csv"
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"  ✓ {out.name}: {len(rows)} rows")


if __name__ == "__main__":
    main()
