claude-opus-5[1m]

**Verdict:** The repo's 14–15M is not too low. On the definition every publisher
actually uses — no permanent status, quasi-legal included — the central range is
**14.6–15.8M for mid-2024** and **15.4–16.7M for January 2025**, each with its
publisher's own coverage adjustment applied. On the narrow definition — no lawful
status and no protection from removal of any kind — the range is **8–9.5M**. The
stock has been falling since early 2025: the most recent reading anywhere is 13.5M for
July 2026. No defensible definition reaches 40 million. The largest number the ACS can
produce for any unauthorized-adjacent concept is **38.1M**, and that already requires
applying a recent-arrival undercount rate to green-card holders and foreign students.
40M is reachable only by counting US citizens: non-citizens plus everyone US-born
sharing their household is 42.2M, and the whole foreign-born population is 50.3M.

Arms 1, 2, 3, 4 and 6 landed in full. Arm 5 landed partially and its gaps are named
in §7.

---

## 1. The definitional fact that reframes the question

Every published residual estimate — DHS, Pew, CMS, MPI and CIS alike — **already
counts** parolees, TPS holders, DACA recipients and pending asylum applicants as
unauthorized. The headline figures are the *broad* definition, not the narrow one.
Asking for "the number including quasi-legal categories" does not raise the published
figure; asking for the number excluding them lowers it by 5–6 million.

DHS OHSS, verbatim [SOURCE: OHSS April 2024, "Definitions"]:

> The resident unauthorized immigrant population is defined as all foreign-born
> noncitizens who are not legal residents as defined above. … Persons who are
> beneficiaries of Temporary Protected Status (TPS), Deferred Action for Childhood
> Arrivals (DACA) or other forms of prosecutorial discretion, or who are residing in
> the United States while awaiting removal proceedings in immigration court are
> included among the estimates of the unauthorized population. … Individuals who were
> paroled into the United States are considered to be unauthorized immigrants until
> they are admitted or otherwise acquire immigration status.

Pew is the only publisher that splits its own headline [SOURCE: Pew, August 21 2025]:
of 14.0M in July 2023, **8.0M had no deportation protection** and **6.0M had some**
(asylum applicants 2.6M, border releases 1.0M, parole 0.7M, crime and violence victims
0.7M, TPS 0.65M, DACA 0.6M). MPI puts the mid-2024 liminal population at "a maximum of
6.3 million people — or 40 percent", noting that overlap makes the true share
"probably substantially lower". CMS puts it at 5.4M of 14.6M and says so bluntly:
"More than one-third of the 'undocumented' (5.4 million) in these estimates are, in
fact, documented and known to the federal government."

**Narrow definition, mid-2024:** 15.75 − 6.32 = 9.4M (MPI, and a floor, because the
liminal count is a maximum); 14.61 − 5.4 = 9.2M (CMS); Pew's 8.0M for July 2023 is the
one directly estimated split. Range **8–9.5M**.

## 2. Arm 1 — published estimates on one table

| Source | Ref. date | Estimate | Survey | Quasi-legal | Coverage adjustment | Mexico |
|---|---|---|---|---|---|---|
| DHS OHSS | 2022-01-01 | 10.99M | ACS | included | 13% at arrival, −7.5%/yr of presence | 44% |
| Pew | 2023-07-01 | 14.0M | ACS (augmented) | included, 6.0M | applied, rate not printed | 4.3M (30%) |
| MPI (superseded) | 2023-07-01 | 13.7M | ACS | included, ~4M | applied, rate not printed | — |
| MPI (revised) | 2023-07-01 | 14.7M | ACS | included | revised upward, rate not printed | — |
| CMS | 2024-07-01 | 14.61M | ACS 2024 | included, 5.4M | 5% pre-2021, 37% for 2021–24 (16% overall) | 5.1M (35%) |
| MPI | 2024-07-01 | 15.75M | ACS | included, max 6.3M | applied, rate not printed | 5.52M (35%) |
| CIS | 2025-01-01 | 15.4M → 15.8M | monthly CPS | included | 2.25% flat | — |
| CIS | 2026-07-01 | 13.1M → 13.5M | monthly CPS | included | 2.25% flat | — |

Full quotes: `derived/published_definitions.md`. Machine-readable: `sources.json` and
`derived/published_estimates.csv`.

