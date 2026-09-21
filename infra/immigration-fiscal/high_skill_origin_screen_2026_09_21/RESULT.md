# High-education origin groups: annual fiscal balances and degree conversion, 2026-09-21

**Verdict:** None of 17 high-education birthplace groups has a clearly negative adult balance,
and Russia/Ukraine-born residents are positive (+$9,798 per adult, 95% interval +$4,450 to
+$15,145, personal allocation). The closest to "educated but not positive" is the
Philippines-born: 56% of working-age adults hold a degree, yet the adult balance is +$948
(−$2,378 to +$4,274) under the personal allocation and −$2,124 (−$5,154 to +$906) once household
costs are shared, because a third of Philippines-born adults are 65 or older. The sharper
finding is that degrees convert unequally. At common ages, degree holders born in Venezuela pay
$19,402 less per year than native degree holders, and those born in Pakistan or Bangladesh
$12,947 less, while India-born degree holders pay $7,545 more. Descriptive 2024-price resident
accounts, not admission effects. [CALCULATION: `screen.py` → `derived/origin_screen.csv`;
CPS ASEC 2025 through the unchanged `education_origin_fiscal_2026_09_19/builder.py`]

Question asked (operator, 2026-09-21): "what's a high skill immigrant group that's not positive
that we could get data on? … Russians?" The 19 origins were listed before the run; none was
added or dropped after seeing results.

## Adult balance by birthplace (ages 25+, all education)

Account `expanded_excluding_N`, stock residents, dollars per adult per year. `personal` charges
each adult their own items; `shared` spreads household costs, which brings in children's
schooling. Natives are shown because "not positive" needs a benchmark: the average native adult
is +$2,785 (personal) and −$1,657 (shared) on this account.

| Birthplace | n 25–64 / 65+ | BA+ (25–64) | 65+ share of adults | Personal, 25+ | 95% interval | Shared, 25+ | 95% interval |
|---|---:|---:|---:|---:|---:|---:|---:|
| Philippines | 669 / 329 | 55.6% | 32.3% | +$948 | −2,378 to +4,274 | −$2,124 | −5,154 to +906 |
| *All native* | 55,652 / 21,681 | 41.1% | 28.0% | +$2,785 | +2,096 to +3,474 | −$1,657 | −2,317 to −998 |
| Venezuela | 338 / 41 | 49.5% | 9.2% | +$4,458 | +1,109 to +7,808 | +$2,013 | −1,895 to +5,922 |
| Pakistan, Bangladesh | 209 / 48 | 59.7% | 19.4% | +$5,331 | −1,109 to +11,772 | +$448 | −4,882 to +5,779 |
| Former USSR (13 codes) | 340 / 68 | 63.3% | 19.4% | +$9,004 | +4,290 to +13,717 | +$2,413 | −1,297 to +6,124 |
| Russia, Ukraine, "USSR" | 217 / 44 | 64.3% | 20.6% | +$9,798 | +4,450 to +15,145 | +$3,738 | −828 to +8,303 |
| Korea | 275 / 98 | 74.3% | 25.2% | +$10,193 | +4,982 to +15,404 | +$5,276 | +617 to +9,936 |
| Nigeria | 114 / 15 | 71.6% | 9.4% | +$14,891 | +5,627 to +24,155 | +$5,374 | +62 to +10,687 |
| China (mainland) | 628 / 190 | 68.5% | 25.8% | +$16,915 | +10,819 to +23,011 | +$10,456 | +5,080 to +15,832 |
| India | 1,232 / 165 | 90.5% | 11.9% | +$29,174 | +25,470 to +32,878 | +$17,965 | +15,232 to +20,698 |

Germany (+$567), Poland (+$3,192), Japan (+$7,438), Egypt, Iran, Brazil, the United Kingdom,
Taiwan/Hong Kong and Canada are in the CSV; each has fewer than 170 working-age records and an
interval tens of thousands of dollars wide. Germany and Poland sit near zero for the age reason:
52% and 39% of their adults are 65 or older. [CALCULATION: `derived/origin_screen.csv`]

Every group is positive at working age (25–64), and every group except the Canada-born
(83 records aged 65+) is negative at 65+, as natives are (+$14,665 and −$27,741). Two
high-degree groups fall below the native working-age balance: Venezuela-born +$7,062 and
Pakistan/Bangladesh-born +$12,134.

## Degree holders against native degree holders, common ages

Personal allocation, BA+ only, age-standardised to the native 25–64 distribution over the age
bands both groups support (`mass` is the share of that distribution covered).

