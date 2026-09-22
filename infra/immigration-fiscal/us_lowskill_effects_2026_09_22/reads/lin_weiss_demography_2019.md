<!-- reader extraction, opus-low agent, 2026-09-22; every numeric row carries a verbatim quote re-found in the parsed corpus text with rg -F; parent spot-checked the rows cited in the memo -->
# Lin & Weiss (2019), "Immigration and the Wage Distribution in the United States", *Demography*, doi:10.1007/s13524-019-00828-9

[UNVERIFIED] — design is associational (state fixed-effects RIF regression); the one
instrument used is a robustness test only, not the headline design. All numbers below are
transcribed from the parsed text with verbatim quotes; no independent replication.

**Verdict:** An association design — unconditional quantile (RIF) regressions of native and
immigrant log hourly wages on state-level immigrant shares, 1980–2015, with state and year
fixed effects and a 1980-settlement IV only as a 2000–2015 robustness check — finding
low-skilled immigrant presence weakly negative at the bottom of the native wage distribution
and both low- and high-skilled immigrant presence strongly positive at the top; identification
is weak and the authors themselves say the coefficients "should be interpreted with caution."

## Population, period, unit

- Full-year, private-sector workers aged 25–65 in the lower 48 states earning at least $5,000
  (2016 dollars) in the previous year. Government workers and part-year workers excluded.
  "Our sample consists of full-year, private-sector workers aged 25–65 in the lower 48 states
  who earned at least $5,000 (2016 dollars) in the previous year."
- 1980, 1990, 2000 decennial census IPUMS plus ACS 2001–2015. N = 16,505,931 in the main models.
- Unit of treatment: **state × year** immigrant share of the workforce. Robustness unit:
  ConsPUMA (543 areas), 1980–2011.
- Outcome: logged hourly wage = pretax annual wage and salary earnings / annual hours, 2016 dollars.
- Skill split: low-skilled = high school or less; high-skilled = at least some college.
  Immigrant = foreign-born, any legal status.
- Coefficients are reported on the **proportion** immigrant (0–1), so a 10 percentage point
  increase = 0.1 × coefficient in log points. The authors convert this way in the text.
- Context: "Between 1980 and 2015, the immigrant shares of workforce grew from 7 % to 19 %."
  Low-skilled 4.4% → 10% of the workforce, high-skilled 2.6% → 9%.

## Design and identification

Main design: **recentered influence function (RIF, Firpo et al. 2009) unconditional quantile
regression**, individual-level, with state fixed effects, year fixed effects, individual
controls (education, age and age², race/ethnicity, part-time status, three-way sex × marital ×
parental interaction) and state controls (logged GDP per capita, % college-educated, logged
population, % metropolitan, unemployment rate, % manufacturing, union density, real minimum
wage). State-clustered robust standard errors. **No instrument in the main specification.**
The parent's belief is correct: the headline is an association design.

The authors state this plainly: "the coevolution of immigration and inequality needs to be
recognized, and any association between immigration and inequality should be interpreted with
caution. We take extensive measures to mitigate omitted variable bias, knowing humbly that our
analysis does not eliminate this issue."

Robustness tests (not the headline):
1. **ConsPUMA** geography instead of states, 1980–2011 (Fig. 3). Bottom-end negative
   association disappears; top-end positive coefficient attenuates.
2. **Instrumental variable**: 2000–2015 only, state-year immigrant density instrumented with
   the **1980 distribution of immigrants** (a settlement/shift-share style enclave instrument).
   "we restrict our samples to the observations between 2000 and 2015 and instrument immigrant" / "each state-year with the distribution of immigrants in 1980, exploiting earlier settlement as" (L813–814) **No first-stage F or first-stage strength
   is reported anywhere in the text.** The authors expect attenuation: "our estimates would be
   downwardly biased because of the extensive gap between our instrument and the period of
   analysis."
