"""Compile the executed complete annual account into one declarative model for the explorer.

Reads producer outputs only; no incidence is recomputed here. Inputs are the receipt and
spending allocations by category, the per-category alternative keys, the 3,888 production
scenarios, the executed category service-response cases and the accounting cases of
`full_account_*_2026_09_20`. Writes `derived/model.json` plus `derived/test_vectors.json`:
rows SELECTED from the executed exports, used to gate `engine.js` (the page's evaluator)
against the account it displays. Fails closed on stale upstream hashes or an incomplete grid.

Two lanes executed after the account add allocation rules (decision 2026-09-23): public order and
safety by use (`cj_use_allocation_2026_09_23`) and Medicaid with the under-charged part of
uncompensated hospital care keyed to uninsured use (`uncompensated_care_2026_09_23`). Each added
rule moves the target's amount on its line by the lane's executed change and keeps the national
total; existing rules and the preferred and alternative choices are untouched.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
ACCOUNT = FISCAL/"full_account_2026_09_20"
sys.path.insert(0, str(ACCOUNT))
from builder import sha  # noqa: E402  (the account's own fingerprint helper)

RECEIPTS = FISCAL/"full_account_receipts_2026_09_20/derived/category_allocations.csv"
SPENDING = FISCAL/"full_account_spending_2026_09_20/derived/allocations.csv"
ALTERNATIVES = FISCAL/"full_account_spending_2026_09_20/derived/category_proxy_alternatives.csv"
BENEFITS = FISCAL/"full_account_benefits_2026_09_20/derived/benefit_scenarios.csv"
GRID = ACCOUNT/"derived/welfare_scenarios.csv"
SERVICE_CASES = ACCOUNT/"derived/service_response_cases.csv"
SERVICE_COMPONENTS = ACCOUNT/"derived/service_response_components.csv"
ACCOUNTS = ACCOUNT/"derived/accounts.csv"
HEADLINE = ACCOUNT/"derived/headline_summary.json"
JUSTICE = FISCAL/"cj_use_allocation_2026_09_23/derived/summary.json"
UNCOMPENSATED = FISCAL/"uncompensated_care_2026_09_23/derived/summary.json"

# welfare.py:response_pools — receipts that are not independently remitted by households.
CAPITAL_CATEGORIES = {"corporate_capital", "corporate_labor", "modeled_owner_property",
                      "remaining_production_property", "personal_property_tax"}
DIRECT_CLASSES = {"personal_income", "household_direct"}
PRODUCTION_DIMS = ["proxy", "split", "normalization", "labor_share", "sigma", "capital_adjustment",
                   "labor_supply_elasticity", "capital_tax_retention", "excluded_capital_owner_share"]
# report.py:baseline — the reference production case behind every headline figure.
REFERENCE = dict(proxy="PEARNVAL", split="hs_or_less", normalization="gdp", labor_share=0.65, sigma=2.0,
                 capital_adjustment=1.0, labor_supply_elasticity=0.0, capital_tax_retention=1.0,
                 excluded_capital_owner_share=0.0)
SPENDING_SCENARIOS = {"preferred": "complete_preferred_F_per_capita",
                      "alternative": "complete_alternative_keys_F_per_capita"}
ROUND = 9


def verify_upstream():
    """Same guard as report.py, extended to the service-response receipt."""
    out = ACCOUNT/"derived"
    for audit_name in ["audit.json", "welfare_audit.json", "service_response_audit.json"]:
        audit = json.loads((out/audit_name).read_text())
        for source, expected in audit["source_hashes"].items():
            if sha(source) != expected:
                raise ValueError(f"[BLOCKED] missing or stale source: {source}")
        for name, expected in audit["outputs"].items():
            if sha(out/f"{name}.csv") != expected:
                raise ValueError(f"[BLOCKED] stale producer output: {name}")


def receipt_lines(receipts):
    complete = []
    for scenario, frame in receipts.groupby("scenario_id"):
        # welfare.py keeps arms with no unallocated residual and no external-owner variant.
        if scenario == "evidence_only" or "external" in scenario or frame.unallocated_bn.abs().sum() > 1e-8:
            continue
        complete.append(scenario)
    lines = []
    for category, frame in receipts.loc[receipts.scenario_id.isin(complete)].groupby("category", sort=False):
        cells = {}
        for row in frame.itertuples():
            direct = row.response_class in DIRECT_CLASSES and category not in CAPITAL_CATEGORIES
            cells.setdefault(row.scenario_id, {})[row.allocation] = dict(
                target_bn=round(row.target_bn, ROUND), other_bn=round(row.other_bn, ROUND),
                key=row.allocation_key, share=round(row.target_key_share, ROUND),
                response_class=row.response_class, direct=bool(direct))
        lines.append(dict(id=category, national_bn=round(float(frame.national_bn.iloc[0]), ROUND), cells=cells))
    return sorted(complete), lines


def spending_lines(spending, alternatives):
    lines = []
    preferred = spending.loc[spending.scenario_id.eq(SPENDING_SCENARIOS["preferred"])]
    alternate = spending.loc[spending.scenario_id.eq(SPENDING_SCENARIOS["alternative"])]
    for category, frame in preferred.groupby("category", sort=False):
        keys = {}
        for row in alternatives.loc[alternatives.category.eq(category)].itertuples():
            keys.setdefault(row.allocation_key, {})[row.allocation] = dict(
                target_bn=round(row.target_bn, ROUND),
                other_bn=round(row.other_household_bn+row.outside_household_bn, ROUND),
                share=round(row.target_key_share, ROUND))
        chosen = {}
        for label, source in [("preferred", frame), ("alternative", alternate.loc[alternate.category.eq(category)])]:
            if source.allocation_key.nunique() != 1:
                raise ValueError(f"Key differs by allocation convention: {category}")
            key = source.allocation_key.iloc[0]
            chosen[label] = key
            for row in source.itertuples():
                cell = dict(target_bn=round(row.target_bn, ROUND), other_bn=round(row.other_bn, ROUND),
                            share=round(row.target_key_share, ROUND))
                known = keys.setdefault(key, {}).setdefault(row.allocation, cell)
                if abs(known["target_bn"]-cell["target_bn"]) > 1e-6:
                    raise ValueError(f"Alternative table disagrees with the scenario export: {category}/{key}")
        lines.append(dict(id=category, family=frame.family.iloc[0], response_class=frame.response_class.iloc[0],
                          national_bn=round(float(frame.national_bn.iloc[0]), ROUND),
                          preferred_key=chosen["preferred"], alternative_key=chosen["alternative"], keys=keys))
    return lines


def use_keys(lines):
    """Add the rules the two use lanes executed. Each is the preferred rule with the target's amount
    moved by the lane's change in both allocations (other residents carry the rest), as
    main_case_2026_09_23/main_case.js shifts it. Every number is read from the lanes' summary.json."""
    justice, care = json.loads(JUSTICE.read_text()), json.loads(UNCOMPENSATED.read_text())
    by_id = {line["id"]: line for line in lines}
    # Positive controls: the justice lane's per-head reference is this account's preferred allocation,
    # and its central target is that reference plus its change.
    for cell in by_id["public_order_safety"]["keys"]["population"].values():
        if abs(cell["target_bn"]-justice["reference_bn"]) > 1e-6:
            raise ValueError("Justice lane reference differs from the account's per-head allocation")
    if abs(justice["reference_bn"]+justice["central"]["change_bn"]-justice["central"]["target_bn"]) > 1e-6:
        raise ValueError("Justice lane central target is not its reference plus its change")
    summary = "derived/summary.json"
    # (line, rule the lane measured its change against, added rule, change in bn, where it is read)
    added = [
        ("public_order_safety", "population", "use", justice["central"]["change_bn"],
         f"cj_use_allocation_2026_09_23/{summary}: central.change_bn"),
        ("public_order_safety", "population", "use_raw_coding", justice["one_at_a_time_change_bn"]["scaling_raw"],
         f"cj_use_allocation_2026_09_23/{summary}: one_at_a_time_change_bn.scaling_raw"),
    ]
    for arm, suffix in [("1.0", ""), ("0.7", "_07")]:
        for i, end in enumerate(("low", "high")):
            added.append(("medicaid_and_chip_other_medical", "medicaid", f"uninsured_use{suffix}_{end}",
                          care[f"inside_undercharged_bn_use_{arm}"][i],
                          f"uncompensated_care_2026_09_23/{summary}: inside_undercharged_bn_use_{arm}[{i}]"))
    record = []
    for line_id, base, key, change, source in added:
        line = by_id[line_id]
        if base != line["preferred_key"] or key in line["keys"]:
            raise ValueError(f"Upstream rules moved under {line_id}: preferred {line['preferred_key']}, keys {sorted(line['keys'])}")
        cells = {}
        for allocation, cell in line["keys"][base].items():
            target, other = cell["target_bn"]+change, cell["other_bn"]-change
            if abs(target+other-line["national_bn"]) > 1e-6:
                raise ValueError(f"{line_id}/{key}/{allocation} does not keep the national total")
            # The share keeps the base rule's denominator (its key's universe, not the national total,
            # which the lanes' own target_share uses), so the ledger compares rules on one footing.
            cells[allocation] = dict(target_bn=round(target, ROUND), other_bn=round(other, ROUND),
                                     share=round(cell["share"]*target/cell["target_bn"], ROUND))
        line["keys"][key] = cells
        record.append(dict(line=line_id, key=key, base_key=base, change_bn=round(change, ROUND), source=source))
    for cell in by_id["public_order_safety"]["keys"]["use"].values():
        if abs(cell["target_bn"]-justice["central"]["target_bn"]) > 1e-6:
            raise ValueError("The use rule does not reproduce the justice lane's central target")
    return record


