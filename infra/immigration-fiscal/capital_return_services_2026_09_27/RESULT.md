**Verdict:** Charged in full, with no netting of charges, the return on public capital gives two readings. The operator
chooses between them.

- **Option D, all enterprises respond: $317.74–383.44bn.**
- **Option A, enterprises out: $300.10–359.84bn.**

Both stack on the same base: the schools case ($258.49–291.95bn) plus the sister lane's long-run road and park
responses. Both keep the case's end specifications, 48 low and 11 high, in both fill-in methods. Rental assistance at
response 1, the build's other addition (+$4.53bn at both ends), is not in these rows. [DATA:
`main_case_long_run_2026_09_27/RESULT.md`, step 2, uncommitted]

| At specification 48 (2%, low responses) / 11 (3%, high responses), $bn | Option D | Option A |
|---|---:|---:|
| Schools case | 258.49 / 291.95 | 258.49 / 291.95 |
| Long-run road and park responses | +19.44 / +29.63 | +19.44 / +29.63 |
| Core return (schools, colleges, offices, safety, health) | +15.99 / +25.78 | +15.99 / +25.78 |
| Roads and parks block | +6.18 / +12.47 | +6.18 / +12.47 |
| Enterprise surplus line at response 1 | +5.71 / +5.71 | — |
| Return on all government-enterprise capital | +11.93 / +17.89 | — |
| **Band** | **317.74 / 383.44** | **300.10 / 359.84** |

- **Fee-financed enterprises do not earn a 2% return.** Their 2024 current surplus covers a 2% return on BEA's stock
  0.29 times for water and sewerage, 0.91 for gas and electricity, 0.88 for toll facilities and 0.06 for air and water
  terminals. Under D each therefore adds a net cost, and so do public housing and transit, whose surpluses are deficits.
  Only lotteries and liquor stores come out ahead (section 8).
- **No interest is counted twice.** NIPA's current surplus of government enterprises is before interest. BEA's
  methodology paper on government transactions (MP-5, 2005, p. I-13) says: "In calculating the current surplus,
  expenses include consumption of fixed capital (CFC), but neither revenue nor expenses include interest." Enterprises'
  "interest payments and receipts are presented with those of general government rather than those of business"
  (p. I-16). They therefore sit in the account's interest row, which is held at 0.
- **Netting is rejected, not a variant.** The account's lines are consumption, gross output less sales, so every charge
  is already credited once. Netting the return by the charge share would credit it a second time. It would remove
  $1.38bn / $2.12bn from the core and $0.50bn / $0.89bn from the block at the case's ends.
- **One key question for D.** The enterprise-surplus receipt keeps model.json's resident-population share, 0.1202. The
  case's corrections re-key the 15 population-keyed spending lines to 0.1172 but leave this receipt alone. At 0.1172,
  D is $317.29–382.84bn.
- **For the build.** `derived/engine_components.json` carries 24 components (8 core, 5 block, 11 enterprise), an
  `enterprises` switch with `allowed: ["D", "A"]` and no default, and 12 definition variants as rules.
  - *What the build must add.* Its `validate()` must accept part `enterprise`, key kind `receipt_amount_over_national`
    and response kind `enterprises_switch`.
  - *Land rows.* Its land regex must also read `enterprise: ` rows.

[CALCULATION: `capital_return.py` → `derived/`; 54 gates pass; two runs are byte-identical over all 20 files; the
schools case's `main_case.cjs` prints "all gates passed"]

Lane run by claude-opus-5-5 on 2026-09-27 for parent session immigration-research-1c ([brief](BRIEF.md)). The numbers
sit beside the account and are not adopted. All amounts are 2024 dollars for income year 2024. [FRAMING-SENSITIVE]
Both rates are conventions, and so is charging a return on public capital at all. The operator's 15:21 rulings fix the
rates (2% at the low end, 3% at the high end, 7% reported only) and keep land a reported gap.

## Results

**The core.** This is the return on the capital behind the tax-financed lines the adopted case already lets respond,
$bn a year, at specifications 48 / 11 with both fill-in methods averaged:

| Line | Capital charged (national, 2024 average) | Key | Response | 2% | 3% | 7% (reported only) |
|---|---:|---|---|---:|---:|---:|
| Education: K-12 | 2,723.9 | account school key 0.1588 / 0.1633 | 1 | 8.65 / 8.89 | 12.98 / 13.34 | 30.28 / 31.13 |
| Education: colleges and libraries | 1,198.4 (of 1,283.6) | college line 0.1545 / 0.1588 | 1 | 3.70 / 3.81 | 5.55 / 5.71 | 12.96 / 13.32 |
| General government: offices, S&L | 1,292.9 | population 0.1172 | 0.6000 / 0.8504 | 1.82 / 2.58 | 2.73 / 3.87 | 6.36 / 9.02 |
| General government: offices, federal nondefense | 152.2 | population 0.1172 | 0.6000 / 0.8504 | 0.21 / 0.30 | 0.32 / 0.45 | 0.75 / 1.06 |
| Public order and safety, S&L | 289.5 | use 0.1342 | 1 | 0.78 | 1.17 | 2.72 |
| Public order and safety, federal nondefense | 110.2 | use 0.1342 | 1 | 0.30 | 0.44 | 1.03 |
| Health, S&L | 366.0 | health_other 0.0566 | 1 | 0.41 | 0.62 | 1.45 |
| Health, federal nondefense | 106.0 | health_other 0.0566 | 1 | 0.12 | 0.18 | 0.42 |
| **Total (core)** | 6,239.1 | | | **15.99 / 17.19** | **23.99 / 25.78** | **55.98 / 60.15** |

[DATA: `derived/components.csv`, `derived/summary.json` → `by_component_at_case_ends_bn`, `by_line_at_case_ends_bn`]

Across the 64 specifications, three things move the core:
- the K-12 key;
- the college key;
- the general-government response.

The school fraction cancels out of both keys, and the normalization and uninsured-care keys do not enter. The return is
therefore smallest at specification 48 and largest at specification 11, the case's own ends. On every line, the return
at 2% is 0.86 (K-12) to 1.14 (federal offices) times the depreciation of the same stock. [CALCULATION]

| Case, $bn a year | Low end | High end | End specs |
|---|---:|---:|---|
| Adopted main case (schools) | 258.49 | 291.95 | 48 / 11 |
| Schools case + core return (2% at the low end, 3% at the high end) | 274.48 | 317.73 | 48 / 11 |
| Same, at 2% | 274.48 | 309.14 | 48 / 11 |
| Same, at 3% | 282.48 | 317.73 | 48 / 11 |
| Same, at 7% (reported only) | 314.47 | 352.11 | 48 / 11 |
| + long-run responses + block: option A | 300.10 | 359.84 | 48 / 11 |
| + long-run responses + block + enterprises: option D | 317.74 | 383.44 | 48 / 11 |

[DATA: `derived/bands.csv`, `derived/combined_bands.csv`]

**The roads and parks block** is priced at the sister lane's long-run responses. It adds $6.18bn at the low end (2%,
low responses) and $12.47bn at the high end (3%, high responses). State and local nontoll highways are $5.23bn and
$10.61bn of that (section 7).

**The enterprise block, option D.** It covers every government enterprise's capital. The total is BEA's government
enterprise fixed assets, $4,960.4bn. Every piece takes the enterprise-surplus receipt's key (0.1202) at response 1.
Returns, $bn:

| Enterprise (BEA source) | Stock, $bn | 2%, spec 48 | 3%, spec 11 |
|---|---:|---:|---:|
| Sewer systems (FAAt701 l68) | 1,224.9 | 2.95 | 4.42 |
| Water systems (l69) | 915.9 | 2.20 | 3.30 |
| Airports (l65 × VIP air share 0.498) | 595.8 | 1.43 | 2.15 |
| S&L electric and gas utilities (l66) | 542.1 | 1.30 | 1.96 |
| Public transit (l65 × VIP land share 0.423) | 505.8 | 1.22 | 1.82 |
| Toll facilities (l67 × toll share 0.1025) | 501.2 | 1.21 | 1.81 |
| Public housing (S&L residential, l58) | 420.4 | 1.01 | 1.52 |
| Ports (l65 × VIP water share 0.079) | 94.4 | 0.23 | 0.34 |
| Other S&L enterprise capital (remainder) | 75.5 | 0.18 | 0.27 |
| Other federal enterprise capital (remainder; Postal Service) | 56.7 | 0.14 | 0.20 |
| Federal power: TVA and the power marketing administrations (l48) | 27.7 | 0.07 | 0.10 |
| **Total (FAAt701 l79)** | **4,960.4** | **11.93** | **17.89** |

[DATA: `derived/enterprise_components.csv`; at 7% the total is $41.75bn at both ends, reported only]

The surplus line's move is +$5.71bn at both ends: the group's share, 0.1202, of NIPA 3.8's total of −$47.46bn, which
is a deficit. Section 8 splits it by enterprise.

## 1. Inventory

`derived/lines.csv` lists every spending line of the engine, with its response and key in the main case.
- *Where the lines come from.* They are the model's own (`assumption_explorer_2026_09_21/engine.js`) plus the case's
  three correction lines.
- *Where the responses and keys come from.* The evaluation that the package's `cost()` makes at each specification
  (`spec_lines.cjs`). That script also returns the enterprise-surplus receipt.

| Line (national $bn) | Response | Key | Capital treatment |
|---|---|---|---|
| Education (1,221.2) | schools 1, colleges 1 | education_mix + corrections | core: K-12, and colleges and libraries |
| General public services (401.6) | 0.6000 / 0.8504 | population | core: offices |
| Public order and safety (519.2) | 1 | use | core: public safety structures |
| Health (306.5) | 1 | health_other | core: health care structures, in full |
| Income security (167.8) | 1 | cash_assistance | none identified: no BEA type; its offices sit in Office, charged under general government |
| Housing and community services (14.5) | 1 | population | sanitation only; its structures are a gap |
| Housing subsidies, rental assistance (60.3) | 0 in the schools case, 1 in the build | housing_support | none: public housing's capital is in the enterprise block (option D) |
| Economic affairs (451.9) | 0, held fixed; long-run responses in the block | resources | block: nontoll highways and federal air and highway structures |
| Recreation and culture (54.3) | 0, held fixed; long-run responses in the block | population | block: parks, museums and zoos, and national parks |
| Enterprise-surplus receipt (−47.46) | 0; option D sets it to 1 | resident_population | enterprise block (option D) |
| Defense (854.8) | 0 | population | none |
| Domestic interest (1,118.9) | 0 | population | none (double-count gate) |
| Other subsidies (34.0) | 0 | wages, resources | none |
| 24 household transfer lines | 1 | various | none: transfers use no public capital; administration capital sits in the function lines |
| Foreign lines, rounding | 0 | external | outside the resident account |
| Lane constants (care, shelter, audit rows) | 1 | constant | none: no BEA asset type |

[DATA: `derived/lines.csv`; gates `line_keys_and_responses_are_the_main_cases`,
`response_zero_and_fixed_lines_stay_at_zero`]

`derived/asset_types.csv` accounts for every BEA government asset type (all levels, $20,931bn on the 2024 average),
with its treatment. The types add to BEA's total to within $0.8bn (gate).

## 2. Capital per line

**Which structure type serves which line is BEA's own mapping.** NIPA 3.17 gives gross investment by function.
For every function, that investment covers the structure-type investment mapped to it (FAAt705). The residual across
all functions equals:
- equipment plus software for state and local governments (1.000 in 2019, 0.962 in 2024);
- equipment plus software plus R&D for federal nondefense (0.999, 1.011).

[CALCULATION: `derived/mapping_check.csv`]

**Offices go to general government, as NIPA files them.**
- **NIPA's own filing.** The general-government "Other" row holds "unallocable state and local government consumption
  expenditures and gross investment" (NIPA 3.15.5 note 3). Its investment is 3.15.5 line 82 less 3.16 line 85.
  - It equals 0.83–0.99 of BEA's S&L Office investment in every year 2005–2024 (0.991 in 2024).
  - NIPA therefore files office-type capital under general government, and presumably its depreciation too.
    [CALCULATION; INFERENCE for the depreciation]
- **What the type holds.** Census's Office category "also includes city halls, borough halls, municipal buildings,
  courthouses, and state capitol buildings" [SOURCE: `_cache/census_c30_definitions.html`].
- **BEA's Office is broader than Census's.**
  - BEA's S&L Office investment is 2.7–4.3 times Census VIP's Office construction (1993–2024).
  - BEA's Public safety tracks VIP's correctional construction (0.83–1.14) rather than all of VIP's public safety.
  - BEA's Office therefore likely also holds buildings that Census puts elsewhere, fire stations among them.
    [DATA: `derived/bea_vs_census_types.csv`; INFERENCE]
- **Consequence.** The central estimate charges all offices at general government's key and response. Variants bound
  the alternatives (section 4).

**Housing and community services.** State and local consumption on this line "Consists of current expenditures for
sanitation" (NIPA 3.16 note 8, $11.8bn). Water, sewer and public housing are enterprises and produce no state and local
consumption, so their capital sits in the enterprise block (section 8). Sanitation structures sit inside BEA's Sewer
systems type, and they are a gap. [SOURCE; gate `sl_housing_consumption_is_sanitation_only`]

**Education.**
- **K-12.** The school lane's script, rerun on its own cached primary files into a scratch directory, gives K-12
  capital of $2,723.9bn. That is educational structures × 0.6748 plus K-12 equipment and software.
- **K-12's key is the account's own.** It is the education line plus `school_reprice`, over the national education line,
  as the case's evaluation gives them.
  - *Why the school fraction drops out.* Both amounts carry the school fraction, which cancels. The key is thus the school
    part plus `school_reprice` over the K-12 national amount.
  - *Its value.* It is 0.1588 at specification 48 and 0.1633 at 11, the same in both methods.
  - *The school lane's key.* That lane used the pupil share, 0.1748, a constant. It is now a variant.
- **K-12 reproduces the school lane.** At the pupil share, this lane reproduces the school lane's return to 1e-9 at
  every specification: $9.52bn at 2%, $14.28bn at 3% and $33.33bn at 7%.
  - *The rerun's files match.* Every CSV that the rerun writes is byte-identical to the committed one.
  - *One difference.* `summary.json` differs only in the recorded hash of `debt_legacy_2026_09_23/RESULT.md`, which a
    peer edited after that lane ran. [CALCULATION; gate `k12_reproduces_the_school_lane`]

  | K-12 return, $bn, specs 48 / 11 | 2% | 3% | 7% |
  |---|---:|---:|---:|
  | Account key (central) | 8.65 / 8.89 | 12.98 / 13.34 | 30.28 / 31.13 |
  | Pupil share (variant; the school lane) | 9.52 | 14.28 | 33.33 |

  [DATA: `derived/engine_components.json` → `k12_keys_at_case_ends`]
- **Colleges and other education.** The non-K-12 part, (1 − 0.6748) × $3,947.6bn = $1,283.6bn, is split by the
  post-1993 VIP vintages, weighted by the school lane's perpetual inventory [CALCULATION]:
  - higher education 0.870, charged in full;
  - libraries 0.064, charged in full;
  - museums, zoos and galleries 0.033, which belong to recreation and are priced in the block (section 7). VIP's
    "other educational" "also includes zoos, arboreta, botanical gardens, planetariums and observatories" [SOURCE];
  - preschool and unlisted 0.034, not charged (a gap).

  Colleges and libraries are thus 0.934 of the non-K-12 part, $1,198.4bn. Pre-1993 vintages take the post-1993
  composition. [INFERENCE]
