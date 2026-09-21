"""Pre-specified cross-birthplace models: admission route against origin-country Muslim share.

Specification and decision rule are fixed in README.md. Inputs: `derived/acs_route_outcomes.csv`
(ACS 2024, entered 2000+), `derived/lpr_class_mix.csv` (DHS Table 10, FY2005-2023) and Pew's
2010 religious composition by country (`_cache/pew_religious_composition_2010_2050.xlsx`).
Outcomes are in percentage points; Muslim share and route shares run 0-1, so a coefficient is
the difference between an origin at 0 and an origin at 1. OLS with HC3 standard errors, one
observation per birthplace; the weighted check uses the entered-2000+ population.
"""
import csv
import json
import sys
from pathlib import Path

import numpy as np
import openpyxl

HERE = Path(__file__).resolve().parent
CACHE, DERIVED = HERE / "_cache", HERE / "derived"
OUTCOMES = {
    "p1_medicaid_degree_25_64": ("P1 Medicaid, degree holders 25-64", False),
    "p2_income_100k_degree_25_64": ("P2 income >= $100k, degree holders 25-64", False),
    "s1_medicaid_all": ("S1 Medicaid, all", True),
    "s2_poverty": ("S2 poverty", True),
    "s3_employed_25_64": ("S3 employed 25-64", True),
    # exploratory, added after the pre-specified run; outside the decision rule
    "x_employed_men_25_64": ("X employed men 25-64 (exploratory)", True),
    "x_employed_women_25_64": ("X employed women 25-64 (exploratory)", True),
}
ROUTES = ["share_employment", "share_refugee_asylee", "share_diversity"]  # family, other omitted
OUTSIDE_LPR_FLOW = {"Mexico", "El Salvador", "Guatemala", "Honduras", "Nicaragua", "Costa Rica",
                    "Panama", "Belize"}
PEW_NAMES = {"Korea": "South Korea", "Myanmar": "Burma (Myanmar)", "Bosnia and Herzegovina":
             "Bosnia-Herzegovina", "Czechia": "Czech Republic", "North Macedonia":
             "Republic of Macedonia", "Cabo Verde": "Cape Verde"}


def pew_muslim_share():
    book = openpyxl.load_workbook(CACHE / "pew_religious_composition_2010_2050.xlsx",
                                  read_only=True, data_only=True)
    rows = book["rounded_percentage"].iter_rows(values_only=True)
    header = [str(c).strip() for c in next(rows)]
    year, country, muslims = header.index("Year"), header.index("Country"), header.index("Muslims")
    shares = {}
    for row in rows:
        if str(row[year]).strip() == "2010":
            text = str(row[muslims]).strip()
            # Pew prints "< 1.0" and ">99.0" at the ends; the midpoints 0.5% and 99.5% are used
            shares[str(row[country]).strip()] = (0.005 if text.startswith("<") else
                                                 0.995 if text.startswith(">") else float(text) / 100)
    return shares


def ols_hc3(y, X, weights=None):
    if weights is not None:
        root = np.sqrt(weights / weights.mean())
        y, X = y * root, X * root[:, None]
    bread = np.linalg.inv(X.T @ X)
    beta = bread @ X.T @ y
    residual = y - X @ beta
    leverage = np.einsum("ij,jk,ik->i", X, bread, X)
    meat = X.T @ (X * (residual ** 2 / (1 - leverage) ** 2)[:, None])
    return beta, np.sqrt(np.diag(bread @ meat @ bread))


