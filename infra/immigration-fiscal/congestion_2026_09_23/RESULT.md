**Verdict:** In the account's main case, which holds highway and transit budgets fixed and so
keeps today's road network, the Mexican-origin group's traffic costs other US residents about
**$19bn a year** in time and fuel. That is approach B with lanes held fixed (B1; range $8–35bn).
Approach A prices network delay on the 2024 Urban Mobility Report, whose 9.8bn hours and $269bn
this lane reproduces. It gives **$34bn** when other drivers partly refill the space the group
leaves, as Duranton and Turner find at fixed lanes (range $14–60bn). It gives **$60bn** if
nobody's trips replace the group's ($34–93bn), and **$7bn** on the Couture–Duranton–Turner
city-level supply curve ($2–49bn). Two inputs explain the spread: how steeply delay rises with
traffic (link-level BPR β of 4, against 1.0–2.5 for whole networks) and how much of the group's
traffic other drivers replace. A and B1 match the fixed-network main case. The proportional
benchmark matches B3, the congestion left after capacity grows in proportion: **$9bn**
($1–19bn; $12bn if capacity shrinks by the account's 8.1% resources key).
[CALCULATION: `arms.py` → `derived/arms_summary.csv`, `derived/arms_grid.csv`]

**Overlap:** add A or B1 to the main case (adopted $203.2–249.6bn, with economic affairs still
fixed) and to the fixed non-school benchmark. Under the proportional reference, which already
charges the group $36.26bn of economic-affairs spending, add only B3. Add nothing for fuel
taxes. **Per other commuter** (88.1m in the 481 matched urban areas), B1 costs $217 and 8.8
hours a year. A ranges from $83 and 3.3 hours to $686 and 28.3 hours. Ten metros carry 47% of
B1's cost. Per other commuter it reaches $767 (31.6 hours) in Los Angeles, $567–581 in Dallas,
Phoenix and Houston, and $1,322–1,619 in San Antonio and Riverside–San Bernardino, against $58 in
New York. [CALCULATION: `derived/metro_distribution.csv`]

Model self-report: `claude-opus-5-5[1m]`

Date: 2026-09-23. Brief: [BRIEF.md](BRIEF.md). Frame unchanged: the complete annual account's
stationary 2024 comparison with and without the 40.896574m CPS Mexican-origin residents, effects
on all other residents, 2024 dollars.

## Results

Central values and the full factorial range of each approach. The per-commuter columns divide
all other residents' savings by other residents' commuters (workers who do not work from home).

| Approach | What it holds | Central | Range | Hours / other commuter | $ / other commuter | Matches |
|---|---|---:|---:|---:|---:|---|
| A1 BPR on UMR delay, trips fixed | lanes and everyone else's trips | $60.5bn | $33.7–93.3bn | 28.3 | 686 | fixed network, no fill-in (upper) |
| A1 BPR, Duranton–Turner fill-in | lanes; others' traffic refills part of the gap | $33.9bn | $13.5–60.3bn | 15.8 | 385 | fixed network |
| A2 CDT supply curve | lanes; others' demand responds (σ 16) | $7.3bn | $2.4–49.2bn | 3.3 | 83 | fixed network |
| B1 speed–population elasticity, lanes fixed | lanes | **$19.2bn** | $8.0–35.3bn | 8.8 | 217 | **fixed network (main case)** |
| B2 speed–population elasticity, unconditional | lanes growing as they do across metros | $11.9bn | $6.9–17.4bn | 5.4 | 135 | in between |
| B3 proportional capacity residual | lanes in proportion to population | **$9.0bn** | $1.1–19.3bn | 4.1 | 103 | **proportional benchmark** |

[CALCULATION: `derived/arms_summary.csv`; the ranges span every combination of the factors
listed under Method, 168–918 rows per approach in `derived/arms_grid.csv`]

Per other resident (207.8m in the matched areas) the central costs are $291 (A1), $163 (A1 with
fill-in), $35 (A2), $92 (B1), $57 (B2) and $44 (B3). Time is 94% of each central, excess fuel 6%.
In UMR's own convention (peak-period savings over car commuters, the rest over residents,
Appendix A Eq. A-4) A1 saves other commuters 22.6 hours with trips fixed and 12.6 with fill-in.
UMR puts the delay everyone suffers at 63 hours per auto commuter. [CALCULATION]

