"""Reconcile a partial resident account to explicit 2024 national boundaries.

Unallocated differences remain unallocated. This is not a policy-effect model.
"""
from __future__ import annotations

import sys as _path_sys
from pathlib import Path as _Path
_path_sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "build"))
import paths as _data_paths


import argparse
import importlib.util
import json
from pathlib import Path

import numpy as np
import openpyxl
import pandas as pd

from finance_vintage import read_finance, vintage_effects

HERE = Path(__file__).resolve().parent
BEA_URL = "https://apps.bea.gov/national/Release/XLS/Survey/Section3All_xls.xlsx"
BEA_SHA = "69b5c7aefb38675324887ce31d6feb4fcde7c903ab952db7328da0813096615e"
BEA_DEFAULT = _data_paths.data_root(require_exists=False) / 'external/bea_nipa/Section3All_xls.xlsx'
UNION = "mexican_observed_total"
RECEIPTS = {"tax", "employer", "sales", "owner_property", "C", "X"}


def parse_sheet(rows, year):
    """Only the declared year header can select a column, never a data value."""
    headers = [r for r in rows if r and r[0] == "Line"]
    if len(headers) != 1:
        raise ValueError("Expected one BEA Line/year header")
    matches = [i for i, value in enumerate(headers[0]) if str(value) == str(year)]
    if len(matches) != 1:
        raise ValueError(f"BEA table has no unique year {year}")
    if rows[1][0] not in {"[Millions of dollars]", "[Millions of dollars; quarterly totals not seasonally adjusted]"}:
        raise ValueError("Unexpected BEA source units")
    column = matches[0]
    result = {}
    for row in rows:
        if not str(row[0]).isdigit():
            continue
        line, value = int(row[0]), row[column]
        if line in result or not isinstance(value, (int, float)) or not np.isfinite(value):
            raise ValueError(f"Missing/duplicate/nonfinite BEA cell {year}/{line}: {value}")
        result[line] = dict(line=line, label=row[1].strip(), series=row[2], amount_bn=value / 1000)
    return result


def close(actual, expected, label, tolerance=.003):
    if not np.isfinite([actual, expected]).all() or abs(actual - expected) > tolerance:
        raise ValueError(f"{label}: {actual} != {expected}")
    return dict(check=label, actual=actual, expected=expected, residual=actual - expected)


def budget_response(gross_receipts, gross_spending, response):
    """All receipts, including fees, are lost independently of avoided spending."""
    return response * gross_spending - gross_receipts


def official_tables(path, sha):
    if sha(path) != BEA_SHA:
        raise ValueError("BEA vintage changed; review source before changing the pinned hash")
    book = openpyxl.load_workbook(path, read_only=True, data_only=True)
    tables = {name: parse_sheet(list(book[name].values), 2024)
              for name in ["T30100-A", "T30200-A", "T30300-A", "T31800B-A"]}
    book.close()
    v = lambda t, n: tables[t][n]["amount_bn"]
    a, f, s, b = "T30100-A", "T30200-A", "T30300-A", "T31800B-A"
    checks = [
        close(v(a, 1), 8008.290, "Published 2024 current receipts anchor", 1e-9),
        close(v(a, 20), 10061.458, "Published 2024 current expenditures anchor", 1e-9),
        close(v(a, 1), sum(v(a, n) for n in [2, 7, 10, 15, 19]), "Receipts components"),
        close(v(a, 20), sum(v(a, n) for n in [21, 22, 27, 30]), "Expenditure components"),
        close(v(a, 1), v(f, 1) + v(s, 1) - v(f, 31), "Current receipts net grants once"),
        close(v(a, 20), v(f, 24) + v(s, 23) - v(f, 31), "Current expenditure net grants once"),
        close(v(f, 31), v(s, 18), "Same-year intergovernmental grants", 1e-9),
        close(v(a, 31), v(a, 1) - v(a, 20), "Current saving identity"),
        close(v(a, 34), v(a, 1) + v(a, 36), "Capital receipt bridge"),
        close(v(a, 37), sum(v(a, n) for n in [20, 39, 40, 41]) - v(a, 42), "Capital spending bridge"),
        close(v(a, 43), v(a, 34) - v(a, 37), "Net borrowing identity"),
        close(v(b, 18), v(b, 1) - v(b, 2) - v(b, 7) + v(b, 12), "Federal FY receipt bridge"),
        close(v(b, 47), v(b, 19) - v(b, 20) - v(b, 37) + v(b, 42), "Federal FY spending bridge"),
    ]
    return tables, checks


