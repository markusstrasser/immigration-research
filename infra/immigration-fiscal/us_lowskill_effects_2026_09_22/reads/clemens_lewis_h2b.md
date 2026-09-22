<!-- reader extraction, opus-low agent, 2026-09-22; every numeric row carries a verbatim quote re-found in the parsed corpus text with rg -F; parent spot-checked the rows cited in the memo -->
[SOURCE: /Users/alien/Projects/corpus/doi_10_3386_w30589/parsed.pymupdf4llm@0.3.4+cfg-99914b93/page.md — Clemens & Lewis, NBER WP 30589, Oct 2022, revised May 2024]

**Verdict:** A pre-registered survey of 472 US firms that entered the randomized H-2B visa lotteries of January 2021 and January 2022 finds that exogenous access to low-skill foreign seasonal workers raises firm revenue, investment and the profit rate and does not reduce US employment; the randomization is genuine and the design is strong, but everything is measured at the firm level in a narrow set of seasonal nonfarm occupations, and the headline substitution elasticity is backed out of a model, not directly estimated.

## Population, period, unit

Unit of observation is the **firm**. Universe is US employers that entered the Department of Labor lottery allocating H-2B (low-skill, nonfarm, seasonal) labour certifications for the second half of fiscal years 2021 and 2022 (April–September of each year). Core pooled sample **472 firms** (251 from the 2021 survey, 221 from 2022), recruited through four industry associations plus, in 2022, two labour recruiters.

> "The pooled 2021 and 2022 core sample is thus 472 firms, that is, 251 from 2021 and 221 from 2002."

Sector mix (share of H-2B workers, sample vs universe): landscaping 46.2% vs 39.5%, forestry 15.5% vs 8.9%, seafood processing 10.2% vs 8.9%, hospitality 7.0% vs 9.1%, carnivals 5.0% vs 2.2%, golf/country clubs 3.8% vs 9.8%, construction 3.0% vs 8.2%, restaurants 0.5% vs 2.5%, other 8.8% vs 10.9%.

> "Landscaping 187,016 0 _._ 395 5,874 0 _._ 462"

26–34% of firms/workers are rural. Mean firm revenue $8.7m; mean 22.6 foreign temporary workers, 31.9 US temporary workers, 50.2 US permanent workers.

**Definition of "US worker":** self-reported by the firm, and the survey told respondents it covers citizens and green-card holders. It therefore *includes* settled immigrants and excludes only non-immigrant visa holders and the unauthorized.

> "were told that “U.S. worker” includes both citizens and lawful permanent residents. The sur"

Two distinct US-worker outcomes: **US temporary workers** (the primary employment outcome, the direct co-workers of H-2B hires) and **US year-round workers** (secondary, "generally higher-skill").

## Design and identification

