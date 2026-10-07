claude-opus-5-5

**Verdict:** Under the September 27 case's rules, 40.9M third-plus-generation non-Hispanic white residents would cost other residents **$154bn / $204bn a year** at specs 48 / 11. On the same rough keys the Mexican-origin union costs them **$311bn / $359bn**. The fiscal replacement delta is **+$157bn / +$155bn a year on the case's cash basis**, about $3,800 per member, or +$168bn / +$183bn against the engine's own union figure. [CALCULATION: `rekey_white.py` → `derived/rekey_summary.csv`]

The white slice still costs other residents money on cash because it is old. 23.4% of it is 65 or over, against 7.7% of the union. Its Social Security and Medicare draws exceed its payroll taxes and premiums by **$170.5bn**; the union has a $44.4bn surplus on the same lines. [CALCULATION]

Three results change the delta:

- **Accrual.** Social Security and Part A on accrual, with payable benefits, move the delta to **+$318bn / +$315bn**. [CALCULATION: `accrual_white.py`]
- **The union's age structure.** Charging white per-age rates at the union's ages gives +$330bn / +$326bn on cash. [CALCULATION]
- **Two case conventions.** Both of them hold down how much whites pay. The CPS top tail of income tax, $393bn federal, is charged to nobody, and capital-side taxes do not respond when people leave. With both arms the delta is +$289bn / +$287bn on cash and **+$450bn / +$447bn on accrual**. [CALCULATION]

Scale is worth the same for either population: +$38.6bn for the union against +$37.4bn for the white slice. The schooling externality favours whites by **+$31bn**, and the joint central by **+$29bn**, with a 95% interval of −$54bn to +$113bn. The 1970–2000 college-share literature gives +$220bn to +$868bn, and Ciccone–Peri gives −$32bn to +$49bn. [CALCULATION: `spillovers_white.py`]

Violent-crime victims outside the group cost **$10–12bn** less like for like. [CALCULATION: `victim_cost_white.py`]

**State-specific replacement (Part F).** The arm replaces the union in California with California's own third-plus whites and in Texas with Texas's. Elsewhere it uses national white rates. All three are charged at the union's ages. The total is **+$412bn / +$406bn** on cash, $10,081 per member.

- **By state:** $14,133 in California, $8,567 in Texas and $7,963 elsewhere. Los Angeles, inside California, is $18,816.
- **At the whites' own ages:** $240bn / $235bn.
- **With both convention arms:** $13,846 per member, about $566bn.

These per-person deltas land within 2–6% of the older partial ledger's age-matched gaps: $14,467 in California, $8,115 in Texas, $10,069 nationally. On a no-response basis the full account adds capital-side taxes and earnings-keyed lines, but the case's zero responses switch most of them off again. [CALCULATION: `state_white.py`]

Every cost channel meets the same scaling exponent whichever population is added. The delta comes from per-head differences in taxes paid and programmes drawn, not from sub- or superlinear scale.

This is an accounting comparison of two populations under one set of rules. It is not a policy scenario. [FRAMING-SENSITIVE]

Lane `infra/immigration-fiscal/white_replacement_2026_09_28/`, written 2026-09-28, 22:12–22:46 JST; Part F 22:47–22:51 JST (times from `date`). Brief: [`BRIEF.md`](BRIEF.md). All figures are in 2024 dollars a year. The low end is spec 48 and the high end spec 11, as in the Black lane.

**Parent's expectation against the result.** The expectation was recorded before any run: A1 at $420–580bn on cash. The cash central is $155–157bn, and the expectation is reached only on accrual with both arms ($447–450bn). The old-age lines do cut the white advantage much more on cash than on accrual, as expected. B's schooling term is positive with a very wide interval, as expected. D is as expected. [CALCULATION; INFERENCE]

## A. Fiscal re-key

### Method

`rekey_white.py` is a modified copy of `black_comparator_rough_2026_09_28/rekey.py`; the original is not edited. Every group runs through one code path. A scenario is a person-weight vector on CPS ASEC 2025 and MEPS 2024, plus external keys for Medicaid LTSS and justice.

The engine lines come from `engine_lines.cjs`. Its output `derived/engine_lines.json` is byte-identical to the Black lane's.

**Gate.** The generalized code reproduces the Black lane's `rekey_summary.csv` exactly for the engine union, the rough union and the NH Black rows. [CALCULATION]

**Slices.** Each slice is scaled to the engine's 40,896,574:

| Arm | Population and ages |
|---|---|
| A1 | Third-plus NH white (native, both parents US-born, NH, white alone; the ledger's `third_plus_nh_white`), 173.05M in CPS, at its own ages |
| A2 | All US-born NH white, 183.82M, at its own ages |
| A3 | A1's per-age rates at the union's age structure (five-year bands, 80+) |
| A4 | A1's rates at the stationary NH white life course (NVSS 2024 Table 16 Lx) |

[DATA: `derived/keys.csv`, `derived/age_structures.csv`]

**White-specific keys.** MEPS NH white (`RACETHX` 2) with `BORNUSA` ≠ 2 gives the US-born rates. MEPS has no parent birthplace, so A1 takes the US-born rates. [INFERENCE] Medicare is 15.8% of MEPS spending for the A1 slice, against a 12.1% population share. [DATA]

Medicaid LTSS uses T-MSIS 2023: white_nh is 57.56% of LTSS spending, keyed per NH white and scaled by the slice's 65+ share against all NH whites. [DATA: `ltss_share_2026_09_23/derived/taf_race_ethn.csv`; the 65+ scaling is INFERENCE]

Justice follows the adopted rule. Custody is 29.34% of prisoners: SPI 2016 NH white 30.08% × 417,141 of 427,675 reporting a US birthplace. [DATA: `research/immigration-crime-race-ethnicity-2026-09-05.md`] NH white adult arrests are 51.1% of the total: FBI 2019 Table 43C white share less the Hispanic share of ethnicity-reported arrests. [DATA: `crime_victim_cost_2026_09_23/derived/fbi_2019_table43c_adult_arrests.csv`; subtracting assumes Hispanic arrestees are coded white, INFERENCE]

Both justice shares are age-adjusted by the NCVS 2024 violent-victimisation age gradient, used as an offending proxy. That factor is 1.10 at union ages. [INFERENCE: flatter than arrest curves]

**Carried from the Black lane.** No production term is scored for a native group. The engine's Mexican-specific repricing lines (school reprice, college re-key, lane constants) are zero.

### Totals

$bn a year. The white rows are the white slice's own cost to other residents; the delta is the union's cost (rough keys) less the white slice's.

| | Low (48) | High (11) | per member, low / high |
|---|---:|---:|---:|
| Union, engine | 321.8 | 387.4 | $7,869 / $9,472 |
| Union, rough keys | 310.8 | 359.0 | $7,599 / $8,779 |
| All-residents slice of 40.9M (benchmark) | 224.1 | 273.8 | $5,480 / $6,696 |
| A1 third-plus NH white | **153.6** | **204.4** | $3,756 / $4,998 |
| A2 US-born NH white | 155.8 | 206.6 | $3,810 / $5,052 |
| A3 white rates, union ages | −19.4 | 32.7 | −$475 / $800 |
| A4 white rates, stationary ages | 151.8 | 201.7 | $3,711 / $4,933 |
| **Delta A1, like for like** | **157.2** | **154.6** | $3,843 / $3,781 |
| Delta A1 against the engine's union | 168.2 | 183.0 | |
| Delta A2 / A3 / A4, like for like | 154.9 / 330.2 / 159.0 | 152.4 / 326.3 / 157.3 | |

[CALCULATION: `derived/rekey_summary.csv`]

On the normalized gap, which charges each slice its population share of the national balance with no responses, the delta is **+$340.5bn**: the union −$253.8bn against A1 +$86.7bn. The gap has no responses, so it credits the white slice's capital-side taxes and every per-head line in full. [CALCULATION]

### Per line, low end

"Cost" is spending saved less receipts lost when the slice is removed. The delta column is the union (rough) less A1; a positive entry means the union costs others more on that line.

| Line | Union, engine | Union, rough | A1 white | A3 white, union ages | Delta (rough − A1) |
|---|---:|---:|---:|---:|---:|
| Income taxes | −137.7 | −141.3 | −357.5 | −343.6 | +216.1 |
| Payroll taxes and Medicare premiums | −162.1 | −169.0 | −255.9 | −237.0 | +86.9 |
| Sales, excise, customs, fees | −100.3 | −102.0 | −166.7 | −155.5 | +64.7 |
| Capital, property, production taxes (response 0 in the case) | 5.6 | 5.6 | 5.6 | 5.6 | 0 |
| Social Security | 56.9 | 61.2 | 240.3 | 91.5 | −179.1 |
| Medicare | 52.4 | 52.4 | 174.5 | 67.8 | −122.1 |
| Medicaid | 117.7 | 117.7 | 95.2 | 80.6 | +22.5 |
| Schools and colleges | 201.4 | 202.1 | 130.4 | 202.4 | +71.7 |
| Police, courts, prisons | 69.7 | 69.7 | 53.3 | 55.7 | +16.4 |
| SNAP, SSI, housing, cash aid, credits | 117.8 | 116.1 | 67.8 | 70.0 | +48.3 |
| Veterans and military medical | 14.1 | 11.6 | 34.2 | 23.0 | −22.6 |
| Per-head lines (government, defense, interest, roads, other) | 66.0 | 66.2 | 99.5 | 83.3 | −33.3 |
| Capital return on public capital | 33.8 | 33.8 | 32.9 | 36.9 | +0.9 |
| Production gain (subtracted) | −13.3 | −13.3 | 0 | 0 | −13.3 |
| **Total** | **321.8** | **310.8** | **153.6** | **−19.4** | **+157.2** |

[CALCULATION: `derived/rekey_buckets.csv`; the high end is there too]

The per-head bucket is larger for whites because some of its lines use earnings or Social Security keys. Economic affairs is keyed on earnings at response 0.38, and other federal benefits on Social Security. The pure per-head lines are identical for the two slices. [DATA: `derived/rekey_line_shares.csv`]

### Old-age lines, cash and accrual

Cash books the 2024 Social Security and Part A benefits paid to today's old as the slice's cost. Accrual books the benefits its 2024 workers earn instead. A young group gains under cash and an old group under accrual, so the basis matters more for this comparison than for any other.

**Method.** `accrual_white.py` imports `pension_accrual_2026_09_28` read-only and runs its central on the lane's own CPS frame for both groups. The central is payable benefits, entry-age attribution, Trustees new-issue rates, general mortality and the age-adjusted Note 2025.7 level.

**Gate.** The union's 1.018378 (payable), 1.297788 (scheduled), $41.137bn Part A and 0.083884 benefit-tax timing reproduce the lane. [CALCULATION]

| Per tax dollar | Union | Third-plus NH white |
|---|---:|---:|
| OASDI accrual, payable (scheduled) | 1.018 (1.298) | 1.019 (1.272) |
| Net of future income tax on benefits, payable | 0.974 | 0.935 |
| Part A accrual per HI tax dollar, payable | 1.461 | 0.994 |
| Share of 65+ with Medicare | 0.906 | 0.952 |

[CALCULATION: `derived/accrual_ratios.csv`]

**The white benefit-tax rate is set, not measured.** Whites' 2024 rate on benefits is set equal to the nation's (relative rate 1.0) [INFERENCE]. The union's measured relative rate is 0.52. The current-receipt removal is carried at the union's per-dollar ratio.

| Delta, like for like | Low | High |
|---|---:|---:|
| Cash (central rules) | 157.2 | 154.6 |
| Accrual, payable (central) | **317.6** | **315.1** |
| Accrual, scheduled | 308.9 | 306.4 |
| A3 (union ages), accrual payable | 318.7 | 314.8 |
| A4 (stationary), accrual payable | 301.4 | 299.8 |

On accrual the A1 slice costs others $77.7bn / $128.5bn and the union $395.3bn / $443.6bn (rough). The A1 and A3 deltas nearly coincide on accrual. That is the expected sign that accrual removes the age-structure effect of pay-as-you-go. [CALCULATION: `derived/accrual_beside.csv`]

### Two conventions that hold the white advantage down

**Top tail.** CPS federal income tax is $2,010.2bn against the national line of $2,403.2bn; state tax is $497.7bn against $536.2bn. The Black lane's rule charges each group its CPS dollars, so the missing $393bn + $38bn is charged to nobody. The arm spreads that gap in proportion to CPS income tax, which moves the delta by +$37bn. The top tail is more concentrated among high-income whites than proportional spreading assumes, so +$37bn is likely too small. [CALCULATION; INFERENCE]

**Capital-side taxes.** The case sets corporate, production and property taxes at response 0, on the reasoning that capital stays when people leave. The white slice pays $188bn more of these than the union on the key amounts. [DATA: `rekey_line_shares.csv`] In a long-run steady state, business capital follows effective labour and the housing stock follows residents. The arm therefore sets response 1, with earnings and property-value keys, and moves the delta by +$95bn. [INFERENCE]

Both are **convention-driven zeros**, flagged here, not adopted.

| Delta, like for like | Low | High |
|---|---:|---:|
| Cash + top tail | 194.4 | 191.8 |
| Cash + capital-side taxes | 252.1 | 249.6 |
| Cash + both | 289.4 | 286.8 |
| **Accrual payable + both** | **449.8** | **447.3** |
| A3 cash + both | 443.9 | 440.0 |

[CALCULATION: `derived/replacement_table.csv`]

## B. Schooling and scale spillovers

**Method.** `tabulate_white.py` builds ACS 2024 PUMS cells for US-born NH whites (not born in Mexico, which the union's rule claims) with the spillover lane's `person_items`. It gates that the union and all-person cells equal the spillover lane's cells. The ACS has no parent birthplace, so B uses the A2 population. [DATA]

`spillovers_white.py` scales each white PUMA cell by 40.9M / 183.62M and so keeps the white settlement pattern. It runs every specification of `scale_spillovers_2026_09_23/arms.py`, imported read-only, and gates that the union's central joint (+$13.9bn) reproduces on all three geographies. The delta's interval is the delta method on the difference, with both gains moving with the same parameter draw. [CALCULATION]

**The white slice's schooling.** Mean years at 25+ are 14.22, against 11.46 for the union; 72.5% of its workers have some college, against 45.2%; BA+ is 43.3% against 18.2%. [DATA: `derived/pums_white_cells.csv`]

Commuting zones, $bn a year. A gain is a benefit to others; the delta in cost terms is the white gain less the union's gain.

| Specification | Union gain | White gain (95%) | Replacement delta (95%) |
|---|---:|---:|---:|
| Scale, CRY by education (central) | +38.6 | +37.4 (31.2 to 43.6) | −1.2 (−1.4 to −1.0) |
| Schooling, CRY net of CES σ 2 (central) | −24.9 | +5.9 (−10.1 to 21.8) | **+30.8 (−53.2 to 114.8)** |
| **Joint CRY, σ 2 (central)** | +13.9 | +43.3 (28.9 to 57.6) | **+29.3 (−54.2 to 112.8)** |
| Joint, σ 1.5 / σ 2.5 / no CES term | +42.4 / −3.2 / −72.5 | +36.5 / +47.3 / +63.4 | −5.9 / +50.5 / +135.9 |
| Joint, with the weight m's SE | +13.9 | +43.3 | +29.3 (−248.6 to 307.2) |
| Ciccone–Peri joint, Table 4 cols 2 / 1 / 4 | +116.1 / +168.2 / +169.1 | +103.7 / +217.5 / +137.6 | −12.5 / +49.4 / −31.6 |
| Glaeser–Resseger joint | +11.8 | +40.8 | +28.9 (−62.2 to 120.1) |
| Moretti earnings-weighted, col 6 (2024 weights) to col 3 (1980–90 weights) | −227.3 to −540.7 | +54.5 to +123.1 | +281.8 to +663.8 |
| Moretti earnings-weighted, col 8 (2024 weights), lowest | −176.9 | +42.7 | +219.6 |
| Moretti NLSY base case, net of CES σ 2 | −327.1 | +76.5 | +403.6 (127.5 to 679.6) |
| Iranzo–Peri, Table 8 col 1 / Table 9 col 4 | −392.0 / −715.5 | +86.4 / +152.1 | +478.4 / +867.6 |

[CALCULATION: `derived/spill_summary.csv`, `derived/spill_grid.csv`, with the CBSA and national columns there]

The central sign is robust in the joint CRY rows except σ 1.5. Its interval spans zero. The 1970–2000 college-share literature makes schooling the largest term in the whole comparison. Adopting it alone would break the spillover lane's symmetry rule 2, as it did for the union. Every row here is beside the account and none is added.

## C. Innovation and the long tail

**BCHTT transport.** Run through the spillover lane's Burchardi et al. transport at 14.22 years, the white slice scores **+$4.8tn** (95% $0.8–8.7tn) on patents. That is **out of support and not usable**. The structural 5% wage effect of 18.4M post-1965 migrants is scaled linearly to 40.9M and then multiplied by a 4× schooling ratio. The estimate identifies migrants' ancestry-network effects, not natives'. The union's figure on the same machinery is −$24bn (±$500bn). [CALCULATION: `derived/spill_innovation.csv`; INFERENCE]

**Inventor rates.** Bell, Chetty, Jaravel, Petkova and Van Reenen (NBER w24062) report the share of NYC public-school children born 1979–85 who patent by 2014. [SOURCE: w24062 p. 13 and Figure II; PDF sha256 55b0647d… in `_cache/`, ignored]

| Children in the NYC sample | Inventors per 1,000 |
|---|---:|
| White non-Hispanic | 1.6 |
| Asian | 3.3 |
| Black | 0.5 |
| Hispanic | 0.2 |

Reweighted to white parental incomes, the Hispanic rate is 0.3 and the Black rate 1.0. Reweighted to white third-grade test scores, the Hispanic rate is 0.3. So the per-capita white-to-Hispanic ratio is 8× raw and about 5× at white incomes.

These figures have limits [INFERENCE]:

- NYC Hispanics are mostly Caribbean, not Mexican-origin.
- The paper publishes no standard errors for these bars.
- The authors say they "cannot be sure that the racial patterns within the NYC schools hold nationally".

No dollar value is attached. Doing so would need a per-inventor social return, and no primary source for one is in the repo. The long tail also enters A through the income-tax top tail above.

## D. Sub- or superlinear, channel by channel

| Channel | Exponent in the repo | Cost per added person as the total grows | Geography |
|---|---|---|---|
| General government | 0.60–0.85 finite removal (ladder 227; case decision 2026-09-26) | falls (sublinear) | cross-state; the same for any population |
| Roads | 0.727 per 1% residents | falls | same |
| Parks | 0.948 | falls slightly | same |
| Schools | ~1% per 1% pupils (full average cost) | flat per pupil | the delta is composition: under-15 share 23.8% union, 14.5% white |
| Transfers, Medicare, Social Security, justice | per recipient or use, by rule | flat per user | none |
| Congestion | speed elasticity −0.12 per log population, lanes fixed (CDT); link BPR β 4 | rises (superlinear) | union lives where delay is higher: 42.8 h per person where it lives against 37.8 h for others; delay-weighted share 0.148 against population-weighted 0.133 |
| Rent | +1–2% per 1% population short run, +0.39% (0.25–0.60) long run | f = 1 − (1 − s)^e, roughly linear in share | metro-local $33.9bn against national-uniform $33.5bn: geography barely matters |
| City size (agglomeration) | +0.0254 log premium per log size (CRY joint) | benefit per person rises (superlinear output) | scale gain +$38.6bn union against +$37.4bn white |

[DATA: `decisions/2026-09-27-main-case-capital-return-and-long-run-responses.md`, `decisions/2026-09-26-main-case-finite-removal-and-consumption-key.md`, `research/immigration-INDEX.md` l.106, `congestion_2026_09_23/derived/ua_exposure.csv`, `housing_transfer_2026_09_23/derived/arms_headline.csv`, B above; CALCULATION for the delay figures]

**Congestion and housing were not rerun.** The congestion lane builds each urban area's traffic share from group-specific ACS commuting, not from a share vector. The housing lane reads its own per-CBSA exposure file.

**Direction for congestion** [INFERENCE]. The white slice is spread out. In the eight CBSAs where it has the most members, its share of residents is 15.3% in Minneapolis, 13.3% in Boston, 12.2% in Philadelphia, 9.7% in Chicago, 8.9% in Atlanta, 8.6% in Dallas, 8.1% in New York and 5.0% in Los Angeles. The union's shares are 48.5% in Riverside, 47.0% in San Antonio, 35.0% in Los Angeles, 31.7% in San Diego, 27.8% in Phoenix, 27.0% in Houston, 24.3% in Dallas and 19.4% in Chicago. [DATA: `derived/spill_checks.json`] That lowers the white slice's congestion per head. Its higher car commuting and income-driven travel raise it. The net sign is not measured.

**Direction for rent** [INFERENCE]. The housing lane's own metro-against-uniform result shows settlement barely matters at its elasticities, so the population term is about equal. Higher incomes per head mean more housing demand per person than a population count carries, which points to a larger rent transfer for whites. It is a transfer among other residents either way.

**Answer to the operator's question.** Administration and infrastructure are sublinear, congestion is superlinear and agglomeration is superlinear. All of these apply to any 40.9M of the same size and similar settlement. They nearly cancel in a replacement: scale −$1.2bn, rent about equal. The replacement delta comes from per-head taxes, transfers and age, not from synergy or scale economies. [INFERENCE]

## E. Crime victims

`victim_cost_white.py` is the Black lane's script with offender "White" (NCVS 2022–24 codes Hispanic offenders separately) and SHR `p_off_nh_white`, at Miller 2021 victim-only prices. The same code with offender Black reproduces the Black lane (gate). [CALCULATION: `derived/victim_cost_white_summary.csv`]

**All NH white offenders, 2024.** Offences cost $205.7bn in full, 4,490 homicides and 3.38M non-fatal victimisations. Of that, $54.1bn falls on non-white victims and $151.7bn on white victims. [CALCULATION]

**A 40.9M slice.** The slice is 21.3% of NH whites. [CALCULATION]

- **Non-white victims only: $11.5bn.** This counts every white victim inside the group. The comparable union arm, with all Hispanic victims inside, is $23.5bn. [DATA: `crime_victim_cost_2026_09_23/derived/arms.csv`]
- **Victims outside a slice drawn at random from whites: $36.9bn.** The union's central is $28.9bn. This pairing is not like for like, because a random slice's victims are mostly other whites outside it. A replacement population living as the union does would victimise itself as the union does.
- **At union ages:** $13.6bn and $43.6bn. This applies the NCVS lane's age-only offending index, 1.18. [DATA]

**Like for like** (all co-ethnic victims in-group): **+$12.0bn** at own ages and +$9.9bn at union ages. It is beside the account, like the union's victim item.

## F. State-specific replacement (addendum 22:23)

### Method

`state_white.py` imports `rekey_white.py`, whose module-level build writes nothing, and prices each piece with its `run()`. `rekey_white.py` got one refactor for this, `keyed()` split out of `scenario()`, and its outputs stayed byte-identical.

**Union pieces.** The union's CPS persons in California (FIPS 6), Texas (48) and the rest of the US, plus the Los Angeles CBSA (31080) as an information row inside California. Lines the rough run keeps at the engine's national union share are split within the union by the piece's share on a CPS proxy [INFERENCE]:

| Line | Proxy |
|---|---|
| Medicare | Medicare coverage |
| VA, TRICARE | veterans' income |
| Medicaid, justice, other public health | persons |
| School reprice | pupils |
| College re-key | college enrolment |
| Lane constants | persons |
| Production gain | earnings |

Gate: the three pieces sum to the national rough union to within $0.001bn at both ends.

**White pieces.** Third-plus NH whites of the same state are reweighted to the union piece's age structure and population. For the rest of the US the whites are national. Each piece is also run at the whites' own ages. CPS samples: 3,073 persons in California, 3,045 in Texas, 787 in Los Angeles and 74,163 nationally [DATA]. MEPS has no state identifier, so medical keys are the national US-born NH white per-age rates at the piece's ages [INFERENCE].

National line prices are the case's. A state piece differs only through its CPS keys and ages: earnings, federal and state income tax, programme dollars, pupils and property. Nothing is state-priced. No sampling error is computed, and Los Angeles's 787 white records are thin.

### Results

$bn a year. Per member is per union member in the region.

| Region | Union members | Union cost, low / high | White cost at union ages | Delta at union ages, low / high | per member | Delta at white own ages, per member | Both A arms, per member |
|---|---:|---:|---:|---:|---:|---:|---:|
| California (CA whites) | 13.08M | 92.7 / 108.7 | −92.2 / −73.3 | **184.9 / 181.9** | **$14,133** / $13,907 | $9,160 | $19,640 |
| Texas (TX whites) | 9.76M | 87.0 / 98.3 | 3.4 / 15.9 | **83.6 / 82.4** | **$8,567** / $8,440 | $5,511 | $11,644 |
| Rest of US (national whites) | 18.05M | 131.0 / 152.1 | −12.7 / 10.3 | **143.8 / 141.8** | **$7,963** / $7,856 | $3,665 | $10,838 |
| **Sum** | 40.90M | 310.8 / 359.0 | −101.5 / −47.1 | **412.3 / 406.2** | **$10,081** / $9,931 | $5,863 ($239.8bn / $234.9bn) | $13,846 (about $566bn) |
| Los Angeles metro (inside CA) | 4.50M | 28.8 / 34.3 | −55.9 / −48.8 | 84.7 / 83.0 | $18,816 / $18,441 | $14,969 | $26,353 |

[CALCULATION: `derived/state_summary.csv`]

Matching whites state by state raises the delta at union ages from A3's national-rate $330bn to $412bn, because the union lives where local whites pay the most tax. California whites at the union's ages pay other residents $92bn more than they cost them. [CALCULATION]

At union ages, schools and most age-driven lines cancel, and income taxes carry the gap. Per union member in California and Texas:

| Line | California | Texas |
|---|---:|---:|
| Whole delta | $14,133 | $8,567 |
| of which income taxes | $10,118 | $4,989 |
| of which payroll taxes | $2,629 | $1,738 |
| of which sales and excise taxes | $2,091 | $1,463 |

[CALCULATION: `derived/state_buckets.csv`]

**Cash and accrual at union ages.** Accrual is not rerun by state. At the union's ages cash and accrual nearly agree nationally: A3 is $330bn on cash and $319bn on accrual. The state figures should move by a similar few percent. [INFERENCE]

### Reconciliation with the partial ledger of 2026-09-21

The partial ledger's age-matched gap compares the union at its own ages with local third-plus whites at the same ages. That is this arm's "union ages" comparison. The memo's headline figures (CA −$12,133, TX −$7,479, LA −$17,196) are standardized to white ages, which is a different comparison. [DATA: `ledger_stress_2026_09_17/derived/state_matched.csv`]

$ per union member, low end:

| | California | Texas | National (state × age) |
|---|---:|---:|---:|
| Partial ledger, age-matched gap | −14,467 | −8,115 | −10,069 |
| Full-account balance at union ages, no responses | −20,538 | −12,449 | −14,521 |
| of which capital, property and production taxes | −6,560 | −3,864 | |
| of which earnings-keyed and per-head lines | +1,168 | +806 | |
| **Full-account cost delta under the case's responses** | **14,133** | **8,567** | **10,081** |
| of which capital return and production gain | −131 and −351 | −106 and −312 | |
| Both A arms | 19,640 | 11,644 | 13,846 |

[CALCULATION: `derived/state_summary.csv`, `derived/state_buckets.csv`; partial ledger DATA]

**What the full-account re-key adds on top of the partial ledger:**

- **At the case's rules, almost nothing net.** The per-person delta is 2% below the partial ledger in California, 6% above in Texas and 0.1% above nationally.
- **The additions largely cancel.**
  - On a no-response basis the full account adds capital, property and production taxes, which the partial ledger leaves out (it has no corporate tax): $6,560 per member in California and $3,864 in Texas.
  - Without them the California balance is −$13,978, close to the partial ledger's −$14,467.
  - The case holds those taxes at zero response, halves the earnings-keyed lines through their responses, and adds a small public-capital return and production credit that favour the union.

  [CALCULATION; INFERENCE]
- **The number moves only when those taxes respond.** The capital-tax and top-tail arms add $5.5k per member in California and $3.1k in Texas.
- **Price levels are still missing.** The partial ledger's price-level caveat carries over: nominal California gaps overstate real-resource gaps.

## Disconfirmation: what makes whites look worse

- **Age.** On cash the white slice's old-age lines cost others $170.5bn. Without them the slice costs others −$16.9bn at low, a net contribution, and +$33.9bn at high. Anyone who reads the cash basis as the right measure for an ageing group will see whites cost $154–204bn a year, 2–3× less than the union but not zero. [CALCULATION]
- **Medicare is understated.** MEPS excludes the institutionalized. Nursing-home residents are older and disproportionately white, so the white Medicare key (15.8%) is likely low. Medicaid LTSS comes from T-MSIS and is not affected. [INFERENCE]
- **Social Security accrual.** At 1.019 per tax dollar payable, whites earn as much per dollar as the union. On scheduled benefits it is 1.272 against 1.298. [CALCULATION] The progressive formula does not give whites a worse deal on the central basis, probably because whites' longer lives and older contributors offset their higher earnings. [INFERENCE]
- **Per-head lines keyed on earnings.** These charge whites $33bn more (economic affairs, other federal benefits). [CALCULATION]
- **The benchmark.** The all-residents slice costs others $224–274bn. So the union costs $85–87bn more than an average resident and whites $70bn less. The replacement delta is not just "whites are average". [CALCULATION]
- **Geography.** It favours whites on congestion. Their higher car use is not priced. [INFERENCE]
- **Missing production term.** No production term is scored for whites. If added whites mostly substitute for similar natives, the CES term for them is near zero or negative. The union's +$13.3bn / $8.8bn is credited to the union, which narrows the delta. [INFERENCE]
- **Assumed benefit-tax rate.** Raising whites' relative rate by 0.1 cuts their net OASDI accrual by about $1.4bn and adds about $1.7bn to the current benefit-tax receipt that accrual removes. The net is about +$0.3bn on the white cost. The assumption is immaterial. [CALCULATION, approximate]

## Limits

- This is not an engine run. On the union the rough keys land 3.4% / 7.3% below the engine's cost. If the same bias holds for whites it cancels in the like-for-like delta. The delta against the engine's union ($168–183bn) is the conservative reading only if whites are not also under-costed by the rough keys.
- Allocation arms are not carried; only responses and the capital rate move between ends.
- CPS under-reports programme dollars, and shares assume equal under-reporting across groups.
- A1 uses US-born MEPS and SPI keys for the third-plus generation.
- The justice age factor uses victim ages as an offending proxy.
- Removing or adding a native-born population is an accounting comparison. [FRAMING-SENSITIVE]

## Reproduce

From the repository root, in order. `accrual_white.py` reads the pension lane's cached CPS frame, about 2 minutes. `tabulate_white.py` reads the 2024 PUMS zip, about 5 minutes.

```sh
L=infra/immigration-fiscal/white_replacement_2026_09_28
node $L/engine_lines.cjs
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $L/rekey_white.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $L/accrual_white.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $L/tabulate_white.py
OPENBLAS_NUM_THREADS=1 uv run --no-project --with statsmodels python3 $L/spillovers_white.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $L/victim_cost_white.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $L/replacement_table.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $L/state_white.py
```

Every script was run twice. All 16 files in `derived/` were byte-identical across the two full runs (sha256), and every gate passed on both. `state_white.py` (Part F) was run twice after the `keyed()` refactor of `rekey_white.py`. Its two outputs and all 16 earlier files were byte-identical. Nothing was written to other lanes, and nothing was committed.

## v4 case (sept29), 2026-09-29

claude-opus-5-5

**Status, 2026-09-29 21:44 JST (from `date`): done; every gate passed; nothing committed (the lead commits).** The run was resumed after the machine rebooted at 20:51 JST. In this run the sept29 steps and every gate, both `rerun_lane.py` passes included, were rerun, and three outputs were added: `rule_alternatives_sept29.csv`, `attribution_sept29.csv` and `attribution_buckets_sept29.csv`. The log is at the end of this section.

**Verdict (sept29).** On the adopted v4 case, with both sides on the 39,712,493 people the account prices, the Mexican-origin union costs other residents more a year than the same number of third-plus-generation non-Hispanic white residents by the amounts below. The central comparison moves from $318.9 / 316.6bn on September 27 (ladder 274) to **$351.2 / 350.5bn**. [CALCULATION: `rekey_sept29.py` → `derived/headline_sept29.csv`]

| Union less whites, $bn a year, spec 48 / 11 | sept29 | Per union member | September 27, row 4 (ladder 274) |
|---|---|---|---|
| **Age artefact removed: A1 (whites at their own ages) on the case's accrual basis** | **351.2 / 350.5** | **$8,844 / 8,826** | 318.9 / 316.6 (A1 on accrual) |
| Age artefact removed the September 27 way: A3 (white rates at union ages), cash set | 351.9 / 350.9 | $8,862 / 8,837 | 325.4 / 322.0 |
| A3 on the accrual basis | 341.4 / 340.5 | $8,598 / 8,573 | — |
| **Raw cash at white ages: A1, cash set** | **197.1 / 196.4** | **$4,964 / 4,946** | 164.5 / 162.1 |
| **Local whites state by state, union ages, accrual basis** | **410.4 / 408.0** | **$10,334 / 10,273** | — |
| Local whites state by state, union ages, cash set | 437.7 / 435.2 | $11,021 / 10,960 | 407.5 / 401.9 |
| **California, union ages, accrual basis** | **189.5 / 188.2** | **$14,488 / 14,383** | — |
| California, union ages, cash set | 204.7 / 203.4 | $15,648 / 15,544 | 186.9 / 184.0 ($14,286 / 14,064) |

Per-member figures divide by 39,712,493, the account's row-4 count; every white slice is scaled to it. California's divide by its 13,082,783 union members on row-4 weights. On the accrual basis the other state pieces are Texas $8,908 / 8,849, the rest of the US $7,939 / 7,910 and Los Angeles $18,902 / 18,717 per member. [CALCULATION: `derived/state_summary_sept29.csv`]

- With the two convention arms (the CPS top tail of income tax spread in proportion, and capital-side taxes responding), A1 is $453.2 / 452.5bn on accrual and $299.1 / 298.4bn on the cash set. [CALCULATION: `derived/rekey_summary_sept29.csv`]
- Against the engine's union instead of the rough union, A1 is $347.2 / 360.8bn. The rough keys put the union at $375.5 / 424.6bn on accrual, against the engine's $371.4 / 434.8bn (+1.1% / −2.4%). On the cash set they put it at $294.9 / 344.0bn, against $294.7 / 361.8bn. [CALCULATION]
- Against 39.7M average residents (the all-residents slice), the union costs $209.0 / 209.3bn more on accrual, and third-plus whites cost $142.2 / 141.2bn less. [CALCULATION]

### What the accrual does to the age-artefact arm

On the cash set, charging white per-age rates at the union's ages (A3) raises the A1 delta by $154.8 / 154.5bn, from $197.1 / 196.4bn to $351.9 / 350.9bn. The case's accrual basis raises A1 by $154.1bn at both ends, to $351.2 / 350.5bn. That is within $0.7 / 0.4bn of A3 on cash, so the accrual already does what the A3 arm did. [CALCULATION]

With the accrual in, A3 comes out $9.8 / 10.1bn *below* A1. At the union's ages the white slice costs other residents more than at its own. The table gives A3's cost less A1's at the low end, by bucket. [CALCULATION: `derived/rekey_buckets_sept29.csv`]

| Bucket, $bn | Cash set | Accrual (the case) |
|---|---|---|
| Social Security | −145.0 | −7.0 |
| Medicare | −104.4 | −67.6 |
| Medicaid | −14.4 | −14.4 |
| Veterans and military medical | −11.2 | −11.2 |
| Per-head lines | −17.0 | −17.0 |
| Schools and colleges | +73.7 | +73.7 |
| Income, payroll, sales and property taxes | +56.0 | +45.8 |
| Police, welfare and the capital return | +7.5 | +7.5 |
| **A3 less A1** | **−154.8** | **+9.8** |

On accrual, Social Security is each group's accrual per tax dollar times its payroll taxes, so it no longer follows the age mix. Medicare Parts B and D (62.5% of the line under the case's rule) and Medicaid's long-term care stay on current benefits, so they still fall at the union's younger ages. The schooling and the lower taxes that come with those younger ages now outweigh them. On sept29 the age-artefact figure is therefore A1 on the accrual basis. A3 remains a sensitivity: it re-prices the white slice at a younger age mix, and on accrual that favours the union by $9.8 / 10.1bn. [CALCULATION; the reading is INFERENCE] The state arm shows the same thing. On accrual, local whites at their own ages give $424.8 / 422.7bn, above the $410.4 / 408.0bn at union ages. On the cash set, own ages give $286.1 / 284.0bn. [CALCULATION: `derived/state_summary_sept29.csv`]

### From September 27 to sept29

The table walks the A1 delta from ladder 263's figure to the sept29 case, in $bn. It uses two decimals with controlled rounding, so the printed steps add to the printed total. [CALCULATION: `derived/attribution_sept29.csv`, `derived/attribution_buckets_sept29.csv`]

| Step | Low | High |
|---|---|---|
| September 27 case, published weights (ladder 263) | 157.16 | 154.62 |
| Audit row-4 weights (ladder 274: 164.46 / 162.13) | +7.30 | +7.51 |
| sept29's lines, nationals and responses; no group state-priced or miles-keyed | +26.76 | +26.54 |
| State prices and road miles for every group (rule 4), giving the cash set's 197.13 / 196.41 | +5.91 | +7.74 |
| The pension accrual (rule 3) | +154.11 | +154.11 |
| **sept29 case** | **351.24** | **350.52** |

- **sept29's lines** add $24.9bn at the low end through capital, property and production taxes. Item 5 lets owner-occupied property tax respond at 0.763, where September 27 held it at 0, and the white slice holds more home value. A line-level check through this library breaks the bucket down [CALCULATION: scratch check, not a lane output]:
  - owner-occupied property +$21.9bn (whites' receipts lost rise by $42.0bn, the union's by $20.2bn);
  - public housing's split (item 1) +$3.5bn;
  - personal property +$0.9bn;
  - tenant-occupied property −$1.4bn.

  The rest of the step (+$1.9bn) is mostly the union's production term on row-4 weights (item 2, +$1.6bn).
- **Rule 4** adds $5.9 / 7.7bn. At the low end:
  - the union lives where police, courts and prisons cost more: +$9.1bn;
  - it lives where health services cost more, and its road key exceeds its earnings key (per-head lines): +$5.4bn;
  - road capital keyed by miles: +$0.9bn;
  - it pays more sales, gasoline and licence tax in those states: −$9.5bn.
- **The accrual** adds $154.1bn. On Social Security (+$128.1bn) the union's cost rises $52.0bn as its workers' accruals replace its small current benefits, and whites' cost falls $76.1bn as their retirees' benefits give way to their workers' accruals. Medicare adds +$40.2bn. The tax on benefits leaving income-tax receipts, most of it whites', subtracts $14.2bn. [CALCULATION: `derived/attribution_buckets_sept29.csv`]

### Rules designed, with the alternative beside each

The rules are stated in `rekey_sept29.py`'s docstring. Each alternative is priced in `derived/rule_alternatives_sept29.csv`. [CALCULATION] The changes below are to the A1 delta on the accrual basis, at spec 48 / 11.

1. **Lines, responses, capital and group keys.**
   - The case's lines, responses, capital stocks and rates are used as they are. Each group's shares are the September 27 rough keys on row-4 weights.
   - The rough Mexican-origin run keeps the engine's medical and justice shares, read from the cash set. The accrual set's Medicare amount already carries the accrual, and taking shares from it would apply the Part A accrual twice.
   - No alternative is priced, because the accrual set's shares would be a double count, not a different choice.
2. **The two receipt lines v4 splits out** (the brief's second trap: `rekey.py` raises a KeyError on them).
   - `housing_enterprise_surplus` is keyed on housing subsidies, where the case keys it on housing support.
   - `tenant_occupied_property` is keyed on cash renters' consumption (`H_TENURE` 2). The case uses contract rent, which the CPS lacks. The proxy holds for the union: 11.67% against the engine's 11.47%.
   - The housing-subsidy key gives the rough union 12.48% of public housing against the engine's 7.52%. That is the same over-assignment as on the rough `housing_subsidies` line.
   - *Alternative:* the keys of the lines v4 split them from: per head, as inside `enterprise_surplus`, and capital income, as inside `remaining_production_property`. It adds **+$5.5bn** at both ends and on both bases: the union's cost rises $4.4bn and A1's falls $1.1bn.
3. **The pension accrual for every group at its own accrual per tax dollar** (the case's central).
   - Social Security is the group's net OASDI ratio times its OASDI taxes: employee, employer and the case's self-employment share.
   - Medicare swaps the Part A share (37.5%) of its cash amount for the group's Part A ratio times its HI taxes.
   - Federal income tax loses the tax on the group's 2024 benefits.
   - The ratios, on payable benefits:

     | Group | Net OASDI ratio | Part A per HI tax dollar | Source |
     |---|---|---|---|
     | Third-plus whites | 0.9346 | 0.9938 | `accrual_ratios.csv` |
     | NH Black (the `nh_black_rough` rows) | 1.0396 | 1.5522 | the Black lane's `accrual_ratios.csv` |
     | All residents | 0.9496 | 1.1403 | the Black lane's `accrual_ratios.csv` |
     | The union | 0.9737 | 1.4609 | the case's own ratios |
   - *Alternative 3a:* every group at the union's ratios, keeping its own benefit-tax rate and timing: **−$23.4bn** at both ends. Whites' Part A ratio is 0.99 against the union's 1.46.
   - *3b:* the tax on benefits uses the case's low-end (shared) receipt per benefit dollar at both ends, because the rough income-tax key shares a tax unit's tax among its members. The case's own rule at each end (personal at spec 11) gives **+$0.0 / +1.1bn**.
4. **State prices (item 9) and road miles (item 10) for every group, from its own residence and driving.**
   - The group's state indexes weight the state lane's per-state relatives by its CPS persons: adults for licences, and persons times the state's imprisonment rate for corrections.
   - Its miles share uses NHTS 2017 driver miles per person aged 5+ at its own age structure. Relative to all residents, NH whites drive 1.100 and NH Black residents 0.773. The union keeps the case's own ratio of 0.874 to the non-Hispanic average.
   - The engine prices these lines for the union only. Their national is 0, so `rekey.py`'s national × share would have priced them at 0 for every group, silently (the brief's first trap).
   - *Alternative:* other groups at national prices and the September 27 road keys, with the union keeping its terms: **−$2.1 / −2.0bn**.
5. **The union-only corrections stay as on September 27.**
   - School reprice, college re-key and lane constants are at the engine's amounts for the union and absent for other groups.
   - The production gain is the union's only; item 2 moves it +$1.6bn.
   - Items 3 (IRS key), 5's vehicle key for personal property tax, 6a (payroll compliance) and 7 (workers' compensation) refine the engine's union keys. They have no counterpart in the rough CPS keys that every group shares.
   - No alternative is priced. The gap between the rough and the engine's union bounds what these refinements do: A1 against the engine's union is $347.2 / 360.8bn, against $351.2 / 350.5bn like for like.

**Frame.** Row-4 weights are set as ladder 274's `population_basis_2026_09_29/white_count.py` set them: the engine's factors on the Mexico-born outside California and Texas. The row-4 union has 39,712,494.5 CPS persons against the account's 39,712,493.3 (gate: within 2). Two setup gates catch both traps if a later case adds lines: one fails when a line of either dump lacks a key, the other when a national-0 line with an amount lacks a rule.

### Limits of the sept29 figures

- This is the rough re-key, not an engine run. The rough union lands +1.1% / −2.4% off the engine's union on accrual, and +0.1% / −4.9% on the cash set.
- Third-plus whites' relative benefit-tax rate stays at the lane's assumed 1.0. The statutory proxy, calibrated to the union's measured rate, gives 0.974 (`black_comparator_rough_2026_09_28/derived/benefit_tax_proxy.csv`); section A found a 0.1 change worth about $0.3bn.
- Medicare Parts B and D and Medicaid's long-term care stay on current benefits in the case's rule. That is why an age effect survives on accrual.
- Driver miles by group are NHTS 2017's, by race, ethnicity and five-year age band.

### Gates (this run, after the reboot)

1. **Old cases unchanged.** `rerun_lane.py` with the lane's eight September 27 commands (`v4_inputs.py` and `rekey_sept29.py` allowed unrun) reports **IDENTICAL, 43/43 files** (21:40–21:41 JST).
   - Two earlier attempts, at 21:13 and 21:35, stopped at `spillovers_white.py`: its `uv run --with statsmodels` hit a PyPI connect timeout.
   - The passing run set `UV_OFFLINE=1`, which takes statsmodels 0.15.0 from uv's cache. The same command online passed in all four gate-4 passes. This was a transport failure, not a lane failure.
2. **sept29 outputs.** Each step exits 0 with no failed gate:
   - `engine_lines.cjs sept29` and `sept29_cash`;
   - `v4_inputs.py` (10 gates);
   - the Black lane's `accrual_black.py`;
   - `rekey_sept29.py` (151 gates).
3. **Oracle.**
   - The dumps' costs equal `main_case_bands.csv`'s `adopted` row, $371.4146 / 434.8410bn, and its `cash_set` row, $294.7011 / 361.8175bn. The tolerance is 5e-5 against the CSV's four decimals.
   - The lane's cost formula on the engine's amounts reproduces each dump to 1e-9.
   - The case's pension rule, applied to the cash set's union amounts, reproduces the accrual set's Social Security, Medicare and income-tax amounts to 1e-9.
4. **Two passes after the sept29 run.** Two `rerun_lane.py` passes with all twelve commands, September 27 and sept29, run after the sept29 run, report **IDENTICAL, 43/43 files, both passes** (21:37–21:38 and 21:38–21:39 JST). An earlier cycle, before the bucket file was added, also passed twice (42/42, 21:16–21:24).

### Reproduce (sept29), after the September 27 list

```sh
L=infra/immigration-fiscal/white_replacement_2026_09_28
B=infra/immigration-fiscal/black_comparator_rough_2026_09_28
node $L/engine_lines.cjs sept29
node $L/engine_lines.cjs sept29_cash
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $L/v4_inputs.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $B/accrual_black.py   # rekey_sept29.py reads its accrual_ratios.csv
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $L/rekey_sept29.py
```

**New files (no existing output moved).**
- Scripts: `v4_inputs.py` and `rekey_sept29.py`.
- In `derived/`: `engine_lines_sept29.json`, `engine_lines_sept29_cash.json`, `v4_state_relatives.csv`, `v4_nhts_vmt.csv`, `rekey_summary_sept29.csv`, `rekey_buckets_sept29.csv`, `state_summary_sept29.csv`, `state_buckets_sept29.csv`, `headline_sept29.csv`, `v4_group_terms_sept29.csv`, `rule_alternatives_sept29.csv`, `attribution_sept29.csv` and `attribution_buckets_sept29.csv`.

`engine_lines.cjs` gained a case argument; its default output, `engine_lines.json`, is byte-identical (gate 1). The Black lane imports `rekey_sept29.py` as its library, and this lane reads that lane's `accrual_ratios.csv`, so commit the two lanes together.

### Log

- 2026-09-29 20:14 JST: resumed after the weekly usage limit stopped the run at 17:24 JST (per the lead). Only this stub had been written; the reads and probes before the stop were not saved in the lane.
- 2026-09-29 20:35 JST: confirmed so far [CALCULATION]:
  - `engine_lines.cjs` (kept identical to the Black lane's) takes a case argument; the default output is byte-identical; `engine_lines_sept29.json` and `engine_lines_sept29_cash.json` hold the case ($371.41 / 434.84bn) and its cash set ($294.70 / 361.82bn).
  - `v4_inputs.py` → `derived/v4_state_relatives.csv`, `v4_nhts_vmt.csv`. Gates: the union's nine state indexes reproduce the state lane (1e-8); NHTS 2017 Hispanic / non-Hispanic driver miles per person 5+ reproduce the congestion lane's 0.8930224334. Driver miles per person 5+ relative to all residents: NH white 1.100, NH Black 0.773, Hispanic 0.910. Third-plus NH whites live where police cost 0.94 and health 0.91 of the national per-resident level (union 1.115 and 1.251).
- 2026-09-29 20:42 JST: first sept29 run, all gates passed [CALCULATION: `rekey_sept29.py` → `derived/headline_sept29.csv`]: against 39.71M third-plus whites the union costs other residents $351.2 / 350.5bn more a year on the case's accrual basis (A3, white rates at union ages: $341.4 / 340.5bn); on the cash set at white ages $197.1 / 196.4bn; against local whites state by state at union ages $410.4 / 408.0bn on accrual ($437.7 / 435.2bn on the cash set); California $14,488 / 14,383 per union member on accrual ($15,648 / 15,544 on the cash set). With other groups at national prices and the September 27 road keys (the alternative to rule 4) the A1 delta is $349.2 / 348.5bn.
- 2026-09-29 21:03 JST: the machine rebooted at 20:51 JST during the gate-4 run of 20:48, and the scratch logs were lost. Resumed from the recovered transcript: the sept29 code and outputs were on disk; every sept29 CSV parsed with the expected row count; tracked outputs matched HEAD.
- 2026-09-29 21:12 JST: added the rule alternatives and the attribution to `rekey_sept29.py`. `run29`'s `local` flag became `rule4` ("all", "union", "none"). The headline and summary values printed the same as before the change, at four decimals.
- 2026-09-29 21:13–21:26 JST: first full gate cycle. Gate 1 Black IDENTICAL; gate 1 white stopped on the PyPI timeout; sept29 run clean; gate 4 IDENTICAL twice for each lane (42/42 white, 23/23 Black).
- 2026-09-29 21:27 JST: added `attribution_buckets_sept29.csv`, with a gate that every step's buckets add to its cost (1e-9).
- 2026-09-29 21:35–21:41 JST: second full cycle, the one reported under Gates above.
- 2026-09-29 21:47 JST: this section written; status line set.

## v5 case (oct05), 2026-10-05

[2026-10-05: on main case v5 (`oct05`, `../main_case_2026_10_05/`), with both sides on the lineage's 42,752,213, the
union costs other residents **$368.8 / 371.9bn** a year more than the same number of third-plus non-Hispanic whites on
the case's accrual basis (A1), **$8,627 / 8,698 per member**. On the September 29 case (`sept29`, both sides on
39,712,493) it was $351.2 / 350.5bn, $8,844 / 8,826 per member. The total rises with the 3.04M added people and the
gap per member falls, because the added people cost $6,309 / 8,790 each (the case lane's +$19.18 / 26.72bn) against
the identified union's $9,447 / 10,683 on the rough keys. [CALCULATION: `rekey_sept29.py --case oct05` →
`derived/headline_oct05.csv`]]

[2026-10-07: the oct05 files are rebuilt on the IPEDS keys for Pell and public higher education, a defect fix decided in
the v6 propagation (section "v6 case (oct07)", "The IPEDS keys"). On them A1 is **$373.9 / 376.8bn**, $8,746 / 8,815
per member (the figures below, on the rough keys of September 27: $368.8 / 371.9bn); local whites $429.2 / 430.6bn;
California $197.9 / 197.6bn; raw cash at white ages $208.0 / 212.3bn. The tables and bullets below keep the rough keys.
[CALCULATION: `derived/headline_oct05.csv`, `ipeds_terms_oct05.csv`]]

claude-opus-5-5 (v5consC)

**The rule (the case lane's Consumers row: both sides on 42.75M).** The CPS keys cannot see the 3,039,720 descendants
v5 adds, who no longer report Mexican origin. So:
- **The union's side** is the rough union on the identified 39,712,493 at v5's responses, plus the added people at
  the case lane's own amounts. `engine_lines.cjs` writes four oct05 dumps. `oct05` and `oct05_cash` are the case and
  its cash set. `oct05_union` and `oct05_union_cash` are the identified union at v5's responses: the base's v4 models
  plus audit row 8's change only, at v5's specifications. Their difference, line by line, is the added people's
  amount, capital return and production term. The library adds it to the union's side (the engine and the rough
  union) after the pension rule, which the added people do not follow: their accrual is the lane's.
- **Every scaled slice** (A1, A2, A3, A4, the all-residents slice) is on 42,752,213. The NH Black group keeps its own
  count.
- [ASSUMPTION] **A3's union ages are the lineage's**: the union's age structure, with the added people at the
  identified G3+ members' ages, as the lineage lane prices them (the G3+ records' weights scaled by 3,039,720 /
  14,342,574.76 on this frame).
