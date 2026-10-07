# The hundred-year fiscal cost of one Mexico-born arrival's lineage

**Status:** The figures below are the lane's current outputs. Births need a parent alive
at 29 (conceptual audit 2026-09-27 §E); ethnic attrition uses the measured generation
split, with C3 measured on the CPS basic monthly files; and the ledger's expanded account
carries the income tax the survey misses, placed on the main case's keys (item T;
[decision](../decisions/2026-10-07-ledger-item-t-income-tax-keys.md)). Item T makes both
lineages pay more tax, the whites' far more, and adds $188,410 to the gap in the central
case and in every legalisation and statutory-bar arm. “Complete” means expanded
**partial** coverage; the headline is not a validated admission cost. Read the
[projection checks](immigration-projection-backtest-2026-09-19.md): recent education,
parental nativity, policy and exit assumptions matter, and exit does not universally
improve balances when benefits continue abroad. The 0–100 horizon has 101 annual
intervals; the projection lane exports both 100 and 101. The crime row imports BJS prisoner
stocks, unsplit ACS institutions and Texas arrest charges, which do not jointly identify
lineage-specific ordinary offending or detention-adjusted crime costs; the
[current scope](immigration-detention-crime-and-fiscal-scope-2026-09-20.md) governs reuse, and
actual detention spending remains a separate fiscal item, counted once.

**Verdict:** One Mexico-born arrival aged 25 who remains unauthorized, followed with their descendants for a century on the complete fiscal account, runs −$1.10M undiscounted, against +$377k for one third-plus non-Hispanic white of the same age followed the same way: a gap of −$1.48M, about −$14,800 a year, or −$570k at a 3% real discount. The founder's own lifetime is −$654k of the gap; the remaining 56% belongs to US-born descendants, and the single most expensive member of either lineage is the US-born second generation (−$608k per person against −$30k for the white second generation), partly because it is the only cohort whose whole life fits inside the window. No arm of 132 brings the lineage gap inside the founder's own lifetime gap (minimum ratio 1.15, central 2.3). Legal status acts through the senior years. The central case gives the never-legalised founder the pooled Mexico-born senior profile, under which legalising at year 10 narrows the gap 1.7%; with the programs federal law closes to someone never legalised removed from 65, legalising widens it by $417,886 (§2b). Ethnic attrition moves the gap 0.26%, and the measured second- and third-generation fertility is already below white, so the white reference lineage generates more people (3.09 vs 3.00) and forcing descendants up to white fertility widens the gap. What moves the gap most is the attribution rule, a definition of "lineage" rather than a measurement: −$977k when mixed children are halved, −$3.08M when every child is attributed whole to one parent. The absolute level is account-dependent and the gap much less so: switching complete to partial moves the Mexican lineage by $1.11M and flips its sign, the gap by $0.42M. [CALCULATION on `ledger_absolute_2026_09_17` period profiles, reproduced to 5.8e-11 dollars; `demo_momentum_2026_09_16` fertility; `status_impute_2026_09_16`; `crime_cost_2026_09_16`; `mexican_origin_population_total_2026_09_19`] [FRAMING-SENSITIVE: attribution rule, account, horizon window; no return migration; no sampling intervals]

Date: 2026-09-19. Lane: `infra/immigration-fiscal/lineage_cost_2026_09_19/` (RESULT.md carries the full arm grid, parameter table and the six defects repaired in the scratch script it replaced).

## 1. Central case (complete account, personal allocation, per-capita attribution, low fertility, generation length 29, 100 years, 2024$)

| | Mexican lineage | White reference | Gap |
|---|---|---|---|
| Persons generated | 3.00 | 3.09 | −0.09 |
| Founder's own lifetime | −$408,580 | +$245,205 | −$653,785 |
| Lineage, 100 years, 0% | −$1,099,425 | +$377,147 | −$1,476,572 |
| Per year | −$10,994 | +$3,772 | −$14,766 |
| Present value at 3% | −$310,108 | +$259,959 | −$570,067 |
| Crime, social cost, 0% (not added to the fiscal line) | $135,014 | $52,254 | +$82,760 |

The gap equals the Mexican lineage less the white reference in every row as printed; two cells (the Mexican 100-year total and the white per-year figure) are rounded away from the nearest dollar, by under $1 each, to keep that true.

