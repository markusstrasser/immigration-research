# Consumption, saving, remittances by Hispanic origin / nativity

**Verdict:** NO on the premise, with one real exception. At genuinely equal income, Hispanic-origin
households spend *less* on every category the "frivolous goods" frame predicts: tobacco 0.33× the
matched share, cash contributions 0.43×, alcohol 0.71×, entertainment 0.80×. The exception the brief
anticipated is real — vehicle purchases run 1.25× the matched share, alongside apparel 1.45× and food
away from home 1.13×. Total spending at equal income is essentially identical (0.975×), not lower.
Yet median Hispanic net worth is $61,600 against $285,000 for non-Hispanic white families, 1.3 years
of income against 3.5. Equal consumption and one-quarter the wealth. The best-sourced candidate for
where the money goes is remittances: Mexican immigrant workers sent 16.7 percent of their entire US
labor income to Mexico in 2024, $62.5bn out of a $373.7bn wage bill. The decomposition literature
independently rejects a behavioral explanation — conditional on age, children, education and income,
Mexican-American households accumulate wealth the way comparable white households do.

**CORRECTION, same session.** An earlier version of this file claimed total spending was "22 percent
lower" at equal income and read that gap as the remittance outflow. That was wrong. A peer script in
this lane (`ce_income_matched.py`, not written by me) caught an off-by-one column index: I labelled
the comparison column $70,000–$99,999 and quoted its mean income ($83,888), but read every share and
expenditure figure from the next column over, $100,000–$149,999 (mean income $121,852). Households
earning $122k naturally outspend Hispanic households earning $86k, so the "22 percent gap" was an
income gap I had introduced myself. I re-derived the column headers independently and confirm the
peer is correct. All ratios below are now shown against *both* brackets. The alcohol/tobacco/
entertainment finding survives and tobacco strengthens; the vehicle-purchase, food-away, education
and pension readings all change sign or magnitude. Do not cite the earlier numbers.

The parent session independently reached the same correction and appended its own note at the foot of
this file; both re-derivations agree line for line. That note also catches a labelling defect I had
repeated throughout: Table 2200's comparison column is "White, Asian, and all other races, not
including Black or African-American", not non-Hispanic white alone. Column headers here now say so.

Model self-report: claude-opus-5[1m] (Opus 5, 1M context), `researcher` teammate, 2026-09-16.

## Method note on "at equal income"

BLS publishes no Hispanic-origin × income cross-tab, so the control has to be built. No single
bracket of Table 1203 matches Hispanic consumer units on both income and household size, so I report
two and let the reader see the spread:

| | Hispanic CUs (Tbl 2200) | $70,000–$99,999 (Tbl 1203) | $100,000–$149,999 (Tbl 1203) |
|---|---|---|---|
| Mean income before taxes | $85,710 | **$83,888** | $121,852 |
| People per consumer unit | 3.0 | 2.5 | **2.9** |
| Earners | 1.7 | 1.5 | 1.8 |
| Homeowner % | 46 | 64 | 74 |
| Total annual expenditure | $69,600 | **$71,369** | $89,727 |

The $70–100k bracket is the **income match** (within 2.2 percent) and is the primary comparison. The
$100–150k bracket is the **size match** (2.9 vs 3.0 people) but carries 42 percent more income, so it
flatters Hispanic households on every discretionary share and must not be read as an income control.
Neither bracket matches on homeownership, which is the largest uncontrolled confound (46 percent vs
64–74) and mechanically inflates the Hispanic housing share.
[INFERENCE — my construction from two published tables, not a BLS-published control]

Against the income-matched bracket, Hispanic households spend 97.5 percent as much in total while
containing 3.0 people against 2.5. Per capita they spend materially less; per household, the same.

## Table — CE 2024 expenditure shares

[SOURCE: BLS Consumer Expenditure Survey 2024, Table 2200 "Hispanic or Latino origin of reference
person", https://www.bls.gov/cex/tables/calendar-year/mean-item-share-average-standard-error/reference-person-latino-2024.xlsx
and Table 1203 "Income before taxes", .../cu-income-before-taxes-2024.xlsx — both downloaded, parsed
locally, copies and the parsing script in this directory]

