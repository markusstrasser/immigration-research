claude-opus-5-5[1m]

**Verdict:** The shared crosswalk `derived/geo_county_cbsa_2013.csv` now has nine rows for Connecticut's 2022 planning regions (09110–09190). The 1,882 existing rows are unchanged byte for byte. Each region takes the 2013 CBSA row (code, title and `is_metro` copied from the old-county row) that holds the majority of its 2020 population. The mapping is built from whole towns, using the Census Bureau's town → old county / planning region crosswalk and 2020 Census town populations. The majority is 65.4% for Naugatuck Valley and at least 89.8% for the other regions. Overall, 6.5% of the state's population sits outside its region's assigned CBSA. The largest dollar change anywhere is **+$0.60bn in a stock**: the construction lane's owners' value offset in C_price_all, low, metro-local ($2,368.96bn → $2,369.56bn). The largest change in an annual flow is **+$0.011bn**: landlords' welfare gain in the housing lane's short-run high, form C, metro-local cell ($192.960bn → $192.971bn). The main flow headlines move by $0.002–0.008bn: the housing long-run central renters' extra rent goes from $33.856bn to $33.859bn, and the short-run central from $110.414bn to $110.422bn. Every figure in the lanes' verdict paragraphs is unchanged at its printed precision. Eleven dollar figures printed in tables or body text across four RESULTs change in their last digit, all by rounding across a boundary. They are listed below and in each lane's `## Revisions` line. Replaying each changed consumer on the old crosswalk reproduced its committed outputs byte for byte, so every change reported here comes from the Connecticut rows alone. [CALCULATION: `src/build_geo.py`; consumer reruns listed below] Date: 2026-09-23. Nothing committed.

## Mapping

Sources, saved under `_cache/` (ignored) and cited in `src/build_geo.py`:

- Town → old county and planning region: Census Bureau, <https://www2.census.gov/geo/docs/reference/ct_change/ct_cou_to_cousub_crosswalk.txt> (`ct_cou_to_cousub_crosswalk.txt`; the `.xlsx` twin is also cached, unused). [SOURCE]
- Town population: 2020 Census PL 94-171 `P1_001N` by county subdivision, on old-county geography, <https://api.census.gov/data/2020/dec/pl?get=NAME,P1_001N&for=county%20subdivision:*&in=state:09%20county:*> with a key (`ct_cousub_pop2020_pl.json`). [DATA]

Both regions and old counties are unions of whole towns, so the town join is exact. The water rows ("County subdivisions not defined") have zero population and are dropped. [DATA]

| Region | Name | 2020 pop | CBSA | Title | is_metro | Inside | Outside | Where the outside share lives |
|---|---|---:|---|---|---:|---:|---:|---|
| 09110 | Capitol | 976,248 | 25540 | Hartford-West Hartford-East Hartford, CT | 1 | 100.0% | 0.0% | — |
| 09120 | Greater Bridgeport | 325,778 | 14860 | Bridgeport-Stamford-Norwalk, CT | 1 | 100.0% | 0.0% | — |
| 09130 | Lower Connecticut River Valley | 174,225 | 25540 | Hartford-West Hartford-East Hartford, CT | 1 | 94.3% | 5.7% | Norwich–New London 5.7% |
| 09140 | Naugatuck Valley | 450,376 | 35300 | New Haven-Milford, CT | 1 | 65.4% | 34.6% | Hartford 13.5%, Torrington 12.1%, Bridgeport 9.1% |
| 09150 | Northeastern Connecticut | 95,348 | 49340 | Worcester, MA-CT | 1 | 96.5% | 3.5% | Norwich–New London 2.7%, Hartford 0.8% |
| 09160 | Northwest Hills | 112,503 | 45860 | Torrington, CT | 0 | 89.8% | 10.2% | Hartford 10.2% |
| 09170 | South Central Connecticut | 570,487 | 35300 | New Haven-Milford, CT | 1 | 100.0% | 0.0% | — |
| 09180 | Southeastern Connecticut | 280,430 | 35980 | Norwich-New London, CT | 1 | 91.3% | 8.7% | Worcester 8.7% |
| 09190 | Western Connecticut | 620,549 | 14860 | Bridgeport-Stamford-Norwalk, CT | 1 | 95.2% | 4.8% | Torrington 4.8% |