3. **GMM** using the first three lags (2000–2002) as instruments, 2003–2015; and **DID**
   (first-differenced), 2001–2015. The three estimators disagree at the bottom: "Although the
   IV and GMM estimators find no significant negative association, the DID estimator indicates
   a large negative coefficient."
4. **Excluded-state sample**: drop CA, FL, IL, MA, NJ, NY, TX, WA (48% of 2016 GDP); pattern holds (Fig. 4).
5. **Occupation model**: 316 occupations × 4 periods, within-occupation changes in immigrant
   share, controlling for change in occupation employment size as a demand proxy (Table 3).

## Headline estimates

Anchors are line numbers in the parsed file
`/Users/alien/Projects/corpus/doi_10_1007_s13524_019_00828_9/parsed.pymupdf4llm@0.3.4+cfg-99914b93/page.md`
(the parse carries no PDF page numbers); table/figure labels are the paper's own.

### Table 1 — all immigration pooled, RIF by percentile, 1980–2015 (coefficients on immigrant share 0–1)

| outcome | estimate | SE | table/anchor | verbatim quote |
|---|---|---|---|---|
| Foreign-born individual gap, 10th pct | –0.096 | 0.006 | Table 1, L619 | "Foreign-born (β1) –0.096*** –0.117*** –0.052*** 0.038*** 0.082***" |
| Foreign-born individual gap, 25th pct | –0.117 | 0.004 | Table 1, L619 | "Foreign-born (β1) –0.096*** –0.117*** –0.052*** 0.038*** 0.082***" |
| Foreign-born individual gap, 50th pct | –0.052 | 0.003 | Table 1, L619 | "Foreign-born (β1) –0.096*** –0.117*** –0.052*** 0.038*** 0.082***" |
| Foreign-born individual gap, 75th pct | +0.038 | 0.006 | Table 1, L619 | "Foreign-born (β1) –0.096*** –0.117*** –0.052*** 0.038*** 0.082***" |
| Foreign-born individual gap, 90th pct | +0.082 | 0.008 | Table 1, L619 | "Foreign-born (β1) –0.096*** –0.117*** –0.052*** 0.038*** 0.082***" |
| Immigrant share → **native** wage, 10th pct | –0.046 (n.s.) | 0.032 | Table 1, L624 | "Immigration (β2) –0.046 –0.068** 0.195*** 0.558*** 1.093***" |
| Immigrant share → native wage, 25th pct | –0.068** | 0.025 | Table 1, L624 | "Immigration (β2) –0.046 –0.068** 0.195*** 0.558*** 1.093***" |
| Immigrant share → native wage, 50th pct | +0.195*** | 0.021 | Table 1, L624 | "Immigration (β2) –0.046 –0.068** 0.195*** 0.558*** 1.093***" |
| Immigrant share → native wage, 75th pct | +0.558*** | 0.028 | Table 1, L624 | "Immigration (β2) –0.046 –0.068** 0.195*** 0.558*** 1.093***" |
| Immigrant share → native wage, 90th pct | +1.093*** | 0.035 | Table 1, L624 | "Immigration (β2) –0.046 –0.068** 0.195*** 0.558*** 1.093***" |
| Foreign-born × immigration (extra effect on immigrant wages), 10th/25th/50th/75th/90th | –0.326 / –0.263 / –0.334 / –0.574 / –0.609 | 0.035 / 0.021 / 0.018 / 0.023 / 0.033 | Table 1, L630 | "Foreign-born × –0.326*** –0.263*** –0.334*** –0.574*** –0.609***" |
| Sample size, all Table 1 models | 16,505,931 | — | Table 1, L634 | "N 16,505,931 16,505,931 16,505,931 16,505,931 16,505,931" |
| R², 10th → 90th | .092 / .175 / .233 / .236 / .173 | — | Table 1, L637 | "R [2] .092 .175 .233 .236 .173" |

Authors' own conversion to a 10-percentage-point shock (pooled immigration, natives):

