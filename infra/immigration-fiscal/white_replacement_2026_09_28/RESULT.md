claude-opus-5-5

**Verdict:** Under the September 27 case's rules, 40.9M third-plus-generation non-Hispanic white residents would cost other residents **$154bn / $204bn a year** at specs 48 / 11. On the same rough keys the Mexican-origin union costs them **$311bn / $359bn**. The fiscal replacement delta is **+$157bn / +$155bn a year on the case's cash basis**, about $3,800 per member, or +$168bn / +$183bn against the engine's own union figure. [CALCULATION: `rekey_white.py` → `derived/rekey_summary.csv`]

The white slice still costs other residents money on cash because it is old. 23.4% of it is 65 or over, against 7.7% of the union. Its Social Security and Medicare draws exceed its payroll taxes and premiums by **$170.5bn**; the union has a $44.4bn surplus on the same lines. [CALCULATION]

Three results change the delta:

- **Accrual.** Social Security and Part A on accrual, with payable benefits, move the delta to **+$318bn / +$315bn**. [CALCULATION: `accrual_white.py`]
- **The union's age structure.** Charging white per-age rates at the union's ages gives +$330bn / +$326bn on cash. [CALCULATION]
- **Two case conventions.** Both of them hold down how much whites pay. The CPS top tail of income tax, $393bn federal, is charged to nobody, and capital-side taxes do not respond when people leave. With both arms the delta is +$289bn / +$287bn on cash and **+$450bn / +$447bn on accrual**. [CALCULATION]

Scale is worth the same for either population: +$38.6bn for the union against +$37.4bn for the white slice. The schooling externality favours whites by **+$31bn**, and the joint central by **+$29bn**, with a 95% interval of −$54bn to +$113bn. The 1970–2000 college-share literature gives +$220bn to +$868bn, and Ciccone–Peri gives −$32bn to +$49bn. [CALCULATION: `spillovers_white.py`]

Violent-crime victims outside the group cost **$10–12bn** less like for like. [CALCULATION: `victim_cost_white.py`]

Every cost channel meets the same scaling exponent whichever population is added. The delta comes from per-head differences in taxes paid and programmes drawn, not from sub- or superlinear scale.

This is an accounting comparison of two populations under one set of rules. It is not a policy scenario. [FRAMING-SENSITIVE]

Lane `infra/immigration-fiscal/white_replacement_2026_09_28/`, written 2026-09-28, 22:12–22:46 JST (times from `date`). Brief: [`BRIEF.md`](BRIEF.md). All figures are in 2024 dollars a year. The low end is spec 48 and the high end spec 11, as in the Black lane.

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
```

Every script was run twice. All 16 files in `derived/` were byte-identical across the two full runs (sha256), and every gate passed on both. Nothing was written to other lanes, and nothing was committed.