About 234,985 of 3,605,944 people (6.5%) live outside their region's CBSA. Northwest Hills maps to the Torrington micropolitan area. Consumers that keep only `is_metro == 1` therefore leave it in `nonmetro_09`, as the 2013 delineation treats Litchfield County. [CALCULATION]

The file has these controls:

- **Town matching.** All 169 towns match one to one.
- **County totals.** Town sums reproduce the eight 2020 county totals from the same API exactly.
- **Geocorr check.** The Geocorr `pop20` in `employment_entry_2026_09_18/_cache/xwalk_puma22.csv`, summed by region, matches five regions exactly. It is 146–1,878 persons above the town sums in the other four (09110, 09140, 09170, 09180), at most 0.42%.

`src/build_geo.py` stops with `[BLOCKED]` under any of these conditions:

- a town fails to match;
- a water row has population;
- a region has no CBSA above 50%;
- a region code is already in the 2013 list.

Rerunning it gives an identical file.

The new rows are inserted in sorted position after 09015, which keeps the builder's "every output is sorted" contract. They are not appended at the end of the file. `git diff` shows 9 insertions and 0 deletions. The new file with the nine rows removed has the old md5, 5d0f3252. [CALCULATION]

The labor-mobility lane's `metro_panel.py` carries its own lane-local `CT_REGIONS` dictionary. It agrees with this mapping on all eight metro regions and omits 09160, which is micropolitan. That lane was not run or edited.

## Inert for old-county consumers (hedonic lane)

The steps were run in this order: a before-snapshot in its own call; `build_geo.py` (rc 0, run twice with identical output); `build_panel.py` (rc 0); `zillow.py` (rc 0); then an after-snapshot.

| File | Before md5 | After md5 |
|---|---|---|
| `geo_county_cbsa_2013.csv` | 5d0f3252 | ca42f783 (+9 rows) |
| `geo_tract2010.csv` | 287259bb | 287259bb |
| `geo_tract20_to_tract10.csv` | b5df2393 | b5df2393 |
| `build_panel_report.txt` | fee8cfda | fee8cfda |
| `tract_panel.csv` (ignored) | 58e05752 | 58e05752 |
| `zcta_panel.csv` (ignored) | 690bc3f7 | 690bc3f7 |
| `results_zillow.csv` | c6197a82 | c6197a82 |

The other 12 files in `derived/` are unchanged. `build_panel.py` keys counties on 2010 tract GEOIDs, and `zillow.py` keys them on the 2010 ZCTA–county file. Both use old CT counties only.

## Consumers (all rc 0; run from the repository root)

**Attribution.** `housing_transfer/arms.py`, `construction/metro.py` + `supply.py`, `care/hours_tax.py` + `summary.py` and `distribution/distribute.py` were each replayed into a scratch directory with the old crosswalk. The distribution replay also used the housing lane's old outputs. Every replay reproduced the committed outputs byte for byte, so there is no upstream drift. [CALCULATION]

**Tests.** The lane tests pass: `housing_transfer/test_arms.py` 5, `congestion/test_arms.py` 11, `construction/test_supply.py` 6.

### housing_transfer_2026_09_23/arms.py

Changed: `arms_grid.csv` d3a83e44→bf884dfe, `arms_headline.csv` cd1a9b04→2f3ce555, `arms_summary.csv` 4df9a37c→a57f4eb4, `cbsa_exposure.csv` abb1450e→4a8a833c, `checks.json` 2812b4c3→0561f4fa. The other 10 files are unchanged.

