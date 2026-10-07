# Projection assumption back-test and fiscal sensitivities

This lane checks an observable NRC 1997 fiscal-policy assumption, performs a new
NRC-style education transition back-test, follows fixed birth/entry groups in
repeated cross-sections, and prices three conditional composition/exit changes.
It does not validate a century's fiscal realization or identify admission costs.

```sh
uv run --no-project \
  --with pandas --with numpy --with openpyxl --with pyreadstat --with duckdb \
  python3 infra/immigration-fiscal/projection_backtest_2026_09_19/builder.py \
  --source-root /Users/alien/Projects/immigration-research --fetch

uv run --no-project \
  --with pandas --with numpy --with pyreadstat --with duckdb \
  python3 -m unittest discover \
  -s infra/immigration-fiscal/projection_backtest_2026_09_19 -p 'test_*.py'
```

`--source-root` reads the canonical repository and its ignored data from an
isolated checkout. `--microdata-db` overrides the read-only IPUMS database.
`--out` overrides `derived/`, whose 12 CSVs are tracked (manifest and downloads ignored). Without `--fetch`, the
two downloaded primary documents must already be in the output directory or
supplied by `--source-cache`. No raw file is modified. Dependencies are existing
canonical CPS/MEPS and profile exports, GSS 1972–2024 release 3a, and the local
IPUMS census/ACS extract. The manifest fingerprints sources, exports and code.

## Measurement contracts

| Output | Question and limits |
|---|---|
| `nrc_budget_assumption_backtest.csv` | OMB FY2027 table 7.1 actual federal debt held by public/GDP, FY2016–2024, against freezing the 2016 ratio. Gross debt is retained separately. |
| `nrc_published_scenarios.csv` | Transcribed source-anchored NRC table 7.6, all-origin immigrant plus descendants, 1996-dollar NPV. Its baseline and no-adjustment scenario are not today's estimates. |
| `gss_transition_cells.csv`, `gss_temporal_prediction.csv` | Our newly fitted school-years transition model, not recovered NRC coefficients. Training: survey through 1996, birth 1961–71; holdout: survey 1998–2024, birth 1972+, both ages 25–34. Each answered maternal/paternal education link receives respondent weight. The estimand weights parent-child links, not unique children. |
| `gss_coverage.csv` | Unique respondents, parent-data coverage, cohorts, and actual observed survey-year range. Strict G2 requires known parent birthplace; G3 requires both US parents and at least one foreign grandparent. Mexican family origin is self-reported, not verified grandparent country. |
| `fixed_birth_entry_cohorts.csv` | Mexico-born 1975–1980 arrivals, birth proxies 1956–65 or 1946–55, repeated 1990/2000/2010/2023 surveys, compared with US-born all-race residents of the same birth proxies. Fixed 1990 target birth-year weights. Ages 25–74; older window stops 2010 to retain its entire birth window. |
| `mixed_parentage_age_profiles.csv` | Exact CPS 2025 G2 partition: two Mexico-born parents, one Mexico-born and one US/territory-born parent, and other/unresolved second parent. Personal-source expanded account excluding N; no parental-pair causal interpretation. |
| `mixed_parentage_lifetime_sensitivity.csv` | Replace only ages 25–64 by measured parentage profiles; hold childhood, seniors, institutional N, survival and policy fixed. Three discount rates; current period profiles. |
| `recent_arrival_education_mix.csv`, `arrival_mix_lifetime_sensitivity.csv` | Current education of 2016–2025-arrival Mexico-born residents aged 25–54 versus stock. Transport the mix to existing supported working-age education fiscal profiles and hold senior profile common. N and extra F excluded. Sparse education-specific senior mixtures remain diagnostic. |
| `return_migration_timing.csv`, `lineage_return_migration.csv` | Illustrative 30% permanent exit at year 5/10/20/40. Share comes from NRC's old all-origin assumption, not measured current Mexican exits. Household departure and retained Social Security are separate arms. |

GSS weights use NORC's recommended cross-year `WTSSPS`; `WTSSALL` has no values
in 2021–2024 and would silently drop those years. Training and test birth cohorts
cannot overlap. English-only is primary because Spanish interviews began 2006;
all-language and pre-2021 English arms expose coverage and pandemic mode changes.
No confidence interval is claimed: 120 training G2 respondents is modest, while
Mexican G2 has 13 and fails the declared 30-respondent minimum per parental category.
School years above 12 are not BA attainment. Exact NRC matrices and ethnic weights
were not printed; the reconstruction does not claim to reproduce Figure 7.A1.

The IPUMS extract lacks wage income, sex and Hispanic origin. `WKSWORK1` is entirely
missing in 2010. Consequently the executable outcome is log annual total personal
income among currently employed positive-income respondents, not wages or
full-year earnings. Education uses diploma coding in 1990+, so the problematic 1980
years-of-schooling crosswalk is avoided. US-born means birthplace<100, excluding
territories; this reference differs from the fiscal lane's broader all-native
definition. Household codes 1/2/5 exclude group quarters. Cohort size changes
combine death, migration, reporting, coverage and selection; they do not identify
an emigration hazard or individual economic progress.

