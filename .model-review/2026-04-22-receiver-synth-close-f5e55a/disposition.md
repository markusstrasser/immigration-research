# Review Findings — 2026-04-22

**15 findings** from 2 axes (0 cross-model agreements)
Structured data: `findings.json`

1. **[HIGH]** Synthetic control is underdetermined and prone to severe overfitting
   Category: logic | Confidence: 0.9 | Source: Gemini (architecture/patterns)
   The review claims the method fits roughly 370 donor weights to only 4-5 annual pre-treatment observations (2018-2021/2022). With far more parameters than pre-treatment periods, the model can fit noise and achieve near-zero pre-treatment error without identifying a stable counterfactual, making post-treatment gaps highly sensitive to random donor variation.
   File: analyze_receiver_synthetic_controls.py
   Fix: Regularize the weight-fitting objective with an L2 penalty or use subset selection / constrained donor selection so the fitted control cannot overfit a tiny pre-period.

---

2. **[HIGH]** Interference/Leakage in Donor Pool
   Category: logic | Confidence: 0.9 | Source: GPT-5.4 (quantitative/formal)
   The donor pool for synthetic controls contains cities that were also significant 'receivers' or 'dispatchers' of the same immigration intervention. Specifically, Denver's synthetic control is weighted heavily on 'District of Columbia CoC' (34.3%) and 'Washington CoC' (20.5%), both of which were primary destinations for migrant busing in the same period. Chicago's donors include 'Harris County CoC' (Houston), a major transit hub. This 'interference' biases the counterfactual toward the treatment effect, likely understating the true impact.
   File: sources/immigration-causal/data/outcomes/analysis/receiver_synth_weights.csv
   Fix: Exclude all known 'receiver' cities (NYC, DC, Chicago, Denver, Boston) and major border/transit hubs (El Paso, Harris County, Bexar County) from the donor pool for all models.

---

3. **[HIGH]** `overall_to_hic_ratio` uses an endogenous denominator that can mask overload
   Category: logic | Confidence: 0.9 | Source: Gemini (architecture/patterns)
   The reviewer argues that HIC is not fixed: CoCs such as NYC and Denver expanded shelters, hotels, and transitional inventory in response to the migrant surge. Because the treatment can increase the denominator, the `overall_to_hic_ratio` may remain flat even when absolute sheltered or total homeless counts rise sharply, causing the analysis to understate physical system stress.
   File: analyze_receiver_synthetic_controls.py
   Fix: Do not rely on HIC-based ratios alone; add parallel analyses on log-transformed absolute counts such as `log(sheltered)` and `log(total_homeless)` and treat ratio-based conclusions as potentially attenuated by denominator endogeneity.

---

4. **[HIGH]** Donor pool is likely contaminated by quasi-treated migrant hubs
   Category: logic | Confidence: 0.8 | Source: Gemini (architecture/patterns)
   The review argues that `analyze_receiver_synthetic_controls.py` uses a national donor universe of roughly 370 CoCs, which likely includes major post-2022 migrant-receiving jurisdictions such as Washington, DC, Los Angeles, El Paso, Miami, and San Diego. If such cities are used as donors for treated units like NYC or Denver, the synthetic control is exposed to treatment leakage, which would mechanically suppress the estimated treatment effect. The reviewer cites `receiver_synth_weights.csv` as the place where this contamination may already be visible.
   File: analyze_receiver_synthetic_controls.py
   Fix: Explicitly filter the donor pool before fitting weights, excluding major border CoCs and known busing/receiving hubs; verify that excluded cities do not appear in `receiver_synth_weights.csv`.

---