- **The college key and response** are the account's own.
  - *Key.* It is (education_mix + college re-key) / the national education line: 0.1545 under shared allocation and
    0.1588 under personal. The response is the college response, 1.
  - *No dollar is charged twice.* The K-12 and college shares of capital come from VIP rather than the account's
    consumption split, so each dollar of educational structures is charged once.

**Health.** State and local and federal nondefense health care structures are charged in full. The account's S&L health
line ($126.8bn) is already net of $364.5bn of hospital and other sales (NIPA 3.17 lines 26–27). The line thus credits
those charges once, and the return on the capital sits outside it. [DATA; INFERENCE]

**Public order and safety.** The charge covers state and local plus federal nondefense Public safety structures:
prisons, jails, police stations, federal prisons and law-enforcement facilities. It is at the use key and response 1.
Courthouses are Office.

**Equipment and intellectual property.**
- **BEA publishes no function split** of equipment, software or R&D stocks. K-12's equipment is keyed by F-33 and is
  part of the reproduced figure; the rest are gaps.
- **A derived split.** NIPA 3.17 function investment less the mapped structures gives shares of equipment-plus-software
  investment. This is the school lane's own method for education's 22.7% (means of 2019 and 2024):
  - state and local: public order and safety 0.113, health 0.226, general government 0.053, income security 0.034,
    colleges 0.078;
  - federal nondefense: public order and safety 0.168, general government 0.195, income security 0.055.
- **Size.** On that split, equipment and software would add $0.65bn / $0.69bn at 2% (a variant).
- **Federal health's investment** ($108.3bn in 2024) is mostly R&D and cannot be separated. [CALCULATION]
- **Enterprises' equipment.** Transit vehicles and other enterprise equipment ($149.5bn) are inside BEA's enterprise
  total, so option D charges them.

## 3. Rates [FRAMING-SENSITIVE]

The rates are the school lane's, and its gates check each sentence in the primary texts
(`school_capital_return_2026_09_26/_cache`):
- **2%:** OMB A-4 (2023): the 30-year average real 10-year Treasury yield plus a 0.3-point PCE adjustment
  (pp. 76–77). Treasury's real yields in 2024 were 1.94–2.15% (10- to 30-year).
- **3%:** A-4 (2003), in force again since M-25-15 revoked the 2023 circular on 12 February 2025.
- **7%:** A-4 (2003)'s "average before-tax rate of return to private capital", reported only.

The real rate applies to the current-cost net stock, averaged over the year-end stocks of 2023 and 2024. This is the
standard user-cost pairing: it leaves out holding gains.

## 4. Variants

Every variant is exported as a rule in `engine_components.json` (section 10), so the build can rerun it at every
specification. Netting is not among them (section 8), and the enterprises switch is a top-level choice, not a variant.

**Core variants.** Change in the core return, $bn, at specifications 48 / 11:

| Variant | 2% | 3% | Band of the schools case + core, at 2% | at 3% |
|---|---:|---:|---:|---:|
| Central | 15.99 / 17.19 | 23.99 / 25.78 | 274.48–309.14 | 282.48–317.73 |
| + equipment and software, derived split | +0.65 / +0.69 | +0.97 / +1.04 | 275.13–309.83 | 283.45–318.77 |
| S&L offices at general government + audit row 8's increment (0.1139) | +0.35 / +0.35 | +0.52 / +0.52 | 274.83–309.49 | 283.00–318.25 |
| All offices at response 1 (upper bound) | +1.35 / +0.51 | +2.03 / +0.76 | 275.84–309.65 | 284.51–318.49 |
| End-2024 stocks | +0.29 / +0.31 | +0.43 / +0.47 | 274.77–309.45 | 282.91–318.20 |
| Higher-education dormitories, parking and unions (0.211 of its construction) fee-financed | −0.73 / −0.75 | −1.09 / −1.12 | 273.76–308.39 | 281.39–316.61 |
| K-12 at the pupil share (0.1748) | +0.87 / +0.63 | +1.31 / +0.94 | 275.35–309.77 | 283.79–318.68 |
| Colleges as (1 − school fraction) of educational structures | −0.46 / −2.23 | −0.69 / −3.34 | 273.10–307.85 (ends 56 / 3) | 280.02–316.21 (ends 56 / 3) |

[DATA: `derived/bands.csv`. Only the colleges-by-fraction variant moves the end specifications, to 56 and 3 in both
methods; every other variant keeps 48 / 11]

