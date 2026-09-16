[DATA] [INFERENCE] [SOURCE: https://opportunityinsights.org/wp-content/uploads/2018/10/national_percentile_outcomes.csv] [SOURCE: https://opportunityinsights.org/paper/the-opportunity-atlas/]

Model self-report: claude-opus-5[1m] (Opus 5, 1M context)

**Verdict:** The Hispanic-white male incarceration gap LARGELY does not survive equalising parental income, but it does not vanish. Pooled Hispanic/white male ratio 1.87x raw (1.80x on common support); reweighting Hispanic men to the white parental-income distribution drops it to **1.22x**, i.e. **72.6% of the raw gap is accounted for by parental income**. A residual ~0.35pp (22% excess) remains. For Black men the same reweighting explains only 42.7% (6.65x -> 4.24x).

## Headline numbers (male, share institutionalised on 2010 Census Day)

| parent pctile | white | Black | Hispanic | Asian | AIAN | hisp/white |
|---|---|---|---|---|---|---|
| p10 | 0.0449 | 0.1481 | 0.0431 | 0.0049 | 0.0810 | 0.96x |
| p25 | 0.0282 | 0.1107 | 0.0302 | 0.0093 | 0.0536 | 1.07x |
| p50 | 0.0161 | 0.0725 | 0.0190 | 0.0087 | 0.0430 | 1.18x |
| p75 | 0.0081 | 0.0406 | 0.0111 | n/a | 0.0267 | 1.36x |
| p90 | 0.0046 | 0.0335 | 0.0072 | n/a | n/a | 1.56x |
| pooled | 0.0155 | 0.1033 | 0.0290 | 0.0061 | 0.0576 | 1.87x |

**Gradient: the ratio WIDENS with parental income, the percentage-point gap does not.** Hispanic men are at parity or slightly below white men at the bottom (0.96x at p10) and 1.56x at p90. In levels the gap is a near-constant 0.19-0.29pp from p25 up, while the white rate falls 6x across the distribution. So "the gap shrinks at higher income" is false in ratio terms and roughly true in absolute terms. Black men are above whites at every percentile (3.3x at p10 rising to 7.3x at p90); AIAN men 1.8-3.3x; Asian men below whites everywhere (0.11-0.54x).

Females: rates are ~6x lower and heavily suppressed. Hispanic women are at or BELOW white women at p10-p50 (0.53x, 0.68x, 1.01x); the pooled 1.14x is a composition artifact. Asian female cells are fully suppressed.

## Decomposition (reweight each group's percentile-specific rate to the white parental-income distribution)

| group (male) | raw | ratio | reweighted | ratio | % of gap explained |
|---|---|---|---|---|---|
| Hispanic | 0.0290 | 1.80x | 0.0196 | 1.22x | 72.6% |
| Black | 0.1033 | 6.65x | 0.0659 | 4.24x | 42.7% |
| AIAN | 0.0576 | 2.60x | 0.0466 | 2.10x | 31.0% |
| Asian | 0.0061 | 0.26x | 0.0059 | 0.25x | -1.5% |

Black/AIAN/Asian rows use their own common support against white (cell counts in `oi_result.txt`), so their white reference rate differs from 0.0155.

## Comparison with the ACS 2023/2024 second-generation finding

The repo memo (`research/immigration-mexican-origin-generation-incarceration-2026-09-16.md` §2, §5, §11) finds US-born Mexican-origin men 18-39 institutionalise at 1.72x (2023) and 1.94x (2024) white rates. The OI raw Hispanic/white male ratio of 1.87x sits squarely inside that band from a completely independent design (tax-linked panel, 2010 Census institutionalisation, cohort born 1978-83, ages 27-32). That is a meaningful external replication of the RAW gap.

The OI result then adds what ACS cross-sections cannot: at equal parental income the ratio falls to about 1.22x. The "just class" rebuttal therefore has most of the explanatory weight for Hispanic men, and far less for Black men. Two cautions on transferring this to the memo's claim: (1) OI "Hispanic" pools all national origins and all generations, not US-born Mexican-origin specifically, and Mexican-origin is the higher-incarceration subset; (2) the OI comparison conditions on PARENTAL income, which is itself partly an outcome of immigrant selection, so "explained by parental income" is a descriptive decomposition, not a causal one.

## Caveats

- **Tax linkage selection.** OI links children to parents via 1989-1991 and later tax records and Census 2000/2010. Children whose parents never filed or lacked an SSN/ITIN are dropped. That disproportionately removes children of unauthorised immigrants, i.e. a chunk of the Mexican-origin population most relevant to the memo. Direction of bias is not signed here.
- **Outcome definition.** `jail_*` is the share residing in a correctional institution on 2010 Census Day (jail + prison), a point-in-time stock, not a flow of arrests or convictions. It also excludes immigration detention facilities that are not counted as correctional.
- **Cohort.** Born 1978-83, ages 27-32 in 2010 — near the peak of the male incarceration age profile, and a different policy era from the ACS 2023/2024 snapshot.
- **Suppression.** Cells below OI thresholds are blank. Asian male p75/p90, Hispanic female p75/p90 and most AIAN female cells are missing; decompositions use common support only and report cell counts.
- **No standard errors used.** The file carries `s_*` standard-error columns; ratios here are point estimates. Hispanic-white differences at individual percentiles are small in levels and may not be individually significant.
- The OI public race tables (`table_1.csv` from the Race and Economic Opportunity paper) carry jail outcomes for Black and white ONLY. The Hispanic/Asian/AIAN incarceration series lives in the Opportunity Atlas national file used here.

## Files

- `oi_incarceration_by_race_income.csv` — race x gender x {p10,p25,p50,p75,p90} jail rate, cell N, pooled rate
- `oi_result.txt` — full script output
- `oi_income.py` — analysis script (exits 0)
- `_cache/national_percentile_outcomes.csv` — raw OI download (gitignored)

## Sources

- Opportunity Atlas, Online Data Table: National by Parental Income Percentile, Race and Gender — `national_percentile_outcomes.csv`, https://opportunityinsights.org/wp-content/uploads/2018/10/national_percentile_outcomes.csv
- Chetty, Friedman, Hendren, Jones, Porter, "The Opportunity Atlas: Mapping the Childhood Roots of Social Mobility" — https://opportunityinsights.org/paper/the-opportunity-atlas/
- Chetty, Hendren, Jones, Porter, "Race and Economic Opportunity in the United States" — https://opportunityinsights.org/paper/race/ (Table 1: https://opportunityinsights.org/wp-content/uploads/2018/04/table_1.csv, Black/white jail only)