Two things the table exposes. **CIS gets the highest number with the smallest coverage
adjustment** — 2.25% against CMS's 16%. The gap comes entirely from a smaller estimate
of the legal stock, not from a bolder undercount assumption, so "CIS assumes a big
undercount" is the wrong criticism of their number. And the most recent reading
available anywhere is CIS's July 2026 figure of 13.5M, down 2.3M from its own January
2025 figure.

## 3. Arm 2 — residual reproduced on repo microdata [CALCULATION]

Same rule list (Borjas 2017), two surveys, no coverage adjustment added:

| Survey | Residual | SE | Mexico-born | Foreign-born |
|---|---|---|---|---|
| CPS ASEC 2025 | 14,896,401 | 316,399 | 4,567,144 | 53,118,195 |
| ACS 2024 1-year PUMS | 12,973,901 | 98,154 | 3,963,961 | 50,280,846 |

The CPS figure reproduces ladder 85 (14.9M / 4.57M) exactly, using
`status_impute_2026_09_16/impute_status.py` imported unmodified. The ACS figure applies
the same rules mapped to ACS variables; rule (f), subsidised housing, has no ACS
counterpart and is dropped, which makes the ACS residual *larger* than a like-for-like
comparison would be. The 1.9M gap between the surveys is therefore real and runs the
opposite way from what the missing rule predicts.

Arrival structure, CPS ASEC 2025: 3,796,130 of the residual arrived 2022 or later,
1,578,270 in 2020–2021. The repo's note that the CPS under-samples 2022–24 arrivals is
confirmed in direction, but the comparison figure should change: CBO's *net*
other-foreign-national inflow for 2022–24 is **5.7M**, not 8.7M, and net is the right
quantity to compare against a stock.

Rule-list sensitivity (`derived/rule_sensitivity.csv`), ACS 2024:

| Variant | Residual | vs published rules |
|---|---|---|
| Borjas as published | 12,973,901 | — |
| occupation rule (h) dropped | 13,253,873 | +2.2% |
| wide refugee-origin list | 12,400,432 | −4.4% |
| both | 12,668,426 | −2.4% |

## 4. Arm 3 — coverage, where the whole spread lives

One counted ACS base, six coverage assumptions (`derived/coverage_grid.csv`):

| Scheme | Adjusted residual | Multiplier | Kind |
|---|---|---|---|
| none | 12,973,901 | 1.000 | — |
| CIS, 2.25% flat | 13,272,533 | 1.023 | assumption |
| **2020 PES, Hispanic net undercount 4.99%** | **13,655,300** | **1.053** | **measurement** |
| DHS OHSS, 13% at arrival decaying 7.5%/yr | 13,953,938 | 1.076 | assumption |
| CMS, 5% pre-2021 / 37% for 2021–24 | 15,856,155 | 1.222 | assumption |
| CMS's highest country rate (65%) on every recent arrival | 21,079,770 | 1.625 | upper bound |

The rule list moves the answer by ±4%. The coverage assumption moves it by +62%. Split
by arrival cohort (`derived/coverage_grid_by_cohort.csv`) the entire spread sits in the
2021–2024 cohort: 4.11M counted becomes 4.21M, 4.33M, 4.65M, 6.53M or 11.75M depending
on whose assumption you take. Every cohort before 2021 moves by less than 6% under any
scheme.

**The one measured rate in the grid is the smallest but one.** The 2020 Census
Post-Enumeration Survey found "a statistically significant undercount rate of 4.99%"
for the Hispanic or Latino population, against a 1.64% *overcount* for non-Hispanic
Whites and a national net coverage error of −0.24% that was not significantly
different from zero [SOURCE: US Census Bureau, press release CB22-CN.02, March 10
2022]. That is a net rate for all Hispanics in the household population in a decennial
census, not an omission rate for recent unauthorized arrivals during a border surge, so
it is a floor rather than a substitute. But it is the only number in the column that
was measured rather than assumed, and it supports a multiplier near 1.05, not CMS's
1.22.

