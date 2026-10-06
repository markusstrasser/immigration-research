#!/usr/bin/env python3
"""Main case v5 on a closed budget: what other residents pay if the lineage shares the fix.

The adopted case (main_case_2026_10_05) is current law. No rule closes the federal budget, so the whole of the
group's net cost counts as a cost to other residents. Orrenius, Viard & Zavodny (AEI, September 2025, p. 11) argue
that every household that joins the population bears part of the tax rises or spending cuts that must eventually
close the fiscal gap, so a current-policy account overstates the burden on everyone else. This lane prices that
argument beside the case; it never replaces the headline.

Let F be the permanent yearly improvement in the primary balance that closes the gap with the group present, and s
the group's share of it. Other residents then pay (1 - s) F instead of F - D, where D is the part of the group's
cost that current law leaves to borrowing; the rest of the group's cost G falls on them today either way. So

    cost to others on a closed budget = G - s * F.

Inputs:
  G   the case's ends, main and cash sets (main_case_2026_10_05/derived/summary.json).
  s   six sharing rules. Each is the lineage's share of the account's national frame (NG / NC, the decomposition's
      own per-capita base) times the group's amount relative to as many average residents, from the v5
      decomposition's line groups (main_case_decomposition_2026_09_29/derived/decomposition_lines_oct05*.csv,
      parts "total" and "shared"), except per_household:
        per_person       every resident pays the same (the most the group could carry of a tax fix);
        per_household    every household pays the same, AEI's own rule (derived/household_share.json, households.py);
        federal_benefits the federal benefit lines cut in proportion: Social Security and Medicare, Medicaid,
                         refundable credits, cash, food and housing benefits, veterans' and other health (each set at
                         its own valuation, so the cash set's Social Security share is its few retirees');
        all_taxes        every tax the account counts, in proportion;
        federal_taxes    income and payroll taxes raised in proportion, at FY2024's federal mix (OMB Historical
                         Table 2.1: individual income $2,426.067bn, social insurance $1,708.926bn);
        income_tax       the individual income tax alone (a progressive fix).
  F   published fiscal gaps as shares of GDP (sources.json), times 2024 GDP ($29.30tn, BEA NIPA T1.1.5, 26 August
      2026 vintage, as labor_mobility_insurance_2026_09_23/RESULT.md quotes it). Every current gap pays scheduled
      Social Security and Part A benefits after the trust funds are depleted; the account values the promises it
      charges at payable benefits (pension_accrual_2026_09_28), so for the account those funds are closed already.
      Each gap is therefore also taken less that post-depletion shortfall over its own window
      (derived/trust_funds.json, trust_funds.py), on the reading of the baseline the gap rests on and on the other
      reading beside it. That general-fund version is the one consistent with the case.

Gates (exit with [BLOCKED] before writing):
  - the decomposition's parts add to the case at both ends and in both sets (shared + age + taxes + use = total);
  - per_person with F at the case's own average-resident gap (shared part x NC / NG) reproduces the printed excess
    over average residents (ladder 269: $280.5 / 297.4bn), tying the arm to a number the case already prints;
  - the household share was computed on the decomposition's frame;
  - every rule's share lies in (0, 1), every general-fund gap is positive, and the cost falls as F rises.

Writes derived/closed_budget.csv (fix x basis x rule x set x end), derived/shares.csv, derived/summary.json (the
ranges the docs quote) and derived/audit.json. Run households.py and trust_funds.py first. From the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/closed_budget_2026_10_06/closed_budget.py
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LANE = Path(__file__).resolve().parent
OUT = LANE / "derived"
CASE = ROOT / "infra/immigration-fiscal/main_case_2026_10_05/derived/summary.json"
DECOMP = ROOT / "infra/immigration-fiscal/main_case_decomposition_2026_09_29/derived"
SOURCES = LANE / "sources.json"
HOUSEHOLDS = OUT / "household_share.json"
TRUST_FUNDS = OUT / "trust_funds.json"

TAXES = ["income_taxes", "payroll_taxes", "consumption_taxes", "property_taxes", "other_receipts"]
FEDERAL_BENEFITS = ["social_security_medicare", "medicaid", "refundable_credits", "cash_food_housing_benefits",
                    "health_veterans"]
PARTS = ["shared", "age_structure", "taxes_at_given_ages", "service_use_at_given_ages"]
RULES = ["per_person", "per_household", "federal_benefits", "all_taxes", "federal_taxes", "income_tax"]
FED_MIX = {"income_taxes": 2426.067, "payroll_taxes": 1708.926}  # OMB Historical Table 2.1, FY2024, $bn
GDP_2024_BN = 29300.0  # BEA NIPA T1.1.5, 26 August 2026 vintage
EXCESS_PRINTED = {"low": 280.5, "high": 297.4}  # ladder 269, one decimal
SETS = {"main": ("oct05", "main_case"), "cash": ("oct05_cash", "cash_set")}
CENTRAL = {"fix": "ag2026_cl", "basis": "general fund (cbo reading)", "rule": "per_household"}


def blocked(msg: str) -> None:
    print(f"[BLOCKED] {msg}", file=sys.stderr)
    sys.exit(2)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_lines(key: str) -> dict:
    """{end: {part: {line_group: bn}}} from the decomposition's line table (positive = cost to others)."""
    out: dict = {"low": {}, "high": {}}
    with open(DECOMP / f"decomposition_lines_{key}.csv", newline="") as f:
        for r in csv.DictReader(f):
            for end in ("low", "high"):
                out[end].setdefault(r["part"], {})[r["line_group"]] = float(r[f"{end}_bn"])
    return out


