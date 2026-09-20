# School peer checks, September 20, 2026

Executed baseline-adjusted classroom associations in the public ECLS-K 1998
cohort, plus observed Texas/California enrollment and staffing. These are evidence
tables, not an essay or a causal estimate of national immigration costs.

Results: [school peer evidence](../../../research/immigration-school-peer-checks-2026-09-20.md).
Inputs/definitions: [dataset card](DATASET_CARD.md), [source lock](sources.json).

## Reproduce

```sh
uv run python3 infra/immigration-fiscal/school_peer_checks_2026_09_20/extract.py
uv run python3 infra/immigration-fiscal/school_peer_checks_2026_09_20/analyze.py
uv run python3 infra/immigration-fiscal/school_peer_checks_2026_09_20/tabulate_growth.py
OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 uv run python3 infra/immigration-fiscal/school_peer_checks_2026_09_20/verify.py --data-dir infra/immigration-fiscal/school_peer_checks_2026_09_20/_cache --results infra/immigration-fiscal/school_peer_checks_2026_09_20/derived/results.json --source-lock infra/immigration-fiscal/school_peer_checks_2026_09_20/sources.json --out infra/immigration-fiscal/school_peer_checks_2026_09_20/derived/verification
```

The input directory must contain `childk8p.dat` and
`ECLSK_Kto8_child_STATA.dct`. Both are pinned by SHA-256. Raw bytes remain
read-only; extraction selects fewer than 100 fields into ignored `_cache/`.
The original run read the 1.59 GB file from the sibling IQ research project.
The default input now lives at `sources/reused-surveys/ecls_k` inside this project;
`--source-dir` can override it.
Readers acquire the public files through the NCES route in the dataset card;
restricted files and personally identifying linkages are not required.

Dependencies are in the project's locked environment. For this machine's cached
offline environment, prefix commands with `UV_CACHE_DIR=/private/tmp/codex-uv-cache`
and insert `--offline` after `uv run`.

`derived/results.json` and `models.csv` contain all 56 specifications: four
exposures × two outcomes × two periods × three adjustment sets, plus eight
future-exposure falsifications. The three adjustments use the same observations
within each exposure/outcome/period. Comparisons across different exposures can
have different samples. `derived/state_growth/` contains five descriptive CSVs.
State-table source values are explicit manual transcriptions in the generator,
with official URLs; their arithmetic is reproducible, not an automated data feed.

## Estimator and checks

Target: non-Hispanic-white children born in the 50 states/DC with English as
primary home language. Kindergarten models predict spring 1999 scores from fall
1998 classroom composition. Follow-up models predict spring 2000 scores from
spring 2000 classroom composition, controlling both previous test rounds.
The latter is a terminal-classroom association, not assigned exposure throughout
the year. Kindergarten/non-kindergarten round-4 questionnaires are harmonized;
retained kindergarten children are included when data permit.

Continuous baseline reading/math scores enter as separate cubic polynomials;
controls also include baseline age, sex, socioeconomic composite and assessment
interval. School fixed effects compare classrooms within a school. Neither
current class size, instructional staffing, peer achievement, grade progression
nor special-program placement is added as a primary adjustment: these can be
mechanisms or consequences of prior exposure. The classroom-size range 5–45 is
an explicit measurement restriction; exposure counts must not exceed enrollment.

Outcomes use the correct IRT scale fields, standardized separately in each wave
using that wave's positive child weights across all origins. These SDs are not
white-only norms. Analysis weights are BYCOMW0/Y2COMW0. Weighted school
demeaning and least squares use CR1 school-cluster covariance and normal 95%
intervals. These are model-based, per-comparison intervals; they do not implement
the complete NCES replicate/stratum/PSU survey variance or simultaneous inference.

Structural LEP-count zeros require a recorded no-other-home-language or no-LEP
gate. Other negative codes stay missing. Contradictory positive counts fail.
Fall-to-spring intervals outside (0,1) years and spring-to-next-spring intervals
outside (0,2) years are excluded and counted in `timing_qa`. These are broad
calendar validity checks, not trimming based on estimated effects.

The future-exposure checks predict already-realized spring 1999 scores from
spring 2000 composition, controlling fall 1998 scores and the matching fall
1998 exposure. Failure to reject does not establish random placement. Teacher
selection, moving, measurement error, differential missingness and schoolwide
effects remain unresolved.

Input hashes, exact row/ID counts, complete-record structure, rank and model
coverage checks fail loudly. `verify.py` independently reconstructs exposures,
samples and all 32 adjusted models using full school-dummy projections and FWL,
without importing the producer. Coefficients, CR1 SEs and sample counts matched;
maximum coefficient/SE disagreement was below 9e-16. A deliberately corrupted
coefficient was rejected under `python -O`. Raw unadjusted models and the eight
placebos are generated but not separately certified by that verifier.
The model does not identify Mexican classmates, descendant
effects, modern high-concentration schools or annual victim/fiscal dollars.
