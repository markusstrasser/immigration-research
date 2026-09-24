# CPS ASEC imputation keys

**Verdict:** The CPS ASEC fill-ins give the Mexican-origin union too much taxable income, so the
account understates the union's net cost by about $9–15bn a year. Across eight corrections the
range is $5–18bn. The adopted $203.2–249.6bn becomes about $212–264bn. Both groups are imputed
at the same rate: 18.1% of union adults and 18.2% of other adults are whole-supplement
nonrespondents. The union's imputed values, however, drift toward the pooled donors. In
whole-supplement records, union wage imputations keep only 9% of the union's within-cell wage gap.
Imputed Social Security, pensions and interest drift up 19–66 log points more than other
residents' do. The two corrections the brief asks for move the adopted band as follows:

- Dropping imputed items and reweighting (a): +$13.0 / +16.5bn (SE $9.5 / 9.0bn).
- A union-matched hot deck (b): +$9.2 / +11.4bn (SE $6.8 / 6.6bn, seed variance included).
- The same hot deck net of its own procedure drift: +$14.6 / +14.8bn (SE $4.1 / 4.2bn). A
  pooled-donor control puts that drift at −$4.9 / −2.9bn (not significant).

Every correction raises the cost. Lower federal income tax does most of it: in these three
corrections the union's federal income tax falls by $7–13bn. Smaller Social Security benefits
offset part of that, by $3–7bn.

The documentation does not settle whether Hispanic origin is a match variable. It names Hispanic
origin only for the health-insurance hot decks. For Social Security it names race and not
Hispanic origin or nativity. For earnings and whole-supplement records it names no variables
[UNVERIFIED].

In the distribution lane only the total moves. Its fiscal cost rises from $227.9bn to
$238.2–242.7bn. Re-ranking other residents moves no quintile by more than $0.2bn.

The dataset audit's tax-compliance re-key (`dataset_integrity_2026_09_23/cps.md` row 1) acts on
the same seven keys. Do not add the two results. On one frame, at the audit's 44% on-books share,
the hot deck and the audit together give +$17.6 / +20.1bn. That is $3.6–3.7bn less than their sum.
The reason is overlap: 65% of this lane's change in union federal-tax dollars, and 76% of its wage
change, falls on people the status lane classes as unauthorized. The audit already counts those
people's taxes at 44%. Step 5c gives the combination key by key. Step 5d uses the on-books lane's
modelled shares and the Treasury-measured non-PTC amount. At the central case, the audit's rules
alone give +$12.7 / +13.1bn. The hot deck adds +$6.1 / +8.2bn to that, or +$12.4 / +12.5bn net of
its control.

Step 5e found a defect in this lane's translation, fixed on 2026-09-24. Its key dictionary used the
name "medicare" for Medicare coverage, the key of the Medicare premium receipt. That value replaced
the account's MEPS key on the $1,102bn Medicare spending line, so the first figures for every
method moved that line by the wrong key. `translate.py` now maps each account key to the lane key
that measures it. The figures above use the fix; the Revisions section lists the earlier ones.
Step 5e also stacks the dataset audit's rows 3 and 4 and a state-aware status flag on the same
frames:

- Row 4, measured by reweighting the overcounted Mexico-born, saves nothing on its own: +$0.2 /
  +0.5bn (SE 0.6 / 0.7). The Mexico-born lane's proportional formula gives −$6.4 / −7.9bn. After
  row 2 the reweighting saves $1.3 / 1.5bn.
- Row 3 overlaps row 2 by $0.9 / 1.0bn, because the audit's rules leave the high-AGI key unscaled,
  and the hot deck by $1.1 / 0.1bn.
- The state-aware flag raises the union's unauthorized from 4.57M to 5.23M but adds only $0.3bn to
  row 2 at the central shares ($0.0–0.6bn across cases) and moves the hot-deck increments by less
  than $0.2bn.

The one public-data check outside both corrections links ASEC records to the March basic
interview's weekly earnings. With n = 98 union records it is too weak to confirm or refute the
drift. This is a proposal. The adopted band stands until the operator adopts a change.
[CALCULATION: `derived/main_case_translation.csv`, `derived/component_deltas.csv`,
`derived/hotdeck_seed_spread.csv`, `derived/match_bias.csv`, `derived/distribution_check.csv`,
`derived/status_combination_by_key.csv`, `derived/status_combination_onbooks_lane.csv`,
`derived/weekly_validation.csv`]

Model self-report: `claude-opus-5-5[1m]`. Date: 2026-09-23; key fix 2026-09-24. Brief:
`BRIEF.md`. Not committed (the lead commits).

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
| brief cells, 5% rule | −18.0 / −14.6 | −4.1 / −3.9 | +2.6 / +2.3 | **+16.5 (9.0) / +13.0 (9.5)** |
| plus labor force | −17.6 / −16.9 | −4.1 / −4.7 | +3.8 / +2.7 | +17.3 (9.0) / +14.8 (9.3) |
| derived fields, 1% rule | −13.2 / −12.7 | −5.9 / −6.5 | +2.6 / +2.3 | +9.9 (9.0) / +8.5 (10.0) |
| derived fields, any flag | −15.2 / −16.1 | −8.9 / −10.7 | +2.6 / +2.3 | +8.8 (10.8) / +7.7 (11.5) |

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
| Medicare coverage (premium receipt key) | −0.4% (0.9) | +1.8% | −2.2% (0.5) | 0.5% |
| Medicaid coverage (not a preferred key) | +2.8% (0.9) | −2.9% | +5.8% (0.5) | 0.8% |
| capital (response 0) | −15.3% (3.5) | +2.9% | −17.7% (3.6) | 1.7% |

