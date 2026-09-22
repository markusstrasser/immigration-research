# Elderly public medical spending by ethnicity: MCBS 2023 check on the 65+ transport

Date: 2026-09-22. [DATA / CALCULATION; FRAMING-SENSITIVE in the ledger translation]
Calculation record; narrative authorship remains operator-owned.

**Verdict:** Among community-dwelling Medicare beneficiaries aged 65+, public medical
payments per beneficiary are **1.27× higher for Hispanic than for non-Hispanic white
beneficiaries** (SE 0.15, 95% CI 0.97–1.56), a gap of **+$3,276 a year** (SE $1,806) that
does not clear 95% significance. All-source spending is the same (ratio 0.99): the
difference is who pays. Medicaid pays 9× more per Hispanic beneficiary and 36% of them have
a Medicaid payment against 5% of whites, while out-of-pocket and private insurance pay
0.3–0.4× as much. Income reverses the sign: 1.54 (CI 1.02–2.05) below $25,000 of household
income, 0.70 (CI 0.48–0.92) at or above, and 51% of Hispanic 65+ beneficiaries sit below
that line against 14% of whites. The ledger's public medical transport carries age and US
birth and nothing else, so for the union's 65+ cell (−$43.6bn) this file bounds the missing
ethnicity dimension at **−3% to +56%: up to about $24bn more cost, and no reduction** [the
"no reduction" clause is WITHDRAWN 2026-09-22 (later): the Mexican-origin check on the transport's own
MEPS file gives 0.89 (CI 0.61–1.18) at 65+, see Revisions]; the point ratio implies $11.6bn more. Hispanic is not Mexican-origin, institutional care is
outside the file, and the Medicare Advantage accounting makes the public figure a lower
bound.
[CALCULATION: [`mcbs_elderly_medical_2026_09_22`](../infra/immigration-fiscal/mcbs_elderly_medical_2026_09_22/RESULT.md)]

## 1. What was computed

The 2023 MCBS Cost Supplement public-use file (6,920 beneficiaries, 134 columns, acquired
and hash-pinned on September 20) carries payments by payer for every beneficiary living in
the community for the whole year, with a four-category race/Hispanic classifier, three age
groups, two income groups and 100 replicate weights. The lane takes beneficiaries aged 65+
(632 Hispanic, 4,454 non-Hispanic white, unweighted) and computes weighted mean payments per
beneficiary by payer, the Hispanic-to-white ratio formed inside every replicate, and Fay
balanced-repeated-replication standard errors with the documented adjustment of 0.3. Before
any spending figure is read, the weighted counts by age group and ethnicity must reproduce
the published Exhibit 3.3 of the file's summary of changes; all eighteen cells reproduce to
the dollar and the build fails otherwise. No published cost figure exists in the acquired
documents, so the spending estimates are unanchored and say so.
[DATA: `fiscal_access_2026_09_20/_cache/CSPUF2023_Data.zip`, user's guide §7.1 p.15 and
Appendix B; CALCULATION: `mcbs_elderly.py`, `derived/anchor_reproduction.csv`]

## 2. Payments per beneficiary at 65+, 2023 dollars

| Payer | Hispanic | SE | NH white | SE | Ratio | 95% CI |
|---|---:|---:|---:|---:|---:|---|
| Public (Medicare + Medicare Advantage + Medicaid) | 15,638 | 1,694 | 12,362 | 593 | 1.27 | 0.97–1.56 |
| Medicare | 8,716 | 1,197 | 7,898 | 419 | 1.10 | 0.78–1.43 |
| Medicare Advantage plan payments | 4,542 | 533 | 4,204 | 367 | 1.08 | 0.77–1.40 |
| Medicaid | 2,379 | 572 | 260 | 48 | 9.16 | 2.83–15.48 |
| Out of pocket | 1,263 | 128 | 3,012 | 80 | 0.42 | 0.33–0.51 |
| Private insurance | 463 | 134 | 1,443 | 82 | 0.32 | 0.14–0.51 |
| Total, all sources | 17,805 | 1,634 | 17,918 | 691 | 0.99 | 0.80–1.19 |
| Share with any Medicaid payment | 0.358 | 0.025 | 0.051 | 0.004 | 7.02 | 5.61–8.44 |
| Share with any Medicare Advantage payment | 0.628 | 0.025 | 0.427 | 0.009 | 1.47 | 1.34–1.60 |

