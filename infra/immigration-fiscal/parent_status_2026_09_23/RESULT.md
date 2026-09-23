# Legal status of Mexico-born parents of US-born children, by education

**Verdict:** About half of the low-education Mexico-born parents of US-born minor children are
imputed unauthorized, not almost all. Among parents without a high-school diploma, 47% are
imputed unauthorized under the paper's rules and 62% with the Medicaid clause dropped; outside
California, where the clause matters least, 54% and 62%. High-school-only parents: 37% and 52%.
Of the 1.35M US-born minors whose best-educated resident parent lacks a diploma, 45–62% have no
legal parent in the household; across all 5.0M US-born minors with a Mexico-born parent, 30–41%.
A rule granting citizenship only when a parent is legal would, on current status, exclude about
half of the children in the lowest-education Mexican families and about a third overall.
[CALCULATION: `parent_status.py`; DATA: CPS ASEC 2025 public use, 160-replicate SDR]

Date: 2026-09-23. Question from the operator: "almost none of the low skill parents are legal?"

## Method

- Status: the Borjas (2017) residual imputation of `status_impute_2026_09_16` (rules quoted in its
  `impute_status.py`), imported unchanged. The script reproduces that lane's published Mexico-born
  25–64 unauthorized counts (3.917M paper rules, 4.778M without Medicaid) before tabulating.
- Two rule sets. The paper's rule (c) calls any Medicaid recipient legal; California's Medi-Cal
  covered income-eligible unauthorized adults in 2024, so that rule moves California's
  low-education parents from 61% to 26% unauthorized. Dropping the clause instead calls legal
  noncitizens on Medicaid unauthorized. The truth sits between the two columns.
- Parents: Mexico-born (`PENATVTY` 303) people named in `PEPAR1`/`PEPAR2` by a co-resident
  US-born (`PRCITSHP` 1) person under 18. Education from `A_HGA`.
- Children: US-born minors with at least one co-resident Mexico-born parent; "no legal parent"
  means no co-resident parent (Mexico-born, other foreign-born or native) is imputed legal.

## Parents of US-born minors, share imputed unauthorized (SDR se)

| Education | Parents | Paper rules | No Medicaid rule | Rest of US, paper | Rest of US, no Medicaid |
|---|---:|---:|---:|---:|---:|
| Below high school | 1.51M (n 743) | 47% (2.2) | 62% (2.0) | 54% (2.7) | 62% (2.4) |
| High school only | 1.40M (n 684) | 37% (2.6) | 52% (2.6) | 45% (2.9) | 55% (3.0) |
| Some college | 0.47M (n 233) | 24% (3.3) | 30% (3.5) | 25% (3.7) | 32% (3.9) |
| Bachelor's or more | 0.34M (n 162) | 22% (4.1) | 29% (4.2) | 28% (5.1) | 33% (5.1) |
| All parents | 3.71M (n 1,822) | 38% (1.6) | 51% (1.5) | 45% (1.8) | 53% (1.8) |
| All Mexico-born adults 25–64 | 9.46M | 41% (1.2) | 51% (1.2) | 49% (1.3) | 55% (1.4) |

California alone, below high school: 26% (4.3) paper rules against 61% (4.2) without Medicaid.
[DATA: `derived/mexico_born_parents_by_status.csv`]

## US-born minors with a Mexico-born parent, share with no legal parent present

| Highest resident parent's education | Children | Paper rules | No Medicaid rule |
|---|---:|---:|---:|
| Below high school | 1.35M (n 604) | 45% (3.3) | 62% (3.2) |
| High school only | 1.88M (n 847) | 33% (2.7) | 46% (3.1) |
| Some college | 1.00M (n 471) | 17% (2.7) | 22% (3.0) |
| Bachelor's or more | 0.77M (n 333) | 14% (2.8) | 19% (3.2) |
| All | 5.01M (n 2,255) | 30% (1.5) | 41% (1.6) |

[DATA: `derived/usborn_children_by_parent_status.csv`]

## Limits

- Status is the parent's imputed status in March 2025, not at the child's birth. Parents who
  legalized after the birth count as legal here, so the share unauthorized at birth is higher.
- The residual method over-assigns unauthorized status overall (Borjas says so), while rules (c)
  and (i) (Medicaid, legal spouse) pull mixed-status parents into the legal cell. The Mexico-born
  total (4.57M all ages) sits near Pew's 4.3M for mid-2023; the split by education and
  parenthood is not validated against an external source.