- **Audit row 8.** The case gives unallocable S&L spending a higher response through audit row 8.
  - *What the row does.* It charges "spending of every kind" at the all-spending elasticity 0.962 rather than the
    administration elasticity 0.842 (`dataset_integrity_2026_09_23/spending.md` #7).
  - *Why it bears on offices.* NIPA's investment filing suggests reading S&L offices as unallocable spending. On that
    reading, the consistent response is general government's plus 0.1139.
  - *Status.* It is arguably the more consistent reading. The central estimate keeps the brief's response. [INFERENCE]
- **Colleges by the school fraction.** This follows one reading of "in proportion to the account's college line": it
  scales college capital by the account's consumption split. It then no longer adds up with the K-12 capital, which comes
  from VIP, so the central estimate does not use it.
- **Auxiliaries fee-financed.** This variant takes dormitories, parking and student unions out. It is a partial netting:
  their room and parking charges are already sales that the college line subtracts. It therefore credits those charges
  twice, like the netting that section 8 rejects. It is kept because the parent listed it, and it serves as a lower
  bound. [INFERENCE]

**Block variants.** Change in the block, $bn, at 48 / 11. It is the same under both options:

| Variant | Change |
|---|---:|
| Toll share at its lowest year (7.16%) | +0.18 / +0.37 |
| Toll share at its highest year (17.27%) | −0.41 / −0.83 |
| Equipment and software added (derived split) | +0.03 / +0.12 |

Under option D the enterprise block keeps BEA's enterprise total whatever the toll share. The toll-share variants
therefore move only the nontoll highways in the block.

**Enterprise variants (option D).** Change in the enterprise returns, $bn, at 48 / 11:

| Variant | Change | Option D band |
|---|---:|---:|
| Public housing at the rental-assistance key (`housing_subsidies`' `housing_support` as the case evaluates it: 0.0740 / 0.0764 by method) | −0.38 / −0.57 | 317.36–382.87 |
| Public housing at model.json's rental key (0.1252), before the case's corrections re-key the line | +0.04 / +0.06 | 317.78–383.50 |
| All enterprise pieces, the receipt included, at the spending lines' population key (0.1172) | −0.45 / −0.60 | 317.29–382.84 |

The last row is a sensitivity row in `derived/combined_bands.csv`, not a variant in the recipe. The variant grammar
overrides components, not the receipt (section 8).

**Transit-share variants were dropped.** The parent asked for transit's share at its high bound and from Census
construction. Under D, transit, airports and ports take one key and one response, so the mode split only moves stock
between them: the total is unchanged. Under A all of line 65 is out. Both variants are therefore zero under either
option.

## 5. Double counts

- **Interest.** The account's interest row responds at 0 at every specification (engine `interest_response`).
  Enterprises' interest sits in that row (MP-5, section 8), so the full return on enterprise capital counts no interest
  twice. If a scenario charged the row, the debt-financed slice of the return would come off; the school lane put
  K-12's at $2.78bn at response 1. [DATA; gates `interest_row_held_at_zero`, `enterprise_surplus_is_before_interest`]
- **debt_legacy is federal only.** It keeps "the lead's no-legacy framing for state-local gaps", and "State-local
  interest ($274.6bn) sits in the account's interest row". [SOURCE; gated]
- **The production term** pays capital its rental rate: "The model pays the opportunity cost of capital"
  (`research/immigration-matched-benefits-2026-09-19.md`, dims `capital_adjustment`, `labor_share`). Public capital is
  not a factor in that CES term. [INFERENCE; gated text]
- **New seats** at today's construction cost stay unpriced (`decisions/2026-09-26-main-case-schools-full-cost.md`). If
  they are ever priced as a user cost of new capacity, they contain this return, and only one should count.
- **Enterprise surplus (option D).** The surplus is after depreciation and before interest, and it carries no return on
  capital (section 8). Moving it with the group and charging the return on the same capital therefore adds two different
  things.
- **Subsidies received (option D).** The surplus includes "subsidies received from other levels of government" (MP-5).
  Among them are "federal subsidies to state and local public housing authorities" (NIPA Handbook ch. 2, p. 2-10).
  - *Where they sit.* Those payments are also spending on the `housing_subsidies` line, which the build sets to
    response 1.
  - *How they net.* Under D the two offset, apart from their different keys: housing_support against the receipt's
    resident-population key. Under A the receipt is at 0 and the line adds its amount once, as the build's overlap check
    found.
- **Fees.** Nothing is netted. The account's lines already credit every charge (section 8).
- **The core, the block and the enterprise block share no asset.**
  - *Highways.* Nontoll highways are in the block and toll facilities in the enterprise block.
  - *The enterprise types.* Transit, airports, ports, power, water, sewer, public housing and federal power sit in the
    enterprise block only.
  - *The enterprise total.* It is BEA's, so the listed types' excess over enterprise structures is absorbed by the
    remainder, not charged twice.
  - *Offices.* Economic administration's offices are charged once, in the core. [DATA: `derived/asset_types.csv`]

## 6. Exclusions and gaps

**Excluded, with the reason** (`derived/asset_types.csv`):

| Excluded | Stock, $bn | Reason |
|---|---:|---|
| Defense, all assets | 2,299 | response 0 |
| S&L and federal conservation and development | 216 / 394 | natural resources and water held at 0 in the long-run responses |
| Government enterprises, all types (option A only) | 4,960 | option A holds enterprises out |

**Gaps.** Each figure is the group's return, $bn, if the item were charged at its line's key and response, at
specifications 48 / 11. The block's figures use the low responses at 48 and the high responses at 11
[DATA: `derived/gaps.csv`, which has one land row per component (gate `gaps_has_one_land_row_per_component`)]:

| Gap | 2% | 3% |
|---|---:|---:|
| **Land**, core, each 10% of land-to-structure value (K-12 0.85, colleges 0.37, offices 0.20, safety 0.11, health 0.05 at 2%, spec 48) | **1.58 / 1.70** | **2.37 / 2.55** |
| **Land**, block, each 10% (nontoll highways 0.52 / 0.71 at 2%) | **0.62 / 0.83** | **0.93 / 1.25** |
| **Land**, enterprises, each 10% (option D; the remainder holds no structures on net) | **1.16 / 1.16** | **1.74 / 1.74** |
| R&D, federal nondefense, health's share (0.18–0.79 of it; mostly NIH) | 0.19–0.86 | 0.29–1.29 |
| R&D, state and local (university research, inside NIPA's education investment) | 0.45 / 0.46 | 0.67 / 0.69 |
| Equipment and software beyond K-12 (derived split; the variant) | 0.65 / 0.69 | 0.97 / 1.04 |
| Equipment and software of the block's components (derived split; the variant) | 0.03 / 0.08 | 0.05 / 0.12 |
| Sanitation structures inside Sewer systems (upper bound, 10.6% of that type's investment) | 0.30 | 0.46 |
| Federal nondefense educational structures (no K-12/other split) | 0.19 / 0.20 | 0.29 / 0.29 |
| Preschool and unlisted educational structures | 0.13 / 0.14 | 0.20 / 0.21 |
| Commercial and other structures, S&L and federal (no function; their parking, liquor-store and Postal Service parts are in the enterprise total) | 0.27 / 0.38 | 0.40 / 0.56 |

Further gaps:
- **Land [GAP].** See section 9 for the sources checked.
- **R&D [GAP].** It is non-rival, so a removal need not shrink it. Its depreciation nevertheless sits in the health and
  education lines that the account charges at response 1. [INFERENCE]
- **Capital per pupil or user where the group lives [GAP].** It is not measured; national average capital per unit of
  key applies.

## 7. Roads and parks: the block

**Why a separate block.** The adopted case holds economic affairs and recreation at 0, under CBO's category lag. The
sister lane lets them respond (committed bccf478). The block prices the return on the capital behind those lines, at
the sister lane's responses, read from its `derived/responses.json`. The build (`main_case_long_run_2026_09_27`)
combines those responses with this return.

**How it reads the responses.**
- **Keys.** The block uses the keys the account already gives the two lines. Economic affairs takes the resources key,
  8.06% at both end specifications. Recreation takes the population key, 11.72%.
- **Which response where.** Each component takes its subfunction's response: the low reading at the low end
  (specification 48) and the high reading at the high end (11), as in the sister lane.
- **Reproduction.**
  - *Per-specification costs.* The sister lane's 128 per-specification costs are the case's cost plus the keyed amounts
    times the blended responses, to a maximum difference of 4.8e-10.
  - *Band.* Its band, $277.93–321.59bn with ends 48 and 11, also reproduces.
  - [gates `long_run_responses_are_the_sister_lanes`, `long_run_per_spec_costs_reproduce`,
    `long_run_candidate_band_reproduces`]

| Component (BEA line) | Response, low / high | Capital charged, $bn | 2%, spec 48 | 3%, spec 11 | 7%, 48 / 11 (reported only) |
|---|---|---:|---:|---:|---:|
| S&L highways and streets less toll facilities (l67 × 0.8975) | 0.7392 / 1 | 4,389.0 of 4,890.2 | 5.23 | 10.61 | 18.31 / 24.77 |
| S&L parks and recreation plus museums and zoos (l64; l62) | 0.9512 / 1 | 425.1 | 0.95 | 1.49 | 3.32 / 3.49 |
| Federal highways and streets (l49) | 0 / 1 | 54.6 | 0 | 0.13 | 0 / 0.31 |
| Federal transportation: air traffic facilities (l47) | 0 / 1 | 35.4 | 0 | 0.09 | 0 / 0.20 |
| Federal amusement and recreation: national parks (l46) | 0 / 1 | 41.8 | 0 | 0.15 | 0 / 0.34 |
| **Block total** | | 4,945.9 | **6.18** | **12.47** | 21.62 / 29.10 |

[DATA: `derived/block_components.csv`, which also carries each component's return per unit of response for
rescaling; `derived/per_spec_block.csv`]

**The highway line, checked.**
- **Size.** FAAt701 line 67 (S&L Highways and streets) is $4,890.2bn on the 2024 average. That is 31% of S&L
  structures and the largest government asset type. [DATA]
- **It is the highway function's capital.**
  - *Investment.* Its 2024 investment is 97.2% of the S&L highway function's gross investment, which is NIPA 3.15.5
    line 90 less the sister lane's consumption ($144.0bn); the rest is equipment.
  - *Census cross-check.* Census VIP highway-and-street construction tracks it at 0.89–1.07 over 1993–2024.
  - [CALCULATION; gate `highway_and_transport_types_are_their_functions_capital`]
- **Toll facilities go to the enterprise block.**
  - *Why they are in the stock.* BEA classifies "toll facilities" as state and local enterprises (BEA WP2022-8). NIPA
    consumption "Excludes gross output and sales of ... government enterprises", while gross investment "Includes
    investment by federal and by state and local government enterprises" (NIPA Handbook ch. 9). Toll roads' costs
    therefore sit outside the account's line, and their capital sits inside line 67. [SOURCE; gate
    `nipa_enterprises_and_their_capital`]
  - *How much.* The toll share is 10.25% of S&L highway construction in the Census individual-unit finance files,
    pooled over FY2012 and FY2017–2023 (7.2–17.3% by year). [CALCULATION; the parse reproduces 18 FY2022 Census API
    fields]
- **Charged in full.** Regular-highway charges cover 0.04 of production costs (2017, BEA WP2022-8 Table 5). They are
  already subtracted in the line, so the nontoll stock is charged in full.
- **Depreciation is already there.** The nontoll stock's depreciation sits inside the $201.0bn of S&L highway
  consumption that the sister lane lets respond. The return is the part still missing. [CALCULATION]
- **Land.** BEA excludes land, so right-of-way is outside the stock (section 9).

**Parks and recreation.**
- *State and local.* S&L Amusement and recreation (line 64, $383.2bn) plus the museums and zoos inside educational
  structures ($41.8bn), which the core leaves to recreation. Both are charged in full.
- *Federal.* Federal Amusement and recreation (line 46) is national parks.

**Federal lines.** Highways and streets (line 49) and Transportation (line 47) take the sister lane's responses: 0 at
the low end and 1 at the high end. Line 47 is assigned to air: federal air's gross investment ($4.5bn in 2024) is 3.6
times line 47's. Federal water transport is held at 0, and federal transit and rail consumes $0.1bn. [INFERENCE]

**Not in the block.**
- *Conservation and development* (S&L line 70, federal line 50). Natural resources and water stay at 0 in the long-run
  responses.
- *General economic and labor affairs* (S&L 0.8504 at both ends; federal 0 / 0.8504). Its capital is offices, already
  charged in the core under general government, so the block adds none. [INFERENCE]
- *Transit.* It is an enterprise and moves to the enterprise block (section 8).

**Congestion stays separate.** Once lanes shrink with highway spending, the response lane's congestion item beside
the account changes by −$5.17bn at the low end and −$7.14bn at the high end. That is a social item, so it is not in the
fiscal bands. [DATA: `service_response_long_run_2026_09_27/derived/net_change.json`; gate
`congestion_change_kept_beside_the_fiscal_case`]

**What the block assumes.**
- **The response carries over to capital.**
  - *Where the responses come from.* The sister lane measures them on nontoll highway and park current operations
    across states (Census codes E44 and E61, `scaling_test_2026_09_20/state_analyze.py`).
  - *How the block uses them.* It applies them to capital, as the account already applies them to the depreciation
    inside the line.
  - *What that presumes.* The network shrinks with spending: κ = 1 in the sister lane's congestion bridge, its central
    case. At κ = 0 the network and its capital would stay, and neither this return nor the depreciation in the line would
    be saved. [INFERENCE]
- **Key.** The resources key gives the group 8.06% of highways. The sister lane reports a traffic share of 10.8%, from
  the congestion lane. At that key the highway component would be about a third larger. [DATA: the sister lane's
  RESULT.md, not re-derived here]

## 8. Enterprises: options D and A

**The two options** (the parent's, 2026-09-27; the operator picks):
- **D, all enterprises respond.**
  - *The receipt.* The `enterprise_surplus` receipt responds at 1 at its own key.
  - *The capital.* The full return on all government-enterprise capital, S&L and federal, of every type, at that key
    and response 1.
  - *What moves.* Transit and public housing leave the block and the core for this block, so each asset is charged once.
- **A, enterprises out.** No enterprise capital, and the receipt stays at 0, as in the adopted case.

**What replaced the earlier rule.** The earlier rule charged an enterprise net of its charge share when charges fell
short of production costs, and excluded it otherwise. It had two faults:
- *Netting credited the charges twice* (below).
- *The zero response did not match.* It charged transit's and public housing's capital while their operating deficits,
  five to seven times larger, stayed at response 0.

D is the symmetric reading: every enterprise's operating result and capital move together. A keeps both out.

**The premise holds: an enterprise's surplus is after its depreciation.** [SOURCE: the pinned NIPA Section 1 workbook,
the vintage debt_legacy pins; NIPA Handbook ch. 9]
- **NIPA 1.7.5 (2024).** Consumption of fixed capital, $4,796.7bn, includes government enterprises' $111.9bn. That is
  government's $803.8bn less general government's $691.9bn, which is NIPA 3.10.5 line 5. National income, net of all
  CFC, contains the enterprises' current surplus (−$47.46bn).
- **NIPA 1.10.** Net operating surplus is private enterprises plus the current surplus of government enterprises, and
  GDI adds consumption of fixed capital beside it.
- **NIPA Handbook ch. 9.** "The value added by government enterprises (as producers of goods and services for the
  marketplace) is recorded in the business sector". There "the difference between the value of output and the costs
  of production is equal to the net operating surplus".
- [gate `enterprise_surplus_is_after_their_depreciation`]

**And the surplus is before interest.** [SOURCE: BEA, *Government Transactions*, NIPA Methodology Paper 5, September
2005, https://www.bea.gov/sites/default/files/methodologies/mp5.pdf; NIPA Handbook ch. 2, December 2024,
https://www.bea.gov/resources/methodologies/nipa-handbook/pdf/chapter-02.pdf; each phrase gated in
`enterprise_surplus_is_before_interest`]
- MP-5, p. I-13: "In calculating the current surplus, expenses include consumption of fixed capital (CFC), but neither
  revenue nor expenses include interest."
- MP-5, p. I-16: "Interest received and paid are ignored in the calculation of the current surplus of government
  enterprises." Also: "(1) Their interest payments and receipts are presented with those of general government rather
  than those of business;"
- MP-5, p. II-30: "The current surplus of government enterprises is equal to current operating revenues and subsidies
  received from other levels of government less current operating expenses."
- Handbook ch. 2, p. 2-10: net operating surplus is measured "before deducting any explicit or implicit interest
  charges, rent, or other property incomes payable on financial assets, land, or other natural resources required to
  carry out production."

Enterprises' debt interest is therefore in the account's interest row, which is held at 0. The surplus carries no
return on capital, and D charges that return once. The last quote also puts the surplus before any rent on land. Under
D the surplus therefore credits what the enterprises earn on their land, while the charge leaves land out, so land's
omission understates D's net cost. [INFERENCE]

**Netting credits the charges twice** (rejected; listed here once). [INFERENCE from the NIPA definitions]
- **The charges are already credited.** The account's service lines are NIPA consumption, gross output less sales:
  NIPA 3.10.5 line 11 subtracts $695.8bn of sales, and S&L health is $126.8bn net of $491.4bn gross. An enterprise's
  surplus is likewise its sales less its costs. Every charge is therefore already credited once.
- **What is missing is the full return.** The NIPAs impute a zero net return, so the return sits outside both.
- **Netting credits them again.** It would multiply the return by the tax-financed share: tuition 0.689, S&L health
  0.258, regular highways 0.96 and parks 0.69.
- **What it would remove.** At 2%, spec 48 / 3%, spec 11: $1.38bn / $2.12bn from the core and $0.50bn / $0.89bn from
  the block. [DATA: `derived/summary.json` → `rejected_netting`]

**The account's receipt.** The enterprise-surplus receipt is NIPA 3.8's total, −$47.46bn. The group's share is
−$5.71bn at the resident-population key. It is an indirect receipt and responds at 0 in all 128 evaluations `cost()`
makes, since the engine takes `indirect_receipt_response` and the package sets no override. [DATA; gate
`enterprise_surplus_line_is_nipa_3_8_held_at_zero`] Under D it responds at 1. Losing a share of a deficit raises the
cost, by $5.71bn at both ends.

**Option D by NIPA 3.8 group.** The table sets each group's 2024 surplus against the return its capital would need
(national, $bn), then shows the group's pieces under D at 2%, spec 48 / 3%, spec 11:

| NIPA 3.8 group | Surplus 2024 | Stock | Return at 2% | at 3% | Surplus / return at 2% | Group's return | Group's surplus move | Net under D |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Water and sewerage | 12.49 | 2,140.8 | 42.82 | 64.23 | 0.29 | 5.15 / 7.72 | −1.50 | +3.65 / +6.22 |
| Gas and electricity | 9.86 | 542.1 | 10.84 | 16.26 | 0.91 | 1.30 / 1.96 | −1.19 | +0.12 / +0.77 |
| Toll facilities | 8.84 | 501.2 | 10.02 | 15.04 | 0.88 | 1.21 / 1.81 | −1.06 | +0.14 / +0.74 |
| Air and water terminals | 0.82 | 690.2 | 13.80 | 20.71 | 0.06 | 1.66 / 2.49 | −0.10 | +1.56 / +2.39 |
| Housing and urban renewal | −40.30 | 420.4 | 8.41 | 12.61 | — | 1.01 / 1.52 | +4.85 | +5.86 / +6.36 |
| Public transit | −66.69 | 505.8 | 10.12 | 15.17 | — | 1.22 / 1.82 | +8.02 | +9.24 / +9.84 |
| Liquor stores and other (lotteries, gaming, parking) | 29.35 | 75.5 | 1.51 | 2.26 | 19.4 | 0.18 / 0.27 | −3.53 | −3.35 / −3.26 |
| Federal (Postal Service, power) | −1.82 | 84.4 | 1.69 | 2.53 | — | 0.20 / 0.30 | +0.22 | +0.42 / +0.52 |
| **Total** | **−47.46** | **4,960.4** | **99.21** | **148.81** | | **11.93 / 17.89** | **+5.71** | **+17.64 / +23.60** |

[DATA: `derived/enterprise_surplus_vs_return.csv`; gate `enterprise_surplus_groups_cover_nipa_3_8_and_the_components`:
the groups add to NIPA 3.8 line 1, their moves to the receipt's, and their nets to D's pieces. Rows may not add
because of rounding.]

- **The fee-financed utilities fall short of a 2% return.**
  - *Charges against costs.* Their charges exceed production costs, meaning operating costs plus depreciation (BEA
    WP2022-8 Table 5, 2017): water 1.25, sewerage 1.33, tolls 2.66, air 1.54 and ports 1.41.
  - *Surplus against the return.* Their 2024 surplus is still below a 2% return on BEA's stock. Power and tolls come
    close (0.91 and 0.88), water and sewerage reach 0.29, and the terminals 0.06.
  - *Consequence.* Under D all four add a net cost: $5.47bn at the low end and $10.13bn at the high end.
- **The residual group comes out ahead.** It is the only group that does. MP-5 (p. III-22) lists the residual category
  as "state lotteries, gaming administered by Indian tribal governments, off-track betting, local parking, and
  miscellaneous commercial activities". Its surplus is a revenue source more than a return on capital, and the group's
  share of it, $3.53bn, leaves under D. [INFERENCE]
- **Public housing and transit carry most of D.** They cost +$15.09bn / +$16.21bn together, most of it their deficits.

**Enterprise capital, accounted.** [DATA: FAAt701 lines 79–82, 58, 65–69 and 48, label-checked; NIPA 7.5; gate
`enterprise_capital_is_beas_enterprise_total`]
- **BEA's total.** Government enterprise fixed assets are $4,960.4bn on the 2024 average: equipment $149.5bn,
  structures $4,791.7bn and intellectual property $19.2bn. BEA publishes them only as a total over levels and types.
- **Depreciation.** FA depreciation in 2024 is $112.62bn. NIPA 7.5's enterprise CFC is $111.904bn (federal $14.026bn,
  S&L $97.878bn), which equals NIPA 1.7.5 line 13.
- **The listed types.** They are the enterprises on BEA's list and add to $4,828.2bn, which exceeds BEA's enterprise
  structures by $36.5bn. Part of the listed stocks is presumably general government in BEA's accounting, sanitation
  inside Sewer systems among it. [INFERENCE]
- **The remainder.** It is $132.2bn: enterprise equipment, software and structures of other types, net of that excess.
  Its structures are negative on net, so it holds no land.
- **The remainder's split.** It is split between S&L ($75.5bn) and federal ($56.7bn) by the enterprise depreciation
  the listed types do not cover: $18.11bn and $13.61bn.
- **Why the split does not matter for the total.** Every piece takes the same key and response.

**The receipt's key.** D keys all enterprise capital by the receipt's key, as the parent asked: "population, as the
account keys it".
- *Its value.* That key is model.json's resident-population amount for the receipt scenario the case uses, 0.1202.
- *The other population key.* The case's corrections, through the CPS lane's stack, re-key the 15 population-keyed
  spending lines from model.json's 0.1215 to 0.1172, but not this receipt. In the adopted case the receipt is at 0, so
  the difference has not mattered. Under D it does.
- *Size.* At 0.1172, D's enterprise pieces fall 2.6%, to $317.29–382.84bn. [DATA: `derived/summary.json` →
  `enterprises.key_consistency`; gate `enterprise_receipt_is_model_jsons_resident_share`]
