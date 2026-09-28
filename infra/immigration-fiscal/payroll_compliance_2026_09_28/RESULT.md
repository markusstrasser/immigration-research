**Verdict:** The adopted case does not assume full compliance for the group's imputed unauthorized, and what it still credits at full compliance nets to about zero. Audit row 2 already scales the payroll and income-tax keys of the flagged Latin-American-born to an on-books share (0.526 for the Mexico-born). For the Mexico-born that takes $64.8bn of their $136.8bn of CPS wages off the books. In construction, landscaping, janitorial work and restaurants it removes $31.6bn of their wages, against the $32.8bn (range $26.9–52.9bn) that the compliance-gap slopes imply. So ladder 220's "already inside" holds for the flagged wage earners.

It does not hold for three parts:
- the group's other self-employed, whose CPS income sits more in informal industries (62% against 38% for other residents);
- the imputed unauthorized born outside Latin America, whom the case leaves unscaled;
- the consumption key, which still subtracts taxes the off-books part never pays.

Each part is priced on the adopted case at specifications 48 / 11 ($321.82 / $387.37bn), calibrated to the case's own flag and keys:

| Item | Cost change at 48 / 11, $bn |
|---|---:|
| Self-employment | +0.48 / +0.69 |
| Off-books slopes | +0.43 / +0.38 |
| Unauthorized born outside Latin America | −0.62 / −0.60 |
| Taxes on cash consumption | −0.58 / −0.57 |
| **All together** | **−0.37 / −0.16** |

The combined range is −1.62 / −1.43 to +3.97 / +4.18 with row 2 held at its central shares, and −2.67 / −2.49 to +5.03 / +5.25 across the on-books range.

The lane also found a convention issue. The case carries row 2 through CBO's re-key in proportion to raw shares. Moving only the group's shares inside CBO's income groups is what a tax-record distribution warrants, and under that rule row 2 is worth $0.81bn less at both ends. These are candidate items, not a new case.

Lane run by claude-opus-5-5 on 2026-09-28 for parent session immigration-research-1c ([brief](BRIEF.md)).

