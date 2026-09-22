# Pew 2017 Survey of U.S. Muslims — microdata cuts by nativity and origin

Reproduces the report-level figures quoted in
[`research/immigration-muslim-origins-funding-outcomes-2026-09-21.md`](../../../research/immigration-muslim-origins-funding-outcomes-2026-09-21.md)
§2 (ids B1–B11) from the respondent microdata, then cuts the same survey by nativity and
by birth region. Results and their caveats are in [`RESULT.md`](RESULT.md).

## Input

`sources/immigration-fiscal/data/external/pew/Pew-2017-US-Muslims.zip`, 6,121,578 bytes,
sha256 `1117f843…5926af`, registered in `sources/immigration-fiscal/data/MANIFEST.md`.
Unzip into the git-ignored `_cache/`; the script reads
`_cache/2017USMuslimPublicData - checked.sav` (1,001 respondents, 222 variables) with
`pyreadstat.read_sav(..., user_missing=True)`, the same route as
`../pew_outcomes_2026_09_20/analyze.py`. The archive also carries the codebook, the
questionnaire and the full report; the report's Appendix B is the methodology source.

```sh
cd infra/immigration-fiscal/pew_muslims_2017_2026_09_22
unzip -o -q ../../../sources/immigration-fiscal/data/external/pew/Pew-2017-US-Muslims.zip -d _cache/
```

## Run

```sh
cd /Users/alien/Projects/immigration-research
UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --offline --no-project --with pyreadstat \
  python3 -m pytest infra/immigration-fiscal/pew_muslims_2017_2026_09_22/ -q
UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --offline --no-project --with pyreadstat \
  python3 infra/immigration-fiscal/pew_muslims_2017_2026_09_22/analysis.py
```

## Method

**Weights.** `weight` for every point estimate, as its own variable label instructs. That
is Pew's trimmed weight (Appendix B winsorizes at the 99.8th percentile); the untrimmed
screener weight, used only for the population total, is not in this file.

**Standard errors.** The file ships 100 jackknife replicate weights, `rpl001`–`rpl100`,
and Appendix B says analyses "used a repeated replication technique, specifically
jackknife repeated replication (JRR), to calculate the standard errors." Every replicate
weight is exactly 0, 1× or 2× the main weight (about five respondents zeroed per
replicate, each respondent zeroed at most once, 501 zeroed at least once), which is a
delete-a-group jackknife with the deleted unit's mate doubled. The variance is therefore
the plain sum of squared replicate deviations, multiplier 1, which is Stata's default for
`jkrweight()` when no `multiplier()` is given. Differences between groups use the
replicate-by-replicate difference, so the covariance between the two cells is carried.

`report_reproduction.csv` also prints the simple-random-sample SE and the implied design
effect, which runs 1.7 to 8.8 across the published rows. Pew's own study-level average is
about 3.5, back-solved from the published ±5.8 point margin of error at p = 0.5 on
n = 1,001. Treating this survey as a simple random sample understates its sampling error
by a factor of roughly 1.3 to 3.

**Codes.** No numeric code is written into the script. `Book.code(variable, label_text)`
resolves each code from its exact codebook value label at run time and fails if the label
is missing or ambiguous, so a relabelled release breaks the build instead of silently
recoding. Every variable touched is written to `derived/audit.json` with its variable
label and its full value-label map.

**Groups.** Nativity from `respondent_birthregion2`. Foreign-born cells are the
respondent's own birth region. U.S.-born cells use the parents: the father's region
identifies the group, the mother's is used when the father is U.S. born or unknown, so
each U.S.-born respondent lands in exactly one cell (a test asserts the partition).
Cells with an unweighted base under 50 carry `small_cell_flag = n<50`.

## Outputs

| File | Contents |
|---|---|
| `derived/report_reproduction.csv` | published figure vs microdata, JRR and SRS SEs, design effect, base n |
| `derived/cuts_by_nativity.csv` | 43 outcomes × {all, U.S. born, foreign born} plus the foreign-minus-U.S.-born difference |
| `derived/cuts_by_origin.csv` | the same outcomes by birth region and by parents' birth region, plus four pre-specified contrasts |
| `derived/audit.json` | source hashes, weight and replicate diagnostics, every variable with its labels, items searched for and absent |

## Gates

| Gate | Check | Where |
|---|---|---|
| G1 | zip sha256 and byte length match the manifest | `load()`, `test_g1_source_bytes` |
| G2 | 1,001 rows, 222 columns, weight finite and positive, 100 replicates | `load()`, `test_g2_shape_and_weights` |
| G3 | every published B-row within 1 percentage point | `test_g3_published_rows_reproduce` |
| G4 | every variable used appears in `audit.json` with its label | `test_outputs_and_audit_written` |

Five further tests guard the method rather than the result: the replicate weights are
jackknife-shaped, a bad label raises, band percentages sum to their base, the origin cells
partition their universe, and the JRR SE exceeds the SRS SE on every published row.

## Scope

Self-identified Muslim adults interviewed by telephone between 23 January and 2 May 2017,
noninstitutionalized only. Income is banded and pre-tax, from 2016. Birthplace is a region,
not a country, so "South Asia" and "MENA" cannot be resolved to Pakistan, Bangladesh, Iran
or Egypt the way the ACS-based rows in the memo's §1 can. Children ever born is top-coded
at "four or more", so the mean is a floor. There is no public-assistance, welfare or
health-coverage item anywhere in the 222 variables.