## Why the approaches differ

A1 applies link-level volume–delay curves to UMR's delay. With β = 4 the delay per vehicle-km
has an elasticity of 0.58 in traffic, because delay is 14.5% of travel time and 4 × 0.145 = 0.58.
CDT estimate 0.15 for whole cities (θ = 0.13, k = θ/(1−θ)).
[CALCULATION: `derived/checks.json` `bpr_implied_time_elasticity`; SOURCE: CDT working paper,
table 5 column 6] Two variants bridge the gap. [CALCULATION: `derived/arms_grid.csv`, rows with a `note`]

| A1 variant (central inputs otherwise) | Trips fixed | Fill-in η 0.44 |
|---|---:|---:|
| β 4 (original BPR; NCHRP 716 average curves 3.0–5.9 give $50.2–75.4bn) | $60.5bn | $33.9bn |
| β 2.52, the UMR's own 2019–2021 national swing (an upper bound, below) | $44.4bn | $23.2bn |
| β 1.03, the slope that equals CDT's k on UMR's delay base | $21.8bn | $10.4bn |
| Marginal β·ψ instead of the integrated removal | $85.0bn | |

With CDT's slope and fill-in, A1 lands at $10.4bn, between A2's $10.7bn (σ 8) and $7.3bn
(σ 16). The network approaches agree once they share a slope and a fill-in rate.
Integrating the inframarginal removal matters. The marginal shortcut overstates A1 by 41%.

**Network slope.** The UMR's 101-area totals show daily VMT falling 20% (log) from 2019 to 2020
while passenger delay fell 70%. That is an elasticity of 3.49 and implies β = 2.49; the 2021
rebound gives 2.54. Both overstate β for a uniform cut, because peak traffic fell and returned
more than daily traffic. Pairs from 2022 to 2024 give 0.3–0.8. Area-level changes cannot be
used: in 2020 each area's freeway and arterial VMT move by one common factor (correlation
0.99999), so those changes are imputed, not measured. [CALCULATION: `panel_check.py` →
`derived/umr_panel_elasticity.csv`] NCHRP 716's average BPR functions are link-level
(freeways 5.883, arterials 3.001; its Table 4.26 parameter averages for large MPOs are higher,
6.95 and 4.40). [SOURCE: NCHRP Report 716, p. 77 and Table 4.26]

**Fill-in.** At fixed interstate lane-km, metro VKT rises with population at elasticity
0.32–0.48. Removing residents therefore frees road space that others' extra driving partly
fills. [SOURCE: Duranton & Turner 2009, NBER w15376, table 2 panel A, columns 2–5] In A2 the same
behaviour enters through the demand elasticity σ: σ 8–16 implies a population elasticity of VKT
of 0.46–0.30 at fixed lanes, which is DT's range. [CALCULATION: 1/(1 + kσ)]

**City size.** B1 uses CDT's regression of speed on log lanes and log population across 100
MSAs in 2008. The population coefficient is −0.12 (SE 0.035) and the lane coefficient 0.066.
[SOURCE: CDT working paper, table 10 column 6] It measures directly how much slower a city with
more people is on the same lanes, and it lands between the network arms. Cross-city differences
also carry built-environment traits that come with size (street grids, signal density), so B1
leans high as a measure of pure congestion [INFERENCE]. Every time-cost arm (A2, B) is capped
at the delay share of travel time, since removing the group cannot make travel faster than free
flow. The cap binds in 32 areas under B1. Most are border and Central Valley areas where the group
is the majority (El Paso, McAllen, Laredo, Bakersfield, Salinas). Together they hold 1.5% of
delay, and the cap trims B1 from $20.1bn to $19.2bn. [CALCULATION: `areas_at_free_flow_cap` in
`derived/arms_grid.csv`; area list from `delay_share` against the B1 fall in time cost]