All amounts are 2024 dollars, $bn, and shown as specification 48 (shared allocation, the band's low end) / 11 (personal allocation, the high end), with both fill-in methods averaged. A plus sign raises the account's cost.

## 1. The keys, line by line, and "already inside"

The account's national totals are BEA collections. They come from NIPA Table 3.4 line 1 (personal current taxes), 3.1 line 8 (contributions for social insurance), 3.5 line 1 (taxes on production and imports) and 3.1 line 15 (current transfer receipts) [DATA: `full_account_receipts_2026_09_20/builder.py` `validate_bea_parents`]. The group's share of each total comes from CPS ASEC 2025 (income year 2024) through the receipts builder's keys. This lane rebuilds those keys element for element [DATA: gate `key_vectors_are_the_accounts`], and they reproduce model.json's shares to 1e-9 [DATA: gate `raw_shares_are_model_json`].

| Line (national $bn) | Group key | Earnings concept | Tax model | Reported or matched | CBO gradient in the case | Row 2 | Already inside? |
|---|---|---|---|---|---|---|---|
| Federal income tax (2,403.2) | `federal_liability` = FEDTAX_BC | the tax unit's survey income | Census tax model: "Federal income tax liability, before refundable credits" | self-reported, nonrespondents hot-decked; not matched | individual income tax, gross (CBO 2022) | scaled | for the flagged only; not the group's self-employment |
| State and local income tax (536.2); other personal tax (9.7) | `state_liability` = STATETAX_A, floored at 0 | same | Census tax model: "State income tax liability, after all credits" | same | none | scaled | same |
| Employee and employer OASDI (610.4; 615.7) | `wage_oasdi` = WSAL_VAL capped at $168,600 | wage and salary earnings, all jobs | the statute, through a wage key | self-reported, hot-decked | payroll taxes (CBO 2022, ratio target) | scaled | for the flagged; not for unflagged off-books workers or the flagged born outside Latin America |
| Employee and employer HI (196.7; 175.0) | `wage` = WSAL_VAL | same | same | same | same | scaled | same |
| Self-employment OASDI+HI (86.9) | `self_payroll`: 12.4% of capped and 2.9% of all net earnings, 0.9235 × (SEMP_VAL + FRSE_VAL), from $400 | CPS self-employment income | SECA on survey income | self-reported, hot-decked | payroll taxes | scaled | for the flagged only |
| Other social contributions (93.4) | `positive_fica_worker`: FICA > 0 | count of workers with modelled FICA | — | — | none | scaled | as wages |
| Corporate taxes on labor (165.9) | `wage` | — | — | — | none | scaled | inert: indirect receipt, response 0 |
| General sales (602.4), excise (371.3), customs (83.6), personal transfers (141.1) | `consumption` = SPM resources per person, floored at 0 | income less modelled FICA, federal and state tax, plus benefits | subtracts taxes at full compliance | survey | excise only, on its federal 26.9% | untouched | no: the off-books part's unpaid taxes stay subtracted |

Sources for the table: [DATA: `compliance.py` `Frame.vectors`; `external_benchmarks_2026_09_24/frame.py`; `derived/pricing.json` `model_json_lines`]. The quotes come from [SOURCE: `_cache/sources/asec2025_ddl_pub_full.txt`, "SubTopic: Tax Model Items", FEDTAX_BC, STATETAX_A]. The CBO specification is `cbo_arm.py`, bundle `all_but_medicaid|2022`, reproduced to 8.3e-16 [DATA: gate `cbo_gradient_reproduces_the_benchmark_lane`].

The tax items are model outputs on survey income. A liability simulated on reported income is what the unit would owe if it filed and reported that income, so every tax key prices full compliance on survey income, and only row 2 departs from it [INFERENCE].

**How the unauthorized enter the survey.**
- **Sampling and weights.** The ASEC samples addresses and asks no legal-status question [INFERENCE: the dictionary has citizenship and birthplace items only]. Weights are controlled to "independently derived population controls" by age, sex, race and Hispanic origin. Their migration component includes "Net international migration of the foreign born" [SOURCE: `_cache/sources/cpsmar25.txt`, Estimation Procedure]. The controls use no nativity or status cell, so the unauthorized count as far as they respond and as far as the Census estimates include them [INFERENCE].
- **Missing items.** Nonrespondents' income is filled by hot deck ("Levels 1-3 indicate imputations use of income range responses") [SOURCE: `asec2025_ddl_pub_full.txt`, I_ANNVAL]. Nothing in the public file is matched to tax or SSA records [INFERENCE].
- **Status.** Status is imputed by the account, not reported. The paper flag (Borjas's residual rules) marks:
  - 4.57M Mexico-born in the group;
  - 4.97M other Latin-American-born, all outside the group;
  - 5.36M born elsewhere, 2.07M of them without a bachelor's degree [CALCULATION: `derived/items.json` `meta.item1`].

  The paper flag counts every Medicaid reporter as legal, which is wrong in status-blind states. The benchmark frame prints `[DEGRADED] impute_status` on every run for that reason [DATA: `compliance.py` run log].

  The case replaces this flag with three changes [SOURCE: `cps_imputation_keys_2026_09_23/RESULT.md`, steps 4b and 5e]:
  - a state-aware flag, which does not read Medicaid as proof of legal status where states cover the unauthorized;
  - row 4 weights, which reweight the Mexico-born outside California and Texas to ACS cells;
  - two fill-in methods, which re-impute imputed items from union-matched donors and recompute taxes.
- **Flag noise.** A Social Security match "allows us to rule out as being unauthorized half of all individuals otherwise classified as unauthorized" [SOURCE: `_cache/sources/vt2026_epmc.txt`, abstract]. The flag is therefore noisy person by person. Its totals are calibrated to counts, so the group's dollars are less affected [INFERENCE].

**Settling "already inside", line by line.**
- **Wage-keyed lines** (employee and employer OASDI and HI, other contributions): inside, for the flagged Latin-American-born. Row 2 scales their wages, liabilities and FICA-worker flag by the on-books share [SOURCE: `onbooks_share_2026_09_23/RESULT.md`, Computation, quote-checked]. It removes $64.8bn of the $136.8bn of Mexico-born flagged CPS wages.
  - In the compliance-gap lane's four industries, row 2 removes $31.6bn of Mexico-born wages. Its slopes on the same CPS base give $26.9 / 32.8 / 52.9bn (low / central / high) [CALCULATION: `derived/item1_off_books_check.csv`].
  - Ladder 220's $2.3bn of Mexico-born payroll tax therefore sits inside row 2's off-books wages. What the slopes add beyond row 2 is priced below as item `slopes`.
  - Not inside: unflagged workers' off-books pay (`authorized_bound`, a bound), and the flagged born outside Latin America (`other_unauth`, which lowers the cost).
- **Self-employment line:** inside only for the flagged. The compliance-gap lane wrote that the 57% proprietor misreporting "is inside the adopted account through the September 24 tax correction". That holds only where row 2 scales the key. The rest of the group's self-employed are keyed at full compliance on survey income. Their income is 61.6% in Alm & Erard's informal categories, against 37.9% for other residents [CALCULATION: `derived/items.json` `self_employment_mix`]. The national total is collections, so the group is credited with self-employment tax that others' more formal income paid (item `se_industry`) [INFERENCE].
- **Income taxes:** inside for the flagged. The self-employment item carries its income-tax part. Misreporting of other income types is a sensitivity (`income_nmp`; see section 3).
- **Consumption lines:** not touched by row 2. Survey wages include cash pay, but SPM resources subtract modelled taxes the off-books part does not pay (item `cash_consumption`).
- **Corporate labor:** row 2 moves its key, but the receipt is indirect with response 0, so no item changes the cost through it [DATA: `pricing.json` `model_json_lines`, `direct: false`].
- **Social Security paid back:** the flagged receive $0.0bn of CPS Social Security [CALCULATION: `meta.item1`]. Payroll tax that is never paid back is therefore inside both sides of an annual account [INFERENCE].

**The items are calibrated to the case's basis.** They are built on the paper flag and the published keys. The case applies row 2 on the state-aware flag, with row 4's weights and the fill-in methods' re-imputed keys, and those keys carry less income-tax liability on flagged group members [CALCULATION: below]. Row 2's raw federal effect (shared) is $3.60 / 3.87bn under the two methods, against $5.66bn on the paper flag [DATA: `cps_imputation_keys_2026_09_23/_cache/onbooks_lane_line_deltas.json`]. Payroll is close: employee OASDI $2.73–2.75bn against $2.92bn.

For each case, line and allocation, `compliance.py` finds the factor c on the group's own part of an item. The factor makes this lane's relative change for "row 2 removed" equal the package's (stack `alone` against the case's stack). Others' part is taken as measured here, since the methods and row 4 act on the group. c is then applied to the group's part of every flag-based change [CALCULATION: `derived/calibration.csv`]. At central, shared / personal:

| Line | c |
|---|---:|
| Federal income tax | 0.72 / 0.71 |
| State income tax | 0.81 / 0.78 |
| OASDI | 0.97 / 0.94 |
| HI | 0.93 / 0.91 |
| Self-employment | 1.21 / 1.19 |
| Other contributions | 1.05 / 1.01 |
| Consumption (weighted by unpaid tax) | 0.84 / 0.82 |

Two checks support the calibration:
- It reproduces the package's receipts for row 2 removed: $12.700bn against $12.769bn at 48, and $12.624bn against $12.696bn at 11 [DATA: gate `calibrated_route_reproduces_row_2`].
- Fitted on row 2 removed alone, it also reproduces the package's receipts at the low and high on-books shares: +2.91 / +2.88 against +2.915 / +2.886, and −2.87 / −2.84 against −2.874 / −2.849 [CALCULATION: `derived/pricing.csv` and `pricing_lines.csv`].

Without calibration, and under the package's own proportional rule, the paper flag overstates row 2's receipts by 14–17% (14.52 / 14.90 against 12.77 / 12.70), mostly in the income taxes [CALCULATION: `pricing.csv`, `row2_r_route` `without` `stack_factor`].

**How items pass through CBO's re-key.** Where the case re-keys a line with CBO's income gradient, an item here moves only the group's shares inside CBO's income groups. CBO's distribution between the groups is left fixed because it is measured on tax returns ("CBO measures income from tax records and administrative transfers") [SOURCE: `external_benchmarks_2026_09_24/RESULT.md`, citing CBO 61911 p.11], and so already carries compliance by income group.

The package instead carries each stack through CBO's re-key in proportion to raw shares (`cboShifts` scales CBO's shift by the stack's factor) [DATA: `main_case_2026_09_24/package.cjs`]. That also counts the difference between income groups a second time [INFERENCE]. The effect is large where compliance differs by income group:
- self-employment: +0.48 / +0.69 by this lane's rule against +1.23 / +1.37 by the proportional rule;
- row 2 itself: under this lane's rule it moves the group's receipts by $0.81bn less at both ends (−11.89 / −11.82 against −12.70 / −12.62, both calibrated). The case would be $321.01 / $386.56bn [CALCULATION: `derived/pricing.csv`, `row2_r_route` `without`].

Both rules are priced for every item. The proportional rule is the sensitivity.

## 2. Compliance by group: evidence, measured and assumed

| Quantity | Value | Measured or assumed | Source |
|---|---|---|---|
| Unauthorized workers, 2010 | 7.0M; 3.1M "working and paying Social Security taxes"; 1.8M "other immigrants" who "used an SSN that did not match their name"; 3.9M in the underground economy | OCACT estimates from Census/DHS population estimates and SSA records | [SOURCE: `ssa_note151.txt` pp.2, 4] |
| Payroll tax from unauthorized workers, 2010 | "as much as $13 billion"; "only about $1 billion" of benefits attributable | OCACT estimate | [SOURCE: `ssa_note151.txt` p.2] |
| On-books share of flagged CPS wages, 2024 | Mexico-born 0.526 (0.415–0.635); other Latin-American-born 0.550 (0.401–0.683) | modelled: SSA's 2010 head count carried forward with assumed erosion, protected share and pay ratio | [DATA: `onbooks_share_2026_09_23/derived/onbooks_split.csv`] |
| On-books share, flagged born outside Latin America | 0.550 (0.401–0.683) | assumed: the case's other-origin share | same |
| Flagged persons (paper flag) | 4.57M Mexico-born in the group; 4.97M other Latin-American-born; 5.36M born elsewhere | CPS weights on an imputed flag | [CALCULATION] |
| Suspense-file wages | $100bn a year added TY2013–2023, from $1.2tn (TY1937–2012) to $2.3tn (TY1937–2023); TY2008–12: $373bn, 1.4–1.8% of wages | measured balances, net of reinstatement; the yearly figure is their difference over 11 years [CALCULATION] | [SOURCE: `ssa_oig_a0315500058.txt` pp.3, 5; `ssa_oig_022401.txt`] |
| IRS net misreporting, TY2014–16 | wages 1%, nonfarm proprietor 57%, rents 53%, other income 42%, capital gains 18%, interest and dividends 4% | measured: random NRP audits with detection-controlled estimation | [SOURCE: `irs_p1415.txt` Table 5] |
| Self-employment tax gap, TY2014–16 | $60bn a year (underreporting 53, nonfiling 7) | measured | [SOURCE: Pub 1415 Table 2] |
| Employer FICA/FUTA underreporting | $29bn a year | measured on the NRP Employment Tax Study, TY2008–10; excludes agricultural and household employers | [SOURCE: Pub 1415 §4.2.3] |
| Tax-return over CPS self-employment income, TY2001 | informal categories 0.489, other industries 0.915 (ratio 0.534) | measured: NRP-corrected returns against the CPS | [SOURCE: `tul1517.txt` Tables 2, 3, 6] |
| The same ratio for TY2014–16 | 0.661 | NMP measured; Alm & Erard's 39/46 split (share of income / share of underreporting) carried from TY2001, assumed | [CALCULATION] |
| Informal categories' share of CPS 2025 self-employment income | all 40.1% (Alm & Erard's 2001 CPS: 39.3%); group 61.6%; others 37.9% | measured; the category-to-code mapping is this lane's reading, published only for construction [INFERENCE] | [CALCULATION: `derived/industry_map.csv`] |
| Group's CPS self-employment income | $50.9bn of $568.3bn | measured (survey) | [CALCULATION] |
| Matched CPS–IRS level check | the self-employed "report 51 percent more to the CPS-ASEC than to the IRS"; the gap is "44 percent larger" than wage earners' | measured, CPS ASEC 2001–2016 linked to IRS and SSA records; no ethnic split | [SOURCE: `imboden_voorheis_weber_2022.txt` abstract, p.2] |
| Hispanic gap in any Schedule SE record, given CPS self-employment | −8.7 to −12.0 points (model 5: −10.7) | measured on matched CPS–SSA data, SSN holders only; carried to dollars as a factor, assumed | [SOURCE: `tv2025_pmc.txt` Table 4] |
| Mexican immigrants' self-employment over native Whites | +3.7 points in tax records, +0.8 in the CPS | measured; runs against the item | [SOURCE: `tv2025_pmc.txt` Table 6] |
| Off-books share of flagged wage workers | construction 0.60 (0.54–0.88); landscaping 0.59 (0.29–0.59); janitorial 0.74 (0.31–0.74); restaurants 0.01 (0–0.59) | cross-state association; the level check allows 0 | [DATA: `compliance_gap_2026_09_24/derived/edges_by_industry.csv`] |

