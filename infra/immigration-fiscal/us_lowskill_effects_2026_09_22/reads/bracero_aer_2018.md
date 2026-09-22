<!-- reader extraction, opus-low agent, 2026-09-22; every numeric row carries a verbatim quote re-found in the parsed corpus text with rg -F; parent spot-checked the rows cited in the memo -->
[SOURCE: Clemens, Lewis & Postel 2018, "Immigration Restrictions as Active Labor Market Policy: Evidence from the Mexican Bracero Exclusion", AER 108(6), doi:10.1257/aer.20170765; parsed text at /Users/alien/Projects/corpus/doi_10_1257_aer_20170765/parsed.marker-modal@2.0.0+balanced+gemini-3-flash-preview+cfg-bba62933/page.md]

**Verdict:** A continuous-treatment difference-in-differences on the Dec-1964 removal of ~half a million Mexican bracero farm workers finds no detectable rise in domestic farm wages or employment, and the confidence intervals are tight enough to reject both the no-adjustment (0.4) and capital-adjustment-only (0.1) wage semi-elasticities the authors' own model predicts; the design is strong on exposure measurement (novel archival state-level bracero counts) and on power against the null it rejects, but it is a state-level DiD with parallel-trends identification, not an instrument.

## Population, period, unit

- Population: hired **seasonal farm workers** in the United States, split into Mexican (bracero) and domestic; domestic further split into local, intrastate and interstate workers. Not the general workforce — this is one sector.
- Treatment event: bracero program abrogation effective **December 31, 1964**, with the Kennedy-era wage-floor squeeze beginning **March 1962**. "The Kennedy administration began the process of *bracero* exclusion in March 1962, making *braceros* 'far less attractive' to farmers by greatly raising the required wage rate".
- Program scale: "It grew to supply almost half a million seasonal workers each year to US farms under typical contracts between six weeks and six months."
- Units and periods: wages are **state-quarters** (hourly index 1948–1971 full state coverage; daily-without-board 1942–1975 missing CA/OR/WA for most quarters). Employment is **state-months**, "Covers only January 1954 to July 1973, as in original sources." 46 clusters (states).
- Data are hand-collected primary archival records: "Collection of these data required in-person visits to study primary print sources at government archives around Washington, DC and at presidential archives in Abilene, Kansas and Independence, Missouri."

## Design and identification

**Not an IV.** Continuous-treatment difference-in-differences following Card (1992):

y_st = α'I_s + β'I_t + γ(I_{t≥1965} · ℓ̄_s^1955) + ε_st

- **Exposure measure**: braceros' share of the state's hired seasonal farm workforce at the program's height. "Treatment is the degree of exposure to exclusion, defined as *braceros*' fraction of seasonal agricultural labor in the state at the program's height in the mid-1950s." The regressor is "average fraction of Mexicans among the state's total hired seasonal workers across the months of 1955" — a **pre-determined 1955 share**, ten years before the event, which is what buys the exogeneity.
- Groups: high exposure is >20% bracero share in 1955 ("the six states where *braceros* made up more than 20 percent of hired seasonal farm labor in 1955"); low exposure is nonzero but <20%; no exposure is zero braceros in 1955. [UNVERIFIED] The text names the six high-exposure states as "Arkansas, Arizona, California, New Mexico, South Dakota, and Texas" while the Figure 2 note reads "High-exposure group is AZ, CA, NE, NM, SD, TX" and places AR in the low group — Arkansas vs Nebraska is inconsistent between body and figure note in this parse; do not cite the state list without checking the published figure.
- Controls: "All regressions include state and quarter-by-year fixed effects" (monthly regressions use month-by-year). Standard errors clustered by state.
- Second design, mechanism side: event study with year dummies omitting 1964 (equation 9) on a state-by-crop physical production index normalized to 100 in 1964.
- Third, non-experimental: Baltagi-Li (2002) semiparametric fixed-effects regressions of wage and of domestic employment on the bracero stock, "local linear with Epanechnikov kernel, bandwidth two log-points."
- **First stage**: no first stage in the IV sense. The "first stage" is the visible collapse of the Mexican share in high-exposure states in Figure 2 panel A, plus "*Bracero* exclusion removed tens of thousands of farm workers from the average high-exposure state."

