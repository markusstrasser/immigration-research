from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
OUTDIR = DATA / "school_wedge_mechanism"


def ensure_outdir() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)


def load_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t")


def build_shift_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    hsls = load_tsv(DATA / "hsls" / "hsls_wedge_refinement_models.tsv")
    hsls_family = {
        "X2TXMTSCOR_z": "tested_math",
        "X3TGPAMAT_z": "evaluation_gpa",
        "X3TGPAHIMTH_z": "evaluation_gpa",
        "precalc_plus": "track",
    }
    for outcome, family in hsls_family.items():
        base = hsls[(hsls["outcome"] == outcome) & (hsls["stage"] == "same_sample_base")].iloc[0]
        adj = hsls[(hsls["outcome"] == outcome) & (hsls["stage"] == "adjusted")].iloc[0]
        rows.append(
            {
                "dataset": "HSLS",
                "family": family,
                "outcome": outcome,
                "mechanism_block": "behavior_identity_teacher_climate",
                "base_female_beta": base["beta_female"],
                "adjusted_female_beta": adj["beta_female"],
                "delta_adjusted_minus_base": adj["beta_female"] - base["beta_female"],
                "base_n": int(base["n"]),
                "adjusted_n": int(adj["n"]),
            }
        )

    els = load_tsv(DATA / "els" / "els_wedge_models.tsv")
    els_family = {
        "F1TXMSTD_z": "tested_math",
        "algebra2_plus": "track",
        "trig_precalc_calc": "track",
        "recognized_good_grades": "evaluation",
        "math_teacher_honors_rec": "evaluation",
        "F1MATHSE_z": "identity",
    }
    for outcome, family in els_family.items():
        base = els[(els["outcome"] == outcome) & (els["stage"] == "same_sample_base")].iloc[0]
        adj = els[(els["outcome"] == outcome) & (els["stage"] == "adjusted")].iloc[0]
        rows.append(
            {
                "dataset": "ELS",
                "family": family,
                "outcome": outcome,
                "mechanism_block": "baseline_math_reading_plus_behavior",
                "base_female_beta": base["beta_female"],
                "adjusted_female_beta": adj["beta_female"],
                "delta_adjusted_minus_base": adj["beta_female"] - base["beta_female"],
                "base_n": int(base["n"]),
                "adjusted_n": int(adj["n"]),
            }
        )

    nels = load_tsv(DATA / "nels" / "nels_wedge_models.tsv")
    nels_family = {
        "F12XMSTD_z": "tested_math",
        "F22XMSTD_z": "tested_math",
        "F2RHMA_C_z": "transcript_quantity",
        "math_grade_quality_z": "evaluation_grade",
        "recognized_good_grades": "evaluation",
        "academic_honors_rec": "evaluation",
        "academic_or_rigorous_program": "track",
        "rigorous_academic_program": "track",
    }
    for outcome, family in nels_family.items():
        base = nels[(nels["outcome"] == outcome) & (nels["stage"] == "same_sample_base")].iloc[0]
        adj = nels[(nels["outcome"] == outcome) & (nels["stage"] == "adjusted_anchor")].iloc[0]
        rows.append(
            {
                "dataset": "NELS",
                "family": family,
                "outcome": outcome,
                "mechanism_block": "baseline_math_reading_anchor",
                "base_female_beta": base["beta_female"],
                "adjusted_female_beta": adj["beta_female"],
                "delta_adjusted_minus_base": adj["beta_female"] - base["beta_female"],
                "base_n": int(base["n"]),
                "adjusted_n": int(adj["n"]),
            }
        )

    nlsy = load_tsv(DATA / "nlsy" / "nlsy97_behavior_block_models.tsv")
    nlsy_family = {
        "math_knowledge_z": "school_knowledge",
        "arithmetic_reasoning_z": "tested_math",
        "transcript_gpa_math_hstr_z": "evaluation_gpa",
    }
    for outcome, family in nlsy_family.items():
        base = nlsy[(nlsy["outcome"] == outcome) & (nlsy["model_name"] == "base_context")].iloc[0]
        adj = nlsy[
            (nlsy["outcome"] == outcome)
            & (nlsy["model_name"] == "plus_behavior_climate")
        ].iloc[0]
        rows.append(
            {
                "dataset": "NLSY97",
                "family": family,
                "outcome": outcome,
                "mechanism_block": "behavior_plus_climate",
                "base_female_beta": base["female_beta"],
                "adjusted_female_beta": adj["female_beta"],
                "delta_adjusted_minus_base": adj["female_beta"] - base["female_beta"],
                "base_n": int(base["n_obs"]),
                "adjusted_n": int(adj["n_obs"]),
            }
        )

    return rows