## Overlap ruling

- **Main case.** The published main case ($165.1–197.4bn) and the case adopted today
  ($203.2–249.6bn, commit 69eb31b) both hold economic affairs and recreation fixed. The adopted
  changes touch general government, justice keys and uncompensated care only.
  [SOURCE: `research/immigration-complete-annual-account-2026-09-20.md`, service-response table;
  `infra/immigration-fiscal/main_case_2026_09_23/RESULT.md`] The account assigns the group
  $36.26bn of the $451.9bn economic-affairs line on its preferred resources key (8.10%). At zero
  response none of it is saved, so the network is the same with or without the group.
  [DATA: `assumption_explorer_2026_09_21/derived/model.json`: line `economic_affairs_services`;
  the main and fixed non-school profiles carry `delayed_response` 0, the proportional reference 1]
  Other residents' extra delay is therefore a cost outside the account's budget lines. Add A or
  B1; the same holds for the fixed non-school benchmark ($158.9–212.6bn). It is a time-and-fuel
  cost, not fiscal. Report it beside the headline, as the uncompensated-care lane reports its
  outside-budget part. Do not scale it onto the generation ledger.
- **Proportional reference** ($307.9–341.0bn). Economic affairs responds at 1, so the absent-group
  network is smaller in proportion, and the account already counts the $36.26bn that absence
  would save as a cost of the group's presence. Add only
  the residual congestion left after capacity grows: B3, $9.0bn ($1.1–19.3bn). The residual
  exists because road travel has decreasing returns to scale. CDT's table 5 puts the lane and
  travel-time coefficients at 0.090 and −0.13 (the F-test rejects a zero sum in columns 1–8). Their
  footnote 19 finds the returns fall to about −6% to −7% on a construction-cost basis. Their
  table 10 regression gives 0.12 − 0.066 = 0.054 per log point of population.
  [SOURCE: CDT working paper, table 5, footnote 19, table 10] The fundamental law says added
  lanes fill with traffic, so capacity growth cannot remove this residual. Keyed as the account
  keys it (capacity shrinks by the 8.10% resources share while population falls by the group's
  share), the residual is $12.0bn. [CALCULATION: `arms_grid.csv` B3 `note` row]
- **Fuel taxes.** Not added: the account's tax side already counts the group's fuel taxes. UMR
  values excess fuel at retail prices, including tax. The tax part of other residents' extra
  fuel is a transfer among them, and fuel is 6% of each central, so it is left in [INFERENCE].
- **Transit crowding and parking.** Not priced (optional in the brief); see Covered / skipped.

## Distribution

Top metros by B1 cost; A1 with fill-in beside it. Group shares are scaled to the CPS union.

