claude-opus-5-5

**Verdict:** The CPS ASEC 2025 counts **0.44M (1.6%) more US-born Mexican self-identifiers than the ACS 2024**,
once the surveys' reference dates and universes are allowed for: 28.41M against an expected 27.97M. If the ACS level
were right, the account's US-born members would be over-counted by that much. At the generations' own cost per member
on main case v5 ($8.2–12.5k), that is **about $3.6–5.5bn a year too high**. The residual is about 1.5 standard errors
of the CPS count, so the September audit's reading, "Mexican-origin natives agree once timing is allowed for", holds
roughly but not exactly. Not adopted. [CALCULATION: `native_count.py` → `derived/summary.json`]

Written 2026-10-07 02:29 JST.

## Why it was checked

The identity-enforcement lane (`g3_identity_enforcement_2026_10_06`, §8) found that the ASEC 2025 final weights give
third-plus Mexican records 5.5% more weight, relative to third-plus non-Hispanics, than the 2022–24 files did. That is
about 0.75M people on 1% more records. The account prices its US-born members at those weights; audit row 4 reweights
only the Mexico-born. The question is whether the 2025 level is out of line with the other survey.

## Result

| | Count |
|---|---|
| ACS 2024, US-born Mexican self-ID, household population | 27.293M |
| ACS 2023, same | 26.639M (growth 2.45% a year, against 1.54% for the household population) |
| CPS-to-ACS ratio of total population (universe and timing) | 1.0180 |
| Expected ASEC 2025 count at the ACS level, the group's faster growth over 0.75 years added | 27.971M |
| ASEC 2025, US-born (PRCITSHP 1–3) Mexican self-ID | 28.410M |
| **Residual** | **+0.439M (+1.57%)** |

By age the CPS-to-ACS ratio is 1.030 for children, 1.046 at 18–34, 1.060 at 35–54 and 1.038 at 55+
(`derived/by_age.csv`), against the 1.018 total-population ratio. The residual sits mostly among working-age adults.

## Reading it

- Both surveys are weighted to the Census Bureau's population estimates, the ACS 2024 to Vintage 2024 and the ASEC
  2025 to its March 2025 projection. Neither is an independent count. They differ in how the Hispanic totals are split
  by detailed origin and nativity among respondents: the CPS has more Mexican-origin people (+5.4%) and fewer Puerto
  Rican (−5.9%) and South American (−8.1%) ones than the ACS (`dataset_integrity_2026_09_23/derived/cps_vs_acs_origin.csv`).
- The ACS has the larger sample, so where the two disagree on a split its level is the better guess [INFERENCE].
- Sampling error: the self-identified total carries a replicate SE of 0.38M (ladder 158). The US-born part's SE is
  not computed here; at about 0.3M the residual is about 1.5 SE [INFERENCE].
- Dollars: the v5 generation split (`generation_account_2026_09_24/derived/generation_results_oct05.csv`, convention
  a) puts G2 at $10,568–12,506 and G3+ at $8,151–11,217 per member, so 0.44M costs $3.6–5.5bn [CALCULATION]. Working-age
  adults cost less than children, and the residual leans to adults, so the true figure is probably at the low end
  [INFERENCE].
- It does not offset the identity lane's result: no fall in identification was found. It qualifies the frame. The
  0.75M weight shift is relative to 2022–24; against the ACS only 0.44M of the 2025 level stands out.

## Gates

The CPS and ACS totals match the dataset audit's `cps_vs_acs_origin.csv` (337.69M and 331.72M); every age band's
count is positive.

## Reproduce

From the repository root:

    uv run --no-project python3 infra/immigration-fiscal/native_count_check_2026_10_07/native_count.py
