claude-opus-5-5

**Verdict:** The land under US public K-12 schools is worth about **$627bn in 2024** at the central price,
arm B: FHFA's residential land price per acre with the developable-share discount [CALCULATION:
derived/summary.json `arms.B`]. That is **0.235 of BEA's $2,663.9bn K-12 structures**. Arm A, every acre at
the residential price, gives $958bn (0.360); arm C, vacant-land plattage, gives $96bn (0.036). The
Mexican-origin group's pupils enroll where land is dearer (where-enrolled ratio 1.142). At the case rate of
2.081%, the group's annual charge is **$2.61bn where enrolled** ($2.28bn at the 0.17481 pupil share): **0.71%
of $368.0bn and 0.60% of $436.6bn**. Beside it, arm A gives $4.00bn and arm C $0.38bn. At 3% and 7%, arm B
gives $3.76bn and $8.76bn where enrolled. The acreage comes from OSM-derived campus polygons that cover 73.5%
of schools and 81.3% of pupils; CA is at 83.5%/89.4% and TX at 79.2%/88.5%. California parcel data put the
lane's acreage 11% low in total; the campus-level median ratio is 0.99. Where that shortfall holds
nationally, arm B rises to $755bn and $3.10bn. The charge sits beside the case, not adopted.

Lane `school_land_2026_10_24`, run by claude-opus-5-5 on 2026-10-24 ([brief](BRIEF.md),
[README](README.md) for run commands and inputs). Rerun: `scripts/rerun_lane.py`, IDENTICAL 15/15, exit 0;
pytest 9/9.

## 1. Results

| Arm | National land, $bn | Per pupil, $ | Land / K-12 structures | Where-enrolled ratio | Group charge at 2.081%: pupil share / where enrolled, $bn | Share of headline (where enrolled) | 3% / 7% where enrolled, $bn |
|---|---:|---:|---:|---:|---:|---:|---:|
| A residential, all acres | 958.2 | 20,266 | 0.360 | 1.146 | 3.49 / 4.00 | 1.09% / 0.92% | 5.76 / 13.44 |
| **B developable share (central)** | **626.9** | **13,258** | **0.235** | **1.142** | **2.28 / 2.61** | **0.71% / 0.60%** | **3.76 / 8.76** |
| C vacant-land plattage (AES 2018) | 95.9 | 2,029 | 0.036 | 1.086 | 0.35 / 0.38 | 0.10% / 0.09% | 0.55 / 1.28 |
| D FHFA county lot-size elasticity (beside) | 54.9 | 1,161 | 0.021 | 1.159 | 0.20 / 0.23 | 0.06% / 0.05% | 0.33 / 0.78 |

[CALCULATION: derived/arms.csv, derived/summary.json]. The per-pupil figures divide by 47.28m K-12 pupils in
non-virtual schools. Each headline share is the charge over $368.0bn and over $436.6bn
(`main_case_2026_10_16` `v9.band_bn`). The group's charge on structures at the pupil share and the case rate is
$9.69bn (s × $2,663.9bn × 2.081%). Arm B's land adds 23.5% to it. That agrees with the capital-return lane's
rule of thumb: each 10% of land/structures adds $0.93bn at 2% (`school_capital_return_2026_09_26/RESULT.md`
§Land).

**Where the value sits.** Under arm B, California holds $221.9bn (35%) and New York $113.4bn (18%; Manhattan
alone is about $78bn). California holds 31% of the group's pupils and New York 1.4%. Both effects explain why
the where-enrolled ratio is only 1.14. California's dear land pushes the group's share up, while Manhattan,
where few group pupils enroll, pulls it down. Without Manhattan (county 36061) the ratio is 1.234, but the
group charge falls to $2.46bn because the national total drops to $548.9bn [CALCULATION:
`sensitivities_B.excluding_manhattan_36061`]. FHFA's FAQ flags Manhattan's land values as extreme
[DATA: _cache/fhfa/faqs.txt].

### Sensitivities on arm B

| Change | National, $bn | Land / structures | Group charge where enrolled, $bn |
|---|---:|---:|---:|
| Central | 626.9 | 0.235 | 2.61 |
| Acreage calibrated to CSCD (polygons ×1.160, imputed ×1.349) | 755.0 | 0.283 | 3.10 |
| Hispanic weights in place of the Mexican-origin share | 626.9 | 0.235 | 2.89 |
| Inside-polygon matches only (near matches imputed) | 640.0 | 0.240 | 2.64 |
| Excluding charter schools (7,719 schools, 54.3k acres, $44.3bn) | 582.6 | 0.219 | 2.45 |
| Excluding Manhattan | 548.9 | 0.206 | 2.46 |
| No 2022→2024 HPI carry-forward | 564.4 | 0.212 | 2.38 |
| Tract-priced schools only (subset total) | 453.0 | 0.170 | 1.92 |

