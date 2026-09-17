**Verdict:** The ACS 2024 common-age wage and income gaps against native non-Hispanic whites agree with CPS in sign everywhere and in magnitude for wages almost exactly (national ACS/CPS ratio 0.98 for Mexico-born, 1.03 for US-born Mexican self-ID), while ACS total-income gaps run about 10% narrower than CPS (ratios 0.90 and 0.88), so CPS earnings measurement does not manufacture the earnings shortfall that drives the ledger's modeled income and payroll tax.

[REPLICATION] ACS 2024 1-year PUMS and CPS ASEC 2025, both computed in this lane.

Both surveys are self-reported. This compares two survey instruments with different
sampling frames, reference periods, questionnaires and editing rules. It tests
survey-specific measurement and sampling, **not** self-report bias in general: an
error common to both instruments would not show up here.

## Common-age per-person gap versus native non-Hispanic whites

Reference age shares are the white group's own full-weight shares in that domain.
Intervals are pointwise normal 95% intervals from replicate variance only
(ACS 4/80, CPS 4/160); they omit model, coverage and nonresponse error.

| Domain | Group | Measure | ACS gap $/std person [95%] | CPS gap $/std person [95%] | ACS/CPS |
|---|---|---|---|---|---|
| national | Mexico-born | wages | -17,241 [-17,541, -16,941] | -17,518 [-18,890, -16,146] | 0.98 |
| national | Mexico-born | total personal income | -26,228 [-26,600, -25,856] | -29,222 [-30,762, -27,682] | 0.90 |
| national | US-born Mexican self-ID | wages | -9,473 [-9,811, -9,134] | -9,208 [-10,834, -7,581] | 1.03 |
| national | US-born Mexican self-ID | total personal income | -14,639 [-15,055, -14,223] | -16,639 [-18,486, -14,793] | 0.88 |
| national | All natives | wages | -2,590 [-2,648, -2,532] | -2,448 [-2,729, -2,168] | 1.06 |
| national | All natives | total personal income | -3,592 [-3,658, -3,527] | -3,893 [-4,221, -3,565] | 0.92 |
| CA | Mexico-born | wages | -28,099 [-28,889, -27,310] | -26,442 [-29,892, -22,992] | 1.06 |
| CA | Mexico-born | total personal income | -43,467 [-44,345, -42,589] | -43,405 [-47,435, -39,374] | 1.00 |
| CA | US-born Mexican self-ID | wages | -18,387 [-19,280, -17,493] | -16,599 [-20,435, -12,762] | 1.11 |
| CA | US-born Mexican self-ID | total personal income | -28,617 [-29,687, -27,547] | -28,203 [-32,629, -23,776] | 1.01 |
| CA | All natives | wages | -6,543 [-6,935, -6,152] | -6,663 [-8,410, -4,917] | 0.98 |
| CA | All natives | total personal income | -9,317 [-9,735, -8,898] | -10,441 [-12,372, -8,509] | 0.89 |
| TX | Mexico-born | wages | -21,413 [-22,142, -20,684] | -21,577 [-24,678, -18,477] | 0.99 |
| TX | Mexico-born | total personal income | -31,061 [-31,834, -30,289] | -33,893 [-37,564, -30,223] | 0.92 |
| TX | US-born Mexican self-ID | wages | -14,560 [-15,246, -13,875] | -10,535 [-15,217, -5,853] | 1.38 |
| TX | US-born Mexican self-ID | total personal income | -21,538 [-22,308, -20,768] | -19,566 [-24,768, -14,364] | 1.10 |
| TX | All natives | wages | -5,899 [-6,205, -5,593] | -3,726 [-5,246, -2,206] | 1.58 |
| TX | All natives | total personal income | -8,116 [-8,423, -7,810] | -6,633 [-8,384, -4,883] | 1.22 |

