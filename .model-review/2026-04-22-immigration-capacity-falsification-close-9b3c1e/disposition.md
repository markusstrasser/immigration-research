# Review Findings — 2026-04-22

**18 findings** from 2 axes (0 cross-model agreements)
Structured data: `findings.json`

1. **[HIGH]** Conflation of newcomer ratio estimands
   Category: logic | Confidence: 1.0 | Source: GPT-5.4 (quantitative/formal)
   The newcomer memo calculates a 4.49% IRS inflow vs 0.21% moved-from-abroad flow, implying a ratio of 21.38, yet reports a 'roughly 20.5x' ratio. This suggests the 20.5x figure is a median of county-level ratios, which is a different estimand than the ratio of medians.
   File: research/immigration-causal-internal-vs-immigrant-newcomers.md
   Fix: Separate and name all newcomer ratio estimands: ratio-of-medians, median-of-ratios, and zero-denominator share.

---

2. **[HIGH]** Invalid Wilson intervals on dependent splits
   Category: bug | Confidence: 1.0 | Source: GPT-5.4 (quantitative/formal)
   The threshold-search null CI uses Wilson intervals over repeated random state splits. Because splits over a finite set of states are dependent, Wilson intervals (which assume i.i.d. Bernoulli trials) are not calibrated for inferential use.
   File: sources/immigration-causal/scripts/analyze_capacity_falsification.py
   Fix: Replace with descriptive intervals or use state-blocked/leave-one-state-out (LOSO) inference.

---

3. **[HIGH]** Ambiguous directional bias in newcomer comparison
   Category: logic | Confidence: 0.9 | Source: GPT-5.4 (quantitative/formal)
   The claim that the domestic-vs-foreign gap is a 'lower-bound' is undermined by a timing mismatch between IRS (2022-2023) and ACS (2022 5-year). If foreign-origin flow accelerated late in the window, the ACS pooled estimate understates current flow, potentially making the gap look too large rather than too small.
   File: research/immigration-causal-internal-vs-immigrant-newcomers.md
   Fix: Downgrade directional-bias claim to 'sign ambiguous' unless verified by a sensitivity grid across population thresholds and MOE filters.

---

4. **[HIGH]** QCEW wage growth is analyzed in nominal terms without inflation adjustment
   Category: logic | Confidence: 0.9 | Source: Gemini (architecture/patterns)
   The review argues that `build_county_outcome_panel.py` relies on QCEW `annual_avg_wkly_wage` in nominal dollars across 2021-2024, a period of elevated inflation. Comparing log changes in nominal wages across counties may confound wage effects with differing regional inflation trajectories, especially if high-permit and low-permit counties experienced different price growth. The reviewer suggests the reported wage penalty could shrink, vanish, or grow after deflation.
   File: build_county_outcome_panel.py
   Fix: Deflate base and end-year wages before computing log changes, at minimum with a national CPI series and ideally with BEA Regional Price Parities or another local price adjustment.

---

5. **[HIGH]** Dropped QCEW nondisclosures may create MNAR sample bias
   Category: logic | Confidence: 0.9 | Source: Gemini (architecture/patterns)
   The review points out that `build_county_outcome_panel.py` converts QCEW `disclosure_code == 'N'` observations to `NA` and drops them from downstream analysis, while suppressions are likely concentrated in low-population, single-employer counties. The concern is that the panel may systematically exclude rural counties where immigrant labor shocks are theoretically important, producing missing-not-at-random bias. The reviewer specifically asks for an audit comparing immigrant-flow measures in suppressed versus non-suppressed counties.
   File: build_county_outcome_panel.py
   Fix: Quantify suppression bias in `county_outcome_panel_audit.json` by comparing characteristics of disclosed versus nondisclosed counties, especially `recent_fb_annual_share`, and consider sensitivity analyses or explicit missingness flags rather than silent exclusion.

---

6. **[HIGH]** Unjustified upgrade to moderate causal confidence
   Category: logic | Confidence: 0.9 | Source: GPT-5.4 (quantitative/formal)
   The memo upgrades the stress-marker result to 'moderate causal confidence' based on geographic robustness, despite clean-window leads being non-null and employment pre-trends being negative. This jump from association to causality is not supported by the cited artifacts.
   File: research/immigration-capacity-falsification-2026-04-21.md
   Fix: Implement a causal-confidence gate: forbid 'moderate' or 'high' ratings if clean pre-surge windows show sign instability or nontrivial lead effects.