**Areas.** There are 428 areas, up from 424. Metros go 377 → 381. `nonmetro_09` falls from 3,675,069 to 114,159 persons (saiz_source `none`). New rows:

| Area | Persons | Group share | Saiz |
|---|---:|---:|---|
| 14860 Bridgeport–Stamford | 972,324 | 2.14% | none |
| 25540 Hartford | 1,168,185 | 1.20% | 1.496 (`causal_lane_code`) |
| 35300 New Haven | 1,039,125 | 2.41% | 0.975 (`causal_lane_code`) |
| 35980 Norwich–New London | 282,750 | 2.20% | none |

Worcester goes from 881,831 to 980,357 persons, with no Saiz elasticity before or after.

**Saiz matches.** Matched areas go 225 → 227, covering 84.4% → 85.1% of other renters' rent. The fill elasticity is 0.5209 before and after.

Only two of the five metros touching Connecticut now carry Saiz elasticities. `housing_causal_2000_2010_2026_09_22/derived/metro_housing_panel.csv` has rows for 14860, 35980 and 49340 but no elasticity for them, because that lane's name match misses them. They take the fill value in the Saiz-local arm. This was not fixed; it lies outside the assigned files.

Headline rows, metro-local geography, $bn/yr:

| Arm | Other renters' extra rent | Welfare net | Owners' stock |
|---|---:|---:|---:|
| Long run, low | 22.146 → 22.148 | 2.301 → 2.301 | 1,263.83 → 1,263.88 |
| **Long run, central** | **33.856 → 33.859** | 3.508 → 3.508 | 1,931.57 → 1,931.64 |
| Long run, high | 50.067 → 50.071 | 5.168 → 5.168 | 2,855.31 → 2,855.41 |
| Short run, central | 110.414 → 110.422 | 10.314 → 10.314 | 6,287.76 → 6,288.01 |
| Short run, high | 137.976 → 137.986 | 12.931 → 12.931 | 7,852.90 → 7,853.22 |
| Saiz-local long run | 45.301 → 45.306 | 4.642 → 4.642 | 2,594.22 → 2,594.45 |

- **Other changes.** Frame and welfare nets move by under $0.001bn everywhere. One grid cell's welfare net (short run, high, form C, high ownership) rounds from 11.04 to 11.03.
- **National-uniform rows.** These are unchanged (max difference 9e-13).
- **Extra rent per native-head renter household.** Long-run central: $834.91 → $834.96.

### congestion_2026_09_23/arms.py

Changed: `cbsa_commute.csv` 3304a6ae→7b8b4c8a. The other 16 files are byte-identical, including `arms_grid`, `arms_summary`, `checks`, `metro_distribution`, `ua_exposure`, `parameters` and `vot_2024`. The urban-area headline is therefore unchanged. So are the inputs that `ancestry_iv/estimate_commute.py` imports from this lane.

In `cbsa_commute.csv`, areas go 424 → 428. `nonmetro_09` other residents fall from 3,610,346 to 113,961. Four rows are added: Hartford (1,154,614 other residents), New Haven (1,015,007), Bridgeport–Stamford (952,276) and Norwich–New London (276,752). Worcester's other residents go from 872,194 to 969,930.

### construction_housing_supply_2026_09_23/metro.py → supply.py

Changed: `construction_metro.csv` 695f776d→3545337e, `supply_checks.json` e4271b31→5cfe28fa (only `areas` 424→428), `supply_grid.csv` 8ddde856→c4fa9e94, `supply_headline.csv` badc5e45→6c28fa03. The other 7 files are unchanged: `supply_premium_incidence`, `supply_monras_transport`, `supply_parameters`, `inputs_bea`, `construction_national`, `construction_puma` and `tabulate_checks`.