By generation: G1 −$408,580; G2 (0.843 persons, born year 4) −$512,639; G3 (0.536, year 33) −$56,839; G4 (0.369, year 62) −$78,797; G5 (0.254, year 91) −$42,570. Generations three and later are cut mid-life by the horizon and are not lifetime balances. Crime net of corrections already inside the ledger is $60,610 over the century, 4.1% of the fiscal gap. [SOURCE: `derived/lineage_table.csv`, `generation_breakdown.csv`, `white_reference.csv`]

## 2. Disconfirmation arms, all preregistered, none reverse

(a) G4+ at the attrition-corrected mixed profile, on the measured generation split with C3 from the CPS basic monthly files: +0.26%. (b) Founder legalised at year 10: +1.7% under the pooled senior profile (ladder 85 at lineage scale). Under statutory eligibility from 65, legalising widens the gap by $417,886, −40.4%. With emergency Medicaid, state programs and uncompensated care priced for the never-legalised senior, it widens the gap by $250–400k, −21% to −38%, across the rules of 2020–2026, and by $355–390k, −32% to −37%, under the rules a new enrollee faced in 2026 (Revisions, 2026-09-25 and 2026-09-26). (c) Descendants at white fertility: −3.5%, the wrong direction for the pro-side hypothesis, because measured second-generation fertility (age-standardised own children under 5, 0.1921) is already below third-plus white (0.2275). [SOURCE: `derived/sensitivities.csv`; `demo_momentum_2026_09_16`]

## 3. Sensitivity ranking (lineage gap from central −$1.48M)

Maternal-full attribution −$3.08M; 1% real growth −$2.33M; high fertility (NVSR 2010 origin-specific TFRs) −$2.17M; group-specific mortality −$1.62M; generation length 26 −$1.54M; shared allocation −$1.49M; generation length 32 −$1.41M; partial account −$1.07M; unauthorized 65+ balance zeroed −$1.03M (a large, favourable, unsourced convention the scratch script used and the central case does not); intermarried-half attribution −$977k; 3% discount −$570k. [SOURCE: `derived/sensitivities.csv`]

## 4. Limits

Period profiles, not cohort projections; no general equilibrium, no behavioural response, no wage growth by default; no return migration (the largest unmodelled channel; the projection checks show that exit need not shrink the gap when benefits continue abroad); intermarriage is a rule, not a measurement; no sampling intervals propagated; the pronatal lane's lifetime balances triangulate only to 0.1–5.4% and the residual is unresolved; crime line sits in a ±40% band by arrest year and is under 5% of the gap. Resident groups, not admission; no policy advice.

## Original sources

`ledger_absolute_2026_09_17/derived/lifetime/period_profiles.csv` and `age_profiles.csv`; `demo_momentum_2026_09_16` (age-standardised fertility by generation; NVSR 74-01 Table 2 white TFR 1.5325; NVSR 61-01 origin-specific 2010 TFRs); `status_impute_2026_09_16` (unauthorized penalty −$870 per adult-year); `crime_cost_2026_09_16`; `crime_cost_firstgen_2026_09_18`; `mexican_origin_population_total_2026_09_19` (fourth-plus identification 0.8881; attriter retained share 0.1995); NVSS life tables via `lifetime_longevity_sstiming_2026_09_18`; ladder 78, 85, 121, 130, 131, 158.

## Revisions