The union-matched hot deck agrees in sign with step 4a on wages, federal and state liability and
Social Security, at 48–70% of its size. The pooled control stays within 1.1% of the
published keys for wages, federal and state liability, consumption and Social Security. Where the
account's receipts are concentrated, this lane's hot deck therefore reproduces the Census values
closely when it does not match on union. The control drifts more on self-employment payroll
(−8%), capital (+3%), Medicare coverage (+1.8%) and the small transfer keys (SNAP +5.7%, cash
assistance −9.8%).

Components, $bn a year. The total SE combines the replicate SE with the between-seed variance by
Rubin's rule, T = W + (1 + 1/M)B [CALCULATION: `derived/hotdeck_seed_spread.csv`]:

| Specification | Direct receipts | Transfers | Income-security services | Net cost change (total SE), personal / shared |
|---|---:|---:|---:|---:|
| union-matched hot deck | −15.5 / −13.8 | −3.4 / −3.3 | −0.7 / −1.2 | **+11.4 (6.6) / +9.2 (6.8)** |
| net of the pooled control | −16.3 / −15.9 | −3.8 / −3.8 | +2.2 / +2.4 | **+14.8 (4.2) / +14.6 (4.1)** |
| all items re-imputed | −12.8 / −10.1 | −4.4 / −4.0 | −0.2 / −0.7 | +8.2 (6.6) / +5.3 (7.5) |
| all items, net of control | −19.1 / −17.4 | −4.0 / −3.7 | +3.3 / +2.8 | +18.4 (6.6) / +16.5 (6.9) |
| control: pooled donors (replicate SE) | +0.9 / +2.3 | +0.6 / +0.7 | −2.7 / −3.4 | −2.9 (5.1) / −4.9 (4.8) |

A single seed's net change has an SD of $3.5–4.2bn in the matched hot deck and $1.1–1.2bn in the
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
| Medicare (MEPS payer key, held at its published share) | 0 | 0 | 0 |
| SNAP and refundable credits | +1.2 | +1.0 | −0.1 |

Housing subsidies (−$0.3 to −0.9bn) and the capital-incidence receipts are subsidy and incidence
lines at response 0, so they do not enter the band. The Medicare premium receipt, keyed by
Medicare coverage, moves by $0.2bn or less under every method.

## Step 5: the adopted main case

`main_case_translate.js` shifts the explorer model's executed allocations by the line changes.
National totals are conserved because other residents' allocations move the other way. It then
recomputes the adopted bands exactly as `main_case_2026_09_23/main_case.js` does: justice by use,
uncompensated care inside $3.65–5.75bn, and general government at 0.59–0.84. The low end is the
shared allocation and the high end the personal one [CALCULATION: `derived/main_case_translation.csv`].

| Method | Adopted band, $bn | Change, low / high | SE, low / high |
|---|---|---:|---:|
| published (adopted) | 203.2–249.6 | — | — |
| (a) reweight, brief cells | 216.2–266.1 | +13.0 / +16.5 | 9.5 / 9.0 |
| (a) plus labor-force status | 218.0–266.9 | +14.8 / +17.3 | 9.3 / 9.0 |
| (a) derived fields at 1% | 211.7–259.6 | +8.5 / +9.9 | 10.0 / 9.0 |
| (a) derived fields, any flag | 210.9–258.5 | +7.7 / +8.8 | 11.5 / 10.8 |
| **(b) union-matched hot deck** | **212.4–261.1** | **+9.2 / +11.4** | 6.8 / 6.6 |
| **(b) net of the pooled control** | **217.8–264.4** | **+14.6 / +14.8** | 4.1 / 4.2 |
| (b) all items re-imputed | 208.5–257.8 | +5.3 / +8.2 | 7.5 / 6.6 |
| (b) all items, net of control | 219.8–268.0 | +16.5 / +18.4 | 6.9 / 6.6 |
| control: pooled donors | 198.3–246.7 | −4.9 / −2.9 | 4.8 / 5.1 |

The changes are the same in the other CBO-lag profile, where other education is fixed and the
published band is $158.9–212.6bn. The lines involved respond at 1 in both. The proportional
reference ($307.9–341.0bn) differs because economic-affairs services also respond there. The
hot-deck changes are $0.5–1.3bn smaller and the reweighting changes $0.2–0.9bn larger.

Two readings of (b) bracket the central estimate. The matched run against the published values
(+$9.2 / +11.4bn) treats the control's −$2.9 to −4.9bn as noise. The matched run against the
control (+$14.6 / +14.8bn) treats it as a real difference between this hot deck and the Census
one.

The Medicare spending line keeps its published allocation under every method. The account keys it
by MEPS payer means, which use none of the items these methods re-impute; for the reweighting (a)
that is an approximation [INFERENCE]. The figures in steps 4a to 5d were first published with a
key-name collision that moved this line by Medicare coverage; step 5e describes it, and the
Revisions section lists the figures before and after the fix.

## Step 5b: the distribution lane's inputs

`distribution_check.py` imports the distribution lane's own functions (`load_cps`, `rank_frame`,
`tax_key`, `per_person`; read only). It reproduces its published quintile splits to 4e-13 bn, then
changes the inputs [CALCULATION: `derived/distribution_check.csv`]:

- **Total.** The lane divides A_mid + F_c = −$227.9bn. A_mid moves by minus the midpoint of the
  band changes. The total becomes −$238.2bn under (b) matched, −$242.6bn under (b) net of the
  control, and −$242.7bn under (a).
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
| (b) matched total | −7.22 | −15.23 | −25.68 | −42.12 | −147.99 | −238.24 |
| (b) net of control total | −7.36 | −15.51 | −26.15 | −42.89 | −150.69 | −242.60 |
| (a) total | −7.36 | −15.52 | −26.16 | −42.90 | −150.73 | −242.67 |

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
| keys the audit does not touch (Social Security, consumption, cash, SNAP, Medicare premiums and others) | 0 | −1.95 | −1.95 | 0 |
| **Net** | **+12.31** | **+11.43** | **+20.08** | **−3.67** |

The shared allocation gives +11.99, +9.21, +17.63 and −3.57. The interaction is concentrated
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
| (a) reweight | +13.0 / +16.5 | +19.0 / +22.6 | +15.7 / +19.2 | +12.7 / +16.0 | +21.7–22.2 / +25.6–26.2 |
| (b) union-matched hot deck | +9.2 / +11.4 | **+17.6 / +20.1** | +13.6 / +15.9 | +9.9 / +12.0 | +20.5–21.1 / +23.0–23.6 |
| (b) net of the pooled control | +14.6 / +14.8 | +24.2 / +24.6 | +19.9 / +20.1 | +15.8 / +15.9 | +26.9–27.5 / +27.6–28.2 |

The replicate SEs of the combined net are 8.9–9.5 for (a), 5.2–5.5 for (b) and 3.9–4.0 for (b)
net of control. Seed variance was not recomputed for the combination; in step 4b it added
$1.2–1.7bn to the SE of (b) and $0.2bn to that of (b) net of control. The interaction grows as the
on-books share falls: for (b) it is −$1.6 to −1.7bn at 0.75, −$2.6bn at 0.60 and −$3.6 to −3.7bn
at 0.44. For (a) it is larger, −$6.0 to −6.2bn at 0.44. The reweighting drops imputed records,
and the audit's unauthorized are heavily imputed.

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

## Step 5d: the audit's rules at the on-books lane's shares

`onbooks_share_2026_09_23` replaces the audit's 0.44 / 0.60 / 0.75 with modelled 2024 shares:
Mexico-born 0.415 / 0.526 / 0.635 and other Latin-American-born 0.401 / 0.550 / 0.683, low /
central / high [DATA: `onbooks_share_2026_09_23/derived/onbooks_split.csv`, rows `evidence_*`]. The
lane frame carries birthplace, so `combine_onbooks_lane.py` gives each of the audit's unauthorized
the share of their origin. All 4.567M of the union's unauthorized are Mexico-born. The 4.968M
other Latin-American-born are all outside the union, so their share enters only through the
national totals. On the refundable line, key changes apply only to the part that is not premium
tax credits: the Treasury-measured $110.46bn of $228.809bn, or 48.3% [DATA:
`dataset_integrity_2026_09_23/derived/spending_mts_credits.json`]. Status stays at its published
assignment.

Gates:

- Without the rules, every method's shares reproduce exactly: the reweighting, each hot-deck seed,
  the seed means and the seed spread.
- At a uniform 0.44 under the old non-PTC range, the script reproduces step 5c to 4e-15 bn. That
  includes (b) at +20.5–21.1 / +23.0–23.6.
- The Node translation of the scaled deltas matches the component arithmetic at both ends of the
  adopted band, within 5e-5 bn. In every case the shared allocation is the low end and the personal
  allocation the high end.

The table gives changes in the adopted band's cost, $bn, as low end (shared) / high end
(personal). The increment is the two corrections on one frame minus the audit's rules alone.
Standard errors are in parentheses. Row 2 and (a) have replicate SEs; (b) adds seed variance by
Rubin's rule.

| Case (Mexico-born / other Latin-American) | Row 2: audit's rules alone | Increment, (a) reweight | Increment, (b) hot deck | Increment, (b) net of control |
|---|---:|---:|---:|---:|
| Low (0.415 / 0.401) | +16.2 (1.4) / +16.8 (1.4) | +6.5 (9.2) / +9.9 (8.6) | +5.4 (6.9) / +7.5 (6.5) | +11.9 (4.4) / +12.0 (4.2) |
| Central (0.526 / 0.550) | +12.7 (1.1) / +13.1 (1.2) | +7.6 (9.2) / +11.1 (8.6) | +6.1 (6.9) / +8.2 (6.5) | +12.4 (4.3) / +12.5 (4.2) |
| High (0.635 / 0.683) | +9.2 (0.9) / +9.5 (0.9) | +8.8 (9.2) / +12.2 (8.6) | +6.8 (6.8) / +8.8 (6.5) | +12.8 (4.3) / +13.0 (4.2) |

[CALCULATION: `combine_onbooks_lane.py` → `derived/status_combination_onbooks_lane.csv`]

At the central shares, the audit's rules with (b) give +$18.8 / +21.3bn (SE 7.1 / 6.8). With (b)
net of control they give +$25.1 / +25.6bn (SE 4.4 / 4.3). The other four methods add, at the
central case:

- reweighting with labor-force cells: +9.5 / +12.1;
- the 1% derived rule: +5.1 / +6.0;
- the any-flag rule: +6.9 / +6.9;
- the all-items hot deck: +2.5 / +5.3, or +13.9 / +15.7 net of its control.

Across all eight methods and three cases the increment runs from +$1.8bn to +$16.3bn.

Each increment is smaller than the method's own change under the same convention. There, (b) alone
gives +9.0 / +11.2 and (b) net of control +14.4 / +14.6. For (b), the interaction is −3.6 / −3.7 at
the low shares, −2.9 / −3.0 at the central and −2.2 / −2.3 at the high. As in step 5c, the lower the
on-books share, the less of this lane's change on the unauthorized survives.

Two checks:

- **Uniform shares.** The on-books lane's uniform equivalents (0.416 / 0.524 / 0.631) reproduce
  every method and case within $0.04bn, and row 2 within $0.01bn.
- **The on-books lane's own arithmetic.** Rescale that lane's arithmetic to $110.46bn and compare
  it at the same shares. Here the personal end of row 2 is $0.2bn higher: +13.1 against +12.9 at the
  central case. All of that gap comes from the self-employment key, which the audit's vector does
  not reproduce (step 5c). The shared end is $0.9–1.6bn lower here: +12.7 against +13.9 at the
  central case. The gap is spread over every key. The audit applies each person's share change to
  both allocations, while the account splits each SPM unit's total among its members (step 5c).

## Step 5e: rows 3 and 4, a state-aware status flag, and a key fix

`combine_onbooks_lane.py` extends step 5d on the same frames [CALCULATION:
`derived/status_combination_onbooks_lane.csv`, column `arm`;
`derived/status_combination_onbooks_lane_row4_lines.csv`]. Figures are changes in the adopted band's
cost, $bn, low end (shared) / high end (personal), with the refundable line at the $110.46bn
non-PTC amount. "Central" is the on-books lane's 0.526 / 0.550. In the CSV, `arm_increment_bn` is
the arm's effect on a stack. `overlap_bn` is the same increment under the published weights, the
paper status flag and liability keying, minus the increment under the arm.

Gates, all passed:

- Row 3: the rebuilt `federal_gap_high_agi` arm gives the union $128.4605bn (shared) and
  $118.6199bn (personal) of federal income tax; keyed by liability alone, $137.9447bn and
  $128.2089bn. All four equal the receipts lane's published values, and the national CPS liability
  and the union's high-AGI share equal its keys [DATA:
  `full_account_receipts_2026_09_20/derived/category_allocations.csv`, `allocation_keys.csv`].
- Row 4: IPUMS USA extract 3 reproduces the Mexico-born lane's ACS 2024 totals (11.069M; 3.817M
  naturalized, 7.252M noncitizen). Outside CA+TX its cells equal the PUMS. With scale factors of 1
  the weights are bit-identical, every key share equals the published one, and every step-5d
  figure reproduces (2.8e-14 bn).
- Status: the state-aware path with no listed state-ages returns the paper flag bit for bit and
  reproduces step 5d. With the listed state-ages it gives 5.2265M union unauthorized (5.1589M with
  California alone), the California lane's figures [DATA:
  `california_medical_status_2026_09_23/derived/cps_counts_by_rules.csv`].
- The rebuilt MEPS payer keys, unit-split adults, justice use target ($68.369bn) and
  uncompensated-care shift ($3.652–5.748bn) reproduce the account's values.
- Node agrees with the line arithmetic within 5e-5 bn at the 606 stack ends it checks. The six it
  skips are the key fix's rows for the audit's rules alone, which the fix leaves unchanged. Adding
  the step-5e arms left the step-5d rows of the CSV byte-identical.

### A key-name collision in steps 5 to 5d

`translate.line_deltas` looked up each line's key by name in one dictionary. In this lane's
dictionary "medicare" is Medicare coverage (MCARE), the key of the Medicare premium receipt. The
account keys its $1,102bn Medicare spending line by MEPS payer means, a different key under the same
name: mean public payments by age band and US or foreign birth, for everyone with a coverage
record. So steps 5 through 5d, as first published, moved the Medicare spending line by the change
in the union's Medicare coverage. The MEPS key does not use the items these methods re-impute, so
under the hot decks the line should not move. For the reweighting (a), holding the MEPS key at its
published share is an approximation [INFERENCE]. The fix, method alone:

| Method | Fix | Step 5 as published | Step 5 with the fix |
|---|---:|---:|---:|
| (a) reweight, brief cells (also the 1% and any-flag rules) | −0.25 / −0.10 | +13.3 / +16.6 | +13.0 / +16.5 |
| (a) plus labor-force status | +0.25 / +0.63 | +14.6 / +16.7 | +14.8 / +17.3 |
| **(b) union-matched hot deck** | +0.40 / +0.24 | +8.8 / +11.2 | **+9.2 / +11.4** |
| **(b) net of the pooled control** | +1.18 / +1.22 | +13.4 / +13.6 | **+14.6 / +14.8** |
| (b) all items re-imputed | +0.38 / +0.36 | +5.0 / +7.8 | +5.3 / +8.2 |
| (b) all items, net of control | +1.27 / +1.22 | +15.3 / +17.1 | +16.5 / +18.4 |

