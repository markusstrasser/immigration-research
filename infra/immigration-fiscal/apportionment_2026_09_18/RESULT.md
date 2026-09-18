claude-opus-5[1m]

**Verdict:** Huntington-Hill reproduces the official 2020 and 2010 seat tables exactly (and the
published 89-person New York near-miss), so the counterfactuals are arithmetic, not estimation.
Removing the Mexican-origin population from the 2020 counts moves **24 of 435 House seats**
(California -12, Texas -8; Florida and New York +3 each); removing only the Mexico-born moves 7;
adding their US-born children under 18 moves 10; removing the unauthorized of all origins moves 2.
On the 2010 counts the full Mexican-origin arm moves 25. **No arm flips the 2020 or 2024
presidential outcome** — the largest shift is 7 electoral votes toward the 2024 Republican column
against a 44-vote flip threshold. The mechanism is geographic concentration: a proportional placebo
of the same size moves **zero seats in every arm**, and a 4,000-draw Monte Carlo over published
margins of error leaves California -4 and Texas -2 in every draw of the Mexico-born arm.

**Arms run:** 12 removal arms across two apportionments, each with a proportional placebo and a
redistribution twin, plus Monte Carlo, house-size (435-500) and source-construction sensitivities,
and a rough 2030 arm anchored against the Brennan Center's projection.
**Skipped:** the CPS ASEC parent-birthplace cross-check of the children ratio (`kids_cps.py` is
written and cached for 8 states) — the Census CPS endpoint stalled repeatedly under contention from
other lanes pulling census.gov, and the ratio is instead checked against two independent local
quantities (see Phase 7). The full 2019 ACS PUMS download was abandoned for the same reason at
119 MB of 568 MB, and replaced by the local IPUMS panel.
**Reproducibility:** a full re-run of all eight scripts reproduces every one of the 55 files in
`derived/` byte-identically.

## Phase 1 — Huntington-Hill verification [DONE]
Implemented method of equal proportions (`hh.py`); reproduces official seat counts EXACTLY for
both 2020 (50 states, 331,108,434 apportionment pop, 435 seats) and 2010 (309,183,463, 435 seats).
Independent sanity check: the 435th seat goes to Minnesota and the first seat missed (436th) is
New York — matches the published 2020 outcome. [SOURCE: census.gov apportionment table 1, 2020 & 2010]

## Phase 2 — state counts fetched [DONE]
`fetch_counts.py` → `derived/state_counts.csv` (50 states, DC and PR excluded; DC is not apportioned).
Sources and national cross-checks:
- Mexican origin 2020: 2020 Census **Detailed DHC-A**, table T01001, POPGROUP 4015 "Mexican".
  State sum 35,837,522; API national value 35,850,702 (difference = DC 13,180). [SOURCE: api.census.gov/data/2020/dec/ddhca]
- Mexican origin 2010: 2010 Census SF1 PCT011004. State sum 31,789,751; national 31,798,258 (difference = DC). [SOURCE: api.census.gov/data/2010/dec/sf1]
- Mexico-born: ACS 5-year B05006 (2016-2020 var _150E: 10,920,636 US; 2006-2010 var _138E). [SOURCE: api.census.gov acs5]
- Mexican origin ACS cross-check: B03001_004E (36,522,946 in ACS 2016-2020 vs 35.84M in the census count).

## Phase 3 — counterfactual arms run [DONE]
`counterfactuals.py` → `derived/arm_*.csv`, `arms_summary.csv`, `ec_arithmetic.csv`,
`house_size_sensitivity.csv`. Headline (2020 apportionment, 435 seats fixed):
- Remove the Mexico-born (10.92M, 3.30% of the apportionment population): **7 seats move**.
  CA -4, TX -2, IL -1 → FL, MA, MI, NY, OH, PA, VA +1 each. [CALCULATION]
- Remove all Mexican-origin (35.84M, 10.82%): **24 seats move**. CA -12, TX -8, AZ -1, CO -1,
  IL -1, NM -1 → FL +3, NY +3, OH +2, PA +2, VA +2, and 11 states +1. [CALCULATION]
- Remove the unauthorized (all origins): Pew 2019 (10.13M) and Pew 2021 (10.40M) both move
  **2 seats** (CA -1, TX -1 → NY +1, OH +1); CMS 2019 (10.34M) also 2 (CA -1, TX -1 → ID +1, OH +1).