What is measured: the IRS gaps and misreporting rates, the return-to-survey ratios, the matched filing gaps, the suspense-file totals and every CPS amount. What is assumed or modelled: every status assignment, the on-books shares, carrying 2001's split to 2016, the industry mapping, and turning the extensive-margin filing gap into dollars. No source splits compliance by origin and status in dollars, so each item applies a measured rate to the group's measured composition [INFERENCE].

## 3. Prices at 48 / 11, within fixed national totals

Every item re-keys the group's share of a fixed collection. Other residents' amount moves by the opposite, cell by cell. There are 17,024 edits across items, variants, methods and rules, and the largest departure is below 1e-9bn [DATA: gate `item_edits_hold_national_totals`]. Every variant keeps 48 and 11 as the band's ends, with 32 distinct specifications [DATA: `derived/pricing.csv` `band_min_bn`, `band_max_bn`, `distinct_specifications`].

| Item | What it does | Headline: calibrated, this lane's rule | Paper flag, this lane's rule | Calibrated, proportional rule | SE bound, 48 |
|---|---|---:|---:|---:|---:|
| `se_industry` central | self-employment income reaches returns at 0.489 (informal) and 0.915 (other) | +0.48 / +0.69 | +0.48 / +0.69 | +1.23 / +1.37 | 0.41 |
| `se_industry` low | informal gap at TY2014–16's relative 0.661 | +0.33 / +0.49 | +0.33 / +0.49 | +0.95 / +1.05 | 0.31 |
| `se_industry` high | adds the matched filing gap by ethnicity and generation for the unflagged | +1.14 / +1.35 | +1.14 / +1.35 | +1.98 / +2.12 | 0.44 |
| `slopes` central | the slopes set the flagged's share in the four industries | +0.43 / +0.38 | +0.46 / +0.42 | +0.34 / +0.29 | 0.63 |
| `slopes` low | | −0.85 / −0.85 | −0.96 / −0.99 | −1.00 / −0.99 | 0.50 |
| `slopes` high | | +4.33 / +4.29 | +5.01 / +5.10 | +4.29 / +4.24 | 1.42 |
| `other_unauth` central | row 2's rule for the flagged born outside Latin America without a degree, at 0.550 | −0.62 / −0.60 | −0.62 / −0.60 | −0.51 / −0.50 | 0.16 |
| `other_unauth` at 0.683 / 0.401 | | −0.44 / −0.42; −0.83 / −0.80 | same | −0.36 / −0.35; −0.69 / −0.66 | 0.11; 0.22 |
| `other_unauth` every flagged (bound) | | −3.49 / −3.29 | −3.49 / −3.29 | −3.92 / −3.71 | 0.25 |
| `cash_consumption` | unpaid taxes of row 2's off-books part added to SPM resources, denied credits taken out | −0.58 / −0.57 | −0.70 / −0.70 | −0.59 / −0.58 | 0.08 |
| `income_nmp` (sensitivity) | `se_industry` plus every other income type at IRS's misreporting rate, income taxes only | −0.77 / −0.69 | −0.77 / −0.69 | −0.26 / −0.19 | 0.79 |
| `authorized_bound` (bound) | the calibrated uncovered share as off-books pay of every unflagged worker in the four industries | +0.41 / +0.46 | +0.41 / +0.46 | +0.47 / +0.50 | 0.14 |
| **`all` central** | `se_industry` + `slopes` + `other_unauth` + `cash_consumption` | **−0.37 / −0.16** | −0.46 / −0.26 | +0.39 / +0.53 | 0.91 |
| `all`, low-cost readings, row 2 central | low slopes and self-employment, others at 0.550 | −1.62 / −1.43 | −1.85 / −1.70 | −1.05 / −0.91 | 0.71 |
| `all`, high-cost readings, row 2 central | high slopes and self-employment | +3.97 / +4.18 | +4.47 / +4.80 | +4.82 / +4.96 | 1.71 |
| `all` low-cost end | one on-books case throughout: row 2 at 0.635 / 0.683, others 0.683, low readings | −2.67 / −2.49 | −2.66 / −2.48 | −2.10 / −1.97 | 0.86 |
| `all` high-cost end | row 2 at 0.415 / 0.401, others 0.401, high readings | +5.03 / +5.25 | +5.29 / +5.58 | +5.88 / +6.02 | 1.36 |
| Row 2's convention (`row2_r_route` without, this lane's rule against the proportional rule, both calibrated) | | −0.81 / −0.81 | | | |

