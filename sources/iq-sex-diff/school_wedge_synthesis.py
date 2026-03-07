#!/usr/bin/env python3
"""Cross-dataset synthesis of late-school tested-math and school-linked surfaces."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
OUT_PATH = DATA_DIR / "school_wedge_synthesis" / "school_wedge_synthesis_summary.tsv"
OUT_FAMILY = DATA_DIR / "school_wedge_synthesis" / "school_wedge_family_summary.tsv"


def pick_hsls() -> list[dict[str, object]]:
    df = pd.read_csv(DATA_DIR / "hsls" / "hsls_wedge_models.tsv", sep="\t")
    picks = {
        ("x2_plus_x1", "tested_math"): "later standardized math, baseline-anchored",
        ("gpa_plus_scores", "gpa"): "transcript math GPA, anchored on baseline and later tested math",
        ("high_gpa_plus_scores_ladder", "high_course_gpa"): "highest-math-course GPA, anchored",
        ("precalc_plus", "track"): "reached precalc+",
    }
    rows = []
    for (model, family), note in picks.items():
        row = df.loc[df["model"].eq(model)].iloc[-1]
        rows.append(
            {
                "dataset": "HSLS",
                "surface_family": family,
                "surface_name": row["outcome"],
                "estimate_type": "beta_female_sd_or_share",
                "beta_female": row["beta_female"],
                "ci95_low": row["ci95_low"],
                "ci95_high": row["ci95_high"],
                "direction": "female" if row["beta_female"] > 0 else "male",
                "note": note,
                "source_file": "data/hsls/hsls_wedge_models.tsv",
            }
        )
    return rows


def pick_els() -> list[dict[str, object]]:
    df = pd.read_csv(DATA_DIR / "els" / "els_wedge_models.tsv", sep="\t")
    picks = {
        ("f1math_by_anchor_behavior", "tested_math"): "later standardized math, baseline-anchored",
        ("algebra2_plus_by_anchor_behavior", "track"): "reached algebra II+",
        ("trig_precalc_calc_by_anchor_behavior", "track_advanced"): "reached trig/precalc/calc",
        ("recognized_by_anchor_effort", "evaluation"): "recognized for good grades",
        ("math_teacher_honors_rec_by_anchor_effort", "recommendation"): "teacher AP/honors recommendation",
    }
    rows = []
    for (model, family), note in picks.items():
        row = df.loc[df["model"].eq(model)].iloc[-1]
        rows.append(
            {
                "dataset": "ELS",
                "surface_family": family,
                "surface_name": row["outcome"],
                "estimate_type": "beta_female_sd_or_share",
                "beta_female": row["beta_female"],
                "ci95_low": row["ci95_low"],
                "ci95_high": row["ci95_high"],
                "direction": "female" if row["beta_female"] > 0 else "male",
                "note": note,
                "source_file": "data/els/els_wedge_models.tsv",
            }
        )
    return rows


def pick_nels() -> list[dict[str, object]]:
    df = pd.read_csv(DATA_DIR / "nels" / "nels_wedge_models.tsv", sep="\t")
    picks = {
        ("f12_math_anchor", "tested_math_f1"): "first-follow-up math, baseline-anchored",
        ("f22_math_anchor", "tested_math_f2"): "second-follow-up math, baseline-anchored",
        ("transcript_math_units", "transcript_quantity"): "transcript math units",
        ("math_grade_quality", "grades"): "self-reported math grades",
        ("recognized_good_grades", "evaluation"): "recognized for good grades",
        ("academic_honors_rec", "recommendation"): "academic honors recommendation",
        ("academic_or_rigorous_program", "track"): "academic or rigorous program",
    }
    rows = []
    for (model, family), note in picks.items():
        row = df.loc[df["model"].eq(model)].iloc[-1]
        rows.append(
            {
                "dataset": "NELS",
                "surface_family": family,
                "surface_name": row["outcome"],
                "estimate_type": "beta_female_sd_or_share",
                "beta_female": row["beta_female"],
                "ci95_low": row["ci95_low"],
                "ci95_high": row["ci95_high"],
                "direction": "female" if row["beta_female"] > 0 else "male",
                "note": note,
                "source_file": "data/nels/nels_wedge_models.tsv",
            }
        )
    return rows


def pick_nlsy97() -> list[dict[str, object]]:
    tested = pd.read_csv(DATA_DIR / "nlsy" / "nlsy97_transcript_deep_models.tsv", sep="\t")
    transcript = pd.read_csv(DATA_DIR / "nlsy" / "nlsy97_transcript_deep_transcript_models.tsv", sep="\t")
    binary = pd.read_csv(DATA_DIR / "nlsy" / "nlsy97_transcript_deep_binary.tsv", sep="\t")
    rows = []

    tested_picks = [
        ("arithmetic_reasoning", "exposure_same_sample", "tested_math_applied", "applied/reasoning math surface"),
        ("math_knowledge", "exposure_same_sample", "tested_math_knowledge", "school-knowledge-heavy math surface"),
        ("quantitative", "exposure_same_sample", "tested_math_composite", "composite quantitative surface"),
    ]
    for outcome, model_name, family, note in tested_picks:
        row = tested.loc[tested["outcome"].eq(outcome) & tested["model_name"].eq(model_name)].iloc[0]
        rows.append(
            {
                "dataset": "NLSY97",
                "surface_family": family,
                "surface_name": outcome,
                "estimate_type": "beta_female_sd_or_share",
                "beta_female": row["female_beta_sd"],
                "ci95_low": row["ci_low"],
                "ci95_high": row["ci_high"],
                "direction": "female" if row["female_beta_sd"] > 0 else "male",
                "note": note,
                "source_file": "data/nlsy/nlsy97_transcript_deep_models.tsv",
            }
        )

    transcript_picks = [
        ("transcript_gpa_math_hstr", "outcome_on_piat_exposure", "gpa", "transcript math GPA"),
        ("transcript_total_math_hstr", "outcome_on_piat_exposure", "transcript_quantity", "total transcript math"),
        ("transcript_total_academic_math_hstr", "outcome_on_piat_exposure", "transcript_academic_quantity", "academic transcript math"),
    ]
    for outcome, model_name, family, note in transcript_picks:
        row = transcript.loc[transcript["outcome"].eq(outcome) & transcript["model_name"].eq(model_name)].iloc[0]
        rows.append(
            {
                "dataset": "NLSY97",
                "surface_family": family,
                "surface_name": outcome,
                "estimate_type": "beta_female_sd_or_share",
                "beta_female": row["female_beta_sd"],
                "ci95_low": row["ci_low"],
                "ci95_high": row["ci_high"],
                "direction": "female" if row["female_beta_sd"] > 0 else "male",
                "note": note,
                "source_file": "data/nlsy/nlsy97_transcript_deep_transcript_models.tsv",
            }
        )

    course_pick = binary.loc[binary["surface_name"].eq("selfreport_precalc_plus_1997")].iloc[0]
    rows.append(
        {
            "dataset": "NLSY97",
            "surface_family": "track_selfreport",
            "surface_name": "selfreport_precalc_plus_1997",
            "estimate_type": "female_minus_male_share",
            "beta_female": course_pick["female_minus_male_share"],
            "ci95_low": course_pick["ci_low"],
            "ci95_high": course_pick["ci_high"],
            "direction": "female" if course_pick["female_minus_male_share"] > 0 else "male",
            "note": "self-reported precalc+",
            "source_file": "data/nlsy/nlsy97_transcript_deep_binary.tsv",
        }
    )
    return rows


def main() -> None:
    rows = []
    rows.extend(pick_hsls())
    rows.extend(pick_els())
    rows.extend(pick_nels())
    rows.extend(pick_nlsy97())
    out = pd.DataFrame(rows)
    out["abs_beta"] = out["beta_female"].abs()
    out = out.sort_values(["dataset", "surface_family"]).reset_index(drop=True)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT_PATH, sep="\t", index=False)
    family = (
        out.groupby("surface_family", dropna=False)
        .agg(
            n=("beta_female", "size"),
            mean_beta=("beta_female", "mean"),
            median_beta=("beta_female", "median"),
            female_count=("direction", lambda s: int((s == "female").sum())),
            male_count=("direction", lambda s: int((s == "male").sum())),
        )
        .reset_index()
        .sort_values("mean_beta", ascending=False)
    )
    family.to_csv(OUT_FAMILY, sep="\t", index=False)


if __name__ == "__main__":
    main()