- Context arm, remove all foreign-born (44.03M): 14 seats move (CA -8, NY -2, FL -2, NJ -1, TX -1).
2010 apportionment: Mexico-born 9 seats (CA -5, TX -3, WA -1); all Mexican-origin 25 seats
(CA -12, TX -9, AZ -2, NV -1, NM -1); Pew 2010 4 seats; CMS 2010 5 seats.

## Phase 4 — electoral-vote arithmetic [DONE]
Pairing each election with the apportionment it actually ran on (2020 election → 2010 census seats,
2024 election → 2020 census seats). Base rows reproduce the certified totals exactly:
306 D / 232 R in 2020 and 312 R / 226 D in 2024. **No arm flips either outcome.**
Largest shift: all-Mexican-origin removal, 7 electoral votes toward the 2024 Republican column
(312 → 319); Mexico-born removal 2; unauthorized-removal arms 0 to 1. [CALCULATION]

## Phase 5 — falsification arms [DONE]
- **Proportional placebo** (same national total removed, spread in proportion to state population):
  **0 seats move in every single arm**. The seat movement is entirely geographic concentration,
  not the size of the removal.
- **Monte Carlo on estimate error** (4,000 draws, state removals ~ N(estimate, MOE90/1.645)):
  Mexico-born 95% interval for seats moved [6,7], CA -4 and TX -2 in every draw; foreign-born
  [14,15]; Pew unauthorized [2,2]. The headline is not an artifact of sampling error.
- **Construction sensitivity**: ACS Mexican-origin (36.52M) instead of the census count gives 25
  seats instead of 24 — a one-seat difference from the choice of source.
- **House-size sensitivity**: at 436-500 seats the Mexican-origin arm moves 23-27 seats and the
  Mexico-born arm 6-8. Not a knife-edge artifact of the 435 cap.
- **Scale invariance note**: under a divisor method, removing a group and redistributing it in
  proportion to the remaining population are the same counterfactual. The "redistributed" arms in
  `arms_summary.csv` are therefore identical to their removal arms by construction, not by finding.

## Phase 6 — rough 2030 arm [DONE]
`projection_2030.py` on Census Vintage 2024 state estimates, straight-line 2020→2024 growth to
April 2030: 13 seats move vs the 2020 apportionment (TX +4, FL +4, AZ/GA/ID/NC/UT +1; CA -4,
IL -2, NY -2, MN/OR/PA/RI/WI -1). Removing the Mexican-origin population from that projection
(2020 shares held constant) moves 23 seats: CA -10, TX -9, AZ -2, CO -1, NM -1. [INFERENCE]

## Phase 7 — arm 4 (Mexico-born plus their US-born children under 18) [DONE]
The local IPUMS panel has no parent pointer, so children are identified by a household proxy:
a US-born person under 18 sharing a household with a Mexico-born person at least 15 years older.
National ratio 0.611 kids per Mexico-born in the 2010 ACS and 0.562 in the 2023 ACS; interpolated
to April 2020 and shrunk toward the national value for thin state samples (K = 50,000), the
weighted national ratio is 0.573. [INFERENCE]
Two cross-checks, both independent of the ratio itself:
1. The implied 6.2M US-born children is 54% of the 11.52M Mexican-origin under-18 population
   counted in the 2020 Census — the right order for a population whose parents are roughly half
   foreign-born. [SOURCE: 2020 DDHC-A T02003]
2. Running the same household proxy against *all* foreign-born adults in the 2023 ACS gives 17.98M
   US-born children under 18, against a published figure of about 16 million US-born children of
   immigrants under 18 from an earlier vintage — the right level for a proxy that overcounts
   slightly and for a population that has grown since. Mexico accounts for 34.9% of that total.
   [SOURCE: pewresearch.org second-generation series for the 16M benchmark; CALCULATION for 17.98M]

