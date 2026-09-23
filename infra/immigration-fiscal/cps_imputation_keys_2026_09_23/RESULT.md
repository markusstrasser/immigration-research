claude-opus-5-5[1m]

# CPS ASEC imputation keys

**Verdict:** The CPS ASEC fill-ins give the Mexican-origin union too much taxable income, so the
account understates the union's net cost by about $9–14bn a year. Across eight corrections the
range is $5–17bn. The adopted $203.2–249.6bn becomes about $212–263bn. Both groups are imputed
at the same rate: 18.1% of union adults and 18.2% of other adults are whole-supplement
nonrespondents. The union's imputed values, however, drift toward the pooled donors. In
whole-supplement records, union wage imputations keep only 9% of the union's within-cell wage gap.
Imputed Social Security, pensions and interest drift up 19–66 log points more than other
residents' do. The two corrections the brief asks for move the adopted band as follows:

- Dropping imputed items and reweighting (a): +$13.3 / +16.6bn (SE $9.5 / 9.0bn).
- A union-matched hot deck (b): +$8.8 / +11.2bn (SE $6.7 / 6.3bn, seed variance included).
- The same hot deck net of its own procedure drift: +$13.4 / +13.6bn (SE $4.1 / 4.2bn). A
  pooled-donor control puts that drift at −$4.1 / −1.9bn (not significant).

Every correction raises the cost. Lower federal income tax does most of it: in these three
corrections the union's federal income tax falls by $7–13bn. Smaller Social Security benefits
offset part of that, by $3–7bn.

The documentation does not settle whether Hispanic origin is a match variable. It names Hispanic
origin only for the health-insurance hot decks. For Social Security it names race and not
Hispanic origin or nativity. For earnings and whole-supplement records it names no variables
[UNVERIFIED].

In the distribution lane only the total moves. Its fiscal cost rises from $227.9bn to
$237.9–242.8bn. Re-ranking other residents moves no quintile by more than $0.2bn.

The dataset audit's tax-compliance re-key (`dataset_integrity_2026_09_23/cps.md` row 1) acts on
the same seven keys. Do not add the two results. On one frame, at the audit's 44% on-books share,
the hot deck and the audit together give +$17.2 / +19.8bn. That is $3.6–3.7bn less than their sum.
The reason is overlap: 65% of this lane's change in union federal-tax dollars, and 76% of its wage
change, falls on people the status lane classes as unauthorized. The audit already counts those
people's taxes at 44%. Step 5c gives the combination key by key.

The one public-data check outside both corrections links ASEC records to the March basic
interview's weekly earnings. With n = 98 union records it is too weak to confirm or refute the
drift. This is a proposal. The adopted band stands until the operator adopts a change.
[CALCULATION: `derived/main_case_translation.csv`, `derived/component_deltas.csv`,
`derived/hotdeck_seed_spread.csv`, `derived/match_bias.csv`, `derived/distribution_check.csv`,
`derived/status_combination_by_key.csv`, `derived/weekly_validation.csv`]

Model self-report: `claude-opus-5-5[1m]`. Date: 2026-09-23. Brief: `BRIEF.md`. Not committed
(the lead commits).

## Step 1: allocation flags and the documented match variables

Every CPS item the account uses carries an allocation flag in the 2025 file. The dictionary
explains the value-flag levels. "Levels 1-3 indicate imputations use of income range responses and
4-8 indicate imputations without range responses. Within each group, lower numbers indicate more
match variables (and better matches)." And: "In levels 1-3, non-respondents are matched to
respondents with values in the range bin they indicated. Full record imputation indicates that an
individual did not provide sufficient income information and all income recipiency and value
variables were imputed." The last three levels are "7 = Level 104 statistical match (age, sex)",
"8 = Level 105 statistical match (all donors can match to all recipients)" and "9 = FL_665 ≠ 1
(full record impute)". The variables at levels 1–6 are not named [SOURCE: `_cache/cpsmar25.txt`,
lines 4249–4282, I_ANNVAL; `derived/flag_semantics.csv` quotes the other flag families].

| Item | Flags on the 2025 file | Documented match variables | Hispanic origin or nativity documented as a match variable? |
|---|---|---|---|
| Wages, self-employment | I_WORKYN, I_ERNYN, I_ERNVAL (longest job), I_WSYN, I_WSVAL, I_SEYN, I_SEVAL, I_FRMYN, I_FRMVAL | Range bin at levels 1–3; age and sex at level 104. The 2019 overhaul skipped earnings: "For all income types, except wage and salary earnings and self-employment earnings, the imputation system was overhauled" (Rothbaum 2019, p. 3). No list found. | [UNVERIFIED] |
| Whole supplement (FL_665 ≠ 1) | FL_665; value flags = 9 | "all income items are imputed together by matching to another individual using characteristics drawn largely from responses to the basic CPS questionnaire" (Rothbaum 2019, p. 6). No list. | [UNVERIFIED] |
| Social Security | I_SSYN, I_SSVAL (composite) | New model: "age, household income, gender, relationship to household head, reason not working, marital status, disability status, transfer income status, presence of children, labor force status of spouse, education, reason for receipt of social security, race, and earnings". Old model: "age, gender, marital status, race education, worker status, and pension type" (Rothbaum 2019, p. 5). | **No**: race is listed; Hispanic origin and nativity are not |
| Dividends, rent | I_DIVYN, I_DIVVAL, I_RNTYN, I_RNTVAL | New dividends value model: Age; Presence of Child; Retirement Interest; Money Market Interest; Education; Savings Interest; Marital Status; Checking Interest; Relation to Householder. The rent models add region, earnings, dividends and household income. The redesign dropped race from both (Rothbaum 2019 PAA slides 13–14). | **No** |
| Interest, SSI, public assistance, unemployment, veterans, workers' comp, pensions and retirement, survivor, disability, other income | I_INTYN, I_INTVAL, I_SSIYN, I_SSIVAL, I_PAWYN, I_PAWVAL, I_PAWTYP, I_PAWMO, I_UCYN, I_UCVAL, I_VETYN, I_VETVAL, I_VETTYP, I_VETQVA, I_WCYN, I_WCVAL, I_WCTYP, I_PEN*, I_DST*, I_ANN*, I_SUR*, I_DIS*, I_CSP*, I_ED*, I_FIN*, I_OIVAL, I_CAP* | "imputation for each income type in this module was updated to include more variables and more match levels"; to choose variables "we used a random forest technique" (p. 4). No lists. | [UNVERIFIED] |
| SNAP, housing, school lunch, energy | I_HFOODS, I_HFDVAL, I_HFOODM, I_HFOODN; I_HPUBLI, I_HLOREN; I_HFLUNC, I_HFLUNN; I_HENGAS, I_HENGVA | "the probability of benefit receipt should be the same for respondents and non-respondents, conditional on the characteristics in the hot deck models" (p. 6). No list. | [UNVERIFIED] |
| WIC | WICYNA | none found | [UNVERIFIED] |
| Medicare, Medicaid coverage | I_MCARE, I_MCAID (1 hot deck, 2 logical, 3 whole unit) | Census authors on the health-insurance processing: "These characteristics are included in health insurance hotdecks"; the characteristics are "age, marital status, sex, race, and Hispanic origin", "which through their use in hotdecks, could have affected health insurance estimates", and income (Berchick and Jackson 2022). | **Hispanic origin: yes**, in the authors' description; no specification table. Nativity not named |
| EITC and tax inputs | none: FEDTAX_BC, FEDTAX_AC, EIT_CRED, ACTC_CRD, STATETAX_A and AGI come from the Census tax model applied to the unit's reported and imputed incomes | inherit the income imputations | — |
| SPM resources | built from the incomes, noncash values, WICYNA, I_MOOP, I_CHCAREVAL | inherit | — |
| Union definition | PXNATVTY, PXMNTVTY, PXFNTVTY, PXHSPNON, PRCITFLG | 0.6–3.8% of union members allocated (step 2) | — |

