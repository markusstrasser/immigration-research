"""The rough re-key to non-Hispanic Black residents on the v4 case adopted 2026-09-29 (case key sept29). Not the engine.

The September 27 outputs of this lane (rekey.py) stay as they are. The sept29 re-key runs through the white lane's
library (white_replacement_2026_09_28/rekey_sept29.py), whose code path reproduces this lane's September 27 rows
(its gate) and which carries the sept29 rules: the case's lines, responses and capital; the two receipt lines v4
splits out keyed on housing subsidies and renters' consumption; the pension accrual at each group's own accrual per
tax dollar (the NH Black ratios from accrual_black.py); state prices and road miles from each group's own residence and
driving; the engine's union-only corrections for the union alone. The frame is audit row 4's, so the union prices the
39,712,493 people the account prices; the NH Black group is its own CPS count. The library's module docstring and
this lane's RESULT section "v4 case (sept29)" give every rule and its alternative.

Two bases: accrual (the case, $371.4146 / 434.8410bn for the engine's union at 48 / 11) and cash (the cash set,
$294.7011 / 361.8175bn). The normalized gap (the group's no-response balance less its population share of the
national balance) is defined on the cash basis only: the national lines are cash totals, so a group's accrued
pension has no national counterpart to be set against.

Gates (exit 1, nothing written): the library's (the dumps are the case; the engine's union reproduces each dump's cost;
the pension rule reproduces the engine's accrual amounts; every line is keyed; the September 27 rows reproduce;
row 4 matches the account's count); and here, on the September 27 dump and published weights, the library reproduces
this lane's rekey_summary.csv cost, gap and old-age columns for all three groups (5e-5, printed at 4 decimals); the
attribution's first step is that file's NH Black cost and its last two are this run's (5e-5).
Beside the rules: rule_alternatives_sept29.csv (the library's four alternatives, plus the NH Black benefit-tax rate at
the uncalibrated proxy and every NH Black career starting at 21) and attribution_sept29.csv (the September 27 case on
published and row-4 weights, the sept29 cash set without and with rule 4, the case with the accrual).
Outputs: derived/rekey_summary_sept29.csv, rekey_by_program_sept29.csv, rekey_line_shares_sept29.csv,
rule_alternatives_sept29.csv, attribution_sept29.csv, attribution_buckets_sept29.csv (the library's buckets).
Run from the repository root after engine_lines.cjs sept29 / sept29_cash, accrual_black.py and the white lane's
v4_inputs.py and accrual_white.py:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/black_comparator_rough_2026_09_28/rekey_sept29.py

--case oct05 re-keys the v5 case adopted 2026-10-05 (main_case_2026_10_05) through the library's oct05 rules (its
docstring): the union's side is the rough union on the identified 39,712,493 at v5's responses plus the 3,039,720 added
people at the case lane's own amounts, 42,752,213 in all; the NH Black group keeps its own CPS count, so its per-member
ratios to the union move with the union's cost per member. The attribution adds step 4 (the lineage). Outputs carry the
key (rekey_summary_oct05.csv, ...). Run it after the white lane's engine_lines.cjs oct05 / oct05_cash / oct05_union /
oct05_union_cash.
"""
from __future__ import annotations

import csv
import importlib.util
import sys
from pathlib import Path

sys.dont_write_bytecode = True   # read-only imports from other lanes: write nothing beside them

import pandas as pd  # noqa: E402

LANE = Path(__file__).resolve().parent
FISCAL = LANE.parent
DER = LANE / "derived"
spec = importlib.util.spec_from_file_location("rekey_sept29_white", FISCAL / "white_replacement_2026_09_28/rekey_sept29.py")
W = importlib.util.module_from_spec(spec)
spec.loader.exec_module(W)
R = W.R
ENDS, BASES = W.ENDS, W.BASES
GROUPS = {"mexican_origin_engine": "eng", "mexican_origin_rough": "mex", "nh_black_rough": "blk"}
# This lane's program groups (rekey.py BUCKETS), with the lines v4 adds
BUCKETS = {
    "income taxes": ["federal_income_tax", "state_local_income_tax", "other_personal_tax"],
    "payroll taxes and Medicare premiums": ["employee_oasdi", "employer_oasdi", "employee_hi", "employer_hi",
                                            "self_employment_oasdi_hi", "medicare_supplementary_premiums",
                                            "other_domestic_social_contributions"],
    "sales, excise, customs, fees": ["general_sales_tax", "excise_selective_sales", "customs_duties",
                                     "personal_current_transfers", "personal_motor_vehicle"],
    "capital, property, production taxes": ["corporate_capital", "corporate_labor", "modeled_owner_property",
                                            "remaining_production_property", "other_production_taxes",
                                            "business_current_transfers", "personal_property_tax",
                                            "government_asset_income", "enterprise_surplus",
                                            "housing_enterprise_surplus", "tenant_occupied_property"],
    "Social Security and Medicare": ["social_security", "medicare", "railroad_retirement", "pension_guaranty"],
    "Medicaid": ["medicaid_and_chip_other_medical"],
    "schools and colleges": ["education_services", "education_benefits", "school_reprice", "college_rekey"],
    "police, courts, prisons": ["public_order_safety", "state_price_public_order_safety"],
    "SNAP, SSI, housing, cash aid, credits, other welfare": [
        "snap", "ssi", "housing_subsidies", "family_and_general_assistance", "other_state_welfare", "energy_assistance",
        "refundable_tax_credits", "income_security_services", "unemployment", "workers_compensation",
        "temporary_disability", "black_lung"],
    "veterans and military medical": ["veterans_pension_disability", "veterans_readjustment", "veterans_other",
                                      "veterans_life_insurance", "military_medical"],
}
PER_HEAD = "per head: government, defense, interest, roads"


