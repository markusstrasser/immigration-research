# Institutional population by education, origin and age

This lane supplies ACS 2024 one-year person-PUMS counts and paired sampling replicates to the education fiscal account. It does not identify prison residents, government payment shares, institutional transitions, or the effects of admission. The source is read-only; the generator writes only to its output directory.

## Reproduce

From this directory:

```sh
UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --no-project python3 -m unittest -v test_institutional_counts.py
UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --no-project python3 institutional_counts.py
```

Dependencies: Python, numpy and pandas. The executed release used numpy 2.5.3 and pandas 3.0.5. `--source`, `--out` and `--chunk-size` override the read-only ZIP path, output directory and chunk size. The expected source is the complete US two-part person ZIP, excluding Puerto Rico; wrong source members or failed national gates abort export. Existing outputs must be treated as stale after an unsuccessful rerun until their hashes and producer hash are checked.

## Definitions

[SOURCE] Field definitions are from the [official 2024 PUMS dictionary](https://www2.census.gov/programs-surveys/acs/tech_docs/pums/data_dict/PUMS_Data_Dictionary_2024.pdf). Point and all 80 person replicate weights come from the [official US person ZIP](https://www2.census.gov/programs-surveys/acs/data/pums/2024/1-Year/csv_pus.zip). SDR variance is `4/80 * sum((replicate − full)^2)`; see [2024 accuracy documentation](https://www2.census.gov/programs-surveys/acs/tech_docs/pums/accuracy/2024AccuracyPUMS.pdf).

- Education: `SCHL=1..15` less than HS; `16,17` HS/GED only; `18..20` some college or associate degree; `21..24` BA or higher. All age-25+ records must have valid completed-schooling codes; these groups partition `all`. Attained schooling is not schooling at admission.
- Ages: 25–34, 35–44, 45–54, 55–64, 65–74, 75+. Counts use observed resident stocks. No entry-year or descendant dimension is present.
- Foreign-born groups require `NATIVITY=2`: Mexico `POBP=303`; other Central America 310–316; Caribbean 321–344; South America 360–374; identifiable Southeast Asia 205,206,211,223,226,233,236,242,247. Geographic Caribbean includes non-Spanish-language origins; no regional group is an ethnicity definition.
- `all_native` is `NATIVITY=1`, including US natives born abroad. `native_nh_white` further requires `HISP=1,RAC1P=1`. It includes every native generation and is an explicit proxy for, not an equivalent of, CPS third-plus NH white. Native categories overlap and must not be summed.
- Institutions: `RELSHIPP=37`; noninstitutional group quarters: `38`. `SERIALNO[4:6]` must be `HU` for households or `GQ` for group quarters, agreeing with those relationship codes. Household population excludes both kinds of group quarters. `population_all` includes both.

## Consumer contract

`derived/counts.npz` contains four integer arrays of shape `[35 domains, 6 bands, 81 weights]`:

| Key | Population counted |
|---|---|
| `population_all` | Households and both group-quarter categories |
| `household_population` | Household residents only |
| `institutional_population` | All institutional residents |
| `institutional_male_population` | Institutional residents with `SEX=1` |

Each has a corresponding `<key>_n` array `[35,6]` containing unweighted PUMS record counts. Group-quarter data include whole-person imputed records; raw n is not an independent-interview count (accuracy document pp. 5–6). Zero counts remain present; no suppression or smoothing is performed. Institutional males are not labeled prisoners.

Axis labels are authoritative in `domains.csv`, `bands.csv`, and `weights.csv`. Domains are origin-major in the order declared above, with education ordered `all,lt_hs,hs_only,some_college,ba_plus`. Weight index zero is `PWGTP`, followed by `PWGTP1..80`. Never independently permute weight columns across domains or quantities.

`counts.csv` is the long human-readable count table with point estimates, ACS design SEs, symmetric 95% intervals, raw counts and sparse flags. Negative lower normal endpoints are retained rather than described as physical count bounds. `raw_n<30` is an explicitly declared disclosure heuristic, not a reliability certification. A zero observation and zero replicate SE do not establish a true zero population.

`unit_cost_scenarios.csv` prices all institutional residents at the same hypothetical annual price of $0, $50,000, $100,000 or $150,000 in 2024 dollars. Every row marks the price as an explicit uncalibrated assumption. These are neither bounds nor estimated correctional costs, and no price is selected as central. The SE is conditional on that price. There is no claim that the price is all publicly financed or additional to medical costs already in another account. The consumer owns the overlap, fiscal coverage and payer choices. The historical prison/nursing proxy is not imported.

The consumer may multiply institutional count replicates by its declared price and apply a separately identified CPS denominator. An ACS numerator over a CPS household denominator is a modeling choice requiring explicit sampling-error combination; this lane does not perform it. The stock profiles must not be applied to recent arrivals as observed institutional risks. For fixed within-ACS contrasts, use paired replicate differences; `contrast()` and its tests enforce shared covariance.

`audit.json` records source ZIP SHA-256, member CRC/size, producer SHA-256, output hashes, source URLs, field/population scope and gates. Verify all applicable hashes before consuming an existing export. Derived files and caches are ignored by Git; generators, tests and documents are versioned.
