**Verdict:** Priced at the main case's own keys and responses for every tax-financed service it lets respond, the
omitted return on public capital is **$15.5–16.4bn a year at 2%** and **$23.2–24.6bn at 3%** ($54.2–57.4bn at 7%,
reported only). K-12 is $9.52bn of it at 2% and $14.28bn at 3%, the school lane's figures reproduced exactly. The rest
comes from colleges and libraries ($2.6–2.7bn at 2%), general government's offices ($2.0–2.9bn), public order and
safety ($1.1bn) and health ($0.2bn). Added at each specification, the candidate main case is **$274.0–316.6bn**
(2% at the low end, specification 48; 3% at the high end, specification 11), against $258.5–292.0bn now. The end
specifications do not move. The largest gap is land, at $1.5–1.6bn at 2% for each 10% of land-to-structure value.
[CALCULATION: `capital_return.py` → `derived/`; 30 gates pass; a second run is byte-identical]

> **Update in progress (14:15 JST).** The parent extended the scope. A conditional block for roads, transit and parks
> capital is being priced at the sister lane's `service_response_long_run_2026_09_27/derived/responses.json`, and
> primary sources for government land are being checked. The figures above stay the core result until this note is
> removed. [UNVERIFIED]

Lane run by claude-opus-5-5 on 2026-09-27 for parent session immigration-research-1c ([brief](BRIEF.md)). The numbers
sit beside the account and are not adopted. All amounts are 2024 dollars for income year 2024.
[FRAMING-SENSITIVE] Both rates are conventions, and so is charging a return on public capital at all.

## Results

The group's return, $bn a year, at the case's end specifications (48 low / 11 high), both fill-in methods averaged:

| Line | Capital charged (national, 2024 average) | Key | Response | 2% | 3% | 7% (reported only) |
|---|---:|---|---|---:|---:|---:|
| Education: K-12 (school lane) | 2,723.9 | pupil share 0.1748 | 1 | 9.52 | 14.28 | 33.33 |
| Education: colleges and libraries | 851.0 (of 1,283.6) | college line 0.1545 / 0.1588 | 1 | 2.63 / 2.70 | 3.94 / 4.05 | 9.20 / 9.46 |
| General government: offices, S&L | 1,292.9 | population 0.1172 | 0.6000 / 0.8504 | 1.82 / 2.58 | 2.73 / 3.87 | 6.36 / 9.02 |
| General government: offices, federal nondefense | 152.2 | population 0.1172 | 0.6000 / 0.8504 | 0.21 / 0.30 | 0.32 / 0.45 | 0.75 / 1.06 |
| Public order and safety, S&L | 289.5 | use 0.1342 | 1 | 0.78 | 1.17 | 2.72 |
| Public order and safety, federal nondefense | 110.2 | use 0.1342 | 1 | 0.30 | 0.44 | 1.03 |
| Health, S&L (net of hospital sales) | 94.5 (of 366.0) | health_other 0.0566 | 1 | 0.11 | 0.16 | 0.37 |
| Health, federal nondefense | 106.0 | health_other 0.0566 | 1 | 0.12 | 0.18 | 0.42 |
| **Total** | 5,620.2 | | | **15.48 / 16.41** | **23.23 / 24.61** | **54.20 / 57.42** |

[DATA: `derived/components.csv`, `derived/summary.json` → `by_component_at_case_ends_bn`, `by_line_at_case_ends_bn`]

Only two things vary across the 64 specifications: the college key, with the allocation rule, and the
general-government response. The school fraction cancels out of the college key, and the normalization and
uninsured-care keys do not enter. The return is therefore smallest at specification 48 and largest at
specification 11, the case's own ends. On every line, the return at 2% is 0.86 (K-12) to 1.14 times the depreciation
already inside it. [CALCULATION]

