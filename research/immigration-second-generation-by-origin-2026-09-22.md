# Second generation by parental origin — adult outcomes in IPUMS-CPS ASEC 1994–2025

**Verdict:** The US-born children of Mexican immigrants close most of the first generation's
gap at the bottom of the education distribution and little of it at the top. Against third-plus
non-Hispanic whites of the same age, sex and survey year, the no-high-school gap falls from
+49.6 to +11.8 points (76% closed) while the college gap falls only from −29.8 to −20.6 points
(31% closed, bootstrap interval 29–33%). Employment closes 59% and log income 66%. Adults who
call themselves Mexican in the third-plus generation sit where the second generation sits, not
closer to the reference. Over 1994–2025 the second generation's own college rate rose 8.9
points, but the reference rose 12.0, so its college gap widened while its no-high-school gap
kept narrowing and its adjusted income gap did not move. Among the ten largest parental
birthplaces, Mexico is the only one whose second generation is still behind on college.
Descriptive, cross-sectional, and the standard errors are lower bounds.

September 22, 2026. Frame: adult outcomes of resident generations in one repeated cross-section,
compared with a fixed reference. This is the measurement FAQ 5 lacked: the fiscal ledger showed
first- and second-generation same-age gaps within $62 of each other and could not say which
inputs converge and which do not. Executed in
[`second_generation_by_origin_2026_09_22`](../infra/immigration-fiscal/second_generation_by_origin_2026_09_22/RESULT.md)
on the IPUMS-CPS extract registered today (`IPUMS_CPS_ASEC_1994_2025_2NDGEN`, 5,721,633 persons,
32 ASEC samples), the dataset the June gated-data spec named as the one that makes the
second-generation-by-origin test runnable
([spec §1](immigration-gated-data-specs-2026-06-25.md)). Confidence ladder entry 178.

## 1. What was measured

`[DATA: sources/immigration-fiscal/data/external/cps/cps_2ndgen.csv.gz, sha256 a510e7a9…, checked
before the first read]` `[CALCULATION: derived/audit.json § universe]`

Civilian adults 25–64, 2,874,753 person records from 1,696,418 households, `ASECWT` weighted.
Generation follows IPUMS `NATIVITY`: foreign-born (first), US-born with at least one foreign-born
parent (second), US-born with two US-born parents (third-plus). The first generation's origin is
its own birthplace; the second generation's is the father's birthplace when he is foreign-born
and the mother's otherwise. The reference group is third-plus non-Hispanic whites. Every gap is a
weighted least-squares contrast with age band × sex × survey-year cells absorbed, so the numbers
compare people of the same age and sex in the same year. A closing ratio is
1 − (second-generation gap ÷ first-generation gap): 1 means the second generation reached the
reference, 0 means nothing closed. Standard errors come from a 200-draw household-cluster
bootstrap and ignore the CPS PSU design and its rotation panel, so they understate sampling
error (see §6).

Three sample rules that move the numbers and were set before estimation: the 2014 ASEC ships two
full-population files (`HFLAG` 0 and 1, 313.4 million each) and only the traditional file is
kept; armed forces are dropped; `NATIVITY` 0 (unknown) is dropped
`[CALCULATION: derived/audit.json § sample_decisions]`. Five gates pass: manifest hash,
reproduction of the repo's loader table to zero difference, ASEC 2025 population totals against
`gen_ledger_extension_2026_09_16` within 5e-8, DDI code labels asserted for 17 code groups, and
a cell floor of 100 observations with finite standard errors. Thirty tests cover the estimator
against a dense dummy regression, planted gaps, composition confounding and the cluster bootstrap.

## 2. Mexico: the closing ratios

`[CALCULATION: derived/closing_ratios.csv, taxonomy region_gen_union, origin Mexico, period all]`
Gaps are in the outcome's own units (points for shares, log points for income); standard errors in
parentheses; 161,785 first-generation and 50,183 second-generation observations behind the share
rows, 131,323 and 45,246 behind log income.