- Co-resident parents only; the CPS under-samples 2022–24 arrivals.
- Imputed legal includes naturalized citizens and green-card holders; the imputation cannot
  separate them.

---

# Children's outcomes by their parents' status (added 2026-09-23)

**Verdict:** While the parents are unauthorized, their US-born children do worse than the children
of legal Mexican immigrants: poorer as minors and less often in college as young adults, after
holding parental education, age, state and two-parent families fixed. When the parents entered
illegally but later legalized, as the 1986-amnesty generation did, their children turned out the
same as the children of legal entrants on schooling, income, arrests and incarceration. The handful
whose mothers never legalized did much worse, on seven cases. Descriptive, not causal: status is
imputed in the CPS and recalled by the adult child in IIMMLA, and unauthorized parents differ in
ways coarse controls do not capture (time in the US, English, occupation).

## Adults, Los Angeles 2004 (IIMMLA)

US-born Mexican-origin respondents aged 20–40 with a Mexico-born mother, by how the mother entered
(Q127A–Q128). Unweighted quota sample. The script first reproduces the IIMMLA lane's Mexican
second-generation row (n 553; no diploma 19.0%, BA+ 16.8%, arrested 17.4%, incarcerated 11.2%).

| Mother entered | n | Years of school | No diploma | BA+ | Employed | Arrested | Incarcerated | Mother without diploma |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| With a green card | 231 | 13.46 | 16% | 20% | 68% | 19% | 10% | 37% |
| Without one | 150 | 13.47 | 19% | 20% | 73% | 15% | 10% | 60% |
| of which with no papers at all | 54 | 13.56 | 19% | 24% | 66% | 13% | 6% | 65% |
| Not legal by 2004 | 7 | 11.43 | 57% | 0% | 71% | 14% | 14% | 43% |

Controlling for age, sex and both parents' education, "without a green card" minus "with one":
years of school +0.09 (SE 0.22), no diploma +2.1 points (4.2), BA+ +2.5 (4.2), employed +10.1
(4.9), personal income +$3.5k (2.0k), arrested −0.1 (4.0), incarcerated +2.1 (3.3). By the
father's entry, no papers at all (n 72): BA+ +11.3 (5.1) and arrested +10.5 (5.4); nothing else
separates. Fathers not legal by 2004: n 12. [CALCULATION: `iimmla_parent_entry.py`;
DATA: `derived/iimmla_second_gen_by_parent_entry.csv`, `derived/iimmla_entry_status_gaps.csv`]

These respondents were born about 1964–1984; nearly all their parents had legalized by 2004, most
of those who entered without papers presumably under the 1986 amnesty [INFERENCE from timing].
The "without papers" contrast is therefore an entry-status contrast, not a lifelong one.

## Children today (CPS ASEC 2025)

US-born children living with a Mexico-born parent. "No legal parent" = every co-resident parent
imputed unauthorized; "legal immigrant parents" = every co-resident parent foreign-born, at least
one imputed legal. Two rule sets (no Medicaid clause / paper rules); adjusted differences control
for child's single year of age, highest parental education (4 levels), California and two-parent
households; SDR standard errors.

| Outcome | No legal parent | Legal immigrant parents | Adjusted difference | White US-born parents |
|---|---:|---:|---:|---:|
| Minors: SPM poor | 36% / 33% | 16% / 24% | +19.7 (3.4) / +10.2 (3.6) | 6% |
| Minors: uninsured now | 18% / 25% | 12% / 9% | +4.8 (2.9) / +14.1 (3.4) | 4% |
| Minors: family resources per person | $12.6k / $13.1k | $16.8k / $15.3k | −$3.9k (0.8) / −$1.7k (0.7) | $29.9k |
| 19–24 at home: high-school diploma | 90% / 90% | 97% / 95% | −5.3 (1.8) / −3.4 (2.1) | 92% |
| 18–24 at home: in or ever attended college | 44% / 41% | 62% / 60% | −12.2 (4.1) / −13.6 (4.2) | 55% |
| 18–24 at home: employed | 56% / 55% | 64% / 63% | −8.5 (3.9) / −6.8 (3.9) | 58% |
| 18–24 at home: neither in school nor working | 15% / 15% | 11% / 11% | +4.1 (2.6) / +4.3 (2.8) | 13% |

Children: 2.1M / 1.5M with no legal parent, 1.5M / 2.1M with legal immigrant parents (n 922 / 666
and 690 / 946); young adults n 406 / 315 and 379 / 470. [CALCULATION: `cps_children_outcomes.py`;
DATA: `derived/cps_children_outcomes_means.csv`, `derived/cps_children_outcomes_gaps.csv`]