## Headline estimates

Minus signs below reproduce the source. Model benchmarks are the authors' own predictions from equations (4) and (5).

| outcome | estimate | SE or CI | table/figure and page | verbatim quote (≤40 words) |
|---|---|---|---|---|
| Real hourly composite farm wage, DiD coef, all years | −0.0356 | SE 0.0426 | Table 1 col. 1, p. 9 (page-9 anchor) | "−0.0356<br>(0.0426)" |
| Daily wage w/o board, DiD coef, all years | −0.385 | SE 0.495 | Table 1 col. 2, p. 9 | "−0.385<br>(0.495)" |
| Real hourly wage, DiD coef, 1960–1970 | −0.0401 | SE 0.0315 | Table 1 col. 3, p. 9 | "−0.0401<br>(0.0315)" |
| Daily wage w/o board, DiD coef, 1960–1970 | −0.0247 | SE 0.309 | Table 1 col. 4, p. 9 | "−0.0247<br>(0.309)" |
| **Wage semi-elasticity ∂ln w/∂(B/L), hourly, all years** | **−0.0831** | SE 0.0654; 95% CI ≈ [−0.211, +0.045] [CALCULATION: ±1.96·SE, mine] | Table 1 col. 1 bottom, p. 9 | "Semi-elasticity $\frac{\partial \ln w}{\partial (B/L)}$ −0.0831 (0.0654)" |
| Wage semi-elasticity, daily w/o board, all years | −0.110 | SE 0.0916; CI ≈ [−0.290, +0.070] | Table 1 col. 2, p. 9 | "−0.110<br>(0.0916)" |
| **Wage semi-elasticity, hourly, 1960–1970 (tightest)** | **−0.0750** | SE 0.0507; CI ≈ [−0.174, **+0.024**] | Table 1 col. 3, p. 9 | "−0.0750<br>(0.0507)" |
| Wage semi-elasticity, daily, 1960–1970 | −0.0410 | SE 0.0541; CI ≈ [−0.147, +0.065] | Table 1 col. 4, p. 9 | "−0.0410<br>(0.0541)" |
| p-value, χ² test semi-elasticity = 0.1 (four columns) | 0.0075 / 0.0263 / 0.0012 / 0.0124 | — | Table 1 bottom row, p. 9 | "[0.0075]", "[0.0263]", "[0.0012]", "[0.0124]" |
| Domestic seasonal farm employment, linear, all years | −6,949.2 workers | SE 9,093.5 | Table 2 col. 1, p. 11 | "−6,949.2<br>(9,093.5)" |
| Domestic seasonal farm employment, ln, all years | −0.311 | SE 0.509 | Table 2 col. 2, p. 11 | "−0.311<br>(0.509)" |
| Domestic employment, linear, 1960–1970 | 1,843.0 | SE 6,859.3 | Table 2 col. 3, p. 11 | "1,843.0<br>(6,859.3)" |
| Domestic employment, ln, 1960–1970 | −0.113 | SE 0.375 | Table 2 col. 4, p. 11 | "−0.113<br>(0.375)" |
| Domestic employment, linear, exposed states only | 312.2 | SE 7,463.0, 23 clusters | Table 2 col. 5, p. 11 | "312.2<br>(7,463.0)" |
| Domestic employment, ln, exposed states only | −0.142 | SE 0.566, 23 clusters | Table 2 col. 6, p. 11 | "−0.142<br>(0.566)" |
| Local domestic workers, linear | -2,971.3 | SE 4,677.9 | Table 3, p. 11 | "-2,971.3<br>(4,677.9)" |
| Intrastate domestic workers, linear | -9,083.2 | SE 9,777.7 | Table 3, p. 11 | "-9,083.2<br>(9,777.7)" |
| Interstate domestic workers, linear | 578.7 | SE 1,127.7 | Table 3, p. 11 | "578.7<br>(1,127.7)" |
| Local / intrastate / interstate, ln | -0.472 / -0.997 / -0.574 | SE 0.738 / 0.639 / 0.458 | Table 3, p. 11 | "-0.472<br>(0.738)", "-0.997<br>(0.639)", "-0.574<br>(0.458)" |
| **Model benchmark: semi-elasticity with no adjustment** | ≈ **0.4** | — | eq. (4) text, p. 6 | "the semi-elasticity (4) would be large, approximately 0.4" |
| Implied wage rise, no adjustment, B/L = 0.3 state | ≈ **+12%** | — | p. 6 | "In a typical high-*bracero* state with $B/L = 0.3$, farm wages rise by about 12 percent after exclusion." |
| **Model benchmark: semi-elasticity, capital adjusts only** | ≈ **0.1** | — | eq. (5) text, p. 6 | "the magnitude of the semi-elasticity (5) is approximately 0.1, or one-quarter as large as without capital adjustment" |
| Implied wage rise, capital-only adjustment, B/L = 0.3 | ≈ **+3%** | — | p. 6 | "In a typical high-*bracero* state, exclusion raises farm wages by approximately 3 percent." |
| Both benchmarks rejected | 1% level (0.4 and hourly 0.1); 5% (daily 0.1) | — | Results text, p. 10 | "In all columns we reject at the 1 percent level the predicted wage semi-elasticity ... of 0.4 ... We likewise reject the predicted wage semi-elasticity of 0.1 ... at the 1 percent level for the hourly wage" |
| Replacement by unauthorized workers, test coefficient = 1 | not rejected | — | Robustness, p. 13 | "All specifications fail to reject a coefficient of unity." |
| Bracero return rate 1963–64 | >99.5% | — | Robustness, p. 13 | "Over 99.5 percent of the *braceros* who arrived in 1963 and 1964 were registered as returning to Mexico." |
| Tomato harvester productivity | ≈ 2× per worker | — | Mechanisms, p. 14 (Harper 1967, p. 12) | "machines that roughly doubled harvest productivity per worker (Harper 1967, p. 12), but adoption was low for the first several years" |
| Crops without a mechanization option: production declines | 5 of 6 crops, large and lasting | — | Figure 6 discussion, p. 15 | "we observe large and lasting relative declines in production in and after 1965 in five" |

