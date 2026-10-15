"""Partial counted group beside the complete-lineage other-resident account.

Scope B supplies counted-member group components only. It retains the complete
lineage's other-resident account, so it cannot define a world welfare total.
"""

import pandas as pd

import beside_arms as B
import g2_premium as G
import mexico as MX
import mexico_capital as K
import valuation as V
from mexico_prices import budget_from_gdp

def require(ok, why):
    if not ok:
        raise SystemExit("[BLOCKED] counted scope: " + why)


def partial_group(I):
    """Exclude missing group recipients while retaining complete-lineage others."""
    require("origin_line" in I["vgen"], "group source identity absent")
    out = dict(I)
    out["vgen"] = I["vgen"][~I["vgen"].origin_line.astype(str).str.startswith("coverage_")].copy()
    out["scope"] = "B_partial_counted_group_complete_others_beside"
    out["scope_enters_total"] = False
    out["world_total_status"] = "[NOT DEFINED] partial group beside complete-lineage others"
    out["coverage_economic_counterfactual"] = dict(scope=out["scope"],
        item12_group_recipients="excluded", item12_other_resident_effects="complete lineage retained")
    return out


def economic_inputs(I, d):
    parents = I.get("parents_schooling")
    if parents is None:
        parents, _ = G.parents_schooling()
    trans = G.transitions()
    cells = {ppp: G.mexico_cells(ppp) for ppp in ("gdp", "consumption")}
    premium = B.premium_table(d, parents, trans, cells)
    profiles = premium.attrs["g3_pay_profiles"]
    rates = MX.ppp()
    premium["source_ppp_divisor"] = premium.ppp.map({"gdp": rates["PA.NUS.PPP"], "consumption": rates["PA.NUS.PRVT.PP"]})
    ages = d[d.gen.ne("")].groupby(["gen", "A_AGE"]).pw.sum().rename("persons").reset_index()
    ages = ages.rename(columns={"gen": "generation", "A_AGE": "age"})
    budget = V.mexico_budget(I["basis"], ages=ages, premium=premium)
    budget["recipient_bn"] = budget.bn
    budget["fiscal_bn"] = budget.bn
    share = I.get("public_pension_share", I.get("pension_meta", {}).get("public_pension_share", 1.))
    budget.loc[budget.item.str.contains("pensions paid", regex=False), "fiscal_bn"] *= share
    return dict(g2=premium, g3_pay_profiles=profiles, ages=ages,
                mxb=budget_from_gdp(budget, rates["PA.NUS.PPP"]))


def build(I, d):
    require(I.get("pension_basis") == "matched_cash", "matched cash required")
    require("pw_counted" in d and "coverage_pw" in d, "completed economic frame required")
    counted = d.assign(pw=d.pw_counted).drop(columns=["pw_counted", "coverage_pw"])
    counted.attrs = {k: v for k, v in d.attrs.items() if k != "coverage_economic_counterfactual"}
    out = partial_group(I)
    out.update(economic_inputs(out, counted))
    out["pos"] = I["pos"].copy()
    for name in tuple(out["pos"].columns):
        if name.startswith("counted_"):
            out["pos"][name.removeprefix("counted_")] = out["pos"][name]
    out["capital_people"] = counted
    out.pop("capital_projected_gen_industry_wages", None)
    out["capital_projected_gen_industry_wages"] = K.projected_shapes(out)
    return out, counted