def case_ends(summary: dict, name: str) -> dict:
    band = summary[name]["band_bn"] if name == "cash_set" else summary[name]
    return {"low": float(band[0]), "high": float(band[1])}


def ratios(parts: dict, household_ratio: float) -> dict:
    """The group's amount over as many average residents', by sharing rule."""
    sh, tot = parts["shared"], parts["total"]
    tax = lambda d, ks: -sum(d[k] for k in ks)  # receipts carry negative signs
    benefits = lambda d: sum(d[k] for k in FEDERAL_BENEFITS)
    r_inc = tot["income_taxes"] / sh["income_taxes"]
    r_pay = tot["payroll_taxes"] / sh["payroll_taxes"]
    w = FED_MIX["income_taxes"] / (FED_MIX["income_taxes"] + FED_MIX["payroll_taxes"])
    return {
        "per_person": 1.0,
        "per_household": household_ratio,
        "federal_benefits": benefits(tot) / benefits(sh),
        "all_taxes": tax(tot, TAXES) / tax(sh, TAXES),
        "federal_taxes": w * r_inc + (1 - w) * r_pay,
        "income_tax": r_inc,
    }


def fixes(src: dict, tf: dict) -> list[dict]:
    """Each published gap as published, and less the trust funds' post-depletion shortfall over its window."""
    rows = []
    for g in src["fiscal_gaps"]:
        base = {"fix": g["id"], "law": g["law"], "window": g["window"]}
        rows.append(base | {"basis": "as published", "pct_gdp": g["pct_gdp"], "trust_funds_pct_gdp": 0.0})
        if not g["includes_scheduled_social_insurance"] or g["reading"] is None:
            continue
        if g["window"] == tf["pv_75_year"]["window"]:
            comp = tf["pv_75_year"]["oasdi"] + tf["pv_75_year"]["hi"]
            rows.append(base | {"basis": "general fund (trustees 75-year obligations)", "pct_gdp": g["pct_gdp"] - comp,
                                "trust_funds_pct_gdp": comp})
            continue
        w = tf["windows"][g["window"]]
        for reading in (g["reading"], "trustees" if g["reading"] == "cbo" else "cbo"):
            comp = w[reading]["total"]
            rows.append(base | {"basis": f"general fund ({reading} reading)", "pct_gdp": g["pct_gdp"] - comp,
                                "trust_funds_pct_gdp": comp})
    return rows


def span(rows: list[dict], key: str) -> list[float]:
    vals = [float(r[key]) for r in rows]
    return [min(vals), max(vals)]