[CALCULATION: `price.cjs` → `derived/pricing.csv`]

Notes on the table:
- The SE bound sums each line's 160-replicate SE of r times the line's amount, as if the lines were perfectly correlated. It covers sampling only.
- The ends of `all` include row 2's own on-books range. The package prices that range with its own low and high stacks at +2.76 / +2.74 (low shares) and −2.72 / −2.70 (high shares) [CALCULATION: `pricing.csv`, `row2` rows]. So at the high end the items add +2.27 / +2.51 on top of the low shares, and at the low end +0.05 / +0.21 on top of the high shares. At the low end the slopes override the high shares in the four industries.
- `income_nmp` stays a sensitivity. The CPS captures less capital, rent and other income than tax returns show, mostly among other residents. That already mimics their misreporting, so applying IRS's misreporting rates on top would count it twice [INFERENCE]. For self-employment the ratios compare returns with the CPS directly, so no such overlap arises.

**Each line alone.** Direct receipts enter the cost one for one (response 0), so a line's price alone is minus its change in the group's amount, and the lines add up to the total [CALCULATION: the totals in `pricing.csv` equal the sums in `pricing_lines.csv` to the third decimal]. Headline rule:

| Line | Case amount 48 / 11 | `all` central | Low-cost readings, row 2 central | High-cost readings, row 2 central |
|---|---:|---:|---:|---:|
| Federal income tax | 111.18 / 101.45 | −0.06 / +0.06 | −0.32 / −0.24 | +1.40 / +1.55 |
| State and local income tax | 26.06 / 23.84 | −0.02 / −0.01 | −0.12 / −0.11 | +0.36 / +0.37 |
| Other personal tax | 0.47 / 0.43 | 0.00 / 0.00 | 0.00 / 0.00 | +0.01 / +0.01 |
| Employee OASDI | 53.28 / 50.12 | −0.05 / −0.05 | −0.29 / −0.29 | +0.73 / +0.71 |
| Employee HI | 15.79 / 14.72 | −0.02 / −0.02 | −0.09 / −0.08 | +0.21 / +0.21 |
| Self-employment OASDI+HI | 7.37 / 6.80 | +0.43 / +0.50 | +0.17 / +0.23 | +0.95 / +1.02 |
| Employer OASDI | 53.74 / 50.55 | −0.05 / −0.05 | −0.29 / −0.29 | +0.73 / +0.72 |
| Employer HI | 14.04 / 13.09 | −0.02 / −0.02 | −0.08 / −0.08 | +0.19 / +0.19 |
| Other social contributions | 10.29 / 9.92 | −0.02 / −0.02 | −0.10 / −0.10 | +0.20 / +0.19 |
| General sales tax | 49.05 / 49.05 | −0.29 / −0.28 | −0.25 / −0.25 | −0.41 / −0.40 |
| Excise | 30.14 / 30.14 | −0.17 / −0.16 | −0.15 / −0.15 | −0.24 / −0.23 |
| Customs | 6.81 / 6.81 | −0.04 / −0.04 | −0.04 / −0.03 | −0.06 / −0.06 |
| Personal current transfers | 11.49 / 11.49 | −0.07 / −0.06 | −0.06 / −0.06 | −0.10 / −0.09 |
| **Total** | | **−0.37 / −0.16** | **−1.62 / −1.43** | **+3.97 / +4.18** |

