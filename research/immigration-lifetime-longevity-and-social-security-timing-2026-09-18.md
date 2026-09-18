# Two objections to a period account: longevity and Social Security timing

**Verdict:** Both objections are real, both are small, and the one usually raised in the group's favour runs against it. Giving the Mexican-origin groups the pooled Hispanic life table instead of the white one widens the complete-account lifetime gap against third-plus whites by $60k to $69k per person undiscounted, because every year past 65 in these profiles is a deficit year; with Mexican-specific mortality (Fenelon, Chinn and Anderson 2017: above the white hazard at 25–64, below it only at 65+) the effect shrinks to $11k to $26k, and the union's lifetime gap lands $1,283 from where the repo's terminal-age-83 convention already had it, 0.2%. On Social Security timing the two halves of the objection point opposite ways: charging this year's workers the present value of the benefits their tax accrues narrows the common-age gap from −$7,224 to −$6,183, while the internally consistent cash-to-accrual switch, which also stops charging today's retirees' benefits to today, widens it to −$7,899. Across 576 Mexican-origin cells no arm makes the gap non-negative; the best is −$3,198 per year. [SOURCE: `infra/immigration-fiscal/lifetime_longevity_sstiming_2026_09_18/RESULT.md`; `derived/combined_summary.csv`]

Date: 2026-09-18. Lane: `infra/immigration-fiscal/lifetime_longevity_sstiming_2026_09_18/` (three scripts, 12 derived files, reproduced byte-identically by the parent from the CPS zip). Prior result: the generation memo's §5.1 priced the same survival swap on the working-age partial ledger, undiscounted, at about $20,000 per adult, 5% of a $250,000 lifetime gap ([2026-09-16 memo](immigration-mexican-origin-by-generation-2026-09-16.md)); this memo moves it to the complete all-age account (ladder 130), adds discounting, the nativity split and Mexican-specific mortality, and prices the timing objection for the first time.

## 1. Longevity

Life expectancy at birth in 2024 is 81.8 Hispanic and 78.9 white non-Hispanic, a gap of 2.9 years at birth and 2.3 at 65. [SOURCE: NVSR 75-5, United States Life Tables 2024, Table A; rebuilt from the published Lx columns in `derived/survival_tables.csv`]

Replacing the constructed terminal age with survival does two things with opposite signs. Realistic survival for everyone narrows the gap, because mortality removes person-years from both groups and the white working years are worth $10k to $15k each against $1k to $6k: the union's complete lifetime gap goes from −$548,270 to −$520,627. The Hispanic advantage then widens it: holding profiles fixed and swapping only the table, +$59,759 (Mexico-born), +$66,152 (second generation), +$69,154 (third-plus) undiscounted from birth, $5.1k to $5.9k at 3%. Three quarters of that is survival after 65, one quarter the higher chance of reaching 65. [CALCULATION: `derived/longevity_gaps.csv`]

The pooled Hispanic table is the wrong instrument for a Mexican-origin population. Fenelon, Chinn and Anderson (SSM Population Health 2017) report unadjusted hazard ratios against non-Hispanic whites of 1.22 (US-born men 25–64), 1.18 and 1.28 (foreign-born men and women 25–64), and 0.71 to 0.92 at 65+. Rebuilding a life table from the white schedule with those hazards gives life expectancy of 79.8 (foreign-born Mexican) and 79.2 (US-born Mexican) against 78.9, an advantage of 0.3 to 0.8 years rather than 2.9. On that table the longevity effect is +$26,120 / +$11,158 / +$11,788, and the union's lifetime gap is −$549,554 against the terminal-83 −$548,270. [SOURCE: Fenelon et al. 2017 tables 3–4, quoted in RESULT.md; CALCULATION]

| Survival arm, union complete lifetime gap, undiscounted from birth | Gap | Change vs repo |
|---|---|---|
| Terminal 83 (repo convention) | −548,270 | 0 |
| White table for everyone | −520,627 | +27,643 |
| Mexican-specific (Fenelon) | −549,554 | −1,283 |
| Hispanic advantage at 65+ only | −567,636 | −19,366 |
| Pooled Hispanic table | −584,655 | −36,385 |