**What magnitude of wage rise the CI excludes.** [CALCULATION: mine, ±1.96·SE on the reported semi-elasticities] The upper 95% bound on ∂ln w/∂(B/L) is +0.045 (hourly, all years), +0.024 (hourly, 1960–70), +0.070 (daily, all years) and +0.065 (daily, 1960–70). Applied to a high-exposure state with B/L = 0.3, the tightest column excludes any farm-wage rise above roughly **0.7%**, and the loosest excludes anything above roughly **2.1%**. The authors' 12% (no adjustment) and 3% (capital only) predictions both sit outside; their own χ² tests state the 0.1 benchmark is rejected at 1% (hourly) and 5% (daily), and 0.4 at 1% everywhere.

## What it says about

- **Native wages by skill/education.** Only one cell is studied: hired seasonal farm labor, overwhelmingly low-skill, measured as a state-level wage index, not by worker education. Zero effect, and the CI excludes a rise above ~2%. No skill or education gradient is estimated. The paper notes the design also covers the non-Mexican subgroup and that specialization would further weaken any effect: "below we consider the outcomes for non-Mexicans, and any Mexican-non-Mexican specialization in employment would further mitigate the wage impacts on that group."
- **Native employment / crowd-out.** No crowd-in of domestic workers. Descriptively: "The gap between high- and low-exposure states is approximately constant before and after exclusion", and the high-vs-no-exposure gap narrows during the program then stays flat, "the opposite of what would be expected if *bracero* exclusion had crowded more domestic labor into farm work." Broken out, none of local, intrastate or interstate workers respond, and: "This indicates that domestic seasonal workers did not move within or between states in substantial numbers to dissipate state-specific shocks to the *bracero* labor supply." That last point matters for spatial designs generally: the state unit is not being contaminated by internal migration here.
- **Housing prices, rents.** Not studied.
- **Fiscal: taxes, transfers, public services, schooling.** Not studied. The paper contains no fiscal accounting of any kind. Braceros were temporary contract workers who returned ("Over 99.5 percent ... registered as returning to Mexico"), so nothing here speaks to a settled-population fiscal ledger.
- **Firms, production, investment, profits.** Studied indirectly and this is the paper's most transportable content. Capital-labor substitution and technology adoption are the adjustment margin. In California tomatoes: "*bracero* exclusion was followed immediately by a dramatic adoption of this existing technology, as predicted by equation (7)", with "No such shift occurred in Ohio", which had essentially no braceros. Analogous suggestive evidence for cotton harvesting and sugar-beet field preparation is in the online appendix. For crops with no mechanized option — "asparagus, strawberries, lettuce, celery, cucumbers, citrus, and melons" — output falls: five of six show "large and lasting relative declines in production in and after 1965". Tomato and cotton show "modest, short-lived relative declines"; sugar beets, with greater adoption frictions, decline more and longer. No profit, investment-value or firm-entry estimates.
- **Mechanism the authors claim.** Endogenous technical advance plus crop switching inside a diversification cone. Where a less labor-intensive technology coexists with the traditional one, removing labor shifts output share toward the advanced technology without changing the marginal product of labor, so the wage is pinned at ŵ. Where no such technology exists, wages can rise but only to the shutdown margin, beyond which land switches to another crop, fallow or non-farm use. The authors' summary: "Employers appear to have instead adjusted to foreign-worker exclusion by changing production techniques where that was possible, and changing production levels where it was not."
- **Reverse causation check on the mechanism.** Lobbying-driven timing is ruled out with Alston-Ferrie congressional voting data: "The sharp 1963 decline in political support for the program occurred only among representatives of states that did *not* rely on the program."

