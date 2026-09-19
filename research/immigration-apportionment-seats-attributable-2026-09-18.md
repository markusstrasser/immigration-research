# Where the Mexican-origin population is counted moves 24 House seats

## Audit correction — September 19, 2026

**Retain 24 seats as the fixed-location counting counterfactual, not a political-effect estimate.** It depends on uneven geography at the observed group size. Proportional removal is a scale-invariance check, not proof that size is irrelevant. The calculation includes US-born citizens, does not assign seats to an ethnic group, and holds electoral winners fixed. [SOURCE: construction below; mechanisms audit]

This supersedes conflicting interpretations below; calculations are retained as evidence. [Audit index](immigration-five-day-cross-check-2026-09-19.md).


**Verdict:** Counting the Mexican-origin population where it lives moves 24 of 435 House seats in the 2020 apportionment (California −12, Texas −8, Arizona, Colorado, Illinois and New Mexico −1; Florida and New York +3, Ohio, Pennsylvania and Virginia +2, eleven states +1) and 25 in 2010. The Mexico-born alone move 7 seats, the Mexico-born with their US-born children under 18 move 10, and the unauthorized population of all origins moves 2. No arm changes the 2020 or 2024 presidential outcome; the largest shift is 7 electoral votes toward the 2024 Republican column against a 44-vote threshold. The mechanism is concentration: a proportional placebo removing the same number of people spread across states moves zero seats in every arm, and removing all 44 million foreign-born, 8 million more people, moves 10 fewer seats than removing the Mexican-origin population, because 59% of it lives in California and Texas against 21% of all residents. This is arithmetic on certified counts under the method of equal proportions, which the lane first reproduced exactly for 2020 and 2010, down to the published 89-person New York near-miss. [SOURCE: `infra/immigration-fiscal/apportionment_2026_09_18/derived/arms_summary.csv`, `ec_arithmetic.csv`]

Date: 2026-09-18. Lane: `infra/immigration-fiscal/apportionment_2026_09_18/` (eight scripts, 55 derived files, reproduced byte-identically by the parent). A third-order political consequence with no identification problem: the Constitution apportions on total persons, so the counterfactual removes people from counts, not from the country, and says nothing about behaviour.

## 1. Inputs and the exactness gate

Apportionment populations 2020 (331,108,434, overseas military included) and 2010 (309,183,463) from the Census Bureau's tables. Mexican origin by state from the 2020 Detailed DHC-A (POPGROUP Mexican, 35,837,522 across the 50 states) and 2010 SF1 (31,789,751); Mexico-born from ACS 5-year B05006 (10,920,636 in 2016–20); unauthorized by state from Pew 2019 and 2021 and CMS 2019; US-born children under 18 of the Mexico-born from a household proxy on the local IPUMS panel (0.573 children per Mexico-born adult, checked against the 2020 Census under-18 Mexican-origin count and the published second-generation total). Huntington–Hill reproduces both official seat tables exactly; the 435th seat goes to Minnesota and New York misses by 88.8 people against the Bureau's published 89. [SOURCE: census.gov apportionment tables; api.census.gov ddhca, sf1, acs5; `hh.py` gate output]

## 2. Arms

| Arm, 2020 apportionment | People removed | Seats moved | Losers | Gainers |
|---|---|---|---|---|
| Mexico-born | 10.92M (3.3%) | 7 | CA −4, TX −2, IL −1 | FL, MA, MI, NY, OH, PA, VA |
| Mexico-born plus US-born children under 18 | 17.13M (5.2%) | 10 | CA −6, TX −3, IL −1 | NY +2; FL, MA, MI, NJ, OH, PA, VA, WV +1 |
| All Mexican-origin | 35.84M (10.8%) | 24 | CA −12, TX −8, AZ, CO, IL, NM −1 | FL +3, NY +3, OH, PA, VA +2, eleven states +1 |
| Unauthorized, all origins (Pew 2019, Pew 2021, CMS 2019) | 10.1–10.4M | 2 | CA −1, TX −1 | NY and OH (Pew), ID and OH (CMS) |
| All foreign-born (context) | 44.03M | 14 | CA −8, NY −2, FL −2, NJ −1, TX −1 | |

2010 apportionment: Mexico-born 9, all Mexican-origin 25, unauthorized 4 to 5. [CALCULATION: `derived/arm_*.csv`]

Electoral votes, pairing each election with the apportionment it ran on: base rows reproduce 306–232 (2020) and 312–226 (2024). The all-Mexican-origin arm moves 7 votes toward the 2024 Republican column (312 to 319); the Mexico-born arm 2; the unauthorized arms 0 to 1. No arm flips either election. [CALCULATION: `derived/ec_arithmetic.csv`]

## 3. Disconfirmation

- **Proportional placebo:** removing the same national total in proportion to each state's population moves zero seats in every arm. The seats move because of where the population lives, not how large it is. [CALCULATION]
- **Monte Carlo on estimate error:** 4,000 draws over the published margins of error give a 95% interval of 6 to 7 seats for the Mexico-born arm, with California −4 and Texas −2 in every draw; 14 to 15 for all foreign-born; exactly 2 for the Pew unauthorized arm. [CALCULATION: `robustness.py`, seed 20260918]
- **Source construction:** ACS Mexican origin (36.52M) instead of the census count gives 25 seats rather than 24.
- **House size:** at 436 to 500 seats the Mexican-origin arm moves 23 to 27 seats and the Mexico-born arm 6 to 8. Not a knife-edge of the 435 cap.
- **Redistribution twin:** under a divisor method, removing a group and redistributing it proportionally over the remainder are the same counterfactual, so the redistribution arms match the removal arms by construction, not by finding. [INFERENCE, verified in `arms_summary.csv`]

A rough 2030 arm on Census Vintage 2024 estimates (straight-line growth) moves 13 seats against 2020 (Texas and Florida +4 each, California −4) and agrees with the Brennan Center on every large mover; removing the Mexican-origin population from that projection moves 23. [INFERENCE: `projection_2030.py`]

## 4. What this is and is not

It is the exact answer to "how much representation follows the Mexican-origin population", which no commentator on either side had computed at the origin level. It is not a statement about who those seats elect: the 2024 arithmetic shows a 7-vote shift on a 44-vote margin, and the unauthorized arms, which are what the apportionment debate is usually about, move 2 seats. The one skipped check is the CPS parent-birthplace confirmation of the children ratio (`kids_cps.py`, cached for 8 states), abandoned because the Census CPS endpoint stalled under load from other lanes; the ratio is bracketed by two independent totals instead. [SOURCE: RESULT.md Phase 7]

## Sources

Census Bureau apportionment tables 2020 and 2010; 2020 Detailed DHC-A T01001 and T02003; 2010 SF1 PCT011; ACS 5-year B05006, B03001, B05002; Pew Research unauthorized estimates 2019 and 2021; Center for Migration Studies 2019; Census Vintage 2024 state estimates; Brennan Center 2030 projection; local IPUMS panel (`~/research-data/immigration-fiscal/derived`). Instrument note: LLM-assisted; every number reproduced by the lane scripts.


## Revisions — September 19, 2026

Corrected the interpretation for the reasons above; see the [decision](../decisions/2026-09-19-bind-report-claims-to-matched-estimands.md).