**The ACS 2024 weights already carry a coverage adjustment [CALCULATION].** The Census
Bureau's Vintage 2024 estimates raised net international migration for July 2021–June
2022 by 69.5% and for July 2022–June 2023 by 101.7% over Vintage 2023, because
"recent humanitarian migrants, the group with the most significant growth in our
benchmark data, were also the least likely to be included in the ACS"; the Bureau
"adjusted our ROYA-based, foreign-born immigration estimates upward to account for 75%
of the humanitarian migrants in our Benchmark Database" [SOURCE: Census Bureau, Random
Samplings blog, December 19 2024]. The ACS 2024 1-year file is controlled to those
estimates: this lane's weighted ACS total is 340,110,990 against the published Vintage
2024 national figure of 340,110,988, a difference of two people.

So "counted, unadjusted" overstates how raw the 12.97M is. The correction is partial,
not total — the Vintage 2024 adjustment enters through population controls by state,
age, sex and race-ethnicity, not through a targeted reweight of recent foreign-born
respondents, so extra weight is spread across everyone in a control cell rather than
landing on the arrivals it was meant for. But layering CMS's 37% on top of a
Vintage-2024-controlled base is, in part, adjusting twice. This is a genuine tension
with CMS's construction, not a refutation of it: CMS justifies its recent-arrival
factor against DHS release counts (their Table A2), not against the ACS weights.

The same caution applies with more force to the CPS. Applying the grid to the CPS
residual (`derived/cps2025_coverage_grid.csv`) gives 14.90M → 15.24M (CIS) → 18.13M
(CMS). **The 18.1M figure should not be quoted.** The ASEC 2025 weights use the same
Vintage 2024 controls.

CMS's own arithmetic, for the record [SOURCE: Warren et al., *JMHS*, July 2026, Table
A1]: total undercount added 2,290,000 on a published 14,610,000 (16%), of which
1,755,000 sits on the 4,750,000 who entered 2021–2024 (37%) and 535,000 on the
9,860,000 who entered 1982–2020 (5%). The implied ACS-counted base is 12.32M — within
5% of this lane's independently computed 12.97M on the same survey.

## 5. Arm 4 — stock-flow from January 2022 forward

CBO's other-foreign-national category is defined as people who entered illegally, who
overstayed a temporary status, or who were paroled in — operationally the same universe
as the DHS residual. CBO's net series [SOURCE: CBO, *The Demographic Outlook: 2026 to
2056*, January 2026, Appendix B]: −130,000/yr average 2010–2019, then 830,000 (2021),
2.0M (2022), 2.4M (2023), 1.3M (2024), **−360,000 (2025)**.

Rolling the DHS January 2022 residual forward on that series
(`derived/stock_flow_cbo.csv`):

| As of | Opening | CBO OFN net | Closing |
|---|---|---|---|
| 2022-01-01 | — | — | 10,990,000 |
| 2023-01-01 | 10,990,000 | +2,000,000 | 12,990,000 |
| 2024-01-01 | 12,990,000 | +2,400,000 | 15,390,000 |
| 2025-01-01 | 15,390,000 | +1,300,000 | **16,690,000** |
| 2026-01-01 | 16,690,000 | −360,000 | **16,330,000** |

**The stock-flow identity gives 16.7M for January 2025**, above every survey reading:
0.9M above CIS and 1.8M above this lane's CPS residual for March 2025. The identity
omits mortality, which is not part of a net-migration concept; on a young population
that is roughly 40–50k a year, so correcting for it widens the gap slightly rather than
closing it.

For 2026 the two sources diverge sharply. CBO estimates a 360,000 decline in 2025; CIS
measures the CPS foreign-born population falling 2.9M between January 2025 and July
2026 and puts the illegal population down 2.3M. Both cannot be right. The survey
reading depends on CPS response behaviour under intensified enforcement, which CIS
itself flags. The CBO figure depends on an emigration model CBO rebuilt for 2025 and on
interior removals extrapolated from seven months of ICE data obtained under FOIA.

**Dependence on the residency share.** CBP's own disposition table
(`derived/stock_flow_dispositions.csv`, DHS OHSS enforcement monthly tables, November
2024 edition — the last published) gives FY2022–24 USBP releases, OFO paroles and HHS
transfers of 3,809,390, plus known gotaways of 1,625,929 (FY24 partial), against DHS
removals of 610,290. If every one of those releases and gotaways became a resident they
account for 5.44M of CBO's 5.70M net for 2022–24, leaving only 265,000 for visa
overstays net of all other exits — implausibly little. At a 70% residency share they
account for 3.80M, leaving 1.90M for overstays net of exits, which is the plausible
region. **The implied stock moves 2.7M across a 50%-to-100% residency assumption**
(`derived/stock_flow_sensitivity.csv`). That single parameter carries more of the
answer than any survey choice.

