# IQ Sex Differences - Matrix Experiment Runbook

**Date:** 2026-03-07
**Purpose:** deployment checklist for the local `OMIB` matrix pilot.

## Use This If

You want to actually run the first randomized timing study rather than just discuss it.

## Minimal deployment

1. Use `Form A` first.
2. Randomize participants into:
   - `tight`
   - `generous`
3. Use the prebuilt HTML fragments in:
   - [pilot_web](/Users/alien/Projects/research/sources/iq-sex-diff/data/matrix_open/omib/pilot_web#L1)
4. Store raw response strings and condition labels.

## Minimum participant fields

Required:

1. `participant_id`
2. `item_id`
3. `response_code`
4. `sex_recorded`
5. `time_condition`

Strongly recommended:

1. `age_years`
2. `country`
3. `education_level`
4. `device_type`
5. `start_ts`
6. `end_ts`

Template:

- [omib_response_schema.tsv](/Users/alien/Projects/research/sources/iq-sex-diff/data/matrix_open/omib/omib_response_schema.tsv#L1)

## Scoring

1. export raw item responses to TSV
2. run:

```bash
cd /Users/alien/Projects/research/sources/iq-sex-diff
uv run --with pandas --with openpyxl python3 score_omib_pilot.py \
  --responses data/matrix_open/omib/YOUR_RESPONSES.tsv \
  --out data/matrix_open/omib/YOUR_RESPONSES_SCORED.tsv
```

## First analysis

Do not overcomplicate the first read.

1. mean accuracy by `sex_recorded x time_condition`
2. completion count by `sex_recorded x time_condition`
3. item-level gap by `difficulty_b`
4. item-level gap by `rotation`

Only after that fit the regression in [iq-sex-differences-matrix-experiment-protocol.md](/Users/alien/Projects/research/research/iq-sex-differences-matrix-experiment-protocol.md#L1).

## Stop rules

Stop and fix design before interpreting anything if:

1. one condition has clear device/browser failures
2. one sex is massively imbalanced across time conditions
3. item logs are missing
4. completion collapses in the tight condition across everyone

That would turn the result into a deployment artifact, not a matrix result. [INFERENCE]