ACS wage is `WAGP`, CPS wage is `WSAL_VAL`; ACS income is `PINCP`, CPS income is
`PTOTVAL`. ACS `PERNP` (total earnings including self-employment) is also in
`derived/acs_gaps.csv`: the national Mexico-born common-age gap is -17,717 (SE 159)
and the US-born Mexican self-ID gap is -10,326 (SE 186), so adding self-employment
earnings does not move the wage conclusion.

### Where the two surveys disagree

Treating the two surveys as independent, sixteen of the eighteen contrasts above
have overlapping 95% intervals (`derived/acs_cps_difference.csv`). The two that do
not are the national Mexico-born income gap (difference 2,994, z = 3.7) and the
Texas all-native wage gap (difference -2,173, z = -2.7).

The income divergence has a visible source in the level means. The CPS reference
group reports more total income than the ACS one (native NH white mean 56,340
versus 53,232, CPS higher by 5.8%), while Mexico-born totals are nearly the same
(34,713 versus 34,191, CPS higher by 1.5%). CPS ASEC asks a detailed income
supplement covering more transfer and retirement sources than the ACS income
block, and those sources concentrate in the older, whiter reference population.
Wage levels differ nearly proportionally between the surveys (white 38,540 versus
37,634, Mexico-born 28,710 versus 27,905), which is why the wage gap survives.

[INFERENCE] The income-block explanation is read off the level means computed here
plus the known questionnaire difference; this lane did not decompose CPS income by
source to prove it.

## Age-matched aggregate gap, $bn

`Σ_b [Y_gb − (N_gb/N_rb) Y_rb]`, with the reference schedule recomputed in every
replicate. Standard errors in parentheses.

| Domain | Group | Measure | ACS $bn (SE) | CPS $bn (SE) |
|---|---|---|---|---|
| national | Mexico-born | wages | -297.6 (2.8) | -337.9 (13.9) |
| national | Mexico-born | total personal income | -383.8 (3.4) | -473.8 (16.2) |
| national | US-born Mexican self-ID | wages | -192.3 (2.8) | -199.7 (14.0) |
| national | US-born Mexican self-ID | total personal income | -241.8 (3.2) | -286.8 (15.9) |
| national | All natives | wages | -701.7 (8.0) | -666.6 (38.8) |
| national | All natives | total personal income | -940.2 (9.1) | -1,023.1 (44.7) |
| CA | Mexico-born | wages | -164.1 (2.8) | -158.9 (12.4) |
| CA | Mexico-born | total personal income | -222.6 (3.1) | -231.3 (14.7) |
| CA | US-born Mexican self-ID | wages | -118.7 (2.8) | -123.4 (15.1) |
| CA | US-born Mexican self-ID | total personal income | -150.1 (3.0) | -165.2 (16.2) |
| CA | All natives | wages | -167.3 (5.1) | -174.0 (24.4) |
| CA | All natives | total personal income | -222.4 (5.3) | -252.1 (26.2) |
| TX | Mexico-born | wages | -76.2 (1.6) | -76.9 (8.1) |
| TX | Mexico-born | total personal income | -98.8 (1.7) | -110.0 (10.6) |
| TX | US-born Mexican self-ID | wages | -78.0 (2.0) | -56.8 (10.7) |
| TX | US-born Mexican self-ID | total personal income | -100.6 (2.1) | -92.0 (11.9) |
| TX | All natives | wages | -131.9 (3.5) | -84.1 (17.2) |
| TX | All natives | total personal income | -173.6 (3.6) | -143.8 (19.4) |

The Mexico-born national aggregate wage gap differs by 12% between the surveys
(-297.6 versus -337.9 $bn) because the ACS counts a smaller Mexico-born household
population, not because the per-person gap differs; see Gate 2.

## Employment and population context

ACS employment rate, 16+, `ESR` in {1,2,4,5}, household population:

| Group | Population 16+ | Employment rate (SE) |
|---|---|---|
| Mexico-born | 10,905,003 | 0.6583 (0.0019) |
| US-born Mexican self-ID | 17,494,323 | 0.6615 (0.0017) |
| Native NH white | 150,134,258 | 0.6080 (0.0004) |
| All natives | 221,028,126 | 0.6161 (0.0004) |