By kind of line, headline rule [CALCULATION: `pricing_lines.csv`]:

| Item | Income taxes | Wage payroll | Self-employment | Consumption | Total |
|---|---:|---:|---:|---:|---:|
| `se_industry` | +0.14 / +0.27 | 0 | +0.34 / +0.42 | 0 | +0.48 / +0.69 |
| `slopes` | +0.15 / +0.13 | +0.15 / +0.13 | +0.12 / +0.11 | 0 | +0.43 / +0.38 |
| `other_unauth` | −0.31 / −0.29 | −0.31 / −0.30 | 0.00 / −0.01 | 0 | −0.62 / −0.60 |
| `cash_consumption` | 0 | 0 | 0 | −0.58 / −0.57 | −0.58 / −0.57 |
| `income_nmp` | −1.11 / −1.11 | 0 | +0.34 / +0.42 | 0 | −0.77 / −0.69 |
| `authorized_bound` | +0.26 / +0.31 | +0.14 / +0.15 | 0 | 0 | +0.41 / +0.46 |
| `all` central | −0.07 / +0.06 | −0.16 / −0.17 | +0.43 / +0.50 | −0.56 / −0.54 | −0.37 / −0.16 |

## 4. The other direction

- **Payroll tax on suspense-file wages that is never paid back** is already in both keys. The tax is in BEA's collections and in the group's wage keys at the on-books share. The flagged receive no CPS Social Security, so an annual cash account needs no item [INFERENCE]. At 15.3% the $100bn a year of suspense wages carry about $15bn of OASDI and HI tax, covering all workers and all origins [CALCULATION]. Note 151 puts 2010's contributions from unauthorized work at up to $13bn against $1bn of benefits [SOURCE: `ssa_note151.txt` p.2]. Benefits later credited when status changes are an accrual question, outside an annual account [INFERENCE].
- **Sales and excise tax on cash income** is partly in the key. Survey wages can include cash pay (off-the-books earnings are absent from SSA records "though they could be reported in the ASEC", Bollinger et al. 2019 as quoted in `onbooks_share_2026_09_23/RESULT.md`) [SOURCE], so SPM resources hold it, but they subtract modelled FICA and income taxes that the off-books part does not pay. Adding those back, less the credits row 2 denies, gives `cash_consumption` at −0.58 / −0.57 (paper flag −0.70 / −0.70). It lowers the cost.
- **The same rule for everyone flagged:** `other_unauth`, −0.62 / −0.60 (bound −3.49 / −3.29). It lowers the cost.
- **Survey under-capture of off-books pay** is not in the case. If the CPS misses 10–25% of off-books pay, row 2 overstates the group's lost tax, and the on-books lane put that at −$0.9 to −2.4bn on its own basis. No source measures it for this population [SOURCE: `onbooks_share_2026_09_23/RESULT.md` verdict]. It lowers the cost.
- **Over-withholding by non-filers** is unpriced. Employers withhold income tax that a worker with a mismatched SSN rarely reclaims. No source was found; it would lower the cost [INFERENCE].
- **Matched evidence against `se_industry`.** Tax records show more self-employment than the CPS for Mexican, Central American and other Latin American immigrants with SSNs (+3.7 against +0.8 points over native Whites; "significantly understated in the CPS relative to the administrative records"). The paper finds that underreporting to tax authorities "does not appear to account for the measurement error we observe" [SOURCE: `tv2025_pmc.txt` Results]. The paper gives rates, not dollars, so this is unpriced. It would shrink the item.