At the same parental education the Mexican-family young adults attend college more often than
white young adults living with parents: parents with a high-school diploma only, 48% / 44% (no
legal parent) and 62% / 61% (legal) against 29% (white, n 519). "In or ever attended college"
counts community-college enrollment and is not degree completion; the degree gap persists into
the third generation (FAQ 5, ladder 178). The white cell below high school is small (n 98) and
unusual (28% of its minors uninsured); it is not used.

## Limits of the children's comparison

- Status: imputed for current CPS parents (see above for the rule-set bias; rules on program
  receipt and government jobs put program users in the legal cell, which biases poverty and
  insurance comparisons in opposite directions under the two rule sets); recalled by adult
  children in IIMMLA.
- Young adults are observed only while living with a parent; CPS counts dormitory students at
  home, but co-residence still differs by group.
- IIMMLA is Los Angeles in 2004, unweighted; its never-legalized cells have 7 and 12 cases.
- Nothing here separates parental status from what goes with it: recency of arrival, English,
  informal work, fear of enforcement.

## Published evidence (added 2026-09-23)

The literature agrees in direction. Bean, Leach, Brown, Bachmeier & Hipp (2011, IIMMLA, 1.5 and
second generation pooled): children of Mexican mothers who remained unauthorized or of unknown
status have 2.04 fewer years of school, 1.51 after controls, 1.24 with an IRCA-timing instrument
[SOURCE: IMR 45(2), pp. 372–374, re-read from the corpus PDF]; this lane's seven explicitly
never-legalized mothers give 2.03 unadjusted. Their book's summary: the harm comes from parents'
"long-term inability ... to acquire green cards", and children of parents who legalize reach
"schooling on par with those whose parents come legally" [SOURCE: publisher summary; book not
read]. Quasi-experiments: DACA protection of mothers cut their citizen children's adjustment and
anxiety diagnoses 4.3–4.5 points from about 7.9% (Hainmueller et al. 2017, Science); IRCA
legalization raised Mexican mothers' birthweights 96 g (Cascio, Cornell & Lewis 2024, NBER
w32635); DACA mothers' children gained 5 points of Medicaid enrollment (Tran 2025). Against a
simple reading: Bean's unauthorized group mixes in unknown-status mothers; Landale et al. (2015)
find children of undocumented Mexican mothers no worse than children of US-born mothers on
behaviour; the Census–IRS mobility studies cannot see children of unauthorized parents at all.
Full table, grades and verification levels: `literature.md`.

---

# How Mexicans get green cards, and how hard it is after entering without papers (added 2026-09-23)

**Verdict:** Hard, and usually only by leaving the country first. In 2003, 55% of the Mexican
adults who received green cards had at some point entered the US without papers (16% for everyone
else), a median 12 years before the green card, and about 1 in 100 unauthorized Mexicans got one
that year. Three quarters of those who had entered without papers adjusted inside the US under
section 245(i), which covers only people whose petition or labor certification was filed by April
30, 2001; that door is shut to anyone who arrived later. For them the main route left is a
US-citizen or permanent-resident spouse or parent, an I-601A waiver of the ten-year bar and a visa
interview in Mexico. A US-born child can petition for a parent only at 21 and does not count toward
the waiver. Family ties carry 94% of Mexico's green cards (2005–2022).

Question from the operator: "how easy is it to get legal status?"

## Mexican green cards by class, FY2005–2022 (DHS)

| Class | Mean per year | Share of Mexico's green cards in these classes | Mexico's share of the class |
|---|---:|---:|---:|
| Spouses of US citizens | 51,991 | 36.9% | 19.2% |
| Children of US citizens | 13,145 | 9.3% | 16.8% |
| Parents of US citizens | 27,632 | 19.6% | 22.7% |
| Spouses and children of permanent residents (F2) | 30,959 | 21.9% | 32.2% |
| Other family preferences (F1, F3, F4) | 8,927 | 6.3% | 8.5% |
| Employment (five preferences) | 8,416 | 6.0% | 5.2% |
| Diversity lottery | 10 | 0.0% | 0.0% |

