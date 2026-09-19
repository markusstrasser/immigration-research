"""Matched population, heterogeneous skills and capital-response scenarios."""
from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
from pathlib import Path
import sys

import numpy as np
import pandas as pd

from model import equilibrium, fiscal_and_private

HERE = Path(__file__).resolve().parent
TARGETS = ("mexico_born", "mexican_second_gen", "mexican_third_plus_selfid")
UNION = "mexican_observed_total"
SOURCES = {
    "model": "https://www.nationalacademies.org/read/23550/chapter/8",
    "tax_and_sigma": "https://www.dominiksachs.com/downloads/fiscal_low_skilled_immigration_final.pdf",
    "publication": "https://doi.org/10.1257/pol.20220176",
    "capital_tax": "https://docs.iza.org/dp15592.pdf",
    "gdp": "https://www.whitehouse.gov/wp-content/uploads/2026/04/2026-Economic-Report-of-the-President.pdf",
}


def summarize(value):
    value = np.asarray(value)
    if value.shape != (161,) or not np.isfinite(value).all():
        raise ValueError("Expected point plus160 finite replicates")
    se = np.sqrt(4 / 160 * np.square(value[1:] - value[0]).sum())
    return dict(estimate=float(value[0]), se_sampling=float(se),
                ci95_sampling_low=float(value[0] - 1.96 * se),
                ci95_sampling_high=float(value[0] + 1.96 * se))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, default=HERE.parents[2])
    parser.add_argument("--gdp-billions", type=float, default=29298.)
    parser.add_argument("--out", type=Path, default=HERE / "derived")
    args = parser.parse_args()
    root = args.source_root.resolve()
    fiscal = root / "infra/immigration-fiscal"
    spec = importlib.util.spec_from_file_location(
        "fiscal_evidence", fiscal / "education_origin_fiscal_2026_09_19/builder.py")
    evidence = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(evidence)
    fingerprints = evidence.verified_upstream_inputs(root)
    sys.path.insert(0, str(fiscal / "gen_ledger_extension_2026_09_16"))
    import extend_ledger as ext
    if "A_HGA" not in ext.base.PERSON:
        ext.base.PERSON.append("A_HGA")
    state = ext.build(argparse.Namespace(
        cps_zip=fiscal / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip"))
    d, weights = state["d"], state["person_weights"]
    civilian = (d.PRPERTYP.eq(2) | d.A_AGE.lt(15)).to_numpy()
    masks = [state["group"][g] & civilian for g in TARGETS]
    if np.any(np.sum(masks, axis=0) > 1):
        raise ValueError("Generation masks overlap")
    target = np.logical_or.reduce(masks)
    other = civilian & ~target
    profiles_path = fiscal / "ledger_absolute_2026_09_17/derived/age_profiles.csv"
    profiles = pd.read_csv(profiles_path)
    anchors = profiles.loc[profiles.account.eq("expanded") & profiles.group.eq(UNION)]
    populations = anchors.groupby("allocation").population.sum()
    if len(populations) != 2 or not np.allclose(populations, weights[target, 0].sum(), rtol=1e-10):
        raise ValueError("Population differs from both canonical fiscal allocations")
    deficits = -anchors.groupby("allocation").net_total.sum()
    components_path = fiscal / "ledger_absolute_2026_09_17/derived/age_profile_components.csv"
    components = pd.read_csv(components_path)
    selected = components.loc[components.account.eq("expanded") & components.group.eq(UNION)]
    if not np.allclose(selected.groupby("allocation").signed_total.sum(), -deficits,
                       rtol=1e-10):
        raise ValueError("Component credits do not reconstruct canonical fiscal totals")
    credits = selected.groupby(["allocation", "component"]).signed_total.sum()
    overlap_rows = []
    for allocation in deficits.index:
        for component, status in {
            "C": "corporate tax pool already credited; replace if attributing modeled capital revenue",
            "owner_property": "possible property-tax overlap; owner-occupied capital is not in production proxy",
            "sales": "excluded from selected capital tax rate .246; do not subtract as known capital overlap",
            "X": "not separately modeled; do not subtract as known capital overlap",
            "tax": "includes capital income taxes but inseparable from labor/payroll in stored aggregate",
        }.items():
            overlap_rows.append(dict(allocation=allocation, component=component,
                                     existing_credit=float(credits[allocation, component]), status=status))
    if not np.isfinite(args.gdp_billions) or args.gdp_billions <= 0:
        raise ValueError("Invalid GDP scale")
    rows, descriptions, thresholds, ownership_rows = [], [], [], []
    for proxy, split in itertools.product(("PEARNVAL", "WSAL_VAL"), ("hs_or_less", "below_ba")):
        raw = d[proxy].to_numpy(float)
        earnings = np.maximum(raw, 0)
        earns = (earnings > 0) & civilian
        if not d.loc[earns, "A_HGA"].between(31, 46).all():
            raise ValueError("Positive earner has missing/reserved education")
        cut = 39 if split == "hs_or_less" else 42
        skill = [d.A_HGA.between(31, cut).to_numpy(), d.A_HGA.between(cut + 1, 46).to_numpy()]
        incomes = {}
        for group, mask in [("target", target), ("outside_target", other), ("national", civilian)]:
            totals = []
            for j, cell in enumerate(skill):
                use = mask & cell
                value = earnings[use] @ weights[use]
                totals.append(value)
                descriptions.append(dict(proxy=proxy, split=split, group=group, skill=j,
                    population=weights[use, 0].sum(), positive_earners=weights[use & earns, 0].sum(),
                    net_earnings=float(raw[use] @ weights[use, 0]), **summarize(value)))
            incomes[group] = np.array(totals)
            if not np.allclose(incomes[group].sum(axis=0), earnings[mask] @ weights[mask], rtol=1e-12):
                raise ValueError("Skill partition loses earnings")
        if not np.allclose(incomes["target"] + incomes["outside_target"], incomes["national"], rtol=1e-12):
            raise ValueError("Target/complement earnings do not conserve")
        national = incomes["national"].sum(axis=0)
        shares = incomes["national"] / national
        fractions = incomes["target"] / incomes["national"]
        for normalization, s, sigma, adjustment, elasticity in itertools.product(
                ("gdp", "cash"), (.60, .65, .70), (1.5, 2., 2.5), (0., .5, 1.), (0., .33)):
            scale = np.full(161, args.gdp_billions * 1e9) if normalization == "gdp" else national / s
            result = equilibrium(shares, fractions, sigma, s, adjustment, elasticity)
            meta = dict(proxy=proxy, split=split, normalization=normalization, labor_share=s,
                        sigma=sigma, capital_adjustment=adjustment, labor_supply_elasticity=elasticity,
                        target_low_efficiency_share=float(fractions[0, 0]),
                        target_high_efficiency_share=float(fractions[1, 0]),
                        national_high_compensation_share=float(shares[1, 0]))
            # Current federal/state/payroll marginal components from source Table1.
            # These are transported2017 parameters, NOT estimated2024 tax rates.
            for retention in (0., .5, 1.):
                partition = fiscal_and_private(result, [.384, .426], .246, retention)
                if (proxy == "PEARNVAL" and split == "hs_or_less" and s == .65
                        and sigma == 2. and adjustment == 1. and elasticity == 0.):
                    for excluded in (0., .5, 1.):
                        owner_partition = fiscal_and_private(result, [.384, .426], .246, retention, excluded)
                        owner_row = dict(**meta, capital_tax_retention=retention,
                                         excluded_capital_owner_share=excluded,
                                         fiscal_dollar_valued_fully_for_included_residents=True)
                        for metric, value in owner_partition.items():
                            owner_row.update({f"{metric}_{k}": v for k, v in summarize(scale*value).items()})
                        ownership_rows.append(owner_row)
                metrics = {k: v for k, v in result.items() if k in (
                    "capital_gain", "domestic_capital_gain", "opportunity_income", "gross_income_gain")}
                metrics.update(labor_gain_low=result["labor_gain"][0], labor_gain_high=result["labor_gain"][1])
                metrics.update(partition)
                # Separate phaseout sensitivity; never add to gross private income.
                metrics["current_transfer_saving"] = (np.array([.038, .010])[:, None] * result["labor_gain"]).sum(axis=0)
                # Source's total wedge includes discounted FUTURE pension liabilities.
                metrics["labor_fiscal_with_future_ss"] = (np.array([.303, .366])[:, None] * result["labor_gain"]).sum(axis=0)
                row = dict(**meta, capital_tax_retention=retention,
                           tax_classification_transport="source_split" if split == "hs_or_less" else "alternate_split_stress",
                           wage_low_without_over_with=result["wage_without_over_with"][0, 0],
                           wage_high_without_over_with=result["wage_without_over_with"][1, 0],
                           hours_low_without_over_with=result["hours_without_over_with"][0, 0],
                           hours_high_without_over_with=result["hours_without_over_with"][1, 0],
                           output_without_over_with=result["output_without_over_with"][0],
                           capital_without_over_with=result["capital_without_over_with"][0])
                for metric, value in metrics.items():
                    row.update({f"{metric}_{k}": v for k, v in summarize(scale * value).items()})
                rows.append(row)
        # How strong would two-skill complementarity need to be for gross income
        # alone to match the attributed fiscal deficit in magnitude? Scale check,
        # NOT a net-welfare break-even. Fixed labor/full capital adjustment.
        for normalization, allocation in itertools.product(("gdp", "cash"), deficits.index):
            scale = args.gdp_billions * 1e9 if normalization == "gdp" else national[0] / .65
            benchmark = float(deficits[allocation])
            lo, hi = .05, 100.
            def value(sig):
                return float(equilibrium(shares[:, 0], fractions[:, 0], sig, .65, 1., 0.)["gross_income_gain"]) * scale
            if value(lo) < benchmark:
                threshold = None
            else:
                for _ in range(80):
                    mid = (lo + hi) / 2
                    if value(mid) > benchmark:
                        lo = mid
                    else:
                        hi = mid
                threshold = (lo + hi) / 2
            thresholds.append(dict(proxy=proxy, split=split, normalization=normalization,
                                   allocation=allocation, benchmark_dollars=benchmark,
                                   sigma_matching_magnitude=threshold,
                                   is_welfare_breakeven=False))
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(descriptions).to_csv(out / "skill_composition.csv", index=False)
    scenarios = pd.DataFrame(rows)
    scenarios.to_csv(out / "scenarios.csv", index=False)
    pd.DataFrame(ownership_rows).to_csv(out / "ownership_sensitivity.csv", index=False)
    pd.DataFrame(overlap_rows).to_csv(out / "existing_tax_credits.csv", index=False)
    # Explicit replacement arithmetic, not a corrected total or causal net
    # effect. The unresolved personal capital-tax component bars direct addition.
    replacements = []
    chosen = scenarios.query("proxy == 'PEARNVAL' and split == 'hs_or_less' and labor_share == .65 and sigma == 2 and capital_adjustment == 1 and labor_supply_elasticity == 0")
    for _, row in chosen.iterrows():
        for allocation in deficits.index:
            corp = float(credits[allocation, "C"])
            prop = float(credits[allocation, "owner_property"])
            for property_replaced in (False, True):
                known_removed = corp + (prop if property_replaced else 0.)
                correction = row.current_receipts_gain_estimate - known_removed
                replacements.append(dict(normalization=row.normalization,
                    capital_tax_retention=row.capital_tax_retention, allocation=allocation,
                    replace_all_owner_property=property_replaced,
                    modeled_outside_receipts=row.current_receipts_gain_estimate,
                    existing_corporate_credit=corp, existing_owner_property_credit=prop,
                    credits_removed=known_removed, candidate_receipts_change=correction,
                    bookkeeping_deficit_before_unidentified_overlap=float(deficits[allocation])-correction,
                    direct_addition_permitted=False,
                    unresolved="Personal capital-income tax overlap; capital-base/property scope; tax incidence transport; avoidable spending"))
    pd.DataFrame(replacements).to_csv(out / "replacement_arithmetic.csv", index=False)
    pd.DataFrame(thresholds).to_csv(out / "magnitude_thresholds.csv", index=False)
    for path in (Path(__file__), HERE / "model.py", Path(ext.__file__), Path(ext.base.__file__),
                 Path(evidence.__file__), Path(state["cps"]), profiles_path, components_path):
        fingerprints[str(path)] = evidence.sha(path)
    manifest = dict(source_hashes=fingerprints, sources=SOURCES,
        population=float(weights[target, 0].sum()), national_population=float(weights[civilian, 0].sum()),
        dollar_year=2024, gdp_billions=args.gdp_billions, scenario_count=len(rows),
        source_vintages={"CPS": "ASEC2025,income2024", "labor_tax": "Colas-Sachs author manuscript2022,ACS2017",
                        "capital_tax": "Clemens2022,Saez-Zucman2011-2013 .246 excludes sales taxes"},
        scope="Observed all-generation Mexican-origin union; outside-union beneficiaries; annual stationary comparison",
        model_assumptions=["Competitive CES skill aggregate under Cobb-Douglas capital",
            "Within each skill target and outside workers are perfect substitutes",
            "Positive cash earnings proxy efficiency units; GDP transports shares to total compensation",
            "Source elasticities transported, not estimated for this population or policy",
            "All initial capital owned by outside residents; released capital earns initial rental rate elsewhere",
            "Capital adjustment is comparative static, not an estimated timing path",
            "Labor supply uses constant uncompensated elasticity and constant marginal taxes; no income effects",
            "Private WTP additionally assumes quasilinear isoelastic disutility and equal dollar valuation",
            "Capital-tax retention is an unestimated fiscal-jurisdiction sensitivity",
            "GDP normalization tax scenarios transport cash-income marginal rates to all compensation",
            "No removal costs, trade, rents, innovation, endogenous skill, public-good saving or historical identification",
            "No consumer-price/production/tax summation; private plus tax identity checked",
            "Existing assigned corporate/property taxes cannot be increased by these scenarios without replacing allocation",
            "Sampling uncertainty conditions on model and transported parameters"],
        checks=["Canonical fingerprints and both population anchors", "All161 earnings partitions",
                "Euler income conservation and fixed-point residual at every scenario/replicate",
                "Private WTP plus tax receipts identity at every scenario/replicate"])
    (out / "audit.json").write_text(json.dumps(manifest, indent=2) + "\n")
    use = scenarios.query("proxy == 'PEARNVAL' and split == 'hs_or_less' and labor_share == .65 and sigma == 2 and labor_supply_elasticity == 0")
    print(use[["normalization", "capital_adjustment", "capital_tax_retention", "gross_income_gain_estimate", "labor_gain_low_estimate", "labor_gain_high_estimate", "current_receipts_gain_estimate"]].to_string(index=False))
    print(f"Validated {len(rows)} scenarios with161 joint CPS weights")


if __name__ == "__main__":
    main()