def main() -> None:
    summary = json.loads(CASE.read_text())
    dsum = json.loads((DECOMP / "summary_oct05.json").read_text())
    NG, NC = dsum["frame"]["row4"]["NG"], dsum["frame"]["row4"]["NC"]
    share = NG / NC
    src = json.loads(SOURCES.read_text())
    hh = json.loads(HOUSEHOLDS.read_text())
    tf = json.loads(TRUST_FUNDS.read_text())

    lines = {s: read_lines(key) for s, (key, _) in SETS.items()}
    G = {s: case_ends(summary, name) for s, (_, name) in SETS.items()}

    gates = []
    for s in SETS:
        for end in ("low", "high"):
            p = lines[s][end]
            total = sum(p["total"].values())
            parts = sum(sum(p[k].values()) for k in PARTS)
            ok = abs(total - G[s][end]) < 1e-4 and abs(parts - total) < 1e-4  # the csv rounds each cell to 1e-6
            gates.append({"gate": f"{s} {end}: decomposition parts add to the case", "pass": ok,
                          "detail": f"total {total:.6f}, parts {parts:.6f}, case {G[s][end]:.6f}"})
    for end in ("low", "high"):
        sh = sum(lines["main"][end]["shared"].values())
        f_rule = sh / share  # the national gap under the case's own rules
        excess = G["main"][end] - share * f_rule
        ok = abs(round(excess, 1) - EXCESS_PRINTED[end]) < 1e-9
        gates.append({"gate": f"main {end}: per_person at the case's own gap reproduces the printed excess",
                      "pass": ok, "detail": f"{excess:.4f} vs {EXCESS_PRINTED[end]}"})
    gates.append({"gate": "household share computed on the decomposition's frame",
                  "pass": abs(hh["frame"]["NG"] - NG) < 1e-2 and abs(hh["frame"]["NC"] - NC) < 1.0,
                  "detail": f"{hh['frame']} vs NG {NG}, NC {NC}"})
    fix_rows = fixes(src, tf)
    for fx in fix_rows:
        if fx["pct_gdp"] <= 0:
            gates.append({"gate": f"{fx['fix']} {fx['basis']}: gap positive", "pass": False, "detail": fx["pct_gdp"]})

    share_rows, out_rows = [], []
    for s in SETS:
        for end in ("low", "high"):
            rat = ratios(lines[s][end], hh["share"] / share)
            for rule in RULES:
                r = rat[rule]
                sr = share * r
                if not 0 < sr < 1:
                    gates.append({"gate": f"{s} {end} {rule}: share in (0, 1)", "pass": False, "detail": f"{sr}"})
                share_rows.append({"set": s, "end": end, "rule": rule, "ratio_to_average": f"{r:.6f}",
                                   "share": f"{sr:.6f}"})
                prev = None
                for fx in sorted(fix_rows, key=lambda x: x["pct_gdp"]):
                    F = fx["pct_gdp"] / 100 * GDP_2024_BN
                    cost = G[s][end] - sr * F
                    if prev is not None and cost > prev + 1e-12:
                        gates.append({"gate": f"{s} {end} {rule}: cost falls as F rises", "pass": False, "detail": ""})
                    prev = cost
                    out_rows.append({"fix": fx["fix"], "law": fx["law"], "window": fx["window"], "basis": fx["basis"],
                                     "pct_gdp": f"{fx['pct_gdp']:.4f}",
                                     "trust_funds_pct_gdp": f"{fx['trust_funds_pct_gdp']:.4f}",
                                     "fix_bn": f"{F:.3f}", "rule": rule, "set": s, "end": end, "share": f"{sr:.6f}",
                                     "case_bn": f"{G[s][end]:.6f}", "offset_bn": f"{sr * F:.6f}",
                                     "cost_to_others_bn": f"{cost:.6f}",
                                     "change_pct": f"{100 * (cost / G[s][end] - 1):.3f}"})
    bad = [g for g in gates if not g["pass"]]
    if bad:
        blocked("; ".join(f"{g['gate']} ({g['detail']})" for g in bad))

    def pick(s, **kw):
        return [r for r in out_rows if r["set"] == s and all(r[k] == v for k, v in kw.items())]

    general = lambda r: r["basis"].startswith("general fund")
    summ = {"lane": "closed_budget_2026_10_06", "gdp_2024_bn": GDP_2024_BN, "sets": {}}
    for s in SETS:
        central = {e: pick(s, end=e, **CENTRAL)[0] for e in ("low", "high")}
        block = {"case_bn": [G[s]["low"], G[s]["high"]],
                 "central": {"definition": CENTRAL, "fix_bn": float(central["low"]["fix_bn"]),
                             "offset_bn": [float(central[e]["offset_bn"]) for e in ("low", "high")],
                             "cost_bn": [float(central[e]["cost_to_others_bn"]) for e in ("low", "high")],
                             "change_pct": [float(central[e]["change_pct"]) for e in ("low", "high")]}}
        for law in ("current law", "current policy"):
            rows = [r for r in pick(s, law=law) if general(r)]
            block[law] = {"fixes": sorted({r["fix"] for r in rows}), "fix_bn": span(rows, "fix_bn"),
                          "offset_bn": span(rows, "offset_bn"), "cost_bn": span(rows, "cost_to_others_bn"),
                          "change_pct": span(rows, "change_pct")}
        aei = {e: pick(s, end=e, fix="aei_auerbach_gale_2013_low", basis="as published", rule="per_person")[0]
               for e in ("low", "high")}
        block["aei_as_published_per_person"] = {"cost_bn": [float(aei[e]["cost_to_others_bn"]) for e in ("low", "high")]}
        summ["sets"][s] = block

    OUT.mkdir(exist_ok=True)
    for name, rows in (("closed_budget.csv", out_rows), ("shares.csv", share_rows)):
        with open(OUT / name, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
            w.writeheader()
            w.writerows(rows)
    (OUT / "summary.json").write_text(json.dumps(summ, indent=1) + "\n")
    audit = {
        "lane": "closed_budget_2026_10_06",
        "inputs": {str(p.relative_to(ROOT)): sha(p) for p in
                   [CASE, DECOMP / "summary_oct05.json", DECOMP / "decomposition_lines_oct05.csv",
                    DECOMP / "decomposition_lines_oct05_cash.csv", SOURCES, HOUSEHOLDS, TRUST_FUNDS]},
        "frame": {"NG": NG, "NC": NC, "share": share},
        "gdp_2024_bn": GDP_2024_BN, "federal_mix_bn": FED_MIX,
        "gates": gates,
    }
    (OUT / "audit.json").write_text(json.dumps(audit, indent=1) + "\n")
    c = summ["sets"]["main"]
    print(f"wrote {len(out_rows)} rows; {len(gates)} gates pass; central {c['central']['cost_bn'][0]:.1f}-"
          f"{c['central']['cost_bn'][1]:.1f}bn; current law {c['current law']['cost_bn'][0]:.1f}-"
          f"{c['current law']['cost_bn'][1]:.1f}bn")


if __name__ == "__main__":
    main()