Gotaway provenance is uneven and is carried with the number: FY21 389,155 traces to a
DHS Border Security Metrics Report, FY22 737,244 to an ICE budget justification, FY23
694,685 to the House Committee on Homeland Security's reading of CBP data, and the FY24
figure of 194,000 through June only to a journalist's posting of unpublished CBP data —
that last is **[UNVERIFIED]**. Gotaways are also not additive on top of CBO: CBO's 2025
inflow decomposition already includes "people who entered without encountering a CBP
official (50,000)" as one of its four components.

## 6. Arm 6 — the 40 million test

`derived/forty_million_ladder.csv`, all ACS 2024 unless noted:

| Definition | Population | ≥40M |
|---|---|---|
| A. Borjas residual, counted | 12,973,901 | no |
| B. A with the DHS coverage model | 13,953,938 | no |
| C. A with the CMS coverage model | 15,856,155 | no |
| D. A with CMS's highest country rate on every recent arrival | 21,079,770 | no |
| E. CPS ASEC 2025 residual, counted | 14,896,401 | no |
| F. Every non-citizen | 24,402,333 | no |
| G. F with the upper-bound coverage model | 38,078,940 | no |
| H′. F plus US-born children under 18 living with a non-citizen | 34,536,637 | no |
| H. F plus every US-born person living with a non-citizen | 42,156,871 | **yes** |
| I. Every foreign-born person | 50,280,846 | **yes** |

**The maximal reading that still names an unauthorized-adjacent population is 38.1M**,
and it is already indefensible: it applies a 65% undercount rate — CMS's highest
published country figure, for Ecuadorians who arrived 2021–2024 — to every non-citizen
in the country, green-card holders, foreign students and H-1B workers included. CMS's
own rate for pre-2021 arrivals is 5%, and the only measured rate anywhere in this lane
is the PES's 4.99%.

Put the other way: reaching 40M by scaling the non-citizen population requires a
multiplier of **1.639**, an implied undercount of **39% of every non-citizen**. Nothing
published supports a rate near that outside the most recently arrived cohort.

The two rungs that clear 40M both work by counting US citizens. H adds 17,754,538
US-born people who live with a non-citizen — a mixed-status-household count, and those
added people are citizens by birth. I is the whole foreign-born population, about half
of it naturalised citizens.

And, as the brief anticipated: 40.9M is close to the Mexican-origin population across
all generations, which is overwhelmingly US citizens and is a different population
entirely.

## 7. Arm 5 and the coverage literature — what landed and what did not

Two research agents were dispatched for the administrative anchors and the coverage
literature; both exhausted their turn limits without returning. The two highest-value
coverage items were then fetched directly and are used above: the **2020
Post-Enumeration Survey** (§4) and the **Census Bureau's December 2024 net
international migration revision** (§4). The latter turned out to be load-bearing — it
is what makes the double-adjustment tension visible.

**NOT OBTAINED, and therefore used nowhere above:** SSA Earnings Suspense File wage
items and dollars; IRS ITIN filer counts; Mexican matrícula consular issuance;
emergency-Medicaid enrolment; city shelter intake totals for New York, Chicago, Denver
and Massachusetts; K-12 recent-arrival enrolment; the Jensen et al. (2015) Census
coverage factors by age, sex and Hispanic origin that CMS's 1.21 baseline comes from;
and the Van Hook ACS-coverage papers. The Jensen table is the most valuable of these
and is the obvious next fetch: it would let the coverage grid be rebuilt on measured
factors rather than publishers' assumptions.

The anchors are worth having but would not move the verdict, and the reason is worth
stating so the gap is not mistaken for a missing datum that would. Each is a partial
signal with a known mismatch to the stock. An Earnings Suspense File wage item is a
job-year, not a person, and includes name-mismatch errors by citizens. An ITIN goes to
some lawfully present people and is not requested by many unauthorized workers. A
matrícula goes to Mexican nationals regardless of status and can be renewed. A shelter
intake is an event, not a resident. Each bounds; none point-estimates.

