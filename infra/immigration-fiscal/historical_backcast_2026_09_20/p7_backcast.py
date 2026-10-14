"""P7 controlled changes and a v7 programme back-cast, beside the frozen live series.

Native-First: reuse the backcast helpers, live engine and its explicit component split.
Every output is derived from source files; no annual yield or pandemic amount is typed.
"""
from __future__ import annotations

import contextlib
import hashlib
import io
import json
import resource
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import numpy as np
import pandas as pd
from pypdf import PdfReader

import backcast as b
from backcast_categories import Cells

HERE = b.HERE
OUT = HERE / "derived/p7"
WINDOWS = {"10y_2015_2024": 2015, "15y_2010_2024": 2010, "20y_2005_2024": 2005}
RULES = ("flat", "ratio", "income")
INCOME_RECEIPTS = {"federal_income_tax", "state_local_income_tax", "employee_oasdi", "employee_hi",
                   "employer_oasdi", "employer_hi", "self_employment_oasdi_hi", "other_domestic_social_contributions",
                   "corporate_capital", "corporate_labor", "remaining_production_property", "other_production_taxes",
                   "general_sales_tax", "excise_selective_sales", "customs_duties", "personal_current_transfers"}
PARENTS = {"school_reprice": "education_services", "college_rekey": "education_services",
           "roads_vmt_sl": "economic_affairs_services", "roads_vmt_fed": "economic_affairs_services",
           "state_price_public_order_safety": "public_order_safety", "state_price_health_services": "health_services",
           "state_price_recreation_culture": "recreation_culture"}


def require(ok, message):
    if not ok:
        raise ValueError("[BLOCKED] " + message)


def write_csv(table, name):
    table.to_csv(OUT / name, index=False, float_format="%.12g", lineterminator="\n")


def primary_rates():
    pins = json.loads((HERE / "inputs/pins.json").read_text())
    for entry in pins.values():
        require(hashlib.sha256((HERE / entry["path"]).read_bytes()).hexdigest() == entry["sha256"],
                "primary source changed: " + entry["path"])
    daily = pd.read_csv(HERE / "_cache/DFII10.csv")
    daily["year"] = pd.to_datetime(daily.iloc[:, 0]).dt.year
    daily["DFII10"] = pd.to_numeric(daily.DFII10, errors="coerce")
    require(daily.year.between(2005, 2024).all(), "FRED dates outside requested years")
    means = daily.groupby("year").DFII10.agg(["mean", "count"]).reindex(b.YEARS)
    require(means["mean"].notna().all() and means["count"].between(245, 265).all(), "incomplete FRED years")
    means["rate_unfloored"] = means["mean"] / 100
    means["rate_floored"] = means.rate_unfloored.clip(lower=0)
    write_csv(means.reset_index(), "real_yields.csv")
    return means


def pandemic_amounts():
    text = PdfReader(HERE / "_cache/bea_pandemic_2022q4_3rd.pdf").pages[-1].extract_text()
    rows = [row for row in text.splitlines() if row.strip().startswith("31 ") and "Economic impact payments" in row]
    require(len(rows) == 1, "cannot identify annual primary BEA EIP row")
    values = rows[0].split("Economic impact payments", 1)[1].split()
    # Footnote 6, then 2017-2022 level cells: three ellipses and three observations.
    require(values[0] == "6" and values[1:4] == ["...", "...", "..."], "BEA annual EIP schema changed")
    eip = {year: float(value.replace(",", "")) for year, value in zip((2020, 2021, 2022), values[4:7])}
    require(eip[2022] == 0 and min(eip[y] for y in (2020, 2021)) > 0, "BEA EIP annual levels invalid")
    return eip


def positive_control():
    argv = sys.argv
    with tempfile.TemporaryDirectory(prefix="backcast-p7-") as tmp:
        sys.argv = ["backcast.py", "--case", "oct14", "--out-dir", tmp]
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                annual, carried = b.main()
        finally:
            sys.argv = argv
        names = ("backcast_annual.csv", "backcast_windows.csv", "case_parts_annual.csv", "case_parts_windows.csv")
        require(all((Path(tmp) / n).read_bytes() == (HERE / "derived/oct14" / n).read_bytes() for n in names),
                "positive control does not reproduce all four live files")
    return annual, carried