| outcome | estimate | anchor | verbatim quote |
|---|---|---|---|
| Native wage, 10th pct, +10pp immigrant share | –0.46%, not significant | text, L577 | "a 0.46 % decrease in native wages at the 10th percentile (not statistically significant)" |
| Native wage, 25th pct, +10pp | –0.68% | text, L578 | "a 0.68 % decrease at the 25th percentile" |
| Native wage, median, +10pp | +2% | text, L580 | "increase in immigrant workforce is associated with a 2 % increase in native wages and a" |
| Native wage, 90th pct, +10pp | +10% | text, L581 | "10 % increase at the 90th percentile. These results support our proposition" |
| Immigrant wage extra loss, 10th pct, +10pp | –3.3% additional | text, L588 | "3.3 % decrease in wages at the 10th percentile and an additional 2.6 % decrease" |
| Immigrant wage extra loss, 25th pct, +10pp | –2.6% additional | text, L588 | "an additional 2.6 % decrease at the 25th" |

### Figure 2 — skill-split effects (the numbers the brief asks for), Eq. (2), +10pp shock

| outcome | estimate | anchor | verbatim quote |
|---|---|---|---|
| **Low-skilled** immigration → native wage, 10th–15th pct | about –2% | text, L660–662 | "The negative association is particularly salient at the 10th and the" ... "roughly a 2 % decrease in native wages." |
| Low-skilled immigration → native wage, middle and top | positive (no point value given in text) | text, L662 | "roughly a 2 % decrease in native wages. The link weakens above this point and turns" |
| Low-skilled immigration → **immigrant** wage, 10th pct | –11.5% | text, L669 | "immigrant workforce is associated with an 11.5 % decrease in immigrant wages" |
| Low-skilled immigration → immigrant wage, middle | –3% | text, L671 | "increase in low-skilled immigrant labor leads to a 3 % decrease" |
| Low-skilled immigration → highest-skilled immigrant wage | no penalty | text, L672 | "immigrants, in contrast, are not penalized by the presence of low-skilled immigrants." |
| **High-skilled** immigration → native wage, ~10th pct | +0.21 coefficient | text, L737 | "associated with some wage increase (0.21) around the 10th percentile" |
| High-skilled immigration → native wage, 90th pct | +15% per 10pp | text, L741 | "point increase in high-skilled immigrant share of workforce is linked to a 15 % increase in" |
| High-skilled immigration → native wage, 95th pct | +22% per 10pp | text, L742 | "The coefficient grows to 22 % at the 95th percentile." |
| High-skilled immigration → immigrant wage, 10th pct | +6.6% per 10pp | text, L746–747 | "At the 10th percentile, a 10 percentage point increase is associated with a" ... "6.6 % increase in immigrant wages." |

Median for the skill split is not given as a number in the text; Fig. 2 is a plot and the parse
carries no readable data from it. Reported medians above are the **pooled** Table 1 figure.

### Table 2 — state-level panel with the 1980-settlement IV, 2000–2015

The Table 2 body did not survive the PDF→markdown parse; only the in-text values exist.

| outcome | estimate | anchor | verbatim quote |
|---|---|---|---|
| All immigration → 10th pct wage (IV) | –0.029, not significant | text, L898 | "The estimates indicate that immigration in general leads to a marginal wage decline at the lower end (–0.029, nonsignificant)" |
| All immigration → 90th pct wage (IV) | +0.303 | text, L898 | "an increase at the upper end (0.303), and a larger" |
| All immigration → wage variance (IV) | +0.217 | text, L899 | "variance (0.217) of the wage distribution, all of which are consistent" |
| Low- and high-skilled immigration → 90th pct (IV) | +0.516 and +0.556 | text, L903 | "the estimates still show that both streams of migration are associated with higher wages at the top (0.516 and 0.556)" |
| Low- and high-skilled immigration → variance (IV) | +0.367 and +0.409 | text, L904 | "linked to wage dispersion (0.367 and 0.409)" |
| Low-/high-skilled effects at the bottom (IV) | both vanish | text, L901 | "adverse association of low-skilled immigration nor the positive association of high-skilled" |

