"""Tabulate every number in the validation memo's verdict and sections 1-3 against lane outputs.

Reads only: the memo, the five validation lanes' ignored derived/ outputs, and the earlier lanes and
memos that section 1 cites. Writes derived/memo_check.csv (one row per memo number) and
derived/construct_checks.csv (computed facts behind the construct review in RESULT.md).

A row matches when the lane value, rounded as the memo prints it, equals the memo value: the
absolute difference is at most half a unit of the memo's last digit. Counts must be equal. Every memo
literal must occur in the memo text, so a transcription error here fails loudly instead of passing.
"""
from __future__ import annotations

import ast
import csv
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

LANE = Path(__file__).resolve().parent
ROOT = LANE.parents[2]
F = ROOT / "infra/immigration-fiscal"
MEMO = ROOT / "research/immigration-validation-and-backtesting-2026-09-28.md"
OUT = LANE / "derived"


def norm(text: str) -> str:
    return " ".join(text.replace("**", "").split())


def table(path: str) -> pd.DataFrame:
    return pd.read_csv(F / path)


def one(df: pd.DataFrame, **eq) -> pd.Series:
    mask = pd.Series(True, index=df.index)
    for key, value in eq.items():
        mask &= df[key].eq(value)
    if int(mask.sum()) != 1:
        raise ValueError(f"[BLOCKED] expected one row for {eq}, found {int(mask.sum())}")
    return df[mask].iloc[0]


def text_numbers(path: Path, pattern: str) -> list[float]:
    match = re.search(pattern, path.read_text())
    if not match:
        raise ValueError(f"[BLOCKED] pattern not found in {path.name}: {pattern}")
    return [float(g.replace(",", "").replace("−", "-")) for g in match.groups()]


