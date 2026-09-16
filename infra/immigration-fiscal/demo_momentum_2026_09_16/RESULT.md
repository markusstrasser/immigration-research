# Demographic momentum: fertility by Hispanic generation + under-30 composition

**Verdict:** The momentum channel is WEAK and shrinking. Age-standardized, US-born Mexican-origin
women aged 15-44 now carry FEWER own children under 5 than third-plus non-Hispanic (NH) white women
(2nd gen 0.192, 3rd+ gen 0.208, NH white 3rd+ 0.228). Mexican-origin fertility has converged past
parity; only the Mexico-born are still above (0.251). The Mexican-origin share of the under-30
population FELL in Texas (41.1% -> 38.0%, 2010 -> 2023) and was flat nationally (15.0% -> 15.5%).
The X claim of a Texas under-30 population "increasingly drawn from ethno-collectivist groups" is
false for the Mexican-origin group that dominates that population; the growth is in other-Hispanic
(Venezuelan/Honduran/Guatemalan, immigration-driven) and NH Asian.

Model self-report: **claude-opus-5[1m]** (Opus 5, 1M context).

Provenance tags below: [SOURCE] primary data, [INFERENCE] my derivation, [UNVERIFIED] not checked.

---

## Validation gates

| Gate | Result |
|---|---|
| (a) Texas under-30 total, ACS 2023 1-year PUMS vs table B01001 | PUMS 12,609,155 vs B01001 12,615,048, diff -0.05% — **PASS** |
| (b) NH white TFR quoted matches NVSR final-data value | 1,532.5 per 1,000 for 2023, quoted directly from NVSR Vol. 74 No. 1, Table 2 (also Table 11) — **PASS** |

## 1. Fertility by generation — CPS ASEC 2025 own-children proxy

[SOURCE] `/Users/alien/research-data/immigration-fiscal/data/external/stage3/census/cps_asec_2025/asecpub25csv.zip`,
person file `pppub25.csv`. Generation coding follows `build/analyze_cps_fiscal_2025.py`: PENATVTY /
PEFNTVTY / PEMNTVTY, 303 = Mexico, US areas {57,60,66,69,73,78}. Own children under 5 linked via the
parent pointers PEPAR1/PEPAR2, where the pointer is the line number and `PPPOS = line + 40` (this
offset was the one non-obvious step; 94.4% of under-5s carry a parent pointer). Weight MARSUPWT/100.

