claude-opus-5[1m]

# Enclave neighborhood quality and storefront informality — lane result

**Verdict:**
- **H1 (Mexican-origin neighborhoods worse maintained at equal income, as a *group* effect):**
  **NOT SUPPORTED.** The descriptive pattern is real — the Mission is 0.67 points dirtier
  than Chinatown on the city's 1–5 inspector litter scale despite Chinatown having lower
  income, higher poverty and higher crowding. It fails on both identified designs. In San
  Francisco the association is almost entirely *between* neighborhoods: with 235 census
  tracts and neighborhood fixed effects the Hispanic coefficient drops by two-thirds to
  t = 2.00 and the **Mexican-origin coefficient is not distinguishable from zero (t = 1.53)**.
  Nationally, in AHS 2023 at equal income, tenure, metro and crowding, Mexico-born
  householders are **no more likely to live in physically inadequate housing (t = −0.06)**,
  report **no more abandoned buildings** (slightly fewer, t = −2.52), **no more petty or
  serious crime** (t = 0.62, t = 1.08), and rate their neighborhoods and homes **better**.
  Los Angeles complaint data says no once income enters.
  **What survives:** trash within half a block, +0.87 pp on a 2.5% base for Hispanic
  householders (replicate-weight t = 2.64) and +0.0056 litter points per pp within San
  Francisco neighborhoods (t = 2.00). Not significant for Mexican origin specifically
  (t = 1.72). Litter, slightly — not adequacy, dumping, graffiti or crime.
- **H2 (a large share of Mission storefronts unregistered):** **FALSIFIED.** Mission Street
  90.9% registered against a citywide 83.6%; the Mission neighborhood 89.9% against
  Chinatown 90.5%. The low-registration corridors are Irving, Geary and Clement.

Memo: `research/immigration-enclave-neighborhood-quality-and-informality-2026-09-18.md`
(16 sections, 863 lines). Brief: `BRIEF.md`. The load-bearing sections are **§4** (tract-level
San Francisco) and **§8** (AHS national household test).

## Headline numbers

### San Francisco inspector audit

| Finding | Value |
|---|---|
| Hispanic share → sidewalk litter, 24 neighborhood groups, full controls | +0.019 per pp, t = 5.7 |
| Same at tract level, 235 tracts, tract income | +0.018 per pp, t = 6.1 |
| **Same, plus neighborhood fixed effects** | **+0.0056 per pp, t = 2.00** (0.06 sd per 10 pp) |
| **Mexican-origin share, tract level, neighborhood FE** | **+0.0065, t = 1.53, p = 0.13 — null** |
| Illegal dumping, tract level, neighborhood FE | −0.0006, t = −0.45 |
| Graffiti, tract level, neighborhood FE | +0.30, t = 1.73 (Mexican: t = 0.60) |
| Housing crowding, same specification | +0.0085, t = 1.82 — as strong as Hispanic share |
| Tract poverty rate, same specification | −0.0047, t = −0.96 — wrong sign |
| Residential routes only (neighborhood-level spec) | +0.0115, t = 3.0 |
| Commercial/mixed routes only | +0.0329, t = 6.9 |
| Mission − Chinatown mean sidewalk litter, land-use adjusted | +0.67 on 1–5, t = 7.6 |
| Chinatown − Tenderloin, same | −0.60, t = −5.2 |
| Feces, Hispanic share after street-homelessness control | +0.006, t = 0.6 |
| Chinatown street-cleaning intensity | 12,080 requests/km²/yr, 2nd in SF (Excelsior 2,088) |

### AHS 2023, 55,669 households, weighted, replicate-weight t in bold