## Method

`compliance.py` rebuilds the seven receipt keys per person and applies each item as a change to them:
- unreported wages or self-employment income, which leaves the payroll key and lowers the carrier's income tax at the tax unit's marginal rate;
- an on-books scale;
- an addition to SPM resources.

It then writes r, the group's share after the item over its share with row 2 at the variant's on-books case. Four ratios are written for each line and allocation, with a 160-replicate SE of r (the calibration adds no replicate spread):
- r, this lane's rule: CBO's weights fixed, so the item moves shares inside CBO's income groups;
- `r_raw`: raw shares, the proportional rule;
- `r_cal` and `r_cal_raw`: the same with the group's part of the flag-based change multiplied by c.

`price.cjs` loads the adopted package unchanged and prices the result. Each line's group amount on the reference incidence rule moves by (ratio − 1) times that amount, expanded to every executed rule with the package's `expand()` and applied with the engine's `applyCorrections` on `modelFor(row2_case, method)`. Costs come from `evaluateFull` at all 64 specifications, both methods averaged. Row 2 itself is priced on the package's own stacks: `alone`, `low` and `high`.

## Gates (all pass)

`compliance.py`, 21 gates [DATA: `derived/gates.json`]:
- **Sources and documentation:** the 11 sources are the pinned files; the IRS Tables 5 and 2, Alm & Erard's tables and Tamborini & Villarreal's tables parse to the expected values; the compliance-gap slopes, the on-books shares and the ASEC industry codes match their sources.
- **CPS frame:** the CPS zip is the pinned file, and its extra columns align with the frame.
- **Keys:** 14 receipt lines sit on seven keys, and the keys equal the account's; raw shares equal model.json (1e-9); CBO's gradient reproduces the benchmark lane (8.3e-16); row 2 reproduces the CPS lane's `origin|<case>|audit_rules_alone` to below 1e-6bn.
- **Evidence checks:** the informal mapping's share (0.401) matches Alm & Erard's (0.393); the self-employment ratios check.
- **Calibration:** its factors lie within 0.71–1.21, and it reproduces the package's row 2 to 0.86% line by line.
- **Items:** the base is row 2's scale, and each item touches only its keys.
- **Quotes:** all 43 are found in the cached texts [DATA: `derived/quotes.csv`].

