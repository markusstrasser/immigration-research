# E-Verify staggered DiD on QWI — observed wage-channel test

**Date:** 2026-04-18
**Question:** Do state E-Verify mandates produce positive QWI wage effects for low-education native workers? Borjas-style large-gain predictions imply yes; Card-style small/native-null predictions imply small or no observed gains.
**Design:** Two-way fixed effects (state + year) on log earnings of stable workers, by education and industry, 2003-2023. Treatment = year ≥ state E-Verify effective year. 9 treated states (AZ, MS, SC, UT, GA, AL, NC, TN, FL), 42 control states.

## Bottom line

E-Verify mandates produced **no statistically significant positive wage effect** on low-education workers in the wage specifications. Point estimates are tiny (within ±1.5%) with mixed signs. The 95% CI rules out large native-wage gains in this observed mandate margin, but it does not rule out small effects or a Borjas prediction scaled to a smaller realized labor-supply shock. **In this E-Verify design, the wage results are closer to the Card-style null than to large Borjas-style native wage gains.**

Employment side: E1 (less than HS) stable W-2 employment in E-Verify-exposed industries (Ag, Constr, Mfg, Food Service) has a negative, statistically nonsignificant point estimate of about -6% (t=-1.40, p≈0.16). Combined picture: QWI wages show no statistically significant positive response, while the W-2 employment point estimate is negative but not conventionally significant. That points away from large native wage bidding in this observed design; it does not identify whether adjustment happened through capital, output, relocation, cash-economy substitution, hours, or composition.

## Method

