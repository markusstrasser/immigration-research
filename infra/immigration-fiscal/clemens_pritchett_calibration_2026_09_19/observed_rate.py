"""Observed Mexican migration rate, on the paper's own denominator convention.

The paper sets its benchmark m0 = 0.3% from "about 950,000 people per year [who]
have obtained permanent residence from countries other than Canada, European
countries, and Japan ... in a country of about 318m" (footnote 6, DHS Yearbook
2013 Table 3). This script builds the Mexico-only analogue from the same DHS
table, current vintage, over the current US resident population, and adds the
stock share the repo measures.

Inputs pinned in _cache/ (sha256 in _cache/SHA256SUMS.txt):
  dhs_lpr_fy2024.xlsx    DHS OHSS Yearbook of Immigration Statistics FY2024, Table 3
  NA-EST2024-POP.xlsx    Census Bureau monthly national population estimates, Vintage 2024

Output: derived/observed_migration.csv
"""
import csv
import os

import pandas as pd

import cpmodel as M

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "derived")
CACHE = os.path.join(HERE, "_cache")
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
LEDGER = os.path.join(REPO, "infra", "immigration-fiscal", "all_age_ledger_2026_09_17",
                      "derived", "estimates.csv")


def lpr():
    d = pd.read_excel(os.path.join(CACHE, "dhs_lpr_fy2024.xlsx"), "Table 3", header=None)
    hdr = d[d[0].astype(str).str.strip() == "Region and country of birth"].index[0]
    years = [int(float(v)) for v in d.iloc[hdr, 1:].tolist()]
    row = d[d[0].astype(str).str.strip() == "Mexico"]
    if len(row) != 1:
        raise SystemExit(f"Table 3: {len(row)} rows named Mexico")
    vals = [float(v) for v in row.iloc[0, 1:].tolist()]
    return dict(zip(years, vals))


def us_population():
    d = pd.read_excel(os.path.join(CACHE, "NA-EST2024-POP.xlsx"), header=None)
    year, out = None, {}
    for _, r in d.iterrows():
        lab = str(r[0]).strip()
        head = lab.split()[0] if lab else ""
        if head.isdigit():          # year rows print as "2024" or "2024 [1]"
            year = int(head)
        elif lab.startswith(".") and year is not None and pd.notna(r[1]):
            out[(year, lab.lstrip("."))] = float(r[1])
    return out


def stock(target):
    with open(LEDGER, encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["scenario"] == "baseline" and r["target"] == target:
                return float(r["population"])
    raise SystemExit(f"{target} population not found in the ledger estimates")


def main():
    L = lpr()
    P = us_population()
    pop24 = P[(2024, "July 1")]
    born = stock("mexico_born")
    origin = stock("mexican_observed_total")

    last10 = sorted(L)[-10:]
    mean10 = sum(L[y] for y in last10) / len(last10)

    rows = [
        {"quantity": "Mexico LPR admissions, FY2024", "value": M.f(L[2024], 0), "unit": "persons",
         "tag": "SOURCE", "source": "DHS OHSS Yearbook FY2024 Table 3 (_cache/dhs_lpr_fy2024.xlsx)"},
        {"quantity": f"Mexico LPR admissions, mean FY{last10[0]}-FY{last10[-1]}",
         "value": M.f(mean10, 0), "unit": "persons per year", "tag": "CALCULATION",
         "source": "DHS OHSS Yearbook FY2024 Table 3"},
        {"quantity": "US resident population, July 1 2024", "value": M.f(pop24, 0), "unit": "persons",
         "tag": "SOURCE", "source": "Census Bureau NA-EST2024-POP, Vintage 2024 monthly estimates"},
        {"quantity": "m_mexico, FY2024 LPR", "value": M.f(L[2024] / pop24, 6), "unit": "per year",
         "tag": "CALCULATION", "source": "LPR/population, the paper's footnote-6 convention"},
        {"quantity": f"m_mexico, FY{last10[0]}-FY{last10[-1]} LPR mean",
         "value": M.f(mean10 / pop24, 6), "unit": "per year", "tag": "CALCULATION",
         "source": "LPR/population, the paper's footnote-6 convention"},
        {"quantity": "Mexico-born resident stock", "value": M.f(born, 0), "unit": "persons",
         "tag": "SOURCE", "source": "all_age_ledger_2026_09_17/derived/estimates.csv (CPS ASEC 2025)"},
        {"quantity": "phi_mexico_born, stock share", "value": M.f(born / pop24, 6), "unit": "share",
         "tag": "CALCULATION", "source": "CPS ASEC 2025 stock over Census July 2024 population"},
        {"quantity": "Mexican-origin resident stock, all three generations",
         "value": M.f(origin, 0), "unit": "persons", "tag": "SOURCE",
         "source": "all_age_ledger_2026_09_17/derived/estimates.csv, mexican_observed_total"},
        {"quantity": "phi_mexican_origin, stock share", "value": M.f(origin / pop24, 6),
         "unit": "share", "tag": "CALCULATION",
         "source": "CPS ASEC 2025 stock over Census July 2024 population"},
    ]
    with open(os.path.join(OUT, "observed_migration.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, ["quantity", "value", "unit", "tag", "source"])
        w.writeheader()
        w.writerows(rows)
    for r in rows:
        print(f"{r['quantity']:<46} {r['value']:>16} {r['unit']}")


if __name__ == "__main__":
    main()