`price.cjs`, 6 gates [DATA: `derived/pricing.json`]:
- the package reproduces the band, $321.819357 / $387.370055bn, and the probe's replica equals `evaluateFull`;
- the 64 specifications hold 32 distinct costs, with 48 = 52 and 11 = 15 as the ends;
- the stacks are the CPS lane's cache and models rebuild;
- items.json was built for the package's methods;
- the edits hold national totals;
- the calibrated route reproduces row 2 within 2% (0.5–0.6% realized).

## Files

- **Scripts:** `acquire.py` (fetch and pin), `compliance.py` (keys, items, ratios, calibration), `price.cjs` (pricing).
- **Outputs** in `derived/`:
  - `items.json` (ratios and meta: sources, input hashes, parameters);
  - `item_ratios.csv`, `calibration.csv`, `pricing.csv`, `pricing_lines.csv`, `pricing.json`;
  - `evidence.csv`, `item1_off_books_check.csv`, `industry_map.csv`, `quotes.csv`, `gates.json`.
- **Cache** (ignored): `_cache/sources/` holds 11 sources with `manifest.json`; `_cache/cps25_frame.parquet` is the frame loader's cache.
- **Read-only inputs**, hashed in `items.json` `meta.inputs`:
  - CPS ASEC 2025 `gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip` (sha256 318845a2b5e0), `assumption_explorer_2026_09_21/derived/model.json`;
  - `external_benchmarks_2026_09_24` (frame, CBO arm, translation);
  - `cps_imputation_keys_2026_09_23/_cache/onbooks_lane_line_deltas.json`;
  - `compliance_gap_2026_09_24/derived/{edges_by_industry,uncovered_summary_by_cell}.csv`;
  - `onbooks_share_2026_09_23/derived/onbooks_split.csv`;
  - the package `main_case_long_run_2026_09_27/package.cjs` and its summary.
- **Skipped, with reasons:**
  - The case's fill-in methods were not rebuilt per person (seeded hot decks, and the result would be a new stack), so row 2 calibrates to them.
  - SIPP-linked studies: one search found only general SIPP–DER earnings-validation papers, with no nativity or status split. The CPS–IRS match (Imboden, Voorheis & Weber) is used as a level check instead.
  - Villarreal & Tamborini 2026: abstract only; no open full text.
  - IRS NRP microdata: not public, so Pub 1415 aggregates are used.
  - Dollars from Tamborini & Villarreal: the paper gives rates only.
  - Over-withholding: no source found.
