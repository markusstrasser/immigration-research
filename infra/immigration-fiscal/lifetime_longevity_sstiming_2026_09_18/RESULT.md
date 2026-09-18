claude-opus-5[1m]

**Verdict:** Both objections are real and both are small, and the one that is usually stated in the immigrant-favourable direction runs the other way. **Longevity costs the Mexican-origin groups, it does not help them**: giving them the Hispanic life table instead of the white one widens the complete-account lifetime gap against third-plus non-Hispanic whites by **$59.8k (Mexico-born), $66.2k (second generation) and $69.2k (third-plus)** undiscounted from birth, $5.1k to $5.9k at 3%. But almost all of that is undone by using *Mexican-specific* mortality rather than the pooled Hispanic table: Fenelon, Chinn and Anderson's hazard ratios put Mexican-origin mortality **above** the white reference at ages 25-64 and below it only at 65+, which cuts the effect to **$26.1k / $11.2k / $11.8k**, and leaves the union's whole lifetime gap **$1,283 from where the repo's terminal-83 convention already had it**. On Social Security timing the two halves of the correction point in opposite directions: charging workers the present value of the benefits this year's OASDI tax buys them **narrows** the −$7,224 common-age gap by **$1,041 to −$6,183** (whites pay more tax, so they accrue more liability), while the complete switch from a cash basis to an accrual basis — which also credits back the benefits the account charges to today's retirees — **widens** it by **$675 to −$7,899**. **No arm, in any combination, closes or reverses the gap**: across 576 Mexican-origin cells not one is non-negative, and the most favourable is −$3,198 per year for the third-plus self-identified group. Against the 2026-09-16 pass, which priced the same swap at **$20,000, about 5%** of a $375,000 partial-ledger gap on the COVID-depressed CDC 2021 tables, completing the account **raises** the share from 8.3% to **10.8%** for the second generation, confirming that pass's own prediction of a larger term still under 15%; the Mexican-specific arm then cuts it to **1.8%**.