| Urban area | Group share of residents | Traffic share φ | B1 $bn | B1 hours / other commuter | B1 $ / other commuter | A1 fill-in hours / other commuter | A1 fill-in $ / other commuter | UMR delay per auto commuter (hours, everyone) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Los Angeles–Long Beach–Anaheim | 36.5% | 34.1% | 2.46 | 31.6 | 767 | 107.6 | 2,604 | 137 |
| Chicago | 19.9% | 18.7% | 1.12 | 15.5 | 382 | 32.4 | 800 | 87 |
| Dallas–Fort Worth–Arlington | 27.1% | 25.1% | 1.07 | 23.0 | 567 | 32.7 | 806 | 69 |
| Houston | 27.9% | 24.6% | 1.03 | 24.2 | 581 | 40.8 | 975 | 77 |
| Phoenix–Mesa | 25.7% | 24.1% | 0.72 | 23.3 | 572 | 43.0 | 1,056 | 76 |
| Riverside–San Bernardino | 54.4% | 52.4% | 0.62 | 60.8 | 1,619 | 108.0 | 2,870 | 95 |
| San Diego | 31.7% | 29.9% | 0.61 | 28.7 | 677 | 55.0 | 1,297 | 88 |
| San Antonio | 50.1% | 46.9% | 0.57 | 51.5 | 1,322 | 45.6 | 1,164 | 48 |
| New York–Newark | 3.5% | 2.1% | 0.45 | 2.5 | 58 | 4.8 | 111 | 99 |
| Las Vegas–Henderson | 23.9% | 22.6% | 0.38 | 20.5 | 532 | 27.2 | 704 | 57 |

[CALCULATION: `derived/metro_distribution.csv` (all 481 areas); DATA: UMR delay per auto commuter]
These ten carry 47% of B1 and 57% of A1 with fill-in; Los Angeles alone carries 13% and 25%.
The per-commuter figures count all other residents' savings, including non-workers' trips,
over other residents' commuters. That is why they can exceed UMR's per-commuter delay where the
group's share is large (San Antonio). The free-flow cap binds area totals, not per-commuter
conventions.

## Method

**1. Group share of road travel.** ACS 2024 one-year PUMS persons, group `HISP=02` or
`POBP=303` (the housing lane's rule): 39.43m persons, 11.59% (SE 0.02 points), scaled by
40.896574/39.429519 = 1.0372 to the CPS union, with the difference taken out of other
residents. The group holds 11.99% of commuters, 12.21% of car commuters and 18.35% of
carpoolers. Counting a carpool member as 1/`JWRIP` of a vehicle, it drives 11.75% of commute
vehicles and 11.92% of commute vehicle-minutes. Mean one-way times are nearly equal (27.4 against
27.2 minutes). The group leaves earlier: 63.4% of its commute vehicles depart 6–10 a.m. against
69.6%, and 19.5% before 6 a.m. against 14.0%. It works from home less (7.7% of workers against
14.0%). [CALCULATION: `tabulate.py` → `derived/pums_commute_national.csv`, 80 replicate SEs]
**Gate passed:** PUMS totals match published B08301 within 0.17% on every major row and B08133
aggregate travel time within 0.11%; the largest cell gap is −2.5% (5–6-person carpools).
[CALCULATION: `derived/pums_gate_b08301.csv`]

NHTS has no Mexican-origin flag, so Hispanic persons stand in, with the 2017 southwestern cut
(CA, TX, AZ, NM; 18,297 Hispanic persons) as central. Hispanic driving is 0.874 of non-Hispanic
driving per person aged 5+. The ratio of all-purpose to commute driving is 0.860 of the
non-Hispanic ratio (ρ). Occupancy is 1.044×, and the weekday-peak share of driving is 1.025× (π).
The 2017 national cut gives 0.893, 0.948, 1.022 and 1.144. The 2022 national file (1,722
Hispanic persons) gives 0.692, 0.742, 1.096 and 0.962. Commuting is 29–30% of non-Hispanic driver
VMT. [CALCULATION: `nhts.py` → `derived/nhts_ratios.csv`] The all-purpose traffic share φ scales
the group's commute vehicle-minute odds by ρ. Nationally that is 10.8%, against 10.7% from its
population share times the NHTS driving ratio. Weighted by delay across the matched areas, φ is
13.5% and the population share 14.8%, because the group lives in congested metros.
[CALCULATION: `derived/checks.json` `national_phi_*`, `phi_delay_weighted`; `derived/ua_exposure.csv`]

**2. Geography.** PUMA cells are spread to 2020 Census urban areas with Geocorr 2022
population allocation factors (totals preserved to 1e-9). UMR's 494 areas are matched by name
and state: 412 exact, 45 by first city, 20 by any city, 4 by hand. Two are unmatched (Pottstown
PA, Twin Rivers–Hightstown NJ; 0.04% of delay) and 11 are in Puerto Rico (1.07%; outside the
PUMS file). Coverage is 98.9% of delay. Shares come from the ACS allocation and levels from
UMR's area population; the two agree on population (delay-weighted ratio 0.997, 10th–90th
percentile 0.92–1.14). Atlantic City and Villas NJ share one Census area; UMR levels keep them
from double counting. The brief's metro tabulation on the housing lane's PUMA→county→CBSA route
is in `derived/cbsa_commute.csv`. [CALCULATION: `arms.py`, `derived/checks.json`]

