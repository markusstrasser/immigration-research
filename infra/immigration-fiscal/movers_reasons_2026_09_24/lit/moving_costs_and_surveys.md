**Verdict:** Published interstate moving-cost estimates run from about $3–4k out of pocket (IRS Form 3903 average $3,053–3,256 per return in TY2014–2017; AMSA about $4,300 in 2009) through structural utility-equivalents of US$18,285 (Bayer–Juessen 2008) to $312,146 for a hypothetical move (Kennan–Walker 2011, whose realized moves average −$80,768), and California surveys put housing cost first (IGS 2019: 71% of voters considering leaving; PPIC 2023: 34% of adults say housing costs make them consider leaving the state), and none of the surveys read offers crime, homelessness, immigrants or ethnic change as a reason; the closest is IGS's "Overcrowding/too many people" (38% of those considering). · model: claude-opus-5-5[1m]

# Moving costs and California-leaver surveys (literature worker, lane movers_reasons_2026_09_24)

Scope. Task 1: published per-move cost estimates for an interstate household move — (a) pecuniary cost (AMSA / ATA Moving & Storage Conference; commercial averages labelled as such), (b) IRS SOI moving-expense adjustment (Form 3903) returns and amounts for tax years ~2014–2017, (c) structural total (pecuniary + non-pecuniary) moving-cost estimates (Kennan & Walker 2011; Bayer & Juessen 2012; others), (d) optional home-sale transaction costs. Task 2: surveys of why people leave or consider leaving California (PPIC Statewide Survey, Berkeley IGS 2019/2021, California Policy Lab, LAO).

Rules followed: every number is quoted verbatim from a source fetched on 2026-09-24 (the PPIC February 2023 survey page on 2026-09-25), with URL and page/table; fetched text is cached under `../_cache/lit/`. Numbers seen only in search snippets are not reported.

## Task 1 — moving costs

### 1(a) Pecuniary cost: AMSA "Industry Fact Sheet" (trade-association figure)