- *Open question.* Whether the stack's population correction should reach the population-keyed receipts
  (`enterprise_surplus`, `government_asset_income`) is a question for the CPS lane. This lane does not decide it.

## 9. Land: sources checked

No primary source gives the value of state and local government land, nationally or by function. Land therefore stays
a conversion per 10% of land-to-structure value [GAP].

| Source | What it gives | Why it does not close the gap |
|---|---|---|
| BEA, Larson (2015), WP2015-3 | Land of the lower 48 states, about $23tn in 2009, "with 24% of the land area and $1.8 trillion of the value held by the federal government" | Its only state and local government figure is Washington, DC (Table 2: $8.03bn on 2,578 acres, 2013); nothing national or by function |
| Federal Reserve, Z.1 table descriptions, F.107 | The state and local balance sheet in the Integrated Macroeconomic Accounts (S.8.a, S.8.q) | It includes "the value of structures, equipment, and software but not the value of land"; the federal sector's likewise |
| BEA, Wasshausen (2011) | How the IMAs build nonfinancial balance sheets | "the net stock of structures (excluding land) is used in lieu of real estate for the sectors with insufficient data on market value of real estate"; OMB's federal real-estate data are "for illustrative purposes" |

[SOURCE: `_cache/bea_larson_wp2015_3.pdf`, `_cache/frb_z1_table_descriptions.pdf`, `_cache/bea_wasshausen_p2011_1.pdf`,
each phrase gated in `land_sources_checked`]

