# IIMMLA raw family-history sensitivity — September 17, 2026

The generator tests whether the earlier source-coded G3/G4+ outcome differences survive explicit respondent/parent/grandparent questions and raw outcome handling. It does not estimate national generational trajectories. [Findings](../../../research/immigration-all-age-and-lineage-findings-2026-09-17.md).

```sh
uv run --no-project python3 infra/immigration-fiscal/iimmla_sensitivity_2026_09_17/analyze.py
```

Requires pandas/NumPy. Defaults to the held read-only `../iimmla_2026_09_17/raw/ICPSR_22627/DS0001/22627-0001-Data.tsv`; writes only this lane's ignored `derived/`. Optional `--source` and `--output-dir` permit reproduction; output must remain in this lane's derived directory or `/private/tmp`.

## Source and definitions

[ICPSR22627](https://www.icpsr.umich.edu/web/ICPSR/studies/22627), IIMMLA2004, five-county Los Angeles, respondent ages20–40. The public TSV has4,655 records and SHA256 `1d5fc8fbb1b2e52c7b5dc6c0e1c4b24d151066a7c19d35d3e4d5cc86ca360424`. No weight variable was found in the inspected release. This is an unweighted local sample with survey selection/nonresponse, not a national probability estimate. The supplied-generation rows are retained as anchors rather than overwritten.

| Construct | Raw rule |
|---|---|
| Respondent US-born | `QS7=1/2`; no conflicting foreign-country `QS8` |
| Both parents US-born | `QS10=1`; no contradictory `QS11/QS12AM/QS12BF` |
| Strict generic G3 | Above + `Q152A=1`; four binary grandparent foreign-birth flags with at least one yes; unknown/refusal flags zero; no nativity/country contradiction |
| Strict generic G4+ | Own/parents US-born + `Q152A=2`; no positive foreign-grandparent flag/country; structural skips following definite no are valid |
| Confirmed Mexico-born grandparent | A matched `Q152B_i=1` and `Q152C_i=43`; never inferred from self-identification |
| Mexican self-ID | Supplied `ETHNOS10=1`, kept separate from family history |
| BA+, no high school | Documented `EDUCRED5>=4`, `EDUCRED5=0` |
| Ever arrested | Family gate `Q201` and respondent/other/both `Q202` |
| Ever incarcerated | `Q203A/Q203B`, includes reform school, detention, jail or prison; not adult imprisonment alone |

Country62 means US,71 refused,72 unknown,−9 structural skip;1–70 except62 includes foreign countries and residual foreign-region categories. Unknown foreign-country details do not defeat an otherwise definite foreign-birth report, but they cannot confirm Mexican birthplace. A stricter complete-country arm is exported. Raw event unknown/refused/contradictory paths remain missing; no-family-event with proper structural skip means zero. Supplied outcomes are exported alongside raw reconstructions.

No symmetric exact-Mexican-lineage G3/G4 comparison is possible: confirmed Mexico-born grandparents can define G3, while G4+ with all US-born grandparents lacks great-grandparent country fields. Nor do the parent questions by themselves prove biological relationships. “One Mexico-born grandparent” is a migration-history observation, not a genetic fraction.

## Checks and outputs

Source G3/G4+ counts212/189 reproduce; explicit own/parent/grandparent consistency yields196/187. Restricting to valid raw education/arrest/incarceration endpoints yields192/182. Every known reconstructed arrest/incarceration answer agrees with the supplied corresponding binary across all4,655 records. Unknown raw paths retain some source-derived zeros/ones; this lane does not assume those undocumented source derivations are mistakes.

`rates.csv` preserves endpoint-specific and common-sample rates. `contrasts.csv` records contrasts with the asymmetric Mexican-grandparent comparison explicitly named. `source_to_strict_counts.csv`, `composition.csv`, `subgroup_rates.csv` expose exclusions and age/sex heterogeneity. `audit.json` includes source/script hashes, counts, definitions and endpoint comparisons. No design-based national confidence intervals are claimed for these unweighted quota-sample contrasts.

Independent read-only review checked the raw questions against the held questionnaire/codebook, independently reconstructed the rows and events, verified the juvenile-inclusive outcome and structural skips, and reproduced the source hash. No consequential coding defect was found. [Review disposition](../../../notes/immigration-construct-review-2026-09-17.md).