- **Central case (§4.1).** It uses uniform geography and is unchanged: **$29.91bn after the $3.56bn offset**. All national-uniform rows differ by at most 1e-14.
- **Metro-local A_central.** Demand-only rent goes $33.856bn → $33.859bn. With supply, $30.414bn → $30.416bn. The offset goes $3.442bn → $3.443bn.
- **Largest flow change.** +$0.009bn, in C_price_all, low, metro-local: $42.573bn → $42.582bn.
- **Largest stock change.** +$0.60bn, in the owners' value offset for the same cell: $2.36896tn → $2.36956tn. This is the largest dollar change anywhere. It moves the printed C_price_all owners' range from 2.01–2.41 to 2.02–2.41.
- **Connecticut trades rows.** Bridgeport's union share of construction-trades earnings is 6.0%, Hartford's 0.9%, New Haven's 6.3% and Norwich's 2.7%. Before the fix, Connecticut was a single `nonmetro_09` row at 3.8%.

### care_household_services_2026_09_23/hours_tax.py (+ summary.py)

`summary.py` was rerun because it reads three of the changed files.

Changed: `ces_output_triangle.csv`, `hours_tax_specs.csv`, `metro_shocks.csv`, `partA_side_view_union_frame.csv`, `shock_summary.csv` and `summary.csv`. The other 11 files are unchanged, including every `elder_care_*` file and `acs_*` file.

`summary.csv`, $bn:

| Channel | Central | Low | High |
|---|---|---|---|
| Taxes on native women's extra hours | 2.6888 → 2.6886 | 1.8018 → 1.8018 | 5.7557 → 5.7560 |
| Additive total | 4.1478 → 4.1476 | 2.5965 → 2.5965 | 13.3493 → 13.3496 |
| Consumer surplus (side view) | unchanged | unchanged | 12.8223 → 12.8233 |

- **Printed text changes.** The 95% upper bound for the taxes on native women's hours goes from 3.86 to 3.85. Cortés–Tessada Table 7 (2.375) all-channel earnings go from 31.30 to 31.29. In `summary.csv` only, the consumer-surplus side view's metro figure goes from 23.39 to 23.40.
- **Largest cell change.** $0.004bn, an `earnings_hi95_bn` cell in a Cortés–Tessada t7 arm.
- **Areas.** 424 → 428.

### distribution_weights_2026_09_23/distribute.py

This lane reads the housing lane's new outputs and runs 212 gates, all of which pass.

Changed: `channel_by_decile`, `channel_by_quintile`, `gates.json`, `inputs.json`, `ranges_weighted`, `regressivity`, `rent_per_renter_household_acs` and `weighted_totals`. `income_frame`, `sources_manifest`, `wage_scenarios` and `weights` are unchanged.

- **Housing inputs.** Renters' extra rent goes −$33.856bn → −$33.859bn and landlords' gain $37.364bn → $37.366bn. Metro-local high renters go −$50.067bn → −$50.071bn, the largest unweighted flow move at $0.003bn.
- **Headline.** Unchanged at $0.1bn:
  - bottom four fifths −$80.7bn;
  - top fifth +$46.0bn;
  - total −$262.6bn (it moves by −$0.000005bn);
  - at η = 1.3, −$407.1bn and −$738.3bn.
- **Weighted equivalents.** Among flow channels, the largest move is 0.09 at η = 2 with a 2nd-percentile floor. This is a welfare-weighted figure, not dollars. The owner-value stock channel at the 1st-percentile floor is degenerate, about 1.06e10. It moves by 6e-5 in relative terms.

### ancestry_iv_congestion_wages_2026_09_23/check_mexico_component.py

All 14 files in `derived/` are byte-identical. The ancestry `.dta` holds only CT codes 09001–09015, and the merge is inner.

## Printed figures that change in their last digit

These were found by scanning each RESULT body for any number whose output cell changed at that printed precision. Each hit was then traced to the table cell it prints. Matches that were only coincidental are excluded. [CALCULATION]