| Outcome, Mexico-born householder | Full controls | + crowding | SDR t |
|---|---|---|---|
| Physically inadequate unit | +1.06 pp (t 1.49) | −0.05 pp (t −0.06) | **−0.08** |
| Large amount of trash within ½ block | +1.54 pp (t 2.47) | +1.07 pp (t 1.69) | **1.72** |
| Abandoned buildings, severe category | +0.12 pp (t 0.21) | −0.53 pp (t −0.90) | **−2.52** |
| Bars on windows, severe category | +5.16 pp (t 5.40) | +4.35 pp (t 4.48) | **1.57** |
| Agrees: a lot of petty crime | +0.70 pp (t 0.62) | −1.13 pp (t −0.98) | — |
| Agrees: a lot of serious crime | +0.89 pp (t 1.08) | −0.23 pp (t −0.27) | — |
| Neighborhood rating, 1–10 | +0.173 (t 3.60) | +0.265 (t 5.35) | **5.66** |

| Outcome, Hispanic householder, all origins | Full controls | + crowding | SDR t |
|---|---|---|---|
| Physically inadequate unit | +0.98 pp (t 2.43) | +0.28 pp (t 0.67) | **0.72** |
| Large amount of trash within ½ block | +1.16 pp (t 3.61) | +0.87 pp (t 2.67) | **2.64** |
| Abandoned buildings, severe category | +0.40 pp (t 1.23) | −0.01 pp (t −0.03) | **−0.39** |
| Neighborhood rating, 1–10 | +0.063 (t 2.24) | +0.122 (t 4.22) | **4.24** |

### Complaint measures and H2

| Finding | Value |
|---|---|
| SF 311 cleaning rate, Hispanic share, full controls | t = 0.37 (null) |
| Mission vs Excelsior 311 cleaning per 1,000 residents | 912 vs 195 at 33.0% vs 30.6% Hispanic |
| LA illegal dumping, Hispanic share, raw → +income | t = 5.43 → t = 1.12 |
| LA graffiti, Hispanic share, raw → +income | t = 4.87 → t = 0.32 |
| LA dumping-per-bulky-item ratio, raw → full | +0.0019 (t 2.3) → −0.0024 (t −1.3) |
| Mission St storefront registration | 90.9% (citywide 83.6%) |
| Mission / Chinatown neighborhood registration | 89.9% / 90.5% |
| Lowest corridors | Irving 62.8%, Geary 82.8%, Clement 83.4% |
| Mission Hispanic population 2011 → 2023 | 21,043 → 17,985 (38.1% → 33.0% share) |

## Data used

| Source | ID | Records | Fetched |
|---|---|---|---|
| **AHS 2023 National PUF v1.0 flat CSV** | census.gov www2 | 141,729,433 bytes verified byte-exact; 3,208 columns; **55,669 households** | 2026-09-18 |
| AHS 2023 National PUF v1.1 (version check only) | same | 3,214 columns, same 55,669 rows, identical distributions on all variables used | 2026-09-18 |
| AHS 2023 Mini Codebook + Definitions + Items Booklet | census.gov | variable wording and response structure | 2026-09-18 |
| SF Street & Sidewalk Maintenance Standards (inspector audit) | `qya8-uhsz` | 7,318 evaluations, Jan 2022 – Jun 2025 | 2026-09-18 |
| Route-centroid coordinate crosswalk (attachment to the above) | asset `25469601-…` | 3,474 routes; 99.6% of evaluations matched to a tract | 2026-09-18 |
| SF 311 cases | `vw6y-z8j6` | 8,923,552; aggregated by neighborhood × service × year 2015–2025 | 2026-09-18 |
| SF Registered Business Locations (active) | `g8m3-pdis` | 99,106 | 2026-09-18 |
| SF Taxable Commercial Spaces (vacancy tax) | `rzkk-54yv` | 21,870 rows; 5,223 distinct 2024 parcel-spaces | 2026-09-18 |
| SF tent/structure/vehicle count | `w9ip-yrij` | 13,111 observations, 31 quarters 2019-04 → 2026-05 | 2026-09-18 |
| SF 2020 / 2010 tracts → Analysis Neighborhoods | `sevw-6tgi` / `m46u-xzix` | 242 / pre-2020 series | 2026-09-18 |
| MyLA311 | `pvft-t768` `rq3b-xjk8` `97z7-y5bt` `i5ke-k6by` `4a4x-mna2` `b7dx-7gc3` `h73f-gn57` | 2019–2025, by ZIP and by neighborhood council | 2026-09-18 |
| ACS 2019–23 5-year, SF tracts / LA ZCTAs | Census API | 244 tracts / 148 ZCTAs | 2026-09-18 |
| ACS 5-year 2011–2023, SF tracts | Census API | Hispanic share series | 2026-09-18 |