[DATA: `derived/ratios.csv`, `derived/elderly_cost_by_race.csv`]

By age band the story does not change (65–74: 1.33, CI 0.87–1.78; 75+: 1.22, CI 0.93–1.51).
By income it reverses:

| Domain | Hispanic public | NH white public | Ratio | 95% CI |
|---|---:|---:|---:|---|
| 65+, household income under $25,000 | 22,458 | 14,604 | 1.54 | 1.02–2.05 |
| 65+, household income $25,000 or more | 8,450 | 12,008 | 0.70 | 0.48–0.92 |

Total all-source payments show the same reversal (1.31 and 0.67), so higher-income Hispanic
beneficiaries in this file use less care in dollars, not merely less public money. The
pooled 1.27 is the weighted mix of the two strata. [DATA: `derived/ratios.csv`]

## 3. What it bounds in the ledger

[FRAMING-SENSITIVE] The ledger assigns public medical cost to each CPS record from MEPS
donors matched on age and US birth. Ethnicity, income and Medicaid status do not enter the
match. For the Mexican-origin union the 65+ public medical charge, including the NHEA
coverage scaling (item M), is −$43.6bn of the −$128.0bn medical total under the shared
allocation [DATA: `ledger_absolute_2026_09_17/derived/age_profile_components.csv`, bands 6
and 7, components `medical` and `M`].

If the union's elderly resemble Hispanic MCBS beneficiaries and the MEPS donors at their
ages resemble the white ones, the pooled interval translates to a 65+ cell of −$42bn to
−$68bn against the −$43.6bn assigned: up to about **$24bn more cost, none less**, point
−$55bn. Two things pull the true adjustment toward the low end and one toward the high
end. Foreign-born MEPS donors are themselves partly Hispanic, so the transport already
carries part of the difference for the Mexico-born; and the union's 65+ are income-mixed,
so the income-conditional ratios (1.54 and 0.70) rather than the pooled one apply cell by
cell. Against that, Medicare Advantage plan payments understate government capitation, and
Hispanic beneficiaries are 47% likelier to be in such plans, so the public figure is a
lower bound on outlay. The re-aged and lifetime figures, which move about $80bn through
public medical when the union is given the white age structure, inherit the same bound on
their 65+ cells. [INFERENCE]

## 4. Limits

- Community-dwelling, full-year beneficiaries only; anyone with a facility interview or
  facility, hospice or institutional event is excluded, so institutional Medicaid, the
  largest 65+ Medicaid outlay, is absent. The ledger prices institutions separately (item
  N) and nothing here bounds that item.
- Hispanic pools every origin; no country of birth, nativity, generation or status on the
  file. Mexican-origin beneficiaries are a subset with their own income and coverage mix.
- One calendar year, top-coded at the 99.5th percentile, 632 Hispanic observations at 65+
  and a few hundred per income stratum. Standard errors are Fay BRR estimates from the
  supplied replicates; the variance equation is the standard definition of the documented
  software options, not an equation printed in the guide.
- Dual eligibility is proxied by any Medicaid payment, which misses partial-benefit duals.

## 5. Sources

[DATA: 2023 MCBS Cost Supplement PUF, codebook, user's guide and summary of changes,
acquired and pinned in `infra/immigration-fiscal/fiscal_access_2026_09_20/` (RESULT.md,
manifest.json, derived/mcbs_validation.json)] [CALCULATION:
`infra/immigration-fiscal/mcbs_elderly_medical_2026_09_22/mcbs_elderly.py`, gates in
`derived/audit.json`, `test_mcbs_elderly.py` (28 tests)]

## Revisions

- 2026-09-22: created. Ladder 173. No ledger value changes.
- 2026-09-22, later: the [Mexican-origin check on the transport's own MEPS file](immigration-mexican-origin-medical-transport-check-2026-09-22.md)
  runs the other way at 65+ (Mexican-origin/all-donor public spending 0.89, CI 0.61–1.18;
  2023–24 pooled 0.81, SE 0.09). Taken together the two files leave the sign of the missing
  ethnicity dimension open, about −40% to +56% on the 65+ cell; the "no reduction" clause in
  the verdict above is withdrawn. The mechanism both files agree on stands: far more Medicaid,
  far less out-of-pocket and private payment, equal or lower total spending. Ladder 175.