## Elasticities or parameters a model could transport

1. **Semi-elasticity of the farm wage with respect to the bracero share of the workforce, ∂ln w/∂(B/L), US state level, hired seasonal farm labor, 1948–1971.** Estimated at **−0.083 (SE 0.065)** all-years hourly and **−0.075 (SE 0.051)** for 1960–70. Population: hired seasonal farm workers in 46 US states. This is the paper's headline structural object and it is a **zero with a tight upper bound**, not a positive elasticity. Transporting it means transporting a null.
2. **The same semi-elasticity for domestic seasonal farm employment**, in logs: **−0.311 (SE 0.509)** all years, **−0.142 (SE 0.566)** exposed states only. Also a null; the SEs are wide, so this bounds crowd-in much less tightly than the wage result does.
3. **Calibration inputs the authors borrow, not estimate** (Herrendorf, Herrington & Valentinyi 2015, postwar US agriculture): "with $\mu, \sigma \equiv 1.6$, $s_K \equiv 0.54$, $s_T \equiv 0.07$, and $s_L \equiv 0.39$". Here μ is the substitution elasticity between capital and the labor-land aggregate, σ between labor and land, and the s are income shares. These feed the 0.4 and 0.1 benchmarks. **Caution for a nested-CES production term:** these are agriculture-specific shares with capital at 54%, not economy-wide, and the authors flag the nesting is not theirs — "They specify the production function differently, imposing that capital and land are in the same nest."
4. **Labor-demand elasticity benchmark, cited not estimated:** "a meta-analysis by Espey and Thilmany (2000) finds that the median wage elasticity of labor demand for hired farm workers across all published studies is $-0.5$".
5. **No elasticity of substitution between natives and foreign-born within an education cell is estimated anywhere in this paper.** The model's two labor types are not native vs immigrant — labor is homogeneous (L = B + N) and the substitution that matters is labor vs capital vs land across two technologies. A parent model needing ε(native, foreign-born) cannot source it here. What this paper does supply is a reason to think a one-technology CES **overstates** the native wage gain from removing immigrant labor, because it holds the technology mix fixed.

## Authors' stated limitations and external-validity notes