def main():
    muslim = pew_muslim_share()
    routes = {r["country"]: r for r in csv.DictReader(open(DERIVED / "lpr_class_mix.csv"))}
    units, dropped = [], []
    for row in csv.DictReader(open(DERIVED / "acs_route_outcomes.csv")):
        name = row["birthplace"]
        pew = muslim.get(PEW_NAMES.get(name, name))
        if name not in routes or pew is None:
            dropped.append({"birthplace": name, "in_dhs": name in routes, "in_pew": pew is not None})
            continue
        units.append({**row, **{k: routes[name][k] for k in ["lpr_total", *ROUTES, "share_family",
                                                           "share_other"]}, "muslim_share_2010": pew})
    with open(DERIVED / "route_units.csv", "w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(units[0]))
        writer.writeheader()
        writer.writerows(units)
    print(f"  ✓ {len(units)} units joined; dropped: {[d['birthplace'] for d in dropped]}")

    def column(name, rows):
        return np.array([float(r[name]) for r in rows])

    results, decisive = [], {}
    for outcome, (label, with_degree_share) in OUTCOMES.items():
        for model, sample in (("1", units), ("2", units),
                              ("3", [u for u in units if u["birthplace"] not in OUTSIDE_LPR_FLOW])):
            terms = ["muslim_share_2010"] + ([] if model == "1" else ROUTES)
            if model != "1" and with_degree_share:
                terms.append("degree_share_25_64")
            y = 100 * column(outcome, sample)
            X = np.column_stack([np.ones(len(sample))] + [column(t, sample) for t in terms])
            for weighting, w in (("unweighted", None), ("weighted", column("entered_2000_plus", sample))):
                beta, se = ols_hc3(y, X, w)
                for term, b, s in zip(["intercept", *terms], beta, se):
                    results.append({"outcome": outcome, "model": model, "weighting": weighting,
                                    "term": term, "coef": round(float(b), 3), "se_hc3": round(float(s), 3),
                                    "ci_low": round(float(b - 1.96 * s), 3),
                                    "ci_high": round(float(b + 1.96 * s), 3), "n": len(sample)})
                    if term == "muslim_share_2010" and weighting == "unweighted":
                        decisive[(outcome, model)] = (float(b), float(b - 1.96 * s), float(b + 1.96 * s))
    with open(DERIVED / "route_models.csv", "w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(results[0]))
        writer.writeheader()
        writer.writerows(results)

    print(f"\n  Muslim-share coefficient, percentage points (origin at 100% against 0%), unweighted")
    print(f"  {'outcome':44} {'model 1':>22} {'model 2':>22} {'model 3':>22}")
    for outcome, (label, _) in OUTCOMES.items():
        cells = [f"{decisive[(outcome, m)][0]:+6.1f} [{decisive[(outcome, m)][1]:+6.1f},{decisive[(outcome, m)][2]:+6.1f}]"
                 for m in "123"]
        print(f"  {label:44} {cells[0]:>22} {cells[1]:>22} {cells[2]:>22}")

    verdict = {}
    for outcome, penalty_sign in (("p1_medicaid_degree_25_64", 1), ("p2_income_100k_degree_25_64", -1)):
        (b1, _, _), (b2, low2, high2) = decisive[(outcome, "1")], decisive[(outcome, "2")]
        verdict[outcome] = {
            "model1": round(b1, 2), "model2": round(b2, 2), "model2_ci": [round(low2, 2), round(high2, 2)],
            "fell_by_more_than_half": abs(b2) < 0.5 * abs(b1),
            "model2_interval_spans_zero": low2 <= 0 <= high2,
            "penalty_persists": (penalty_sign * b2 > 0) and not (low2 <= 0 <= high2),
        }
    route = all(v["fell_by_more_than_half"] and v["model2_interval_spans_zero"] for v in verdict.values())
    persists = all(v["penalty_persists"] for v in verdict.values())
    verdict["reading"] = ("route accounts for it" if route else
                          "an origin-religion penalty persists" if persists else
                          "not settled by this design")
    verdict["dropped_units"] = dropped
    (DERIVED / "route_verdict.json").write_text(json.dumps(verdict, indent=1))
    print(f"\n  decision rule → {verdict['reading']}")


if __name__ == "__main__":
    sys.exit(main())