def production_table(benefits):
    levels = {d: sorted(benefits[d].unique().tolist()) for d in PRODUCTION_DIMS}
    size = int(np.prod([len(v) for v in levels.values()]))
    if len(benefits) != size or benefits.duplicated(PRODUCTION_DIMS).any():
        raise ValueError("Production scenarios are not a complete grid over the declared dimensions")
    paired = benefits.groupby("split").tax_classification_transport.nunique()
    if not paired.eq(1).all():
        raise ValueError("split and tax_classification_transport are no longer one dimension")
    index = np.zeros(len(benefits), dtype=int)
    for d in PRODUCTION_DIMS:
        index = index*len(levels[d])+benefits[d].map({v: i for i, v in enumerate(levels[d])}).to_numpy()
    order = np.argsort(index)
    if not np.array_equal(index[order], np.arange(size)):
        raise ValueError("Mixed-radix index does not cover the grid")
    b = benefits.iloc[order]
    return dict(dims=levels, reference=REFERENCE,
                split_transport=benefits.groupby("split").tax_classification_transport.first().to_dict(),
                private_wtp_bn=b.private_after_tax_wtp_bn.round(ROUND).tolist(),
                induced_receipts_bn=b.induced_current_receipts_bn.round(ROUND).tolist(),
                sampling_se_bn=[None if pd.isna(x) else round(x, ROUND) for x in b.private_plus_receipts_se_sampling_bn])