Both Mexican-origin groups are employed at a *higher* rate than native NH whites in
ACS, by 4 to 5 points. The CPS analogue computed here (share of 16+ with positive
`PEARNVAL`, not an `ESR` recode, so not directly comparable) shows the same ordering:
0.677 Mexico-born, 0.673 US-born Mexican self-ID, 0.626 native NH white. The wage
gap therefore comes from pay per worker and hours, not from a lower share working.

## Gates

**Gate 1 — PASS.** CPS civilian household populations reproduce the held ledger
(`all_age_ledger_2026_09_17/derived/estimates.csv`, scenario `all_age_shared`,
metric `absolute_total`) to floating-point exactness, far inside the 1-person bound.

| Group | Ledger | This lane | Difference |
|---|---|---|---|
| mexico_born | 12,220,781.883 | 12,220,781.883 | 0.0 |
| mexican_second_gen | 14,333,217.664 | 14,333,217.664 | 3.7e-09 |
| mexican_third_plus_selfid | 14,342,574.606 | 14,342,574.606 | 0.0 |

**Gate 2 — reported, not forced.** ACS and CPS household populations, national:

| Group | ACS | CPS | ACS/CPS |
|---|---|---|---|
| Mexico-born | 11,438,267 | 12,220,782 | 0.936 |
| US-born Mexican self-ID | 27,292,685 | 28,347,920 | 0.963 |
| Native NH white | 179,193,267 | 183,822,016 | 0.975 |
| All natives | 282,180,396 | 283,672,180 | 0.995 |

The CPS Mexico-born count exceeds the ACS one by 6.8%, a larger discrepancy than
for any other group here. The two counts are not reconciled and no adjustment was
applied. Both are weighted survey estimates of the same nominal quantity, so at
least one is off; the ACS group-quarters exclusion and the CPS one are also not
identical in construction (see caveats).

**Gate 3 — PASS.** The ACS full-weight national household population is 331,722,429,
identical to the published ACS 2024 1-year `B25008_001E` total population in occupied
housing units fetched from the Census API (ratio 1.0000, bound was 0.5%). This is an
identity rather than an independent check: PUMS person weights are controlled to that
total.

## What this says about the ledger

The ledger attributes about 89% of the Mexican-origin shortfall against non-Hispanic
whites to modeled income and payroll tax on CPS earnings. Payroll and income tax in
that model are functions of wages and of total income. The wage input replicates on
ACS within 2 to 3% nationally, so the payroll-tax leg of the attribution is not a CPS
artifact. The total-income input is about 10% narrower on ACS, so an income-tax leg
built on ACS instead of CPS would be correspondingly smaller. That is a bound on the
sensitivity of the tax component to the survey, not a re-estimate of the ledger: this
lane did not rerun the tax model on ACS.

[FRAMING-SENSITIVE] Whether a 10% narrower income gap materially changes the 89%
figure depends on how the ledger splits payroll from income tax, which is not
recomputed here.

## Scope caveats

- **ACS has no parent birthplace.** `usborn_mexican_selfid` (NATIVITY=1 & HISP=2)
  pools second, third and later generations and excludes US-born people of Mexican
  descent who do not report Mexican Hispanic origin. It is not the ledger's
  `mexican_second_gen` or `mexican_third_plus_selfid` and cannot be split into them.
  The corresponding CPS pool built here (native & `PRDTHSP`==1, parent birthplace
  ignored) is the like-for-like comparison, and it is not a ledger category either.
  The CPS-only generation split is in `derived/cps_gaps.csv`.
- **Reference periods differ.** ACS interviews across all twelve months of 2024 and
  asks about the twelve months before interview, so its income window is a rolling
  one spanning parts of 2023 and 2024. CPS ASEC 2025 asks about calendar 2024.
  `ADJINC` (divided by 1,000,000) was applied to `WAGP`, `PINCP` and `PERNP` to put
  ACS dollars on a 2024 basis; no equivalent adjustment exists or is needed for CPS.