At 3% every arm sits between −$234,828 and −$240,789, a 2.5% spread: discounting removes most of the question because the disputed years are 50 to 100 years out. The 2023 tables move the Mexico-born gap 0.4%; single-sex tables bracket it by ±0.7%. [CALCULATION: `derived/combined_summary.csv`]

## 2. Social Security timing

Each CPS person's 2024 OASDI tax (2 × 6.2% of wages to the $168,600 cap, plus self-employment) is multiplied by the SSA money's-worth ratio for their birth cohort, earnings level and family type (Actuarial Note 2025.7, Table 1, interpolated in cohort and log earnings) to give the present value of benefits that tax accrues. [SOURCE: SSA Actuarial Note 2025.7; `derived/mwr_table.csv`] The account's OASDI tax on civilian households is $1,347.8bn against $1,293.3bn published for 2024, ratio 1.042, because statutory rates are applied to non-covered employment too; a coverage-scaled arm is reported. [SOURCE: 2025 Trustees Report short-range table]

Two adjustments. Accrual only, the objection as usually put: charge workers the accrued liability and leave today's retirees' benefits where they are. The union accrues 1.53 dollars of liability per tax dollar and the white reference 1.33, but whites pay 1.44 times the tax per person, so the tax difference dominates: the common-age gap narrows by $1,041 to −$6,183. Cash to accrual, the consistent version: an accrual account cannot charge 2024 for benefits accrued in 1985, so the $4,924 of Social Security per white resident and $1,253 per union resident charged to 2024 are credited back; the gap widens by $675 to −$7,899. Eight family, earnings, self-employment and coverage arms keep both signs (accrual only +$947 to +$1,620; cash to accrual −$96 to −$769). [CALCULATION: `derived/ss_timing_arms.csv`]

The SSA results that read as immigrant-favourable answer different questions. The Trustees' sensitivity (0.10% of taxable payroll per 100,000 net immigrants) varies a flow of young arrivals, which is admission, not the resident stock; Actuarial Note 151 (Goss et al. 2013, $13bn paid by unauthorized workers in 2010 against $1bn of benefits) is a cash-flow statement in the repo's own snapshot arithmetic and says nothing about accrued liability. Its distinctive point, that unauthorized earnings often never convert to a benefit, would push the accrual-only arm further in the group's favour and cannot be priced on CPS groups without legal status. [SOURCE: 2025 Trustees Report VI.D3; SSA Actuarial Note 151]

## 3. Why closure is unavailable

The two channels bind by sign. Any Hispanic survival advantage widens the gap, so the most longevity can help is the no-advantage arm, +$27,643 on −$548,270, and that arm denies the premise of the objection. The accrual channel narrows the gap only by the union accruing less than the reference, with an absolute bound at the reference's own accrual of $5,758 per standardized person, reached only if the union paid no OASDI tax, which removes the same dollars from the receipts side. Across 144 combinations of account, rate, start age, survival and timing arms for each of four groups, no Mexican-origin cell is non-negative; the best is the third-plus group from age 25 on the partial account, −$3,198 a year. [CALCULATION: `derived/combined_summary.csv`, 576 rows]

## 4. Limits

The 75+ band is carried flat to age 100, so the longevity penalty is a floor if the per-person deficit rises with age. NVSS models Hispanic mortality above 84 rather than observing it; truncating at 82 removes a quarter of the pooled-Hispanic effect. Salmon bias (return migration before death) overstates the foreign-born advantage and would move the result toward the Fenelon arm. No sex-specific profiles, no legal-status split, no standard errors on the accrual adjustment (the arms matrix is the width). [SOURCE: RESULT.md §What was not done]

## Sources

NVSS United States Life Tables 2024 (NVSR 75-5) and 2023 (NVSR 74-6). Fenelon A, Chinn JJ, Anderson RN, SSM Population Health 2017;3:245–254. SSA Actuarial Note 2025.7 (Rose and Burkhalter), Actuarial Note 151 (Goss et al. 2013), 2025 OASDI Trustees Report. CPS ASEC 2025 via the pronatal-lane profiles. Instrument note: LLM-assisted; every number reproduced by the lane scripts.