### Data
- **QWI (Census LEHD)** `se` endpoint, 2003-Q1 to 2023-Q4, all 50 states + DC, 9 industries (00, 11 Ag, 23 Constr, 31-33 Mfg, 44-45 Retail, 56 Admin, 62 Health, 72 Accom/Food, 81 Other), 4 education groups (E1 less-HS, E2 HS, E3 some college, E4 BA+). 151k state×year×quarter×industry×education observations. [SOURCE: api.census.gov/data/timeseries/qwi/se]
- **E-Verify mandate panel** (compiled from Bohn-Lofstrom-Raphael 2014, Orrenius-Zavodny 2015, state legislation):
  - AZ effective 2008; MS 2008; SC 2010; UT 2010 (15+ ee); GA 2012 (10+ ee); AL 2012; NC 2012 (25+ ee); TN 2012 (6+ ee); FL 2023 (25+ ee)
  - Public-only mandates (IN, MO, NE, OK, PA, VA, ID, MN, TX) excluded from treatment (don't bind on private labor market)

### Specifications

**Main TWFE:**
$$\log \text{EarnS}_{ist} = \beta \cdot \text{EVerify}_{st} + \alpha_s + \gamma_t + \varepsilon_{ist}$$

where i = (industry, education) cell, s = state, t = year×quarter. SE clustered at state level (Liang-Zeger).

Run separately by education group, with three industry restrictions:
- All industries (excluding 00 aggregate to avoid double-counting)
- E-Verify-exposed (11, 23, 31-33, 72)
- Total aggregate (00 only)

**Event study:** Replace the treatment indicator with leads and lags 1[year - effective_year = k] for k ∈ {-6, ..., +8} \ {-1}. Identifies dynamic effects with state and year FEs absorbed.

**Employment:** Same specification with log(EmpS) as outcome.

## Results

### TWFE main (clustered SE on state)

| Education | Industry set | β (log earns) | % effect | SE | t | n |
|-----------|--------------|---------------|----------|-----|---|---|
| **E1 (<HS)** | All non-aggregate | -0.0044 | -0.44% | 0.0094 | -0.47 | 37,716 |
| **E1 (<HS)** | E-Verify-exposed | +0.0051 | +0.51% | 0.0081 | +0.63 | 16,736 |
| **E1 (<HS)** | Total aggregate (00) | -0.0148 | -1.46% | 0.0113 | -1.30 | 4,196 |
| E2 (HS) | E-Verify-exposed | +0.0080 | +0.80% | 0.0080 | +0.99 | 16,737 |
| E3 (some col) | E-Verify-exposed | +0.0039 | +0.39% | 0.0080 | +0.49 | 16,737 |
| E4 (BA+) | E-Verify-exposed | -0.0096 | -0.95% | 0.0125 | -0.76 | 16,737 |

**No coefficient reaches conventional significance (|t|>1.96). Point estimates are mostly within ±1%.** The 95% CI excludes E1 exposed-industry wage gains above about +2.1%. That rules out large gains in this observed mandate margin, but a benchmark mechanically scaled from Borjas's 10% supply -> 3-4% wage elasticity to a smaller effective shock would be closer to the CI boundary.

### Event study (E1 in E-Verify-exposed industries)

Pre-trends are flat. Post-treatment coefficients are slightly negative through year 7, then jump positive at year 8 with very high SE (likely COVID-era noise + small treated cohort at long horizons).

| Event time | β (log earns) | SE |
|-----------|---------------|-----|
| -6 | +0.005 | 0.012 |
| -5 | +0.002 | 0.011 |
| -4 | -0.006 | 0.007 |
| -3 | -0.004 | 0.006 |
| -2 | +0.003 | 0.003 |
| -1 | 0 (ref) | — |
| 0 | +0.001 | 0.003 |
| +1 | -0.005 | 0.005 |
| +2 | -0.007 | 0.006 |
| +3 | -0.009 | 0.007 |
| +4 | -0.004 | 0.006 |
| +5 | -0.006 | 0.008 |
| +6 | -0.006 | 0.008 |
| +7 | -0.004 | 0.010 |
| +8 | +0.011 | 0.012 |

No significant pre-trend. No significant post-treatment jump in either direction. Point estimates lean slightly negative for years 1-7, but they are not statistically distinguishable from zero and should not be read as evidence for a specific complementarity-loss mechanism.

### Employment side

| Education | Industry set | β (log emp) | % effect | t | n |
|-----------|--------------|-------------|----------|---|---|
| **E1** | E-Verify-exposed | **-0.0630** | **-6.11%** | -1.40 | 16,723 |
| E1 | Total aggregate | -0.0089 | -0.88% | -0.22 | 4,196 |
| E2 | E-Verify-exposed | -0.0153 | -1.52% | -0.48 | 16,723 |
| E3 | E-Verify-exposed | -0.0149 | -1.48% | -0.60 | 16,721 |
| E4 | E-Verify-exposed | -0.0129 | -1.28% | -0.50 | 16,719 |
| E4 | Total aggregate | +0.0405 | **+4.13%** | +2.19** | 4,196 |

**E1 stable-employment in exposed industries has a negative ~6% point estimate post-mandate** (not conventionally significant, p≈0.16). The sign is qualitatively consistent with Bohn-Lofstrom-Raphael (2014) for Arizona alone (~10pp unauthorized-pop decline), but this pooled QWI estimate should not be treated as a measured employment decline. QWI also captures W-2 employment, so it underweights cash-economy displacement.

Total-economy E4 (BA+) employment grew ~4% (p<0.05) but this likely reflects national skill-upgrading rather than mandate causal effect.

## Interpretation

### What Card predicted

- Low-skill immigrants are imperfect substitutes for low-skill natives
- Removing them via enforcement is predicted to produce small or zero wage gains for natives
- General-equilibrium effects (output loss, capital reallocation, output-mix shift) may even hurt natives
- Card-Peri (2016) and Foged-Peri (2016) Denmark: native low-skill workers move into more communication-intensive tasks, see no wage loss

### What Borjas predicted

- Substitution elasticity is high; immigrant supply shifts shift the native wage curve down
- Borjas (2003) QJE: 10% increase in supply lowers wages of competing natives by 3-4%
- Borjas (2017) reanalysis of Mariel Boatlift: -10 to -30% wage drop for HS dropouts
- Implication: removing unauthorized labor should raise native low-skill wages substantially

### What the data show

- **No statistically significant positive QWI wage effect was observed for native low-skill workers after E-Verify**, including the most sympathetic test (E1 workers in the exact industries where unauthorized are concentrated — Ag, Constr, Mfg, Food Service)
- **Stable W-2 employment in exposed industries has a negative point estimate** for E1 workers (~6%, p≈0.16). This is qualitatively consistent with the Bohn-Lofstrom-Raphael Arizona result, but QWI cannot by itself distinguish true labor-supply contraction from cash-economy movement, hours changes, establishment composition, or worker reclassification.
- **Together: no statistically significant positive QWI wage effect, plus a negative but nonsignificant W-2 employment point estimate, means the large native wage-bidding channel is not observed in this design.** Candidate adjustment channels remain hypotheses, not measured mechanisms:
  1. Capital substitution (mechanization in Ag, prefab in Constr)
  2. Output reduction or relocation (firms exit; consumers face higher prices/lower service)
  3. Cash economy / non-W-2 hiring (which doesn't show up in QWI)
  4. Outsourcing across state lines
  5. Hours, occupation, or establishment-composition shifts inside QWI cells

For this enforcement margin, the adjustment looks Card-style: the wage curve is flatter than the large-Borjas-gain prediction, and observed E-Verify mandate variation shows no statistically significant rent transfer to native low-skill workers through higher QWI wages.

### Power and caveats

1. **Power.** With 9 treated states, 42 controls, and 21 years, the minimum detectable effect (MDE) at α=0.05 with 80% power is roughly ±2-3% for E1 in exposed industries given clustered SE. Large Borjas-style gains would be detectable in this margin, but a benchmark scaled to the nonsignificant employment point estimate could be around the CI boundary. **We can reject large gains in this observed mandate design; we cannot reject small positive effects.**

2. **TWFE under heterogeneous treatment.** Sun-Abraham (2021), Goodman-Bacon (2021) caution: TWFE with staggered timing can be biased when effect sizes vary across cohorts. Robustness check should use Callaway-Sant'Anna or Sun-Abraham. Given the mostly-flat event-study coefficients here, I judge the bias is unlikely to flip the sign or magnitude meaningfully.

3. **Treatment intensity heterogeneity.** AZ all-employer mandate (2008) is much tighter than UT 15+ employee (2010). A continuous "fraction of workers covered" treatment would sharpen the test. Doable as a follow-up.

4. **Compliance is partial.** US E-Verify compliance ~50% even in mandate states (CIS 2017 estimate). The intent-to-treat estimate underweights actual treated workers. A 2× adjustment is a sensitivity only, not a measured compliance correction; it would put the MDE around 4-6%, weakening claims about the low end while still cutting against high-end Borjas magnitudes.

5. **Unauthorized substitution to cash economy.** If displaced unauthorized workers stayed in the same labor market but moved to off-W-2 jobs (day labor, gig), QWI misses them. That possibility weakens any interpretation of the QWI E1 drop as a full labor-supply contraction; it does not rescue a large QWI-wage-gain prediction in this design.

6. **External validity.** This is the policy variation we have. Results may not generalize to a hypothetical mass deportation, large refugee inflow, or border closure. It is one relevant test for marginal tightening of unauthorized labor supply via state enforcement mandates, not the policy debate as a whole.

## What this updates in the existing repo

### Confidence ladder
- Move `Federal-positive vs federal-negative origin ranking from ACS income/benefit proxies` from `weak` → unchanged (this finding addresses wages, not federal fiscal)
- Add new entry: **`Borjas substitution prediction for U.S. low-skill native wages from E-Verify policy variation`** — `strong against large Borjas-style gains in this E-Verify margin`. Point estimate ±1%, 95% CI excludes the high-end Borjas magnitudes.
- Strengthen entry on `Claim that the Clark agree papers are scope-limited rather than obviously false` from `strong` → `strong+`. The small-native-wage-effect reading associated with those Clark responses is supported on this E-Verify margin.

### Verified-findings report bottom line
- The previous report said: "Some national output and consumer-price gains exist; some indirect federal fiscal offsets likely exist; but local schooling, housing, and service-capacity costs remain concentrated." [SOURCE: research/immigration-verified-findings-report-2026-04-10.md, finding #6]
- This holds. **Add:** for the wage channel specifically, observed E-Verify policy variation in 2008-2023 supports the Card-side reading on this margin. No statistically significant positive higher-QWI-wage effect is observed for native low-skill workers under these mandates; this cuts against large Borjas-style gains in the observed mandate margin but does not directly measure the full wage effect of current low-skill immigration levels.

### Adversarial review §1 ("we still don't have a full national welfare ledger")
- This finding doesn't deliver a full national welfare ledger.
- It narrows one open question: the labor-market wage channel for native low-skill workers under observed marginal enforcement variation. That contributes to the ledger from the credit side only within this policy range, not as a universal no-native-loss claim.

### Updates to the smith-decker-friedman audit
- David D. Friedman's open-borders argument relies in part on Card-style wage elasticity. This analysis supports that wage-channel premise for observed E-Verify variation, not the full open-borders conclusion.
- Camarota's CIS-style native-wage-depression argument is not supported for large native wage effects in this observed E-Verify wage-channel test.
- Smith and Decker's average-consumer-gains framing is consistent with this finding.

## Comparison to literature

| Study | Population | Design | Wage effect | Direction in that design |
|-------|-----------|--------|-------------|------|
| Card (1990) | Mariel Boatlift, Miami | Synthetic control vs comparison cities | ~0% on Miami HS dropouts | Card |
| Borjas (2017) | Mariel reanalysis, restricted to HS dropouts | Same data, narrower group | -10 to -30% | Borjas |
| Bohn-Lofstrom-Raphael (2014) | AZ LAWA | Pop survey on unauth share | Unauth ↓; native effects mixed | Mixed |
| Orrenius-Zavodny (2015) | E-Verify rollout | DiD on CPS earnings | Small positive on Hispanic native women only | Weak Borjas |
| **This analysis** | **9 E-Verify states** | **TWFE on QWI 2003-2023** | **+0.5% (n.s.) E1 in exposed industries** | **no detected large native gain in this margin** |
| Foged-Peri (2016) | Denmark refugee-country inflow | Dispersal-policy IV / DiD | Native low-skill wages ↑ from refugee shock | cuts against large native loss in that setting |
| Card-Peri (2016) | Cumulative immigration | National panel | Small / null on natives | small/native-null in that design |

This analysis adds a 21-year multi-state version of the E-Verify test. Read with Card (1990) and Foged-Peri (2016), it supports the bounded claim that large native low-skill wage losses/gains are not observed in these designs; it does not identify one shared adjustment mechanism or rule out small effects.

## Honest limits

1. The wage-effect non-result is what I expected from prior literature. **Confirmation, not surprise.** This is not a novel finding — it extends the E-Verify policy-margin check with a longer QWI panel and broader treatment set, and is consistent with the Card-Peri wage literature. The contribution is updating the *repo's* confidence in the Card view from "the agree economists are scope-limited" to "their small-native-wage-effect premise is better supported for the policy variation we have."

2. **What this does NOT settle:**
   - Whether a mass-deportation shock would behave the same (unknown — different magnitudes and equilibria)
   - Whether wage effects exist for sub-groups outside QWI's coverage (cash economy, very small firms exempt from mandate)
   - Whether non-wage channels (employment composition, occupational sorting, hours) absorb the supply shock
   - Whether the long-run (>10 year) effect differs from the medium-run captured here

3. **Replication invitation.** Code: `sources/immigration-causal/scripts/analyze_everify_wages.py` and `analyze_everify_employment.py`. Data: `data/lehd/qwi_state_panel.parquet` (151k rows, 2 MB). Treatment panel: `data/everify/everify_state_mandates.csv`.

## Revisions

| Date | Change |
|------|--------|
| 2026-06-16 | Replaced "suggestive of mild complementarity loss" and "probably not" mass-shock shorthand with interpretation language that keeps nonsignificant coefficients and out-of-margin shocks unresolved. See `immigration-conclusion-audit-running-fixes.md`. |
| 2026-06-16 | Rephrased the Card-side setup from "will produce" wage gains to prediction language, keeping theory expectations distinct from measured findings. See `immigration-conclusion-audit-running-fixes.md`. |
| 2026-06-16 | Replaced speculative cash-economy substitution language with a narrower measurement caveat: off-W-2 substitution weakens E1 as a total labor-supply proxy, while leaving the QWI wage-gain result bounded to this design. See `immigration-conclusion-audit-running-fixes.md`. |
| 2026-06-16 | Narrowed the external-validity caveat from "the relevant test for the actual policy debate" to one relevant test for marginal enforcement mandates. See `immigration-conclusion-audit-running-fixes.md`. |
| 2026-06-16 | Replaced residual "do not move wages much" summary with bounded no-large-native-wage-loss/gain language and separated it from any shared mechanism claim. See `immigration-conclusion-audit-running-fixes.md`. |
| 2026-06-16 | Replaced residual "does not measurably transfer rents" shorthand with no-statistically-significant higher-QWI-wage transfer language; small effects remain outside rejection. See `immigration-conclusion-audit-running-fixes.md`. |
| 2026-06-16 | Scoped the title/question and bottom-line employment/wage shortcut to the observed QWI E-Verify wage-channel test rather than a broad Card-vs-Borjas verdict for U.S. data. See `immigration-conclusion-audit-running-fixes.md`. |
| 2026-06-16 | Replaced "removing/restricting unauthorized labor" exports with observed E-Verify mandate variation and QWI wage language; the design does not directly observe total unauthorized labor supply. See `immigration-conclusion-audit-running-fixes.md`. |
| 2026-06-16 | Narrowed the employment/wage mechanism interpretation: QWI shows a negative but nonsignificant stable W-2 employment point estimate while no statistically significant positive wage effect was observed; it does not identify capital, output, relocation, cash-economy, hours, or composition adjustment mechanisms. See `immigration-conclusion-audit-running-fixes.md`. |
| 2026-06-16 | Replaced "Clark economists were correct/right" language with support for the small-native-wage-effect premise in the observed E-Verify margin. See `immigration-conclusion-audit-running-fixes.md`. |
| 2026-06-16 | Bounded "data side with Card" and commentator-update language to the observed E-Verify wage-channel design; the result rejects large Borjas-style native wage gains for this margin, not all wage or open-borders questions. See `immigration-conclusion-audit-running-fixes.md`. |
| 2026-06-16 | Aligned the proposed confidence-ladder update with the same margin-specific wording: strong against large Borjas-style gains in the E-Verify margin, not a global "STRONG REJECTION." See `immigration-conclusion-audit-running-fixes.md`. |
| 2026-06-16 | Clarified Foged-Peri design shorthand from opaque "RA quasi-IV" to dispersal-policy IV / DiD, matching the paper's quasi-experimental design. See `immigration-conclusion-audit-running-fixes.md`. |
| 2026-06-16 | Replaced "replicates Orrenius-Zavodny and Card-Peri" with extension/consistency language; the QWI E-Verify panel is not a direct replication of those papers. See `immigration-conclusion-audit-running-fixes.md`. |

[SOURCE: data/analysis/everify_twfe_results.csv]
[SOURCE: data/analysis/everify_event_study_E1.csv]
[SOURCE: data/analysis/everify_employment_twfe.csv]
[SOURCE: scripts/analyze_everify_wages.py]
[SOURCE: scripts/analyze_everify_employment.py]
[SOURCE: scripts/pull_qwi_state_panel.py]

<!-- knowledge-index
generated: 2026-04-19T03:43:48Z
hash: 224b29836cf0

cross_refs: research/immigration-verified-findings-report-2026-04-10.md

end-knowledge-index -->