- **Domain construction differs.** The ACS domain is the housing-unit population;
  the 2024 1-year person PUMS carries no `TYPEHUGQ` column, so this was taken from
  `SERIALNO` positions 4:6 equal to "HU" and verified to agree exactly with
  `RELSHIPP` not in {37,38} on all 3.4M records. The CPS domain is the civilian
  household population, `PRPERTYP==2 | A_AGE<15`, the ledger's own definition. These
  are close but not identical; the CPS version additionally excludes armed forces
  members aged 15 and over living in households.
- **Mexican self-identification codes.** ACS `HISP`==2 is Mexican; CPS `PRDTHSP`==1
  is Mexican in the detailed Hispanic-origin recode, the same code the ledger uses
  for its third-plus self-ID group.
- **Two reference definitions on CPS.** Gaps are reported against the ACS-aligned
  `native_nh_white` (all CPS natives, `PEHSPNON`==2 & `PRDTRACE`==1) and against the
  ledger's `third_plus_nh_white` (additionally requiring two US-area-born parents).
  The two references differ by 166 dollars in common-age wages, so the choice does
  not affect any conclusion here.
- **Standard errors are replicate-only.** Neither survey's interval includes model,
  coverage, undercount or nonresponse-adjustment error. The ACS intervals are four
  to five times tighter than the CPS ones purely because the ACS sample is roughly
  twenty times larger; that is not evidence that ACS is more accurate.
- **No tax model was run on ACS.** This lane compares earnings and income inputs
  only.

## Files

Covered, all under
`/Users/alien/Projects/immigration-research/infra/immigration-fiscal/acs_earnings_replication_2026_09_17/`:

| File | Role |
|---|---|
| `acs_gaps.py` | ACS PUMS load, groups, cells, gaps, gates 2 and 3 |
| `cps_gaps.py` | CPS state via the held `extend_ledger`, groups, cells, gaps, gate 1 |
| `common.py` | age bands, replicate cell totals, SDR variance, gap estimators |
| `make_tables.py` | assembles the side-by-side tables in this file |
| `derived/acs_gaps.csv`, `derived/acs_cells.csv`, `derived/audit.json` | ACS outputs and provenance |
| `derived/cps_gaps.csv`, `derived/cps_cells.csv`, `derived/cps_audit.json` | CPS outputs and provenance |
| `derived/acs_cps_difference.csv`, `derived/tables.md` | cross-survey differences and rendered tables |

Source: ACS 2024 1-year person PUMS,
`https://www2.census.gov/programs-surveys/acs/data/pums/2024/1-Year/csv_pus.zip`,
602,847,146 bytes (matching the `Content-Length` probe), sha256
`afdc6d90c6e2f0bab365ed32d95ba4c4d8ac651162f46ac7861295b2dc469894`, staged at
`/Users/alien/research-data/immigration-fiscal/data/external/acs_pums_2024_1yr/csv_pus.zip`.
Free space on the destination at probe time was 73 GiB. The archive holds
`psam_pusa.csv` and `psam_pusb.csv` (two parts, not four), 3,239,682 household-population
person records. CPS source is the held
`gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip`; its sha256 is in
`derived/cps_audit.json`.

## Verification run

Positive controls on the gap machinery, all passing: the common-age gap and the
age-matched aggregate gap of a group against itself are exactly 0.0; constant
replicates give standard error exactly 0.0; the crude weighted mean matches a direct
weighted mean to 1e-15 relative.

## Skipped

- No tax or fiscal model was recomputed on ACS; the brief asked for the earnings and
  income gaps only.
- The CPS employment figure is a positive-earnings analogue rather than an `ESR`
  recode, because CPS ASEC as parsed by the held builder does not carry an
  employment-status recode. It is labeled as such above and in `derived/cps_audit.json`.
- No attempt was made to reconcile the 6.8% Mexico-born population difference
  (Gate 2 explicitly says not to force agreement).
