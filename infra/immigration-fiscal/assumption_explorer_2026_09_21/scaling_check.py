"""How state and local spending by function scales with population across states (FY2022).

ln(spending) = a + b ln(population) over the 50 states (DC reported separately as a sensitivity).
b = 1: the function costs the same per resident in large and small states, so it behaves like a
congestible service; b well below 1: a fixed-cost public good. A cross-section is long-run
evidence about scale, not an estimate of the response to one group's presence.
Sources: Census 2022 State & Local Government Finance Table 1 (_cache/slf2022.xlsx, fetched
2026-09-21 from www2.census.gov/programs-surveys/gov-finances/tables/2022/22slsstab1.xlsx);
Census NST-EST2024-ALLDATA.csv POPESTIMATE2022.
"""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import numpy as np
import openpyxl

HERE = Path(__file__).resolve().parent
SLF_URL = "https://www2.census.gov/programs-surveys/gov-finances/tables/2022/22slsstab1.xlsx"
SLF_SHA256 = "4dd123c5ad520e33d9692f622d389a020e2d3a7e6e782763663854dd84643b9b"
POP = Path("/Users/alien/research-data/immigration-fiscal/data/external/census_popest_2024/NST-EST2024-ALLDATA.csv")
FUNCTIONS = {  # label -> Census line codes summed
    "Governmental administration (financial, judicial, buildings, other)": ["106", "107", "108", "109"],
    "Financial administration": ["106"], "Judicial and legal": ["107"], "Other governmental administration": ["109"],
    "Police protection": ["92"], "Correction": ["94"], "Fire protection": ["93"],
    "Elementary and secondary education": ["73"], "Direct general expenditure": ["66"],
}


BEA = Path("/Users/alien/research-data/immigration-fiscal/data/external/bea_nipa/Section3All_xls.xlsx")


def general_public_service_2024():
    """BEA Table 3.16 lines 3, 4, 6 (all governments) and 44, 45, 47 (federal), $bn, interest excluded."""
    rows = list(openpyxl.load_workbook(BEA, read_only=True, data_only=True)["T31600-A"].values)
    header = [r for r in rows if r and r[0] == "Line"][0]
    year = [i for i, x in enumerate(header) if str(x) == "2024"][0]
    cell = {int(r[0]): (str(r[1]).strip(), float(r[year])/1000) for r in rows if r and str(r[0]).isdigit()}
    expected = {3: "Executive and legislative", 4: "Tax collection and financial management", 6: "Other",
                44: "Executive and legislative", 45: "Tax collection and financial management", 47: "Other"}
    for line, label in expected.items():
        if not cell[line][0].startswith(label):
            raise ValueError(f"BEA Table 3.16 line {line} is no longer {label}")
    v = {k: cell[k][1] for k in expected}
    return dict(federal_executive_legislative=v[44], federal_tax_financial=v[45], federal_other=v[47],
                state_local_executive_legislative=v[3]-v[44], state_local_tax_financial=v[4]-v[45], state_local_other=v[6]-v[47])


def main():
    source = HERE/"_cache/slf2022.xlsx"
    if not source.exists():
        raise SystemExit(f"[BLOCKED] missing source: fetch {SLF_URL} to {source}")
    if hashlib.sha256(source.read_bytes()).hexdigest() != SLF_SHA256:
        raise SystemExit(f"[BLOCKED] stale source: {source} is not the file pinned on 2026-09-21")
    rows = list(openpyxl.load_workbook(source, read_only=True, data_only=True).worksheets[0].values)
    names = rows[8]
    columns = {str(name).strip(): i for i, name in enumerate(names) if name and i >= 2}
    columns.pop("United States Total", None)
    by_line = {str(r[0]).strip(): r for r in rows if r and r[0] is not None}
    with POP.open(encoding="latin-1") as stream:
        population = {r["NAME"]: float(r["POPESTIMATE2022"]) for r in csv.DictReader(stream) if r["SUMLEV"] == "040"}
    states = [s for s in columns if s in population]
    if len(states) != 51:
        raise ValueError(f"Expected 50 states and DC, matched {len(states)}")
    out = []
    for label, lines in FUNCTIONS.items():
        spend = {s: sum(float(by_line[l][columns[s]]) for l in lines)*1000 for s in states}  # table is in $ thousands
        for scope in ("50 states", "50 states + DC"):
            use = [s for s in states if scope.endswith("DC") or s != "District of Columbia"]
            x = np.log([population[s] for s in use]); y = np.log([spend[s] for s in use])
            X = np.column_stack([np.ones(len(x)), x])
            beta, *_ = np.linalg.lstsq(X, y, rcond=None)
            resid = y-X@beta
            cov = np.linalg.inv(X.T@X)*(resid@resid/(len(x)-2))
            out.append(dict(function=label, scope=scope, elasticity=round(float(beta[1]), 3), se=round(float(np.sqrt(cov[1, 1])), 3),
                            r2=round(1-float(resid@resid)/float(((y-y.mean())**2).sum()), 3),
                            us_per_capita=round(sum(spend.values())/sum(population.values()), 0), n=len(use)))
    composition = general_public_service_2024()
    b = {r["function"]: r["elasticity"] for r in out if r["scope"] == "50 states"}
    admin = b["Governmental administration (financial, judicial, buildings, other)"]
    total = sum(composition.values())
    state_local = composition["state_local_executive_legislative"]+composition["state_local_tax_financial"]+composition["state_local_other"]
    # Low: federal executive and legislative fixed, federal tax collection at the financial-administration
    # elasticity, state and local at the administration elasticity. High: everything at the administration elasticity.
    low = (state_local*admin+composition["federal_tax_financial"]*b["Financial administration"])/total
    summary = dict(elasticities=out, general_public_service_2024_bn=composition, state_local_share=round(state_local/total, 3),
                   composite_low=round(low, 2), composite_high=round(admin, 2))
    (HERE/"derived").mkdir(exist_ok=True)
    (HERE/"derived/scaling_check.json").write_text(json.dumps(summary, indent=1)+"\n")
    print(f"  general public service ex interest, 2024: {total:.1f} bn, {state_local/total:.0%} state and local; "
          f"implied response {summary['composite_low']} to {summary['composite_high']}")
    for r in out:
        if r["scope"] == "50 states":
            print(f"  {r['function'][:66]:66s} b={r['elasticity']:.3f} (se {r['se']:.3f})  R2={r['r2']:.2f}  ${r['us_per_capita']:,.0f}/head")


if __name__ == "__main__":
    main()
