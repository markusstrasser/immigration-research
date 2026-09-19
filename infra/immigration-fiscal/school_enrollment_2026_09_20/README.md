# Measured public K–12 enrollment correction

**Result:** replacing the old uniform 80.27% factor with October 2024 measured
age/origin enrollment raises attributed annual school costs for the canonical
Mexican-origin target by **$25.040bn shared / $26.937bn personal**. These are
model corrections in nominal 2024 dollars, not marginal immigration effects.
The all-age school-only revised balances are −$259.379bn / −$283.200bn against
the finance-vintage baseline −$234.339bn / −$256.263bn. Other correction lanes
must be combined separately, once, by component.

| Construction | Shared target change, $bn | Personal target change, $bn |
|---|---:|---:|
| Measured origin/age rates, ages 5–17 only | −16.607 | −17.874 |
| Measured origin/age rates, grades K–12 at ages 3–24 | −24.481 | −26.401 |
| Measured origin/age rates, all reported K–12 ages | −25.040 | −26.937 |
| Pool all origins within age; all ages | −15.289 | −16.159 |

The final row is a transport sensitivity that discards the measured enrollment
difference by origin; it is not the preferred measurement. The ages-3–24 row
shows the small effect of excluding older reported elementary/high-school
students, whose fit to the standard per-pupil cost schedule is less secure.
The larger change comes from the measured rate and omitted ages, not that tail.

## Reproduce

From this directory, using the canonical repository for read-only dependencies:

```sh
UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --no-project python3 acquire.py
OPENBLAS_NUM_THREADS=1 UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --offline --no-project \
  --with numpy --with pandas --with openpyxl --with pyreadstat --with duckdb \
  python3 builder.py --source-root /Users/alien/Projects/immigration-research
UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --offline --no-project \
  --with numpy --with pandas python3 -m unittest discover -s .
```

`acquire.py` verifies the committed source lock, probes headers, downloads via
atomic `.part` files, and resumes interrupted downloads. An existing incomplete
ZIP cannot become a pinned source. Initial `--pin` creation is a deliberate
review step and refuses an existing lock. No paid API or credentials are used.
Raw inputs, download receipts, and generated outputs are ignored. Four source
files total about 82.3 MB; sources and exact SHA256 values are in `sources.json`.

## Measurement contract

