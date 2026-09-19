# Housing comparison: original specification and modern sensitivity checks

**Verdict:** Withdraw the label **exact specification reproduction** from the September19 housing lane. Its modern measurements and specification differ materially from Saiz–Wachter2011. Completed checks do not recover the old negative coefficient, but cannot establish that the historical relationship disappeared. Original-data reproduction remains pending ICPSR download-terms acceptance. No original estimation data have yet been acquired. [SOURCE: paper, online appendix, code and computed comparisons below]

## Source contract

| Component | Original source | Existing modern lane |
|---|---|---|
| Outcome and window | Log **average** value change,1980–1990/1990–2000 | ACS median values, five-year windows ending2013/2018/2023 |
| Baseline controls |44, including detailed housing quality and initial socioeconomic characteristics |12; different attributes and timing |
| Sample rule | Foreign-born stock increase at least5% of initial metro population per decade | Cutoff chosen to capture76.5% of positive growth; the paper's76.5% is an outcome of its threshold, not its rule |
| Inference | Tract clusters | CBSA clusters |
| Gravity | β=1.6; Euclidean longitude–latitude degree distances; other tracts in metro | β=1 main; haversine miles and quarter-mile floor; neighbors filtered by outcome/control validity |
| IV columns | Column5 excludes Pull and two interactions, controlling initial FB share; column6 includes Pull and excludes the interactions | Column5 form omitted from the original modern run |

All original value regressions use initial owner-unit weights and metro×period fixed effects. Table1 baselineβ=−0.246(SE0.015),N34,833; IV columns4–6 β=−0.323/−0.211/−0.214 with SE0.136/0.050/0.054. These are published targets, not newly reproduced estimates. Exact rows, first stages and rounding targets are in the [replay lane](../infra/immigration-fiscal/hedonic_replay_2026_09_19/table1_targets.json). [SOURCE: main paper pp172–179,Table1,A1; [online appendix](https://www.aeaweb.org/articles/materials/1124) §3 and Table3]

The appendix's Table2 col4 reports a median-value estimate of−0.278(SE0.057),N21,681, for1990–2000. This is evidence against explaining the historical finding solely by use of means. It is not a matched-row mean-versus-median decomposition; the appendix's printed column note is inconsistent with its header. Executable source remains the next authority for reproduction details. [SOURCE: online appendix Table2 header and body]

## Completed modern comparisons

All coefficients below are changes in log owner value per unit change in foreign-born share. Multiplyβ by0.1 for log-value change per ten-percentage-point share increase; these are conditional statistical estimates, not welfare dollars. Owner-unit weighting and modern12-control matrix are held fixed within each comparison. [CALCULATION: `src/modern_bridge.py`, `derived/modern_bridge.csv` in the replay lane]

| Comparison | Coefficient | Cluster SE | N / metro clusters |
|---|---:|---:|---:|
| Existing pooled coverage sample |+0.04589|0.01987|45,369 /133|
| Identical rows, tract clustering |+0.04589|0.01435|45,369 /30,825 **tract** clusters|
| Native-boundary periodA,2013→2018 |−0.02430|0.02712|21,765 /85|
| Ten-year2013→2023, all valid metros |−0.04393|0.02514|56,071 /377|
| Same ten-year construction, coverage cutoff |+0.02136|0.03412|25,300 /88|
| Same ten-year construction, fixed5% cutoff |+0.13612|0.07641|5,441 /13|

Clustering changes uncertainty, exactly as expected; the coefficient is invariant. The ten-year cutoff changes sample and point estimate, but does not restore the historical negative slope. With only13 clusters, the last row is a descriptive sensitivity check, not a precise causal estimate. PeriodA versus pooled differences change the era as well as crosswalk exposure; they do not isolate the crosswalk. [INFERENCE]

The gravity comparisons freeze the same21,765 periodA outcome rows. Neighbor expansion is57,348 price-valid tracts→60,414 cached tracts with usable geography and initial FB share. Each successive row below changes one instrument-construction choice; controls, treatment, outcomes, weights and clustering remain fixed. Column6-style IV includes Pull directly; only its interactions are excluded.

| Gravity construction, column6 form | β̂ | SE | Excluded-instrument F |
|---|---:|---:|---:|
| Existing neighbors, exponent1, haversine |+5.537|3.694|3.03|
| All available neighbors, exponent1 |+3.238|2.016|5.93|
| All neighbors, exponent1.6 |+2.835|1.784|7.16|
| Same, remove quarter-mile floor |+2.736|1.697|7.66|
| Same, degree-plane distance |+2.586|1.507|9.82|

These imprecise, weak-first-stage results do not yield a defensible causal valuation. The separately added **column5 form** hasβ=+0.511(SE0.373),F62.14 under the final gravity convention. Therefore “gravity has no first stage” is not a specification-general conclusion. Column5 excludes Pull itself and makes a stronger exclusion assumption than column6; a higher F does not establish that assumption. This check supplies no verified overidentification verdict. [CALCULATION; INFERENCE]

## What survives and what remains open

- **Survives:** the modern lane does not supply an identified composition-amenity dollar price. Its matched-row ACS-versus-Zillow results remain evidence of outcome sensitivity.
- **Withdraw:** “exact reproduction,” an established era change, and the explanation that declining aggregate Mexican-born counts prove local diffusion stopped. Aggregate decline alone does not rule out local redistribution. The original authors' contemporaneous mean/median and transaction-data checks also preclude dismissing their result solely with the modern ACS measurement concern. [SOURCE: main paper p172 footnote3; appendix Table2; INFERENCE]
- **Still required:** acquire the original `.dta` and author `.do`, recover Table1 on those rows, check our estimator on that identical matrix, and only then bridge original controls and outcomes. Do not substitute today's sensitivity checks for that gate.
- **Identification limit:** preferences, schools, crime, housing quality and sorting can be bundled in relative prices. Neither an unstable slope nor its absence proves zero amenity value, and relative price redistribution does not by itself settle welfare. [FRAMING-SENSITIVE]

Verification: stored modern baseline recovered within its printed precision; coefficient invariance under clustering; independent statsmodels WLS and linearmodels2SLS with explicit fixed-effect dummies agree with the custom estimator on coefficients and SEs; independent first-stage jointF agrees. Inputs and row/matrix hashes are retained in ignored derived outputs. [Reproduction instructions](../infra/immigration-fiscal/hedonic_replay_2026_09_19/README.md)

Instrument: LLM-assisted source audit, subject to the project's [bias caveat](../notes/llm-bias-caveat.md); deterministic checks verify calculation, not causal interpretation. No inference about individual preferences follows from these aggregate regressions.

## Revisions

- **2026-09-19:** [Specification-equivalence decision](../decisions/2026-09-19-require-housing-specification-equivalence.md) withdraws the earlier exact-reproduction rating while preserving its estimates. Original archive download is pending legal-terms acceptance, not evidence of failed replication or unavailable data.