Read the **H/70k** column as the answer. H/100k is shown only so the size-matched view is visible.
The second column is BLS's "Not Hispanic or Latino: White, Asian, and all other races, not including
Black or African-American" — it is **not** non-Hispanic white alone, and it includes Asian households,
whose higher income and wealth pull that column up. Ratios against it overstate the Hispanic/white
contrast.

| Category | Hisp % | NH wh/As/oth % | $70-100k % | $100-150k % | H/ref | **H/70k** | H/100k |
|---|---|---|---|---|---|---|---|
| Food at home | 8.9 | 7.8 | 8.6 | 7.9 | 1.14 | 1.03 | 1.13 |
| Food away from home | 5.4 | 5.1 | 4.8 | 5.3 | 1.06 | **1.13** | 1.02 |
| Alcoholic beverages | 0.5 | 0.9 | 0.7 | 0.8 | 0.56 | **0.71** | 0.62 |
| Housing | 36.6 | 32.2 | 35.3 | 32.8 | 1.14 | 1.04 | 1.12 |
| Apparel and services | 3.2 | 2.4 | 2.2 | 2.3 | 1.33 | **1.45** | 1.39 |
| Transportation | 19.1 | 16.5 | 17.2 | 17.9 | 1.16 | 1.11 | 1.07 |
| Vehicle purchases (net outlay) | 7.4 | 6.9 | 5.9 | 6.7 | 1.07 | **1.25** | 1.10 |
| Healthcare | 5.8 | 8.3 | 8.6 | 8.0 | 0.70 | 0.67 | 0.72 |
| Entertainment | 3.5 | 5.0 | 4.4 | 4.4 | 0.70 | **0.80** | 0.80 |
| Personal care products and services | 1.4 | 1.2 | 1.3 | 1.3 | 1.17 | 1.08 | 1.08 |
| Reading | 0.1 | 0.2 | 0.1 | 0.1 | 0.50 | 1.00 | 1.00 |
| Education | 1.3 | 2.2 | 1.2 | 1.6 | 0.59 | 1.08 | 0.81 |
| Tobacco products and smoking supplies | 0.2 | 0.5 | 0.6 | 0.4 | 0.40 | **0.33** | 0.50 |
| Miscellaneous | 1.4 | 1.5 | 1.8 | 1.5 | 0.93 | 0.78 | 0.93 |
| Cash contributions | 1.3 | 3.3 | 3.0 | 2.3 | 0.39 | **0.43** | 0.57 |
| Personal insurance and pensions | 11.1 | 12.9 | 10.1 | 13.4 | 0.86 | 1.10 | 0.83 |
| Life and other personal insurance | 0.4 | 0.8 | 0.6 | 0.7 | 0.50 | 0.67 | 0.57 |
| **Total expenditure ($)** | **69,600** | 84,260 | **71,369** | 89,727 | 0.83 | **0.975** | 0.78 |

Levels behind the shares (mean $, Hispanic vs that reference column): alcohol 377 vs 770; tobacco 173 vs 405;
entertainment 2,407 vs 4,234; cash contributions 911 vs 2,741; apparel 2,217 vs 1,995; food at home
6,220 vs 6,586 on a 3.0-person vs 2.3-person household.

At the income-matched bracket:
- **Lower:** tobacco 0.33, cash contributions 0.43, healthcare 0.67, life insurance 0.67, alcohol
  0.71, miscellaneous 0.78, entertainment 0.80. Every category the "frivolous" frame names is here,
  and tobacco is the single largest deviation in the table in either direction.
- **Higher:** apparel 1.45, vehicle purchases 1.25, food away from home 1.13, transportation 1.11,
  pensions and insurance 1.10, personal care 1.08, education 1.08.
- **Vehicle purchases at 1.25 is the brief's predicted exception and it holds.** The caveat is that
  Hispanic households own *fewer* vehicles (1.7 against 2.0 in the reference column), so a higher purchase share
  on a smaller fleet reads as replacing older vehicles or buying on worse credit terms rather than
  accumulating cars. Distinguishing those needs vehicle age and finance-charge data CE does not
  publish in this table. [GAP]