**3. UMR base and positive control.** Summing the 494 areas in the 2025 UMR workbook gives
9,800,519 thousand person-hours of delay, $268,724m of congestion cost, $35,766m of truck cost
and 2.818bn gallons of excess fuel. Exhibit 1 reports 9.8bn hours, $269bn, $35.8bn and 2.8bn.
Rebuilding each area's cost from its parts (passenger hours × $24.01, truck hours ÷ 1.14 ×
$80.16, gallons × state fuel prices) is within 1.02% for every area above $50m. The largest gap
is Gadsden AL, from rounding. Eq. A-4 with the peak share read from Exhibits 10, 13 and 15
(δ = 0.526 of delay in weekday peaks) returns 62.3 hours per auto commuter against the published
63. [CALCULATION: `derived/umr_positive_control.json`]

**4. Arms.** Removal is integrated over the group's whole traffic in every arm.
- A1: per area and period (weekday peak, other), ψ = (1 − w_truck)·φ_period + w_truck·τ. Other
  residents' delay falls by 1 − (1 − ψ_eff)^β with ψ_eff = 1 − (1 − ψ)^η. Their person-share of
  passenger delay uses the occupancy ratio, trucks save (1 − τ) of theirs, and excess fuel falls
  in proportion. Factors: β {3.001, 4, 5.883}; value of time {low, central, high}; τ {7.4%, 9.7%,
  12.0%}; NHTS inputs {2017 southwest, 2017 national, 2022 national}; peak ratio π {NHTS, ACS
  0.911}; η {1 (trips fixed), 0.48, 0.44, 0.32}.
- A2: ln C₀ = k/(1 + kσ)·ln(1 − ψ), and others gain T_o·(1 − C₀^(1−σ))/(1 − σ), where T_o is
  their vehicle-occupant hours (NHTS hours per person aged 5+ by urban-area size × residents
  aged 5+). Factors: θ {0.07, 0.13, 0.19}; σ {0, 8, 16, 32}; value of time; τ; NHTS inputs; NHTS
  hours year {2022, 2017}. [SOURCE: CDT working paper, section 7 and table 8]