Citation: American Moving & Storage Association, "Industry Fact Sheet" (5-page PDF; AMSA's own text: "We are the industry's national trade group … AMSA offers the most complete membership services in the industry"). Fetched copy is a reprint hosted by a third party (MI-BOX), PDF created 2012-09-07 per `pdfinfo`. [SOURCE: https://getmiboxsystem.com/the-market/industry_fact_sheet, accessed 2026-09-24; cached `_cache/lit/mibox_industry_fact_sheet.pdf` / `.txt`, p. 2 of the PDF text]

Verbatim:
> "Average cost of an interstate household move: About $4,300, based on an average weight of 7,400 pounds and average distance of 1,225 miles (2009) and including packing and other services that might be needed."
> "Average cost of an intrastate household move: About $2,300, based on an average weight …" (line continues on the same basis; intrastate figure given for contrast only)

| Measure | Value | Unit | Dollar year |
|---|---|---|---|
| Average interstate household move (professional mover, incl. packing/other services) | ~$4,300 | $ per household shipment (7,400 lb, 1,225 mi) | 2009 (nominal) |

Measures: the mover's bill for a full-service van-line shipment of household goods. Does not measure the household's own travel, lodging, lost work time, deposits, home-sale costs, or any non-pecuniary cost; it is per shipment (≈ per household), not per person, and it is a 2009 figure that later sites keep recycling. Industry sites fetched in search results (Allied, North American, 2026 "report" sites) still quote the same $4,300 / 7,400 lb basis; commercial sites give other averages (HomeAdvisor "$4,566", Allied cross-country "$7,780") but I did not fetch those pages, so they are not reported as numbers here. [GAP: original moving.org copy of the fact sheet not yet located]

### 1(b) IRS SOI moving-expense adjustment (Form 3903), tax years 2014–2017

Citation: IRS Statistics of Income, Individual Complete Report (Publication 1304), **Table 1.4 "All Returns: Sources of Income, Adjustments, and Tax Items, by Size of Adjusted Gross Income"**, row "All returns, total", columns headed "Moving expenses adjustment — Number of returns" and "Amount" (table column numbers (95)/(96) for TY2014–2016, (97)/(98) for TY2017). Header line: "(All figures are estimates based on samples—money amounts are in thousands of dollars)". Source lines: "Source: IRS, Statistics of Income Division, Publication 1304, August 2016" (TY2014), "September 2017" (TY2015), "August 2018" (TY2016).
Files [SOURCE, accessed 2026-09-24]: https://www.irs.gov/pub/irs-soi/14in14ar.xls · https://www.irs.gov/pub/irs-soi/15in14ar.xls · https://www.irs.gov/pub/irs-soi/16in14ar.xls · https://www.irs.gov/pub/irs-soi/17in14ar.xls ; cached in `_cache/lit/`; extraction [CALCULATION: `_cache/lit/soi_totals.py`].

| Tax year | Returns with moving-expense adjustment | Amount ($ thousands) | Average per return ($, nominal, same year) | All returns |
|---|---|---|---|---|
| 2014 | 1,128,284 | 3,444,883 | 3,053 | 148,606,578 |
| 2015 | 1,133,792 | 3,692,173 | 3,256 | 150,493,263 |
| 2016 | 1,114,665 | 3,486,633 | 3,128 | 150,272,157 |
| 2017 | 1,082,452 | 3,467,230 | 3,203 | 152,903,231 |

Average = Amount×1000 / Number of returns [CALCULATION]. Measures: the deductible, unreimbursed moving expenses claimed on a return for a work-related move (per return, i.e. per tax unit ≈ household). Does not measure moves that fail the IRS distance/time tests, employer-reimbursed costs, non-itemized items outside the Form 3903 definition (see Pub 521 note below), or any non-pecuniary cost; it covers intrastate as well as interstate job moves. [GAP filled: Pub 521 definition quoted below.]

**Form 3903 definition: IRS Publication 521 (2017).** Added 2026-09-24 by the resumed worker. [SOURCE: https://www.irs.gov/pub/irs-prior/p521--2017.pdf. PDF title "2017 Publication 521", 18 pp., created 2018-01-03. Accessed 2026-09-24; cached `_cache/lit/irs_p521_2017.pdf/.txt`. Page numbers are the printed "Page N" footers, which match the PDF pages.]
> p. 2: "You can deduct your moving expenses if you meet all three of the following requirements. Your move is closely related to the start of work. You meet the distance test. You meet the time test."
> p. 2: "In most cases, you can consider moving expenses incurred within 1 year from the date you first reported to work at the new location as closely related in time to the start of work."
> p. 3, Distance Test: "Your move will meet the distance test if your new main job location is at least 50 miles farther from your former home than your old main job location was from your former home."
> p. 4, Time Test for Employees: "If you are an employee, you must work full time for at least 39 weeks during the first 12 months after you arrive in the general area of your new job location (39-week test)."
> p. 7, Deductible Moving Expenses: "you can deduct the reasonable expenses of: Moving your household goods and personal effects (including in-transit or foreign-move storage expenses), and Traveling (including lodging but not meals) to your new home." … "You can't deduct any expenses for meals."
> p. 8: "Household goods and personal effects. You can deduct the cost of packing, crating, and transporting your household goods and personal effects and those of the members of your household from your former home to your new home." … "Travel expenses. You can deduct the cost of transportation and lodging for yourself and members of your household while traveling from your former home to your new home."
> p. 9, Nondeductible Expenses: "You can't deduct the following items as moving expenses." The list includes "Expenses of buying or selling a home (including closing costs, mortgage fees, and points)", "Expenses of entering into or breaking a lease", "Loss on the sale of your home", "Pre-move househunting expenses", "Return trips to your former residence" and "Security deposits (including any given up due to the move)".

What this means for the SOI averages above: the $3,053–3,256 per return covers only moving goods plus one trip, with lodging but no meals, for job-related moves that pass the 50-mile and 39-week tests. It excludes home-sale and lease costs, house-hunting and lost work time, and every move not tied to a job. It is a lower bound on the pecuniary cost of an owner household's move. [INFERENCE]

### 1(c) Structural total moving cost: Kennan & Walker (2011)

Citation: John Kennan and James R. Walker, "The Effect of Expected Income on Individual Migration Decisions," *Econometrica* 79(1), January 2011, 211–251, doi:10.3982/ECTA4657. [SOURCE: https://users.ssc.wisc.edu/~jfkennan/research/ECTA4657.pdf (published version, 42 pp., `pdfinfo` title verified), accessed 2026-09-24; cached `_cache/lit/kennan_walker_2011_ecta4657.pdf/.txt`]

Population (abstract, p. 211): "The model is estimated using panel data from the National Longitudinal Survey of Youth on white males with a high-school education." Sample (p. 220 area, §5): NLSY79 respondents who "completed high school by age 20", followed "from age 20 to the 1994 interview".

Verbatim (p. 232, Table IV "MOVING COST EXAMPLES"): "Young mover … $384,743"; "Average mover … $312,146".
Verbatim (p. 232, §6.2): "Since utility is linear in income, the estimated moving cost can be converted to a dollar equivalent. … For the average mover, the cost is about $312,000 (in 2010 dollars) if the payoff shocks are ignored."
> "the estimates in Table IV do not refer to the costs of moves that are actually made, but rather to the costs of hypothetical moves to arbitrary locations. In the model, people choose to move only when the payoff shocks are favorable, and the net cost of the move is, therefore, much less than the amounts in Table IV." … "if the location with the most favorable payoff shock is chosen, the expected net cost of the move is reduced by log(J − 1)/α0. Using the estimated income coefficient, this is a reduction of $271,959."
Verbatim (p. 233): "We estimate that such a subsidy [$10,000 per move] would lead to a substantial increase in the interstate migration rate: from 2.9% to about 4.9%."
Verbatim (p. 234–236, §6.3 "Average Costs of Actual Moves", Table V "AVERAGE MOVING COSTS"): "There is considerable variation in these costs, but for a typical move the cost is negative. The interpretation of this is that the typical move is not motivated by the prospect of a higher future utility flow in the destination location, but rather by unobserved factors yielding a higher current payoff in the destination location". Table V, Total row × Total column: "−$80,768 [124]" (124 moves); "From Home" total "−$147,930 [64]"; "To Home" total "$25,871 [43]".

| Measure | Value | Unit | Dollar year |
|---|---|---|---|
| Deterministic cost of a hypothetical move, "average mover" (Table IV) | $312,146 | $ per move, per person (utility-equivalent lump sum) | 2010 |
| Same, "young mover" (age 20, 1,000 mi) | $384,743 | same | 2010 |
| Reduction when mover picks best payoff-shock location | $271,959 | same | 2010 |
| Average cost of moves actually made (Table V, all 124 moves) | −$80,768 | same | 2010 [INFERENCE: dollar year taken from §6.2; Table V note does not restate it] |

Measures: the utility cost, in lifetime-dollar equivalent, that rationalizes how rarely young high-school-educated white men move across states; it bundles pecuniary and psychic costs. Does not measure an out-of-pocket bill, and the paper itself warns the headline $312k is for hypothetical moves to arbitrary states; for moves actually made the net cost is negative on average. Not estimated on women, college graduates, older adults, or households. [GAP filled below: the cost parameters are in Table II, not Table III; Table III holds the wage parameters.]

**Standard errors (added 2026-09-24, resumed worker).** Source: Table II "INTERSTATE MIGRATION, YOUNG WHITE MEN", journal p. 230 (PDF p. 21). I read the values from the rendered page because the text layer drops their decimal points. Note a: "There are 4,274 (person-year) observations, 432 individuals, and 124 moves." Table IV (p. 232) states the parameter vector it converts: "θ 4.790 0.312 …", so Table II column 1 underlies the $312,146 and $384,743 figures.

| Parameter (Table II, column 1) | θ̂ | σ̂θ | Relative SE [CALCULATION] |
|---|---|---|---|
| Disutility of moving (γ0) | 4.790 | 0.565 | 12% |
| Distance (γ1) (1000 miles) | 0.265 | 0.182 | 69% |
| Adjacent location (γ2) | 0.808 | 0.214 | 26% |
| Income (α0) | 0.312 | 0.100 | 32% |
| Column 4 (adds location-match preference): γ0 / α0 | 4.851 / 0.297 | 0.604 / 0.116 | 12% / 39% |

The paper gives no standard error or confidence interval for any dollar figure; the only "standard errors" in the text are those of Table II (p. 229: "The table gives estimated coefficients and standard errors for four versions of the model"). The dollar cost is proportional to 1/α0, so α0's 32% relative SE alone implies a wide interval around $312k. [INFERENCE: a delta-method interval would need the γ0–α0 covariance, which the paper does not report.]

### 1(c) continued: Bayer & Juessen (2008 working paper; 2012 *Review of Economic Dynamics*)

Citations.
- Working paper, the text I read: Christian Bayer and Falko Juessen, "On the Dynamics of Interstate Migration: Migration Costs and Self-Selection," IZA Discussion Paper No. 3330, February 2008. [SOURCE: IZA DP 3330 PDF, fetched by the earlier worker on 2026-09-24; cached `_cache/lit/bayer_juessen_iza_dp3330.pdf/.txt`. Table 2 was verified on the rendered page, PDF p. 21 = DP p. 19.]
- Published version: *Review of Economic Dynamics* 15(3), July 2012, 377–401, doi:10.1016/j.red.2012.02.002. I read only its abstract, on RePEc; ScienceDirect is paywalled. [SOURCE: https://ideas.repec.org/a/red/issued/10-90.html, accessed 2026-09-24; cached `_cache/lit/bayer_juessen_repec.html/.txt`]

Population and data. The paper uses aggregate state-pair flows, not individuals. DP p. 15: "the Internal Revenue Service (IRS) migration data, which is our empirical … states for the period 1989-2004"; "Income data is taken from the REIS database, CPI deflated, and in logs" (p. 15, footnote); Table 1 note (p. 18): "REIS/IRS data set, with data on 50 US states and D.C. over the period 1989-2004." The model agent is a household, calibrated to "a mean household income of US$ 45,000" taken from Storesletten, Telmer and Yaron (2004) (DP p. 16).

Verbatim, working paper (DP 3330):
> Abstract: "For US interstate migration, we obtain a cost estimate of less than one-half of an average annual household income. This is substantially smaller than the migration costs estimated by previous studies."
> Table 2, "Simulated moments estimation: structural parameter estimates" (p. 19), row "Migration Costs": "All Moments Matched 18,285¹ (2, 211)"; "w/o Average Migration Rate 18,571¹ (6756)"; "CRRA (log utility) 0.4762² (0.6863)". Notes: "¹ Migration cost estimate ĉ in US$ terms. ² exp (ĉ) − 1 measures the relative income gain necessary to offset migration costs. Standard errors in parenthesis."
> p. 19: "The estimated migration costs are US$ 18,285. This is a substantially smaller number than the estimates reported in previous contributions such as Davies, Greenwood, and Li (2001) or Kennan and Walker (2006)."
> p. 21 (log utility): "Our estimate of c = 0.4762 implies an estimated migration cost of US$ 32,738."
> Introduction (p. 2): "Davies, Greenwood, and Li (2001) report a cost estimate of about US$ 180,000 for each migration between US states, and Kennan and Walker (2003, 2006) conclude that, for a typical move, migration costs are between US$ 176,000 and US$ 270,000. This magnitude of migration costs corresponds to roughly 4-6 average annual household incomes."

Their own estimators that ignore the dynamic self-selection give larger costs, which shows how much the method moves the number (DP §6.2):
> "Migration cost estimates are with US$ 57,713 substantially higher in this setting [income autocorrelation set to zero]" (p. 23).
> Static conditional logit on data simulated with a true cost of US$18,285: "the conditional-logit estimation suggests a cost of US$ 40,576 … In comparison, 'true' and estimated costs correspond to 0.3 and 0.77 average annual incomes, respectively. … Adding measurement errors to the simulated income data drives the cost estimate up to US$ 99,457." (p. 25)
> Unconditional incentive distribution: "the estimated migration costs are with US$ 363,300 substantially larger." (p. 28)

Verbatim, published 2012 abstract (RePEc): "For US interstate migration, we obtain a cost estimate of roughly two-thirds of an average annual household income." The published estimate therefore differs from the working paper's (less than one-half, US$18,285). I did not read the published paper's dollar figure or its standard error. [GAP: published RED 2012 Table value and SE; paywalled]

| Measure | Value | SE | Unit | Dollar year |
|---|---|---|---|---|
| DP 3330 baseline, all moments matched | US$18,285 | 2,211 | per migration (household), total cost incl. non-pecuniary | not stated [GAP]; income is "CPI deflated", base year not given |
| DP 3330, without the average-migration-rate moment | US$18,571 | 6756 | same | same |
| DP 3330, log utility | US$32,738 (from c = 0.4762, SE 0.6863) | none in dollars | same | same |
| RED 2012 published | "roughly two-thirds of an average annual household income" | not read | share of income | not read |

What this measures: the per-move cost, pecuniary and psychic together, that makes the model reproduce aggregate state-to-state IRS flows once dynamic self-selection is tracked. It rests on a pure income-incentive model; DP p. 20 acknowledges the objection that "we attribute all migration to be driven by the income incentive." It does not describe any demographic subgroup, and the working-paper and published numbers differ. [INFERENCE, not a sourced number: two-thirds of the DP's US$45,000 calibration would be about US$30,000, if the published version keeps that calibration. Unverified.]

**Range for the ledger's cost column, from sources read.** The out-of-pocket mover bill is about $4,300 (AMSA, 2009 dollars; 1(a)). The IRS deductible job-move expense averages $3,053–3,256 per return (TY2014–2017, nominal; 1(b)). Structural total costs run from US$18,285 (Bayer–Juessen 2008 baseline) through about 0.67 of annual household income (Bayer–Juessen 2012) to $312,146 for a hypothetical move by K&W's "average mover" (2010 dollars). K&W themselves put the average realized move at −$80,768 (Table V), because moves happen when payoff shocks are favorable. The structural figures are utility-equivalents for movers who chose to move, not resource costs, and the sign and size depend on the estimator. [FRAMING-SENSITIVE: whether a revealed-preference move counts as a "harm" at all is a framing choice; the structural literature implies that the average voluntary move is a net gain to the mover.]

### 1(d) Home-sale transaction cost for owners: FTC and DOJ (2007)

Citation: Federal Trade Commission and U.S. Department of Justice, "Competition in the Real Estate Brokerage Industry: A Report by the Federal Trade Commission and U.S. Department of Justice," April 2007, 78 pp. [SOURCE: https://www.ftc.gov/sites/default/files/documents/reports/competition-real-estate-brokerage-industry-report-federal-trade-commission-and-u.s.department-justice/v050015.pdf, accessed 2026-09-24; cached `_cache/lit/ftc_doj_brokerage_2007.pdf/.txt`]

Verbatim (printed p. 30, PDF p. 35):
> "from 1998 to 2005, housing prices rose 37 percent in real terms and, although national average commission rates appear to have fallen from 5.5 percent to 5 percent, average brokerage fees per transaction rose 26 percent in real terms during the same period."

| Measure | Value | Unit | Year |
|---|---|---|---|
| National average brokerage commission rate | 5.5% → 5% | share of sale price | 1998 → 2005 |

What this measures: the seller's broker commission as a share of sale price, as a national average. It excludes transfer taxes, title and escrow, seller concessions, repairs and staging, the buyer-side closing costs at the destination, and the price effect of a hurried sale. It is not a total transaction cost, it applies only to leavers who own and sell, and it is 2005 practice. Applied to an owner-leaver, the commission is about 0.05 × sale price. [INFERENCE] The p. 35 passage "In most markets, the prevailing rate is either 6 or 7 percent" is an indented quotation whose speaker I did not confirm, so I do not report it as the agencies' finding.
[GAP: an academic or government estimate of total seller-side transaction costs (commission plus taxes and closing) as a share of value was not fetched in this pass. The next query would be Haurin & Gill (2002, *Journal of Urban Economics*) or a CFPB closing-cost report.]

## Task 2 — surveys of why people leave California

Added by the resumed worker, 2026-09-24/25. Stated consideration is not a move: the surveys below measure intentions or attitudes, while the lane's CPS `WHYMOVE` measures the reason actual movers gave. [INFERENCE]

### 2(a) Berkeley IGS Poll Release #2019-08 (27 September 2019)

Citation: Mark DiCamillo, "Release #2019-08: Leaving California: Half of State's Voters Have Been Considering This; Republicans and Conservatives Three Times as likely as Democrats and Liberals to be Giving Serious Consideration to Leaving the State," Berkeley IGS Poll, 27 September 2019, 12 pp. [SOURCE: https://escholarship.org/uc/item/96j2704t; PDF https://escholarship.org/content/qt96j2704t/qt96j2704t.pdf, accessed 2026-09-24. Cached `_cache/lit/igs_2019_08_leaving_ca.pdf/.txt`, byte-identical in size to the lead's `igs_2019_08.pdf/.txt`. Page numbers are PDF pages.]

Sample (p. 11, "About the Survey"): "The poll was administered online in English and Spanish September 13-18, 2019 among 4,527 registered voters statewide." The sample came from "Samples of registered voters with email addresses … provided to IGS by Political Data, Inc." and was post-stratified. Sampling error (p. 12): "approximately +/- 2 percentage points at the 95% confidence level." The population is registered voters, not all adults or all residents.

Question wording (p. 11, "Questions Asked"), verbatim:
> "Have you given any consideration recently to moving out of California? (1) Yes, am giving serious consideration to moving out of California (2) Yes, am giving some consideration to moving out of California (3) No, but am considering moving to another location within California (4) No, am not considered a move"
> "What is the main reason why you have considered moving out of the state? You may select more than one reason, if you wish. (ORDERING OF REASONS DISPLAYED WAS RANDOMIZED) (1) High cost of housing (2) High taxes (3) Lack of job opportunities (4) Family considerations (5) Overcrowding/too many people (6) The state's political culture (7) Other reasons"

Table 1 (p. 3), "Are you giving any consideration to moving out of California? (among California registered voters)", in %:

| Group | Serious | Some | Moving within CA | Not considering |
|---|---|---|---|---|
| Total registered voters | 24 | 28 | 10 | 38 |
| Democrats | 14 | 24 | 13 | 48 |
| Republicans | 40 | 31 | 3 | 26 |
| No Party Preference/other | 23 | 32 | 11 | 34 |
| White non-Hispanic | 26 | 30 | 6 | 37 |
| Latino | 19 | 24 | 15 | 42 |
| Asian American | 17 | 27 | 12 | 44 |
| African American | 27 | 31 | 17 | 25 |

Table 2 (p. 5), "Main reasons given for considering moving out of California (among registered voters giving serious or some consideration to moving out of state)", multiple responses allowed, in %:

| Group | High cost of housing | High taxes | State's political culture | Overcrowding | Family considerations | Lack of job opportunities | Other reasons |
|---|---|---|---|---|---|---|---|
| Total considering a move | 71 | 58 | 47 | 38 | 14 | 13 | 26 |
| Democrats | 77 | 36 | 11 | 33 | 13 | 14 | 24 |
| Republicans | 63 | 77 | 85 | 45 | 12 | 12 | 26 |
| No Party Preference/other | 72 | 60 | 43 | 35 | 16 | 13 | 29 |
| White non-Hispanic | 67 | 59 | 51 | 39 | 14 | 11 | 27 |
| Latino | 76 | 56 | 40 | 38 | 11 | 15 | 21 |
| Asian American | 76 | 56 | 39 | 34 | 16 | 13 | 35 |
| African American | 83 | 57 | 27 | 35 | 9 | 22 | 30 |

The text on p. 2 says: "The high cost of housing (71%) is the most common reason given by voters for wanting to leave California. However, high taxes (58%) and the state's political culture (46%) are also prominently mentioned, particularly by Republicans and conservatives." Note that the text says 46% for political culture where Table 2 prints 47. The responses sum to 267% because multiple answers were allowed. [CALCULATION] Share of all registered voters naming each reason = 52% considering × Table 2 share: housing ≈ 37%, taxes ≈ 30%, political culture ≈ 24%, overcrowding ≈ 20%. [CALCULATION]

Answer options relevant to this lane. The reason list offered no crime, homelessness, schools, neighborhood, "quality of life", immigration or ethnic/demographic-change option. The nearest item is "(5) Overcrowding/too many people", which 38% of considerers chose (39% of white non-Hispanic and 38% of Latino considerers). That item concerns crowding and population size; it cannot be read as a statement about immigrants or ethnic composition. [INFERENCE] "Other reasons" took 26%, and the release shows no breakdown of what those respondents meant.

### 2(b) PPIC Statewide Survey, "Californians and Their Government", February 2023

Citation: Mark Baldassare, Dean Bonner, Rachel Lawler and Deja Thomas, "PPIC Statewide Survey: Californians and Their Government," Public Policy Institute of California, February 2023. [SOURCE: https://www.ppic.org/publication/ppic-statewide-survey-californians-and-their-government-february-2023/. curl returned HTTP 403, so the page was read through Exa web_fetch on 2026-09-25; that text is cached as `_cache/lit/ppic_sw_feb2023_exa.txt`.]

Methodology (section "Methodology"): "Findings in this report are based on a survey of 1,539 California adult residents. … Interviews were conducted from January 13–20, 2023." "The survey was conducted by Ipsos, using its online KnowledgePanel, in English and Spanish". KnowledgePanel members "are recruited through probability-based sampling".

Item, verbatim ("Questions and Responses", Q35):
> "35. Does the cost of your housing make you and your family seriously consider moving away from the part of California you live in now? (if yes, ask: " Does it make you consider moving elsewhere in California, or outside of the state?") 11% yes, elsewhere in California 34% yes, outside the state 55% no 1% don't know"

Text (section "Homelessness and Housing Affordability"): "45 percent say the cost of their housing makes them and their family seriously consider moving out of the part of California where they currently live, with most (34%) saying they would move outside the state. Last March, similar shares (46%) said they were considering a move because of the cost of their housing."

This item names the reason, housing cost, in the question. It measures how many people housing costs push toward moving; it cannot rank housing against other reasons. The same survey asks about crime only as a local problem, never as a reason to move. Q39: "How much of a problem are violence and street crime in your local community today? … 30% big problem 46% somewhat of a problem 24% not a problem". Its open-ended "most important issue" question (Q1) returns "20% homelessness", "5% immigration, illegal immigration" and "4% crime, gangs, drugs". Neither item is tied to moving.

### 2(c) PPIC blog "Who's Leaving California—and Who's Moving In?" (2021 and 2023 versions)

2021 version: Hans Johnson, blog post, 6 May 2021. [SOURCE: https://www.ppic.org/blog/whos-leaving-california-and-whos-moving-in/. This is the PDF print cached by the lane lead on 2026-09-24, `_cache/lit/ppic_whos_leaving_2021.pdf/.txt`; I read the cached text.]
> p. 2/3: "During the 2010s about 6.1 million people moved from California to other states, while only 4.9 million people moved to California from other parts of the country."
> p. 2/3: "California has been losing lower- and middle-income residents to other states for some time while continuing to gain higher-income adults."
> p. 3/3: "Most people who move across state lines do so for economic or family reasons. The vast majority of adults who left California in the 2010s cited jobs (49%), housing (23%), or family (20%) as the primary reason (according to the Current Population Survey). The PPIC Statewide Survey finds that one-third of Californians have seriously considered leaving the state because of housing costs."

2023 version: Hans Johnson and Eric McGhee, blog post, 21 March 2023. The PDF title is "Who's Leaving California—and Who's Moving In? March 2023", 5 pp., same URL. The post says: "Earlier versions of this post were published on May 6, 2021 and March 28, 2022." [SOURCE: same URL; PDF cached by the lead as `_cache/lit/ppic_whos_leaving_2023.pdf`. Its text layer is garbled under both `pdftotext` and `pdftotext -layout`, so I transcribed the quotes below from the rendered pages 1–5.]
> p. 2/5: "from 2010 through 2021 about 7.7 million people moved from California to other states, while only 5.8 million people moved to California from other parts of the country." … "a record net outflow of 407,000 from July 2021 to July 2022."
> p. 4/5: "Among recent higher-income Californians leaving the state, over half (53%) report working from home."
> p. 4/5: "Most people who move across state lines cite employment, housing, or family as the primary reason. Since 2015, California has experienced net losses of over 500,000 adults who cite housing as the primary reason, according to the Current Population Survey. About half of those who leave the state buy a house in their new state, whereas only one-third of those moving to California buy a house. Net losses among those who cite jobs as the primary reason totaled 309,000 and among those who cite family 307,000. The PPIC Statewide Survey finds that 34% of Californians have seriously considered leaving the state because of high housing costs. Political outlook might also play a role for some movers, as conservatives are more likely to contemplate leaving the state than liberals."

Both versions report the CPS reason groups for all leavers: jobs, housing and family. Neither version reports the CPS "better neighborhood/less crime" category or a split by nativity. The lane's own `WHYMOVE` tabulation fills that gap. The 2021 shares (jobs 49%, housing 23%, family 20%, adults leaving in the 2010s) are an outside check for it.

### 2(d) Crime, neighborhood, homelessness, quality of life, demographic change: what the surveys offer

- **Berkeley IGS 2019**: none of these was offered as a reason. The closest item is "Overcrowding/too many people", at 38% of considerers, about 20% of registered voters. [CALCULATION]
- **PPIC Statewide Survey, February 2023**: the moving item is prompted by housing cost only. Crime (30% "big problem" locally) and homelessness appear as issue items, not as reasons to move.
- **PPIC blogs, 2021 and 2023**: report only the CPS reason groups jobs, housing and family. Neither reports a neighborhood or crime share.
- **Immigrants or ethnic change as a reason**: no item in any source read asks about it. This absence holds for the sources read, not for all surveys. [GAP: see next queries]

### Task 2 gaps and next queries

- [GAP] I found no Berkeley IGS 2021 release on leaving California. The IGS archive page I fetched (`_cache/lit/igs_poll_archives.txt`) lists only 2017–2019 releases. Release #2017-16 (19 September 2017, on housing costs and moving) is listed there but was not read. A search result showed a 2021 UC San Diego survey (15 April–8 May 2021, 2,768 adults, Luc.id) that repeated the IGS 2019 wording. I saw it only as a docslib mirror in search output, did not read it, and report none of its numbers. Next: the original UCSD report PDF, and escholarship.org searches for "Berkeley IGS Poll 2023 leaving California", since a 2023 release may carry crime or homelessness reasons.
- [GAP] California Policy Lab and LAO were not fetched within the budget. Next: LAO "California Losing Residents Via Domestic Migration" (2023) and CPL "Pandemic Pushes" (2021). These cover characteristics of leavers, not stated reasons.
- [GAP] The PPIC Statewide Survey of November 2025 has a lack-of-well-paying-jobs moving item. I saw it only in a search snippet and did not fetch it, so no number is reported.

## Sources tried and failed

- **Bayer & Juessen (2012, *RED*) full text**: ScienceDirect is paywalled (RePEc: "Access to full texts is restricted to ScienceDirect subscribers"). Only the published abstract was read. The published dollar estimate and its SE are unread.
- **ppic.org with curl**: HTTP 403 (exit 56) on the February 2023 survey page, the "Who's Leaving California" blog and "Californians and Housing Affordability" (2017). Workarounds: Exa web_fetch for the February 2023 survey; the lead's cached PDF prints for the blog. The 2017 report was not read.
- **PPIC 2023 blog PDF text layer**: `pdftotext` and `pdftotext -layout` both return 350 bytes of glyph codes (the font lacks a Unicode map). I read the rendered pages 1–5 instead, which worked.
- **Berkeley IGS 2021 release on leaving**: not found. The IGS archive page covers only 2017–2019.
- **AMSA original on moving.org**: not located (first worker's gap). The figure comes from a third-party reprint.
- **California Policy Lab, LAO, a total home-sale transaction-cost source, and the PPIC 2017 report**: not attempted within the budget; next queries listed above.
- The first worker's own failed attempts before its rate-limit stop were not recorded in this file and cannot be reconstructed.

Model: claude-opus-5-5[1m]