| outcome | 1st-gen gap | 2nd-gen gap | closing ratio | 95% interval | raw ratio |
|---|---|---|---|---|---|
| Bachelor's or more | −0.2984 (0.0010) | −0.2060 (0.0023) | **0.310 (0.008)** | 0.293–0.326 | 0.396 |
| No high-school credential | +0.4964 (0.0015) | +0.1184 (0.0021) | **0.762 (0.004)** | 0.753–0.768 | 0.797 |
| Employed | −0.1005 (0.0013) | −0.0408 (0.0023) | **0.594 (0.023)** | 0.548–0.640 | 0.763 |
| Log total personal income | −0.5985 (0.0045) | −0.2047 (0.0079) | **0.658 (0.013)** | 0.633–0.688 | 0.730 |
| Log wage and salary income | −0.5945 (0.0034) | −0.2212 (0.0055) | 0.628 (0.009) | 0.609–0.646 | 0.690 |
| In the labor force | −0.0843 (0.0012) | −0.0287 (0.0022) | 0.659 (0.027) | 0.607–0.712 | 0.955 |
| Women in the labor force | −0.2154 (0.0019) | −0.0315 (0.0031) | 0.854 (0.015) | 0.827–0.883 | 0.968 |
| Any wage income | −0.0987 (0.0013) | −0.0297 (0.0024) | 0.699 (0.024) | 0.654–0.745 | 1.006 |
| Coresident children, women 40–49 | +0.7835 (0.0092) | +0.2407 (0.0213) | 0.693 (0.028) | 0.643–0.749 | 0.646 |

The raw ratios (no age, sex or year adjustment) differ from the adjusted ones because the Mexican
second generation is much younger than the reference; the adjusted ratio compares people of the
same age and sex in the same year and is the one to quote.