No first-stage statistic, F test, or overidentification test is reported for the IV.

### Table 3 — within-occupation model, native log wage, 1990–2015

| outcome | estimate | SE | anchor | verbatim quote |
|---|---|---|---|---|
| Δ immigrant share of occupation (at skill = 0) | –1.580*** | 0.019 | Table 3, L1030 | "Δ Immigration (β1) –1.580***" |
| Δ occupation employment size (demand control) | +0.845*** | 0.039 | Table 3, L1032 | "Δ Demand (β2) 0.845***" |
| Δ immigration × occupation skill | +1.838*** | 0.036 | Table 3, L1034 | "Δ Immigration × Skill (β3) 1.838***" |
| N | 8,857,481 | — | Table 3, L1037 | "N 8,857,481" |

Interpretation given by the authors: "Immigrants compete with natives in low-skilled
occupations (–1.580) ... the interaction term shows that the adverse effect of immigrants
attenuates as the level of skill increases (1.838)." Since skill is scaled 0–1, the net
within-occupation coefficient at the top of the skill scale is about +0.258.

## What it says about

- **Native wages by skill/education.** This is the whole paper, but measured by *wage
  percentile*, not by education cell. Low-skilled immigrant presence: roughly –2% at the 10th
  and 15th percentiles per 10pp, turning positive above the lower quartile. High-skilled
  immigrant presence: +2.1% at the 10th percentile, +15% at the 90th, +22% at the 95th per
  10pp. Pooled immigration: –0.46% (n.s.) at the 10th, +2% at the median, +10% at the 90th.
  The top-end magnitudes are very large for a 10pp shock and rest on cross-state variation.
- **Native employment / crowd-out.** Only an appendix check, reported as a null on selection:
  "in section A of the online appendix, we examine the association between immigration and
  natives’ likelihood of being employed. The result indicates that the findings reported here
  are unlikely to be driven by selection into employment." No employment coefficients are in
  the main text. Native out-migration is discussed as a bias, not estimated; the ConsPUMA
  result is read as evidence of it: "the negative association between the presence of
  low-skilled immigrants and low-skilled native wages disappears, potentially a result of these
  natives migrating out of the area."
- **Housing prices, rents.** Not studied.
- **Fiscal: taxes, transfers, public services, schooling.** Not studied. The outcome is pretax
  wage and salary earnings only. The one adjacent remark is a criticism of a prior paper:
  "the aggregate-level analysis did not distinguish earned from unearned income (e.g.,
  transfers)". State minimum wage, union density and % college-educated enter only as controls.
- **Firms, production, investment, profits.** Not measured, but capital inflow is the claimed
  mechanism and is asserted from prior literature, not estimated here. The occupation-level
  interaction is offered as indirect support: "This result suggests that high-skilled
  immigration may be associated with the inflow of capital that benefits native workers."
- **Mechanism the authors claim.** Three: cross-skill complementarity (low-skilled immigrants
  supply productivity-augmenting household and personal services consumed disproportionately by
  high-wage natives, and/or are paid below marginal product so the gap is captured by natives,
  employers or customers); network-induced capital inflow following high-skilled immigrants;
  and asymmetric regulation (formal visa channels with prevailing-wage rules shield
  similarly-skilled natives from high-skilled immigrants, while weak enforcement in the informal
  channel does not shield low-skilled natives). Summary: "immigration could promote the wages of
  native workers through cross-skill complementarity, capital inflow, and selection."

## Elasticities or parameters a model could transport

Caution for the parent's production-term use: **none of these is a structural elasticity of
substitution.** They are reduced-form semi-elasticities of a wage quantile with respect to the
immigrant share of a state workforce, in an association design with state and year fixed
effects. They cannot be read as ε between natives and foreign-born within an education cell,
and they are not marginal products.

