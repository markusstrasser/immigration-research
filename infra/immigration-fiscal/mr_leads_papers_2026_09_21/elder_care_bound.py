"""Upper bound on the nursing-home channel attributable to the Mexico-born, in 2024 dollars.

Butcher–Moran–Watson (NBER w29520) estimate the effect of the less-educated foreign-born share of
the working-age population on institutionalization of the US-born elderly. This script applies
their coefficients to the 2024 Mexico-born part of that share and prices the result with CMS
national health expenditure data. Every step is favourable to a large channel except where noted:
the output is a bound, not an estimate.
"""
import csv
import hashlib
import sys
from collections import defaultdict
from pathlib import Path

import openpyxl

LANE = Path(__file__).resolve().parent
INPUTS = LANE / "derived/acs_care_inputs.csv"
NHE_ZIP = LANE / "_cache/nhe-tables.zip"
NHE_SHA256 = "a09ef6d3e84e25d745047a47b6b08a0d96b303085b4c725b67ce67a0eb0c4420"
NHE_TABLE = LANE / ("_cache/nhe_tables/Table 15 Nursing Care Facilities and Continuing Care "
                    "Retirement Communities Expenditures.xlsx")

# Butcher–Moran–Watson 2SLS coefficients, institutionalization probability of the US-born 65+ per
# unit of share. Table 2 Panel C col 1 (preferred, F 28.31); Table 7 without California (F 9.2);
# Table 7 with year-by-state effects (not significant, F 4.8).
COEFFICIENTS = {"preferred": 0.151, "without_california": 0.090, "year_by_state_ns": 0.061}


def acs():
    table = defaultdict(dict)
    for row in csv.DictReader(open(INPUTS)):
        cell = dict(item.split("=") for item in row["cell"].split(";"))
        table[row["query"]][tuple(sorted(cell.items()))] = int(row["weight"])

    def total(query, **where):
        return sum(w for key, w in table[query].items() if all(dict(key).get(k) == v for k, v in where.items()))

    return total


def nhe_2024():
    if hashlib.sha256(NHE_ZIP.read_bytes()).hexdigest() != NHE_SHA256:
        raise SystemExit("[BLOCKED] CMS NHE tables changed: re-pin after review")
    sheet = openpyxl.load_workbook(NHE_TABLE, read_only=True, data_only=True).active
    for row in sheet.iter_rows(values_only=True):
        if row and str(row[0]).strip() == "2024":  # first match is the levels block, $bn
            return {"total": float(row[1]), "medicare": float(row[5]), "medicaid": float(row[6])}
    raise SystemExit("[BLOCKED] 2024 row not found in NHE Table 15")


def main():
    total = acs()
    working_age = total("wa_pop_by_nativity")
    treat_all = total("wa_lowed_by_nativity", NATIVITY="2")
    treat_mex = total("wa_lowed_mexico_born", NATIVITY="2")  # foreign-born only, as treat_all
    care_fb = total("care_by_nativity", NATIVITY="2")
    care_mex = total("care_mexico_born", NATIVITY="2")  # excludes Mexico-born US citizens at birth
    elderly_us = total("age65_by_gq_nativity", NATIVITY="1")
    institutional = total("age65_by_gq_nativity", TYPEHUGQ="2")
    nhe = nhe_2024()

    share_all, share_mex = treat_all / working_age, treat_mex / working_age
    mechanism = (care_mex / care_fb) / (treat_mex / treat_all)
    medicaid_each = nhe["medicaid"] * 1e9 / institutional
    all_payer_each = nhe["total"] * 1e9 / institutional
    print(f"working-age population {working_age:,}; less-educated foreign-born {treat_all:,} = {share_all:.2%}")
    print(f"Mexico-born part {treat_mex:,} = {share_mex:.2%} of working-age population, "
          f"{treat_mex / treat_all:.1%} of the treatment group")
    print(f"Mexico-born share of foreign-born direct-care workers {care_mex / care_fb:.1%}; "
          f"mechanism weight {mechanism:.3f}")
    print(f"institutional 65+ {institutional:,}; Medicaid ${medicaid_each:,.0f} and all payers "
          f"${all_payer_each:,.0f} per resident (overstated: CMS totals include residents under 65)")

    rows = []
    for name, coefficient in COEFFICIENTS.items():
        for weighting, factor in (("labour_share", 1.0), ("care_workforce", mechanism)):
            people = coefficient * share_mex * factor * elderly_us
            rows.append({
                "coefficient": name, "weighting": weighting,
                "rate_change_pp": round(100 * coefficient * share_mex * factor, 3),
                "fewer_institutionalized": round(people),
                "medicaid_bn": round(people * medicaid_each / 1e9, 2),
                "all_payer_bn": round(people * all_payer_each / 1e9, 2),
            })
    with open(LANE / "derived/elder_care_bound.csv", "w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    for row in rows:
        print("  ", row)


if __name__ == "__main__":
    sys.exit(main())