| Case, $bn a year | Low end | High end | End specs |
|---|---:|---:|---|
| Adopted main case | 258.49 | 291.95 | 48 / 11 |
| **Candidate: 2% at the low end, 3% at the high end (the brief's band)** | **273.97** | **316.56** | 48 / 11 |
| Candidate at 2% | 273.97 | 308.36 | 48 / 11 |
| Candidate at 3% | 281.72 | 316.56 | 48 / 11 |
| Candidate at 7% (reported only) | 312.68 | 349.37 | 48 / 11 |

**Move at fixed specifications.** Both fill-in methods keep specification 48 as the low end and 11 as the high end at
every rate, so each band end moves by the return at that specification. The low end moves +$15.48bn at 2% and the high
end +$24.61bn at 3%. [DATA: `derived/bands.csv`, which carries the return at specifications 48 and 11 and at each
band's own ends]

## 1. Inventory

Every spending line of the engine (`assumption_explorer_2026_09_21/engine.js`, model lines plus the case's three
correction lines) with its response and key in the main case is in `derived/lines.csv`. The responses and keys come
from the evaluation that the package's `cost()` makes at each specification (`spec_lines.cjs`).

| Line (national $bn) | Response | Key | Capital treatment |
|---|---|---|---|
| Education (1,221.2) | schools 1, colleges 1 | education_mix + corrections | charged: K-12 and colleges/libraries |
| General public services (401.6) | 0.6000 / 0.8504 | population | charged: offices |
| Public order and safety (519.2) | 1 | use | charged: public safety structures |
| Health (306.5) | 1 | health_other | charged: health care structures, S&L net of fees |
| Income security (167.8) | 1 | cash_assistance | none identified: no BEA type; its offices sit in Office, charged under general government |
| Housing and community services (14.5) | 1 | population | excluded: fee-financed (below); sanitation a gap |
| Economic affairs (451.9) | 0, held fixed | resources | none: highways, transportation, power, conservation |
| Recreation and culture (54.3) | 0, held fixed | population | none: amusement and recreation, museums, zoos |
| Defense (854.8) | 0 | population | none |
| Domestic interest (1,118.9) | 0 | population | none (double-count gate) |
| Subsidies (94.2) | 0 | various | none |
| 24 household transfer lines | 1 | various | none: transfers use no public capital; administration capital sits in the function lines |
| Foreign lines, rounding | 0 | external | outside the resident account |
| Lane constants (care, shelter, audit rows) | 1 | constant | none: no BEA asset type |

[DATA: `derived/lines.csv`; gates `line_keys_and_responses_are_the_main_cases`, `response_zero_and_fixed_lines_stay_at_zero`]

`derived/asset_types.csv` accounts for every BEA government asset type (all levels, $20,931bn on the 2024 average),
with its treatment. The types add to BEA's total to within $0.8bn (gate).

## 2. Capital per line

**Which structure type serves which line is BEA's own mapping.** NIPA 3.17 gives gross investment by function.
For every function, it covers the structure-type investment mapped to it (FAAt705). The residual across all
functions equals equipment plus software for state and local governments (1.000 in 2019, 0.962 in 2024) and
equipment plus software plus R&D for federal nondefense (0.999, 1.011).
[CALCULATION: `derived/mapping_check.csv`]

**Offices go to general government, as NIPA files them.**
- **NIPA's own filing.** State and local "unallocable" investment, the general-government "Other" row, is
  "unallocable state and local government consumption expenditures and gross investment" (NIPA 3.15.5 note 3). Taken
  as 3.15.5 line 82 less 3.16 line 85, it equals 0.83–0.99 of BEA's S&L Office investment in every year 2005–2024
  (0.991 in 2024). NIPA therefore files office-type capital, and so presumably its depreciation, under general
  government. [CALCULATION; INFERENCE for the depreciation]
- **What the type holds.** Census's Office category "also includes city halls, borough halls, municipal buildings,
  courthouses, and state capitol buildings" [SOURCE: `_cache/census_c30_definitions.html`].
- **BEA's Office is broader than Census's.** BEA's S&L Office investment is 2.7–4.3 times Census VIP's Office
  construction (1993–2024). BEA's Public safety tracks VIP's correctional construction (0.83–1.14) rather than all of
  VIP's public safety. BEA's Office therefore likely also holds buildings that Census puts elsewhere, fire stations
  among them. [DATA: `derived/bea_vs_census_types.csv`; INFERENCE]
- **Consequence.** The central estimate follows the brief and NIPA, charging all offices at general government's key
  and response. Variants bound the alternatives (section 4).

**Housing and community services: excluded as fee-financed.** State and local consumption on this line "Consists of
current expenditures for sanitation" (NIPA 3.16 note 8, $11.8bn). Water, sewer and public housing therefore produce
no state and local consumption: they are enterprises whose fees recover their capital. Sanitation structures sit
inside BEA's Sewer systems type and are a gap. [SOURCE; gate `sl_housing_consumption_is_sanitation_only`]

**Education.**
- **K-12.** The school lane's script, rerun on its own cached primary files into a scratch directory, gives K-12
  capital of $2,723.9bn. That is educational structures × 0.6748 plus K-12 equipment and software. It reproduces $9.52bn
  at 2%, $14.28bn at 3% and $33.33bn at 7% to 1e-9 at every specification. Every CSV the rerun writes is byte-identical
  to the committed one. `summary.json` differs only in the recorded hash of `debt_legacy_2026_09_23/RESULT.md`, which a
  peer edited after that lane ran. [CALCULATION]
- **Colleges and other education.** The non-K-12 part, (1 − 0.6748) × $3,947.6bn = $1,283.6bn, is split by the
  post-1993 VIP vintages, weighted by the school lane's perpetual inventory [CALCULATION]:
  - higher education 0.870, charged net of tuition;
  - libraries 0.064, charged in full;
  - museums, zoos and galleries 0.033, not charged: they belong to recreation, which is held fixed. VIP's "other
    educational" "also includes zoos, arboreta, botanical gardens, planetariums and observatories" [SOURCE].
  - preschool and unlisted 0.034, not charged (gap).

  Pre-1993 vintages take the post-1993 composition [INFERENCE].
- **The college key and response** are the account's own: (education_mix + college re-key) / national education line,
  0.1545 under shared allocation and 0.1588 under personal, at the college response (1). The group is charged in
  proportion to the account's college line. The school fraction scales both the group's college charge and the
  national college line, so it cancels. K-12 and college shares of capital come from VIP rather than the account's
  consumption split, so each dollar of educational structures is charged once.
- **Tuition-financed share.** S&L higher-education consumption is $229.96bn (NIPA 3.16 line 108; education's social
  benefits sit in "Other" to within $0.69bn, gated). Tuition and related charges are $103.91bn (NIPA 3.10.5 line 58).
  The tax-financed share is 229.96 / 333.87 = **0.689**, and the composite factor on the non-K-12 stock is 0.663.

**Health.**
- **State and local.** The account's line is net of $364.5bn of S&L sales, so S&L health care structures are charged
  at net / gross = 126.839 / 491.383 = **0.258** (NIPA 3.17 lines 26–27), as the brief asks.
- **Federal nondefense health care structures** are charged in full. Federal nondefense sales across all functions
  are at most 3.1% of federal health consumption (NIPA 3.10.5 line 46). [DATA]
- **Why the netting is not a loss.** The fees recover part of the capital's cost, and part of them is paid through
  Medicaid and education benefits, which the account charges on their own lines. Charging the full stock would count
  that part twice. [INFERENCE]

**Public order and safety.** State and local plus federal nondefense Public safety structures (prisons, jails, police
stations; federal prisons and law-enforcement facilities), at the use key and response 1. Courthouses are Office.

**Equipment and intellectual property.**
- **BEA publishes no function split** of equipment, software or R&D stocks, so beyond K-12's F-33-keyed equipment,
  which is part of the reproduced figure, they are gaps.
- **A derived split.** NIPA 3.17 function investment less the mapped structures gives shares of equipment-plus-software
  investment, the school lane's own method for education's 22.7% (means of 2019 and 2024):
  - state and local: public order and safety 0.113, health 0.226, general government 0.053, income security 0.035,
    colleges 0.078;
  - federal nondefense: public order and safety 0.168, general government 0.195, income security 0.055.
- **Size.** On that split, equipment and software would add $0.55–0.59bn at 2% (variant below).
- **Federal health's investment** ($108.3bn in 2024) is mostly R&D and cannot be separated. [CALCULATION]

## 3. Rates [FRAMING-SENSITIVE]

The rates are the school lane's, and its gates check each sentence in the primary texts (`school_capital_return_2026_09_26/_cache`):
- **2%:** OMB A-4 (2023), the 30-year real 10-year Treasury rate plus 0.3 points; 2024 real par yields were 1.94–2.15%.
- **3%:** A-4 (2003), in force again since M-25-15 revoked the 2023 circular on 12 February 2025.
- **7%:** A-4 (2003)'s "average before-tax rate of return to private capital", reported only.

The real rate applies to the current-cost net stock, averaged over the year-end stocks of 2023 and 2024. This is the
standard user-cost pairing: it leaves out holding gains.

## 4. Variants

Change in the group's return, $bn, at specifications 48 / 11:

| Variant | 2% | 3% | Candidate band at 2% | at 3% |
|---|---:|---:|---:|---:|
| Central | 15.48 / 16.41 | 23.23 / 24.61 | 273.97–308.36 | 281.72–316.56 |
| + equipment and software, derived split | +0.55 / +0.59 | +0.82 / +0.88 | 274.52–308.95 | 282.54–317.45 |
| S&L offices at general government + audit row 8's increment (0.1139) | +0.35 / +0.35 | +0.52 / +0.52 | 274.32–308.71 | 282.23–317.08 |
| All offices at response 1 (upper bound) | +1.35 / +0.51 | +2.03 / +0.76 | 275.33–308.87 | 283.75–317.32 |
| End-2024 stocks | +0.28 / +0.30 | +0.42 / +0.44 | 274.25–308.66 | 282.13–317.01 |
| Higher-education dormitories, parking, unions (0.211 of its construction) fee-financed | −0.50 / −0.52 | −0.75 / −0.77 | 273.47–307.85 | 280.96–315.79 |
| K-12 at the account's school key (0.159 / 0.163) instead of the pupil share | −0.87 / −0.63 | −1.31 / −0.94 | 273.10–307.73 | 280.41–315.62 |
| Colleges as (1 − school fraction) of educational structures | −0.33 / −1.58 | −0.49 / −2.37 | 273.22–307.21 | 280.19–315.24 |

[DATA: `derived/bands.csv`; no variant moves an end specification]

- **Audit row 8.** The case gives unallocable S&L spending a higher response through audit row 8: "spending of every
  kind" at the all-spending elasticity 0.962 rather than the administration elasticity 0.842
  (`dataset_integrity_2026_09_23/spending.md` #7). If S&L offices are read as unallocable spending, as NIPA's
  investment filing suggests, the consistent response is general government's plus 0.1139. That adds $0.35bn at 2% at
  both ends. It is arguably the more consistent reading. The central estimate keeps the brief's response. [INFERENCE]
- **Colleges by the school fraction.** This variant follows one reading of "in proportion to the account's college
  line": it scales college capital by the account's consumption split. It then no longer adds up with the K-12
  capital, which comes from VIP, so the central estimate does not use it.

## 5. Double counts

- **Interest.** The interest row responds at 0 at every specification of the evaluation `cost()` makes (engine
  `interest_response`). If a scenario charged it, the debt-financed slice of this return would come off; the school
  lane put K-12's at $2.78bn at response 1. [DATA; gate `interest_row_held_at_zero`]
- **debt_legacy is federal only.** It keeps "the lead's no-legacy framing for state-local gaps", and "State-local
  interest ($274.6bn) sits in the account's interest row". [SOURCE; gated]
- **The production term** pays capital its rental rate: "The model pays the opportunity cost of capital"
  (`research/immigration-matched-benefits-2026-09-19.md`, dims `capital_adjustment`, `labor_share`). Public capital is
  not a factor in that CES term. [INFERENCE; gated text]
- **New seats** at today's construction cost stay unpriced
  (`decisions/2026-09-26-main-case-schools-full-cost.md`). If they are ever priced as a user cost of new capacity, they
  contain this return, and only one should count. Land is not priced (next section).
- **Fees.** The fee-recovered share of hospitals and colleges is netted out (section 2).

## 6. Exclusions and gaps

**Excluded, with the reason** (`derived/asset_types.csv`):

| Excluded | Stock, $bn | Reason |
|---|---:|---|
| Defense, all assets | 2,299 | response 0 |
| S&L highways and streets | 4,890 | economic affairs held fixed |
| S&L transportation, power | 1,196 / 542 | held fixed; largely fee-financed |
| S&L sewer, water, residential | 1,225 / 916 / 420 | enterprises; fees recover their capital |
| S&L conservation; amusement and recreation | 216 / 383 | held fixed |
| Federal nondefense conservation, highways, transportation, power, recreation | 554 | held fixed |
| Museums and zoos inside educational structures | 42 | recreation, held fixed |

**Gaps.** Each figure is the group's return, $bn, if the item were charged at its line's key and response, at
specifications 48 / 11 [DATA: `derived/gaps.csv`]:

| Gap | 2% | 3% |
|---|---:|---:|
| **Land**, each 10% of land-to-structure value (K-12 0.93, colleges 0.26/0.27, offices 0.20/0.29, safety 0.11, health 0.02) | **1.53 / 1.62** | **2.29 / 2.43** |
| R&D, federal nondefense, health's share (0.18–0.79 of it; mostly NIH) | 0.19–0.86 | 0.29–1.29 |
| R&D, state and local (university research, inside NIPA's education investment) | 0.45 / 0.46 | 0.67 / 0.69 |
| Equipment and software beyond K-12 (derived split; the variant) | 0.55 / 0.59 | 0.82 / 0.88 |
| Sanitation structures inside Sewer systems (upper bound, 10.6% of that type's investment) | 0.30 | 0.46 |
| Federal nondefense educational structures (no K-12/other split) | 0.19 / 0.20 | 0.29 / 0.29 |
| Preschool and unlisted educational structures | 0.13 / 0.14 | 0.20 / 0.21 |
| Commercial and other structures, S&L and federal (no function) | 0.27 / 0.38 | 0.40 / 0.56 |

Further gaps:
- **Land [GAP].** BEA's stocks cover produced assets only. The figure is a conversion, not an estimate; as the school
  lane notes, closing it takes parcel acreage and land prices.
- **R&D [GAP].** It is non-rival, so a removal need not shrink it. Its depreciation nevertheless sits in the health
  and education lines that the account charges at response 1. [INFERENCE]
- **Other sales by function [GAP].** S&L "other sales" of $215.8bn are not published by function. Only hospital
  charges and tuition are netted.
- **Capital per pupil or user where the group lives [GAP].** It is not measured; national average capital per unit of
  key applies.

**Conditional on a later case.** The peer lane `service_response_long_run_2026_09_27` is working out long-run
responses for economic affairs and recreation. If either comes to respond, multiply by that response:
- tax-financed economic-affairs structures (highways, conservation; $5,555bn): **$8.96bn at 2% and $13.43bn at 3% per
  unit of response**, at the resources key 0.0806;
- transportation and power (largely fee-financed; $1,801bn): $2.90bn and $4.36bn;
- recreation (amusement and recreation, museums and zoos; $467bn): $1.09bn and $1.64bn.

## Gates (30 pass; `derived/gates.json`)

- **The case.** Per-specification costs from `cost()` reproduce $258.4885–291.9548bn, with ends 48 / 11 in both
  methods. The published corrections.json gives the same cost at every specification to 1.7e-13. The responses equal
  `meta.responses`. Each line's key and response are the case's, and the lines held at zero stay there.
- **Sources.** The account's lines equal NIPA 3.17. The FA types add to BEA's totals. The mapping leaves no negative
  residual, and its residuals fit equipment and IP within 5%. NIPA files S&L office investment under general
  government. Census puts courthouses in Office. S&L housing consumption is sanitation only.
- **Factors.** The higher-education and health fee factors pass their checks, and the VIP parse matches the school
  lane's.
- **K-12.** It reproduces the school lane: the return and the land conversion to 1e-9, and structures equal to the key
  × educational structures.
- **Coverage and bands.** The asset types cover all government capital. The candidate band is ordered, and its ends
  keep the case's specifications.
- **Double counts.** The interest row stays at 0, debt_legacy is federal only, the production term pays private
  capital only, and new seats and land are unpriced.

## Files covered and skipped

Covered, all parsed by the script:
- **The school lane's cached primary files**, hash-checked by its `sources.csv`:
  - BEA Fixed Assets Section 7 (FAAt701, 703, 705), with lines 1, 22 and 38–74 label-checked;
  - Census VIP state and local, 1993–2025, including the Library/archive, Dormitory, Parking and Student
    union/cafeteria rows;
  - its OMB texts, gated there.
- **Pinned NIPA Section 3** (`sources/immigration-fiscal/data/external/bea_nipa/Section3All_xls.xlsx`):
  - T3.10.5 lines 46 and 57–60;
  - T3.15.5 lines 82, 100–114 and note 3;
  - T3.16 lines 85, 101 and 106–111, with note 8;
  - T3.17 lines 2–31, 55 and 115–133.
- **Census C30 definitions**, fetched 2026-09-27 from https://www.census.gov/construction/c30/definitions.html into
  `_cache/` (hash in `derived/summary.json`).
- **Repo files, read-only** (hashes in `summary.json`):
  - `main_case_schools_full_2026_09_26` (`package.cjs` through `spec_lines.cjs`; `derived/corrections.json`,
    `summary.json`, `main_case_bands.csv`);
  - the September 24 and 26 packages; `finite_response_2026_09_26/derived/r_values.json`;
  - engine.js and model.json;
  - `debt_legacy_2026_09_23/RESULT.md`, the matched-benefits memo and the schools decision;
  - `dataset_integrity_2026_09_23/spending.md` (row 8, read, not parsed).

Skipped:
- **BEA's detailed government fixed-asset files.** None are public by function. The school lane found the detailed
  files cover private assets only.
- **Census of Governments capital outlay by function.** It is a flow that includes land and equipment. NIPA's function
  investment, which BEA builds from it, was used instead.
- **Land data.** See the gap.

## Reproduce and validation

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/capital_return_services_2026_09_27/capital_return.py
node infra/immigration-fiscal/main_case_schools_full_2026_09_26/main_case.cjs | tail -1
```

- **Wall time.** The final run took 1.5 s: the school lane's rerun, `node spec_lines.cjs` and the BEA parse.
- **Reruns.** Two consecutive runs leave all 11 files in `derived/` byte-identical (sha256 compared).
- **`main_case.cjs`** prints "all gates passed", with no FAIL line. The four files in its `derived/`, and
  `main_case_2026_09_24/derived/stack_line_deltas.json`, which the package rewrites when the CPS cache changes, are
  byte-identical before and after. `git status` shows no change outside this directory.
- **Side effects.** Importing the school lane sets `sys.dont_write_bytecode`, so no `__pycache__` is left in its
  directory.

## Run log

- 13:32 Stub written.
- 13:55 Design checkpoint: keys, the mapping and the fee factors were probed.
- 13:58 First full run: 28 gates.
- 14:05 Added the brief's combined band, the asset-type accounting (30 gates), the BEA-versus-Census table, the
  college-by-fraction variant and the conditional economic-affairs and recreation conversions. Validation above.