The audit's rules alone do not touch Medicare coverage, so row 2 is unchanged. At the step-5d
central case the (b) increment becomes +6.10 / +8.16 (published +5.69 / +7.92) and the (b)-net
increment +12.36 / +12.52 (published +11.18 / +11.30). At the low shares they are +5.42 / +7.45 and
+11.87 / +12.01; at the high shares +6.76 / +8.84 and +12.84 / +13.01. A second collision, the shared
motor-vehicle receipt keyed by unit-split adults, matters only when weights change and is fixed
in every step-5e arm. Every other step-5e arm is measured against the fixed stacks.

On 2026-09-24, with the lead's approval, `translate.py` was corrected and steps 5–5d were rerun.
`translate.KEYS` maps each account key to the lane key that measures it, per side and, where
they differ, per allocation, and the lookup stops on any account key it does not define. Keys the
lane never recomputes are held at their published allocation. The rerun reproduces the "with the
fix" column within 5e-5 bn and the 5d increments above within 3e-14 bn; row 2 and every step-5e
row are byte-identical to the file before the fix. The "as published" column is the record of
the first figures. `translate.AS_PUBLISHED` keeps the first lookup only to recompute them for the
`medicare_key_fix` arm.

### Row 3: the BEA federal income tax gap keyed by high AGI

The gap is $384.8bn (shared) / $422.1bn (personal). The union holds 3.28% / 3.06% of high-AGI
liability against 5.74% / 5.33% of liability, so row 3 alone costs +9.48 / +9.59 (SE 2.0 / 2.1). That
share rests on 34 union records (73k people). Imputed tax units carry 74% of their liability,
against 57% of all union liability.

The audit's rules scale liability but not the high-AGI key. Under row 3, row 2 therefore acts only
on the CPS part of the line, and the gap part keeps the union's full high-AGI share. That is the
overlap with row 2. The audit's unauthorized in the union include 7.8k people with AGI of $500k or
more and $2.0bn of liability. If the rules scaled that key too, row 2 under row 3 would cost $0.67 /
0.77bn more at the central shares, and the overlap would fall to about $0.2–0.3bn [CALCULATION:
`combine_onbooks_lane.py` log, `[row3]` lines; full-sample weight, no SE].

| On-books case | Row 2 over row 3 (overlap) | (b) increment over rows 2+3 (overlap) | (b)-net increment (overlap) |
|---|---:|---:|---:|
| Low | +15.13 / +15.50 (1.11 / 1.29) | +4.41 / +7.46 (1.00 / −0.01) | +11.75 / +11.90 (0.12 / 0.12) |
| Central | +11.81 / +12.08 (0.91 / 1.05) | +5.02 / +8.08 (1.08 / 0.07) | +12.18 / +12.34 (0.18 / 0.18) |
| High | +8.54 / +8.73 (0.70 / 0.81) | +5.61 / +8.69 (1.15 / 0.15) | +12.61 / +12.77 (0.23 / 0.23) |

A method's overlap is the gap times the amount by which it cuts the union's liability share more
than its high-AGI share. The hot deck (b) cuts the liability share 0.28 points more under the
shared allocation (1.08 / 384.8) and 0.02 points more under the personal one. Without row 2, (b)
alone gives +7.63 / +10.74 under row 3 (overlap 1.38 / 0.42) and (b)-net +14.01 / +14.22 (0.40 /
0.43). The reweighting runs the other way: under row 3 its increment grows by $4.2–4.9bn with the
brief cells and by $4.2–6.5bn across the four (a) variants. Dropping imputed tax units removes more
of the union's high-AGI liability (74% imputed) than of its liability (57%). With 34 records behind
the high-AGI share, that figure is fragile [INFERENCE]. At the central case, rows 3 and 2 with (b)
give +26.31 / +29.76, and with (b)-net +33.47 / +34.01.

### Row 4: the Mexico-born count by reweighting

The ASEC puts 1.678M naturalized (n 943) and 4.250M noncitizen (n 2,139) Mexico-born outside CA+TX,
against ACS 2024's 1.436M and 3.307M in the same universe [DATA: IPUMS USA extract 3, STRATA mod 100
= state, checked against `dataset_integrity_2026_09_23/_cache/acs_person_2024.parquet`]. Their
weights fall by factors of 0.856 and 0.778 (replicates 0.80–0.93 and 0.74–0.82). That removes 1.185M
people, 0.943M of them noncitizens. The union falls from 40.897M to 39.712M and its imputed
unauthorized from 4.567M to 3.963M. The Mexico-born lane gets 4.07M from a national noncitizen
factor; here the whole correction falls outside CA+TX, where the lane found the excess and where
59.6% of the union's unauthorized live [CALCULATION: `combine_onbooks_lane.py` log, `[status]`
lines].

**(i) Row 4 alone: +0.24 / +0.50 (SE 0.60 / 0.74).** The Mexico-born lane's formula gives −6.44 /
−7.91. That formula charges each removed person the first generation's average net cost: the
ledger's first-generation share (0.333, waterfall step 14) times the main case, or $5.5–6.8k a head.
The complete account carries no generation split, and this repo's routing notes warn against
flat-scaling the ledger's split onto it. Reweighting instead recomputes every key. In those keys the
removed people pay about what they are charged. Removing them takes $10.8 / $12.7bn of receipts
from the union and $10.5 / $12.2bn of spending [CALCULATION:
`derived/status_combination_onbooks_lane_row4_lines.csv`]:

- Receipts: federal income tax +3.19 / +3.67, OASDI (both halves) +2.79 / +3.59, sales, excise and
  customs +2.02, state income tax +0.87 / +1.04, HI +0.80 / +1.03, other contributions and
  self-employment +0.56 / +0.73.