Sources: Rothbaum (2019), "Processing Changes to Income in the CPS ASEC", SEHSD Working Paper
2019-18, and his PAA 2019 slides, "Changes to Income Processing in the CPS ASEC"; Berchick and
Jackson (2022), *Medical Care Research and Review* 79(2): 308–316 (PMC10232008); Census Technical
Paper 77 (2019), p. 21: "missing supplement items are assigned values based on hot deck
imputation, a method in which each missing value is replaced with an observed response from a
'similar' unit." [SOURCE: `_cache/docs/sehsd-wp2019-18.txt`, `sehsd-wp2019-bb.txt`,
`pmc10232008_oai.xml`, `tp77.txt`; working notes in `_cache/docs/MATCH_VARIABLES.md`] The monthly
basic CPS hot decks that TP77 lists (pp. 133–134) use race but not Hispanic origin. They fill
basic-survey items, not ASEC income.

The documentation cannot tell whether the earnings or whole-supplement hot decks use Hispanic
origin. Steps 3 and 6 measure what matters: whether the imputed values track group membership. For
wages, Social Security and property income they do not.

## Gate (step 0): the account's keys and totals reproduce

`gate.py` rebuilds every CPS ASEC key the complete account uses. It works from the pinned zip (SHA
`318845a2…`) under all 161 weights and matches the producers' exports [CALCULATION:
`derived/gate_keys.csv`, `derived/gate_totals.csv`]:

- 70 key shares (30 receipt, 40 CPS-based spending) equal the published shares to a relative
  1.5e-14. The 30 receipt-key SEs equal the published SEs to 1e-6.
- Union receipts, `cbo_collective`: $517.100bn personal / $545.119bn shared (published 517.100 /
  545.119). Receipts that respond at 1 in the main case: $424.52bn / $444.81bn.
- Union spending, preferred keys: $1,017.925bn / $1,023.882bn (published). Household transfers:
  $364.27bn / $374.74bn.
- Every receipt and spending line of the explorer model that `main_case_2026_09_23` evaluates
  equals the rebuilt line to 5e-10 bn.
- `main_case_translate.js` reproduces the published adopted bands with zero changes, to 1e-4 bn
  in all three profiles: $203.207–249.640bn, $158.881–212.563bn and $307.899–340.972bn.

## Step 2: shares imputed, union against other residents

Weighted with the ASEC weight; SE of the difference from the 160 replicates. "Dollars" is the
share of the item's weighted dollars carried by imputed values [CALCULATION: `flags.py` →
`derived/imputed_shares.csv`].

| Item | Measure | Union % | Other % | Union − other, pts (SE) |
|---|---|---:|---:|---:|
| Whole supplement imputed (FL_665 ≠ 1) | persons 15+ | 18.1 | 18.2 | −0.2 (0.8) |
| Wage and salary | dollars | 42.5 | 38.3 | +4.1 (1.2) |
| of which whole supplement | dollars | 20.0 | 17.9 | +2.0 (1.1) |
| Longest-job earnings, range answer (levels 1–3) | dollars | 18.3 | 15.6 | +2.7 (0.8) |
| Longest-job earnings, no range (levels 101–103) | dollars | 4.2 | 5.0 | −0.8 (0.4) |
| Longest-job earnings, age-sex or pooled (levels 104–105) | dollars | 0.0 | 0.0 | 0.0 |
| Self-employment | dollars | 56.8 | 51.0 | +5.8 (3.6) |
| Interest / dividends / rent | dollars | 86.1 / 73.2 / 48.7 | 82.8 / 72.0 / 47.7 | +3.2 / +1.2 / +1.0 |
| Pensions, retirement distributions, annuities | dollars | 58.5 | 53.3 | +5.2 (4.0) |
| Social Security | dollars | 41.8 | 43.6 | −1.8 (2.1) |
| SSI / public assistance | dollars | 36.3 / 33.9 | 37.2 / 42.4 | −0.9 / −8.6 (7.5) |
| Unemployment / veterans / workers' comp | dollars | 46.6 / 37.7 / 34.8 | 41.6 / 40.1 / 37.9 | +5.0 / −2.3 / −3.2 |
| Medicare / Medicaid coverage, donor (flags 1, 3) | persons | 23.0 / 23.3 | 23.4 / 23.5 | −0.3 / −0.3 |
| SNAP | persons / dollars | 22.5 / 26.7 | 22.7 / 30.8 | −0.2 / −4.1 (3.8) |
| Housing (public, reduced rent) | persons / dollars | 10.2 / 30.5 | 7.5 / 17.6 | +2.6 / +12.9 (7.6) |
| School lunch / energy | persons | 10.2 / 24.4 | 7.1 / 24.9 | +3.0 / −0.5 |
| WIC | persons / unit dollars | 19.5 / 15.4 | 19.4 / 21.7 | +0.1 / −6.3 (4.1) |
| Tax unit with material imputation (5% rule) | federal liability dollars | 57.2 | 59.4 | −2.2 (2.0) |
| same | refundable credit dollars | 45.5 | 50.2 | −4.7 (2.1) |
| SPM resources with an imputed input | dollars | 70.4 | 70.9 | −0.5 (1.1) |
| Union definition: own birthplace / mother's / father's / Hispanic origin / citizenship allocated | persons | 2.8 / 3.4 / 3.8 / 0.6 / 3.5 | 2.2 / 2.8 / 2.9 / 0.9 / 1.2 | ≤ +2.3 |