def grid_vectors():
    """Executed welfare rows: a deterministic hash sample plus both extremes."""
    con = duckdb.connect()
    con.execute(f"create view w as select * from read_csv_auto('{GRID}', sample_size=-1)")
    columns = PRODUCTION_DIMS+["receipt_scenario", "spending_scenario", "allocation", "public_goods_response",
                               "service_response", "fiscal_weight", "direct_fiscal_response_bn", "welfare_bn"]
    picked = con.execute(f"""
        select {', '.join(columns)} from w
        where hash(scenario_id, receipt_scenario, spending_scenario, allocation,
                   public_goods_response, fiscal_weight) % 199 = 0
           or welfare_bn = (select min(welfare_bn) from w) or welfare_bn = (select max(welfare_bn) from w)
        order by all""").df()
    rows, covered = con.execute("select count(*) from w").fetchone()[0], {}
    for d in columns[:-2]:
        covered[d] = sorted(picked[d].unique().tolist()) == sorted(
            r[0] for r in con.execute(f"select distinct {d} from w").fetchall())
    if not all(covered.values()):
        raise ValueError(f"Sample misses a level: {covered}")
    return rows, picked.to_dict("records")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=HERE/"derived")
    args = parser.parse_args()
    verify_upstream()
    receipts, spending = pd.read_csv(RECEIPTS), pd.read_csv(SPENDING)
    alternatives, benefits = pd.read_csv(ALTERNATIVES), pd.read_csv(BENEFITS)
    receipt_scenarios, r_lines = receipt_lines(receipts)
    accounts = pd.read_csv(ACCOUNTS)
    population = accounts[["target_population", "resident_population"]].drop_duplicates()
    if len(population) != 1:
        raise ValueError("Accounting cases disagree on the populations")
    cases = pd.read_csv(SERVICE_CASES)
    components = pd.read_csv(SERVICE_COMPONENTS)
    profiles = []
    for case in cases.itertuples():
        part = components.loc[components.case_id.eq(case.case_id) & components.allocation.eq(case.allocation)
                              & components.profile.eq(case.profile)]
        profiles.append(dict(
            case_id=case.case_id, allocation=case.allocation, normalization=case.normalization, profile=case.profile,
            education_split=case.education_split, school_share=case.school_share, school_response=case.school_response,
            other_education_response=case.other_education_response, delayed_response=case.delayed_response,
            effective_service_response=case.effective_service_response, welfare_bn=case.welfare_bn))
        if part.empty:
            raise ValueError(f"Service case without components: {case.case_id}")
    grid_rows, vectors = grid_vectors()
    s_lines = spending_lines(spending, alternatives)
    added_keys = use_keys(s_lines)
    model = dict(
        meta=dict(
            title="Complete annual account, income year 2024", units="billions of 2024 dollars per year",
            target="Observed CPS Mexican-origin residents, all generations, ages and schooling",
            target_population=float(population.target_population.iloc[0]),
            resident_population=float(population.resident_population.iloc[0]),
            grid_rows=grid_rows, headline=json.loads(HEADLINE.read_text()),
            inputs={str(p.relative_to(FISCAL.parents[1])): sha(p) for p in
                    [RECEIPTS, SPENDING, ALTERNATIVES, BENEFITS, GRID, SERVICE_CASES, ACCOUNTS, JUSTICE, UNCOMPENSATED]}),
        receipts=dict(scenarios=receipt_scenarios, reference="cbo_collective", lines=r_lines),
        spending=dict(scenarios=SPENDING_SCENARIOS, lines=s_lines, added_keys=added_keys),
        production=production_table(benefits),
        # service_response.py: the two categories CBO's evidence treats as slow to respond.
        service=dict(delayed=["economic_affairs_services", "recreation_culture"], profiles=profiles),
    )
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out/"model.json").write_text(json.dumps(model, sort_keys=True, separators=(",", ":"))+"\n")
    complete = accounts.loc[accounts.complete & accounts.spending_scenario.isin(SPENDING_SCENARIOS.values())
                            & accounts.receipt_scenario.isin(receipt_scenarios)]
    vectors = dict(grid=vectors, service=profiles, accounts=complete[[
        "receipt_scenario", "spending_scenario", "allocation", "target_balance_bn", "normalized_gap_bn"]].to_dict("records"))
    (args.out/"test_vectors.json").write_text(json.dumps(vectors, sort_keys=True, separators=(",", ":"))+"\n")
    print(f"model.json: {len(r_lines)} receipt lines, {len(model['spending']['lines'])} spending lines, "
          f"{len(model['production']['private_wtp_bn'])} production scenarios, {len(profiles)} service cases, "
          f"{len(added_keys)} rules added from the use lanes")
    print(f"test_vectors.json: {len(vectors['grid'])} of {grid_rows} grid rows, {len(profiles)} service cases, "
          f"{len(vectors['accounts'])} accounting cases")


if __name__ == "__main__":
    main()