- **Pre-trends.** Acknowledged and partly real: "Recasting the regressions as a year-by-year event study reveals no significant pre-trends in wages. In employment there are significant pre-trends, but not when the sample is restricted to states with nonzero exposure to the program."
- **Unauthorized replacement.** Tested, but the test is weak and the authors say so: "These estimates should be considered only suggestive because the original sources omit 'total hired farm workers' counts for 11 of the 46 states." The supporting evidence is the >99.5% registered return rate and the absence of a post-1964 rise in border apprehensions with enforcement effort held constant.
- **SUTVA.** Explicitly raised — a credible threat to import braceros from another state could hold wages down in never-treated states. Answer is indirect: the result survives dropping zero-bracero states.
- **Coverage gaps.** Daily wage missing for CA, OR, WA in most post-1949 quarters; farm-worker stocks missing for Rhode Island and New Hampshire in 1955; "If no workers reported for state-month in month when source report was issued, assume zero."
- **Mechanism evidence is suggestive, not identified.** The mechanization series exists for only two states: Figure 5 is "the two states with mechanization time series", and the conclusion says "This mechanism requires further elucidation."
- **Scope.** One sector (agriculture), one era (1960s), one worker type (temporary seasonal contract labor with near-universal return). The result is about a *technologically adjustable* sector; the authors' own model implies wages would rise where no advanced technology exists and land cannot switch use.
- Measurement error in the novel archival series is discussed in the online appendix, which is not in this parsed text: "The online Appendix details the sources and discusses the potential for measurement error."

## Data availability

- **Replication package: yes, AEA/openICPSR, cited as a dataset by the authors.** "Clemens, Michael A., Ethan G. Lewis, and Hannah M. Postel. 2018. 'Immigration Restrictions as Active Labor Market Policy: Evidence from the Mexican *Bracero* Exclusion: Dataset.' *American Economic Review*. https://doi.org/10.1257/aer.20170765." The paper also points to the article page for additional materials: "Go to https://doi.org/10.1257/aer.20170765 to visit the article page for additional materials and author disclosure statements."
- No restricted-access data. All inputs are government publications and archival print sources, hand-entered by the authors.
- **[BLOCKED-AS-SPECIFIED] The path the brief named does not exist on this machine.** There is no `harvard-dataverse/bracero-aer-2018` anywhere under `/Users/alien` (searched `find /Users/alien -maxdepth 8 -iname "*bracero*"` and `-type d -iname "harvard-dataverse"`, plus `/Volumes`). What is on disk is a **Julia re-implementation mirror**, not the AEA Stata package, at:
  `/Users/alien/Projects/immigration-research/infra/immigration-fiscal/frontier_execution_2026_09_17/policy/raw/bracero-mirror/`
  containing `README.md`, `cleaning.jl`, `data.csv`, `cpi.csv`, `table1.jl`, `table2.jl`. Sibling artifacts in the same `raw/` directory: `bracero-working-paper.pdf`, `bracero-appendix.txt`, `bracero-aea.html`, `bracero-material-9090` (empty directory), and several GitHub-search JSON files. A prior replication script exists at
  `/Users/alien/Projects/immigration-research/infra/immigration-fiscal/frontier_execution_2026_09_17/policy/replicate_bracero_danzer.py`
  with output at `.../policy/derived/bracero_raw_mirror_results.csv`. I did not run anything. [UNVERIFIED] Whether that Julia mirror reproduces the published tables — I did not open or execute it.

## Verification

**46 of 46** numeric and quoted fragments re-found with `rg -F` against the parsed page. Every row in the Headline table carries a fragment that returned exactly one hit (`average fraction of Mexicans among the state` and `Standard errors clustered by state in parentheses` return 2 hits, both in the intended table notes). Note for future readers: Table 3's figures use an ASCII hyphen while Tables 1–2 use U+2212, so `rg -F -- "-0.472"` needs the `--` separator or rg reads it as a flag. Zero rows were dropped.

Derived numbers are tagged [CALCULATION] and are mine, not the paper's: the ±1.96·SE confidence intervals on the four semi-elasticities and the implied maximum wage rise at B/L = 0.3.