The intended exact check — CPS ASEC mother's and father's country of birth (PEMNTVTY/PEFNTVTY,
Mexico = 303), which needs no household proxy — is written as `kids_cps.py` and cached for 8 states,
but the Census CPS endpoint stalled repeatedly (one state per 60-180 seconds, then hanging) while
other lanes in this session were pulling census.gov. Re-run `kids_cps.py` when the endpoint is
responsive; it will use the cached states and finish the rest. [SKIPPED — transport, not method]
Arm: remove 17.13M (5.17% of the apportionment population) → **10 seats move**.
CA -6, TX -3, IL -1 → NY +2, and FL, MA, MI, NJ, OH, PA, VA, WV +1 each. Electoral-vote shift
toward the 2024 Republican column: 2. [CALCULATION]

## Implementation anchor
Beyond reproducing both official seat tables exactly, the priority-value table reproduces the
published near-miss: New York needed **88.8 more people** to take the 435th seat from Minnesota,
against the Census Bureau's published figure of 89. [SOURCE: census.gov 2020 apportionment results]

## Phase 8 — reproducibility [DONE]
Full re-run of all eight scripts from the cached inputs reproduces every one of the 55 files in
`derived/` byte-identically (md5 of `derived/*.csv` and `derived/*.json` before and after; diff empty).
The Monte Carlo uses a fixed seed (20260918).

---

# Draft memo section

## Where the Mexican-origin population is counted moves 24 House seats

Apportionment is arithmetic. The Census Bureau counts every resident, the method of equal
proportions (Huntington-Hill) divides 435 seats among the states, and each state's electoral votes
are its seats plus two. Removing a population from the counts of the states where it actually lives,
and re-running the same method, gives an exact answer to how many seats sit where they do because
that population is counted there.

The implementation reproduces both official apportionments exactly — the 2020 seat table from the
331,108,434 apportionment population and the 2010 table from 309,183,463 — and reproduces the
published near-miss: New York needed 88.8 more people to take the 435th seat from Minnesota,
against the Bureau's published figure of 89. [SOURCE: census.gov apportionment tables 1, 2020 and 2010]

### The arms

| Counterfactual (2020 apportionment) | People removed | Share of apportionment population | Seats moved |
|---|---|---|---|
| Mexico-born | 10,920,636 | 3.30% | 7 |
| Mexico-born plus their US-born children under 18 | 17,131,915 | 5.17% | 10 |
| All Mexican origin, foreign and US-born | 35,837,522 | 10.82% | 24 |
| Unauthorized, all origins (Pew 2019) | 10,132,500 | 3.06% | 2 |
| Unauthorized, all origins (Pew 2021) | 10,395,000 | 3.14% | 2 |
| Unauthorized, all origins (CMS 2019) | 10,337,000 | 3.12% | 2 |
| All foreign-born, context arm | 44,031,435 | 13.30% | 14 |

[SOURCE: 2020 Census Detailed DHC-A T01001 POPGROUP 4015; 2020 Census SF-equivalent counts;
ACS 2016-2020 B05006 and B05002; Pew Research Center state trends 1990-2023; Center for Migration
Studies state file 2010-2019] [CALCULATION: Huntington-Hill on official apportionment populations]

In the full Mexican-origin arm the losers are California -12 (52 seats to 40), Texas -8 (38 to 30),
Arizona, Colorado, Illinois and New Mexico -1 each. The gainers are Florida and New York +3, Ohio,
Pennsylvania and Virginia +2, and eleven states +1: Georgia, Iowa, Kentucky, Louisiana, Maryland,
Massachusetts, Michigan, Missouri, New Jersey, North Carolina, Tennessee and West Virginia.
[CALCULATION]

The same exercise on the 2010 apportionment moves 25 seats (California -12, Texas -9, Arizona -2,
Nevada -1, New Mexico -1), and the Mexico-born arm moves 9 (California -5, Texas -3, Washington -1).
[CALCULATION]

### Electoral college

Pairing each election with the apportionment it actually ran on — the 2020 election used the 2010
census seats, 2024 used the 2020 census seats — the base rows reproduce the certified totals
exactly: 306 to 232 in 2020 and 312 to 226 in 2024. **No arm changes either outcome.** The largest
movement is the full Mexican-origin arm, worth 7 electoral votes to the 2024 Republican column
(312 to 319) and 4 in 2020 (306-232 to 302-236). The Mexico-born arm moves 2, the unauthorized arms
0 to 1. A flip would need 44 electoral votes in 2024 and 38 in 2020. [CALCULATION on certified
statewide results; this is arithmetic on seat counts, not a claim about how anyone would vote.]