[Census release](https://www.census.gov/data/datasets/2024/demo/cps/cps-school-enrollment.html),
[dictionary](https://www2.census.gov/programs-surveys/cps/techdocs/cpsoct24.pdf),
[replicate layout and official totals](https://www2.census.gov/programs-surveys/cps/datasets/2024/supp/cps_school_repwgt_oct24.sas).
Attachment 7 of the dictionary supplies the two edited question branches:

- Ages 3–14: child record, `PESCH35=1` or `PESCH614=1`, `PECHPUB=1`,
  `PECHGRDE=3..16` (full/part-day kindergarten or grades 1–12).
- Ages 15+: civilian adult record, `PESSCHOL=1`, `PEPUBLIC=1`, `PRGRADE=7..12`
  (elementary grades or high school). Do not substitute basic `PESCHENR`, whose
  age and school universe is narrower. Nursery/preschool, private school and
  college are excluded. No homeschooling category is independently priced.
- `PWSUPWGT` and 160 replicate weights have four implied decimal places. Match
  `QSTNUM/OCCURNUM` within October only. The 27,342 unmatched source records are
  zero-weight nonperson records (age/type −1); any missing actual person fails.

Actual October public K–12 counts: **47.954m nationally (SE 0.359m)**,
**8.634m canonical target (SE 0.222m)**. Target pupils outside 5–17 number
0.485m. The broad self-ID/own/parent-Mexico OR diagnostic gives 8.773m pupils;
it is not substituted for the canonical fiscal target. The latter is exactly
the existing union of Mexico-born foreign-born, native with a Mexico-born
parent, and Mexican self-ID natives with two US-area-born parents. Unknown or
other parental origins are not silently recoded as US-born.

## Transport and allocation

Fit national target/rest rates in ages 5–13, 14–17 and 18–24; pool all origins
at ages 3–4 and 25+ because grade-K–12 cases are scarce. Every estimation cell
must have at least 50 observed records and Kish effective N at least 50.
Production effective Ns range from 606 to 53,952; target public-pupil sample
counts are 1,334, 683 and 77 in the three unpooled age bands. Target rates are
90.24%, 89.43%, 7.02%; rest rates 83.37%, 84.32%, 5.68%.

Apply those probabilities to the March 2025 ASEC population using each record's
age and canonical origin. This assumes those rates transport across survey
months, within broad age cells and across states. It does not claim the records
are linked, measure actual annual pupil-months, or adjust March population
controls. Expected national pupils move 43.728m → 48.551m; target pupils move
7.181m → 8.487m. Direct October and transported March counts are separate.

Price exposure using the canonical state operating, capital/interest and
district-differential schedules. Cost vintages and average-cost interpretation
remain unchanged. For personal allocation the pupil carries the expense; for
shared allocation the expense is split once among SPM resource-unit members.
Receiver person weights are retained exactly, so national weighted shared and
personal costs need not be equal. School-lunch reversal is held fixed because
it cancels an already included benefit; no extra lunch expense is added.

The $25.040bn shared change comprises $20.499bn operating, $4.042bn capital/
interest and $0.500bn district differential. The personal change comprises
$22.030bn, $4.349bn and $0.557bn. National changes are −$95.728bn / −$98.596bn;
rest-of-population changes −$70.688bn / −$71.659bn. Target plus rest exactly
equals national for each allocation, scenario and component.

## Validation, uncertainty and remaining discrepancies

All 161 weight sums reproduce Census's SAS controls within 0.005 person, and
replicate0 equals the source supplement weight record by record. The public
enrollment branch construction agrees with the published `PRENPUPR` recode.
All 18 original school/K/D × allocation × population totals reconcile to the
current macro account within $1,000. Seven boundary/regression tests cover
grade/age/private/preschool/college branches, canonical versus broad origin,
unequal-weight sharing, replacement deltas, malformed records and nonperson
replicate exclusions. An interrupted download and the nonperson merge issue
were corrected before pinning/analysis; fail-loud guards remain.

For geographical validation only, refit rates **excluding both CA and TX**.
Target pupils are overpredicted by 17k in CA (residual SE69k) and 27k in TX
(SE59k). TX rest-of-population pupils are underpredicted by 154k (SE69k), so
the transport is not uniformly validated. These are descriptive checks, not
causal tests or an adjustment fitted to state controls.

Unused direct ACS2024 cells give national all-age public K–12 46.981m versus
October47.954m. The 0.973m difference remains; annual-average versus October
timing and survey construction have not been decomposed. CA October total
5.701m is 72k above CDE2024–25 K–12 excluding TK. TX5.225m is 31k below the
lagged TEA2023–24 K–12 control, but Hispanic enrollment is 330k below that
lagged control (October SE116k). Hispanic is not Mexican-origin. Controls and
locators come from `admin_school_checks_2026_09_19/sources.json`; the ACS source
was used previously for the old adult-household proxy, so these are unused
comparison cells, not a wholly new independent source. None is raked to fit.

Uncertainty refits every October rate under its 160 replicates and separately
reweights March exposure under its 160 replicates. For the primary target
delta, October SE is $1.754bn/$1.923bn and March SE $0.364bn/$0.340bn.
Because the CPS samples can overlap, their covariance is not assumed zero:
sum-of-SE upper envelopes are **$2.118bn/$2.263bn**. The file also gives the
zero-covariance value and absolute-difference lower envelope. These describe
conditional sampling error of the correction, not the SE of the entire annual
account, not transport/cost uncertainty, and not confidence in causal costs.

The leading explanation is an understated exposure proxy; alternatives include
month/state/age transport and survey-definition differences. A matched current
administrative age/origin pupil count or repeated October release that overturns
the measured rate differential would supersede this correction. Source choice
and interpretation remain subject to the project's LLM instrument caveat.

## Integration outputs

- `derived/correction_effects.csv`: primary `all_ages` only; exact keys
  `allocation`, `group`, `component`; `balance_change_bn` is the signed delta.
  Components are `school`, `K`, `D`. Add each once to the macro finance-vintage
  baseline; no aggregate subtotal row is present in this integration file.
- `derived/fiscal_effects.csv`: all constructions plus correlated component
  subtotal `school_K_D`; **do not sum the subtotal with its components**.
- `derived/annual_balance.csv`: subtotal changes and school-only revised net.
- `derived/updated_account_components.csv`: complete school-only revised table.
- `derived/october_counts.csv`, `national_rates.csv`, `transported_pupils.csv`,
  `heldout_CA_TX.csv`, `comparators.csv`: measurement and validation outputs.
- `derived/manifest.json`: loaded canonical code/input hashes and checks.
- `DATASET_CARD.md`: registration snippet for parent integration; no shared
  index/register/core file changed by this lane.