def historical_paths(annual):
    bea = b.ROOT / "sources/immigration-fiscal/data/external/bea_nipa"
    book = b.workbook(bea / "Section3All_xls.xlsx")
    price = b.series(b.workbook(bea / "Section1All_xls.xlsx"), "T10109-A", "Gross domestic product")
    people = b.series(b.workbook(HERE / "_cache/Section7All_xls.xlsx"), "T70100-A", "Population (midperiod, thousands)")
    real = price[2024] / price.reindex(b.YEARS)
    share = annual.group_millions / people.reindex(b.YEARS)
    share /= share[2024]
    g3 = annual.g3plus_millions_cps / people.reindex(b.YEARS)
    g3 /= g3[2024]
    return book, real, share, g3


def controlled_changes(annual, carried, rates, book, real, share, g3):
    data = b.case_parts("oct14")["concepts"]["net_cost_cbo_informed"]
    metadata = {k: v for prefix in ("v4", "v5", "v6") for k, v in data[prefix + "_parts"].items()}
    linked = {k for k, p in metadata.items() if p["rule"] == "accrual"
              or (p["side"] == "receipt" and p["line"] in INCOME_RECEIPTS)
              or (p["side"] == "production" and p["line"] == "induced_receipts_bn")}
    write_csv(pd.DataFrame([dict(part=k, line=p["line"], side=p["side"], source_rule=p["rule"],
                                 income_scaled=k in linked) for k, p in metadata.items()]), "income_classification.csv")
    total = b.series(book, "T30100-A", "Current expenditures").reindex(b.YEARS) / 1e3
    cells = Cells(book)
    excluded = {"defense": cells.get("T31700-A:3"), "interest": cells.get("T30100-A:27"),
                "subsidies": cells.get("T30100-A:30")}
    charged = total - sum(excluded.values())
    require((charged > 0).all(), "charged base not positive")
    require((charged + sum(excluded.values()) - total).abs().max() < 1e-9, "national charged-base closure")
    write_csv(pd.DataFrame(dict(year=b.YEARS, total_bn=total, charged_bn=charged, **excluded)), "charged_base.csv")
    s_change = (charged * real / charged[2024] - total * real / total[2024]) * share
    base_receipts = json.loads((b.FISCAL / "main_case_schools_full_2026_09_26/derived/summary.json").read_text()) \
        ["group_receipts_bn"]["adopted"]["shared"]
    income = annual.relative_per_capita_income / annual.relative_per_capita_income[2024]
    scenarios, rows = {}, []
    for end in ("low", "high"):
        name = f"net_cost_cbo_informed_oct14_{end}"
        split = carried[name]
        for rule in RULES:
            parts = split["by_rule"][rule]
            own = ({k: g3 * v for k, v in split["lineage_2024"].items()} if rule == "flat"
                   else split["lineage_parts"])
            if rule == "flat":
                flat_g3 = annual.g3plus_millions_cps / annual.g3plus_millions_cps[2024]
                own = {k: flat_g3 * v for k, v in split["lineage_2024"].items()}
            for population in ("union", "lineage"):
                subset = {k: v - own.get(k, 0.0) if population == "union" else v for k, v in parts.items()}
                # The published four-decimal band is the old control's anchor. P7 uses the
                # component export's full-precision principal, without changing the old files.
                rounding = data["ends"][end]["cost_bn"] - sum(parts.values())[2024]
                precision_path = annual.group_millions / annual.group_millions[2024] if rule == "flat" \
                    else total * real / total[2024] * share
                subset["base"] += rounding * precision_path
                baseline = sum(subset.values())
                capital = sum(v for k, v in subset.items() if k.startswith("capital_"))
                rate_f = capital * (rates.rate_floored / 0.02 - 1) if end == "low" else capital * 0
                rate_u = capital * (rates.rate_unfloored / 0.02 - 1) if end == "low" else capital * 0
                sigma = (split["base"] + base_receipts) * s_change if rule != "flat" else capital * 0
                earnings = sum(v for k, v in subset.items() if k in linked) * (income - 1) \
                    if rule == "income" else capital * 0
                corrections = {"fixed_2pct": capital * 0, "yield_floor0": rate_f, "yield_unfloored": rate_u,
                               "charged_base": sigma, "income_linked": earnings,
                               "stack": rate_f + sigma + earnings}
                for scenario, delta in corrections.items():
                    values = baseline + delta
                    require(np.isfinite(values).all(), "nonfinite controlled result")
                    scenarios[(end, rule, population, scenario)] = values
                    rows += [dict(end=end, rule=rule, population=population, scenario=scenario, year=y,
                                  baseline_bn=baseline[y], delta_bn=delta[y], cost_bn=values[y]) for y in b.YEARS]
    write_csv(pd.DataFrame(rows), "changes_annual.csv")
    return scenarios, linked


