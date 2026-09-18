"""Pull the CDC WONDER homicide victim denominators used to scale the SHR cells.

Underlying Cause of Death, 2018-2024, Single Race (D158); ICD-10 X85-Y09 (assault).
*U01-*U02 (terrorism) are pulled separately and reported; they are a rounding error.
Writes derived/wonder_*.csv.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import wonder  # noqa: E402

OUT = HERE / "derived"
OUT.mkdir(exist_ok=True)
YEARS_ALL = [str(y) for y in range(2018, 2025)]
YEARS_1923 = [str(y) for y in range(2019, 2024)]
# The NCHS 113-cause category "Assault (homicide)" (GR113-127) reproduces the published
# homicide series exactly (2021 = 26,031); the raw ICD-10 range X85-Y09 runs ~1.2% lower,
# so the 113-cause list is the denominator and X85-Y09 is kept as a cross-check.
ASSAULT = {"V4": "GR113-127"}
ASSAULT_ICD = {"V2": "X85-Y09"}


def num(x):
    if x is None:
        return None
    x = x.replace(",", "").strip()
    if x in ("", "Suppressed", "Unreliable", "Not Applicable"):
        return None
    return float(x)


def main() -> None:
    # 1. deaths by year x Hispanic origin (ethnicity missingness on death certificates)
    r = wonder.request(["V1-level1", "V17"], {"V1": YEARS_ALL, **ASSAULT}, tag="yr_hisp_113")
    d = pd.DataFrame(wonder.rows(r, 2), columns=["year", "hispanic_origin", "deaths"])
    d["year"] = d.year.str.strip()
    d["deaths"] = d.deaths.map(num)
    d.to_csv(OUT / "wonder_deaths_year_hispanic.csv", index=False)
    print("[wonder] year x hispanic ->", int(d.deaths.sum()), "deaths 2018-2024")

    # 2. deaths by year x Hispanic origin x race (the SHR scaling target)
    r = wonder.request(["V1-level1", "V17", "V42"], {"V1": YEARS_ALL, **ASSAULT},
                       tag="yr_hisp_race_113")
    d2 = pd.DataFrame(wonder.rows(r, 3), columns=["year", "hispanic_origin", "race", "deaths"])
    d2["year"] = d2.year.str.strip()
    d2["deaths"] = d2.deaths.map(num)
    d2.to_csv(OUT / "wonder_deaths_year_hispanic_race.csv", index=False)
    print("[wonder] year x hispanic x race rows:", len(d2))

    # 3. five-year age x Hispanic origin x race x sex, 2019-2023
    r = wonder.request(["V51", "V17", "V42", "V7"], {"V1": YEARS_1923, **ASSAULT},
                       tag="age_hisp_race_sex_1923_113")
    d3 = pd.DataFrame(wonder.rows(r, 4),
                      columns=["age5", "hispanic_origin", "race", "sex", "deaths"])
    d3["deaths"] = d3.deaths.map(num)
    d3.to_csv(OUT / "wonder_deaths_age_hispanic_race_sex_2019_2023.csv", index=False)
    print("[wonder] age x hisp x race x sex rows:", len(d3), "deaths", d3.deaths.sum())

    # 4. single-year ages x Hispanic origin x sex, 2019-2023 (profile integration)
    r = wonder.request(["V52", "V17", "V7"], {"V1": YEARS_1923, **ASSAULT},
                       o_age="V52", tag="age1_hisp_sex_1923_113")
    d4 = pd.DataFrame(wonder.rows(r, 3), columns=["age", "hispanic_origin", "sex", "deaths"])
    d4["deaths"] = d4.deaths.map(num)
    d4.to_csv(OUT / "wonder_deaths_age1_hispanic_sex_2019_2023.csv", index=False)
    print("[wonder] single-year age rows:", len(d4), "deaths", d4.deaths.sum())

    # 5. population by five-year age x Hispanic origin: WONDER rejects the population
    #    measure on this crossing ("Invalid column name 'pop'"); the age-standardisation
    #    denominator comes from CPS ASEC 2025 in disconfirm.py instead.

    # 6. terrorism codes, for the record
    try:
        r = wonder.request(["V1-level1"], {"V1": YEARS_ALL, "V2": ["U01", "U02"]}, tag="terror")
        d6 = pd.DataFrame(wonder.rows(r, 1), columns=["year", "deaths"])
        d6["deaths"] = d6.deaths.map(num)
        d6.to_csv(OUT / "wonder_deaths_terrorism.csv", index=False)
        print("[wonder] U01-U02 deaths 2018-2024:", d6.deaths.sum())
    except Exception as exc:  # noqa: BLE001
        print("[wonder] U01-U02 pull failed:", exc)


if __name__ == "__main__":
    main()