| Lane RESULT | Where | Before → after |
|---|---|---|
| housing_transfer | line 159, arms table, short run central, metro: landlords' gain from other renters | 106.5 → 106.6 |
| housing_transfer | line 161, same, short run high, metro | 133.1 → 133.2 |
| housing_transfer | counts: line 106 "225 metros … 84%"; line 124 "377 metros" | 227, 85%; 381 |
| construction | line 229, §4.2 table, C_price_all owners' offset range, $tn | 2.01–2.41 → 2.02–2.41 |
| care | lines 24, 83 and 96: central 95% interval upper bound | 3.86 → 3.85 |
| care | line 105: Cortés–Tessada Table 7 (2.375), all-channel earnings | 31.30 → 31.29 |
| care | counts: line 72 and line 232 "424" | 428 |
| distribution | lines 97 and 179: Total (b), η = 1, per person p5 | −557.0 → −557.1 |
| distribution | line 177: (a), η = 1.4, quintile bins floored | −419.9 → −420.0 |
| distribution | line 178: (a), η = 2, quintile bins | −781.0 → −781.1 |
| distribution | line 182: (b), η = 2, quintile bins | −1,567.4 → −1,567.5 |
| distribution | line 268: owner-occupiers' stock, top fifth; per household | $815bn → $816bn; $31,892 → $31,895 |

The care side view's metro figure, 23.39 → 23.40, appears only in `derived/summary.csv` (`ci_note`), not in the RESULT body. The body text of these RESULTs was not edited; the `## Revisions` lines carry the new values.

## Read only (not rerun)

- `housing_causal_2000_2010_2026_09_22/estimate.py` is **unaffected**. Its input `county_housing_2000_2010.csv` carries Connecticut as 09001–09015 only, and it inner-merges on `county_fips`.
- `ancestry_instrument_2026_09_22/second_instrument.py` is **unaffected**. `AncestryInstrument_County.dta` carries Connecticut as 09001–09015 only (Fairfield … Windham), and the merge is inner.

## Flags for the lead

- **Labor-mobility lane (running; not touched).** Its next `metro_panel.py` run will read the shared rows instead of its `[DEGRADED]` fallback. It should print "differs from the lane mapping at none". Its `derived/xwalk_manifest.json` pins the old sha256 bc2d9cc8…; the file is now 83d0f0a0….
- **Scale-spillovers lane.** Note 4 in its RESULT ("Adjacent defect … not fixed here … probably under $0.1bn, but that has not been checked") is now fixed and measured: flows move by $0.011bn at most. The lane was not edited.
- **Stale body text left in place.** The table "Printed figures that change in their last digit" lists every stale value. Each lane's `## Revisions` line carries the new ones; the body text was not edited.
- **Naugatuck Valley.** 34.6% of its population lies outside its assigned CBSA. A town-level split (PUMA → town → old county) would remove this. The brief asked for majority assignment, so the split was not built.

## Files modified (not committed)

- `hedonic_composition_2026_09_19/`:
  - `src/build_geo.py`
  - `derived/geo_county_cbsa_2013.csv`
  - `RESULT.md` (Revisions)
  - `CT_PLANNING_REGIONS.md` (new)
  - ignored `_cache/`: `ct_cou_to_cousub_crosswalk.txt`, `ct_cou_to_cousub_crosswalk.xlsx`, `ct_cousub_pop2020_pl.json`
- `housing_transfer_2026_09_23/`: the five `derived/` files above and `RESULT.md` (Revisions).
- `congestion_2026_09_23/`: `derived/cbsa_commute.csv` and `RESULT.md` (Revisions).
- `construction_housing_supply_2026_09_23/`: the four `derived/` files above and `RESULT.md` (Revisions).
- `care_household_services_2026_09_23/`: the six `derived/` files above and `RESULT.md` (Revisions).
- `distribution_weights_2026_09_23/`: the eight `derived/` files above and `RESULT.md` (Revisions).

The following files were rewritten by reruns but are byte-identical: the hedonic tract files and panels, `results_zillow.csv`, and every unchanged output listed above. The scratch replays, logs and md5 snapshots are in the session scratchpad, outside the repository.