141,100 a year in these classes (16.1% of all such green cards), from 88,600 in 2020 to 187,200 in
2008. The workbook omits refugees, asylees and the "other" classes, cancellation of removal among
them; in FY2003 those added 3.6% to Mexico's count (cancellation 2,503, other 1,557, refugee and
asylee 85 of 115,864) [SOURCE: DHS, 2003 Yearbook of Immigration Statistics, Table 8].
[CALCULATION: `lpr_routes.py`; DATA: `derived/lpr_class_summary_mexico.csv`,
`derived/lpr_class_by_year_mexico_and_total.csv`]

## Who had entered without papers, and how they got through (NIS 2003)

New Immigrant Survey 2003, adults granted permanent residence May–November 2003 (ICPSR 38031),
design-weighted, standard errors from a bootstrap within sampling strata. For every move of 60 days
or more to the US, Section K asks "did you have a visa or other entry document?"; a "no" on any
move counts as entering without papers.

| New green-card holders, 2003 | n | Ever entered without papers (SE) | Adjusted inside the US |
|---|---:|---:|---:|
| Born in Mexico | 1,164 | 55.0% (1.7) | 76.4% |
| Born elsewhere | 7,409 | 15.8% (0.5) | 53.3% |

Mexicans who had entered without papers (n 599), by how they got the green card:

| Route | Share (SE) |
|---|---:|
| Adjusted inside the US in a family or employment class, last entry without papers: needed 245(i) | 76.7% (1.6) |
| Left and came back on an immigrant visa | 11.3% (1.3) |
| Cancellation of removal or registry (class Z) | 7.4% (0.9) |
| Legalization classes (W) | 3.5% (0.7) |
| Adjusted inside, last entry documented | 0.8% (0.4) |

INA 245(a) requires inspection and admission or parole, so an adjustment inside the US in a family
or employment class after an entry without papers needed 245(i) [SOURCE: INA 245(a), 245(i); code
list in the 2003 Yearbook, Table 5]. Years from the first entry without papers to the green card,
median (interquartile range): all 12 (8–16); spouses of US citizens 11 (7–14); children of
citizens 10 (7–15); spouses of permanent residents 12 (9–15); other family preferences 13 (10–16);
cancellation or registry 14 (12–15); employment 15 (12–17); parents of citizens 16 (2–26);
legalization classes 23 (22–25). Parents of citizens had entered without papers least often (29%)
and more often came back from abroad (59% of those who had). [CALCULATION:
`nis_prior_undocumented.py`; DATA: `derived/nis2003_entered_without_papers.csv`,
`derived/nis2003_mexico_route_type.csv`, `derived/nis2003_mexico_route_by_entry.csv`,
`derived/nis2003_mexico_years_to_green_card.csv`]

Checks. The script reproduces the codebook counts and the handout's 17.5% weighted Mexican share.
In the two classes whose recipients had all been unlawfully present (legalization, cancellation or
registry), the item flags 90%, so it misses about one in ten, presumably overstays. The Mexican
class mix tracks the FY2003 Yearbook where an adults-only survey should: parents of citizens 18.5%
against 18.0%, employment 2.5% against 2.8%; children of citizens 5.6% against 12.9% because
minors are excluded. [DATA: `derived/nis2003_mexico_vs_yearbook.csv`]

## About 1 in 100 a year, in 2003

In FY2003, 115,864 Mexicans got green cards [SOURCE: 2003 Yearbook, Table 3]. With the NIS share
who had entered without papers (55%, or 61% corrected for the missed tenth), less those who came
back from abroad, 56,500–62,800 previously undocumented Mexicans became permanent residents. DHS
put the unauthorized Mexican population at 4.68M in January 2000 and 5.97M in January 2005
[SOURCE: DHS OIS, Estimates of the Unauthorized Immigrant Population, January 2005, Table 3];
interpolated to 2003, 5.45–5.58M. The ratio is 1.0–1.15% a year. Measured: the FY2003 count and
the adults' share. Assumed: the adult share holds for children, and the stock grows linearly
between the DHS estimates. [CALCULATION: `derived/nis2003_mexico_annual_legalization_rate.csv`]

## The routes in September 2026, for someone who entered without papers

Statute text checked on the US Code (Cornell LII) on 2026-09-23; the time-sensitive rows come from
[`legal_routes_facts.md`](legal_routes_facts.md), each with its primary source and an exact quote.

