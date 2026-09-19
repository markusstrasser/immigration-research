"""Matched-population scale checks and a conditional production-surplus model.

This is not a complete welfare estimate or an immigration-policy simulation.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import sys

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
FISCAL = HERE.parent
TARGETS = ("mexico_born", "mexican_second_gen", "mexican_third_plus_selfid")
UNION = "mexican_observed_total"


def surplus_fraction(share, labor_share):
    """Exact Cobb-Douglas surplus to other residents, fixed capital.

    Current output=1; target receives labor_share*share. Without target labor,
    output=(1-share)**labor_share. All capital is assumed owned by others.
    """
    share = np.asarray(share)
    if not 0 < labor_share < 1 or np.any((share < 0) | (share >= 1)):
        raise ValueError("Invalid production-model shares")
    return -labor_share * share - np.expm1(labor_share * np.log1p(-share))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--gdp-billions", required=True, type=float)
    parser.add_argument("--gdp-source", required=True)
    parser.add_argument("--out", type=Path, default=HERE / "derived")
    args = parser.parse_args()
    if not np.isfinite(args.gdp_billions) or args.gdp_billions <= 0:
        raise ValueError("GDP must be positive and finite")
    spec = importlib.util.spec_from_file_location(
        "fiscal_evidence", FISCAL / "education_origin_fiscal_2026_09_19/builder.py")
    evidence = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(evidence)
    fingerprints = evidence.verified_upstream_inputs(ROOT)
    sys.path.insert(0, str(FISCAL / "gen_ledger_extension_2026_09_16"))
    import extend_ledger as ext
    state = ext.build(argparse.Namespace(
        cps_zip=FISCAL / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip"))
    d, weights = state["d"], state["person_weights"]
    civilian = (d.PRPERTYP.eq(2) | d.A_AGE.lt(15)).to_numpy()
    groups = {name: state["group"][name] & civilian for name in TARGETS}
    if np.any(np.sum(list(groups.values()), axis=0) > 1):
        raise ValueError("Generation masks overlap")
    groups[UNION] = np.logical_or.reduce(list(groups.values()))
    groups["third_plus_nh_white"] = state["group"]["third_plus_nh_white"] & civilian
    groups["national_civilian"] = civilian
    profiles_path = FISCAL / "ledger_absolute_2026_09_17/derived/age_profiles.csv"
    profiles = pd.read_csv(profiles_path)
    accounts = profiles[profiles.account.eq("expanded")].groupby(
        ["allocation", "group"], as_index=False)[["population", "net_total"]].sum()
    accounts["net_per_person"] = accounts.net_total / accounts.population
    accounts["deficit_pct_gdp"] = -100 * accounts.net_total / (args.gdp_billions * 1e9)
    totals, rows, scenario_rows = {}, [], []
    for name, mask in groups.items():
        population = weights[mask].sum(axis=0)
        if name != "national_civilian":
            anchor = accounts.loc[accounts.group.eq(name), "population"].to_numpy()
            if len(anchor) != 2 or not np.allclose(anchor, population[0], rtol=1e-10):
                raise ValueError(f"Population differs from fiscal anchor: {name}")
        for measure in ("WSAL_VAL", "PEARNVAL"):
            raw = d[measure].to_numpy(dtype=float)
            if not np.isfinite(raw).all():
                raise ValueError(f"Nonfinite income: {measure}")
            positive = np.maximum(raw, 0)
            total = positive[mask] @ weights[mask]
            totals[name, measure] = total
            rows.append(dict(group=name, measure=measure, population=population[0],
                             positive_income_total=total[0],
                             net_income_total=float(raw[mask] @ weights[mask, 0]),
                             positive_earners=float(weights[mask & (raw > 0), 0].sum()),
                             **ext.base.summarize(total)))
    for measure in ("WSAL_VAL", "PEARNVAL"):
        if not np.allclose(sum(totals[g, measure] for g in TARGETS), totals[UNION, measure]):
            raise ValueError("Generation income totals do not conserve")
        share = totals[UNION, measure] / totals["national_civilian", measure]
        if not np.isfinite(share).all():
            raise ValueError("Nonfinite labor-efficiency proxy")
        for labor_share in (0.60, 0.65, 0.70):
            scales = {"gdp_calibrated": args.gdp_billions * 1e9,
                      "cash_earnings_calibrated": totals["national_civilian", measure] / labor_share}
            for normalization, output in scales.items():
                value = output * surplus_fraction(share, labor_share)
                scenario_rows.append(dict(
                    proxy=measure, capital="fixed", normalization=normalization,
                    labor_share=labor_share, target_efficiency_share=share[0],
                    **ext.base.summarize(value)))
        # Constant returns, homogeneous efficiency labor, fully adjusted capital:
        # wage and capital return unchanged; this particular surplus is zero.
        scenario_rows.append(dict(proxy=measure, capital="fully_adjusted",
                                  normalization="either",
                                  labor_share=0.65, target_efficiency_share=share[0],
                                  estimate=0.0, se_sampling=0.0,
                                  ci95_sampling_low=0.0, ci95_sampling_high=0.0))
    # Independent accounting identity and local approximation probes.
    m, s = .1, .65
    assert np.isclose(surplus_fraction(m, s), 1 - s*m - (1-m)**s)
    assert np.isclose(surplus_fraction(1e-5, s), .5*s*(1-s)*1e-10, rtol=1e-4, atol=0)
    assert surplus_fraction(0, s) == 0
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(out / "income.csv", index=False)
    accounts.to_csv(out / "fiscal_scale.csv", index=False)
    pd.DataFrame(scenario_rows).to_csv(out / "surplus_scenarios.csv", index=False)
    for path in (Path(__file__), Path(ext.__file__), Path(ext.base.__file__),
                 Path(evidence.__file__), Path(state["cps"]), profiles_path):
        fingerprints[str(path)] = evidence.sha(path)
    manifest = dict(
        gdp_billions=args.gdp_billions, gdp_source=args.gdp_source,
        source_hashes=fingerprints, population_anchor="expanded annual ledger, both allocations",
        model_source="https://www.nationalacademies.org/read/23550/chapter/8",
        interpretation="Conditional gross-income surplus to non-target residents; not total welfare",
        assumptions=["Positive cash earnings share proxies homogeneous labor efficiency",
                     "GDP calibration assumes the target share transports to total labor compensation",
                     "Cash normalization uses implied output national positive cash earnings/labor share",
                     "All preexisting capital owned by non-target residents; capital ownership unmeasured",
                     "Competitive Cobb-Douglas production; fixed technology; no policy adjustment",
                     "Foreign ownership, heterogeneous skills, trade, land, innovation and congestion omitted",
                     "Income and benefits of the target group are outside this beneficiary definition",
                     "Fully adjusted case concerns this channel only, not all economic benefits",
                     "Sampling intervals condition on model, GDP and selected parameters",
                     "Fiscal assigned spending is not the corresponding avoidable-spending counterfactual",
                     "Do not add sectoral price benefits or generated taxes without an overlap audit"],
        checks=["Canonical source fingerprints", "Five group population anchors, both allocations",
                "Disjoint generations", "Income conservation across every replicate",
                "Exact output-income identity", "Small-shock limit", "Zero-target limit"])
    (out / "audit.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(pd.DataFrame(scenario_rows).to_string(index=False))


if __name__ == "__main__":
    main()