Not checked:
- **FHWA's right-of-way outlays.** They are acquisition costs, not values, so they would give only a floor.
- **OMB's federal real property reports.** They are federal only.

Each 10% of land-to-structure value adds, at 2% for specification 48 and 3% for specification 11:

| Land per 10% of structures | $bn |
|---|---:|
| Nontoll highways | 0.52 / 1.06 |
| Whole block | 0.62 / 1.25 |
| Core | 1.58 / 2.55 |
| Enterprises (option D) | 1.16 / 1.74 |

## 10. The build's recipe: `derived/engine_components.json`

The main-case build (`main_case_long_run_2026_09_27`, brief 53efc3d) imports this file, so the capital definitions
live in this lane only.

- **Components (24).** Each has an id, a part (core, block or enterprise), a level (state_local or federal), its engine
  lines, its national stock and `stock_charged_bn`. The return is stock × rate × key × response.
  - *Core (8).* K-12, colleges and libraries, S&L and federal offices, safety and health.
  - *Block (5).* Nontoll highways, S&L parks and museums, and the three federal lines.
  - *Enterprise (11).* The types of section 8, with `engine_lines: []` and `receipt_lines: ["enterprise_surplus"]`.
- **Key rules.**
  - *Spending lines.* Every core and block key is the sum of named lines' `amount_bn` over one line's `national_bn` in
    the evaluation (`lines_amount_over_national`). A re-keyed evaluation, by generation say, therefore splits the return.
  - *K-12.* The education line plus `school_reprice`.
  - *Colleges.* The education line plus `college_rekey`.
  - *Enterprises.* They take `receipt_amount_over_national`: the `enterprise_surplus` receipt's `amount_bn` over its
    `national_bn`.