---

7. **[HIGH]** Permutation null may be invalid if shuffled series re-aligns on original index
   Category: bug | Confidence: 0.5 | Source: Gemini (architecture/patterns)
   The review raises a specific implementation risk in `analyze_capacity_falsification.py`: if the null permutation is generated with something like `df['recent_fb_annual_share'].sample(frac=1)` and then assigned back without stripping the original index, pandas may align values back to their original rows. In that failure mode, the 'permuted' null could accidentally equal the actual data, making the null benchmark moot. The reviewer explicitly notes this depends on implementation details and cannot verify it without execution.
   File: analyze_capacity_falsification.py
   Fix: Ensure permutations break index alignment by resetting the index or assigning `.to_numpy()`/`.values` from the shuffled series before reattachment; add a test asserting that the permuted column differs from the original ordering.

---

8. **[MEDIUM]** Median-county newcomer ratios likely misstate typical resident exposure
   Category: logic | Confidence: 1.0 | Source: Gemini (architecture/patterns)
   The review flags that `analyze_internal_vs_immigrant_newcomers.py` computes the stylized fact using the median county-level `us_inflow_share` versus the median `moved_from_abroad_share` for counties with `totpop >= 10k`. This overweights small counties, so the quoted `20.5x` ratio reflects the median county rather than the exposure faced by the median resident. The reviewer specifically recommends population-weighted means and also an aggregate national ratio because median-county statistics can systematically overweight rural dynamics.
   File: analyze_internal_vs_immigrant_newcomers.py
   Fix: Replace or supplement median-county reporting with population-weighted means (e.g. `np.average(..., weights=totpop)`) and compute aggregate IRS inflow totals divided by aggregate ACS moved-from-abroad totals; update the memo to report these measures.

---

9. **[MEDIUM]** Threshold-search null lacks regional or spatial correlation structure
   Category: missing | Confidence: 0.9 | Source: Gemini (architecture/patterns)
   The review says `analyze_capacity_falsification.py` only uses a within-state permutation null for recent-flow thresholds. That controls for state-level confounding but may miss cross-state spatial blocks such as a whole Census division moving together. The reviewer recommends a tougher adversarial null, such as within-division permutation or a spatial-lag-aware design, and notes that some small states may have too few counties for a meaningful within-state null.
   File: analyze_capacity_falsification.py
   Fix: Add alternative null designs such as within-division permutation or spatially constrained permutation, and record the null design in the output JSON.

---

10. **[MEDIUM]** Pretrend instability is not formalized with an explicit stability metric
   Category: missing | Confidence: 0.9 | Source: Gemini (architecture/patterns)
   The review agrees with downgrading the wage-channel claim but criticizes the current approach for relying on sign comparisons between `2017-2018` and `2018-2019` windows. It recommends that `analyze_capacity_falsification.py` compute an explicit pre-treatment variance or stability score and penalize the post-surge effect when pretrend variance exceeds effect magnitude. The proposed output includes a formal `wage_pretrend_stability_index`.
   File: analyze_capacity_falsification.py
   Fix: Add a quantitative pretrend-stability metric based on the variance or standard error of pre-period estimates and include it in summary outputs used to qualify post-period claims.

---

11. **[MEDIUM]** Underspecified newcomer ratio for zero denominators
   Category: bug | Confidence: 0.9 | Source: GPT-5.4 (quantitative/formal)
   The median ratio for newcomer flow is reported without defining how counties with zero 'moved_from_abroad' shares are handled. For sparse data, this omission significantly changes the estimand.
   File: sources/immigration-causal/scripts/analyze_internal_vs_immigrant_newcomers.py
   Fix: Add an explicit machine-readable field for the share of zero or undefined ratio counties and document the handling of zero denominators.

---

12. **[MEDIUM]** Lack of quantitative metrics for threshold surface diffuseness
   Category: missing | Confidence: 0.9 | Source: GPT-5.4 (quantitative/formal)
   The claim that the threshold-location surface is 'diffuse' is qualitative and impressionistic. With only 100 splits across a 14-cell grid, selection shares move in 1-point increments without a formal concentration metric.
   File: sources/immigration-causal/scripts/analyze_capacity_falsification.py
   Fix: Quantify instability using concentration metrics like entropy, HHI, or actual-minus-null top-cell share.