The two groups are imputed at nearly the same rates. The union's whole-supplement rate matches
other residents' (18.1% against 18.2%), and most item rates differ by a few points. The difference
lies in what the imputed records carry. For the union, 20.0% of wage dollars come from
whole-supplement records, which are 18.1% of its adults; for others, 17.9% of dollars come from
18.2% of adults. Property income shows the same pattern more strongly. Union whole-supplement
records carry 32.5% of the union's dividend dollars and 30.7% of its interest dollars, against
15.5% and 16.7% for others [DATA: `imputed_shares.csv`, `dollars_whole_supplement_only`]. The
union definition itself is little affected: birthplace, parents' birthplace and Hispanic origin
are edited or allocated for 0.6–3.8% of union members. The 2000 census allocated 68% for
institutional men (ladder 196).

"Material imputation" for the Census tax-model and SPM fields is this lane's rule
(`common.material_status`). A return or SPM unit counts as imputed when an adult's whole
supplement or work status was imputed, or when imputed dollars reach 5% of the unit's gross income.
The strict alternative, any flag, marks 61% of union and 74% of other persons. Interest drives it:
interest is imputed for 54% of other adults and 38% of union adults. Step 4a runs both
alternatives.

## Step 3: match-bias test

The test works within cells of basic-CPS match variables: sex × 6 age groups × 4 education
groups × race (white, Black, other) × labor-force status (employed, unemployed, retired, disabled,
other). Within each cell it compares the union's imputed and reported means with other residents'
reported means. It covers adults 15+ and weights cells by the union's imputed weight; 95–97% of
that weight falls in usable cells. The log difference-in-differences is
ln(union imputed / union reported) − ln(other imputed / other reported). Zero means the union's
imputed values sit as far from its reporters as others' imputed values sit from theirs. A positive
value means the union's imputed values drift up toward the donor pool
[CALCULATION: `matchbias.py` → `derived/match_bias.csv`].

| Item, per adult | Imputed set | Union reported − other reported, $ | Union imputed − other reported, $ | Share of the gap retained | Log DiD (SE) |
|---|---|---:|---:|---:|---:|
| Wage and salary | whole supplement | −6,330 | −577 | 0.09 | **+0.139 (0.046)** |
| Wage and salary | item level (mostly range answers) | −9,316 | −6,229 | 0.67 | +0.028 (0.038) |
| Wage and salary | all imputed | −7,643 | −2,804 | 0.37 | +0.082 (0.034) |
| Social Security | all imputed | −679 | +317 | < 0 | **+0.189 (0.058)** |
| Pensions and retirement | all imputed | −388 | +800 | < 0 | +0.546 (0.180) |
| Interest | all imputed | −615 | +1,103 | < 0 | +0.661 (0.183) |
| Federal liability, per SPM member | material 5% | −2,209 | −1,498 | 0.68 | +0.102 (0.066) |
| State liability, per SPM member | material 5% | −650 | −514 | 0.79 | +0.098 (0.068) |
| Refundable credits, per SPM member | material 5% | +129 | +110 | 0.85 | +0.043 (0.077) |
| SPM resources per member | any input | −7,062 | −6,740 | 0.95 | −0.029 (0.026) |
| SNAP per member | household flags | +8 | +38 | — | −0.098 (0.151) |

Wages and Social Security show match bias. For whole-supplement nonrespondents, the union's
imputed wages retain 9% of the gap between its reporters and other residents in the same cell.
Their log drift is 14 points (SE 4.6) larger than others'. Item nonrespondents who gave a range
answer are held inside their own earnings bracket; their drift is small and insignificant (2.8
points, SE 3.8). Social Security, pensions and interest drift up by 19, 55 and 66 log points. For
the Census tax fields the drift is 10 points (SE 6.6–6.8), about 1.5 SE. SPM resources show none
(−3 points, SE 2.6), because taxes and transfers inside the SPM measure offset each other. Two
facts from step 1 fit this pattern. The redesign re-specified the models "For all income types,
except wage and salary earnings and self-employment earnings". Whole-supplement records are
matched on "characteristics drawn largely from responses to the basic CPS questionnaire", and no
list is given. Neither passage says whether Hispanic origin or nativity is among the variables. The
Social Security model lists race and neither of the two [SOURCE: `_cache/docs/sehsd-wp2019-18.txt`,
pp. 3, 5, 6].

## Step 4a: drop imputed items and reweight reported records

Imputed values get weight 0. Reported records in each age (9) × sex × education (5) ×
nativity × union cell are reweighted by the cell's total weight over its reported weight, under
each replicate weight. A cell without reported records collapses to age (6) × sex × education (4),
then to age (3) × sex, then to nativity × union. This affected 1–56 cells per key in the main
specification. Variants add current labor-force status, or use the 1% and any-flag rules for the
derived fields [CALCULATION: `ipw.py` → `derived/ipw_keys.csv`].

Change in the union's key share, relative, main specification (brief cells, material 5%):

