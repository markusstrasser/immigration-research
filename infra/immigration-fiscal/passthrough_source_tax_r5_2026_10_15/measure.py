"""Conditional item 19 source-tax measurement; no unidentified point correction.

Native-First: consume pinned IRS cells and existing gated job keys. The scenario
parameters are estimand definitions, never measured replacement probabilities.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np

from job_keys import dump, se
from owner_tax_sources import direct_replacement_loss, gilti_current_us_tax

HERE = Path(__file__).resolve().parent
FORMS = {"s_corporation": "3", "partnership": "4", "sole_proprietor": "5"}
AGI_FORMS = {"s_corporation": "s_corporation", "partnership": "partnership", "sole_proprietor": "schedule_c"}
SECTORS = {"agriculture": "11", "mining": "21", "utilities": "22", "construction": "23",
           "durable": "31-33", "nondurable": "31-33", "wholesale": "42", "retail": "44-45",
           "transportation": "48-49", "information": "51", "finance": "52", "real_estate": "53",
           "professional": "54", "management": "55", "administrative": "56", "education": "61",
           "health": "62", "arts": "71", "accommodation_food": "72", "other_services": "81"}


def read(name):
    return json.loads((HERE / name).read_text())


def csv_out(name, rows):
    with (HERE / "derived" / name).open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def rates(year, signed=False):
    table = next(x for x in read("inputs/owner_agi_rates.json")["years"] if x["year"] == year)
    field = ("signed_net" if signed else "positive") + "_tax_after_credits_rate_positive_agi_only"
    return {f: table["by_form"][g][field] for f, g in AGI_FORMS.items()}


def key_for(row, keys):
    codes = sorted({SECTORS[s] for s in row["k1_sectors"]})
    form = FORMS[row["form"]]
    if len(codes) != 1:
        # The source merges 61+81. No equal split of IRS dollars is invented:
        # combine legal-form national/group payroll sufficient statistics.
        key = keys["pooled_shares"]["+".join(codes)][form]
        extra = keys["completion"]["pooled_shares"]["+".join(codes)][form]
    else:
        key = keys["shares"][codes[0]][form]
        extra = keys["completion"]["shares"][codes[0]][form]
    return None if key is None or extra is None else {**key, "completion": extra}


def source_rows():
    income = read("inputs/income_sectors.json")
    keys = read("derived/job_keys.json")
    rows, skipped = [], []
    for row in income["records"]:
        # Mining capital does not leave under item6. Agriculture mixes excluded
        # crops with SUSB-covered support; no unsupported forestry transport.
        if row["naics"] in ["11", "21", "99"] or not row["k1_sectors"]:
            skipped.append({"form": row["form"], "naics": row["naics"],
                            "direct_income_net_bn": row["direct_income_net_bn"],
                            "reason": "mining response0" if row["naics"] == "21" else "unmatched source scope"})
            continue
        key = key_for(row, keys)
        if key is None:
            skipped.append({"form": row["form"], "naics": row["naics"],
                            "direct_income_net_bn": row["direct_income_net_bn"],
                            "reason": "no matching SUSB form profile"})
            continue
        rows.append((row, key))
    return rows, skipped


def calculate(rows, v8, config):
    by_end = {}
    tax_rates = rates(config["owner_rate_year"], config["signed_rate"])
    allocations = read("inputs/income_sectors.json")["national"]["partnership"]["partner_allocations_bn"]
    national_individual_proxy = (allocations["individual_general"] + allocations["individual_limited"]) / allocations["all"]
    if not 0 <= national_individual_proxy <= 1:
        raise ValueError("[BLOCKED] national immediate individual allocation cannot serve as a fraction")
    for end in ["low", "high"]:
        parts, total_reps = [], np.zeros(161)
        for row, key in rows:
            form = row["form"]
            # No ScheduleC extrapolation of the top-owner death experiment.
            capital_fraction = config["sole_capital_fraction"] if form == "sole_proprietor" else config["sp_capital_fraction"]
            capital = row["direct_income_net_bn"] * capital_fraction
            normal = capital
            if end == "high":
                if config["high_rule"] == "normal_zero":
                    normal = 0.0
                elif config["high_rule"] == "tangible_equity_yield":
                    stock_fields = [row.get(k) for k in ["net_equity_book_bn", "other_investments_book_bn", "net_depreciable_book_bn", "land_book_bn"]]
                    # A missing stock is withheld and explicitly identified.
                    stock = 0.0 if any(x is None for x in stock_fields) else max(0.0, min(
                        stock_fields[0] - stock_fields[1], stock_fields[2] + stock_fields[3]))
                    normal = min(max(capital, 0.0), stock * config["normal_yield"])
                elif config["high_rule"] != "all_residual_normal":
                    raise ValueError("[BLOCKED] unknown normal-return rule")
            income = normal * config["income_scale"] * config["outside_owner_fraction"]
            # Partnership immediate individual allocations are an optional proxy,
            # never treated as a measured share of direct operating profits.
            owner_share = 1.0
            if form == "partnership" and config["ownership"] == "national_immediate_individual_proxy":
                # Sector signed allocations are not probabilities (e.g. utility
                # sector denominator nearly cancels). Use only the explicitly
                # named national proportional-allocation arm, never clip them.
                owner_share = national_individual_proxy
                income *= owner_share
            share = np.array(key["lineage"])
            federal = income * tax_rates[form]
            loss = direct_replacement_loss(income, tax_rates[form], config["domestic_share"],
                                           config["foreign_credit_fraction"], config["foreign_income_ratio"])
            if config["replacement_route"] == "cfc_current_inclusion":
                foreign_profit = max(income, 0) * config["foreign_income_ratio"]
                foreign_tax = foreign_profit * config["cfc_foreign_tax_rate"]
                tested = foreign_profit - foreign_tax
                residual = gilti_current_us_tax(tested, tested * config["cfc_inclusion_share"],
                                                foreign_tax)["current_us_residual"] if tested > 0 else 0.0
                loss = (1 - config["domestic_share"]) * (federal - residual)
            # State rate is a declared extra source-rate sensitivity; not an
            # assertion of a national PTE rate. Domestic replacement cancels it.
            state_loss = income * config["state_source_rate"] * (1 - config["domestic_share"])
            net = -(loss + state_loss) * share
            completion_cost = -(loss + state_loss) * key["completion"]
            # Completion's main amount held fixed across the existing CPS
            # replicates: this SE does not estimate completion uncertainty.
            total_reps += net + completion_cost
            parts.append(dict(line=f"owner_federal_{form}", naics=row["naics"],
                              source_income_bn=row["direct_income_net_bn"], capital_fraction=capital_fraction,
                              taxable_moving_income_bn=income, owner_share=owner_share,
                              lineage_key=float(share[0]), completion_key=key["completion"],
                              source_receipt_cost_bn=float(-federal * (share[0] + key["completion"])),
                              replacement_receipt_cost_bn=float((federal - loss) * (share[0] + key["completion"])),
                              state_source_cost_bn=float(-state_loss * (share[0] + key["completion"])),
                              base_cost_bn=float(net[0]), completion_cost_bn=float(completion_cost),
                              total_bn=float(net[0] + completion_cost)))
        # Completion and coverage prices are not measured for this new source:
        # expose, rather than silently flat-scale, the cost omitted here.
        by_end[end] = dict(total_bn=float(total_reps[0]), parts_by_line=parts,
                           cps_conditional_se_bn=se(total_reps),
                           uncertainty_rule="source-key CPS replicates only; completion main increment held fixed; no source-table, transport, ownership, normal-return or coverage uncertainty",
                           by_generation_bn={g: float(sum(
                               p["base_cost_bn"] * (key[g][0] / key["lineage"][0]) if key["lineage"][0] else 0
                               for p, (_, key) in zip(parts, rows))) for g in ["G1", "G2", "G3plus"]},
                           population_scope="row4 union plus v6 age-mix descendants plus item10 own observed job keys; item12 increment withheld pending own age/sex repricing",
                           omitted_population_people=v8["population"]["coverage"])
        by_end[end]["by_generation_bn"]["G3plus"] += sum(p["completion_cost_bn"] for p in parts)
        by_end[end]["by_generation_bn"]["added_G3plus"] = by_end[end]["total_bn"] - sum(by_end[end]["by_generation_bn"].values())
    return by_end


def scenarios():
    # No values below are unidentified 'central' values. Each named arm states
    # what it holds fixed and the scope in which its number is interpretable.
    base = dict(owner_rate_year=2023, signed_rate=False, sp_capital_fraction=.25,
                sole_capital_fraction=0, high_rule="all_residual_normal", normal_yield=0,
                domestic_share=0, foreign_credit_fraction=1, foreign_income_ratio=1,
                state_source_rate=0, income_scale=1, outside_owner_fraction=1,
                replacement_route="direct_owner", cfc_foreign_tax_rate=0, cfc_inclusion_share=1,
                ownership="all_individual_exposure")
    variants = {
        "foreign_full_ftc_top_owner_labor": {},
        "domestic_replacement": {"domestic_share": 1},
        "foreign_no_ftc_same_income": {"foreign_credit_fraction": 0},
        "foreign_half_ftc_same_income": {"foreign_credit_fraction": .5},
        "half_domestic_full_ftc": {"domestic_share": .5},
        "foreign_full_ftc_no_normal": {"high_rule": "normal_zero"},
        "foreign_full_ftc_all_profit_capital": {"sp_capital_fraction": 1, "sole_capital_fraction": 1},
        "foreign_full_ftc_sole_all_capital": {"sole_capital_fraction": 1},
        "foreign_full_ftc_immediate_individual": {"ownership": "national_immediate_individual_proxy"},
        "foreign_full_ftc_signed_owner_rate": {"signed_rate": True},
        "foreign_full_ftc_2022_owner_rate": {"owner_rate_year": 2022},
        "foreign_full_ftc_state_one_pp": {"state_source_rate": .01},
        "foreign_full_ftc_half_outside_owners": {"outside_owner_fraction": .5},
        "foreign_cfc_no_foreign_tax_no_qbai": {"replacement_route": "cfc_current_inclusion"},
        "foreign_cfc_ten_pct_tax_no_qbai": {"replacement_route": "cfc_current_inclusion", "cfc_foreign_tax_rate": .1},
        "foreign_cfc_normal_covered_by_qbai": {"replacement_route": "cfc_current_inclusion", "cfc_inclusion_share": 0},
    }
    normal_file = HERE / "inputs/owner_normal_yield.json"
    if normal_file.exists():
        normal = json.loads(normal_file.read_text())
        yield_2022 = next(x["rate"] for x in normal["observations"] if x["year"] == 2022)
        variants["foreign_full_ftc_tangible_normal_proxy"] = {"high_rule": "tangible_equity_yield", "normal_yield": yield_2022}
        variants["foreign_full_ftc_individual_tangible_normal"] = {"high_rule": "tangible_equity_yield", "normal_yield": yield_2022, "ownership": "national_immediate_individual_proxy"}
    return {name: {**base, **overrides} for name, overrides in variants.items()}


def main():
    rows, skipped = source_rows()
    v8, keys = read("derived/v8.json"), read("derived/job_keys.json")
    arms = {}
    for name, config in scenarios().items():
        by_end = calculate(rows, v8, config)
        arms[name] = dict(config=config, by_end=by_end)
    corp = keys["corporate"]
    w09 = {}
    for which in ["set", "cash"]:
        w09[which] = {}
        for end, response in [("low", 1), ("high", .37)]:
            original = sum(v8["parts"].values())
            # Positive control links the key calculation to the case's own parts.
            assert abs(original - corp["lineage"]["before_bn"][0]) < 1e-6
            union_lineage = (original - corp["lineage"]["after_bn"][0]) * response
            snap = v8["by_end"][which][end]
            completion = -snap["completion_corporate_receipts_bn"] * (corp["G3plus"]["ratio"] - 1)
            coverage = sum(cost * (corp[g]["ratio"] - 1)
                           for g, cost in snap["coverage_corporate_cost_by_generation_bn"].items())
            w09[which][end] = dict(total_bn=union_lineage + completion + coverage,
                                   union_and_v6_descendants_bn=union_lineage,
                                   completion_G3_profile_proxy_bn=completion,
                                   coverage_generation_profile_proxy_bn=coverage,
                                   proxy_warning="item10 own size/legal form and item12 missing-person selection unobserved; profile transport arms, not exact own-record repricing")
    item = dict(id="passthrough_source_tax", item_number=19, kind="post_engine", central=None,
                status="conditional measurement; parent must select an arm; no identified correction",
                arms=arms, source_scope_skips=skipped,
                interactions={"item6": "same jobs/capital premise; does not change corporate/property/production lines",
                              "item9": "direct operating bases exclude known upstream income; foreign geography not identified; replacement FTC/CFC residual must offset source loss",
                              "item10": "231 authoritative completion IDs and own industry/enterprise-size wages added once; G3 wage fill-in factor; new source-key replicate uncertainty not measured",
                              "item11": "no stayer tax reprice; owner overlap outside-owner fraction must exclude tax losses already in personal tax/removal lines",
                              "item12": "new source-tax coverage increment withheld, not flat-scaled from corporate; sensitivity needs own age/sex/tenure keys"},
                population=v8["population"], w09=w09)
    dump(HERE / "derived/item.json", item)
    table = []
    for name, arm in arms.items():
        for which in ["set", "cash"]:
            for i, end in enumerate(["low", "high"]):
                delta = arm["by_end"][end]["total_bn"]
                table.append(dict(arm=name, accounting_set=which, end=end,
                                  v8_bn=v8["baseline"][which][i], delta_cost_bn=delta,
                                  with_item_bn=v8["baseline"][which][i] + delta,
                                  delta_per_member_usd=delta * 1e9 / v8["population"]["with_coverage"]))
    csv_out("arms.csv", table)
    dump(HERE / "derived/w09.json", w09)
    csv_out("income_key_exposures.csv", [dict(form=row["form"], naics=row["naics"],
        direct_income_net_bn=row["direct_income_net_bn"], lineage_key=key["lineage"][0],
        completion_key=key["completion"],
        income_at_jobs_bn=row["direct_income_net_bn"] * (key["lineage"][0] + key["completion"]),
        allocated_owner_rate_2023=rates(2023)[row["form"]]) for row, key in rows])
    print(json.dumps({"item19_arms": len(arms), "w09": w09}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