- **Response rules.**
  - *For core and block components:* the line's response, `school_reprice` or `college_rekey` over the school or
    college fraction, or the long-run subfunction value (low, high, across_high).
  - *For enterprises:* `enterprises_switch`, with `values: {D: 1, A: 0}`.
  - *No lane-only rules.* The file has no `lane_central_*` fields. K-12's central key is now the account's own, which
    the build already uses.
- **The switch.** `enterprises` sets `choice: "the operator's: D or A (no default)"` and `allowed: ["D", "A"]`. It also
  carries:
  - each option's component response and receipt responses (`enterprise_surplus`: 1 under D, 0 under A);
  - the receipt rule (the cost moves by −amount × response);
  - the capital note, the interest quotes and the subsidies note.
- **Variants (12)** in the build's grammar, `{name: {label, overrides: [{component, stock_charged_bn | key | response |
  drop}], adds: [components]}}`:
  - core: `equipment_and_software` (adds), `end_2024_stocks`, `sl_office_at_unallocable_response` (adds an
    increment at a fixed response), `offices_at_response_1`, `higher_ed_auxiliaries_fee_financed`,
    `college_by_account_school_fraction` and `k12_at_pupil_share`;
  - enterprise (act under D): `public_housing_at_rental_assistance_key` and `public_housing_at_uncorrected_rental_key`;
  - block: `block_toll_share_at_its_lowest_year`, `block_toll_share_at_its_highest_year` and
    `block_equipment_and_software_added`.

  Each carries `check_at_case_ends_bn`: this lane's core, block and option D enterprise returns at 2% and 3%.
- **Checks.** Values at the end specifications, both option bands, and the sha256 of all inputs.

**The recompute gates.** Both read the serialized file back.
- `engine_components_recompute_the_per_spec_outputs`: from the file and the spec_lines.cjs evaluation alone, it rebuilds
  every column of `per_spec.csv` and `per_spec_block.csv` (128 rows each, the enterprise columns included; max |diff| 0).
  Option A gives exactly 0 for the enterprise block and the receipt.
- `engine_components_variants_reproduce_this_lanes_variants`: all 12 variants, applied as the build applies them
  (overrides, then drops, then adds), reproduce this lane's variant outputs at every specification and reading (max
  |diff| 3.6e-15).

**What the build must add** (`main_case_long_run_2026_09_27/package.cjs`, the build's file, not edited here).
- *The switch already reads.* The build reads `enterprises.allowed`. With its option unset it stops with "[BLOCKED] the
  enterprise option (D or A) is not set in package.cjs", as designed.
- *Where it fails next.* I set `ENTERPRISES = "D"` in memory only, without writing any file. Its `validate()` then stops
  with "[BLOCKED] engine_components.json: unknown rule in component ent_housing_sl (the lane's definition)".
- *Its fixes:*
  - accept part `enterprise`;
  - accept key kind `receipt_amount_over_national`, read from `evaluation.receipts`, including in the evaluation-key
    check;
  - accept response kind `enterprises_switch`, taking `values[ENTERPRISES]`;
  - let its land regex read `enterprise: land at 10% ...` rows.
- *The receipt override exists.* The receipt's response override is already in place (`"receipt:enterprise_surplus"`,
  8d87481).

## Gates (54 pass; `derived/gates.json`)

- **The case.**
  - Per-specification costs from `cost()` reproduce $258.4885–291.9548bn, with ends 48 / 11 in both methods.
  - The published corrections.json gives the same cost at every specification to 1.7e-13.
  - The responses equal `meta.responses`, and the pupil share is the finite-response lane's.
  - Each line's key and response are the case's, and the lines held at zero stay there.
  - The evaluated rental-assistance amount is model.json's $7.54bn plus corrections.json's −$3.01bn edit.
  - The enterprise receipt is model.json's resident-population amount at every specification, with no edit.
- **Sources.**
  - The account's lines equal NIPA 3.17, and the FA types add to BEA's totals.
  - The mapping leaves no negative residual, and its residuals fit equipment and IP within 5%.
  - NIPA files S&L office investment under general government, and Census puts courthouses in Office.
  - S&L housing consumption is sanitation only.
- **Factors.** The higher-education and health figures pass their checks, and the VIP parse matches the school lane's.
- **K-12.** It reproduces the school lane: the return and the land conversion to 1e-9, and structures equal to the key
  × educational structures.
- **Coverage and bands.**
  - The asset types cover all government capital.
  - The core band is ordered, and its ends keep the case's specifications.
  - Every combined row keeps ends 48 / 11, and D lies above A at both ends.
- **Double counts.** The interest row stays at 0, debt_legacy is federal only, the production term pays private capital
  only, and new seats and land are unpriced.
- **Enterprises.**
  - The Section 1 workbook is the vintage debt_legacy pins. NIPA 1.7.5 and 1.10 add up and carry the expected labels.
  - The surplus is after depreciation (Handbook ch. 9) and before interest (MP-5 and Handbook ch. 2, with the chapter's
    December 2024 date).
  - The account's enterprise line is NIPA 3.8's total and responds at 0 in all 128 evaluations.
  - Enterprise capital is BEA's total, and NIPA 7.5's CFC matches NIPA 1.7.5.
  - The NIPA 3.8 groups cover the total and the components, and their moves and nets add to D's pieces.
- **Block: inputs.**
  - The sister lane's responses are well formed. They reproduce its blends, its per-specification costs and moves, its
    band and its across-state band.
  - Its congestion file carries the same account moves at the ends.
  - BEA's enterprise list and the Handbook's scope statements are present in the cached texts.
  - Table 5 parses (11 years):
    - toll, airport, port and parking charges are at or above 1 in every year;
    - sewerage and water charges are above 1 in 2017;
    - parks, regular highways, transit and housing charges are below 0.5 in 2017.
  - The Census parse reproduces 18 FY2022 API fields, and the toll share is bracketed by its years.
- **Block: capital.**
  - The highway, transport and recreation types are at most their functions' gross investment, and VIP tracks lines 65
    and 67 within 0.8–1.2.
  - The transport perpetual inventory reproduces BEA's stock within 10%.
  - The block's equipment residuals are shares.
  - The land-source phrases are present.
- **Recipe.**
  - `gaps.csv` has one land row per component.
  - engine_components.json and the evaluation alone rebuild both per-specification files.
  - The 12 variants reproduce this lane's.

## Files covered and skipped

Covered, all parsed by the script:
- **The school lane's cached primary files**, hash-checked by its `sources.csv`:
  - BEA Fixed Assets Section 7 (FAAt701, 703, 705, 706), with lines 1, 22, 38–74 and 79–82 label-checked;
  - Census VIP state and local, 1993–2025, including the Library/archive, Dormitory, Parking, Student union/cafeteria,
    Highway and Street, and Transportation (Air, Land, Water) rows;
  - its OMB texts, gated there.
- **Pinned NIPA Section 3** (`sources/immigration-fiscal/data/external/bea_nipa/Section3All_xls.xlsx`):
  - T3.8 lines 1–15;
  - T3.10.5 lines 5, 11, 46 and 57–60;
  - T3.15.5 lines 41, 54–57, 67, 78, 82, 89–93, 100–114 and note 3;
  - T3.16 lines 85, 101 and 106–111, with note 8;
  - T3.17 lines 2–31, 55 and 115–133.
- **Pinned NIPA Section 1** (`Section1All_xls.xlsx`, sha256 238ba851…, the vintage `debt_legacy_2026_09_23` pins):
  - T1.7.5 lines 4–6, 11–16 and 22;
  - T1.10 lines 1, 2, 7–10, 20 and 21.
- **NIPA Section 7** (`nipa_Section7All_xls.xlsx` in the school lane's cache): T7.5 lines 21, 22 and 25–27.
- **The sister lane's outputs**, read-only: `service_response_long_run_2026_09_27/derived/responses.json`,
  `per_spec_costs.csv`, `candidate_band.json` and `net_change.json`.
- **Census finance files:**
  - the individual-unit files, FY2012 and FY2017–2023 (`local_spending_composition_2026_09_18/_cache/indunit_*.zip`),
    checked against the pins in `administration_response_2026_09_20/inputs.sha256.json`;
  - the pinned FY2022 Census API file (`macro_closure_2026_09_19/_cache/finance_2022_us_combined.json`).
- **Fetched 2026-09-27 into `_cache/`** (hashes in `derived/summary.json`; each `.txt` is `pdftotext -layout` of its
  `.pdf`):
  - Census C30 definitions (https://www.census.gov/construction/c30/definitions.html);
  - BEA WP2022-8 (Highfill, https://www.bea.gov/sites/default/files/papers/BEA-WP2022-8.pdf);
  - NIPA Handbook ch. 9 (https://www.bea.gov/resources/methodologies/nipa-handbook/pdf/chapter-09.pdf);
  - NIPA Handbook ch. 2 (https://www.bea.gov/resources/methodologies/nipa-handbook/pdf/chapter-02.pdf);
  - BEA MP-5, *Government Transactions* (https://www.bea.gov/sites/default/files/methodologies/mp5.pdf);
  - BEA WP2015-3 (Larson), BEA's Wasshausen (2011) paper, and the Fed's Z.1 table descriptions.
- **Repo files, read-only** (hashes in `summary.json` and `engine_components.json`):
  - `main_case_schools_full_2026_09_26`: `package.cjs` through `spec_lines.cjs`, plus `derived/corrections.json` (its
    housing and population edits parsed), `summary.json` and `main_case_bands.csv`;
  - the September 24 and 26 packages; `finite_response_2026_09_26/derived/r_values.json`;
  - engine.js (how it charges a key: `target_bn`) and model.json (the `housing_subsidies` keys and the
    `enterprise_surplus` receipt);
  - `debt_legacy_2026_09_23/RESULT.md` and `debt_legacy.py` (its Section 1 pin), the matched-benefits memo and the
    schools decision;
  - `dataset_integrity_2026_09_23/spending.md` (rows 6 and 8, read, not parsed);
  - `scaling_test_2026_09_20/state_analyze.py` (which Census codes the responses measure; read, not run).
- **Read by hand, not parsed:**
  - `main_case_2026_09_24/derived/stack_line_deltas.json`, to trace the population re-key to the CPS lane's stack;
  - `main_case_long_run_2026_09_27/BRIEF.md`, `RESULT.md` and `package.cjs` (what the build expects; probed in memory).

Skipped:
- **BEA's detailed government fixed-asset files.** None are public by function. The school lane found the detailed
  files cover private assets only.
- **Census of Governments capital outlay as a stock split.** It is a flow, and it includes land and equipment. It is
  used only for the toll share and a transit cross-check. NIPA's function investment serves the core mapping.
- **Land data.** See section 9.
- **Which correction makes the −$3.01bn rental edit.** corrections.json carries the combined edit; this lane does not
  trace it to a correction lane.

## Reproduce and validation

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/capital_return_services_2026_09_27/capital_return.py
node infra/immigration-fiscal/main_case_schools_full_2026_09_26/main_case.cjs | tail -1
```