5. **[HIGH]** Placebo inference may be invalid if placebos are ranked by raw post-gap without fit-quality filtering
   Category: logic | Confidence: 0.8 | Source: Gemini (architecture/patterns)
   The review states that raw placebo gap distributions are not meaningful when placebo units have poor pre-treatment fit. It specifically warns that if `receiver_synth_placebos.csv` is built from absolute post-treatment gaps without filtering on pre-treatment MSPE or using post/pre RMSPE ratios, the resulting placebo p-values are structurally invalid.
   File: analyze_receiver_synthetic_controls.py
   Fix: For treated units and all placebos, compute pre-MSPE, post-MSPE, and post/pre RMSPE ratio; drop placebos with pre-MSPE substantially worse than the treated unit (for example >5x), and rank inference by RMSPE ratio rather than raw post-gap. Include these metrics in `receiver_synth_placebos.csv`.

---

6. **[MEDIUM]** Inconsistent Placebo P-Value Filtering
   Category: logic | Confidence: 0.9 | Source: GPT-5.4 (quantitative/formal)
   The placebo analysis in 'receiver_synth_placebos.csv' includes rank-based p-values but doesn't consistently apply a pre-treatment fit filter (e.g., excluding donors with pre-RMSPE > 5x the target's). Without this, the p-value is diluted by 'bad' donors that don't provide a valid counterfactual, leading to potentially misleading 'decisive' results in the memo.
   File: sources/immigration-causal/data/outcomes/analysis/receiver_synth_placebos.csv
   Fix: Calculate p-values based on the ratio of post-intervention RMSPE to pre-intervention RMSPE, rather than the absolute gap, to normalize for the quality of pre-treatment fit across donors.

---

7. **[MEDIUM]** Memo conclusions rely on ratios and omit absolute sheltered/unsheltered count checks
   Category: missing | Confidence: 0.9 | Source: Gemini (architecture/patterns)
   The review says the conclusion in `research/immigration-receiver-counterfactuals-2026-04-22.md` that Boston and Chicago do not survive as simple positive shelter-divergence cases is based entirely on ratio metrics. It argues this misses an obvious disconfirming test: absolute `sheltered` and `unsheltered` PIT counts could have risen substantially while HIC expanded in parallel, leaving ratios near 1.0 and hiding real overload.
   File: research/immigration-receiver-counterfactuals-2026-04-22.md
   Fix: Re-run the counterfactual analysis on absolute count outcomes and revisit memo conclusions wherever ratio-based null findings could be explained by concurrent HIC expansion.

---

8. **[MEDIUM]** Temporal Misalignment of Post-Period Start
   Category: logic | Confidence: 0.8 | Source: GPT-5.4 (quantitative/formal)
   The script defines the post-intervention period as starting after 2022 (year > 2022). However, significant migrant busing to New York City and Chicago began in the spring and summer of 2022. By including 2022 in the pre-treatment optimization, the model attempts to fit the synthetic control to a period where the intervention had already begun, potentially contaminating the baseline.
   File: sources/immigration-causal/scripts/analyze_receiver_synthetic_controls.py
   Fix: Shift the intervention start year to 2022 or use 2021 as the final pre-treatment year to ensure the donor weights are calculated on an uncontaminated baseline.

---

9. **[MEDIUM]** Treatment timing is oversimplified despite PIT counts being annual January snapshots
   Category: logic | Confidence: 0.8 | Source: Gemini (architecture/patterns)
   The review notes that HUD PIT counts occur on a single night in late January, while migrant inflows spiked in late spring/summer 2023. Under that timing, January 2023 largely reflects pre-crisis conditions and January 2024 reflects the shock, so treating 2023 as fully post-treatment creates an overly sharp structural break and may misclassify a transition year.
   File: analyze_receiver_synthetic_controls.py
   Fix: Model 2023 as a partial-treatment or transition period, or shift treatment timing so annual PIT measurement dates align better with when the migrant shock would appear in the observed outcomes.

---

10. **[MEDIUM]** Synthetic control specification omits structural covariates
   Category: missing | Confidence: 0.8 | Source: Gemini (architecture/patterns)
   The review argues the implementation appears to rely only on lagged dependent variables despite a very short pre-period. It says this leaves the model blind to major structural differences across CoCs, such as population density, housing costs, and climate, which standard synthetic control workflows often include to improve match quality and plausibility.
   File: analyze_receiver_synthetic_controls.py
   Fix: Augment the matching/fitting step with structural covariates relevant to homelessness dynamics, in addition to lagged outcomes.