| Key | Weight dropped | Personal | Shared | Main-case lines it feeds |
|---|---:|---:|---:|---|
| wage (payroll, HI, corporate labor) | 26% | −2.9% (1.3) | −2.8% (1.4) | employee/employer OASDI, HI |
| federal liability | 53% | **−10.5% (3.7)** | −8.3% (3.5) | federal income tax $128–138bn |
| state liability | 53% | −8.1% (3.6) | −7.0% (3.4) | state income tax $27–29bn |
| consumption (SPM resources) | 68% | +1.3% (1.6) | +1.3% (1.6) | sales, excise, customs, transfers $97bn |
| Social Security | 22% | **−10.0% (2.1)** | −10.5% (2.0) | Social Security $60–63bn |
| refundable credits | 53% | +0.9% (2.7) | +1.1% (2.3) | EITC and ACTC $52–55bn |
| SNAP / WIC | 23% / 22% | +5.1% (3.0) / +6.2% (3.2) | same | $14.3bn / $5.1bn |
| cash assistance | 18% | +9.4% (10.8) | +7.9% (9.7) | income security services + family assistance $38–40bn |
| capital (response 0) | 45% | −41.6% (7.4) | −48.3% (7.1) | corporate and property incidence only |

Under the derived-field alternatives, federal liability moves −7.6% (1% rule) or −9.3% (any flag),
and refundable credits −2.5% or −8.4%. Adding labor-force status to the cells changes little:
wage −2.8%, federal −9.6%, Social Security −9.9%.

The components follow the main case's formula. Direct receipts respond at 1, transfers and
income-security services at 1, delayed services at 0, and the capital-incidence receipts at 0.
Figures are $bn a year; a positive net means a higher cost:

| Specification | Direct receipts | Transfers | Income-security services | Net cost change (SE), personal / shared |
|---|---:|---:|---:|---:|
| brief cells, 5% rule | −18.0 / −14.6 | −4.0 / −3.7 | +2.6 / +2.3 | **+16.6 (9.0) / +13.3 (9.5)** |
| plus labor force | −17.6 / −16.9 | −4.8 / −5.0 | +3.8 / +2.7 | +16.7 (9.0) / +14.6 (9.2) |
| derived fields, 1% rule | −13.2 / −12.7 | −5.8 / −6.3 | +2.6 / +2.3 | +10.0 (9.0) / +8.8 (9.9) |
| derived fields, any flag | −15.2 / −16.1 | −8.8 / −10.5 | +2.6 / +2.3 | +8.9 (10.8) / +7.9 (11.5) |

[CALCULATION: `translate.py` → `derived/component_deltas.csv`, profile `cbo_lag`]

## Step 4b: re-impute from union-matched donors

`hotdeck.py` is a sequential cell hot deck. Each imputed item gets a reported donor drawn with
probability proportional to the ASEC weight from the recipient's cell. Union membership and
nativity are always held fixed. The other match variables are basic-CPS items, which exist even
for whole-supplement nonrespondents. The cell-collapse rule drops variables in the order of
`LEVELS` until a cell holds at least 5 donors (`MIN_DONORS`), then accepts a base cell with any
donor, then union alone, then all donors:

| Level | Variables beside union and nativity |
|---:|---|
| 0 | age (9), sex, education (5), race (3), labor force (5), class of worker, occupation, married, relationship, region |
| 1 | age (9), sex, education (5), race, labor force, class of worker, married |
| 2 | age (6), sex, education (4), race, labor force, class of worker |
| 3 | age (6), sex, education (4), labor force |
| 4 | age (3), sex, labor force |
| 5 | age (3), sex |
| 6 | none (union × nativity) |

Details:

- Whole-supplement nonrespondents take all income blocks from one donor. Donors are adults with
  every income block reported except interest, dividends, rent and other income.
- Item nonrespondents are re-imputed block by block. A recipient who reported receipt draws only
  from reported recipients. A longest-job earnings value imputed from a range answer draws only
  from donors in the same range bin and earnings source.