- **Wall time.** The final run took 2.2 s. That covers the school lane's rerun, `node spec_lines.cjs`, the BEA parse
  and the eight Census files.
- **Reruns.** Two consecutive runs leave all 20 files in `derived/` byte-identical.
- **`main_case.cjs`.** The schools case's gate script prints "all gates passed", and `git status` on its directory is
  empty.
- **Side effects.** Outside this directory, `git status` shows only peers' lanes. Importing the school lane sets
  `sys.dont_write_bytecode`, so no `__pycache__` is left in either directory. Nothing is committed.

## Run log

Times are JST. The entries through 16:15 are the ones written then; the parent's message times there are approximate.

- 13:32 Stub written.
- 13:55 Design checkpoint: keys, the mapping and the fee factors probed.
- 13:58 First full run: 28 gates.
- 14:05 Added four pieces (30 gates); the parent committed the result as 172226c:
  - the brief's combined band;
  - the asset-type accounting;
  - the BEA-versus-Census table;
  - the college-by-fraction variant and the conditional economic-affairs and recreation conversions.
- 14:15 The parent extended the scope to a roads, transit and parks block and to a primary source for land.
- 14:38 Added the block, the enterprise and fee sources, the Census toll share, the VIP transport split, the land
  sources and the combined band (42 gates). The per-unit-response conversions of the earlier section 6 were replaced by
  the block.
- 14:50 The parent's follow-up added three checks (44 gates):
  - the across-state band, checked against the response lane's;
  - the response lane's per-specification moves, checked directly;
  - the congestion change, kept beside the fiscal case.
- About 15:00 The parent made two definition calls: transit out of the block, public housing into the core. I objected
  that both are enterprises with charges below costs, and computed readings A and B beside them.
- About 15:10 The parent's correction set one rule for every enterprise. Transit is back in, public housing is in, and
  the net-of-depreciation premise was to be verified.
- 15:29 Done (46 gates):
  - the premise holds (NIPA 1.7.5);
  - the account's enterprise line is at response 0;
  - netting credits the charges twice;
  - the section 8 readings;
  - the first version's Medicaid argument for health netting corrected.
- About 15:40 The parent made three calls:
  - B is the headline, with A and C kept as labelled rows;
  - public housing is keyed to rental assistance, tied to `housing_subsidies`;
  - the recipe `engine_components.json`, with a recompute gate.
- 15:50 Done (47 gates):
  - public housing at the evaluated rental-assistance key, 7.40% / 7.64%;
  - the recipe, with the build's rules and this lane's beside them;
  - both per-specification files rebuilt from it to 1e-12;
  - K-12's account key reported beside the pupil share.
- 16:15 Fixed the variant at model.json's rental key. It had used the key cell's `share` (0.1264), but the engine
  charges `target_bn`, so the key is 0.1252, the parent's 12.5%. Added the gate that the evaluated amount is model.json's
  plus the case's edit (48 gates). The public-housing figures are unchanged, and that variant moves by −$0.01bn.
- After 16:15 The parent accepted both findings. It asked for no netting on any line, and for option D (all enterprises
  respond) beside option A (enterprises out). It also asked for a primary-text check of whether the enterprise surplus
  is before interest, and for the `enterprises` switch in the recipe. A second message asked for:
  - every variant as a rule;
  - netting listed once, as rejected;
  - the switch as a top-level choice.

  Section 8's readings A, B and C and the earlier rule are superseded by options D and A.
- 17:07 Done (52 gates):
  - no netting;
  - the enterprise block, with BEA's total and its remainder;
  - the NIPA 3.8 groups against their returns;
  - MP-5 and Handbook ch. 2 fetched and gated;
  - K-12's central key moved to the account's;
  - the 12 variants as rules, with a gate that reproduces them.
- 17:13–17:23 Four interface fixes for the build (53, then 54 gates):
  - `enterprises.allowed`, which the build's reader requires;
  - one land row per component in `gaps.csv`, gated;
  - a separate note on each public-housing variant;
  - the group nets under D, the receipt-key gate, and D at the spending lines' population key.