- B1/B2/B3: ln C₀ = ε·ln(1 − s) with s the group's share of residents (or φ as a variant).
  B1: ε {0.085, 0.12, 0.155} (table 10 column 6, ± 1 SE). B2: ε = 0.072 (section 6, 100 MSAs;
  CDT note Bombardini and Trebbi's similar −7.5%, not read here). B3: (θ − a)/(1 − θ)/(1 + kσ)
  for table 5 columns 0, 2, 4, 6, 8 and the PMSA estimates, the footnote 19 cost basis, and the
  table 10 difference 0.054. Every time-cost arm is capped at the delay share of travel time.
- Trucks and fuel in A2 and B: their delay falls by the same fraction of travel time, divided by
  the delay share of travel time (14.5% across the matched areas).

**5. Value of time.** USDOT's 2016 guidance, revision 2, with 2024 inputs. Local personal travel
is 50% of hourly median household income: $83,160/2,080 × 0.5 = $19.99 (range 35–60%).
Business travel is 100% of the median wage times the compensation/wage ratio, $23.80 × 1.453 =
$34.58. All purposes (95.4/4.6) is $20.66, range $14.62–24.79. Truck drivers are
$25.54 × 1.458 = $37.24, range $29.79–44.69. The method reproduces the guidance's own 2015
values from 2015 inputs ($13.59, $25.42, $14.13, $27.23 against $13.60, $25.40, $14.10, $27.20).
[CALCULATION: `derived/vot_2024.csv`, `checks.json`; SOURCE: USDOT guidance pp. 10–14; Census
H-8; BLS OEWS May 2024 table 1; BLS ECEC 2015Q2 and 2024Q2] The brief paraphrases the personal
rate as "50% of the median wage". The guidance's text (p. 11) uses household income. Read
literally, the paraphrase gives $12.94 an hour and B1 $13.2bn, A1 $41.2bn and $23.2bn with
fill-in, A2 $5.1bn. [CALCULATION: `arms_grid.csv` rows noted "brief's wording"]

**6. Trucks.** UMR truck delay (0.47bn person-hours in the matched areas) is weighted by its share
of vehicle delay (6.2%). τ, the group's share of truck traffic, ranges from its share of
personal income (7.4%) to its share of residents (12.0%) [INFERENCE: freight follows spending].
Truck drivers' time is 9–12% of each central's dollars. [CALCULATION: `others_truck_person_hours_m`
× $37.24 over `total_bn`]

## Sources

Files in `_cache/` (ignored), with sha256 prefixes from `_cache/manifest.json`:

| Source | File | sha256 |
|---|---|---|
| TTI 2025 Urban Mobility Report workbook (2024 data) | `complete-data-2025-umr-by-tti.xlsx` | 8fe5f4e0d833 |
| UMR 2025 report; Appendix A methodology | `mobility-report-2025.pdf`; `-appx-a.pdf` | 67fc8eb59a20; 6a0c4af1122e |
| NHTS 2022 and 2017 public CSV | `nhts2022_csv.zip`; `nhts2017_csv.zip` | 64530c396d5f; 4f1917d9470f |
| ACS 2024 PUMS persons (repo source tree) | `sources/.../acs_pums_2024_1yr/csv_pus.zip` | afdc6d90c6e2 |
| ACS 2024 B08301, B08133, B01001 (API) | `acs2024_b08301_us.json`, `acs2024_b08133_us.json`, `acs2024_b01001_us.json` | c323bec18a43, e687037b3423, 3c594adf5831 |
| Geocorr 2022 PUMA→urban area | `xwalk_puma22_ua20.csv` | f279af7bb319 |
| Couture, Duranton & Turner, "Speed" (REStat 2018), 2016 working paper on HAL; NBER w18234 | `cdt_speed_2016_hal.firecrawl.md`; `w18234.pdf` | 899b9cde921b; 352cb3aa5854 |
| Duranton & Turner, "The Fundamental Law of Road Congestion", NBER w15376 | `w15376.pdf` | e231dbe9277a |
| NCHRP Report 716 | `nchrp_rpt_716.pdf` | 0a68f2d472fb |
| USDOT Revised Value of Travel Time Guidance (2016, rev. 2) | `usdot_vtts_2016_rev2.firecrawl.md` | 9204b167d928 |
| Census H-8; BLS OEWS May 2024; BLS ECEC | `census_h08.xlsx`; `bls_ocwage_may2024.firecrawl.md`; `bls_ecec_2015_2024.json` | 5cd4278aafb9; 6eb32d2cbe90; fd842474c964 |

Reused repo inputs: the housing route's `employment_entry_2026_09_18/_cache/xwalk_puma22.csv` and
`hedonic_composition_2026_09_19/derived/geo_county_cbsa_2013.csv`; the account's
`assumption_explorer_2026_09_21/derived/model.json`.

## Limits

- The approaches disagree about fourfold at central values within the fixed-network case ($7–34bn,
  B1 in between). The spread traces to two measurable inputs, the network slope and fill-in.
  Neither is pinned down for a removal of this size.
- B1's coefficient is a cross-section of 100 MSAs in 2008 (OLS on log lanes and log
  population). Large cities differ from small ones in more than traffic, so B1 leans high for
  pure congestion; the free-flow cap handles only the extreme cases.