- For non-earnings items, the item-level cells also match on household income (quintile of the
  household's total income) and earnings (7 groups). This follows the documented Social Security
  and rent models, which use both.
- Coverage (flags 1 and 3) is re-imputed from reported persons.
- Household noncash benefits are re-imputed per SPM unit. The unit cells use the head's union
  status and nativity, unit size, children, earners, head's age and education, region and tenure.
- Federal tax, EITC and ACTC change by the difference of `taxcalc.py`, a simplified 2024
  calculator, evaluated on the new and published incomes. State tax changes by each state's
  marginal rate on AGI, and payroll tax follows the statute. SPM resources move by the change in
  cash and noncash income less the change in taxes.

Seeds are 20260923–20260927 in the main specification and 20260923–20260925 in `all_items`. The
main specification leaves item-level property, retirement and other income at the Census values;
`all_items` re-imputes them too. The mean collapse level for whole-supplement recipients is 0.85.
No recipient in any block fell back past the union × nativity cell. Veterans' benefits went
furthest: some recipients used that cell with fewer than 5 donors [DATA:
`derived/hotdeck_diagnostics.csv`].

The same procedure with pooled donors, dropping union and nativity from the cells, is the
control. It measures how far this lane's hot deck drifts from the Census values without any
union matching.

**Tax calculator check.** Before its use as a difference operator, the calculator was compared
with the Census tax model on published incomes [CALCULATION: `taxcalc.py` →
`derived/taxcalc_validation.csv`]:

| Field | Weighted correlation | Model total | Census total | Returns within $100 |
|---|---:|---:|---:|---:|
| federal tax before credits | 0.990 | $2,123bn | $1,988bn | 78% |
| EITC | 0.977 | $41.0bn | $43.3bn | 98.6% |
| ACTC | 0.990 | $20.6bn | $21.9bn | 98.5% |

Change in the union's key share, relative, main specification, personal allocation, mean of 5
seeds (replicate SE) [CALCULATION: `run_hotdeck.py` → `derived/hotdeck_keys.csv`]:

| Key | Union-matched vs published | Pooled control vs published | Match effect (matched / pooled) | SD of one seed |
|---|---:|---:|---:|---:|
| wage | −2.0% (0.9) | +0.2% | −2.2% (0.6) | 0.9% |
| federal liability | **−6.4% (2.5)** | +0.8% | **−7.1% (1.8)** | 1.7% |
| state liability | −3.9% (1.6) | +0.1% | −4.0% (1.1) | 1.8% |
| consumption (SPM resources) | −2.7% (0.6) | +0.4% | −3.1% (0.4) | 0.5% |
| Social Security | **−6.0% (1.6)** | +1.1% | **−6.9% (0.9)** | 0.6% |
| self-employment payroll | −16.8% (3.4) | −8.0% | −9.5% (2.3) | 1.3% |
| refundable credits | +1.0% (1.2) | +0.5% | +0.5% (0.7) | 0.3% |
| SNAP / WIC | +2.9% (3.0) / +3.9% (3.1) | +5.7% / +4.2% | −2.6% / −0.3% | 1.9% / 3.8% |
| housing support | −11.5% (4.8) | −2.9% | −8.8% (3.3) | 3.6% |
| cash assistance | −2.5% (7.0) | −9.8% | +8.1% (4.7) | 6.2% |
| Medicare | −0.4% (0.9) | +1.8% | −2.2% (0.5) | 0.5% |
| Medicaid coverage (not a preferred key) | +2.8% (0.9) | −2.9% | +5.8% (0.5) | 0.8% |
| capital (response 0) | −15.3% (3.5) | +2.9% | −17.7% (3.6) | 1.7% |

The union-matched hot deck agrees in sign with step 4a on wages, federal and state liability and
Social Security, at 48–70% of its size. The pooled control stays within 1.1% of the
published keys for wages, federal and state liability, consumption and Social Security. Where the
account's receipts are concentrated, this lane's hot deck therefore reproduces the Census values
closely when it does not match on union. The control drifts more on self-employment payroll
(−8%), capital (+3%), Medicare (+1.8%) and the small transfer keys (SNAP +5.7%, cash assistance
−9.8%).

Components, $bn a year. The total SE combines the replicate SE with the between-seed variance by
Rubin's rule, T = W + (1 + 1/M)B [CALCULATION: `derived/hotdeck_seed_spread.csv`]:

| Specification | Direct receipts | Transfers | Income-security services | Net cost change (total SE), personal / shared |
|---|---:|---:|---:|---:|
| union-matched hot deck | −15.5 / −13.8 | −3.6 / −3.8 | −0.7 / −1.2 | **+11.2 (6.3) / +8.8 (6.7)** |
| net of the pooled control | −16.3 / −15.9 | −5.0 / −4.9 | +2.2 / +2.4 | **+13.6 (4.2) / +13.4 (4.1)** |
| all items re-imputed | −12.8 / −10.1 | −4.7 / −4.4 | −0.2 / −0.7 | +7.8 (6.7) / +5.0 (7.6) |
| all items, net of control | −19.1 / −17.4 | −5.3 / −5.0 | +3.3 / +2.8 | +17.1 (6.5) / +15.3 (6.8) |
| control: pooled donors (replicate SE) | +0.9 / +2.3 | +1.6 / +1.5 | −2.7 / −3.4 | −1.9 (5.1) / −4.1 (4.8) |

A single seed's net change has an SD of $3.2–3.9bn in the matched hot deck and $1.1–1.3bn in the
drift-netted version. Matched and pooled runs share their random streams, so their ratio is
steadier than either run.

Line-level changes, personal allocation, $bn [CALCULATION: `derived/line_deltas.csv`]:

| Line | (a) reweight | (b) matched | (b) net of control |
|---|---:|---:|---:|
| federal income tax | −13.4 | −8.1 | −9.1 |
| state and local income tax | −2.2 | −1.1 | −1.1 |
| employee + employer OASDI and HI | −3.5 | −2.1 | −2.1 |
| self-employment OASDI and HI | −0.1 | −1.5 | −0.8 |
| general sales + excise (consumption key) | +1.0 | −2.1 | −2.4 |
| Social Security benefits | −6.0 | −3.6 | −4.2 |
| income-security services + family assistance (cash key) | +3.6 | −1.0 | +3.1 |
| Medicare | +0.1 | −0.2 | −1.2 |
| SNAP and refundable credits | +1.2 | +1.0 | −0.1 |

Housing subsidies (−$0.3 to −0.9bn) and the capital-incidence receipts are subsidy and incidence
lines at response 0, so they do not enter the band.

## Step 5: the adopted main case

`main_case_translate.js` shifts the explorer model's executed allocations by the line changes.
National totals are conserved because other residents' allocations move the other way. It then
recomputes the adopted bands exactly as `main_case_2026_09_23/main_case.js` does: justice by use,
uncompensated care inside $3.65–5.75bn, and general government at 0.59–0.84. The low end is the
shared allocation and the high end the personal one [CALCULATION: `derived/main_case_translation.csv`].

| Method | Adopted band, $bn | Change, low / high | SE, low / high |
|---|---|---:|---:|
| published (adopted) | 203.2–249.6 | — | — |
| (a) reweight, brief cells | 216.5–266.2 | +13.3 / +16.6 | 9.5 / 9.0 |
| (a) plus labor-force status | 217.8–266.3 | +14.6 / +16.7 | 9.2 / 9.0 |
| (a) derived fields at 1% | 212.0–259.7 | +8.8 / +10.0 | 9.9 / 9.0 |
| (a) derived fields, any flag | 211.1–258.6 | +7.9 / +8.9 | 11.5 / 10.8 |
| **(b) union-matched hot deck** | **212.0–260.8** | **+8.8 / +11.2** | 6.7 / 6.3 |
| **(b) net of the pooled control** | **216.6–263.2** | **+13.4 / +13.6** | 4.1 / 4.2 |
| (b) all items re-imputed | 208.2–257.5 | +5.0 / +7.8 | 7.6 / 6.7 |
| (b) all items, net of control | 218.5–266.8 | +15.3 / +17.1 | 6.8 / 6.5 |
| control: pooled donors | 199.1–247.7 | −4.1 / −1.9 | 4.8 / 5.1 |

The changes are the same in the other CBO-lag profile, where other education is fixed and the
published band is $158.9–212.6bn. The lines involved respond at 1 in both. The proportional
reference ($307.9–341.0bn) differs because economic-affairs services also respond there. The
hot-deck changes are $0.5–1.3bn smaller and the reweighting changes $0.2–0.9bn larger.

Two readings of (b) bracket the central estimate. The matched run against the published values
(+$8.8 / +11.2bn) treats the control's −$1.9 to −4.1bn as noise. The matched run against the
control (+$13.4 / +13.6bn) treats it as a real difference between this hot deck and the Census
one. For Medicare that second reading over-corrects. Census documents Hispanic origin in its
health-insurance hot decks, so the control's +1.8% Medicare drift is plausibly the Census matching
itself. Using the matched-vs-published Medicare figure instead raises the drift-netted high end by
about $1.0bn [INFERENCE: Medicare line −0.24 against −1.22].

## Step 5b: the distribution lane's inputs

`distribution_check.py` imports the distribution lane's own functions (`load_cps`, `rank_frame`,
`tax_key`, `per_person`; read only). It reproduces its published quintile splits to 4e-13 bn, then
changes the inputs [CALCULATION: `derived/distribution_check.csv`]:

- **Total.** The lane divides A_mid + F_c = −$227.9bn. A_mid moves by minus the midpoint of the
  band changes. The total becomes −$237.9bn under (b) matched, −$241.4bn under (b) net of the
  control, and −$242.8bn under (a).
- **Ranking and spread.** Other residents' SPM resources and household money income change when
  their own imputed values are re-drawn from other-resident donors. Re-ranking them and
  re-spreading the CBO and ITEP group shares moves each quintile's share of the fiscal cost by at
  most $0.18bn (Q5 −141.58 → −141.40, seed SD 0.09). The CPS tax-field check key moves by at most
  $0.5bn per quintile. The part due to union matching (matched minus pooled) is at most $0.34bn.

Fiscal cost under tax-share financing (`fiscal_a`), $bn, other residents' quintiles by SPM
resources:

| | Q1 | Q2 | Q3 | Q4 | Q5 | Total |
|---|---:|---:|---:|---:|---:|---:|
| published | −6.91 | −14.57 | −24.57 | −40.29 | −141.58 | −227.92 |
| (b) matched, re-ranked, published total | −6.96 | −14.59 | −24.66 | −40.33 | −141.40 | −227.92 |
| (b) matched total | −7.21 | −15.21 | −25.65 | −42.06 | −147.79 | −237.92 |
| (b) net of control total | −7.32 | −15.44 | −26.02 | −42.68 | −149.95 | −241.40 |
| (a) total | −7.36 | −15.53 | −26.18 | −42.93 | −150.84 | −242.84 |

Under per-person financing (`fiscal_b`) each quintile carries a fifth of the new total: −$47.6bn
under (b) matched against −$45.6bn published. The correction moves no channel other than the
fiscal cost.

## Step 5c: combining with the dataset audit's status re-key

`dataset_integrity_2026_09_23/cps.md` row 1 re-keys the account's receipt keys for the Census
tax model's resident and full-compliance assumption. The audit takes the Latin-American-born
people that `status_impute_2026_09_16` classes as unauthorized: 9.54M, 4.567M of them in the
union. It zeroes their EITC. It scales their ACTC, federal and state liability, capped and uncapped
wages, self-employment payroll and FICA-worker count to an on-books share of 0.44, 0.60 or 0.75.
Those are the keys this lane corrects.

`combine_status.py` applies the audit's rules to the account's own key vectors. It does so on the
published file (the audit alone), and on top of each of this lane's corrections on the same frame.
Every result runs through the same gated main-case translation [CALCULATION:
`derived/status_combination_by_key.csv`, `status_combination_translation.csv`,
`status_combination_components.csv`, `status_combination_overlap.csv`].

Gates:

- The audit's per-key share changes reproduce on the account's keys within 0.05 points. Federal
  liability moves −5.49% in both; EITC + ACTC moves −13.60% against the audit's −13.65%.
- Self-employment is the exception: −8.2% on the account's key against −5.7% on the audit's
  `SE_VAL` vector. The audit notes its vector does not reproduce the account's key.
- Without the rules, step 4a's shares and every hot-deck seed's shares reproduce exactly.

Key by key, at 0.44 on-books, with the union-matched hot deck (b), personal allocation (the high
end of the band). The figures are changes in cost, $bn, with the whole refundable line keyed by
EITC + ACTC as adopted:

| Key (main-case lines) | Audit alone | This lane alone | Both on one frame | Interaction |
|---|---:|---:|---:|---:|
| federal liability (federal income tax) | +7.03 | +8.14 | +12.87 | −2.31 |
| state liability (state income and other personal taxes) | +1.75 | +1.07 | +2.47 | −0.35 |
| capped wages (employee and employer OASDI) | +7.11 | +1.48 | +8.14 | −0.45 |
| wages (employee and employer HI) | +2.00 | +0.62 | +2.40 | −0.21 |
| self-employment payroll | +0.73 | +1.49 | +2.12 | −0.10 |
| FICA workers (other social contributions) | +0.79 | +0.04 | +0.83 | 0.00 |
| EITC + ACTC (refundable credits) | −7.09 | +0.54 | −6.80 | −0.24 |
| keys the audit does not touch (Social Security, consumption, cash, SNAP, Medicare and others) | 0 | −2.20 | −2.20 | 0 |
| **Net** | **+12.31** | **+11.19** | **+19.84** | **−3.67** |

The shared allocation gives +11.99, +8.80, +17.23 and −3.57. The interaction is concentrated
where the two corrections hit the same people. Across the five seeds, 65% of the hot deck's change
in union federal-tax dollars falls on the audit's unauthorized, and so do 43% of the state-tax
change and 76% of the wage change. The audit already scales those people's values to the on-books
share, so only that share of this lane's change on them survives. Keys only one correction
touches add without interaction. Social Security, consumption and the transfer keys come from
this lane alone. The EITC side of refundable credits comes from the audit alone.

Combined results on the adopted main case ($203.2–249.6bn), changes in $bn, low / high. The audit's
rules alone give +12.0 / +12.3 at 0.44, +7.0 / +7.1 at 0.60 and +2.3 / +2.3 at 0.75:

| This lane's method | Alone | Both at 0.44 | Both at 0.60 | Both at 0.75 | Both at 0.44, non-PTC convention |
|---|---:|---:|---:|---:|---:|
| (a) reweight | +13.3 / +16.6 | +19.3 / +22.7 | +16.0 / +19.3 | +12.9 / +16.1 | +22.0–22.5 / +25.7–26.3 |
| (b) union-matched hot deck | +8.8 / +11.2 | **+17.2 / +19.8** | +13.2 / +15.7 | +9.5 / +11.8 | +20.1–20.7 / +22.8–23.4 |
| (b) net of the pooled control | +13.4 / +13.6 | +23.0 / +23.3 | +18.7 / +18.9 | +14.7 / +14.7 | +25.8–26.3 / +26.3–26.9 |