- [ASSUMPTION] **The state arm** gives each union piece the added people's cost in proportion to its share of the
  identified G3+ persons, and its white pieces the piece's lineage count at the piece's lineage ages. California's
  union becomes 13.95M (13.08M on sept29).
- The same comparison **on the identified 39,712,493 at v5's responses** (the overlay off, every slice on 39.71M) is
  computed beside, in `headline_oct05.csv` (`identified_bn`) and as attribution steps 1–3.

**Headline** ($bn a year, spec 48 / 11; per member on 42,752,213, California's on its 13,949,823):

| Union less whites | oct05 | Per member | Identified 39.71M at v5's responses | sept29 |
|---|---|---|---|---|
| **A1, accrual (central)** | **368.8 / 371.9** | **$8,627 / 8,698** | 351.5 / 350.8 ($8,851 / 8,833) | 351.2 / 350.5 ($8,844 / 8,826) |
| A3 (white rates at the lineage's ages), accrual | 353.9 / 356.8 | $8,278 / 8,346 | 341.6 / 340.6 | 341.4 / 340.5 |
| A3, cash set | 363.0 / 367.3 | $8,491 / 8,592 | 352.1 / 351.1 | 351.9 / 350.9 |
| **A1, cash set (raw cash at white ages)** | **202.9 / 207.3** | **$4,746 / 4,849** | 197.4 / 196.7 | 197.1 / 196.4 |
| **Local whites state by state, union ages, accrual** | **427.7 / 429.1** | **$10,003 / 10,036** | 410.7 / 408.3 | 410.4 / 408.0 |
| Local whites, cash set | 454.4 / 457.2 | $10,628 / 10,694 | 438.0 / 435.6 | 437.7 / 435.2 |
| **California, union ages, accrual** | **197.2 / 196.8** | **$14,133 / 14,110** | 189.7 / 188.4 ($14,502 / 14,397) | 189.5 / 188.2 ($14,488 / 14,383) |
| California, cash set | 212.6 / 212.7 | $15,243 / 15,248 | 204.9 / 203.5 | 204.7 / 203.4 |

[CALCULATION: `derived/headline_oct05.csv`, `rekey_summary_oct05.csv`, `state_summary_oct05.csv`]

- Step 4 of the attribution moves A1 by +$17.36 / +21.09bn. The union's side gains the added people, +$19.18 /
  26.72bn. The white slice grows by 42,752,213 / 39,712,493 = 1.076543, +$1.81 / 5.62bn. v5's responses alone (step
  3 against sept29) move A1 by +$0.24 / +0.25bn. [CALCULATION: `derived/attribution_oct05.csv`]
- A3 is now $15.0 / 15.0bn below A1 (sept29 $9.8 / 10.1bn). The lineage's ages are younger than the identified
  union's, and white rates at younger ages charge more schooling. [CALCULATION]
- Against the engine's union, A1 is $364.8 / 382.1bn. With the two convention arms it is $480.9 / 484.9bn on accrual.
  Against 42.75M average residents the union costs $215.7 / 219.8bn more. [CALCULATION: `rekey_summary_oct05.csv`]
- On the rough keys the identified union is $375.2 / 424.2bn against the engine's $371.1 / 434.5bn at v5's responses.
  The union's side on 42.75M is $394.3 / 451.0bn against the case's $390.3 / 461.2bn.

**Gates (`rekey_sept29.py --case oct05`: 177 gates, exit 0).**
- The case dumps are `main_case_bands.csv`'s `adopted` and `cash_set` rows (5e-5). The lane's cost formula reproduces
  the case dumps (1e-9) with the added people's amounts on the union dumps, and each union dump on its own amounts.
- Each union dump is the September 29 case plus the union's response move, and each case dump less its union dump is
  the lane's G3+ and white parts, at both ends (`summary.json` `change_at_fixed_specifications`, 1e-9). The
  payload's pension, state-price and road meta are the September 29 payload's.
- The frame's identified G3+ is the lineage's `identified_g3plus`: 14,342,574.76 against 14,342,574.61 (1 person).
  The union plus the added people at G3+ weights is the lineage population within 2 persons, the frame's union gate:
  42,752,214.13 against 42,752,212.92.
- Step 4 moves the union by exactly the added people's cost and the NH Black group not at all. It moves every slice
  at fixed ages by 1.076543 (1e-9 relative; the re-key is linear in a slice's weights).
- `rekey_sept29.py` (sept29) rewrites its files byte for byte (151 gates).
- `rerun_lane.py --online` with all eighteen commands (the eight September 27 ones, the five sept29 ones with the
  Black lane's `accrual_black.py`, and the five oct05 ones below): **IDENTICAL 56/56, exit 0** (2026-10-06
  00:32:24–00:33:45 JST). `--online` lets uv fetch statsmodels for `spillovers_white.py`; the offline pass stopped
  there because statsmodels was not in uv's cache.
- In `attribution_oct05.csv`, steps 1–3 are labelled as the identified union at v5's responses (`STEPS_IDENTIFIED`),
  since on oct05 step 1 also carries v5's response move.

**Reproduce (oct05), after the sept29 list.**

```sh
L=infra/immigration-fiscal/white_replacement_2026_09_28
for c in oct05 oct05_cash oct05_union oct05_union_cash; do node $L/engine_lines.cjs $c; done
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $L/rekey_sept29.py --case oct05
```

New in `derived/`: the four `engine_lines_oct05*.json` dumps and `rekey_summary_oct05.csv`, `rekey_buckets_oct05.csv`,
`state_summary_oct05.csv`, `state_buckets_oct05.csv`, `headline_oct05.csv`, `v4_group_terms_oct05.csv`,
`rule_alternatives_oct05.csv`, `attribution_oct05.csv` and `attribution_buckets_oct05.csv`. `rekey_sept29.py` gained
`use_case()` (sept29 at import), the overlay in `run29()`, `on_lineage()`, `identified()`, `lineage_setup()`,
`lineage_gates()`, `headline_lineage()` and `--case`; importers call `use_case()` before `setup()`.

## v6 case (oct07), 2026-10-07

[2026-10-07: on main case v6 (`oct07`, `../main_case_2026_10_07/`), with both sides on the lineage's 42,752,213 and
every group on the IPEDS keys for Pell and public higher education, the union costs other residents **$380.3 /
384.7bn** a year more than the same number of third-plus non-Hispanic whites on the case's accrual basis (A1), **$8,896
/ 8,998 per member** (v5 on the same keys without the tuition term: $373.9 / 376.8bn). Against local whites state by
state at union ages it is **$430.3 / 433.1bn** (v5 $429.2 / 430.6bn). On the rough keys of September 27, A1 would be
$373.8 / 378.2bn: the IPEDS keys and item 4's tuition term add $6.55 / 6.47bn, and Pell, which the rough keys charged
by Social Security receipt, alone adds $6.97bn. Item 4's hospital-fee term stays beside the comparators' central, at
the team lead's decision; with it A1 would be $383.0 / 387.3bn. From v5 to v6 the white slice's cost falls: the 2026
Trustees' separate-funds path lowers its Social Security and Part A accrual, and retiree health on accrual takes pay-go
federal retiree benefits off a slice the rough keys charge by Social Security receipt. [CALCULATION: `rekey_sept29.py
--case oct07` → `derived/headline_oct07.csv`, `ipeds_terms_oct07.csv`]]

claude-opus-5-5 (prop-d)

**Rules.** The oct05 rules carry over (the case lane's Consumers row: both sides on 42.75M). v6 adds four items,
`meta.items` of the case payload, and the library takes each by its kind, driven from that registry (the case lane's
Consumers table, R1–R4):
- [ASSUMPTION] **Item 1, the pension accrual on the 2026 Trustees' separate-funds path** (`pension_tr2026`, two cell
  shifts on Social Security and Medicare with union and lineage parts). The union dumps carry its union parts and the
  added people its lineage parts. Every other group is priced on the same path: `accrual_white.py --case oct07` and
  the Black lane's `accrual_black.py --case oct07` rebuild the payable ratios through the pension lane's own code
  (`tr2026_path.py`), and the union's row must reproduce the case's (5e-9). Net OASDI accrual per tax dollar, 2025
  reports → 2026 path: union 0.973667 → 0.953547, third-plus NH whites 0.934598 → 0.916489; Part A per HI tax dollar,
  whites 0.993818 → 0.988833. [DATA: `derived/accrual_ratios_oct07.csv`]
- [ASSUMPTION] **Item 2, retiree health on accrual** (`retiree_health`, ten national-scale edits). Its edits change
  national totals, so every group takes them through the rough keys' shares of those lines, as the engine does.
  Other federal benefits fall by $19.8bn (pay-go retiree benefits, a legacy at response 0) and nine service lines rise
  by the accrual. The rough keys charge other federal benefits by Social Security receipts, so the old white slice
  sheds more of the pay-go benefits than the union.
- [ASSUMPTION] **Item 3, the added people at their measured age mix** (`added_age_mix`, the lineage item). The case
  less the union dumps carries it, as the added people's amounts. A3's union ages put the added people at the measured
  mix (`meta.lineage.age_mix`): each identified G3+ record's weight is tilted by its band's measured over identified
  share, so with the tilt at 1 it is v5's placement. The state arm keeps each piece's added count (its share of the
  identified G3+) and tilts its ages the same way.
- [ASSUMPTION] **Item 4, user fees and the education keys** (`user_fees`, union-only). The union dumps take it whole and
  the added people none of it. In the rough re-key the union keeps the fee item where its lines are the union's own
  (`school_reprice`, `college_rekey`, rule 5's union-only lines) and where it takes the engine's share (health
  services). On `education_services` and `other_federal_benefits` every group, the rough union included, takes the
  IPEDS keys below, so the item's higher-education and Pell terms reach both sides by one rule. (Before the fix the
  rough union carried neither, since those lines took the CPS keys: +$0.26 / 0.36bn left out on its side.) The carrier
  receipt lines are union-only lines (the rough union takes the engine's amount, every other group 0). The fee item's
  capital offsets go to the rough union where it takes the engine's key for the component they offset (health: about
  $0) and to no other group.
- [ASSUMPTION] **The IPEDS keys, for every group on oct05 and oct07** (a defect fix of the rough keys, decided by the
  team lead in this propagation; section "The IPEDS keys" below). sept29 keeps the rough keys of September 27.

**Headline** ($bn a year, spec 48 / 11; per member on 42,752,213, California's on its lineage count):

| Union less whites | oct07 | Per member | Identified 39.71M at v6's responses | oct05 (IPEDS keys) |
|---|---|---|---|---|
| **A1, accrual (central)** | **380.3 / 384.7** | **$8,896 / 8,998** | 361.1 / 360.1 | 373.9 / 376.8 |
| A3 (white rates at the lineage's ages), accrual | 356.6 / 361.0 | $8,342 / 8,443 | 345.5 / 344.2 | 355.4 / 358.3 |
| A3, cash set | 364.9 / 371.2 | $8,535 / 8,683 | 355.5 / 354.3 | 364.6 / 368.8 |
| **A1, cash set (raw cash at white ages)** | **212.2 / 218.6** | **$4,964 / 5,112** | 206.4 / 205.4 | 208.0 / 212.3 |
| **Local whites state by state, union ages, accrual** | **430.3 / 433.1** | **$10,064 / 10,130** | 414.6 / 412.0 | 429.2 / 430.6 |
| Local whites, cash set | 455.8 / 460.6 | $10,661 / 10,774 | 441.3 / 438.6 | 456.0 / 458.8 |
| **California, union ages, accrual** | **198.5 / 198.5** | **$14,227 / 14,232** | 191.6 / 190.2 | 197.9 / 197.6 |
| California, cash set | 213.4 / 214.0 | $15,296 / 15,343 | 206.5 / 205.0 | 213.4 / 213.4 |

[CALCULATION: `derived/headline_oct07.csv`, `rekey_summary_oct07.csv`, `state_summary_oct07.csv`]

- A1 rises by $6.43 / 7.85bn from v5 on the IPEDS keys. The white slice costs $5.38 / 5.30bn less: the 2026 path
  lowers its Social Security and Medicare accrual by $3.51bn; its per-head lines fall by $3.04 / 2.96bn, as retiree
  health takes pay-go benefits out of other federal benefits (the rough keys charge that line's non-Pell part by Social
  Security receipt); schools and police rise by $1.13bn (retiree health's accrual and the tuition term); other lines
  +$0.04bn. The union's side rises by $1.05 / 2.55bn: schools and colleges +$3.41 / 4.52bn with the fee item, Social
  Security and Medicare −$3.65 / 4.37bn, the rest +$1.29 / 2.40bn. [CALCULATION: `rekey_buckets_oct07.csv` against
  `rekey_buckets_oct05.csv`]
- On the identified 39.71M at v6's responses (attribution step 3), A1 is $361.1 / 360.1bn, $4.9 / 4.7bn above v5's
  ($356.2 / 355.4bn on the same keys). Step 4 adds the lineage, +$19.2 / 24.6bn: the added people +$20.3 / 29.5bn on
  the union's side, less the white slice's growth by 1.076543 ($1.1 / 4.9bn). On v5 step 4 was +$17.7 / 21.4bn
  (+$19.2 / 26.7bn less $1.5 / 5.3bn); the measured ages and the items' lineage parts add $1.1 / 2.8bn to the added
  people. [CALCULATION: `derived/attribution_oct07.csv`, `attribution_oct05.csv`; one decimal by controlled rounding]
- The rough union on 42.75M is $395.4 / 453.4bn against the case's $389.1 / 461.5bn (+1.6% / −1.8%). Against 42.75M
  average residents the union costs $221.3 / 226.6bn more (cash $121.6 / 129.0bn). With the two convention arms A1 is
  $492.8 / 498.3bn on accrual. [CALCULATION: `rekey_summary_oct07.csv`]

**The IPEDS keys** (`ipeds_keys.py` → `derived/ipeds_keys.json`; `rekey_sept29.py` `IPEDS_CASES` oct05 and oct07,
`FEE_CASES` oct07). The rough keys gave every group the CPS college key (enrolled at 16–24, any sector) on the
education line's higher-education part and charged other federal benefits, which hold Pell's $31.264bn (NIPA T3.12
line 26), by Social Security receipts: Pell fell on old whites and missed the young union. v6's fee item re-keys both
for the union alone. [ASSUMPTION] From oct05 on, every group, the rough union included, takes one rule, measured where
IPEDS measures it, by race:
- **Pell:** the line's amount is N·ss + P·(pell − ss), P = $31.264bn. A race's Pell share is its public undergraduate
  FTE share times its within-unit intensity, halfway between 1 and NPSAS:20's Pell dollars per undergraduate relative
  to all (white 0.880, Black 1.258, Asian 0.980) [SOURCE: NCES 2023-466, Tables A-5 and A-6, the fee lane's "mid" rule
  for Hispanic students], and at private institutions the public share times the race's private / public
  undergraduate enrollment ratio (IPEDS EF2023A: white 1.004, Black 1.296, Asian 0.763), weighted 0.68 / 0.32.
- **Public higher education:** the education line moves by N·h·(use − college), h = 0.1916 (BEA's consolidated
  higher-education weight, the fee lane's central), where use is the race's share of public institutions'
  education-and-related cost by FTE (the fee lane's `higher_ed.py` run unchanged with the race's FTE). The college
  capital stock is keyed 0.961 by use and 0.039 by the CPS key (κ, higher education's share of non-K-12 education
  investment).
- **On oct07 only, the fee terms**, as the fee item prices them for the union: tuition, R·(use − tuition) with R =
  $103.911bn, at residency θ = 1 for a race (IPEDS has no residency by race; the union keeps the fee lane's θ = 0.5),
  in the central; and hospital charges, Σ_q net_q·(s_q − s_K), by MEPS payer (Medicare, Medicaid, private) against the
  group's health key, **beside the central** for every group but the union, whose term is the case's own and comes with
  the engine's health share (the team lead's decision of 2026-10-07; the hospital bullet below).
- **Within a race** a group takes its race's share times its CPS college key over the race's (use and tuition), or its
  CPS education-benefit key over the race's (Pell). The rough union is its own race (the fee lane's shares on the
  identified 39.71M: use 0.116, tuition 0.098, Pell 0.169); the white slices take the white shares (use 0.456, tuition
  0.441, Pell 0.367), the NH Black group the Black ones (0.099, 0.095, 0.192), and an all-residents slice its CPS
  shares (no move).

| $bn a year, oct07, accrual (low / high where they differ) | Pell | Higher-ed use | College capital | Tuition | Move | Hospital (beside) |
|---|---:|---:|---:|---:|---:|---:|
| Rough union, 42.75M | +4.02 | −3.64 | −0.36 / −0.53 | +1.85 | +1.87 / +1.70 | the case's own |
| A1 third-plus whites, 42.75M | −2.95 | −1.89 | −0.19 / −0.28 | +0.35 | −4.68 / −4.77 | −2.65 |
| A3, white rates at union ages | +1.54 | −2.75 | −0.27 / −0.41 | +0.51 | −0.97 / −1.11 | −4.09 |
| **A1's gap (union less A1)** | **+6.97** | **−1.75** | **−0.17 / −0.25** | **+1.50** | **+6.55 / +6.47** | **+2.65** |
| NH Black, 41.95M (its own lane) | +2.97 | −12.79 | −1.25 / −1.88 | +0.33 | −10.74 / −11.37 | −0.44 |
| Indian origin, 6.08M (its own lane) | +0.45 | −0.75 | −0.07 / −0.11 | +0.28 | −0.09 / −0.13 | −0.49 |

[CALCULATION: `derived/ipeds_terms_oct07.csv` (each group on the rough keys of September 27, each part's move, the
hospital term beside and the union-minus-group change); the Black and Indian lanes' `ipeds_terms` files. The parts are
the same on the cash set. Two decimals by controlled rounding: each row's parts add to its move, and the gap row is
the union's less A1's.] The rough union's hospital term is item 4's, in the engine's health share it takes, and so in
its central. On oct05 the parts are the same without the tuition term (the use terms −3.62 for the union, −1.89 for
A1, −12.74 for the NH Black group): A1's gap moves +$5.07 / 4.98bn.

**Old → new**, accrual, $bn a year, low / high (the rough keys of September 27 → the IPEDS keys):

| Figure | oct05 | oct07 |
|---|---|---|
| A1 | 368.8 / 371.9 → **373.9 / 376.8** | 373.8 / 378.2 → **380.3 / 384.7** |
| A3, white rates at union ages | 353.9 / 356.8 → 355.4 / 358.3 | 353.8 / 358.2 → 356.6 / 361.0 |
| A1, raw cash at white ages | 202.9 / 207.3 → 208.0 / 212.3 | 205.7 / 212.1 → 212.2 / 218.6 |
| Local whites, union ages | 427.7 / 429.1 → **429.2 / 430.6** | 427.5 / 430.3 → **430.3 / 433.1** |
| California | 197.2 / 196.8 → 197.9 / 197.6 | 197.2 / 197.3 → 198.5 / 198.5 |
| Against an all-residents slice | 215.7 / 219.8 → 215.8 / 219.7 | 219.4 / 224.9 → 221.3 / 226.6 |
| NH Black, cost of removal | 541.7 / 589.7 → **530.7 / 578.0** | 538.6 / 586.7 → **527.9 / 575.3** |
| Indian origin, cost of removal | −73.1 / −64.8 → −73.5 / −65.2 | −73.7 / −65.4 → −73.8 / −65.5 |

[CALCULATION: `headline_oct05.csv`, `headline_oct07.csv` and `ipeds_terms_*`; the pre-fix figures are this lane's,
the Black lane's and the Indian lane's earlier oct05 files (committed) and oct07 runs (the rough-keys columns of the
`ipeds_terms` files)]

- **Pell drives it.** The union's Pell share (0.169) is about four times its Social Security share (0.040). The white
  slice's Pell share is below its Social Security share: whites hold 0.367 of Pell against 0.467 of public
  undergraduate FTE, and the slice holds more retirees. Use moves A1's gap the other way (−$1.7bn): IPEDS's
  cost-weighted use puts less public higher education on the union than the CPS enrollment key does (0.116 against
  0.131 of the line's higher-education part).
- **The hospital term stays beside the comparators' central** (the team lead's decision of 2026-10-07)
  [FRAMING-SENSITIVE]. Private payers pay government hospitals about 1.45 times cost (the fee lane's payment-to-cost
  ratio), and A1's MEPS payer shares (Medicare 0.169, private 0.166) are about twice its health key share (0.087, the
  OTHPUB key). So the term would credit the white slice with $2.65bn of insured payments while its hospital spending
  stays on that key: the fee side would take a measure of hospital use the spending side never charges. The union's
  side keeps item 4's hospital term, which is the adopted case's, so on this point the comparison counts the union's
  fees and not the comparators'. With the comparators' terms in, A1 would be $383.0 / 387.3bn, A3 $360.7 / 365.1bn,
  the NH Black cost $527.5 / 574.9bn and the Indian-origin cost −$74.3 / −66.0bn. [CALCULATION: `ipeds_terms_oct07.csv`
  `delta_with_hospital_bn` and `cost_with_hospital_bn`; the Black and Indian lanes' files] Revisit item (the lead's):
  key the comparators' health_services by MEPS hospital use on both the spending and the fee side. On such a key the
  white slice's spending would rise as well and the net credit would shrink [INFERENCE; not computed]. The union's
  uncompensated-care key has no comparator counterpart, an asymmetry that predates this fix.
- **Readers outside this propagation whose outputs move** (not edited here): `pension_legacy_2026_09_30` reads
  `group_lines_oct05/oct07.csv` (its comparator rows move on education services and other federal benefits, on oct07
  with the tuition term; its engine row does not); the evidence map's `quantity_registry.csv` rows 111–120 and the
  drift audit's `source_map.csv` rows that trace INDEX and FAQ figures to this lane's, the Black lane's, the Indian
  lane's and the legacy lane's oct05 files.

**Limits of the v6 figures** (`limits_oct07.py` → `derived/limits_oct07.csv`, read-only through this library at oct07;
the lead records each as a revisit item):
- [ASSUMPTION] **The case's own W keeps the rough keys** (the lead's decision for v6). The case prices 1,082,721
  members of the lineage as third-plus non-Hispanic whites (`meta.lineage.members.white`), on lines from
  `main_case_lineage_2026_10_05/white_lines.py` and `added_age_mix_2026_10_07/band_lines.py`, which import this library
  at its sept29 default. On the IPEDS keys they would cost $22.51 / 25.82 less each at the G3-rate persons' measured
  mix (v6's placement of them), so the case would be $0.024 / 0.028bn lower. At the identified G3+'s ages (v5's
  placement) it is $30.92 / 33.86 each, $0.033 / 0.037bn; at whites' own ages $117.72 / 119.89, $0.127 / 0.130bn.
  Item 4's tuition term, had they taken it, would add $12.48 each, $0.014bn. The moves are the same on the cash set.
- [ASSUMPTION] **Item 4's Pell share stays at the fee lane's assumed private/public ratio of 0.75** (the lead's
  decision). IPEDS's Hispanic undergraduate ratio is 0.677 (EF2023A, `ipeds_keys.json`); at it the union's Pell share
  falls from 0.1693 to 0.1650 and item 4's Pell term by $0.135bn at both ends, inside the fee lane's own arms (0.5 and
  1.0: shares 0.155 and 0.184). The same rule reproduces those arms' shares and terms (gate).
- [ASSUMPTION] **A race's tuition residency is θ = 1** (IPEDS has no residency by race; the union keeps the fee lane's
  0.5). At θ 0.5 / 1.5 the white race's tuition share is 0.399 / 0.482 and A1 is $379.4 / 383.8bn and $381.3 /
  385.6bn; A3 $355.3 / 359.6bn and $358.0 / 362.3bn; the NH Black cost $528.5 / 575.8bn and $527.3 / 574.7bn.
- **Left out or held** [ASSUMPTION]: sept29 keeps the rough keys (three lanes outside this propagation import
  `run29()` at the sept29 default and gate against its outputs); the case lane's own import of this library is
  untouched; the education line's part outside K-12 that is not BEA higher education (0.068 of the line) stays on the
  CPS college key.

**Gates (`rekey_sept29.py --case oct07`: 286 gates, exit 0; `--case oct05`: 255).** The IPEDS gates (`ipeds_gates`,
`ipeds_rows`): `ipeds_keys.json` carries the fee lane's current shares and constants; each dump's other federal
benefits hold Pell and one college stock is keyed; the rough union's shares are the fee lane's (1e-15 relative), the NH
Black group's are IPEDS's Black shares (1e-12), an all-residents slice's are its CPS shares (1e-12); the hospital
term's MEPS records are the library's and its payers `ipeds_keys.json`'s; positive control, the fee lane's union
reproduces its hospital residual 0.641351 (1e-9); for every group, basis and end the keys' parts are the move with the
fees off and the tuition part the rest with them on (1e-9), so the central carries no hospital term, and the terms'
cost is the summary's (5e-5). The hospital term beside is the run with it switched on (`HOSPITAL_ON`) less the
central. `ipeds_keys.py`: 16 gates, exit 0 (the fee lane's `higher_ed.py` on its own inputs reproduces its central
shares, 1e-9; the NPSAS:20 Hispanic ratio is the fee lane's constant, 1e-12; each race's Pell share at intensity 1 is
within 0.1 of its undergraduate FTE share). `limits_oct07.py`: 30 gates, exit 0 (the library's oct07 setup; the white
count is the payload's; the G3-rate mix is on the identified mix's bands and sums to 1; the share rule reproduces the
fee lane's central share and its 0.5 and 1.0 arms' shares and personal terms, 1e-12 and 1e-9; the case's
other_federal_benefits response is 1; at the central θ each group's cost is `rekey_summary_oct07.csv`'s, 5e-5, and the
union's cost does not move with a race's θ). Beside the oct05 gates (`items_gates`):
- The payload's meta is v5's but for the items' `meta_changed` (lineage, pension_accrual, retiree_health, user_fees)
  and the stamps. Its capital return is v5's with the items' offset components appended. The lineage's counts and the
  pension rule's other inputs are v5's.
- The edit sets do not interact (1e-9, each pair, both bases).
- On each basis and end, the case less v5's case is the case lane's change from v5. The union dump less v5's union
  dump is the edit sets' union parts plus its capital-return move, which lies inside the split items' capital parts.
  The added people less v5's are the items' lineage parts, the lineage item and its interactions (1e-9). On accrual
  the union dump is $368.74 / 432.01bn (v5 $371.12 / 434.53bn) and the added people $20.34 / 29.47bn (v5 $19.18 /
  26.72bn).
- The accrual files' union is the case's 2026 arm (1e-6), and the frame's identified G3+ ages are the age-mix lane's
  identified mix exactly.
- `engine_lines.cjs`'s union dump gates its national totals and carrier lines against the case model.
- The September 27 and sept29 runs rewrite their files byte for byte (sept29: 151 gates). The oct05 run with the
  IPEDS keys off (`IPEDS_CASES = ()`) reproduces every committed oct05 file byte for byte; with them on, eight oct05
  files change and `v4_group_terms_oct05.csv` does not. The four oct07 dumps rebuild byte for byte on the case lane's
  outputs of 15:03 JST.
- The library's importers outside this propagation, run read-only into scratch: `main_case_lineage_2026_10_05/
  white_lines.py` and `added_age_mix_2026_10_07/band_lines.py` rebuild their files byte for byte, and
  `net_contributor_comparison_2026_10_01/compare.py` its CSVs (its `audit.json` differs only in `rekey_sept29.py`'s
  source hash). Each imports the library at the sept29 default, which the fix leaves alone. Rechecked at 16:53–16:54
  after the hospital term moved beside.
- The hospital term moved beside after the 15:16 runs. Rerun in place, oct05 rewrites its files byte for byte but for
  `ipeds_terms_oct05.csv`, which gains the beside columns (its values are unchanged; oct05 has no fee terms); oct07
  changes nine files and leaves `accrual_ratios_oct07.csv`, the four dumps and `v4_group_terms_oct07.csv` as they were;
  no sept29 file changes.

**Reproduce (oct07), after the oct05 list.** `ipeds_keys.py` runs first, since oct05 reads its keys as well.

```sh
L=infra/immigration-fiscal/white_replacement_2026_09_28
B=infra/immigration-fiscal/black_comparator_rough_2026_09_28
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $L/ipeds_keys.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $L/rekey_sept29.py --case oct05
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $L/accrual_white.py --case oct07
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $B/accrual_black.py --case oct07
for c in oct07 oct07_cash oct07_union oct07_union_cash; do node $L/engine_lines.cjs $c; done
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $L/rekey_sept29.py --case oct07
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $L/limits_oct07.py
```

New in `derived/`: `ipeds_keys.json`, `ipeds_terms_oct05.csv`, `accrual_ratios_oct07.csv`, the four
`engine_lines_oct07*.json` dumps, `rekey_summary_oct07.csv`, `rekey_buckets_oct07.csv`, `state_summary_oct07.csv`,
`state_buckets_oct07.csv`, `headline_oct07.csv`, `v4_group_terms_oct07.csv`, `rule_alternatives_oct07.csv`,
`attribution_oct07.csv`, `attribution_buckets_oct07.csv`, `ipeds_terms_oct07.csv` and `limits_oct07.csv`; eight oct05
files rebuilt on the IPEDS keys. New scripts: `tr2026_path.py` (a module for the accrual scripts), `ipeds_keys.py`
and `limits_oct07.py`. `accrual_white.py`
gained `--case oct07` (its default output is unchanged); `engine_lines.cjs` gained the oct07 cases, the items' union
parts in the union dumps, and their gates; `rekey_sept29.py` gained the oct07 case, `items_gates()`, the age tilt, the
IPEDS keys (`IPEDS_CASES`, `FEE_CASES`, `HOSPITAL_ON`, `ipeds_move()`, `hospital_term()`, `ipeds_gates()`,
`ipeds_rows()`) and a wrapper that keeps the MEPS weights on each scenario for the hospital term (`rekey_white.py` is
unchanged).

### Log (times from `date`)

- 2026-10-07 14:28 JST: `ipeds_sizing_oct07.py` written and run (11 gates). A first run read the wrong race's Pell
  shares through a late-bound closure; fixed, and a gate now checks each race's Pell share against its own FTE share.
- After 14:28: the team lead decided to apply the keys in this propagation, to every comparator and both sides, as a
  named defect fix (oct05 and oct07; sept29 kept, as proposed to the lead, no objection received).
- 15:06:35 (file time): `ipeds_keys.py` run, 16 gates, `derived/ipeds_keys.json` written. Its NPSAS:20 intensities
  come from NCES 2023-466 Tables A-5 and A-6 (the PDF, sha256 dd373083…), replacing the sizing script's TRAINING-DATA
  ranges.
- 15:10–15:12 (log times): scratch runs. oct05 with the keys off reproduces every committed oct05 file; oct05 and oct07
  with them on pass every gate.
- 15:14:30–15:16:09 (file times): in place, September 27, sept29 (151 gates, byte for byte), oct05 (255 gates) and
  oct07 (286 gates). 15:15: the three outside importers checked in scratch (above).
- Between 15:36:04 and 15:38:07 (by `date`): `ipeds_sizing_oct07.py` and `derived/ipeds_sizing_oct07.csv` removed
  from the lane (never committed; `ipeds_keys.py` supersedes them).
- After the 15:16 runs the team lead decided: the hospital-fee term comes out of every comparator's central on oct07
  and stays beside, with a revisit item; θ = 1 for a race stays, with 0.5–1.5 printed; the case's own W keeps the old
  keys in v6, sized as a limitation; the union keeps item 4 at the fee lane's 0.75, with IPEDS's Hispanic 0.677 sized
  beside. v6 is final.
- 16:26:24–16:26:50 (log times): `HOSPITAL_ON = False`; oct05 (255 gates) and oct07 (286 gates) rerun in place, exit 0.
- 16:40:30–16:40:47 (by `date`): the W, Pell-ratio and θ sizings in scratch. 16:48:51–16:49:10: `limits_oct07.py`
  written and run in place (30 gates, exit 0), replacing them.
- 16:53:21–16:54:12 (by `date`): the three outside importers rechecked in scratch (above).
- 16:55:28–16:58:52 (by `date`): `rerun_lane.py --online` with all 27 commands (the eight September 27 ones, the five
  sept29 ones with the Black lane's `accrual_black.py`, the five oct05 ones, `ipeds_keys.py`, the two oct07 accrual
  runs, the four oct07 dumps, `rekey_sept29.py --case oct07` and `limits_oct07.py`; `--allow-unrun tr2026_path.py`, a
  module the accrual scripts import): **IDENTICAL 77/77, exit 0**.