| Birthplace | n | Gap per person per year | 95% interval | mass | z |
|---|---:|---:|---:|---:|---:|
| Venezuela | 180 | −$19,402 | −23,852 to −14,953 | 0.76 | −8.6 |
| Mexico | 475 | −$14,998 | −19,541 to −10,454 | 1.00 | −6.5 |
| Pakistan, Bangladesh | 130 | −$12,947 | −21,152 to −4,742 | 0.53 | −3.1 |
| Former USSR (13 codes) | 225 | −$7,519 | −13,399 to −1,639 | 1.00 | −2.5 |
| Philippines | 343 | −$6,460 | −11,713 to −1,207 | 1.00 | −2.4 |
| Korea | 201 | −$3,690 | −11,173 to +3,793 | 1.00 | −1.0 |
| Russia, Ukraine, "USSR" | 149 | −$1,438 | −11,743 to +8,867 | 0.48 | −0.3 |
| India | 1,112 | +$7,545 | +3,193 to +11,896 | 1.00 | +3.4 |
| China (mainland) | 425 | +$10,110 | +2,912 to +17,308 | 1.00 | +2.8 |

Sixteen origins were compared. At a family-wise 5% level the threshold is |z| > 2.96, which
Venezuela, Mexico, Pakistan/Bangladesh and India pass; the former-USSR and Philippines gaps are
suggestive only. Degree holders of every origin remain positive in absolute terms (+$7,264 for
Venezuela to +$36,021 for Iran per adult aged 25+). [CALCULATION: same file]

## At the native age mix (added later on 2026-09-21)

The headline table is a snapshot at each group's own ages, which flatters young groups: 12% of
India-born adults are 65 or older against 28% of natives. `age_standardized.py` re-weights each
group's own 25–64 and 65+ balances to the native 65+ share, and as a bound replaces the group's
65+ balance with the native one (−$27,741), since today's immigrant elderly often arrived late
and hold smaller entitlements than today's workers will. Personal allocation, dollars per
adult-year; the standard error treats the two bands as independent (approximate).
[CALCULATION: `derived/origin_screen_native_ages.csv`]

| Birthplace | 65+ share | Own ages | Native age mix (±se) | Native old-age cost |
|---|---:|---:|---:|---:|
| India | 11.9% | +29,174 | +21,832 (1,795) | +17,121 |
| Iran | 30.0% | +21,228 | +22,292 (6,380) | +19,083 |
| United Kingdom | 38.9% | +15,931 | +21,798 (4,831) | +18,801 |
| China (mainland) | 25.8% | +16,915 | +15,966 (2,704) | +12,522 |
| Brazil | 8.0% | +17,438 | +10,128 (3,228) | +6,891 |
| Nigeria | 9.4% | +14,891 | +8,866 (5,223) | +5,145 |
| Russia, Ukraine, "USSR" | 20.6% | +9,798 | +6,629 (2,059) | +5,641 |
| Third-plus NH white | 31.6% | +3,294 | +4,861 (387) | +4,653 |
| Philippines | 32.3% | +948 | +2,895 (1,568) | +3,440 |
| All native | 28.0% | +2,785 | +2,785 (330) | +2,785 |
| Pakistan, Bangladesh | 19.4% | +5,331 | +2,329 (3,287) | +963 |
| Venezuela | 9.2% | +4,458 | −877 (1,436) | −2,689 |
| Mexico | 14.9% | −2,282 | −5,684 (642) | −6,650 |

Youth supplies a quarter of the India-born figure and 40% or more of the Brazil- and
Nigeria-born figures; the ordering survives. With age held at the native mix the Venezuela-born
are at or below zero and the Pakistan/Bangladesh-born cannot be told from natives. On the shared
allocation, which charges household children's costs to the adults, the same re-weighting gives
India +$13,452, natives −$1,657, Pakistan/Bangladesh −$1,709, Venezuela −$2,329 and Mexico
−$7,903. Two bands only; this is not a lifetime account, and it prices no descendants.

## What the account cannot see: ACS 2024 proxies (large samples, no dollars)

The CPS account transports public medical spending by age band and US birth only, so an origin's
own Medicaid reliance does not enter. The ACS shows where that matters.
[DATA: `derived/acs_origin_screen.csv`, ACS 2024 one-year PUMS, foreign-born by birthplace]

