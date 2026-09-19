#!/usr/bin/env python3
"""Reporting tables for the incidence lane. Reads derived/ and derived_F_percapita/."""
from pathlib import Path
import hashlib
import json
import pandas as pd
import numpy as np

HERE = Path(__file__).resolve().parent
UNION = "mexican_observed_total"
WHITE = "third_plus_nh_white"


def load(sub):
    d = HERE / sub
    audit = json.loads((d / "audit.json").read_text())
    digest = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
    if (audit.get("builder_sha256") != digest(HERE / "incidence.py")
            or audit.get("annual_audit_sha256") != digest(HERE.parent / "ledger_absolute_2026_09_17/derived/audit.json")):
        raise ValueError(f"[BLOCKED] stale incidence scenario {sub}; rebuild with an explicit correctional financing share")
    for name in ["incidence_matrix.csv", "account_by_level.csv", "interest.csv"]:
        if audit.get("output_sha256", {}).get(name) != digest(d / name):
            raise ValueError(f"[BLOCKED] stale or altered incidence output: {sub}/{name}")
    return (pd.read_csv(d / "incidence_matrix.csv"),
            pd.read_csv(d / "account_by_level.csv"),
            pd.read_csv(d / "interest.csv"))


def decile_table(m, group, geo, conv, pt):
    u = m[(m.group == group) & (m.geography == geo) & (m.convention == conv)
          & (m.passthrough == pt)]
    t = u.groupby("decile", as_index=False)[
        ["households", "income_dollars", "federal_dollars", "state_local_dollars",
         "total_dollars"]].sum()
    t["per_household"] = t.total_dollars / t.households
    t["pct_of_income"] = 100 * t.total_dollars / t.income_dollars
    return t


def tenure_decile(m, group, geo, conv, pt, value="per_household"):
    u = m[(m.group == group) & (m.geography == geo) & (m.convention == conv)
          & (m.passthrough == pt)]
    return u.pivot_table(index="decile", columns="tenure", values=value)


def main():
    out = []
    w = out.append
    m0, lvl0, int0 = load("derived")
    mF, lvlF, intF = load("derived_F_percapita")

    w("## A. Expanded partial account, item F = zero; correctional financing is the explicit recorded assumption\n")
    t = lvl0[lvl0.group.isin([UNION, WHITE, "all_native"])].copy()
    t["federal_share_of_deficit"] = t.federal_bn / t.total_bn
    w(t.round(3).to_string(index=False))

    w("\n\n## A2. Same, item F = per capita\n")
    t = lvlF[lvlF.group.isin([UNION, WHITE, "all_native"])].copy()
    t["federal_share_of_deficit"] = t.federal_bn / t.total_bn
    w(t.round(3).to_string(index=False))

    for name, m in [("F=zero", m0), ("F=per_capita", mF)]:
        for geo in ["US", "CA", "TX"]:
            for conv in sorted(m.convention.unique()):
                t = decile_table(m, UNION, geo, conv, 0.5)
                w(f"\n\n## B [{name}] {geo} / {conv} / passthrough 0.5 — union, by decile\n")
                w(t.assign(households=t.households/1e6,
                           total_bn=t.total_dollars/1e9,
                           federal_bn=t.federal_dollars/1e9,
                           state_local_bn=t.state_local_dollars/1e9)[
                    ["decile", "households", "federal_bn", "state_local_bn", "total_bn",
                     "per_household", "pct_of_income"]].round(3).to_string(index=False))

    w("\n\n## C. Pass-through spread, per household, US union, average convention\n")
    rows = []
    for name, m in [("F=zero", m0), ("F=per_capita", mF)]:
        for pt in [0.0, 0.5, 1.0]:
            u = m[(m.group == UNION) & (m.geography == "US")
                  & (m.convention == "average_pro_rata") & (m.passthrough == pt)]
            g = u.groupby("tenure").apply(
                lambda x: x.total_dollars.sum() / x.households.sum(), include_groups=False)
            rows.append(dict(arm=name, passthrough=pt, **{k: round(v, 1) for k, v in g.items()},
                             all_households=round(u.total_dollars.sum()/u.households.sum(), 1)))
    w(pd.DataFrame(rows).to_string(index=False))

    w("\n\n## D. Convention spread, per household, US union, passthrough 0.5\n")
    rows = []
    for name, m in [("F=zero", m0), ("F=per_capita", mF)]:
        for conv in sorted(m.convention.unique()):
            u = m[(m.group == UNION) & (m.geography == "US")
                  & (m.convention == conv) & (m.passthrough == 0.5)]
            rows.append(dict(arm=name, convention=conv,
                             total_bn=round(u.total_dollars.sum()/1e9, 2),
                             federal_bn=round(u.federal_dollars.sum()/1e9, 2),
                             state_local_bn=round(u.state_local_dollars.sum()/1e9, 2),
                             per_household=round(u.total_dollars.sum()/u.households.sum(), 0)))
    w(pd.DataFrame(rows).to_string(index=False))

    w("\n\n## E. Whites-as-control: the same matrix on the white reference's own balance\n")
    rows = []
    for name, m in [("F=zero", m0), ("F=per_capita", mF)]:
        for group, label in [(UNION, "Mexican-origin union"), (WHITE, "3rd+ NH white")]:
            for geo in ["US", "CA", "TX"]:
                u = m[(m.group == group) & (m.geography == geo)
                      & (m.convention == "average_pro_rata") & (m.passthrough == 0.5)]
                tot = u.total_dollars.sum()
                rows.append(dict(arm=name, group=label, geography=geo,
                                 financed_bn=round(tot/1e9, 2),
                                 per_household=round(tot/u.households.sum(), 0),
                                 pct_of_income=round(100*tot/u.income_dollars.sum(), 3)))
    w(pd.DataFrame(rows).to_string(index=False))

    w("\n\n## F. Interest arithmetic\n")
    w(int0.round(4).to_string(index=False))
    w("\n\n## F2. Interest arithmetic, item F = per capita\n")
    w(intF.round(4).to_string(index=False))

    w("\n\n## G. Tenure x decile, per household, US union, average, passthrough 0.5 and 1.0\n")
    for pt in [0.0, 1.0]:
        w(f"\npassthrough {pt}:")
        w(tenure_decile(m0, UNION, "US", "average_pro_rata", pt).round(0).to_string())

    w("\n\n## H. Property-tax structure\n")
    w(pd.read_csv(HERE / "derived/property_tax_structure.csv").round(4).to_string(index=False))

    text = "\n".join(str(x) for x in out)
    (HERE / "derived/TABLES.txt").write_text(text)
    print(text)


if __name__ == "__main__":
    main()