[CALCULATION: derived/summary.json `sensitivities_B`]. Every variation keeps the charge within $1.9–3.1bn.
The price arm moves it far more than any of them: $0.38bn to $4.00bn.

## 2. Method

1. **Schools.** The universe is 99,297 operating CCD schools in 2023-24 in the 50 states and DC, with EDGE
   points and 052 membership aggregated by the where-enrolled lane's own `_aggregate`. The 1,232
   exclusively virtual schools carry no land, which leaves 98,065 schools and 47.28m K-12 pupils
   [DATA: NCES EDGE/CCD 2023-24].
2. **Campuses.** Overture 2026-10-21.0 land-use polygons (from OSM): 88,999 school, 3,298 kindergarten and
   2,471 schoolyard polygons, merged by union-find when they intersect, with geodesic area. The 1,203
   `landuse=education` polygons are a fallback only [DATA: _cache/overture].
3. **Matching.** A school matches a campus whose polygon contains its point, else the nearest campus within
   60 m, else one within 200 m that shares a distinctive name token. Campuses tagged private or religious
   are excluded. Several schools on one campus split it by K-12 pupils. Matches: 71,110 inside, 713 near,
   265 near by name, for 72,088 (73.5% of schools, 81.3% of pupils). The median matched site is 11.0 acres.
4. **Unmatched schools.** Acreage comes from a log-acres regression on sole-occupant matched schools, with
   level, type, charter, log pupils, NCES locale and state as regressors (n 46,840, R² 0.510, Duan smearing
   factor 1.219). The imputation gives 0.320m of the 1.467m acres.
5. **Price.** Each site takes its 2010 tract, priced by FHFA WP 19-01 v4.0 as-is residential land value per
   acre (pooled cross-section, 2015 prices). Missing tracts fall back to county, then state; by acres,
   82.6% are priced at tract, 14.6% at county and 2.8% at state level. Prices are carried to 2022 by the
   county (else state) panel ratio of land per acre 2022/2015 (county median 1.525), and to 2024 by FHFA's
   annual county all-transactions HPI 2024/2022 (median 1.14). The acre-weighted 2024 price is $653k per
   acre [DATA: FHFA WP 19-01 v4.0; FHFA county HPI].
6. **Arms.**
   - A applies the price to every acre.
   - B applies it to 65% of a site over 2 acres and 80% of one under 2.
   - C applies the Albouy–Ehrlich–Shin plattage cubic in log lot size, from the tract's average residential
     lot to the site's acreage.
   - D values a standardized quarter-acre at FHFA's own price and scales it by the county's lot-size
     elasticity bL, capped at A.