The replicate SEs of the combined net are 8.9–9.4 for (a), 5.2–5.4 for (b) and 3.9–4.0 for (b)
net of control. Seed variance was not recomputed for the combination; in step 4b it added $1.1–1.6bn
to the SE. The interaction grows as the on-books share falls: for (b) it is −$1.6 to −1.7bn at 0.75,
−$2.6bn at 0.60 and −$3.6 to −3.7bn at 0.44. For (a) it is larger, −$6.0 to −6.2bn at 0.44. The
reweighting drops imputed records, and the audit's unauthorized are heavily imputed.

The "non-PTC convention" applies key changes on the refundable line only to its part that is not
premium tax credits: $108.8–128.8bn of $228.8bn (`spending.md` #1). The audit's headline uses it.
On the account's keys, the audit's rules alone give +$15.4–16.0bn (personal) and +$14.9–15.5bn
(shared) under that convention. The audit reports +$15.2–15.8bn and +$16.4–17.0bn. The shared end
differs by about $1.5bn because the audit applies the person-level share change to both
allocations. The account's shared allocation instead splits each SPM unit's total equally among
its members. Many of the audit's unauthorized plausibly share units with members whose values it
does not scale [INFERENCE].

The audit's status flag rests partly on hot-decked fields. The status lane counts Social
Security, SSI, Medicare or Medicaid receipt as evidence of legal status. Coverage is imputed for
about 23% of persons, and 36–42% of Social Security and SSI dollars are imputed (step 2). Re-drawing them in the hot deck moves
0.47–0.58M union members across the status line in each seed. The net count falls from 4.567M to
4.47–4.55M unauthorized. Recomputing status this way changes the combined result by only −$0.1 to
−0.3bn.

## Every specification computed

| Step | Specifications | Output |
|---|---|---|
| 0 gate | 70 keys × 161 weights; explorer lines; adopted bands in 3 profiles | `gate_keys.csv`, `gate_totals.csv` |
| 2 shares | 60 item × measure rows, union and other, SDR SEs; material rules 5%, 1%, any flag | `imputed_shares.csv` |
| 3 match bias | sex × age (6) × education (4) × race (3) × labor force (5) cells, at least 2 records per group; 11 items × imputed sets | `match_bias.csv` |
| 4a reweight | brief cells × {5%, 1%, any flag}; plus labor force × 5%; 27 keys × 2 allocations | `ipw_keys.csv` |
| 4b hot deck | main (5 seeds) and all_items (3 seeds) × {union-matched, pooled}; 27 keys × 2 allocations | `hotdeck_keys.csv`, `hotdeck_diagnostics.csv`, `hotdeck_seed_spread.csv` |
| 5 translation | 9 methods × 3 profiles × 2 allocations; line and component changes | `main_case_translation.csv`, `component_deltas.csv`, `line_deltas.csv` |
| 5b distribution | fiscal_a and CPS tax-field key × {published, matched, pooled re-rank} × 3 totals | `distribution_check.csv` |
| 5c audit combination | audit rules at 0.44, 0.60, 0.75 × {alone, with (a), with (b), with (b) net of control}; status fixed and recomputed for (b) | `status_combination_*.csv`, `status_combination_line_deltas.json` |
| 6 weekly test | published, matched and pooled frames (5 seeds each) × {whole supplement, item} × {raw, cells} | `weekly_validation.csv`, `weekly_validation_counts.csv` |
| tax check | calculator vs Census tax model | `taxcalc_validation.csv` |

The capital key moves −14% to −48%. Capital-incidence receipts respond at 0 in every main-case
profile, so this does not move the band. It would matter to a reader who counts incidence receipts
directly: union corporate and property incidence falls by $5.8–21.1bn
[CALCULATION: `component_deltas.csv`, `incidence_receipts`].

## Step 6: the case that imputation makes no difference

The strongest version of that case:

1. **Rates are equal.** 18.1% and 18.2% of adults are whole-supplement nonrespondents, and 57%
   and 59% of federal liability dollars come from tax units with material imputation. If the hot
   deck were unbiased within its cells, equal rates would mean equal and offsetting errors. Step 3
   answers this: the rates are equal but the drift is not. Union imputed wages keep 9% of the
   union's within-cell gap, and the log drift is 14 points (3.0 SE) larger than others'.
2. **Range answers anchor most item imputations.** 18% of union wage dollars are range-bracketed
   imputations, and their drift is +2.8 points (SE 3.8). This part of the case holds. The effect
   comes from whole-supplement records and from non-earnings items.
3. **SPM resources do not drift** (−2.9 points, SE 2.6). The consumption key does not move in
   (a) (+1.3%, SE 1.6). It moves −2.7% in (b), where taxes are recomputed. The consumption-based
   lines (±$2bn) are not robust in sign.
4. **Nonresponse may not be ignorable.** Both corrections assume that, within cells, union
   nonrespondents resemble union respondents. The Census values assume they resemble all
   respondents in cells that ignore union status. If union nonrespondents earn more than union
   respondents in the same cell, for example because high earners refuse the income questions
   more often, the Census values could be closer to the truth. Validation studies linking CPS
   ASEC to Social Security earnings records report nonresponse rising in both tails of the
   earnings distribution [TRAINING-DATA: Bollinger, Hirsch, Hokayem and Ziliak 2019, *Journal of
   Political Economy*; not re-read here]. For a lower-earning group the left tail would make the
   correction larger, not smaller [INFERENCE].
5. **Precision.** Once seed variance is included, the two drift-netted hot decks are 3.2–3.3 SE
   and 2.2–2.6 SE from zero. The other six corrections are 0.7–1.9 SE. The eight corrections
   share one sample, so their agreement in sign is not independent evidence. (a) and (b) disagree
   in sign on the consumption and cash keys. They agree on federal liability, state liability,
   wages and Social Security, which carry the net change.

What would show that imputation makes no difference: union whole-supplement nonrespondents whose
true incomes, measured outside the ASEC hot deck, match their imputed values rather than their
cell's union reporters. The public data allow one such check. Outgoing-rotation workers report
usual weekly earnings in the March basic interview even when they skip the supplement. The 2025
ASEC public file blanks its copy of that item (A_GRSWK is nonzero for 45 of 15,207
earnings-eligible records). `validate_weekly.py` therefore links the March 2025 basic public file
by the dictionary's rule (PERIDNUM = HRHHID + HRHHID2 + PULINENO). 93,649 ASEC persons link, with
sex and age agreeing in 100%. The outcome is ln(annual wage) − ln(weekly earnings) for workers
with reported, non-top-coded weekly earnings [DATA: `_cache/basic/mar25pub.csv`, sha256
`c7ad5dad…`; CALCULATION: `derived/weekly_validation.csv`]:

| Frame | Imputed set | Union gap vs union reporters | Other gap | DiD, raw (SE) | DiD within cells (SE) |
|---|---|---:|---:|---:|---:|
| published | whole supplement (union n = 98, other n = 670) | +0.034 | +0.073 | −0.04 (0.11) | +0.08 (0.12) |
| published | item level (n = 83, 631) | −0.208 | −0.002 | −0.21 (0.11) | −0.08 (0.13) |
| (b) union-matched | whole supplement | −0.049 | +0.049 | −0.10 (0.12) | +0.07 (0.16) |
| control: pooled | whole supplement | −0.034 | +0.119 | −0.15 (0.14) | −0.05 (0.15) |

The test is underpowered. Its SE of 0.11–0.12 log points cannot separate zero from the +0.14 drift
of step 3. It does not confirm the mechanism, and it does not refute it. The item-level rows lean
the other way: union item-level imputations sit below union reporters relative to weekly earnings
(DiD −0.21, SE 0.11 raw; −0.08, SE 0.13 within cells). Step 3 found item-level drift near zero.
Pooling the redesigned ASEC files for 2019–2025 with their March basic files would give about 700
union whole-supplement workers and an SE near 0.04–0.05 [INFERENCE: seven files of this size].
That would separate zero from 0.14. The decisive test uses linked administrative earnings (W-2 or
SSA records) by Hispanic origin, which are restricted-use.

## Limits

- **Assumption.** Both corrections replace one missing-at-random assumption with another: within
  cells that include union status, instead of cells that do not. The data cannot test this
  without outside records (step 6).
- **Documentation.** The earnings, whole-supplement, other-income and noncash match variables are
  [UNVERIFIED]. The correction does not rest on them; it rests on the measured drift.
- **Procedure.** This lane's hot deck is not the Census one. The control's drift (−$1.9 to
  −4.1bn, SE about 5) is why two readings of (b) are reported.
- **Taxes.** Tax changes use a simplified 2024 calculator as a difference operator, with 2024
  parameters from [TRAINING-DATA: IRS Rev. Proc. 2023-34], not re-checked against the
  publication. The EITC and ACTC agreement with the Census model (98.5–98.6% of returns within
  $100) suggests the credit parameters are right. The before-credit total runs 7% above Census,
  so federal changes may be about 7% too large. State tax uses one marginal rate per state.
- **Production term.** P + F ($8.8–13.3bn in the headline cases) is not recomputed. The nest
  builds its labor input from CPS ASEC earnings (PEARNVAL), and the union wage key moves about −2%.
  A proportional move would be about $0.2–0.3bn [INFERENCE; DATA:
  `full_account_2026_09_20/derived/headline_cases.csv`, `production_nativity_nest_2026_09_22/builder.py`].
- **Health insurance.** Census documents Hispanic origin in the health-insurance hot decks. The
  drift-netted Medicare correction (−$1.2bn) is probably too large (step 5).
- **Scope.** One file (ASEC 2025, income year 2024), like the account. Medicaid coverage moves
  +2.8% to +5.8%, but the account's Medicaid line uses another key, so it is not in the band.

## Reproduce

From the repository root, in order (about 6 minutes; the hot-deck steps take 80 s each):

```sh
export OPENBLAS_NUM_THREADS=1
L=infra/immigration-fiscal/cps_imputation_keys_2026_09_23
uv run --no-project python3 $L/gate.py
uv run --no-project python3 $L/flags.py
uv run --no-project python3 $L/matchbias.py
uv run --no-project python3 $L/ipw.py
uv run --no-project python3 $L/taxcalc.py
uv run --no-project python3 $L/run_hotdeck.py
uv run --no-project python3 $L/translate.py        # runs main_case_translate.js; "all gates passed"
uv run --no-project python3 $L/distribution_check.py
uv run --no-project python3 $L/validate_weekly.py  # fetches the March 2025 basic file on first run
uv run --no-project python3 $L/combine_status.py   # reads status_impute_2026_09_16 and the audit's CSV
```

A full rerun on 2026-09-23 reproduced every file in `derived/` byte for byte, and
`combine_status.py` reproduced its own outputs.

## Did not complete

- The earnings and whole-supplement match variables. The cached documentation does not name
  them; Census's internal specifications would.
- The pooled 2019–2025 weekly-earnings test described in step 6.
- Any administrative-record validation (restricted-use).
- A check of the calculator's 2024 parameters against Rev. Proc. 2023-34.

## For the lead to check

1. `translate.py` ends with "all gates passed", and the published bands reproduce to 1e-4 bn.
2. Which figure to propose: (b) matched, +$8.8 / +11.2bn, the conservative one; (b) net of
   control, +$13.4 / +13.6bn, the most precise; or the range, +$5–17bn. The proposal is the
   operator's call. The adopted band stands until then.
3. The shared-allocation SEs (6.7 for (b), 9.5 for (a)). Only the two drift-netted hot decks are
   significant at 5% (3.2–3.3 and 2.2–2.6 SE). The others are 0.7–1.9 SE.
4. The distribution lane: only its fiscal total needs updating, by the same midpoint (−$10.0 to
   −$14.9bn).
5. The combination with `cps.md` row 1: carry the one-frame figure from step 5c, never the sum.
   With the (b) hot deck at 0.44 on-books that is +$17.2 / +19.8bn on the adopted line. Under the
   non-PTC convention it is +$20.1–23.4bn. The audit's own shared-allocation figure is about $1.5bn
   high on the account's keys.

## Revisions

- 2026-09-23: first complete version.
- 2026-09-23: step 5c added at the lead's request, combining this lane with the dataset audit's
  status re-key key by key (`combine_status.py`).