---

11. **[MEDIUM]** HUD PIT data are treated as neutral despite known instrument bias
   Category: constitutional | Confidence: 0.7 | Source: Gemini (architecture/patterns)
   The review argues the memo and script do not acknowledge that HUD PIT counts are politically sensitive, subject to local methodological changes, and structurally weak for fast-moving migrant populations, especially for winter unsheltered undercount. It characterizes this as a failure to name the frame and flag instrument bias while drawing causal conclusions from the PIT-based outcomes.
   File: research/immigration-receiver-counterfactuals-2026-04-22.md
   Fix: Add explicit limitations on PIT measurement bias, document known undercount risks and methodological sensitivity, and qualify causal claims accordingly.

---

12. **[MEDIUM]** No in-time placebo falsification is reported
   Category: missing | Confidence: 0.7 | Source: Gemini (architecture/patterns)
   The review recommends an in-time falsification test by assigning treatment to 2020 and checking whether the model still produces a non-zero effect during 2020-2022. A significant pseudo-effect in that period would indicate the pre-treatment fit is artifactual rather than identifying a real post-2022 shock.
   File: analyze_receiver_synthetic_controls.py
   Fix: Add an in-time placebo test that shifts treatment earlier (for example to 2020) and require the pseudo-treatment effect to be near zero before trusting the main specification.

---

13. **[MEDIUM]** Unified panel treats transit hubs and destination cities as causally identical
   Category: architecture | Confidence: 0.7 | Source: Gemini (architecture/patterns)
   The review claims the script applies one common panel setup to places with different roles in the migrant network, such as Bexar/San Antonio as a transit hub versus NYC and Chicago as terminal destinations. This may blur distinct overload mechanisms and undermine causal interpretation because the same treatment ontology is imposed on heterogeneous node types.
   File: analyze_receiver_synthetic_controls.py
   Fix: Stratify analyses by node type or run separate specifications for transit hubs, border hubs, and terminal destination CoCs rather than assuming a single common treatment mechanism.

---

14. **[MEDIUM]** Donor pool is not screened for unstable pre-treatment measurement artifacts
   Category: missing | Confidence: 0.6 | Source: Gemini (architecture/patterns)
   The review recommends excluding CoCs with large pre-treatment PIT volatility, noting that localized methodological changes in counting can create artifact-driven fits. It proposes flagging donor units with more than 30% year-over-year variance in the pre-treatment period and dropping them so unstable measurement practices do not distort the synthetic control weights.
   File: analyze_receiver_synthetic_controls.py
   Fix: Add donor-pool scrubbing that detects unusually volatile pre-treatment series (for example >30% YoY changes) and excludes those CoCs from eligibility as donors. [UNCALIBRATED]

---

15. **[LOW]** Strict Convex Hull Constraint Without Intercept
   Category: architecture | Confidence: 0.8 | Source: GPT-5.4 (quantitative/formal)
   The optimization uses SLSQP to enforce weights that sum exactly to 1.0 with no intercept term. For extreme outliers like New York City (sheltered homelessness > 80k), there are few or no donors with comparable magnitudes. This forces the synthetic control to the upper boundary of the donor pool's convex hull, resulting in a poor pre-treatment fit (high pre_rmse) and a 'mechanical' gap that may not represent a true causal divergence.
   File: sources/immigration-causal/scripts/analyze_receiver_synthetic_controls.py
   Fix: Implement an intercept/bias term in the synthetic control calculation (Abadie 2021) or de-mean the series prior to optimization to allow for level differences between the target and donors.

---

## Agent Response (fill before implementing)

### Where I disagree with the disposition:
<!-- "Nowhere" is valid. Don't invent disagreements. -->


### Context I had that the models didn't:
<!-- If context file was comprehensive, say so. -->