### Why the effect is large relative to the size of the population

Concentration, not headcount. The Mexican-origin population is 10.8% of the apportionment
population but 59.2% of it lives in California and Texas, against 20.8% of all residents.

| Group | Share in California and Texas | Share in the top five states |
|---|---|---|
| All residents | 20.8% | 37.3% |
| Mexican origin | 59.2% | 71.8% |
| Mexico-born | 58.7% | 71.4% |
| All foreign-born | 34.7% | 59.2% |

[CALCULATION on the same sources]

That is why the foreign-born arm removes 8.2 million *more* people than the Mexican-origin arm and
moves 10 *fewer* seats: immigrants overall are spread across states that lose seats (California,
New York, Florida, New Jersey) as well as states that gain them.

### Disconfirmation

Four arms were run that could have overturned the headline.

1. **Proportional placebo.** Remove the same national total from every state in proportion to its
   population. **Zero seats move, in every arm without exception.** The seat movement is entirely
   the geography of where the population lives.
2. **Monte Carlo over estimate error.** Drawing each state's removal from a normal centred on the
   published estimate with the published 90% margin of error, 4,000 draws: the Mexico-born arm
   moves 6 or 7 seats (California -4 and Texas -2 in every single draw), the foreign-born arm 14
   or 15, the Pew unauthorized arm exactly 2. The result is not sampling noise.
3. **Source construction.** Using the ACS Mexican-origin estimate (36,522,946) instead of the
   census count (35,837,522) gives 25 seats instead of 24 — a one-seat sensitivity to the source.
4. **House size.** At 436 through 500 seats the Mexican-origin arm moves 23 to 27 seats and the
   Mexico-born arm 6 to 8. Not an artifact of the 435 cap.

One methodological note that falls out of the arithmetic: under a divisor method, removing a group
and redistributing that group across the remaining population in proportion are the same
counterfactual, because the method is scale-invariant. The "redistributed" rows in
`arms_summary.csv` are identical to their removal rows by construction, not by finding.

### The rough 2030 arm

On Census Vintage 2024 state estimates extrapolated straight-line to April 2030, 13 seats move
against the 2020 apportionment: Texas and Florida +4, Arizona, Georgia, Idaho, North Carolina and
Utah +1; California -4, Illinois and New York -2, Minnesota, Oregon, Pennsylvania, Rhode Island and
Wisconsin -1. Removing the Mexican-origin population from that projection, holding each state's 2020
share constant, moves 23 seats (California -10, Texas -9, Arizona -2, Colorado -1, New Mexico -1).
[INFERENCE — a straight-line extrapolation of 2020-2024 growth, not a Census projection.]

External anchor: the Brennan Center's projection from the same Vintage 2024 estimates agrees on
every large mover — Texas and Florida +4, California -4, Illinois -2 — and differs at the margin,
giving New York -3 to this arm's -2 and adding South Carolina and Tennessee where this arm has
Minnesota, Oregon, Rhode Island and Wisconsin losing one each. That spread is the difference
between extrapolating four-year and two-year trends, and it is the right size for a rough arm.
[SOURCE: brennancenter.org, "How Congressional Maps Could Change in 2030"]

### What this is and is not

[FRAMING-SENSITIVE] The Constitution apportions on persons, not citizens or voters; counting
everyone where they live is the design, not a defect in it, and every number here is the size of
that design's effect rather than evidence about whether it should hold. The arms remove people from
the counts, not from the country: they do not model what California or Texas would look like had
that population never arrived, and they hold the House at 435 and every state's certified winner
fixed. The children arm rests on a household proxy rather than a parent pointer.

Three data caveats carry through every number above. The 2020 Mexican-origin count comes from the
Detailed DHC-A, which is released under differential privacy, so state cells carry injected noise;
the ACS construction arm (25 seats rather than 24) bounds how much that choice matters. Pew rounds
state estimates to the nearest 5,000 to 25,000 and censors its smallest cells as "<5,000", read here
as the midpoint 2,500; the Monte Carlo propagates Pew's own published margins. The 2010-to-2020
comparison spans the 2020 Census's revised race and origin coding, which affects race write-ins more
than the separate Hispanic-origin question but is not nothing. The apportionment
population also includes 348,698 overseas federal employees allocated to home states (0.11% of the
total), which these arms leave untouched.