---

13. **[MEDIUM]** IRS migration data uncertainty is not quantified alongside ACS error
   Category: missing | Confidence: 0.9 | Source: Gemini (architecture/patterns)
   The review notes that `analyze_internal_vs_immigrant_newcomers.py` flags high ACS margins of error for moved-from-abroad estimates but does not provide an analogous quantified warning for IRS SOI migration undercoverage, especially omission of low-income non-filers. This asymmetry can make the domestic inflow numerator appear more trustworthy than the foreign inflow numerator and may exaggerate the domestic-versus-foreign newcomer contrast.
   File: analyze_internal_vs_immigrant_newcomers.py
   Fix: Add an explicit IRS coverage caveat or uncertainty flag, and if possible quantify sensitivity to non-filer undercount or report the domestic-versus-foreign ratio as descriptive with stronger source-limitations language.

---

14. **[MEDIUM]** Improper source attribution for semantic claims
   Category: style | Confidence: 0.8 | Source: GPT-5.4 (quantitative/formal)
   Semantic claims regarding construct definitions (e.g., newcomer totals not being immigration-specific) are sourced to data parquets rather than the scripts or data dictionaries that define those constructs.
   File: research/immigration-causal-internal-vs-immigrant-newcomers.md
   Fix: Cite scripts and data dictionaries for construct meaning; reserve parquet citations for data provenance.

---

15. **[MEDIUM]** Flow-to-capacity stress metric may be unstable near zero permit capacity
   Category: logic | Confidence: 0.8 | Source: Gemini (architecture/patterns)
   The review argues that the flow/capacity construct has a zero lower bound in the permit denominator, so counties with near-zero historical permit rates can generate explosive or undefined continuous stress ratios. The current analysis reportedly sidesteps this with quantiles, but the underlying continuous manifold is left unexamined, raising concerns about monotonicity and interpretability.
   File: analyze_capacity_falsification.py
   Fix: Inspect the continuous stress measure directly, regularize or floor the denominator, and test robustness to alternative formulations such as log transforms, winsorization, or discrete bins justified by data support.

---

16. **[MEDIUM]** Wilson intervals may be too narrow if holdout folds are correlated
   Category: logic | Confidence: 0.7 | Source: Gemini (architecture/patterns)
   The review flags a statistical validity issue in the threshold-evaluation code: Wilson score intervals assume approximately independent Bernoulli trials, but the holdout folds are states that may share regional economic shocks and intra-class correlation. If folds are correlated, the reported confidence intervals for transfer or sign success could be anti-conservative.
   File: analyze_capacity_falsification.py
   Fix: Use a dependence-robust uncertainty method for fold-level success rates, such as block bootstrap, cluster-robust intervals, or explicitly report that Wilson intervals are heuristic under correlated folds.

---

17. **[LOW]** Newcomer shares use inconsistent denominators
   Category: bug | Confidence: 0.9 | Source: Gemini (architecture/patterns)
   The review notes a denominator mismatch in `analyze_internal_vs_immigrant_newcomers.py`: `moved_from_abroad_share` uses ACS `B07001_081E / B07001_001E` (population age 1+), while `us_inflow_share` uses `us_inflow_persons / totpop` where `totpop` is `B01003_001E` (total population). Even if the numerical effect is small, the two ratios are not strictly comparable and may introduce silent measurement drift.
   File: analyze_internal_vs_immigrant_newcomers.py
   Fix: Normalize both shares to the same population denominator, preferably using a consistent ACS universe or total population for both measures, and document the choice.

---

18. **[LOW]** Non-falsifiable policy relevance claim
   Category: missing | Confidence: 0.8 | Source: GPT-5.4 (quantitative/formal)
   The claim that 'policy relevance remains high' lacks an operationalized metric or success criterion, making it untestable and framing-sensitive.
   File: 
   Fix: Define a specific, falsifiable metric for policy relevance or tag the claim as [FRAMING-SENSITIVE].

---

## Agent Response (fill before implementing)

### Where I disagree with the disposition:
<!-- "Nowhere" is valid. Don't invent disagreements. -->


### Context I had that the models didn't:
<!-- If context file was comprehensive, say so. -->