def export_programme():
    proc = subprocess.run(["node", str(HERE / "programme_inputs.cjs")], capture_output=True, text=True)
    require(proc.returncode == 0, "programme engine export: " + proc.stdout + proc.stderr)
    return json.loads((OUT / "programme_inputs.json").read_text())


def programme(annual, carried, book, real, share, g3):
    engine = export_programme()
    cells = Cells(book)
    cats = pd.read_csv(b.FISCAL / "full_account_spending_2026_09_20/derived/categories.csv").set_index("category")
    data = b.case_parts("oct14")
    concept = data["concepts"]["net_cost_cbo_informed"]
    metadata = {k: v for prefix in ("v4", "v5", "v6") for k, v in concept[prefix + "_parts"].items()}
    national = lambda ref: cells.get(ref)
    index = lambda ref: national(ref) * real / national(ref)[2024]
    gdp_book = b.workbook(b.ROOT / "sources/immigration-fiscal/data/external/bea_nipa/Section1All_xls.xlsx")
    gdp = b.line(gdp_book, b.V4_GDP[0]).reindex(b.YEARS)
    production_path = gdp * real / gdp[2024]
    income = annual.relative_per_capita_income / annual.relative_per_capita_income[2024]
    measured_dir = b.FISCAL / "backcast_pandemic_measured_2026_09_28"
    sys.path.insert(0, str(measured_dir))
    import backcast_measured as measured
    plain, eip = measured.load_measured(measured_dir / "derived")
    eip_u = measured.eip_use(eip, "borjas", "personal")
    paid = pandemic_amounts()
    use = pd.read_csv(OUT / "historical_use.csv").set_index(["key", "group", "year"])
    reps = pd.read_csv(OUT / "historical_use_replicates.csv").set_index(["group", "year", "replicate"]).sort_index()
    outputs, line_rows, se_rows, annual_se, pandemic_se = {}, [], [], [], []
    for end in ("low", "high"):
        name = f"net_cost_cbo_informed_oct14_{end}"
        split = carried[name]
        # Each pension accrual part's 2024 value is positive; displaced cash parts stay out.
        # The case-components consumer rule assigns every lineage part explicitly. Use that
        # same rule for the programme union, rather than the debt twin's attribution of the
        # response change at the enlarged group's size.
        full = engine[end]["lineage"]
        twin = json.loads(json.dumps(full))
        own_by_line = {}
        for part, values in split["lineage_parts"].items():
            if part.startswith("capital_"):
                continue
            meta = metadata[part]
            key = (meta["side"], meta["line"])
            own_by_line[key] = own_by_line.get(key, 0.) + values[2024]
        for side, singular in (("spending", "spending"), ("receipts", "receipt")):
            for row in twin[side]:
                row["effect_bn"] += own_by_line.get((singular, row["id"]), 0.)
        for field in ("private_wtp_bn", "induced_receipts_bn"):
            target = "production_private_bn" if field == "private_wtp_bn" else "production_receipts_bn"
            twin[target] += own_by_line.get(("production", field), 0.)
        twin["capital"]["total_bn"] -= sum(v[2024] for k, v in split["lineage_parts"].items() if k.startswith("capital_"))
        twin["cost_bn"] = full["cost_bn"] - sum(v[2024] for v in split["lineage_parts"].values())
        engine[end]["union"] = twin
        accrual = {lid: sum(split["parts"][k][2024] for k, p in metadata.items()
                           if p["rule"] == "accrual" and p["line"] == lid) for lid in ("social_security", "medicare")}
        acc_l = {lid: sum(split["lineage_parts"].get(k, pd.Series(0., index=b.YEARS))[2024]
                         for k, p in metadata.items() if p["rule"] == "accrual" and p["line"] == lid)
                 for lid in accrual}
        values_by_pop = {}
        for population in ("union", "lineage"):
            paths = {}
            for side in ("spending", "receipts"):
                full = {r["id"]: r for r in engine[end]["lineage"][side]}
                twin = {r["id"]: r for r in engine[end]["union"][side]}
                require(set(full) == set(twin), "programme union/full line sets differ")
                for lid, row in full.items():
                    sign = -1.0  # engine effect_bn is welfare; all costs reverse its sign
                    amount = sign * row["effect_bn"]
                    u_amount = sign * twin[lid]["effect_bn"]
                    if amount == 0 and u_amount == 0:
                        continue
                    if lid == "lane_constants":
                        path = annual.group_millions / annual.group_millions[2024]
                        path_l = annual.g3plus_millions_cps / annual.g3plus_millions_cps[2024]
                    elif lid == "social_security" or lid == "medicare":
                        contribution = "oasdi" if lid == "social_security" else "hi"
                        refs = b.V4_ACCRUAL[contribution]
                        se = data["pension_accrual"]["se_oasdi_share"]
                        se = se if contribution == "oasdi" else 1 - se
                        payroll = sum(national(ref) for ref in refs) + se * national(b.V4_SELF_EMPLOYED[0])
                        payroll_path = payroll * real / payroll[2024]
                        cash_path = index(cats.loc[lid, "source_cells"])
                        a = accrual[lid] - acc_l[lid]
                        cash = u_amount - a
                        # Medicare B/D retain their own benefit path; OASDI is all accrual.
                        require(lid != "social_security" or abs(cash) < 1e-6, "OASDI accrual split does not close")
                        values = (a * payroll_path + cash * cash_path) * share
                        if population == "lineage":
                            values += (acc_l[lid] * payroll_path + (amount - u_amount - acc_l[lid]) * cash_path) * g3
                        paths[f"spending:{lid}"] = values
                        continue
                    elif side == "spending":
                        parent = PARENTS.get(lid, lid)
                        path = index(cats.loc[parent, "source_cells"]) * share
                        path_l = index(cats.loc[parent, "source_cells"]) * g3
                    elif lid == "other_production_taxes":
                        nom = national("T30500-A:1") - national("T30500-A:20;T30500-A:38;T30500-A:4;T30500-A:23;T30500-A:15")
                        path = nom * real / nom[2024] * share
                        path_l = nom * real / nom[2024] * g3
                    elif lid == "enterprise_surplus":
                        nom = national("T30100-A:19") - national("T30800-A:13")
                        path = nom * real / nom[2024] * share
                        path_l = nom * real / nom[2024] * g3
                    elif lid == "housing_enterprise_surplus":
                        # Fixed part of the federal subsidy plus housing's own deficit, same as v4_series.
                        meta = next(p for p in metadata.values() if p["line"] == lid)
                        deficit, subsidy = national("T30800-A:13"), national("T31300-A:4")
                        weight = (meta["national_bn"] - deficit[2024]) / subsidy[2024]
                        nom = deficit + weight * subsidy
                        path, path_l = nom * real / nom[2024] * share, nom * real / nom[2024] * g3
                    else:
                        require(lid in b.V4_RECEIPT_CELLS, "no programme source for receipt " + lid)
                        path = index(b.V4_RECEIPT_CELLS[lid]) * share
                        path_l = index(b.V4_RECEIPT_CELLS[lid]) * g3
                    paths[f"{side}:{lid}"] = u_amount * path
                    if population == "lineage":
                        paths[f"{side}:{lid}"] += (amount - u_amount) * path_l
            paths["capital"] = sum(v for k, v in split["parts"].items() if k.startswith("capital_"))
            if population == "union":
                paths["capital"] -= sum(v for k, v in split["lineage_parts"].items() if k.startswith("capital_"))
            r = engine[end][population]
            paths["production_private"] = -r["production_private_bn"] * production_path * share
            paths["production_receipts"] = -r["production_receipts_bn"] * production_path * share
            if population == "lineage":
                u = engine[end]["union"]
                for part, field in (("production_private", "production_private_bn"), ("production_receipts", "production_receipts_bn")):
                    paths[part] = -u[field] * production_path * share \
                        - (r[field] - u[field]) * production_path * g3
            total = sum(paths.values())
            require(abs(total[2024] - r["cost_bn"]) < 1e-6,
                    f"programme does not close to v7 {end}/{population}: {total[2024]} vs {r['cost_bn']}, "
                    f"capital carried {paths['capital'][2024]} engine {r['capital']['total_bn']}")
            baseline_union = sum(split["by_rule"]["ratio"].values()) - sum(split["lineage_parts"].values())
            baseline_union += concept["ends"][end]["cost_bn"] - sum(split["by_rule"]["ratio"].values())[2024]
            if population == "union":
                require(abs(total[2024] - baseline_union[2024]) < 1e-6,
                        f"programme union anchor differs from component control: {total[2024]} vs {baseline_union[2024]}")
            for variant in ("programme", "programme_pandemic", "programme_measured"):
                updated = {k: v.copy() for k, v in paths.items()}
                if variant != "programme":
                    credits = updated["spending:refundable_tax_credits"]
                    source = national("T31200-A:25")
                    u24 = plain.loc[("refundable_credits", "personal", 2024), "relative_use"]
                    union_amount = -engine[end]["union"]["spending"][[r["id"] for r in engine[end]["union"]["spending"]].index("refundable_tax_credits")]["effect_bn"]
                    # The union's measured payment share replaces its credit-key share. Added people's shares
                    # use the measured union ratio as an explicit assumption on their own G3 path.
                    for year in (2020, 2021):
                        credit_use = plain.loc[("refundable_credits", "personal", year), "relative_use"] / u24
                        group_share24 = annual.group_millions[2024] / b.anchors("shared")["residents"]
                        new_union = union_amount * real[year] * share[year] * credit_use * (source[year] - paid[year]) / source[2024] \
                            + paid[year] * real[year] * share[year] * group_share24 * eip_u[year]
                        scale = (credits[year] / (union_amount * index("T31200-A:25")[year] * share[year])) if population == "lineage" else 1.
                        credits[year] = new_union * scale
                        rounds = [("eip1_advance", 2020)] if year == 2020 else [("eip2", 2020), ("eip1_catchup", 2020), ("eip3", 2021)]
                        observations = [eip.loc[(key, "borjas", "personal", y)] for key, y in rounds
                                        if (key, "borjas", "personal", y) in eip.index]
                        weights = np.asarray([value.national_bn for value in observations], float)
                        weights /= weights.sum()
                        terms = np.asarray([value.relative_use_se for value in observations]) * weights
                        require(np.isfinite(terms).all(), "missing pandemic source SE")
                        coefficient = abs(paid[year] * real[year] * share[year] * group_share24 * scale)
                        pandemic_se.append(dict(end=end, population=population, year=year,
                                                eip_component_bn=coefficient * eip_u[year],
                                                eip_se_lower_bn=coefficient * max(0., 2 * terms.max() - terms.sum()),
                                                eip_se_upper_bn=coefficient * terms.sum(),
                                                credit_rest_conditional_se_bn=abs(union_amount * real[year] * share[year]
                                                    * (source[year] - paid[year]) / source[2024] / u24 * scale)
                                                    * plain.loc[("refundable_credits", "personal", year), "relative_use_se"],
                                                conditioning="2024 keys and prices fixed; round covariance not stored, bounds not a combined SE"))
                if variant == "programme_measured":
                    for key, lid, fraction in (("school_age_5_17", "education_services", r["spec"]["share"]),
                                                ("school_age_5_17", "school_reprice", 1.0),
                                                ("medicaid_covered", "medicaid_and_chip_other_medical",
                                                 r["medicaid_coverage_fraction"])):
                        series_key = f"spending:{lid}"
                        if series_key not in updated:
                            continue
                        old = updated[series_key].copy()
                        u_row = engine[end]["union"]["spending"][[x["id"] for x in engine[end]["union"]["spending"]].index(lid)]
                        ua = -u_row["effect_bn"] * fraction
                        la = (-next(x["effect_bn"] for x in engine[end]["lineage"]["spending"] if x["id"] == lid) * fraction - ua)
                        nat_index = index(cats.loc[PARENTS.get(lid, lid), "source_cells"])
                        for year in b.YEARS:
                            changes, replicate_changes = [], np.zeros(161)
                            for group_name, amount, path in (("union", ua, share), ("g3plus", la if population == "lineage" else 0., g3)):
                                if (key, group_name, year) not in use.index:
                                    continue  # Held explicitly where the extract has no coverage variable.
                                value = use.loc[(key, group_name, year)]
                                anchor = use.loc[(key, group_name, 2024)]
                                ratio = value.relative_use / anchor.relative_use
                                contribution = amount * nat_index[year] * path[year]
                                changes.append(contribution * (ratio - 1))
                                if key == "medicaid_covered":
                                    relative_reps = reps.loc[(group_name, year)].relative_use.reindex(range(161)).to_numpy()
                                    require(np.isfinite(relative_reps).all(), "missing Medicaid price replicate")
                                    if year == 2024:
                                        relative_reps = np.repeat(anchor.relative_use, 161)  # fixed anchor by construction
                                    replicate_changes += contribution * (relative_reps / anchor.relative_use - 1)
                                se_rows.append(dict(end=end, population=population, key=key, group=group_name, year=year,
                                                    coefficient_bn=contribution / anchor.relative_use,
                                                    relative_use_se=value.relative_use_se))
                            updated[series_key][year] = old[year] + sum(changes)
                            if key == "medicaid_covered" and changes:
                                require(abs(replicate_changes[0] - sum(changes)) < 1e-9, "coverage-price replicate zero parity")
                                annual_se.append(dict(end=end, population=population, year=year,
                                                      delta_bn=sum(changes), conditional_se_bn=np.sqrt(4/160 *
                                                          np.square(replicate_changes[1:] - replicate_changes[0]).sum()),
                                                      conditioning="2024 relative-use key and case prices fixed; covariance of union/G3 preserved"))
                for rule in ("programme", "programme_income"):
                    adjusted = {k: v * income if rule == "programme_income" and
                                (k.removeprefix("receipts:") in INCOME_RECEIPTS or k == "production_receipts") else v
                                for k, v in updated.items()}
                    # Accrual is income-linked too; the baseline programme holds payroll-relative use fixed.
                    if rule == "programme_income":
                        for lid in accrual:
                            amount = accrual[lid] if population == "lineage" else accrual[lid] - acc_l[lid]
                            ref = b.V4_ACCRUAL["oasdi" if lid == "social_security" else "hi"]
                            se = data["pension_accrual"]["se_oasdi_share"]
                            se = se if lid == "social_security" else 1 - se
                            nom = sum(national(x) for x in ref) + se * national(b.V4_SELF_EMPLOYED[0])
                            pay = nom * real / nom[2024]
                            acc_path = (accrual[lid] - acc_l[lid]) * pay * share
                            if population == "lineage":
                                acc_path += acc_l[lid] * pay * g3
                            adjusted["spending:" + lid] += acc_path * (income - 1)
                    vals = sum(adjusted.values())
                    require(abs(vals[2024] - r["cost_bn"]) < 1e-6, "measured programme anchor closure")
                    outputs[(end, rule, population, variant)] = vals
                    line_rows += [dict(end=end, population=population, variant=variant, rule=rule, part=k,
                                       year=y, cost_bn=v[y]) for k, v in adjusted.items() for y in b.YEARS]
            values_by_pop[population] = paths
    write_csv(pd.DataFrame(line_rows), "programme_lines.csv")
    write_csv(pd.DataFrame(se_rows).drop_duplicates(), "programme_use_uncertainty.csv")
    write_csv(pd.DataFrame(annual_se), "programme_medicaid_se.csv")
    write_csv(pd.DataFrame(pandemic_se).drop_duplicates(), "programme_pandemic_se.csv")
    return outputs