Randomized federal lottery over H-2B certification petitions. Two pre-specified instruments: a dichotomous "lottery win" (receiving letter 'A' on petitions covering at least 50% of workers requested) and a continuous "expected share" (expected certification share given the firm's letter draw). Outcomes come from a novel online survey; the pre-analysis plan was registered at osf.io/zdyun on the morning the survey went out.

First stage is strong. Winning raises foreign employment by 86%, semielasticity 0.618 (SE 0.112 in Appendix Table A4); losing cuts foreign employment by 46%.

> "causes firms to employ 86 percent more foreign workers as lottery-losing firms, corresponding to"
> "a first-stage semielasticity"

All 2SLS specifications are just-identified and each reports an Anderson-Rubin p-value robust to weak instruments. Controls: baseline (pre-lottery year) revenue, US year-round workers, US temporary workers, foreign temporary workers, plus a year dummy. Revenue in logs; employment and investment in inverse hyperbolic sine, with a PPML robustness check. Randomization inference (Heß 2017) reported in the appendix. A partial replication on the 2020 lottery gives similar magnitudes in a much slacker labour market.

## Headline estimates

All 2SLS elasticities are with respect to foreign (H-2B) employment, instrumented by the lottery, with full baseline controls. Sample 472 firms unless noted.

| Outcome | Estimate | SE / CI / p | Table, col., page | Verbatim quote |
|---|---|---|---|---|
| First stage: foreign employed (IHS) on lottery win | 0.618 | SE 0.112 | App. Table A4, p. A-10 | "a first-stage semielasticity" |
| First stage, % effect | +86% foreign workers (losing: −46%) | — | §6, p. 27 | "causes firms to employ 86 percent more foreign workers as lottery-losing firms, corresponding to" |
| Revenue (ln), 2SLS lottery-win | 0.218 | SE 0.080; AR p=0.008 | Table 2 col. 6, p. 29 | "0.218, among firms whose foreign employment was altered" |
| Revenue (ln), 2SLS expected-share | 0.198 (text: 0.20) | SE 0.069; AR p=0.004 | Table 2 col. 10, p. 29 | "0.20 in column 10, compared to the estimate of 0.22" |
| Revenue, reduced form (lottery win) | 0.135 (+13.2% revenue) | SE 0.051 | Table 2 col. 4, p. 28 | "raise it with elasticity" (context: "Winning the lottery causes firm revenue to grow by 13.2%") |
| US temporary employment, reduced form | 0.116, not significant | SE 0.095 | Table 3 col. 4, p. 30 | "the lottery is 0.116, an estimate that is not statistically" |
| US temporary employment, 2SLS lottery-win | 0.188, cannot reject zero | SE 0.149; AR p=0.219 | Table 3 col. 6, p. 30 | "temporary employment is 0.188, though again we cannot reject" |
| US temporary employment, 2SLS expected-share | 0.061 | SE 0.125; AR p=0.630 | Table 3 col. 10, p. 31 | "the causal elasticity of U.S. temporary employment to foreign" |
| US employment, overall summary range | +0.06 to +0.19, imprecise | — | §9 Conclusion, p. 54 | "elasticity +0.06–0.19, statistically imprecise" |
| US employment, rural subsample | +0.61 | AR p = 0.05 | Fig. 7b / §9, p. 54 | "positive effect of foreign worker employment on native employment (elasticity +0.61, Anderson" |
| Investment (IHS), 2SLS lottery-win | 2.072 | SE 0.721; AR p=0.001 | Table 4 col. 6, p. 34 (N=456) | "foreign employment causes greater investment with an elasticity of 2.072" |
| Investment (IHS), 2SLS expected-share | 1.466 | SE 0.610; AR p=0.012 | Table 4 col. 10, p. 34 (N=456) | "yields a causal elasticity of 1.466" |
| Change in profit rate, 2SLS | 0.15 (0.152 / 0.151) | SE 0.075 / 0.067; AR p=0.024–0.047 | Table 5 cols. 6 and 10, p. 35 (N=441) | "growth in the profit rate, with a causal elasticity of 0.15 (Anderson-Rubin _𝑝_ value 0.024–0.047)." |
| US temporary employment, PPML (no IHS), lottery win | 0.292 | p=0.122 | Table 6 col. 1, p. 39 | "is 0.292, with a" |
| US temporary employment, PPML, expected share | 1.157 | p=0.043 | Table 6 col. 2, p. 39 | "the coefficient estimate is 1.157 with a" |
| US **year-round** employment, 2SLS | 0.07–0.09, indistinguishable from zero | — | App. Table A8 / §A13, p. A-13 | "employment (elasticity 0.07–0.09) is statistically indistinguishable from zero" |
| Foreign-native effective elasticity of substitution σ (preferred) | 1.26 | 95% CI (0.12, 2.39) | Table 7 centre, §8.4 p. 48 | "with a 95% confidence interval (0.12, 2.39)" |
| σ, range across all parameter assumptions | 0.8–2.2 | max upper CI bound 3.37 | Table 7, §8.4 pp. 48–49 | "never fall outside the range 0.8–2.2" |
| σ, authors' rounded headline | ≈ 1.3 | — | §8.4, p. 49 | "Our preferred estimate of" (full: "Our preferred estimate of _𝜎_ ≈ 1 _._ 3 is somewhat lower than prior…") |
| Black-market substitution fraction φ | ≈ 0.009, imprecise | not statistically precise | eq. (17), §8.6 p. 52 | "Solving for the unobserved black-market fraction" |
| Randomization-inference p-values (lottery win) | revenue 0.005, US temp 0.235, investment 0.003 | — | App. Table A6, p. A-20 | "Lottery win 0.6176 0.1347 0.1160 1.3251" |

Implied dollar effect on profits: a doubling of foreign employment raises dollar profits about 40%, combining the 15.2% rise in the profit rate with the 21.8% rise in revenue.

## What it says about

- **Native wages by skill/education — not studied.** No wage outcome is measured. The H-2B wage itself is administratively fixed at the DOL prevailing wage, so the design holds immigrant wages constant by construction. Native wage markdowns appear only as a theoretical mechanism behind the rural heterogeneity.
- **Native employment / crowd-out — the central result.** No crowd-out anywhere. Firm-level elasticity of US temporary employment to foreign employment is +0.06 to +0.19 and statistically imprecise overall; +0.61 and significant at AR p=0.05 in the pre-registered rural subsample; the US employment effect is 7.9 times larger in rural than urban areas. US year-round (higher-skill) employment is +0.07 to +0.09, indistinguishable from zero. No pre-registered subgroup shows a sign flip.
- **Housing prices, rents — not studied.**
- **Fiscal: taxes, transfers, public services, schooling — not studied.** H-2B workers are temporary and non-immigrant; the paper makes no fiscal claim whatsoever.
- **Firms, production, investment, profits — the core outcomes.** Revenue elasticity 0.20–0.22, investment elasticity 1.5–2.1, profit-rate elasticity 0.15. Effects are larger for small firms, for firms facing more competition, and for rural firms. The authors argue the aggregate effect is probably not smaller than the firm-level effect: the lottery does not change firms' reported competitive environment, the 2020 replication (where losers vastly outnumbered winners, so there was more business to steal) gives similar magnitudes, and the revenue effect is smaller in urban areas where reallocation should be easiest.
- **Mechanism the authors claim.** Legally authorized low-skill foreign workers have few substitutes at the marginal firm. Natives substitute poorly (σ ≈ 1.3); capital is a complement, not a substitute, so shortages cannot be automated away; and the forensic test finds no shift into black-market labour. Restricting the visa therefore forces the firm to contract rather than to re-source labour.

## Elasticities or parameters a model could transport

1. **Firm-level foreign–native "effective" elasticity of substitution σ within the low-skill labour nest, at H-2B lottery-entrant firms: 1.26, 95% CI (0.12, 2.39); range 0.8–2.2 across parameter assumptions.** This is the "about 1.3" the parent's removal model is citing. It is *not* directly estimated. It is obtained by solving the paper's equation (7) for σ using the **US-employment** 2SLS coefficient in **Table 3, column 10** (the expected-share instrument with full controls, point estimate 0.061, SE 0.125, which is itself not significantly different from zero). The wide CI is inherited from that imprecise coefficient.

   Auxiliary parameters plugged in: output demand elasticity η ≈ 8 (from De Loecker et al. markups of 1.12–1.16 in low-skill services, implying η = 7.3–9.3); capital elasticity of output β ≈ 0.35 (capital share 0.292–0.310 in landscaping and hospitality); high-skill labour elasticity γ ≈ 0.35; native share of the inner low-skill nest 1 − α = 0.668 (SE 0.012, N=470); share of year-round native employees in total employment 0.421 (SE 0.013, N=470). Note the parsed text's derivation of γ prints "0.470 − …= 0.313", which does not reconcile cleanly with the stated 0.421 or with the preferred γ ≈ 0.35 — treat the exact γ arithmetic as unresolved from this parse.

   > "share of native workers in the inner (low-skill) labor nest in the survey"

2. **Scope warning for transport.** This σ is (a) measured at the **firm** level, so it *excludes* Hicksian "community level" / Rybczynski between-firm demand substitution that aggregate education-cell estimates include; (b) an **effective** elasticity that *includes* institutional imperfections such as monopsony, not a purely technical σ; and (c) estimated on low-skill **seasonal nonfarm** jobs (landscaping, forestry, seafood, hospitality) among firms at the visa-quota margin. The authors themselves position it against aggregate estimates of about 4 (Cortés 2008) and 4–10 (Peri–Sparber, Peri, Ottaviano et al.), and they reject those values for their setting because the highest upper CI bound in Table 7 is 3.37.

   > "the highest upper bound on any 95% confidence interval implied by Table 7 is 3.37"

   A nested-CES fiscal model that uses ε between natives and foreign-born *within an education cell for the whole resident population* is not the same object. Using 1.3 there imports a firm-level, seasonal, H-2B-margin parameter into an economy-wide cell. The transport is defensible only as a low-substitutability bound, and the underlying CI (0.12, 2.39) means the paper cannot pin ε anywhere near tightly enough to drive a headline number on its own.

3. **Other transportable objects:** revenue elasticity to low-skill immigrant labour 0.20–0.22; investment elasticity 1.5–2.1; profit-rate elasticity 0.15; output demand elasticity η ≈ 8 for low-skill service industries; capital share 0.24–0.45 across H-2B industries; unauthorized-for-authorized substitution fraction φ ≈ 0.009 (imprecise).

## Authors' stated limitations and external-validity notes

- **Firm level ≠ aggregate.** "The firm-level analysis in Section 6 need not imply aggregate effects of equal magnitude." Lottery winners may take market share from losers. Three non-pre-registered tests argue against pure reallocation, but the authors concede "some potential for our estimates overstate the aggregate impact."
- **Short run only.** Effects are measured within the same half-year as the hiring change; the year-round employment null is explicitly attributed in part to this.
- **A one-shot lottery is not a quota change.** A permanent quota increase would reduce uncertainty and probably produce *larger* investment and year-round hiring responses.
- **The IHS transformation** is flagged as needing care (Chen and Roth 2024), hence the PPML robustness table.
- **Pre-analysis plan deviation.** The plan specified 2021 data only; 2022 was added with an identical instrument to gain precision, and the authors defend this explicitly.
- **Non-response and sample construction.** 14.6% of 2021 forms dropped as too incomplete, plus smaller drops for zero-petition and duplicate responses. Firms declining to give a postal code cannot enter the rural/urban tests; Appendix Table A7 shows no significant difference for that group.
- **Labour-market tightness.** 2021–22 was exceptionally tight (unemployment 5.5%, job openings nearly doubled). The 2020 partial replication (unemployment 10.9%) gives similar magnitudes, which the authors read as evidence the results do not depend on tightness.
- **Unauthorized substitution is inferred, not observed.** The survey deliberately avoided asking about unauthorized hires; φ is a forensic residual and is not statistically precise.

## Data availability

Pre-analysis plan is public at https://osf.io/zdyun (registered 21 October 2021). The lottery data come from public USCIS and DOL sources. Firm survey conducted under Dartmouth IRB #STUDY00032360; the questionnaire is reproduced in Appendix A16. **No replication package, data repository or code archive is announced anywhere in this working-paper text.** The firm-level survey responses are not stated to be publicly available.

---

**Verification:** every numeric row in the headline table carries a quote fragment re-found with `grep -F` against the parsed paper. A final sweep re-checked all 29 distinct fragments used anywhere in this file; all 29 returned at least one hit. Three fragments initially failed on line breaks in the parse and were replaced with the exact on-line form before acceptance. **20 of 20 table rows verified, 29 of 29 fragments verified, 0 rows dropped.**
