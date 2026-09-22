"""Native-immigrant nest inside the production term of the complete annual account.

Replays the existing matched-benefits chain, reproduces its published production
term to the dollar, then re-solves the same counterfactual with a branch nest
inside each skill cell. Conditional model scenarios, never identified policy
effects. No number here is carried from memory; every output is computed from the
CPS extract and the replayed upstream grid.
"""
from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

import nest_model as nest

HERE = Path(__file__).resolve().parent
TARGETS = ("mexico_born", "mexican_second_gen", "mexican_third_plus_selfid")
TAU = [.384, .426]
CAPITAL_TAX = .246
KEYS = ["proxy", "split", "normalization", "labor_share", "sigma",
        "capital_adjustment", "labor_supply_elasticity", "capital_tax_retention"]
SOLVE_KEYS = ["proxy", "split", "labor_share", "sigma", "capital_adjustment",
              "labor_supply_elasticity"]
BRANCHES = ("native_non_union", "union_us_born", "other_foreign_born", "union_mexico_born")
OPTIONS = ("A_by_nativity", "B_target_branch")
SIGMA_FT = 14.
KEEP = ("labor_gain", "capital_gain", "domestic_capital_gain", "opportunity_income",
        "disutility_difference", "labor_gain_by_branch", "disutility_by_branch",
        "wage_without_over_with")
# Section 4 of SPEC.md; 5 and 7 carry no source in this repository.
SIGMA_NI_GRID = ((1.3, True), (3., True), (4.6, True), (5., False), (7., False),
                 (8.7, True), (9., False), (17.9, True), (20., True), (np.inf, True))
SIGMA_NI_CITATION = {
    "1.3": "SOURCE: Cravino-Levchenko-Ortega-Pandalai-Nayar w34790 p.23 - Clemens and Lewis (2024) randomized estimate 1.3; primary text Table 7: sigma = 1.26, 95% CI (0.12, 2.39), firm-level effective elasticity on 472 H-2B firms (us_lowskill_effects_2026_09_22/reads/clemens_lewis_h2b.md)",
    "3": "SOURCE: same paper p.23 and Table 1 p.24 - the selected native-foreign elasticity 3",
    "4.6": "SOURCE: same paper p.23 - Burstein et al. (2020) estimate 4.6; primary text Table III: calibrated within one occupation, no standard error (reads/burstein_ecta_2020.md)",
    "5": "UNVERIFIED: no repo source for this value",
    "7": "UNVERIFIED: no repo source for this value",
    "8.7": "SOURCE: Caiumi and Peri w32389 Table 7 Panel A - 1/sigma_IMMI = 0.115 (0.031) for natives vs immigrants inside no-diploma cells, 2000-2019 2SLS (reads/caiumi_peri_nber_2024.md); their pooled value is 17",
    "9": "INFERENCE: Burstein et al. (2020) footnote 42 - the aggregate native-immigrant elasticity 'is roughly twice as high as our assumed value of rho' (4.6); no numeric value printed",
    "17.9": "SOURCE: Piyapromdee (2020) Table 1 Panel I - sigma_M,L = 17.870 (0.819), natives vs immigrants inside low-skill x gender cells, 114 metros (reads/piyapromdee_restud_2020.md)",
    "20": "SOURCE: same paper p.23, the upper end of the literature range the primary text states; NOT attributed to Ottaviano-Peri, who have no numeric elasticity in this repository",
    "inf": "DATA: the account's own current assumption, matched_benefits_2026_09_19/derived/audit.json model_assumptions",
}
PRODUCTION_ANCHORS = {
    "ces_0086_owner000": dict(private_after_tax_wtp_bn=-0.23592432475743744,
                              induced_current_receipts_bn=13.558522244013947,
                              private_plus_receipts_bn=13.32259791925651),
    "ces_0248_owner000": dict(private_after_tax_wtp_bn=-0.15566955604694444,
                              induced_current_receipts_bn=8.946297252512256,
                              private_plus_receipts_bn=8.790627696465311),
}
PUBLISHED = {name: value["private_plus_receipts_bn"] for name, value in PRODUCTION_ANCHORS.items()}
COMPOSITION_ANCHORS = {("target", 0): 482524920302.8101, ("target", 1): 567059391429.6035,
                       ("national", 0): 2706191503630.509, ("national", 1): 9859381493300.324}
LIMITS = [
    "No change to the capital block: the single comparative-static capital adjustment, the .246 capital tax, domestic_capital_gain and opportunity_income are untouched; the nest moves labor composition only",
    "No dynamics: two stationary economies with versus without the union's labor; no transition path, no arrival or removal timing, no capital accumulation path",
    "The union's own welfare stays out, as the account defines its beneficiaries; target_branch_gain_bn is a diagnostic and never enters a welfare total",
    "No new fiscal channel: the direct fiscal response A is unchanged; only P and F move, and the 165-197bn headline is recomputed by re-running the parent, not here",
    "Other residents contains both winners and losers: natives gain and other foreign-born residents lose from the union's presence under the nest, so the net moves much less than either side",
    "The elasticity is transported, not estimated: no epsilon here is estimated on this population; every value comes from a paper about a different population and a different shock",
    "No occupations, no regions, no trade, no prices: two education cells and one closed economy, so a number here is not comparable to Cravino's 38.6bn except in order of magnitude",
    "No unauthorized/authorized split: the union is defined by origin and generation, and the CPS carries no legal-status variable",
    "Sign is not at stake: ladder entry 166 already records that this affects size, not sign",
    "Sampling standard errors condition on the model and on every transported parameter; the spread across epsilon is a model range, not a confidence interval",
]