def build_family_summary(shift_df: pd.DataFrame) -> pd.DataFrame:
    return (
        shift_df.groupby(["family", "mechanism_block"], dropna=False)
        .agg(
            n_rows=("outcome", "size"),
            mean_base_beta=("base_female_beta", "mean"),
            mean_adjusted_beta=("adjusted_female_beta", "mean"),
            mean_delta=("delta_adjusted_minus_base", "mean"),
            min_delta=("delta_adjusted_minus_base", "min"),
            max_delta=("delta_adjusted_minus_base", "max"),
        )
        .reset_index()
        .sort_values(["family", "mechanism_block"])
    )


def build_course_summary() -> pd.DataFrame:
    course = load_tsv(DATA / "nlsy" / "nlsy97_course_causal_models.tsv")
    keep = course["model_name"].isin(["observed_confounders_wls", "offer_stress_wls"])
    course = course.loc[keep].copy()
    return (
        course.groupby(["outcome", "treatment", "model_name"], dropna=False)
        .agg(
            n_rows=("n_obs", "size"),
            mean_treatment_beta=("treatment_beta_sd", "mean"),
            min_treatment_beta=("treatment_beta_sd", "min"),
            max_treatment_beta=("treatment_beta_sd", "max"),
            mean_female_residual=("female_beta_sd", "mean"),
            min_female_residual=("female_beta_sd", "min"),
            max_female_residual=("female_beta_sd", "max"),
            min_p_value=("treatment_p_value", "min"),
        )
        .reset_index()
        .sort_values(["outcome", "treatment", "model_name"])
    )


def build_notes(shift_df: pd.DataFrame, course_df: pd.DataFrame) -> pd.DataFrame:
    notes: list[dict[str, object]] = []
    for row in shift_df.itertuples(index=False):
        delta = float(row.delta_adjusted_minus_base)
        if row.family in {"evaluation", "evaluation_gpa", "evaluation_grade"} and delta >= -0.01:
            read = "evaluation_family_survives_or_strengthens"
        elif row.family == "tested_math" and delta > 0.01:
            read = "tested_math_compresses_toward_zero"
        elif row.family == "track" and delta >= 0:
            read = "track_signal_survives_or_strengthens"
        elif row.family == "transcript_quantity" and abs(delta) < 0.02:
            read = "quantity_stays_near_neutral"
        elif row.family == "school_knowledge" and abs(delta) < 0.01:
            read = "school_knowledge_residual_unchanged"
        else:
            read = "mixed"
        notes.append(
            {
                "dataset": row.dataset,
                "family": row.family,
                "outcome": row.outcome,
                "interpretation": read,
            }
        )

    for row in course_df.itertuples(index=False):
        if float(row.mean_treatment_beta) <= 0 and float(row.mean_female_residual) > 0.1:
            read = "course_exposure_not_explaining_female_residual"
        else:
            read = "mixed"
        notes.append(
            {
                "dataset": "NLSY97",
                "family": "track_selfreport",
                "outcome": f"{row.outcome}:{row.treatment}:{row.model_name}",
                "interpretation": read,
            }
        )

    return pd.DataFrame(notes)


def main() -> None:
    ensure_outdir()
    shift_df = pd.DataFrame(build_shift_rows()).sort_values(["dataset", "family", "outcome"])
    family_df = build_family_summary(shift_df)
    course_df = build_course_summary()
    notes_df = build_notes(shift_df, course_df)

    shift_df.to_csv(OUTDIR / "school_wedge_mechanism_shift.tsv", sep="\t", index=False)
    family_df.to_csv(OUTDIR / "school_wedge_mechanism_family_summary.tsv", sep="\t", index=False)
    course_df.to_csv(OUTDIR / "school_wedge_course_mechanism_summary.tsv", sep="\t", index=False)
    notes_df.to_csv(OUTDIR / "school_wedge_mechanism_notes.tsv", sep="\t", index=False)


if __name__ == "__main__":
    main()
