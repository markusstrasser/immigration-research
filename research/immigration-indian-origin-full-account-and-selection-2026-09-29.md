# Indian-origin residents: the full account, arrival cohorts and home regions

2026-09-29. Ladder 276–277. Lanes:
[indian_full_account_2026_09_29](../infra/immigration-fiscal/indian_full_account_2026_09_29/RESULT.md),
[indian_cohort_selection_2026_09_29](../infra/immigration-fiscal/indian_cohort_selection_2026_09_29/RESULT.md),
design [percentile_mapping_design_2026_09_29](../infra/immigration-fiscal/percentile_mapping_design_2026_09_29/DESIGN.md).

**Verdict:** On the main case and the same social rows the Mexican-origin union carries, Indian-origin
residents benefit other residents by about $9,300–10,800 per member a year ($57–65bn), and by
$7,100–8,400 at the third-plus white age distribution. The flow the household surveys see is not
becoming less selected: each arrival cohort since 1995 sits at the 75th–78th percentile of US white
education at arrival. "Indian" is several populations: south-Indian and Hindi-speaking professionals
sit near the 80th percentile, Punjabi speakers at the 47th. The unmeasured risk is the post-2021
irregular inflow, which the surveys under-cover. [CALCULATION: both lanes; FRAMING-SENSITIVE: the
reference is third-plus non-Hispanic whites]

Instrument caveat: LLM-conducted on a charged topic (`notes/llm-bias-caveat.md`).

## 1. The question

The operator's objection: the pro-immigration case leans on Indians, the ledger's +$10.7k per adult
(ladder 150) is a narrow account of a young, visa-selected group, and recent cohorts may be weaker,
including outsourcing-firm hires, motel and store owners and irregular arrivals. Three tests: put
the group on the full account at its own ages and at white ages; see whether arrival cohorts have
lost selection; split the group by home region.

## 2. The full account

Per member a year, low / high end of the case; positive costs others, negative benefits them
[CALCULATION: `indian_full_account_2026_09_29/derived/combined.csv`]:

| Group | Fiscal | Social rows | Total |
|---|---:|---:|---:|
| Indian-origin, actual ages (6.08M, CPS) | −12,006 / −10,635 | +1,243 / +1,329 | **−10,763 / −9,305** |
| Indian-origin, white ages | −9,886 / −8,594 | +1,467 / +1,525 | **−8,419 / −7,069** |
| India-born, actual ages | −12,179 / −10,751 | +888 / +990 | −11,292 / −9,761 |
| India-born, white ages | −7,492 / −6,212 | +1,256 / +1,328 | −6,236 / −4,884 |
| Mexican-origin union, actual ages | +9,353 / +10,950 | +2,424 / +2,535 | +11,777 / +13,485 |
| Third-plus whites | +610 / +1,865 | +2,254 / +2,294 | +2,864 / +4,159 |

- Fiscal standard errors for the Indian rows are about $1,000–1,150 (160 CPS replicate weights).
- Ageing to white ages removes about a sixth of the group's lead over whites; the India-born alone
  lose about half of their benefit (−$11.3k → −$6.2k at the low end), because their old age is still ahead of them.
- The gate: the same code reproduces the adopted union account, $371.4146 / 434.8410bn, exactly.
- Pooling ASEC 2022–26 for the second generation (941 adults, not 209) moves the total by $136 per
  member. Self-employed and wage-earning India-born adults do not differ measurably
  (−$18.4k/−16.7k, SE 4.9k, against −$19.8k/−18.1k). Motel, grocery and gas-station owners are 27
  of 350 sampled self-employed India-born adults pooled: too few to estimate.