The education split is the finding. Bottom-end convergence is nearly complete: an adult born in
Mexico is 49.6 points more likely than the reference to hold no high-school credential; the
US-born child of Mexican immigrants is 11.8 points more likely. Top-end convergence is not: a
29.8-point college deficit becomes a 20.6-point deficit, and the interval 0.293–0.326 excludes
anything that could be called half closed. Labor-market outcomes sit between the two, with the
income ratio (0.66) below the participation ratios (0.85 for women's labor-force participation)
because participation converges faster than earnings conditional on working.

### 2a. The third-plus generation does not continue the movement

`[CALCULATION: derived/adjusted_gaps.csv, region_gen_union, period all]`

| outcome | 2nd gen, Mexican parent | 3rd+ Mexican self-ID | 3rd+ other (non-white or Hispanic) |
|---|---|---|---|
| Bachelor's or more | −0.2060 (0.0023) | −0.2013 (0.0018) | −0.1451 (0.0010) |
| No high-school credential | +0.1184 (0.0021) | +0.1147 (0.0017) | +0.0640 (0.0008) |
| Employed | −0.0408 (0.0023) | −0.0541 (0.0021) | −0.0924 (0.0011) |
| Log total personal income | −0.2047 (0.0079) | −0.2244 (0.0064) | −0.2035 (0.0034) |

The third-plus group is defined by who still identifies as Mexican, and ethnic attrition selects
on exactly these outcomes: Duncan and Trejo (2017) put the adults who stop identifying at +0.76
years of schooling relative to those who keep identifying, the figure the
[population-total memo](immigration-mexican-origin-population-total-2026-09-19.md) uses, and the
repo's reproduction of their design on CPS 2025 finds attrition about half their rate
([ladder 158](immigration-confidence-ladder.md)). So the third-plus row understates the
lineage's position by an amount this lane cannot measure. `[INFERENCE]` The direction is known;
the size is not. Even with that caveat, the second-to-third step is small
next to the first-to-second step on every row, which is the same shape the fiscal ledger shows
(FAQ 5: −$7,584, −$7,521, −$6,195 at common ages).

## 3. Mexico over three decades

`[CALCULATION: derived/period_trends.csv, region_gen_union, group Mexico|2nd_gen_all and
3rd+_NH_white]`

| Mexican second generation | 1994–2004 | 2005–2014 | 2015–2025 | change |
|---|---|---|---|---|
| Bachelor's or more, level | 0.124 | 0.166 | 0.213 | **+0.089 (0.005)** |
| Bachelor's or more, gap | −0.174 | −0.196 | −0.225 | **−0.052 (0.005)** |
| No high-school credential, level | 0.249 | 0.187 | 0.118 | **−0.131 (0.005)** |
| No high-school credential, gap | +0.169 | +0.135 | +0.085 | **−0.084 (0.005)** |
| Employed, gap | −0.051 | −0.033 | −0.039 | +0.012 (0.006) |
| Log total personal income, gap | −0.217 | −0.161 | −0.224 | −0.007 (0.021) |

The second generation improved on both education margins in absolute terms. Its college gap
widened anyway because the reference gained 12.0 points of college completion over the same
stretch and the second generation gained 8.9. Its no-high-school gap narrowed because the
reference had little left to shed. The adjusted income gap is flat within one standard error.
The closing ratios are stable across periods (college 0.32, 0.34, 0.31; no high school 0.71,
0.74, 0.80) `[CALCULATION: derived/closing_ratios.csv, origin Mexico, by period]`, so the ratio
is a property of the population rather than of one decade.

The first generation moved too: Mexico-born adults' no-high-school rate fell from 0.654 to 0.464
and their college rate rose from 0.049 to 0.095 across the three periods, and their naturalization
rate from 0.230 to 0.316 `[CALCULATION: derived/period_trends.csv, group Mexico|1st_foreign_born,
outcome us_citizen_g1]`. Two measured mechanisms point the same way: arrival cohorts got more
schooled ([ladder 133](immigration-confidence-ladder.md)) and the men who return to Mexico are
about a year less schooled than those who stay ([ENADID, ladder 174](immigration-confidence-ladder.md)),
which raises the resident first generation's average without any individual improving. Their
split is not measured here. `[INFERENCE]` Income levels are nominal and not comparable across
periods; only the same-year gaps are.

## 4. Other origins: the ratio mostly does not apply

`[CALCULATION: derived/adjusted_gaps.csv, region_gen_union, period all]`

| origin | college gap, 1st gen | college gap, 2nd gen | log-income gap, 1st gen | log-income gap, 2nd gen |
|---|---|---|---|---|
| Mexico | −0.298 (0.001) | −0.206 (0.002) | −0.599 (0.005) | −0.205 (0.008) |
| Central America | −0.265 (0.002) | −0.082 (0.007) | −0.494 (0.009) | −0.058 (0.019) |
| US outlying (Puerto Rico 90%) | −0.172 (0.003) | −0.169 (0.004) | −0.367 (0.011) | −0.198 (0.016) |
| Caribbean | −0.124 (0.003) | +0.028 (0.005) | −0.275 (0.009) | +0.015 (0.017) |
| South America | −0.016 (0.003) | +0.078 (0.008) | −0.279 (0.010) | +0.099 (0.023) |
| Europe | +0.106 (0.003) | +0.107 (0.002) | −0.035 (0.009) | +0.147 (0.008) |
| Africa | +0.082 (0.005) | +0.174 (0.013) | −0.189 (0.014) | +0.147 (0.038) |
| Canada | +0.167 (0.006) | +0.071 (0.006) | +0.094 (0.024) | +0.115 (0.016) |
| Asia | +0.190 (0.002) | +0.211 (0.004) | −0.105 (0.006) | +0.182 (0.013) |

Only Mexico, Central America, the US outlying areas and the Caribbean have a first-generation
college deficit for a ratio to close. Central America closes most of it (−26.5 → −8.2 points)
and nearly all of its income gap. The Caribbean and South American second generations are ahead
of the reference on both. For Asia, Europe, Africa and Canada the first generation is already
ahead on education and the second generation is ahead on income as well; their rows in
`closing_ratios.csv` divide by a surplus and are shipped as computed with that warning, and the
arithmetic fails visibly where the denominator is near zero (Canada's employment ratio is 20.7
with a bootstrap standard error of 2,290).

Among the ten largest single parental birthplaces, the second-generation college gaps are China
+0.354, Poland +0.195, Ireland +0.146, Philippines +0.103, Germany +0.077, Canada +0.071, Cuba
+0.067, Italy +0.061, England +0.053, Mexico −0.206
`[CALCULATION: derived/adjusted_gaps.csv, country_gen_union, period all]`. Mexico is the only
one behind, and by a wide margin.

The Puerto Rico case is a check on the mechanism. Adults born in the outlying areas are US
citizens by birth, arrive with no legal-status barrier and full access to mainland schooling for
their children, and their second generation still shows the same college gap as their first
(−0.172 → −0.169, closing ratio 0.018 (0.029)). `[INFERENCE]` Whatever holds the Mexican second
generation's college rate down is not only legal status.

## 5. What this does and does not say about the fiscal question

The fiscal generation ledger found the first and second generations $62 apart at common ages,
with taxes converging and the first generation's lower benefit use disappearing by the second
([FAQ 5](immigration-objections-faq-2026-09-21.md), [generation memo](immigration-mexican-origin-by-generation-2026-09-16.md)).
This lane shows the input side of that result: the second generation works and participates
nearly like the reference, earns about two thirds of the way to it, and reaches the reference at
the high-school margin but not at the college margin. Since the fiscal gap for degree holders
of most origins is small or positive and the gap for adults without degrees is the bulk of the
account ([high-education screen, ladder 168](immigration-confidence-ladder.md)), a 31% college
closing ratio is the number most consistent with a same-age fiscal gap that barely moves between
the first and second generation. `[INFERENCE]` That is a consistency reading, not a
decomposition; the fiscal ledger and this extract are different files and are not joined.

Nothing here identifies a cause. Cross-sectional generations are not lineages: the first
generation observed in 2015–2025 is not the parent generation of the second generation observed
in the same years. Origin differences carry selection into migration, arrival cohort, destination,
legal status and period along with anything transmitted in families. Education, state of residence
and legal status are deliberately not controlled, because they are the outcomes or endogenous to
the comparison. The crime side of the second-generation question is untouched; the extract has no
crime item, and the custody rule in the
[detention and crime scope memo](immigration-detention-crime-and-fiscal-scope-2026-09-20.md) governs
any such claim.

## 6. Disconfirmation and limits

- **Could the college gap be an artifact of who is counted as second generation?** The second
  generation here pools adults with two foreign-born parents and adults with one. In the loader
  table the mixed-parentage Mexican groups are not systematically better placed (mean `EDUC`
  code 79.3 with a foreign-born father only, 82.6 with a foreign-born mother only, 79.6 with
  both, 88.3 for all third-plus adults) `[CALCULATION:
  sources/immigration-fiscal/derived/lifetime/cps_second_gen_by_origin.csv, 2026-09-22 build]`,
  so the pooling is unlikely to move the college ratio far in either direction. `[INFERENCE]`
  The split is estimated in `adjusted_gaps.csv` under the `region_gen_detail` taxonomy.
- **Could ethnic attrition rescue the third-plus row?** In direction only. On the fiscal side,
  adding the estimated attriters narrowed the per-person gap from −$7,105 to −$6,864
  ([ladder 158](immigration-confidence-ladder.md)), about 3%; a correction of that order
  cannot move a −0.201 college gap near zero. `[INFERENCE from ladder 158, not computed on this
  extract]`
- **Reference choice.** The reference is third-plus non-Hispanic whites, the account's
  convention. Against all third-plus adults the Mexican gaps would be smaller, because the
  third-plus "other" group (Black, Asian, third-plus Hispanic and others) is itself behind the
  white reference (college −0.145, log income −0.204). That alternative reference is not
  estimated; the levels of every group are in `cells.csv`.
- **Standard errors** ignore the CPS PSU design and the rotation panel (about half of each March
  sample returns the next March), so they are lower bounds twice over. The closing-ratio intervals
  should be read as at least this wide.
- **Income** is nominal, conditional on positive income, and top-coded as IPUMS delivers it;
  survey-year fixed effects absorb the common price level within a year. Any-wage-income is
  reported beside it so the participation margin is visible.
- **`NCHILD`** counts coresident own children, not completed fertility.
- **The 2014 double file.** The repo's loader table double counted 2014 by weight until today;
  the fix is in `build/load_cps_second_gen.py` and moved the Mexican rows in the third decimal.
- **Only one extract.** All of this rests on one IPUMS-CPS extract with its own DDI; a replicate
  on IPUMS-USA is impossible (no parental birthplace) and the CPS is the only public file with it
  at country detail.

## 7. What would change it

A linked parent–child file (NLSY97 parent linkage, [memo](immigration-nlsy97-parent-linkage-2026-09-17.md))
or the second generation tabulated by parents' arrival cohort would turn the cross-sectional
contrast into a lineage statement. A years-of-schooling scale is not imputed here because the
DDI does not supply one. The both-foreign-parents definition is already estimated
(`adjusted_gaps.csv`, taxonomy `region_gen_detail`); an all-third-plus reference would be a
re-run of the estimator with a different reference group, and the levels it needs are in
`cells.csv`.

**Instrument note.** Tabulations are mechanical and gated; the readings marked `[INFERENCE]` are
this model's and could carry the dispositions in `notes/llm-bias-caveat.md`. The lane was built
by a separate agent from a written brief and graded here against an independent DuckDB
re-derivation of the raw Mexican closing ratios (college 0.396, no high school 0.798), which
matched.

## Sources

- IPUMS-CPS ASEC 1994–2025 extract, dataset register entry `IPUMS_CPS_ASEC_1994_2025_2NDGEN`;
  DDI codebook beside the file (`cps_2ndgen.xml`). [DATA]
- Lane: [`second_generation_by_origin_2026_09_22`](../infra/immigration-fiscal/second_generation_by_origin_2026_09_22/RESULT.md),
  outputs `derived/cells.csv`, `adjusted_gaps.csv`, `closing_ratios.csv`, `period_trends.csv`,
  `audit.json`. [CALCULATION]
- Loader: `infra/immigration-fiscal/build/load_cps_second_gen.py` (origin-code and 2014 fixes,
  2026-09-22). [CALCULATION]
- Repo context: [FAQ 5](immigration-objections-faq-2026-09-21.md),
  [Mexican-origin by generation](immigration-mexican-origin-by-generation-2026-09-16.md),
  [gated-data spec §1](immigration-gated-data-specs-2026-06-25.md), confidence ladder entries
  133, 158, 168, 174.

## Revisions

- **2026-09-22 (initial).** Written from the lane's RESULT.md after grading; the loader's 2014
  double count was fixed and the lane re-run before any number here was copied.