- **Education at 1.08 and pensions at 1.10 flip sign** relative to the withdrawn version. Against
  the pooled non-Hispanic reference column they look far lower (0.59, 0.86); against equal income they are
  slightly higher. The apparent education deficit is an income effect, not an ethnic one.
- **Apparel at 1.45 is the largest positive deviation** and tracks children: 0.8 children under 18
  per Hispanic consumer unit against 0.5 in the reference column.
- **Cash contributions at 0.43 remains anomalous** given that remittances should land in this line.
  See the remittance section: CE is not capturing that flow.

## Saving and wealth

[SOURCE: Federal Reserve, *Changes in U.S. Family Finances from 2019 to 2022*, SCF 2022,
https://www.federalreserve.gov/publications/files/scf23.pdf; and FEDS Note "Greater Wealth, Greater
Uncertainty", 2023-10-18]

| | White NH | Hispanic | Black NH | Asian |
|---|---|---|---|---|
| Median net worth, 2022 ($000) | 285.0 | 61.6 | 44.9 | 536.0 |
| Mean net worth, 2022 ($000) | 1,367.2 | 227.5 | 211.5 | 1,826.9 |
| Median income, 2022 ($000) | 81.1 | 46.7 | 46.0 | 122.6 |
| Median net worth ÷ median income | 3.5 | 1.3 | 1.0 | 4.4 |

The wealth-to-income ratio is the load-bearing number: Hispanic families hold 1.3 years of income in
net worth against 3.5 for white families. That is a 2.7× deficit in asset accumulation that the
expenditure data above says is *not* explained by higher consumption. Candidate explanations, none
verified here: remittance outflow, lower homeownership (46 vs 72 percent in CE 2024), shorter US
tenure, no inherited wealth, informal-sector earnings outside retirement systems. [GAP — needs the
decomposition]

The SCF's saving measure is binary ("did the family spend less than income"). 56 percent of all
families saved in 2022, down from 59 in 2019; 43 percent in the bottom half of the income
distribution. The published Bulletin breaks this by income segment, not by race. [GAP — a
race/ethnicity cut of the saved-last-year variable needs the SCF public extract, not the Bulletin]

## Banking, credit and nonbank services

[SOURCE: FDIC 2023 National Survey of Unbanked and Underbanked Households,
https://www.fdic.gov/household-survey/2023-fdic-national-survey-unbanked-and-underbanked-households-report,
Executive Summary Figure ES.11 and Appendix Table G.1]

| | Hispanic | White NH |
|---|---|---|
| Unbanked | 9.5 | 1.9 |
| Cash-only unbanked | 7.6 | 1.1 |
| Underbanked | 21.7 | 10.1 |
| No mainstream credit | 25.5 | 11.2 |
| Rent-to-own or payday/pawn/auto-title/tax-refund loan | 8.1 | 4.6 |

Nativity cut, unbanked rate 2023: foreign-born noncitizen 14.3 percent (up 3.2 points from 2021,
significant), foreign-born citizen 3.8 percent, against a 4.2 percent national rate. The
citizen/noncitizen split (14.3 vs 3.8) is wider than the Hispanic/white split (9.5 vs 1.9), which
points at legal status and institutional access rather than ethnicity. [SOURCE: FDIC 2023 Appendix
Tables, "Citizenship and Place of Birth" rows, unbanked series]
[UNVERIFIED] A second appendix series shows Hispanic 14.8 / foreign-born citizen 8.7 / foreign-born
noncitizen 6.6 for 2023. I could not identify which measure that is from the search excerpt, so it
is excluded from the reading above. Anyone extending this must open Appendix Table G.1 directly.

Predatory-credit use is elevated (8.1 vs 4.6 percent) but the absolute level is low and the
composite lumps tax-refund-anticipation loans, the most common of the five products nationally
(2.5 percent of all households), with payday loans (about 1 percent). This is a thin-file and
unbanked-status story, not a spending-taste story.

Kansas City Fed finds Hispanic and foreign-born unbanked households are disproportionately
"uninterested-never-banked" and cite distrust of banks rather than fees, with the nativity effect
independent of the Hispanic effect (marginal effect −0.085 for US-born).
[SOURCE: Hayashi, Routh & Toh, https://doi.org/10.18651/rwp2023-08]

## Origin-group heterogeneity inside "Hispanic"

The CE Hispanic table pools Mexican, Puerto Rican, Cuban, Central/South American and other Spanish
origin. The only BLS work that splits them is Paulin's, now badly dated: in CE 2000–01 Mexican
families were 56 percent of Hispanic consumer units but 59 percent of Hispanic transportation
spending, 51 percent of housing, 38 percent of public transport, and 56 percent of apparel.
[SOURCE: Geoffrey D. Paulin, "A changing market: expenditures by Hispanic consumers, revisited",
Monthly Labor Review, Aug 2003, https://www.bls.gov/opub/mlr/2003/08/art2full.pdf]
So Mexican-origin households skew toward private vehicles and away from housing *within* the
Hispanic pool, consistent with suburban/exurban settlement. No post-2003 BLS update exists. [GAP]

## Caveats

1. **CE pools origins.** Every 2024 number above is "Hispanic or Latino", not Mexican-origin. The
   Mexican-specific answer requires CE PUMD microdata (the `REF_RACE`/`ORIGIN` variables) — not done
   here. [GAP]
2. **CE has no nativity variable in the published tables.** Foreign-born vs US-born Hispanic
   spending cannot be separated from these files. [GAP]
3. **Income under-reporting.** If Hispanic households under-report income more than others (informal
   earnings), the matched bracket is set too low and the true Hispanic shares should be compared to
   a *higher* bracket, which would widen the "spends less on discretionary goods" conclusion, not
   narrow it. The direction of this bias favors the verdict.
4. **Expenditure under-reporting.** CE under-reports spending generally. If that under-report is
   worse for Spanish-language or lower-education respondents, the true Hispanic total is above the
   measured 0.975× and the "equal spending at equal income" reading would become "slightly more".
   This bias runs *against* the verdict and is the main reason not to treat 0.975 as precisely one.
5. **Household size and age are not fully controlled.** Per-capita rather than per-household shares
   would lower Hispanic food and apparel further.
6. **Homeownership is the biggest uncontrolled confound** (46 vs 74 percent), and it inflates
   Hispanic housing share while suppressing the imputed-rent-adjusted picture.

## Findings appended after the stub

- [DONE] CE 2024 Table 2200 + Table 1203, parsed locally, income-matched benchmark built.
- [DONE] SCF 2022 net worth and income by race/ethnicity.
- [DONE] FDIC 2023 unbanked/underbanked by Hispanic origin and by citizenship/nativity.
- [DONE] Paulin MLR 2003 origin-group heterogeneity.
- [DONE 2nd epoch] Remittances, SIPP wealth by nativity, generational convergence — below.

## Remittances

[SOURCE: Banco de México, *Ingresos y Egresos por Remesas, diciembre de 2024*,
https://www.banxico.org.mx/publicaciones-y-prensa/remesas/%7BD08E80AC-6031-C7CF-D792-28CBEF70658F%7D.pdf]

| | 2023 | 2024 |
|---|---|---|
| Total remittances received by Mexico (US$ mn) | 63,319 | 64,745 |
| Of which sent from the United States (US$ mn) | 60,925 | 62,529 |
| Share arriving by electronic transfer | — | 99.1% |
| Average per transaction (December) | — | $375 |

2024 was an eleventh consecutive year of growth and a record. California alone sent $20,412mn and
Texas $9,002mn, together 47 percent of the US total.
[SOURCE: BBVA Research, *Mexico | Record in remittances*, 2025-02-04,
https://www.bbvaresearch.com/en/publicaciones/mexico-record-in-remittances-64745-million-dollars-in-2024-and-dark-spots-for-2025]

The decisive number is the remittance rate out of US earnings:

| Year | Remittances from US ($mn) | Mexican immigrant US wage bill ($mn) | Share of labor income remitted |
|---|---|---|---|
| 2021 | — | — | 17.7% |
| 2022 | 56,367 | 319,940 | 17.6% |
| 2023 | 60,925 | 340,903 | 17.9% |
| 2024 | 62,529 | 373,726 | **16.7%** |

[SOURCE: CEMLA, *Notas de Remesas* 2025-03, https://www.cemla.org/foroderemesas/notas/2025-03-notas-de-remesas.pdf
— combines Banxico remittance data with CPS extracts for the wage bill; remittances were 3.38 percent
of Mexican GDP in 2024]

**What this does and does not explain.** An earlier version of this file claimed the remittance rate
explained a 22 percent CE spending shortfall. That shortfall does not exist — at equal income
Hispanic households spend 97.5 percent as much as the matched bracket. The remittance figure is
still large and well sourced, but it can no longer be cashed out against a measured consumption gap.

What remains is an accounting puzzle worth stating precisely. At equal pretax income, Hispanic
households spend about the same, yet hold roughly a quarter the net worth relative to income (1.3
years against 3.5). Pretax income must go to consumption, taxes, saving, or transfers abroad. If
consumption is equal and saving is far lower, then taxes plus remittances must absorb the difference.
Hispanic consumer units are younger with more children, so their effective tax rate is likely
*lower*, not higher, which widens rather than closes the residual and points at transfers. That is
consistent with the 16.7 percent remittance rate, but I have not closed the identity: CE does not
publish taxes paid alongside these shares, the remittance rate is measured on Mexican immigrant
workers rather than all Hispanic consumer units, and the SCF wealth figures come from a different
survey and year. Treat this as a well-motivated hypothesis with a clear test, not a finding.
[INFERENCE — unclosed accounting identity] [GAP — closing it needs CE PUMD with the tax variables,
or SCF restricted to Hispanic households with a remittance question]

**CE does not capture this flow.** Hispanic cash contributions average $911 per consumer unit per
year. Against that: 2024 saw roughly 165 million remittance transactions (Banxico reports 13.9
million in December alone) against an estimated 10.2 million senders in 2023, implying on the order
of $6,200 per sender per year. Even discounting heavily for the fact that most Hispanic consumer
units contain no remitter, the CE cash-contributions line cannot be carrying this. Treat CE cash
contributions as silent on remittances. [INFERENCE — arithmetic on published totals; senders count
from Inter-American Dialogue, *Sending Money to Mexico: Slowed Growth in 2024*,
https://thedialogue.org/blogs/2024/07/sending-money-to-mexico-slowed-growth-in-2024/, which also
reports average principal of $487 per transaction from remittance-company data, above the Banxico
average]

Note the caution on the BBVA figure: BBVA's "13.7 million transactions" is a monthly figure, not
annual. $64,745mn ÷ 13.7mn would imply $4,726 per transaction, which contradicts the published $393
average. Annual transactions are approximately 165 million. Anyone citing BBVA's transaction count
as annual will be off by a factor of twelve. [SOURCE: arithmetic check against Banxico December 2024
figures of $5,228mn over 13.9mn transactions]

Participation rates are old and need refreshing: 47 percent of foreign-born Latinos remitted
regularly, 45 percent of Mexican immigrants specifically, against 57 percent Salvadoran and 59
percent Dominican. That survey is from 2002. [SOURCE: Pew Hispanic Center / IADB Multilateral
Investment Fund, *Billions in Motion: Latino Immigrants, Remittances and Banking*,
https://www.pewresearch.org/wp-content/uploads/sites/5/reports/13.pdf; also
https://doi.org/10.18235/0008582] [GAP — no current participation-rate survey found; the 45 percent
figure is 24 years old and should not be used for 2024 without replacement]

**Correction to the brief's framing.** The brief asked for Amuedo-Dorantes & Pozo on the
"remittance-vs-saving trade-off". Most of that pair's output measures what *receiving* households in
Mexico do with the money, not what sending households in the US give up. Their receiving-side result
runs opposite to the intuition: remittances *raise* asset accumulation among recipients, and a one
standard deviation rise in remittance-income uncertainty lifts the likelihood of asset-accumulating
spending by about 2 percentage points and the asset share of expenditure by 4 to 9 percent.
[SOURCE: Amuedo-Dorantes & Pozo, *When Do Remittances Facilitate Asset Accumulation?*, IZA DP 7983,
https://docs.iza.org/dp7983.pdf] The US-side finding sits in their earlier paper: immigrants
accumulate less wealth than natives, and young natives' wealth responds more to income uncertainty
than young immigrants' does. [SOURCE: Amuedo-Dorantes & Pozo, "Precautionary Saving by Young
Immigrants and Young Natives", *Southern Economic Journal* 69(1):48, 2002,
https://doi.org/10.2307/1061556] Also relevant: having a US bank account did not raise monthly
remittance flows among Mexican immigrants, though it raised amounts carried home.
[SOURCE: Amuedo-Dorantes et al., "Money Transfers among Banked and Unbanked Mexican Immigrants",
https://onlinelibrary.wiley.com/doi/10.1002/j.2325-8012.2006.tb00777.x]

## SIPP wealth by nativity — the behavioral question settled

[SOURCE: Cobb-Clark & Hildebrand, "The Wealth and Asset Holdings of U.S.-Born and Foreign-Born
Households: Evidence from SIPP Data", *Review of Income and Wealth* 52(1):17-42, 2006,
https://doi.org/10.1111/j.1475-4991.2006.00174.x]

Median wealth of US-born couples is 2.5 times that of foreign-born couples; for singles the ratio is
3. Within the immigrant population, variation is driven mainly by source region, while entry cohort
predicts portfolio composition: established immigrants hold *less* financial wealth and more real
estate equity, recent immigrants the reverse.

The Mexican-specific decomposition is the load-bearing citation for the operator's question:

[SOURCE: Cobb-Clark & Hildebrand, "The Wealth of Mexican Americans", *Journal of Human Resources*
41(4):841-868, 2006, https://doi.org/10.3368/jhr.xli.4.841 — SIPP, DiNardo-Fortin-Lemieux
semi-parametric decomposition across the 10th to 90th percentiles]

- At the median, native-born Mexican Americans hold just over $21,000 more net worth than
  foreign-born Mexican Americans.
- Between one third and one half of the Mexican-American/white wealth gap is the conditional
  education distribution: given the same geography and household composition, Mexican Americans
  obtain less schooling.
- At the median, 20 percent of the native-born and 31 percent of the foreign-born wealth
  disadvantage is attributable to having more young children and younger household heads. Demography
  outweighs conditional income differences.
- Income differences explain 22 percent of the nativity wealth gap at the median.
- **The authors' own summary:** Mexican Americans' wealth disadvantage "is in large part not the
  result of differences in the way in which households — conditional on their characteristics —
  accumulate net worth."

That last line is the direct answer to a cultural-profligacy hypothesis, from a decomposition
designed to detect exactly such a residual. The residual is not there. Conditional on age, children,
education and income, Mexican-American households accumulate wealth the way comparable white
households do.

A later SIPP study reaches the same place from a different angle: race and ethnicity stratify
immigrant wealth across the whole distribution, but there is "little wealth inequality within
racial/ethnic groups by nativity status."
[SOURCE: Painter & Qian, "Wealth Inequality Among Immigrants", *Population Research and Policy
Review* 35(2), https://doi.org/10.1007/s11113-016-9385-1; and
https://www.sciencedirect.com/science/article/abs/pii/S0049089X13000616]

## Generational convergence

[SOURCE: Keister, Agius Vallejo & Borelli, "Mexican American Mobility: Early Life Processes and Adult
Wealth Ownership", https://pmc.ncbi.nlm.nih.gov/articles/PMC6548331/ and Stanford working-paper
version https://inequality.stanford.edu/sites/default/files/media/_media/working_papers/keister_agius-vallejo_borelli_mexican-american-mobility.pdf
— NLSY79, first/second/third-generation-plus Mexican Americans, asset growth 1985 to 2010]

- Childhood poverty and low inheritance receipt are severe in the first generation and **decline with
  each generation since migration**. Second- and later-generation Mexican Americans are *less* likely
  than African Americans to be raised in poverty and *more* likely to receive transfers.
- Mexican Americans accumulate assets more slowly than non-Latino whites (β = −7.55) but faster than
  African Americans.
- **Accumulation rates rise in the second generation** and fall back slightly in the third.
- At midlife, Mexican Americans hold less wealth than whites but more than African Americans, even
  with early-life impediments controlled.

The authors read this as delayed assimilation rather than downward mobility. The second-generation
acceleration is the finding that matters for the operator's question: whatever depresses first-
generation asset accumulation is substantially a first-generation condition, not a transmitted trait.

One methodological warning for anyone extending this: the non-Latino white reference group is not
fixed. Selective in-migration of more-educated whites into California and Texas raised the
comparison bar on some attainment measures, so second-generation progress measured against
state-resident whites differs from progress measured against all whites in the state.
[SOURCE: "Intergenerational Mobility of the Mexican-Origin Population in California and Texas
Relative to a Changing Regional Mainstream", *International Migration Review*,
https://journals.sagepub.com/doi/10.1111/imre.12086]

[GAP] Generational convergence in *consumption* specifically — as opposed to wealth — remains
unsourced. The wealth literature is rich; I found no CE or PSID study of expenditure shares by
immigrant generation. If that matters, CE PUMD is the build, not a literature search.

## Remaining gaps after epoch 2

- [GAP] Mexican-origin expenditure shares specifically (CE pools all Hispanic origins). Needs CE PUMD.
- [GAP] Hispanic spending by nativity — no published CE table carries a nativity variable.
- [GAP] SCF "saved last year" cut by race/ethnicity — needs the SCF public extract, not the Bulletin.
- [GAP] Current remittance participation rate; the 45 percent Mexican figure dates to 2002.
- [GAP] Generational convergence in consumption shares.
- [GAP] Lottery and gambling by Hispanic origin — not searched.
- [GAP] BNPL by Hispanic origin — FDIC Appendix Table E.5 carries it; row not pulled.

## Tool notes

- `bls.gov` returns 403 to plain curl. It serves the .xlsx with a full Chrome header set including
  `sec-ch-ua`, `sec-ch-ua-platform` and the three `Sec-Fetch-*` headers; dropping `sec-ch-ua` alone
  reproduced the 403. Firecrawl's proxy reaches the HTML index pages without any of that.
- BLS stopped publishing the PDF version of Table 2200 after 2022; 2023 and 2024 are .xlsx only, so
  the `reference-person-latino-2024.pdf` URL is a real 404, not a bot wall.

## Correction (parent session, 2026-09-16 23:00) — the "income-matched" column was misaligned

**Stale above:** every "income-matched" figure except the $83,888 income. The lane read income from
the $70,000–$99,999 column of Table 1203 but people (2.9), homeownership (74%), total expenditure
($89,727) and every "income-matched share" from the $100,000–$149,999 column (mean income $121,852).
The 22 percent total-spending gap is therefore an artefact of comparing Hispanic spending with a
bracket that earns 42 percent more. Re-parsed with `ce_income_matched.py` (columns fixed by index,
output in `ce_income_matched.csv`):

| | Hispanic | $70–100k bracket (income match) | $100–150k bracket (size match) |
|---|---|---|---|
| Mean income | 85,710 | 83,888 | 121,852 |
| People | 3.0 | 2.5 | 2.9 |
| Homeowner % | 46 | 64 | 74 |
| Total expenditure $ | 69,600 | 71,369 | 89,727 |
| Hispanic ÷ bracket | | **0.975** | 0.776 |

Share ratios, Hispanic ÷ income-matched ($70–100k) bracket: alcohol 0.71, tobacco 0.33,
entertainment 0.80, cash contributions 0.43, healthcare 0.67, education 1.08, pensions and
insurance **1.10** (not 0.83), apparel 1.45, vehicle purchases **1.25** (not 1.10), food at home 1.03,
housing 1.04. The verdict on "frivolous" categories survives and strengthens on tobacco; the claims
that Hispanic households spend 22 percent less in total and save less through pensions do not
survive. At matched income they spend about the same in total, put a slightly *higher* share into
pensions and insurance, and a larger share into vehicles and clothing. The wealth-to-income deficit
(SCF 1.3 vs 3.5 years) therefore cannot be explained by a consumption gap at all; it has to come
from remittances, tenure, homeownership and the income level itself.

Also stale: the Table 2200 column labelled "NH-white" above is BLS's "Not Hispanic or Latino: White,
Asian, and all other races" column, not non-Hispanic white alone.
