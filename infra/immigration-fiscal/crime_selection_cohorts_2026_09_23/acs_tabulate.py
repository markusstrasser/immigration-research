#!/usr/bin/env python3
"""Pull ACS 1-year PUMS weighted tabulations from the Census API as an independent check on the
IPUMS microdata this lane analyses (same PUMS records, separate processing chain).

The tabulate endpoint accepts only the main PWGTP weight and cannot use AGEP or YOEP as row
dimensions in years whose metadata give them as ranges (2006 fails), so years since migration is
set with YOEP range predicates and age is held to 18-40 by predicate. Aggregates only.

Men 18-40, ACS 2006-2019 and 2021-2024 (2020 is experimental; 2005 has no group quarters).
US-born = CIT 1 (born in the 50 states or DC; equals POBP 001-056, checked for 2019).
Mexico-born immigrants = POBP 303 and CIT 4-5 (drops people born in Mexico to US-citizen parents).
Institutional group quarters = TYPE 2 (2006-2019) or TYPEHUGQ 2 (2021+).

Run from the repository root:
  set -a; . infra/immigration-fiscal/acquire/config.local.env; set +a
  uv run --no-project python3 infra/immigration-fiscal/crime_selection_cohorts_2026_09_23/acs_tabulate.py
Out: _cache/api/tab_*.json (raw responses)
"""
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import census_api as ca  # noqa: E402

YEARS = [y for y in range(2006, 2025) if y != 2020]
BINS = {"0-5": (0, 5), "6-10": (6, 10), "11-15": (11, 15)}
BASE = "SEX=1&AGEP=18:40"


def gq(year: int) -> str:
    return "TYPE" if year <= 2019 else "TYPEHUGQ"


def jobs():
    for y in YEARS:
        col = f"tabulate=weight(PWGTP)&col+{gq(y)}"
        yield (f"{y}/acs/acs1/pums?{col}&row+HISP&row+RAC1P&{BASE}&CIT=1", f"tab_us_hisp_race_{y}.json")
        # US-born side of the allocation check: was birthplace imputed?
        yield (f"{y}/acs/acs1/pums?{col}&row+FPOBP&{BASE}&CIT=1", f"tab_us_alloc_{y}.json")
        for b, (lo, hi) in BINS.items():
            yield (f"{y}/acs/acs1/pums?{col}&row+CIT&{BASE}&POBP=303&YOEP={y - hi}:{y - lo}",
                   f"tab_mex_ysm{b}_{y}.json")
            # Allocation flags: was year of entry or birthplace imputed? (0 = reported, 1 = allocated)
            yield (f"{y}/acs/acs1/pums?{col}&row+FYOEP&row+FPOBP&{BASE}&POBP=303&CIT=4:5&YOEP={y - hi}:{y - lo}",
                   f"tab_mex_alloc_ysm{b}_{y}.json")


def main() -> None:
    os.environ.setdefault("PYTHONUNBUFFERED", "1")
    todo = list(jobs())

    def run(job):
        path, name = job
        try:
            return name, len(ca.get(path, name)) - 1
        except RuntimeError as e:
            return name, f"FAILED {e}"

    with ThreadPoolExecutor(6) as ex:
        for i, (name, n) in enumerate(ex.map(run, todo), 1):
            print(f"  [{i}/{len(todo)}] {name}: {n}")


if __name__ == "__main__":
    main()