## 8. Answer to "is 14–15M too low"

No, not for its reference date, and the direction of the error is the opposite of the
one the question assumes.

The repo carries 14.9M from the CPS ASEC 2025 residual, reference March 2025. For that
date the published range is 15.4–15.8M (CIS, the only publisher with a January 2025
figure) and the stock-flow identity gives 16.7M, so 14.9M is at the low end — by 1–2M,
not by 25M. Against ACS-based estimates for mid-2024 the picture inverts: this lane's
ACS residual is 12.97M and CMS's ACS-counted base is 12.32M, so the CPS residual of
14.9M is the *high* survey reading. It is also, in substance, partly coverage-adjusted
already, because the ASEC 2025 weights embed the Census Bureau's December 2024 upward
revision.

Three qualifications the repo should carry with the number.

First, **the reference date now matters more than the method.** The stock peaked
somewhere in 2024 or early 2025 and has been falling since. CIS's July 2026 reading is
13.5M and CBO's 2025 net flow is −360,000. A ledger built on ASEC 2025 describes a
population at or near its maximum, which is the right choice for a peak-burden
question and the wrong one for a steady-state question.

Second, **the definition choice is worth 5–6M and should be stated every time.** 14.9M
is the broad reading. The narrow reading is 8–9.5M. For a fiscal ledger this is not
cosmetic: parolees, TPS holders and work-authorised asylum applicants have work
authorisation and different programme eligibility from people with no status at all.

Third, **nothing supports a figure near 40M**, and the arithmetic that approaches it is
arithmetic on US citizens.

### Disconfirmation

Two arms were run that could have reversed the headline upward, and both partly did.
The stock-flow identity (§5) puts January 2025 at 16.7M, above every survey. The CMS
coverage model applied to this lane's own ACS residual (§4) gives 15.86M, and the
upper-bound model gives 21.08M. Against those, three findings push down: the ACS
counted residual is 12.97M; the only *measured* coverage rate in the grid is 4.99% and
supports a 1.05 multiplier; and the ACS and CPS weights already carry part of the
adjustment that CMS adds on top. The net of the four is that 14–15M is a defensible
central figure for 2024–25 with real uncertainty of roughly ±2M, and that the upside
tail runs to about 17M, not to 40M.

---

## Draft memo section (liftable)

