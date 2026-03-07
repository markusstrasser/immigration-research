"""
Descriptive analysis of timing channels in WAIS subtests.

Question:
Do timed / speed-bonus spatial-fluid subtests reduce the observed male advantage
relative to less speeded reasoning tasks, as we would expect if speed were acting
mainly as a female-favoring equalizer inside the spatial battery?

Data source:
- Effect sizes already extracted in this repo from Dutch WAIS-III, Italian WAIS-IV,
  and German WAIS-IV standardization papers.

Classification notes:
- Block Design: timed, includes time bonus. [Pearson WAIS-IV Q&A]
- Visual Puzzles: strict time limits. [Pearson WAIS-IV Q&A]
- Figure Weights: strict time limits. [Pearson WAIS-IV Q&A]
- Matrix Reasoning: 30-second guideline, but not strict; delayed correct responses
  may be allowed. [Pearson WAIS-IV Q&A]

Convention:
- Negative d = male advantage
- Positive d = female advantage

This is descriptive, not a formal meta-analysis. Subtests within studies are
correlated, and raw item-level data are not available here.
"""

from statistics import mean


studies = {
    "Dutch WAIS-III": {
        "citation": "van der Sluis et al. 2006",
        "matrix_reasoning": -0.20,
        "speeded_spatial_fluid": {
            "Block Design": -0.26,
        },
        "clerical_processing_speed": {
            "Digit-Symbol": 0.71,
            "Copying": -0.19,
        },
    },
    "Italian WAIS-IV": {
        "citation": "Pezzuti et al. 2020",
        "matrix_reasoning": -0.19,
        "speeded_spatial_fluid": {
            "Block Design": -0.29,
            "Visual Puzzles": -0.30,
            "Figure Weights": -0.32,
        },
        "clerical_processing_speed": {
            "Symbol Search": -0.09,
            "Coding": 0.02,
            "Cancellation": 0.01,
        },
    },
    "German WAIS-IV": {
        "citation": "Daseking et al. 2017",
        "matrix_reasoning": -0.157,
        "speeded_spatial_fluid": {
            "Block Design": -0.180,
            "Visual Puzzles": -0.315,
            "Figure Weights": -0.293,
        },
        "clerical_processing_speed": {
            "Symbol Search": 0.108,
            "Coding": 0.285,
            "Cancellation": 0.070,
        },
        "indices": {
            "FSIQ_diff_iq": 3.16,  # male minus female
            "GAI_diff_iq": 4.07,   # male minus female
        },
    },
}


def fmt(x: float) -> str:
    return f"{x:+.3f}"


def main() -> None:
    print("=" * 84)
    print("TIMING CHANNEL ANALYSIS: WAIS SUBTESTS")
    print("Negative d = male advantage | Positive d = female advantage")
    print("=" * 84)
    print()

    overall_matrix = []
    overall_speeded = []
    overall_ps = []

    for study, data in studies.items():
        mr = data["matrix_reasoning"]
        speeded_mean = mean(data["speeded_spatial_fluid"].values())
        ps_mean = mean(data["clerical_processing_speed"].values())
        contrast = speeded_mean - mr

        overall_matrix.append(mr)
        overall_speeded.append(speeded_mean)
        overall_ps.append(ps_mean)

        print(study)
        print(f"  Matrix Reasoning (less speeded)        {fmt(mr)}")
        print(f"  Mean speeded spatial/fluid tasks       {fmt(speeded_mean)}")
        print(f"  Contrast: speeded minus matrix         {fmt(contrast)}")
        print(f"  Mean clerical processing-speed tasks   {fmt(ps_mean)}")
        if "indices" in data:
            idx = data["indices"]
            print(
                "  German composite check: "
                f"GAI male advantage {idx['GAI_diff_iq']:.2f} IQ > "
                f"FSIQ male advantage {idx['FSIQ_diff_iq']:.2f} IQ"
            )
        print()

    print("-" * 84)
    print("Cross-study averages")
    print(f"  Matrix Reasoning mean                 {fmt(mean(overall_matrix))}")
    print(f"  Speeded spatial/fluid mean            {fmt(mean(overall_speeded))}")
    print(f"  Clerical processing-speed mean        {fmt(mean(overall_ps))}")
    print()
    print("Interpretation:")
    print(
        "  1. If timed scoring in spatial/fluid tasks mainly acted as a "
        "female-favoring equalizer, speeded spatial/fluid tasks should be less "
        "male-leaning than Matrix Reasoning."
    )
    print(
        "  2. In all three standardization samples here, the opposite pattern "
        "appears: speeded spatial/fluid tasks are more male-leaning than "
        "Matrix Reasoning."
    )
    print(
        "  3. Female advantages are concentrated in clerical processing-speed "
        "tasks such as Coding and Symbol Search, not in speeded spatial tasks "
        "as a class."
    )


if __name__ == "__main__":
    main()