def main() -> int:
    memo = norm(MEMO.read_text())
    rows: list[dict] = []

    def add(section, quantity, literal, memo_value, tol, lane_value, source, definition=""):
        if norm(literal) not in memo:
            raise ValueError(f"[BLOCKED] memo literal not found: {literal!r}")
        diff = float(lane_value) - float(memo_value)
        rows.append({"section": section, "quantity": quantity, "memo_literal": literal,
                     "memo_value": memo_value, "lane_value": float(lane_value),
                     "difference": diff, "tolerance": tol,
                     "status": "match" if abs(diff) <= tol + 1e-9 else "MISMATCH",
                     "lane_source": source, "lane_definition": definition})

    # Intro: the September 27 account and its component sensitivity.
    b = one(table("main_case_long_run_2026_09_27/derived/main_case_bands.csv"),
            profile="long_run_non_school_full", variant="adopted")
    src = "main_case_long_run_2026_09_27/derived/main_case_bands.csv (long_run_non_school_full, adopted)"
    add("intro", "account, low end, $bn", "$321.8–387.4bn", 321.8, .05, b.cost_low_bn, src + ": cost_low_bn")
    add("intro", "account, high end, $bn", "$321.8–387.4bn", 387.4, .05, b.cost_high_bn, src + ": cost_high_bn")
    add("intro", "component sensitivity, low, $bn", "$258.6–436.1bn", 258.6, .05, b.range_low_bn, src + ": range_low_bn")
    add("intro", "component sensitivity, high, $bn", "$258.6–436.1bn", 436.1, .05, b.range_high_bn, src + ": range_high_bn")

    # Section 1 table.
    acs = table("same_year_tax_2026_09_20/derived/acs_cps_comparison.csv")
    sm = one(acs, region="US", group="selfid_mexican", metric="mean_ratio_to_complement")
    mb = one(acs, region="US", group="mexico_born", metric="mean_ratio_to_complement")
    src = "same_year_tax_2026_09_20/derived/acs_cps_comparison.csv (US, {g}, mean_ratio_to_complement): {c}"
    for literal, value, series, group, col in [
            ("0.6919 in ACS2024", .6919, sm, "selfid_mexican", "estimate_acs"),
            ("0.6866 in CPS2025", .6866, sm, "selfid_mexican", "estimate_cps"),
            (".6867–.6972", .6867, sm, "selfid_mexican", "ci95_low_acs"),
            (".6867–.6972", .6972, sm, "selfid_mexican", "ci95_high_acs"),
            (".6649–.7082", .6649, sm, "selfid_mexican", "ci95_low_cps"),
            (".6649–.7082", .7082, sm, "selfid_mexican", "ci95_high_cps"),
            (".6851/.6458", .6851, mb, "mexico_born", "estimate_acs"),
            (".6851/.6458", .6458, mb, "mexico_born", "estimate_cps")]:
        add("1 table: earnings", f"{group} {col}", literal, value, .00005, series[col],
            src.format(g=group, c=col))
    ssa = table("same_year_tax_2026_09_20/derived/ssa_comparisons.csv")
    gw = one(ssa, scope="civilian", region="US", source="awi_all_areas", metric="gross_wages")
    ww = one(ssa, scope="civilian", region="US", source="awi_all_areas", metric="wage_workers")
    src = "same_year_tax_2026_09_20/derived/ssa_comparisons.csv (civilian, awi_all_areas, {m}): {c}"
    add("1 table: wages", "income2023 CPS wages, $bn", "$11,105.6bn", 11105.6, .05, gw.cps_value / 1e9,
        src.format(m="gross_wages", c="cps_value"))
    add("1 table: wages", "SSA compensation, $bn", "$11,103.2bn", 11103.2, .05, gw.source_value / 1e9,
        src.format(m="gross_wages", c="source_value"))
    add("1 table: wages", "income2023 difference, %", "+0.021%", .021, .0005, gw.raw_pct_difference,
        src.format(m="gross_wages", c="raw_pct_difference"))
    add("1 table: wages", "income2023 recipient shortfall, %", "6.09%/5.27%", 6.09, .005, -ww.raw_pct_difference,
        src.format(m="wage_workers", c="-raw_pct_difference"))
    admin = ROOT / "research/immigration-administrative-checks-2026-09-19.md"
    cps24, ssa24 = text_numbers(admin, r"\| Wage dollars \| \$([0-9,.]+)bn \| \$([0-9,.]+)bn \|")
    add("1 table: wages", "income2024 difference, %", "+2.25%", 2.25, .005, 100 * (cps24 / ssa24 - 1),
        "research/immigration-administrative-checks-2026-09-19.md, Wage dollars row", "100*(CPS/SSA-1)")
    rc24, rs24 = text_numbers(admin, r"\| Wage recipients \| ([0-9.]+)m \| ([0-9.]+)m \|")
    add("1 table: wages", "income2024 recipient shortfall, %", "6.09%/5.27%", 5.27, .005, 100 * (1 - rc24 / rs24),
        "research/immigration-administrative-checks-2026-09-19.md, Wage recipients row", "100*(1-CPS/SSA)")
    four = ROOT / "research/immigration-four-fiscal-checks-2026-09-20.md"
    ca, tx, se_ca, se_tx = text_numbers(
        four, r"residuals of \+([0-9]+)k/\+([0-9]+)k, against residual sampling SEs\s+of ([0-9]+)k/([0-9]+)k")
    tx_other, tx_other_se = text_numbers(four, r"underpredicted by ([0-9]+)k \(SE ?([0-9]+)k\)")
    src = "research/immigration-four-fiscal-checks-2026-09-20.md (cited text)"
    for literal, value, lane, q in [("+17k/+27k", 17, ca, "California residual, k pupils"),
                                    ("+17k/+27k", 27, tx, "Texas residual, k pupils"),
                                    ("69k/59k", 69, se_ca, "California residual SE, k"),
                                    ("69k/59k", 59, se_tx, "Texas residual SE, k"),
                                    ("154k (SE69k)", 154, tx_other, "Texas other-resident underprediction, k"),
                                    ("154k (SE69k)", 69, tx_other_se, "its SE, k")]:
        add("1 table: school transport", q, literal, value, 0, lane, src)
    snap = one(table("admin_benefit_keys_2026_09_24/derived/share_comparisons.csv"), programme="snap",
               geography="CA", definition="benefit dollars split over participants")
    src = "admin_benefit_keys_2026_09_24/derived/share_comparisons.csv (snap, CA, dollars over participants): "
    add("1 table: SNAP", "California QC Hispanic dollar share, %", "43.989% administrative QC", 43.989, .0005,
        100 * snap.admin_share, src + "admin_share")
    add("1 table: SNAP", "California CPS Hispanic dollar share, %", "44.078% CPS", 44.078, .0005,
        100 * snap.cps_share, src + "cps_share")
    irs = one(table("same_year_tax_2026_09_20/derived/irs_national.csv"), scope="civilian",
              metric="income_tax_after_nonrefundable")
    add("1 table: federal tax", "CPS tax before refundable credits below IRS, %", "13.73% below IRS", 13.73, .005,
        -irs.raw_pct_difference, "same_year_tax_2026_09_20/derived/irs_national.csv (civilian, "
        "income_tax_after_nonrefundable): -raw_pct_difference")
    br = table("same_year_tax_2026_09_20/derived/irs_bracket_summary.csv")
    br = br[br.metric.eq("income_tax_after_nonrefundable")]
    if sorted(br.bracket) != sorted(["under_100k", "100k_to_200k", "200k_to_500k", "500k_plus"]):
        raise ValueError("[BLOCKED] IRS bracket set changed")
    top = one(br, bracket="500k_plus").difference / 1e9
    below = br[br.bracket.ne("500k_plus")].difference.sum() / 1e9
    src = "same_year_tax_2026_09_20/derived/irs_bracket_summary.csv (income_tax_after_nonrefundable): "
    add("1 table: federal tax", "shortfall above $500k AGI, $bn", "$489.8bn", 489.8, .05, -top,
        src + "-difference, 500k_plus")
    add("1 table: federal tax", "excess below $500k AGI, $bn", "$200.2bn", 200.2, .05, below,
        src + "sum of difference, other brackets")
    (k,) = text_numbers(ROOT / "research/immigration-outside-checks-2026-09-24.md",
                        r"raise the school component of the key by k = ([0-9.]+)")
    add("1: school price", "school cost raised by location, %", "about 3.4%", 3.4, .05, 100 * (k - 1),
        "research/immigration-outside-checks-2026-09-24.md: k", "100*(k-1)")
    diag = table("validation_medical_2026_09_28/derived/diagnostics.csv")

    def ratio(survey, domain="raw_65plus_medicare_ever", payer="public_common"):
        return one(diag, survey=survey, domain=domain, payer=payer, statistic="ratio")

    src = "validation_medical_2026_09_28/derived/diagnostics.csv ({s}, raw_65plus_medicare_ever, public_common, ratio): {c}"
    for literal, value, survey, col in [("0.845 (SE .089)", .845, "MEPS2023", "value"),
                                        ("0.845 (SE .089)", .089, "MEPS2023", "se"),
                                        ("1.265 (.152)", 1.265, "MCBS2023", "value"),
                                        ("1.265 (.152)", .152, "MCBS2023", "se")]:
        add("1: healthcare", f"{survey} Hispanic/NH-white ratio {col}", literal, value, .0005,
            ratio(survey)[col], src.format(s=survey, c=col))
    pooled, pooled_se = text_numbers(
        F / "medical_ethnicity_pooled_2026_09_23/RESULT.md",
        r"\| 5 Public = Medicare \+ Medicaid only \(the MCBS payer set\) \| \*\*([0-9.]+) \(([0-9.]+)\)\*\*")
    src = "medical_ethnicity_pooled_2026_09_23/RESULT.md, row 5 (cited text)"
    add("1: healthcare", "pooled MEPS2016-24 ratio", "1.005 (.056)", 1.005, .0005, pooled, src)
    add("1: healthcare", "pooled MEPS2016-24 SE", "1.005 (.056)", .056, .0005, pooled_se, src)

    # Section 2: the scaling test and the two audit probes.
    cv = table("scaling_test_2026_09_20/derived/school_cv.csv")
    ex = cv[cv["sample"].eq("existing_screen")].set_index("model")
    src = "scaling_test_2026_09_20/derived/school_cv.csv (existing_screen): "
    if ex.n.nunique() != 1:
        raise ValueError("[BLOCKED] scaling folds differ in n")
    add("2: school scaling", "districts scored", "scored 12,370 districts", 12370, 0, ex.n.iloc[0], src + "n")
    for literal, value, model in [(".301 for a 3/4", .301, "three_quarters"), (".233 for 5/6", .233, "five_sixths"),
                                  (".223 for .85", .223, "point85"), (".203 for proportional", .203, "linear"),
                                  (".192 for a freely fitted", .192, "free")]:
        add("2: school scaling", f"log RMSE, {model}", literal, value, .0005, ex.loc[model, "log_rmse"],
            src + f"log_rmse, {model}")
    broad = cv[cv["sample"].eq("broader_screen")].set_index("model").log_rmse
    same_order = list(ex.log_rmse.sort_values().index) == list(broad.sort_values().index)
    add("2: school scaling", "broader screen keeps the ranking (1 = yes)", "The broader screen preserves that order",
        1, 0, int(same_order), src + "log_rmse ranks, broader_screen")
    gss = json.loads((F / "validation_audit_2026_09_28/derived/gss_baseline.json").read_text())
    g = {(r["frame"], r["group"]): r for r in gss["results"]}
    src = "validation_audit_2026_09_28/derived/gss_baseline.json results ({f}, {g}): {c}"
    for literal, value, frame, group, col in [
            ("4.59pp", 4.59, "english_only", "all_origins_G2", "model_tv_pp"),
            ("5.67pp", 5.67, "english_only", "all_origins_G2", "naive_tv_pp"),
            ("2.80pp", 2.80, "english_only", "all_origins_G3", "model_tv_pp"),
            ("5.16pp", 5.16, "english_only", "all_origins_G3", "naive_tv_pp"),
            ("3.39pp", 3.39, "english_only", "all_origins_G4plus", "model_tv_pp"),
            ("9.24pp", 9.24, "english_only", "all_origins_G4plus", "naive_tv_pp"),
            ("3.29pp versus 2.72pp", 3.29, "english_only_pre2021", "all_origins_G2", "model_tv_pp"),
            ("3.29pp versus 2.72pp", 2.72, "english_only_pre2021", "all_origins_G2", "naive_tv_pp")]:
        add("2: GSS", f"{frame} {group} {col}", literal, value, .005, g[(frame, group)][col],
            src.format(f=frame, g=group, c=col))
    wins = sum(r["model_tv_pp"] < r["naive_tv_pp"] for r in gss["results"])
    add("2: GSS", "comparisons the model wins", "eight of nine", 8, 0, wins,
        "gss_baseline.json: count model_tv_pp < naive_tv_pp")
    add("2: GSS", "comparisons reported", "eight of nine", 9, 0, len(gss["results"]), "gss_baseline.json: results")
    (n13,) = text_numbers(ROOT / "research/immigration-projection-backtest-2026-09-19.md",
                          r"Mexican-family-origin G2 has \*\*([0-9]+)\*\* usable training respondents")
    add("2: GSS", "Mexican-origin G2 training respondents", "only13 training respondents", 13, 0, n13,
        "research/immigration-projection-backtest-2026-09-19.md (cited upstream text)")
    add("2: GSS", "frames skipping Mexican-origin G2", "fails the upstream cell-support rule in every frame", 3, 0,
        sum(s["group"] == "Mexican_family_origin_G2" for s in gss["skipped"]), "gss_baseline.json: skipped")
    snap = json.loads((F / "validation_audit_2026_09_28/derived/snap_loso.json").read_text())
    a, h = snap["all_valid_states"], snap["at_least_30_raw_hispanic_records"]
    src = "validation_audit_2026_09_28/derived/snap_loso.json "
    for literal, value, tol, lane, key in [
            ("on 25 valid state/DC jurisdictions", 25, 0, a["states"] - 1, "all_valid_states.states - 1"),
            ("predict the 26th", 26, 0, a["states"], "all_valid_states.states"),
            ("worsens from 5.16 to 5.69pp", 5.16, .005, a["raw"]["mae_pp"], "all_valid_states.raw.mae_pp"),
            ("worsens from 5.16 to 5.69pp", 5.69, .005, a["corrected"]["mae_pp"], "all_valid_states.corrected.mae_pp"),
            ("RMSE from 8.13 to 8.79pp", 8.13, .005, a["raw"]["rmse_pp"], "all_valid_states.raw.rmse_pp"),
            ("RMSE from 8.13 to 8.79pp", 8.79, .005, a["corrected"]["rmse_pp"], "all_valid_states.corrected.rmse_pp"),
            ("+1.03 to −0.19pp", 1.03, .005, a["raw"]["bias_pp"], "all_valid_states.raw.bias_pp"),
            ("+1.03 to −0.19pp", -.19, .005, a["corrected"]["bias_pp"], "all_valid_states.corrected.bias_pp"),
            ("20 of 26 jurisdictions improve", 20, 0, a["states_improved"], "all_valid_states.states_improved"),
            ("17-state higher-sample-support subset", 17, 0, h["states"], "at_least_30_raw_hispanic_records.states"),
            ("MAE 5.42→6.11pp", 5.42, .005, h["raw"]["mae_pp"], "at_least_30_raw_hispanic_records.raw.mae_pp"),
            ("MAE 5.42→6.11pp", 6.11, .005, h["corrected"]["mae_pp"],
             "at_least_30_raw_hispanic_records.corrected.mae_pp")]:
        add("2: SNAP", key, literal, value, tol, lane, src + key)

    # Section 3: schools.
    sc = table("validation_schools_2026_09_28/derived/scores.csv")
    pre = sc[sc.panel.eq("prepandemic") & sc.outcome.eq("current") & sc.stratum.eq("all")]

    def s(fit, score, arm, col):
        return one(pre, fit_weight=fit, score_weight=score, arm=arm)[col]

    src = "validation_schools_2026_09_28/derived/scores.csv (prepandemic, current, all; fit {f}, score {w}, {a}): {c}"
    for literal, value, tol, fit, score, arm, col, scale in [
            ("Across 12,011 districts", 12011, 0, "district", "district", "free_trend", "n", 1),
            ("log RMSE .182", .182, .0005, "district", "district", "free_trend", "log_rmse", 1),
            ("versus .202 for proportional enrollment", .202, .0005, "district", "district", "proportional_trend",
             "log_rmse", 1),
            (".169 versus .175", .169, .0005, "initial_pupils", "initial_pupils", "proportional", "log_rmse", 1),
            (".169 versus .175", .175, .0005, "initial_pupils", "initial_pupils", "free_trend", "log_rmse", 1),
            ("$5.86m versus $7.09m", 5.86, .005, "district", "district", "proportional", "level_mae", 1e6),
            ("$5.86m versus $7.09m", 7.09, .005, "district", "district", "free_trend", "level_mae", 1e6)]:
        add("3: schools", f"{arm} {col}, fit {fit}, score {score}", literal, value, tol,
            s(fit, score, arm, col) / scale, src.format(f=fit, w=score, a=arm, c=col))
    strata = sc[sc.panel.eq("prepandemic") & sc.outcome.eq("current") & sc.fit_weight.eq("district")
                & sc.score_weight.eq("district")]
    for stratum, arm, literal in [("growing", "proportional", "Growing districts favor the simple proportional rule"),
                                  ("shrinking", "frozen", "shrinking districts favor unchanged real spending")]:
        t = strata[strata.stratum.eq(stratum)]
        best = t.loc[t.log_rmse.idxmin(), "arm"]
        add("3: schools", f"best arm in {stratum} districts is {arm} (1 = yes)", literal, 1, 0, int(best == arm),
            f"scores.csv (prepandemic, current, {stratum}, district fit and score): arm with least log_rmse = {best}")
    jo = one(table("validation_schools_2026_09_28/derived/joint_observed.csv"), stratum="all")
    src = "validation_schools_2026_09_28/derived/joint_observed.csv (all): "
    add("3: schools", "matched districts", "12,138 districts matched", 12138, 0, jo.n, src + "n")
    add("3: schools", "pupil decline, %", "pupils fall 3.46%", 3.46, .005, -jo.pupils_growth_percent,
        src + "-pupils_growth_percent")
    add("3: schools", "real current spending growth, %", "real current spending rises 5.50%", 5.50, .005,
        jo.current_growth_percent, src + "current_growth_percent")
    add("3: schools", "teacher FTE growth, %", "teacher FTE rises 1.99%", 1.99, .005, jo.teachers_growth_percent,
        src + "teachers_growth_percent")
    q = table("validation_schools_2026_09_28/derived/state_resource_quality.csv")
    r4 = q[q.subject.eq("reading") & q.grade.eq(4)]
    both = int(((r4.pupil_teacher_ratio1 < r4.pupil_teacher_ratio0) & (r4.score_change < 0)).sum())
    src = "validation_schools_2026_09_28/derived/state_resource_quality.csv (reading, grade 4): "
    add("3: schools", "jurisdictions with lower pupils/teacher and lower grade-4 reading", "46 of 51", 46, 0, both,
        src + "count(pupil_teacher_ratio1 < ratio0 and score_change < 0)")
    add("3: schools", "jurisdictions in the join", "46 of 51", 51, 0, len(r4), src + "rows")

    # Section 3: medical.
    src = "validation_medical_2026_09_28/derived/diagnostics.csv ({s}, raw_65plus_medicare_ever, public_common, ratio): {c}"
    for literal, value, survey, col in [("1.114 (SE .151)", 1.114, "MCBS2022", "value"),
                                        ("1.114 (SE .151)", .151, "MCBS2022", "se"),
                                        ("1.009 (.109)", 1.009, "MEPS2022", "value"),
                                        ("1.009 (.109)", .109, "MEPS2022", "se")]:
        add("3: medical", f"{survey} ratio {col}", literal, value, .0005, ratio(survey)[col],
            src.format(s=survey, c=col))
    gaps = table("validation_medical_2026_09_28/derived/cross_survey_gaps.csv")
    g22, g23 = one(gaps, year=2022, payer="public_common"), one(gaps, year=2023, payer="public_common")
    src = "validation_medical_2026_09_28/derived/cross_survey_gaps.csv ({y}, public_common): {c}"
    add("3: medical", "2022 MCBS-MEPS gap", "gap is .106 (.186)", .106, .0005, g22.difference,
        src.format(y=2022, c="difference"))
    add("3: medical", "2022 gap SE", "gap is .106 (.186)", .186, .0005, g22.se, src.format(y=2022, c="se"))
    add("3: medical", "2023 MCBS-MEPS gap", "compared with .420 (.177) in 2023", .420, .0005, g23.difference,
        src.format(y=2023, c="difference"))
    add("3: medical", "2023 gap SE", "compared with .420 (.177) in 2023", .177, .0005, g23.se,
        src.format(y=2023, c="se"))
    add("3: medical", "2022 gap, 95% interval low", "[−.259,+.470]", -.259, .0005, g22.difference - 1.96 * g22.se,
        src.format(y=2022, c="difference - 1.96*se"))
    add("3: medical", "2022 gap, 95% interval high", "[−.259,+.470]", .470, .0005, g22.difference + 1.96 * g22.se,
        src.format(y=2022, c="difference + 1.96*se"))
    add("3: medical", "interval contains the 2023 gap (1 = yes)", "still includes the old gap", 1, 0,
        int(g22.difference - 1.96 * g22.se <= g23.difference <= g22.difference + 1.96 * g22.se),
        "cross_survey_gaps.csv: 2023 difference inside the 2022 interval")
    dec = table("validation_medical_2026_09_28/derived/payer_decomposition.csv")
    contrib = {(r.survey, r.payer): r.excess_ratio_contribution for r in dec.itertuples()}
    medicare = contrib[("MCBS2023", "medicare")] - contrib[("MEPS2023", "medicare")]
    medicaid = contrib[("MCBS2023", "medicaid")] - contrib[("MEPS2023", "medicaid")]
    add("3: medical", "Medicare share of the 2023 gap, %", "85.1%", 85.1, .05, 100 * medicare / (medicare + medicaid),
        "validation_medical_2026_09_28/derived/payer_decomposition.csv: MCBS2023 minus MEPS2023 "
        "excess_ratio_contribution, Medicare over the sum")
    src = "diagnostics.csv public_common ratios, MCBS2023 {a} minus MEPS2023 {b}"
    for literal, value, dom_a, dom_b in [
            ("leaves .374 of the original .420 gap", .374, "uniform_age_sex", "uniform_age_sex"),
            ("leaves .374 of the original .420 gap", .420, "raw_65plus_medicare_ever", "raw_65plus_medicare_ever"),
            ("disclosure treatment leaves .411", .411, "raw_65plus_medicare_ever", "cms_tail_mean_analogue"),
            ("p99 caps leave .293", .293, "common_winsor_0.99", "common_winsor_0.99")]:
        add("3: medical", f"remaining gap, {dom_a} vs {dom_b}", literal, value, .0005,
            ratio("MCBS2023", dom_a).value - ratio("MEPS2023", dom_b).value, src.format(a=dom_a, b=dom_b))
    ret = table("validation_medical_2026_09_28/derived/retrospective_2024.csv")
    pooled_ = ret[ret.predictor.eq("train_2016_2023")].set_index(["group", "payer"]).absolute_error
    repeat = ret[ret.predictor.eq("last_year_2023")].set_index(["group", "payer"]).absolute_error
    better = pooled_ < repeat.reindex(pooled_.index)
    src = "validation_medical_2026_09_28/derived/retrospective_2024.csv"
    add("3: medical", "outcomes where pooling beats repeating 2023", "four of six correlated outcomes", 4, 0,
        int(better.sum()), src + ": count absolute_error(train_2016_2023) < absolute_error(last_year_2023)")
    worse = sorted(f"{grp}/{pay}" for (grp, pay), ok in better.items() if not ok)
    add("3: medical", "pooling worsens exactly hispanic medicaid and public_common (1 = yes)",
        "worsens the Hispanic aggregate public-payment ratio and Medicaid ratio", 1, 0,
        int(worse == ["hispanic/medicaid", "hispanic/public_common"]), src + f": worsened = {'; '.join(worse)}")
    mx = ret[ret.group.eq("mexican") & ret.payer.eq("public_common")].set_index("predictor")
    add("3: medical", "Mexican/all-donor public error, pooled", "−.074 (SE .137)", -.074, .0005,
        mx.loc["train_2016_2023", "error"], src + " (mexican, public_common, train_2016_2023): error")
    add("3: medical", "its SE", "−.074 (SE .137)", .137, .0005, mx.loc["train_2016_2023", "error_se"],
        src + " (mexican, public_common, train_2016_2023): error_se")
    add("3: medical", "Mexican/all-donor public error, repeat 2023", "versus −.202 repeating 2023", -.202, .0005,
        mx.loc["last_year_2023", "error"], src + " (mexican, public_common, last_year_2023): error")

    # Section 3: fiscal years.
    fs = table("validation_fiscal_years_2026_09_28/derived/scores.csv")
    prim = fs[fs.split.eq("primary")]
    mae = prim.groupby("arm").absolute_error_pp.mean()
    src = "validation_fiscal_years_2026_09_28/derived/scores.csv (primary, 2022→2024): "
    add("3: fiscal years", "declared outcomes", "eight declared, overlapping outcomes", 8, 0, prim.metric.nunique(),
        src + "distinct metric")
    add("3: fiscal years", "mean absolute share error, frozen", "from .495pp with frozen shares", .495, .0005,
        mae["frozen_share"], src + "mean absolute_error_pp, frozen_share")
    add("3: fiscal years", "mean absolute share error, composition", "to .415pp with updated", .415, .0005,
        mae["composition_transport"], src + "mean absolute_error_pp, composition_transport")
    p = prim.set_index(["metric", "arm"]).absolute_error_pp.unstack()
    worse = sorted(p.index[p.composition_transport > p.frozen_share])
    add("3: fiscal years", "composition worsens exactly SNAP, Social Security, SSI (1 = yes)",
        "SNAP, Social Security and SSI worsen", 1, 0, int(worse == ["snap_shared", "ss_shared", "ssi_shared"]),
        src + f"metrics where composition error exceeds frozen: {'; '.join(worse)}")
    irsd = table("validation_fiscal_years_2026_09_28/derived/irs_distribution.csv")
    tv = irsd.groupby("arm").error_pp.apply(lambda e: 0.5 * e.abs().sum())
    src = "validation_fiscal_years_2026_09_28/derived/irs_distribution.csv: "
    add("3: fiscal years", "IRS AGI bins", "across 19 AGI bins", 19, 0, irsd.agi_band.nunique(),
        src + "distinct agi_band")
    for literal, value, arm in [("gives 25.20pp total-variation error", 25.20, "frozen_cps_2022"),
                                ("versus 2.43pp simply freezing 2022 IRS shares", 2.43, "frozen_irs_2022"),
                                ("still errs by 24.06pp", 24.06, "same_year_cps_2023")]:
        add("3: fiscal years", f"total variation, {arm}", literal, value, .005, tv[arm],
            src + f"0.5*sum|error_pp|, {arm}")
    ps = one(fs, split="policy_stress", metric="federal_after_shared", arm="composition_transport")
    src = "validation_fiscal_years_2026_09_28/derived/scores.csv (policy_stress 2021→2024, federal_after_shared, composition_transport): "
    add("3: fiscal years", "2021 net-tax profile underprediction, pp", "underpredicts the target union's share by 4.77pp",
        4.77, .005, -ps.error_pp, src + "-error_pp")
    add("3: fiscal years", "same in conditional 2024 dollars, $bn", "or $90.86bn conditional", 90.86, .005,
        -ps.conditional_union_error_bn, src + "-conditional_union_error_bn")

    # Section 3: the bracket a022fc6 added to the tax paragraph from the held-out tax lane.
    tk = table("tax_key_heldout_2026_09_28/derived/scores.csv")
    src = "tax_key_heldout_2026_09_28/derived/scores.csv ({a}, 2023, {b}): total_variation_pp"
    for literal, value, arm, bins in [
            ("scores 23.5pp against IRS 2023", 23.5, "key_final_calibrated", "19 bins"),
            ("(8.4pp with $1M+ pooled", 8.4, "key_final_calibrated", "15 bins, $1M and up pooled"),
            ("against 18.5pp before CBO's gradient", 18.5, "key_before_cbo_gradient", "15 bins, $1M and up pooled")]:
        add("3: fiscal years, bracket a022fc6", f"total variation, {arm}, {bins}", literal, value, .05,
            one(tk, arm=arm, irs_target_year=2023, bins=bins).total_variation_pp, src.format(a=arm, b=bins))
    ch = table("tax_key_heldout_2026_09_28/derived/main_case_change.csv")
    src = "tax_key_heldout_2026_09_28/derived/main_case_change.csv (irs_2023_raked_with_cbo_groups, {e}): -cost_change_bn"
    for value, end in [(3.2, "low"), (3.1, "high")]:
        add("3: fiscal years, bracket a022fc6", f"group income tax raised, {end} end, $bn", "$3.2bn / $3.1bn", value,
            .05, -one(ch, target="irs_2023_raked_with_cbo_groups", band_end=end).cost_change_bn, src.format(e=end))

    # Section 3: Mariel.
    ms = table("validation_mariel_2026_09_28/derived/june30_scores.csv")
    ph = ms[ms.phase.eq("pre_holdout")].groupby(["weighting", "method"]).joint_normalized_rmse_pct
    if int(ph.nunique().max()) != 1:
        raise ValueError("[BLOCKED] joint score differs across outcome rows")
    jn = ph.first()
    src = "validation_mariel_2026_09_28/derived/june30_scores.csv (pre_holdout, {w}, {m}): joint_normalized_rmse_pct"
    for literal, value, w, m in [("39.75% and 26.65%", 39.75, "component_relative", "joint"),
                                 ("39.75% and 26.65%", 26.65, "common_revenue_unit", "joint"),
                                 ("versus 16.02%", 16.02, "component_relative", "donor_growth"),
                                 ("versus 16.02%", 16.02, "common_revenue_unit", "donor_growth")]:
        add("3: Mariel", f"joint normalized RMSE, {w} {m}", literal, value, .005, jn[(w, m)], src.format(w=w, m=m))
    rescued = [jn[(w, "drop_largest")] < jn[(w, "donor_growth")] for w in ("component_relative", "common_revenue_unit")]
    add("3: Mariel", "drop-largest fits that beat the baseline", "Deleting the largest donor does not rescue either fit",
        0, 0, sum(rescued), "june30_scores.csv: drop_largest < donor_growth, both weightings")
    script = (F / "validation_mariel_2026_09_28/joint_budget.py").read_text()
    scored = next(ast.literal_eval(n.value) for n in ast.parse(script).body if isinstance(n, ast.Assign)
                  and any(isinstance(t, ast.Name) and t.id == "SCORED" for t in n.targets))
    add("3: Mariel", "scored endpoints", "normalizes six endpoints", 6, 0, len(scored),
        "validation_mariel_2026_09_28/joint_budget.py: len(SCORED)")
    split = '("pre_holdout", list(range(1970, 1977)), list(range(1977, 1980)))' in script
    add("3: Mariel", "fit 1970–1976, predict 1977–1979 in code (1 = yes)", "On a 1970–1976 fit predicting 1977–1979",
        1, 0, int(split), "joint_budget.py: pre_holdout train and test ranges")

    OUT.mkdir(exist_ok=True)
    fields = list(rows[0])
    with (OUT / "memo_check.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: (f"{v:.10g}" if isinstance(v, float) else v) for k, v in row.items()})
    with (OUT / "memo_check.md").open("w") as stream:
        stream.write("| # | Section | Quantity | Memo | Lane value | Lane source | Status |\n"
                     "|---:|---|---|---|---:|---|---|\n")
        for i, row in enumerate(rows, 1):
            cells = [str(i), row["section"], row["quantity"], row["memo_literal"], f"{row['lane_value']:.6g}",
                     row["lane_source"] + (f"; {row['lane_definition']}" if row["lane_definition"] else ""),
                     row["status"]]
            stream.write("| " + " | ".join(c.replace("|", "/") for c in cells) + " |\n")
    construct_rows = construct_checks()
    with (OUT / "construct_checks.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=["check", "value", "source", "note"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(construct_rows)
    bad = [r for r in rows if r["status"] != "match"]
    print(f"memo numbers checked: {len(rows)}; mismatches: {len(bad)}")
    for r in bad:
        print(f"  MISMATCH {r['section']} | {r['quantity']}: memo {r['memo_value']} vs lane {r['lane_value']:.6g}")
    for r in construct_rows:
        print(f"  {r['check']}: {r['value']}")
    return 0


def construct_checks() -> list[dict]:
    out = []

    def add(check, value, source, note=""):
        out.append({"check": check, "value": value if isinstance(value, str) else f"{value:.10g}",
                    "source": source, "note": note})

    gss = json.loads((F / "validation_audit_2026_09_28/derived/gss_baseline.json").read_text())
    g = {(r["frame"], r["group"]): r for r in gss["results"]}
    a, b = g[("english_only", "all_origins_G4plus")], g[("all_available_languages", "all_origins_G4plus")]
    dup = all(a[k] == b[k] for k in ("model_tv_pp", "naive_tv_pp", "training_respondents", "heldout_respondents"))
    add("gss_g4plus_rows_identical_across_two_frames", str(dup), "gss_baseline.json",
        "english_only and all_available_languages G4+ rows are the same sample")
    distinct = {(round(r["model_tv_pp"], 12), round(r["naive_tv_pp"], 12), r["heldout_respondents"]): r
                for r in gss["results"]}
    add("gss_distinct_comparisons", len(distinct), "gss_baseline.json")
    add("gss_distinct_comparisons_model_wins", sum(r["model_tv_pp"] < r["naive_tv_pp"] for r in distinct.values()),
        "gss_baseline.json")
    snap = json.loads((F / "validation_audit_2026_09_28/derived/snap_loso.json").read_text())
    add("snap_json_embeds_git_head", str("head" in snap), "snap_loso.py line 113",
        "`git rev-parse HEAD` is written into the output, so any later commit changes the file")
    sc = pd.read_csv(F / "validation_schools_2026_09_28/derived/scores.csv")
    pre = sc[sc.panel.eq("prepandemic") & sc.outcome.eq("current") & sc.stratum.eq("all")
             & sc.fit_weight.eq(sc.score_weight)].set_index(["fit_weight", "arm"]).log_rmse
    for weight in ("district", "initial_pupils"):
        add(f"schools_best_arm_{weight}_weighted", pre[weight].idxmin(), "validation_schools scores.csv",
            f"log RMSE {pre[weight].min():.4f}")
    diag = pd.read_csv(F / "validation_medical_2026_09_28/derived/diagnostics.csv")
    base = diag[diag.domain.eq("raw_65plus_medicare_ever") & diag.payer.eq("public_common")
                & diag.statistic.isin(["hispanic", "white"])].set_index(["survey", "statistic"])
    for year in (2022, 2023):
        for grp in ("hispanic", "white"):
            meps, mcbs = base.loc[(f"MEPS{year}", grp)], base.loc[(f"MCBS{year}", grp)]
            add(f"medical_{year}_{grp}_records_meps_mcbs", f"{int(meps.n)} / {int(mcbs.n)}", "diagnostics.csv")
            add(f"medical_{year}_{grp}_weighted_population_ratio_meps_over_mcbs", meps.weighted_n / mcbs.weighted_n,
                "diagnostics.csv", "same eligibility code path in both years (analysis.py meps_frame, mcbs_frame)")
    annual = pd.read_csv(F / "validation_mariel_2026_09_28/derived/june30_annual.csv")
    scored = ["Total_Revenue", "Total_Expenditure", "Total_Current_Oper", "Total_Rev_Own_Sources",
              "Total_Fed_IG_Revenue", "Total_State_IG_Revenue"]
    ph = annual[annual.phase.eq("pre_holdout") & annual.outcome.isin(scored)]
    for (w, m), block in ph.groupby(["weighting", "method"]):
        train = block[block.year.between(1970, 1976)]
        scale = train.groupby("outcome").actual.mean()
        floor = .01 * train[train.outcome.eq("Total_Revenue")].actual.mean()
        scale = scale.clip(lower=floor)
        err = (train.counterfactual - train.actual) / train.outcome.map(scale)
        add(f"mariel_in_sample_joint_nrmse_1970_1976_{w}_{m}", float(np.sqrt(np.mean(err ** 2)) * 100),
            "june30_annual.csv", "same normalization as the holdout score, applied to the training years")
    panel = pd.read_csv(F / "causal_execution_2026_09_20/mariel/work/scm-june-only-panel.csv", dtype={"ID": str})
    train = panel[panel.fiscal_year.between(1970, 1976)]
    dade = train[train.ID.eq("105013001")].set_index("fiscal_year").sort_index()
    donors = train[train.donor_eligible.eq(1)]
    if len(dade) != 7 or donors.ID.nunique() != 28:
        raise ValueError("[BLOCKED] Mariel training panel changed")
    for col in ("Total_Fed_IG_Revenue", "Total_Expenditure", "Total_Revenue"):
        top = donors.groupby("fiscal_year")[col].max().reindex(dade.index)
        add(f"mariel_dade_above_every_donor_years_{col}", int((dade[col] > top).sum()),
            "causal_execution_2026_09_20/mariel/work/scm-june-only-panel.csv", "of 7 training years")
    bench = pd.read_csv(F / "external_benchmarks_2026_09_24/derived/benchmarks.csv")
    has_effect = bench.effect_low_bn.notna() | bench.effect_high_bn.notna()
    corr = bench.verdict.eq("corroborates")
    add("benchmarks_corroborates_via_effect_le_2bn", int((corr & has_effect).sum()),
        "external_benchmarks_2026_09_24/derived/benchmarks.csv", "benchmarks.py:31-32")
    add("benchmarks_corroborates_via_ratio_0p8_1p25", int((corr & ~has_effect).sum()),
        "external_benchmarks_2026_09_24/derived/benchmarks.csv", "benchmarks.py:33-35")
    return out


if __name__ == "__main__":
    sys.exit(main())