No CPS June fertility supplement was available: the Census FTP `supp/` directories for 2022 and 2024
contain no June fertility file, so the own-children proxy is the measure. [SOURCE: directory listings
of https://www2.census.gov/programs-surveys/cps/datasets/2024/supp/ and .../2022/supp/]

Own children under 5 per woman aged 15-44, direct age-standardized to the NH white 3rd+ age
distribution (six 5-year groups):

| Group | n (unwtd) | Crude | Age-standardized | Implied TFR (rate x 6) |
|---|---|---|---|---|
| Mexico-born | 1,039 | 0.261 | 0.251 | 1.51 |
| Mexican 2nd gen (US-born, >=1 Mexico-born parent) | 1,818 | 0.168 | 0.192 | 1.15 |
| Mexican 3rd+ gen (US-born, US-born parents, Mexican self-ID) | 1,386 | 0.185 | 0.208 | 1.25 |
| NH white 3rd+ gen | 13,506 | 0.228 | 0.228 | 1.37 |

Age-specific rates (own kids u5 per woman):

| Group | 15-19 | 20-24 | 25-29 | 30-34 | 35-39 | 40-44 |
|---|---|---|---|---|---|---|
| Mexico-born | 0.047 | 0.289 | 0.300 | 0.403 | 0.283 | 0.166 |
| Mexican 2nd gen | 0.018 | 0.114 | 0.258 | 0.363 | 0.253 | 0.121 |
| Mexican 3rd+ gen | 0.023 | 0.103 | 0.294 | 0.392 | 0.300 | 0.109 |
| NH white 3rd+ gen | 0.008 | 0.076 | 0.295 | 0.441 | 0.363 | 0.143 |

Reading: the US-born Mexican-origin advantage over NH whites is confined to ages 15-24 (teen and
early-20s births, roughly 2-3x the white rate). From age 25 on, NH white women have MORE own young
children in the household. Crude means understate the gap-closing because Mexican-origin women
15-44 skew young (26.7% of 2nd-gen women in the 15-19 cell vs 17.3% of NH whites); the
standardization reverses the ordering, which is why the crude column must not be quoted alone.

Caveats [INFERENCE]: own-children-in-household undercounts fertility for women whose children have
left, died or live elsewhere, and slightly undercounts for foreign-born women with children abroad,
which biases the Mexico-born estimate DOWN. Standard errors are approximate (weighted variance, no
replicate weights); the 2nd-gen-vs-NH-white difference (0.192 vs 0.228) is roughly 2-3 SE with the
crude SEs of 0.011 and 0.005, so the sign is credible but the magnitude is soft.

Outputs: `cps_fertility_proxy.csv`, `cps_fertility_agestd.csv`.

## 2. NCHS natality — TFR by Hispanic origin, 2010 vs 2023

[SOURCE] NVSR Vol. 74 No. 1, "Births: Final Data for 2023" (Osterman et al., March 18, 2025),
Tables 2, 11 and 12, from https://stacks.cdc.gov/view/cdc/175204. [SOURCE] NVSR Vol. 61 No. 1,
"Births: Final Data for 2010", Tables 8 and 14, https://www.cdc.gov/nchs/data/nvsr/nvsr61/nvsr61_01.pdf.

| Group | TFR 2010 | TFR 2023 | Change |
|---|---|---|---|
| All races and origins | 1,931.0 | 1,621.0 | -16% |
| NH white | 1,791.0 (bridged race) | 1,532.5 (single race) | -14% |
| Hispanic, total | 2,350.0 | 1,946.0 | -17% |
| Mexican origin | 2,256.0 | not published separately in NVSR 74-01 | — |

The Mexican-to-NH-white TFR ratio was 1.26 in 2010. NVSR 74-01 stops publishing TFR by Hispanic
subgroup, so the 2023 ratio cannot be quoted from the report. [INFERENCE] Mexican-origin births fell
from 598,317 (2010, NVSR 61-01 Table 14) to 508,127 (2023, NVSR 74-01 Table 12), a 15% drop, while
the Mexican-origin female population of childbearing age grew, so the 2023 Mexican TFR is below the
Hispanic total of 1,946 and the ratio to NH whites is well under 1.26. The CPS proxy in section 1
puts US-born Mexican-origin fertility at or below the NH white level.

Share of births to Hispanic mothers: 945,200 of 3,596,017 in 2023 = **26.3%**, versus 945,180 of
3,999,386 in 2010 = **23.6%**. The absolute number of Hispanic births is unchanged over 13 years;
the share rose only because non-Hispanic births fell. Mexican-origin births are 14.1% of all US
births in 2023, down from 15.0% in 2010.

Nativity: 64.9% of Mexican-origin mothers in 2023 were born in the 50 states or DC, up from 42.1%
in 2010 (NVSR 74-01 Table 12; NVSR 61-01 Table 14). Hispanic births are now majority US-born-mother
(53.3% vs 44.3%) — the generational transition the memo studies is already most of the birth cohort.

## 3. Under-30 composition by state, ACS 1-year PUMS 2010 vs 2023

[SOURCE] Census API `acs1/pums?tabulate=weight(PWGTP)` for 2010 and 2023, AGEP 0:29, key from
`acquire/config.local.env`. Hispanic detail from a `row+HISP` tabulation (HISP=02 is Mexican);
NH race groups from HISP=01 crossed with RAC1P 1/2/6. A range predicate `HISP=03:24` silently
matched every record on the 2023 endpoint, so all Hispanic detail is computed from the per-value
HISP tabulation instead — anyone reusing this pattern should not trust range predicates on PUMS
string variables. Outputs: `acs_under30.csv`, script `acs_final.py`, raw responses in `_cache/`.

Percent of the population under 30:

| Geo | Group | 2010 | 2023 | Change (pp) |
|---|---|---|---|---|
| Texas | Hispanic Mexican | 41.07 | 37.96 | **-3.11** |
| Texas | Other Hispanic | 5.13 | 9.50 | +4.37 |
| Texas | All Hispanic | 46.20 | 47.46 | +1.26 |
| Texas | NH white | 35.88 | 30.67 | -5.21 |
| Texas | NH Black | 12.04 | 12.21 | +0.17 |
| Texas | NH Asian | 3.57 | 4.85 | +1.28 |
| Texas | Hispanic AND US-born | 38.75 | 41.95 | +3.20 |
| California | Hispanic Mexican | 41.37 | 41.51 | +0.14 |
| California | Other Hispanic | 6.95 | 9.05 | +2.10 |
| California | NH white | 29.90 | 24.17 | -5.73 |
| California | NH Black | 5.72 | 4.75 | -0.97 |
| California | NH Asian | 11.46 | 13.01 | +1.55 |
| California | Hispanic AND US-born | 39.99 | 45.85 | +5.86 |
| Arizona | Hispanic Mexican | 36.93 | 36.86 | -0.07 |
| Arizona | Other Hispanic | 3.46 | 5.53 | +2.07 |
| Arizona | NH white | 44.60 | 38.81 | -5.79 |
| Arizona | NH Black | 4.45 | 5.12 | +0.67 |
| Arizona | NH Asian | 2.50 | 3.17 | +0.67 |
| Arizona | Hispanic AND US-born | 34.49 | 38.96 | +4.47 |
| Florida | Hispanic Mexican | 5.39 | 5.26 | -0.13 |
| Florida | Other Hispanic | 21.89 | 26.54 | +4.65 |
| Florida | NH white | 46.92 | 40.44 | -6.48 |
| Florida | NH Black | 20.03 | 17.63 | -2.40 |
| Florida | NH Asian | 2.51 | 2.79 | +0.28 |
| Florida | Hispanic AND US-born | 20.59 | 24.98 | +4.39 |
| US | Hispanic Mexican | 15.04 | 15.45 | +0.41 |
| US | Other Hispanic | 6.92 | 9.76 | +2.84 |
| US | All Hispanic | 21.96 | 25.21 | +3.25 |
| US | NH white | 55.14 | 48.78 | -6.36 |
| US | NH Black | 13.89 | 12.69 | -1.20 |
| US | NH Asian | 4.67 | 5.40 | +0.73 |
| US | Hispanic AND US-born | 17.70 | 21.95 | +4.25 |

"Hispanic AND US-born" is NATIVITY=1 (born in the US, its territories, or abroad to US parents),
summed over all non-"01" HISP values.

Two facts the X claim gets wrong. First, the Mexican-origin under-30 share in Texas DECLINED by 3.1
points over 13 years; nationally it moved +0.4 points, inside sampling noise for a composition
measure. Second, the Hispanic under-30 population is now overwhelmingly US-born: 88.4% of Texas
Hispanics under 30 (4,394,375 of 4,785,854 Mexican-origin under-30 Texans are US-born by the same
tabulation). The under-30 Hispanic population is not an immigrant population; it is the second and
third generation the memo measures.

Where growth actually came from: "Other Hispanic" (+4.4 pp in Texas, +4.7 in Florida, +2.8 in the
US) and NH Asian. Both are immigration-driven, not fertility-driven.

## 4. Does the third-plus Mexican-origin share keep growing with zero further immigration?

[INFERENCE] Simple cohort-component sketch, no migration, generation-specific fertility from section 1.

Take net reproduction as proportional to the age-standardized own-children rate. Relative to NH white
3rd+ = 1.00: Mexican 2nd gen 0.84, Mexican 3rd+ gen 0.91, Mexico-born 1.10. With immigration set to
zero, the Mexico-born stock stops replenishing and ages out; the 2nd generation stops being fed by
new immigrant births within about one generation; the 3rd-plus generation keeps growing for two to
three decades purely from the age structure already in place, then stalls.

Rough magnitude per decade for the third-plus Mexican-origin share of the under-30 population:
- Decades 1-2: +1.5 to +2.5 pp per decade nationally, almost entirely reclassification as today's
  large second generation has children who are third generation. This is momentum from the existing
  age pyramid, not from higher fertility.
- Decade 3 onward: roughly flat to slightly declining, because third-plus Mexican-origin fertility
  (0.208) sits below NH white 3rd+ (0.228). At a ratio of 0.91 per generation, the group loses about
  9% of relative size every ~27 years once the age structures equalize.

So: the third-plus Mexican-origin share grows for 20-30 years from momentum alone and then turns
over. It does not compound. A second, larger caveat runs the other way — ethnic attrition. Duncan and
Trejo have shown repeatedly that third-plus-generation Mexican descendants with weaker Mexican
identification stop reporting as Mexican, which mechanically shrinks the measured third-plus group
and selects the remaining group toward lower socioeconomic status. Everything in this section is
about the SELF-IDENTIFIED third-plus population. [UNVERIFIED] I did not pull the Duncan-Trejo
attrition rates for this memo.

## 5. Literature

- Parrado and Morgan (2008), "Intergenerational Fertility Among Hispanic Women: New Evidence of
  Immigrant Assimilation", Demography 45(4): 651-671, doi:10.1353/dem.0.0023. Cross-sectional
  comparisons had suggested Mexican-origin fertility was NOT declining across generations; by
  combining biological and immigrant generations, so that immigrant women are compared with their own
  daughters' and granddaughters' generations rather than with contemporaneous cohorts, they find
  Hispanic and specifically Mexican fertility IS converging on white fertility and responds the same
  way to period conditions and education. Mexican-origin was the only subgroup with the sample size
  to disaggregate. [SOURCE: link.springer.com/article/10.1353/dem.0.0023]
- Lichter, Johnson, Turner and Churilla, "Hispanic Assimilation and Fertility in New Destinations",
  finds the same convergence pattern in new-destination counties. [SOURCE: PMC3544406]
- A 2018 update, "The fertility integration of Mexican-Americans across generations: confronting the
  problem of the 'third' generation" (Journal of Ethnic and Migration Studies), addresses exactly the
  ethnic-attrition problem in section 4. [UNVERIFIED] I located it but did not extract its numbers.
- The 2020s confirmation is in the data above, not the literature: the 2010-2023 NVSR series shows
  Hispanic TFR falling 17%, faster than the NH white 14% decline, closing the ratio from 1.31 to 1.27
  at the aggregate level while the US-born component converged much further.

## 6. Framing note [FRAMING-SENSITIVE]

The X claim conflates three separate things: the NH white share of the under-30 population falling
(true, -5.2 pp in Texas), the Mexican-origin share rising (false in Texas, flat nationally), and
higher fertility among the growing groups (false for US-born Mexican-origin, which is now below NH
white). The NH white under-30 share falls mainly because NH white fertility fell 14% since 2010 and
because "NH white" loses people to multiracial reporting, not because any other group out-reproduces
it. Labeling groups "ethno-collectivist" versus "individualist" is not a measurement; nothing in
these data speaks to it.

## Files

- `/Users/alien/Projects/immigration-research/infra/immigration-fiscal/demo_momentum_2026_09_16/cps_fertility_proxy.py`
- `.../age_std.py`, `.../cps_fertility_agestd.csv`, `.../cps_fertility_proxy.csv`
- `.../acs_under30.py`, `.../acs_fix.py`, `.../acs_final.py`, `.../acs_under30.csv`
- `.../_cache/` (all Census API responses, both NVSR PDFs)