- Spending: Medicaid (MEPS key) −1.93, Medicare (MEPS key) −1.93, Social Security −1.22 / −1.45,
  schooling (age proxy) −1.13 / −1.28, general government −0.73 / −1.04, the per-head part of justice
  −0.75, refundable credits −0.67 / −1.30, other MEPS health −0.67, cash assistance (income-security
  services and family assistance) −0.36 / −0.51, SNAP −0.26, uncompensated care −0.24 / −0.37.

Per removed person that is $9.1–10.7k of taxes against $8.9–10.3k of keyed spending. The account
counts their taxes at the Census tax model's full compliance, which is what row 2 corrects.

**(ii) With row 2 first,** the unauthorized among them already pay only the on-books share of their
taxes and get no EITC, so removing them saves money. Row 4 over row 2 is −1.34 / −1.48 at the
central shares (−1.76 / −2.06 low, −0.93 / −0.93 high). Row 2 over row 4 is +11.13 / +11.15, an
overlap of 1.58 / 1.98.

**(iii) With the hot deck as well** (central case):

| Stack | Published weights | Under row 4 | Overlap |
|---|---:|---:|---:|
| (b) increment over row 2 | +6.10 / +8.16 | +4.98 / +6.96 | 1.12 / 1.19 |
| (b)-net increment over row 2 | +12.36 / +12.52 | +11.69 / +11.66 | 0.68 / 0.86 |
| Row 4 over row 2 + (b) | — | −2.46 / −2.68 | |
| Row 4 over row 2 + (b)-net | — | −2.02 / −2.34 | |
| Total with (b) | +18.81 / +21.29 | +16.35 / +18.61 | |
| Total with (b)-net | +25.07 / +25.65 | +23.06 / +23.31 | |

Row 4 over row 2 + (b) is −2.78 / −3.12 at the low shares and −2.14 / −2.25 at the high; over row 2
+ (b)-net, −2.38 / −2.83 and −1.66 / −1.86.

**Reassignment sensitivity.** The removed weight goes to other Hispanic origins in the same state ×
sex × age cell (1.180M there, 0.005M at state × sex; the largest recipient factor is 3.05). Row 4
alone becomes −0.00 / +0.19 and row 4 over row 2 −1.63 / −1.84. The difference, −0.25 / −0.31 alone
and −0.29 / −0.36 over row 2, comes from the national totals. The removed weight stays in the
population (336.7M), so every union share falls further. The cut in the union's keyed spending is
13% larger than under row 4, mostly through per-head keys, and the cut in its taxes 10% larger
[CALCULATION: row-4 lines file, arm `row4_other_hispanic` against `row4`].

**(iv) US-born arm, a sensitivity only.** CPS Mexican-origin natives outside CA+TX (11.962M) are
scaled to ACS's 11.279M for 2024, moved to 11.484M at 15 March 2025 at the 2023–24 pace (2023:
10.988M; factor 0.960) [DATA: PUMS 2023, 2024, RELSHIPP ≠ 37, NATIVITY 1, HISP 2]. With row 4 it
gives −1.43 / −1.85 alone (SE 1.1 / 1.5). The US-born part is −1.67 / −2.35: the 0.48M fewer
natives carry $6.3bn of keyed spending, half of it schooling and Medicaid, against $4.0–4.6bn of
taxes. Over row 2 it gives −3.05 / −3.82 at the central shares, and over row 2 + (b) −4.19 / −5.06.

**Scope.** Held at published values: the household pool fraction, the production term and the
non-per-head parts of the justice use key (arrests, ACS custody, ICE bed-days). The union's wage
keys fall 2.4–3.3% under row 4; a proportional move in P + F ($8.8–13.3bn) would add $0.2–0.4bn of
cost [INFERENCE]. The school keys use the union's share of persons 5–24 (18–24 for postsecondary)
as a proxy; they carry −1.13 / −1.28 of the arm. The MEPS and school keys use the published frame
under each weight set. The reweighting methods (a) were not rerun under row 4 or the state-aware
flag.

### State-aware status flag

`california_medical_status_2026_09_23/cps_ca_status.py` (imported read-only) runs the paper rules
with MCAID set to "No" at the state-ages in its `STATUS_BLIND_2024`, where 2024 coverage ignored
status. The union's unauthorized rise from 4.567M to 5.227M (5.159M with California alone). All of
the audit's unauthorized rise from 9.535M to 10.612M (10.359M). Under row 4's weights the union
count is 4.607M (4.555M): the two corrections nearly cancel in the count.

Changes against the paper-rules flag, all listed states:

| On-books case | Row 2 | (b) increment | (b)-net increment |
|---|---:|---:|---:|
| Low | +0.51 / +0.57 | +0.04 / +0.04 | −0.16 / −0.15 |
| Central | +0.26 / +0.32 | +0.02 / +0.02 | −0.13 / −0.13 |
| High | +0.02 / +0.08 | +0.00 / +0.01 | −0.10 / −0.10 |

California alone gives row 2 +0.49 / +0.55, +0.26 / +0.31 and +0.03 / +0.08; (b) −0.01 to −0.02;
(b)-net −0.10, −0.08 and −0.07. Under row 4's weights the flag's effect is almost the same: row 2
+0.50 / +0.55, +0.25 / +0.31 and +0.02 / +0.07; (b) +0.03, +0.01 and −0.00; (b)-net −0.14, −0.12 and
−0.09.

