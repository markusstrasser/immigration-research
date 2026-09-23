#!/usr/bin/env python3
"""California's state+local spending on public welfare, health and hospitals (Census finance files).

Source: Census Annual Survey of State and Local Government Finances, public-use "state by level of
estimate" files (`YYstatetypepu.txt`: FIPS state, level of estimate, item code, amount in $000,
coefficient of variation, survey year; layout on p. 1 of the 2024 technical documentation). Level 1
is state and local combined, 2 the state government, 3 local governments. State code 00 is the US.
Cached zips, read in place:
  2024: detention_reconciliation_2026_09_20/_cache/census_2024_units.zip
  2021-2023: local_spending_composition_2026_09_18/_cache/indunit_YEAR.zip

Direct expenditure by function (current operation E, construction F; the public-use files carry
no other capital-outlay codes for these functions):
  public welfare = E77 + E79 + F77 + F79, plus E74, E75 (vendor payments, medical / other) and
                   J67, J68 (cash assistance, federal categorical / other) where a file carries
                   them. The 2022-2024 releases (re-issued July 2026) fold those four into E79.
  health         = E32 + F32;  hospitals = E36 + F36.
Federal intergovernmental revenue for the same functions: B79 (public welfare), B42 (health and
hospitals). Survey 2024 is fiscal years ending July 2023-June 2024; California's is FY 2023-24.
Per-resident figures divide by the ACS 2024 1-year PUMS person-weight total for each state.

Run from the repository root:
    OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 uv run --no-project python3 \
        infra/immigration-fiscal/california_medical_status_2026_09_23/finance.py
"""
from __future__ import annotations

import zipfile
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
ZIPS = {
    2024: ROOT / "detention_reconciliation_2026_09_20/_cache/census_2024_units.zip",
    2023: ROOT / "local_spending_composition_2026_09_18/_cache/indunit_2023.zip",
    2022: ROOT / "local_spending_composition_2026_09_18/_cache/indunit_2022.zip",
    2021: ROOT / "local_spending_composition_2026_09_18/_cache/indunit_2021.zip",
}
ACS = ROOT / "unauthorized_population_size_2026_09_19/_cache/acs2024_person_subset.parquet"
FUNCTIONS = {
    "public_welfare": ["E74", "E75", "J67", "J68", "E77", "E79", "F77", "F79"],
    "vendor_payments_medical": ["E74"], "vendor_payments_other": ["E75"],
    "cash_assistance": ["J67", "J68"], "welfare_institutions": ["E77", "F77"],
    "welfare_nec": ["E79", "F79"],
    "health": ["E32", "F32"], "hospitals": ["E36", "F36"],
    "federal_ig_public_welfare": ["B79"], "federal_ig_health_hospitals": ["B42"],
}
STATES = {1: "AL", 2: "AK", 4: "AZ", 5: "AR", 6: "CA", 8: "CO", 9: "CT", 10: "DE", 11: "DC", 12: "FL",
          13: "GA", 15: "HI", 16: "ID", 17: "IL", 18: "IN", 19: "IA", 20: "KS", 21: "KY", 22: "LA",
          23: "ME", 24: "MD", 25: "MA", 26: "MI", 27: "MN", 28: "MS", 29: "MO", 30: "MT", 31: "NE",
          32: "NV", 33: "NH", 34: "NJ", 35: "NM", 36: "NY", 37: "NC", 38: "ND", 39: "OH", 40: "OK",
          41: "OR", 42: "PA", 44: "RI", 45: "SC", 46: "SD", 47: "TN", 48: "TX", 49: "UT", 50: "VT",
          51: "VA", 53: "WA", 54: "WV", 55: "WI", 56: "WY"}


def read_year(year: int) -> pd.DataFrame:
    with zipfile.ZipFile(ZIPS[year]) as z:
        name = next(n for n in z.namelist() if n.endswith(f"{year % 100:02d}statetypepu.txt"))
        lines = z.read(name).decode("latin-1").splitlines()
    rows = [{"state": int(s[0:2]), "level": int(s[2]), "item": s[4:7], "amount_k": float(s[8:20]),
             "cv": s[22:32], "yy": s[33:35]} for s in lines if s.strip()]
    t = pd.DataFrame(rows)
    t["cv"] = pd.to_numeric(t.cv.str.strip(), errors="coerce")   # blank or "." when not published
    if not t.yy.eq(f"{year % 100:02d}").all():
        raise ValueError(f"{name}: survey-year field does not match {year}")
    return t


def main():
    pop = pd.read_parquet(ACS, columns=["STATE", "PWGTP"]).groupby("STATE").PWGTP.sum()
    out_rows, rank_rows = [], []
    for year in sorted(ZIPS):
        t = read_year(year)
        items = set(t.item)
        for func, codes in FUNCTIONS.items():
            have = [c for c in codes if c in items]
            for level in (1, 2, 3):
                sub = t[(t.level == level) & t.item.isin(have)]
                by_state = sub.groupby("state").amount_k.sum() / 1e6          # $bn
                us_file = float(by_state.get(0, float("nan")))
                states = by_state.drop(index=0, errors="ignore").reindex(list(STATES), fill_value=0.0)
                ca = float(states[6])
                rank = int((states > ca).sum() + 1)
                out_rows.append({"survey_year": year, "function": func, "level": level,
                                 "items_present": "+".join(have) or "none",
                                 "california_bn": round(ca, 3), "us_file_bn": round(us_file, 3),
                                 "us_sum_of_states_bn": round(float(states.sum()), 3),
                                 "california_share": round(ca / float(states.sum()), 4) if states.sum() else None,
                                 "california_rank_of_51": rank,
                                 "california_per_resident": round(ca * 1e9 / float(pop[6])) if year == 2024 else None,
                                 "us_per_resident": round(float(states.sum()) * 1e9 / float(pop.sum()))
                                 if year == 2024 else None})
                if year == 2024 and level == 1 and func in ("public_welfare", "health", "hospitals"):
                    for st, v in states.items():
                        rank_rows.append({"function": func, "state": STATES[st], "bn": round(float(v), 3),
                                          "per_resident": round(float(v) * 1e9 / float(pop[st]))})
    t = pd.DataFrame(out_rows)
    out = HERE / "derived"
    out.mkdir(exist_ok=True)
    t.to_csv(out / "census_finance_ca.csv", index=False)
    r = pd.DataFrame(rank_rows)
    r["rank_total"] = r.groupby("function").bn.rank(ascending=False, method="min").astype(int)
    r["rank_per_resident"] = r.groupby("function").per_resident.rank(ascending=False, method="min").astype(int)
    r.sort_values(["function", "rank_total"]).to_csv(out / "census_finance_2024_states.csv", index=False)
    pd.set_option("display.width", 220)
    print(t[t.level == 1].to_string(index=False))
    print(r[r.state.isin(["CA", "NY", "TX", "FL", "PA"])].to_string(index=False))
    print(f"ACS 2024 population: CA {pop[6]:,.0f}; US {pop.sum():,.0f}")


if __name__ == "__main__":
    main()