What rests on proxies: no Indian offending data exists in the repo's sources, so institutionalization
in ACS 2023 stands in (about 7% of the union's rate per member); medical shares rest on 317 Asian
Indians in MEPS; long-term care, driving and school discipline use Asian rates. The white-ages
arm holds today's age profile of the group, whose older members are mostly parents who arrived
late, so it probably understates the aged group's taxes. CPS weights the India-born at 4.28M
against 2.94M in ACS 2023: the $bn totals scale with the count, the per-member figures do not.

## 3. Arrival cohorts

Education percentile against US third-plus whites of the same year, ages 25–54, at 0–5 years in
the US [CALCULATION: `indian_cohort_selection_2026_09_29/derived/`]:

| Arrival cohort | Percentile |
|---|---:|
| 1970–74 (at 6–10 years) | 78.3 |
| 1975–94 | 69.0–72.7 |
| 1995–2000 | 75.5 |
| 2005–10 | 76.6 |
| 2018–23 | 78.2 |

- Earnings percentiles at 6–10 years are flat to rising (62.1 for 1990s arrivals, 64.3 and 63.8 for
  2010–14 and 2015–19). The 2020–24 arrivals earn less at 0–5 years (47.5 against 51–54), at a mean
  of 1.4 years in the US; too early to tell a weaker cohort from a slow start.
- The job mix changed: physicians fell from 12% of employed pre-1980 arrivals to 1%; computing
  rose from 14% to 36%; retail stays at 6–10%.
- The future second generation: 1.62M US-born with an India-born parent, 61% under 18; about 0.22M
  are 35 or older. The parents of today's children are 42% 2000–09 and 39% post-2010 arrivals, and
  their earnings percentile is 8 points above the parents of the adult G2. Through the selection
  curve's slopes the future adult G2 comes out 0.1–1.8 points higher on education and 2.3–4.5 on
  earnings, about +$1.1–2.2k per adult-year [INFERENCE: percentile regression, not a model of
  inheritance; see §6].
- Stock (ACS 2024): 3.22M India-born; pre-1990 waves 13%, mostly past 60; post-2010 arrivals 51%.

## 4. Home regions

India-born adults 25–64 by language at home, ACS 2021–24 [DATA: `derived/language_profile.csv`]:

| Language | Stock | Education pct | Earnings pct | Note |
|---|---:|---:|---:|---|
| Telugu | 418k | 80.3 | 66.5 | half the employed in computing |
| Tamil | 268k | 80.1 | 65.4 | |
| Marathi, Kannada, Bengali | 66–106k | 80–81 | 64–67 | |
| Hindi | 719k | 77.6 | 64.7 | |
| Malayalam | 158k | 72.6 | 60.8 | 18% health practitioners |
| Gujarati | 322k | 66.1 | 55.6 | 16.5% in retail |
| Punjabi | 223k | 47.4 | 47.3 | 17% of the employed in trucking, 21% self-employed |

Across waves the flow moved toward the selected regions: Gujarati and Punjabi speakers together
fell from 25–30% of pre-1990 arrivals to 11% of 2020+ arrivals; Telugu rose from 4–5% to 21% and
Hindi from 20% to 32%. Language is a region proxy, not caste; no US survey records caste.

## 5. Flows the surveys do and do not see

[SOURCE: archived primary tables, `indian_cohort_selection_2026_09_29/context/flows_2015_2025.csv`]

- H-1B approvals for India-born beneficiaries: 195k (FY2015) → 284k (FY2025), 70–76% of all
  approvals. The six outsourcing firms file almost nothing at wage Level I (1.8% FY2019, 0.9% FY2024;
  23% in FY2015) and cluster at Level II; wage level is a job's pay band, not the worker's skill.
- Active F-1/M-1 records, citizens of India: 247k (2017) → 422k (2024).
- LPR grants to India-born: 64k (FY2015) → 127k (FY2022) → 67k (FY2024).
- CBP encounters, citizenship India (events): 19.9k (FY2020) → 96.9k (FY2023) → 34.1k (FY2025).
- Unauthorized India-born: DHS 220k (2022), Pew 680k (2023).

ACS 2024 shows about 63k non-degree Indian noncitizens who arrived 2021–24, against 64–97k
encounters a year. If 200k irregular arrivals were missed, the G1 education mean falls about 2.6
points and the projected G2 about 1 point [CALCULATION: §5 of the cohort lane].

## 6. Disconfirmation

- **For the operator's objection:** the fiscal advantage is a period account; the white-ages arm
  reweights today's profile and cannot see future cohorts' earnings. The irregular channel is
  under-counted, and if it comes mainly from Punjab and Gujarat [UNVERIFIED], it is the
  least-selected part of the flow. The Indian second generation old enough to judge is small.
- **Against it:** every measured cohort since 1995 is at least as selected as the 1975–94 wave; the
  pooled G2 and the class-of-worker split do not move the result.
- **On the projection:** the cross-lab attack on the percentile design (`attack_astra.md`, verified,
  committed 842726fd) found that a regression on percentile means is predictive only. A national
  origin mean cannot speak to a shift within India; only a sub-population mixture can.

## 7. Next steps

1. **Origin means by sub-population.** India's IHDS and NSS/PLFS give education and income by state
   × caste × language. Map them to the US scale and weight by the ACS language × cohort mix: the
   composition half of the revised design.
2. **Linkage audit.** Before any transmission estimate, check which files link adult G2 to parents'
   arrival year (NLSY97 parent linkage, CILS, co-resident ACS/CPS). Without it the cohort forecast
   stays a synthetic-cohort exercise.
3. **Test scores of the future G2.** Find a file with parent birthplace country and child scores
   (ECLS-K:2011 restricted, HSLS:09, state files with home language) to read the children of
   post-2000 arrivals directly.
4. **The irregular flow.** Region of origin of recent Indian border crossers (court records, EOIR
   asylum filings by language, press counts), and whether ACS 2025 picks them up.
5. **Caste in the tail.** Surname-coded caste for public name lists (NPPES physicians, USPTO
   inventors, math olympiad rosters) to see whether the selected tail is a few castes.
6. **Offending.** An Indian-specific incarceration or conviction series (Texas DPS by birthplace,
   BOP citizenship) to replace the institutionalization proxy.
7. **Reconcile the count.** CPS 4.28M against ACS 2.94M India-born: needed before any $bn total is
   quoted.