def eps_key(value):
    return "inf" if np.isinf(value) else f"{value:g}"


def summarize(value):
    value = np.asarray(value)
    if value.shape != (161,) or not np.isfinite(value).all():
        raise ValueError("Expected point plus 160 finite replicates")
    se = np.sqrt(4 / 160 * np.square(value[1:] - value[0]).sum())
    return float(value[0]), float(se)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def replay_upstream(root, out):
    """Run the existing generator so nothing downstream reads a stale file."""
    upstream = root / "infra/immigration-fiscal/matched_benefits_2026_09_19"
    replay = out / "upstream_replay"
    command = [sys.executable, str(upstream / "builder.py"), "--source-root", str(root),
               "--out", str(replay)]
    completed = subprocess.run(command, text=True, capture_output=True)
    (out / "upstream_replay.log").write_text(completed.stdout + completed.stderr)
    if completed.returncode:
        raise RuntimeError(f"Upstream replay failed ({completed.returncode}); see upstream_replay.log")
    return replay, json.loads((replay / "audit.json").read_text())


def branch_composition(root):
    """Four-branch earnings per skill cell with all 161 CPS replicate weights."""
    fiscal = root / "infra/immigration-fiscal"
    sys.path.insert(0, str(fiscal / "gen_ledger_extension_2026_09_16"))
    import extend_ledger as ext
    if "A_HGA" not in ext.base.PERSON:
        ext.base.PERSON.append("A_HGA")
    state = ext.build(argparse.Namespace(
        cps_zip=fiscal / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip"))
    d, weights = state["d"], state["person_weights"]
    civilian = (d.PRPERTYP.eq(2) | d.A_AGE.lt(15)).to_numpy()
    masks = [state["group"][group] & civilian for group in TARGETS]
    if np.any(np.sum(masks, axis=0) > 1):
        raise ValueError("Generation masks overlap")
    union = np.logical_or.reduce(masks)
    native = d.PRCITSHP.isin([1, 2, 3]).to_numpy()
    foreign = d.PRCITSHP.isin([4, 5]).to_numpy()
    if not (native | foreign).all() or np.any(native & foreign):
        raise ValueError("Citizenship recode does not partition the CPS universe")
    if np.any((masks[1] | masks[2]) & ~native) or np.any(masks[0] & ~foreign):
        raise ValueError("Union generations contradict the citizenship recode")
    parts = {"native_non_union": civilian & native & ~union,
             "union_us_born": civilian & (masks[1] | masks[2]),
             "other_foreign_born": civilian & foreign & ~union,
             "union_mexico_born": civilian & masks[0]}
    if np.any(np.sum(list(parts.values()), axis=0) > 1):
        raise ValueError("Branch masks overlap")
    if not np.array_equal(np.logical_or.reduce(list(parts.values())), civilian):
        raise ValueError("Branch masks do not exhaust the civilian universe")
    rows, calibration = [], {}
    for proxy, split in itertools.product(("PEARNVAL", "WSAL_VAL"), ("hs_or_less", "below_ba")):
        earnings = np.maximum(d[proxy].to_numpy(float), 0)
        earns = (earnings > 0) & civilian
        if not d.loc[earns, "A_HGA"].between(31, 46).all():
            raise ValueError("Positive earner has missing or reserved education")
        cut = 39 if split == "hs_or_less" else 42
        cells = [d.A_HGA.between(31, cut).to_numpy(), d.A_HGA.between(cut + 1, 46).to_numpy()]
        four = np.empty((4, 2, 161))
        national = np.empty((2, 161))
        target = np.empty((2, 161))
        for skill, cell in enumerate(cells):
            use = civilian & cell
            national[skill] = earnings[use] @ weights[use]
            use = union & cell
            target[skill] = earnings[use] @ weights[use]
        for index, name in enumerate(BRANCHES):
            for skill, cell in enumerate(cells):
                use = parts[name] & cell
                four[index, skill] = earnings[use] @ weights[use]
                estimate, se = summarize(four[index, skill])
                rows.append(dict(proxy=proxy, split=split, skill=skill, branch=name,
                                 population=float(weights[use, 0].sum()),
                                 positive_earners=float(weights[use & earns, 0].sum()),
                                 earnings_estimate=estimate, se_sampling=se,
                                 share_of_cell=float(estimate / national[skill, 0])))
        # The nest's calibration is derived from one array, so branch shares sum
        # to one to a single rounding. Dividing instead by the separately
        # accumulated civilian total leaves a 1.3e-14 defect, which the cell
        # power mean amplifies by 1/kappa and the labor-gain cancellation by
        # another order, enough to break the 1e-12 collapse gates. G7 below
        # asserts this total against the independent civilian and union totals.
        cell_total = four.sum(axis=0)
        calibration[(proxy, split)] = dict(
            shares=cell_total / cell_total.sum(axis=0), four_share=four / cell_total[None, :, :],
            union_share=(four[1] + four[3]) / cell_total, cell_total=cell_total,
            national=national, target=target, four=four)
    return pd.DataFrame(rows), calibration, state


def check_composition(calibration, replay, gates):
    """G7: branch earnings reconcile to the upstream skill composition."""
    composition = pd.read_csv(replay / "skill_composition.csv")
    worst = 0.
    for (proxy, split), case in calibration.items():
        four, national, target = case["four"], case["national"], case["target"]
        if not np.allclose(four.sum(axis=0), national, rtol=1e-12, atol=0):
            raise ValueError(f"Branch earnings do not reconstruct the cell total: {proxy}/{split}")
        if not np.allclose(four[1] + four[3], target, rtol=1e-12, atol=0):
            raise ValueError(f"Union branches do not reconstruct the target: {proxy}/{split}")
        rows = composition.loc[composition.proxy.eq(proxy) & composition.split.eq(split)]
        for group, stored in (("national", national), ("target", target)):
            for skill in range(2):
                published = float(rows.loc[rows.group.eq(group)
                                           & rows.skill.eq(skill), "estimate"].iloc[0])
                worst = max(worst, abs(stored[skill, 0] / published - 1))
                if not np.isclose(stored[skill, 0], published, rtol=1e-6, atol=0):
                    raise ValueError(f"Composition drift: {proxy}/{split}/{group}/{skill}")
        if (proxy, split) == ("PEARNVAL", "hs_or_less"):
            for (group, skill), expected in COMPOSITION_ANCHORS.items():
                stored = (national if group == "national" else target)[skill, 0]
                if not np.isclose(stored, expected, rtol=0, atol=1e-3):
                    raise ValueError(f"Anchor composition mismatch: {group}/{skill}")
    gates["G7_calibration_reconciliation"] = dict(
        passed=True, worst_relative=worst, tolerance=1e-6,
        detail="The four branch earnings totals sum to national and the two union branches sum to target, in every one of the 161 weights and all four proxy/split combinations; the four PEARNVAL/hs_or_less anchors match the stored estimates to a tenth of a cent")


def check_anchors(benefits, gates):
    """G1: the published production term, reproduced to the dollar."""
    worst = 0.
    for scenario, expected in PRODUCTION_ANCHORS.items():
        row = benefits.loc[benefits.scenario_id.eq(scenario)]
        if len(row) != 1:
            raise ValueError(f"Anchor scenario missing: {scenario}")
        for column, value in expected.items():
            actual = float(row[column].iloc[0])
            worst = max(worst, abs(actual - value))
            if not np.isclose(actual, value, rtol=0, atol=1e-9):
                raise ValueError(f"Anchor mismatch {scenario}/{column}: {actual!r} vs {value!r}")
    gates["G1_published_production_term"] = dict(
        passed=True, worst_absolute_bn=worst, tolerance_bn=1e-9,
        detail="ces_0086_owner000 = 13.32259791925651 bn (gdp) and ces_0248_owner000 = 8.790627696465311 bn (cash), with both components, reproduced from a fresh replay of matched_benefits_2026_09_19 through full_account_benefits_2026_09_20.expand_ownership")


def make_case(case, option, sigma_ni):
    """Branch weights, removal shares, tree and welfare groups for one nest arm."""
    four = case["four_share"]
    native, foreign = four[0] + four[1], four[2] + four[3]
    if option == "A_by_nativity":
        shares = np.stack([native, foreign])
        removed = np.stack([four[1] / native, four[3] / foreign])
        return nest.two_level(shares, sigma_ni), removed, (), ("native", "other_immigrant")
    if option == "B_target_branch":
        shares = np.stack([four[0], four[2], four[1] + four[3]])
        removed = np.stack([np.zeros_like(four[0]), np.zeros_like(four[2]),
                            np.ones_like(four[0])])
        return (nest.two_level(shares, sigma_ni), removed, (2,),
                ("native", "other_immigrant", "target"))
    if option == "B_deep_cravino":
        shares = np.stack([native, foreign])
        inner = np.stack([four[2] / foreign, four[3] / foreign])
        removed = np.stack([four[1] / native, np.zeros_like(four[2]), np.ones_like(four[3])])
        return (nest.three_level(shares, sigma_ni, 1, inner, SIGMA_FT), removed, (2,),
                ("native", "other_immigrant", "target"))
    raise ValueError(f"Unknown nest option: {option}")


def solve_case(case, option, sigma_ni, sigma, labor_share, adjustment, elasticity,
               proportional=False, keep=KEEP):
    tree, removed, dropped, groups = make_case(case, option, sigma_ni)
    if proportional:
        removed = np.repeat(case["union_share"][None, :, :], removed.shape[0], axis=0)
        dropped = ()
    result = nest.solve(case["shares"], tree, removed, sigma, labor_share, adjustment,
                        elasticity, dropped)
    trimmed = {name: result[name] for name in keep}
    trimmed["groups"] = groups
    return trimmed


def collapse_gates(calibration, source, model, gates):
    """G3 and G4 over all 1296 upstream scenarios, both collapse code paths."""
    worst = {"G3": [0., 0.], "G4": [0., 0.]}
    base_cache, nest_cache = {}, {}
    arms = [("G3", value, True) for value, _ in SIGMA_NI_GRID] + [("G4", np.inf, False)]
    for row in source.itertuples():
        case = calibration[(row.proxy, row.split)]
        key = tuple(getattr(row, name) for name in SOLVE_KEYS)
        if key not in base_cache:
            base_cache[key] = model.equilibrium(
                case["shares"], case["union_share"], row.sigma, row.labor_share,
                row.capital_adjustment, row.labor_supply_elasticity)
        base = base_cache[key]
        expected = model.fiscal_and_private(base, TAU, CAPITAL_TAX, row.capital_tax_retention)
        for option in OPTIONS:
            for label, epsilon, proportional in arms:
                inner = (key, option, eps_key(epsilon), proportional)
                if inner not in nest_cache:
                    nest_cache[inner] = solve_case(
                        case, option, epsilon, row.sigma, row.labor_share,
                        row.capital_adjustment, row.labor_supply_elasticity, proportional,
                        keep=("labor_gain", "capital_gain", "domestic_capital_gain",
                              "opportunity_income", "disutility_difference"))
                got = nest_cache[inner]
                actual = model.fiscal_and_private(got, TAU, CAPITAL_TAX, row.capital_tax_retention)
                for name, want in (("labor_gain", base["labor_gain"]),
                                   ("capital_gain", base["capital_gain"]),
                                   ("private_wtp", expected["private_wtp"]),
                                   ("current_receipts_gain", expected["current_receipts_gain"])):
                    have = got[name] if name in got else actual[name]
                    deviation = float(np.max(np.abs(have - want)))
                    scale = float(np.max(np.abs(want)))
                    worst[label][0] = max(worst[label][0], deviation)
                    worst[label][1] = max(worst[label][1],
                                          deviation / scale if scale else 0.)
                    if not np.allclose(have, want, rtol=1e-12, atol=1e-15):
                        raise ValueError(f"{label} collapse failed: {name} at {inner}")
    gates["G3_strict_generalization"] = dict(
        passed=True, worst_absolute_normalized=worst["G3"][0],
        worst_relative_to_own_scale=worst["G3"][1],
        assertion="numpy.allclose(rtol=1e-12, atol=1e-15) on normalized units, where one unit is GDP",
        scenarios=int(len(source)), reformulated=True,
        detail="REFORMULATED, and strictly stronger in the collapse direction. With the removal proportional across branches the nest returns the unnested labor_gain, capital_gain, private_wtp and current_receipts_gain at EVERY epsilon in the grid, not only at epsilon = sigma, for all 1296 upstream scenarios and both options. SPEC section 5 G3 as worded is unsatisfiable: at kappa = rho the cell aggregate is the power mean of the branch quantities while the unnested model uses their arithmetic mean, so Jensen separates the two whenever the removal is uneven across branches. test_nest_model.test_literal_spec_g3_is_not_an_identity records the measured gap; test_epsilon_equals_sigma_matches_an_independent_flat_ces checks that case against an independently written flat CES instead.")
    gates["G4_perfect_substitution_limit"] = dict(
        passed=True, worst_absolute_normalized=worst["G4"][0],
        worst_relative_to_own_scale=worst["G4"][1],
        assertion="numpy.allclose(rtol=1e-12, atol=1e-15) on normalized units, where one unit is GDP",
        scenarios=int(len(source)),
        detail="At epsilon = infinity (kappa = 1, its own code path, never a large number) the nest returns the unnested results for every one of the 1296 upstream scenarios with the real uneven removal, under both options")


def literal_g3_gap(calibration, model, gates):
    """Measure, on the real calibration, how far the SPEC wording of G3 is from true.

    Recorded so the reformulation in G3 is evidenced by a number in a tracked
    output rather than by an argument in prose.
    """
    case = calibration[("PEARNVAL", "hs_or_less")]
    base = model.equilibrium(case["shares"], case["union_share"], 2., .65, 1., 0.)
    got = solve_case(case, "A_by_nativity", 2., 2., .65, 1., 0.,
                     keep=KEEP + ("cell_quantity_without_over_with", "gross_income_gain"))
    arithmetic = 1 - case["union_share"][:, 0]
    power_mean = got["cell_quantity_without_over_with"][:, 0]
    four = case["four_share"][..., 0]
    gates["G3_strict_generalization"]["literal_spec_wording"] = dict(
        holds=False,
        unnested_cell_quantity=[float(value) for value in arithmetic],
        nested_cell_quantity_at_epsilon_equals_sigma=[float(value) for value in power_mean],
        gross_income_gain_unnested=float(base["gross_income_gain"][0]),
        gross_income_gain_nested=float(got["gross_income_gain"][0]),
        ratio_nested_over_unnested=float(got["gross_income_gain"][0]
                                         / base["gross_income_gain"][0]),
        removed_share_of_foreign_branch_cell0=float(four[3, 0] / (four[2, 0] + four[3, 0])),
        removed_share_of_native_branch_cell0=float(four[1, 0] / (four[0, 0] + four[1, 0])),
        note="At epsilon = sigma the nested cell quantity is the power mean of the branch quantities and the unnested model uses their arithmetic mean, so the two agree only when the removal is even across branches. At PEARNVAL/hs_or_less/sigma=2/adj=1/eta=0 they are not equal and the income gains differ by the ratio shown. This is why G3 is run with a proportional removal at every epsilon instead.")


def zero_shock_gate(calibration, gates):
    """G5: nothing removed, nothing gained, at every epsilon and option."""
    worst = 0.
    for case in calibration.values():
        for option in OPTIONS:
            for epsilon, _ in SIGMA_NI_GRID:
                tree, removed, _, _ = make_case(case, option, epsilon)
                for elasticity in (0., .33):
                    result = nest.solve(case["shares"], tree, np.zeros_like(removed),
                                        2., .65, 1., elasticity)
                    worst = max(worst, float(np.max(np.abs(result["gross_income_gain"]))),
                                float(np.max(np.abs(result["wage_without_over_with"] - 1))))
                    if worst > 1e-13:
                        raise ValueError(f"G5 zero shock moved the economy at {epsilon}")
    gates["G5_zero_shock"] = dict(
        passed=True, worst_absolute=worst, tolerance=1e-13,
        detail="Zero removal leaves every branch wage at one and every gain at zero, across all four proxy/split calibrations, both options, all seven epsilon and both labor-supply elasticities")


def linearization_gate(calibration, gates):
    """G8: exact solver against the section 3.2 first-order formulas."""
    case = calibration[("PEARNVAL", "hs_or_less")]
    four = case["four_share"][..., 0]
    shares = np.stack([four[0] + four[1], four[2] + four[3]])
    point = case["shares"][:, 0]
    report = {}
    for epsilon, _ in SIGMA_NI_GRID:
        deviations = []
        for shock in (1e-2, 1e-4, 1e-6):
            removed = np.zeros((2, 2))
            removed[1, 0] = shock
            exact = np.log(nest.nested_equilibrium(point, shares, removed, 2., epsilon,
                                                   .65, 1., 0.)["wage_without_over_with"])
            linear = nest.linearized_wage_response(point, shares, 0, 2., epsilon,
                                                   np.log(1 - shock), 1)
            if np.sign(exact).tolist() != np.sign(linear).tolist():
                raise ValueError(f"G8 sign disagreement at epsilon={epsilon}, shock={shock}")
            deviations.append(float(np.max(np.abs(exact - linear) / np.abs(linear))))
        if not (deviations[0] > deviations[1] > deviations[2]) or deviations[0] > 1e-2:
            raise ValueError(f"G8 linearization does not converge at first order: {epsilon}")
        report[eps_key(epsilon)] = dict(shock_1pct=deviations[0], shock_1e4=deviations[1],
                                        shock_1e6=deviations[2])
    gates["G8_small_shock_linearization"] = dict(
        passed=True, tolerance_at_1pct=1e-2, by_epsilon=report,
        detail="A 1 percent removal of the foreign branch in the low-skill cell agrees with the section 3.2 formulas in sign, in both cells and for both branches, to the relative deviation listed, and the deviation falls in proportion to the shock. The literal 'three significant figures at 1 percent' reading is NOT met at any epsilon: the measured deviation is 3.0e-3 to 4.3e-3. That is the truncation error of a first-order formula at a finite shock, not a solver error, as the 1e-4 and 1e-6 shock columns show; the gate's stated purpose, catching sign and index errors the collapses cannot catch, is met.")


def delta_floor_check(calibration, audit):
    """Option B removal is exact; the delta floor is a convergence diagnostic only."""
    case = calibration[("PEARNVAL", "hs_or_less")]
    report = {}
    for epsilon, _ in SIGMA_NI_GRID:
        tree, removed, dropped, _ = make_case(case, "B_target_branch", epsilon)
        exact = float(nest.solve(case["shares"], tree, removed, 2., .65, 1., 0.,
                                 dropped)["gross_income_gain"][0])
        deviations, previous = {}, np.inf
        for delta in (1e-6, 1e-9, 1e-12):
            floored = removed.copy()
            floored[2] = 1 - delta
            approximate = float(nest.solve(case["shares"], tree, floored, 2., .65, 1.,
                                           0.)["gross_income_gain"][0])
            deviation = abs(approximate / exact - 1)
            if deviation >= previous:
                raise ValueError(f"Delta floor not converging at epsilon={epsilon}")
            deviations[f"delta_{delta:g}"] = deviation
            previous = deviation
        report[eps_key(epsilon)] = dict(**deviations, meets_1e9_criterion=bool(previous < 1e-9))
    audit["delta_floor_convergence"] = dict(
        estimator="Exact removal of the branch term; the floor never produces a published number",
        monotone_in_delta=True, by_epsilon=report,
        note="The floored aggregate deviates from the exact drop as delta**kappa with kappa = 1 - 1/epsilon, so the brief's 'agree to 1e-9 relative' is reachable only at high epsilon; at epsilon = 1.3 even delta = 1e-12 is about 2e-3 away. Convergence is monotone at every epsilon and nothing published depends on it, because the estimator drops the term exactly.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=HERE / "derived")
    args = parser.parse_args()
    root, out = args.source_root.resolve(), args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    (out / "audit.json").unlink(missing_ok=True)
    fiscal = root / "infra/immigration-fiscal"
    fab = load(fiscal / "full_account_benefits_2026_09_20/builder.py", "full_account_benefits")
    replay, manifest = replay_upstream(root, out)
    fingerprints = dict(manifest["source_hashes"])
    for path, expected in fingerprints.items():
        if fab.sha(path) != expected:
            raise ValueError(f"Upstream input drift: {path}")
    model = load(fiscal / "matched_benefits_2026_09_19/model.py", "matched_stationary_model")
    gdp_bn = manifest["gdp_billions"]
    source = pd.read_csv(replay / "scenarios.csv")
    composition = pd.read_csv(replay / "skill_composition.csv")
    print(f"Replayed {len(source)} upstream scenarios; GDP scale {gdp_bn} bn")

    gates = {}
    benefits = fab.expand_ownership(source, model, composition, gdp_bn)
    fab.validate_ownership_baselines(benefits, pd.read_csv(replay / "ownership_sensitivity.csv"))
    if len(benefits) != 3888 or len(source) != 1296:
        raise ValueError("Upstream grid is not intact")
    gates["G2_grid_intact"] = dict(
        passed=True, upstream_scenarios=int(len(source)),
        expanded_scenarios=int(len(benefits)), ownership_baselines=18,
        detail="expand_ownership and validate_ownership_baselines are imported and run unweakened from full_account_benefits_2026_09_20/builder.py; their own 1296-row, duplicate-key and 18-baseline assertions are the gate")
    check_anchors(benefits, gates)
    print("G1 published production term reproduced; G2 grid intact")

    frame, calibration, state = branch_composition(root)
    check_composition(calibration, replay, gates)
    print("G7 branch composition reconciled to the upstream skill composition")
    collapse_gates(calibration, source, model, gates)
    literal_g3_gap(calibration, model, gates)
    print("G3 proportional-removal collapse and G4 perfect-substitution limit passed")
    zero_shock_gate(calibration, gates)
    linearization_gate(calibration, gates)
    print("G5 zero shock and G8 linearization passed")

    rows, cache, partition_worst = [], {}, 0.
    tau = np.asarray(TAU).reshape(2, 1)
    for row in benefits.itertuples():
        case = calibration[(row.proxy, row.split)]
        scale = (np.full(161, gdp_bn * 1e9) if row.normalization == "gdp"
                 else case["national"].sum(axis=0) / row.labor_share)
        union_pay = row.labor_share * (case["shares"] * case["union_share"]).sum(axis=0)
        for option in OPTIONS:
            for epsilon, sourced in SIGMA_NI_GRID:
                key = (row.proxy, row.split, row.labor_share, row.sigma,
                       row.capital_adjustment, row.labor_supply_elasticity,
                       eps_key(epsilon), option)
                if key not in cache:
                    cache[key] = solve_case(case, option, epsilon, row.sigma, row.labor_share,
                                            row.capital_adjustment, row.labor_supply_elasticity)
                result = cache[key]
                part = model.fiscal_and_private(result, TAU, CAPITAL_TAX,
                                                row.capital_tax_retention,
                                                row.excluded_capital_owner_share)
                private = ((1 - tau) * (result["labor_gain_by_branch"]
                                        - result["disutility_by_branch"])).sum(axis=1)
                residual = (1 - row.excluded_capital_owner_share) * (
                    result["capital_gain"] - part["capital_tax_gain"])
                total = private.sum(axis=0) + residual
                partition_worst = max(partition_worst,
                                      float(np.max(np.abs(total - part["private_wtp"]))))
                if not np.allclose(total, part["private_wtp"], rtol=1e-10, atol=1e-15):
                    raise ValueError(f"Branch private partition does not close: {key}")
                wage = result["wage_without_over_with"]
                estimate, se = summarize(scale * part["private_plus_receipts"] / 1e9)
                item = {name: getattr(row, name) for name in KEYS}
                item.update(
                    scenario_id=row.scenario_id,
                    excluded_capital_owner_share=row.excluded_capital_owner_share,
                    nest_option=option, sigma_NI=epsilon, sigma_NI_sourced=sourced,
                    native_production_gain_bn=float(scale[0] * private[0, 0] / 1e9),
                    other_immigrant_production_gain_bn=float(scale[0] * private[1, 0] / 1e9),
                    capital_private_residual_bn=float(scale[0] * residual[0] / 1e9),
                    other_residents_private_bn=float(scale[0] * part["private_wtp"][0] / 1e9),
                    induced_current_receipts_bn=float(
                        scale[0] * part["current_receipts_gain"][0] / 1e9),
                    private_plus_receipts_bn=estimate,
                    private_plus_receipts_se_sampling_bn=(
                        se if row.excluded_capital_owner_share == 0 else np.nan),
                    sampling_status=("nest_joint_161_weight_SE"
                                     if row.excluded_capital_owner_share == 0
                                     else "point_only_no_covariance_inference"),
                    target_branch_gain_bn=float(scale[0] * union_pay[0] / 1e9),
                    capital_gain_bn=float(scale[0] * result["capital_gain"][0] / 1e9),
                    capital_tax_gain_bn=float(scale[0] * part["capital_tax_gain"][0] / 1e9),
                    wage_pct_native_cell0=float(100 * (wage[0, 0, 0] - 1)),
                    wage_pct_native_cell1=float(100 * (wage[0, 1, 0] - 1)),
                    wage_pct_other_fb_cell0=float(100 * (wage[1, 0, 0] - 1)),
                    wage_pct_other_fb_cell1=float(100 * (wage[1, 1, 0] - 1)),
                    interpretation="CONDITIONAL_MODEL_NOT_IDENTIFIED_POLICY_EFFECT")
                rows.append(item)
    scenarios = pd.DataFrame(rows)
    if len(scenarios) != len(benefits) * len(SIGMA_NI_GRID) * len(OPTIONS):
        raise ValueError("Nest expansion lost rows")
    print(f"Solved {len(scenarios)} nest scenarios over {len(cache)} distinct equilibria")
    gates["G6_euler_and_partition"] = dict(
        passed=True, worst_private_partition=partition_worst, tolerance=1e-10,
        detail="The unweakened Euler assertion inside nest_model.solve fires per skill cell and in total at every scenario and all 161 replicates, fiscal_and_private's own partition identity is unchanged and fires at every row, and the branch split of private WTP closes against it to the deviation shown")

    perfect = scenarios.loc[np.isinf(scenarios.sigma_NI)].set_index(
        ["scenario_id", "nest_option"]).private_plus_receipts_bn.to_dict()
    scenarios["delta_vs_perfect_substitution_bn"] = [
        value - perfect[(scenario, option)] for value, scenario, option
        in zip(scenarios.private_plus_receipts_bn, scenarios.scenario_id, scenarios.nest_option)]
    scenarios["reproduces_published_term_bn"] = [
        PUBLISHED.get(scenario) if np.isinf(epsilon) else np.nan
        for scenario, epsilon in zip(scenarios.scenario_id, scenarios.sigma_NI)]
    for scenario, value in PUBLISHED.items():
        rows_here = scenarios.loc[scenarios.scenario_id.eq(scenario) & np.isinf(scenarios.sigma_NI)]
        if len(rows_here) != len(OPTIONS):
            raise ValueError(f"Missing perfect-substitution row for {scenario}")
        fab.close(rows_here.private_plus_receipts_bn.to_numpy(), value,
                  f"perfect-substitution reproduction {scenario}", 1e-9)
    print("Perfect-substitution rows reproduce the published production term under both options")

    headline = scenarios.loc[scenarios.scenario_id.isin(PUBLISHED)
                             & scenarios.excluded_capital_owner_share.eq(0.)].copy()
    headline["epsilon_order"] = [0 if np.isinf(value) else 1 for value in headline.sigma_NI]
    headline = headline.sort_values(
        ["normalization", "nest_option", "epsilon_order", "sigma_NI"]).drop(columns=["epsilon_order"])
    if len(headline) != len(PUBLISHED) * len(OPTIONS) * len(SIGMA_NI_GRID):
        raise ValueError("Headline block is not the published cases by epsilon and option")

    monotone = []
    for (normalization, option), block in headline.groupby(["normalization", "nest_option"]):
        block = block.loc[~np.isinf(block.sigma_NI)].sort_values("sigma_NI")
        native = block.native_production_gain_bn.to_numpy()
        other = block.other_immigrant_production_gain_bn.to_numpy()
        monotone.append(dict(
            normalization=normalization, nest_option=option,
            other_immigrant_side=("loses_from_the_union" if other.max() < 0
                                  else "gains_from_the_union" if other.min() > 0 else "mixed"),
            native_gain_falls_in_epsilon=bool(np.all(np.diff(native) < 0)),
            other_immigrant_magnitude_falls_in_epsilon=bool(np.all(np.diff(np.abs(other)) < 0)),
            other_immigrant_loss_shrinks_in_epsilon=bool(np.all(np.diff(other) > 0)),
            native_range_bn=[float(native.min()), float(native.max())],
            other_immigrant_range_bn=[float(other.min()), float(other.max())]))
    gates["G9_monotonicity"] = dict(
        reported_not_asserted=True, cases=monotone,
        non_monotone=[case for case in monotone
                      if not (case["native_gain_falls_in_epsilon"]
                              and case["other_immigrant_magnitude_falls_in_epsilon"])],
        detail="Reported, never asserted, over the six finite epsilon of the published cases; the infinite point is the collapse and is excluded from the difference. Both sides fall in magnitude as epsilon rises, converging on the perfect-substitution result, in all four blocks. The SPEC wording 'other immigrants' loss falls' presumes Option A's sign: only under Option A is the other-foreign-born branch itself cut, so only there do other immigrants lose from the union's presence. Under Option B nothing outside the union is removed, both surviving branches face the same wage change and other immigrants gain, so other_immigrant_loss_shrinks_in_epsilon is false there by construction and is not a non-monotonicity.")

    audit = dict(gates=gates)
    delta_floor_check(calibration, audit)
    audit["b_deep_cravino"] = dict(
        built=False, machinery_tested=True, sigma_FT=SIGMA_FT,
        options_clean=bool(all(gate.get("passed", True) for gate in gates.values())),
        reason="Not built, and the omission is a judgment about transport, not a gate failure. Options A and B pass every gate, which is the brief's condition, but the deep arm's inner elasticity sigma_FT = 14 is Cravino's authorized-versus-unauthorized elasticity while this lane's inner split is Mexico-born versus other foreign-born, a different partition that the CPS cannot resolve (SPEC section 7.8). Shipping it would add a fourth arm whose only new parameter is transported across a partition mismatch. nest_model.three_level and test_three_level_nest_absorbs_into_two_when_elasticities_match are written and passing, and make_case already accepts 'B_deep_cravino', so the arm is one grid entry away once the operator accepts that transport.")
    for path in [Path(__file__), HERE / "nest_model.py", HERE / "test_nest_model.py",
                 HERE / "SPEC.md", HERE / "BRIEF.md",
                 fiscal / "matched_benefits_2026_09_19/model.py",
                 fiscal / "matched_benefits_2026_09_19/builder.py",
                 fiscal / "matched_benefits_2026_09_19/test_model.py",
                 fiscal / "full_account_benefits_2026_09_20/builder.py",
                 fiscal / "full_account_benefits_2026_09_20/derived/benefit_scenarios.csv",
                 Path(state["cps"]), *sorted(replay.glob("*.csv")), replay / "audit.json"]:
        fingerprints[str(path)] = fab.sha(path)
    audit.update(
        source_hashes=fingerprints, dollar_year=2024, gdp_billions=gdp_bn,
        population=manifest["population"], national_population=manifest["national_population"],
        upstream_scenarios=int(len(source)), expanded_ownership_scenarios=int(len(benefits)),
        nest_scenarios=int(len(scenarios)), distinct_equilibria=int(len(cache)),
        sigma_NI_grid={eps_key(value): dict(sourced=bool(sourced),
                                            citation=SIGMA_NI_CITATION[eps_key(value)])
                       for value, sourced in SIGMA_NI_GRID},
        nest_options=dict(
            A_by_nativity="Two branches: native (PRCITSHP 1-3, including union G2 and G3+) against foreign-born (PRCITSHP 4-5, including union G1). Removal cuts both branches, because most of the union's earnings belong to people who are US-born.",
            B_target_branch="[UNVERIFIED-STRUCTURAL] Three branches: native non-union, other foreign-born, and the union at the same epsilon against natives. It asserts that a third-generation self-identified Mexican-origin US-born worker is a worse substitute for other natives than a foreign-born non-Mexican worker is, which this repository has no evidence for. Reported beside Option A, never instead of it."),
        sign_convention="With target minus without target; positive means other residents gain from the union's presence",
        beneficiaries="Other US residents outside the canonical target; the union's own welfare is excluded",
        counterfactual="Stationary economy with versus without the union's labor, with a branch nest inside each skill cell",
        sampling="161 joint CPS replicate weights carried through the branch composition and the core excluded_capital_owner_share == 0 rows; no covariance is invented for the epsilon dimension, which is an assumption and not a sampled quantity",
        limitations=LIMITS)
    frame.to_csv(out / "branch_composition.csv", index=False)
    headline.to_csv(out / "nest_headline.csv", index=False)
    scenarios.to_csv(out / "nest_scenarios.csv", index=False)
    audit["outputs"] = {path.name: fab.sha(path) for path in sorted(out.glob("*.csv"))}
    (out / "audit.json").write_text(json.dumps(audit, indent=2, allow_nan=False) + "\n")
    show = headline[["normalization", "nest_option", "sigma_NI", "native_production_gain_bn",
                     "other_immigrant_production_gain_bn", "other_residents_private_bn",
                     "private_plus_receipts_bn", "delta_vs_perfect_substitution_bn"]]
    print(show.to_string(index=False))
    print(f"Wrote {len(scenarios)} nest scenarios, {len(headline)} headline rows, "
          f"{len(frame)} branch-composition rows")


if __name__ == "__main__":
    main()