The effect is small because the people the flag adds pay little tax. In the union they are 0.659M,
90% in California and 18% under 19. Per person they average $705 of federal liability, $17.5k of
wages and $813 of EITC, against $2,544, $29.9k and $583 for the paper-rule unauthorized. The flag
reclassifies nobody as legal [CALCULATION: `combine_onbooks_lane.py` log, `[status]` lines,
full-sample weight].

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
| 5d on-books lane shares | on-books lane's low, central and high shares, by origin and uniform × {audit's rules alone, with each of the 8 methods} × 2 allocations; refundable line at the $110.46bn non-PTC amount; gated on step 5c at 0.44 | `status_combination_onbooks_lane.csv` |
| 5e rows 3 and 4, status flag, key fix | key fix on every step-5d stack; row 3 × {alone, each of the 8 methods} × {without rules, 3 origin cases}; row 4, other-Hispanic reassignment and US-born arm × {alone, 4 hot-deck methods} × {without rules, 3 cases}; state-aware flag (all listed states, California) × {published, row-4 weights} × the same stacks; identity gates for weights and flag | `status_combination_onbooks_lane.csv` (column `arm`), `status_combination_onbooks_lane_row4_lines.csv` |
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
5. **Precision.** Once seed variance is included, the two drift-netted hot decks are 3.5 SE
   and 2.4–2.8 SE from zero. The other six corrections are 0.7–1.9 SE. The eight corrections
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
- **Procedure.** This lane's hot deck is not the Census one. The control's drift (−$2.9 to
  −4.9bn, SE about 5) is why two readings of (b) are reported.
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
  account's Medicare spending line uses MEPS payer means, so it keeps its published allocation;
  for the reweighting (a) that is an approximation. Medicare coverage keys only the $7.4bn premium
  receipt, which moves by $0.2bn or less.
- **Step 5e.** Row 4 and the state-aware flag hold the household pool fraction, the production
  term and the justice use key's non-per-head parts. The school keys are an age proxy, and the
  reweighting (a) was not rerun under either. Row 3's high-AGI key rests on 34 union records, and
  the audit's rules do not scale it.
- **Scope.** One file (ASEC 2025, income year 2024), like the account. Medicaid coverage moves
  +2.8% to +5.8%, but the account's Medicaid line uses another key, so it is not in the band.

## Reproduce

