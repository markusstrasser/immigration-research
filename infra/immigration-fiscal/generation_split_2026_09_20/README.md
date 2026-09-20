# Observed G3/G4+ separation

Reproduce the partial CPS2025 split of the existing all-age Mexican-origin
civilian-household account and separate historical Pew/NLSY97 descriptive tables.
No fiscal reallocation, ancestry imputation, or exact G4/G5 classification.

```sh
UV_CACHE_DIR=/private/tmp/codex-uv-cache uv run python3 infra/immigration-fiscal/generation_split_2026_09_20/analyze_cps.py
UV_CACHE_DIR=/private/tmp/codex-uv-cache uv run python3 infra/immigration-fiscal/generation_split_2026_09_20/analyze_historical.py
UV_CACHE_DIR=/private/tmp/codex-uv-cache uv run python3 infra/immigration-fiscal/generation_split_2026_09_20/verify.py
```

Requires numpy, pandas and pyreadstat in the existing local environment. Inputs
are read-only; acquire restricted survey files through their original providers.
`derived/` is ignored. There are no changes to existing public APIs.

## Inputs and sources

- CPS2025 person file and 161 weights: the existing Census archive at
  `~/research-data/immigration-fiscal/data/external/stage3/census/cps_asec_2025/asecpub25csv.zip`.
  The generator verifies its SHA-256 against the existing fiscal ledger's source
  lock. [Census download](https://www2.census.gov/programs-surveys/cps/datasets/2025/march/asecpub25csv.zip),
  [technical documentation](https://www2.census.gov/programs-surveys/cps/techdocs/cpsmar25.pdf).
- Current account population anchor:
  `../full_account_receipts_2026_09_20/derived/allocation_keys.csv`.
- Pew2015 identifying-Hispanic survey and 2015–16 ancestry-screened nonidentifier
  survey: two SAVs and release metadata in
  `../new_datasets_2026_09_17/derived/pew/`. Exact paths and SHA-256 hashes are
  written to `derived/historical/audit.json`.
  [Pew methodology](https://www.pewresearch.org/race-and-ethnicity/2017/12/20/methodology-hispanic-identity/).
- NLSY97: `../new_datasets_2026_09_17/derived/nlsy_family/family_analysis_rows.csv`,
  created by that lane's audited parent linkage. The new audit records its hash.
  See [linkage evidence](../../../research/immigration-nlsy97-parent-linkage-2026-09-17.md)
  for raw inputs, extraction and limits.

## Classifications and limitations

CPS keeps the canonical G1/G2/G3+ masks and civilian restriction. It links parent
line numbers inside the same household, uses biological parents only, and reads
their parents' countries of birth. Reported Mexico-born grandparent evidence
identifies G3 even when the other branch is unobserved. G4+ requires all four
grandparents explicitly born in US areas. Contradictory linked parent birthplaces,
missing branches and other unresolved histories stay unresolved. G4+ rests on
the person's Mexican identification; no Mexican-born great-grandparent is observed.
The unallocated arm withholds classifications depending on changed/imputed
birthplace, identity, or parent-link fields; it does not reweight retained cases.

All-age counts include children and all education levels. CPS household respondents
can report other members' origin, so "self-ID" is the canonical variable label,
not a guarantee that each person answered individually. The main partial split
retains Census edits. Sampling SE uses 4/160 successive-difference replication;
all 132 negative replicate-weight cells are retained, as required by the Census
documentation (PDF page 376). Classification, coverage and co-residence selection
are not included in those SEs. Missing adults are not assigned the child split.

Pew restricts origin to `q3_combo==1`; mixed-origin code9 loses components and is
excluded. These are generic immigrant generations among Mexican-origin adults;
grandparent country is unavailable. Puerto Rico counts as migrant origin in the
Pew convention, whereas CPS includes US areas as native. The pooled historical
sensitivity normalizes the full surveys before applying 37.8/4.9 million
benchmarks and then selecting Mexican origin. It is not an observed 2025 headcount.
NLSY is the survey-retained 1980–84 birth cohort resident in the US in 1997,
using round21 weights and Mexican/Chicano identification. Unknowns remain in
every denominator. No survey-design CI is claimed for these historical tables.

## Checks and outputs

`cps_generation_split.csv`: full and partial classifications by all ages,
under18 and 18+, with counts, SDR SEs and shares of the age-specific target.
`audit.json`: input hash, 142125 rows and exact 40896574.15235156 target reconciliation.
Historical CSVs: source-specific/pooled Pew generation shares, excluded origin
categories, and a separate NLSY97 cohort distribution.

Generators check disjoint/exhaustive masks, valid links, finite weights, full
weight scale and population conservation. `verify.py` tests missing grandparents,
one known Mexican grandparent, step-parent exclusion, imputation, conflicting
parent records, duplicate parent slots, and valid negative replicate weights.
The independent respondent-wise Pew classifier matches all 1901 records.

Findings: [fourth-generation scope and executed split](../../../research/immigration-fourth-generation-scope-2026-09-20.md).

## Additional recovery checks

```sh
UV_CACHE_DIR=/private/tmp/codex-uv-cache uv run python3 infra/immigration-fiscal/generation_split_2026_09_20/analyze_gss.py
UV_CACHE_DIR=/private/tmp/codex-uv-cache uv run python3 infra/immigration-fiscal/generation_split_2026_09_20/probe_adjacent_years.py
```

These standalone probes add evidence; they do not apply candidate classifications
to `cps_generation_split.csv` or change the fiscal account. No existing public
interface changes. Outputs go to ignored `derived/recovery/`; the adjacent-year
script also runs `audit_unresolved.py` to produce the missing-history partition.

- GSS input: `../attitudes_gen_2026_09_16/raw/GSS_stata/gss7224_r3a.dta`,
  SHA-256 `a7622e03d9130e25968943b6f022f44dc0087baf0aa6b5cef150871152827344`.
  [NORC source](https://gss.norc.org/get-the-data.html). Local 2024 R3a codebook,
  printed p.40, recommends WTSSNRPS when available. The recent subgroup table
  gives WTSSNRPS and WTSSPS; the wider historical diagnostic uses WTSSPS only.
  `HISPANIC=2`, `BORN=1`, `PARBORN=0` defines the recent subgroup. `GRANBORN=0`
  identifies four US-born grandparents; 1–4 establishes a foreign grandparent,
  without country. Unknown grandparents and unknown ages remain visible.
  Pooled survey weights are not normalized to equal year mass or standardized
  to CPS age composition. No design-based intervals or current-year imputation.
- CPS2024 input: `../same_year_tax_2026_09_20/_cache/asecpub24csv.zip`.
  [Census download](https://www2.census.gov/programs-surveys/cps/datasets/2024/march/asecpub24csv.zip).
- CPS2026 input: `../ledger_asec2026_2026_09_16/_cache/asecpub26csv.zip`.
  [Census download](https://www2.census.gov/programs-surveys/cps/datasets/2026/march/asecpub26csv.zip).
  Both archive hashes are pinned in the script and recorded with the 2025 hash
  in the audit manifest. `PERIDNUM` is a string with unique, nonmissing values.

Adjacent-wave candidates retain the current 2025 sample and weights. Own and
parental birthplace, sex, citizenship and Mexican identification must agree;
age must change by 0–2 years in the expected direction. The existing biological
parent classifier runs on each adjacent wave. Shared parents' own and parental
birthplaces must agree. Current inconsistent parent histories remain excluded.
The stricter arm also excludes any currently observed biological parent absent
from the other wave. Both arms remain candidates: edited-field adjudication,
complementary partial-branch combination, and all monthly interviews are unrun.
The union removes cross-wave G3/G4 conflicts and uses each target person once.

Generated outputs:

- `gss_generation_subgroup_20260920.csv`: recent G3+/adult denominator, two
  weighting methods, age bands, known/unknown counts and shares.
- `gss_generation_probe_20260920.csv`: wider historical origin-definition diagnostic.
- `generation_unresolved_reasons_20260920.csv`: exhaustive reasons plus explicitly
  overlapping diagnostics; do not add overlapping rows to the partition.
- `cps_adjacent_generation_candidates_20260920.csv`: each linkage filter and
  candidate union, all-age/child/adult counts and conditional sampling SEs.
- JSON manifests: raw hashes, labels, counts and material limitations.

The annual-wave candidate yield does not bound the unexecuted monthly or
complementary-branch routes. Public CPS contains no name fields. A surname
ethnicity classifier would not supply the missing grandparents' birthplaces.