- 2026-10-08, later: rewrote the memo to its current state. The verdict's four dated brackets, §2's five, the 2026-09-19 qualification and the 2026-09-20 crime note above the title became one Status paragraph and current text; the withdrawn "legal status is nearly irrelevant" sentence (2026-09-25) and §4's "direction unambiguous" and "3–5× any plausible interval" clauses (superseded 2026-09-19) are deleted, their records kept below. No figure changes. Concept affected: none; the lineage results' presentation.
- 2026-10-08: The verdict body, §1, §2 and §3 are restated on the lane's current outputs, because the white-reference ledger's expanded account now charges the income tax the survey misses on the main case's keys (item T; [decision](../decisions/2026-10-07-ledger-item-t-income-tax-keys.md)); the body had not taken the September 28 change either. Central at 0%: the gap −$1,297,150 → −$1,476,572 (−$1,288,162 after September 28) and −$514,635 → −$570,067 at 3%; the Mexican lineage −$1,199,871 → −$1,099,425 and the white +$97,280 → +$377,147; the founder's gap −$554,852 → −$653,785, so descendants carry 57% → 56%; legalising a never-legalised founder at year 10 still widens the gap by $417,886, 48.9% → 40.4%. Switching to the partial account still flips the Mexican lineage's sign, but it moves the gap $0.23M → $0.42M, so the verdict says the gap is much less account-dependent rather than not at all. Concept affected: the lineage's century cost against a white lineage (ladder 159).
- 2026-10-05: Ethnic attrition's C3, the share of the gap that attriters lost at the third-generation rate close, is now measured on the CPS basic monthly files 1994–2026 (526 unique G3 non-identifiers at 25+) pooled with NLSY97: 0.557 (SE 0.246), in place of 0.7758 ([g3_identity_pooled_2026_10_05](../infra/immigration-fiscal/g3_identity_pooled_2026_10_05/RESULT.md), monthly frame). Row 2a moves to −$1,284,710, 0.27% of the central; the central and every other arm do not move. Ladder 159 bracketed.
- 2026-09-28: Births now need a living parent (conceptual audit 2026-09-27 §E), and ethnic attrition uses the measured generation split ([carryover lane](../infra/immigration-fiscal/carryover_identity_2026_09_27/RESULT.md) §2, §5; 4e9c2e2). The gap moves from −$1,297,150 to −$1,288,162 (−$514,635 to −$513,398 at 3%); no ranking or sign changes. Ladder 159 and 241 bracketed.
- 2026-09-26: Priced what stays open to a never-legalised senior under the statutory rule: emergency Medicaid, state programs that cover people regardless of status (weighted by where unauthorized Mexico-born people aged 50–64 live), and the government-financed part of uncompensated care. Public care from 65 runs $1.1–2.9k a year with no state program, $1.6–3.8k under the rules a new enrollee faced in 2026 (California froze new full-scope enrollment at 19+ on 1 January 2026), and $4.3–10.0k with every state that covered unauthorized seniors in 2020–2025 open. Legalising at year 10 then widens the lineage gap by $355–390k (39–44%) under the 2026 rules and $250–400k (24–46%) across all three, against $418k (48.9%) with nothing priced. Even coverage everywhere at the highest price leaves $125k, because Social Security and the other cash programs ($10.7–11.6k a year) have no counterpart. Take-up and emergency Medicaid use are inference brackets. [CALCULATION: `lineage_cost_2026_09_19/RESULT.md` Revisions, `derived/sensitivities.csv` last twelve rows; sources `senior_pricing_sources.md`] [Decision](../decisions/2026-09-25-weekly-audit-corrections.md).
- 2026-09-25: Withdrew "legal status is nearly irrelevant". The lane gave an unauthorized founder the pooled Mexico-born profile from 65, so legalising could only remove the working-age difference, and ladder 85 measures working ages only. A statutory rule now removes from 65 the programs federal law closes to someone never legalised (cash transfers including Social Security, public medical, institutional care, noncash aid; 42 U.S.C. 402(y), 8 U.S.C. 1611) and keeps taxes and services. The never-legalised lineage gap is then −$854,686 (founder −$112,387), and legalising at year 10 moves it to −$1,272,572, a 48.9% larger gap; the zero-senior rule gives −$850,861. Emergency Medicaid, state coverage such as California's and uncompensated care are not added back, so legalising raises the lineage's cost unless those come close to the federal entitlements they replace. [CALCULATION: `lineage_cost_2026_09_19/derived/sensitivities.csv`, last three rows] [Decision](../decisions/2026-09-25-weekly-audit-corrections.md).
- 2026-09-20: Separated institutional residence, civil detention, criminal offenses and fiscal costs; historical counts are retained with narrower interpretation. [Decision](../decisions/2026-09-20-separate-detention-offenses-and-spending.md).

2026-09-19, later: [Matched accounts and projection checks](../decisions/2026-09-19-matched-accounts-and-projection-checks.md)
narrows completeness, horizon, uncertainty and exit-direction claims; preserves
the historical calculations and links current sensitivity tables above.