## Verification commands

```bash
cd /Users/alien/Projects/immigration-research/infra/immigration-fiscal/enclave_quality_2026_09_18
UV='uv run --no-project --with pandas>=2 --with numpy>=2 --with statsmodels'

# DECIDING TEST 1 (tables 22-23): SF tract-level, with and without neighborhood FE
$UV --with shapely --with openpyxl python3 sf_tract_level_test.py

# DECIDING TEST 2 (tables 18-21): AHS 2023 national household test, in a container
modal run --detach modal_ahs_run.py      # regressions + SDR errors + income bands
modal run --detach modal_ahs_codes.py    # empirical code ordering + signed re-run
grep -E "downloaded bytes|header column count|weighted Hispanic" ahs_run_log.txt
# expect: 141729433 MATCH / 3208 (expected 3208) / 13.57% (ACS benchmark ~14%)

# H1, neighborhood-level audit (tables 1-3, 8-10, 15-16)
$UV python3 sf_quality_analysis.py
$UV python3 sf_quality_robustness.py
$UV python3 sf_quality_robustness2.py

# H1, complaint measures (tables 4-5, 12-14)
$UV python3 sf_311_analysis.py
$UV python3 la311_analysis.py

# H2 (tables 6v2, 7v2, 17). v2 is the correct denominator; v1 is circular.
$UV python3 h2_storefront_registration_v2.py
$UV python3 h2_match_sensitivity.py

# Gentrification series (table 11)
uv run --no-project --with pandas>=2 --with requests python3 sf_hispanic_series.py

# Local AHS runner, if the 141,729,433-byte file is ever on disk
$UV python3 ahs_analysis.py
```

Re-fetching raw data: `sf311_pull.py`, `sf_streeteval_pull.py`, `sf_business_pull.py`,
`sf_storefront_pull.py`, `la311_pull.py`, `acs_sf_neighborhoods.py`, `acs_zcta_la.py`,
`sf_geo_context.py` (needs `shapely`).

## Corrections made inside this lane

1. **The H1 verdict was reversed twice, both times by a better design.** The
   neighborhood-level analysis (§3) supported H1 and was written up that way. Adding route
   coordinates and neighborhood fixed effects (§4) cut the estimate by two-thirds and nulled
   the Mexican-origin coefficient. The AHS national test (§8) then found unit adequacy flat
   at equal income. Superseded verdict text is in git history.
2. **H2 denominator was circular in my first pass.** The vacancy registry's `lin` is derived
   from the business tax account number (`lin` = `<ban>-NN-NNN`), so restricting to rows with
   a `lin` conditions on a business account existing. Measured circularity: 90.7%
   registration among occupied spaces with a `lin` versus 77.4% without. `v2` uses the parcel
   universe. Headline numbers changed (Mission 85.3% → 90.9%, citywide 80.1% → 83.6%); the
   H2 verdict did not.
3. **`filed` is not an independent compliance measure.** In tax year 2024 it is perfectly
   collinear with having a `lin` (both 47.9%). Dropped.
4. **The brief's AHS variable names were partly wrong.** The litter, abandoned-buildings and
   bars-on-windows items are `NEARTRASH`, `NEARABAND`, `NEARBARCL`, not
   `NHQTRASH`/`NHQABAN`/`NHQBAN`. The `NHQ*` names for crime, schools, transit and risk are
   correct. Verified against the real 3,208-column header.
5. **The `NEAR*` response scales are not yes/no, and code 1 is not always the severe
   category.** They are frequency and count scales. Order was established empirically from
   the weighted mean of `RATINGNH` within each category: severe is code **1** for
   `NEARTRASH` but code **2** for `NEARABAND` and `NEARBARCL`. A naive `== 1` indicator, which
   my first AHS pass used, measured the wrong group for two of three items.