[DATA: NVSS United States Life Tables 2024 (NVSR Vol 75 No 5) and 2023 (Vol 74 No 6), complete tables by Hispanic origin, race and sex; SSA Actuarial Note 2025.7 Table 1; CPS ASEC 2025, 142,125 person records]
[INFERENCE: a period life table applied to a period fiscal profile is a synthetic-cohort device twice over, not a projection of anyone's life]
[UNVERIFIED: the 75+ band's per-person balance is carried flat to age 100, and NVSS models Hispanic mortality above age 84 rather than observing it]

## Files

- `/Users/alien/Projects/immigration-research/infra/immigration-fiscal/lifetime_longevity_sstiming_2026_09_18/longevity.py`
- `/Users/alien/Projects/immigration-research/infra/immigration-fiscal/lifetime_longevity_sstiming_2026_09_18/ss_timing.py`
- `/Users/alien/Projects/immigration-research/infra/immigration-fiscal/lifetime_longevity_sstiming_2026_09_18/combine.py`
- `/Users/alien/Projects/immigration-research/infra/immigration-fiscal/lifetime_longevity_sstiming_2026_09_18/README.md`
- `derived/`: `survival_tables.csv` (1,414 rows), `longevity_lifetime.csv` (400), `longevity_gaps.csv` (320), `mwr_table.csv` (55), `ss_timing_arms.csv` (96), `ss_timing_group.csv` (12), `ss_timing_by_band.csv` (768), `combined_lifetime.csv` (864), `combined_summary.csv` (576), two audit JSONs, one cached CPS frame

## Gates executed

| gate | result |
|---|---|
| terminal-83 lifetime reproduces the pronatal lane's `lifetime_equivalence.csv` | max \|diff\| **$0.000000** — PASS |
| hazard-rebuild at HR = 1 reproduces the White non-Hispanic table | \|Δe0\| **0.0000 years** — PASS |
| 40 group x band populations reproduce `age_profiles_references.csv` | max \|diff\| **0.000000 people** — PASS |
| money's worth table parses to 5 levels x 11 cohorts, monotone in earnings | PASS |
| every life table: 101 ages, radix 100,000, monotone `lx` | PASS (14 tables) |
| re-run from scratch reproduces `derived/` | see **Reproducibility** below |

**External check, not a gate.** The account's OASDI payroll tax on CPS civilian households is **$1,347.8bn**, against **$1,293.3bn** of published 2024 net payroll tax contributions [SOURCE: 2025 OASDI Trustees Report, short-range estimates, combined OASDI table, `_cache/ssa_tr2025_IVA.html`]. The ratio is **1.0422**: the CPS calculation applies statutory rates to all reported wage and salary income, including employment not covered by OASDI. A `coverage_scale = 0.9595` arm rescales to the published total and moves the headline gap change from $1,041 to $999.

---

# Relation to the 2026-09-16 pass

Longevity was priced once before, and this lane does not redo it. [SOURCE: `research/immigration-mexican-origin-by-generation-2026-09-16.md` section 5.1, built by `infra/immigration-fiscal/cps_generation_welfare_2026_09_16/lifecycle_ledger_by_generation.py`, commit `1dc8b8e`] That pass ran the **CDC 2021** period life tables against the **partial** working-age ledger plus transported health, all-members allocation, undiscounted, and reported the swap as *"about $20,000 undiscounted, $1,600 at 3%, roughly 5% of the $375,000 white-versus-Mexican-second-generation gap from birth."*

Reading its stored output confirms the figure: the Mexican second generation moves from −186,415 on the Hispanic table to −166,963 on the white one, a swap of **$19,452** inside a gap of **$374,627**, which is **5.2%** [SOURCE: `cps_generation_welfare_2026_09_16/lifecycle_ledger_result.txt` lines 69-84]. Expected years lived in that pass were **78.3 Hispanic against 77.1 White non-Hispanic, a 1.2-year gap** — the 2021 tables are COVID-depressed, which is why the gap has since widened to 2.88 years.

**Life-table vintage.** The CSV in the derived root is the 2021 table (NVSR 72-12), so the brief's fallback applies. This lane goes past it: the central tables are **2024** (NVSR Vol 75 No 5, published 2026-08-25, the latest final year), with **2023** (NVSR Vol 74 No 6) carried as a stability arm. The 2023-versus-2024 choice moves the Mexico-born complete gap by 0.4%, so the vintage question is settled either way.

**The prior pass made a prediction. It holds.** It wrote that with a 2.9-year gap instead of 2021's 1.1, *"the term is roughly 2.5 times larger, still under 15%."* Measured on the same share basis, second generation, undiscounted from birth:

| | life tables | ledger | swap $ | gap $ | share |
|---|---|---|---:|---:|---:|
| 2026-09-16 pass | CDC 2021, 1.2-year gap | partial + health, all-members | 19,452 | 374,627 | **5.2%** |
| this lane, partial | NVSS 2024, 2.88-year gap | partial, pronatal profiles | 43,982 | 528,489 | **8.3%** |
| this lane, complete | NVSS 2024, 2.88-year gap | complete (ladder 130) | 66,152 | 610,857 | **10.8%** |

The multiplier is 1.6x on the partial account and **2.1x on the complete one**, against the predicted 2.5x, and both sit under the predicted 15% ceiling. The prediction was slightly conservative and correct in direction.

**Does completing the account move the share? Yes, upward, by about a third.** Undiscounted from birth, the longevity term as a share of the lifetime gap:

| group | partial | complete |
|---|---:|---:|
| Mexico-born | 6.6% | **9.1%** |
| 2nd generation | 8.3% | **10.8%** |
| 3rd+ self-ID | 11.6% | **14.4%** |

The mechanism is direct. The complete account adds a uniform charge of $6,926 to $7,762 per person-year on top of the partial profile, so every extra year of life carries that charge too. Extra years are pure cost on the complete account in a way they are not on the partial one. At 3% the shares collapse to 1.8-3.2%, because the disputed years are 50 to 100 years out.

**The nativity split the prior pass left open.** It flagged the question and cited linked-mortality evidence that US-born Hispanic life expectancy at 50 is at parity with whites while the advantage concentrates in the foreign-born at about +2.8 years at 50 [SOURCE: as cited there, Cantu et al. NHIS-LMF; García et al. 2018, *Innovation in Aging* 2(2)]. This lane resolves it two ways and both agree with that direction.

The crude version is the `paradox_fades` arm: Hispanic table for Mexico-born, white table for their descendants, which zeroes the longevity term for the second and third-plus generations by construction. The measured version is the `fenelon_mexican` arm below, built from Mexican-origin hazard ratios by nativity. Its rebuilt life expectancies are **79.76 at birth and 21.70 at 65 for the foreign-born, 79.20 and 20.32 for the US-born, against 78.93 and 19.47 for the white reference**, so the advantage roughly halves between the generations rather than vanishing.

Under that arm the longevity term falls to **4.0%, 1.8% and 2.5%** of the complete-account gap — **below the 5.2% the 2026-09-16 pass measured on the COVID-depressed 2021 tables.** Two errors in the prior pass were cancelling: it used life tables that understated the Hispanic advantage, and it applied that advantage to a Mexican-origin population that does not have the pooled Hispanic one. Correcting both leaves the prior 5% conclusion standing, and for a better reason than it was originally given.

---

# Phase A — longevity

## What the life tables say

[SOURCE: NVSR Vol 75 No 5, "United States Life Tables, 2024", Arias, Xu and Tejada-Vera, August 25 2026, abstract] life expectancy at birth in 2024 was **81.8 for the Hispanic population** and **78.9 for the White non-Hispanic population**. Rebuilt from the published `Lx` columns the figures are 81.81 and 78.93, a gap of **+2.88 years**. The gap is +3.00 years at age 25 and **+2.31 years at age 65** [CALCULATION: `derived/longevity_audit.json`].

The objection is therefore correctly stated: the repo gives everyone 83 years, and the Hispanic 65+ bands should be drawn about 2.3 years longer than the white ones.

## Two effects, opposite signs

Replacing the terminal age does two things at once, and they must be reported apart.

**Realistic survival, applied to everyone, narrows the gap.** Under the white life table for every group, the white reference's lifetime balance falls from +$399,670 to +$385,196 (partial account, undiscounted, from birth) while Mexico-born rises from −$154,904 to −$143,678. Mortality removes person-years from both ends; the white profile's working years are worth $10k-$15k each and the Mexican-origin ones $1k-$6k, so the reference loses more. The union's complete-account lifetime gap narrows from −$548,270 to −$520,627.

**The Hispanic longevity advantage then widens it.** Swapping the Hispanic table in for the three Mexican-origin groups, holding profiles fixed, is the longevity difference alone:

| longevity alone, complete account, $ per person | Mexico-born | 2nd gen | 3rd+ self-ID |
|---|---:|---:|---:|
| undiscounted, from birth | **+59,759** | **+66,152** | **+69,154** |
| undiscounted, from 25 | +61,274 | +67,692 | +70,634 |
| 3%, from birth | +5,141 | +5,614 | +5,903 |
| 3%, from 25 | +11,298 | +12,257 | +12,749 |

All positive: longer life is a fiscal cost here, because every year past 65 in these profiles is a deficit year. On the partial account the same figures are +$37.4k / +$44.0k / +$47.4k undiscounted.

Restricting the mortality difference to ages 65 and over (`mortality_65plus`: white survival to 65, group-specific conditional survival after) recovers **73%** of the effect — +$43.6k / +$48.9k / +$51.1k undiscounted. So roughly three-quarters of the longevity penalty is old-age survival and one-quarter is the higher chance of reaching old age at all.

## The arm that nearly cancels it

The pooled Hispanic life table is the wrong instrument for a Mexican-origin population.

> "Both US-born and foreign-born Mexicans between ages 25 and 64 have mortality disadvantaged relative to non-Hispanic whites, while older Mexicans exhibit clear advantages."
> — [SOURCE: Fenelon A, Chinn JJ, Anderson RN, "A comprehensive analysis of the mortality experience of hispanic subgroups in the United States: variation by age, country of origin, and nativity", *SSM - Population Health* 2017;3:245-254, abstract]

> "Although much of the focus of the Hispanic paradox is on Mexican-origin populations, foreign-born Dominicans, Central/South Americans, and other Hispanics have the most consistent mortality advantage across age and sex among Hispanic subgroups."
> — [SOURCE: same paper, Results]

Their unadjusted hazard ratios against non-Hispanic whites (Model 1, tables 3 and 4), Mexican origin:

| | men 25-64 | women 25-64 | men 65+ | women 65+ |
|---|---:|---:|---:|---:|
| US-born | 1.22 (1.15-1.30) | 0.98 (0.91-1.06) | 0.87 (0.81-0.94) | 0.92 (0.86-0.99) |
| foreign-born | 1.18 (1.11-1.25) | 1.28 (1.19-1.38) | 0.71 (0.64-0.78) | 0.79 (0.72-0.86) |

The `fenelon_mexican` arm rebuilds a life table from the white `qx` with those hazards (sexes averaged, HR = 1 below 25, where the paper has no estimate). Rebuilt life expectancy at birth: **79.76 foreign-born Mexican, 79.20 US-born Mexican, against 78.93 White non-Hispanic** — an advantage of 0.8 and 0.3 years, not 2.9. The longevity-only effect falls to **+$26,120 / +$11,158 / +$11,788** undiscounted, that is to **44%, 17% and 17%** of the pooled-Hispanic figure.

The generational point the brief asked for is in the same numbers: the 65+ advantage is 0.71-0.79 for the foreign-born and 0.87-0.92 for the US-born, so it is roughly **halved** by the second generation rather than eliminated. The `paradox_fades` arm, which gives the Hispanic table only to Mexico-born and the white table to their descendants, is the crude version of that; the Fenelon arm is the measured one.

NVSS itself reports the range the paradox sits in: *"A consistent finding across diverse studies has been that Hispanic mortality in the adult and advanced ages varies between about 80% and 89% relative to that of the White non-Hispanic population"* [SOURCE: NVSR 75-05, Technical Notes]. Fenelon's Mexican-origin 65+ ratios sit inside that band; his 25-64 ratios sit above 1 and outside it entirely.

## The headline for Phase A

On the union's complete-account lifetime gap against third-plus whites, undiscounted from birth, against the repo's terminal-83 baseline of **−$548,270**:

| survival arm | union lifetime gap | change vs repo |
|---|---:|---:|
| terminal83 (repo) | −548,270 | 0 |
| common_white | −520,627 | +27,643 |
| **fenelon_mexican** | **−549,554** | **−1,283** |
| mortality_65plus | −567,636 | −19,366 |
| group_specific (pooled Hispanic) | −584,655 | −36,385 |

Positive means the gap narrowed. **Under Mexican-specific mortality the whole longevity correction is worth −$1,283 on a −$548,270 gap, which is 0.2%.** The repo's terminal-83 convention is, by accident, almost exactly right for this population, because the two effects it gets wrong cancel.

At 3% the arms compress to a range of −$234,828 to −$240,789, a spread of 2.5%; discounting kills most of the longevity question, since the years in dispute are 50 to 100 years out.

## Stability and brackets

The 2023 life tables in place of 2024 move the Mexico-born complete gap from −$654,640 to −$652,075, **0.4%**. Single-sex tables bracket the both-sex central arm: male −$647,631, female −$656,535 against −$654,640. Both are small against the pooled-versus-Mexican-specific choice, which is worth $34k.

---

# Phase B — Social Security timing

## Method

[SOURCE: SSA Actuarial Note 2025.7, "Money's Worth Ratios Under the OASDI Program for Hypothetical Workers", Karen Rose and Kyle Burkhalter, December 2025] defines the money's worth ratio as *"the ratio of the present value of expected benefits to the present value of expected payroll taxes (contributions) for an individual or a cohort of workers"*, on the intermediate assumptions of the 2025 Trustees Report. So the present value of the benefits a dollar of 2024 OASDI tax buys is exactly that dollar times the ratio.

Each CPS person's accrued liability is `MWR × OASDI tax paid in 2024`, with the tax computed as `2 × 6.2% × min(wage, $168,600)` plus a self-employment component. The ratio is interpolated bilinearly in birth year (11 cohorts, 1920 to 2004) and in log earnings relative to the average wage index, against the note's five hypothetical career-average levels — Very Low, Low, Medium, High and Maximum at $16,556, $29,800, $66,223, $105,957 and $163,970 wage-indexed to 2023 [SOURCE: Note 2025.7 Table A], which are 0.249, 0.447, 0.994, 1.590 and 2.461 times the 2023 average wage index of $66,621.80 [SOURCE: ssa.gov/oact/cola/awidevelop.html]. Family type is the person's own: married with an earning spouse takes the two-earner-couple column, married as the sole earner takes the one-earner-couple column, unmarried takes the single column for their sex. Assigning the couple ratio to the earner and nothing to the non-earning spouse counts each couple's auxiliary benefits exactly once.

The earnings and family inputs, ages 21-64:

| group | mean wage incl. zeros | ratio to AWI | share married | share sole earner in a couple | OASDI tax per resident, all ages |
|---|---:|---:|---:|---:|---:|
| Mexico-born | 33,685 | 0.482 | 0.568 | 0.189 | 3,629 |
| 2nd generation | 42,738 | 0.612 | 0.333 | 0.072 | 2,745 |
| 3rd+ self-ID | 46,856 | 0.671 | 0.410 | 0.083 | 2,712 |
| 3rd+ NH white | 63,773 | 0.913 | 0.555 | 0.123 | 4,331 |
| all natives | 58,927 | 0.844 | 0.480 | 0.105 | 3,837 |

## Two adjustments, opposite signs

**`accrual_only` — the objection as usually stated.** Charge every worker the present value of the benefits their 2024 tax accrues, and leave the 2024 retiree's benefit where it is. Per resident person-year: union **−$4,600**, white **−$5,758**, all natives −$5,124. For the union that is **−$188.1bn** a year; for the white reference −$996.5bn.

Standardized to the white age mix, the union's complete common-age gap moves from **−$7,224 to −$6,183, a narrowing of $1,041 or 14.4%.** The reason is arithmetic and unflattering to the objection: the implicit ratio of accrued liability to tax paid is **1.53 for the union and 1.33 for the white reference**, so each Mexican-origin dollar does buy more future benefit, but whites pay 1.44 times as much tax per person, and the tax difference dominates the ratio difference.

**`cash_to_accrual` — the complete switch.** An accrual account cannot charge the 2024 worker for benefits they will claim in 2050 *and* charge 2024 for benefits accrued in 1985. Crediting back the OASDI benefits the account charges to today's retirees: union **−$3,347** per person-year (−$136.9bn), white **−$834** (−$144.4bn). The gap moves from **−$7,224 to −$7,899, a widening of $675 or 9.3%.**

The white reference receives **$4,924** of Social Security per resident per year against the union's **$1,253**, because it is far older. Removing that charge from 2024 is worth nearly four times as much to the reference as to the union, and it swamps the accrual side.

**The correct read is the second one.** The first is the arm that answers the objection in the form it is usually put, and it is the arm that helps the Mexican-origin groups; it is also internally inconsistent. The objection, stated completely, makes the gap worse.

## Arms

Union, change in the common-age gap, dollars per standardized person. Positive narrows the gap toward zero.

| family | earnings | self-empl. | coverage | accrual_only | cash_to_accrual |
|---|---|---|---|---:|---:|
| observed (central) | individual | in | 1.000 | **+1,041** | **−675** |
| observed | individual | in | 0.960 | +999 | −717 |
| observed | individual | out | 1.000 | +983 | −733 |
| observed | group mean | in | 1.000 | +1,362 | −354 |
| all one-earner couple | individual | in | 1.000 | +1,620 | −96 |
| all two-earner couple | individual | in | 1.000 | +996 | −721 |
| all single man | individual | in | 1.000 | +947 | −769 |
| all single woman | individual | in | 1.000 | +1,028 | −688 |

`accrual_only` narrows the gap in all eight arms, by $947 to $1,620. `cash_to_accrual` widens it in all eight, by $96 to $769. No arm changes either sign.

## Cross-check: the Trustees, and Goss et al. 2013

**Route 2, the Trustees' immigration sensitivity.** [SOURCE: 2025 OASDI Trustees Report, appendix VI.D, table VI.D3] the 75-year actuarial balance is **−4.28, −3.82 and −3.40 percent of taxable payroll** at average annual net immigration of 833,000, 1,253,000 and 1,696,000 for 2035-2099. The report states: *"Increasing average annual total net immigration by 100,000 persons increases (improves) the long-range actuarial balance by about 0.10 percent of taxable payroll."* The 2026 report repeats the coefficient at the same 0.10 with a lower intermediate assumption of 1,176,000.

**Route 3, unauthorized immigrants.** [SOURCE: SSA Actuarial Note 151, Goss, Wade, Skirvin, Morris, Bye and Huston, April 2013] *"While unauthorized immigrants worked and contributed as much as $13 billion in payroll taxes to the OASDI program in 2010, only about $1 billion in benefit payments during 2010 are attributable to unauthorized work. Thus, we estimate that earnings by unauthorized immigrants result in a net positive effect on Social Security financial status generally, and that this effect contributed roughly $12 billion to the cash flow of the program for 2010."*

**They disagree with my route, and the disagreement is not an error in either.** Both SSA results are positive for immigration; my accrual charge is negative for every group. Three reconciliations, in order of size.

1. **Admission versus residence.** The Trustees vary a *flow* of new arrivals, who are young; the repo measures a *resident stock* with its own age structure, including its retirees. The Trustees' own explanation is explicit: *"The cost rate decreases with an increase in total net immigration because immigration occurs at relatively young ages, thereby increasing the numbers of covered workers earlier than the numbers of beneficiaries."* That is a statement about arrival age, not about lifetime value.
2. **Pay-as-you-go versus accrual.** The money's worth ratio charges the full present value of a worker's own future benefits to the year the tax is paid. It is silent on the fact that in a pay-as-you-go system that same tax is simultaneously funding someone else's benefit today. The Trustees' measure captures that transitional gain; the accrual measure by construction cannot. Both are correct about different questions, and neither is the other's sanity check.
3. **Note 151 is a cash-flow statement, not an accrual one.** $13bn in, $1bn out is the same snapshot arithmetic the repo already does; it says nothing about the liability those $13bn accrue. Its distinctive claim is that a large share of unauthorized earnings never converts into a benefit at all, which would raise the Mexico-born accrual's true discount and push my `accrual_only` narrowing *further* in the immigrant-favourable direction. I have not priced it: the repo's CPS groups are not split by legal status, and Note 151's 2010 vintage precedes the 2012 Trustees assumptions it is built on.

One thing the ratios are not is a group story. In Note 2025.7's Table 1 the ratio exceeds 1 in 31 of 55 single-man cells and in all 55 one-earner-couple cells, but it stays **below** 1 for every maximum earner in every cohort after 1920 and for high earners in all but one. The accrual charge is negative for the white reference too, and larger for it, simply because the charge is a liability and whites pay more tax. Progressivity changes the ratio; it does not change the sign.

---

# Falsification

**The arm under which longevity and timing together would close or reverse the common-age gap does not exist inside the published ranges.** Each group is evaluated on 144 combinations of account, rate, start age, survival arm and timing arm; across the 576 Mexican-origin cells, **not one has a non-negative gap** on either the lifetime or the annual-equivalent measure.

The union's lifetime gap against third-plus non-Hispanic whites never rises above **−$142,985**, and its best annual equivalent is **−$3,949 per year**. The single most favourable cell for any Mexican-origin group is the third-plus self-identified group from age 25 on the partial account with `accrual_only` timing and white survival: **−$3,198 per year** undiscounted, or **−$102,339** as a lifetime total at 3%. Even that is 44% of the repo's −$7,224, and it is the group with the smallest gap on the account that omits the most items.

The two corrections work against each other in a way that makes closure structurally unavailable. The timing arm that narrows the gap, `accrual_only`, is the internally inconsistent one; the survival arm that narrows it, `common_white`, is the one that denies the Hispanic longevity advantage the objection is built on. **They cannot both be used**, because `common_white` is the arm that says Hispanic and white survival are the same, and the objection's whole premise is that they are not. Taking the objection at its word — pooled Hispanic survival plus the complete accrual switch — gives the union **−$7,626 per year** on the complete account from birth, against **−$6,606** for the same measure under the repo's own conventions. Stating the objection fully makes the gap 15% worse, not better. (That −$6,606 is the lifetime-annualized analogue of the repo's cross-sectional −$7,224; the two weight ages differently and are not the same statistic, which is why the comparison above is drawn within the measure rather than across.)

**Both channels are bounded, and neither bound reaches zero.**

On longevity, any Hispanic survival advantage *widens* the gap, so the most the channel can ever help is to have no advantage at all. That bound is the `common_white` arm: **+$27,643** on a −$548,270 lifetime gap, 5%. There is no arm on the other side of it, because a mortality *disadvantage* at 25-64 — which is what Fenelon actually measures — pushes back the other way through lost working years.

On timing, the accrual channel narrows the gap only to the extent the union accrues *less* liability than the white reference, and its accrual cannot go below zero. The absolute bound is therefore the white reference's own accrual, **$5,758 per standardized person**, reached only if Mexican-origin residents paid no OASDI tax whatsoever. Even that impossible arm leaves the gap at **−$1,466**, and it is self-defeating: removing their payroll tax also removes it from the receipts side of the same account, which widens the gap by more than the accrual saves. A larger money's worth ratio does not help either — it makes the union's accrued liability *larger*, which moves the gap the wrong way.

So closure is not a matter of finding a more generous parameter inside the published ranges. The signs of the two channels rule it out before the magnitudes are consulted.

# What was not done, and why

- **No sex-specific fiscal profiles.** The repo's bands are not split by sex, so the sex-specific life tables are reported as a bracket (±0.7% on the Mexico-born gap) rather than composited to each group's own sex mix.
- **No legal-status split.** Note 151's central mechanism — unauthorized earnings that never convert to a benefit — cannot be priced on CPS groups that do not carry status.
- **The 75+ band is carried flat to age 100.** Its value is the mean over everyone 75 and over, whose mean age is near 82; if the per-person deficit rises with age past 82, every survival arm understates the cost of extra years and the longevity penalty in Phase A is a floor.
- **NVSS models Hispanic mortality above age 84** with a Brass relational logit on the White non-Hispanic standard [SOURCE: NVSR 75-05, Technical Notes], so the ages where the terminal-age replacement matters most are the ages that are modelled rather than observed. The `truncate83` arm, which applies survival but still stops the sum at 82, isolates that: it puts the Mexico-born complete gap at −$639,888 against −$654,640, so about a quarter of the pooled-Hispanic longevity effect comes from the modelled tail.
- **Salmon bias is not corrected.** Turra and Elo's return-migration critique [cited by NVSR 75-05 as reference 28] implies the measured foreign-born advantage is overstated. Correcting it would move the result further toward the Fenelon arm, which is already reported.
- **No standard errors on the timing adjustment.** The CPS replicate weights are carried by the upstream estimator but the accrual is a deterministic function of a published ratio table; the arms matrix, not a standard error, is the width here.

# Reproducibility

`derived/` was copied aside, deleted in full — including the cached CPS frame, so the CPS ASEC build ran again from the zip — and all three scripts were re-run in order. **All 12 files reproduce byte-identically**, the Parquet cache included.

```
IDENTICAL  combined_lifetime.csv      IDENTICAL  ss_timing_arms.csv
IDENTICAL  combined_summary.csv       IDENTICAL  ss_timing_audit.json
IDENTICAL  cps_ss_stage.parquet       IDENTICAL  ss_timing_by_band.csv
IDENTICAL  longevity_audit.json       IDENTICAL  ss_timing_group.csv
IDENTICAL  longevity_gaps.csv         IDENTICAL  survival_tables.csv
IDENTICAL  longevity_lifetime.csv     IDENTICAL  mwr_table.csv
---
identical=12 differs=0
```

Both in-script gates re-fired on the fresh run: the terminal-83 lifetime reproduced the pronatal lane at $0.000000 and the 40 group x band populations reproduced `age_profiles_references.csv` at 0.000000 people. Nothing was committed and nothing outside this lane directory was written.