- Nothing outside this directory was edited.

## Reproduce

```sh
L=infra/immigration-fiscal/payroll_compliance_2026_09_28
uv run --no-project python3 scripts/rerun_lane.py $L \
  "uv run --no-project python3 {lane}/acquire.py" \
  "uv run --no-project python3 {lane}/compliance.py" \
  "node {lane}/price.cjs"
```

`acquire.py` runs offline once `_cache/sources/` holds the pinned files. `compliance.py` takes about 65 s and `price.cjs` under 1 s.

## Log

- Stub written before reading the inputs.
- Item 1, first pass [DATA: `main_case_2026_09_24/derived/stack_line_deltas.json` via the adopted package;
  `dataset_integrity_2026_09_23/cps_status_keys.py`; `onbooks_share_2026_09_23/RESULT.md`;
  `cps_imputation_keys_2026_09_23/RESULT.md` steps 5d–5e]: the adopted case does not assume full compliance
  for the group's imputed unauthorized. The tax-records stack (`row4+status_state_aware|central|<method>`)
  contains the audit's row 2, which scales each imputed-unauthorized Latin-American-born person's wages
  (capped and uncapped), self-employment key, FICA-worker flag, federal and state liabilities and ACTC to an
  on-books share: 0.526 Mexico-born, 0.550 other Latin-American-born (the on-books lane's central, range
  0.415–0.635 / 0.401–0.683). It acts on all six lines in the brief and also on `corporate_labor` (keyed by
  wages). With the audit's rules alone the central stack moves, shared/personal: employee OASDI −4.30/−4.65,
  employer OASDI −4.33/−4.69, employee HI −1.28/−1.39, employer HI −1.14/−1.24, self-employment −0.93/−1.00,
  other contributions −0.99/−1.05, federal income tax −8.36/−8.94 (before CBO's gradient), state −2.12/−2.27
  ($bn; these include row 4 and the state-aware flag). Nothing in the case adjusts authorized or US-born
  members' compliance, nor other residents'.
- Sources pinned by `acquire.py` (sha256 in `_cache/sources/manifest.json`; offline on rerun): IRS Pub 1415
  (TY2014–16 tax gap), Alm & Erard (Tulane WP 1517, over http because the https certificate had expired), SSA
  Actuarial Note 151 and the OIG edit-routine audit (Wayback `id_` captures; ssa.gov refuses scripts), OIG
  A-03-15-50058 and 022401 (suspense file), the CPS ASEC 2025 technical documentation and dictionary, Tamborini &
  Villarreal (Demography 2025, PMC11969445: CPS ASEC 2011–2020 matched to SSA's Detailed Earnings Records) and the
  Europe PMC record of Villarreal & Tamborini (Demography 2026, abstract only).
- First read of the matched study [SOURCE: `_cache/sources/tv2025_pmc.txt`, Tables 4–6]: among men with
  self-employment in the CPS, Hispanic men are 8.7–12.0 points less likely than White men to have any Schedule SE
  record (all models significant); immigrant status adds nothing. In the other direction, tax records show more
  self-employment than the CPS for Mexican immigrants (+3.7 points over native Whites, against +0.8 in the CPS).
  The unauthorized are excluded (no SSN match). The two effects run opposite ways and the paper gives no dollars.
- The combined item's low- and high-cost ends now move row 2's on-books case with the other items: one SSA count sets both the
  Latin-American-born shares and the other-origin share. Its ends are priced on the package's low and high stacks, and a
  second pair holds row 2 central.
- Row 2 by this lane's rule on the paper flag overstated the package's own row 2 (receipts 13.72 against 12.77 at
  48; federal income tax 4.70 against 3.35). A split of the paper-flag effect into the group's own part and others'
  part [CALCULATION: scratch probe, then `compliance.py` calibration] showed the gap is the group's own part: the
  case's flag, weights and re-imputed keys carry less income-tax liability on flagged group members. The items are
  now calibrated to the case's basis (c per line), and the calibration reproduces the package's row 2 and carries
  over to its low and high shares.
- The proportional rule (the package's way of carrying a stack through CBO's re-key) and this lane's
  within-group rule differ most for self-employment (+1.23 against +0.48 at 48). CBO's shares come from tax
  records, so the within-group rule is the headline and the proportional rule the sensitivity. Under it, row 2 itself is
  $0.81bn smaller.
- Added the CPS–IRS matched level check (Imboden, Voorheis & Weber 2022, pinned) and quote checks for the
  ASEC weighting, tax-model items and CBO's data source.
- Two runs through `scripts/rerun_lane.py` (acquire, compliance, price): exit 0 and IDENTICAL, 16/16 files each time.