7. **Group.** The group's pupils take the where-enrolled lane's district weights (Hispanic K-12 pupils ×
   the district's raked Mexican share), carried to schools by Hispanic K-12 pupils. That gives 8.592m
   against the lane's 8.643m. The where-enrolled ratio is the group's pupil-weighted land per pupil over
   the national average.

## 3. Why arm B is central

The question is what a school site would fetch if it were not a school. Its alternative use is mostly
residential redevelopment. School sites are large: the median is 11 acres. A buyer of a large parcel
gives up land for streets, drainage and open space, so per acre it pays less than the price of built
house lots.

- **Arm B prices that loss directly.** Gyourko & Krimmel (2021, NBER w28993, note 13 and p. 16) take NAHB's
  rule that "no more than 65% of a large parcel can be used for housing", and 80% for parcels under two
  acres. For the smaller parcels they say "we do not have hard data" [SOURCE: corpus
  doi_10_3386_w28993, page.md lines 155, 177].
- **Priced parcels support B over C.** G&K describe four vacant parcels sold in 2013–2018 for single-family
  development. Each parcel's price per acre, over FHFA's county as-is price per acre (2013 and 2018 panel
  values), is:
  - Cobb 54.5 acres: 0.61–0.86;
  - Marin 3.9 acres: 0.85–1.35;
  - Alameda 10.2 acres: 0.55–1.04;
  - Fulton 9.9 acres: 0.18–0.27.

  The median of the midpoints is 0.76. Arm B's factor is 0.65 for all four; arm C's plattage factors for
  these parcels are 0.05–0.24, and only Fulton sits near them [CALCULATION: derived/discount_evidence.csv;
  parcel sizes and prices checked against the parsed paper]. Three of four parcels sold at 5–14 times what
  arm C predicts.
- **Arm C carries a different discount.** AES's cubic measures how land's price per acre falls with lot
  size across every CoStar land sale without a structure in metro areas, 2005–2010, whatever the proposed
  use [SOURCE: corpus doi_10_1162_rest_a_00710, p. 2 and Table A.1]. Applied from a house lot to an
  11-acre site, it removes about 90% of the price (C/A = 0.10 nationally). That is more than the
  developer-sale evidence supports. It stays as the lower reference.
- **Arm D extrapolates out of sample.** FHFA's bL is estimated on house lots, mostly under one acre, and
  arm D applies it at 11 acres. It stays beside.
- **Arm A is the ceiling.** It assumes every acre is a buildable residential lot.

Four parcels are thin evidence, and arm B's 65% is a subdivision rule, not a measurement on school sites.
Some sites could be rezoned for denser uses, which would raise the value. Others hold floodplains, fields
or deed restrictions, which would lower it.

## 4. Validation: California School Campus Database 2025

The California School Campus Database (CSCD) 2025, from GreenInfo Network, traces public-school campuses on
assessor parcels: 8,545 properties and 133,602 acres [DATA: _cache/bench_cscd, FeatureServer layers 0 and
2]. It is independent of OSM.

| Check | Result |
|---|---|
| Lane's California acreage over CSCD's total | 119,048 / 133,602 = **0.891** |
| Campus level, matched schools (n 6,954): median ratio | **0.990** |
| Mean absolute log error | 0.178 |
| Share within 25% | 79.8% |
| Sum ratio | 0.862 |
| Sole occupants (n 5,734): median / sum ratio | 0.991 / 0.889 |
| Imputed schools (n 769): median / sum ratio | 1.086 / 0.741 |

[CALCULATION: derived/validation_cscd_ca.csv, summary.json `validation`]. The typical campus is right. The
total is short because OSM polygons miss parts of large campuses: athletic fields, bus yards, the second
parcel. The imputation is also short on large sites, so the shortfall falls on the biggest and often the
cheapest-per-acre land. The calibrated sensitivity applies California's factors nationally, which assumes
OSM's coverage elsewhere resembles California's. That assumption is untested, and in low-match states such
as AR, MS, KY and OK it is probably worse.

## 5. Coverage by state

`derived/by_state.csv` has all 51 rows.

- **Lowest school match rates:** AR 42.5%, MS 45.2%, KY 47.8%, OK 48.1%, NJ 49.0% and TN 50.3%; their pupil
  rates are 49–60%.
- **Highest:** VT 99.3%, ME 96.3%, CT 96.2%, IA 94.8%.
- **The group's two main states:**
  - CA: 8,581 of 10,271 schools matched (83.5%; 89.4% of pupils); 14.3k of 119.0k acres imputed.
  - TX: 7,279 of 9,191 matched (79.2%; 88.5%); 22.4k of 151.2k acres imputed.

The low-match states hold cheap land and few group pupils, so their imputation error barely moves the
group charge.

## 6. Confounders and limits

- **Acreage understatement.** The California benchmark puts polygons 14% low and imputation 26% low in sum.
  If that holds nationally, the central is about 20% low ($3.10bn). Gates: median ratio within 0.9–1.1,
  mean absolute log error ≤ 0.25, California total within 0.8–1.2.
- **One benchmark state.** No other state's official inventory with per-site acreage was found in this
  pass; Florida's FISH reports carry none.
- **Land price vintage.** FHFA's tract prices are a 2012–2019 pooled cross-section at 2015 prices. They are
  carried to 2024 by the land panel to 2022, then by the house-price index, which may move differently from
  land. Without the 2022→2024 step, the charge is $2.38bn.
- **Price extremes.** Manhattan's roughly $105m per acre is consistent with its land market, but it holds
  12% of arm B's national value.
- **Charters.** Charter schools that lease their buildings already pay land rent through current spending,
  which the account counts. That part may be counted twice; excluding all charters gives $2.45bn.
- **Near matches.** A near match may land on a neighbouring private school or park. Inside-polygon matches
  only give $2.64bn.
- **Group proxy.** The district Mexican-origin share is a raked proxy carried to schools by Hispanic pupils
  (the where-enrolled lane's caveat). Hispanic weights instead give $2.89bn.
- **Removal response.** The charge prices the group's share of existing land at the average. Whether
  districts would sell land if the group were gone is the same question as for structures, and this lane
  does not answer it [FRAMING-SENSITIVE].
- **Rate.** Land does not depreciate, so the annual charge is rate × value. The case's rate is the
  Trustees' flat-equivalent real rate (item 20); 3% and 7% are beside.

## 7. Sources

- [DATA] NCES EDGE public-school geocodes 2023-24 and CCD 2023-24 files 029, 052 and 129; URLs and sha256 in
  `derived/acquired_sources.json`.
- [DATA] Overture Maps Foundation, release 2026-10-21.0, `theme=base/type=land_use`, remote parquet.
- [DATA] Larson, Shui, Davis & Oliner, "The Price of Residential Land for Counties, ZIP codes, and Census
  Tracts in the United States", FHFA Working Paper 19-01, data version 4.0 (June 2024).
- [DATA] FHFA House Price Index, annual county all-transactions, last updated 2026-03-31.
- [DATA] US Census Bureau, 2010 cartographic boundary tracts (500k) and 2010/2020 tract gazetteers.
- [DATA] GreenInfo Network, California School Campus Database 2025, ArcGIS FeatureServer.
- [SOURCE] Albouy, D., Ehrlich, G., & Shin, M. (2018). Metropolitan land values. *Review of Economics and
  Statistics*, 100(3), 454–466. Table A.1, read in the parsed full text (corpus doi_10_1162_rest_a_00710).
- [SOURCE] Gyourko, J., & Krimmel, J. (2021). The impact of local residential land use restrictions on land
  values across and within single family housing markets. NBER Working Paper 28993. Read in the parsed full
  text (corpus doi_10_3386_w28993).

## Log (append-only; times from `date`)
- 2026-10-24 00:34 Sources probed: FHFA land prices v4.0 (June 2024; tract pooled cross-section at 2015 prices, panel 2012–2022, county plattage elasticities) downloaded; Overture 2026-10-21.0 base/land_use (32 files, 18.9 GB) queried remotely; NCES EDGE 2023-24 geocodes and CCD 2023-24 school files to fetch.
- 2026-10-24 01:18 Inputs in place: EDGE 2023-24 points + CCD 029/052/129 (99,297 operating schools, 47.84m K-12 pupils, 14.13m Hispanic); FHFA tracts are 2010 tracts (99.97% of 54,515 match the 2010 gazetteer, 85.7% the 2020 one), so 2010 cartographic tracts were fetched; Overture pull: 88,999 school + 3,298 kindergarten + 2,471 schoolyard + 1,203 education polygons in the US boxes (UNION ALL per box; an OR of boxes defeated row-group pruning). Validation benchmark: California School Campus Database 2025 (GreenInfo; parcel-aligned; 8,545 properties, 133,602 acres, median 10.0). Discount evidence read: Albouy, Ehrlich & Shin (2018) Table A.1 vacant-land plattage cubic; Gyourko & Krimmel (2021, NBER w28993) on 65% developable share of large parcels (NAHB).
- 2026-10-24 01:33 First full build (checkpoint, not final): matched 73.5% of 98,065 non-virtual schools (81.3% of pupils); 1.147m polygon acres + 0.320m imputed. National land: A residential $958bn, B developable share $627bn, C vacant-land plattage $96bn; land/K-12 structures 0.36 / 0.235 / 0.036; where-enrolled ratio 1.09–1.15. Group charge at the case rate (where enrolled): A $4.00bn, B $2.61bn, C $0.38bn. California vs CSCD: lane total 0.891 of CSCD acres; campus-level median ratio 0.99; imputed schools 0.74 of their CSCD acres.
- 2026-10-24 01:39 Final: G&K parcel table added (`discount_evidence.csv`; parcel sizes and prices checked against the parsed paper; median price/FHFA county 0.76, arm C factors 0.05–0.24), so B is central. pytest 9/9; `rerun_lane.py` with five commands IDENTICAL 15/15, exit 0. README and verdict written. Not committed; the parent reviews.

## Reviewer note

- 2026-10-24 01:42 JST: the group charge uses pupil share 0.1748 × 1.142. The case keys K-12 capital at
  0.17724, or 0.193 effective once completion, coverage and count parts are included
  (`school_capital_where_enrolled_2026_10_24/derived/case_base.json`). On adoption, land must take the same key and
  where-enrolled factor as structures. That adds roughly 10% to the charge (B ≈ $2.8–2.9bn); not re-derived here.