| Birthplace | Foreign-born | BA+ (25–64) | Poverty | Medicaid, all ages | Medicaid, 65+ | SSI, 65+ | Social Security, 65+ | Income ≥ $100k (25–64) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| India | 3,176,719 | 85.9% | 6.1% | 7.5% | 20.8% | 6.7% | 61.9% | 48.3% |
| United Kingdom | 320,096 | 69.2% | 6.1% | 6.7% | 8.5% | 1.7% | 76.3% | 46.6% |
| Korea | 1,078,899 | 69.7% | 10.4% | 15.2% | 28.1% | 11.5% | 72.9% | 29.5% |
| Russia | 431,452 | 69.4% | 12.6% | 24.1% | 42.1% | 17.5% | 62.1% | 27.4% |
| Ukraine | 508,017 | 55.8% | 12.9% | 30.9% | 41.9% | 19.4% | 65.6% | 22.3% |
| China | 2,379,080 | 60.4% | 14.6% | 21.7% | 37.9% | 14.3% | 61.0% | 30.3% |
| Egypt | 222,127 | 68.7% | 18.2% | 28.8% | 26.0% | 7.9% | 67.1% | 24.0% |
| Armenia | 113,070 | 51.7% | 19.9% | 45.9% | 48.7% | 17.6% | 49.6% | 18.5% |
| Bangladesh | 353,066 | 49.9% | 16.3% | 39.5% | 48.4% | 12.5% | 44.4% | 15.0% |
| Venezuela | 998,984 | 48.3% | 19.3% | 14.3% | 14.0% | 2.8% | 32.1% | 9.6% |
| Mexico | 11,153,915 | 10.7% | 15.9% | 22.2% | 33.0% | 8.8% | 68.8% | 5.8% |

Russia-born and Ukraine-born residents aged 65 and over are on Medicaid at about 42%, twice the
India-born rate and five times the UK-born rate, and on SSI at 17–19% (India 6.7%, UK 1.7%);
only 62–66% draw Social Security. That is the pattern of people who arrived too old to build a contribution
record. The CPS account above therefore overstates the ex-Soviet balance by an amount this lane
does not measure. [INFERENCE from the two tables]

## Answer to the question

1. **Best-measured example of "educated but not positive": Philippines-born.** About a thousand
   CPS records, 54–56% with degrees, adult balance indistinguishable from zero and below the
   native average. The driver is age structure (family reunification of parents), not earnings:
   the working-age balance is +$15,575, above natives.
2. **Most likely to be negative once Medicaid is measured by origin: Bangladesh-born and
   Armenia-born.** Half hold degrees; 40–46% are on Medicaid; 15–19% earn $100,000 or more
   against 48% of the India-born. The CPS has too few records for either alone (Pakistan and
   Bangladesh pooled: +$448, −$4,882 to +$5,779 shared). The ACS one-year file should hold a few
   thousand Bangladesh-born records (353,066 people at typical weights near 100) [INFERENCE], so
   the next step is an ACS-based account, as `indian_ledger_2026_09_18` did.
3. **Russians: positive on this account, with an elderly population that is among the heaviest
   users of Medicaid and SSI of any educated group.** The sign of the whole group is unlikely to
   flip; the size is overstated.
4. **Venezuela-born: the largest degree-conversion failure measured here**, −$19,402 against
   native degree holders. 69% of Venezuela-born adults entered in 2016 or later (India-born 37%,
   former USSR 26%), so part of the gap is recency and unsettled work authorisation [INFERENCE];
   the group stays positive because only 9% of its adults are 65+.

## Limits

- One CPS year. Small origins have intervals wider than their estimates. The support rule
  (n ≥ 30 and effective n ≥ 20 per age band) holds in all six age bands for Mexico, India,
  China, the Philippines, Korea, Canada and the 13-code former USSR; it fails in one or two bands
  for Pakistan/Bangladesh, the United Kingdom, Venezuela, Russia/Ukraine and Taiwan/Hong Kong,
  and in three or more for Brazil, Japan, Nigeria, Germany, Poland, Egypt and Iran
  (`unsupported_age_bands` in the CSV).
- Adults 25 and over only; children enter through the shared allocation's household costs.
- Current attainment, not education at arrival; foreign and US degrees are not distinguished.
- Age at arrival, years in the country and legal status are not held constant. The CPS
  under-covers recent arrivals.
- Excludes institutional costs (N) and average public goods (F); medical spending is transported
  by age band and US birth, not by coverage type.
- Levels depend on the account. Ladder 150 put the same 1,232 India-born working-age records at
  +$24,163 on the September 18 ledger (white reference +$13,431); this account gives +$34,582
  (+$17,262). Sign and ranking agree; the two are not reconciled item by item.
- A resident account describes who is here. It does not identify the effect of admitting more
  people from any origin. [FRAMING-SENSITIVE: whether "not positive" means below zero or below
  the native average changes which groups qualify; both benchmarks are shown.]