def reconstruct(root, evidence, census_cache):
    """Reuse canonical person-level components; export disjoint national groups."""
    A, AL, arrival = evidence.configure(root)
    fiscal = root / "infra/immigration-fiscal"
    params_path = fiscal / "ledger_absolute_2026_09_17/params/params.json"
    params = AL.Params(params_path, False)
    state = A.ext.build(argparse.Namespace(cps_zip=fiscal / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip"))
    d, weights = state["d"], state["person_weights"]
    weight = weights[:, 0]
    civilian = (d.PRPERTYP.eq(2) | d.A_AGE.lt(15)).to_numpy()
    parts = [state["group"][g] & civilian for g in AL.TARGETS]
    if np.any(np.sum(parts, axis=0) > 1):
        raise ValueError("Overlapping target generations")
    target = np.logical_or.reduce(parts)
    groups = {UNION: target, "other_residents": civilian & ~target, "national_civilian": civilian}
    shared, personal, _ = A.matrices(state)
    medical_zip = root / "sources/immigration-fiscal/data/external/stage3/ahrq/meps_2024/h256dat.zip"
    medical, _ = A.read_meps(medical_zip, medical_zip.with_name("h256su.txt"))
    cells, codes, _ = A.donor_model(medical, d, False)
    payer_means = arrival._payer_means(medical, cells)
    exposure = ~(d.PUB.eq(0) & d.PRIV.eq(0)).to_numpy()
    health = np.eye(len(cells))[codes] * exposure[:, None]
    means = cells.mean_public_paid.to_numpy()
    state_population = arrival.resid.read_state_population()
    old = fiscal / "ledger_absolute_2026_09_17/derived"
    profiles = pd.read_csv(old / "age_profiles.csv")
    details = pd.read_csv(old / "age_profile_components.csv")
    national = pd.read_csv(old / "national_reconciliation.csv")
    n_national = float(national.loc[national.line.eq("item N institutional care"), "amount_bn"].iloc[0])
    rows, anchors, f_rows, vintage_rows, census_checks = [], [], [], [], []
    for allocation, matrix in [("shared", shared), ("personal", personal)]:
        ctx = dict(d=d, index=state["index"], n_units=state["n_units"], civilian=civilian,
                   weights=weights, heads=d.loc[d.SPM_HEAD.eq(1)].sort_values("SPM_ID"),
                   general_services=arrival.resid.read_general_services_per_capita(state_population),
                   assf=AL.read_assf_k12(arrival.GENEXT / "census_assf_fy2024_summary_tables.xlsx"),
                   omb=AL.read_omb_functions(arrival.RESIDUAL / "_cache/omb_hist03z1_fy2027.xlsx"),
                   capital=AL.read_cog_capital(arrival.RESIDUAL / "_cache/22slsstab1.xlsx", state_population),
                   donor_codes=codes, donor_payer_means=payer_means, exposure=exposure,
                   n_civilian=float(weight[civilian].sum()), us_resident=params.pick("population", ["2024"], "count"),
                   consumption_proxy=matrix[:, 4], off=[], allocation=allocation,
                   is_white_ref=state["group"][AL.WHITE] & civilian, is_target=target)
        charges, _, centrals, _, _ = AL.build_charges(ctx, AL.Params(params_path, False))
        values = {name: matrix[:, i] * A.COEFFICIENTS[i] for i, name in enumerate(A.COMPONENTS)}
        values["medical"] = -(health @ means)
        values.update({item: charges.data[charges.columns.index(f"{item}|{arm}")]
                       for item, arm in centrals.items() if arm is not None})
        changed, controls, _ = vintage_effects(d, weight, groups, values, ctx, charges,
                                               AL.Params(params_path, False), root, census_cache, allocation)
        vintage_rows.extend(changed)
        if not census_checks:
            census_checks = controls
        gm = charges.meta[f"G|{centrals['G']}"]
        fees = d.GESTFIPS.map(gm["fees_by_state_per_capita"]).to_numpy(dtype=float) * gm["deflator"]
        if not np.isfinite(fees).all():
            raise ValueError("Missing state fee value")
        n_target = float(details.loc[details.allocation.eq(allocation) & details.account.eq("expanded")
                                    & details.group.eq(UNION) & details.component.eq("N"), "signed_total"].sum()) / 1e9
        n_values = {UNION: n_target, "other_residents": n_national - n_target, "national_civilian": n_national}
        for group, mask in groups.items():
            population = float(weight[mask].sum())
            for component, vector in values.items():
                total = float(vector[mask] @ weight[mask]) / 1e9
                rows.append(dict(allocation=allocation, group=group, component=component, population=population,
                                 signed_bn=total, receipts_bn=total if component in RECEIPTS else 0,
                                 spending_bn=0 if component in RECEIPTS else -total))
            rows.append(dict(allocation=allocation, group=group, component="N", population=population,
                             signed_bn=n_values[group], receipts_bn=0, spending_bn=-n_values[group]))
            fee = float(fees[mask] @ weight[mask]) / 1e9
            rows.append(dict(allocation=allocation, group=group, component="G_fee_grossup", population=population,
                             signed_bn=0, receipts_bn=fee, spending_bn=fee))
            f_vector = charges.data[charges.columns.index("F|per_capita")]
            f_rows.append(dict(allocation=allocation, group=group, per_capita_F_charge_bn=float(f_vector[mask] @ weight[mask]) / 1e9,
                               administrative_F_bn=charges.meta["F|per_capita"]["national_dollars"] / 1e9,
                               resident_denominator=ctx["us_resident"]))
        total = sum(r["signed_bn"] for r in rows if r["allocation"] == allocation and r["group"] == UNION)
        expected = profiles.loc[profiles.allocation.eq(allocation) & profiles.account.eq("expanded")
                                & profiles.group.eq(UNION), "net_total"].sum() / 1e9
        anchors.append(close(total, expected, f"{allocation} canonical union", 1e-7))
    table = pd.DataFrame(rows)
    for (allocation, component), frame in table.groupby(["allocation", "component"]):
        frame = frame.set_index("group")
        for col in ["signed_bn", "receipts_bn", "spending_bn"]:
            anchors.append(close(frame.loc["national_civilian", col], frame.loc[UNION, col] + frame.loc["other_residents", col],
                                 f"Disjoint {allocation}/{component}/{col}", 1e-7))
    old_audit = json.loads((old / "audit.json").read_text())["national_reconciliation_vs_consolidated_budget"]
    shared_national = table[table.allocation.eq("shared") & table.group.eq("national_civilian")]
    for col, key in [("receipts_bn", "account_receipts"), ("spending_bn", "account_outlays")]:
        anchors.append(close(shared_national[col].sum(), old_audit[key] / 1e9, f"Canonical national {col}", 1e-7))
    return table, pd.DataFrame(f_rows), anchors, pd.DataFrame(vintage_rows), census_checks


def bridges(tables, accounts, f_charges):
    v = lambda n: tables["T30100-A"][n]["amount_bn"]
    summaries = accounts.groupby(["allocation", "group"], as_index=False).agg(
        population=("population", "first"), receipts_bn=("receipts_bn", "sum"),
        spending_bn=("spending_bn", "sum"), balance_bn=("signed_bn", "sum"))
    rows, coverage, conditional = [], [], []
    official_categories = {
        "personal_tax_and_social_contributions": (v(3) + v(8), {"tax", "employer"}),
        "corporate_income_taxes": (v(5), {"C"}),
        "production_and_import_taxes": (v(4), {"sales", "owner_property", "X"}),
        "other_current_receipts": (v(6) + v(9) + v(10) + v(15) + v(19), set()),
    }
    for allocation in ["shared", "personal"]:
        a = summaries[summaries.allocation.eq(allocation)].set_index("group")
        n = a.loc["national_civilian"]
        raw = accounts[accounts.allocation.eq(allocation) & accounts.group.eq("national_civilian")]
        fee = raw.loc[raw.component.eq("G_fee_grossup"), "receipts_bn"].sum()
        for boundary, receipts, spending in [("current", v(1), v(20)), ("total_net_borrowing", v(34), v(37))]:
            rows.append(dict(allocation=allocation, boundary=boundary, modeled_receipts_bn=n.receipts_bn - fee,
                             modeled_spending_bn=n.spending_bn - fee, modeled_balance_bn=n.balance_bn,
                             official_receipts_bn=receipts, official_spending_bn=spending,
                             official_balance_bn=receipts - spending,
                             unallocated_receipt_difference_bn=receipts - (n.receipts_bn - fee),
                             unallocated_spending_difference_bn=spending - (n.spending_bn - fee),
                             unallocated_balance_difference_bn=receipts - spending - n.balance_bn,
                             scope="Model still mixes capital/current and FY/CY; differences are not missing causal costs"))
        for category, (official, components) in official_categories.items():
            modeled = raw.loc[raw.component.isin(components), "receipts_bn"].sum()
            coverage.append(dict(allocation=allocation, category=category, official_bn=official,
                                 modeled_bn=modeled, difference_bn=official - modeled,
                                 classification="Broad diagnostic only: credits, premiums, pension accrual, universe and vintage differ"))
        target = a.loc[UNION]
        target_f = -float(f_charges.loc[f_charges.allocation.eq(allocation) & f_charges.group.eq(UNION), "per_capita_F_charge_bn"].iloc[0])
        # Unlike the static BEA presentation, this grid explicitly loses ALL
        # receipts including fees, independently of the expenditure response.
        r, c = target.receipts_bn, target.spending_bn
        for f_fraction in [0, .5, 1]:
            cost = c + f_fraction * target_f
            for response in [0, .25, .5, .75, 1]:
                conditional.append(dict(allocation=allocation, F_allocated_fraction=f_fraction,
                                        assigned_gross_spending_bn=cost, attributed_receipts_bn=r,
                                        spending_response_fraction=response,
                                        conditional_budget_improvement_bn=budget_response(r, cost, response),
                                        break_even_spending_response=r / cost,
                                        scope="Arithmetic only: all assigned receipts lost; fraction of assigned spending avoided; no policy identified"))
    return summaries, pd.DataFrame(rows), pd.DataFrame(coverage), pd.DataFrame(conditional)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=HERE.parents[2])
    parser.add_argument("--bea", type=Path, default=BEA_DEFAULT)
    parser.add_argument("--census-cache", type=Path, default=HERE / "_cache")
    parser.add_argument("--out", type=Path, default=HERE / "derived")
    args = parser.parse_args()
    root = args.source_root.resolve()
    helper = root / "infra/immigration-fiscal/education_origin_fiscal_2026_09_19/builder.py"
    spec = importlib.util.spec_from_file_location("macro_evidence", helper)
    evidence = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(evidence)
    fingerprints = evidence.verified_upstream_inputs(root)
    tables, checks = official_tables(args.bea, evidence.sha)
    print("[verified] official current/capital and federal/state identities", flush=True)
    accounts, f_charges, anchors, vintage, census_checks = reconstruct(root, evidence, args.census_cache)
    checks.extend(anchors)
    summaries, bridge, coverage, conditional = bridges(tables, accounts, f_charges)
    adjusted = summaries.merge(vintage.groupby(["allocation", "group"], as_index=False).balance_change_bn.sum(),
                               on=["allocation", "group"], validate="one_to_one")
    adjusted["updated_balance_bn"] = adjusted.balance_bn + adjusted.balance_change_bn
    updated_accounts = accounts.merge(vintage[["allocation", "group", "component", "balance_change_bn", "receipt_change_bn", "spending_change_bn"]],
                                      on=["allocation", "group", "component"], how="left", validate="one_to_one")
    for original, delta in [("signed_bn", "balance_change_bn"), ("receipts_bn", "receipt_change_bn"), ("spending_bn", "spending_change_bn")]:
        updated_accounts[original] += updated_accounts[delta].fillna(0)
    updated_summaries, updated_bridge, updated_coverage, updated_policy = bridges(tables, updated_accounts, f_charges)
    for row in updated_summaries.itertuples():
        close(row.receipts_bn - row.spending_bn, row.balance_bn, "Updated receipts minus spending", 1e-7)
    adjusted = adjusted.merge(updated_summaries[["allocation", "group", "receipts_bn", "spending_bn"]].rename(
        columns={"receipts_bn": "updated_receipts_bn", "spending_bn": "updated_spending_bn"}), on=["allocation", "group"])
    # A contemporaneous fiscal-year comparator is also retained, separately from
    # NIPA calendar-year saving. State fiscal years and federal FY do not coincide.
    _, _, arrival = evidence.configure(root)
    p = arrival.AL.Params(root / "infra/immigration-fiscal/ledger_absolute_2026_09_17/params/params.json", False)
    f_r = p.pick("omb", ["receipts_total"], "money", preferred="receipts_total") / 1e9
    f_e = p.pick("omb", ["total_outlays"], "money", preferred="total_outlays") / 1e9
    fiscal_bridges = []
    for year in [2022, 2024]:
        _, controls = read_finance(args.census_cache, year)
        get = lambda line: next(r["national_dollars"] for r in controls if r["line"] == f"LF{line:04}") / 1e9
        fiscal_bridges.append(dict(state_local_year=year, federal_year=2024,
                                   state_local_own_revenue_bn=get(7), state_local_direct_general_expenditure_bn=get(103),
                                   federal_grants_received_bn=get(4), federal_receipts_bn=f_r, federal_outlays_bn=f_e,
                                   comparator_receipts_bn=f_r + get(7), comparator_outlays_bn=f_e + get(103) - get(4),
                                   comparator_balance_bn=f_r + get(7) - f_e - get(103) + get(4),
                                   scope="General-finance fiscal-year comparator, not NIPA total or exact cash identity;2022 rows nominal source-control only"))
    args.out.mkdir(parents=True, exist_ok=True)
    output = {"account_components": accounts, "account_totals": summaries, "national_bridge": bridge,
              "receipt_diagnostics": coverage, "policy_arithmetic": conditional, "F_attribution": f_charges,
              "finance_vintage_effects": vintage, "finance_vintage_totals": adjusted,
              "updated_account_components": updated_accounts, "updated_national_bridge": updated_bridge,
              "updated_receipt_diagnostics": updated_coverage, "updated_policy_arithmetic": updated_policy,
              "fiscal_year_comparators": pd.DataFrame(fiscal_bridges),
              "official_cells": pd.DataFrame([dict(table=t, year=2024, **r) for t, lines in tables.items() for r in lines.values()])}
    for name, frame in output.items():
        frame.to_csv(args.out / f"{name}.csv", index=False)
    fingerprints.update({str(p): evidence.sha(p) for p in [Path(__file__), helper, args.bea]})
    for path in [HERE / "finance_vintage.py", HERE / "census_sources.json"]:
        fingerprints[str(path)] = evidence.sha(path)
    census_manifest = json.loads((HERE / "census_sources.json").read_text())
    for entry in census_manifest["files"]:
        path = args.census_cache / entry["file"]
        if evidence.sha(path) != entry["sha256"]:
            raise ValueError(f"Census acquisition manifest drift: {entry['file']}")
        fingerprints[str(path)] = entry["sha256"]
    audit = dict(source_hashes=fingerprints, bea_source=BEA_URL, bea_vintage="August 26, 2026; 2024 calendar year unless table3.18B FY",
                 price_year=2024, checks=checks, census_control_checks=census_checks, target=UNION,
                 status="National boundaries reconciled; group residual deliberately unallocated",
                 limitations=["Institutional N national add covers natives and Mexico-born only",
                              "Model current/capital mixture is not silently called NIPA current spending",
                              "Fees grossed up in canonical totals and netted symmetrically for BEA diagnostic",
                              "No assumption that remaining receipts or spending follow population shares",
                              "Fiscal-year federal source vintage differs between OMB and BEA bridge",
                              "BEA3.19 latest published annual bridge is 2023; no2024 Census-to-NIPA micro bridge",
                              "Policy response grid is conditional arithmetic, not behavioral evidence"],
                 outputs={name: evidence.sha(args.out / f"{name}.csv") for name in output})
    (args.out / "audit.json").write_text(json.dumps(audit, indent=2, allow_nan=False) + "\n")
    print(summaries.to_string(index=False))
    print(bridge.to_string(index=False))
    print(adjusted[["allocation", "group", "balance_change_bn", "updated_balance_bn"]].to_string(index=False))


if __name__ == "__main__":
    main()