def write(name, rows):
    with open(DER / name, "w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        wr.writeheader()
        wr.writerows(rows)


def by_program(rows, pop_share):
    """Per program group: the cost to others (effects: spending saved less receipts lost) and the no-response gap."""
    cost, gap = {}, {}
    for side, lid, nat, amt, resp in rows:
        if lid in R.ZERO:
            continue
        b = next((k for k, v in BUCKETS.items() if lid in v), PER_HEAD)
        sgn = 1 if side == "receipts" else -1
        cost[b] = cost.get(b, 0.0) - sgn * amt * resp
        gap[b] = gap.get(b, 0.0) + sgn * (amt - pop_share * nat)
    return cost, gap


def main(case="sept29"):
    W.use_case(case)
    W.setup()
    print("[this lane's September 27 rows through the library, published weights]", flush=True)
    # setup() leaves the frame on row 4; the published-weight check runs on a fresh copy of the weights and shares.
    w4, n4 = R.w.copy(), R.TARGET
    W.set_frame(W.PUBLISHED_W.copy(), W.DUMP27["low"]["target_population"], W.DUMP27)
    ref = pd.read_csv(DER / "rekey_summary.csv")
    for lab, g in GROUPS.items():
        sc = "eng" if g == "eng" else R.scenario(g, scaled=g != "blk")
        for end in ENDS:
            r = W.run29(sc, end, v4=False, dump=W.DUMP27)[0]
            want = ref.query("group == @lab and end == @end").iloc[0]
            for col in ("cost", "gap", "cost_ex_old_age", "gap_ex_old_age", "capital"):
                W.gate(f"{lab} {end} {col} reproduces rekey_summary.csv", abs(r[col] - float(want[col])) < 5e-5,
                       f"{r[col]:.4f} vs {float(want[col]):.4f}")
    W.stop_if_failed()
    W.set_frame(w4, n4, W.DUMP["cash"])
    W.UNION_SC = R.scenario("mex")

    summary, programs, shares = [], [], {}
    res, alt = {}, {}
    for b in BASES:
        for end in ENDS:
            for lab, g in GROUPS.items():
                sc = "eng" if g == "eng" else (W.UNION_SC if g == "mex" else R.scenario("blk", scaled=False))
                res[(b, lab, end)] = W.run29(sc, end, b)
                # the alternative to rule 4: the group at national prices and the September 27 road keys
                alt[(b, lab, end)] = W.run29(sc, end, b, rule4="union")[0]["cost"]
    W.stop_if_failed()
    # The library's alternatives, and two of this lane's: the NH Black benefit-tax rate at the uncalibrated proxy, and
    # every NH Black member's career starting at 21
    groups = {"mexican_origin_rough": W.UNION_SC, "nh_black_rough": R.scenario("blk", scaled=False)}
    rows = {(r["group"], r["entry_rule"], r["scenario"]): r for r in csv.DictReader(open(DER / "accrual_ratios.csv"))}
    proxy = pd.read_csv(DER / "benefit_tax_proxy.csv").set_index("group")
    extra = [("NH Black benefit-tax rate",
              f"the NH Black relative benefit-tax rate at the uncalibrated statutory proxy "
              f"({proxy.loc['nh_black', 'relative_rate_proxy']:.6f}, not scaled by the union's measured / proxy ratio)",
              ("accrual",), {**W.ACC, "black": W.acc_entry(rows[("nh_black", "immigrants_at_arrival", "payable")],
                                                          rel=float(proxy.loc["nh_black", "relative_rate_proxy"]))}),
             ("NH Black career entry", "every NH Black member's career starting at 21 (immigrants too)", ("accrual",),
              {**W.ACC, "black": W.acc_entry(rows[("nh_black", "all_at_21", "payable")])})]
    alt_rows = W.alternatives(groups, extra)
    attr_rows = W.attribution(groups)
    final = {"4": "accrual"} if W.LINEAGE_ON else {"2": "cash", "3": "accrual"}    # the steps that are the case's runs
    for r in attr_rows:
        if r["step"] in final:
            want = res[(final[r["step"]], r["group"], r["end"])][0]["cost"]
            W.gate(f"attribution step {r['step']} is the {W.CASE} run {r['group']} {r['end']}", abs(float(r["cost_bn"]) - want) < 5e-5)
    for end in ENDS:
        want = float(ref.query("group == 'nh_black_rough' and end == @end").cost.iloc[0])
        got = W.STEP_COST[("a", "nh_black_rough", end)][0]
        W.gate(f"attribution step a is this lane's rekey_summary.csv nh_black_rough {end}", abs(got - want) < 5e-5, f"{got:.4f}")
    W.stop_if_failed()
    for (b, lab, end), (r, rows, _, terms, acc) in res.items():
        eng = res[(b, "mexican_origin_engine", end)][0]
        rough = res[(b, "mexican_origin_rough", end)][0]
        pm = r["cost"] * 1e9 / r["population"]
        summary.append({"basis": b, "group": lab, "end": end, "spec": W.DUMP[b][end]["spec"],
                        **{k: f"{v:.4f}" for k, v in r.items() if k not in ("population", "pop_share", "gap", "gap_ex_old_age")},
                        "gap": f"{r['gap']:.4f}" if b == "cash" else "",
                        "gap_ex_old_age": f"{r['gap_ex_old_age']:.4f}" if b == "cash" else "",
                        "population": f"{r['population']:.0f}", "pop_share": f"{r['pop_share']:.6f}",
                        "cost_per_member": f"{pm:.0f}",
                        "gap_per_member": f"{r['gap'] * 1e9 / r['population']:.0f}" if b == "cash" else "",
                        "per_member_over_engine_union": f"{pm / (eng['cost'] * 1e9 / eng['population']):.4f}",
                        "per_member_over_rough_union": f"{pm / (rough['cost'] * 1e9 / rough['population']):.4f}",
                        "cost_at_national_prices": f"{alt[(b, lab, end)]:.4f}",
                        "per_member_at_national_prices_over_engine_union":
                            f"{alt[(b, lab, end)] / r['population'] / (eng['cost'] / eng['population']):.4f}"})
        if end == "low":
            cost, gap = by_program(rows, r["pop_share"])
            for k in list(BUCKETS) + [PER_HEAD]:
                programs.append({"basis": b, "group": lab, "program": k, "cost_bn": f"{cost.get(k, 0.0):.4f}",
                                 "cost_per_member": f"{cost.get(k, 0.0) * 1e9 / r['population']:.0f}",
                                 "gap_bn": f"{gap.get(k, 0.0):.4f}" if b == "cash" else "",
                                 "gap_per_member": f"{gap.get(k, 0.0) * 1e9 / r['population']:.0f}" if b == "cash" else ""})
            for k, v in (("capital return", r["capital"]), ("production gain (subtracted)", -r["production_gain"])):
                programs.append({"basis": b, "group": lab, "program": k, "cost_bn": f"{v:.4f}",
                                 "cost_per_member": f"{v * 1e9 / r['population']:.0f}", "gap_bn": "", "gap_per_member": ""})
            if b == "accrual":
                shares[lab] = rows
    line_rows = []
    for i, (side, lid, nat, _, resp) in enumerate(shares["mexican_origin_engine"]):
        row = {"side": side, "line": lid, "national_bn": f"{nat:.4f}", "response_low": f"{resp:.4f}"}
        for lab in GROUPS:
            amt = shares[lab][i][3]
            row[f"amount_{lab}_bn"] = f"{amt:.4f}"
            row[f"share_{lab}"] = f"{amt / nat:.6f}" if abs(nat) > 1e-6 else ""
        line_rows.append(row)
    write(f"rekey_summary_{W.CASE}.csv", summary)
    write(f"rekey_by_program_{W.CASE}.csv", programs)
    write(f"rekey_line_shares_{W.CASE}.csv", line_rows)
    write(f"rule_alternatives_{W.CASE}.csv", alt_rows)
    write(f"attribution_{W.CASE}.csv", attr_rows)
    write(f"attribution_buckets_{W.CASE}.csv", W.attribution_buckets(groups))
    s = pd.DataFrame(summary)
    print(s[["basis", "group", "end", "cost", "cost_per_member", "gap", "cost_ex_old_age", "capital",
             "per_member_over_engine_union", "per_member_over_rough_union"]].to_string(index=False))
    a = pd.DataFrame(alt_rows).query("group == 'nh_black_rough'")
    print(a[["rule", "basis", "end", "cost_bn", "change_bn"]].to_string(index=False))
    t = pd.DataFrame(attr_rows).query("group == 'nh_black_rough'")
    print(t[["step", "basis", "end", "cost_bn", "cost_per_member", "change_bn"]].to_string(index=False))


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--case", default="sept29", choices=list(W.CASES), help="sept29 (default) or oct05 (v5, the lineage on the union's side)")
    main(ap.parse_args().case)