def main():
    started = time.perf_counter()
    OUT.mkdir(parents=True, exist_ok=True)
    rates = primary_rates()
    annual, carried = positive_control()
    book, real, share, g3 = historical_paths(annual)
    scenarios, linked = controlled_changes(annual, carried, rates, book, real, share, g3)
    scenarios.update(programme(annual, carried, book, real, share, g3))
    rows = []
    for (end, rule, population, scenario), values in scenarios.items():
        base_rule = "income" if rule == "programme_income" else "ratio" if rule == "programme" else rule
        base = scenarios[(end, base_rule, population, "fixed_2pct")]
        rows.append(dict(end=end, rule=rule, population=population, scenario=scenario,
                         anchor_2024_bn=values[2024], anchor_change_bn=values[2024] - base[2024],
                         **{w + "_bn": values[values.index >= start].sum() for w, start in WINDOWS.items()},
                         **{w + "_delta_bn": (values - base)[values.index >= start].sum() for w, start in WINDOWS.items()}))
    write_csv(pd.DataFrame(rows), "windows.csv")
    audit = dict(positive_control="four live files byte-identical", national_closure_tolerance_bn=1e-9,
                 programme_anchor_tolerance_bn=1e-6, structural_zero_series="T31200-A:20, 2005-2014 only",
                 income_receipt_lines=sorted(INCOME_RECEIPTS), income_linked_parts=sorted(linked),
                 historical_rate_anchor="Each year's measured yield including 2024; 2024 movement reported, not hidden",
                 missing_use_years="Medicaid: hold 2024 relative use before 2019; no historical survey SE without replicates",
                 capital_high="fixed 3 percent", status="beside, not adopted")
    measured = b.FISCAL / "backcast_pandemic_measured_2026_09_28/derived"
    sources = [HERE / "inputs/acs_mexican_origin.csv", b.G3PLUS_PATH,
               measured / "measured_shares.csv", OUT / "historical_use.csv", OUT / "historical_use_replicates.csv",
               b.ROOT / "sources/immigration-fiscal/data/external/bea_nipa/Section3All_xls.xlsx",
               b.ROOT / "sources/immigration-fiscal/data/external/bea_nipa/Section1All_xls.xlsx",
               HERE / "_cache/Section7All_xls.xlsx", b.FA_WORKBOOK]
    audit["inputs"] = {str(p.relative_to(b.ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    audit["case_inputs"] = b.case_parts("oct14")["inputs"]
    audit["precision"] = "Control reproduces printed bands; P7 restores full-precision case_components cost_bn"
    audit["programme_union_rule"] = "Full engine line effects less case_components' explicit lineage parts; response-size change stays on union"
    audit["programme_measured_rule"] = "School age on K12 operating share and school reprice; coverage on medical line excluding uncompensated-care key shift; fees and capital use fixed 2024 keys"
    audit["programme_uncertainty"] = "Annual Medicaid SDR SE conditional on 2024 key and case prices; no cumulative SE without cross-year covariance"
    (OUT / "audit.json").write_text(json.dumps(audit, sort_keys=True, indent=2) + "\n")
    print("PASS positive control, national closure, programme anchors and finite outputs")
    print(f"elapsed_seconds={time.perf_counter() - started:.3f} peak_rss_bytes={resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}")


if __name__ == "__main__":
    main()
