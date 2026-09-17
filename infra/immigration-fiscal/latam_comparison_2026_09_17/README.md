# Latin American origin economic comparisons

Specification set before computing this run's country outcomes, 2026-09-17.

Use the five public CPS ASEC releases 2022–2026 (income years 2021–2025).
Primary population: civilian household adults 25–54. Show men/women and
ages 25–64 as sensitivities, not independent replications. Benchmark: US-born
respondents with two US-born parents, both all races and non-Hispanic white
alone. Broader CPS-native white benchmark is an additional sensitivity.
These are birthplace definitions, not genetic or four-grandparent categories.

G1 = foreign-born citizen/noncitizen born in each country. G2 = US-born with
at least one parent born in that country. Mixed foreign-parent origins count
in both country rows. The aggregate LATAM group counts each person once.
The fixed primary roster has 20 Latin American countries, including Brazil
and Haiti. Belize, Guyana, Jamaica and Trinidad/Tobago are supplementary
regional comparisons, not silently added to the LATAM aggregate.

Four primary outcomes: BA or higher; currently employed / all adults;
official person poverty among those in the poverty universe; mean annual
earnings / all adults including zeros and losses. Secondary: high school
completion and prior-year full-time/full-year work (>=50 weeks, >=35 hours).
Convert preceding-year earnings to 2025 dollars with the held official BLS
CPI-U annual series. This is observed personal gross earnings, not net fiscal
contribution, native welfare, trust, crime, or a genetic effect.

Pool weighted totals across years. This estimates a five-year person-period
population mixture, not a simple average of annual percentages or a panel
of unique people. Preserve the original release weights; population-control
vintage changes are a limitation. Present crude and directly age/sex
standardized results using fixed 2025 benchmark shares in age decades
(25–34, 35–44, 45–54, with 55–64 for sensitivity) crossed with sex. Inference
is conditional on that reference distribution. Fail visibly on empty pooled
strata or nonpositive replicate denominators. Publish raw counts, distinct
IDs (not validated longitudinal identity), and minimum stratum counts.

Join all 160 replicate weights and the full weight by PH_SEQ/PPPOS and
require one-to-one coverage, unique string IDs and agreement with
MARSUPWT/100. Perturb one annual block at a time while holding other years
at full weights. Apply Census SDR variance factor 4/160. Compute benchmark
contrasts/ratios within each replicate. Because adjacent years overlap and
cross-year replicate alignment is unknown, the sum of annual-block SEs
is a conservative first-order covariance bound. Do not use the smaller
independence SE for claims. Save both replication and first-order linearized
SEs as a denominator-instability diagnostic.

For exploratory comparisons, define small differences as +/-5 percentage
points for rates and +/-10% for earnings. These are explicit analyst choices.
Do not equate nonsignificance with equivalence. Distinguish point estimates
within those bands, a 95% interval entirely within the band, favorable
outperformance, and an unresolved interval. "No materially worse on all
four" uses four one-sided noninferiority checks jointly, with Bonferroni
correction across the fixed 20-country search (alpha .05/20 per country;
intersection-union across four outcomes). First- and second-generation
families are reported separately; do not treat exploring both as a single
corrected existence test. Guard that verdict against <200 observations,
<20 observations in any included standardization stratum, or zero events
or zero non-events in any primary binary outcome. These are conservative
reporting rules, not proofs of survey representativeness.

The central falsifiers are a large earnings/poverty gap despite schooling
parity, benchmark sensitivity, sex divergence, imprecise small-country
estimates, and differences between G1 and G2 that cannot be read as a
parent-child causal transition.

## Reproduce

```sh
UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --no-project python3 infra/immigration-fiscal/latam_comparison_2026_09_17/acquire_cps.py --phase docs
# Read the dictionaries before the bulk acquisition.
UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --no-project python3 infra/immigration-fiscal/latam_comparison_2026_09_17/acquire_cps.py --phase data
OPENBLAS_NUM_THREADS=1 UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --no-project python3 infra/immigration-fiscal/latam_comparison_2026_09_17/analyze.py
```

Requires NumPy and pandas. Input discovery reuses held 2024–2026 archives
and the existing BLS cache; it does not redownload them. New archives live
in ignored `_cache/` because the normal external SSD is not mounted.
`_cache/ACQUIRED.md` and `acquisition.json` bind source URLs and hashes.
All tables and diagnostics are regenerated into ignored `derived/`.

Additional public sources: `acquire_oi.py` reproduces acquisition of five
Opportunity Insights CSV tables, seven codebooks and the official library
inventory into `_cache/oi/`. `inspect_oi.py` validates their hashes and
prepares country-income context using the already-held 6a/6b tables.
The original manifest retains temporary acquisition paths; the inspector
resolves newly acquired files under the durable cache and verifies bytes.
These aggregate datasets do not join to CPS people. Native-mother income
fields do not establish two native parents or third-plus ancestry.

`gss_readiness.py` audits the held GSS detailed Hispanic-origin variable and
generation questions without computing outcome estimates. A newly acquired
LAPOP US2019 codebook in `_cache/social/` failed the detailed-origin and
parent-birthplace requirement; no LAPOP respondent data were acquired.

After analysis, run `summarize.py` to write the complete country tables,
margin sensitivity and exportable PDF/PNG. The 20-country corrected flag
is reserved for the prespecified roster; aggregate and supplementary rows
have no corrected existence verdict. Crude, sex and age-window comparisons
are sensitivities, not extra confirmatory searches.

After the first country results, a transparent exploratory sensitivity was
added: distinguish two parents born in the same country from one country-born
parent plus one US-born parent. These profiles were motivated by the
any-parent membership definition and the user's classification question;
they are not part of the prespecified 20-country confirmatory search.
They measure reported parental birthplaces, never genetic fractions.

`check_estimator.py` provides deterministic estimator and classification
checks. `verify_raw.py` independently rebuilds full-weight G2 estimates from
raw CSVs, allowing for rounding of published main weights, and reports
weighted medians and upper-tail diagnostics. Tuple-valued age/sex keys use
explicit dictionaries to avoid pandas `.loc` interpreting them as multiple
indexers. The independent raw rerun checks this path on actual data.

Plotting requires Matplotlib as well as pandas/NumPy. If absent, use the
temporary environment without changing the project installation:

```sh
OPENBLAS_NUM_THREADS=1 MPLCONFIGDIR=/private/tmp/latam-matplotlib UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --no-project --with matplotlib --with pandas --with numpy python3 infra/immigration-fiscal/latam_comparison_2026_09_17/summarize.py
```

Validation completed September 17: all five weight joins passed; independent
raw reconstruction checked every available main G2/reference primary key
(76/76), with both legitimately incomplete country profiles explicitly
logged. `check_estimator.py` checks empty-stratum failure, mixed origins,
strict native definition, standardization and survey variance against hand
calculations. Native code review and independent numerical-gradient probes
passed after fixing corrected-family flags outside the declared country
roster and adding a verifier coverage gate. The latter prevents a zero-check
or incomplete run from printing PASS. The figure was visually inspected.

These are new analysis CLIs rather than a refactor of the existing social
estimator: the older script has top-level execution and an equal-year
estimand; this lane needs pooled totals, country coverage and age/sex cells.
Its validated join and SDR definitions were retained and independently
checked, without changing the older analysis or its callers.
