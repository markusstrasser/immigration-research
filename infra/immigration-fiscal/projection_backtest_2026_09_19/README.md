# Projection assumption back-test and fiscal sensitivities

This lane checks an observable NRC1997 fiscal-policy assumption, performs a new
NRC-style education transition back-test, follows fixed birth/entry groups in
repeated cross-sections, and prices three conditional composition/exit changes.
It does not validate a century's fiscal realization or identify admission costs.

```sh
UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --no-project \
  --with pandas --with numpy --with openpyxl --with pyreadstat --with duckdb \
  python3 infra/immigration-fiscal/projection_backtest_2026_09_19/builder.py \
  --source-root /Users/alien/Projects/immigration-research --fetch

UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --no-project \
  --with pandas --with numpy --with pyreadstat --with duckdb \
  python3 -m unittest discover \
  -s infra/immigration-fiscal/projection_backtest_2026_09_19 -p 'test_*.py'
```

`--source-root` reads the canonical repository and its ignored data from an
isolated checkout. `--microdata-db` overrides the read-only IPUMS database.
`--out` overrides the local ignored output directory. Without `--fetch`, the
two downloaded primary documents must already be in the output directory or
supplied by `--source-cache`. No raw file is modified. Dependencies are existing
canonical CPS/MEPS and profile exports, GSS1972–2024 release3a, and the local
IPUMS census/ACS extract. The manifest fingerprints sources, exports and code.

## Measurement contracts

| Output | Question and limits |
|---|---|
| `nrc_budget_assumption_backtest.csv` | OMB FY2027 table7.1 actual federal debt held by public/GDP, FY2016–2024, against freezing the2016 ratio. Gross debt is retained separately. |
| `nrc_published_scenarios.csv` | Transcribed source-anchored NRC table7.6, all-origin immigrant plus descendants,1996-dollar NPV. Its baseline and no-adjustment scenario are not today's estimates. |
| `gss_transition_cells.csv`, `gss_temporal_prediction.csv` | Our newly fitted school-years transition model, not recovered NRC coefficients. Training: survey through1996, birth1961–71; holdout: survey1998–2024,birth1972+, both ages25–34. Each answered maternal/paternal education link receives respondent weight. The estimand weights parent-child links, not unique children. |
| `gss_coverage.csv` | Unique respondents, parent-data coverage, cohorts, and actual observed survey-year range. Strict G2 requires known parent birthplace; G3 requires both US parents and at least one foreign grandparent. Mexican family origin is self-reported, not verified grandparent country. |
| `fixed_birth_entry_cohorts.csv` | Mexico-born1975–1980 arrivals, birth proxies1956–65 or1946–55, repeated1990/2000/2010/2023 surveys, compared with US-born all-race residents of the same birth proxies. Fixed1990 target birth-year weights. Ages25–74; older window stops2010 to retain its entire birth window. |
| `mixed_parentage_age_profiles.csv` | Exact CPS2025 G2 partition: two Mexico-born parents, one Mexico-born and one US/territory-born parent, and other/unresolved second parent. Personal-source expanded account excludingN; no parental-pair causal interpretation. |
| `mixed_parentage_lifetime_sensitivity.csv` | Replace only ages25–64 by measured parentage profiles; hold childhood, seniors, institutionalN, survival and policy fixed. Three discount rates; current period profiles. |
| `recent_arrival_education_mix.csv`, `arrival_mix_lifetime_sensitivity.csv` | Current education of2016–2025-arrival Mexico-born residents aged25–54 versus stock. Transport the mix to existing supported working-age education fiscal profiles and hold senior profile common. N and extraF excluded. Sparse education-specific senior mixtures remain diagnostic. |
| `return_migration_timing.csv`, `lineage_return_migration.csv` | Illustrative30% permanent exit at year5/10/20/40. Share comes from NRC's old all-origin assumption, not measured current Mexican exits. Household departure and retained Social Security are separate arms. |

GSS weights use NORC's recommended cross-year `WTSSPS`; `WTSSALL` has no values
in2021–2024 and would silently drop those years. Training and test birth cohorts
cannot overlap. English-only is primary because Spanish interviews began2006;
all-language and pre2021 English arms expose coverage and pandemic mode changes.
No confidence interval is claimed:120 training G2 respondents is modest, while
Mexican G2 has13 and fails the declared30-respondent minimum per parental category.
School years above12 are not BA attainment. Exact NRC matrices and ethnic weights
were not printed; the reconstruction does not claim to reproduce Figure7.A1.

The IPUMS extract lacks wage income, sex and Hispanic origin. `WKSWORK1` is entirely
missing in2010. Consequently the executable outcome is log annual total personal
income among currently employed positive-income respondents, not wages or
full-year earnings. Education uses diploma coding in1990+, so the problematic1980
years-of-schooling crosswalk is avoided. US-born means birthplace<100, excluding
territories; this reference differs from the fiscal lane's broader all-native
definition. Household codes1/2/5 exclude group quarters. Cohort size changes
combine death, migration, reporting, coverage and selection; they do not identify
an emigration hazard or individual economic progress.

Exit removes future domestic flows, not costs already incurred. Social Security
may continue abroad, so0/100% of the current founder SS profile is carried as a
sensitivity. This is not earned-entitlement estimation; the cohort's accrued
credits, residency/legal status and overseas taxable income are not observed.
Child departure removes the corresponding future branch only while G2 is under18;
adult descendants remain. Fertility, per-capita attribution and generation timing
reuse the existing lane. The century is100 calendar intervals; a101-interval arm
reproduces the original lane's inclusive0..100 convention for comparison.

## Validation

Six unit tests cover missing-schooling handling, pre-exit cost preservation,
zero-exit identity, discount clock, invalid retention and age-band completeness.
Source header/table checks bind historical figures. Canonical current personal
fiscal totals reproduce by age for Mexico-born, MexicanG2 and white reference
to at most$0.0016 on billion-dollar totals. Parentage and education partitions
conserve population; sparse working-age cells fail rather than extrapolate.

Upstream CPS/MEPS sampling errors already exist. These new point sensitivity
arms are not confidence bounds; parameter, cohort and policy uncertainty is not
certified by passing deterministic arithmetic tests.

Independent read-only review checked the GSS source labels/weights and temporal
split, income-proxy scope, profile transport and exit/retained-SS arithmetic.
Its missing imported-helper fingerprints were repaired: the education builder,
lineage inputs builder and education manifest now accompany the raw/export hashes.