| Route | Who qualifies | What an entry without papers means | Scale or wait, 2026 |
|---|---|---|---|
| Spouse of a US citizen | the spouse | Cannot adjust inside (INA 245(a) requires inspection). Must attend a visa interview in Mexico; leaving after a year of unlawful presence bars return for ten years unless an I-601A waiver is approved first, and the waiver counts only hardship to a citizen or resident spouse or parent. A re-entry without inspection after a year of unlawful presence or a removal is a further bar (INA 212(a)(9)(C)). Someone who entered on a visa and overstayed can adjust inside. | I-601A median 24.3 months (FY2026). FY2026 through June: 20,826 approved, 2,612 denied, 77,755 pending. ICE arrested overstaying spouses at San Diego green-card interviews from November 2025 (one outlet, one city). |
| Spouse or minor child of a permanent resident (F2A) | the spouse or child | Same interview abroad and bars; the waiver can rest on the resident spouse or parent | Mexico final action date 22 Aug 2025: about a year in line |
| US-born child | a parent, once the child is 21 (INA 201(b)(2)(A)(i)) | Same interview abroad. The ten-year-bar waiver is open only to the "spouse or son or daughter" of a citizen or resident, so a child's petition carries no waiver: ten years abroad after a year of unlawful presence | Parents of citizens: 27,600 Mexican green cards a year, 20% (2005–2022) |
| Adult children and siblings of citizens; adult children of residents | F1, F2B, F3, F4 | Same bars | Mexico final action dates 1 Jan 2008 (F1), 15 Feb 2009 (F2B), 1 Jul 2001 (F3), 8 Apr 2001 (F4): 17–25 years in line |
| Employer sponsorship | EB-3 "other workers" with labor certification | Same interview abroad and bars; no waiver without a citizen or resident spouse or parent | Mexico final action date 1 Apr 2022; employment is 6% of Mexican green cards |
| Cancellation of removal | 10 years' presence and "exceptional and extremely unusual hardship" to a citizen or resident spouse, parent or child | Available despite the entry, but only as a defense in removal proceedings | 4,000 a year nationwide (INA 240A(e)); Mexico 2,503 in FY2003 |
| U visa | victims of listed crimes who help the police | Available despite the entry | 10,000 a year; 288,243 principal petitions pending (June 2026), about 29 years of the cap; interim work permit after a median 19.3 months, with 34% of FY2026 determinations ineligible |
| Asylum | persecution | Available, with a one-year filing deadline [TRAINING-DATA] | Mexicans won 16.6% of immigration-court asylum decisions in FY2024 (TRAC via Axios) |
| Military parole in place | relatives of service members | Parole counts as admission for an immediate relative's adjustment | Still offered; median 12.8 months (FY2026) |
| DACA | arrived as children | Not a status and no path to one; initial requests held since 2021 | Fifth Circuit (January 2025) limited relief to Texas; district court had not ruled on implementation as of February 2026 |
| Legalization or registry | registry: entry before 1 January 1972 | None enacted since IRCA (1986): nearly 2.7M legalized, 75% born in Mexico. The Dignity Act (H.R. 4393) has sat in subcommittee since July 2025 | Keeping Families Together (2024) would have paroled an estimated 500,000 spouses of citizens with ten years' presence; a Texas federal court vacated it on 7 Nov 2024 |

Mexico has never had Temporary Protected Status [TRAINING-DATA]. The 2026 visa-bulletin dates
advanced partly because a January–August 2026 pause on immigrant visas for 75 countries (not
Mexico) freed numbers; the State Department warns of retrogression.

Read together: a Mexican who entered without papers after 2001 and has no citizen or resident
spouse or parent has no way to a green card except a defense in removal proceedings (4,000 a year
nationwide) or a crime-victim visa with a queue of decades. A citizen spouse opens a route of about
two years plus an interview abroad. A US-born child opens one only at 21, and only after ten years
outside the country. In 2003, 245(i) carried 77% of the Mexicans who legalized after entering
without papers; it reaches only petitions filed by 30 April 2001 by people present on 21 December
2000 [SOURCE: 8 U.S.C. 1255(i)]. [INFERENCE from the table]

## Limits of the green-card evidence

- The survey item misses overstays and short undocumented visits; in classes where every recipient
  had been unlawfully present it flags 90%.
- Only people who got green cards are observed, so the 12-year median is the wait of those who
  made it; nothing here gives the chance of ever legalizing.
- One cohort, 2003, when 245(i) filings from 1998–2001 were being adjudicated; no later survey
  repeats the question, so the 2026 picture rests on the law and on administrative counts.
- "Needed 245(i)" is read from the class, the adjustment flag and the survey's last recorded entry;
  a documented visit shorter than 60 days after that entry would have allowed an immediate relative
  to adjust without it.
- The 1-in-100 rate applies the adults' share to children and interpolates the DHS stock; it
  describes 2003 only.