1. *Semi-elasticity of the native log hourly wage at quantile τ with respect to the immigrant
   share of the state workforce (share in 0–1), US states 1980–2015, private full-year workers
   25–65*: –0.046 (10th), –0.068 (25th), +0.195 (50th), +0.558 (75th), +1.093 (90th).
2. *Same, split by immigrant skill (Fig. 2, per 10pp)*: low-skilled immigrants about –2% at the
   10th–15th percentile, positive above; high-skilled immigrants +2.1% at the 10th, +15% at the
   90th, +22% at the 95th.
3. *Same, own-group (immigrant-on-immigrant) at the bottom*: low-skilled immigration lowers
   immigrant wages at the 10th percentile by 11.5% per 10pp — the largest effect in the paper,
   and the cleanest statement that the incidence of low-skill inflow falls on earlier immigrants
   rather than natives. This is the estimate most relevant to a Mexican-origin G1 wage question.
4. *Within-occupation semi-elasticity of native log wage to the change in the occupation's
   immigrant share, 316 occupations, 1990–2015*: –1.580 at the lowest-skill occupations,
   +1.838 interaction with occupation skill scaled 0–1, so approximately +0.26 at the top.
   This is the only estimate that holds occupation fixed.
5. *IV (1980 settlement) variance effect, 2000–2015, state panel*: +0.217 pooled, +0.367
   low-skilled, +0.409 high-skilled on the variance of the wage distribution.

## Authors' stated limitations and external-validity notes

- Endogenous location choice is not solved: "any association between immigration and inequality
  should be interpreted with caution ... our analysis does not eliminate this issue."
- Sample restrictions make bottom-end estimates conservative: "These sample restrictions imply
  that our estimates will be conservative at the bottom of wage distribution, given that the
  most disadvantaged workers are not retained in the sample." Also footnote 3: "These estimates
  are smaller than previous findings and are likely due to sample restrictions."
- The spatial approach ignores native geographic adjustment and so understates substitution:
  "the spatial approach should provide more conservative estimates ... because it does not
  consider the geographical adjustments that workers make."
- The immigrant premium at the top is compositional, not causal: "Because our models do not
  consider industry and occupation, the immigrant premium at the upper end is likely driven by
  their clustering in high-paying industries and occupations."
- The IV is deliberately weak/attenuating: "our estimates would be downwardly biased because of
  the extensive gap between our instrument and the period of analysis."
- GMM/DID may be inappropriate: "the GMM and DID estimators may not be statistically
  appropriate considering the limited variability between 2000 and 2015."
- Legal status cannot be separated: "Because of data limitations, we are unable to distinguish
  the wage consequences of
  documented and undocumented immigrants"
- External validity is explicitly institution-contingent: "the link between inequality and
  immigration is contingent on labor market institutions and can vary substantially across
  national contexts"
- Estimates from Eq. (3) and Eqs. (1)–(2) are not comparable: "the estimates in this model
  capture only within-occupation coefficients and are therefore not comparable to the estimates
  in Eqs. (1) and (2), which represent the ecological associations"

## Data availability

No replication package. Inputs are public IPUMS census/ACS extracts plus state aggregates from
BEA, BLS, the Tax Policy Center and the Department of Labor. There is an online appendix
(sections A and B) as electronic supplementary material. Full model output is by request only:
"Considering the large number of models and parameters, we present only the coefficients and
standard errors of interest. Full estimates are available upon request."

## Verification

66 quoted fragments checked against the parsed source with `rg -F` / normalized
whitespace matching; all 66 re-found, including all 40 quotes attached to numeric table rows
(Tables 1, 2, 3 and the in-text Fig. 2 conversions). Zero rows dropped.

Anchors are line numbers in the parsed markdown, not PDF pages: the pymupdf4llm parse of this
article carries no page numbers, and the Table 2 and Figure 2/3/4 bodies did not survive the
parse (Figure values are taken from the authors' own in-text readings of those figures).