- UMR delay is measured against overnight free-flow speeds on freeways and arterials and includes
  incident delay. Congestion on local streets and outside the 494 urban areas is not in A.
- The traffic share comes from where commuters live (ACS), converted with Hispanic, not
  Mexican-origin, NHTS ratios. The 2022 NHTS Hispanic sample is small (1,722 persons).
- T_o uses non-Hispanic NHTS hours for all other residents. The 2017 hours (pre-pandemic) raise
  B1 to $23.4bn; the 2022 hours are central.
- τ, the group's share of truck traffic, is an assumption, not a measurement.
- Stationary comparison: no re-sorting of residents or jobs across metros. The national-uniform
  variant, which spreads the group evenly, raises A1 to $82.5bn: the BPR saving is concave, so
  concentration lowers the total. It leaves B1 at $20.2bn.
- Excess fuel is valued at retail prices, including taxes that are transfers among other
  residents (6% of each central).

## Covered / skipped

Covered:
- ACS tabulation of means, one-way time, departure time and occupancy, national (with replicate
  SEs), by urban area and by CBSA, plus the B08301/B08133 gate.
- NHTS 2022 and 2017 driving, hours, peak shares and occupancy by Hispanic origin.
- UMR positive control (national totals, per-area cost identity, Eq. A-4).
- A1 (β range, integrated against marginal, fill-in), A2 (θ × σ), B1, B2 and B3 (with the
  account-key variant).
- USDOT value of time in 2024 dollars, with the 2015 reproduction check.
- Trucks, excess fuel, the network-slope check on UMR's own series, the per-commuter
  distribution and the overlap ruling.

Skipped:
- **Transit crowding and parking:** optional in the brief; no crowding or parking data pass was
  run.
- **Puerto Rico's 11 UMR areas:** the PUMS file covers the 50 states and DC.
- **Two unmatched small areas:** 0.04% of delay.
- **Crash, emission and pavement-wear externalities of the group's driving:** outside the brief's
  congestion scope. Pavement wear on a fixed maintenance budget is a further unpriced cost of the
  main case's assumption.
- **Cross-area volume–delay regression:** area VMT changes are imputed (above).
- **Bombardini–Trebbi's own paper:** not read; their estimate appears only as CDT's
  corroborating remark and enters no calculation.

## Reproduce

```sh
# from the repository root; fetch.py needs the Census key (config.local.env), never printed
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/congestion_2026_09_23/fetch.py files census geocorr
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/congestion_2026_09_23/tabulate.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/congestion_2026_09_23/nhts.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/congestion_2026_09_23/panel_check.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/congestion_2026_09_23/arms.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 -m pytest infra/immigration-fiscal/congestion_2026_09_23/ -q
```

`arms.py` stops with `[POSITIVE CONTROL FAILED]` if the UMR totals are not reproduced, and
`tabulate.py` with `[GATE FAILED]` if the PUMS totals miss B08301 by more than 3%.

## Revisions

2026-09-23: Connecticut planning regions (09110–09190) now map to 2013 CBSAs in the shared crosswalk; only `derived/cbsa_commute.csv` changes (424 → 428 areas; `nonmetro_09` other residents 3.61m → 0.11m; Hartford, New Haven, Bridgeport–Stamford and Norwich–New London rows added; Worcester 0.87m → 0.97m other residents). The urban-area headline and every other output are byte-identical. Detail: [`CT_PLANNING_REGIONS.md`](../hedonic_composition_2026_09_19/CT_PLANNING_REGIONS.md).