6. **`NHQ*` polarity differs by item.** `NHQSCHOOL` and `NHQPUBTRN` are positive amenities
   ("has good schools", "has good bus, subway, or commuter train service"), not problems. The
   first pass named them `school_problem` and `transit_problem`, which inverted their
   meaning; the large Mexico-born transit coefficient (+12.4 points) is a *positive* amenity
   finding.
7. **Central American ACS variable.** `B03001_007` is Dominican, not Central American;
   `B03001_008` is Central American. Fixed in `acs_sf_neighborhoods.py`.

## How the AHS download was resolved

The local outbound link was saturated for the whole lane: Census served fresh range requests
at 17–27 kB/s and an unrelated control host at 1.6 kB/s. A local resume lost ground twice
(92.5 MB → 82.6 MB) because the transfer was restarting rather than resuming. On the
parent's instruction the file was downloaded and analysed in a Modal CPU container, which
returned only the result tables — option (b), since shipping 141 MB back over the same link
was the slow half. The container verified the byte count, that the zip opens, and the
3,208-column header before doing anything else. Two runs: `modal_ahs_run.py` for the
regressions, replicate-weight errors and income bands, and `modal_ahs_codes.py` for the
empirical code ordering and the correctly-signed re-run.

## Covered / skipped

**Covered.** All three designs in the brief. Design 1 (national equal-income test) with AHS
2023 microdata, weighted, with replicate-weight standard errors and a v1.0/v1.1 version
check. Design 2 for San Francisco with a better instrument than the brief specified (the
Controller's random-sample inspector audit rather than 311 alone) plus a tract-level join the
brief did not ask for and that decided the question; and for Los Angeles by ZIP and by
neighborhood council. Design 3 with a better denominator than OpenStreetMap. Gentrification
steel-man with the ACS Hispanic-share series 2011–2023. Enclave literature
(Cutler–Glaeser–Vigdor 2008, Edin–Fredriksson–Åslund 2003). Crowding by neighborhood and by
tract via `B25014`.

**Skipped, with reasons.**
- **East Los Angeles.** Unincorporated Los Angeles County, so absent from MyLA311 entirely.
  Not testable with this data; ZIP 90063 is the nearest city-side proxy.
- **AHS metropolitan PUF, metro-by-metro estimates.** Would test whether the national null
  hides offsetting positives across the 35 identified metros. Not run. **[GAP]**
- **OpenStreetMap storefront counts via Overpass.** Superseded by the vacancy-tax registry,
  an administrative census of storefronts rather than a volunteer map. Not run.
- **CDTFA seller's-permit counts by ZIP.** Not published at that granularity in a public API;
  not pursued once the registry gave a direct answer.
- **California LETF / EDD underground-economy reports.** Read. They report >80%
  non-compliance on *targeted* inspections of suspected violators in car washes, restaurants,
  garment manufacturing, roofing, construction, agriculture and auto repair. That is a hit
  rate on a selected sample with no neighborhood or ethnicity base rate, so it can neither
  support nor refute H2, and is reported as such.
- **LA CleanStat** — the observational analogue of the SF audit. Not on data.lacity.org;
  needs a records request. Highest-value remaining item for an out-of-sample test of the
  between-neighborhood result. **[GAP]**
- **A design separating neighborhood-scale group mechanisms from municipal service
  geography.** A Community Benefit District boundary discontinuity is the obvious candidate.
  This is the one live objection to the verdict and it is not answerable with these data.
  **[GAP]**
- **DBI code-enforcement complaints per housing unit** (`gm2e-bten`). Not pulled; 311 already
  carries a building-request category and the audit is the stronger instrument.

## Do not

Nothing was committed. Raw pulls and downloaded documentation are cached under `_cache/` and
are untracked. `ahs_analysis.py` reads the v1.0 archive at
`sources/immigration-fiscal/data/external/ahs_2023/ahs2023_flat_v1_0.zip`.