Exit removes future domestic flows, not costs already incurred. Social Security
may continue abroad, so 0/100% of the current founder SS profile is carried as a
sensitivity. This is not earned-entitlement estimation; the cohort's accrued
credits, residency/legal status and overseas taxable income are not observed.
Child departure removes the corresponding future branch only while G2 is under 18;
adult descendants remain. Fertility, per-capita attribution and generation timing
reuse the existing lane. The century is 100 calendar intervals; a 101-interval arm
reproduces the original lane's inclusive 0..100 convention for comparison.

Births need a parent alive at 29, as in the lineage lane (conceptual audit
2026-09-27 §E): `sensitivities.py` multiplies each generation's count by the
parent's survival to 29 on this lane's 2024 total table, 0.99596 from age 25 for
the founder and 0.98143 from birth for later parents [CALCULATION:
`survival_tables.csv` lx].

## Validation

Six unit tests cover missing-schooling handling, pre-exit cost preservation,
zero-exit identity, discount clock, invalid retention and age-band completeness.
Source header/table checks bind historical figures. Canonical current personal
fiscal totals reproduce by age for Mexico-born, Mexican G2 and white reference
to at most $0.0033 on billion-dollar totals. Parentage and education partitions
conserve population; sparse working-age cells fail rather than extrapolate.

Upstream CPS/MEPS sampling errors already exist. These new point sensitivity
arms are not confidence bounds; parameter, cohort and policy uncertainty is not
certified by passing deterministic arithmetic tests.

Independent read-only review checked the GSS source labels/weights and temporal
split, income-proxy scope, profile transport and exit/retained-SS arithmetic.
Its missing imported-helper fingerprints were repaired: the education builder,
lineage inputs builder and education manifest now accompany the raw/export hashes.

## Revisions

- **2026-09-28 (296991d): births need a living parent.** Moved here from the method text on 2026-10-08. Births
  now need a parent alive at 29, as in the lineage lane since 4e9c2e2 (conceptual audit 2026-09-27 §E). All 96 rows
  of `lineage_return_migration.csv` move. The no-exit lineage NPV at 100 intervals goes from −$1,150,003 to
  −$1,140,296 at 0%, −$318,370 to −$316,023 at 3% and −$185,766 to −$184,507 at 5%; at 101 intervals, from
  −$1,166,640, −$319,236 and −$185,893 to −$1,156,487, −$316,866 and −$184,630. Where dependent children leave (exit
  years 5–20), the exit gain falls by $187–3,025, equally in both retained-SS arms; at year 10 and 3% it is
  $64,810–79,152 (was $65,413–79,755). Founder-only gains and every other output are unchanged [CALCULATION:
  `derived/` before and after]. A second run matched 21 of 21 files and the unit tests pass. The rebuild also
  refreshed provenance that had drifted before this change: four upstream fingerprints, this lane's `builder.py`
  hash (97e1470) and the microdata path, which now resolves under `sources/` with the same hash.
- **2026-10-08: item T.** `sensitivities.py` now passes the ledger's income-tax keys to `build_charges`; without them
  it stopped with a KeyError once item T (the income tax on the main case's keys, `ledger_absolute_2026_09_17`) joined the ledger. The
  ignored `derived/` was not regenerated: `builder.py` also reruns the IPUMS cohort check, which loads 8.66M records
  and was stopped at the session's per-process memory cap (2.45 GB, 01:57 on 2026-10-08), after its NRC and GSS outputs
  had matched `derived/` byte for byte. Until a rerun with more memory it holds the pre-T sensitivities, and
  `manifest.json` the pre-T hashes. A scratch run of `sensitivities.run` alone (0.98 GB, 7 s) gives, at
  3%, old → new: stock and recent-arrival age-25 NPVs −$48,545 and −$8,195 → −$36,943 and +$12,630 (difference
  +$40,350 → +$49,573); at birth, the two-Mexico-born-parent and mixed-nativity G2 profiles −$288,347 and −$266,206 →
  −$288,830 and −$239,308 (difference $22,141 → $49,522); the founder's year-10 exit gain $11,804–26,146 →
  $10,743–25,085; the lineage no-exit balance −$316,023 → −$289,270, and with dependent children leaving, the year-10
  exit balance −$251,213 to −$236,871 → −$229,010 to −$214,668 (gain $64,810–79,152 → $60,260–74,602). At 5% an
  early founder-only exit with full Social Security retained still worsens the balance (−$1,273 → −$3,393).
- **2026-10-08 (04:37 JST): rebuilt in place.** `builder.py` ran without `--fetch`, alone on the machine, with a
  peak of 2.95 GB resident, and exited 0. All 12 tables and `manifest.json` in `derived/` are rebuilt. The five fiscal
  tables (parentage profiles and lifetimes, arrival mix, return-migration timing and lineage) now carry item T and
  equal the scratch run in the previous bullet byte for byte. The NRC and GSS tables equal the 01:57 run
  byte for byte, and the IPUMS cohort table still matches §3 of the memo. The canonical profiles now reproduce within
  $0.0033 (the white reference; Mexico-born $0.00003, Mexican G2 $0.0002), against $0.0016 before; the Validation
  section says so. Unit tests 6/6. The memo's §4 is restated on these tables.