From the repository root, in order (about 6 minutes before `combine_onbooks_lane.py`, which takes
about 3; the hot-deck steps take 80 s each):

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
uv run --no-project python3 $L/combine_onbooks_lane.py  # steps 5d and 5e; inputs below
```

`combine_onbooks_lane.py` reads `onbooks_share_2026_09_23` and the MTS credit split (step 5d). For
step 5e it also reads the receipts lane's `allocation_keys.csv` and `category_allocations.csv`, the
Mexico-born lane's `annual_series.csv`, IPUMS USA extract 3, the ACS PUMS person files for 2023 and
2024 in `dataset_integrity_2026_09_23/_cache/`, MEPS 2024 (`h256dat.zip`, through
`build/meps_health_transport_2024.py`), the CPS ASEC coverage item NOCOV_CYR, the justice lane's
`summary.json` and `central_split.csv`, the uncompensated-care lane's `summary.json`,
`main_case_2026_09_23/derived/inputs.json`, and
`california_medical_status_2026_09_23/cps_ca_status.py` with its `cps_counts_by_rules.csv`. With
`--inputs-only` it stops after the input gates and the Node check of the stacks without methods,
and writes only `_cache/`.

A full rerun on 2026-09-23 reproduced every file in `derived/` byte for byte, and
`combine_status.py` reproduced its own outputs. A second run of `combine_onbooks_lane.py`
reproduced `status_combination_onbooks_lane.csv` byte for byte after step 5d. After step 5e, two
runs of the final script (167 s and 162 s) gave byte-identical copies of both of its CSVs, and the
24 other files in `derived/` stayed identical to their state before step 5e. After the key fix
(2026-09-24), two runs of `translate.py`, `distribution_check.py`, `combine_status.py` and
`combine_onbooks_lane.py` gave byte-identical copies of all 26 files in `derived/`. The outputs of
steps 0–4 and 6 did not change; `hotdeck_seed_spread.csv` did, because `translate.py` writes it.

## Did not complete

- The earnings and whole-supplement match variables. The cached documentation does not name
  them; Census's internal specifications would.
- The pooled 2019–2025 weekly-earnings test described in step 6.
- Any administrative-record validation (restricted-use).
- A check of the calculator's 2024 parameters against Rev. Proc. 2023-34.
- The reweighting (a) under row 4 and under the state-aware flag, and the production term under
  row 4.
- Row 2 with the high-AGI key scaled as well, beyond the full-sample figure in step 5e.

## For the lead to check

1. `translate.py` ends with "all gates passed", and the published bands reproduce to 1e-4 bn.
2. Which figure to propose: (b) matched, +$9.2 / +11.4bn, the conservative one; (b) net of
   control, +$14.6 / +14.8bn, the most precise; or the range, +$5–18bn. The proposal is the
   operator's call. The adopted band stands until then.
3. The shared-allocation SEs (6.8 for (b), 9.5 for (a)). Only the two drift-netted hot decks are
   significant at 5% (3.5 and 2.4–2.8 SE). The others are 0.7–1.9 SE.
4. The distribution lane: only its fiscal total needs updating, by the same midpoint (−$10.3 to
   −$14.7bn).
5. The combination with `cps.md` row 1: carry the one-frame figure from step 5c, never the sum.
   With the (b) hot deck at 0.44 on-books that is +$17.6 / +20.1bn on the adopted line. Under the
   non-PTC convention it is +$20.5–23.6bn. The audit's own shared-allocation figure is about $1.5bn
   high on the account's keys.
6. Row 2 at the on-books lane's shares (step 5d): +$16.2 / +16.8bn low, +$12.7 / +13.1bn central
   and +$9.2 / +9.5bn high, on the account's keys at the $110.46bn non-PTC amount. The (b) hot deck
   adds +$5.4–6.8bn at the low end of the band and +$7.5–8.8bn at the high end, or +$11.9–13.0bn
   net of its control.
7. The key fix (step 5e), applied on 2026-09-24. Every figure in steps 4a–5d is the fixed one.
   Row 13 of the audit synthesis, derived as before, becomes 6.76 / 9.78 / 12.01 (was 6.36 /
   9.02 / 10.79). Row 2 does not change.
8. Row 4 (step 5e). Reweighting gives +$0.2 / +0.5bn alone, not −$6.4 / −7.9bn. The stacked figure
   is the one to carry: −$0.9 to −2.1bn over row 2, and −$2.1 to −3.1bn over row 2 with the hot
   deck. The US-born arm is a sensitivity only.
9. Row 3 (step 5e). At the central shares it overlaps row 2 by $0.9 / 1.0bn and the hot deck by
   $1.1 / 0.1bn. Both overlaps depend on the audit's rules leaving the high-AGI key unscaled.
10. The state-aware flag (step 5e) adds $0.0–0.6bn to row 2 and moves the hot-deck increments by
    −$0.16 to +$0.04bn.

## Revisions

- 2026-09-23: first complete version.
- 2026-09-23: step 5c added at the lead's request, combining this lane with the dataset audit's
  status re-key key by key (`combine_status.py`).
- 2026-09-23: step 5d added at the lead's request (`combine_onbooks_lane.py`). It applies the
  audit's rules at the on-books lane's shares, by origin, with the refundable line at the
  Treasury-measured $110.46bn non-PTC amount. The stray model-name line above the title was removed.
- 2026-09-23: step 5e added at the lead's request (addenda 1–4), in the same script: the dataset
  audit's rows 3 and 4, a state-aware status flag, and a US-born sensitivity. It found that the
  translation keyed the Medicare spending line by Medicare coverage instead of the account's MEPS
  key. With the account's key, the hot-deck figures of steps 5–5d rise by $0.2–1.3bn; the verdict
  and step 5 carry notes. New output `status_combination_onbooks_lane_row4_lines.csv`. The step-5d
  rows of `status_combination_onbooks_lane.csv` are unchanged.
- 2026-09-24: key-name fix applied at the lead's request. `translate.KEYS` now resolves each account
  key explicitly: the Medicare spending line keeps the account's MEPS payer key at its published
  share, the shared motor-vehicle receipt uses unit-split adults, and an account key the map does
  not define stops the run. `combine_onbooks_lane.py` dropped its local key remapping. Steps 5–5d
  were rerun; the outputs of steps 0–4 and 6, row 2 and every step-5e row are unchanged. Step 5's
  argument that the control over-corrects Medicare, and the Limits note built on it, were removed:
  the line no longer moves. The §5e table keeps the "as published" column as the record. Old → new,
  $bn, low / high end:
  - Verdict: about $9–14bn → $9–15bn; eight corrections $5–17bn → $5–18bn; adopted band about
    $212–263bn → $212–264bn.
  - (a) reweight: +13.3 / +16.6 → +13.0 / +16.5 (SE 9.5 / 9.0, unchanged).
  - (b) hot deck: +8.8 / +11.2 (SE 6.7 / 6.3) → +9.2 / +11.4 (SE 6.8 / 6.6).
  - (b) net of control: +13.4 / +13.6 → +14.6 / +14.8 (SE 4.1 / 4.2, unchanged). Control:
    −4.1 / −1.9 → −4.9 / −2.9.
  - Distance from zero of the drift-netted hot decks: 3.2–3.3 and 2.2–2.6 SE → 3.5 and 2.4–2.8 SE.
  - Distribution lane total: $237.9–242.8bn → $238.2–242.7bn; midpoint −$10.0 to −14.9bn →
    −$10.3 to −14.7bn.
  - Step 5c, (b) with the audit at 0.44: +17.2 / +19.8 → +17.6 / +20.1; non-PTC +20.1–23.4 →
    +20.5–23.6.
  - Step 5d increments at the central shares: (b) +5.7 / +7.9 → +6.1 / +8.2; (b) net of control
    +11.2 / +11.3 → +12.4 / +12.5. Across the three cases: (b) +5.0–6.4 / +7.2–8.6 → +5.4–6.8 /
    +7.5–8.8; net of control +10.7–11.8 → +11.9–13.0. All eight methods: +1.5 to +15.1 → +1.8 to
    +16.3.
  - Step 5d totals at the central shares: (b) +18.4 / +21.0 → +18.8 / +21.3; (b) net of control
    +23.9 / +24.4 → +25.1 / +25.6.
  - Row 13 of the audit synthesis: 6.36 / 9.02 / 10.79 → 6.76 / 9.78 / 12.01.
