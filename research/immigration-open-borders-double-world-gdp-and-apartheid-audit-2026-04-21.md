# Open Borders “double world GDP” and “apartheid” audit

**Current assessment: 2026-09-05.** The literature supports potentially large gains from labor mobility. It does not supply a single verified policy forecast of doubling world GDP. This repo's former “rejected” verdict also went beyond what its model comparison and capacity calculations demonstrated. The distinction is between a conditional result, an empirically supported central estimate, and a proved upper bound. [INFERENCE]

## Evidence and current status

| Proposition | Current assessment |
|---|---|
| Labor mobility can create substantial gains | Supported by the cited models and place-premium evidence; magnitude remains conditional. |
| Marginal place premiums alone determine a fully liberalized equilibrium | Not established: large-scale wages, capital, institutions, and migration choices are additional questions. |
| A realistic central estimate is near 100% of world GDP | Not established by this audit. This is not equivalent to proving long-run gains must be smaller. |
| The most realistic estimate is necessarily about 4% | Withdrawn. This privileges a 2012 draft and conflates different scenarios and horizons. |
| Current US construction proves global housing binds in year 1 | Withdrawn. The geographic denominator and transition assumptions do not identify global capacity. |
| The moral analogy determines the GDP result | No. Moral premises and institutional comparisons do not settle the empirical counterfactual. |

[SOURCE: https://www.aeaweb.org/articles?id=10.1257/jep.25.3.83; https://doi.org/10.1111/sjoe.12097] [INFERENCE]

## Model comparisons

Clemens's survey collects conditional estimates; it is not itself a realized policy experiment. Kennan, Bradford, and Iregui use different migration responses, capital assumptions, and measures of gains. Large movements in particular models are relevant to their implementation, but Bradford's 94–97% workforce relocation should not be attributed to every near-doubling model. A result that assumes extensive movement is not arithmetically invalid merely because its implementation is difficult. [SOURCE: https://www.aeaweb.org/articles?id=10.1257/jep.25.3.83; https://freit.org/WorkingPapers/Papers/Immigration/FREIT432.pdf] [INFERENCE]

The **2012 Docquier–Machado–Sekkat draft** gives roughly 17% with incompressible costs and roughly 4% after its combined refinements and networks. The **published 2015 paper** reports **11.5–12.5% in the medium term**, with **7.0–17.9%** across reported robustness cases. The older low estimate is real but cannot stand in for the published benchmark. [SOURCE: https://sites.uclouvain.be/econ/DP/IRES/2012023.pdf; https://doi.org/10.1111/sjoe.12097]

**[GAP]** The 2012 model sections were read; the final 2015 figures were verified on the publisher's abstract, but the final full model body was not retrieved. The precise model revisions remain unverified. This audit therefore does not claim the final benchmark is the identical all-frictions scenario with a corrected number.

GDP, equivalent-variation welfare, and consumption-equivalent gains must remain distinct. Comparing their magnitudes can be informative if the definitions are stated. Compressing them into literal GDP without conversion is not justified. [INFERENCE]

## What the local calibration actually says

The recorded assumptions are $7,500 annual gain per additional migrant and $110T world GDP:

| Additional migrants | Annual gain | World-GDP share |
|---|---:|---:|
| 200M | $1.5T | 1.36% |
| 500M | $3.75T | 3.41% |
| 1B | $7.5T | 6.82% |
| 3B | $22.5T | **20.45%** |

[CALCULATION: migrants × $7,500; divide by $110T]

The calculation has been recomputed. It does not yield doubling at 3B; that would require 14.67B additional migrants if this gain were held fixed. Nor is the conservative constant an independent empirical bound on other models' endogenous gains. The underlying scripts and data paths cited in the original analysis are absent from this checkout, so this repair reproduces the stated arithmetic, not the original generator or data provenance. [CALCULATION] [INFERENCE]

## What the housing comparison does and does not establish

At 2.5 people per unit, 200M migrants require 80M units. Over 30 years this is 2.67M units annually, about 1.90 times the recorded 1.4M **US** annual starts. This is a US comparator for a **multi-country** migration scenario, not total destination capacity. The five-year “binds in year 1” calculation additionally assumes a particular arrival schedule and unchanged construction. [CALCULATION; SOURCE: immigration-open-borders-break-even-bounds-2026-04-22.md]

A credible transition analysis must allocate migrants across destinations and estimate construction, existing demand, vacancies, household formation, financing, and adjustment. The old comparison supplies none of those jointly. Short-run congestion can reduce or delay gains; it does not by itself disprove a long-run result. Conversely, eventual capital adjustment is not evidence that transition costs are zero. [INFERENCE]

The recorded correlation between immigrant shares and housing inelasticity is a sorting-confounded cross-sectional association. It cannot distinguish a world of small long-run gains from one of large gains realized after investment and geographic adjustment. Treating that correlation as confirmation of the low-gains hypothesis was not a valid discriminating test. [INFERENCE]

## Limits on the earlier causal argument

The earlier 0.20/0.65/0.15 hypothesis probabilities and specificity scores were subjective judgments, not calibrated posteriors or a statistical test. They are withdrawn as quantitative evidence. No likelihood, mutually exclusive model class, or out-of-sample validation was provided. [INFERENCE; historical values retained below]

A statistically insignificant local E-Verify or sanctuary coefficient also does not prove no economically meaningful wage response, no native gains, or the absence of task complementarity. These interventions and their first stages are different from global migration liberalization. The scope of each estimand and its uncertainty must be retained. [INFERENCE]

A meaningful update would compare models on matched policy, horizon, destinations, welfare definition, and migration response, and test their transition predictions. The present evidence shows sensitivity, not a measured single-digit ceiling. [INFERENCE]

## The apartheid analogy

The analogy raises a normative comparison about exclusion based on birthplace and an institutional comparison with a specific historical regime. Those are separate from the GDP calculation. Neither moral agreement with the analogy nor disagreement about institutional similarity identifies the economic gains, costs, or feasible migration path. The earlier claims about what the analogy “moralizes away” are framing judgments, not empirical findings. [FRAMING-SENSITIVE] [INFERENCE]

## Current conclusion

Treat doubling as a conditional model-literature proposition whose applicability needs assessment. Do not present the old 4% scenario or the repo's US housing comparator as a falsification. Large gains, substantial transition costs, and uneven incidence can coexist; their magnitudes need to be estimated on the same counterfactual and horizon. [INFERENCE]

## Revisions

### 2026-09-05 — withdraw unsupported magnitude and causal closure

[Material inference repair decision](../decisions/2026-09-05-material-inference-repair.md): correct source versions and 3B arithmetic; separate geography, horizon, and welfare metrics; withdraw subjective probabilities and a non-discriminating correlation test as evidence. Historical source quotations and prose remain verbatim below.

### 2026-09-29 — remove the superseded analysis

[Cleanup decision](../decisions/2026-09-29-delete-superseded-and-cruft-docs.md): the verbatim pre-repair analysis that followed this section was removed; recover it with `git show 36c4477:research/immigration-open-borders-double-world-gdp-and-apartheid-audit-2026-04-21.md`.