> ### How many unauthorized residents are there
>
> Every organisation that publishes a residual estimate — DHS, Pew, the Center for
> Migration Studies, the Migration Policy Institute and the Center for Immigration
> Studies — counts parolees, TPS holders, DACA recipients and pending asylum applicants
> as unauthorized. DHS states it plainly: "Individuals who were paroled into the United
> States are considered to be unauthorized immigrants until they are admitted or
> otherwise acquire immigration status." [SOURCE: DHS OHSS, *Estimates of the
> Unauthorized Immigrant Population Residing in the United States: January 2018–January
> 2022*, April 2024] The published headline is therefore the broad definition. The
> narrow one — no lawful status and no protection from removal — is 5 to 6 million
> smaller.
>
> On the broad definition the estimates for mid-2024 run 14.6M (CMS) to 15.8M (MPI),
> and CIS reads 15.8M for January 2025 from the CPS. [SOURCE: Allen, Warren and Pacas,
> *JMHS*, July 2026; Ruiz Soto, Gelatt and Van Hook, MPI, 2026; Camarota and Zeigler,
> CIS, March 2025] Pew's 14.0M for July 2023 splits into 8.0M with no deportation
> protection and 6.0M with some. [SOURCE: Passel and Krogstad, Pew Research Center,
> August 21 2025] On the narrow definition the mid-2024 figure is 8 to 9.5 million.
>
> This repo's own residual, run on CPS ASEC 2025 with the Borjas (2017) rule list,
> gives 14,896,401 nationally and 4,567,144 Mexico-born. [CALCULATION] The same rule
> list on ACS 2024 one-year microdata gives 12,973,901: the two surveys disagree by 1.9
> million on identical rules. [CALCULATION] Rule-list choices move the answer by about
> 4%. The coverage assumption moves it by up to 62%, and almost all of that spread sits
> in the cohort that arrived after 2021. [CALCULATION]
>
> Coverage is assumed, not measured, in every published estimate. The one measured
> figure available is the 2020 Census Post-Enumeration Survey's "statistically
> significant undercount rate of 4.99%" for the Hispanic population, against a 1.64%
> overcount for non-Hispanic Whites. [SOURCE: US Census Bureau, CB22-CN.02, March 10
> 2022] Applied to this repo's ACS residual that rate yields 13.7 million, against the
> 15.9 million CMS's assumed rates yield. [CALCULATION] Some of the correction is also
> already in the data: the Census Bureau raised its net international migration
> estimates for 2021–23 by 70% and 102% in December 2024 because "recent humanitarian
> migrants … were also the least likely to be included in the ACS", and the ACS 2024
> and ASEC 2025 weights are controlled to those revised estimates. [SOURCE: Census
> Bureau, Random Samplings, December 19 2024; CALCULATION]
>
> An independent stock-flow check runs above the surveys. Adding CBO's net
> other-foreign-national immigration — 2.0 million in 2022, 2.4 million in 2023, 1.3
> million in 2024 and −360,000 in 2025 — to the DHS residual of 10.99 million for
> January 2022 implies 16.7 million by January 2025 and 16.3 million by January 2026.
> [SOURCE: CBO, *The Demographic Outlook: 2026 to 2056*, January 2026, Appendix B;
> CALCULATION] How solid that is turns on one parameter: at a 70% residency share for
> border releases and gotaways the bottom-up accounting reconciles, and the implied
> stock moves 2.7 million across a 50%-to-100% assumption. [CALCULATION]
>
> The population is now shrinking. CBO estimates net other-foreign-national immigration
> at −360,000 for 2025, and CIS reads the CPS foreign-born population down 2.9 million
> between January 2025 and July 2026, with the illegal population down 2.3 million to
> 13.5 million. [SOURCE: CBO, January 2026; Camarota and Zeigler, CIS, September 3
> 2026] A ledger built on ASEC 2025 therefore describes the stock near its peak.
>
> A figure of 40 million does not correspond to any defensible definition. Every
> non-citizen in the 2024 ACS — green-card holders, students and temporary workers
> included — numbers 24.4 million. [CALCULATION] Applying CMS's highest published
> undercount rate of 65%, which CMS uses only for Ecuadorians who arrived after 2021,
> to that entire population still yields only 38.1 million. [CALCULATION] Reaching 40
> million by scaling non-citizens requires assuming that 39% of every non-citizen in
> the country is missed by the ACS, against a measured 4.99% net undercount for all
> Hispanics in the 2020 Census. The only ACS constructions that do exceed 40 million
> count US citizens: non-citizens plus every US-born person living with one is 42.2
> million, of whom 17.8 million are US-born; the entire foreign-born population is 50.3
> million, about half of them naturalised citizens. [CALCULATION] The 40.9 million
> Mexican-origin population across all generations is a different population again, and
> is overwhelmingly composed of US citizens.

---

## Verification run

Every script re-run from scratch over the existing `_cache/` leaves `derived/`
byte-identical. Verified by copying `derived/` aside, re-running all scripts, and
`diff -r` reporting no differences. No script uses randomness, sampling, wall-clock
time or hostname. Exact commands: `README.md`.

## What was skipped and why

- **Arm 5 administrative anchors and the academic coverage literature**: two dispatched
  research agents exhausted their turn limits without returning. The two highest-value
  coverage sources were fetched directly instead (§4). The remaining gaps are listed in
  §7; the Jensen et al. (2015) Census coverage table is the one worth fetching next.
- **A 2025 or 2026 disposition table**: the DHS OHSS enforcement monthly series stops
  with the November 2024 edition. No substitute was used.
- **Pew's and MPI's coverage rates**: neither publishes a rate in the document fetched.
  Reported as "applied, rate not printed" rather than guessed.
- **CMS's pre-2024 revisions**: CMS states that revising 2023 on the new DHS data would
  raise it by 255,000 but did not publish a revised series; the unrevised 12.2M is
  carried with that note.
- **Replicate-weight SEs on the coverage-adjusted figures**: a coverage multiplier is an
  assumption, not a sampled quantity, so a sampling SE on the product would understate
  the real uncertainty by an order of magnitude. Counted figures carry SEs; adjusted
  ones deliberately do not.
