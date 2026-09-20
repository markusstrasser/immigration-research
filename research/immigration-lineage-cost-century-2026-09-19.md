**Crime measurement correction, 2026-09-20:** Historical additions below import BJS prisoner stocks, unsplit ACS institutions and Texas arrest charges. These do not jointly identify lineage-specific ordinary offending or detention-adjusted crime costs. The [current scope](immigration-detention-crime-and-fiscal-scope-2026-09-20.md) governs reuse; actual detention spending remains a separate fiscal item, counted once.

# The hundred-year fiscal cost of one Mexico-born arrival's lineage

**Current qualification, 2026-09-19:** The scenarios below are retained historical
calculations. “Complete” means expanded **partial** coverage; the headline is
not a validated admission cost. Read the [projection checks](immigration-projection-backtest-2026-09-19.md):
recent education, parental nativity, policy and exit assumptions matter. Exit
does not universally improve balances when benefits continue abroad. The
original 0–100 horizon has 101 annual intervals; the new lane exports both
100 and 101. No numerical sampling interval supports the old “3–5× any plausible
interval” claim. These qualifications supersede the corresponding wording below.

**Verdict:** One Mexico-born arrival aged 25 who remains unauthorized, followed with their descendants for a century on the complete fiscal account, runs −$1.20M undiscounted, against +$97k for one third-plus non-Hispanic white of the same age followed the same way: a gap of −$1.30M, about −$13,000 a year, or −$515k at a 3% real discount. The founder's own lifetime is −$555k of the gap; the remaining 57% belongs to US-born descendants, and the single most expensive member of either lineage is the US-born second generation (−$664k per person against −$148k for the white second generation), partly because it is the only cohort whose whole life fits inside the window. No arm of 115 brings the lineage gap inside the founder's own lifetime gap (minimum ratio 1.16, central 2.3). Legal status is nearly irrelevant (legalisation at year 10 moves the gap 1.9%), ethnic attrition moves it 0.4%, and the measured second- and third-generation fertility is already below white, so the white reference lineage generates more people (3.15 vs 3.05) and forcing descendants up to white fertility widens the gap. What moves the gap most is the attribution rule, a definition of "lineage" rather than a measurement: −$848k when mixed children are halved, −$2.71M when every child is attributed whole to one parent. The absolute level is account-dependent and the gap is not: switching complete to partial moves the Mexican lineage by $1.21M and flips its sign, the gap by $0.23M. [CALCULATION on `ledger_absolute_2026_09_17` period profiles, reproduced to 5.8e-11 dollars; `demo_momentum_2026_09_16` fertility; `status_impute_2026_09_16`; `crime_cost_2026_09_16`; `mexican_origin_population_total_2026_09_19`] [FRAMING-SENSITIVE: attribution rule, account, horizon window; no return migration; no sampling intervals]

Date: 2026-09-19. Lane: `infra/immigration-fiscal/lineage_cost_2026_09_19/` (RESULT.md carries the full arm grid, parameter table and the six defects repaired in the scratch script it replaced).

## 1. Central case (complete account, personal allocation, per-capita attribution, low fertility, generation length 29, 100 years, 2024$)

| | Mexican lineage | White reference | Gap |
|---|---|---|---|
| Persons generated | 3.05 | 3.15 | −0.10 |
| Founder's own lifetime | −$428,735 | +$126,117 | −$554,852 |
| Lineage, 100 years, 0% | −$1,199,871 | +$97,280 | −$1,297,150 |
| Per year | −$11,999 | +$973 | −$12,972 |
| Present value at 3% | −$339,261 | +$175,374 | −$514,635 |
| Crime, social cost, 0% (not added to the fiscal line) | $136,160 | $52,733 | +$83,427 |

By generation: G1 −$428,735; G2 (0.847 persons, born year 4) −$562,455; G3 (0.548, year 33) −$78,083; G4 (0.384, year 62) −$85,362; G5 (0.269, year 91) −$45,235. Generations three and later are cut mid-life by the horizon and are not lifetime balances. Crime net of corrections already inside the ledger is $61,101 over the century, 4.7% of the fiscal gap. [SOURCE: `derived/lineage_table.csv`, `generation_breakdown.csv`, `white_reference.csv`]

## 2. Disconfirmation arms, all preregistered, none reverse

(a) G4+ at the attrition-corrected mixed profile: +0.4%. (b) Founder legalised at year 10: +1.9% (ladder 85 at lineage scale). (c) Descendants at white fertility: −4.5%, the wrong direction for the pro-side hypothesis, because measured second-generation fertility (age-standardised own children under 5, 0.1921) is already below third-plus white (0.2275). [SOURCE: `derived/sensitivities.csv`; `demo_momentum_2026_09_16`]

## 3. Sensitivity ranking (lineage gap from central −$1.30M)

Maternal-full attribution −$2.71M; 1% real growth −$2.03M; high fertility (NVSR 2010 origin-specific TFRs) −$2.02M; group-specific mortality −$1.45M; generation length 26 −$1.35M; shared allocation −$1.32M; generation length 32 −$1.24M; partial account −$1.08M; unauthorized 65+ balance zeroed −$851k (a large, favourable, unsourced convention the scratch script used and the central case does not); intermarried-half attribution −$848k; 3% discount −$515k. [SOURCE: `derived/sensitivities.csv`]

## 4. Limits

Period profiles, not cohort projections; no general equilibrium, no behavioural response, no wage growth by default; no return migration (the largest unmodelled channel, direction unambiguous: smaller lineage, smaller gap); intermarriage is a rule, not a measurement; no sampling intervals propagated (arm spread is 3–5× any plausible interval); the pronatal lane's lifetime balances triangulate only to 0.1–5.4% and the residual is unresolved; crime line sits in a ±40% band by arrest year and is under 5% of the gap. Resident groups, not admission; no policy advice.

## Original sources

`ledger_absolute_2026_09_17/derived/lifetime/period_profiles.csv` and `age_profiles.csv`; `demo_momentum_2026_09_16` (age-standardised fertility by generation; NVSR 74-01 Table 2 white TFR 1.5325; NVSR 61-01 origin-specific 2010 TFRs); `status_impute_2026_09_16` (unauthorized penalty −$870 per adult-year); `crime_cost_2026_09_16`; `crime_cost_firstgen_2026_09_18`; `mexican_origin_population_total_2026_09_19` (fourth-plus identification 0.8881; attriter retained share 0.1995); NVSS life tables via `lifetime_longevity_sstiming_2026_09_18`; ladder 78, 85, 121, 130, 131, 158.

## Revisions

- 2026-09-20: Separated institutional residence, civil detention, criminal offenses and fiscal costs; historical counts are retained with narrower interpretation. [Decision](../decisions/2026-09-20-separate-detention-offenses-and-spending.md).

2026-09-19, later: [Matched accounts and projection checks](../decisions/2026-09-19-matched-accounts-and-projection-checks.md)
narrows completeness, horizon, uncertainty and exit-direction claims; preserves
the historical calculations and links current sensitivity tables above.
